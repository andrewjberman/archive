# ADVI_INFMVP.F4 — Fee-split NNA in Lifetime Activity ties to Exec Summary Flows (DS + RD, CVO-gated) — STAGED on F5

**Project:** [ADVI_INFMVP](../../../projects/ADVI_INFMVP.json)
**PRD:** `docs/architecture/ADVI_INFMVP.md` v0.1 §3 F4 + §4 (depends on F5) (commit 5f6018778)
**Pod:** 0.4.0_DS_ClientPlatform (emit) + 0.4.2_RD_AdvisorIntelligence (FE) + 3.0.0_SA_CVO (gate)
**Lane:** DS_ClientPlatform (fee-split emit/tie-out); RD-leg + CVO-leg authored at DS-emit RAVC2 moment
**Issued to:** 0.4.0_DS_ClientPlatform
**Author:** 2.0.0_SA_COO 2026-05-28T~19:46Z (/drive — CTO NOVEL_PRD_READY handoff 19:45Z)
**Sizing:** ~varies; sequenced after F5 canonical-NNA lands
**Authority anchor:** CTO PRD v0.1 5f6018778 + Andrew direct 2026-05-28

<status>complete</status>
<!-- DS self-flip on RAVC2-Request 2026-05-28T~22:10Z (per /work Step 3.4). AC4-sum PASS: fee_paying.nna + no_fee.nna == total.nna (delta=0.00) for peter_lee + joe_brandenburg + firm across QTD/YTD/MAX, verified empirically against deployed artifact s3://opal-data-inf/platinum/firm/advisor_nna_canonical.json (generated_at 2026-05-28T20:29:29Z). No new code needed — sub-buckets already in F5 emit. Cohort dimension (new-vs-existing) flagged as small follow-on per COO direction. RAVC2 to COO CC CTO+CVO. -->

## Objective

The fee-paying vs no-fee NNA split shown in the **Lifetime Activity** panel must be **correct** and **tie exactly** to the Advisor-level NNA in the **Flows container of the Executive Summary** panel (the fee-split cohorts feed that chart — built on today's F11 `fee_breakdown` emit).

## Tie-out requirement

`fee-paying NNA + no-fee NNA = total Advisor NNA` (the F5 canonical total), and each sub-bucket matches what the Executive Summary Flows container renders for the same advisor / window / fee-view. **No divergence** between the two panels for the same cohort/window selection.

## Acceptance criteria

- **AC4.** For Peter, across all windows (QTD / YTD / MAX): Lifetime Activity fee-split NNA (fee-paying, no-fee, total) reconciles **exactly** with the Executive Summary Flows NNA for the matching fee-view. CVO verifies the tie-out **empirically** (real silver/platinum, not synthetic).
- **AC4-sum.** fee-paying + no-fee = F5 canonical total for every advisor × window (consistency with the F5 spine).

## Dependencies

- **HARD: F5 canonical Advisor-NNA emit (RAVC2-Accepted).** F4 builds the fee-split decomposition of F5's canonical total — it cannot proceed until the canonical total exists and is fixed.
- F11 `fee_breakdown` emit (shipped earlier today) supplies the fee-paying/no-fee cohort dimension.

## Sequencing (post-F5)

1. On F5 accept: COO GO's this TO + (if needed) authors the RD FE-leg + CVO-gate leg
2. DS: emit/verify fee-split sub-buckets summing to F5 canonical total
3. RD: render the fee-split in Lifetime Activity reading the canonical-derived buckets
4. CVO: empirical tie-out gate (AC4) on real data → RAVC2

## RAVC2 deliverable

`[RAVC2-Request] ADVI_INFMVP.F4 — fee-split NNA tie-out` to ws COO. CC ws CTO + ws CVO. Body: the tie-out reconciliation table for Peter across QTD/YTD/MAX (fee-paying + no-fee = total = Exec Summary Flows value) + commit/diff + CVO empirical sign-off.

## Cross-domain coordination

`<scoped/>` — fee-split decomposition of the F5 canonical total; same NNA artifact + Lifetime Activity + Exec Summary Flows consumers. Tightly coupled to F5 — keep the same canonical definition.

## Notes

- F4 is the fee-view decomposition of the F5 spine; authored now as STAGED so the dependency + tie-out contract is recorded, GO'd on F5 accept. Avoids divergent fee-split work landing before the canonical total is fixed.

— ws COO /drive 2026-05-28T~19:46Z
