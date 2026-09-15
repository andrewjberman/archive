# LGIC_ENFORCE.TO-EN-r-5-r2 -- the gateway registration, whole: result

Worker `0.9.0_WK_LGIC_ENFORCE~6`, worktree `.worktrees/wk-lgic-enforce-2-6` (branch `wk-lgic-enforce-2-6`,
spawn base `671925aecc` = `git merge-base HEAD CLOUD`). Cell `EN-r-5`, decomposition v2.1 @8e0d09e418 s.0b.

## What landed

Commit `c19dcc8147` carries 12 paths, 38 insertions and 29 deletions, the same `--stat` as the issuer's patch:

| Part | Path | Change |
|---|---|---|
| 1 | `infra/logic/registry/systems.json` | row `gateway`: class `PLATFORM_SUBSYSTEM`, owner `D9`, `owner_claim` measured, with the patch's basis; `_about.platform_subsystems` names gateway |
| 2 | `lib/opal_naming.py` | `_VECTOR_SHAPES`: `("opal", "gateway", None, "lb")` -> `("opal", "ingress", None, "lb")` |
| 3 | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md` | the `opal-gateway` LOAD_BALANCER case: canonical `opal-gateway-lb` -> `gateway-lb`, with the patch's why |
| 4 | 7 DEC-5 carriers, `generated_locals.tf`, `tests/vectors.json` | registry stamp `ba5318901b937130` -> `0f9240483015d802`; `vectors.json` 8 `opal`/`gateway` vectors -> `opal`/`ingress` |

How it was applied: the order names `git apply <the worktree's copy of gateway_whole.patch>`, and that
returned rc=1, refusing 7 of 12 paths. The checkout copy is CRLF (`w/crlf`, autocrlf); the 7 refused targets
are `eol=lf` files. The committed blob of the same patch (`git show HEAD:<patch>`, hash-object
`fd3b303d56` = the HEAD blob) passed `--check` and applied 12 of 12 cleanly. It was applied as is: nothing was
re-made by hand and nothing was widened. Row `LGIC_ENFORCE-W6-S2`.

Regeneration: `python lib/opal_naming.py generate --out .` gave `GENERATE: 9 written, 0 skipped, into . at
registry@0f9240483015d802`, and the git diff was byte-identical before and after (cmp). The patched tree already
was the generator's output. The tftest (`opal_name.tftest.hcl`) is not written by `generate` at this base and
was not touched.

## Criteria (7 of 7 mechanical, 0 judgment)

| Id | Invocation (`check_en_r2.py <sub>`) | Deciding line | rc |
|---|---|---|---|
| R5-AC1 | `r5-validate` | `rc=0  REFUSED: 0  SYSTEM ROWS: 17` / `VERDICT: PASS-R5-SEVENTEEN-SYSTEMS` | 0 |
| R5-AC2 | `r5-generate` | `generate rc=0  VIEWS: 9  NOT EQUAL TO THE COMMITTED BYTES: []` / `VERDICT: PASS-R5-VIEWS-MATCH` | 0 |
| R5-AC3 | `r5-tests` | `FAILING HERE: 0  FAILING AT THE BASE'S BYTES: 1  NEW: []` / `VERDICT: PASS-R5-NO-NEW-SUITE-FAILURE` | 0 |
| R5-AC4 | `r5-address` | `= s3://opal-data-assets/gateway/49financial/bronze/taxsma_workbook/date=2026-09-15/snap-0001.json` / `VERDICT: PASS-R5-ADDRESS-IN-ASSETS` | 0 |
| R5-AC5 | `r5-name` | `= gateway-49f-taxsma-role` / `VERDICT: PASS-R5-NAME-BUILT` | 0 |
| R5-AC6 | `r5-sharepoint` | `raises ValueError: source 'sharepoint' is not a systems.json key` / `VERDICT: PASS-R5-SHAREPOINT-STILL-REFUSED` | 0 |
| R5-AC7 | `r5-worked-case` | `LINES CHANGED IN GRADING_RULE.md SINCE THE BASE: 2 (every one the opal-gateway case: True)` / `VERDICT: PASS-R5-ONE-WORKED-CASE-MOVED` | 0 |

Every criterion ran on the tree at `c19dcc8147`, from the worktree root. `r5-tests` ran alone, because it
swaps `lib/opal_naming.py` to the base's bytes and back; the worktree was clean afterwards.

Before state, measured at the spawn base before the apply: `python lib/opal_naming.py validate` ->
`VALIDATE: OK 16 system row(s), 9 scope row(s), 9 warning(s) at registry@ba5318901b937130`. R5-AC1 needs 17.

## Controls

- Mutant arm A: one line appended to `generated_locals.tf`. `r5-generate` -> `NOT EQUAL TO THE COMMITTED BYTES:
  ['infra/aws/terraform/modules/opal_name/generated_locals.tf']`, `VERDICT: FAIL-R5-VIEWS-DIFFER`, rc 1.
  Restored from saved bytes; `git diff --quiet` rc 0.
- Mutant arm B: a different worked case (`globgrph-serving`, verdict `RAISE` -> `RAISEX`) changed in
  `GRADING_RULE.md`. `r5-worked-case` -> `LINES CHANGED ... 4 (every one the opal-gateway case: False)`,
  `VERDICT: FAIL-R5-WORKED-CASES`, rc 1. Restored from saved bytes; cmp identical, `git diff --quiet` rc 0.
- Determinism: the six criteria other than R5-AC3 ran a second time. With CR stripped and the generator's temp
  directory masked, 6 of 6 outputs were identical, and every rc was 0.

## Notes and what is not claimed

- The commit gate passed commit 1 (`pre-commit gate clean for 7 of 12 file(s)`; ruff and py_compile passed on
  the .py files). The naming gate printed one WARN, `NAMING OUT-OF-PATTERN lib/opal_naming.py:1359 etfs ->
  lookup('etfs')`, `EXISTING hand-kept carrier (context rule): WARN`. The WARN is on the pre-existing `etfs`
  token of the `_VECTOR_SHAPES` line the patch changed, which the issuer's patch leaves as it was.
- Nothing live moved. There were no AWS reads or writes, no Terraform and no deploy (BOUNDS). Re-grading the
  14 live `opal-gateway-*` names to `gateway-*` canonical forms is a verdict, not a rename, and was not
  exercised here.
- The G-V19 cells, the tftest and every other round-2 cell are outside this order.
