# Council ~D — Structural / Decision Framework

**Agent:** 0.4.0_DS_ClientPlatform~D
**Date:** 2026-04-17 (UTC ~04:27Z)
**Trigger:** `1.0.0_SA_CTO` council dispatch `20260417T041138Z` + council update `20260417T042454Z`.
**Scope:** Synthesize ~A (historical), ~C (RPS forensics), ~B (BD-txn forensics, pending) into (i) decision tree tonight, (ii) ONE recommended path, (iii) TO list, (iv) halt threshold policy.

---

## TL;DR — Recommendation

**Tonight: LET THE HALT FIRE. Do NOT override. Do NOT raise the threshold.**

File **four TOs** in priority order:

1. **[AE, P0] Restore Schwab RPS ingestion** — diagnose why `CRS2026041x.RPS` stopped landing in `s3://opal-data-bd/schwab/bronze/` and backfill 04-08 through 04-17. This is the root cause; every other remediation depends on it.
2. **[DS, P0 gate on #1] Post-restore holdings_lots backfill audit** — once RPS data is current, rebuild holdings_lots parquets for 04-08 onward and quantify the corruption that slipped out under pre-halt silent force-close (i.e., before 04-15). Write a reconciliation manifest per date.
3. **[DS, P0] Add RPS-age heartbeat guard to B_01** — before any `_apply_rps_lot_corrections` call, if `rps_date < snapshot_date - N days` (N=2 proposed), RuntimeError with a "FEED STALE" message. Replaces the inline `match=YES/NO` print with a hard gate. This is the alert we should have had 10 days ago.
4. **[AE, P1] Schwab ingest dead-man-switch alarm** — CloudWatch/SNS alarm on `schwab/bronze/CRS*.RPS` absence for 48h+. Independent of B_01. Owner: whoever owns `schwab-feed-ingest` (AE to triage).

**Halt threshold:** keep at 200. ~C's finding confirms `717764fe`'s 200 was correct — it caught a real upstream data-pipeline failure. Do not relax.

---

## 1 — The Root-Cause Reframing

**Pre-~C framing (CTO initial diagnosis):** 1,169 accounts is *steady-state* FIFO-vs-RPS drift that has silently force-closed every night since weeks ago. Envelope is routine; safety halt threshold is too tight.

**Post-~C framing (this council):** 1,169 accounts is **10 days of legitimate BD trading activity that RPS cannot confirm because the Schwab RPS feed went dark on 2026-04-07**. The envelope is *not* routine. The safety halt is *not* too tight — it caught a data-pipeline failure precisely as designed.

The two framings have opposite remediation:
| Framing | Action |
|---|---|
| Steady-state drift | Override tonight, raise limit, file long-term TO, ship portal |
| Feed-outage staleness | Let halt fire, restore upstream, audit corrupted outputs, keep limit |

**~C provides three independent proofs** for the feed-outage framing, each sufficient on its own (deliverable council_c §1):

1. **Direct absence:** `aws s3 ls s3://opal-data-bd/schwab/bronze/` confirms no `CRS2026041x.RPS` file for any date 04-08 through 04-17. Last bronze: `CRS20260407.RPS` uploaded 2026-04-08T22:02:36Z.
2. **Silent fallback mechanism:** `B_01.holdings_lots.py:_load_latest_rps_partition()` L434-448 sorts all partition keys and takes the last one — when the newest is 10 days old, no guard fires.
3. **RPS structural stability (when fresh):** 99.9% account-cohort stability across sampled 3/27, 4/02, 4/07 partitions; mean per-account position Jaccard 0.982. The feed is not structurally gappy for these accounts; it is *absent*.

**Plus ULN as control:** Silver ULN partitions exist through 04-13 (backfilled 04-15). Schwab ingest is *partially* alive — RPS specifically is dead, not the entire Schwab path. This narrows the AE remediation scope significantly.

---

## 2 — Why Pre-~C Readings Converge on the Same Tree

~A's historical analysis (council_a §5) lists three readings of tonight's 5.8x envelope:
- (a) txn-orphan FIFO
- (b) legitimate triple-source agreement
- (c) pre-`ec2c1efc` runner SHA / snapshot_date drift

~A's own §4 Phase 3 post-mortem explicitly names "stale RPS partition" as `717764fe`'s **first-listed** root-cause hypothesis — literally hard-coded into B_01.L1176-1178's error message. ~C's finding is the direct observation of that hypothesis, weighted by 10-day duration.

Reading (c) is partial — `ec2c1efc` snapshot_date fix was shipped but wouldn't have prevented tonight's halt because the RPS partition it would realign to (04-15 or 04-16) *doesn't exist*. Even a perfectly-aligned snapshot_date still falls back to the 04-07 partition via `_load_latest_rps_partition`.

Reading (a) txn-orphan FIFO cannot be *fully* ruled out without ~B's deliverable, but is structurally subsumed by (c+stale-RPS): if RPS had been current 04-15, the z0814307721 drill case would have shown its 04-08-through-04-15 transactions backed by Schwab RPS rows, and FIFO "orphans" would resolve to live positions.

**Synthesis:** tonight's halt is **primarily** (c+) stale-RPS-partition, not (a) txn-orphan FIFO. ~A's recommendation #1 ("confirm runner SHA at tonight's boot") loses priority — the root cause sits upstream of the SHA, in the ingest layer.

---

## 3 — Decision Tree (tonight, PROD fires ~04:23Z and has halted)

| Option | What happens | Data integrity | Ops discipline | Portal freshness | Tech debt |
|---|---|---|---|---|---|
| **(i) Override** `BD_FORCE_CLOSE_OVERRIDE=1` on PROD | B_01 runs, writes 2026-04-16.parquet with 1,169 legitimate BD positions force-closed to zero because frozen RPS can't see them. Downstream aggregates drop by ~$182M artificially | CATASTROPHIC — we silently ship $182M of phantom closes into partner-analytics, leaderboards, advisor books | BAD — reverses the safety-halt design intent the first time it tripped on the real thing | Portal shows artificially low NNA/AUA for affected accounts | Compounds — every overrun run past RPS outage adds another day of corrupted parquets to reconcile later |
| **(ii) Raise `BD_FORCE_CLOSE_LIMIT` to 2,000** | Same as (i) but via a different knob. Halt stops firing until cohort > 2,000. Envelope grows linearly per day RPS stays dead | Same as (i), plus now the halt is disarmed for subsequent pathologies | BAD — moves goalposts in response to a correctly-firing guard | Same as (i) | Same as (i) |
| **(iii) Let halt fire tonight, no PROD write** | 2026-04-17.parquet remains 404. Portal freezes at last good parquet (likely 2026-04-07, the last RPS-current run) for ~24-48h until RPS restored | CLEAN — zero corruption shipped tonight | GOOD — guard works, we don't bypass | Stale by 2-10 days depending on last good parquet date, but NO false data | LOW — gives AE time to fix root cause |
| **(iv) Switch B_01 source-of-truth to silver/unrealized for this cohort** | Skip RPS sell-corrections entirely; trust BD's own silver/unrealized as authoritative | Moderate — silver/unrealized has its own known gaps (49F PCRA/SWTC per ~A §Phase 1) but is fresher than 04-07 RPS | Risky — unproven as primary source | Better than (iii), worse than (i+fix) | HIGH — large code-path change in a hot window |

**Clear recommendation: (iii) — let halt fire.** (i) and (ii) both ship known-false data. (iv) is too big a change under deadline pressure; sleeve shadow emit (ADVI_ROLLUP.SL-P1) is the right long-term path to a second authoritative source, but is Phase 1 of 4 and not ready.

**Portal staleness cost is real but acceptable:** last known clean PROD `holdings_lots` parquet is likely 2026-04-07 (pre-RPS-outage). Every parquet 04-08 through 04-14 was written under pre-halt behavior — force-closed silently against an already-stale 04-07 RPS for days 04-08 through 04-14, each progressively more corrupted. 04-15 and 04-16 were 404 (halt fired, no write). Portal is therefore *already* stale by ~10 days functionally; letting tonight's halt fire extends that by 1 day to ~11.

---

## 4 — The Downstream Corruption Problem (non-negotiable)

`holdings_lots/2026-04-08.parquet` through `holdings_lots/2026-04-14.parquet` were written under pre-halt behavior. Each of those seven writes force-closed 10 days of legitimate BD transactions against an RPS partition that was *itself* stale on the day of write (RPS of 04-07 used for each of 04-08 through 04-14).

These seven parquets feed every downstream gold script:
- `C_08.advisor_fee_efficiency` → advisor leaderboards
- `07_build_nna_aua_by_geography` / `08_build_nna_aua_by_advisor` → PartnerAnalytics
- `09_generate_partner_analytics` → portal header metrics
- `10_generate_advisor_rolling_flows` → AdvisorsTab 88MB payload

All seven downstream artifacts derived from these parquets are **silently tainted** — portal already shows artificially deflated NNA/AUA for the 1,169-account cohort. Tonight's halt stops the taint from extending to 04-16 but does not repair 04-08 through 04-14.

**This is TO #2 (Post-restore backfill audit).** Must run after AE restores RPS; the backfill depends on having fresh RPS partitions 04-08 through 04-17 to rebuild correctly. Emit a per-date reconciliation manifest: pre-halt vs post-backfill MV delta per account.

---

## 5 — Full TO List (in priority / dependency order)

### TO 1 — `ADVI_FEEDRS.R01.ae-restore-schwab-rps-ingestion` (P0, AE, open now)

**Scope:** Diagnose why `CRS2026041x.RPS` bronze upload stopped on 2026-04-08. Restore ingestion. Backfill bronze partitions for 04-08 through 04-17 from Schwab source. Confirm silver/rps partitions follow.
**Owner:** 0.6.0_AE_PartnerETL (escalation from 0.4.0 pod)
**Acceptance:** `aws s3 ls s3://opal-data-bd/schwab/bronze/CRS*.RPS | tail -15` shows files for every business date 04-08 through today. `aws s3 ls s3://opal-data-bd/schwab/silver/rps/` shows matching silver partitions.
**Blocks:** TO 2 and TO 4.
**Time estimate:** unknown — depends on why ingestion stopped (credential expiry? network? Schwab-side?). AE triage needed.

### TO 2 — `ADVI_FEEDRS.R02.ds-rebuild-holdings-lots-backfill` (P0, DS, gated on TO 1)

**Scope:** Once RPS is restored for 04-08 through 04-17, rebuild `holdings_lots` parquets for 04-08, 04-09, 04-10, 04-13, 04-14, 04-16, 04-17 (business days only; 04-15 already 404). Each run: `aws lambda invoke bd-gold-trigger --payload '{"mode": "incremental", "date": "YYYY-MM-DD"}'`. Emit per-date manifest: pre-backfill vs post-backfill MV, account_count, affected-cohort delta.
**Owner:** 0.4.0_DS_ClientPlatform
**Acceptance:** 7 fresh parquets written. Per-date reconciliation manifest in `data/black_diamond/diagnostics/rps_outage_backfill_recon_2026-04-17.json`. Firm-level MV delta reported to CTO.
**Depends on:** TO 1 complete.
**Time estimate:** 1-2 days (each run is ~30-60 min B_01 alone, more if full-mode needed).

### TO 3 — `ADVI_FEEDRS.G01.ds-rps-age-heartbeat-guard` (P0, DS, parallel to TO 1)

**Scope:** Add a pre-correction guard to `B_01.holdings_lots.py` that RuntimeErrors if `(snapshot_date - rps_date).days > N` where N=2 (business days). Message: `"RPS FEED STALE: loaded rps_date=YYYY-MM-DD, snapshot_date=YYYY-MM-DD, gap=X days. Feed likely dead. Check s3://opal-data-bd/schwab/bronze/ for latest CRS*.RPS upload."`. Override via `BD_STALE_RPS_OVERRIDE=1` (distinct from `BD_FORCE_CLOSE_OVERRIDE`). Fires *before* `_apply_rps_lot_corrections` is called, not after. Unit tests: (a) fresh RPS (gap=0) passes, (b) stale RPS (gap=5) halts, (c) override=1 + stale passes with warning.
**Owner:** 0.4.0_DS_ClientPlatform
**Acceptance:** py_compile clean; `comp-pipescript deployed B_01` MATCH post-upload; QA run with frozen 04-07 RPS halts; QA run with fresh RPS passes; runbook entry added.
**Ship after TO 1 is resolved (to avoid halting during the restore window).**
**Time estimate:** 2-4 hours. Low-risk change.

### TO 4 — `ADVI_FEEDRS.G02.ae-schwab-ingest-deadman-switch` (P1, AE)

**Scope:** CloudWatch alarm (or SNS topic + Lambda) that checks S3 `schwab/bronze/CRS*.RPS` every 4h. Alarm on: no new object for >48h. Route to on-call / Slack. Independent of B_01 — catches outage *before* nightly gold run notices.
**Owner:** 0.6.0_AE_PartnerETL
**Acceptance:** Alarm defined in Terraform; test trigger (simulated 48h absence) fires alarm; operator acknowledges alarm in channel.
**Time estimate:** 4-8 hours.

### TO 5 — `ADVI_FEEDRS.O01.ds-standalone-force-close-diagnostic` (P2, DS) — from ~A recommendation #3

**Scope:** Promote B_01 inline diagnostic to standalone `E_25.rps_force_close_audit.py`. Emits `gold/diagnostics/rps_force_close/{date}.parquet` with columns `account_id, closed_accts_count, closed_mv, veto_applied, cusip_gap_applied, residual_cohort_tag, rps_partition_date, rps_age_days`. Reads same inputs as B_01 but writes a persistent parquet instead of stdout print. Runs as post-step after B_01.
**Owner:** 0.4.0_DS_ClientPlatform
**Acceptance:** Parquet emitted; columns populated; nightly dispatch updated.
**Time estimate:** 1-2 days.

---

## 6 — Halt Threshold Policy Revision

**Recommendation: keep `BD_FORCE_CLOSE_LIMIT=200`. Do NOT raise.**

Reasoning:
- `717764fe` set 200 to catch *real* incidents, and it caught one — tonight. A higher threshold would have silently shipped the RPS-outage corruption.
- ~C's stability data shows RPS account churn is ~18 accounts over a 10-day window (0.3%) when data is current. Steady-state force-close cohort should be tiny (<50 accounts), so 200 is already a generous 4x buffer.
- The CTO initial diagnosis assumed "1,169 is steady-state" but ~C disproved that: pre-outage, the halt would *not* have fired at all (cohort was small). The post-outage cohort is large only because RPS is stale.

**What to add instead of raising the threshold:**
- TO 3 — RPS age heartbeat fires *before* the force-close count is computed. The age-gap catches outages at gap=1-2 days, long before the cohort grows to 200.
- (Optional, P2) Emit a 7-day rolling average of force-close cohort size; alert on `current > 2 × rolling_avg`. Separates real growth from noise. Not required if TO 3 ships.

---

## 7 — Observability Gap (meta-finding from ~C)

**10 days of silent feed outage is the real headline.** No process caught it. `B_01` saw the stale date and fell back silently. Portal shipped progressively corrupted partner-analytics for 10 days. The halt only caught it at day 10 when the cumulative drift exceeded the already-existing 200 threshold.

This is an operational gap that transcends any single fix:

| Layer | What should have alerted | Whose gate |
|---|---|---|
| Schwab ingest | Bronze file absence >24h | AE / whoever owns schwab-feed-ingest |
| B_01 pre-correction | `rps_age_days > 2` | DS (TO 3) |
| Portal publisher | AUA/NNA week-over-week delta >5σ | DE / pipeline owner |
| Exec dashboard | Pipeline freshness by feed-source | SA / CTO |

**TO 4 addresses the first layer only.** The other three are follow-ups outside tonight's scope but should land on SA/CTO backlog.

---

## 8 — Open Questions (pending ~B)

~B's BD-transaction forensics deliverable is pending at time of ship. The council update reframed ~B's task to:

1. **Validate ~C's finding:** spot-check that BD transactions 04-08 through 04-15 for the flagged accounts are legitimate trades (not duplicate/error entries).
2. **Quantify the pre-halt corruption:** how much $MV was silently force-closed across all runs since 04-08? (Rough upper bound = 1,169 accounts × $182M / 10 days × 7 days ≈ $127M cumulative silent closes, but actual per-day cohort was likely smaller pre-drift-compounding.)

**If ~B confirms legitimacy:** no change to this recommendation. If ~B finds a material fraction of BD transactions are erroneous (e.g., duplicate buys without sells), a separate P1 TO should be added to flag/fix the BD transaction feed itself — but this does NOT alter tonight's decision to let the halt fire.

---

## 9 — One-sentence summary for Andrew

> Schwab RPS feed has been dead for 10 days, the halt caught it tonight exactly as designed, don't override — let the halt fire, restore RPS ingestion, backfill 04-08 through 04-17, and keep the 200 threshold because lowering it further isn't necessary once we add an RPS-age heartbeat that would've alerted us on day 1.

---

## 10 — Compiler Tools

| Tool | Command | Result | Note |
|---|---|---|---|
| Read | council_a_historical_2026-04-17.md (230 lines) | Full | Primary ~A input |
| Read | council_c_rps_coverage_2026-04-17.md (~600 lines) | Full | Primary ~C input |
| Read | CTO dispatch `20260417T041138Z` + update `20260417T042454Z` | Full | Assignment + reframing |
| Read | CTO diagnosis `20260417T040552Z` | Full | Pre-~C hypothesis — now superseded |
| Read | ~A session_j_council_a_historical_forensics.md | Full | ~A self-observation of partial-stale overlap |
| `comp-pipescript io B_01` | not re-run | — | ~B ran fresh at session_i 04:17Z; ~A cited; no DS write this pass |
| `comp-blast B_01` | not re-run | — | Synthesis-only; no code change this deliverable |

This is a synthesis deliverable only — no code change, no S3 upload, no bd-gold-trigger invocation from lane ~D this pass.

---

## 11 — MCP / RAVC

- ACK to CTO: `20260417T042728Z`.
- ACK stand-down-on-option-(d) to COO: `20260417T041527Z` (prior; unrelated to this synthesis).
- MCP COMPLETE to 1.0.0_SA_CTO + 2.0.0_SA_COO on ship of this deliverable.
- `~D` scope strictly synthesis. No lane overlap with ~A (historical), ~C (RPS forensics), or ~B (BD-txn forensics, pending).
