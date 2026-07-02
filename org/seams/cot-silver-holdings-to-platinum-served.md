# SEAM: cot silver/holdings (snapshot) -> gold-canonical -> platinum served -> freshness alarm   (scale: MACRO)
**archetype:** DIAGNOSE (+ VALIDATE)
**run:** 0.4.0_DS_ClientPlatform~C · 2026-07-02 ~1957Z · ADVI_COTETL WS-2b · `/seams check`
**grounding:** every axis below cited against LIVE S3 / deployed lambda / live CloudWatch (this session), not source-belief.

## Seam definition
The MACRO "silver -> platinum served" chain whose served output (cot firm AUA, the #1 portal
surface) is content-frozen at 2026-06-30 while the pipeline runs fresh nightly. Decomposed into
4 constituent seams; **weakest-seam-binds**.

- **Expected contract:** served `platinum/firm/*.json` `data_as_of` advances to the last settled
  trading-day frontier each nightly, and if it does NOT, the `bd-cot-served-aua-stale` alarm pages
  (Andrew email + COO /drive SQS rider) rather than going silent.
- **Contract recorded in:** `data/cot/scripts/gold/gold_freshness_config.yaml` (freshness registry);
  `infra/aws/terraform/cot-pipeline/cot-detection-layer.tf` (the L4-GUARD detection layer).

---

## Constituent seams + axis verdicts

### S1 — vendor `HOLDINGS_DAILY_*.xlsx` -> `forwardfill_v2/holdings/` -> `silver/holdings/`
| Axis | Verdict | Evidence |
|---|---|---|
| MECHANICAL | PASS | 07-02 ingest fetched + silver-merge converted the newest export (silver-run log `cot-silver-run-20260702-020412.log`: holdings leg OK, `HOLDINGS_DAILY_2026-06-30.xlsx` -> `silver/holdings/2026-06-30.parquet` 11,453 rows). Auth/fetch work — txn/realized got 07-02 files the same run. |
| DECLARATIVE | PASS | holdings is a documented NON-GATING sentinel-decoupled daily leg (`cot-pipeline/ssm.tf:201-213`); matches behavior. |
| SEMANTIC | **STALE-INPUT** | The payload is the newest the VENDOR published = data-date **06-30**. `silver/holdings/2026-07-01.parquet` ABSENT (live ls: max partition 06-30). 2 trading-days behind the 07-02 frontier. This is an UPSTREAM INPUT property (Cottonwood/BD holdings export lag), not a seam defect — the seam carries faithfully what exists. |

### S2 — `silver/holdings/` -> `gold/canonical/holdings/` + NNA date-axis (B_00, snapshot-first)
| Axis | Verdict | Evidence |
|---|---|---|
| MECHANICAL | PASS | B_00 `_cot_snapshot_dates()` lists `silver/holdings/` (`B_00.canonical_holdings.py:106-118`), `_build_canonical_from_snapshot()` writes canonical (`:121-151`). Gold-run log `cot-gold-run-20260702-020514.log:276` "canonical holdings from silver/holdings ... skipping positions-FIFO", `:293` "16 date(s)", `:296` "[auto] latest canonical: 2026-06-30". |
| DECLARATIVE | PASS | COT snapshot-first is documented (B_00 docstring `:121-125`; gold-run log `:318` "nna date-axis from canonical_holdings ... nna VALUE stays transaction-derived"). Map == territory. |
| SEMANTIC | PASS (faithful) | Gold canonical frontier = **06-30** = a FAITHFUL reflection of the 06-30 holdings-snapshot input. `gold/canonical/{nna,holdings,positions_cube}` max partition = 06-30 (live ls). No defect introduced. |

### S3 — `gold/canonical` -> `gold/artifacts` (D_00) -> `platinum/firm/*` (D_04 verbatim)
| Axis | Verdict | Evidence |
|---|---|---|
| MECHANICAL | PASS | D_00 stamps `data_as_of`; D_04 `build_firm_pass_throughs()` promotes verbatim (`D_04.client_portal_summary.py:2543-2585`). |
| DECLARATIVE | PASS | D_04 docstring "Content is passed through verbatim -- no reshape" (`:2553-2554`); confirmed live — platinum & `gold/artifacts/summary/header_metrics.json` share `generated_at=2026-07-02T02:06:12Z`. |
| SEMANTIC | PASS (faithful) | Served `platinum/firm/{header_metrics,timeseries_chart,timeseries_overview}.json` all carry `data_as_of=2026-06-30`, timeseries blocks end 06-30 (63 rows) — a FAITHFUL propagation of the 06-30 canonical frontier. D_00/D_04 are NOT the bug. |

### S4 — served platinum -> `bd-cot-freshness-probe` -> `AUADataAsOfLag` -> `bd-cot-served-aua-stale` alarm -> operator/COO  **(the MONITORING seam — WHERE THE FINDING IS)**
| Axis | Verdict | Evidence | Delta |
|---|---|---|---|
| MECHANICAL | PASS | Probe reads `SERVED_AUA_KEY=platinum/firm/timeseries_overview.json` (exists, live `data_as_of=2026-06-30`), `_served_aua_lag()` computes `_trading_days_behind(06-30, expected=07-02)=2` (`bd-cot-freshness-probe/lambda_function.py:246-264, 172-183`), emits `AUADataAsOfLag`. Live alarm datapoint = **2.0** @ 07-02T01:27Z. Wiring carries; probe is CONTENT-grounded by design (docstring `:251-252` "a gold re-run rewrites the file while data_as_of stays frozen ... the 06-22 case"). | — |
| DECLARATIVE | **FAIL** | `gold_freshness_config.yaml:119` note: "threshold 2 matches the alarm." LIVE alarm `bd-cot-served-aua-stale` = `GreaterThanThreshold(2.0)` -> pages only at **>2 (3+ td)**. comp-freshness WARNs at **>=2**. The threshold VALUE matches (both 2) but the BOUNDARY diverges: at lag=2 comp-freshness WARNs, the alarm is SILENT. The note implies WARN<->page parity that does not hold. | believed: WARN@2td == alarm@2td; actual: WARN fires @2td, alarm fires @3td (1-td silent gap). Materialized LIVE this run — comp-freshness WARNed on 06-30, alarm stayed OK. |
| DECLARATIVE (2) | **NOTE** | comp-freshness registry watches `header_metrics.json` + `timeseries_chart.json` (`gold_freshness_config.yaml:113,122`); the ALARM probe watches a THIRD key `timeseries_overview.json` (`cot-detection-layer.tf:308`). All three are 06-30 (consistent today), but the tool and the alarm cover DIFFERENT served keys — a coverage-declaration gap worth reconciling. | tool != alarm on WHICH served object is authoritative. |
| SEMANTIC | **FLAG (tolerance-vs-defect — CTO H1)** | The signal crossing to operator/COO is "all-clear" while served AUA is genuinely **2-td stale**. Defensible-by-design: BD prices T+1, so 1-td lag is the unavoidable floor -> the >2 page-point tolerates normal(1)+one(2), pages at the third. So 2-td = soft-WARN band (comp-freshness), not yet page. NOT a clean defect — but whether the #1 served surface sitting 2-td-frozen SHOULD page is the open **H1** decision (CTO-gated). Expected(if intended-loud): page@2td; Actual: silent@2td. | signal="clear" vs truth="2-td frozen"; tolerance band, CTO rules. |

---

## Knowledge-parity delta
- **BELIEVED:** platinum content-staleness implies a gold/platinum producer bug or a broken chain;
  and (per config note) the served-AUA alarm catches any 2-td staleness comp-freshness WARNs on.
- **TRUE (grounded):** (1) the data seams S1–S3 are SOUND and faithfully propagate an UPSTREAM
  vendor holdings-export lag (06-30) — no producer bug; (2) the served-AUA alarm PAGES at >2 td
  while comp-freshness WARNs at >=2 td — a 1-td silent gap the config note misrepresents as parity;
  the current 2.0-td freeze sits exactly in that gap.
- **Record correction (declarative repair) — DEFERRED, coupled to H1:** the `gold_freshness_config.yaml:119`
  note should state the >=2-WARN / >2-page boundary offset explicitly. Its CORRECT final wording
  depends on CTO's H1 ruling (tighten alarm to >=2 -> note becomes literally true; keep >2 as intended
  T+1 tolerance -> note needs the offset clarification). Landing it preemptively could contradict H1;
  per COO+MSTR "no change before the arch-gate," it lands WITH H1. Routed to CTO.

## Verdict
- **Data chain (S1->S2->S3): SOUND** on all three axes — the platinum 06-30 content is a faithful,
  correct propagation of a stale UPSTREAM input, not a seam break.
- **Monitoring seam (S4): BROKEN@DECLARATIVE** (config note asserts a WARN/page parity that is false;
  tool/alarm watch different served keys) + **FLAG@SEMANTIC** (2-td-frozen #1 surface is silent-by-threshold;
  page-vs-tolerate is the CTO H1 decision).
- **MACRO pipeline verdict = its weakest seam = S4: the served-staleness is CORRECTLY DETECTED
  (probe emits 2.0) but INCORRECTLY UN-SURFACED (alarm silent at 2-td) and MIS-DOCUMENTED (parity note).**
  The bug is not that platinum is stale (it faithfully mirrors a vendor lag) — it is that a 2-td freeze
  of the #1 served surface reaches nobody loudly, and the record says it would.

## grounding: (Rule 22 — per causal claim)
- "platinum content 06-30 BECAUSE the gold frontier pins to max(silver/holdings)=06-30 (snapshot-first) and
  the newest vendor HOLDINGS export is 06-30": **grounding: SOURCE-CONFIRMED** — `B_00.canonical_holdings.py:106-151`
  + gold-run log `:276/:296/:318` + silver-run log holdings leg ("Data date ... 2026-06-30") + live `forwardfill_v2/holdings/` newest=`HOLDINGS_DAILY_2026-06-30.xlsx` + `silver/holdings/2026-07-01.parquet` ABSENT.
- "the 2-td freeze is served-SILENT BECAUSE the alarm is GreaterThanThreshold(2.0) (pages at 3+ td)":
  **grounding: SOURCE-CONFIRMED** — live `describe-alarms` (Threshold 2.0, GreaterThanThreshold, datapoint 2.0
  StateReason "not greater than the threshold") + `bd-cot-freshness-probe/lambda_function.py:246-264,172-183`.
- "MTIME-fresh/content-stale BECAUSE holdings is non-gating/sentinel-decoupled -> nightly re-runs fresh-mtime
  on frozen 06-30": **grounding: SOURCE-CONFIRMED** — `cot-pipeline/ssm.tf:201-213` (`_SILVER_STAGE_TABLES`
  excludes holdings; `{ ... || echo NON-GATING; }`).

## Residual / unknowns
- The `bd-cot-freshness-probe` lambda was read from the REPO source (`infra/aws/lambda/cot-pipeline/...`),
  not the deployed zip; behavior cross-EVIDENCED by the live emitted datapoint (2.0) matching the source
  computation `_trading_days_behind(06-30, 07-02)=2`. Exercise-or-evidence: SATISFIED via the live metric.
- H1 (alarm threshold tune) + the config-note correction are DEFERRED to CTO's arch-gate (infra/AE lane +
  DS-doc repair, landed together). NO change made this run.
- alloc/unrealized 0-row (chronic; Andrew-flagged) is a SEPARATE seam (silver/{allocations,unrealized} ->
  C_04/C_02/B_00) — routed to COO as a follow-on WS candidate; not folded here.

## Compiler Tools
- `comp-freshness chain cot` — surfaced the S3->S4 symptom (platinum WARN, MTIME-FRESH/CONTENT-STALE).
- `comp-which` — routed the platinum-stale question (near-tie: comp-freshness/comp-xray/comp-lambdamap).
- Live grounding via `aws s3`/`aws cloudwatch describe-alarms`/`aws events describe-rule` (rail-checked:
  partition-date, alarm-threshold, EventBridge-state — lineage/live-state questions no comp tool surfaces).
