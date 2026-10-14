# IRPT_ANLREQ release 29b ADDENDUM 1 -- the missing KMS read for the owner check; no code rollback -- COO half

**WRITTEN, NOT APPLIED. No apply order is cut on this file until its blob matches the CTO half's text.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-14 ~15:5xZ. CTO half: SIGNED by `1.0.0_SA_CTO~DELL2` @6dc939b104 (`deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE29B_ADDENDUM_1_KMS_DECRYPT_CTO_HALF.md`, CTO msg 7715), written FIRST; this half is written on the same statement text. It amends the release-29b pair (COO half blob `355d8e9e8a`, CTO half @5389d0d949) and nothing else.

Claim words: MEASURED = this seat ran or read it in this session; RECORD = a committed record this seat opened; RELAYED = carried by another seat; INFERRED = said so; ABSENT = not read.

## 1. What happened, and whose miss it is

- **The sitting stopped at K1** (`TO-EXERCISE-R30`, applier `0.7.0_AE_CloudOps~AQ2`, msg 7710): R0i passed (advisor A's input row present and not B's), the tickets table COUNT was equal before and after (31, nothing written), and K1 as advisor B answered HTTP 503 `input ownership could not be verified`, the fail-closed answer. K2 and K3 were not run. RELAYED, AQ2's reads.
- **The cause** (MEASURED by AQ2 and re-read by this seat): the check's `GetItem` on `irpt-requests` is denied at the key, not at the table. This seat read the table's description: `SSEType KMS`, `KMSMasterKeyArn arn:aws:kms:us-east-1:313476888478:key/7f4d3042-10d8-49a7-b55e-3c963cea8111`; and the simulator for `opal-ticket-api-role`, `kms:Decrypt`: `implicitDeny`. AQ2 reports the key policy delegates to IAM and that `irpt-ycharts-generate-role`, which reads this table, holds `kms` statements (RELAYED, not re-read by this seat).
- **The miss is the issuer's:** the pair's R0g read the role's policy and the grant shape asked of the CTO (msg 7631) was `GetItem` only; neither read the table's encryption. The CTO signed the shape this seat asked for. The release-29b grant is therefore INCOMPLETE, and the second statement below is a second widening nobody had signed.

## 2. The state now, and the position on the code (MEASURED / RELAYED)

G is applied and C is live (`opal-ticket-api` CodeSha256 `Fg8MdfvC...`). A CLIENT-class analysis SUBMIT answers 503 and writes nothing. An INTERNAL human's submit is not checked and is unchanged. The Ticket Center is shown to Opal users only (PRD ADDENDUM v0.6), so the only client-class route to SUBMIT-FORM is a direct API call.
**Position: NO code rollback, concurring with the CTO half.** The pair's section 6 says a 503 on K1 rolls the CODE back; this addendum overrides that for THIS failure only. Reasons (MEASURED / INFERRED): the 503 fails closed and meets no live user; a rollback to the release-28 package re-opens row `W101-S3` (any client login could name another firm's input), which the fail-closed state does not; and the window is finished in session, with the NEVER-2 ledger of 29b kept open until K1 to K3 read as expected (the hard stop: finish in session or roll back; a half-landed deploy is not left). **If the window below fails, the code rolls back as signed.**

## 3. The one further statement (the second widening)

Added to the policy `opal_ticket_api_ddb` (`aws_iam_role_policy`, `infra/aws/terraform/ticket-center/main.tf`), after `IrptRequestsInputOwnerRead`, in the estate's own pattern (`infra/aws/lambda/investor-reporting/holdings/iam.tf` lines 108-118, `DecryptRequestTableViaDynamoOnly`):

```
      {
        Sid      = "IrptRequestsDecryptViaDynamoOnly"
        Effect   = "Allow"
        Action   = ["kms:Decrypt"]
        Resource = [data.aws_dynamodb_table.irpt_requests.server_side_encryption[0].kms_key_arn]
        Condition = {
          StringEquals = {
            "kms:ViaService"                               = "dynamodb.us-east-1.amazonaws.com"
            "kms:EncryptionContext:aws:dynamodb:tableName" = "irpt-requests"
          }
        }
      }
```

- **Who gains:** the ticket Lambda's service role. It may decrypt with THAT key only through DynamoDB and only for the table `irpt-requests`. No person gains anything; no key is created or changed.
- **What it does not grant:** no `GenerateDataKey` (the role never writes the table), no `DescribeKey`, no `kms:*`, no `Resource: "*"`, never the alias.
- **Contingency named:** if the plan or the K1 re-run shows the DynamoDB read path needs `kms:DescribeKey`, that is NOT added by the applier: STOP, report, and the CTO re-reads (a third statement is a third widening).
- **Limits (INFERRED, not verified against the simulator with every context):** the encryption-context condition key is the standard DynamoDB one; the simulator arms below discriminate it. The reference `server_side_encryption[0].kms_key_arn` of the data source was NOT read by this seat; the scoped plan shows the resolved key ARN and it must equal the table's `KMSMasterKeyArn` above.

## 4. The window (one applier, in this order; each step opens only when the one before reads met)

**G2:** in the applier's own worktree edit `main.tf` to add exactly the statement above (nothing else), commit it (the diff printed with its `git hash-object`); the scoped plan from `infra/aws/terraform/ticket-center` with `-target=aws_iam_role_policy.opal_ticket_api_ddb`: ONE in-place update that adds that one statement; the resolved `Resource` must equal `arn:aws:kms:us-east-1:313476888478:key/7f4d3042-10d8-49a7-b55e-3c963cea8111`; ANY other change: STOP, nothing applied. `safe-apply`. Read the policy back (`get-role-policy`): five statements, the new one exactly once, the earlier four unchanged.
**T5 (kms arms):** `simulate-principal-policy` for `kms:Decrypt` on the key ARN, one resource per call: (a) with `kms:ViaService` = `dynamodb.us-east-1.amazonaws.com` and `kms:EncryptionContext:aws:dynamodb:tableName` = `irpt-requests` -> allowed; (b) WITHOUT `kms:ViaService` -> denied; (c) with the right ViaService and a DIFFERENT tableName context -> denied; (d) `kms:GenerateDataKey` on the same key -> denied (implicit). Print every decision. (a) not allowed or (b) or (c) allowed: STOP, the statement is not what was signed; roll the statement back (remove it) and report; the code stays as the CTO half says only while the window is being finished, so report at once.
**R0i again, then K1 to K3** (`TO-EXERCISE-R30`, unchanged): K1, K2 and K3 each HTTP 400 `attachment.input_id is not available to the caller`, equal bodies, the tickets COUNT equal. **A 503 again is a STOP and a report; it is not retried.** A 2xx is BLOCKING (the check is not firing).
**Close:** the 29b ledger closes on K1 to K3 reading as expected. The partner page's PROD hold lifts only then (CTO half condition 5 of the pair).

## 5. Both branches

| state | safe? | evidence |
|---|---|---|
| G2 applied, K1 to K3 read 400 | the intended state | section 4 |
| G2 applied, K1 still 503 | fail-closed; STOP and report, the CTO re-reads (DescribeKey contingency); the code rolls back as signed if the CTO does not rule another way | section 3 |
| G2 not applied | fail-closed 503 for client-class callers, no live user; the code stays only while the window is being finished | section 2 |
| rollback | CODE first (VersionId `7vn6xyMOZjpSaKwiT73UaNfXj6mNSljr`), then both statements may stay (additive) | the pair's section 3 |

## 6. Limits named

- The key policy (delegates to IAM) was read by AQ2, not by this seat. No live read of the role's effective KMS access was made by this seat beyond the simulator `implicitDeny`.
- The Terraform state was not read; the plan is the first read of it for this root in this window.
- The positive arm (an owner's own client filing, 201) is NOT part of this addendum; the PRD v0.6 moves FWD-1's filer to an Opal staff user, whose submit is not owner-checked, so the 201 path stays covered by its 21 unit tests until a client-class filing exists.

## 7. Owed

1. The CTO half is signed (@6dc939b104) and binds to this half's statement text; a different statement text voids it.
2. The applier order(s) to `0.7.0_AE_CloudOps~AQ2` (G2 and T5; then `TO-EXERCISE-R30` resumes), each carrying a `# pipeline-override:` line, cut by this seat now.
