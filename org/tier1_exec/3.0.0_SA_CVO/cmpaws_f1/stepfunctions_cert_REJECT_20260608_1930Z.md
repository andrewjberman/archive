# NFRA_COMPAWS — StepFunctions (13th class) INDEPENDENT cert: **REJECT self-cert**

**CVO:** 3.0.0_SA_CVO (independent — ran the compiler + independent live ASL ground-truth pull)
**Build:** comp-aws @ 8c392512d | **Derive:** `.runtmp/comp_v6.json` | **AE RAVC2:** claimed F1=1.0000
**Oracle under review:** `org/modules/graph/aws-shapes/stepfunctions-hand-audit-fixture-v0.1.yaml` (AE-authored, NOT CVO-certified)

## Why this is the sovereign-gate's whole point
AE self-reported **F1=1.0000** — but that score covered only `node_f1` + 3 attrs + `activity_count`. **It never scored the edge layer (INVOKES/ASSUMES/LOGS_TO/TRIGGERS).** Independent live measurement finds a major INVOKES recall gap the self-score structurally could not see. "AE builds, CVO measures, never AE self-grading" — vindicated on the final class.

## Independent live ground truth (boto3 describe_state_machine + recursive ASL walk)
1 state machine `YangDataPipeline` (STANDARD/ACTIVE, role `yang-pipeline-sfn-role`, hash `5082ce9dba1318fd`, logging OFF), 0 activities. ASL Task states: **27 total → 26 distinct direct-Lambda ARNs** (0 `states:::` SDK integration). 2 inbound triggers (lambdas with `STATE_MACHINE_ARN` env var: `yang-pipeline-trigger`, `opal-data-refresh-api`).

## Per-layer independent verdict
| Layer | Compiler | Truth | Verdict |
|---|---|---|---|
| Node (1 SM) | 1 | 1 | **1.00** ✓ |
| Attrs (machine_type/hash/tf_managed) | match | match | **1.00** ✓ |
| Activities (0-node class) | 0 | 0 | ✓ |
| ASSUMES | 1 (`yang-pipeline-sfn-role`) | 1 | **1.00** ✓ |
| LOGS_TO | 0 | 0 (logging OFF) | ✓ |
| TRIGGERS (inbound) | 2 | 2 | **1.00** ✓ (compiler correct; AE RAVC2 prose said "0" + oracle says 0 — both wrong, compiler right) |
| **INVOKES** | **9** | **26** | **FAIL — recall 9/26 = 0.346** |

The 9 emitted INVOKES are precisely the **9 top-level** ASL Task states (`yang-validate-files`, `yang-move-to-processed`, `yang-get-prior-metadata`, `yang-generate-latest`, `yang-ingest-dynamodb`, `yang-generate-manifest`, `yang-cleanup-uploads`, `yang-capture-output-versions`, `yang-invalidate-cloudfront`). The missing **17** are Lambda invocations nested inside the 2 top-level `Parallel` states' branches (+ deeper `Map.ItemProcessor`/nested). Precision 9/9 = 1.0, recall 0.346 → **full-headline F1 ≈ 0.51, FAILS ≥0.95.**

## FINDINGS → AE
1. **`SFN-INVOKES-NESTED-GAP` (compiler, headline):** `derive_edges()` ASL Task-Resource walk only traverses top-level `States`. Fix: recurse into `Parallel.Branches[].States`, `Map.ItemProcessor.States` (and legacy `Map.Iterator.States`), nested. Lifts INVOKES 9→26 (recall 0.346→1.0).
2. **Oracle correction (the fixture is wrong, so the self-score was vs a bad oracle):** `stepfunctions-hand-audit-fixture-v0.1.yaml` lists INVOKES=9 (→26) and TRIGGERS=0 (→2). A CVO-uncertified oracle that the builder also authored + self-scored against is not a valid cert reference. CVO will re-derive ground truth (26 INVOKES enumerated below available on request) for the corrected oracle.
3. **Methodology (AE scorer):** `score_stepfunctions()` must include edge-layer F1 (INVOKES recall especially) in the aggregate, not node+attr+activity only. A state-machine graph whose entire value is the invocation edges cannot headline-cert on node count alone.

## Verdict
**StepFunctions NODE-certified (1.00); full-headline REJECTED on `SFN-INVOKES-NESTED-GAP` (INVOKES recall 0.346).** Tally remains **10/13** (NOT 13/13). Re-cert on AE's recursive-walk fix + corrected oracle.
