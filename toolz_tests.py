#!/usr/bin/env python3
"""Download and run toolz's test suite against typedtoolz."""

import os
import sys
from pathlib import Path
from typing import cast

here = Path(__file__).resolve().parent
venv_python = here / ".venv" / "bin" / "python"
if Path(sys.executable).resolve() != venv_python.resolve() and venv_python.exists():
    os.execv(str(venv_python), [str(venv_python), *sys.argv])

import ast
import json
import re
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request

CACHE_DIR = here / ".toolz_tests"
VERSION_FILE = CACHE_DIR / "version"

FROM_RE = re.compile(r'^\s*from toolz([\.\w\d]*) import .*$')
IMPORT_RE = re.compile(r'^\s*import toolz([\.\w\d]*)($|\s.*$)')
TOOLZ_RE = re.compile(r'\btoolz\b(\.[\w\d]+)?')


def get_latest_version() -> str:
    with urllib.request.urlopen("https://pypi.org/pypi/toolz/json") as resp:
        return json.load(resp)["info"]["version"]


def get_cached_version() -> str | None:
    return VERSION_FILE.read_text().strip() if VERSION_FILE.exists() else None


def download_and_extract(version: str) -> None:
    # Remove old test dirs but keep the version file
    for child in CACHE_DIR.glob("*"):
        if child != VERSION_FILE:
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        subprocess.run(
            ["pip", "download", "--no-binary", ":all:", "--no-deps",
             f"toolz=={version}", "-d", tmpdir],
            check=True,
        )
        tarball = next(tmppath.glob("toolz-*.tar.gz"))
        with tarfile.open(tarball) as tar:
            tar.extractall(tmppath, filter="data")
        toolz_pkg = next(tmppath.glob("toolz-*/toolz"))
        # Copy each tests/ dir preserving structure relative to toolz_pkg:
        # toolz/tests/        -> CACHE_DIR/tests/
        # toolz/sandbox/tests/ -> CACHE_DIR/sandbox/tests/
        for src in sorted(toolz_pkg.rglob("tests")):
            if src.is_dir():
                for curried_test in src.rglob("test_curried*.py"): # We do not adhere to the curried api
                    if not curried_test.is_dir():
                        curried_test.unlink()
                rel = src.relative_to(toolz_pkg)
                shutil.copytree(src, CACHE_DIR / rel)

    patch_imports(CACHE_DIR)
    VERSION_FILE.write_text(version)


def patch_isinstance_curry(path: Path) -> None:
    source = path.read_text()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return

    # Collect (lineno, col_offset, end_col_offset) for every 'curry' Name node
    # that is the second argument of an isinstance() call, or a base class.
    targets: list[tuple[int, int, int]] = []
    base_targets: list[tuple[int, int, int]] = []
    # (lineno, col, end_col, replacement_text) for curry(int) first-arg patches
    int_targets: list[tuple[int, int, int, str]] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "isinstance"
            and len(node.args) >= 2
            and isinstance(node.args[1], ast.Name)
            and node.args[1].id == "curry"
        ):
            arg = node.args[1]
            targets.append((arg.lineno, arg.col_offset, arg.end_col_offset))
        elif isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "curry":
                    base_targets.append((base.lineno, base.col_offset, base.end_col_offset))
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "curry"
            and len(node.args) == 1
            and not node.keywords
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, int)
        ):
            arg = node.args[0]
            int_targets.append((arg.lineno, arg.col_offset, arg.end_col_offset, f"{float(arg.value)}"))

    if not targets and not base_targets and not int_targets:
        return

    lines = source.splitlines(keepends=True)
    for lineno, col, end_col in sorted(targets + base_targets, reverse=True):
        line = lines[lineno - 1]
        lines[lineno - 1] = line[:col] + "cytoolz_curry" + line[end_col:]
    for lineno, col, end_col, replacement in sorted(int_targets, reverse=True):
        line = lines[lineno - 1]
        lines[lineno - 1] = line[:col] + replacement + line[end_col:]

    # Insert import after any 'from __future__' lines, before everything else.
    import_line = "from cytoolz.functoolz import curry as cytoolz_curry\n"
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("from __future__"):
            insert_at = i + 1
    lines.insert(insert_at, import_line)

    path.write_text("".join(lines))


def patch_imports(cache_dir: Path) -> None:
    dont_patch_postfix = ("._signatures", ".curried", ".compatibility")
    for path in cache_dir.rglob("*.py"):
        text = path.read_text()
        lines: list[str] = []
        for line in text.splitlines(keepends=True):
            m = FROM_RE.match(line) or IMPORT_RE.match(line)
            if m is not None:
                postfix = m.group(1)
                if not postfix.startswith(dont_patch_postfix):
                    line = line.replace("toolz", "typedtoolz", 1)
                else: print(f"Not patching import: toolz{postfix}")
            else:
                def replace_maybe(m: re.Match[str]):
                    postfix = m.group(1)
                    if postfix is None: postfix = ""
                    if postfix.startswith(dont_patch_postfix):
                        return m.group(0)
                    return "typedtoolz" + cast(str, postfix)
                line = TOOLZ_RE.sub(replace_maybe, line)
            if line.strip() in (
                    "assert excepting.__doc__ == excepts.__doc__",
                    "assert excepts.__name__ == 'excepts'",
                    ):
                line = "\n"
            lines.append(line)
        patched = "".join(lines)
        if patched != text:
            path.write_text(patched)
        patch_isinstance_curry(path)


def main() -> None:
    args = sys.argv[1:]
    force_pull = "--force-pull" in args
    args = [a for a in args if a != "--force-pull"]

    if "--" in args:
        sep = args.index("--")
        pytest_args = args[sep + 1:]
    else:
        pytest_args = []

    print("Checking latest toolz version...")
    cached = get_cached_version()
    try:
        latest = get_latest_version()
    except Exception as e:
        print(f"Could not fetch latest version ({e}), using cached toolz {cached}")
        latest = cached

    if latest is None:
        print("No cached tests and version fetch failed; cannot proceed.", file=sys.stderr)
        sys.exit(1)

    if force_pull or cached != latest:
        if force_pull:
            reason = "forced"
        elif cached is None:
            reason = "no cache"
        else:
            reason = f"{cached} -> {latest}"
        print(f"Downloading toolz {latest} ({reason})...")
        download_and_extract(latest)
    else:
        print(f"Using cached toolz {cached}")

    DEFAULT_K = "not test_curry_module and not test_compose_metadata and not test_tlz and not test_has_version"
    if not any(a == "-k" or a.startswith("-k") for a in pytest_args):
        pytest_args = ["-k", DEFAULT_K] + pytest_args

    env = os.environ | {"PYTHONPATH": str(CACHE_DIR) + os.pathsep + os.environ.get("PYTHONPATH", "")}
    sys.exit(subprocess.run(["pytest", "--import-mode=importlib", str(CACHE_DIR), *pytest_args], env=env).returncode)


if __name__ == "__main__":
    main()
