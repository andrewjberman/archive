# irpt-ycharts-generate RELEASE 6 -- never-widen pair DRAFT (the custody factory: a Performance client statement is accepted)

**Deployer:** `2.0.0_SA_COO~Y2`. **Applier:** `0.7.0_AE_CloudOps~DELL2`.

**Source:** round 76, `IRPT_BCKEND.TO-IB-yr-761`, drained @2ae4d86e00; L8 packet `ledger/IRPT_BCKEND_ROUND76_Y_L8_COMPILE.md`
@bea2a2ceb3.

**Sequenced AFTER release 5b** (`release4_ycg/NEVER_WIDEN_PAIR_RELEASE5B_E11.md`, `TO-APPLY-Y75`). Release 6's package carries 5b's six
members, and its rollback target is 5b's build. If 5b has not landed, this pair does not start.

DRAFT: no half signed.

## 1. Pin and artifact

- **Pin:** box/dell2 `bea2a2ceb3` (LOCAL when drafted). It must be on origin before the apply.
- **Built** (BUILD_ONLY at the pin, this seat; reproduced twice): `V6EiBNcJ2267Ox2cZAj7VZC+rlv+XrmpW5y6aCr/YOM=`.
- **Expected live at start / ROLLBACK:** `5FRkux2oSNN1jB4xJEibio+F9F2ofl9mgcuH9jN/JrY=` (release 5b). Live when drafted was
  `Un0wVZqjqpwKhpYyFeBRW3fVFddrlHR0BtHjYuP5eNY=` (release 3), because 5b was still queued.

## 2. Three gates, run by this seat at the pin

| gate | reading |
|---|---|
| census | `changed_members=11`: 7 changed (composition, ExportBundle.schema.json, custody_submission, generate_installed, reporting_policies.json, repository, retention); 4 added (custody_interpreter, custody_ports, holdings_publication, holdings_publication_port). Against release 5b, only `generate_installed` and the 4 added members are new. |
| `checks/r73/cochange_closure.py` | `rows=88 commits_checked=33 split=0` |
| `checks/r71/symbol_closure.py` on the BUILT zip | `modules=66 pairs=296 missing=0 optional_fallbacks=2` (the fallbacks are ~M2's guarded `except ImportError` import, AMENDMENT 1 of IB-yr-761); build import-closure OK, 67 files |

## 3. Terraform, plan-only (this seat, `ycharts/` root, `-target` the two addresses): 1 to add, 1 to change, 0 to destroy

**Added:** `aws_iam_role_policy.generate_custody_factory`, named `irpt-ycharts-generate-custody-factory-policy` (from `name()`), on
`irpt-ycharts-generate-role`. Its rendered grants, printed beside each owner's statement (CTO/CVO condition, msg 2162):

| Sid | actions | resources (rendered) | owner of the read set |
|---|---|---|---|
| ReadCustodySilverSourcesByVersion | GetObjectVersion | `opal-data-assets/blackdiamond/cottonwood/silver/fact_holdings/date=*/data.parquet`, `.../fact_allocations/date=*/data.parquet` | ~P2 (`0.9.0_WK_IRPT_BCKEND~190/IB94-1_custody_ports_read_set.json`); cottonwood only, the interpreter's default admitted firm |
| ReadPinnedHoldingsPublication | GetObject, GetObjectVersion | `opal-data-{49financial,cottonwood,inflection}/irpt/<firm>/platinum/holdings/current/manifest.json` and `.../holdings/date=*/*` (6 ARNs) | ~M2 (`IRPT_BCKEND_ROUND34_M_L8_COMPILE.md`); no List, no Put |
| PutAndReadCustodyReports | PutObject, GetObject, GetObjectVersion | `opal-data-irpt/irpt/{49financial,cottonwood,inflection}/platinum/custody_reports/*` (3 ARNs) | ~M2 msg 2163 (policy row `irpt-custody-x10-v1`, family CUSTODY_REPORT) |

**Changed in place:** `module.irpt_ycharts_generate.aws_lambda_function.this`. The layers gain
`arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python312:16` (row `IRPT_BCKEND-D2-S19`). `opal-data-assets` is SSE-S3, so
no KMS grant is needed.

**Widens:** one role gains 3 statements over 11 ARNs, plus one layer. **No new principal class and no new route.**
**Moves:** one function. **Does not move:** every other function and every other policy.

IAM change reported to `0.0.0_AB_MSTR~DELL2` after the apply (Andrew-direct: dell2 writes its own IAM, reported after the fact).

## 4. After-reads (order fixed)

0. Live re-read at start is `5FRkux2o...`; otherwise STOP.
1. Re-run the symbol closure on the UPLOADED zip (downloaded back by version): `missing=0`, or STOP before the apply.
2. After the apply:
   - live == `V6EiBNcJ...`;
   - the policy reads back with exactly the 11 ARNs above;
   - the layers read `irpt-common` plus `AWSSDKPandas-Python312:16`;
   - re-plan 0;
   - the import census `failed: {}` gates the rest.
3. **Statement submission:** one Performance client statement submission for cottonwood, with no `input_id`, reaches the custody
   factory. The CloudWatch line shows no `CUSTODY_FACTORY_REQUIRED`. The outcome is an accepted custody entry, or a typed refusal
   from the factory's own validation, and its message is quoted.
4. **The prospect path holds:** one `input_id` submission still reaches the prospect factory (the release-3 shape).
5. **Cleanup, every branch:** every object read 3 wrote under `custody_reports/` is listed by version and named. The S3 deletes need
   Andrew's word.

**Branch B:** any of 0-2 or 4 fails, or read 3 raises `CUSTODY_FACTORY_REQUIRED` or an ImportError:
- roll back to `5FRkux2o...` the same session;
- remove the policy and the layer (a targeted revert apply);
- then cleanup, then a BLOCKING row.
Read the failing call's CloudWatch line BEFORE halting.

## 5. Owed before signing

- Release 5b landed (live `5FRkux2o...`).
- The CTO half.
- Pin `bea2a2ceb3` on origin.
- The service principal for IRPT_CUSTDY E2a's scoped POST (CTO msg 2124, the svc-analyst-intake pattern). It is named by the CTO, or
  by IRPT_CUSTDY's issuer, before the CTO half. This pair grants no principal for it.
- Andrew's word on the S3 deletes of the read-3 objects.
