# ADVI_INFMVP.F5-RD — Repoint 3 NNA views to canonical field + fold F4 fee-split render (RD)

**Project:** [ADVI_INFMVP](../../../projects/ADVI_INFMVP.json)
**PRD:** `docs/architecture/ADVI_INFMVP.md` v0.1 §3 F5 (RD-repoint leg) + F4 (fee-split render) (commit 5f6018778)
**Pod:** 0.4.2_RD_AdvisorIntelligence~B
**Lane:** RD_AdvisorIntelligence ~B (reassigned from base post-crash; base NOT_REGISTERED; ~B LIVE + gated on MDPF S1 Phase-2 — ideal parallel work)
**Issued to:** 0.4.2_RD_AdvisorIntelligence~B
**Author:** 2.0.0_SA_COO 2026-05-28T~20:35Z (/drive — F5 emit RAVC2-Accept downstream leg)
**Sizing:** ~60-90min (3-view repoint + fee-split render + window-label harmonize)
**Authority anchor:** F5 emit RAVC2-Accept (DS-CP bcc29881c) + Andrew direct 2026-05-28 WITH SCREENSHOTS (DS+CVO RIGID; NNA cannot vary between views)

<status>complete</status>

<!-- COMPLETE 2026-05-28T~23:25Z — CVO F5 RIGID GATE = PASS (verify_2318Z_F5_RIGID_gate_PASS.md). All 4 NNA surfaces (snapshot donut / continuous hero / Lifetime headline / Exec Summary) read same windows[W]; cross-view equality BY CONSTRUCTION. Peter+control verified every window QTD/YTD/1Y/3Y/MAX identical across surfaces; fee-split invariant OK; no regression. 3-iteration converge: window_bounds unification (3Y) → emit-clamp (Max current-period) → hero windows[W].nna (granularity-invariant, 84df1272). F4 fee-split rides same single-source = AC4 satisfied. Done-signal routed to CTO 23:30Z → Andrew smoke. Honest-limit: browser-pixel not captured (playwright unavail) — render deterministic via single-source, not gate-blocking. -->

<!-- v1 SHIPPED 48566175 (22:30Z) → CVO RIGID gate BLOCKED 22:40Z (verify_2240Z). REWORK dispatched 22:44-22:46Z (RD~B, one re-ship): (1) THE BLOCK — continuous-3Y $21.69M != Lifetime-3Y $24.46M by $2.77M; DistributionTab.tsx:1567-9 (setDate -1095) vs AdvisorAnalytics.tsx:161-3 (setFullYear -3) compute window cutoff differently + derive from FUTURE latest period_end 2026-06-30; Q2'23 bucket boundary. Fix: unify cutoff, anchor to precomputed windows[W].nna OR canonical window_bounds[W]. (2) Exec Summary Flows repoint to canonical (CVO concern#2 confirmed — durable single-source vs fragile leaderboard as-of-match). Substrate CLEAN (CVO: served artifact exists+correct; pure FE windowing). CVO concern#1 (firm.series L0/L1) = NOT a bug. Re-ship → CVO re-fires full RIGID gate. -->


## Objective

DS-CP emitted the canonical Advisor-NNA field (`platinum/firm/advisor_nna_canonical.json`, INF_D_00f). **Repoint all 3 NNA surfaces to it** so the same advisor × window × cohort × fee-view shows IDENTICAL numbers everywhere. This is the RD leg of the F5 spine + folds in the F4 fee-split render. CVO runs the RIGID cross-view-equality gate after you ship.

## The canonical field (read from advisor_nna_canonical.json)

- `advisors[advisor_key].windows[<window>].{nna, inflows, outflows, fee_paying, no_fee}` ← hero totals, donut totals, Lifetime headline
- `advisors[advisor_key].series.{weekly,monthly,quarterly}[]` ← continuous area + tooltips (**REPLACES the buggy `cumulative_chart.nna_adv`**)
- `firm.{windows, series}` ← firm-level
- Windows available: QTD / YTD / MAX / 1Y / 3Y + calendar q_current/q1/q2/q3.

## Requirements (per DS-CP F5 RAVC2 a/b/c)

- **(a)** Repoint **snapshot donut** + **continuous** + **Lifetime Activity** to the shared field for the matching window. Remove per-view re-derivation.
- **(b) [CVO gate-blocking — window harmonization]** Either harmonize the default window across the 3 panels OR **label each panel's window explicitly** so a Q1-calendar-quarter total and a 1Y-cumulative total don't read as contradictory. The numbers must be canonical-identical *for the same window selection*; different default windows are OK only if each panel's window is labeled unambiguously.
- **(c) [the 60%-bug fix]** The **continuous** area + tooltips specifically repoint onto `series.*` — this stops it reading the weekly-sampled `nna_adv` (which lost 60% of flow). INF_D_00d's `nna_adv`/`nna_geo` are thereby superseded (deprecate later, not this TO).
- **F4 fee-split render (folded in):** Lifetime Activity fee-paying-vs-no-fee split reads `windows[w].{fee_paying,no_fee}` from the canonical field (they already tie out: fee_paying.nna + no_fee.nna == total.nna). DS-CP verifies the tie-out under F4; you render it.

## Acceptance criteria

- **AC5-RD.** Snapshot donut, continuous, and Lifetime all read the canonical field; for the same advisor × window × fee-view they display IDENTICAL numbers. Continuous reads `series.*` (not cumulative_chart.nna_adv). Per-view re-derivation removed.
- **AC5-window-labels.** Each panel's active window is unambiguously labeled (or harmonized) — no contradictory-looking totals across panels for Peter.
- **AC4-render.** Lifetime fee-split (fee-paying / no-fee / total) renders from the canonical field + visually reconciles with the Exec Summary Flows for the matching fee-view.
- **AC5-gate (CVO, downstream — NOT yours to self-certify).** CVO asserts snapshot==continuous==Lifetime for Peter + 1 control across every window×cohort×fee-view on real data. Any mismatch = BLOCKED.
- Portal stays on DEV (Rule 19); tsc clean; `comp-transform schema-check` on the touched panels.

## Dependencies

- **F5 emit (DONE, RAVC2-accepted):** advisor_nna_canonical.json live in S3 + readable. Confirm the FE fetch path/route for `platinum/firm/advisor_nna_canonical.json` exists (coordinate with AE if a serving route is needed — same class as other platinum/firm reads).
- Coordinate field-shape questions with DS-CP (0.4.0_DS_ClientPlatform) — it owns the canonical definition.

## Sequencing

1. ~15min: read the 3 panels' current NNA read-paths (DistributionTab snapshot + continuous; Lifetime) + the canonical JSON shape
2. ~40min: repoint all 3 to the canonical field; continuous→series.*; remove per-view re-derivation; window labels
3. ~15min: fee-split render in Lifetime from fee_paying/no_fee
4. verify on DEV (Peter: snapshot==continuous==Lifetime per window) → RAVC2 → **CVO RIGID gate**

## RAVC2 deliverable

`[RAVC2-Request] ADVI_INFMVP.F5-RD — 3-view canonical repoint` to ws COO. CC CTO + CVO (CVO runs the RIGID gate). Body: portal/DEV commit + the 3 repoint diffs + window-label approach + a Peter cross-view-equality table (snapshot/continuous/Lifetime identical per window) as your pre-gate self-check.

## Cross-domain coordination

`<scoped/>` — 3 portal NNA panels + the canonical field. DS-CP owns the field; CVO owns the gate. **firmAccess.ts not touched** (this is NNA panels, not partner-scoping) — no MDPF S1 collision.

## Notes

- This is the visible payoff of the F5 spine: it's what makes Peter's NNA stop disagreeing across views (Andrew's screenshot defect). Demo-relevant — pace is up.
- Don't delete INF_D_00d's series this TO; just stop reading the buggy one (supersede, deprecate later).

— ws COO /drive 2026-05-28T~20:35Z
