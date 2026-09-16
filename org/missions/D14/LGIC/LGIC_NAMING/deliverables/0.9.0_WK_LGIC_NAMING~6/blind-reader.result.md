# LGIC_NAMING.TO-LN-e-4 -- blind reader -- result

**Worker:** 0.9.0_WK_LGIC_NAMING~6 | **Branch:** wk-lgic-naming-1-6 | **Base:** 64dd54e67f (HEAD before this worker's commit)

**Input read:** column 2 of `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n3-namer-a.tsv` only (`cut -f2`), 18 names after the `# base` line, taken in byte-sorted ascending order. The marks were written before any other project file was opened. `check_ln.py` was run, not read.

**Output:** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n3-reader.tsv` -- 18 of 18 names marked, 0 `none`.

## Marking rule the reader applied (read from the names alone)

- A token that recurs in the second segment under several different leading tokens (`49f`, `cot`, `inf`), or its long form in the same slot (`49financial`, `inflection`), or as the owner suffix (`cottonwood` in `opal-data-cottonwood`), was read as the FIRM and marked when present.
- Otherwise the recurring leading product token was marked (`mdpf`, `etfs`); in `pathfinder-etfs-ingest-task` the first token was read as a source system like `schwab`/`orion`/`smartx`, and `etfs` as the product.
- `demo` in `mdpf-demo-publish-failure-alarm` sits in the slot where its `mdpf` siblings carry the firm, and is marked as that tenant: the reader's weakest mark.

## Criteria (mechanical; graded by the checker's output)

| id | invocation | deciding output | rc |
|---|---|---|---|
| E4-AC1 | `timeout 120 python .../fixed_inputs/check_ln.py e4-marked` | `NAMES: 18  MARKED: 18  MISSING: 0` / `VERDICT: PASS-ALL-MARKED` | 0 |

Controls: one mark blanked -> `MARKED: 17  MISSING: 1` / `VERDICT: FAIL-UNMARKED` (the checker's rc is 0 on that path too; the VERDICT line is the discriminator), file restored cmp-identical; re-run on the restored file -> PASS again.

## Rows

- `LGIC_NAMING-W6-S1` -- the reader was not blind: CLAUDE.md and the auto-memory, loaded before any tool call, name the firm tokens (ARMED, disarm 2.0.0_SA_COO~G).
- `LGIC_NAMING-W6-S2` -- a name carrying both a product and a firm token has two candidate marks; the reader took firm over product (INERT).
- `LGIC_NAMING-W6-S3` -- appending a row needs a read of the channel, which quotes the items; marks were fixed first (INERT).

Whether the marks match the key is not this cell's criterion; the reader did not open `N3_KEY.json`.
