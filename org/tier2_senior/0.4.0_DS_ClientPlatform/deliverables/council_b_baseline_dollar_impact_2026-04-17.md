# Council ~B — 261-Baseline Dollar Impact (post-CUSIP-exemption residual)

**Date:** 2026-04-17 (UTC ~04:35Z)
**Author:** 0.4.0_DS_ClientPlatform~B
**Trigger:** 1.0.0_SA_CTO council correction (20260417T042855Z) — quantify $-impact of ~A's forecast 261-acct baseline after option (d) removes the T+1 overnight UTC inflation. Decision call: material block vs. tolerable silent-closure bridge until WP-9.

---

## TL;DR

**The 261 baseline is NOT tolerable as silent closures.** Point-estimate actual-zeroed MV is **$28–$35M** on the post-CUSIP-exemption residual, or **1.7–2.1% of firm AUA**. Pre-2026-04-15 silent closure at this magnitude was the direct cause of the 3.4% silver/gold firm gap that motivated the halt in the first place. Bypassing the halt now re-introduces the same failure mode.

**Recommendation: (iii) ship option (d) + KEEP halt threshold at 200. Do NOT raise to 500.** Add empirical observation layer + accelerate WP-9 as the structural fix.

---

## 1 — Baseline dollar estimate

### Upstream reference points (from ~A Council, fixed-evidence)

| Incident | Date | Accts | Pre-close MV | Actual-close MV | Halt envelope |
|---|---|---|---|---|---|
| 49F PCRA/SWTC silent | 2026-04-10 | 476 | $39.9M silver AUA | $35.9M non-cash destroyed | N/A (halt did not exist) |
| First halt (pre-CUSIP fix) | 2026-04-15 | 1,307 | $366.6M total | $140–175M | 6.5x / $200 limit |
| **Forecast post-CUSIP-fix residual (~A §5)** | — | **~261 (−80%)** | **~$73M** | **~$28–$35M** | **~1.3x / $200 limit** |
| Tonight (pre-option-d) | 2026-04-17 04:23Z | 1,169 | $182M | ~$95M (midpoint scaled) | 5.8x |

### Derivation

Source math (from ~A §5 + Andrew's Phase 4 math, both citing the 2026-04-15 halt event):
- 1,307-cohort pre-close MV = $366.6M total-account
- Within that, actual-close MV (the subset of each account's MV that would be zeroed by the force-close path) = **$140–175M** (Andrew's bracket)
- CUSIP exemption forecast drop = 80% (residual factor 0.20)
- Linear scale: **261 × ($140–175M / 1,307) = $28–$35M actual-close MV**
- Alternate linear on total MV: **261 × ($366.6M / 1,307) = $73.2M total-account MV** (≈ ~A's headline number)

### Material-block thresholds

| Lens | 261-baseline $ impact | Firm-level ratio | Interpretation |
|---|---|---|---|
| Actual-close MV | $28–$35M | **1.7–2.1% of firm AUA ($1.68B)** | Matches the 3.4% silver/gold gap that motivated 2026-04-15 halt — blowing through 200-limit silently restores exactly the precondition the halt was built to prevent |
| Total-account MV | $73M | 4.3% of firm AUA | Accounts touched; not all zeroed |
| Per-account average actual-close | ~$107–134k | — | Non-trivial per-acct — individual advisor books would show obvious discrepancies |
| Per-day silent accumulation (if threshold raised to 500 and residual stays at 261) | $28–35M / day | — | 10 biz days = **$280–350M silent distortion**, larger than the 2026-04-15 event that motivated the halt |

### Sensitivity / caveats

1. **Forecast is linear extrapolation, not measured.** Actual residual after `ec2c1efc` may land higher than 261 if CUSIP-gap was not the dominant pathology (per ~A §5 reading 1: z0814307721 drill suggests txn-orphan FIFO, not CUSIP drift, is the new dominant sub-pathology). If residual is 400–600 accts, $-impact scales to $43–$80M actual-close.
2. **Not every account in residual is a "phantom."** Some fraction legitimately closed — BD silver/unrealized agrees, Schwab agrees, FIFO lagged. Without the silver/unrealized veto pass cross-check on the 261, we can't partition phantom vs. legitimate. Assume worst case ≥50% phantom (because the halt only fires on accts where >50% of open MV would be zeroed AND the veto did NOT catch them — meaning silver/unrealized also disagrees).
3. **Firm AUA $1.68B is the 49F number from 2026-04-14 doc.** Full-firm AUA is larger (~$2B range per prior bd_canonical math); the 1.7–2.1% ratio is conservative relative to total firm.

---

## 2 — Why "silent closures until WP-9" is not tolerable

### The halt exists specifically because pre-2026-04-15 silent closures at this magnitude produced the 3.4% firm gap

Pre-2026-04-15 behavior shipped 1,307-cohort silent closures to PROD nightly. Downstream signal was a -3.4% silver/gold gap that looked like routine cash/timing drift. Reconciliation did not attribute it back to force-close until the 2026-04-14 diagnostic work (docs/analysis/2026-04-14_fifo_rps_injection_mechanics.md). **The halt was built as the control that makes this visible BEFORE PROD write.** Raising threshold to 500 / overriding silently reintroduces the blindness.

### Linear accumulation math

A single-day $28–35M silent distortion is within historical reconciliation noise. Ten business days at the same rate compounds to $280–350M — larger than the 2026-04-15 event that triggered the halt. There is no ceiling on the duration WP-9 takes to land (BDPL_ASTDIM W4 blocked). Holding the halt is the only durable guardrail.

### Downstream consumer exposure

Phantom-closed FIFO lots feed:
- `gold/timeseries/holdings_lots/{date}.parquet` → BooksTab, Advisor Book, Client Detail drills
- Downstream aggregates via B_03/C_* chain → PartnerAnalytics, AdvisorIntelligence, leaderboards

Per-advisor misses can be bookable-material (advisor with a client in the 261 residual sees their book undercounted by ~$107–134k instantly). Not hypothetical — exactly the 49F PCRA/SWTC pathology that was observed and documented.

---

## 3 — Policy recommendation for CTO / Andrew call

**(iii) ship option (d) + keep halt threshold = 200.** Add three short-term observability layers + accelerate the structural fix.

### Do
- **Ship option (d) (`ec2c1efc`) — done, MATCH on S3, PROD picks up next boot.** Removes T+1 UTC inflation. Post-fix residual will tell us whether 261 forecast is accurate (reading 2/3) or inflated by a new sub-pathology (reading 1).
- **Keep `BD_FORCE_CLOSE_LIMIT=200`.** It is the only guardrail that attributes silent distortion to a specific cohort before PROD write.
- **Single `BD_FORCE_CLOSE_OVERRIDE=1` QA run AFTER `ec2c1efc` is loaded** (per ~A §8 rec 6). Capture: post-close silver/gold firm delta, per-advisor book delta for top-affected advisors, per-acct actual-close MV distribution. This is the empirical measurement that converts the forecast into fact. Scope: qa-runner only, single run, full diagnostic logged to parquet — not PROD.
- **Wire WP-10b gold↔silver recon harness into nightly.** Currently shipped (cff234b5) but not wired into `gold_dispatch` post-step. Once wired, firm-level silver/gold delta is quantified every night independent of B_01's own diagnostic. Turns the question "is 261 tolerable?" into a daily observable instead of a forecast.
- **Accelerate BDPL_ASTDIM W4 → WP-9.** Structural fix is CUSIP-keyed FIFO replay. Every tactical patch to date is a defensive layer around `(account_id, asset_name)` keying defect. W4 status check is the critical dependency.

### Do NOT
- **Do NOT raise halt threshold to 500 as a bridge.** That is equivalent to "ship silent closures at $28–$35M/day rate indefinitely" — the exact precondition the halt exists to prevent. No valid bridge exists that silently accepts the baseline residual until WP-9 lands.
- **Do NOT `BD_FORCE_CLOSE_OVERRIDE=1` in PROD.** QA only, single run, diagnostic capture. Applying it in PROD writes zeroed holdings_lots to the downstream consumer surface.

### Bridge options ranked by trade-off

| Option | Detection | Distortion risk | Effort | Reversibility |
|---|---|---|---|---|
| (iii) keep 200 + observability (recommended) | Halt fires, portal freezes at last-good | None — no distortion written | Low | Always reversible (halt is a gate, not a write) |
| (iii-lite) keep 200, no observability | Halt fires | None | Zero | Same as above |
| Raise to 500 | Silent at 261 | $28–35M/day firm-level | Zero | Detection lost — distortion is downstream within one night |
| Override=1 in PROD | No halt, silent | Full $28–35M single-run | Zero | Needs reconciliation pass to identify which lots got closed |
| Override=1 in QA only | No halt, measured | Zero PROD risk | Low | Provides the empirical measurement option (iii) lacks |

---

## 4 — Confidence + open questions

**Confidence:** medium-high on the magnitude band ($28–$35M actual-close point estimate; upper sensitivity $43–$80M if residual > 261), high on the recommendation (block vs. raise threshold). The underlying $140–175M actual-close bracket is from Andrew's 2026-04-15 Phase 4 math against the full 1,307 cohort — the linear scale-down to 261 is the extrapolation.

**Open questions (would sharpen the estimate):**
1. **What is the silver/unrealized veto hit rate on the 261 forecast?** If veto catches N of the 261, only (261 - N) are phantom closures. Needs post-`ec2c1efc` QA residual to measure.
2. **Is the residual pathology CUSIP-gap (covered by `8eda12a3`) or txn-orphan FIFO (new)?** ~A reading 1 suggests txn-orphan is dominant. If true, a new exemption is needed — and the $-impact number may understate.
3. **Firm full AUA (not 49F-only).** The 1.7–2.1% ratio uses $1.68B (49F silver). Full-firm number sharpens the materiality framing.

**Time-to-sharpen:** 30–60 min on QA `BD_FORCE_CLOSE_OVERRIDE=1` single run with full diagnostic capture. Recommend as ~A §8 rec 6 calls out.

---

## 5 — Connection to ~A + ~C findings

- **~A (historical):** this is the 5th escalation of `(account_id, asset_name)` keying drift between FIFO and RPS. Every tactical patch to date is defensive. WP-9 is the structural fix; blocked on BDPL_ASTDIM W4. My $-impact math operates against ~A's forecast residual, not against tonight's pre-option-d 1,169.
- **~C (Schwab-side) — as corrected by CTO T042855Z:** RPS feed is ALIVE in canonical `opal-data-schwab` bucket (partitions through 2026-04-15). ~C's original finding applied to the dead secondary mirror `opal-data-bd/schwab/*`. T+1 delivery cadence explains 2-day staleness during overnight ET runs — which is exactly what option (d) corrects by aligning snapshot_date to latest silver/allocations.
- **Synthesis framing:** (a) option (d) is the overnight-UTC-drift fix, (b) tonight's 1,169 halt is pre-`ec2c1efc` behavior, (c) 261 is the forecast post-`ec2c1efc` residual, (d) 261 at $28–$35M/day silent is NOT tolerable, (e) WP-9 is the terminal fix, (f) empirical QA override run is the recommended bridge to convert forecast into observed.

---

## 6 — Compiler tools / evidence trail

| Tool | Command | Result |
|---|---|---|
| `comp-pipescript deployed B_01` | — | MATCH (session_i, 2 MATCH, 0 STALE, 0 MISSING). Confirms `ec2c1efc` is on S3 — PROD next boot loads the fix. |
| `comp-pipescript io B_01` | — | READS `accounts_dimension_latest`; WRITES `holdings_lots/{date}.parquet` + 3 shadow/backfill keys. No COLUMN GAPS. |
| git log / Read | `docs/analysis/2026-04-14_fifo_rps_injection_mechanics.md` L1–80 | Pulled firm AUA ($1.68B 49F) + 476-acct $35.9M non-cash ref point. |
| Read | `deliverables/council_a_historical_2026-04-17.md` §5 | Pulled forecast table (261 / ~$73M / 1.3x envelope) + 1,307 / $366.6M / $140–175M actual-close bracket. |
| Read | `B_01.holdings_lots.py` L2085–2109 + L1578–1595 | Confirmed option (d) shipped at both snapshot_date touchpoints. |

No `comp-blast` run this pass — scope is dollar-impact analysis, not code-change. ~A ran `comp-pipescript io` and `comp-blast` survey in council_a_historical; no duplication warranted.

---

## 7 — RAVC

- ACK delivered to 1.0.0_SA_CTO at 20260417T042939Z (in response to COUNCIL CORRECTION T042855Z).
- COMPLETE delivered with this deliverable path.
- Scope held: 261-baseline $-impact quantification + block-vs-bridge recommendation. No lane overlap with ~A (historical/code) or ~C (Schwab-side) or ~D (synthesis).
