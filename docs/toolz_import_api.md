# toolz / cytoolz Import API

Each row is one named export. Columns list full import paths by availability:

- **left** — toolz-only paths (no cytoolz mirror at that path)
- **middle** — paths shared by both: `toolz.X / cytoolz.X`
- **right** — cytoolz-only paths (no toolz mirror at that path)

`i:` prefix = incidental export (submodule object, stdlib ref, etc.)

---

| toolz only                                                              | shared                                                                                                                 | cytoolz only                 |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| `toolz.sandbox.EqualityHashKey`<br>`toolz.sandbox.core.EqualityHashKey` |                                                                                                                        |                              |
|                                                                         | `i:toolz.curried / i:cytoolz.curried`                                                                                  |                              |
|                                                                         | `i:toolz.dicttoolz / i:cytoolz.dicttoolz`                                                                              |                              |
|                                                                         | `i:toolz.functoolz / i:cytoolz.functoolz`                                                                              |                              |
|                                                                         | `i:toolz.itertoolz / i:cytoolz.itertoolz`                                                                              |                              |
|                                                                         | `i:toolz.recipes / i:cytoolz.recipes`                                                                                  |                              |
|                                                                         | `i:toolz.utils / i:cytoolz.utils`                                                                                      |                              |
| `i:toolz.sandbox`                                                       |                                                                                                                        |                              |
| `i:toolz.sandbox.core`                                                  |                                                                                                                        |                              |
| `i:toolz.sandbox.parallel`                                              |                                                                                                                        |                              |
| `i:toolz.sandbox.parallel.functools`                                    |                                                                                                                        |                              |
|                                                                         | `toolz.accumulate / cytoolz.accumulate`<br>`toolz.itertoolz.accumulate / cytoolz.itertoolz.accumulate`                 |                              |
|                                                                         | `toolz.apply / cytoolz.apply`<br>`toolz.functoolz.apply / cytoolz.functoolz.apply`                                     |                              |
|                                                                         | `toolz.assoc / cytoolz.assoc`<br>`toolz.dicttoolz.assoc / cytoolz.dicttoolz.assoc`                                     |                              |
|                                                                         | `toolz.assoc_in / cytoolz.assoc_in`<br>`toolz.dicttoolz.assoc_in / cytoolz.dicttoolz.assoc_in`                         |                              |
|                                                                         | `toolz.comp / cytoolz.comp`                                                                                            |                              |
|                                                                         | `toolz.complement / cytoolz.complement`<br>`toolz.functoolz.complement / cytoolz.functoolz.complement`                 |                              |
|                                                                         | `toolz.compose / cytoolz.compose`<br>`toolz.functoolz.compose / cytoolz.functoolz.compose`                             |                              |
|                                                                         | `toolz.compose_left / cytoolz.compose_left`<br>`toolz.functoolz.compose_left / cytoolz.functoolz.compose_left`         |                              |
|                                                                         | `toolz.concat / cytoolz.concat`<br>`toolz.itertoolz.concat / cytoolz.itertoolz.concat`                                 |                              |
|                                                                         | `toolz.concatv / cytoolz.concatv`<br>`toolz.itertoolz.concatv / cytoolz.itertoolz.concatv`                             |                              |
| `i:toolz.sandbox.core.cons`                                             | `toolz.cons / cytoolz.cons`<br>`toolz.itertoolz.cons / cytoolz.itertoolz.cons`                                         |                              |
|                                                                         |                                                                                                                        | `cytoolz.utils.consume`      |
|                                                                         | `toolz.count / cytoolz.count`<br>`toolz.itertoolz.count / cytoolz.itertoolz.count`                                     |                              |
|                                                                         | `toolz.countby / cytoolz.countby`<br>`toolz.recipes.countby / cytoolz.recipes.countby`                                 |                              |
|                                                                         | `toolz.curry / cytoolz.curry`<br>`toolz.functoolz.curry / cytoolz.functoolz.curry`                                     |                              |
|                                                                         | `toolz.diff / cytoolz.diff`<br>`toolz.itertoolz.diff / cytoolz.itertoolz.diff`                                         |                              |
|                                                                         | `toolz.dissoc / cytoolz.dissoc`<br>`toolz.dicttoolz.dissoc / cytoolz.dicttoolz.dissoc`                                 |                              |
|                                                                         | `toolz.do / cytoolz.do`<br>`toolz.functoolz.do / cytoolz.functoolz.do`                                                 |                              |
|                                                                         | `toolz.drop / cytoolz.drop`<br>`toolz.itertoolz.drop / cytoolz.itertoolz.drop`                                         |                              |
|                                                                         | `toolz.excepts / cytoolz.excepts`<br>`toolz.functoolz.excepts / cytoolz.functoolz.excepts`                             |                              |
|                                                                         | `toolz.filter / cytoolz.filter`                                                                                        |                              |
|                                                                         | `toolz.first / cytoolz.first`<br>`toolz.itertoolz.first / cytoolz.itertoolz.first`                                     |                              |
|                                                                         | `toolz.flip / cytoolz.flip`<br>`toolz.functoolz.flip / cytoolz.functoolz.flip`                                         |                              |
| `toolz.sandbox.fold`<br>`toolz.sandbox.parallel.fold`                   |                                                                                                                        |                              |
|                                                                         | `toolz.frequencies / cytoolz.frequencies`<br>`toolz.itertoolz.frequencies / cytoolz.itertoolz.frequencies`             |                              |
|                                                                         | `toolz.get / cytoolz.get`<br>`toolz.itertoolz.get / cytoolz.itertoolz.get`                                             |                              |
|                                                                         | `toolz.get_in / cytoolz.get_in`<br>`toolz.dicttoolz.get_in / cytoolz.dicttoolz.get_in`                                 |                              |
| `i:toolz.sandbox.core.getter`                                           |                                                                                                                        |                              |
|                                                                         | `toolz.groupby / cytoolz.groupby`<br>`toolz.itertoolz.groupby / cytoolz.itertoolz.groupby`                             |                              |
|                                                                         | `toolz.identity / cytoolz.identity`<br>`toolz.functoolz.identity / cytoolz.functoolz.identity`                         |                              |
|                                                                         |                                                                                                                        | `cytoolz.utils.include_dirs` |
|                                                                         | `toolz.interleave / cytoolz.interleave`<br>`toolz.itertoolz.interleave / cytoolz.itertoolz.interleave`                 |                              |
|                                                                         | `toolz.interpose / cytoolz.interpose`<br>`toolz.itertoolz.interpose / cytoolz.itertoolz.interpose`                     |                              |
|                                                                         | `toolz.isdistinct / cytoolz.isdistinct`<br>`toolz.itertoolz.isdistinct / cytoolz.itertoolz.isdistinct`                 |                              |
|                                                                         | `toolz.isiterable / cytoolz.isiterable`<br>`toolz.itertoolz.isiterable / cytoolz.itertoolz.isiterable`                 |                              |
|                                                                         | `toolz.itemfilter / cytoolz.itemfilter`<br>`toolz.dicttoolz.itemfilter / cytoolz.dicttoolz.itemfilter`                 |                              |
|                                                                         | `toolz.itemmap / cytoolz.itemmap`<br>`toolz.dicttoolz.itemmap / cytoolz.dicttoolz.itemmap`                             |                              |
|                                                                         | `toolz.iterate / cytoolz.iterate`<br>`toolz.itertoolz.iterate / cytoolz.itertoolz.iterate`                             |                              |
|                                                                         | `toolz.join / cytoolz.join`<br>`toolz.itertoolz.join / cytoolz.itertoolz.join`                                         |                              |
|                                                                         | `toolz.juxt / cytoolz.juxt`<br>`toolz.functoolz.juxt / cytoolz.functoolz.juxt`                                         |                              |
|                                                                         | `toolz.keyfilter / cytoolz.keyfilter`<br>`toolz.dicttoolz.keyfilter / cytoolz.dicttoolz.keyfilter`                     |                              |
|                                                                         | `toolz.keymap / cytoolz.keymap`<br>`toolz.dicttoolz.keymap / cytoolz.dicttoolz.keymap`                                 |                              |
|                                                                         | `toolz.last / cytoolz.last`<br>`toolz.itertoolz.last / cytoolz.itertoolz.last`                                         |                              |
|                                                                         | `toolz.map / cytoolz.map`                                                                                              |                              |
|                                                                         | `toolz.mapcat / cytoolz.mapcat`<br>`toolz.itertoolz.mapcat / cytoolz.itertoolz.mapcat`                                 |                              |
|                                                                         | `toolz.memoize / cytoolz.memoize`<br>`toolz.functoolz.memoize / cytoolz.functoolz.memoize`                             |                              |
|                                                                         | `toolz.merge / cytoolz.merge`<br>`toolz.dicttoolz.merge / cytoolz.dicttoolz.merge`                                     |                              |
|                                                                         | `toolz.merge_sorted / cytoolz.merge_sorted`<br>`toolz.itertoolz.merge_sorted / cytoolz.itertoolz.merge_sorted`         |                              |
|                                                                         | `toolz.merge_with / cytoolz.merge_with`<br>`toolz.dicttoolz.merge_with / cytoolz.dicttoolz.merge_with`                 |                              |
| `i:toolz.sandbox.parallel.no_default`                                   | `toolz.utils.no_default / cytoolz.utils.no_default`                                                                    |                              |
|                                                                         | `toolz.nth / cytoolz.nth`<br>`toolz.itertoolz.nth / cytoolz.itertoolz.nth`                                             |                              |
|                                                                         | `toolz.partial / cytoolz.partial`                                                                                      |                              |
|                                                                         | `toolz.partition / cytoolz.partition`<br>`toolz.itertoolz.partition / cytoolz.itertoolz.partition`                     |                              |
| `i:toolz.sandbox.parallel.partition_all`                                | `toolz.partition_all / cytoolz.partition_all`<br>`toolz.itertoolz.partition_all / cytoolz.itertoolz.partition_all`     |                              |
|                                                                         | `toolz.partitionby / cytoolz.partitionby`<br>`toolz.recipes.partitionby / cytoolz.recipes.partitionby`                 |                              |
|                                                                         | `toolz.peek / cytoolz.peek`<br>`toolz.itertoolz.peek / cytoolz.itertoolz.peek`                                         |                              |
|                                                                         | `toolz.peekn / cytoolz.peekn`<br>`toolz.itertoolz.peekn / cytoolz.itertoolz.peekn`                                     |                              |
|                                                                         | `toolz.pipe / cytoolz.pipe`<br>`toolz.functoolz.pipe / cytoolz.functoolz.pipe`                                         |                              |
| `i:toolz.sandbox.core.pluck`                                            | `toolz.pluck / cytoolz.pluck`<br>`toolz.itertoolz.pluck / cytoolz.itertoolz.pluck`                                     |                              |
|                                                                         | `toolz.utils.raises / cytoolz.utils.raises`                                                                            |                              |
|                                                                         | `toolz.random_sample / cytoolz.random_sample`<br>`toolz.itertoolz.random_sample / cytoolz.itertoolz.random_sample`     |                              |
|                                                                         | `toolz.reduce / cytoolz.reduce`                                                                                        |                              |
|                                                                         | `toolz.reduceby / cytoolz.reduceby`<br>`toolz.itertoolz.reduceby / cytoolz.itertoolz.reduceby`                         |                              |
|                                                                         | `toolz.remove / cytoolz.remove`<br>`toolz.itertoolz.remove / cytoolz.itertoolz.remove`                                 |                              |
|                                                                         | `toolz.second / cytoolz.second`<br>`toolz.itertoolz.second / cytoolz.itertoolz.second`                                 |                              |
|                                                                         | `toolz.sliding_window / cytoolz.sliding_window`<br>`toolz.itertoolz.sliding_window / cytoolz.itertoolz.sliding_window` |                              |
|                                                                         | `toolz.sorted / cytoolz.sorted`                                                                                        |                              |
| `i:toolz.sandbox.core.starmap`                                          |                                                                                                                        |                              |
|                                                                         | `toolz.tail / cytoolz.tail`<br>`toolz.itertoolz.tail / cytoolz.itertoolz.tail`                                         |                              |
|                                                                         | `toolz.take / cytoolz.take`<br>`toolz.itertoolz.take / cytoolz.itertoolz.take`                                         |                              |
|                                                                         | `toolz.take_nth / cytoolz.take_nth`<br>`toolz.itertoolz.take_nth / cytoolz.itertoolz.take_nth`                         |                              |
| `i:toolz.sandbox.core.tee`                                              |                                                                                                                        |                              |
|                                                                         | `toolz.thread_first / cytoolz.thread_first`<br>`toolz.functoolz.thread_first / cytoolz.functoolz.thread_first`         |                              |
|                                                                         | `toolz.thread_last / cytoolz.thread_last`<br>`toolz.functoolz.thread_last / cytoolz.functoolz.thread_last`             |                              |
|                                                                         | `toolz.topk / cytoolz.topk`<br>`toolz.itertoolz.topk / cytoolz.itertoolz.topk`                                         |                              |
|                                                                         | `toolz.unique / cytoolz.unique`<br>`toolz.itertoolz.unique / cytoolz.itertoolz.unique`                                 |                              |
| `toolz.sandbox.unzip`<br>`toolz.sandbox.core.unzip`                     |                                                                                                                        |                              |
|                                                                         | `toolz.update_in / cytoolz.update_in`<br>`toolz.dicttoolz.update_in / cytoolz.dicttoolz.update_in`                     |                              |
|                                                                         | `toolz.valfilter / cytoolz.valfilter`<br>`toolz.dicttoolz.valfilter / cytoolz.dicttoolz.valfilter`                     |                              |
|                                                                         | `toolz.valmap / cytoolz.valmap`<br>`toolz.dicttoolz.valmap / cytoolz.dicttoolz.valmap`                                 |                              |

---

## typedtoolz diff

Comparison of typedtoolz's import API against the combined middle and left columns of the table above (i.e. the full toolz import surface). `i:` = incidental. `definition moved` shows the primary non-`_` module of origin → destination. Absent means the it does not exist at all.

| `export`          | `new in typedtoolz`                                                        | `definition moved`                                  | `not in typedtoolz`                      | `absent` |
| ----------------- | -------------------------------------------------------------------------- | --------------------------------------------------- | ---------------------------------------- | -------- |
| `cons`            |                                                                            |                                                     | `i:toolz.sandbox.core.cons`              |          |
| `excepts`         | `typedtoolz.functoolz.exceptions.excepts`                                  | `toolz.functoolz → typedtoolz.functoolz.exceptions` |                                          |          |
| `getter`          |                                                                            |                                                     | `i:toolz.sandbox.core.getter`            | x        |
| `map`             | `typedtoolz.itertoolz.map`                                                 | `builtins → typedtoolz.itertoolz`                   |                                          |          |
| `no_default`      | `i:typedtoolz.functoolz.no_default`<br>`i:typedtoolz.itertoolz.no_default` |                                                     | `i:toolz.sandbox.parallel.no_default`    |          |
| `partial`         | `typedtoolz.functoolz.partial`                                             | `functools → typedtoolz.functoolz`                  |                                          |          |
| `partition_all`   |                                                                            |                                                     | `i:toolz.sandbox.parallel.partition_all` |          |
| `pluck`           |                                                                            |                                                     | `i:toolz.sandbox.core.pluck`             |          |
| `reduce`          | `typedtoolz.functoolz.reduce`                                              | `functools → typedtoolz.functoolz`                  |                                          |          |
| `starmap`         |                                                                            |                                                     | `i:toolz.sandbox.core.starmap`           | x        |
| `tee`             |                                                                            |                                                     | `i:toolz.sandbox.core.tee`               | x        |
| `zip`             |                                                                            |                                                     |                                          | x        |
| `zip_longest`     |                                                                            |                                                     |                                          | x        |
