# EGRESS LEDGER -- 0.9.0_WK_NFRA_OPALAI~9

Authority: Andrew-direct 2026-09-26 ~03:2xZ (API egress is permitted this session; every call is ledgered by the seat that
makes it), as relayed by 2.0.0_SA_COO~O in the NFRA_OPALAI.TO-OA-g-3 spawn prompt. This ledger holds no identifier. The
tid, oid and email of the principal were held only in a temp file outside the repo, and that file was deleted after the act.

| # | time (UTC) | endpoint | method | credential | purpose | order | result |
|---|---|---|---|---|---|---|---|
| 1 | 2026-09-27T00:42:52Z | `https://graph.microsoft.com/v1.0/users?$filter=displayName eq 'Alyssa Keith'&$select=id,displayName,mail,userPrincipalName,accountEnabled` (Opal's Entra tenant, tid prefix 6810043e) | GET, read-only, via `az rest` | the operator's existing `az` sign-in to tenant "Opal Capital" | resolve Alyssa Keith's Entra oid for her portal-only grant (CTO ruling (B)) | NFRA_OPALAI.TO-OA-g-3 step 1 | rc=0; exactly 1 match (accountEnabled=true, mail present) |

Calls to Opal's own AWS in the same act are not egress. They are listed here for completeness: sts get-caller-identity,
iam get-role, sts assume-role into opal-gateway-access-admin (session wk-nfra-opalai-9-oa-g-3), the operator command's
POLICY read and single operator_transact at 00:48Z, and the dynamodb scans run by g3.AC1.sh and g3.AC2.sh.
