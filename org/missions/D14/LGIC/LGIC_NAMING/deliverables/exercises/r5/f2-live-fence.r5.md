# F2 live fence -- LN-f-2, round 5, FWD-3's LIVE half (R-17, R-20)

Cell `LN-f-2` (decomposition v7.1 section 0f). Read by `0.9.0_WK_LGIC_NAMING~4`. RULING R-17 classifies
FWD-3's live half as a LIVE-plane claim (a repo read cannot see a system the repo never declared); RULING
R-20 (`org/tier1_exec/1.0.0_SA_CTO/deliverables/SELF_DRIVE_LGIC_RULINGS_20260916.md:854-897`) cuts this
criterion into three clauses -- POSITIVE (i), NEGATIVE (ii), COVERAGE-disclosure (iii) -- so it cannot pass
on an empty claim set.

## Instrument

`comp-find --corpus aws <firm key> --limit 60` for `49financial`, `inflection`, `demo`; `--limit 40` for
`cottonwood` (F2R5-AC4's own invocation). Never `simulate-policy` (R-17, by name). Four independent runs,
2026-09-16, this worktree. The estate's built database is the SAME across all four runs (same vintage,
same nodes-scanned denominator) -- one built snapshot queried four times, not four separate builds.

## Per-run evidence (comp-find's own lines, verbatim)

- `49financial`: `DENOMINATOR: 8 hit(s) across 2558 aws node(s) scanned [corpus=aws]`; `BANDS ... IAM_ROLE=1`
  (BANDS states "true totals, not this page"). The one IAM_ROLE hit: `irpt-core-firm-49financial`
  (`arn:aws:iam::313476888478:role/irpt-core-firm-49financial`, drift=DECLARED).
- `inflection`: `DENOMINATOR: 5 hit(s) across 2558 aws node(s) scanned [corpus=aws]`; `BANDS ... IAM_ROLE=1`.
  The one IAM_ROLE hit: `irpt-core-firm-inflection`
  (`arn:aws:iam::313476888478:role/irpt-core-firm-inflection`, drift=DECLARED).
- `cottonwood`: `DENOMINATOR: 7 hit(s) across 2558 aws node(s) scanned [corpus=aws]`; `BANDS ... IAM_ROLE=1`.
  The one IAM_ROLE hit: `irpt-core-firm-cottonwood`
  (`arn:aws:iam::313476888478:role/irpt-core-firm-cottonwood`, drift=DECLARED).
- `demo`: `DENOMINATOR: 6 hit(s) across 2558 aws node(s) scanned [corpus=aws]`; `BANDS ... IAM_ROLE=1`.
  The one IAM_ROLE hit: `demo-transform-runner-ec2-role`
  (`arn:aws:iam::313476888478:role/demo-transform-runner-ec2-role`, drift=DECLARED).

Each firm's `BANDS` line is the TRUE total for that node type over the whole sweep, not a page artifact
(comp-find's own annotation: "true totals, not this page"), and each run's `PAGE 1 of 1 (showing N of N)`
confirms nothing was truncated at `--limit`. So each firm's single IAM_ROLE hit above is the WHOLE of what
this read found for that firm's key at this vintage, not a sample.

This measurement agrees with RULING R-20's own (`SELF_DRIVE_LGIC_RULINGS_20260916.md:859-861`), re-derived
here on this worker's own run rather than carried from the ruling's text -- the ruling's numbers are context
per the order's own bound ("yours is whatever your own run reads"), and this run reads the same four names.

## What this read CANNOT see

A firm's IAM role that carries no firm key anywhere in its name or ARN is outside a text match on that key
and is invisible to every list below by construction -- its absence from a firm's list is NOT evidence that
the firm has no such role. This record does not claim the lists below are the whole of any firm's IAM_ROLE
population, only the live nodes a text match on the firm's key surfaced at this vintage. RULING R-20 names
this the walk's UNMEASURED class (`SELF_DRIVE_LGIC_RULINGS_20260916.md:891-892`): "a firm role carrying no
firm key in its name is outside a text read."

## Record

```json
{
  "vintage": "VINTAGE: Built from the estate as of 2026-09-16 12:17:46 UTC. Stitch source: stitch-codebuild built 2026-09-16T03:01:17Z.  manifest: 9ef84d8b3ded",
  "nodes_scanned": 2558,
  "firms": {
    "49financial": ["irpt-core-firm-49financial"],
    "inflection": ["irpt-core-firm-inflection"],
    "cottonwood": ["irpt-core-firm-cottonwood"],
    "demo": ["demo-transform-runner-ec2-role"]
  }
}
```
