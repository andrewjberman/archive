# RESULT -- IRPT_BCKEND.TO-IB-rtf-6: the manifest re-pinned after the shared-surface drains

`0.9.0_WK_IRPT_BCKEND~4`, cell `IB-rtf-6`, R63-AC1/R63-AC2. Battery:
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/battery_ib_rtf_6.py`. Full
verbatim run: `IB-rtf-6_R63-AC1_battery_output.txt` (this commit).

## Premise re-grounded at the cut

The task order's issued status states HEAD's `_authz/enforce.py` = `blob 79c9d9dee1` and
`_authz/served.py` = `blob fd8b189e5c` at the ORIGINAL cut. This worker's own worktree was handed
at `HEAD 4ee8426c72` (one commit later than that cut, an unrelated `IRPT_FNTEND` L4 commit), where
the SAME two blobs read identically:
`git rev-parse HEAD:infra/aws/lambda/investor-reporting/_authz/enforce.py` = `79c9d9dee1b44ce3d40466466c37a95d452c88db`
and `.../served.py` = `fd8b189e5c5f4dd39525fa7368c48cf9bb9240bf` (both @`4ee8426c72`, this run) --
the premise holds, unwidened.

## (a) THE CENSUS

Population by subtraction over `files[]` (never the face's "14 across 7" taken on faith): every
zip-based, non-Image, non-nodejs investor-reporting function (9 total) whose `files[]` names
`enforce.py` or `served.py`. The census itself found **14 members across 7 functions**
(`battery_ib_rtf_6.py:280` @`4ee8426c72`, this run's own printed population line), matching the
face's number by measurement, not by construction.

`14 stale of 14 members` (`battery_ib_rtf_6.py` output line 24, `IB-rtf-6_R63-AC1_battery_output.txt`):
- `PIN-MATCHES-SERVED`: 0
- `PIN-STALE-HEAD-MATCHES-SERVED`: 13 (all 6 `enforce.py` placements + all 7 `served.py`
  placements, pin resolves to a blob that no longer matches served, HEAD's blob DOES)
- `PIN-STALE-SERVED-DIVERGED-FROM-HEAD`: 1 (`irpt-holdings` :: `enforce.py`, no `staged_from`
  entry at all -- a local, tracked-at-path fork, `infra/aws/lambda/investor-reporting/holdings/enforce.py`
  -- compared against the SHARED `_authz/enforce.py` at HEAD per row `IRPT_BCKEND-W1-S29`)
- `PACKETED`: 0

Every member's pin blob, HEAD blob and served sha256 were fetched fresh this run: the pin via
`git show <pin>:<repo_path>`, HEAD via `git show HEAD:<repo_path>`, served via the LIVE DEPLOYED
Lambda's own `Code.Location` (never the S3 build-artifact bucket -- IB-rtf-1's own trap, reused
verbatim, `live_deployed_zip_bytes()`).

## (b) THE RE-PIN

13 of 14 re-pinned to HEAD's blob at the SAME immutable commit (`4ee8426c72bb6261f055a6cd31fe23e5ebf75ff5`),
old pin -> new pin printed per member (`IB-rtf-6_R63-AC1_battery_output.txt:29-42`, this run).
Sample (full table in the battery output):

| function | member | old pin | new pin | old sha256 | new sha256 |
|---|---|---|---|---|---|
| irpt-directory-search | enforce.py | `28ccac62c9` | `4ee8426c72` | `69808e783c` | `d1c8e7e094` |
| irpt-directory-search | served.py | `28ccac62c9` | `4ee8426c72` | `be03f2fa69` | `ba0cea6d42` |
| irpt-export-render | served.py | `c28c728a30` | `4ee8426c72` | `2f622a4ccb` | `ba0cea6d42` |
| irpt-holdings | served.py | `c28c728a30` | `4ee8426c72` | `2f622a4ccb` | `ba0cea6d42` |
| irpt-ycharts-generate | enforce.py | `28ccac62c9` | `4ee8426c72` | `69808e783c` | `d1c8e7e094` |

`irpt-holdings` :: `enforce.py` (`PIN-STALE-SERVED-DIVERGED-FROM-HEAD`) is NOT re-pinned to either
served or HEAD -- classed, rowed at `IRPT_BCKEND-W4-S42` (disarm_owner `1.0.0_SA_CTO`, citing
`IRPT_BCKEND-W1-S29`) and left for the CTO's ruling, per BOUNDS.

Diff, this commit, `infra/aws/lambda/ci/lambda-source-map.json` @HEAD-to-be: 13 `pin`/`sha256`
pairs changed inside existing `staged_from` entries (never a new entry, never a third copy), plus
5 `artifact_sha256`/`artifact_s3_key` bookkeeping fields updated as a side effect of the REAL
build in part (c) for the 5 of 6 functions whose zip content changed (`irpt-directory-refresh`'s
zip is byte-identical to before -- unrelated to this fix, no diff line). No served bytes committed
as source; ONLY `infra/aws/lambda/ci/lambda-source-map.json` touched.

## (c) THE CONTROL, both signs

**MUTANT** (scratch `BAU_SOURCE_MAP_OVERRIDE`, the real file untouched during this arm): the
ORIGINAL, pre-re-pin manifest (stale pins to `28ccac62c9`/`c28c728a30`) built via the REAL
`build-and-upload.sh` for the representative function `irpt-status` (packages both shared files).
Result (`IB-rtf-6_R63-AC1_battery_output.txt:87-93`, this run):
- mutant build rc=0, built_ok=True (the REAL pipeline accepts the stale pins and produces a
  valid, uploadable zip -- the regression is silent, no build error)
- `irpt-status :: enforce.py` built=`69808e783c` served=`d1c8e7e094` -- MISMATCH, as expected
- `irpt-status :: served.py` built=`2f622a4ccb` served=`ba0cea6d42` -- MISMATCH, as expected
- the built `enforce.py` carries the PRE-INVERSION text verbatim (`AN UNPROJECTED GRANT IS A
  REFUSAL` present, `THE INVERSION (CTO ruling` absent) -- `1 of 1` canonical check (this
  function's blob is byte-identical to the other 5 sharing functions' declared pin, established by
  (a)'s own per-member sha256 census, so this single check generalizes without redundant downloads)
- the built `served.py` LACKS the post-disclosure marker `unprojected_grant=None` -- pre-fix, as
  expected
- MUTANT CONTROL = True

**REAL** (the re-pinned, now-committed-to-be manifest, no override), whole-pipeline build run
LAST so the artifact bucket ends this order in a state matching HEAD (`IB-rtf-6_R63-AC1_battery_output.txt:96-274`):
rc=1 overall (`6 built, 3 failed: irpt-directory-search irpt-intake-poller irpt-ycharts-generate`)
-- **the 3 failures are on members THIS order does not touch and cannot fix**:
`irpt-directory-search` on `data/custodian_key_seam.json`, `irpt-intake-poller` (not in this
order's population at all -- no `enforce.py`/`served.py` entry) and `irpt-ycharts-generate` on
`firm_registry.json`/`settings.json` -- all three are IB-rtf-1's own pre-existing, already-rowed
CANONICAL-ABSENT members (rows `IRPT_BCKEND-W4-S34`/`S35`/`S39`), unrelated to this cell.
Per IB-rtf-1's own control philosophy (`battery_ib_rtf_1.py:558-561` @`949dc88099`, quoted): "A
function can still legitimately fail overall on a DIFFERENT, CANONICAL-ABSENT member this order
cannot fix ... requiring rc==0 there would conflate two independent findings" -- this order's own
control grades MEMBER-LEVEL equality, never the whole-pipeline rc.

Per-member verification, `13 of 13`:
- 6 functions completed the WHOLE pipeline this run (staged, zipped, uploaded, upload VERIFIED by
  the script's own size+sha256 check): `irpt-export-render`, `irpt-narrative`,
  `irpt-performance-adapter`, `irpt-status`, `irpt-holdings` (`served.py` only) -- **9 of 13**
  members independently re-downloaded from the FRESHLY uploaded S3 artifact and sha256-verified
  equal to the LIVE served bytes this census measured.
- 2 functions (`irpt-directory-search`, `irpt-ycharts-generate`) did not complete the whole zip
  (blocked by the UNRELATED missing member above) but the real script's OWN materialize-and-verify
  step (`build-and-upload.sh` TMPJS_STAGE, `:161-201` @`4ee8426c72`) DID run for `enforce.py`/
  `served.py` on both before hitting the unrelated failure, printing `OK: staged <member> <-
  <repo_path>@4ee8426c72 (... sha256 verified ...)` for all 4 -- the SAME real, mechanistic,
  sha256-gated step (a mismatch there prints `BLOB HASH MISMATCH` and REFUSES instead of an `OK`
  line), so this is real evidence, never a self-wrapped stand-in (BOUNDS 12). **4 of 13** members
  verified this way.
- `9 + 4 = 13 of 13` re-pinned members verified equal to served/HEAD. REAL CONTROL = True.

## Instrument trap hit and fixed this run (filed as a row, not silently patched)

`build-and-upload.sh`'s own comment (`:509-513` @`4ee8426c72`) asserts passing `SHA256` via
environment variable to the JSON tool is "already MSYS-safe" against the leading-`/`
base64-to-Windows-path mangle it names for CLI args. Measured this run: `irpt-performance-adapter`'s
computed sha256 `/CB3B9irhRbHafBMdcPe6zQGxU1bkCZbGPBPpv8npSY=` -- printed CLEAN by the script's own
`echo` and confirmed CLEAN in the real S3 object's `content-sha256` metadata
(`.tools/aws s3api head-object`, this run) -- was written into `lambda-source-map.json`'s
`artifact_sha256` field as `C:/Program Files/Git/CB3B9irhRbHafBMdcPe6zQGxU1bkCZbGPBPpv8npSY=` (the
exact drive-letter mangle the script's OWN CLI-arg comment describes, this time on the env-var
path it claims is safe -- the value's `/C` prefix is what triggers MSYS's single-letter
drive heuristic; no other member's sha256 begins that way). Corrected in this commit by writing
back the value read from the real S3 object's metadata (the SAME field this order is bounded to
touch); the whole manifest re-scanned for any further `C:\`/`Program Files`-shaped value after the
fix (0 found). Rowed at `IRPT_BCKEND-W4-S43` (disarm_owner `2.0.0_SA_COO~B`), since the script
itself is read-only under BOUNDS.

## (d) NO DEPLOY

0 deploys: `.tools/safe-apply.sh` / `terraform apply` / `aws lambda update-function-code` never
invoked by this battery or this order. `build-and-upload.sh` only stages S3 artifacts (the
build-artifact bucket), never a Lambda's served code -- confirmed by this run's own instrument
(the LIVE `Code.Location` census in part (a), read again after the REAL build in part (c), is
unchanged: served bytes for every function are exactly what they were before this order started;
this order changed the DECLARATION to match, never the served code itself).

## Token

`IBR63-MANIFEST-RE-PINNED-TO-THE-SERVED-BYTES` printed, rc=0, final run
(`IB-rtf-6_R63-AC1_battery_output.txt:285`, this commit).
