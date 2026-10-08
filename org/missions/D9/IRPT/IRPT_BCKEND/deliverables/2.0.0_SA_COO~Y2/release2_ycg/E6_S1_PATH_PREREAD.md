# E6 pre-read -- the admit-record read-back/delete path (row IRPT_BCKEND-D2-W156-S1)

By `2.0.0_SA_COO~Y2`, 2026-10-08 ~18:1xZ, ahead of E6 (CTO ADDENDUM 3 @3b0845f19e: the new pair names this path before any
write -- function read + delete-item first with a dry probe, laptop fenced read second, new grant last). E6 waits on ~P2's E5.

**Instrument:** `comp-iam service irpt-ycharts-generate` (TF declaration of `irpt-ycharts-generate-role`,
`infra/aws/terraform/investor-reporting/ycharts/generate.tf`, 17 statements). DECLARED, not an applied-policy read; the dry
probe in the pair is the live test.

| need | role grants (declared) | statement |
|---|---|---|
| read the admit's `UPLOAD#` row in `irpt-requests` | `dynamodb:GetItem`, `dynamodb:PutItem` on the requests table | 5 |
| decrypt it | `kms:Decrypt`, `kms:GenerateDataKey` (resource not printed by the tool) | 11 |
| delete it | **none**: no `dynamodb:DeleteItem` on the requests table in any of the 17 statements | -- |

**Reading:** route 1 covers the READ-BACK through the function (a direct invoke the handler already serves), not the
DELETE. The delete needs route 2 (laptop fenced) or route 3 (a new, scoped grant). The S3 object `artifacts.put` writes is a
separate key; its delete path is not yet read.

## The W174-S3 grant (CTO ADDENDUM 7 @dd1667f93a: E6's new pair carries it; laptop Terraform via MSTR)

Read 2026-10-08 ~18:5xZ by `2.0.0_SA_COO~Y2`.

- **Call shape at the E5 pin (fff1b0395a):** `served.py` `_advisor_owner` -> `reads.partner(email, tenant)` ->
  `CanonicalProfileReaders.get_partner_profile` (`_scope/canonical_profile_reads.py:105-113`): ONE `get_item` on
  `opal-partner-<firm_id>` keyed by `email`. No index, no Query, no write.
- **Registry firms:** `ids.firm_ids('data/firm_registry.json')` = 3 enabled client firms: `49financial`, `cottonwood`, `inflection`.
  Live tables `opal-partner-*`: 4 (those three plus `opal-partner-demo`, which is NOT in the registry and NOT granted).
- **Encryption:** all three tables are SSE-KMS on ONE customer key `arn:aws:kms:us-east-1:313476888478:key/86cc6c40-2387-4446-b7e1-de79392e06b3`,
  a different key from `opal-users-v2` (`64f25291-...`).
- **The grant, modelled on generate.tf's users-table statements (lines ~193-213):**
  1. `dynamodb:GetItem` on exactly `table/opal-partner-49financial`, `table/opal-partner-cottonwood`, `table/opal-partner-inflection`.
  2. **No KMS statement.** Key `86cc6c40-...` is the AWS-managed DynamoDB key: its policy (`kms get-key-policy`, read ~18:5xZ)
     allows `kms:Decrypt` to `{"AWS": "*"}` with `kms:CallerAccount = 313476888478` and `kms:ViaService = dynamodb.*.amazonaws.com`.
     A role holding `dynamodb:GetItem` on the table decrypts through DynamoDB with no IAM KMS grant (unlike `opal-users-v2`'s own
     customer key, which needed `DecryptCanonicalUsersTableViaDynamoOnly`).
  So the whole grant is ONE statement: `dynamodb:GetItem` on the three table ARNs.
