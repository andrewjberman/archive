# MDPF_GLOBAL.T1A — Trigger + Route Census (human summary)

    author:    0.7.0_AE_CloudOps
    vintage:   2026-08-03T20:34Z..21:10Z (live AWS reads; account 313476888478, us-east-1)
    machine:   census.yaml (same folder) — the authoritative row-level record
    baseline:  docs/briefs/TRIGGER_GRAPH_AND_RUNTIME_MAP.md (2026-07-29 vintage)
    class:     READ-ONLY census. Nothing was created, modified, disabled, or deleted.

## Denominators (every count from a materialized token-walked list; never `--query length()`)

| Surface | Denominator | Pagination |
|---|---|---|
| EventBridge buses | **1** (`default`) | token-walked, 1 page |
| EventBridge rules | **142** | token-walked, 2 pages |
| — MDPF-relevant subset | **23** (predicate in census.yaml), all 23 target-resolved | token-walked per rule |
| Scheduler groups | **1** (`default`, ACTIVE) | token-walked, 1 page |
| Scheduler schedules | **12** (10 detail-resolved) | token-walked, 1 page |
| S3 buckets notification-probed | **5** (TO's 3 + chain-named `opal-data-bd` + defensive `opal-data-etfs`) | n/a (get calls) |
| SSM associations | **0** | token-walked, 1 page |
| SSM self-owned documents | **20** (3 MDPF-relevant) | token-walked, 2 pages |
| CloudWatch alarms | **51 metric + 0 composite** (7 MDPF-family; census-only) | token-walked, 2 pages |

Scope widening vs the TO's bucket list (noted per the Phase-1 `if_mismatch` instruction): comp-estate
chain prose names `opal-data-bd` (BD silver freshness gate), so it was probed; `opal-data-etfs` probed
defensively. Both carry zero MDPF triggers (BD's 3 notification edges are BD-estate).

## Dispositions (59 census rows — full table in census.yaml)

**CANONICAL 40 · ACCELERATOR 0 · LEGACY-KILL-CANDIDATE 1 · UNKNOWN-loud 2 · OUT-OF-MDPF-SCOPE 12 · CANONICAL-ABSENCE 4**

- **ACCELERATOR = 0 is the headline.** The one event trigger (`mdpf-daily-refresh-trigger`, S3
  ObjectCreated on INF's `gold/meta/pipeline-complete.json`) is still **load-bearing, not an
  accelerator**: it is the SOLE trigger of the runner chain (ScheduleExpression=None confirmed live).
  The NEVER#4 defect the memo names **stands at census time** — it froze the Global view on 08-03 when
  INF wrote `pipeline-failed.json`. The scheduled accrual family (`mdpf-accrual-bridge-daily`
  cron(45 15 UTC) → `mdpf-accrual-trigger`) ran through the same failure. T2.B ruling @440d16e018
  demotes the INF event to accelerator-only once T2C lands the schedule floor (my next TO).
- **LEGACY-KILL-CANDIDATE (1):** `canonical-schwab-si2-download-schedule` (DISABLED, superseded by the
  two per-account daily pulls; 49F Converter ops deprecated Andrew-direct 07-30). Kill routes through
  T5.A + CTO gate — this census only nominates.
- **UNKNOWN-loud (2):** `smartx-daily-export-trigger` (DISABLED rule) and
  `smartx-model-monthly-pull-daily` (DISABLED schedule) — disable rationale not recoverable from live
  state; neither is HOLD-doc-named; owner ruling needed (T5.A input).
- **HOLD-doc rule applied:** `org/critical_paths/DO_NOT_DECOMMISSION_portal-v2_json_mdpf_49financial_20260722.md`
  was read in full. Everything adjacent to `json/mdpf/**` (the portal publisher cron, the
  `mdpf-legacy-emit-on-demand` SSM doc) is dispositioned **CANONICAL-retained** with that citation —
  the prefix is a live producer input for 49F account counts; halting a writer is a blocked act
  (CTO+COO never-widen co-sign required).

## Diff vs the 07-29 trigger map (drift enumerated, both directions)

| Direction | Entry | Detail |
|---|---|---|
| map-has / live-lacks | `inf-etf-ownership-on-gold-complete` | event rule DELETED — replaced by the row below |
| map-has / live-lacks | `dc2-test1-offpeak-harness` | DISABLED test-harness rule deleted |
| live-has / map-lacks | `inf-etf-ownership-daily-schedule` | cron(0 15 UTC) ENABLED → `inf-etf-ownership-daily`, target id `InfEtfOwnershipDailyScheduledFloor` — event→schedule conversion (NEVER#4-correct direction) |
| live-has / map-lacks | `estate-report-0900et` | Scheduler, DISABLED (ESTATE program, out of MDPF scope) |
| state flip | `seeking-alpha-analysis-daily`, `seeking-alpha-news-daily` | ENABLED→DISABLED (news estate, out of MDPF scope) |

**Otherwise zero drift**: 141/143 baseline rules and 11/11 baseline schedules survive by name with
unchanged states on the MDPF-relevant set. (Live count 142 = 143 − 2 + 1; schedules 12 = 11 + 1.)

## Findings (loud)

1. **F1 — No schedule floor on the MDPF runner chain** (the census-grounded restatement of the memo
   defect). Confirmed live: `mdpf-daily-refresh-trigger` is event-only, and `opal-data-mdpf` itself
   carries ZERO notification/EventBridge wiring, so nothing fires on MDPF artifact writes either.
   Fix vehicle: T2C (staged, mine).
2. **F2 — Repo-vs-applied divergence on the inf-etf-ownership conversion.** The live estate already
   has the scheduled floor (born since 07-29) while the matching TF edit
   (`infra/aws/terraform/inf-pipeline/inf-etf-ownership-daily.tf` + Lambda source) sits UNCOMMITTED in
   the shared working tree. Surfaced to COO+CTO, not adjudicated: owner unestablished by this census.
3. **F3 — comp-estate is stale on the freshness family.** It names `mdpf-freshness-checker` +
   `mdpf-freshness-check-trigger` cron(45 16) + alarm `mdpf-daily-freshness-stale`; all three are
   ABSENT live (Lambda probe ResourceNotFoundException with passing positive control; 142 rules and 51
   alarms materialized contain no `freshness` name). Absent from the 07-29 baseline too — torn down
   before 07-29; the instrument's snapshot lags.
4. **F4 — The hyphen serve plane has no identified trigger-writer.** Serve reads the HYPHEN
   `aggregate-aua-timeseries.json` (comp-routes); no enumerated trigger names it. Writer
   identification is T1.B/T2.B work; the 4-way `account-distribution.json` name collision makes
   name-matching unsafe. Marked UNKNOWN-loud, deliberately.
5. **F5 — The legacy `json/mdpf/**` plane has NO scheduled producer.** Its adjacent writers are an
   on-demand SSM bridge (`mdpf-legacy-emit-on-demand`) and the portal-publisher cron. Given the HOLD
   doc makes this plane a live producer input, its freshness rests on ad-hoc fires — a standing
   fragility for the T2C clock declaration to address explicitly.

6. **F6 — Timing-sensitive edge (DS-provided): runner Stage 6d resolves the cottonwood
   `fact_model_assignment` partition at RUN TIME** (`mdpf-daily-dispatch.sh:521-524`, citation from
   `0.2.0_DS_PortfolioAnalytics` 20260803T211523Z; not independently re-read here — INFERRED at line
   grain). The clock's fire time determines which T-1/T-2 partition the chain sees, so the T2C clock
   must pin fire time relative to the declared silver close.

## What this feeds

- **T1.B** (code-store migration — likely my follow-on): the S3-pull dispatch route is confirmed live
  (`s3://opal-data-mdpf/code/mdpf-daily-dispatch.sh`, 32,077 B @2026-07-23), and CI-R11's record that
  mdpf is NOT in safe-deploy's PIPELINE_MAP still binds.
- **T2.B** (CTO producer-unification ruling): the denominator + disposition table above.
- **T2.C** (mine, activates on this commit): the clock must cover the accrual family (45 15 UTC), the
  feeder pulls (TUE-SAT 03:30 UTC + ET-anchored SmartX 09:00–09:35), the publisher (16:15 UTC), and
  the F5 legacy-plane gap.
- **T5.A** (legacy kill-list): 1 nominated kill candidate + 2 UNKNOWN-loud rows.
