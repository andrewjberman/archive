# PORTAL_S3_SURVEY -- NFRA_IAMROLES202609.TO-IAM-x-5 PHASE A (row Z-S39, round-6 analysis Addendum 3 item E5)

**Cell:** IAM-x-5, the MOST URGENT of round 7. **Executed by:** `0.7.0_AE_CloudOps~IR`.
**Authority:** the round-7 issuance @`7203dca6ab`; Addendum 3 is `1.0.0_SA_CTO~Z` @`85cbea7549`.
**Measured:** 2026-10-11 ~10:2xZ-10:4xZ, worktree `C:/tmp/iam-w1b`, branch `wk-iamroles-r7-x5a`.
**PHASE A APPLIED NOTHING.** Every AWS call below is a read; the declaration edit was made, planned, graded and
then **reverted and never committed**, per step 3.

---

## 1. THE REQUIRED LINES

```
REFS: opal-data-smartx: env=0 code=0
REFS: opal-data-smartx-v2: env=0 code=0
REFS: opal-portal-data: env=0 code=0
REFS: opal-data-portal-s3: env=0 code=0
REFS: opal-market-data-v2: env=0 code=0
REFS: opal-data-aaii-sentiment: env=0 code=0
CONTROL: opal-data-portal-v2: env=1 code=16
PLAN: shared-infra: Plan: 0 to add, 1 to change, 0 to destroy.
```

**THE NARROWING BREAKS NOTHING: all six dead names have ZERO live references, in environment variables and in
deployed code alike.** The control is amply found, which is what makes those zeros readable.

> **EVERY ONE OF THOSE ZEROS WAS A NON-ZERO ON FIRST MEASUREMENT, AND THE CORRECTION IS THE MOST IMPORTANT THING
> IN THIS SURVEY.** A substring census over the same files returned `opal-data-smartx-v2: code=2`,
> `opal-data-smartx: code=1` and `opal-portal-data: code=1`. **All four were false positives**, and had I reported
> them the cell's own rule -- *"a reference found is NOT a reason to keep the grant: it is a broken feature the
> grant hides. Narrow anyway, and file the reference as its own row naming the function"* -- would have had me
> file three rows naming three production functions for features that are not broken. Section 3 classifies every
> hit.

## 2. THE SIX NAMES, RE-READ LIVE -- the error CODE, not an HTTP status

```
opal-data-smartx           rc=254  NoSuchBucket
opal-data-smartx-v2        rc=254  NoSuchBucket
opal-portal-data           rc=254  NoSuchBucket
opal-data-portal-s3        rc=254  NoSuchBucket
opal-market-data-v2        rc=254  NoSuchBucket
opal-data-aaii-sentiment   rc=254  NoSuchBucket
-- POSITIVE CONTROLS, same call, each its own invocation --
opal-data-portal-v2        rc=0    {"LocationConstraint": null}
opal-data-news-v2          rc=0    {"LocationConstraint": null}
```

`get-bucket-location` was used rather than `head-bucket` **because the order asks for the error CODE and
`head-bucket` cannot carry one**: it is a HEAD request, so the response has no body and S3 transmits no code --
the CLI prints a bare `(404)`, which is an HTTP status. `get-bucket-location` is a GET and returns
`NoSuchBucket`. (x-2's AC1 failed on exactly this distinction; the lesson is applied here rather than re-learned.)

## 3. THE REFERENCE CENSUS, AND WHY A SUBSTRING COUNT IS NOT A REFERENCE COUNT

**ENVIRONMENT VARIABLES** -- `get-function-configuration` on each of the **12** functions that carry this role
(12 of 237 live functions, denominator printed; the consumer set was read from the role ARN, not guessed). Every
dump was size-checked so a failed call could not read as zero references.

| name | env refs | where |
|---|---|---|
| all six dead names | **0** | -- |
| **CONTROL `opal-data-portal-v2`** | **1** | `opal-portal-fear-greed-fetcher[S3_BUCKET]` |
| `opal-data-news-v2` (also kept) | 1 | `opal-news-ai-sentiment[S3_BUCKET]` |

**DEPLOYED CODE** -- read through the **source map**'s declared file list (`lambda-source-map.json`), never by
filename, per the order. 13 files across 12 functions. **Raw substring hits vs real references:**

| name | raw substring | REAL code refs | what the difference was |
|---|---|---|---|
| `opal-data-smartx-v2` | 2 | **0** | both inside the **docstring** of `check_smartx_pipeline()` in `opal-infrastructure-monitor`, which documents that a prior check watched this dead bucket and was REPLACED. Proven by counting triple-quote delimiters before the line: 11, odd, so the line is inside the docstring. |
| `opal-data-smartx` | 1 | **0** | `SMARTX_TABLE = os.environ.get('SMARTX_TABLE', 'opal-data-smartx')` in `opal-portal-data-proxy` -- a **DynamoDB table name** that happens to equal the S3 bucket name. A different resource namespace; this S3 grant does not reach it. |
| `opal-portal-data` | 1 -> **0** | **0** | the hit was `opal-portal-data` matched inside **`opal-portal-data-proxy`**, the function's own name in a docstring. A word-boundary re-census (`(?![-A-Za-z0-9])`) drops it to 0 raw. |
| `opal-data-portal-s3`, `opal-market-data-v2`, `opal-data-aaii-sentiment` | 0 | **0** | genuine absences |
| **CONTROL `opal-data-portal-v2`** | 17 | **16** | real assignments: `DEST_BUCKET =`, `S3_BUCKET =`, `BUCKET =`, `PORTAL_DATA_BUCKET =`, `SMARTX_SERVED_BUCKET =`, `REPORT_BUCKET =`, across 6 functions. 1 of the 17 is a comment. |

**THREE DISTINCT WAYS A SUBSTRING COUNT LIES, all three present in one census of 13 files:** prose inside a
docstring; a name that is a PREFIX of a longer identifier; and the same string naming a resource in a DIFFERENT
service. The control is what made them findable -- a census returning 0 everywhere would have looked like a
working instrument.

### 3a. COVERAGE GAP, named rather than absorbed into a zero

**1 of the 12 functions' code was NOT censused.** `opal-session-analytics`'s source map entry names
`infra/aws/opalinvest_dev/lambda/session-analytics/dist/index.mjs`, and **there is no `dist/` directory at all**
in the repo -- it is a bun-built artifact produced at deploy time. I checked this with a forward-slash path
specifically because a mixed path separator on this device can make a present file read absent; it is genuinely
not there. **So that function's contribution to every count above is UNKNOWN, not zero**, and the six zeros are
zeros over 11 of 12 functions' code plus 12 of 12 functions' environment. Its `env` reads 0 like the rest.

A second, smaller gap: `opal-news-ai-sentiment` declares `files: []`, so its `source_dir` was globbed for `*.py`
(1 file found) rather than read from a manifest. That substitution is named here because the order says to read
the manifest, not the directory.

## 4. THE PLANNED NARROWING, GRADED PER ATTRIBUTE AND PER ARN

The edit drops exactly the 12 ARNs and nothing else. `terraform fmt -check` rc=0; the heredoc still parses as
JSON; the diff is 13 removed / 1 added lines, the extra pair being `opal-data-news-v2/*` rewritten without its
trailing comma. **The diff touches no other block of a file that declares many policies** -- confirmed by reading
the whole diff, because the comma fix was applied with a global regex.

```
PLAN: shared-infra: Plan: 0 to add, 1 to change, 0 to destroy.
```

From `terraform show -json` of the saved plan:

| graded property | measured |
|---|---|
| `resource_changes` / non-no-op | 2 / **1** |
| non-no-op addresses that are NOT the target | **`[]`** |
| `restricted_breakglass` in `resource_changes` | **0** |
| destroys / replaces | **0 / 0** |
| attributes that differ | **1** (`policy`) |
| `name` / `role` / `id` | all **byte-identical** |
| statements / `Sid` | 1 -> 1 / `S3ReadWrite` -> `S3ReadWrite` |
| **actions** | **unchanged, all four**: `GetObject`, `PutObject`, `DeleteObject`, `ListBucket` |
| ARNs | **16 -> 4** |
| **ARNs ADDED** | **0** |
| ARNs REMOVED | **exactly the 12**, enumerated below |
| ARNs KEPT | the 4: `opal-data-portal-v2` + `/*`, `opal-data-news-v2` + `/*` |

```
- arn:aws:s3:::opal-data-smartx            - arn:aws:s3:::opal-data-smartx/*
- arn:aws:s3:::opal-data-smartx-v2         - arn:aws:s3:::opal-data-smartx-v2/*
- arn:aws:s3:::opal-portal-data            - arn:aws:s3:::opal-portal-data/*
- arn:aws:s3:::opal-data-portal-s3         - arn:aws:s3:::opal-data-portal-s3/*
- arn:aws:s3:::opal-market-data-v2         - arn:aws:s3:::opal-market-data-v2/*
- arn:aws:s3:::opal-data-aaii-sentiment    - arn:aws:s3:::opal-data-aaii-sentiment/*
```

A policy is ONE opaque string attribute, so `1 to change` is not a grade: it would read identically if an action
had been dropped or a live ARN removed. The per-ARN decomposition is the measurement.

### 4a. THE UNTARGETED PLAN -- and the order's expectation for it is ALREADY STALE

```
UNTARGETED-MODULE-PLAN: infra/aws/terraform/shared-infra: Plan: 0 to add, 1 to change, 0 to destroy.
```

Step 3 says to record the untargeted plan "(its `restricted_breakglass` adds unchanged)". **There are no
`restricted_breakglass` adds any more.** The pair appears only as two `Refreshing state...` lines carrying live
ids, and the untargeted plan's single change is my own narrowing. `ADVI_COTBKF` applied that pair at
**2026-10-11T09:05:05Z** (live `CreateDate`; backend state written 09:05:07Z), which is row **`Z-S40`**.

> **THE X-5 PAIR MUST NOT BIND "2 to add UNCHANGED".** Row 6's pair did, and that clause was unsatisfiable before
> its act began for exactly this reason. The correct binding for this cell is what the plan now shows: **0 to add,
> 0 to destroy, and exactly one change which is this policy.** `-target` remains load-bearing on principle -- the
> module holds 256 state addresses and another project applies to it -- but the specific hazard the order names
> (an untargeted apply CREATING an IAM role) no longer exists, because those resources now exist.

## 5. NAMING, graded on the `.tf` with `--no-renames`

```
DENOMINATOR: 1 path(s); declaration-tree domain = 1
COVERAGE: 0 path(s) the gate could not see; 1 seen
NAMING-GATE: PASS 0 graded                        rc=0
```

**`0 graded` is correct here and is not a vacuous pass, but it is worth saying why:** the gate grades ADDED
lines, and this edit is a deletion of 12 ARN lines plus one re-written line carrying an ARN that already existed
at HEAD. There is genuinely no new name to grade. The pre-check was run first -- 1322 bytes, 1 file, 1 added
line -- so the verdict is read over a diff known to be non-empty.

## 6. THE ROLLBACK, saved and proven against a FRESH re-fetch

`portal_s3/ROLLBACK_opal-portal-s3-read.json`, 1152 bytes, LF-only, 0 non-ASCII. Carries `RoleName`,
`PolicyName` and the as-live document: 1 statement, `Sid S3ReadWrite`, 4 actions, **16 ARNs**.

**Equality was proven against a SECOND, FRESH `get-role-policy` call, not against the file just written** --
comparing a saved file to itself proves nothing. Canonical `sort_keys` compare: **True**.

## 7. WHAT THIS CELL IS NOT ASKED TO FIX, AND I AM NOT PROPOSING IT

- **The policy's NAME.** It is called `opal-portal-s3-read` while its only statement is `S3ReadWrite` granting
  `PutObject` and `DeleteObject`. The module's own comment at `:382` already flags this as "a
  name-vs-computation drift that helped this over-grant hide" and records why it was left: renaming an inline
  policy is a destroy-plus-create on a live public-authorizer role. Out of this cell's BOUNDS; named here because
  a grader reading only the policy name would misjudge the blast radius.
- **Whether `DeleteObject` belongs in this policy at all**, and whether any of the six buckets is scheduled to
  exist. `opal-market-data-v2` is DECLARED in `market-overview/s3.tf:6`, so Terraform's own intent is that it
  exist -- which makes "recreate the bucket" and "remove the grant" opposite answers for that one name. The cell
  removes the grant, which is correct for closing the squatting hazard and does NOT settle the product question.
  `RULINGS_LEDGER.jsonl:44` carries a prior `DELETE-GATED` ruling on that bucket and should be read before anyone
  decides. Six buckets may not share one answer; that is the CTO's call.
- **`opal-data-smartx`'s DynamoDB table.** A table of that exact name is referenced live by
  `opal-portal-data-proxy`. This S3 grant does not reach it and removing the S3 ARNs cannot affect it, but the
  name collision is worth a reader's attention because it is what made the substring census lie.

**PHASE A ENDS HERE. Nothing was applied; the declaration edit is reverted and uncommitted; only this survey and
the rollback are committed.**
