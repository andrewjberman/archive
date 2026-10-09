# Never-widen ask -- OG-da-1, the data_refresh admission fails closed

By: `0.7.0_AE_CloudOps~Z`, 2026-10-09, PHASE A (build and measure; nothing is deployed, uploaded or sent).
Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-da-1.data-refresh-admission-fail-closed.md` @e9bfb749dc.
Ruling: `1.0.0_SA_CTO~Z` msg 32354 (relayed by `0.0.0_AB_MSTR~Z` msg 32368) on dell2 row `TCKT_VNEXT-D2-W6-S2`.

**Halves owed:** `1.0.0_SA_CTO~Z` (the site-Z CTO half, per the ruling) and `2.0.0_SA_COO~O`, both against THIS file at
its commit. **No deploy until both halves are at HEAD.**

---

## 0. The one open point the halves must settle

The ruling says admit `Dev` **or an Opal-internal principal (firm `opal-capital`)**. A firm-bearing field DOES reach the
Lambda, but it is named **`firmId`**, not `firm`, and its VALUE is not observable from this function's own logs. So this
ask implements BOTH recognisers and asks the halves to ratify the pair:

1. `tier == 'internal'` -- observable on 124 of 124 observed calls, and the authorizer's OWN internal test;
2. `firmId == 'opal-capital'` -- exactly the ruling's words, compared by exact match.

Either admits. If the halves want only (2), say so and this seat re-cuts: on today's evidence that would refuse the
majority of real callers, because `firmId`'s value is unverified from here (section 3).

**Also for ratification: how the ruling's two sentences compose.** "Admit Dev or an Opal-internal principal" and
"REFUSE an empty or null userType" resolve one way only -- an empty userType is refused UNLESS the principal is
independently Opal-internal. Read the other way, with empty always refused, the rule would lock out 65 of 124 observed
calls, which the order forbids ("every named caller must read ADMITTED"). The implementation takes the first reading.

## 1. The drift: the live function does NOT equal HEAD, and it is comments and line endings ONLY

The order required this named before any deploy, because a deploy from HEAD ships the difference too. Measured by
downloading the live zip (`lambda get-function` presigned URL) and diffing every member. **The download's sha256 equals
the live `CodeSha256 E4944Imr7Y4S4//rTR6HN5sbwczbwLw5DcaH4IZ0D0E=`, so these are the authentic live bytes.**

| member | live | HEAD | difference |
|---|---|---|---|
| `check_triggered_by.py` | 1880 B, 55 CRLF | 1825 B, 55 LF, 0 CRLF | **line endings ONLY.** Content byte-identical once normalised. +55 B = exactly the 55 CR bytes |
| `lambda_function.py` | 82655 B, 1894 CRLF | 80853 B, 1895 LF, 0 CRLF | line endings, PLUS one comment hunk |

The live zip holds 2 members. Six other files in `infra/aws/lambda/data_refresh/` (`deploy.sh`, `diagnose_auth.sh`,
`fix_triggered_by.sh`, `test_auth_context.py`, `FIX_COMPLETE.md`, `TRIGGERED_BY_FIX_SUMMARY.md`) are NOT packaged and
must stay unpackaged; the new `test_admission_gate.py` is a test and likewise must not ship.

**The whole real hunk, normalised diff, HEAD vs live:**

```
@@ -169,8 +169,7 @@
-        # Method 2: JWT authorizer claims (claims in authorizer.claims) -- NOT Cognito;
-        # Opal does not use Cognito, the bearer is a portal-issued RS256 JWT
+        # Method 2: Cognito JWT authorizer (claims in authorizer.claims)
```

HEAD carries the corrected comment; live still carries the old "Cognito" wording. Introduced on box/sitez at
**`a2c88e77ae`** (2026-09-03, `0.7.0_AE_CloudOps~Z`, NFRA_OPSEC202609 TO-OP-S-1: "no Cognito claim survives in the eight
Lambda sources").

**ZERO EXECUTABLE DRIFT, proven by the right instrument.** `ast.parse` + `ast.dump` of live-normalised and HEAD are
byte-identical (same 175051-char dump, same sha256 `0a36ce03244b6a1f...`), because comments and line endings are
invisible to the parser. NEGATIVE CONTROL: flipping one `return False` to `return True` in a copy changes the dump, so
the comparison does discriminate. **Therefore a deploy of HEAD plus this fix changes no behaviour except this fix.**

## 2. The fix (one file, `infra/aws/lambda/data_refresh/lambda_function.py`)

`validate_user_type` admitted on `if not user_type or user_type == 'Dev'` (line ~165), so an EMPTY userType admitted --
and dell2's row counts 45 PROFILE rows with no userType. A call with NO authorizer context at all was admitted as a
fictional `dev@test.com` ("development fallback", Method 3).

New rule, all three paths:

- **Method 1 (Lambda authorizer):** `userType == 'Dev'` admits. Otherwise `is_opal_internal(context)` admits. Otherwise
  REFUSE, with the reason logged.
- **Method 2 (JWT claims):** the SAME rule, against the claims dict.
- **Method 3 (no authorizer context):** REFUSES, and no longer names an actor of `dev@test.com`.
- New helper `is_opal_internal(context)`: `tier == 'internal'` or `firmId == 'opal-capital'`, both by EXACT match after
  `strip()`, nothing by truthiness, and `False` for anything it cannot positively recognise.

**One trap the implementation turns on.** The authorizer sets `firmId: J.firmId || "null"` -- the STRING `"null"`, not a
null. `if firm_id:` would be TRUE for it and would admit every principal with no firm claim, which is the same class of
hole this order exists to close. Exact match refuses it, and `test_ogda1_ac03` pins that arm.

## 3. The callers: every one is ADMITTED under the new rule

`W/da1_callers.json`. 14 days of `/aws/lambda/opal-data-refresh-api`, auto-paginated and counted client-side.
**No email, token or principal id appears there or here; callers are by role.**

| role | calls (14d) | userType | tier | admitted today via | admitted under the fix via |
|---|---|---|---|---|---|
| Opal internal staff account | 62 | `<EMPTY>` | internal | the EMPTY arm | `tier == 'internal'` |
| Opal internal staff account | 50 | Dev | internal | `userType == 'Dev'` | `userType == 'Dev'` |
| Opal principal / operator account | 4 | Dev | internal | `userType == 'Dev'` | `userType == 'Dev'` |
| Opal engineering account | 3 | Dev | internal | `userType == 'Dev'` | `userType == 'Dev'` |
| Opal internal staff account | 3 | `<EMPTY>` | internal | the EMPTY arm | `tier == 'internal'` |
| non-production test principal (opal.test) | 2 | Dev | internal | `userType == 'Dev'` | `userType == 'Dev'` |

**6 of 6 admitted, 0 refused**, exercised against the real function: each row's observed context was run through the
patched `validate_user_type` and printed ADMITTED, with Dev as the positive control and 9 of 9 control cases as wanted
(including `firmId == 'null'` REFUSED).

**PATH CENSUS, 14 days:** Method 1 = 124, **Method 2 (JWT) = 0, Method 3 (no authorizer) = 0.** Refusing Method 3 and
tightening Method 2 therefore breaks no observed caller. LIMIT, stated rather than hidden: 14 days is the window, not
all time. A caller that last called 15+ days ago is outside it, and a caller with a non-Dev userType and no internal
signal WOULD now be refused -- that is the point of the change, and it is the one way this act can bite.

**Why the firm value is unverified.** `opal-data-refresh-api`'s own log line is a fixed-format print of `email`,
`userType` and `tier`, so it never shows `firmId`. An earlier count of mine read "0 of 124 lines carry `firm=`"; that
measured the print statement, not the context, and is corrected here. The context's real shape comes from the LIVE
authorizer (`opal-portal-authorizer`, `index.mjs`, downloaded): `{ email, name, tier, role, advisorId, firmId, officeId,
regionId, userType, allowedFirmIds, advisorKey, advisorName, advisorRole, firmRole }`, and that authorizer itself grants
ALL access on `tier === 'internal'`.

## 4. Tests

`infra/aws/lambda/data_refresh/test_admission_gate.py`, pytest, offline, no AWS and no network. Named exactly as
`da1.AC1.sh`'s header requires: `test_ogda1_ac01` (Dev admitted, the positive control) .. `test_ogda1_ac05` (no
authorizer refused, and the actor is never `dev@test.com`).

`bash .../r32/checks/da1.AC1.sh` -> `pytest rc=0; named tests passed 5 of 5; failed/error lines 0` / `RESULT: PASS`.
`.tools/commit-gate.sh` clean for 2 of 2 files.

## 5. Blast radius

- **One Lambda's code:** `opal-data-refresh-api`, via `module.data_refresh_api` in
  `infra/aws/terraform/data-refresh/main.tf`. Nothing else.
- **UNCHANGED:** the IAM role (`opal-data-refresh-lambda-role`), the environment, `timeout 60`, `memory_size 256`,
  `runtime python3.11`, every route, the authorizer itself, the API, and `portal-time-machine` (the other function in
  the same root). No cron, alarm, monitor or notification.
- **What changes in the world:** which callers the function admits. Nothing is written differently; the admission
  decision is the only behaviour this touches.
- **Writers of the served property:** the execution record in `opal-data-refresh-executions` gains no new writer. One
  value it records changes for the Method-3 path only: an unauthenticated call used to be stored with actor
  `dev@test.com` and is now refused before any write. Method 3 fired 0 times in 14 days, so no stored record is
  expected to change.

## 6. Rollback

Point the function back at the live artifact version through the same Terraform path and read `CodeSha256` back:

- artifact `s3://opal-313476888478-lambda-artifacts/data-refresh/opal-data-refresh-api.zip`
- **VersionId `WJQGGIAlTSMp0Vny8avvQ7LxflVuvLf6`**, ETag `15413b4ac88881c9b0e19dae0eceb215`, 19753 B, 2026-08-03
- **`CodeSha256 E4944Imr7Y4S4//rTR6HN5sbwczbwLw5DcaH4IZ0D0E=`**

Nothing else changes, so nothing else needs undoing. The bucket is versioned.

## 7. The deploy path (PHASE B, not done here)

1. NEVER-2 ledger `nfra-oplgtw-og-da-1-data-refresh-admit`, entry AND sentinel committed before the act.
2. Build and upload the artifact. `module.data_refresh_api` is a `yang-lambda`, so `source_code_hash` comes from the S3
   object's `content-sha256` USER METADATA and `s3_object_version` from its version id -- a bare `aws s3 cp` without
   that metadata breaks the apply. Verify the upload on size AND metadata, never on `rc=0`.
3. `terraform plan -target='module.data_refresh_api' -out=...`; expect **1 resource changed, code only**
   (`source_code_hash`, `s3_object_version`, `last_modified`). Any other row is a STOP. Apply the SAVED plan through
   `bash .tools/safe-apply.sh`. Never `aws lambda update-function-code`.
4. Read back `CodeSha256` equal to the built hash, `State Active`, `LastUpdateStatus Successful`, and a post-apply
   re-plan reading `No changes`. Close the ledger and commit before any proof.
5. `AC3` is the CVO's at L9: each caller in `W/da1_callers.json` reads ADMITTED in the function's own log on its first
   real call after the deploy. This seat records it UNVERIFIABLE-BY-INSTRUMENT and names the CVO.

## 8. Halves

**CTO (`1.0.0_SA_CTO~Z`) -- owed.** Please settle section 0: the two recognisers (`tier == 'internal'` and
`firmId == 'opal-capital'`), and the composition of the ruling's two sentences.

**COO (`2.0.0_SA_COO~O`) -- owed.** Please sign sections 5, 6 and 7: the per-resource blast radius, the named rollback,
and the deploy path.
