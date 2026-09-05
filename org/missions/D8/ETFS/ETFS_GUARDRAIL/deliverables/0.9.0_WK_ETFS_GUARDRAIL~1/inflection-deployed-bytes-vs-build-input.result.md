# EG-s-12 -- Inflection's lineage: the DEPLOYED bytes of inf-etf-ownership-daily diffed against the build input

**TO:** `ETFS_GUARDRAIL.TO-EG-s-12` · **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` · **Worktree HEAD:** `4f926099df` (branch `wk-ETFS_GUARDRAIL-1`) · **Verb:** verify, live reads only, no change.

## 1. S12-AC1 -- live configuration read

**Invocation:**
```
.tools/aws lambda get-function-configuration --function-name inf-etf-ownership-daily --query "[FunctionName,LastModified,CodeSha256]" --output text
```
**Output (rc=0):**
```
inf-etf-ownership-daily	2026-08-11T10:29:39.000+0000	Sibchin3yNutF+OC6d06fZNlfQKuKCcPUC3cG/m3LJI=
```
Full configuration also captured (`.tools/aws lambda get-function-configuration --function-name inf-etf-ownership-daily`, rc=0): `Environment.Variables` carries BOTH the legacy keys (`INF_BUCKET=opal-data-inf`, `HOLDINGS_PREFIX=gold/canonical/holdings_`) AND the new-design keys (`ASSETS_BUCKET=opal-data-assets`, `FACT_POSITIONS_PREFIX=orion/inflection/silver/fact_positions`, `META_DEDUP_PREFIX=orion/inflection/meta/dedup`) simultaneously, plus `ETFS_BUCKET`, `CONFIG_KEY`, `OUTPUT_PREFIX`, `PARTNER`. `Layers`: `pandas-pyarrow-requests-layer:1` only (no first-party layer on this function). `CodeSize=4942`.

## 2. S12-AC2 -- deployed-bytes diff

Script written per the deliverable spec: `org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/deployed_bytes_diff.py`.

**Build-zip.sh deviation (recorded per the TO's own fallback clause):** `bash infra/aws/lambda/ci/build-zip.sh inf-etf-ownership-daily infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily .scratch/build lambda_function.py dedup_core.py trading_calendar.py` FAILED, rc=1: `touch: invalid date format '202600010000'` -- the script's reproducible-build step hardcodes a `touch -t` argument with an invalid month (`00`); `touch -t "202601010000"` (month `01`) succeeds standalone, confirming the script's literal string is the defect, not the environment. This worker built an equivalent deterministic zip directly via Python's `zipfile.ZipInfo(date_time=(2026,1,1,0,0,0))` (sorted member order, fixed mtimes) instead, exactly as the TO's fallback clause permits ("or an equivalent deterministic zip of the same files if that script's output dir convention refuses -- say which").

**Invocation:**
```
python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/deployed_bytes_diff.py
```
**Output (rc=0):**
```
SOURCE_MAP: source_dir=infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily files=lambda_function.py,dedup_core.py,trading_calendar.py artifact_sha256=Sibchin3yNutF+OC6d06fZNlfQKuKCcPUC3cG/m3LJI= last_deployed_commit=af4f123e2c665058de54a2fa9079bb904acce636 last_deployed_at=2026-08-01T19:35:16Z
DEPLOYED_ZIP_MEMBERS: lambda_function.py
REPO_ZIP_MEMBERS: dedup_core.py,lambda_function.py,trading_calendar.py
MEMBER dedup_core.py            deployed=ABSENT     repo=78f24ab352 DIFFERS
MEMBER lambda_function.py       deployed=3e98e00e16 repo=afcbd401a7 DIFFERS
MEMBER trading_calendar.py      deployed=ABSENT     repo=41b1c0c126 DIFFERS
VERDICT: MISMATCH files=3 differing=dedup_core.py,lambda_function.py,trading_calendar.py
DEPLOYED_READS: env_bindings=ETFS_BUCKET<-ETFS_BUCKET,INF_BUCKET<-INF_BUCKET,HOLDINGS_PREFIX<-HOLDINGS_PREFIX,CONFIG_KEY<-CONFIG_KEY,OUTPUT_PREFIX<-OUTPUT_PREFIX,PARTNER<-PARTNER
REPO_READS: env_bindings=ETFS_BUCKET<-ETFS_BUCKET,ASSETS_BUCKET<-ASSETS_BUCKET,FACT_POSITIONS_PREFIX<-FACT_POSITIONS_PREFIX,META_DEDUP_PREFIX<-META_DEDUP_PREFIX,CONFIG_KEY<-CONFIG_KEY,OUTPUT_PREFIX<-OUTPUT_PREFIX,PARTNER<-PARTNER
```

**Denominator:** 3 of 3 declared source-map files compared; 2 of 3 (`dedup_core.py`, `trading_calendar.py`) ABSENT from the deployed zip entirely; 1 of 3 (`lambda_function.py`) present on both sides but byte-DIFFERENT. `VERDICT: MISMATCH`.

**Independent corroboration (a second instrument, not the deployed-zip download):** the deployed `lambda_function.py` is byte-IDENTICAL to the repo's copy at commit `af4f123e2c` (the source map's own `last_deployed_commit`):
```
git show af4f123e2c:infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/lambda_function.py | sha256sum
-> 3e98e00e16d51664362096d64cabeff35cd73038b63579d195c7a1934cdbc401
sha256sum .scratch/deployed_extract/lambda_function.py
-> 3e98e00e16d51664362096d64cabeff35cd73038b63579d195c7a1934cdbc401   (MATCH)
```
`dedup_core.py` and `trading_calendar.py` do not exist at `af4f123e2c` (`git show af4f123e2c:...dedup_core.py` -> `fatal: path ... exists on disk, but not in 'af4f123e2c'`), consistent with the deployed zip containing neither.

## 3. S12-AC3 -- last repo commit touching the source dir, re-measured

**Invocation:**
```
git log --format="%h %ad %s" --date=short -1 -- infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/
```
**Output (rc=0):**
```
001a73530a 2026-08-03 fix(ADHOC.inf-etf-regularization): complete the stranded COMMIT leg of the half-landed inf-etf deploy -- COMMIT ALL / APPLY NOTHING per CTO F2 ruling 20260803T215051Z
```
Matches the brief's stated `2026-08-03 @001a73530a`. The commit's own message and the `.tf` file's inline marker (`infra/aws/terraform/inf-pipeline/inf-etf-ownership-daily.tf:70-91`, block `>> DECLARED HEAD-AHEAD-OF-APPLIED DIVERGENCE`) state explicitly: *"the monolith-dedup increment (3 IAM statements ...; 3 env vars ASSETS_BUCKET/FACT_POSITIONS_PREFIX/META_DEDUP_PREFIX) is committed here COHERENT with its code (dedup_core.py) but DELIBERATELY NOT APPLIED -- behaviorally inert today (deployed env carries only legacy keys, CTO-read live), ARMING on any code-artifact deploy ... inf-pipeline remains TARGETED-APPLIES-ONLY until the parked increment is deliberately landed or retired."*

## 4. S12-AC4 -- newest September slice + its `source_artifact`

**Invocation:**
```
.tools/aws s3api list-objects-v2 --bucket opal-data-etfs --prefix daily/inflection/2026-09 --query "Contents[-1].Key" --output text
```
**Output (rc=0):**
```
daily/inflection/2026-09-04.json
```
Fetched (`.tools/aws s3api get-object --bucket opal-data-etfs --key daily/inflection/2026-09-04.json`, rc=0, ETag `1527e8a5171eb23157893bf4d7189f75`, LastModified `Fri, 04 Sep 2026 15:00:42 GMT`): every row's `source_artifact` reads
```
"source_artifact": "s3://opal-data-inf/gold/canonical/holdings_2026-09-04.parquet"
```
-- the LEGACY path, dated **today**, confirming the brief's second fact ("slices cite `opal-data-inf/gold/canonical/holdings_`") is still current, not historical.

## 5. S12-AC5 -- THE ANSWER (judgment; recorded, no verdict)

### 5a. Do the three brief facts now fit?

They fit, and the mechanism is now measured rather than attributed:

1. **"Repo computes one bucket"** (`opal-data-assets/orion/inflection/silver/fact_positions`) -- TRUE, but this is the **COMMITTED, NOT-APPLIED** state as of `001a73530a` (2026-08-03), by an explicit CTO ruling (F2, `20260803T215051Z`) to "COMMIT ALL / APPLY NOTHING." The repo's HEAD is a design that has never run in production.
2. **"Slices cite another"** (`opal-data-inf/gold/canonical/holdings_`) -- TRUE, re-measured live today (S12-AC4): every row of the 2026-09-04 slice cites the legacy path. This is the bucket the code that is ACTUALLY RUNNING reads, confirmed two ways: (a) the live `Environment.Variables` bind `INF_BUCKET`/`HOLDINGS_PREFIX` and the deployed `lambda_function.py` only ever references those two names (`DEPLOYED_READS`, S12-AC2); (b) the deployed `lambda_function.py`'s bytes are byte-identical to the repo's copy at `af4f123e2c` (2026-08-01), which predates the Orion repoint entirely and cannot reference the new names.
3. **"Deploy postdates the last repo change"** (`LastModified 2026-08-11` > commit `001a73530a` on `2026-08-03`) -- TRUE IN TIME, but the deployed CODE bytes are NOT from after `001a73530a` -- they match `af4f123e2c`, an EARLIER commit (2026-08-01). The only way a later `LastModified` timestamp is consistent with older code bytes is that the 2026-08-11 event was a **configuration-only Lambda update** (the resource's `Environment.Variables` block, which the same `.tf` file shows was already committed on 2026-08-03) that ran WITHOUT the code artifact being rebuilt/re-uploaded (the source map's `artifact_sha256`/`last_deployed_commit` were never bumped past `af4f123e2c`/2026-08-01). This is the live confirmation, ~1 month later, of exactly the hazard the `.tf` file's own inline marker warned about on 2026-08-03: *"IT GOES LIVE THE INSTANT A CODE ARTIFACT DEPLOYS ... Do not apply this increment as a side effect of an unrelated apply: inf-pipeline is TARGETED-APPLIES-ONLY."* The env-var half of the "parked increment" reads as LIVE today though the code half does not -- the exact half-arming the marker named as the failure mode to avoid, now measured as having happened.

### 5b. Which bucket and prefix the DEPLOYED code actually reads

`opal-data-inf` / `gold/canonical/holdings_{date}.parquet` (via env vars `INF_BUCKET` + `HOLDINGS_PREFIX`) -- the LEGACY, own-firm-monolith path. It does **not** read `opal-data-assets/orion/inflection/silver/fact_positions` despite that env var now being present and populated on the live function (`ASSETS_BUCKET`, `FACT_POSITIONS_PREFIX`) -- the deployed code simply never references those names (confirmed by both `DEPLOYED_READS` in S12-AC2 and the byte-identical-to-`af4f123e2c` comparison, which predates their introduction).

### 5c. What rung 2 of the ladder (`EG-s-7`) must check for Inflection

- **Never read repo HEAD as ground truth for what Inflection's producer reads.** The repo's `opal-data-assets/orion/inflection/silver/fact_positions` design is real but UNDEPLOYED; a coverage/remediation check that trusts the source tree over the deployed bytes will look for freshness/holes in the wrong bucket entirely.
- **The live check must be against `opal-data-inf/gold/canonical/holdings_{date}.parquet`** -- the bucket and prefix this worker confirmed BOTH the deployed code reads AND today's served slice's `source_artifact` cites. That is the correct upstream partition for `EG-s-7`'s per-date presence check on Inflection.
- **A future code-only redeploy of `inf-etf-ownership-daily` is ARMING, not benign**, per the `.tf` file's own marker: because the env vars for the new design are already live, the NEXT time anyone rebuilds and uploads this function's zip (for ANY reason -- including an unrelated fix), the new `dedup_core.py`/Orion code path activates automatically, with the IAM grants for it in an UNVERIFIED state (this worker's one live-IAM read attempting to check that state exceeded this TO's enumerated read surface -- filed as `ETFS_GUARDRAIL-W1-S4`, INERT, and not relied on here). `EG-s-7` (or whoever next redeploys this function for any reason) should treat a code-artifact deploy on `inf-etf-ownership-daily` as a design-cutover event requiring its own sign-off, not a routine push.
- **The source map's `artifact_sha256`/`last_deployed_commit` fields are themselves stale-but-self-consistent evidence**: they still name `af4f123e2c` / 2026-08-01, matching the deployed bytes exactly -- so for THIS function, trusting the source map's own last-deployed pointer (rather than assuming "latest commit deployed") is the correct read, and generalizes as a caution for any other producer `EG-s-7` checks via the same source map.

## 6. Push state (measured at report)

```
git ls-remote origin refs/heads/CLOUD
```
