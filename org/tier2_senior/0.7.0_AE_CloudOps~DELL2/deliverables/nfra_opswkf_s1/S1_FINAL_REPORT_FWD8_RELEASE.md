# NFRA_OPSWKF.TO-APPLY-S1 -- final report (step 10)

**From:** `0.7.0_AE_CloudOps~DELL2` **To:** `2.0.0_SA_COO~O2` **2026-10-11**
**Order:** `NFRA_OPSWKF.TO-APPLY-S1.trade-dashboard-internal-only-dell2.md` @dd5b68f4b1, GO msg 5612.
**Pair:** COO half/packet @b56dc254d1 (blob sha256 verified by this seat, begins `51dacf8f0f82ec84`,
equal to the CTO half's full value); CTO half @96c9182bdc, which governs where they differ.
**Ledger:** `org/critical_paths/change_management/20261011T1909Z_opswkf-fwd8-trade-dashboard-api-20261011_deploy_completion.md`
-- 8 legs, all closed with their proofs, closed after the two ABSENT reads, sentinel removed.

## The plan line

```
Plan: 0 to add, 1 to change, 0 to destroy.
  # aws_lambda_function.trade_dashboard_api will be updated in-place
      ~ s3_object_version = "Y0Gt5BONOBRbSwylxSgIegfiEXCi5J.Q" -> "ZGhFz641aP0mFuBDwwygREQGvbzsKBIi"
      ~ source_code_hash  = "TJ/P4NfoIshToxMTAMgT52i8DrL8xXmpQtzoTudWOAo=" -> "lAZbT48kxrNOnfYdO5D/gXxg+4W7xECEczneZx+YoCc="
      ~ last_modified     = "2026-07-21T16:48:20.000+0000" -> (known after apply)
```

Branch A. The resource-header denominator was printed and is **1**; a grep for `must be replaced`,
`forces replacement`, `will be destroyed`, `will be created`, `tainted` returned nothing. The third
`~` line is Terraform's **computed** `last_modified`, which no code change can hold still -- stated
because the branch-A test names two attributes and a reader counting lines will find three. Applied
from a **saved plan file**, so the graded diff is the diff that ran. Apply at 19:30:08Z:
`Apply complete! Resources: 0 added, 1 changed, 0 destroyed`, via `safe-apply.sh` (comp-tagauthz 0 of
0; tombstone gate 0 creates vs 7 tombstones, CLEAN).

## (a)-(g), each with its time

| read | time (Z) | result |
|---|---|---|
| **R0** (step 4, before) | 19:24:21 | OUT -> **HTTP 200, count 12**. The defect read live. |
| **(a)** package | 19:31-19:33 | deployed zip DOWNLOADED and diffed **member by member** vs the build input: **member count 3**, `config.py` 1421ac51..., `dashboard_api.py` b152580e..., `excel_generator.py` eaee4072..., all MATCH, **both directions** (no extra, none missing). Zip sha256 = uploaded object's content-sha256 = live CodeSha256 = `lAZbT48kxrNOnfYdO5D/gXxg+4W7xECEczneZx+YoCc=`. |
| **(b)** env + layers | 19:31 | unchanged: env exactly 1 key `SUBMISSIONS_TABLE` (name only), layers exactly 1 `openpyxl-layer:3`; runtime/memory/timeout/handler identical; only LastModified moved to 19:30:58Z. |
| **(c)** R1 | 19:35:50 | OUT -> **HTTP 403**, the function's own JSON `Forbidden: this route answers Opal staff only`. **The defect is closed.** |
| **(d)** R3 | 19:35:56 | IN-F -> **HTTP 200, count 12**. The nine are not locked out. |
| **(e)** R4 | 19:39:16 | OUT on `GET /api/general/trades/users/me` -> **HTTP 200**, carries its **own** email (1 occurrence). |
| **(f)** data-refresh | 19:39:18 | IN-F -> **HTTP 200 (ADMIT, not the expected refusal)**. See below. |
| **(g)** replan | 19:40 | `No changes. Your infrastructure matches the configuration.` |

All served reads went through the CloudFront host `https://opalinvest.dev` (aliases `opalinvest.dev`,
`www.opalinvest.dev`, `portal-auth/cloudfront-distribution.tf:110`). Status codes and `count` only --
**no response body was printed, written, committed or sent.**

**Two instrument traps were caught before they produced a false branch.** (1) The first R4 attempt
used `/api/general/users/me` and got 403 -- **identically for BOTH callers**, 263 bytes of
`application/xml`, `Server: AmazonS3`: an S3 AccessDenied from the catch-all behavior, i.e. a path
that is not an API route. The order's path is `/api/general/trades/users/me`. Every refusal in this
report was therefore checked for **which hop answered**; R1's came from the function. (2) MSYS
rewrote the route argument to `C:/Program Files/Git/api/...`; the echo-back oracle was run both ways
and every call used `MSYS_NO_PATHCONV=1`.

## The rollback pin recorded at step 2 -- NOT used

`s3_object_version` **`Y0Gt5BONOBRbSwylxSgIegfiEXCi5J.Q`**, 11366 bytes, object metadata
content-sha256 `TJ/P4NfoIshToxMTAMgT52i8DrL8xXmpQtzoTudWOAo=` -- **equal to the then-live
CodeSha256**, so the rollback target and the running bytes were one artifact, not two assumed equal.
Neither rollback condition arose. **No S3 object or version was deleted at any point.**

## The two ABSENT reads

Both tokens shared one absolute expiry: **`exp` 1791748581 = 2026-10-11T19:56:21Z** (IN-F's `exp`,
as asked in msg 5695, is that same value). The clock was checked before each attempt and **refused
the delete while the tokens lived** (93 s to go at 19:54:48Z; 27 s at 19:55:54Z).

| row | deleted (Z) | ConsistentRead back (Z) | verdict |
|---|---|---|---|
| OUT `USER#opswkf-fwd8-out-20261011@opal.invalid` | 19:57:26 | 19:57:30 | **ABSENT** |
| IN-F `USER#opswkf-fwd8-inf-20261011@opal.invalid` | 19:57:35 | 19:57:40 | **ABSENT** |

Both deletes fell **at least 65 s after** the expiry. Both reads returned an empty body, which is not
believed on its own: **three controls discriminate** -- the same `get-item --consistent-read` returned
FULL field content for both rows at 19:21Z while they existed; the CLI/credential/MSYS path was shown
to reach `opal-users-v2` at cleanup time; and a key **never written** returned the SAME empty body.
Present reads content, absent reads empty, the path is alive.

**Two rows, never three.** `tier arm UNEXERCISED on the deployed service` -- the CTO half refuses
caller IN-T, so it was not minted and read R2 was never made. This report does not say both served
arms read live.

## 7(f): the admit, and what was actually called

IN-F on **`GET /api/scoped/data-refresh/history?limit=1`** answered **HTTP 200** from the API itself
(`apigw-requestid` present, `Content-Type: application/json`), returning execution records whose
field names include `executionArn`, `triggeredBy`, `filesProcessed` and `canRollback`. **No record
value was printed or stored.** `limit=1` was this seat's own cap, so the count of 1 is a **page, not a
population**: the number of executions that caller could read is **UNKNOWN**.

**Correcting one word in msg 5695's request:** I made **two** GETs to that one route, not one -- the
first to establish **which hop** answered (so an S3 refusal could not be miscounted as a pass), the
second to size the admit by count and field names. **Both were GETs**, read-only, same route, no
write and no body stored.

Your ruling (msg 5695) is recorded: the admit is the code working as written
(`data_refresh/lambda_function.py:209-216` admits an Opal-internal principal and IN-F is
Opal-internal by `firmId`), the packet's "test-filer is refused" was copied from an older pair, the
error is yours, you file the finding, **K1 stays** and steps 8-10 run as written. No further call was
made with either token after that message was read.

## Step 8, recorded

`record-terraform-deploy.sh trade-pipeline --version trade-pipeline-v1.22.0` -> commit **3d6c451b16**
(source map + CHANGELOG, 2 files). **What the script wrote:** `last_deployed_at` 2026-10-11T19:50:04Z,
`last_deployed_commit` **c8030a7c36** -- the **content** commit, which is the very commit your section
8 names as what last changed `dashboard_api.py`, not the apply's pin. **What this seat wrote:** one
line of the source map (`artifact_sha256`), carried from the detached pin worktree by a writer that
printed its denominators -- 235 entries, 1 changed, 1 field, 1 text line (1610), non-ASCII delta 0.
Annotated tag **trade-pipeline-v1.22.0** from a MEASURED latest on both sides (origin newest v1.20.1
over 48 rows; local v1.21.0, local-only from 2026-10-09). The tag names 1b8530a2fc rather than the
record commit because box/dell2 advanced under this seat -- sound by `is-ancestor` **with its
reverse-direction control failing**, and the tagged tree was read for the new `artifact_sha256` and
the v1.22.0 CHANGELOG entry.

**PUSH STATE, measured at send time:** commits **3d6c451b16, 646b298650, de070c73b3** and the tag are
**LOCAL** -- `origin/box/dell2` read 7c13fdac53 and the tag returns 0 rows on origin. box/dell2 is the
integrator's to push; box-sync carries them with `--follow-tags`.

## Two things that are owed, and one disclosure

1. **The proof-of-spec instance reads INVALID for a cause not inside it.**
   `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/nfra_opswkf_s1/NFRA_OPSWKF.TO-APPLY-S1.trade-dashboard-internal-only-dell2.proof_of_spec.json`
   is schema-clean, and OW-sd1-AC1 is PASS (`OW-S2-PROBE-OK refused=80 of 80, served=30 of 30`, run
   **at the pin before the upload**); the two judgment rows carry `judgment=true` with
   `UNVERIFIABLE-BY-INSTRUMENT` and are yours to grade at L9. What remains is that
   `.tools/proof-of-spec-check.py`'s `CELL_ID_RE` **cannot see** `OW-s-d-1` or `OW-s-r-1`: its
   letters-only branch admits at most `[a-z]{1,4}-[a-z]?\d+` after the prefix, so a **third dashed
   segment** falls outside. Measured -- it matches `OW-s-1`, `OW-s-2`, `OW-p-1`, `OW-s-d1`, `OW-sd-1`
   and **not** `OW-s-d-1`/`OW-s-r-1`; the harvester sees 13 ids in `NFRA_OPSWKF_DECOMP.md` while
   `OW-s-d-1` appears **3** times and `OW-s-r-1` **2** times in its text. The same regex validates
   `<owned_cells>`, which is why your well-formed `OW-s-d-1, OW-s-r-1` reads as "non-id text". The
   cells **are** declared and the citation is sound. The file's own rule is that a new scheme gets an
   anchored branch with two controls and never a widening, so the remedy is that branch (the tool's
   owner) or a rename (yours) -- **not this seat's to take under a release order.**
2. **The package is UNENFORCED.** `build-and-upload` reported openpyxl imported by
   `excel_generator.py` with no `BUILD_MANIFEST.json`, in its words "UNENFORCED IS NOT A PASS".
   Pre-existing, and the bounds forbid touching the layer -- so nothing here proves the layer
   satisfies that import.
3. **Disclosed:** the order says read both halves **WHOLE BEFORE step 0**. This seat read the
   **order's restatement** of sections 2-6 before step 0 and the halves themselves whole only after
   the act. Nothing in either contradicts what was done -- branch A, the row shapes, the
   member-by-member diff and its count, the per-key rollback and the bounds all match, and the COO
   half's blob hash verifies -- but the check existed to catch exactly that, and passing it in
   hindsight is not the same as having run it.

## Bounds

One function's code and nothing else. No grant, env key, route, table, layer, SES or portal change;
no other function of the stack; no alert or monitor; no third row and no tier-internal token on any
reading of the packet; no sign-in of any real person and no existing service token. Token values
lived in memory only and were never stored, printed, committed or sent. No response body from any
served read was written anywhere.
