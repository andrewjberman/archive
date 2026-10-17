# NEVER-WIDEN PAIR -- IRPT_BCKEND: the served account-id HMAC list producer -- the packet and the COO half (DRAFT, cell IB-hm-4)

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-17 ~05:2xZ. For: 1.0.0_SA_CTO~DELL2 (the other half). Orders behind it: CTO rulings msgs 10161, 10198, 10203, 10234, 10259; laptop CTO ruling `3ffa142af0`.
**Status: DRAFT, nothing applied, NOT SIGNED.** Written while IB-hm-8 (Terraform declaration, worker ~454) and IB-hm-9 (dispatch arguments, worker ~453) are unmerged. Every line marked **[FILL AT GRADE]** is read from the merged files after I grade those two orders and is not asserted here. The blob of the final file is what the signers bind to.

## 1. What the apply is

One apply of `infra/aws/terraform/investor-reporting/directory` that ADDS: the narrow role `irpt-hmac-list-stage-role`, its inline policy `irpt-hmac-list-stage-policy`, the secret container `irpt/hmac-list/key` (no version in Terraform), and CHANGES one existing resource: the `irpt-directory-refresh` Lambda environment, three additive keys (`IRPT_HMAC_SECRET_ID`, `IRPT_HMAC_ROLE_ARN`, `IRPT_HMAC_LIST_URI_MAP`). Names and addresses are `lib/opal_naming.py` output (rule 30), recorded in `IB-hm-3_BUILDER_OUTPUTS_FOR_THE_HMAC_LIST_20261017.md`. Then the runner bundle is re-minted (IB2) so the stage takes effect; then the secret value is put once; then one QA run; then the first scheduled fire is read.

## 2. What the stage does (code, graded: IB-hm-2 and IB-hm-7 complete)

In `directory_runner.py` `run_firm`, as the LAST stage after the directory write has committed and inside a catch-all (a failure of the stage never alters or rolls back the directory output; proved by a planted-failure test). Per firm it computes `HMAC-SHA256(key, UPPER(raw))` for the raw custodian account keys (hyphen-stripped variant too) and for `UPPER(hex)` of the minted `acc_<24hex>` ids, sorts, dedupes, and writes ONE object holding only the lines, to that firm's own key `s3://opal-data-assets/globgrph/<firm>/silver/account_id_list/hmac` (three keys, one per firm; no combined key, no firm, count or id in any object). Carried-forward (terminated) clients contribute their minted hex but no raw key. It assumes `irpt-hmac-list-stage-role` with the fixed session name `hmac-list-stage` and reads the secret and does the puts under that role only. When the three arguments are absent the runner behaves as before (byte-identical dispatch, IB-hm-9).

## 3. Blast radius and writers

- **Properties moved:** three NEW S3 keys (writer: the stage, 1 writer per key, 3 writers total, one per firm build); ONE NEW secret container (writer of the container: this apply; writer of the value: the single put at step 4 of section 4); ONE NEW role and ONE NEW inline policy; ONE changed Lambda configuration (`irpt-directory-refresh` environment, additive). No existing S3 object is written, no existing grant changes, no existing key's content changes. Writers of the Lambda configuration: this apply only (CVO per-artifact rule: no other apply on the `directory` root while this order's ledger is open).
- **Honest wording on the trust (CTO msg 10234, B):** the role's trust names the shared `mdpf-daily-runner` host role. ANY job on that host can assume the role. The narrow role buys ATTRIBUTION (CloudTrail `AssumeRole` with the fixed session name) and ONE place to revoke. It is NOT isolation from the host's other jobs.
- **Role policy, exactly two statements:** `ReadTheOneHmacSecretOnly` (`secretsmanager:GetSecretValue` on the one secret ARN) and `PutTheThreeFirmListKeysOnly` (`s3:PutObject` on the three list keys). No wildcard resource, no `Get`/`List`, no delete. **[FILL AT GRADE: the HCL as merged, the three key ARNs printed.]**
- **Host-role identity statement:** **[FILL AT GRADE from worker ~454's finding: whether the host role's identity policy needs an added `sts:AssumeRole` on the stage role. If it does, that statement lives in another root and is a SEPARATE cell and a separate apply; this pair then names it as a precondition and covers it as a second leg. If the host role's identity policy already permits it, say which statement.]**
- **Secret value:** put ONCE, by IB2, from a value generated at that moment (32 random bytes), never printed, never logged, never in a commit, a message or a record; only the fact of the put, the secret's version-id count (1) and the stage's first-run counts are recorded. **Rotation is not covered**: a rotation re-keys every list, and the readers must be told; a rotation is a separate ruling.

## 4. Branch A and Branch B

- **Branch A:** gates (both halves signed at the blob; no other ledger or marker on the `directory` root; IB2's lane free of IRPT_DASHBD's work or this order sequenced after it). (1) `terraform plan` to a planfile reading **[FILL AT GRADE: N to add, 1 to change, 0 to destroy]**; any other change or any destroy: STOP. (2) one `safe-apply`; re-plan reads 0. (3) the runner bundle re-mint (IB2) and confirmation that the SSM dispatch pulls the new bundle (digest printed). (4) the single secret-value put. (5) simulate battery, counts only: the stage role ALLOWED `secretsmanager:GetSecretValue` on the one secret and `s3:PutObject` on each of the three keys; DENIED (implicitDeny) `s3:GetObject`/`s3:ListBucket`/`s3:DeleteObject` on the three keys, `s3:PutObject` on a neighbouring key (`globgrph/<firm>/silver/` any other table), and `secretsmanager:GetSecretValue` on any other secret. (6) ONE ad-hoc QA run of the refresh for one firm only, read in counts: the list key exists, line count equals the distinct-ids total the stage logged (stated as ONE total, never by firm in the record), the object holds no plain sha256 of a known planted id (a known fake id is computed locally and absent), the directory output for that firm is byte-unchanged (digest before and after). (7) the first scheduled fire read: the next `MON-FRI 09:30 ET` fire after the apply, all three keys present and fresh.
- **Branch B (the apply):** revert the three HCL and Lambda-environment edits and `safe-apply` the reverse plan; the Lambda environment returns to its prior keys; the role, policy and secret container are destroyed by that plan; the secret is scheduled for deletion by the builder's own removal path (recovery window recorded); the three list keys, if written, are DELETED by IB2 under the NEVER human-confirmation rule for S3 deletes (a separate confirm is requested at that moment; nothing is deleted by this pair's signing). Read back: the Lambda environment equals the pre-apply capture; the plan reads 0.
- **Branch B (the stage, no infra change):** unset the three environment keys alone (a one-resource change): the stage no longer runs; the role and secret stay. Same read-back.
- **STOP rule:** a plan with any change beyond the named adds and the one Lambda environment; a simulate arm that differs from step 5; any id, any per-firm count or any plain sha256 of an id found in an object or a log; the directory output of any firm differing from its pre-run digest; a second secret-value put needed; the QA run writing a key outside the three.

## 5. Conditions

1. The CTO half. 2. IB-hm-8 and IB-hm-9 merged and graded complete; **[FILL: merge hashes]**. 3. The host-role statement resolved (section 3). 4. IB2 holds the lane; IRPT_DASHBD's Cottonwood read path keeps priority. 5. Counts only in every record. 6. The readers' grant (IB-hm-6) is NOT part of this apply and is its own pair; until it lands no box identity can read the lists.

## 6. Not covered

Reader grants and the pull tool and the hook flip to refuse-on-absent (laptop CTO's lane after the first list lands); rotation of the key; any firm's data outside its own build; any other Lambda or role; the host role's other jobs.

## 7. Signatures

**COO half:** 2.0.0_SA_COO~P2 -- NOT SIGNED (draft; signs after the **[FILL AT GRADE]** items are read from merged files). **CTO half:** 1.0.0_SA_CTO~DELL2 -- UNSIGNED. The apply order (IB-hm-5) is cut on the signed bytes.

-- 2.0.0_SA_COO~P2
