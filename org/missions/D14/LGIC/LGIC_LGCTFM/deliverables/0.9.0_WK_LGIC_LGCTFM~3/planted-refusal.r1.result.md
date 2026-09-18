# LT-x-2-r1 result -- the planted refusal

**Worker:** `0.9.0_WK_LGIC_LGCTFM~3` on `LGIC_LGCTFM.TO-LT-x-2-r1`. **Branch:** `wk-lgic-lgctfm-1-3`
@`fa69ff65ea`. **PRD** v1.4 @`459b4a736d`. **Decomp** v1.1 @`60aac06844`, cell `LT-x-2`.

## What ran

A practice worktree (`wk3-practice-plant` off HEAD `ea26e21bc1`, never pushed) carried
`org/mcp/naming-gate.enforce` (present there only) and two edits to
`data/black_diamond/scripts/gold/gold_freshness_config.yaml`, each staged and diffed separately, never
committed:

- **ADD:** one new freshness entry, `bd_gold_accounts_dimension_e12_strict`, reusing the exact
  existing `s3_key_prefix` of line 181's `bd_gold_accounts_dimension` entry
  (`s3://opal-data-bd/gold/dimensions/accounts_dimension_latest.parquet`) -- a second, tighter watch on
  the same A_00 gate artifact for an `E_12` reconciliation diagnostic. `s3://opal-data-bd/.../gold/...`
  is the ADVI_FIRMBKTS remediation's s3-prefix surface (`infra/logic/registry/remediations.json`
  remediations[0].surfaces[4]: `{"kind": "s3-prefix", "bucket": "opal-data-bd", "prefix": "gold/"}`).
- **REMOVE:** deletion of the pre-existing `bd_gold_accounts_dimension` entry outright (lines 180-188),
  an existing use of the same surface removed.

Both diffs were run through `python .tools/naming-gate.py --diff <file> --enforce`: once in the
practice worktree, once again directly against this worktree's real HEAD (same pre-image blob,
`4f72d6e53333...`) after the practice worktree was removed. Output was byte-identical both times.

## What was seen

ADD: `rc=1`, `NAMING-GATE: REFUSE 2 graded`. The S3Key line's `why` reads *"EXISTING and OUT-OF-PATTERN
as S3Key in a surface remediations.json assigns to the live remediation ADVI_FIRMBKTS: REFUSE unless
the diff removes it"* -- naming-gate.py's `remediation_of()` (`.tools/naming-gate.py:649-668`) fires
because the literal is byte-identical to text already in the file's pre-image (graded EXISTING, not
NEW) and its bucket (`opal-data-bd`) matches the surface's `bucket-alias`... here the s3-prefix match
(`gold/` under `opal-data-bd`).

REMOVE: `rc=0`, `NAMING-GATE: PASS 0 graded`. A diff that only removes lines has no ADDED literal to
grade (`grade_file`, `.tools/naming-gate.py:891-893`: `if not added: return []`).

## Mutant control

`add.diff`'s reused literal was mutated to a fabricated new suffix
(`..._latest_v2.parquet`, absent from the file's pre-image) and re-graded the same way, never staged
anywhere. Still `rc=1` REFUSE (a new, out-of-pattern, hand-kept S3Key refuses regardless), but the
`why` text drops to *"NEW and OUT-OF-PATTERN as S3Key: REFUSE"* -- zero occurrences of `ADVI_FIRMBKTS`
in the output. This is the discriminator behind X2R1-AC1: the criterion's "names ADVI_FIRMBKTS" bar is
satisfied specifically because `add.diff` reuses the EXISTING literal, not merely because it touches
the marked bucket/prefix.

## Estate flag

`org/mcp/naming-gate.enforce` was created only inside the deleted practice worktree. In this worktree:
`git log --oneline <base>..HEAD -- org/mcp/naming-gate.enforce` and
`git status --porcelain -- org/mcp/naming-gate.enforce` both empty.

## Criteria

| id | verdict | evidence |
|---|---|---|
| X2R1-AC1 | PASS | `x2-adding` -> `VERDICT: PASS-X2-ADDED-USE-REFUSED` |
| X2R1-AC2 | PASS | `x2-removing` -> `VERDICT: PASS-X2-REMOVED-USE-PASSES` |
| X2R1-AC3 | PASS | `x2-flag` -> `VERDICT: PASS-X2-ESTATE-FLAG-UNTOUCHED` |
| X2R1-AC4 | judgment, no verdict from this worker | recorded for `3.0.0_SA_CVO` at L9 |

Full instance: `LGIC_LGCTFM.TO-LT-x-2-r1.planted-refusal.proof_of_spec.json` (this folder).
