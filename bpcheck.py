#!/usr/bin/env python3
"""
Run basedpyright and filter warnings, fixing the bug where
# pyright: ignore[reportUnnecessaryTypeIgnoreComment] doesn't suppress
reportUnnecessaryTypeIgnoreComment warnings on the same line.
"""

import os
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
venv_python = here / ".venv" / "bin" / "python"

if Path(sys.executable).resolve() != venv_python.resolve() and venv_python.exists():
    os.execv(str(venv_python), [str(venv_python), *sys.argv])

import json
import subprocess
import re

SELF_IGNORE_MSG = re.compile(r'^Unnecessary.*"reportUnnecessaryTypeIgnoreComment"$')
RULE = "reportUnnecessaryTypeIgnoreComment"


def load_config() -> dict:
    config_path = here / "bpcheck.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def matches_ignore(diag: dict, ignore_rules: list) -> bool:
    for entry in ignore_rules:
        match_type, rule, message = entry
        if match_type == "exactly":
            if diag.get("rule") == rule and diag.get("message") == message:
                return True
    return False


def main() -> None:
    args = sys.argv[1:]
    if "--level" not in args:
        args = ["--level", "warning"] + args
    # --outputjson must come last and always be present
    args = [a for a in args if a != "--outputjson"] + ["--outputjson"]
    result = subprocess.run(
        ["basedpyright", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(result.stdout, end="")
        sys.exit(result.returncode)

    diagnostics: list[dict] = data.get("generalDiagnostics", [])
    config = load_config()
    ignore_rules: list = config.get("ignoreMessages", [])

    # Build set of (file, line) that have the self-referential ignore comment warning.
    # Presence of this warning means the user put # pyright: ignore[reportUnnecessaryTypeIgnoreComment]
    # on that line, so all reportUnnecessaryTypeIgnoreComment warnings there should be suppressed.
    suppressed_locations: set[tuple[str, int]] = set()
    for diag in diagnostics:
        if "range" not in diag:
            continue
        if diag.get("rule") == RULE and "message" in diag and SELF_IGNORE_MSG.fullmatch(diag["message"]):
            file = diag["file"]
            line = diag["range"]["start"]["line"]
            suppressed_locations.add((file, line))

    after_self_ignore = [
        diag for diag in diagnostics
        if not (
            diag.get("rule") == RULE
            and "range" in diag
            and (diag["file"], diag["range"]["start"]["line"]) in suppressed_locations
        )
    ]

    filtered = [diag for diag in after_self_ignore if not matches_ignore(diag, ignore_rules)]

    for diag in filtered:
        file = diag["file"]
        severity = diag.get("severity", "warning")
        message = diag["message"].replace("\n", " ")
        rule = diag.get("rule", "")
        rule_str = f" ({rule})" if rule else ""
        if "range" in diag:
            line = diag["range"]["start"]["line"] + 1  # convert 0-indexed to 1-indexed
            col = diag["range"]["start"]["character"] + 1
            print(f"{file}:{line}:{col}: {severity}: {message}{rule_str}")
        else:
            print(f"{file}: {severity}: {message}{rule_str}")

    total = len(diagnostics)
    shown = len(filtered)
    self_ignore_suppressed = total - len(after_self_ignore)
    config_suppressed = len(after_self_ignore) - shown
    summary_parts = [f"{shown} warning(s) shown"]
    if self_ignore_suppressed:
        summary_parts.append(f"{self_ignore_suppressed} suppressed by reportUnnecessaryTypeIgnoreComment fix")
    if config_suppressed:
        summary_parts.append(f"{config_suppressed} suppressed by bpcheck.json")
    print(f"\n{', '.join(summary_parts)}")

    sys.exit(0 if not filtered else 1)


if __name__ == "__main__":
    main()
