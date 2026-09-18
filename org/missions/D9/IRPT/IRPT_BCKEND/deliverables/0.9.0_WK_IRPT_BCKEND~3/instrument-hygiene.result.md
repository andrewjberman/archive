# IB-rtc-4 RESULT -- instrument hygiene: served bytes, stale batteries, vendor bar, layer cache

**TO:** `IRPT_BCKEND.TO-IB-rtc-4` | **worker:** `0.9.0_WK_IRPT_BCKEND~3` | **branch:** `wk-irpt_bckend-3-3`
**Worktree:** `/c/tmp/wk-irpt-3-3`, cut from `CLOUD` at `e9dc18f302`.
**Cold start.** No live vendor call, no deploy, no mint, no apply -- every AWS call this cell made
is a read (`get-function-configuration`, `get-function`, `get-layer-version`, and the downloads
those calls' own URLs point at). Every produced/served artifact this cell grades carries its
content hash (R-40), listed per arm below and again in the proof-of-spec instance.

## Criteria

| id | verdict | invocation | deciding line |
|---|---|---|---|
| `R34-AC1` | **PASS-by-output** | `timeout 1200 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_rtc_4.py` | rc=0, all four arms print their measurement, `IBR34-FOUR-ARMS-MEASURED` |
| `R34-AC2` | **RECORDED (judgment)** -- no verdict | evidence assembled for `3.0.0_SA_CVO` at L9 | in the proof-of-spec instance under `UNVERIFIABLE-BY-INSTRUMENT`; the judgment text is below |

Battery: `battery_ib_rtc_4.py` (SHA-256/hash-object `3c96c575fcbdf73ded8ab96aa3d730be37543f50`).
Transcript: `IB-rtc-4_R34-AC1_battery_output.txt` (hash-object `4b9e99edff92e2f3da31a927a90eda4dd56fa20b`).

---

## (a) W4-S28 -- the bytes comparison, PERFORMED, reading NOT-REPRODUCIBLE-shaped DIFFER

**Terraform root read:** `infra/aws/terraform/investor-reporting/ycharts/generate.tf`
(hash-object `bee392adbeaef351b3364c87d77cbd1b81e18288`) -- module `irpt_ycharts_generate` sources
`../../modules/yang-lambda`, whose `data.aws_s3_object.artifact` pins `source_code_hash` to the S3
object's own `content-sha256` metadata; the header names `infra/aws/lambda/ci/build-and-upload.sh`
as the upload mechanism.

**Three build attempts, one served reading:**

| attempt | mechanism | result |
|---|---|---|
| 1 | `build-and-upload.sh`'s own resolution rule (`source_dir/<name>`, no shared-root fallback) | **REFUSES**: 11 of 30 declared members (`enforce.py`, `errors.py`, `gate.py`, `keys.py`, `resolve.py`, `ids.py`, `firm_destination_policy.json`, `firm_registry.json`, `settings.json`, `served.py`, `loaders.py`) do not exist at the literal `source_dir` -- the canonical script cannot even attempt a zip |
| 2 | `rt2_package.py`'s multi-root packager (source_dir first, then `_authz`/`_scope`/`_keys`/`_ids`/`_gate`/`intake`/`directory`/`data/`/`terraform/investor-reporting/core`; `ZIP_DATE=2026-09-11`) | resolves 30 of 30; `sha256(b64) = c6BiKUE4bZNbvy72mtzD6RlOPAWTUi2yhcWogDsOQxQ=` |
| 3 | the SAME 30 resolved members, rebuilt with `build-and-upload.sh`'s own zip recipe (PowerShell `System.IO.Compression.ZipFile`, sorted entries, `LastWriteTime=2020-01-01`) | `sha256(b64) = SyHWPla5ejQqzg/o/GABrOPt0oLVKImhzYCO25wd5AQ=` |
| served | `.tools/aws lambda get-function-configuration --function-name irpt-ycharts-generate --query CodeSha256` | `CJ6aBh7BWJFcT2Vv0/cJFSXHaH5cs1LvqXvJRfkXHm8=` (equal to the DECLARED `artifact_sha256` in `lambda-source-map.json`) |

**NEGATIVE CONTROL:** sibling `irpt-status`'s served `CodeSha256` =
`j2IVLsWpxJKajr19li3XTQkrrl/Yp/TWs6fqStybzUI=` -- DIFFERS from the target's served value, so the
comparison mechanism discriminates rather than reading a constant.

**MEASUREMENT (verbatim from the battery):**
`MEASUREMENT: served CodeSha256 CJ6aBh7BWJFcT2Vv0/cJFSXHaH5cs1LvqXvJRfkXHm8= vs built
c6BiKUE4bZNbvy72mtzD6RlOPAWTUi2yhcWogDsOQxQ= -> DIFFER`

Two legitimate, deterministic build recipes disagree with the served bytes AND with each other,
and the CANONICAL mechanism cannot even run unassisted. This is read as **DIFFER**, not a clean
EQUAL, and printed with the reason and both hashes per the face's own instruction ("If the root's
build is not reproducible byte-for-byte from a worktree ... the arm prints that as the
measurement ... and the row stays ARMED with a named next act -- never a PASS by timestamp").

**PREMISE FOUND NOT TO HOLD, filed as `IRPT_BCKEND-W3-S39`:** the fix commit `56a6e07e8f`
(`infra/aws/lambda/investor-reporting/ycharts/extract/certify.py`) is not a declared or
resolvable member of ANY of the 216 functions in `lambda-source-map.json` -- including
`irpt-ycharts-generate` itself. `job.py`, `recipe.py`, `transport.py` and `entry.py` (the whole
`generate` package) were read for a reference to `certify`/`extract`; none imports it. So W4-S28's
own `disarm_owner` text ("the corrected extractor reaches a running function only at the
irpt-ycharts-generate package's next build") rests on a premise this cell's census does not
confirm, and no bytes comparison this cell could construct would ever be able to see that fix
aboard this function, EQUAL or not.

## (b) S32 -- the two stale round-1 batteries, RETIRED

- `deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_s_4.result.md` (hash-object
  `2bd60e94f7aa4a8172a24050580a90d3eddf6e08`) -- arm (h)'s `head-object` on the loose
  `.../directory_runner.py` key.
- `deliverables/0.9.0_WK_IRPT_BCKEND~1/holdings-snapshot-three-partner-joins-reconciled.result.md`
  (hash-object `56a2b75e11730af7eeb4d671771a16702fe2cd39`) -- the rule-13 deploy section's
  `head-object` on the loose `.../holdings_snapshot.py` key.

Each now opens with a header line reading, verbatim:

> **SUPERSEDED AT `86d2d0835f` BY row `IRPT_BCKEND-S32`: the deploy leg reads FALSE RED after the
> correct bundle mint; not an instrument at HEAD.**

followed by the reason (the loose per-file key is now a PERMANENT, by-design 404 after IB-rt-5's
correct bundle mint, per `safe_deploy_core.py`'s "loose leg frozen 2026-08-11, X-iii") and a
pointer to the CURRENT instrument for this surface
(`deliverables/0.4.0_DS_ClientPlatform~X/battery_ib_rt_5.py`). **0 keys minted, moved or re-keyed**
-- per S32's own NEVER, this cell issued no S3 write of any kind. Battery arm (b) confirms both
headers present: `2 of 2 result doc(s) carry the SUPERSEDED header`.

## (c) W4-S23 -- the vendor bar re-cut

**Bar text, verbatim, BEFORE this edit** (`RT8-AC1(a)` and `battery_ib_rt_8.py`'s own arm (a)
print block): *"0 external connections during the render (host guard log, denominator printed)"*.

**Bar text, verbatim, AFTER this edit** (`battery_ib_rt_8.py`, new `vendor_bar_report()`
function, hash-object `628b449a54d7ec6a6f870d3ee67f7a8d3a7c87f8`): *"0 VENDOR connections during
the render, over an enumerated vendor host list (host guard log, denominator printed);
foreign-but-not-vendor hosts (e.g. webfonts) are named, not counted against the bar."*

Exercised against the REAL committed render record
(`deliverables/0.9.0_WK_IRPT_BCKEND~4/RT8-a_render_record.json`, hash-object
`eab8e729b36a1d5a62c1bdf0d23c2134202bc5ab`) -- never a synthetic copy:

```
VENDOR LIST ENUMERATED (4)      : ycharts.com, api.ycharts.com, bd3.bdreporting.com, api.cloud.orionadvisor.com
FOREIGN, NOT VENDOR (2)         : fonts.googleapis.com, fonts.gstatic.com
VENDOR 0 of 12 requests         : 0 VENDOR CONNECTIONS
```

`battery_ib_rt_8.py`'s arm (a) `ok_a` predicate now gates on this same function
(`vendor_ok`) rather than a re-typed copy of the vendor-zero check, so the bar and the print are
one instrument, not two hand-maintained copies of one fact.

## (d) W1-S17 / S54 -- the layer fetch

`deliverables/0.9.0_WK_IRPT_BCKEND~2/rt2_verify_deployed.py` (hash-object
`7fe0406462d9986651c6c53e0e0bea2b9cac78a3`) gained ONE behaviour in `layer_python()`: when
`.scratch/layer/` lacks the `irpt-common` layer zip it needs, it parses the layer name and
version from the cache path's own filename, calls `.tools/aws lambda get-layer-version
--layer-name irpt-common --version-number 5` for `Content.Location`, downloads that URL into the
cache, and proceeds -- WARNing and returning `""` (never crashing) on any fetch failure. Nothing
else in the verifier or in `battery_ib_rt_2.py` changed.

**Exercised on a forced-cold cache** (this cell's own `.scratch/layer/` was deleted first to
guarantee a genuine cache-miss, not an already-warm one):

```
cache present before this run : False
FETCHING: C:\tmp\wk-irpt-3-3\.scratch\layer\irpt-common-5.zip absent -- downloading irpt-common version 5 (row W1-S17/S54)
FETCHED: C:\tmp\wk-irpt-3-3\.scratch\layer\irpt-common-5.zip (644526 bytes)
DIRECT run VERIFIED : 7 of 7
```

**Then `IB-rt-2`'s TERMINAL battery, re-run FROM THIS FRESH WORKTREE** (unmodified except for the
verifier edit above):

```
declared artifact_sha256 == live CodeSha256: 7 of 7; handler is the guarded entry: 7 of 7; Active/Successful: 7 of 7
IMPORT-OK 7 of 7 | negative control FIRES 7 of 7 | VERIFIED 7 of 7
15 of 15 arms PASS
IBRT2-SIX-GUARDED
```

Arm (e) reads 7 of 7 and the sha256 chain reads EQUAL 7 of 7, exactly as the face requires.

---

## R34-AC2 -- THE JUDGMENT, RECORDED AND NOT SELF-GRADED

Addressed to `3.0.0_SA_CVO` at L9. No verdict is claimed here.

### 1. Does arm (a)'s reading DISARM W4-S28?

**No, and not because of the DIFFER reading alone.** The literal reading is DIFFER: neither of two
independently-built, deterministic zips (this project's own proven multi-root packager, and the
canonical script's own zip recipe over the same resolved members) reproduces the served
`CodeSha256`. Read narrowly, DIFFER would mean "the fix is not aboard, and what is served instead
is whatever produced `CJ6aBh7B...`" -- but that framing assumes the fix's file was ever a
candidate member of this build, and it is not: `extract/certify.py` (the fix's actual location,
commit `56a6e07e8f`) is not declared or resolvable in ANY of the 216 functions this estate
deploys, `irpt-ycharts-generate` included. So the honest answer is narrower than DIFFER: **this
arm cannot speak to whether the certify.py fix is aboard, because that fix was never a candidate
input to any build this cell (or, by the same census, any other cell) could construct for this
function.** What WOULD settle it: first establish which deployed function, if any, is SUPPOSED to
import `extract/certify.py` at runtime (today, none does); if the answer is "none, it is an
offline/certification-only module", then W4-S28's own `disarm_owner` premise needs correcting
rather than a rebuild; if some function should carry it, wire it into that function's declared
`files[]` and rebuild via a byte-verified recipe, THEN compare bytes. Filed as
`IRPT_BCKEND-W3-S39` (ARMED, `disarm_owner: 2.0.0_SA_COO~B`).

A second, narrower fact worth separating from the above: even setting the certify.py question
aside, no recipe available in this worktree reproduces `irpt-ycharts-generate`'s served bytes at
all (three attempts, three different hashes, all differing from the served value). That is itself
grounds to distrust ANY future "EQUAL" reading on this function until the actual build history is
pinned -- an EQUAL from an unvalidated recipe would be exactly as uninformative as this DIFFER.

### 2. Does the S32 retirement leave any round-1 claim citing those batteries' deploy leg uncorrected?

Both `battery_ib_s_4.result.md` and the IB-s-12 result document now carry the SUPERSEDED header at
their top, above every other section, so a reader who opens either file sees the correction before
reaching the stale deploy-leg claim. This cell did not, however, search every OTHER file in the
project (task-order faces, other batteries, prior CVO reads, `project.json`) for a citation of
`battery_ib_s_4.py` arm (h) or `battery_ib_s_12.py`'s rule-13 section that might restate the FALSE
RED as a live fact -- that census is outside this cell's `<paths>` grant (only the two named
result docs and the two named `~1`/`~4`/`~2` deliverable directories in the grant carry a
directory-wide write, and a project-wide read-for-citations was not asked for by the face). If the
CVO or a later round wants that census run, it is a distinct act.

### 3. Is the W4-S23 vendor list complete against the estate's vendor set (YCharts, Black Diamond,
Orion, Eclipse, SmartX, Bloomberg, Schwab, Microsoft Graph)?

**No -- the render record's own enumerated list (`ycharts.com`, `api.ycharts.com`,
`bd3.bdreporting.com`, `api.cloud.orionadvisor.com`) covers 3 of the 8 named vendors: YCharts
(both hosts), Black Diamond (`bd3.bdreporting.com`) and Orion (`api.cloud.orionadvisor.com`).
Eclipse, SmartX, Bloomberg, Schwab and Microsoft Graph are ABSENT from the enumerated list.**
Whether that absence matters depends on what this specific render (the export
worker's print route) could ever reach: the portal print route this arm measures serves a
PDF render of an already-assembled bundle, and Eclipse/SmartX/Bloomberg/Schwab/Microsoft Graph are
upstream DATA sources for OTHER cells (performance adapters, narrative, directory), not hosts the
export-render page's own browser session would plausibly call. So the omission may be CORRECT for
THIS render's actual reachable surface -- but that reachability claim is not measured here, only
asserted by inference from the architecture, and this cell did not verify it by, e.g., reading
`render_export.cjs` or the print route's own allowed-origin configuration for a complete host
census. Recommend: either (a) the CVO accepts the four-vendor list as scoped to what THIS render
could ever call (a narrower, defensible claim than "the estate's vendor set"), or (b) a future cell
widens the enumerated list to all eight names and re-measures, in case the print route's browser
session can reach a wider surface than this record shows.

---

## Bounds observed

No live vendor call anywhere. No deploy, no mint, no apply -- every write this cell made is to its
own deliverables, the two named `.result.md` files (a header line only), the shared verifier and
the shared battery (both explicitly granted). No S3 object was created, moved, deleted or
re-keyed. Every AWS call was a read (`get-function-configuration`, `get-function`,
`get-layer-version`, and reads of the URLs those calls return). Every `.py` edit passed
`.tools/commit-gate.sh`. Every invocation ran under `timeout`. Scratch used only under
`.scratch/` in this worktree. No existing surprise row edited -- one new row appended,
`IRPT_BCKEND-W3-S39`.
