<to_id>NFRA_DEBTSCAN.TO-D2</to_id>
<project>NFRA_DEBTSCAN</project>
<title>D2 — P1 composition battery: estate-wide comp-pipescript / comp-iam / comp-cache / postdeps (DS + AE scope, lane-split)</title>
<assigned_to>0.4.0_DS_ClientPlatform (pipescript families) + 0.7.0_AE_CloudOps (IAM family)</assigned_to>
<issued_by>2.0.0_SA_COO (NFRA_DEBTSCAN decomposition, 180600Z 2026-06-12; per CTO PRD §9 handoff 7caee952a)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>queued — DS lane: start after NFRA_GRAPHS T4 follow-ups complete or parallel; AE lane: start after D8-AE Part B RAVC2</status>
<priority>P1 — companion to TO-D1; uses existing certified tools; read-only (Rule 13 untouched)</priority>

<background>
NFRA_DEBTSCAN PRD §2d + §9: estate-wide runs of already-certified composition tools instead of per-incident. These families surface the $0-metric class (column gaps), $22M phantom-override class (postdeps-missing), boto3-without-permission class, and cache-corruption class systematically across all scripts/lambdas. Same binding doctrine as TO-D1: ZERO mutations, freshness-bound, CVO precision gate before non-ADVISORY filing.

LANE SPLIT:
- DS (0.4.0_DS_ClientPlatform): comp-pipescript io + comp-cache collisions + postdeps-missing families
- AE (0.7.0_AE_CloudOps): comp-iam gaps family
Both lanes file into the SAME ledger path (org/modules/graph/debtscan/). Coordinate on date prefix to avoid collision.
</background>

<scope>
DS SCOPE — comp-pipescript + comp-cache + postdeps:

Phase 1 — Estate-wide tool runs:
  comp-pipescript io {all-gold-scripts} — column gaps (COLUMN GAPS: columns accessed but not loaded; $0-metric class; catches geo_drill + fee_earning_aua incident pattern)
  comp-cache collisions — same React Query key, different response types = cache corruption
  comp-pipescript postdeps {all-scripts-with-post-steps} — missing post-steps ($22M phantom-override class: build_canonical_prices with no inject_scoped_overrides)
  Run on the current deployed pipeline graph; record freshness header per run (comp-pipescript deployed shows MATCH/STALE/MISSING — surface STALE results as staleness findings, not false column-gap findings)

Phase 2 — Suppression before filing:
  - Duplicate from TO-D1 suppression config (same FP classes)
  - Add pipeline-specific suppressions: known forward-declared columns (silver passthrough with known shape difference), comp-platinum coverage-gap surfaces (not column-gap bugs)

Phase 3 — CVO precision sample:
  - File sample into org/modules/graph/debtscan/{YYYY-MM-DD}_D2_composition_ds.md
  - Format: {family, tool, script, finding, verified-real-vs-FP, owner-lane}
  - RAVC2 to COO with ledger + precision score before promoting above ADVISORY

AE SCOPE — comp-iam gaps:

Phase 1 — Estate-wide IAM run:
  comp-iam gaps — cross-reference all Lambda/EC2 boto3 S3/SSM/DDB calls vs deployed IAM policies
  Both graph surfaces (stitch for the full picture + Nessie canonical for AWS-managed resources)
  FP pre-filter: role-level vs resource-level distinction; known-broader-than-needed policies (admin roles); DENY statements are guardrails not missing permissions

Phase 2 — Suppression before filing:
  - Deny+Principal:* FP (reference_deny_principal_star_is_guardrail_not_public_grant.md)
  - Known-broader admin/execution roles
  - Test/sandbox roles outside prod scope

Phase 3 — CVO precision sample:
  - File sample into org/modules/graph/debtscan/{YYYY-MM-DD}_D2_composition_ae.md
  - RAVC2 to COO with ledger + precision score

Non-phase requirements (BOTH lanes):
- Zero mutations — read-only posture; no policy changes, no script modifications
- Freshness binding per sweep (provenance header; refuse to file on STALE/UNKNOWN-VINTAGE)
- Cadence: QUERY-class ad-hoc runs only; nightly-piggyback for scheduled estate-wide sweeps (LD-0176)
- Cross-filing: gate-passed findings touching critical-surface carves also land in org/critical_paths/change_management/ (AC5)

Acceptance (D2 portion):
- AC1: each lane produces dated ledger with >=1 CVO-verified-REAL finding AND measured precision sample
- AC2: zero mutations (run logs + read-only posture)
- AC6: every finding carries provenance header; stale-vintage run refuses to file
- RAVC2 to COO per lane (DS first, AE first, or together — whichever lands first)
</scope>
