# DATA_PLATFORM D3 -- Orion + Eclipse Architecture Spec (DS draft -- RETIRED)

**This v0.1 draft is RETIRED (2026-06-26).** D3 was ALREADY FINAL **v1.2** at
`docs/architecture/DATA_PLATFORM_D3_orion_eclipse_arch_spec.md` (CTO arch-gated +
CVO reconcile-to-live PASS + the S14 completeness-basis addendum, dated 2026-06-24)
BEFORE this draft was written -- the TO's `active` status was stale. My v0.1 was an
inadvertent re-derivation; CTO caught it (look-at-the-target-before-overwriting),
restored v1.2 untouched, and asked for a net-new diff.

**Diff outcome (DS, 2026-06-26): v1.2 is a strict SUPERSET of this draft -- NO net-new
content to fold.** The three candidate deltas are all already covered in v1.2 at
GREATER depth:
- Verbose != runtime-body gotcha -> v1.2 **§3.5** (exact null fields + the Generate layering).
- Orion->Eclipse `GET /v1/admin/Token` exchange -> v1.2 **§5.1** (HS256-vs-HS512, float exp,
  firmId=209900, the distinct Eclipse userId, the 3-tier SM/file/exchange load, the 422 gap).
- `/portfolios/simple` vs `/portfolios` deliberate double-pull -> v1.2 **§5.2 + §6.3**
  (/simple carries the accountId /full lacks; join on portfolio id).

The only literal difference -- this draft's raw `/Portfolio/Clients/{clientId}/Assets/{date}`
+ `/Portfolio/Lots` + `/Portfolio/Accounts/Simple/Search` endpoint URLs (from the
PATH_DISCOVERY_MSTAR discovery doc) -- is **NOT recommended for a fold:** v1.2 deliberately
grounds Surface-2 on the PRODUCTION path (the `inf-api-assets-v2` lambda + the §13.2 CVO
silver-hop correction `Orion Assets -> bronze -> silver/api_dims/positions_mv -> INF_B_00`),
and the §14 bounded-complete framing already treats raw discovery-doc endpoints as the
expansion frontier, not the integrated surface. Folding exploratory paths would muddy that
honest completeness boundary.

**Canonical spec-of-record:** `docs/architecture/DATA_PLATFORM_D3_orion_eclipse_arch_spec.md`
(v1.2, CTO-lane). Do NOT edit or promote this stub. Any future D3 amend goes to the
canonical copy via CTO promotion.
