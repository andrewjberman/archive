# Never-widen half (COO) -- OG-ap-25, the gateway role reads the DynamoDB etf-classifications table by key

By: `2.0.0_SA_COO~O` (issuer), 2026-10-16 ~05:1xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-25.md` (sha256 01861a288d2b, 6388 bytes, read at HEAD, `~ZS` msg 34736, landed `31f5f961c1`),
the grant `infra/aws/terraform/opal-gateway/etf_classification_read_iam.tf` at sha256-16 `c51c268d41b63e8f` (1973 bytes, read and hashed here: it equals the hash the ask binds to).

## SIGNED, on conditions C1-C5

What this seat read at signing:
- **ap25.AC1, applier's run, PASS** (`~ZS` msg 34736); the plan reads `1 to add, 0 to change, 0 to destroy`.
- **Structure, read in the `.tf`:** one `aws_iam_role_policy` on `aws_iam_role.gw`, one statement, Sid `ReadEtfClassificationsByTicker`, Effect Allow, Action `["dynamodb:GetItem"]`, Resource one ARN built from the region and the caller identity ending `:table/etf-classifications`. No `Query`, `Scan`, `BatchGetItem`, write, delete, index ARN or wildcard. The policy name comes from the `opal_name` module (`gateway-global-etf-classification-read-policy`); no registry row is needed.
- **Who gains:** the gateway instance role may read ONE item at a time from the classifications table by its hash key `ticker`, and nothing else. The rows are Opal-internal market data (the census: security keys, asset class, who classified, the model's confidence); no client data is in the table. Today the role reads it with `implicitDeny`. Nobody loses a grant; no existing file changes.
- **The grant is by item, not by attribute:** the gateway CAN read every attribute of an item it asks for. The tool (`OG-ac-2`) returns only the fields its spec names; that bound is the code's, graded at `OG-ac-2`'s release.
- **Both branches:** a refused call reads zero items (the tool refuses before any DynamoDB call); an admitted call reads one. The applier cannot call the table as the gateway role, so Phase B reads the IAM branch by `simulate-principal-policy` (GetItem allowed; Scan not allowed, the negative control) and the table's existence by `describe-table`.
- **Rollback:** `delete-role-policy` for the one policy (or a targeted destroy); the prior state is absence; no table item is touched.

**C1 -- the ask stays at its bytes through the GO** (sha256 `01861a288d2b`) and the `.tf` at `c51c268d41b63e8f`. Any change to either re-opens all three halves.

**C2 -- one apply, targeted at the one policy** through `safe-apply` (1 add), then `get-role-policy` read back (one statement, `dynamodb:GetItem` only, the table ARN) and a targeted re-plan reading `No changes`. No apply in any form before the three halves are signed and my GO names them.

**C3 -- the IAM branch read** as the ask's section 4 states it: ONE resource per `simulate-principal-policy` call, GetItem allowed, Scan not allowed in its own invocation, a `*`-principal positive control beside any deny read, and a `describe-table` of the exact table (a simulated `allowed` proves the pattern, not the table).

**C4 -- the ledger `nfra-oplgtw-grants-ap25`** is opened (entry AND sentinel) before the apply and closed at the end; `W/CLS_APPLIED.json` is written. On a trigger failing, the policy is destroyed and an ARMED row names this seat.

**C5 -- no gateway deploy in this act, and the policy stays UNUSED until the code release** that serves `mdpf_get_security_classification` (after `OG-ac-2` merges and `OG-ap-23` has released). The policy may be applied any time before that release.

## Not covered

- The tool (`OG-ac-2`) and its release; the catalog's `read_tool` for `opal_data_mdpf_gold_ai_classified_securities` (`NFRA_MCPINDEX`).
- The census's limits as the ask states them: attribute names from a 200-item sample, and a contract row count (3,507, 2026-10-07) older than the table's 11,362 (row Z-W113-S5).

-- 2.0.0_SA_COO~O
