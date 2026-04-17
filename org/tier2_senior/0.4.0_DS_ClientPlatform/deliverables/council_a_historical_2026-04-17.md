# Council ~A — Historical / Existing-Code Angle

**Date:** 2026-04-17 (UTC ~04:25Z)
**Author:** 0.4.0_DS_ClientPlatform~A
**Trigger:** 1.0.0_SA_CTO council dispatch 20260417T041138Z — 1,169 accounts / $182M / 5.8x envelope safety halt on QA and PROD.
**Question:** Has this phantom-transaction / force-close scenario been diagnosed before? What does institutional knowledge say?

---

## TL;DR

**Yes. This exact pattern has been diagnosed and patched iteratively across ~4 weeks.** Tonight's halt is the **fifth** escalation of the same root mechanism — `B_01._build_rps_synthetic_lots` misinterpreting "absence of an RPS row" as "evidence of a sale." The 1,169-account / $182M envelope is **smaller than 2026-04-15's 1,307-account / $366M incident** (which itself motivated the safety halt), so the halt is doing its job. What the halt does NOT answer is whether the residual cohort is a new failure mode or the long-tail residue of the CUSIP / veto fixes.

**Institutional knowledge says:** this is not fresh drift. It is a structural `(account_id, asset_name)` keying problem between FIFO-derived lots and Schwab RPS, with at least five known sub-pathologies (PCRA sleeves, Schwab Trust Bank, joint/trust sub-masters, CUSIP-bridge gaps, stale-RPS-partition overnight UTC drift). Each sub-pathology has had a targeted patch; tonight's 1,169 accounts is the set that slips through every patch we've layered so far.

---

## 1 — Institutional Knowledge (chronological diagnosis trail)

### Phase 0 — Original RPS sell-correction (2026-03-20 to 2026-04-05, ADHC_HISTRY project)

| Commit | Date | Scope |
|---|---|---|
| `2666dc1f` | 2026-04-04 | feat(ADHC_HISTRY P2): Schwab RPS injection in gold scripts 02 + 03 |
| `5800ae2a` | 2026-04-05 | fix(ADHC_HISTRY): RPS sell corrections in holdings lots — closes phantom positions inflating asset mix |
| `80ec50e9` | 2026-04-06 | fix(ADHC_HISTRY P2): extend CUSIP bridge to cover vanished positions via transaction CUSIPs |
| `91d2342f` | 2026-04-06 | fix(ADHC_HISTRY): phantom exclusion drops RPS-injected accounts + CASH COWS false positive |

**Origin story:** the RPS sell-correction path in `B_01._build_rps_synthetic_lots` + `_apply_rps_lot_corrections` was introduced to close **inflating-phantom** positions (FIFO says lot is open, Schwab says sold). At that time, the concern was the opposite direction: asset-mix OVERSTATEMENT from FIFO holding on to stale open lots. The CUSIP bridge was already extended once to cover "vanished positions" where asset names drifted between transaction and RPS feeds.

**Critical subtlety, documented in `80ec50e9`:** the CUSIP bridge was never perfect. It lived inside `_build_rps_synthetic_lots` and was derived from `silver/unrealized`. Positions whose CUSIP didn't round-trip through the bridge produced incoherent joins — this is the exact defect later tackled by `8eda12a3` (2026-04-15 CUSIP-bridge-gap exemption).

### Phase 1 — PCRA/SWTC discovery (2026-04-14)

Document: `docs/analysis/2026-04-14_fifo_rps_injection_mechanics.md` (272 lines, search-keyed: "FIFO force-close, RPS sell-correction, PCRA missing positions, silver/unrealized open lots, holdings_lots is_open=False, bd_covered, sell_corrections, _build_rps_synthetic_lots, Bump, Grundhoefer, Craig Smith, Faulk, Marcuson PCRA").

**Mirror-image diagnosis:** the same sell-correction was silently **destroying** $35.9M across 476 49F accounts (PCRA sleeves, Schwab Trust Bank TTEE, certain joint/trust structures). Root mechanism: these accounts are BD-mapped to Schwab but their positions flow through a **different feed than standard CRS RPS**, so RPS has zero rows for them → `_apply_rps_lot_corrections._CLOSE_ALL` zeroes every FIFO lot.

The 476 cohort was quantified at firm level (-$35.9M of the $57M 49F silver/gold gap) and traced end-to-end on 7 named accounts (z0822224971 Grundhoefer, z0822553691 Craig Smith TTEE, z0822068871 Schwab Trust Bank TTEE, z0820765271 Stephanie Bourland PCRA, z0822561091 Bump Joint, z0815410731 Faulk Joint, z0813335991 Marcuson PCRA).

### Phase 2 — Tactical shadow fix + WP-9 addendum (2026-04-14, commits `1eb495b0` + `cec02a29`)

| Commit | Scope |
|---|---|
| `1eb495b0` | PCRA/SWTC force-close fix (dryrun shadow) + diagnostic + WP-9 addendum |
| `cec02a29` | GOING ALL IN — promote tactical 3-bond + PCRA/SWTC shadows to PROD |

**Fixes landed:**

1. `dryrun_mode=True` gate restricts sell-corrections to accounts that actually delivered RPS rows (`bd_covered_with_rps = set(rps['bd_account_id'].unique())`) rather than any mapped account.
2. Silver/unrealized veto — force-close fires only when BOTH Schwab RPS AND `silver/unrealized/{date}` disagree with FIFO. BD's own custodial view is treated as authoritative for position openness.
3. Nightly diagnostic — accounts where force-close would zero >50% of open MV, alert threshold >5/day.
4. WP-9 (CUSIP-keyed FIFO replay) addendum: specific test case that PCRA/SWTC accounts must survive CUSIP-keyed replay.

**Governing document:** `docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md` §WP-9 Addendum (lines 159–167).

### Phase 3 — First safety halt + veto-normalize post-mortem (2026-04-15, commit `717764fe`)

**Trigger event:** 2026-04-15 03:49Z Group D run — the `dryrun_mode=True` PROD pass flagged **1,307 accounts / $366.6M >50% force-close**. Halted before write. Portal untouched. Three defects identified:

1. **Silver/unrealized veto dtype mismatch.** MultiIndex lookup built from raw `(account_id, asset_name)` had whitespace/dtype drift between `unrl_open_set` and `sell_gaps` → every `isin()` missed → veto never fired.
2. **RPS partition date was not logged.** Stale-RPS-partition is a recurring root cause; operator had no visibility.
3. **No safety halt.** $366M of phantom close was silently acceptable under prior code.

**Fix:** `.astype(str).str.strip()` normalize before MultiIndex; print RPS partition date + match=YES/NO; **`BD_FORCE_CLOSE_LIMIT=200` RuntimeError halt** (`B_01.holdings_lots.py` L1163–1183). `BD_FORCE_CLOSE_OVERRIDE=1` bypass for intentional cutovers.

**This is the halt that tripped tonight.** It did not exist pre-2026-04-15.

### Phase 4 — CUSIP-bridge-gap exemption (2026-04-15, commit `8eda12a3`)

Andrew's math on 2026-04-15 tied the residual 1,307-cohort to CUSIP coverage:

```
firm AUA                            $1.68B
CUSIP resolution coverage           ~90%
Unresolved ceiling (10% of firm)    ~$168M
Halt cohort pre-close MV            $234M total-account (~$140–175M actual-close MV)
Overlap with CUSIP ceiling          tight (within error bars)
```

**Mechanism:** `rps['asset_name']` is `cusip.map(cusip_to_name)`. ~10% of CUSIPs don't round-trip the bridge — those RPS rows are filtered at line 521 (`rps = rps[rps['asset_name'].notna()].copy()`). FIFO still has the asset under its own name. The merge shows "FIFO has it, RPS doesn't" → force-close fires. But absence-from-our-join for an unresolvable CUSIP is **uninformative, not evidence of a sellout**.

**Fix:** after `sell_gaps` is built, drop rows whose `asset_name` is not in `set(cusip_to_name.values())`. Applies to both `dryrun_mode` branches. Expected drop in force-close cohort: **~80%**. Structural fix lives upstream in BDPL_ASTDIM (CUSIP as first-class key in `silver/bd_assets.parquet`); this is the defensive version.

### Phase 5 — Stale-RPS auto-skip flipflop (2026-04-16, commits `a9f42c3b` → `0e9ece2a`)

| Commit | Scope | Status |
|---|---|---|
| `a9f42c3b` | stale-RPS auto-skip when `rps_date != snapshot_date` | REVERTED |
| `0e9ece2a` | fix(B_01): remove epistemically-broken STALE-RPS auto-skip | CURRENT |

`a9f42c3b` added silent skip of `sell_corrections` whenever the loaded RPS partition date didn't match `snapshot_date`. Intent was to prevent stale-partition force-closes. Actual effect: auto-skip fired on **legitimately fresh RPS data** (dates don't match when RPS is nightly and snapshot is ET) → ~$800M–$1B MV overcount ($2.493B gold vs $1.695B silver). `0e9ece2a` reverted because "the skip spec is semantically invalid; the operator can see match=YES/NO in logs and decide."

### Phase 6 — snapshot_date overnight UTC drift (2026-04-17, commits `59340b42` / `ec2c1efc`)

`snapshot_date = pd.Timestamp.now().normalize()` on EC2 (UTC tz) during overnight ET runs yields a date 1–2 days ahead of `silver/allocations` partition. Misalignment cascades through RPS synthetic-lot generation. **Option (d) fix:** derive `snapshot_date` from latest `silver/allocations` YYYY-MM-DD.parquet (with `args.date` > `GOLD_RUN_DATE` env > silver discovery > `now()` fallback). Shipped tonight in `ec2c1efc` by ~B; PROD next nightly picks it up on EC2 boot.

This does NOT fix phantom txns — it aligns dates so the RPS lookup reads the correct day's partition, eliminating one source of over-fire but leaving the inherent FIFO/RPS keying drift.

---

## 2 — Existing Code Paths That Already Address The Pattern (inventory)

All paths listed live in `data/black_diamond/scripts/gold/B_01.holdings_lots.py` — there is **no** separate `diag_rps_force_close.py` (the diagnostic proposed in `2026-04-14_fifo_rps_injection_mechanics.md` §"Permanent diagnostic" was inlined into B_01 instead).

| Path | File:Line | Purpose | Status |
|---|---|---|---|
| `bd_covered_with_rps` cohort restriction | L557, L932, L951–957 | Under `dryrun_mode=True`, sell-corrections only fire against accounts with at least 1 RPS row. Excludes mapped-but-missing cohort (PCRA/SWTC). | ACTIVE in dryrun path |
| Silver/unrealized veto with dtype normalize | L998–1042 | Before `_CLOSE_ALL` fires, veto any `(account_id, asset_name)` that BD's own `silver/unrealized` shows as open. Both sides `.astype(str).str.strip()` normalized. | ACTIVE |
| CUSIP-bridge-gap exemption | L651 (cmt) + `8eda12a3` range in `_build_rps_synthetic_lots` | Drop `sell_gaps` rows whose `asset_name` is not in `set(cusip_to_name.values())` — unresolvable CUSIPs can't be used as evidence of sale. | ACTIVE |
| Extended CUSIP bridge from transactions | L512–518 | Augments `cusip_to_name` (originally built from `silver/unrealized`) with CUSIPs learned from `silver/transactions`. Widens round-trip coverage. | ACTIVE |
| Nightly >50% force-close diagnostic | L1130–1161 | Prints per-account flag + ALERT line if >5 accounts flagged. First line of defense — visible in runner stdout. | ACTIVE |
| `BD_FORCE_CLOSE_LIMIT=200` safety halt | L1163–1183 | RuntimeError before any write if `>200` accounts flagged >50% force-close. `BD_FORCE_CLOSE_OVERRIDE=1` bypass. | ACTIVE — **this is what fired tonight** |
| RPS partition-date print + match=YES/NO | L~1025 (cmt) | Operator visibility for stale-partition detection. | ACTIVE |
| `snapshot_date` derivation from latest `silver/allocations` | L1578, L2085 (commit `ec2c1efc`) | Eliminates overnight UTC drift at the source. | ACTIVE (new tonight) |
| Shadow write `gold/holdings_lots_v2_dryrun/{date}.parquet` | `save_lots` helper + `holdings_lots_v2_dryrun_key` | Emits alternate build under dryrun_mode=True alongside PROD output for diffing. | ACTIVE |

**The stack is mature.** Five distinct guardrails already apply. Tonight's 1,169 accounts survived every single one — they are the residual of all layered defenses.

---

## 3 — E_* diagnostic script inventory (reconciliation-relevant)

None of the existing E_* scripts address the FIFO/RPS force-close pattern directly. Most address aggregate AUA-gap decomposition, not lot-level phantom detection.

| Script | Relevance to phantom-txn / force-close |
|---|---|
| `E_00.decompose_aua_gap.py` | AUA-gap decomposition at firm level. Silent to per-account force-close. |
| `E_02.diagnose_positions_cube.py` | Upstream (positions cube, not lots). |
| `E_03.trace_account_cube.py` | Per-account trace of the positions cube. Closest existing tool — traces what went into the cube, not what `_apply_rps_lot_corrections` did to lots downstream. |
| `E_09.unrecognized_exit_types.py` | Transaction-exit type classification. Orthogonal. |
| `E_19.write_aua_certification.py` | Certification output, not diagnostic. |
| `E_21.generate_reconciliation_reference.py` | Canonical reconciliation reference; closest proxy for a gold↔silver harness. **Superseded by WP-10b harness `cff234b5` (pending AE wire-up into nightly, per ~B)**. |

**Gap:** we have no standalone `diag_rps_force_close.py`. The proposed script in 2026-04-14 §"Permanent diagnostic" (count accounts closed >50%, breakdown by account_type PCRA/SWTC/other, nightly) was absorbed into the inline B_01 diagnostic. That inline version does NOT persist output to S3 — it only prints to runner stdout. **Post-mortem access is via CloudWatch / S3 log parsing, not a parquet.**

---

## 4 — Why Pre-2026-04-15 Runs "Silently Force-Closed"

The CTO's framing ("Pre-2026-04-15 runs silently force-closed this exact cohort every night") is literally correct and has a specific mechanism:

- Before `1eb495b0` (2026-04-14): no `dryrun_mode`, no veto, no CUSIP exemption. `_apply_rps_lot_corrections` ran on **every** mapped account every night. Any account with zero RPS rows got `_CLOSE_ALL` applied to all its FIFO lots.
- Before `717764fe` (2026-04-15): no diagnostic, no safety halt. A run that zeroed 1,000+ accounts for $300M+ would write PROD `holdings_lots` and move on. The only signal was the -3.4% firm-level silver/gold gap which looked like routine cash/timing drift.
- `holdings_lots/2026-04-15.parquet` = 404: this is because the safety halt landed 2026-04-15 and immediately tripped on the very first run (1,307 accts/$366M). No PROD write produced that day. **The 2026-04-15.parquet absence is a feature, not a regression** — prior to that date, PROD writes happened even when the force-close was pathological. Operator only saw the damage after-the-fact in reconciliation.
- The same mechanism applies to tonight's halt: it is the halt **doing its job**. Pre-2026-04-15 behavior was to write 1,169 zero-closed accounts and ship $182M of phantom closes into downstream aggregates.

---

## 5 — How Tonight's 1,169 / $182M / 5.8x Envelope Fits The Sequence

| Incident | Date | Accounts | MV | Envelope (accts/limit) | Status at time of fire |
|---|---|---|---|---|---|
| 49F PCRA/SWTC (observed, not halted) | 2026-04-10 (detected 04-14) | 476 | $35.9M (non-cash) | N/A — halt didn't exist | Silent — diagnostic retrofit |
| First safety halt | 2026-04-15 03:49Z | 1,307 | $366.6M | 6.5x | Halt fires. Motivates veto-normalize + CUSIP exemption |
| (expected post-CUSIP-fix residual) | forecast | ~261 (−80%) | ~$73M | ~1.3x | CUSIP exemption expected to clear 200-limit |
| **Tonight** | 2026-04-17 04:23Z | **1,169** | **$182M** | **5.8x** | Halt fires. Residual is NOT near the forecast |
| Account z0814307721 drill (this council) | 2026-04-17 | 1 of 1,169 | FIFO $4.77M vs RPS perfect match on 15 positions; $1.91M residual is FIFO-only orphans | — | CUSIP match works; orphan txns cause gap |

**Key observation for ~D synthesis:** the CUSIP-bridge-gap exemption was forecast to drop the cohort by ~80% (to ~261 accounts). Tonight landed at 1,169 — **4.5x the forecast**. Three possible readings, all of which merit confirmation from ~B (txn forensics) and ~C (Schwab-side forensics):

1. **Residual is not CUSIP-gap dominant.** z0814307721's drill (CUSIP match is perfect on 15 positions) suggests the phantom residue is now **txn-originated orphan FIFO lots**, not CUSIP misses. That would match the ADHC_HISTRY P0 "vanished positions" pathology from 2026-04-06 (`80ec50e9`) but in a new cohort.
2. **Veto is not firing for this cohort.** Silver/unrealized may not have these FIFO-only orphans because BD's own feed agrees the position is closed — so the veto correctly declines to veto, and the close is legitimate. If so, these aren't phantom; they're **real FIFO-orphan positions** that Schwab confirms closed and BD silver/unrealized confirms closed, but BD silver/transactions never emitted the sale event.
3. **snapshot_date fix landed overnight.** Per ~B session_i, `ec2c1efc` just shipped tonight. Tonight's halt may have fired against the **old** `B_01` (pre-option-d) still running on the runner from last boot — i.e., the halt cohort reflects date-drift residual, not the post-fix state. **Needs confirmation:** what SHA did the runner actually load for this QA/PROD pass? If pre-`ec2c1efc`, tomorrow night's run (post-boot, loading `ec2c1efc`) would test reading 2:.

My bet: **(1) + partial (3)**. Tonight's halt is old-SHA residual with txn-orphan FIFO as the dominant sub-pathology. If tomorrow night still halts at >1,000 accounts, (1) is the answer and we need a new fix — likely an "orphan FIFO lot" exemption paralleling the CUSIP one.

---

## 6 — WP-9 Addendum reference (referenced in the halt error)

Source: `docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md` §WP-9 Addendum (lines 159–167).

Content (paraphrased from the search-key reads above):
- Tactical fix `1eb495b0` writes shadow `gold/holdings_lots_v2_dryrun/{date}.parquet` under `dryrun_mode=True`.
- `dryrun_mode=True` restricts corrections to `bd_covered_with_rps` AND vetoes against `silver/unrealized`.
- WP-9 acceptance requires that PCRA/SWTC accounts survive CUSIP-keyed FIFO replay.
- WP-9 guardrail = the >50%-force-close nightly alert.

**Structural plan from the same addendum:** WP-9 replaces `(account_id, asset_name)` keying with CUSIP-first-class keying; BDPL_ASTDIM W4 (`silver/bd_assets.parquet` with CUSIP as first-class key) is the upstream dependency. Neither has shipped. **All current mitigations are defensive layers around the underlying keying defect.**

---

## 7 — Prior council / decision-memo references

Located in this survey (not exhaustive — 30-min bound):

| Doc | Topic |
|---|---|
| `docs/analysis/2026-04-14_fifo_rps_injection_mechanics.md` | Primary diagnosis. Full reproduction commands + blast radius math |
| `docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md` §WP-9 + §WP-9 Addendum | Governing architectural plan |
| `docs/briefs/data-scientist-2026-04-10-pricing-cleanup-session.md` | 49F cleanup session that uncovered the 3.4% gap |
| `docs/architecture/ADVI_SLEEVE_PLAN.md` | Sleeve shadow emit (SL-P0/P1) — uses `silver/unrealized` as second authoritative feed. If SL-P1 promotes and proves out, it's a candidate upstream source of truth that could replace Schwab RPS for this cohort entirely |
| `org/projects/ADHC_HISTRY.json` | Original RPS injection + phantom work (Phase 0) |

---

## 8 — Recommendations for ~D synthesis

1. **Confirm runner SHA at tonight's boot.** If pre-`ec2c1efc`, tonight's halt is not evidence against the CUSIP exemption. Re-test post-`ec2c1efc` PROD nightly before drawing conclusions on residual size.
2. **If residual persists at >1,000 on next run:** the halt cohort is a new pathology, almost certainly **txn-orphan FIFO lots** (z0814307721 fact pattern). Fix shape likely mirrors the CUSIP exemption: after `sell_gaps` construction, drop rows where FIFO evidence is "orphan Buy with no matching transaction chain" rather than asset-name-drift evidence.
3. **Promote the inline diagnostic to a standalone E_* script.** `E_25.rps_force_close_audit.py`-style artifact that emits a parquet (not just stdout) per nightly run, indexed by account_id with columns: `closed_accts_count, closed_mv, veto_applied, cusip_gap_applied, residual_cohort_tag`. Would give post-mortem access without CloudWatch scraping.
4. **Accelerate WP-9 (CUSIP-keyed FIFO replay).** Every tactical patch to date is defensive against the `(account_id, asset_name)` keying defect. Until CUSIP is the primary key, a new sub-pathology will keep slipping through. WP-9 depends on BDPL_ASTDIM W4 (silver/bd_assets.parquet) — check W4 status.
5. **Wire WP-10b (gold↔silver recon harness) into nightly.** Per ~B status (cff234b5), harness code is shipped but not wired into `gold_dispatch` post-step. Once wired, it will quantify the 1,169-cohort's real silver/gold MV impact at firm level every night independent of B_01's own diagnostic — decouples detection from the thing being diagnosed.
6. **Consider overriding halt ONCE to observe post-fix residual.** Set `BD_FORCE_CLOSE_OVERRIDE=1` for a single QA run AFTER confirming the runner has `ec2c1efc` + all prior fixes. Log the post-close silver/gold delta. Would confirm whether the residual force-closes are real or phantom without any further code change. High-risk-looking but well-scoped (QA runner only, single run, full diagnostic captured).

---

## 9 — Compiler Tools

| Tool | Command | Result |
|---|---|---|
| Grep | `phantom|force.?clos|PCRA|SWTC` over `docs/` | 15 files surfaced — all primary references located |
| Grep | `WP-9` over `docs/` | 3 files — architecture doc + analysis + NNA framework |
| Grep | `safety.?halt|force.?close` over DS logs | 2 hits in 2026-03-23/24 (pre-dates current pattern — false positive, different context) |
| git log | `--grep="force-close|phantom|SAFETY HALT|PCRA|SWTC|rps.synth|CUSIP.bridge"` | 30 commits, full diagnosis trail reconstructed |
| git log | `B_01.holdings_lots.py` | 14 commits since 2026-04-14, all traced |
| Read | `docs/analysis/2026-04-14_fifo_rps_injection_mechanics.md` | 272 lines, primary institutional knowledge |
| Read | `docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md` §WP-9 Addendum | lines 159–167 — governing plan |
| Read | `B_01.holdings_lots.py` L500–570, L930–1050, L1130–1210 | All active guardrail code paths inventoried |

`comp-pipescript io B_01` and `comp-blast B_01` not re-run this pass — `comp-pipescript io B_01` was freshly run by ~B at session_i 04:17Z with full `READS/WRITES/COLUMN GAPS` clean output; no write done by ~A this pass.

---

## 10 — MCP / RAVC

- ACK delivered to 1.0.0_SA_CTO at 20260417T041949Z.
- MCP COMPLETE to 1.0.0_SA_CTO + 2.0.0_SA_COO on ship.
- Scope held: historical / existing-code. No lane overlap with ~B (BD-txn forensics) or ~C (Schwab-RPS forensics). ~D synthesizes.
