# LGIC_ENFORCE.TO-EN-s-25-r4 -- result

**Worker:** `0.9.0_WK_LGIC_ENFORCE~2` | **Branch:** `wk-lgic-enforce-4-2`, cut from CLOUD @`a7ae7f5e01` |
**Commit:** `7fbf6faa19` (LOCAL, this worktree's branch)

## What ran

`python lib/opal_naming.py census --live --repo --not-judged
org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/NOT_JUDGED_R4.json --report
org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~2/NAMING_CENSUS_REPORT.r4.md` --
**rc=0**, `CENSUS: COMPLETE 3237 judged + 467 carded (live 1690+136 of 1826 nameable, repo 1547+331 of 1878)`.
Both planes close: `judged_live 1690 + carded_live 136 == live_nameable 1826`; `judged_repo 1547 +
carded_repo 331 == repo 1878`; `stopped: null`. Registry read at `4f192e91bd64ee70`, unchanged by this
worker. Live vintage `Built from the estate as of 2026-09-17 18:16:22 UTC. Stitch source: stitch-codebuild
built 2026-09-17T03:01:15Z.  manifest: 514495fde115`, corroborated by a separate
`comp-find --corpus aws --name . S3_BUCKET --limit 1` read printing the byte-identical `VINTAGE:` line.

## Verdicts

| criterion | verdict | evidence |
|---|---|---|
| S25R4-AC1 (live complete) | **PASS** | `check_en_r4.py s25-live-complete` -> `VERDICT: PASS-S25-LIVE-COMPLETE`, rc=0 |
| S25R4-AC2 (repo complete) | **PASS** | `check_en_r4.py s25-repo-complete` -> `VERDICT: PASS-S25-REPO-COMPLETE`, rc=0 |
| S25R4-AC3 (no placeholder) | **FAIL** | `check_en_r4.py s25-no-placeholder` -> `1411 of 3237 rows carry a placeholder` -> `VERDICT: FAIL-S25-NO-PLACEHOLDER`, rc=1 |
| S25R4-AC4 (judgment) | UNVERIFIABLE-BY-INSTRUMENT | for `3.0.0_SA_CVO` at L9; see `NAMING_CENSUS_COMPARISON.r4.md` Section 3 |

## Why AC3 FAILs, and why it is not worked around

Round 4's campaign cells closed the **RAISE population** (`RAISE_POPULATION_S6.r3.md`, 351 triples): every
name that would have STOPPED the run is now either carded (348 in `NOT_JUDGED_R4.json`) or resolved by a
registry mint (`EN-h-24-r4`'s 3 CW_ALARM rows). That is why this run reaches `stopped: null` for the first
time in the project's history -- AC1 and AC2 PASS.

W2-S10's placeholder rule (AC3) is a **different, non-RAISE-bounded** rule: `grade()` writes a literal
`{system}`/`{scope}`/`{cadence}` into `canonical` whenever the relevant token is placeholder-eligible (V3)
rather than unresolved (V2) -- this never raises, so it was never presented to either campaign cell's
mint-or-card loop. `EN-h-24-r4` resolved exactly the 8 placeholder rows round 3's EARLY-STOPPED 21-row
report exposed; round 3 never judged past row 21, so the remaining ~1400 placeholder rows this round's
COMPLETE run now reaches were invisible to both campaign cells at cut time. `infra/logic/registry/` is
outside this worker's grant (BOUNDS), so this criterion is reported FAIL with its measured evidence (1411
of 3237 rows, breakdown by (plane,type) in the report and the surprise row) rather than minted or carded by
this worker. Surprise row `LGIC_ENFORCE-W2-S13` (BLOCKING, ARMED, disarm_owner `2.0.0_SA_COO~G`) files it.

## Comparison against the hand products

`NAMING_CENSUS_COMPARISON.r4.md`: N2 (45) 34 compared, 33 agree, 1 disagree; N6 (88) 57 compared, 40 agree,
17 disagree (15 of 17 are a registry-growth effect: N6's hand answer RAISEd at an earlier vintage on a token
the current registry now resolves or places a placeholder for). 42 hand rows left uncompared, each with an
individually re-derived reason (23 NOT-GRADED-TYPE, 2 AWS_FIXED-EXCLUDED, 11 CARDED, 11 HAND-SPECIMEN-ABSENT).

## Status

`<status>` stays `pending` -- one mechanical criterion (S25R4-AC3) is FAIL by measurement. This instance and
result are the final report on this order as cut; the FAIL is real, measured, and outside this worker's
grant to fix.
