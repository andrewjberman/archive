# NFRA_ONTOLOGY2 P1 -- Arch-Gate Package (route to CTO~Z before canonization)

**Author:** `0.8.0_AE_CloudComp~C` (rule-bank content lane) · **Date:** 2026-07-23 · **Gate:** CTO~Z (arch) -> CVO~Z (verify)
**TO:** `NFRA_ONTOLOGY2.P1` (issued_to ~C) · **Design:** `NFRA_ONTOLOGY2_PRD.md` s.2 + `NFRA_PSTMRT_PRD.md` s.3 · **Constitution:** `docs/doctrine/INTENT_DENOMINATOR_SYNCHRONIZATION.md`

## Why this is a routed package, not a commit
`org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` + `variance_dimensions.yaml` are lane=**ANY_EXEC** (owned-paths); `~C` authors content, an exec **co-canonizes** (commits). The authored changes are:
- **staged live** in the shared working tree (ready for CTO~Z `safe-commit --only`), AND
- **preserved durably** as `ontology2_p1_authored.patch` (this dir) -- `git apply` it if the working tree is clobbered by concurrent org/modules/graph activity.

## What was authored (ADDITIVE; ratified C0-C3 + 14 roles + 10 relations + variance BYTE-IDENTICAL)
1. **`dynamic_rails`** -- D1 value/grain (C0-C1), D2 path/flow (C1-C2), D3 contract/obligation (C2-C3). Each carries vocabulary + graph_evidence (printed denominators) + honest coverage_boundary (R1 discipline on the ontology itself) + derivations licensed.
2. **`completeness`** axis (PSTMRT P2) alongside `variance` -- separation=never-merge; completeness=never-missing. Mechanical set-comparison vs the governed `data/firm_registry.json`; verdicts Complete/Incomplete/Unregistered/Undeclared-keyed.
3. **`type_tuple`** -- the enforced typing vocabulary (base 0.8.0's registration invariant validates tool declarations against it, stage-2 on canonization):
   - `rail` [C0,C1,C2,C3,D1,D2,D3] / `grain` [artifact,partition,row(FORWARD),field] / `plane` [source,projection,desired,applied,live,mixed,graph-cache] (adopted VERBATIM from base's R1R3 enum) / `scope` [estate,tree,firm,pipeline,motif,partition-window,single-artifact].
4. **`c1_frontend_adapter`** -- the DESIGN FORK resolution (below).
5. **`variance_dimensions.yaml`** -- `+registry_binding: data/firm_registry.json` (additive annotation).
6. **`meta.version`** 1.1 -> 1.2 (LAW-2 promotion w/ printed denominators) + scaffold.py 2 provenance labels synced (CTO~Z ruling 185208Z).

## THE DESIGN FORK (CTO~Z 191540Z): 11 unmapped edges -- binds-additively vs needs-new-vocab
**VERDICT: 11/11 bind to an existing relation ADDITIVELY. 0/11 need new ratified vocab.** Grounded per edge (comp-kuzu @2026-07-23T14:52Z, HEAD current, src->dst printed):

| edge (n) | grounded src->dst | binds_up | grain | verdict |
|---|---|---|---|---|
| RENDERS 2447 | JSXRender->Field | consumes | field | additive |
| PROP_PASSES 1382 | JSXElement->Field/Prop | derives-from | field | additive |
| NOTIFIES 40 | CW_ALARM->SNS_TOPIC | produces | - | additive |
| GRANTS 17 | IAM_POLICY->SVC_PRINCIPAL/IAM_USER | guards | - | additive |
| LOGS_TO 13 | LAMBDA->LOG_GROUP | produces | - | additive |
| DEAD_LETTERS_TO 5 | EVENT_RULE/SQS->SQS_QUEUE | produces | - | additive |
| SUBSCRIBES 3 | SNS_TOPIC->SQS/LAMBDA | produces | - | additive (SNS->LAMBDA leg trigger-flavored, noted) |
| USES_SG 2 | VPC_ENDPOINT/LB->SECURITY_GROUP | depends-on | - | additive |
| USES_OAC 1 | CLOUDFRONT->S3_BUCKET | projects | - | additive |
| ALIAS_TO 1 | ROUTE53_RECORD->LOAD_BALANCER | depends-on | - | additive (resolution-flavored) |
| IN_VPC 1 | LAMBDA->SECURITY_GROUP | depends-on | - | additive |

The 97.9% frontend mass (RENDERS+PROP_PASSES) **dissolves into additive rail+adapter work** precisely because the frontend edges are consumes/derives-from **at field grain** -- exactly what D1 adds. `binds_up` arrays extended additively (authority-of-record). No ratified-vocab candidate raised.

**Note -- LIVE CLASSIFIER PROPAGATION (flagged, NOT done here):** the live role-classifier consumes `canon-patterns.yaml`, not rule-bank `binds_up`. So the `binds_up` extension updates the AUTHORITY with zero runtime effect today; propagating these mappings into `canon-patterns.yaml` is a P2+ wiring step. It was deliberately NOT done because `canon-patterns.yaml` IS a `summary_corpus.py` input -- touching it would break the zero-diff acceptance.

**9 ZERO-LIVE direction-2 tokens** (DEPENDS_ON/REQUIRES/IMPORTS/AUTHENTICATES/AUTHORIZES/ALLOWED/GOVERNS/DENIED/REFERENCES) = a SEPARATE fork (not retired here): auth family likely a plane-visibility gap (CSE/trace plane); code-import deps genuinely absent from the graph (forward). Retiring ratified vocab -> ratification chain.

## Acceptance (EXERCISED, not inferred)
- **summary_corpus.py ZERO-DIFF**: self-test 10/10 identical; `--build` corpus identical; and the sharp **isolation control** (edit-OFF vs edit-ON `--describe` at the SAME graph vintage) is byte-identical -- my edits are in the null space of the live consumer (summary_corpus never reads the rule bank; reads only unmodified variance_dimensions keys). A describe-bd baseline flip was proven to be graph-vintage non-determinism, not the edit.
- **comp-ontolint** check PASS + self-test PASS (10 base relations single-axis, 3 dual-axis composites, 14-role role_priority total order -- ratified vocab intact).
- **git diff strictly additive**: only deletions are the version-string swaps; no ratified content removed.

## Open items for the gate
- **Co-canonize** the 2 exec-locked files (staged live OR apply the patch).
- **scaffold.py** v1.2 sync -- currently reflects v1.2 (verify it lands under the right author; SDK-owner lane per your guard).
- **comp-system** 06_current_state regen was bundled to clear the _SOURCE drift gate (census delta 85->86 / 64->65 orthogonal). If you commit the rule bank separately, re-run `comp-system` at that commit.
- **canon-patterns.yaml propagation** of the 11 binds_up mappings -> P2+ (would break zero-diff if done now).

## Base 0.8.0 convergence (seam LOCKED)
plane adopted verbatim (no-op reconcile); base stages grain+scope as first-class fields + stage-2 value-validation, firing on the **canonization signal** (not the draft) to avoid churn across 18+ declarations. On canonization, send base the final tokens + the signal.
