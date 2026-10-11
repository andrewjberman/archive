# CANON_RUN_R5 -- the FWD-5 run: the onboarding checklist end to end on the practice wave

**Cell:** `CN-q-3`, LGIC_CANON round 5, slot `~1`. **Worker:** `0.9.0_WK_LGIC_CANON~1`, issued by `2.0.0_SA_COO~B1`.
**Subject:** the `LGIC_LGCTFM` practice wave `20260918T011619Z-8db9eb1` under
`workflows/legacy_transform/blackdiamond-49financial/`, `contract.json` hash `33204e29839de89af81fb293317cce3ccdf2266d`
(`git hash-object` on the file and `git rev-parse HEAD:<path>` agree). Shape: `C6_RUN.md` (round 4). Machine record:
`CANON_RUN_R5.json`.

Each step is a READ against 49financial's live state or a pure or dry-run call. No `safe-apply`, no Terraform, no AWS write,
no portal push, no route change, no IAM change. `live_acts` is `[]`.

## THE GRADE

```
  steps in the checklist ............................ 16
  graded units (step 14 split into 14a and 14b) ..... 17
  REACHED ............................................ 15   (1-9, 11, 12, 13, 14a, 14b, 15)
  CARDED ............................................. 2    (10, 16 -- owner ADVI_FIRMBKTS, both firm-bucket causes)
  reached + carded ................................... 17  (round 4: 12 + 4 = 16)
```

Round 4 reached 12 and carded 4 (10, 13, 14, 16). Step 13 and step 14a, the two causes outside the firm-bucket carve-out,
now read REACHED. Step 14b also reads REACHED here (below), so the carded set is the two firm-bucket steps only.

**The criterion Q3R5-AC1 does not pass, and not for a reason in the run.** Its check (`check_cn_r5.py run`) demands
`reached + carded == 16`. The order splits step 14 into 14a and 14b, which makes the units 17; no honest record of 16 steps
split that way sums to 16. Row `LGIC_CANON-D1-W1-S32`. Nothing was dropped or merged to fit the number.

## STEP BY STEP

1. **Identity row (R2,R5,R7).** REACHED. The 49financial FIRM row carries every field Step 1 describes
   (`tenant.pages` `["/trade-submission"]` now among them). `validate`: `VALIDATE: OK 54 system row(s), 14 scope row(s), 0
   warning(s) at registry@5b98192dc286ddde over all 13 registry file(s)`.
2. **Two forms in the schema (R1).** REACHED. `NAMING_SCHEMA.json` v1.17 has no `firm_forms` key; `validate` printed no warning.
3. **Vendor masters + pipeline tree (R3,R7).** REACHED. Masters `08242234`, `08335338`; `monolith_scopes` and `pipeline_trees`
   (`data/black_diamond/`, the family's directory) read, not invented.
4. **Regenerate the views (R1,R6).** REACHED via DRY RUN. `generate --out .scratch/gen_preview` wrote 13 files. All 13 differ
   from the committed file, only by the embedded registry-hash header and by rows for scopes other than 49financial (scope
   `4698`, vendors `commonwealth`, `yahoo`) that the registry gained since the last regeneration. The 153 lines carrying
   `49financial`, `49f` or a 49financial master id are identical in all 13. Nothing was written to a tracked path.
5. **Exemption list (R6,R7).** REACHED. `exemptions.json` carries `"opal-data-49financial"` with 19 declared principals.
6. **Mint the bucket (R1,R5,R6).** REACHED via READ. `s3-49financial.tf` is the template; the bucket is in
   `org_trail_read_logged_buckets` and `scope_bucket`; `bucket_provisioned` is `true`. No apply.
7. **Name every resource (R1,R7).** REACHED. `name('blackdiamond','49financial','gold-runner','runner')` ->
   `blackdiamond-49f-gold-runner-runner`.
8. **Bronze/silver (R4,R9,R10).** REACHED. Both addresses resolve into `opal-data-assets`.
9. **Gold/state/code (R5,R11,R13,R16,R21).** REACHED. All three resolve into `opal-data-49financial`.
10. **Platinum (R6,R12,R14).** **CARDED, owner `ADVI_FIRMBKTS`.** The edge auth validator reads
    `platinum/{firmId}/ownership_map.json` (`auth-validator-edge/index.mjs:174`) and the router asserts `platinum/advi/{firm}/`.
    Live read: `opal-data-portal-v2/platinum/advi/49financial/ownership_map.json` is 566205 B and `mix_summary.json` 11129 B;
    the `address()` home key in `opal-data-49financial` returns 404.
11. **Commit through the naming flagger (R1,R20).** REACHED. A synthetic diff with the literal `opal-data-49f` -> `NAMING REFUSE
    ... -> opal-data-49financial`, `NAMING-GATE: REFUSE 1 graded`, exit 1.
12. **Apply through `safe-apply` (R1,R18).** REACHED via DRY RUN. `grade('opal-data-49financial','S3_BUCKET')` ->
    `('CONFORMANT','opal-data-49financial')`.
13. **Census the firm's names (R1).** REACHED -- was carded in round 4. On CN-q-1's registry rows, the wave's 183 gradable
    contract names (1 planted row excluded) through `census --names` with no `--not-judged` file: rc 0, `CENSUS: COMPLETE 175
    judged + 0 carded + 8 ruled`, 0 RAISE (`check_cn_r5.py step13`: `PASS-R5-STEP13`). The checklist's own command
    `census --all-roots`: rc 0, `ALL-ROOTS ok=True roots_total=86 mapped=86 unmapped=0 completed=86 stopped=0 ... carded=0
    refused=0`.
14a. **Portal paths (R6).** REACHED -- was carded in round 4. `python lib/opal_portal_paths.py 49financial`: DERIVED 8 (the
    7-page core plus `/trade-submission`), CARDED 0; equals `FIRM_ALLOWED_PATHS['49financial']` (8 of 8).
    `--check`: `CHECK: firms=4 pages=35 graded_firms=3 skipped_firms=1 stops=0 OK`. See `portal-paths-r5b.result.md`.
14b. **The partner table (R6, register entry X8).** REACHED by READ for this subject. `partner-firms/49financial.tf` holds
    `module "firm_49financial"`; live `describe-table opal-partner-49financial` -> ACTIVE, 11 items;
    `grade('opal-partner-49financial','DYNAMODB_TABLE')` -> `OUT-OF-PATTERN`, which X8 (GRANTED, CONDITIONAL, owner
    `1.0.0_SA_CTO`) declares for exactly this table. X8's STOP is for a new firm's table; 49financial's is one of its four
    enumerated names. The order's text expected 14b carded under the firm-bucket carve-out; the evidence does not support that
    cause (the table is not a firm-bucket matter), so it is recorded REACHED and the difference is stated here.
15. **Open the routes (R6,R12).** REACHED. `FIRM_CONFIG` carries 49financial (`opal-data-bd`); `opal-data-bd` is shared with
    `mockadv` -- the file's already-ruled exception (CTO ruling 65047), not a new finding. No deploy.
16. **Confirm the served dashboard (R6,R12,R14).** **CARDED, owner `ADVI_FIRMBKTS`** (the same repoint as step 10). The
    content served today is read from the legacy tree in `opal-data-portal-v2`; an authenticated sign-in and its 401
    negative control are live acts this order forbids.

## NOTHING LIVE MOVED

`live_acts: []`. `infra/aws/lambda-edge/_shared/firm-config.mjs`, read by `git hash-object` before and after the run:
`0de2f0f6def5ee0583c9637886a4fed6e7ccf763` both times. (Round 4 read `07412e48...`; the file is registry-generated and the
registry moved since.)
