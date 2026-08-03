# Instrument-register entries: two comp-tool CloudFront coverage gaps (2026-08-03)

**Registered by:** 3.0.0_SA_CVO, from COO consolidation 171600Z (CTO-routed 171227Z, grounded by
0.7.0_AE_CloudOps~F during MDLP_MONPUB.W9). Register entries ONLY -- no build implied
(moratorium-clean); coverage gets built when its owner routes it.

## GAP 1 -- `comp-routes behaviors` carries no cache-policy identity or TTL values

The behavior map names origins/edge-lambdas/path patterns but not which cache policy a behavior
uses nor its TTLs. Any TTL/caching question falls through to live `get-distribution-config` +
`get-cache-policy`.
**Independently hit by CVO the same day, before the register note arrived:** my DataRefresh/
CloudFront audit (@30a13b89b1) needed raw `aws cloudfront get-distribution-config` +
`get-cache-policy` under `# rail-checked:` markers for exactly this -- the markers in
`org/mcp/comp-which-rail.log` are the live evidence trail. Two independent same-day instances =
the gap is on the working path of an Andrew-watched family, not a corner.

## GAP 2 -- `comp-blast` has no CloudFront path-pattern / cache-policy nodes

Blast-radius on a CF behavior (which behaviors share a cache policy; what consumes a path
pattern) is unanswerable from the graph; ~F derived a 2-of-25 sharing denominator from the live
distribution config. For the W9 change class the blast radius IS the load-bearing control (a
shared MANAGED policy propagates a TTL change to every sharing behavior) -- the graph is blind on
precisely the coupling axis it exists to carry. Note W9 itself was correctly re-shaped by this
fact (a dedicated policy instead of editing the shared managed one would be the propagation-safe
shape; that design call belongs to the W9 owner).

**Interim pattern until coverage exists (proven twice today):** comp-routes for the map, live
primitives for policy identity/TTLs, with `# rail-checked:` markers -- and any TTL claim cites
the live read, never the comp-tool.
