# LGIC_ENFORCE.TO-EN-g-1 -- the commit limb: result and session log

Worker `0.9.0_WK_LGIC_ENFORCE~2`, branch `wk-lgic-enforce-1-2-g1`, cut from CLOUD @1ca17cc88e. Everything here is LOCAL on that branch (never pushed).

## The bar

- `git rev-parse --abbrev-ref HEAD` -> `wk-lgic-enforce-1-2-g1`; `test -d org && test -d .tools` -> `TREE-OK`.
- The paths the order names exist at the base: `lib/opal_naming.py`, `.tools/safe-commit.sh` (1100 lines), the five registry files, `check_en.py`, the 10 g1 fixture diffs and the 2 pre-images (both tracked at HEAD).

## Premises re-grounded

- `.tools/naming-gate.py` and `org/mcp/naming-gate.enforce` were absent at the base. `org/mcp/naming-gate-verdicts.log` is gitignored (`.gitignore:68 *.log`).
- The stage placement: the commit-gate call was at `safe-commit.sh:652` and the to-pipeline call at `:688`. The order's `:686` is the `if` line guarding that call, two lines above it.
- Negative arm, before the build: `g1-refuse-key` FAIL-NOT-REFUSED, `g1-stage` FAIL-STAGE-ORDER, `g1-shipped-warn` FAIL-ENFORCE-SHIPPED, `g1-warn-mode` FAIL-WARN-MODE (4 of 4 sampled FAIL).
- `grade()` on the fixture strings, before the gate existed: `mdpf-cottonwood-publisher-role` IAM_ROLE -> ALIAS `mdpf-cot-publisher-role`; `opal-data-inf/silver/positions/` S3Key -> OUT-OF-PATTERN `{source}/inflection/silver/positions/`; `opal-data-inf` S3_BUCKET -> ALIAS `opal-data-inflection`; `cottonwood-publisher-lambda` LAMBDA -> OUT-OF-PATTERN `{system}-cot-publisher-lambda`.

## What was built

`.tools/naming-gate.py` (new; final bytes at 8a60d8e74e):
- It parses a unified diff and fails with `NAMING ERROR` on anything else.
- It reads each pre-image with `git show HEAD:<path>` (none for `--- /dev/null`), and builds the post-image by applying the hunks. `--post-from-index` reads the post-image from the index instead; it is added for safe-commit, and the checker never passes it.
- It grades the string literals on ADDED lines only. Python strings come from the syntax tree; JS/TS, Terraform, JSON and YAML strings come from a comment-aware scanner.
- Terraform strings carry their block context: block labels are dropped; strings in an `opal_name` module block are permitted; a resource's own-name attribute gives the node type, with the same Terraform-type map as the EN-t-1 census.
- DEC-6's matrix is applied as the order writes it. The generated-file check runs `lib/opal_naming.py generate()` on the post-image and compares. It also refuses the mark on a file the generator does not produce. The mark is matched with its 16 hex, so the prose `<16 hex>` in `lib/opal_naming.py`'s docstring is not a mark.
- Verdict lines are appended to `org/mcp/naming-gate-verdicts.log`, each prefixed with a UTC stamp, the serial and the mode.

`.tools/safe-commit.sh`: ONE new stage (43 lines, commit 02d2869cf0) between the commit-gate stage and the to-pipeline stage, over the staged `.py .js .mjs .ts .tf .json .yaml .yml` files.
- It decides ENFORCE itself: `NAMING_GATE_ENFORCE=1`, or `org/mcp/naming-gate.enforce` present.
- In WARN mode it prints the gate's output and never touches the exit code, whatever the gate returns, including on a crash.
- In ENFORCE mode a non-zero gate exit unstages the files and exits 1, like the commit-gate above it.
- `org/mcp/naming-gate.enforce` stays ABSENT and untracked.

## Criteria (after the final gate bytes, 8a60d8e74e)

| id | subcommand | VERDICT | rc |
|---|---|---|---|
| G1-AC1 | g1-refuse-key | PASS-REFUSED-WITH-CANONICAL | 0 |
| G1-AC2 | g1-pass-builder-key | PASS-CANONICAL-PASSES | 0 |
| G1-AC3 | g1-alias-warn | PASS-ALIAS-WARNED | 0 |
| G1-AC4 | g1-refuse-carrier | PASS-CARRIER-REFUSED | 0 |
| G1-AC5 | g1-pass-lookup | PASS-LOOKUP-PASSES | 0 |
| G1-AC6 | g1-refuse-name | PASS-NAME-REFUSED | 0 |
| G1-AC7 | g1-pass-name-builder | PASS-BUILDER-PASSES | 0 |
| G1-AC8 | g1-pass-key-scope | PASS-LONG-FORM-IN-KEY-PASSES | 0 |
| G1-AC9 | g1-refuse-generated | PASS-GENERATED-EDIT-REFUSED | 0 |
| G1-AC10 | g1-warn-mode | PASS-WARN-EXIT-0 | 0 |
| G1-AC11 | g1-error-nonblocking | PASS-ERROR-NONBLOCKING | 0 |
| G1-AC12 | g1-logged | PASS-LOGGED | 0 |
| G1-AC13 | g1-stage | PASS-STAGE-PLACED | 0 |
| G1-AC14 | g1-shipped-warn | PASS-SHIPPED-WARN | 0 |

14 of 14 mechanical criteria PASS by output. No criterion is `judgment="true"`. The full battery was run twice: first on the 02d2869cf0 bytes (14 of 14 PASS), then after the classifier fix (14 of 14 PASS).

## Controls

- **The live WARN window, exercised on this order's own commits.**
  - Commit 02d2869cf0: the new stage graded its own file and printed `NAMING-GATE: WARN 9 graded` (5 REFUSE, 4 RAISE). The line under it read `(WARN window: 5 REFUSE verdict(s) did not block ...)`, and safe-commit returned rc=0.
  - All 9 verdicts were false positives in the gate's own source:
    - node-type constants read as resource names (`LAMBDA_LAYER`, `S3_BUCKET_POLICY`);
    - bare prefixes (`opal-data-`, `/aws/`);
    - one literal refused token of the file's own.
  - They were fixed in 8a60d8e74e. After the fix the same self-grade reads `NAMING-GATE: PASS 0 graded`, and the stage on 8a60d8e74e printed `NAMING-GATE: PASS 0 graded`.
- **Discrimination (mutant) -- the same strings, only the context changed:**
  - The fixture-02 strings in a tuple instead of `key()` -> `NAMING REFUSE ... inflection -> lookup('inflection')`, rc=1 (fixture 02 itself: PASS, rc=0).
  - The fixture-03 alias in a NEW file -> `NAMING REFUSE ... mdpf-cottonwood-publisher-role -> mdpf-cot-publisher-role`, rc=1 (fixture 03, EXISTING: ALIAS, rc=0).
- **Generated-file controls on the two live generated carriers** (`.tools/ds-precommit-check.py`, `data/assets/scripts/gold/runners_49f/perfrp_firm_pin.py`): a same-bytes touch inside the generated block -> `NAMING-GATE: PASS 0 graded` rc=0; a hand edit there -> `NAMING REFUSE ... <generated-file-edit> -> python lib/opal_naming.py generate --out <dir> --target <path>` rc=1, on both.
- **Determinism:** two runs of the gate on fixture 04 with `--enforce` were byte-identical at 472 bytes (cmp rc=0).

## Rows filed

- `LGIC_ENFORCE-W2-S5` (OBSERVATION, INERT). A product token is matched as the whole string, not as a whole segment. mdpf and etfs are also systems.json keys, which `name()` writes in the system slot. Arguments of `float()` are exempt, because `lookup('inf')` is the inflection row.
- `LGIC_ENFORCE-W2-S6` (OBSERVATION, INERT). The line verdict for a bare hand-kept carrier (OUT-OF-PATTERN) and for a RaiseDefect (RAISE) falls outside the order's "the grade, or REFUSE".

## Limits

- **The ENFORCE branch of the shell stage** is not exercised end to end. Doing so would need a commit carrying a refused literal outside this order's grant, with the enforce state switched on. The branch reads the same gate exit code the checker exercises under `--enforce` (G1-AC1, AC4, AC6, AC9: rc=1). Its unstage-and-exit lines copy the commit-gate stage above it.
- **The literal scanners are readers, not parsers**, except Python's syntax tree. For JS/TS, a regex literal holding a quote can mis-scan that one line. A YAML value is read per added line.
- **"EXISTING" is a whole-token search of the pre-image text**, so a string that appears only in a comment of the pre-image counts as EXISTING.
- **The generated-file check needs the registry to validate.** When the generator cannot run, the file is reported RAISE (a registry defect), never REFUSE.

## Commits (LOCAL on wk-lgic-enforce-1-2-g1)

- 02d2869cf0 -- the gate and the safe-commit stage.
- 8a60d8e74e -- the classifier precision fix; rows W2-S5 and W2-S6.
- The proof instance, this file and the `complete` flip ride the next commit.
