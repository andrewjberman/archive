# SEAM (durable): bd advisor-NNA attribution — C_01 → {D_00f, D_00c} → ADVI frontend

**Status:** BROKEN@DECLARATIVE+SEMANTIC (advisor-level); SOUND on the source. First QA'd: 3.0.0_SA_CVO
2026-06-17 (`/seams`). Remediation plan APPROVED (project ADVI_NNAATTR); NNA value-limb encoded as the
gate-of-record (`graph_contracts.yaml`, commit 9e5a6f782). Full audit:
`org/tier1_exec/3.0.0_SA_CVO/logs/2026-06-17/cvo_1804Z_nna_estate_audit_seams_verdict.md` (9543c4392).

## The seam in one paragraph
`C_01.canonical_nna` is the single canonical NNA SOURCE (account×date atomic, from `load_flows`). Two
downstream scripts attribute it to advisors via **different sources** — that is the defect:
- **D_00f.advisor_nna_canonical** uses C_01's stamped `architect` (from `acct_dim` SCD, latest-snapshot) →
  leaves unresolved accounts as `Unassigned`/`49F House` placeholders (**34.5% of firm QTD NNA, $35.3M**,
  parked there 2026-06-17). Additive (Σ==firm) only because placeholders absorb the residual.
- **D_00c.portal_leaderboard** uses C_07's `account_team` melt — Layer-3 "architect-implied" (modal-
  implementor ≥60%) **resolves** those placeholders to real advisors (**0 placeholder entries**) and credits
  ALL roles (architect/implementor/consultant/local_ops/additional) → non-additive (Σ≈3× firm).

## Why the same advisor reads two numbers
Travis Penfield QTD 2026-06-17: D_00f architect $4.14M vs D_00c role_breakdown.architect $6.17M (same
concept, +49%) vs D_00c all-roles total $6.95M. The $4.14M-vs-$6.17M gap is the **attribution-source
mismatch** (acct_dim SCD vs C_07-resolved), NOT a per-day gate (that hypothesis was falsified by /seams).
FE routing makes it user-visible: DistributionTab/Continuous-ADV-NNA = architect ($4.14M);
AdvisorPublicProfile SummaryCard = all-roles ($6.95M); silent (no lens label). Plus F-1c: the card's
`periodNna` (all-roles) ≠ its inflows−outflows (architect, after the ADVI_INFMVP.F5 override).

## Trap for the next reader
- D_00f's `advisors` dict lists `Unassigned`/`49F House` AS advisors — placeholders absorbing a THIRD of
  firm NNA, not real advisors. Σ(canonical advisors)==firm does NOT mean attribution is complete.
- "filtered to architect" (D_00f docstring/contract) is true but hides the acct_dim-SCD source + the 34.5%
  placeholder parking.
- Per-advisor NNA is **scope-dependent** (architect-only vs all-roles) AND **source-dependent** (acct_dim
  vs C_07). Pin both before comparing two surfaces' "advisor NNA".

## Resolution (approved plan / Andrew decisions)
One C_07-resolved attribution source + one tenure rule for per-advisor NNA; scope = ALL roles (non-additive);
firm stays additive (account-once); served identically to every route; `nna==inflows−outflows` per surface;
MAX=2021-Q1. Gate-enforced via the NFRA_GCONTR NNA value-limb (5 invariants, advisory v1).
**Open decision (Andrew/CTO, NNA-cluster):** adopt C_07's *inferred* architect (resolves the 34.5%) vs keep
unknown accounts `Unassigned` (conservative) [F-0]; confirm the headline invariant [F-4].

## Re-verify (the sharp checks — CVO close-gate for ADVI_NNAATTR)
- `Unassigned`+`49F House` NNA share ≈ 0 post-resolution (catches F-0 regression).
- Same advisor × window: identical NNA across `advisor_nna_canonical` / `leaderboard` / rendered profile /
  rendered Distribution (cross-route identity).
- `nna == inflows − outflows` per surface; MAX start == 2021-01-01 in every artifact.
- Σ(architect/account-once) == firm; per-advisor all-roles declared non-additive.

— first record: 3.0.0_SA_CVO 2026-06-17
