# SDK globgrph IAM-fidelity sweep -- 2026-07-19 (one-time, CTO-ruled security check)

**Owner:** `0.7.0_AE_CloudOps~B` · **Ruling:** CTO @225831Z (one-time sweep NOW; standing tool blessed-DEFERRED post-consolidation)
**Why:** the WS-8 structural cross-walk missed 2 IAM-CONTENT gaps (intraday under-grant, fedobs fail-open); a 3rd
undetected **fail-open** SDK role (tenant could write semantic truth) would be a live security risk. This sweep
grounds that no 3rd exists. **VERDICT: CLEAN.**

## Method
Every SDK globgrph role vs its real applied globgrph counterpart. Rule-22a on the APPLIED real roles
(simulate-principal-policy, ONE --resource-arn, isolated positive controls in SEPARATE invocations) + a
Deny-boundary census (get-role-policy) + SDK-policy read/compare. Fail-OPEN = SDK can write truth the real
role can't; UNDER-GRANT = SDK lacks what the mechanism calls.

## Denominator -- 9 SDK globgrph roles
| SDK role | verdict | grounding |
|---|---|---|
| fedobs_emitter_task | **FIXED this session** | was fail-open (producer on shared derive_runner); now scoped read-only-on-truth. sim: truth-write=explicitDeny / findings=allowed |
| incremental_updater | **FIXED this session** | was under-grant; now full BoundedDeriveReadOnly. sim: DescribeTable=allowed |
| derive_runner_task | CLEAN (faithful) | has DeriveRunnerAccountDescribe (estate-describe, fuller than incremental's); warehouse-write BY DESIGN (sole graph_edges writer). no Deny needed |
| nessie_task | CLEAN (by-design) | writes warehouse/* (Iceberg catalog manages all tables) + dynamodb version-store scoped to nessie_table_prefix*; matches real (DynamoAccess + S3WarehouseAccess) |
| trino_task | CLEAN (read-only) | SDK grants GetObject/ListBucket only (zero PutObject). sim on real: PutObject-on-truth=**implicitDeny**, GetObject=allowed. NOT fail-open |
| derive_runner_execution | CLEAN | ECS execution role (image pull + logs) -- no data write |
| nessie_execution | CLEAN | ECS execution role -- no data write |
| trino_execution | CLEAN | ECS execution role -- no data write |
| derive_runner_events | CLEAN | EventBridge -> ECS RunTask -- no data write |

## Result
- **FAIL-OPEN class (security):** Deny-boundary census -> ONLY fedobs carried an explicit Deny (fixed). trino
  sim-confirmed read-only. derive/nessie write by-design. execution/events roles no data write. **No 3rd fail-open.**
- **UNDER-GRANT class:** incremental_updater fixed; derive_runner faithful (has the estate-describe); non-resolver
  roles run no estate-resolver code. **No 3rd under-grant.**
- The 2 gaps the structural cross-walk missed were the ONLY ones. **Live security residual CLOSED.**

Standing IAM-fidelity cross-walk tool: BLESSED but DEFERRED (post-consolidation) -- operationalizes CTO's
faithful-by-construction WS-5 bar (VERIFIED not asserted); build when Andrew signals the consolidation phase changed.
