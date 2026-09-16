# Result -- LGIC_NAMING.TO-LN-f-2-r5 (LN-f-2, round 5): FWD-3's live half, the fence over the live inventory

Assignee `0.9.0_WK_LGIC_NAMING~4`. Worktree `.worktrees/wk-lgic-naming-5-4`, branch `wk-lgic-naming-5-4`,
cut from CLOUD at `119a08a196`.

## What ran

Four `comp-find --corpus aws <firm key>` reads (`--limit 60` for `49financial`, `inflection`, `demo`;
`--limit 40` for `cottonwood`, matching F2R5-AC4's own invocation), plus a re-run of the `cottonwood` read
to check determinism. Never `simulate-policy` (R-17, by name; not invoked at any point in this session).
Estate database vintage across all five runs: `Built from the estate as of 2026-09-16 12:17:46 UTC.
Stitch source: stitch-codebuild built 2026-09-16T03:01:17Z.  manifest: 9ef84d8b3ded`; 2558 aws nodes
scanned, identical on every run.

Each firm's `BANDS` line (comp-find's own "true totals, not this page" annotation) showed exactly one
`IAM_ROLE` hit carrying that firm's key:

| firm key | live IAM_ROLE name | DENOMINATOR (comp-find) |
|---|---|---|
| 49financial | irpt-core-firm-49financial | 8 hit(s) across 2558 aws node(s) scanned |
| inflection | irpt-core-firm-inflection | 5 hit(s) across 2558 aws node(s) scanned |
| cottonwood | irpt-core-firm-cottonwood | 7 hit(s) across 2558 aws node(s) scanned |
| demo | demo-transform-runner-ec2-role | 6 hit(s) across 2558 aws node(s) scanned |

These four names agree with RULING R-20's own measurement (`SELF_DRIVE_LGIC_RULINGS_20260916.md:859-861`),
re-derived here on this worker's own instrument run rather than carried forward from the ruling's text
(BOUNDS: "the `0 of 4` is the issuer's measurement at the cut; yours is whatever your own run reads").

The record `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r5/f2-live-fence.r5.md` was written
with this data and committed at `f13a91bdffae5bb7205ea89cbaeae2c431398f3b` before this proof-of-spec
instance was authored (BOUNDS: "commit the artifact first, then pin it; never PENDING-THIS-COMMIT").

## Mechanical criteria

All four run from the worktree root against the issuer's fixed checker
`org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r5/check_ln_r5.py` (read-only,
never edited):

- `f2-positive` -> `VERDICT: PASS-FENCE-CLAIMS-ITS-OWN` -- 8 of 8 strings (4 firms x {probe, canonical})
  matched their own firm's `fence_patterns()` glob.
- `f2-negative` -> `VERDICT: PASS-FENCE-EXCLUDES-OTHERS` -- 0 leaks of 12 cross-firm pairs.
- `f2-coverage` -> `VERDICT: PASS-COVERAGE-DISCLOSED` -- 0 of 4 live nodes carrying the firm key are caught
  by that firm's own fence (disclosure, not a bar, R-20 iii); every uncaught node printed with its
  `grade()` verdict and canonical form. This is the finding R-20 names, not a defect in this cell's work.
- `comp-find --corpus aws cottonwood --limit 40` -> `DENOMINATOR: 7 hit(s) across 2558 aws node(s)
  scanned [corpus=aws]`, matching F2R5-AC4's expected pattern.

## What this read cannot see

A firm's IAM role that carries no firm key anywhere in its name or ARN is outside a text match on that
key and is invisible to every list in the record -- its absence there is not evidence of its absence in
AWS. The record and this result do not claim the four-name set is the whole of any firm's IAM_ROLE
population; RULING R-20 names this the walk's UNMEASURED class.

## AWS plane contact

Read-only throughout: every AWS contact was `comp-find --corpus aws`, a read of a built node database.
No `aws` write command, no Terraform, no rename of any live resource, in this session.
