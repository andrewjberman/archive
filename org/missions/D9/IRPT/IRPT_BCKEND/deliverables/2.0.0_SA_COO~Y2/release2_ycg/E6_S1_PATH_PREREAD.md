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
