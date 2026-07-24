<task_order>
<id>MDPF_3FIRMS.GC-BF1</id>
<title>BF1 — 49F schwab/silver/rps is stuck at 2026-07-15 and it is BLOCKING ANDREW'S CLOSE-OUT. FIRST DELIVERABLE IS A FIVE-MINUTE DISCRIMINATION, NOT A CONVERSION: are the Schwab source files PRESENT-and-unconverted, or ABSENT since 07-15?</title>
<project>MDPF_3FIRMS</project>
<workstream>Global-Count closeout — ON THE CRITICAL PATH (CTO-confirmed 152352Z). Andrew is waiting.</workstream>
<issued_to>0.6.2_AE_PartnerETL~C</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-24T15:26Z</issued_at>
<status>complete</status>
<!-- COMPLETE 20260724T1638Z. Ledger schwab-0824-silver-rollforward-20260724 CLOSED, all 8 legs proven,
     nothing stranded (NEVER#6). Acceptance criteria 1-4 all met:
     (1) discrimination reported FIRST and separately (153852Z COO / 153917Z CTO) naming what was inspected;
     (2) PRESENT branch -> all seven legs run, 42/42 silver partitions landed + content-verified, and
         schwab/silver/rps demonstrated within max_lag 2 by EXERCISING the deployed trigger's own
         _check_schwab_rps() (fresh=True, behind=1) with a positive control reproducing its pre-run
         log line and mutants proving it can still fail -- condition cited from lambda_function.py:453;
     (3) n/a (not the ABSENT branch); (4) explicit-Z throughout, no ad-hoc gold run to validate.
     BEYOND SCOPE, done because leaving it would have been a silent partial: canonical store caught up
     20260715 -> 20260723 (54/54 partitions) around a source-confirmed defect in build_canonical_daily.py.
     TWO defects found and ROUTED, not fixed (Rule 17a / Rule 13):
       org/tier2_senior/0.6.2_AE_PartnerETL/deliverables/FINDING_49f_monolith_key_grammar_and_canonical_orchestrator_20260724.md -->

<!-- 0.6.2_AE_PartnerETL~C 20260724T1531Z: picked up from the TO commit 62594e9911 (no inbox GO had landed yet).
     DISCRIMINATION reported 153852Z/153917Z BEFORE any conversion, per the TO's first deliverable:
     PRESENT-and-unconverted in monolith bronze, all 11 consumed types complete through 20260723, third state
     (present-but-partial) ruled OUT by a 17-prefix enumeration. NO ANDREW ACTION.
     Seven-step cycle run; 42/42 partitions landed; mdpf gate exercised on DEPLOYED bytes -> fresh=True.
     NOTE the TO's <forbidden_shortcuts> "look at the DELIVERY FOLDER" clause is DEFECTIVE and COO has
     accepted it as such (153941Z): the OneDrive folder alone returns ABSENT and would have sent Andrew to
     download data that already existed. The monolith channel is the authoritative one. -->
<!-- Ledger: schwab-0824-silver-rollforward-20260724 (org/critical_paths/change_management/20260724T1542Z_*) -->

<authorization>Andrew-direct ~1432Z (MDPF counts PRIMARY through to VALIDATED) + ~1509Z (collect, ping, visual-smoke, close) -> CTO 152352Z confirming this is on the critical path and directing the spawn without further confirmation.</authorization>

<why_this_is_urgent>
**THE CHART ANDREW WILL VISUAL-SMOKE IS AN OUTPUT OF THE MDPF GOLD CHAIN, AND THE CHAIN IS NOT
DISPATCHING.** CTO's traced path (his own audit, not inference):

```
chart Global count line  <- ModelPortfolios.tsx globalMdpfData, readCountTotalSeries :806-808
reads                    <- json/mdpf/global/aggregate-aua-timeseries.json   (SERVED)
produced by              <- dim_mdpf_aggregate_aua_timeseries.py             (MDPF GOLD)
imports counts from      <- json/mdpf/{firm}/aggregate-aua-timeseries.json   (SELF-REFERENTIAL)
```

`mdpf-daily-trigger` FIRED correctly at 15:01:43Z and then **DEFERRED**:
`49financial fresh=FALSE, schwab/silver/rps, latest_partition 2026-07-15, trading_days_behind 7 (max_lag 2)`.

**So: no dispatch -> no new served artifact -> backfilled counts never reach the chart.** We would collect
22 dates, verify them, ping Andrew, and he would smoke **a chart that had not moved** — whose most likely
reading is *"the fix did not work."* That is the worst outcome available for a close-out.

**And the self-referential import makes it STRICTER:** because the importer reads the PREVIOUS served
artifact, a backfill landing upstream while the chain defers is **inert, and stays inert every subsequent
night until a build succeeds.**
</why_this_is_urgent>

<scope>
>> **DO NOT START BY RUNNING THE CONVERSION. START BY ANSWERING ONE QUESTION.**

The `/49-schwab-conv` cycle (account `08242234`) **begins by syncing newly-delivered Schwab CRS files from
the local OneDrive DELIVERY FOLDER to S3.** Its first step depends on files having been delivered. So:

```
ARE THE SCHWAB SOURCE FILES FOR 2026-07-16 ONWARD PRESENT LOCALLY AND UNCONVERTED?

  PRESENT + unconverted  -> we are unblocked. Run the /49-schwab-conv cycle. NO Andrew action.
  ABSENT since 07-15     -> ANDREW MUST DELIVER THEM. Nothing we do fixes it, and every hour we
                            spend elsewhere is an hour he is not being asked.
```

**REPORT THAT ANSWER BEFORE DOING ANYTHING ELSE.** It is a five-minute check and it decides whether this is
our problem or a sovereign one. **An unnecessary hour of silence here is an hour Andrew waits on a close-out
that cannot happen.**

**IF PRESENT:** run `/49-schwab-conv` — ALL SEVEN STEPS, every time (sync → ACC → RPS → TRN-Layer-A →
TRN-NNA-Layer-B → ULN → **RLD, which is NON-OPTIONAL**), then verify the latest partition per table on S3.
The gate needs `schwab/silver/rps` to advance to within `max_lag 2` trading days of
`expected_last_trading_day`.

**IF ABSENT:** say so immediately with the evidence (what you looked at, what date range is missing, what
the newest delivered file is). Do not attempt a workaround, do not synthesise a partition, do not "roll
forward" what is not there.
</scope>

<explicitly_out_of_scope>
- **The 22-date backfill itself** — `0.6.2_AE_PartnerETL~B` (GC-BF0 capability assessment) and gated by CTO.
- **The mdpf trigger's misdiagnosis** of ABSENT-vs-UNREADABLE (403-not-404 from a missing `s3:ListBucket`).
  Real, routed separately, and **granting ListBucket unblocks nothing** — both states defer. Not yours.
- Anything in the MDPF composition, the render, or the roster design.
- **DS is blocked from this tree** by the `opal-data-schwab` PutObject SSE deny — that is WHY it is AE-owned.
  Do not hand any part of it back to DS.
</explicitly_out_of_scope>

<forbidden_shortcuts>
Per `docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md` @d3681d1d0:
- *Easiest pass on the discrimination:* check whether the S3 prefix has new partitions and conclude the
  files are absent. **S3 emptiness is downstream of the sync — it tells you the conversion has not run, not
  whether the SOURCE exists.** Look at the DELIVERY FOLDER.
- *Easiest pass on the conversion:* run the cycle, see `rps` advance, report unblocked. **The gate is
  `trading_days_behind <= 2` against `expected_last_trading_day`** — verify against the gate's own
  condition, not against "a new partition appeared."
- **MISSING THIRD STATE:** the answer is not `present | absent`. It is
  `present-and-unconverted | absent-since-07-15 | present-but-partial` — and a partial delivery that
  converts cleanly up to a date short of the gate leaves you reporting success on a still-deferred chain.
</forbidden_shortcuts>

<acceptance_criteria>
1. **THE DISCRIMINATION, REPORTED FIRST AND SEPARATELY**, with what you inspected named explicitly.
2. If PRESENT: all seven `/49-schwab-conv` steps run, latest partition verified per table on S3, and
   **`schwab/silver/rps` demonstrated within `max_lag 2`** of `expected_last_trading_day` — i.e. the
   condition the trigger actually evaluates, cited from the trigger's own logic.
3. If ABSENT: the evidence, the missing date range, and the newest delivered file. **No workaround.**
4. Explicit-Z timestamps. NEVER#4 respected (no ad-hoc gold run to validate).
</acceptance_criteria>

<deliverables>
  - The discrimination answer to **COO + CTO immediately** — before any conversion work.
  - If converted: the per-table S3 verification + notify per the `/49-schwab-conv` protocol.
</deliverables>

<notes>
Register as `0.6.2_AE_PartnerETL~C` — FULL suffixed serial. `~A` (D_00 + retry-net verify, SoD-bound) and
`~B` (GC-BF0 capability assessment, also critical path) are both LIVE. **Do not take their work.**
`/49-schwab-conv` is the canonical procedure and folds every banked gotcha for this cycle — use it rather
than improvising the seven steps.
</notes>
</task_order>
