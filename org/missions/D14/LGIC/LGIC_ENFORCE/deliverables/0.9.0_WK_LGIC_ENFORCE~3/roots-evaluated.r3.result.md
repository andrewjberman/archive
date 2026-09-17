# EN-t-8 round 3 -- result

**Task order:** `org/missions/D14/LGIC/LGIC_ENFORCE/task-orders/LGIC_ENFORCE.TO-EN-t-8-r3.roots-evaluated.md`
**Worker:** `0.9.0_WK_LGIC_ENFORCE~3`, worktree branch `wk-lgic-enforce-3-3`.
**Status:** the order is complete -- `T8R3-AC1`, `T8R3-AC2`, `T8R3-AC3` PASS by output; `T8R3-AC4` RECORDED
(judgment, UNVERIFIABLE-BY-INSTRUMENT, for `3.0.0_SA_CVO` at L9).

## What ran

The round-2 roots census (`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/LIMB_ROOTS_CENSUS.md`) had **not**
drained the placement cell and was still at its round-2 flat path, so this cell read it there and named that
path in the reproduction record's `census_path`.

**Spot re-plan of one planned root** (`infra/aws/terraform/49f-value-parity`), run in a throwaway location
outside the graded worktree (`.scratch/throwaway_49f-value-parity/`), mirroring the real repo's directory
depth so the root's out-of-root relative source (`data.archive_file` reading `../../compdiff`, row S16)
resolves:

1. `terraform init -input=false` (creates the dependency lock file; none was tracked/committed).
2. `terraform init -input=false -lockfile=readonly` (re-init read-only against the now-present lock file;
   this is where `-lockfile=readonly` is a valid flag -- `terraform plan` does not accept it at all on
   v1.9.8, row S14).
3. `terraform plan -lock=false -input=false -out=plan.tfplan` -- 8 to add, 0 to change, 0 to destroy,
   matching round 2's 8-address extract for this root.
4. `terraform show -json plan.tfplan` -- the raw plan document, `timestamp: 2026-09-17T14:06:38Z`.
5. Reduced the raw `resource_changes` to round 2's own documented shape (its task order
   `LGIC_ENFORCE.TO-EN-t-3-r2.roots-census.md:22`: address/mode/type/name/change.actions and the own-name
   attribute of before/after, read from `.tools/naming-gate.py`'s `TF_NODE` map -- row S15), keeping the
   document's own `timestamp`. Canonically equals the committed round-2 extract (AC1 PASS).
6. `.terraform` (704 MB) removed immediately after step 4; the footprint never exceeded one root
   (`df -h /c` before: 7.9 GB free; after cleanup: 7.3 GB free).

Nothing was applied; no state was written; the scratch clone and its `.terraform` never entered the graded
worktree's tracked tree (both are outside `<paths>` and untracked/gitignored where they touch it).

**Round-3 census** (`LIMB_ROOTS_CENSUS.r3.md`): every one of round 2's 72 rows carried forward unchanged
(`extract`, `plan_sha256`, `reason`), each now carrying `init_flags: "-input=false"` -- the uniform value
round 2's own record (section 1) states was used across all 72 roots. The 4 NOT-planned rows keep their
round-2 `reason` unchanged.

## The four criteria

| id | verdict | deciding line | denominator |
| --- | --- | --- | --- |
| `T8R3-AC1` | **PASS** | `PASS-T8-EXTRACT-REPRODUCED` (rc=0) | re-plan resource_changes 8; committed extract 8; canonical equal: True |
| `T8R3-AC2` | **PASS** | `PASS-T8-INIT-FLAGS-PRINTED` (rc=0) | 72 root row(s); 0 without init_flags |
| `T8R3-AC3` | **PASS** | `PASS-T8R-UNPLANNED-ROOTS-CARRY-CAUSE` (rc=0) | 72 root(s); 4 NOT planned; 0 of those with no recorded cause |
| `T8R3-AC4` | **RECORDED** (judgment) | no self-verdict; `3.0.0_SA_CVO` grades it at L9 | N/A -- judgment |

## Surprises filed

Three rows, `org/missions/D14/LGIC/LGIC_ENFORCE/surprise-channel/investigations/INVESTIGATION_v1.md`:

- `LGIC_ENFORCE-W3-S14` -- the cell text's literal `terraform plan -lockfile=readonly` does not run on
  terraform v1.9.8 (`-lockfile` is `init`-only); this worker's recorded `command` field states the actual
  sequence, which carries the required substring but is not the literal words.
- `LGIC_ENFORCE-W3-S15` -- AC1's checker compares the "full document" literally against round 2's REDUCED
  extract with no reduction step of its own; a genuinely raw `terraform show -json` can never pass, only a
  document reduced the same way round 2's own task order specifies.
- `LGIC_ENFORCE-W3-S16` -- a "throwaway clone" of one root is not self-contained by directory alone when the
  root references a sibling tree by relative path outside its own directory (49f-value-parity's
  `../../compdiff`); root-dependent, caught and fixed in the same turn.

All three: `class` OBSERVATION, `hazard_standing` INERT, `disposition` UNDER_INVESTIGATION.
