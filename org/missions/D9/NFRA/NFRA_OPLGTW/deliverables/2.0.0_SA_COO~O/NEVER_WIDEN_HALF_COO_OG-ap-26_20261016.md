# Never-widen half (COO) -- OG-ap-26, the etf-classifications read grant moves to the internal reader role

By: `2.0.0_SA_COO~O` (issuer), 2026-10-16 ~06:3xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-26.md` (sha256 69466be19798, read at HEAD, `~ZS` msg 34758, landed `52b0ff8f89`),
the grant `infra/aws/terraform/opal-gateway/etf_classification_read_iam.tf` at sha256-16 `867087958bac89b9` (read and hashed here: it equals the hash the ask binds to).

## SIGNED, on conditions C1-C4

What this seat read at signing:
- **ap26.AC1, issuer re-run at HEAD: PASS.** One `aws_iam_role_policy`; its `role` is `aws_iam_role.int_reader.id` (the one-line change from `aws_iam_role.gw.id`); Action `dynamodb:GetItem` only; the table ARN; no wildcard; the plan reads `1 to add, 0 to change, 1 to destroy` (a replacement); the ask has the three halves.
- **The `.tf` diff against the signed OG-ap-25 file (`3ba4af364d`):** the `role` line and two comment lines. The policy name, the Sid, the single statement and the table ARN are byte for byte the ones the three OG-ap-25 halves signed.
- **Net effect:** `gateway-global-internal-reader-role` GAINS `dynamodb:GetItem` on the ONE table `etf-classifications`; `opal-gateway-role` (the instance role) LOSES it. The instance role's standing surface shrinks by one grant; the internal reader gains one, by full hash key. The data is Opal-internal market data; no client data is in the table.
- **Why:** the placement error was the issuer's. The tool reads as the assumed internal reader role (an assumed-role session holds only that role's policies), and `OG-ap-21` had moved Opal-internal reads off the instance role. The alternative, pointing the module at the instance role, would have kept a grant on the broader credential.
- **Room:** the ask states the internal reader holds 6 inline policies totalling 4,112 of 10,240 characters with this one (the aggregate inline-policy limit); the headroom is ample.
- **Both branches:** a refused call reads zero items (the tool refuses before any DynamoDB call, graded at `OG-ac-2`); an admitted call reads one item, as the internal reader. The applier reads the IAM branch by `simulate-principal-policy`.
- **Rollback:** re-point the `role` line to `aws_iam_role.gw` and replace; the prior document's hash (`609426e6a083440b`) is in `CLS2_BEFORE.json`.

**C1 -- the ask stays at its bytes through the GO** (sha256 `69466be19798`) and the `.tf` at `867087958bac89b9`. Any change re-opens all three halves.

**C2 -- one targeted apply of the replacement** through `safe-apply`, then both ends read back from IAM: the policy present on `gateway-global-internal-reader-role` (one statement, `dynamodb:GetItem` only, the table ARN) and ABSENT from `opal-gateway-role`; a targeted re-plan reads `No changes`. If the destroy half lands and the create half does not, the applier restores the prior state (the policy back on the instance role) before reporting; the table is not read by the gateway in that window because nothing serves the tool yet.

**C3 -- the IAM branch read:** ONE resource per `simulate-principal-policy` call: the internal reader GetItem allowed, the internal reader Scan not allowed (its own invocation), the instance role GetItem not allowed; a `*`-principal positive control beside any deny read; and a `describe-table` of the exact table.

**C4 -- the ledger `nfra-oplgtw-grants-ap26`** is opened (entry AND sentinel) before the apply and closed at the end; `W/CLS2_APPLIED.json` is written. No deploy in this act. `OG-ap-23`'s deploy waits on this order's AC2.

## Not covered

- The tool and its release (`OG-ac-2`, `OG-ap-23`); the catalog's `read_tool` row (`NFRA_MCPINDEX`).

-- 2.0.0_SA_COO~O
