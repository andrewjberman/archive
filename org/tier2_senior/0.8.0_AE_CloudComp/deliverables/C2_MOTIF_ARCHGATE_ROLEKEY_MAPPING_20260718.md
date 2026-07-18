# C2 motif-enrichment -- arch-gate package: position->role-key mapping + SERVED_LINEAGE delivery

**From:** 0.8.0_AE_CloudComp~D  **For:** 1.0.0_SA_CTO (arch-gate + roles: blessing) via 0.8.0_AE_CloudComp (base, design-of-record)
**Date:** 2026-07-18  **Code:** SERVED_LINEAGE delivered @4c57b963a; TO NFRA_COMPSIMILAR.PH2-C2 @9dd8c9ad2.

CTO asked (relay @034518Z): "when you have classify_motif's SERVED_LINEAGE mapping working, surface the
position->role-key mapping table for the other 3 at the gate, so keys + canon positions line up exactly."
Here it is, grounded on the LIVE canonical-graph topology (verified 2026-07-18, Rule 22a).

## 1. SERVED_LINEAGE_CANON -- DELIVERED (roles: blessed @ddfe05ae9, exercised live)
| role_key (blessed) | label | classify_motif structural predicate (LIVE-grounded) | fires today? |
|---|---|---|---|
| served_url | "served URL" | node_type == ServedURL | node has no ARN* |
| data_fetch | "data fetch" | node_type == DataFetch | node has no ARN* |
| jsx_render | "render terminal" | node_type == JSXRender | node has no ARN* |
| gold_field | "served gold field" | node_type == Field | node has no ARN* |
| **s3** | **"S3 tail"** | **node_type == S3_BUCKET AND has an incoming ORIGIN edge from a CLOUDFRONT_DISTRIBUTION** | **YES -- 5 served tails / 39 ARN buckets** |

*SCOPE FINDING (1):* the 4 FE-stitch types have **0 ARNs** in the graph, so on the ARN-keyed `--describe`
corpus the **`s3` role is the SOLE operative SERVED_LINEAGE role**. The other 4 predicates are built +
self-test-covered (M7) and correct; they light up if/when the corpus scope includes non-ARN FE nodes (a
future describe-by-id path). EXERCISED: `opal-data-bd` -> "instantiates SERVED_LINEAGE_CANON as S3 tail";
`opal-data-mdpf` (not CF-served) -> no clause (graceful, no data-bucket mislabel).

*DRIFT FINDING (2, for CTO -- canon-patterns roles: comments):* the SERVED_LINEAGE motif PROSE (and the
roles: comments) describe edges that have DRIFTED from live -- prose `(Field)-[SERVED_FROM]->(ServedURL)`;
LIVE `ServedURL-[SERVED_FROM]->S3_BUCKET_POLICY`, `Endpoint-[READS_URL]->ServedURL`, `JSXRender-[RENDERS]->Field`,
`CLOUDFRONT-[ORIGIN]->S3_BUCKET`. The blessed KEYS anchor on node_type so the mapping is correct; only the
comments mislead. Suggest CTO refresh the roles: comments to the live edges (keys/labels stay).

## 2. The other 3 classes -- proposed position->role-key mapping + SOURCE-WIRING status
CTO to bless the roles: keys; each class's clauses only fire once its instance-grain SOURCE is wired (base
build-notes table). None is buildable on the canonical graph today without its source:

| class | proposed role_keys (base FEED) | structural position (per canon motif) | instance-grain source | status |
|---|---|---|---|---|
| DEPLOY_CANON | code_prefix, runner | S3 `code/`-prefix -[READS]-> EC2/LAMBDA/ECS runner | **code/-prefix nodes / deploy-ledger** -- canonical DB is BUCKET-grain (no code/ prefix), so a bucket-grain "code-runner" can't be told from a data-reader -> would MISLABEL. HOLD. | source UNWIRED |
| AUTH_CANON | route, edge_fn, origin_s3 | (API_ROUTE\|ServedURL) -[TRIGGERS]-> auth-edge LAMBDA -[READS]-> S3 | **comp-routes BEHAVIOR** -- the route->auth-edge TRIGGERS is unmodeled on the canonical graph. HOLD. | source UNWIRED |
| PIPELINE_CANON | bronze, silver, gold, served_s3 | (bronze)->(silver)->(gold)-[WRITES]->(S3)->served | **comp-pipescript** interior (bronze..gold NOT in canonical DB). served_s3 OVERLAPS SERVED_LINEAGE.s3. C3 system-membership HELD (NFRA_ONTOLOGY). HOLD interior. | source UNWIRED |

**Recommendation:** bless the role_keys for all 3 now (defines the closed vocab; graceful-degrade means no
clause fires until a source wires), then each class is a SEPARATE follow-up increment gated ONLY on wiring
its source (DEPLOY: code-prefix; AUTH: comp-routes adapter; PIPELINE: pipescript adapter) -- exactly the
build-notes sequencing. C3 + Twin/Fork-Shadow stay held to NFRA_ONTOLOGY (LD-0310).

## 3. Governance / determinism (in place)
- LABEL read from canon-patterns roles: (never hardcoded); ABSENT label -> NO clause (self-test M6: absent->
  no-clause, blessed->splices, off-canon key->no-clause). classify_motif is PURE + deterministic (M7).
- No new comp-* surface (enriches derive_summary -> flows into --describe zero-surface-change); manifest-check
  exit 0. self-test 7/7. commit-gate clean.
