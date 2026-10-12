# IAM-z-6 PHASE A -- fred-data-ingestion retires its raw-series write to the 404 opal-market-update

**Seat:** `0.7.0_AE_CloudOps~IR` - **Order:** `NFRA_IAMROLES202609.TO-IAM-z-6` - **Risk:** WORLD
**Authority:** `1.0.0_SA_CTO~Z` ruling @3e091a9436; rows Z-S45 (mine), Z-S48 (issuer)
**Read time:** 2026-10-11T20:4xZ - 21:3xZ. Every live value below was measured in that window.
**Standing (Z-S40):** this survey names its read time; PHASE B re-reads its baseline before it applies.
**Worktree:** `C:/tmp/iam-r9-fred`, branch `wk-iamroles-r9-fred`, cut from `box/sitez` HEAD (verified equal).

---

## 0. THE FORM CHOSEN (the pair signs THIS)

**Retire the raw-series S3 write path entirely; keep the FRED fetch; leave the fold untouched.**

Concretely, in `infra/aws/lambda/fred-data-ingestion/lambda_fred_ingestion.py` only:

| removed | why |
|---|---|
| `upload_to_s3()`, `upload_json_to_s3()` | the only two `put_object` call sites in the module |
| `observations_to_csv()`, `get_series_metadata()` | became unreachable -- each existed solely to feed one of the two uploads |
| `self.s3_bucket`, `self.s3_prefix`, `self.s3_client` | the class no longer touches S3 |
| `os.environ.get('S3_BUCKET', 'opal-market-update')` and the `S3_PREFIX` read | the retired write was their only consumer |
| `import os`, `import csv`, `import io` | unused after the above (ruff F401 caught `os`; see section 7) |

**Kept:** `download_series()` and `process_frequency()`'s download loop, so each frequency still exercises
the FRED API and still reports `series_count` / `failed_series` in its result. **Untouched:** the daily
yield-curve fold (`lambda_handler` lines 282-291 at the base) -- not one byte of it changes.

`FREDIngestionLambda.__init__` drops two parameters, so its one call site changes with it:
`FREDIngestionLambda(api_key, s3_bucket, s3_prefix)` -> `FREDIngestionLambda(api_key)`.

**Why the fold then runs:** nothing in `process_frequency` can raise out to the outer `except` any more,
so control reaches the `if frequency == 'daily':` fold. The fold itself is already wrapped in its own
`try/except` and is documented best-effort, so it cannot re-break the ingest it now follows.

---

## 1. TWO CELL PREMISES CORRECTED (neither changes the ACT; both change the METHOD or the wording)

### 1a. The build method -- the cell's named build is forbidden for THIS function by the source map itself

The cell says: *"Build the zip locally the way `infra/aws/lambda/ci/build-and-upload.sh fred-pipeline
fred-data-ingestion` would."* That script must **not** be used here. `infra/aws/lambda/ci/lambda-source-map.json`
carries a `_build_note` on this exact function, verbatim:

> `"YALP_MDSRC.F2: NOT built via build-and-upload.sh. fred-data-ingestion is a pre-Rule-3 vendored-deps
> Lambda (~220 vendored files: requests/urllib3/certifi/idna/charset_normalizer). Standard
> build-and-upload.sh has no vendored-deps/whole-dir mode. F2 build = swap-into-deployed-zip
> (COO-signed-off Option Y): download the deployed zip, replace only the source-of-truth files[] .py,
> re-zip, upload. The files[] above are the repo source-of-truth; the deps are byte-identical to the
> prior deployed zip."`

So PHASE A used **Option Y**, the sanctioned build, and section 3 records it. This is a method correction,
not a scope change: the artifact still ends up as one zip at
`s3://opal-313476888478-lambda-artifacts/fred-pipeline/fred-data-ingestion.zip`.

### 1b. The failure MECHANISM is a raise at :273, not a return ordered before the fold

The cell says *"the handler returns 500 BEFORE the daily yield-curve fold (:276-291)"*. The 500 is
returned at **:306**, inside the outer `except`, and the fold sits at :282-291 -- textually **after**
`process_frequency` (:273) and **before** the normal return (:293-302). What skips the fold is that
`upload_to_s3` **re-raises** (`:139 raise`), so the exception unwinds from :273 straight past the fold.

The live log proves the mechanism rather than inferring it -- stream
`2026/10/10/[$LATEST]15f493fd2bc34983bf964be9cc3df986`, run `db4d9c08-fabc-47bd-8372-57d4ed183910`:

```
2026-10-10T23:00:29.577Z  Processing daily frequency data for 2026-10-10
2026-10-10T23:00:29.577Z  Downloading DCOILWTICO
2026-10-10T23:00:38.790Z  [ERROR] Error uploading to S3: An error occurred (NoSuchBucket) when
                          calling the PutObject operation: The specified bucket does not exist
2026-10-10T23:00:38.790Z  [ERROR] Lambda execution error: ... (NoSuchBucket) ...
                          Traceback (most recent call last):
                            File "/var/task/lambda_fred_ingestion.py", line 273, in lambda_handler
```

`:273` at HEAD is `result = handler.process_frequency(frequency, as_of_date)` -- the frame the traceback
names. The outcome the cell describes is exactly right; only the mechanism's wording is corrected, and it
is the mechanism that makes the chosen form sufficient.

**Corroborating positive control that the run gets that far:** secret `opal/external-apis` reads
`LastAccessedDate = 2026-10-10T20:00:00-04:00`, so the daily invocation reaches `get_fred_api_key()` and
succeeds there. The function is alive and failing at the write, not failing to start.

---

## 2. THE DIFF

Gate: `.tools/commit-gate.sh` **rc=0** -- `All checks passed!` / `OK: no unguarded strict-utf8 log reads.`
/ `OK: pre-commit gate clean for 1 of 1 file(s)`.

```
1 file changed, 26 insertions(+), 90 deletions(-)      13 hunks
removed non-comment lines: 74        added non-comment lines: 23
bytes 12109 -> 10383        lines 337 -> 272
CR bytes: 0        non-ASCII characters: 0 (base also 0, so the control discriminates)
```

Residual-surface census on the edited file -- every executable S3-write token is gone:

| token | count | token | count |
|---|---|---|---|
| `put_object` | 0 | `s3_client` | 0 |
| `upload_to_s3` | 0 | `s3_bucket` | 0 |
| `upload_json_to_s3` | 0 | `s3_prefix` | 0 |
| `observations_to_csv` | 0 | `get_series_metadata` | 0 |

Positive control on the same read (must be non-zero): `download_series`=2, `process_frequency`=3,
`FREDYieldCurveIngestion`=2, `get_fred_api_key`=3.

**One thing a later census must not misread:** `opal-market-update` still appears **2** times in this file
and `S3_BUCKET` **2** times -- all four inside the module docstring and the handler docstring, explaining
the retirement. They are COMMENT-class, not code. A bare substring census of the dead name will hit this
file; the classification is what makes the hit meaningful (the same discipline round 9's reference census
used).

---

## 3. THE ARTIFACT, BUILT WITHOUT UPLOADING (Option Y)

Builder: `scratchpad/z6_build.py`, run with `-I`. It copies every member of the **deployed** zip preserving
each `ZipInfo` (name, date_time, compress_type, attrs) and replaces exactly one member's bytes, then
asserts per member by sha256 that nothing else moved.

```
MEMBERS: deployed=195 candidate=195  (equal sets: True)
CONTENT-CHANGED MEMBERS: 1  -> ['lambda_fred_ingestion.py']
UNCHANGED MEMBERS (content sha256 equal): 194 of 195
SWAPPED MEMBER: lambda_fred_ingestion.py  12109 -> 10383 bytes
ZIP-BYTES: deployed=1056764 candidate=1071875
DEPLOYED-SHA256-B64:  ztobyfBFFsd05mtbxVuWAn6nsMb7FwnhvftqdSQbSZ0=
CANDIDATE-SHA256-B64: KdzPgI23K0f4Af5dIOqbyJTQ2SaeZgR+pKI5T4rMdRM=
```

**File list** (source map `files[]`, both present as zip members):

| member | before (sha256 head) | after | |
|---|---|---|---|
| `lambda_fred_ingestion.py` | `4b6c649aca942e4c` | `cdb8a33a550e82ab` | SWAPPED |
| `ingest_yield_curve_fred.py` | `fb079eb8567eaec0` | `fb079eb8567eaec0` | carried unchanged |

Vendored dep tree carried across (195 members, 13 top-level entries): `urllib3` 74, `requests` 36,
`charset_normalizer` 27, `idna` 17, `certifi` 8, `bin` 1, four `*.dist-info` dirs 23 total, plus the two
`.py` above.

> **Stated honestly:** the candidate's **container bytes are larger** (1056764 -> 1071875) even though the
> swapped member shrank, because Python's `zipfile` re-deflates each member at its own level. The
> source map's "the deps are byte-identical" claim holds at the only grain a consumer can act on -- member
> **content** -- and that is asserted per member by sha256 (194 of 195 equal), not assumed. If the pair
> wants container-byte identity instead, that needs a different builder and I have not built one.

---

## 4. DEPLOYED BYTES **ARE** THE BASE (the cell's step-1 check)

Source: `aws lambda get-function --query Code.Location` (presigned, 1218 chars), downloaded with curl rc=0.

```
deployed zip bytes:                 1056764
sha256(b64) of my download:         ztobyfBFFsd05mtbxVuWAn6nsMb7FwnhvftqdSQbSZ0=
CodeSha256 from the Lambda API:     ztobyfBFFsd05mtbxVuWAn6nsMb7FwnhvftqdSQbSZ0=   <-- equal: download intact
source map artifact_sha256:         ztobyfBFFsd05mtbxVuWAn6nsMb7FwnhvftqdSQbSZ0=   <-- equal: map is accurate
```

Per-file, deployed member vs repo file at HEAD:

| file | deployed sha256 | base sha256 | verdict |
|---|---|---|---|
| `lambda_fred_ingestion.py` | `4b6c649a...af9d` | `4b6c649a...af9d` | **IDENTICAL** |
| `ingest_yield_curve_fred.py` | `fb079eb8...3d29` | `fb079eb8...3d29` | **IDENTICAL** |

So there is **no running-bytes-older-than-built drift** here: the deployed code is exactly the pre-edit
base, and the whole delta PHASE B introduces is section 2's diff. `LastModified 2026-06-05T15:46:21` and
the source map's `last_deployed_at` agree.

**Function configuration, re-read live:** runtime `python3.11`, handler `lambda_fred_ingestion.lambda_handler`,
timeout 900, memory 512, role `FredIngestionLambdaRole`, and
`Environment` = **`null`** -- `length(Environment.Variables || {})` = **0**. The order's premise that zero
env keys force the `opal-market-update` default is confirmed on the live function.

---

## 5. THE ROLLBACK

`s3api list-object-versions --bucket opal-data-portal-v2 --prefix json/macro/yield_curve_fred.json`:
**1** version in total (auto-paginated, counted client-side), bucket versioning `Enabled`.

```
ROLLBACK-VERSION: opal-data-portal-v2/json/macro/yield_curve_fred.json 4B7uNcT9Rli6_4LWUQORdWyhoBaABq.l
```

That version is `LastModified 2026-08-05T23:02:30+00:00`, `ContentLength 675314` -- identical to
`head-object`, i.e. the latest version **is** the frozen artifact. Two consequences for the pair:

- There is **no earlier version to fall back to**; the rollback restores the state the key is in *now*.
- A fold **failure** needs no restore at all: the key is only written on success, so a failed fold leaves
  this exact VersionId in place. That is the second branch in section 8.

---

## 6. THE PLAN, AND WHAT IT READS BEFORE THE UPLOAD

`lambdas.tf:21-32` deploys from S3 and takes its hash from the **S3 object's own metadata**:

```hcl
s3_bucket         = "opal-313476888478-lambda-artifacts"
s3_key            = "fred-pipeline/fred-data-ingestion.zip"
s3_object_version = data.aws_s3_object.fred_data_ingestion_artifact.version_id
source_code_hash  = data.aws_s3_object.fred_data_ingestion_artifact.metadata["content-sha256"]
```

**Therefore the plan cannot show this change before the artifact is uploaded** -- it is the cell's stated
alternative branch. What the plan reads right now, measured on the live object:

```
VersionId      T5QPdxBm94U_iA4R6iJscrZkVj_AWJDW
LastModified   2026-06-05T15:45:46+00:00
ContentLength  1056764
Metadata       {"content-sha256": "ztobyfBFFsd05mtbxVuWAn6nsMb7FwnhvftqdSQbSZ0="}
```

Both inputs still describe the **deployed** artifact, so the targeted plan is necessarily a no-op. Measured,
graded from the saved plan via `show -json` (never a positional slice of the human output):

```
PLAN: fred-pipeline -target=aws_lambda_function.fred_data_ingestion
  resource_changes entries: 1      ACTION HISTOGRAM: {'no-op': 1}      NON-NO-OP TOTAL: 0
  (human line: "no differences, so no changes are needed")
```

Untargeted plan, beside it:

```
PLAN: fred-pipeline (untargeted)
  resource_changes entries: 28     ACTION HISTOGRAM: {'no-op': 28}     NON-NO-OP TOTAL: 0
  (human line: "No changes. Your infrastructure matches the configuration.")
```

**fred-pipeline is fully converged**, so unlike round 7's `shared-infra` and `market-overview` acts,
`-target` here is **not load-bearing** -- it is belt-and-braces. PHASE B's apply can ride nothing
unexpected, and the number to re-check at apply time is this 28/28.

`terraform init` was required first (backend `s3` uninitialised in this checkout); it installed
`hashicorp/aws v5.100.0` and rc=0. The plans ran in the shared tree, which is sound here precisely
*because* the plan reads the S3 object and not my worktree file -- the edit cannot influence it.

---

## 7. ONE DEFECT THE GATE CAUGHT IN MY OWN EDIT

First `commit-gate.sh` run: **rc=1**, `F401 'os' imported but unused` at line 25. Removing the two
`os.environ.get` calls had orphaned `import os` and I had not noticed. Removed, re-run, rc=0.

Recorded because the ruff limb was the only instrument that would have caught it: `py_compile` passes an
unused import, and the function would have deployed and run correctly with it. The cost of the gate here
was one re-run.

A separate instrument note from the same hour, worth the line: the gate's **first** failure was
`ModuleNotFoundError: comp_constants_cli` -- my worktree's sparse cone did not include
`org/modules/graph/`. That is an **instrument** failure, not a code verdict, and reading it as "the gate
refused my code" would have been wrong. Fixed with `sparse-checkout add org/modules/graph org/standards`.

---

## 8. WHAT THE NEVER-WIDEN PAIR MUST COVER (blast radius, both branches)

**Blast radius:** (i) the code of one Lambda, `fred-data-ingestion`, via its one S3 artifact; (ii) one
served key, `s3://opal-data-portal-v2/json/macro/yield_curve_fred.json`. Nothing else: no env, no
schedule, no IAM document, no `fred-macro-ingestion`, no second key.

**Branch A -- the fold succeeds.** The key is written with 10 valued tenors; `LastModified` moves off
2026-08-05T23:02:30Z; a new VersionId appears beside `4B7uNcT9Rli6_4LWUQORdWyhoBaABq.l`. The served
portal yield curve unfreezes after 67 days.

**Branch B -- the fold fails.** `run()` only calls `upload_to_s3` after its fetch, so a failed fold writes
**nothing**: the key keeps VersionId `4B7uNcT9Rli6_4LWUQORdWyhoBaABq.l` and its 2026-08-05 timestamp, and
the served artifact is exactly as frozen as it is today. The handler still returns **200** in this branch,
because the fold is best-effort by design (`result['yield_curve'] = {'success': False, ...}`) -- so
**AC1 would fail while AC2's `statusCode=200` could still read true**. The grade must read
`yield_curve_success`, not the status code alone. Per the cell I restore nothing on my own in this branch:
file a row and report.

**Read from the producer's own rule, not predicted from the input's shape** (NEVER-1): `run()` writes the
key on **every** success path, including the merge-preserve path where some tenors are carried forward from
the prior artifact. So a partially-empty FRED day still rewrites the key -- with real prior observations
for the empty tenors, never fabricated values, and it logs `PRESERVE:` per carried tenor. **Writers of this
key: N=1** (`ingest_yield_curve_fred.FREDYieldCurveIngestion.upload_to_s3`, reached only from this
function's daily fold); 1 rule read, and the fold passes **no** bucket/key arguments, so it always resolves
`DEFAULT_BUCKET='opal-data-portal-v2'` / `DEFAULT_KEY='json/macro/yield_curve_fred.json'`
(`ingest_yield_curve_fred.py:56-57`, `:256`).

**Weekly and monthly must not start failing for a new reason** -- they currently fail for the *same* reason
(`process_frequency` raises on the first upload, whatever the frequency). After this change they take the
download-only path and return 200. No schedule is touched.

**The fire set, enumerated rather than sampled** -- `eventbridge.tf` holds **6** rule blocks and **6**
target blocks, and **5** of them drive *this* function (the 6th, `fred_macro_daily` `:163`, drives
`fred-macro-ingestion`, which this cell does not touch):

| rule | line | schedule | input frequency |
|---|---|---|---|
| `daily` | `:14` | `cron(0 23 * * ? *)` | `daily` |
| `weekly` | `:42` | `cron(0 14 ? * THU *)` | `weekly` |
| `monthly_early` | `:70` | `cron(0 15 ? * 6#1 *)` | `monthly` |
| `monthly_mid` | `:98` | `cron(0 15 15 * ? *)` | `monthly` |
| `monthly_late` | `:126` | `cron(0 15 25 * ? *)` | `monthly` |

So there are **five** fire paths into this handler, not three, and `monthly` fires **three times a month**
(first Friday, the 15th, the 25th). The order's preflight named three of the five; I am stating the full
set because AC4 asks whether *any other run frequency* started failing, and that question has five
answers. All five take the same `process_frequency` path, so all five move from 500 to 200 together.

This is a change from failing to succeeding, not a new failure mode -- but
it does mean **the weekly and monthly runs stop writing CSVs they were already not writing**, which is the
retirement the CTO ruled, applied uniformly across all three frequencies rather than only the daily one.

---

## 9. GRANTS: THE FOLD'S DESTINATION IS ALREADY COVERED, AND z-1'S TARGET IS ENTIRELY DEAD

Read live on `FredIngestionLambdaRole` (4 inline policies + 1 managed `AWSLambdaBasicExecutionRole`):

| policy | resource | status | TF-declared? |
|---|---|---|---|
| `yield-curve-artifact-write` | `arn:aws:s3:::opal-data-portal-v2/json/macro/yield_curve_fred.json` (Put+Get) | **the fold's grant -- live, key-scoped** | yes, `fred-pipeline/iam.tf:23` |
| `fred-ingestion-secrets-read` | `secret:opal/external-apis-EsGSYa` (us-east-1) | live, used 2026-10-10 | yes, `:45` |
| `S3Access` | `opal-market-update/*` **and** `opal-market-update` (Put+Get+ListBucket) | **both ARNs dead** | **no** |
| `SecretsManagerAccess` | `secret:FredApiKey-yWbGDi` (**us-east-2**) | **secret does not exist** | **no** |

Three consequences, all of them z-1's or the issuer's to act on, not mine:

1. **The fold needs nothing added.** Put and Get on exactly the one key are already granted, and `run()`'s
   merge-preserve `load_existing` uses `get_object` (not `list`), so no `ListBucket` is required. z-6 PHASE B
   needs **no** IAM change -- consistent with its BOUNDS.
2. **z-1's FRED act is a policy DELETE, not a narrowing, and it is an IAM-API act.** `S3Access` contains
   two ARNs and both are the dead bucket, so narrowing empties it; and it is **not Terraform-declared**
   (0 hits for `S3Access` in `fred-pipeline/iam.tf` against a positive control of **4** declared
   `aws_iam_role_policy` blocks in the same 4887-byte file, two of which are this role's). The one
   `opal-market-update` hit in that file is the comment at `:15`, not a grant. So the act is
   `delete-role-policy`, the same IAM-API re-route round 7 made for x-2's smartx act -- I will carry this
   into `NARROW_DEAD_SURVEY.md`.
3. **A fourth dead-reference class, newly found: a dead SECRET, not a dead bucket.** `SecretsManagerAccess`
   grants `GetSecretValue` on a us-east-2 secret that returns `ResourceNotFoundException`. Filed as row
   **Z-S49**; out of z-6's BOUNDS (`no IAM`) and outside z-1's five dead *bucket* names, so it is parked on
   the issuer with an owner rather than swept in silently.

### The sequencing point the CTO's ruling asked me to name

The ruling requires this survey to name *"the failure mode after narrowing (AccessDenied at :257)"*. It is
**order-dependent**, and the pair should know both orders:

- **If z-1's narrowing lands FIRST:** `:257`'s default still resolves to `opal-market-update`, the
  `put_object` still fires, and the error changes from **NoSuchBucket** to **AccessDenied**. Same break,
  same frozen key, *less* informative error -- strictly worse for whoever debugs it next.
- **If z-6 lands FIRST:** `:257` no longer exists. Nothing on the role ever calls `opal-market-update`,
  so deleting `S3Access` has **no failure mode at all** and the AccessDenied branch never materialises.

**Recommendation to the issuer: run z-6 PHASE B before z-1's FRED act.** They are independent per z-6's
DEPENDENCIES, so this is a free ordering choice, and taking it deletes a reachable bad state instead of
passing through it.

---

## 10. TWO OBSERVATIONS PARKED, NOT ACTED ON

1. **A vestigial second copy of this handler carries the same dead default.**
   `portal/etl/orchestration/green/fred/lambda/fred-data-ingestion/lambda_fred_ingestion.py:234` holds
   `os.environ.get('S3_BUCKET', 'opal-market-update')`. It is 10210 bytes / 296 lines, has **no**
   yield-curve fold, and is **outside my `<paths>`**, so I did not touch it. A `comp-find` of
   `FREDIngestionLambda|lambda_fred_ingestion` returns **4 HEAD hits across 187568 files scanned** -- 2 in
   the function's real source and 2 in that copy -- so after PHASE B the dead default survives in the repo
   in exactly one place, and a future census will find it there. Folded into row Z-S49.
2. **`S3Access`'s `ListBucket` on the bucket ARN** was never needed by this code even when the bucket
   existed -- `process_frequency` only ever called `put_object`. Noted for z-1's record so the delete is not
   mistaken for a capability loss.

---

## 11. WHAT PHASE A DID AND DID NOT DO

**Did:** edited one file in my own worktree (uncommitted there); ran the Rule-14 gate to rc=0; built the
candidate artifact locally and verified it member-by-member; proved deployed == base; read the rollback
version; ran both plans and graded them from `show -json`; measured the role's four policies; committed
**this survey only**.

**Did NOT:** upload the artifact, apply anything, touch IAM, open a NEVER-2 entry, commit the code edit,
or write the served key. No AWS write of any kind was made in PHASE A.

**PHASE B preconditions:** both halves of
`ledger/NEVER_WIDEN_ROUND9_Z-6_{COO,CTO}_HALF.md` SIGNED, then the issuer's GO. The grade is the
`cron(0 23 * * ? *)` daily fire; today is **Sunday 2026-10-11**, so the fold will carry Friday 2026-10-09
as the last trading day's observations -- AC4's "as of the last trading day" must be read against the
trading-day frontier, not the calendar day.
