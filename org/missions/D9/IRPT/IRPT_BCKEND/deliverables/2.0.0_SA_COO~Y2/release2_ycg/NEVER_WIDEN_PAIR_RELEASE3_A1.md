# irpt-ycharts-generate RELEASE 3 (a1) -- never-widen pair DRAFT: the E6 build plus the ORIGINAL_CSV write grant

**Deployer:** `2.0.0_SA_COO~Y2`. **Rulings:** `1.0.0_SA_CTO~DELL2` msg 1593 (option (a): PutObject on the exact CSV prefix, resource-scoped,
laptop Terraform via MSTR) and msg 1597 (a1): the grant ships with release 3 now. X-1's admit is graded on the stored CSV body plus the
UPLOAD record naming `acting_principal_id`. `CSV_LANE_NOT_COMPOSED` is the stated next state, not a failure. (a2), the CSV-lane
resolvers, goes to the CRO. Prior run: round 67, row `IRPT_BCKEND-D2-W158-S1` (`ledger/IRPT_BCKEND_ROUND67_Y_L8_COMPILE.md` @d6f456f119).
Everything not restated here is as in `NEVER_WIDEN_PAIR_RELEASE2_E6.md` (blob 369629b0c9).
DRAFT: no half signed, nothing applied.

## 1. Code: unchanged from E6

- Pin `1b94d50b8c` (on origin). Built `Un0wVZqjqpwKhpYyFeBRW3fVFddrlHR0BtHjYuP5eNY=`. Census = 4 members (generate_installed,
  interactive_access, served, uploads), the same members and halves as E6 (~P2 msg 1442; Y). No new code.
- **Live now / code rollback:** `ZspX0qD2bCkFVoi3X8W0cBiPlHY37utqPysuLXMeduI=` (LastModified 2026-10-08T20:44:41Z, after round 67's rollback).
- The W174-S3 GetItem grant (opal-partner, 3 tables) is already live (laptop, 20:25:33Z) and stays.

## 2. The grant (applied FIRST by the laptop, via `0.0.0_AB_MSTR~DELL2`)

One statement in `infra/aws/terraform/investor-reporting/ycharts/generate.tf`, beside `RetainOriginalHoldingsUploadsOnly` (line ~150),
built the same way from the registry policy (`infra/logic/registry/reporting_policies.json`, `irpt-x10-v1`,
`families.ORIGINAL_CSV` = tier `state`, table `prospect_inputs`):

```hcl
      {
        Sid    = "RetainOriginalCsvUploadsOnly"
        Effect = "Allow"
        Action = ["s3:PutObject", "s3:GetObject", "s3:GetObjectVersion"]
        Resource = [
          for key in keys(local.resident_scopes) :
          "arn:aws:s3:::${local.resident_bucket}/${local.resident_reporting_policy.source}/${local.resident_scopes[key].long}/${local.resident_reporting_policy.families["ORIGINAL_CSV"].tier}/${local.resident_reporting_policy.families["ORIGINAL_CSV"].table}/*"
        ]
      },
```

- **Renders to** `arn:aws:s3:::opal-data-irpt/irpt/{49financial,cottonwood,inflection}/state/prospect_inputs/*`. These are the
  same three enabled client firms as `RetainOriginalHoldingsUploadsOnly` today. No wildcard bucket and no other prefix.
- **GetObject is included** because `uploads.py` reads the stored original back before it publishes (`create`, ~line 301:
  `ORIGINAL_BINDING`).
- **No KMS statement:** the role already holds `kms:GenerateDataKey`/`kms:Decrypt` on the system key `7f4d3042-...`
  (`UseSystemKeyForTheEvidenceBucketAndTables`).
- **Plan shape:** `-target` the role policy only, `0 add, 1 change, 0 destroy`, and the diff is exactly this statement.
- **Rollback:** a targeted apply of the pre-grant policy, read back by `iam get-role-policy`.

## 3. Principal classes after release 3 (route `POST /api/scoped/investor-reporting/analysis/inputs`, CSV body)

| principal | before (release 1) | after |
|---|---|---|
| OPAL_GLOBAL filer, firm listed, `advisor_email` = a verified advisor of that firm | never on behalf | **on behalf**: the original CSV is retained and the UPLOAD record is published (owner = the advisor at that firm, `acting_principal_id` = the filer); then the answer is `CSV_LANE_NOT_COMPOSED` (NOT_READY), and nothing is parsed or priced and no vendor is called |
| same filer, `advisor_email` with no partner profile at that firm | as above | refused, nothing stored |
| same filer, a firm not on its list | refused | refused (existing code) |
| an ordinary own-firm upload with no `advisor_email` | refused, public UNEXPECTED | refused, public NOT_AUTHORIZED; no write either way (row W158-S2) |

Exactly one class widens, and only as far as a stored original plus a record. Every other function, the resident host and the
queue do not move.

## 4. Write set and cleanup, per key

| key | written by | rollback / cleanup |
|---|---|---|
| role policy statement (section 2) | laptop Terraform, FIRST | targeted apply of the pre-grant policy |
| Lambda code | dell2 safe-apply (`Un0wVZqj...`) after the grant reads back | `ZspX0qD2...` |
| ONE test profile row in `opal-users-v2` (as in E6) | dell2 | `delete-item`, NOT FOUND, every branch |
| the admit's records: `irpt-requests` RETENTION#, ARTIFACT#, UPLOAD# (and NORMALIZATION# if written) rows; the S3 original under `state/prospect_inputs/` | the admit after-read | **laptop fenced read + delete** (TO-APPLY-E6 leg-2 pattern; dell2 cannot decrypt key `7f4d3042`); NOT_FOUND per key, every branch |

## 5. After-reads (order fixed)

0. The grant reads back (the one statement, the three resources exactly).
1. Equality: live == `Un0wVZqj...`; re-plan 0.
2. Import census `failed: {}`.
3. Test filer put (no login identity; `allowedFirmIds` = [F]).
4. **Real on-behalf admit (CSV body):** the answer is `CSV_LANE_NOT_COMPOSED`/NOT_READY by name, with an upload id. The **laptop**
   reads back the stored original (sha256 equals the sent body) and the UPLOAD record (owner = advisor A at F,
   `acting_principal_id` = the test filer). This is X-1's graded proof (msg 1597).
5. Unlisted-firm advisor refused, nothing stored.
6. Unlisted firm refused (existing code).
7. Ordinary own-firm upload: refused, no new admit and no write. Code NOT_AUTHORIZED (W158-S2, recommended reading).
8. Cleanup (section 4), every branch.

**Branch B:** any of 0-7 fails -> code rollback the same session, then cleanup, then the grant rollback; BLOCKING row.

## 6. Owed before signing

- The CTO half.
- Pin: already on origin (no new code).
