# Plan note -- transcripts key: the two Dell agent users may DECRYPT (NFRA_CTLPLN TO-CT-a-1, amendment 3)

Built and measured by `0.9.0_WK_NFRA_CTLPLN~14`. NOTHING was applied and NO `terraform plan` was run against the backend: the issuer measures the plan.
No object was read, no bucket listed, no decrypt call made. Evidence: `infra/aws/terraform/transcripts/tests/transcripts_access.json` (the first read),
`tests/read_transcripts_access.py`, `tests/check_transcripts_dell_decrypt.py` (both re-runnable).

## What the apply would show, by reading

- One resource changes: `aws_kms_key.transcripts` is UPDATED IN PLACE (its `policy` attribute gains one statement, `DellAgentUsersDecryptOnly`). Expected
  summary `0 to add, 1 to change, 0 to destroy`. Nothing is replaced: description, rotation, deletion window and alias are untouched.
- The new variable `dell_agent_user_names` is not a resource. The bucket, the bucket policy, `var.reader_principal_arns` (one user, whose statement is
  byte-identical in the render), the pull, mail-pull and chat-assist grants and their roles are not touched.
- The live key policy was read (`kms get-key-policy`): two statements, equal to the pre-edit render once a one-element list is read as KMS stores it.
  The only difference the plan should print is the added statement.

## What the two Dell users gain, and do not gain

- GAIN: `kms:Decrypt` on the key, so, with the object read their own policies already allow, they can read EVERY object in the transcripts store, the raw tier
  included (Andrew's word at 4.0.0_SA_CRO's terminal, record @a3e5396e1e item 5). `kms:DescribeKey` is also named; they already had it (their deploy policy allows it and the root
  statement delegates `kms:Describe*`), so that line adds nothing.
- DO NOT GAIN: encrypt, `GenerateDataKey`, `ReEncrypt`, key administration. Measured: against the rendered document `kms:Encrypt`, `kms:GenerateDataKey`,
  `kms:ReEncryptFrom`, `kms:ScheduleKeyDeletion`, `kms:PutKeyPolicy` are not allowed for either user under the KMS rule (10 of 10 arms; the raw simulator reads two of the ten as
  allowed on the pre-edit document as well, see row NFRA_CTLPLN-W14-S6). A write still fails at the key: their policies allow `s3:PutObject` on the bucket, but the bucket default is
  this key and they hold no `GenerateDataKey` on it.

## Is the object read already allowed without this change?

YES at the S3 layer, NO at the key. The simulator against each Dell user's LIVE policies: `s3:GetObject`, `s3:PutObject`, `s3:ListBucket` allowed by
`cloudops-dell-agent-deploy-policy` (the estate's `opal-data-*` bucket pattern), `s3:DeleteObject` explicitDeny; `kms:Decrypt` implicitDeny. The bucket policy declares
no Allow and no reader list (a TLS Deny and a write-under-another-key Deny only). So today a Dell read fails at the key; after the apply it succeeds.
Other users of the key today (declared in Terraform): 1 key-policy reader (the owner's user) and 3 grants (the pull role, the mail-pull role, the chat-assist function's execution role through the ldo module); live grants were not listed.

## Rollback

Delete the statement (and the variable) from `infra/aws/terraform/transcripts/main.tf`, i.e. revert the commit, and apply: the key policy returns to its two statements in one in-place update.
Do NOT roll back by setting `var.dell_agent_user_names` to `[]`: an empty `Principal.AWS` list is a malformed policy and KMS would reject the update. Rollback stops further reads only: content a Dell already read before the rollback is not recalled.

## What the simulator cannot show

A real decrypt of a real object (needs the apply and is another route's); the S3 bucket-policy conditions (`aws:SecureTransport`, the write-key Deny); organisation SCPs; live KMS grants;
and the KMS rule that a customer-managed key needs the KEY POLICY to permit use (the simulator unions identity and resource policies, so the proof uses a neutral identity policy for the
key-policy arms and composes the KMS rule explicitly).
