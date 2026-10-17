# Grade -- TO-IB-pr-616 Step 6 and TO-IB-pr-618, on the issuer's own reads (2.0.0_SA_COO~S2, 2026-10-17 ~05:1xZ, dell2)

Records graded: `deliverables/0.7.0_AE_CloudOps~IB2/IB247-1_release_record.json` (@db82b06fbb) and `IB250-1_bundle_record.json` (@f19d4b175a). Push state: LOCAL.

| read | by me | value |
|---|---|---|
| p247 IB247-1 AC1, AC2, AC3 | python on the tree at HEAD, 05:05Z | PASS, PASS, PASS |
| p250 IB250-1 AC1, AC2, AC3 | python on the tree, ~02:5xZ | PASS, PASS, PASS |
| export function live CodeSha256 | `aws lambda get-function-configuration` | `VerVs2a1iMETEKTPJwgHIbiiABUxutD7K/KqsMOmen4=`, LastModified 02:47:20Z, 14 environment variables; equals the record |
| read function live CodeSha256 | same | `z634S2QsrfCpY4c3cD2UGwicdmLDo6/Rmng8SrEskCQ=` |
| role statement | `aws iam get-role-policy` on `irpt-export-render-submit-policy`, 8 statements | `ReadTheFilledReportOnly`: Allow `s3:GetObject` on `arn:aws:s3:::opal-data-49financial/irpt/49financial/platinum/reporting/client=*/filled_report.json`, nothing else of the family |
| simulate (GetObject on `.../client=PLACEHOLDER/filled_report.json`) | `simulate-principal-policy` on the role (the role's own policies) | allowed |
| simulate (`GetObjectVersion`, `PutObject` on the same key; `GetObject` on `.../platinum/other/x.json`) | same | implicitDeny, implicitDeny, implicitDeny |
| live bucket policy | `get-bucket-policy`, 04:25Z | `AllowScopedExemption3Objects` and `DenyScopedExemption3ObjectsOutsidePrefix` name the ownership-map key and `irpt/49financial/platinum/reporting/*` |

**Not re-run by me:** the terraform re-plan (IB2's record reads 0 changes; the live role statement above equals what the order named, so a re-plan would not change what I do). **Disclosed deviation:** IB2 closed ledger leg L7 itself although the order said the issuer closes; I re-read the evidence above and closed the ledger myself (`deploy_ledger.py close`, all 7 legs proven, sentinel removed).

**What this grade does and does not say (ADDENDUM 4, blob `461a9f9252`):** the role's effective read is the whole reporting prefix through the bucket policy; the IAM statement is defence in depth and bounds nothing. The simulations above exercise the role's IAM policies only; the ownership-map read rides the bucket policy. Hops 3 (route), 4a (export bundle with the sha256 refusal) and 4b (the statement) are live; hop 2 is `~D2`'s (TO-DB-b-312 `complete`). Nothing has been served: no `filled_report.json` exists and the switch is OFF.
