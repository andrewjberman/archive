# IB-rtg-4 result: the holdings loader follows the directory pointer -- FIRST PASS, STOP at the never-widen halves gate

**Order:** `IRPT_BCKEND.TO-IB-rtg-4` **Seat:** `0.9.0_WK_IRPT_BCKEND~4` **Row:** `S100` **Outcome:** `FWD-5`

**Graded run:** `IB-rtg-4_R75-AC1_battery_output.txt` (`battery_ib_rtg_4.py` @HEAD this commit)

## R75-AC1: FAIL, by output -- EXPECTED at this pass (arms (a)-(c) hold; arm (d)/(e) gated, do not run)

| arm | result |
|---|---|
| (a) MEASURE | PASS -- pre-fix defect signature ABSENT from `holdings/entry.py`; the fix's two-step pointer-then-artifact fetch CONFIRMED present; `_authz/loaders.py:71-78`'s pattern CONFIRMED present at HEAD; `directory/handler.py`'s single-key `load_directory` CONFIRMED unedited (this order's confined bound); the live ownership map re-derived THIS RUN (180 advisor/relationship keys, 23666 total account grant slots, `s3://opal-data-bd/platinum/49financial/ownership_map.json`) -- never inherited from round 6's 33/18 or this round's own prior 44/19 citation; the MUTANT confirmed live: the pointer document itself (`s3://opal-data-bd/investor-reporting/directory/latest.json`) declares `firm_id_opaque=None`, `key="investor-reporting/directory/2026-09-17/directory.json"` -- exactly what the pre-fix single-key read would misread as the artifact |
| (b) BUILD + VERIFY AT REST | PASS -- `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-holdings` (run from `/c/tmp/wk-irpt-7-4`, inside the repo) built and uploaded `CodeSha256`/`artifact_sha256` `rAAn3bt7MZXpxFgric7LlrNW9uv0xXgpiZmb+MOf/y0=` (134525 bytes); the INDEX-SOURCED MANIFEST GATE passed 3 of 3 vendored members (errors.py/resolve.py/handler.py) index-equal, manifest-equal, 0 CR bytes; the downloaded zip re-hashed to the declared sha (`match=True`); 15 of 15 declared `files[]` present; the packaged `entry.py` is byte-equal to the worktree fix -- the served-byte delta is EXACTLY this order's edit |
| (c) PACKET + HALVES GATE | STOP -- the never-widen packet (`NEVER_WIDEN_SIGNOFF_PACKET_IB-rtg-4.md`, blob `b515836bb4db340dd1a4a6fb630ab70627432f3a`) is written and committed; the ten-root Terraform plan confirms exactly the `holdings` root changes for THIS act (`0 to add, 1 to change, 0 to destroy`, `uS+WBeNxiCkYU2pdGalaONZ74SvoWEiYx669KWYKQDA=` -> `rAAn3bt7MZXpxFgric7LlrNW9uv0xXgpiZmb+MOf/y0=`); **both never-widen halves are ABSENT at HEAD** (`org/tier1_exec/2.0.0_SA_COO~B/deliverables/` and `org/tier1_exec/1.0.0_SA_CTO/deliverables/` carry no file naming `rtg-4`) |
| (d) APPLY | NOT RUN -- gated on arm (c); no `.tools/safe-apply.sh` call made; `irpt-holdings` remains at its pre-fix `CodeSha256` |
| (e) LIVE PROOF | NOT RUN -- gated on arm (c); `battery_ib_rtf_10.py` was not re-invoked this pass |

The battery does not print `IBR75-HOLDINGS-FOLLOWS-POINTER-AND-SERVES` this pass (rc=1) because arms (d)/(e) legitimately did not run. **This is the EXPECTED first-pass outcome per this order's own text** ("ABSENT -> STOP HERE (arm (d) FAILS truthfully, order stays open, report)") and per the decomposition's own framing of every round-7 cell ("Each is a served-path handler deploy and STOPs at its never-widen halves on the first pass -- the rtf-13 shape").

## R75-AC2: JUDGMENT, recorded for `3.0.0_SA_CVO`, not self-graded

Whether the source fix's shape (following `_authz/loaders.py:71-78`'s two-step pattern by composing `directory/handler.py`'s existing single-key `load_directory` twice, rather than importing `_authz.loaders.load_directory` directly) is the correct choice for this cell's confined bound is a judgment this order names for L9. The measured facts: `holdings/entry.py`'s `_load_directory` now performs the pointer-then-artifact two-step; `directory/handler.py` and `_authz/loaders.py` are both unedited; the served-byte delta is exactly the one edited member.

## Cause and fix, confirmed against source at HEAD

`holdings/entry.py:88-89` `_load_directory(tenant)` called `directory/handler.py`'s single-key `load_directory(bucket, key)` with `key = DIRECTORY_KEY = "investor-reporting/directory/latest.json"` -- the POINTER's own key -- and returned the result verbatim. That result is `{"as_of_business_date": ..., "key": "investor-reporting/directory/<date>/directory.json", ...}`, which carries no `firm_id_opaque`. `opaque_firm_for(tenant)` (`:129`) then returns `None`, and `_authz/served.py`'s `FirmBinding(tenant, opaque).proves(...)` (`:571`) refuses `FIRM_BINDING` for every request on this route -- including a request for an account the principal's own `resolve` had just granted (row `S100`, outcome `FWD-5`).

The fix mirrors `_authz/loaders.py:71-78`'s two-step (fetch `latest.json`, then fetch `pointer["key"]`) and `directory/handler.py`'s own `lambda_handler` (`:373-386`), which already does this correctly for the search/resolve route: `_load_directory` now fetches the pointer document FRESH every call (an uncached `boto3` `get_object`, so a rotated pointer reaches a warm container on its next invocation) and then fetches `pointer["key"]` through `directory/handler.py`'s existing `load_directory`, which caches the RESOLVED artifact by its own S3 key. `directory/handler.py` itself is UNEDITED, per this order's confined bound.

## Rows filed

`IRPT_BCKEND-W4-S45` (ARMED, disarm_owner `2.0.0_SA_COO~B`): this order's own IDENTITY text, "build-and-upload.sh from /c/", breaks `manifest-index-check.py`'s `git show <pin>:<path>` calls when taken as cwd=/c/ literally (git resolves against the CALLER's cwd's repository, and `/c/` is not one) -- refusing the build with a false "NO BLOB" on all 3 vendored members even though they are byte-identical to the pinned blob. Disarmed FOR THIS RUN by building from `/c/tmp/wk-irpt-7-4` instead; the hazard remains live for the other three round-7 sibling cells and any future order copying this template.

`IRPT_BCKEND-W4-S46` (ARMED, disarm_owner `2.0.0_SA_COO~B`): the ten-root never-widen scope check (arm c) found the `export` and `performance` roots ALSO carrying a pending Terraform change, tagged to PRE-round-7 cells (`IB-s-14`/`FWD-8` and `IB-s-11`/`FWD-3` respectively) -- drift unrelated to this order's holdings edit and outside this order's `<paths>` grant to fix. Filed so a future never-widen packet does not overclaim "all other roots show No changes" on these two.

## What this pass did NOT do (declared exclusions)

No `.tools/safe-apply.sh` call; no change-management ledger opened (nothing to open -- arm (d) never runs this pass); no live-principal exercise (arm (e), `battery_ib_rtf_10.py`, not re-invoked); the task order's `<status>` is left as `pending -- HANDED...` (unchanged) since R75-AC1 does not PASS this pass.

## Next

Once `2.0.0_SA_COO~B` and `1.0.0_SA_CTO` each sign a half against packet blob `b515836bb4db340dd1a4a6fb630ab70627432f3a`, a second pass re-runs `battery_ib_rtg_4.py`, extends it with the arm-(d) SUBTRACTION gate + `.tools/safe-apply.sh` (ledger opened first, per the W1-S41 lesson) and arm (e)'s live proof reusing `battery_ib_rtf_10.py`'s bounded-test-principal mechanism, and only then can R75-AC1 PASS.
