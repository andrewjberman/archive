# TO 3F-B7 — Inflection July Anomaly Validation: MECHANISM VERDICT

**Agent:** 0.6.2_AE_PartnerETL~A · **Date:** 2026-07-22 (~20:26–21:0xZ) · **Project:** MDPF_3FIRMS (PRD v1.4 @36be68476)
**Andrew's observation (verbatim in TO):** "a jump on july 6 that dropped july 7 then came back on july 10 or a little later
jumped back up again; that is just questionable and to me smells like changing methodology"

## VERDICT (one paragraph)

Andrew's observed pattern is **two mechanisms, neither a methodology change**: the "jump on July 6" is the
**RF-11 served-layer axis mis-stamp** — the served point labeled 2026-07-06 carries the **2026-07-10 snapshot,
exact to the dollar on both value axes** (model 136,859,722; custody 202,320,729) — and the "came back July 10
or later" is **real book movement**: 65 portfolios were migrated from IWM models into Opal models on 07-10
(+$11,400,606), reconciling the day's +$11,765,853 step to a **zero residual** with market drift (+$365,247) on
the 475 unchanged portfolios. The methodology-change hypothesis was tested **independently** and is
**REFUTED** for this window on four probes (below). The @b47d2ff10 raw-producer defect is **adjacent but
distinct** — it begins 07-11 and touches nothing Andrew saw. **Repull recommendation: NO-GO** — a repull fixes
nothing observed; the defect is in the served layer's axis stamping, not in any pull.

## 0. Trading calendar (resolved FIRST, NEVER#1)

`lib/trading_calendar.py` (canonical), window 2026-07-01..07-15:
TRADING = 07-01, 07-02, 07-06, 07-07, 07-08, 07-09, 07-10, 07-13, 07-14, 07-15 (10 days).
CLOSED = 07-03 (Independence Day observed), 07-04/05 (weekend), 07-11/12 (weekend).
07-06 is the Monday after a 3-day weekend. No anomaly claim below rests on a closed-day movement.

## 1. Per-date 5-layer trace (denominators printed; positive control 2026-07-16)

Values = Opal-model totalValue sum via the production crosswalk (eclipse feed) and sum(currentValue) (orion
feed). bronze = opal-data-inf; silver = opal-data-assets monolith; gold = staged
`gold/mdpf_revamp/inflection/aggregate_aua_timeseries.json` @2026-07-22T12:54:57Z; served =
`opal-data-portal-v2 json/mdpf/inflection/aggregate-aua-timeseries.json` @2026-07-18T15:01:52Z.

### ECLIPSE model chain (acct = Opal account count / denom = all live rows read)
```
date        td       bronze  acct  denom        silver  acct  denom   gold_staged        served
2026-06-30  T   122,509,723   472    855   122,509,723   472    855   122,509,723      OFF-AXIS
2026-07-01  T        ABSENT     -      -        ABSENT     -      -        ABSENT      OFF-AXIS
2026-07-02  T   122,227,270   474    856   122,227,270   474    856   122,227,270   122,227,270
2026-07-03  -        ABSENT     -      -        ABSENT     -      -      OFF-AXIS      OFF-AXIS
2026-07-06  T   122,866,034   474    856   122,866,034   474    856   122,866,034   136,859,722 <-- MIS-STAMP
2026-07-07  T   123,562,809   474    856   123,562,809   474    856   123,562,809   123,562,809
2026-07-08  T   125,450,227   475    856   125,450,227   475    856   125,450,227   125,450,227
2026-07-09  T   125,093,869   475    856   125,093,869   475    856   125,093,869      OFF-AXIS
2026-07-10  T   136,859,722   540    856   136,859,722   540    856   136,859,722      OFF-AXIS  <-- REAL STEP
2026-07-11  -        ABSENT     -      -        ABSENT     -      -      OFF-AXIS      OFF-AXIS  (weekend)
2026-07-12  -        ABSENT     -      -        ABSENT     -      -      OFF-AXIS      OFF-AXIS  (weekend)
2026-07-13  T        ABSENT     -      -        ABSENT     -      -        ABSENT      OFF-AXIS  (eclipse unfillable)
2026-07-14  T        ABSENT     -      -        ABSENT     -      -        ABSENT      OFF-AXIS  (eclipse unfillable)
2026-07-15  T        ABSENT     -      -        ABSENT     -      -        ABSENT      OFF-AXIS  (eclipse unfillable)
2026-07-16  T   138,056,428   545    847   137,835,585   545    847   137,835,585   138,056,428 <-- CONTROL (see 4c)
```

### ORION custody chain (cl = distinct clients / denom = rows)
```
date        td       bronze   cl  denom        silver  denom   gold_staged        served
2026-06-30  T   202,125,678  313  33588   202,125,678  33588   202,125,678      OFF-AXIS
2026-07-01  T   202,567,940  312  33588   202,567,940  33588   202,567,940      OFF-AXIS
2026-07-02  T   201,689,910  312  33618   201,689,910  33618   201,689,910   201,689,910
2026-07-03  -   202,542,850  312  33732   202,542,850  33732      OFF-AXIS      OFF-AXIS
2026-07-06  T   202,542,850  312  33732   202,542,850  33732   202,542,850   202,320,729 <-- MIS-STAMP (=true 07-10)
2026-07-07  T   203,686,268  312  33732   203,686,268  33732   203,686,268   203,686,268
2026-07-08  T   202,246,989  316  33737   202,246,989  33737   202,246,989   202,246,989
2026-07-09  T   200,386,009  316  33753   200,386,009  33753   200,386,009      OFF-AXIS
2026-07-10  T   202,320,729  316  33760   202,320,729  33760   202,320,729      OFF-AXIS
2026-07-11  -   202,843,646  318  34935        ABSENT      -      OFF-AXIS      OFF-AXIS  (repaired bronze; mirror pending)
2026-07-12  -   202,843,646  318  34935        ABSENT      -      OFF-AXIS      OFF-AXIS  (repaired bronze; mirror pending)
2026-07-13  T   201,601,607  318  34935        ABSENT      -        ABSENT      OFF-AXIS  (repaired bronze; mirror pending)
2026-07-14  T   202,375,855  319  34942        ABSENT      -        ABSENT      OFF-AXIS  (repaired bronze; mirror pending)
2026-07-15  T   202,880,787  319  34942        ABSENT      -        ABSENT      OFF-AXIS  (repaired bronze; mirror pending)
2026-07-16  T   202,471,099  319  34839   202,471,099  34839   202,471,099   202,471,099   <-- CONTROL clean
```

**Denominators:** 15 dates scanned x 2 feeds x 4 layers; every ABSENT explicit; positive control 07-16
non-ABSENT at every layer on both feeds. bronze==silver==gold EXACT at every present date on both feeds
(sole exception 07-16 eclipse, explained in 4c). The 07-11..15 silver/gold absence is the polling mirror's
pending pass (next 03:30Z 07-23) over my 07-22 source repair — EXPECTED, labeled, not chased (COO 203234Z).

## 2. Candidate 1 — RF-11 axis artifact: CONFIRMED, source-grounded end to end

The mechanism is a three-step chain, every step cited at vintage:

1. **The stamp.** `data/mdpf/scripts/gold/mdpf_aggregate_aua.py:1150 @ed415e268` (last commit 07-09 20:14Z;
   file unchanged to HEAD, so run-vintage == HEAD): `served_as_of_date = source_vintage["overall"] or date`.
   On the 07-10T14:53:43Z run, the 49F partner block was **rolled forward** at 2026-07-06, and the
   rolled-forward vintage-conservatism rule (`:1176-1179 @ed415e268`, "overall forced to min(as_of_by_partner)
   ... CTO 233614Z: no current-over-rolled") forced `overall = 2026-07-06`. The partition
   `platinum/mdpf/aggregate_aua/2026-07-10.json` (LastModified 2026-07-10T14:53:44Z) therefore carries
   `as_of_date="2026-07-06"` while its inflection block holds the **live 07-10 eclipse snapshot**
   (`as_of_by_partner: {49financial: 2026-07-06, inflection: 2026-07-10}` — on the face of the artifact).
   A vintage-honesty rule (correct for provenance) was reused as the **timeseries axis stamp** (wrong for a
   mixed-vintage partition): one scalar stamp, two partner vintages, oldest wins.
2. **The axis replacement.** `data/mdpf/scripts/backfill/build_aggregate_aua_timeseries.py:306-316 @HEAD`:
   the rollup axes on the partition's INTERNAL `as_of_date` and dedups newest-filename-wins per internal
   date. `2026-07-10.json` (internal 07-06, inflection=136,859,722) therefore **replaces** the correct
   `2026-07-06.json` (internal 07-06, inflection=122,866,034, written 07-07T15:31:39Z) — and no 07-10 point
   exists on the served axis at all.
3. **The measured result** (dollar-exact, TWO independent value axes + the count axis):
   served["2026-07-06"].model_aua = 136,859,722 == true 07-10 (true 07-06 = 122,866,034);
   served["2026-07-06"].custody = 202,320,729 == true 07-10 (true 07-06 = 202,542,850);
   count axis previously measured by DS: 540 (07-10 roster) vs true 474
   (`dim_mdpf_aggregate_aua_timeseries.py:808-818 @HEAD`).
   Served axis in-window = {07-02, 07-06, 07-07, 07-08, 07-16..}: **omits real trading days 07-01, 07-09,
   07-10, 07-13..15** — RF-11's omission half, measured.

So Andrew's "jump on July 6 / dropped July 7": the 07-06 slot renders the 07-10 snapshot (+$14.0M vs true
07-06); the next rendered point is the TRUE 07-07 value — a manufactured spike-and-revert.

## 3. Candidate 2 — methodology change: REFUTED (tested independently, four probes)

Tested WITHOUT reference to the axis artifact, per the TO's hard requirement:

- **(a) Per-date methodology tag.** Every platinum partition in the window carries
  `methodology_version = "v0_9_1"` (07-02, 07-06, 07-07, 07-08, 07-10, 07-16 — read directly from the
  partitions). The per-date basis tag exists precisely to record methodology transitions
  (MDPF_ASSETS.016 Correction 8, `build_aggregate_aua_timeseries.py:280`); it is constant.
- **(b) Stayed-cohort level test (the sharp one).** A valuation-methodology change moves the portfolios
  whose ASSIGNMENT did not change. On 07-09 -> 07-10, the 475 continuing Opal portfolios moved **+$365,247
  (+0.29%)** — ordinary daily drift, no level shift. Denominators 856/856 live portfolios both days.
- **(c) Exact composition decomposition.** The +$11,765,853 step = 65 portfolios ENTERING Opal models
  (+$11,400,606, every one from an "IWM ..." model — resolved via the production crosswalk) + drift
  (+$365,247) + 0 leavers + 0 new rows; **residual $0**. Counts reconcile: 475+65 = 540 == the 07-10 Opal
  account count. Corroborated by the 07-22 eclipse audit census (848/848 portfolios): 67 assignment-change
  records on exactly 07-10. Custody flat (~$202.3M) — reassignment of existing assets, not new money.
  **Positive control:** the same diff on the quiet pair 07-07 -> 07-08 shows a different signature
  (1 entry +$2.8M, drift -$0.9M, residual $0) — the instrument discriminates.
- **(d) Transformation-chain faithfulness + code census.** bronze==silver==gold EXACT at every present
  date on both feeds (section 1), and the step exists **inside the raw same-day vendor captures**
  (bronze 07-09 pulled 07-09T13:40:47Z; bronze 07-10 pulled 07-10T13:38:31Z — original, untouched), so no
  repo/pipeline code change could have manufactured it. The 07-01..07-16 commit window on
  `data/inf/` + the legacy builder (184 commits) contains no change to eclipse `totalValue` / orion
  `currentValue` value semantics.

Residual honestly stated: eclipse history cannot be re-queried (the API ignores every date parameter —
exercised 07-22, 8 params, byte-identical bodies), so a vendor-side restatement BEFORE 07-09 is not directly
testable; it is also not needed — every rendered number Andrew saw is accounted for by (2) and (c) above.

## 4. Part (c) — relation to @b47d2ff10, and residual findings

- **(c-verdict): (ii) + (iii), jointly; NOT (i).** The raw-producer death (@b47d2ff10) begins at 07-11 —
  bronze 07-01..07-10 are original same-day captures (LastModified 13:3x-15:0xZ each own day, listed in
  section 1 evidence). Andrew's window (07-06..07-10) is untouched by that defect. His observed pattern =
  a SEPARATE served-layer defect (the axis mis-stamp, section 2) + REAL movement (the 07-10 migration,
  section 3c). The 07-11..15 downstream absence remains the @b47d2ff10 window: source-repaired 07-22,
  propagation at the 03:30Z 07-23 mirror pass (3F-B3 verifies it).
- **(4c) 07-16 eclipse double-pull (minor, new).** Monolith silver 07-16 was converted 14:16:08Z from an
  earlier intra-day pull; bronze `portfolios_full.json` was re-pulled 15:03:04Z. Delta 220,843 (0.16%) =
  intra-day movement between two same-day snapshots, same 545/847 counts. Not a defect requiring action;
  recorded so nobody reads the 220,843 as drift. (Legacy served 07-16 == the later pull.)
- **(4d) 07-01 eclipse ABSENT** — pre-existing known gap (2 assignment changes that day per the 848/848
  census); unfillable (date-ignoring endpoint); NOT part of Andrew's observed pattern (served has no
  07-01 point).

## 5. Repull recommendation to CTO: **NO-GO**

A July repull fixes **nothing that produced the observation**:
- Orion July bronze is COMPLETE (07-01..07-10 original + 07-11..15 repaired 07-22, verified with per-date
  rosters); a repull would rewrite honest captures with today-vintage data for zero gain.
- Eclipse July CANNOT be repulled: the vendor endpoint ignores date parameters; the `--date`-is-a-filename
  ban is undisturbed and this verdict does not touch it. 07-13..15 stay honest holes pending the separate
  3F-B4 recoverability verdict.
- The defect Andrew saw lives in the SERVED layer's axis stamping (section 2) — no pull at any layer
  changes it. What actually cures the chart: the MDPF_REVAMP staged artifact is already trading-day-clean
  and value-verified here (section 1); cutover is the S5 flip governed under LD-0330, outside this TO.
  A targeted legacy fix (stamp per-partner as_of, or axis on run-date) is possible but is CTO's call and
  arguably moot given the pending cutover.

## 6. Escalation check (TO <escalation>)

The evidence does NOT indicate a methodology change occurred — the escalation trigger is NOT met. COO was
escalated in-flight (203305Z) per the LOUD-immediately list; this verdict completes that thread.

## Evidence inventory

- Trace + diff scripts (reproducible): scratchpad `b7_trace.py`, `b7_diff_0710.py` (read-only; boto3 reads,
  no writes to any bucket).
- Artifacts read: served json @2026-07-18T15:01:52Z; staged @2026-07-22T12:54:57Z; platinum partitions
  2026-07-{02,06,07,08,10,16}.json (vintages listed in section 2); bronze/silver objects per section 1.
- Citations at vintage: `mdpf_aggregate_aua.py:1150,1176-1179 @ed415e268` (== run vintage, verified via
  `git show`); `build_aggregate_aua_timeseries.py:306-316 @HEAD`; `dim_mdpf_aggregate_aua_timeseries.py:808-818 @HEAD`.
- comp-freshness self-test PASS 3/3; `chain inf` run 20:2xZ (flat-hours basis gap recorded — only the
  platinum row resolves trading-day; NO staleness raised off it, NEVER#1).

## Addendum (post-CVO spot-verify @6bb15dbcb, 2026-07-22 21:19Z — verdict PASS, no rework)

Two CVO refinements folded, both strengthening:
1. **The replacement in §2 step 2 is STRUCTURALLY FORCED, not behavioral:** BOTH platinum partitions
   (2026-07-06.json and 2026-07-10.json) carry internal `as_of_date=2026-07-06` — a visible collision in
   the payloads themselves — so ANY internal-date dedup with newest-filename-wins MUST overwrite the true
   07-06. The claim does not depend on trusting the dedup description.
2. **Probe (a) in §3 is CORROBORATIVE, not discriminating** (a constant tag proves no RECORDED methodology
   change; an unrecorded one reads identical). Probe (d) carries the discriminating weight — a step inside
   untouched same-day vendor bronze cannot be manufactured downstream. Read §3 in the order (d),(b),(c),(a).
CVO independently confirmed the identity to the cent on both value axes and the citations at vintage
(positive-controlled at 1385 lines); probes (b)/(c)/(d) were NOT re-derived by CVO and are so labeled in
the CVO record.
