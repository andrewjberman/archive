# NFRA_COMPTEAM B2-DESIGN -- Scoped Read-Partition Design over the Shared Graph

**Author:** 0.8.0_AE_CloudComp | **Date:** 2026-07-07 | **Status:** DESIGN DRAFT, pending SCTY-coord RAVC
**TO:** `org/tier1_exec/2.0.0_SA_COO/task_orders/NFRA_COMPTEAM.B2-DESIGN.scoped-read-partition-design.md`

## Objective (verbatim from the TO)
Per-team/per-surface read-partition design over kuzu/nessie/iceberg, read-slices off B1's map
(B1 CLOSED, CTO-gated 965c0a8c1), binding to the SCTY user-type-tier + read-only-scope
entitlement (the tier-model is ALREADY LIVE-CERTIFIED 07-01, CVO 4/4).

## Grounding (both inputs are FROZEN/certified contracts -- this design consumes, never modifies)
- **B1 map** (`org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/NFRA_COMPTEAM.B1_portal_surface_data_source_map.json`,
  schema_version `1.0-FROZEN`, CTO-accepted 2026-07-01): `pages[].clusters[].sources[]` -- 91
  PanelClusters / 125 source-bindings across 15 portal pages. Every source carries `tier`
  (STATIC|DYNAMIC) + either `{bucket, s3_key}` (STATIC) or `{relative_key, firm}` (DYNAMIC) +
  `artifact_pattern`. B1 v0.3.1 closure proved every cluster has >=1 source binding (no orphans) --
  req#1 below is therefore already TRUE by construction of the input, not something B2 re-derives.
- **SCTY tier model** (`infra/aws/ec2/m365-mcp-gateway/app/tier.py`, live-certified 2026-07-01,
  CVO 4/4 independent live-cert `51090a2fa`): `Tier{READ_ONLY, STANDARD_EMPLOYEE, MASTER_ADMIN}`,
  `resolve_tier(email, cfg)` -- fail-closed to READ_ONLY under any signature-unverified identity
  provider (`_provider_is_verified`), exact-match-only allowlists (`MASTER_ADMIN_EMAILS`/
  `WRITE_CAPABLE_EMAILS`), unmatched-but-verified identity defaults to READ_ONLY (never a guess).
  `tier_meets_min()` does capability-RANK comparison, fail-closed on an unparseable tier string.

## req#1 -- every PanelCluster maps to a served source (from B1)
Satisfied by B1's own schema guarantee (91/91 clusters carry sources[], exhaustively grounded
across STATIC + DYNAMIC FIRM-LEVEL + PER-ENTITY + TAIL tiers, B1 v0.3.1 CLOSED). B2's partition
UNIT is the PanelCluster: `partition_key = (page, cluster_id, firm|shared)` -- firm-suffixed for
DYNAMIC sources (per-firm data), unsuffixed ("shared") for STATIC sources that serve all firms
identically. Never split finer than a PanelCluster -- this matches the existing TSGRAPH `CLUSTERS`
semantic B1 already carves the estate along, so a partition boundary is never a NEW taxonomy,
just a grant/deny predicate over an EXISTING one.

## req#2 -- a partition reads its slice + is DENIED cross-team/cross-surface
Proposed module: `org/modules/graph/graph_read_scope.py` (new, mirrors the `guard.py` deny-shape
pattern from SCTY_MCPGUARD for consistency across the estate's two independent access-control
surfaces -- portal-API tier gating vs. graph-read partitioning).

```
TeamSurfaceGrant = {team: str, allowed_partitions: frozenset[str]}
```
A team (AE / DS / DT / COO / CVO / a per-firm portal-proxy identity) is granted an EXPLICIT
allowlist of partition keys -- never a wildcard or blanket grant, mirroring tier.py's ADD-2
principle ("write is opt-in per identity, never the default"; here: "a partition is readable
only if explicitly granted, never the default").

```
def scoped_read(team: str, partition_key: str, query_fn) -> QueryResult:
    grant = _grants_for(team)                       # TEAM_ROSTER lookup, exact-match (ADD-1 style)
    if partition_key not in grant.allowed_partitions:
        raise ScopedReadDenied(team, partition_key)  # LOUD deny, logged -- never a silent empty result
    node_prefixes = _node_prefixes_for_partition(partition_key)   # derived from B1's sources[], below
    return query_fn(scope=node_prefixes)             # comp-kuzu MATCH filtered to ONLY this slice
```

`_node_prefixes_for_partition` derives DETERMINISTICALLY from B1's frozen `sources[]` entries for
that cluster (the `s3_key`/`relative_key` values resolved to `s3:`/`gold:` node-id prefixes via
the SAME `CLOUDNODE_PREFIX_TO_ENTITY` mapping `cse_schema.py` already canonicalizes) -- never a
second hand-maintained prefix list. This is the same "one authority, never a parallel guess"
discipline CLAUDE.md Rule 13 enforces for `PIPELINE_MAP` (bd/inf/cot firm-bucket mapping):
B1's JSON is the single source B2 derives partition membership from, not a re-derivation.

Cross-team/cross-surface default = **DENY**. There is no partition reachable without an explicit
grant row -- fail-closed, matching tier.py's fail-closed order exactly (default-deny, not
default-allow-minus-blocklist).

## req#3 -- scope resolves off SCTY-verified identity, fail-closed on unverified
B2 does **not** reimplement identity verification -- it binds ONE LEVEL ABOVE `tier.py`'s
already-certified root-of-trust, reusing the SAME verified-email claim:

```
def team_for_identity(email: str, cfg) -> str:
    if not tier._provider_is_verified(cfg):
        return TEAM_DENY_ALL          # (1) unverified provider -> the universal-deny team (no grants)
    if _exact_in(email, TEAM_ROSTER.get(...)):
        return matched_team           # (2) exact-match roster lookup (ADD-1 discipline, reused)
    return TEAM_LEAST_PRIVILEGE       # (3) verified but unmatched -> least-privilege team, never a guess
```

This makes B2's read-partition entitlement structurally DEPENDENT on the exact same fail-closed
root-of-trust `tier.py` enforces for the portal-API surface, rather than a second, independently-
drifting security boundary. A provider misconfiguration that would degrade `tier.py`'s guarantees
(caught today by `validate_identity_provider_for_prod`) degrades B2's guarantee identically, by
construction -- one root-of-trust, two consuming surfaces.

## Open items for SCTY-coord RAVC (not resolved unilaterally here)
1. **TEAM_ROSTER ownership/location** -- alongside `MASTER_ADMIN_EMAILS`/`WRITE_CAPABLE_EMAILS`
   in the same gateway config surface, or a separate `org/modules/graph`-owned roster? A
   security-boundary ownership call; SCTY should rule, not AE.
2. **Deny shape** -- a hard exception (`ScopedReadDenied`, fails the request loud) vs. an
   empty-result silent return? I lean toward the loud exception (matches `guard.enforce_min_tier`'s
   deny-shape precedent, and a silent empty result risks reading as "this partition is just empty"
   rather than "you are not entitled to it") -- flagging for SCTY's explicit ruling since this is
   a new security-relevant surface, not assuming.
3. **Severity/critical-surface registration** -- should `graph_read_scope` get its own
   `critical-surfaces.yaml` entry (SEV1, given a read-partition leak is a genuine cross-team data-
   exposure risk)? I'd propose SEV1 (stricter than GOV-B's SEV2 compiler-mechanism entry, since
   this gates actual DATA exposure, not a build-tooling mechanism) -- pending SCTY confirmation.
4. **TEAM_ROSTER population** -- who is on which team (AE/DS/DT/COO/CVO/per-firm-proxy) is a
   people/access decision, not an architecture one; needs SCTY-coord + likely Andrew sign-off
   before any roster is populated for real (this design specifies the MECHANISM, not the roster).

## Non-goals (this design)
- Does **not** modify B1's frozen schema (`schema_version: 1.0-FROZEN`) or `tier.py`'s
  certified `resolve_tier`/`tier_meets_min` -- both consumed read-only, as-is.
- Does **not** implement code. Per the TO's own scoping (`NFRA_COMPTEAM.B2-DESIGN`, distinct
  from a future `B2-BUILD`), this is the design; implementation is a follow-on TO once
  SCTY-coord RAVCs the open items above.
