# OG-ap-35 Phase A -- operator identity, the IAM preflight and the candidate (NO write ran)

Seat `0.7.0_AE_CloudOps~NFRA1`, 2026-10-17T03:12:09Z. Identifiers appear nowhere in this file: roles, operation names, counts and key names only.

## 1. Operator identity

- calling principal: an IAM user of the account (read access used for the before-record scan and the roster read)
- operator role: `opal-gateway-access-admin` (assumed for real: `sts get-caller-identity` names `arn:aws:sts::<acct>:assumed-role/opal-gateway-access-admin/ag1-phasea-readonly`)

## 2. Simulated actions on the role (one resource, `dynamodb:LeadingKeys` context where marked)

| action | LeadingKeys POLICY# context | decision |
|---|---|---|
| `dynamodb:GetItem` | no | **allowed** |
| `dynamodb:PutItem` | yes | **allowed** |
| `dynamodb:UpdateItem` | yes | **allowed** |
| `dynamodb:PutItem` | no | **implicitDeny** |
| `dynamodb:DeleteItem` | yes | **implicitDeny** |
| `dynamodb:Scan` | no | **implicitDeny** |

The act needs `PutItem` and `UpdateItem` with the context (allowed means no STOP). `DeleteItem` and `Scan` are expected implicitDeny: the writer's `activate()` builds only Put operations and never deletes.

## 3. The candidate and prepare() under the operator role

- prepare accepted: True
- base revisions read by prepare: profile 4, grant 4; equal to the live read: True
- **Changed keys (candidate scope against her live grant): operations**
- diff line count printed by prepare: 8
- candidate operations: describe, list, query (live: describe, download_filtered, list, query)
- next revisions if activated: profile 5, grant 5
- deny emails the plan would put: 1

## 4. What `activate()` writes besides the grant (read from the module, not assumed)

One transaction: the principal_profile put (revision +1, grant_revision +1), the data_entitlement put (the new revision), the operator_audit append, and one email_deny put per plan deny email, conditioned `attribute_not_exists(pk) OR (tid = :tid AND oid = :oid)`.
Her email_deny record today: present True, status active True, attribute names oid, pk, record_type, sk, status, tid.
The put's item carries tid, oid and status active; the browser-route deny state therefore stays what it is (a restricted principal that is denied the browser routes by contract C2 stays denied).
