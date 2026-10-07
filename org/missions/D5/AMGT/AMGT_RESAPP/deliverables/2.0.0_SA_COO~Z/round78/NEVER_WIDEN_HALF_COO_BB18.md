# AMGT_RESAPP round 78 -- `AMGT-bb-18` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-07 ~19:5xZ

**SIGNED** (the signature block is the last section). Measured and drafted by a subagent of this seat on 2026-10-07, 18:4xZ to
19:3xZ, with nothing built, deployed, applied or uploaded and no `pip` command run; read whole by the issuer, whose calls on
its seven open points are the section THE ISSUER'S CALLS. Every number was measured in that session unless its line says
INFERRED or CITED.

**THE PIN: `9e42b6cdb7f13c45629245d9bdbd512095e0e0f0`** (the bb-23 drain; the shared tree's HEAD when the session started).
Every `git show <pin>:<path>` read and the whole CONTENT-DIFF below are at this one commit.

**THE PIN IS NOT HEAD ANY MORE, AND THAT MATTERS.** HEAD moved four times during the session (`5133f144fb`, `d7bbe4f5a3`,
`abc0541e42`, then `f6cff376d1` at 19:18Z, a pull-merge of the laptop trunk by `0.0.0_AB_MSTR~Z`). Up to `abc0541e42` the
packaged files were unchanged (0 diff lines over the closure paths). At `f6cff376d1`, **5 of the 132 packaged repo files differ
from the pin**, all from other projects:

| file | lines +/- pin to `f6cff376d1` | commits (author) |
|---|---|---|
| `lib/opal_naming.py` | +69 / -4 | `736a8f8a06`, `c17998e4fb` (`0.9.0_WK_LGIC_BLANKFIX~1`), `cc0c2b4b5c` (`0.9.0_WK_NFRA_CTLPLN~6`), merge `9cada5eb48` (`2.0.0_SA_COO~C`) |
| `infra/logic/registry/systems.json` | +95 / -95 | `c09b1ad769`, `11f54fba67` (`4.0.0_SA_CRO`) |
| `infra/logic/registry/resources.json` | +0 / -6 | `17ae4222c7` (`4.0.0_SA_CRO`) |
| `infra/logic/registry/exemptions.json` | +36 / -0 | `d5516cb074` (`4.0.0_SA_CRO`) |
| `org/standards/NAMING_SCHEMA.json` | +6 / -3 | `eb29bf7f37`, `f701d5da50` (`4.0.0_SA_CRO`, v1.16) |

`systems.json` and `resources.json` are NOT on this half's CHANGED list. So: **the GO names the pin exactly, or this half is
measured again at the commit the GO names.** A build at `f6cff376d1` would list 21 CHANGED, and the order makes a file off the
list a STOP. The pin is a sound build commit: 20 of 20 drains and cell commits checked are its ancestors (the 17 round-78 build
drains in the orders' last `<status>` lines, bb-23's `e01c130815`, ba-13's `281015b156`, AMGT_CORPUS's `04e5612a71`; negative
control: `f6cff376d1` is not an ancestor, rc 1).

**The act** for `opal-amgt-scoped-api`, under ONE NEVER-2 entry. Executor `0.7.0_AE_CloudOps~A`. Order:
`task-orders/AMGT_RESAPP.TO-AMGT-bb-18.the-code-redeploy.md` (LEG 0, cell bb-23, is landed at the pin and is not this half's act).

1. **Code leg.** ONE artifact built from a DETACHED worktree at EXACTLY the pin, never "at or after" it, under the build terms of
   the section THE BUILD'S TERMS. Then ONE `safe-apply` on `infra/aws/terraform/harvest/`, the plan graded UNTARGETED. It may move
   exactly the function's code (its artifact object and hash). **No route, no IAM, no memory, no schedule.** `memory_size` stays
   1769. Then `round71/checks/leadpanel_cold_warm.py --label after` and the cold invokes' `AMGT_PHASE` lines, reported, not graded.
2. **Snapshot event.** ONE direct invoke with exactly `{"amgt_scheduled_action": "refresh_freshness_snapshot"}`. Read its stamp.

## THE BASE, read live in this session (~18:5xZ to 19:0xZ) -- the rollback per key

| object | value | rollback |
|---|---|---|
| function CodeSha256 | `MkM9Kf37nmI+thEmZR+ij8ybbxGrHxqtsonjyI7N5eg=` (round 77 ba-20, built at `14a36147bd`), CodeSize 41,981,131, MemorySize 1769, runtime python3.11, LastModified 2026-10-07T04:40:17Z, one layer `opal-amgt-print-deps:1` | the prior artifact through the module, ONE code-only `safe-apply` |
| the artifact object `s3://opal-313476888478-lambda-artifacts/research/opal-amgt-scoped-api.zip` | VersionId `VHwcuot4i70V2evVL44EBgQc0BcAtScd`, 41,981,131 B, `content-sha256` metadata `MkM9Kf37...`, LastModified 2026-10-07T04:36:17Z | copy-object of that VersionId onto the key (or `upload_verified` of the kept zip), then the `safe-apply`; never an S3 delete |
| the deployed package on this box | `C:/tmp/ba20-r77-14a36147bd.zip`, 41,981,131 B, 380 entries; its sha256 in base64 is `MkM9Kf37nmI+thEmZR+ij8ybbxGrHxqtsonjyI7N5eg=`, EQUAL to the live CodeSha256 (one `get-function-configuration` read and one local hash) | it IS the rollback artifact and the build's input: it is not deleted, moved or renamed by this act |
| the /freshness snapshot object | `s3://opal-data-harvest/amgt/harvest/state/freshness_snapshot/current/snapshot.json`, 3,894,841 B, 2026-10-07T12:30:47Z, VersionId `GyD7kjRk9hcHp4npg3vtTFiEOpz8QHGL`, 302 rows | copy-object from that VersionId; NEVER an S3 delete |
| the gateway route list, IAM, schedule | not moved by this act: 0 `.tf` files differ between `14a36147bd` and the pin (section TERRAFORM) | none needed; a plan that shows one is a STOP |
| open NEVER-2 entries on this function | none on the shared tree at the pin; see OPEN DEPLOYS for the stale copies and for `amgt-corpus-r40-ap10d` | -- |

A rollback to `MkM9Kf37` also puts the dossier reader back at method `/5`: the 51 values of the section THE DOSSIER MOVE read
their `/5` text again (the `/5` objects stay stored; AMGT_CORPUS COO half, blast-radius table). The code and that reader roll back
TOGETHER.

## THE CONTENT-DIFF, measured at the pin against deployed `MkM9Kf37`

**How it was measured (no build ran).** The build script's own seed, closure and data-member code (lines 169 to 441 of
`build-and-upload-scoped-amgt.sh` at the pin, executed unchanged) was run over a `git archive` export of the pin. Its answer:
`CLOSURE: 114 entr(ies) at the fixed point after 5 pass(es) -- 41 seeded (1 handler + 40 .py under 5 seed package dir(s)), 73
added by closure`, plus 18 data members. Those 132 files were compared by content with the same paths in the deployed zip.

- The deployed zip: 380 entries = 124 repo-sourced + 256 vendored (147 under the four deployed folders, 109 from the five pure
  wheels).
- **Repo-sourced files, 132 at the pin: IDENTICAL 105, CHANGED 19, ADDED 8, REMOVED 0.** No file differs by line endings only
  (0); 5 members carry CRLF at the pin and the same 5 do in the deployed zip.
- **What `content_diff.py` should print at the build (INFERRED from the two counts above):** `files 388, IDENTICAL 361,
  CHANGED 19, ADDED 8, REMOVED 0, against MkM9Kf37...`. The 147 deployed-folder files are identical by construction (bb-23); the
  109 pure-wheel files are identical ONLY IF the five wheels that arrive are the files the last build used (same pins, same
  prune). A CHANGED or ADDED line under a vendored folder is a STOP.
- Cross-check against git: `git diff --name-status 14a36147bd <pin>` over the 132 paths lists 29 (19 M, 10 A). The 2 extra are
  `lib/research/lists/data/publishers.json` and `social_accounts.json`: ba-13 gave them a repo home, their bytes equal the
  deployed members, so they are IDENTICAL in the artifact.
- The handler `lambda_function.py` is IDENTICAL.

### CHANGED, 19 files

| file | lines +/- | who changed it | what |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | +68 / -14 | bb-17 `59f820cf17` (`0.9.0_WK_AMGT_RESAPP~302`) | the adapter: six hookups (coverage marker, country, inputs statement, officer rank, source names, peer price listing) |
| `lib/research/api/name_search.py` | +7 / -1 | bb-7 `8f6e1003db` (`~293`) | a record also matches on its legal name |
| `lib/research/identity/crosswalk.py` | +89 / -10 | bb-7 `8f6e1003db`; round 77 ba-13 `281015b156` (`~279`) | `legal_name` on the built pool record (a builder path; the route reads the stored pool); one default path reworded |
| `lib/research/management/bloomberg_fallback.py` | +2 / -2 | bb-4 `a27f993331` (`~292`) | the stored-officers reader lists the writer's slash-safe folder |
| `lib/research/scores/peers_v.py` | +13 / -0 | bb-13 `c8ff0a700e` (`~298`) | below 3 peers V reads not available, with the count |
| `lib/research/scores/divergence.py` | +5 / -4 | bb-22 `afb0a25ca1` (`~306`) | the six dispersion field names |
| `lib/research/freshness/build_view.py` | +10 / -22 | bb-15 `b06a551b1c` (`~300`); ba-13 `281015b156` | the rot signal's one home; default paths |
| `lib/research/lists/rot.py` | +3 / -0 | bb-15 `b06a551b1c` | `SIGNAL_HOME` |
| `lib/research/metrics/chatter_axis.py` | +3 / -5 | round 77 ba-13 `281015b156` | a default path and a comment |
| `lib/research/posture/fit.py` | +3 / -5 | round 77 ba-13 `281015b156` | `REGISTRY_PATH` now beside the module |
| `lib/research/provenance/render_print.py` | +2 / -3 | round 77 ba-13 `281015b156` | the hand-run `main()` output path |
| `lib/research/rules/figure.py` | +1 / -1 | round 77 ba-13 `281015b156` | a comment |
| **`lib/research/corpus/dossier.py`** | +275 / -3 | **AMGT_CORPUS**: `763e1e9885`, `a5bf4bd876`, `04e5612a71` (`0.9.0_WK_AMGT_CORPUS~2`) | `METHOD_VERSION` `/5` -> `/6`; see THE DOSSIER MOVE |
| **`lib/research/corpus/backlog.py`** | +16 / -16 | **AMGT_CORPUS**: `a74a1aff0e` (`2.0.0_SA_COO~X`) | one class value renamed `outside-fence` -> `unresolved-with-reason`, and a printed line |
| **`lib/research/harvest/publication_gold.py`** | +10 / -0 | **AMGT_HARVST**: `3c2a514a57` (`0.9.0_WK_AMGT_HARVST~106`) | anchored gold aliases in `_security_mentions` (the gold BUILD's counter) |
| **`lib/trading_calendar.py`** | +104 / -18 | **NFRA_CTLPLN**: `4b766e4e2d` (`0.9.0_WK_NFRA_CTLPLN~12`) | the fallback covers 2010-2027 and now RAISES outside it; see the branch below |
| **`lib/opal_naming.py`** | +95 / -13 | **LGIC_BLANKFIX / NFRA_CTLPLN / ADVI_COTBKF**: `40a21e850b` (`2.0.0_SA_COO~G`), `19b61836e4` (`0.9.0_WK_LGIC_BLANKFIX~2`), `4991b8b11b`, `1ea925a095` (`4.0.0_SA_CRO`) | a fourth grade verdict, `legacy_address()`, `name(fifo=)`, a census flag |
| **`org/standards/NAMING_SCHEMA.json`** | +15 / -9 | `19b61836e4` (`0.9.0_WK_LGIC_BLANKFIX~2`), `1ea925a095`, `01c56eda2b` (`4.0.0_SA_CRO`) | v1.12 -> v1.15 |
| **`infra/logic/registry/exemptions.json`** | +18 / -0 | **NFRA_CTLPLN**: `e7ac51a04c` (`4.0.0_SA_CRO`) | three fence-exemption rows for `cloudops-dell2-agent-user` |

### ADDED, 8 files (all round-78 cells; 0 from another project)

| file | cell | how it enters the artifact |
|---|---|---|
| `lib/research/api/coverage_marker.py` | bb-10 `e9e5227823` | seed dir `lib/research/api`; imported by the adapter |
| `lib/research/api/country_name.py` | bb-9 `a5872a91fa` | seed dir; imported by the adapter |
| `lib/research/api/inputs_statement.py` | bb-2 `047bef87aa` | seed dir; imported by the adapter |
| `lib/research/api/source_names.py` | bb-11 `49910b360c` | seed dir; imported by the adapter |
| `lib/research/management/officer_rank.py` | bb-3 `b0537d6b6f` | closure: `scoped_amgt.py` imports it inside a function |
| `lib/research/peers/price_listing.py` | bb-8 `d9299642ef` | closure: `scoped_amgt.py` imports it inside a function |
| `lib/research/api/segment_table.py` | bb-1 `eb4b736c75`, `6cf8a0d403` | seed dir ONLY (every `.py` under `lib/research/api` is packaged); nothing imports it |
| `lib/research/api/segment_period.py` | bb-21 `167efe1022` | seed dir ONLY; nothing imports it |

- **Size (INFERRED: pin repo files + the deployed zip's vendored files, the layer figure from the script):** 3,588,700 B +
  130,126,155 B = 133,714,855 B, + layer 121,743,633 B = **255,458,488 B against 262,144,000 B (97.4%, 6,685,512 B spare)**. The
  deployed package is 133,657,520 B unzipped, so the round adds 57,335 B.
- **Any file outside the two tables is a STOP.**

### SEVEN FILES FROM OTHER PROJECTS RIDE THIS ARTIFACT (7 of 19 CHANGED; 0 of 8 ADDED)

Round 77 had no rider. This round has seven. Each is read here for what it can change on a served route.

1. **`lib/trading_calendar.py` (NFRA_CTLPLN) -- a NEW BRANCH ON SERVED ROUTES.** The deployed package carries no
   `pandas_market_calendars` (0 members in the zip), so the function runs on the hardcoded fallback. At the pin that fallback is
   FAIL CLOSED: `is_trading_day`, `prev_trading_day`, `trading_days_behind`, `trading_days_between` and `weekly_production_day`
   raise `CalendarCoverageError` (a `ValueError`) for a date whose year is outside 2010-2027. The deployed copy never raises: it
   answers by weekday.
   - The closure dates for 2024-2027 are EQUAL in both copies (41 and 41, 0 only in one), so no trading-day count inside those
     years moves.
   - Callers in the closure: `scoped_amgt._stale_trading_days` (the served date against the frontier; the function holds no `try`, and its callers were not read),
     `scoped_amgt` top band (wrapped: a plain reason, never a 500), `rolling_windows`, `harvest/window_tone`,
     `freshness/stale_rule._age`.
   - Measured on the live snapshot with the pin's stale rule and calendar: 302 of 302 rows answered, 0 raised; 203 readable
     input days, oldest 2026-09-11, 0 outside 2010-2027.
   - **The branch the half names:** a stored date before 2010 (or the clock passing 2027-12-31) makes a staleness read raise
     where it answers today. No such date was found in the snapshot; the generation dates behind `_stale_trading_days` were not
     enumerated.
2. **`lib/research/corpus/dossier.py` (AMGT_CORPUS):** the dossier reader at method 6. See THE DOSSIER MOVE.
3. **`lib/research/corpus/backlog.py` (AMGT_CORPUS):** reached only through `corpus/continuation.py` (a function-scope import).
   The renamed value and the reworded print line are the backlog BUILDER's; no line of `scoped_amgt.py` names `fence14`
   (0 of the 114 code members outside `backlog.py` do).
4. **`lib/research/harvest/publication_gold.py` (AMGT_HARVST):** the 10 added lines are inside `_security_mentions`, the gold
   build's mention counter (called at `publication_gold.py:367` only). The routes call `_latest_gold_snapshot_rows_cached` and
   `_day_of`, which did not change. A security with no `anchored_aliases` skips the new lines.
5. **`lib/opal_naming.py`, `org/standards/NAMING_SCHEMA.json`, `infra/logic/registry/exemptions.json` (LGIC_BLANKFIX,
   NFRA_CTLPLN, the CRO's registry acts):** the function imports `lib.opal_naming` at `harvest/store` import, on the /thesis path
   and at the snapshot address.
   - `REGISTRY_FILES` now names an eighth file, `legacy_addresses.json`. The build packages seven and does NOT package it. The
     pin's module lists it as OPTIONAL and reads its absence as None.
   - Exercised in this session on a folder holding exactly the 132 packaged files: the registry loads with `legacy_addresses`
     None, `lib.research.harvest.store` imports, and `snapshot_address()` reads
     `s3://opal-data-harvest/amgt/harvest/state/freshness_snapshot/current/snapshot.json`, EQUAL to what the deployed package's
     own files compute. The five generated harvest prefixes are equal (same digest). So the snapshot event writes the same key.
   - `legacy_address()` raises a plain `RegistryError` if called in the package; 0 of the 114 code members call it.

**Round 77's ba-13 also rides** (the order's issuer notes say so): its drain came after `14a36147bd`. It moved default file
paths from worker folders to `data/` folders beside the modules. In the artifact neither the old nor the new path exists
(`lib/research/identity/data/universe.json` and `lib/research/posture/data/scanner_factor_metadata.json` are not data members),
so the absent-file branch each reader took before is the one it takes after. The local in-process checks cannot see that
branch (the files exist in the repo); the packaged-file-set run in EXPECTED OUTCOMES does.

## DATA FILES: `rot_signal.json` IS NOT PACKAGED, AND NO ROUTE READS IT

- The script's `DATA_MEMBERS` at the pin: 18, the same 18 arcnames as the deployed zip. Neither
  `lib/research/lists/data/rot_signal.json` nor `lib/research/freshness/seeking_alpha_job_record.schema.json` is among them.
  Both files exist at the pin; neither is in the closure; neither will be in the artifact.
- bb-15's last status says "the data file must be in the redeploy's closure (issuer reads it at the bb-18 pair)". **This is the
  read: it is not, and the served route does not need it.**
  - `rot.SIGNAL_HOME` is read by `build_view.find_rot_signal_path()`, called from `build_view.py:246` only: the hand-run
    `build()`. No other of the 114 code members calls it (3 text lines, all in `build_view.py`).
  - The served `/freshness` route imports only `NEVER`, `VENDOR_INPUTS` and `render_rot_signal` from `build_view`
    (`scoped_amgt.py:5794`), and feeds `render_rot_signal` the register it computes IN MEMORY from the two packaged list files
    (`read_list_register()`, `scoped_amgt.py:5812-5813`). It never opens `rot_signal.json`.
  - **The absent-file branch, named:** if the hand-run `build()` were ever run inside the package, `find_rot_signal_path()`
    returns None and the line reads `no rot signal at this vintage`. No route reaches it.
- **A call for the issuer:** accept that as read, or ask for the file in `DATA_MEMBERS`. The second is an edit to the build
  script: it lands before the commit the GO names, moves the pin, and adds one ADDED line to the table above.
- `seeking_alpha_job_record.schema.json` belongs to bb-16's reader, which is not in the artifact at all (next section).

## BUILT AND NOT SERVED, by ruling: proven at the pin

| module | in the artifact? | who reads it in the artifact |
|---|---|---|
| `lib/research/api/segment_table.py` (bb-1) | YES, as a seed-directory file | nobody: 0 import sites across the 114 code members (AST read). The only line of `scoped_amgt.py` that holds the words is `4015: "segment_table": "ABSENT_ON_INTERFACE"`, a dictionary key in a contract table, not an import or a call |
| `lib/research/api/segment_period.py` (bb-21) | YES, as a seed-directory file | nobody: 0 import sites; 0 text lines outside the module itself |
| `lib/research/freshness/collector_record.py` (bb-16) | **NO**: `lib/research/freshness` is not a seed directory and nothing imports it | nobody: 0 import sites, 0 text lines across the 114 |

`read_segment_table` and `label_periods` are named in 0 packaged files outside their own two modules. If the build's
`CLOSURE+` lines or the CONTENT-DIFF show `collector_record.py`, or any file importing one of the three, STOP.

## THE DOSSIER MOVE (CTO msg 31204; AMGT_CORPUS CTO half condition C2)

- **The reader's version:** deployed `lib/research/corpus/dossier.py:144` reads `METHOD_VERSION = "amgt-corpus-dossier/5"`
  (read from the deployed zip). The pin reads `"amgt-corpus-dossier/6"` (line 144), and `dossier.py` at the pin equals
  `04e5612a71`'s (`git diff --quiet`, rc 0).
- **What that moves:** `read_dossier` picks among the stored objects that carry the READER'S OWN method version when any exist,
  else among all. A package at `/6` serves each name's `/6` dossier as soon as one is stored.
- **The size of the move, CITED and not re-measured here:** **51 section values in 35 names** change on the Security Analysis
  page and the print pack: 25 gain their prose and 26 read absent with a reason where a bare heading was shown.
  - The after-census file:
    `org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/evidence/r40_ap10_section_recompose_census_after_a3_20261007.txt`,
    committed at `14c896b419` and present at the pin (55 lines). Its last lines: `section_recompose_census names_read 95
    fields_compared 950 fields_changed 51 other_change 2` and `served_under_40 49 gain_prose 23 absent_table_reason 2
    absent_no_prose_reason 24`. Every changed value is listed in it by name and field.
  - The pair it belongs to: COO half
    `org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/NEVER_WIDEN_ROUND40_AP10D_SERVED_ACT.md` @`14c896b419`; CTO
    half `org/missions/D5/AMGT/AMGT_CORPUS/ledger/NEVER_WIDEN_ROUND40_AP10D_CTO_HALF.md` @`b39724f085`.
- **Which act moves the page (CTO half C2: whichever of the dossier write and this deploy comes SECOND).** Read at ~19:0xZ with
  the tree's reader (`/6`): of 5 names sampled, 3 pick a `/6` object (BA US, 8306 JP, AMD US) and 2 still pick `/5` (TSM US,
  ZTS US). So AMGT_CORPUS's write (leg w, entry `amgt-corpus-r40-ap10d`, OPEN, its proof field empty at the pin) was under way or
  partly done at that minute.
  - **Branch W-first (the write is complete before this apply):** this apply is the act that moves the 51 values. Expected after
    it: TSM US positives reads its gained prose and 8306 JP management reads absent with its reason, as the census printed.
  - **Branch D-first (this apply lands before the write completes):** a name with no `/6` object keeps its `/5` values, and each
    moves when its `/6` object is written. Then the write is the served act, not this deploy.
  - **Either way, the AMGT_CORPUS CTO half's C1 comes before the second act:** the 25 gained values are read WHOLE and graded
    by `3.0.0_SA_CVO~Z`. Whether that grading exists was NOT measured here. The issuer reads it before the GO.

## THE BUILD'S TERMS (CTO msg 31206; AMENDMENT 1; Andrew's word that nothing is fetched from the internet on this box)

Read from the script at the pin (772 lines); the script was not run.

1. **`AMGT_DEPLOYED_ZIP=C:/tmp/ba20-r77-14a36147bd.zip`.** Line 134 stops the build when it is unset. Line 136 reads the live
   CodeSha256 on every run (one AWS read). Lines 139-140 call `vendor_from_deployed.py`, which exits non-zero on a hash mismatch,
   so `set -e` stops the build before any pip command (the first pip download is at line 154). There is no download fallback
   for pyarrow or rpds-py; the helper imports only `argparse`, `base64`, `hashlib`, `os`, `sys`, `zipfile`.
2. **`PIP_NO_INDEX=1` and `PIP_FIND_LINKS=<the folder holding the wheel files>`.** The script has two pip downloads and passes
   neither option itself: lines 154-156 (the five pure pins for cp311 manylinux2014_x86_64) and lines 592-593 (`rpds-py==2026.6.3`
   for the BUILD interpreter, which runs when this interpreter cannot import the zip's Linux binary; on this Windows box that is
   every build). **Both are satisfied from that one folder or the build stops.** The folder holds SIX files: the five pure
   wheels and the `cp314-cp314-win_amd64` rpds-py wheel (`python` here is 3.14.7).
   - Found on this box in this session: **0 of 6** (read: Downloads, Desktop, Documents and `C:\tmp`, three levels deep). The
     GO waits on their arrival, as the order says.
   - That pip honours the two variables end to end is pip's documented behaviour and is NOT exercised until the build.
     `PIP_LOG=<file>` in the same environment records it; the executor attaches that log.
   - `SITEZ_INSTALL_DOWNLOAD_LINE_CENSUS_20261007.md` lists 4 lines for this script (old numbering 130, 135, 138, 560: one
     comment, the two downloads, one echo). At the pin the two downloads sit at 154 and 592. With the two variables set neither
     reaches an index.
3. **`content_diff.py` DOWNLOADS THE DEPLOYED PACKAGE FROM AWS ON EVERY BUILD -- a call for the CTO, stated plainly.** Line 761
   of the script runs `content_diff.py --zip` in both modes. It calls `lambda get_function` (boto3) and then
   `urllib.request.urlopen(fn["Code"]["Location"])`: an HTTPS download of the 41,981,131-byte package from the function's code
   location. It is Opal's own artifact and an AWS read, not a package index, and it does not feed the two folders, so the
   ruling's Term 1 is not broken by it. But it is a fetch over the network during the build, and the same bytes are already on
   disk and hash-proven. The census does not list it: the census matches install and download command words and says itself
   that a Python `urllib` call is not matched. **The CTO half says whether the rule reaches it.** If it does, the build cannot
   run as written (the order's Rule: "if a listed line can fetch, the script does not run as it is").
4. **The build's other AWS use:** `gen_harvest_prefixes.py --check` (line 127) imports `lib.opal_naming` and makes no call. A
   `--build-only` run makes no AWS write. The upload (`upload_verified.sh`) is one `s3 cp` and one `head-object` read-back.
5. **Term 2, read on the zip this build makes:** `python .../round78/checks/r78_bb23.py --compare-zip <the built zip>` reads
   `R78 BB23 COMPARE-ZIP EQUAL: YES`, 147 of 147. Anything else is a STOP before the upload.
6. **THE THEN-DEPLOYED ZIP IS KEPT ON DISK AFTER THE APPLY.**
   - The script builds under `mktemp -d` and deletes that folder on exit. Without `--build-only <path>` no copy of the built
     zip survives on this box. So the build is run `--build-only <a kept path>`, and THAT file is the one uploaded.
   - After the apply, the kept file's sha256 in base64 equals the new live CodeSha256. It is the next build's
     `AMGT_DEPLOYED_ZIP`. If it is lost, the only copy is the function's code location, and taking it from there is the
     download Term 1 forbids as a fallback.
   - `C:/tmp/ba20-r77-14a36147bd.zip` is ALSO kept: it is this act's rollback artifact.
   - The live hash moves at the apply, not at the upload: a build between the two still wants the OLD zip. After a rollback
     the old zip is the deployed zip again.
   - After the apply `r78_bb23.py` AC1 clause C1 reads FAIL against the old zip (the helper refuses it, which is the ruling
     working). A re-run of AC4 to AC6 after the apply sets `R78_BB23_DEPLOYED_ZIP` to the new kept zip.
7. The order's preflight line "the build pip-downloads its pinned wheels" predates AMENDMENT 1 and is superseded by it.

## TERRAFORM: only the function's code may move

`git diff --stat 14a36147bd <pin> -- infra/aws/terraform/harvest/`: 3 files changed, 203 insertions, 43 deletions.

| file | commit | a `.tf` file? |
|---|---|---|
| `build-and-upload-scoped-amgt.sh` (106 lines changed) | bb-23 `e01c130815` (`0.7.0_AE_CloudOps~A`); ba-13 `281015b156` | no |
| `vendor_from_deployed.py` (new, 137 lines) | bb-23 `e01c130815` | no |
| `lambda_src/build_zip.py` (3 lines) | ba-13 `281015b156` | no: the chatter-axis builder, another function's package, not built by this act |

**0 `.tf` files changed.** No route, no IAM statement, no memory value, no schedule moved in the text since the round-77
build commit, whose own entry required a 0-diff re-plan after its apply and closed at `0fabcf4f0f` (the re-plan's own line
was not read here). So the expected plan is exactly ONE in-place update,
`module.scoped_amgt_api.aws_lambda_function.this`, moving `source_code_hash` (`MkM9Kf37...` -> the built artifact's),
`s3_object_version` (`VHwcuot4...` -> the new one) and `last_modified`. Anything else is a STOP before the apply. What the
plan actually shows is not measured: no plan was run.

## WRITERS OF WHAT MOVES (NEVER-1)

- **The function's code: N = 1 writer,** this act.
- **The snapshot object: N = 1 writer,** `refresh_freshness_snapshot()` in this function, reached by the daily schedule (12:30
  UTC) and this act's one event. Its key is computed by `lib.opal_naming.address()`, a file this act changes: the key was
  computed on the packaged file set and is EQUAL to the deployed one. The stored view stays the unannotated one, and its rot
  line is computed in memory as before.
- **The dossier values on the page: N = 2 acts,** AMGT_CORPUS's write and this deploy. Each has its own pair; the second one
  moves the page (THE DOSSIER MOVE).
- **Served bodies, read from the producer's own rule (the adapter diff at the pin, +68 / -14):**
  - `/overlay` and `/thesis`: ADDED `research_coverage` (covered, outside coverage with one sentence, or not known when the
    list cannot be read).
  - `/overlay` and `/thesis` `header_figures`: the COUNTRY_FULL_NAME figure's `value` changes from the stored upper case to
    plain case, with `value_as_stored` beside it. **An existing served value changes** (`UNITED STATES` -> `United States`).
  - `/thesis`: ADDED `input_provenance`, one statement with one filings row before the pack row. The overlay's own
    `input_provenance` is unchanged (issuer ruling on row Z-W302-S2).
  - `/thesis` `management.officers`: the same rows REORDERED, chief executive first. **An existing served order changes.**
  - `/overlay` `provenance` entries, the feed, and the ledger provenance: ADDED `source_name`; feed items gain
    `publisher_name`.
  - `/overlay` peers: a row whose listing rule refuses the record carries `price_currency_reason` and NO `price_currency`.
    **An existing served value is withheld** (deployed today: 2 of 60 sampled rows serve USD behind a foreign price).
  - Stored officers for a slash name (BP/ LN, NG/ LN) are found (bb-4).
  - `/resolve` also matches a legal name, where the stored pool record carries one (bb-7, after the issuer's pool mint).
  - Peers V: below 3 peers the scorer answers not available with the count. The route serves STORED score records, so the
    sentence appears only after the next scores run (bb-13). Divergence stays ABSENT until its fields land (bb-22).

## EXPECTED OUTCOMES (both branches)

| check | before (`MkM9Kf37`) | expected after | if not |
|---|---|---|---|
| `r78_deployed.py`, line 1: `r78_bb17.py --crit AC1 --where deployed` | **NO, 0 of 6 clauses** (run in this session): H1 no marker, H2 `UNITED STATES`, H3 no rows, H4 2 of 6 rosters, H5 0 of 3, H6 2 wrong of 60 rows | YES, 6 of 6 | rollback of the leg |
| the further lines the issuer lists (section PROPOSED LINES) | each a bound that passes at the base, by its own docstring; not re-run here | YES each | rollback of the leg |
| AC2: r76 c62 and c63, r75 c59 with its 40-wide burst | YES each (round 77's proof) | YES each: no round-78 cell changes a clause they grade. The country value, the officer order and the peer currency are not read by them | a NO is a rollback trigger; a c59 that reads UNMEASURED (exit 2) is reported, not a rollback |
| AC3: `r77_served_shape.py --where deployed` | YES (round 77's one real run) | YES, no regression | rollback of the leg |
| new CodeSha256 | `MkM9Kf37...` | differs AND equals the artifact built at the pin (the kept zip's sha256 in base64) | an unchanged hash is a 0-diff deploy: STOP |
| the built zip against the deployed zip's four folders (`--compare-zip`) | -- | EQUAL: YES, 147 of 147 | STOP before the upload |
| the CONTENT-DIFF the build prints | -- | CHANGED 19, ADDED 8, REMOVED 0, and exactly the files in the two tables | any other file, or a vendored file CHANGED: STOP before the upload |
| the plan | -- | exactly one in-place update of the function | any other resource: STOP before the apply |
| the dossier values | `/5` on every name | Branch W-first: 51 values in 35 names move at this apply. Branch D-first: none moves until its `/6` object is written | not a rollback of itself: a served value the after-census does not list is a row to the CTO (AMGT_CORPUS Branch C) |
| the snapshot after the event | 3,894,841 B, 302 rows, VersionId `GyD7kjRk...` | a new VersionId at the SAME key, 302 rows, written by the new code | copy-object of `GyD7kjRk...`; never a delete |
| cold read (leadpanel `after`) | -- | reported; the adapter gains four module-scope imports of small pure modules | not a rollback |

**Measured locally before this draft:**
- **On the packaged file set** (a folder holding exactly the 132 repo files of the pin at their zip names, imported from there
  with the repo root off the path; `rot_signal.json`, `identity/data/universe.json`, `posture/data/scanner_factor_metadata.json`
  and `legacy_addresses.json` absent, as they will be in the artifact): `r78_bb17` AC1 reads **YES, 6 of 6** (H4 6 of 6 rosters,
  H6 0 wrong of 60), and `/freshness?view=page` answers 200 with 95 rows, 3 stale, and the owner line "Andrew owns the publisher
  list and the social account list." The vendored packages came from this box's own Python, not from the zip.
- On the shared tree while its packaged files equalled the pin (0 diff lines, read before and after the run): `r78_bb17` AC1
  YES 6 of 6; `r78_bb17` AC2 YES (`r77_served_shape.py --where local` reads YES).
- `r76_served.py --cell c62 --where local`: YES, 95 names, 69 items. INFERRED for the pin: the run began ~19:02Z and the trunk
  merge landed in the tree at 19:12Z, after its modules were loaded.
- `r76_served.py --cell c63 --where local`: YES (95 names, 0 entries disagreeing with /freshness), but it started at 19:16Z on a
  tree that was no longer the pin (the trunk merge had landed). It is a read of the merged trunk, NOT a pin measurement.

**Not proven by this act, stated so it is not assumed:**
- The gateway: every check invokes the function directly. The walk (bb-19) is the first read through the edge.
- bb-4 (slash-name officers), bb-7 (legal names in search) and bb-13 (the Peers V sentence) have NO deployed check: their
  checks take `--where local` only, and H4's roster sample holds no slash name.
- The absent-file branches of ba-13's moved paths on the real function (the packaged-file-set run above is their only
  exercise before the deploy).

## THE LINES OF `round78/checks/r78_deployed_cells.txt` (filled by the issuer in the commit that carries this half)

The format is round 77's: one shell command per line, run from the repo root with `PYTHONPATH` set to it; `#` lines are
comments; a command passes on exit 0; an empty list reads NO CELLS LISTED (exit 2).

Of the 22 `r78_bb*.py` checks, 4 accept `--where deployed` (read from each script's argparse): `r78_bb17.py`, `r78_bb5.py`,
`r78_bb6.py`, and `r78_bb12.py` for its `ORGANIC` arm only. The other 18 are local-only or take no `--where`.

```
# AMGT_RESAPP round 78 -- the deployed checks AMGT-bb-18's AC1 runs (r78_deployed.py). THREE lines; filled by the issuer at the GO.
# Line 1 FAILS against the deployed BASE MkM9Kf37 (0 of 6 clauses, run 2026-10-07 ~18:5xZ). Lines 2 and 3 are bounds over all 95 /thesis reads.
python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb17.py --crit AC1 --where deployed
python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb5.py --crit AC1 --where deployed
python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb6.py --crit AC1 --where deployed
```

- **Line 1 is the round's line** (its own docstring: "the line the redeploy's list carries"). It grades six of the served
  changes: the coverage marker (bb-10), the country (bb-9), the statement of inputs on /thesis (bb-2), the officer order
  (bb-3), the source names (bb-11) and the peer price currency withheld (bb-8).
- **Lines 2 and 3 are bounds, and they are the only deployed reads of all 95 /thesis bodies:** every /thesis answers 200, the
  class counts sum to 95, and the named controls hold (BA served, ASML NA refused, AMD with no filing analysis; ASML NA carrying
  both labels). They are the widest read of the dossier reader at `/6` and of the inputs statement that this round has.
  Neither writes without `--write`. Each makes 95 invokes (line 2 also 95 S3 lists); `r78_deployed.py` allows 1,500 s a line.
  They were NOT run against the base in this session. If the issuer lists them, each is run once against `MkM9Kf37` first,
  as round 77 did; if either does not pass there, it is not listed.
- **The count the GO states:** 3 with all three lines; 1 with line 1 alone.
- **NOT proposed:** `r78_bb12.py --crit ORGANIC --where deployed`. It passes only when the real social account list has
  organically fallen due, which is a fact about the list's review date, not about this deploy.
- **Served changes with no line:** the slash-name officers (bb-4), the legal-name search (bb-7), the Peers V sentence (bb-13),
  and the dossier version. For the dossier, AMGT_CORPUS's own leg v reads TSM US positives and 8306 JP management through the
  live route. A deployed arm for bb-4 or bb-7 would be a new check, which is the issuer's to cut.

## OPEN DEPLOYS (every live worktree read)

`git worktree list --porcelain`: **89 worktrees, 89 answered `ls-tree`, 0 errors, 0 with an empty folder.** Entries per tree: 16
to 29 (1,770 in all); **72 distinct entry files in the union.** The shared tree's HEAD holds 20 (24 files on disk: 4 untracked
`irpt-*` entries). A text read of the shared tree's folder for `opal-amgt-scoped-api`, `terraform/harvest`, `scoped_amgt` or
`bb-18`: 1 file.

| entry | where | what it is to this act |
|---|---|---|
| `amgt-corpus-r40-ap10d.json` | the shared tree and 3 worker trees; OPEN since 2026-10-07T17:08Z; legs Lw and Lv, both proofs empty at the pin | **The one that matters.** AMGT_CORPUS's dossier write. Its title names this deploy as the act that serves it. Its Lv leg reads the live route AFTER this deploy, so it stays open across this act and is not this executor's to close |
| `amgt-resapp-r77-ba20.json` | 3 stale worktrees only (`C:/tmp/r77-279`, `C:/tmp/wk-oplgtw-r26b-29`, `Desktop/coo-o-r23`); absent from the shared tree | closed on CLOUD at `0fabcf4f0f`. The artifact was measured: the live CodeSha256 IS its build (`MkM9Kf37`). World-done; nothing to re-execute |
| `amgt-resapp-r76-az5.json` | 1 stale worktree | closed on CLOUD at `cad400c0b3`; superseded by round 77's deploy |
| `amgt-resapp-r74-ax5.json`, `amgt-resapp-r56-af6-price-cutover.json` | 1 and 13 stale worktrees; absent from the shared tree at the pin | older entries of this project in trees cut before they closed. af6 is a box-side merge for the price producer, not this function. Their closing commits were not read |
| `amgt-corpus-r40-ap10m.json` | the shared tree and 9 others; OPEN, leg Lv waits on the 2026-10-08 13:00Z fire | the induction re-pin that lands the dispersion fields bb-22 reads. Not this function's code; not touched |
| `harvst-sa-job-record-m-20261007.json`, `amgt-harvst-r49-av2-...json`, `amgt-corpus-r39-ao2.json` | 10, 4 and 29 trees; none on the shared tree at the pin | AMGT_HARVST and AMGT_CORPUS acts; none names this function or this terraform root |
| `leadpanel-price-producer-schedule.json`, `freshguard-leg4-writer-wiring-finish.json` | all 89 trees; OPEN since 2026-09-24 and HELD since 2026-07-09 | a box-side schedule and a graph writer; neither is this function |

No entry in any tree is open on `opal-amgt-scoped-api` or on `infra/aws/terraform/harvest/`. The executor reads the trees again
before acting: this read is from ~18:5xZ and the trunk has moved since.

## THE ISSUER'S CALLS ON THE SEVEN OPEN POINTS (`2.0.0_SA_COO~Z`, at signing, 2026-10-07 ~19:5xZ)

I read this half whole before signing. The measurements are the drafting read's (a subagent of this seat); two base reads below
are mine, run at signing.

1. **The build commit is `9e42b6cdb7f13c45629245d9bdbd512095e0e0f0`, EXACTLY.** The GO names it. The trunk merge that landed at
   19:18Z (`f6cff376d1`) is NOT built: it moves 5 packaged files of other projects, two of them off this half's list. They ride a
   later redeploy under their own measurement.
2. **`content_diff.py`'s download of the deployed package: the CTO's call,** asked in the message that carries this half. This
   seat's recommendation: it is a read of Opal's own artifact from AWS, not a package from the internet, and it is the build's
   only check of the new zip against what is live; it stays.
3. **`rot_signal.json`: ACCEPTED as read.** It is not packaged and no served route opens it; `/freshness` computes the register
   in memory. The note on bb-15's status line ("must be in the redeploy's closure") was this seat's assumption at the drain and
   is wrong; it is corrected on the order in the commit that carries this half. No build-script edit.
4. **The seven riders: ACCEPTED on the measurements above,** with one branch named for the CTO half: the trading calendar now
   RAISES for a date whose year is outside 2010-2027 where the deployed copy answers by weekday. 302 of 302 snapshot rows
   answered and 0 raised. The generation dates behind `_stale_trading_days` were not enumerated, so a stored date before 2010
   there would surface as a failed read after the apply: it is covered by line 2 of the deployed list (every one of the 95
   `/thesis` reads answers 200) and by AC3.
5. **The dossier order:** this half covers BOTH branches (W-first and D-first). A condition of the GO, not of this signature:
   the issuer reads, at the GO, whether AMGT_CORPUS's write is complete and whether `3.0.0_SA_CVO~Z`'s whole read of the 25
   gained values exists (AMGT_CORPUS CTO half, C1). If this apply would be the SECOND act and that read does not exist, the GO
   is not given.
6. **The deployed list is THREE lines.** Both bounds were run by this seat against the base at signing (live CodeSha256 read
   `MkM9Kf37...` immediately before): `r78_bb5.py --crit AC1 --where deployed` exit 0, `83 + 10 + 2 = 95 of 95`, READ: YES;
   `r78_bb6.py --crit AC1 --where deployed` exit 0, 95 of 95, READ: YES. Line 1 reads NO at the base (0 of 6). The file
   `round78/checks/r78_deployed_cells.txt` is filled in the same commit; the GO states 3.
7. **The six wheel files: 0 of 6 on this box.** The GO waits on them. No part of this act runs before they are here.

Served changes this act makes with NO deployed check (bb-4 slash-name officers, bb-7 legal-name search, bb-13's sentence): the
issuer reads bb-4 and bb-7 by hand through direct GET-shaped invokes after the apply (`/thesis` officers for `BP/_LN_Equity`;
`/resolve?q=apple` and `?q=microsoft`) and prints them in the round's one real run.

## NOT MEASURED

- **The build itself.** No zip was made. The closure is the script's own code run over the pin's files; the vendored half
  (the five pure wheels, their prune, the walk of the copied folder, lines 443-487) and the script's verify, isolated-runtime
  and size steps were not run. The size line and the `files 388` line are INFERRED.
- **The edited Python block of the build script** (bb-23's S4 to S7) has never run: bb-18's build is its first real run.
- **pip under `PIP_NO_INDEX` and `PIP_FIND_LINKS`:** not exercised. Whether the six wheel files have arrived beyond the four
  folders read. Whether the arriving wheels are byte-equal to the ones the last build used.
- **The plan.** No `terraform plan` ran. Live drift in this root since round 77's 0-diff re-plan is not measured.
- **IAM:** whether any round-78 module needs a read the function role lacks. The order's preflight says the issuer ran
  `comp-iam` at the cut; it was not re-run. The new reads by text: `_research_coverage` reads the covered list the routes
  already read; bb-4 lists the same bronze prefix under a differently spelled folder.
- **The deployed function at the new code.** Every "expected after" is a prediction from the pin's code run locally.
- **The base reads of AC2 and AC3** (r76 c62 and c63, r75 c59, `r77_served_shape.py --where deployed`) were not re-run against
  `MkM9Kf37` in this session; they are cited from round 77. `r78_bb5` and `r78_bb6` were not run at all.
- **r76 c63 local at the pin:** not measured (the tree moved; the YES above is the merged trunk's). **r75 c59** was not run
  locally.
- **The 51 values:** cited from AMGT_CORPUS's census, not recomputed. Whether the dossier write is complete (5 names sampled of
  95). Whether the CVO has graded the 25 gained values.
- **The trading calendar's reach:** the snapshot's 302 rows were tested; the generation dates read by `_stale_trading_days`
  and the dates read by `rolling_windows` and `window_tone` were not enumerated. Whether the layer `opal-amgt-print-deps:1`
  holds `pandas_market_calendars` was not read (the zip holds none).
- **The layer** was not opened; its unzipped size is the script's constant.
- **The stale worktrees' older entries** (`r74-ax5`, `r56-af6`): their closing commits were not read. The 72 union entries
  were not each opened: the shared tree's 24 files were text-read for this function's name, the others were judged by name.
- **`lib/opal_naming.py` in the package beyond the calls exercised:** registry load, `lookup`, `address`, the store import and
  the five prefixes were run on the packaged file set; `grade()` and `name()` are not called by any route and were not run.
- **The portal:** whether a page or a test reads `UNITED STATES` literally, or depends on the old officer order, was not read.
  The page's use of the new fields belongs to the walk (bb-19).

AWS calls made in this session, all reads: `lambda get-function-configuration` (1, plus those inside the check runs),
`s3api head-object` (2), `s3api get-object` of the snapshot (1), GET-shaped direct invokes of the deployed function by
`r78_bb17.py --where deployed`, and the S3 reads of the local handler runs and of 5 `read_dossier` calls.

## SIGNED

`2.0.0_SA_COO~Z`, 2026-10-07 ~19:5xZ, for the act as stated, at the pin `9e42b6cdb7` only. The CTO half is owed by
`1.0.0_SA_CTO~Z` and names: the dossier move (msg 31204), the two build terms (msg 31206), the seven riders with the
trading-calendar branch, and its ruling on `content_diff.py`. No leg runs before both halves, the six wheel files and the GO.

## ADDENDUM 1 (`2.0.0_SA_COO~Z`, 2026-10-07 ~23:1xZ) -- THE RE-PIN: `fbb643923e9ab3db14aa8d8062fa9015a6722690`, ONE PACKAGED FILE MOVED

**Why:** the CTO's half made the dossier's gained passages a condition of the GO (C2). AMGT_CORPUS repaired the dossier
(`e3d276634c`, then AMENDMENT 5 `901be95e86`), wrote 95 dossiers at method 7 (ledger `amgt-corpus-r40-ap10d2` CLOSED @94a90adc3a),
and `3.0.0_SA_CVO~Z` re-read them: C1 MET, 25 of 25 gained passages the section's prose, NKE and SAP clean, 5 values pure trims of
55 characters (grade `org/tier1_exec/3.0.0_SA_CVO/deliverables/AMGT_CORPUS_ROUND40_AP10D2_METHOD7_REREAD_GRADE_20261007.md`
@09c91edcc2). The CTO asked for the re-pin (msg 31457).

**The new pin is `fbb643923e`,** on the local scratch branch `bb18-pin-r78-method7-amended`. It REPLACES `9e42b6cdb7` everywhere
this half says "the pin". How it was made: git plumbing by this seat (read-tree of `9e42b6cdb7`, six blobs taken from CLOUD at
`09c91edcc2`, commit-tree, parent `9e42b6cdb7`). It is a build pin only and is never merged. Resolved by CONTENT, measured:

- `git diff --stat 9e42b6cdb7 fbb643923e`: **6 files**, 265 insertions, 14 deletions: `lib/research/corpus/dossier.py` and five
  files under `lib/research/corpus/tests/`. Nothing else.
- Each of the six blobs equals CLOUD's at `09c91edcc2`: 6 of 6.
- Those six files were touched between `9e42b6cdb7` and CLOUD `09c91edcc2` by exactly two non-merge commits, `e3d276634c` and
  `901be95e86` (both `0.9.0_WK_AMGT_CORPUS~2`); 0 other commits touch any of the six.
- **Packaged paths that differ from the old pin: ONE, `lib/research/corpus/dossier.py`** (+63 / -4 against `9e42b6cdb7`;
  +335 / -4 against the round-77 build commit `14a36147bd`). The five test files are not packaged.
- The `import` and `from` lines of `dossier.py` are the same set at both pins (0 differing lines), so the closure is unchanged:
  the CONTENT-DIFF stays **CHANGED 19, ADDED 8, REMOVED 0**, the same file lists; `dossier.py` was already on the CHANGED list.
- `METHOD_VERSION` at the new pin: `"amgt-corpus-dossier/7"` (deployed: `/5`).
- The scratch branch `bb18-pin-r78-DO-NOT-BUILD-method7` (`e06970c43f`) carries the WITHDRAWN first repair and is never built.

**What changes in the section THE DOSSIER MOVE:** the reader goes from `/5` to `/7`, not `/6`. The served move is AMGT_CORPUS's
method-6 census (51 values in 35 names) plus the method-7 trims (5 values, 55 characters; that project's (d2) record). The write
is complete (95 of 95 at method 7), so this apply IS the act that moves the page: branch W-first. **Six values are served
known-truncated, stopping mid-sentence, by the CTO's ruling (msgs 31383, 31394): LLY, NU (two), QXO, UNH, and SHOP management.**
Round 41 of AMGT_CORPUS reads across page breaks first. A rollback puts the reader back at `/5`.

**The chatter base (CTO half of AMGT_HARVST gold rebuild #8, C1):** the rebuild ran BEFORE this act and ended (last write read
back 22:41:32Z, verify ended 22:48Z; `2.0.0_SA_COO~H` msg 31459). The base this act's checks read against: mention table 48,025
rows (was 33,665), daily table 67,760 rows (was 59,148). The base reads of r76 c62/c63 and r75 c59 in this half predate that move;
the executor's AC2 is the first read of them on the moved chatter, and a NO there is read against the rebuild's record before it
is called this deploy's.

**Not re-measured for this addendum:** the closure (argued from the unchanged import lines, not re-run); the packaged-file-set
run of `r78_bb17` AC1 (it ran at the old pin; `dossier.py` is not read by its six clauses' assertions but is on the `/thesis`
path); `r78_bb5` and `r78_bb6` against method 7 locally.

**Still waiting:** the six wheel files (0 of 6 on this box at 23:0xZ). SIGNED for the new pin: `2.0.0_SA_COO~Z`, 2026-10-07 ~23:1xZ.
