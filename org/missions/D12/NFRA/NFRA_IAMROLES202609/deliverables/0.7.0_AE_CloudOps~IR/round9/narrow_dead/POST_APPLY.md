# IAM-z-1 PHASE B -- POST-APPLY, one line per act

**Seat:** `0.7.0_AE_CloudOps~IR` - **Order:** `NFRA_IAMROLES202609.TO-IAM-z-1` - **Risk:** WORLD
**GO:** msg 33438, all 8 halves SIGNED (COO @`3860c1c906`, CTO @`364e77ecdd`).
Acts run in the cell's order -- write-bearing names first, `opal-data-smartx` last: **4, 3, 1, 2**.

POST-APPLY: act4-fred-s3access: verified
POST-APPLY: act3-workspace-sync: verified
POST-APPLY: act1-shared-infra: verified
POST-APPLY: act2-smartx-pipeline: verified

---

## ACT 4 -- `delete-role-policy S3Access` on `FredIngestionLambdaRole`

**NEVER-2 entry:** `iamroles-r9-narrow-dead-fred-s3access`, opened 02:03Z before the act, closed after.
**Baseline re-read immediately before the act (the pair's stop condition):** the live `S3Access` document
canonically EQUALLED `ROLLBACK_FredIngestionLambdaRole_S3Access.json` (1 statement,
`opal-market-update/*` and `opal-market-update`) -> **MATCHED, so the act was signed.**

| check | result |
|---|---|
| `delete-role-policy` | rc=0 |
| `list-role-policies` **read back** (never the delete's own rc) | `fred-ingestion-secrets-read`, `SecretsManagerAccess`, `yield-curve-artifact-write` -- **3, and S3Access absent** |
| `get-role-policy S3Access` | **rc=254 `NoSuchEntity`** -- here the error IS the pass |
| positive control on the same call | `get-role-policy yield-curve-artifact-write` -> **rc=0**, so the instrument reads a real policy and the `NoSuchEntity` is the world |
| the fold's grant, before vs after | sha256 `9e39ddff2822b58f...` both sides -- **BYTE-IDENTICAL** |
| `simulate-principal-policy`, one `--resource-arns` per call | `s3:PutObject` -> **allowed**, `s3:GetObject` -> **allowed**, both on `opal-data-portal-v2/json/macro/yield_curve_fred.json` |
| **negative control** -- the retired destination | `s3:PutObject` on `opal-market-update/fred/raw/daily/x.csv` -> **implicitDeny** |

The negative control is what makes the pair's "both branches" readable: the narrowing demonstrably took
effect, and the fold demonstrably kept exactly the two actions it needs on exactly the one key it writes.
The simulated `allowed` is sound here rather than pattern-matching a name that does not exist -- the key
was written at 2026-10-11T23:00:58Z by z-6's graded fire, so the resource is real.

**Why the 23:00Z fire is NOT a leg of this entry.** The cell's step 7 asks for one real run on each
changed role after the change. This role's next run is the `cron(0 23 * * ? *)` fire, ~21 hours out, and
NEVER-2 requires an act to finish in-session or roll back -- so holding the entry open until then would
be the half-landed state the rule exists to prevent. I closed on the document evidence plus the
simulation, and the fire is recorded as the **confirming, not gating,** read: it is already AC1/AC2 of
IAM-z-6, whose own grade re-runs tonight. If that fire fails, the rollback is
`put-role-policy S3Access` with the rollback document, and a row.

**Sequencing honoured:** the pair requires this act after z-6, which is COMPLETE @`4729bf8ba0` with live
`CodeSha256 KdzPgI23...`; the running code has `put_object` = 0, so nothing on the role calls
`opal-market-update` and the delete has no failure mode. This is why the act's error surface is
`implicitDeny` on a path no code takes, rather than the AccessDenied-at-`:257` it would have been in the
reverse order.

---

## ACT 3 -- `put-role-policy workspace-sync-permissions` on `workspace-sync-lambda-role`

**NEVER-2 entry:** `iamroles-r9-narrow-dead-workspace-sync`, opened 02:17Z before the act, closed after.
**Baseline re-read immediately before the act:** the live document (10 statements, 19 ARNs) canonically
EQUALLED `ROLLBACK_workspace-sync-lambda-role_workspace-sync-permissions.json` -> **MATCHED, signed.**

| check | result |
|---|---|
| `put-role-policy` | rc=0 |
| live document **read back** == the committed AFTER-document, canonical `sort_keys` compare | **True** |
| statements / ARNs | **10 / 15** live, matching the after-document's 10 / 15 |
| diff against the rollback | **4 ARNs gone, 0 added** |
| the 4 gone, per Sid | `[S3Access] ajb-workflow`, `ajb-workflow/*`, `opal-data-portal-s3`, `opal-data-portal-s3/*` |
| the kept control in the same Sid | `opal-data-news-av` -> **2 hits live** (bucket and `/*`) |
| actions | **every live statement has an action-identical twin in the rollback: True** |
| Sid set | live 10, rollback 10, **identical set: True** |

So the act removed exactly the four signed ARNs from exactly one Sid, added nothing, and changed no
action and no statement.

**The document is the whole oracle available here, and the pair says so.** The role has **0 functions**
(`comp-kuzu` over the served graph, with a validated positive control) and `RoleLastUsed
2025-12-30T19:10:42Z` -- 9.5 months. There is no consumer run to read, so the cell's step-7 "read ONE
real invocation" has no referent for this act. I am not substituting a weaker check and calling it that:
the evidence is the canonical document compare plus the kept-ARN control, and the absence of a run is
named rather than papered over.

The compact one-line form of the after-document was passed as `--policy-document` rather than a
`file://` path, to avoid both MSYS path mangling and the `aws.cmd` multi-line-argv cliff; argv length
1994, newlines 0. The read-back is what proves it arrived intact, not the put's rc.

---

## ACT 1 -- `shared-infra` Terraform: `aws_iam_role_policy.infrastructure_ops_permissions`

**NEVER-2 entry:** `iamroles-r9-narrow-dead-shared-infra`, opened 02:33Z before the act, closed after.
**Baseline re-read immediately before the act:** the live document (13 statements, 15 ARNs) canonically
EQUALLED its rollback -> **MATCHED, signed.**

| check | the pair required | measured |
|---|---|---|
| targeted plan | `{no-op: 1, update: 1}` | **`{no-op: 1, update: 1}`**, 0 add / 1 change / 0 destroy |
| untargeted plan before | 244 no-op + 1 update, 0 add, 0 destroy | **245 changes, `{no-op: 244, update: 1}`** |
| apply | -- | `safe-apply` of the **saved** plan: **0 added, 1 changed, 0 destroyed** |
| live document vs rollback | exactly `opal-data-smartx-v2/*` gone | **1 gone, 0 added**: `[S3InfraWrite] arn:aws:s3:::opal-data-smartx-v2/*` |
| statements / ARNs | 13 -> 13, 15 -> 14 | **13 / 14** |
| residual dead name | 0 | **0** |
| kept controls in the same Sid | both kept | `opal-infrastructure-snapshots` **1**, `opal-data-portal-v2` **1** |
| actions, Sids | unchanged | **action-identical twins: True; Sid set identical: True** |
| 0-diff after | 0 | **245 changes, all no-op, 0 to destroy** |

Code `0298578f63` on `wk-iamroles-r9-z1`, drained to `box/sitez` at `e259a408fe` (safe-merge rc=0, tree
check 1 needed / 0 dropped / 0 foreign). ACT 2's edit was deliberately left uncommitted so this drain
carried one act only -- verified before merging: 1 commit ahead, `smartx-pipeline/iam.tf` still modified.

**Two sparse-worktree gates fired before the apply, and both were instrument failures rather than
verdicts -- worth recording because each one fails CLOSED and says exactly what it needs.**
1. `safe-apply`'s HALT-gate refused with `unknown-base`: no agent home folder under `org/tier*_*/`
   matched my serial in the sparse cone. Its own message is the reason this matters -- *"Scanning a
   nonexistent inbox would PASS while a real [STOP] to the real you sits unread"* -- so it refuses
   instead of passing vacuously. Fixed by adding `org/tier2_senior/0.7.0_AE_CloudOps` to the cone, never
   by writing a different serial.
2. The naming limb then **BLOCKED** (`LGIC_ENFORCE DEC-6`, ENFORCE mode) with `NAMING ERROR
   lib/opal_naming.py is absent` -- again the cone, not a naming violation. Fixed by adding `lib`.
   `crossbox-deploy-check` had already WARNed on the same cause (`lib/devices.py`).

Neither was a finding about the act, and I did not treat "the gate blocked" as "the change is wrong".
The applied plan was the **saved** plan file from the graded run, so widening the cone changed what the
gates could read and nothing about what landed.

**No consumer run exists to read.** The role has 0 functions and `RoleLastUsed` **None** -- never
assumed since creation 2026-02-19. The cell's step-7 run has no referent here; the evidence is the
document compare, the kept-ARN controls and the 0-diff, and the missing plane is named rather than
implied clean.

---

## ACT 2 -- `smartx-pipeline` Terraform: `ec2_s3_access` + `ingestion_s3` (the last act)

**NEVER-2 entry:** `iamroles-r9-narrow-dead-smartx-pipeline`, opened 02:50Z before the act, closed after.
Run last, per the cell's ordering: `opal-data-smartx` is the only read-only grant of the five names.
**Baseline re-read immediately before the act -- all THREE documents, including the one that must not
move:** `s3-access` 3 stmt / 6 ARN, `smartx-s3-access` 2 / 6, `smartx-dynamodb-access` 1 / 1, each
canonically EQUAL to its rollback -> **MATCHED, signed.**

| check | the pair required | measured |
|---|---|---|
| targeted plan | `{no-op: 2, update: 2}` | **`{no-op: 2, update: 2}`**, 0 add / 2 change / 0 destroy |
| untargeted plan before | 45 no-op + 2 updates, 0 add, 0 destroy | **47 changes, `{no-op: 45, update: 2}`** |
| **`smartx-dynamodb-access` in either plan** | **absent -- its presence VOIDS the half** | **0 non-no-op entries in BOTH plans** |
| `s3-access` after | statements 3 -> 1, ARNs 6 -> 2 | **3 -> 1, 6 -> 2**; 4 gone, **0 added** |
| the 4 gone, per Sid | the two whole dead statements | `[SmartXDataReadWrite] opal-data-smartx-v2` + `/*`, `[SmartXLegacyRead] opal-data-smartx` + `/*` |
| `PortalViewsSync` | stays | **the only Sid left** |
| `ingestion_s3` after | statements 2 -> 2, ARNs 6 -> 4 | **2 -> 2, 6 -> 4**; 2 gone (both `opal-data-smartx-v2`), **0 added** |
| `MdpfFeedReadForDistribution` | kept | **kept** |
| `smartx-dynamodb-access` after | untouched | **byte-identical to its rollback** (1 stmt, 1 ARN, 0 gone, 0 added) |
| 0-diff after | 0 | **47 changes, all no-op, 0 to destroy** |

Code `2d7558d54d` on `wk-iamroles-r9-z1`, drained to `box/sitez` at `8502f777aa`.

**The distinction this act turned on.** `opal-data-smartx` is a 404 **S3 bucket** and a **live DynamoDB
table** (`arn:aws:dynamodb:us-east-1:313476888478:table/opal-data-smartx`, `drift=LIVE-no-DECLARED`).
A narrowing driven by the NAME would have deleted `smartx-dynamodb-access` and broken the ingestion
pipeline's table access. The act removed only `arn:aws:s3:::` ARNs, and the proof that it did is that the
DynamoDB document is byte-identical afterwards -- not that I intended to leave it alone.

**No consumer run to read, and the half says why.** Both roles are cold (`RoleLastUsed` 2026-06-01 for
the exporter, 2026-08-14 for ingestion) and both consumers already fail against the 404 bucket -- 30 live
S3 references in the exporter and 14 in the Lambda (row Z-S51). So the narrowing turns `NoSuchBucket`
into `AccessDenied` on a chain that is already dead; it does not break a working feature. If a scheduled
`opal-smartx-ingestion-pipeline` run fires and fails, branch B applies: roll back through Terraform and
file a row.

---

## ALL FOUR ACTS: WHAT CHANGED IN TOTAL

| act | surface | statements | ARNs | added |
|---|---|---|---|---|
| 4 | `FredIngestionLambdaRole/S3Access` | policy **deleted** | 2 -> 0 | 0 |
| 3 | `workspace-sync-lambda-role/workspace-sync-permissions` | 10 -> 10 | 19 -> 15 | 0 |
| 1 | `infrastructure-ops-lambda-role/infrastructure-ops-permissions` | 13 -> 13 | 15 -> 14 | 0 |
| 2 | `smartx-exporter-role.../s3-access` | 3 -> 1 | 6 -> 2 | 0 |
| 2 | `smartx-ingestion-lambda-role/smartx-s3-access` | 2 -> 2 | 6 -> 4 | 0 |

**13 dead ARNs removed across 4 roles and 5 documents, one whole policy deleted, three statements
dropped, and ZERO ARNs, actions, statements or Sids added anywhere.** Every one of the five names reads
`NoSuchBucket`, so every removed ARN pointed at a name any AWS account could have claimed. Four NEVER-2
entries, each opened before its act and closed after it, all legs proven.
