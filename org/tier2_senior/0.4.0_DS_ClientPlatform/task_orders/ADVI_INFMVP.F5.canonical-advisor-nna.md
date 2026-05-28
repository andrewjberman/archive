# ADVI_INFMVP.F5 — Canonical Advisor NNA (single source of truth) (DS — SPINE / HIGHEST PRIORITY)

**Project:** [ADVI_INFMVP](../../../projects/ADVI_INFMVP.json)
**PRD:** `docs/architecture/ADVI_INFMVP.md` v0.1 §3 F5 + §4 (spine) + §7 Q2 (commit 5f6018778)
**Pod:** 0.4.0_DS_ClientPlatform
**Lane:** DS_ClientPlatform (canonical NNA emit). Downstream legs: RD repoint (0.4.2) + CVO RIGID gate (3.0.0) — authored at DS-emit RAVC2 moment.
**Issued to:** 0.4.0_DS_ClientPlatform
**Author:** 2.0.0_SA_COO 2026-05-28T~19:46Z (/drive — CTO NOVEL_PRD_READY handoff 19:45Z)
**Sizing:** Phase-0 ~60-90min (locate/define canonical series) + emit ~varies by Phase-0 finding
**Authority anchor:** CTO PRD v0.1 5f6018778 + Andrew direct 2026-05-28 WITH SCREENSHOTS ("DS + CVO must be RIGID that NNA cannot vary between Segment Analytics and Lifetime Activity panels")

<status>complete</status>
<!-- DS self-flip on RAVC2-Request 2026-05-28T~20:31Z (per /work Step 3.4). Emit: INF_D_00f.advisor_nna_canonical.py (bcc29881c) -> platinum/firm/advisor_nna_canonical.json (deployed+verified). Phase-0 brief: docs/briefs/advi-infmvp-f5-canonical-advisor-nna-phase0-20260528.md. RAVC2 to COO CC CTO+CVO. AC5-DS-self-check: canonical-exact QTD/YTD/MAX/q1 for Peter; continuous-chart 60%-flow-loss sampling bug found + corrected via bucket-summed series. COO owns ratification + RD-repoint/CVO-gate leg authoring. -->


## Objective — the spine

Peter's Advisor NNA is **different in every view**: Segment Analytics **continuous** total −$274K (+$105K in / −$379K out, 63 new clients; Q1'26 tooltip −$53.4K); Segment Analytics **snapshot** NNA-by-Advisor donut +$2.35M; Lifetime Activity disagrees with both. **MANDATE: ONE canonical Advisor-NNA per advisor × window × cohort × fee-view.** All three surfaces read that same source and display identical numbers. Visualization differences (donut vs waterfall vs area) are fine; the underlying numbers must be identical.

## Root-cause hypothesis (ws CTO)

`DistributionTab.tsx` snapshot reads donut/bell snapshot data; continuous reads `cumulative_chart` keys (different upstream series); Lifetime Activity reads a third path. Each applies its own aggregation (period-end snapshot vs cumulative sum vs flow-bucket), so the same advisor yields three totals.

## Approach (PRD §3 F5)

**Phase 0 (this TO's gating deliverable) — Q2 resolution:**
1. Identify the canonical Advisor-NNA series in the gold/platinum artifact — or **define one** if the artifact emits multiple inconsistent series.
2. Establish the canonical definition: what Advisor-NNA means per window × cohort × fee-view (inflows − outflows over the window; consistent period boundaries). Document it as the contract RD + CVO will hold to.

**Emit:**
3. Emit the canonical Advisor-NNA as a **single field** the FE reads everywhere. ADDITIVE per Rule 17 spirit at gold layer — do not slim existing series; add the canonical field.

**Downstream (authored at your emit-RAVC2 moment, not now):**
- RD (0.4.2) repoints Segment Analytics snapshot + continuous + Lifetime Activity to the canonical field; removes per-view re-derivation.
- CVO (3.0.0) RIGID empirical gate (see AC5).

## Acceptance criteria

- **AC5-DS.** Canonical Advisor-NNA series identified-or-defined (Q2 resolved) + emitted as one field per advisor × window × cohort × fee-view, with a written canonical definition. ADDITIVE (no existing-series regression).
- **AC5-gate (CVO, downstream).** For Peter + one control advisor: displayed Advisor NNA **identical** across Segment Analytics snapshot, Segment Analytics continuous, and Lifetime Activity, for **every** window × cohort × fee-view combination, on **real data**. Any mismatch = BLOCKED. This is the acceptance bar — **not advisory**.
- **AC5-DS-self-check.** Before RAVC2, DS asserts the canonical field reconciles the −$274K continuous vs +$2.35M snapshot discrepancy for Peter to a single explained number (or documents why the two were measuring different things and which is canonical).

## Dependencies

- **None upstream to start Phase 0.** F4 (fee-split tie-out) DEPENDS ON this — F4's sub-buckets must sum to F5's canonical total. F5 sequences first (or jointly with F4 per PRD §4).
- Builds on today's F11 fee_breakdown emit (shipped earlier) for the fee-view dimension.

## Sequencing

1. ~20min: read `DistributionTab.tsx` (snapshot vs continuous read paths) + Lifetime Activity read path + the gold/platinum NNA artifact schema
2. ~30min: determine whether a canonical series exists or must be defined; write the canonical definition (Q2)
3. emit the canonical field (ADDITIVE); ds-commit-gate (Rule 14) if a `data/*/scripts/gold|silver` script
4. DS-self-check reconciliation for Peter (AC5-DS-self-check)
5. RAVC2-Request → COO authors RD-repoint + CVO-gate legs on accept

## RAVC2 deliverable

`[RAVC2-Request] ADVI_INFMVP.F5 — canonical Advisor-NNA emit` to ws COO. CC ws CTO + ws CVO (CVO pre-reads the canonical definition before the RIGID gate). Body: Q2 resolution (existing vs new field) + canonical definition + emit commit/diff + AC5-DS-self-check reconciliation of the Peter snapshot-vs-continuous discrepancy + the field name/path RD will repoint to.

## Compiler tools mandate

- `comp-pipescript io <gold-script>` before edit (COLUMN GAPS + PORTAL CONSUMERS — the NNA views are platinum consumers).
- `.tools/ds-commit-gate.sh <files>` before commit (Rule 14) if touching `data/*/scripts/gold|silver/*.py`.
- `comp-validate <script> --artifact <file>` post-run if a gold artifact is regenerated.

## Cross-domain coordination

`<scoped/>` — gold/platinum NNA artifact + 3 portal consumer views (RD). Coordinate the canonical field name with RD before they repoint. **MDPF_SCOPED overlap:** none expected for F5 (advisor-NNA canonicalization is INFMVP-specific), but flag ws COO if Andrew's sibling PRD touches the NNA artifact.

## Notes

- This is the **highest-priority defect** in INFMVP and the spine F4 hangs off of. Andrew was explicit (with screenshots) that DS + CVO must be RIGID. The CVO gate is empirical cross-view equality on real data — synthetic will not satisfy it.
- Per [[feedback_silver_no_field_slimming]] / Rule 17 — canonical-field add is ADDITIVE; do not prune the existing per-view series in the same change (RD removes the per-view *re-derivation* on the FE side, not the DS series).

— ws COO /drive 2026-05-28T~19:46Z
