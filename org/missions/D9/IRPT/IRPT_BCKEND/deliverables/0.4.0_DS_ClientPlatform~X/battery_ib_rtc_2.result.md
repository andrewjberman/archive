# IB-rtc-2 -- THE BUNDLE CARRIES THE RUNNER'S WHOLE CLOSURE: result

**TO:** `IRPT_BCKEND.TO-IB-rtc-2` | **serial:** `0.4.0_DS_ClientPlatform~X` |
**branch:** `wk-irpt_bckend-3-ds` | **worktree:** `/c/tmp/wk-irpt-3-ds` | **base:** `e9dc18f302`
**Invocation:** `timeout 900 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.4.0_DS_ClientPlatform~X/battery_ib_rtc_2.py`
**Result:** `rc=1`, **0 of 6 graded arms PASS** (4 FAIL, 2 NOT-EVALUATED), token withheld.
**R32-AC1 = FAIL. The order stays OPEN.** Nothing was declared, nothing was minted, no host was started.

---

## The short version

The closure is **8 files** and the bundle declares **3** of them. I did not declare the other 5,
because each one runs into something the order did not expect:

| missing member | what stops it | row |
|---|---|---|
| `data/assets/scripts/gold/runners_49f/runner_common.py` | a bundle member is routed **out of its own per-file deploy leg**; this file is served today at `s3://opal-data-49financial/_code/runner_common.py` | `IRPT_BCKEND-S62` |
| `data/inf/scripts/gold/runners_inf/runner_common.py` | same: served at `s3://opal-data-inf/code/gold/runners_inf/runner_common.py` | `S62` |
| `data/cot/scripts/gold/runners_cot/runner_common.py` | same: served at `s3://opal-data-cot/code/gold/runners_cot/runner_common.py` | `S62` |
| `data/firm_registry.json` | outside `data/*/scripts/gold/**` and `lib/**`, so the face itself calls it a BLOCKING row | `S58` |
| `infra/aws/lambda/investor-reporting/_contracts/DirectoryEntry.schema.json` | same | `S58` |

Separately, **declaring all 5 would still not let IB-rtc-3 build anything.** The deployed dispatch
unpacks the tarball into the runner's own directory and moves exactly three flat-named files. The
runner looks for each firm's `runner_common.py` outside that directory. I built one payload that
carries the full closure and placed it two ways: the declared layout gives 3 of 3 firms IMPORT-OK,
the dispatch's own unpack gives 0 of 3 (row `S59`). **The member list and the dispatch's unpack
have to be decided together, and that decision belongs to the CTO.**

---

## Why I declared nothing

The face says to declare each member "exactly as IB-rt-5 declared the first members". IB-rt-5's
members had no live per-file leg: their loose keys returned 404, so moving them into a bundle cost
nothing. The three `runner_common.py` files are the opposite case. The guard's own functions show it:

```
data/assets/scripts/gold/runners_49f/runner_common.py: loose leg [advi] s3://opal-data-49financial/_code/runner_common.py -- SERVED, ETag 5221d6b5d73157ce9728807a7a6b9c80 == the repo md5
    declared as a member, bundle_for_member() -> investor_reporting: the main() routing loop moves it OUT of the loose leg (BUNDLE-ROUTED, loose leg frozen)
... (inf and cot read the same) ...
undeclared closure members with a LIVE loose leg: 3; that a declaration would route out of it: 3
```

`safe_deploy_core.py:1279-1287 @e9dc18f302` sends a bundle member to the bundle mint and **not** to
the loose leg. `bundle_for_member` (`:731-738`) checks every tree, so a declaration in the mdpf
tree's bundle would take over deploys for files in the advi, inf and cot trees. After that, the next
DS commit to any of those three modules would re-mint the IRPT tarball and leave that firm's served
`runner_common.py` on its old bytes. The push would still read green. Three production gold chains
would keep running stale code and nothing would report it.

Whether that is acceptable, or whether the guard gets a "distribution member" semantic that keeps
the loose leg, is a change to the CTO-blessed X-iii contract. It is not a `CODE_TREES` edit, so it
is not mine to make. Row `S62` gives three possible fixes and this seat's recommendation.

With no declaration, a re-mint would have produced the same bytes as the object already served.
So I opened no change-management entry, took no sentinel and made no mint.

---

## The six graded arms

### (a) CLOSURE -- FAIL, 3 of 8 declared
Two instruments derive the closure, and they agree:
- a **static AST sweep** of 6 modules (the runner, `trading_calendar`, `ids`, and the three
  `runner_common`) finds 8 USED repo-file references and 1 DEAD one;
- a **dynamic audit** imports the runner, instantiates SourceSet for all three firms and calls
  the runner's no-S3 entry points (`client_firms`, `firm_bucket_map`, `load_contract`,
  `opaque_id`, `tcal.calendar_source`). It records every repo file opened or imported, and finds
  the same 8.

```
CLOSURE N = 8
  DECLARED  data/assets/scripts/gold/investor_reporting/directory_runner.py
  MISSING   data/assets/scripts/gold/runners_49f/runner_common.py
  MISSING   data/cot/scripts/gold/runners_cot/runner_common.py
  MISSING   data/firm_registry.json
  MISSING   data/inf/scripts/gold/runners_inf/runner_common.py
  MISSING   infra/aws/lambda/investor-reporting/_contracts/DirectoryEntry.schema.json
  DECLARED  infra/aws/lambda/investor-reporting/_ids/ids.py
  DECLARED  lib/trading_calendar.py
```

**Diff against W2-S51.** The row names 8 paths and counts them as seven. At this tip one of them
has dropped out: `infra/aws/lambda-edge/_shared/firm-config.mjs` is still assigned at
`directory_runner.py:123` (`FIRM_CONFIG_PATH`) but nothing reads it, because `firm_bucket_map()`
became a generated literal (LGIC_ENFORCE DEC-5, `@45187da290`). No file needed to be added.
`ids.py:64` names `_ids/raw_keys.json`, but only `raw_keys()` and `raw_key_for()` open it, and
no runner path calls either one, so it is outside the closure. `holdings_snapshot.py` is declared
but not in this closure (it is a sibling runner).

### (b) GUARD TESTS -- FAIL, 2 of 4 green
The denominator is the four test files that exercise the guard. `test_code_trees_invariant.py`
fails 3 of 18 and `test_safe_deploy.py` fails 7 of 14. Both counts match IB-rt-5's pre-edit
baseline exactly. This cell edited nothing in the guard, so the red is pre-existing (row
`IRPT_BCKEND-S29`, not re-filed). The two files in `.tools/tests/` pass 4/4 and 9/9.

### (c) SERVED -- FAIL, 3 of 8 closure members named
```
ETag 7791109bada2dbb44c5ac742b65671ee  VersionId AxKzxFHuxAP7TTIJsmkxtWZxxgEgVJDC  42026 bytes
md5(downloaded bytes) == ETag: True   sha256 = 3441f09d6fafe077a64254c76d9f3ce300ce882c5f3dcbceaa0ba9b32aaf7159
served members (4): directory_runner.py, holdings_snapshot.py, ids.py, trading_calendar.py
source-repo-paths names 3 of 8 closure members
stamps equal to the repo at this tip: 4 of 4 declared
```
Every stamp matches. The object is correct for what it declares and incomplete for what the runner
needs.

### (d) HOST TAR, (e) HOST IMPORT -- NOT-EVALUATED
The host `i-02448edb624a7a7cf` was **stopped**. The mdpf daily chain started it at 13:00Z and it
shut itself down afterwards. Nothing was re-minted, so the object the host would unpack is the one
arm (c) already read byte for byte, and SourceSet construction depends only on whether each file
exists (`directory_runner.py:217-218`). I did not use the face's one admitted `StartInstances` to
measure an object that had not changed. The battery **never** starts or stops the host. When the
host is up it runs both placements read-only under `/tmp` in one SSM command. IB-rtc-3, or the
cell that replaces it, is the right place to use the start.

### (f) NEG CONTROL -- FAIL (NO-OP)
The face's premise does not hold: IB-rt-5's ETag `cd188f6e...` carried **2** members, not 3 (row
`S60`). The key has 19 versions. The 3-member tarball is `a35420ac...` (IB-rt-6, 09-12). The object
served when this cell began is `7791109b...` with 4 members, uploaded five times since 09-15 (three
distinct objects) by pushes that touched member files. The arm compares against that pre-cell object and reads **NO-OP**.

---

## The two disclosures (not graded; they are the evidence for rows S62 and S59)

**(g) ROUTING.** Shown above: 3 of 3 undeclared `runner_common.py` have a live, current loose leg,
and 3 of 3 would be routed out of it. The probe ran the guard's `bundle_for_member` against a deep
copy of `CODE_TREES` and restored the original. `git diff --stat .tools/safe_deploy_core.py` is empty.

**(h) PLACEMENT.** One payload, built by the guard's own `build_bundle_payload`, with 9 members:
the 4 declared plus the 5 missing, each missing one named by its repo path.
```
DECLARED placement (unpack rc=0): IMPORT-OK 3 of 3 ['49financial', 'cottonwood', 'inflection']
DEPLOYED placement (unpack rc=1): IMPORT-OK 0 of 3 []
  IMPORT-FAIL 49financial RuntimeError: REFUSE: identity runner module absent: <tmp>\e2root\E2\data\assets\scripts\gold\runners_49f\runner_common.py
  (cottonwood, inflection the same)
dot-dot probe (GNU tar, local): rc=2  tar: ../runners_inf/runner_common.py: Member name contains '..'
```
The DEPLOYED run uses `refresh.runner_script`'s own lines, cut before the build, with only the
`aws s3 cp` swapped for a local copy. Its rc=1 comes from the last line of the cut, a
`[ -f $R/DirectoryEntry.schema.json ] && mv` test, and does not mean the extract failed: tar listed
every member. The contract **can** be placed today under a flat member name, because the dispatch
already moves a flat `DirectoryEntry.schema.json`. The registry and the three `runner_common.py`
cannot be placed by any member name.

---

## R32-AC2 -- the facts, for `3.0.0_SA_CVO` (no verdict)

1. **Beyond W2-S51's list: nothing to add, and one path to remove.** `firm-config.mjs` is a dead
   reference at this tip. The closure is the runner plus 7 files: `lib/trading_calendar.py`,
   `_ids/ids.py`, `_contracts/DirectoryEntry.schema.json`, `data/firm_registry.json`, and the three
   `runner_common.py`. The three modules import only stdlib, `boto3` and `pandas`, so the
   transitive walk ends there.
2. **Cross-firm.** The three modules are *code*. At import they bind only constants: bucket and
   prefix names (`opal-data-49financial`, `schwab/08335338`, `opal-data-inf`,
   `blackdiamond/cottonwood/silver/`) and a lazy `_s3 = None`. A shared bundle in `opal-data-mdpf`
   carrying all three would widen what the mdpf host can **import**, not what it can **read**.
   Reads stay bound by the host role and by `opal-data-49financial`'s `DenyForeignFirmPrincipals`
   (the 49F arm stays BLOCKED by that control, per decomposition v0.3 s.R3.1). The cross-firm
   effect the bound should hear about is on the **deploy plane** (row `S62`): one shared DS-lane
   artifact would become the deploy path for three firms' own runner code and freeze their
   per-firm legs. Of the three fixes in S62, option (2) (fetch each firm's served module at build
   time) would make the mdpf principal read `opal-data-49financial/_code/`.
3. **The 49 Financial import read no 49 Financial data.** Locally, `Firm49F()` instantiated
   IMPORT-OK, and the audit hook recorded **0** network events (socket connect / getaddrinfo /
   http connect) across the import and all three SourceSet constructions. Its positive control, a
   loopback resolve, moved the counter, so the zero is a real measurement. `SourceSet.__init__`
   only calls `_import_runner` (`directory_runner.py:237-239`). Not measured on the host (see d/e).

---

## What this cell did NOT do, and why

- **No `CODE_TREES` edit, no mint, no ledger entry, no sentinel.** The reasons are above. Once the
  shape is decided, the declaration and re-mint are each one command, and the battery re-derives
  everything, so it will grade that act unchanged.
- **No `StartInstances`**, and never a stop.
- **No edit to `refresh.py`** (outside `<paths>`), to any runner, or to the dead constant.
- **Row ids:** the face asks for `IRPT_BCKEND-D-S<k>`, which the ratified schema refuses (row
  `S30`, round 2). These rows use the seat form `S58`-`S60` and `S62`, continuing from the channel's measured
  maximum of `S56` on both this branch and `CLOUD` (`662d53b793`).
- **The channel holds two json fences, not one:** the CVO's `S56` sits in a second fence. These
  rows are appended inside the **first** array, as the face instructs. The file is written LF.

## Rows filed (4)

| id | class | one line |
|---|---|---|
| `IRPT_BCKEND-S62` | BLOCKING | declaring the three `runner_common.py` would freeze three live per-firm deploy legs |
| `IRPT_BCKEND-S58` | BLOCKING | the registry and the contract are outside the admitted globs (the face's own rule) |
| `IRPT_BCKEND-S59` | BLOCKING | the deployed dispatch cannot place the closure, so IB-rtc-3 cannot land inf/cot as cut |
| `IRPT_BCKEND-S60` | OBSERVATION | the negative control's prior is 2 members, not 3; graded against the pre-cell object |

## Row id re-labelled before the drain -- read this before chasing a citation

This seat's first row was written as `IRPT_BCKEND-S57`. It is now **`IRPT_BCKEND-S62`**, because
`CLOUD` landed `2.0.0_SA_COO~B`'s own `IRPT_BCKEND-S57` (the round-3 intake row) at `e83de1a17e`
after this branch was cut at `e9dc18f302`. The drain's row gate refuses a duplicate id across the
merged index. The issuer asked for the change (msg 97786), and this seat confirmed the collision
itself at `CLOUD` `d5d102aee4` before making it: `S57` is `surfaced_by: 2.0.0_SA_COO~B` there,
`S58`-`S62` were free, and `S61` is reserved for the issuer. `S58`, `S59` and `S60` keep their ids.
Content is unchanged; only the id and the references to it moved.

The two earlier commit messages on this branch (`802cee5eab`, `39caa17744`) name the OLD id.
Commit messages cannot be changed, so a citation of `IRPT_BCKEND-S57` taken from those messages
now points at the ISSUER's row, not this one.

---
---

# AMENDMENT 1 (R-45) -- 2026-09-18, re-handed pass

**Branch:** `wk-irpt_bckend-3-ds2` | **worktree:** `/c/tmp/wk-irpt-3-ds2` | **cut:** `65a95ae8db`
**Invocation:** `timeout 1200 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.4.0_DS_ClientPlatform~X/battery_ib_rtc_2.py`
**Result:** `rc=0`, **5 of 5 graded arms PASS**, final line `IBR32-CLOSURE-MINTED-AND-IMPORTS-ON-HOST`.

The first pass above measured the gap and stopped. R-45 (`1.0.0_SA_CTO` @57bc083d45) ruled
the shape: a member-level DISTRIBUTION flag, members named by repo path, and a consistency
check across both legs with a one-leg mutant. This pass builds and grades that shape.

## What changed in the world

| key | before | after |
|---|---|---|
| `s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz` | ETag `7791109b...`, v `AxKzxFHu...`, 4 flat members | ETag `0020e7afc760b827a6adb7c0ad538903`, v `1jPgGCGLP.uGY5RpMlMJTrKvKzvyYf7O`, **9 members named by repo path**, sha256 `86e3a9b0...` |
| `s3://opal-data-cot/code/gold/runners_cot/runner_common.py` | ETag `384920cf...`, v `vrG96E7l...` | ETag `d88a5939e5adeb81a40de26f3e051868`, v `bobsNlnm...`. **Comment-only**: the file now names its own two legs |

Nothing else moved. Every change went through `.tools/safe-deploy.sh`; there was no bare
`aws s3 cp`. The 49F and INF loose keys were read and not written. The host
`i-02448edb624a7a7cf` was started once (it was stopped; `stopped -> pending` at 04:11:09Z) and
was never stopped. The daily chain owns its shutdown.

## Commits, in the order bound 4 requires

| commit | what |
|---|---|
| `949dd1a4f5` | change-management entry `irpt-bckend-rtc2-distribution-mint` OPENED, sentinel committed **before any act** |
| `0f86089471` | L1a: the guard's flag, the factored routing, and the 9-member declaration |
| `6be251a0e3` | L1b: the flag's own tests (lane override, see below) |
| `d3508ff714` | L3: the REAL commit to one distribution member (COT `runner_common.py`, comment block) |
| `68e3b02bcb` | ledger CLOSED, 6 of 6 legs proven, sentinel removed, **before the grading reads** |

## The five arms

**(a) FLAG TESTS -- 9 of 9, and no earlier pass regressed.** The flag's own battery passes 9 of 9.
It covers both legs for 3 of 3 flagged members, bundle-only for an unflagged member, loose-only for
a non-member, and bundle-only for a config member. It checks that the declared flag set is exactly
the three runner modules, each with a real per-file target, and that no flag anywhere sits on a file
without a loose leg. It includes a MUTANT: remove the flag on a copy and the member freezes again.
The guard's four test files show the SAME named failures as at `65a95ae8db`: `test_code_trees_invariant`
3/18 and `test_safe_deploy` 7/14, the S29 class; the other two still pass 4/4 and 9/9. **The whole
`.tools` suite, run file by file before and after (logs committed beside this file, each headed by
its tip):** 69 files before with 59 passing; 70 after with 61 passing; **0 of the 59 regressed**.
The new flag test is added, and `test_comp_pulse_battery` went from fail to pass (unrelated; its
input is a time-dependent danger map). The nine files that fail after were all failing before, and
are named in the logs.

**(b) DECLARED -- 8 of 8, 3 flagged.** The closure was re-derived at this tip by the static AST
sweep and the dynamic open/import probe, and it matches the first pass's 8 exactly (added none,
removed none). All 8 are declared and named by repo path. `holdings_snapshot.py` is the ninth member
(the sibling runner). The three DISTRIBUTION members are the three per-firm `runner_common.py`.

**(c) CONSISTENCY -- both legs after a real commit, and the one-leg mutant FAILS.**
```
REAL commit d3508ff714 touches ['data/cot/scripts/gold/runners_cot/runner_common.py'] (md5 384920cf -> d88a5939)
THE ACT'S RESULT: CONSISTENCY CONSISTENT: 3 of 3 DISTRIBUTION members agree on both legs
  COT  loose v bobsNlnm... ETag d88a5939... == blob md5 ; bundle member 80a7d89e... == blob sha256
the deploy's OWN mint (L4, v DVjQwk75...): CONSISTENT
MUTANT v MpTRS5v.gk_0rrd7fkGz8Fp7z281noBB: CONSISTENCY DIVERGED: 2 of 3
  COT  loose d88a5939 == blob (current) ; bundle member 63110bfe != blob 80a7d89e (stale)
loose key: 2 versions in history; written inside the mutant window [04:05:30Z, 04:08:05Z]: 0
```
**What the mutant advanced, and on which plane:** the BUNDLE leg only. The plane is the production
bundle key, through the guard's own `--mint-bundle`, run from a detached worktree at the pre-commit
tree `6be251a0e3` (removed afterwards). The loose leg gained no version in that window. A restore
mint from the tip brought the bundle back to the L4 bytes (same md5 `0020e7af...`; deterministic
payload), and the check read CONSISTENT again. The arm grades **recorded VersionIds and the commit
hash**, never "current" or "HEAD", so a grader after the drain re-grades these exact objects. The
living state is printed beside it as INFO.

**(d) RE-MINT -- the minted version, 8 of 8 named, and it DIFFERS from the pre-cell object.**
`source-repo-paths` names 8 of 8 closure members, and all 9 stamps equal their member's bytes.
Negative control: `7791109b` (4 members) versus `0020e7af` (9 members) DIFFERS. Seven of 9 members
equal their git blob byte for byte. **The two JSON members do not**: they carry CR bytes because
the packer reads the worktree on this autocrlf box (row `IRPT_BCKEND-S63`; no consumer breaks,
since `json.loads` ignores CR, but the bundle's identity depends on the device).

**(e) HOST -- 8 of 8 placed at repo shape, IMPORT-OK 3 of 3, 0 network events.**
```
SSM 15294ea9-696d-4ef9-86b7-2a2db341dc84 Success rc=0, caller mdpf-daily-runner-ec2-role
host sha256 86e3a9b0... == the MINTED version's sha256
tar -tzf: 9 members; extracted at ONE /tmp root: 8 of 8 closure files at their repo paths
IMPORT-OK 49financial /tmp/.../W/data/assets/scripts/gold/runners_49f/runner_common.py
IMPORT-OK cottonwood  /tmp/.../W/data/cot/scripts/gold/runners_cot/runner_common.py
IMPORT-OK inflection  /tmp/.../W/data/inf/scripts/gold/runners_inf/runner_common.py
NET-EVENTS 0 ; NET-POSITIVE-CONTROL True
```
The host role holds `s3:GetObject` on the key but **not `s3:GetObjectVersion`**. A pinned
`--version-id` fetch was AccessDenied (SSM `cde13229...`, a dry run of this battery). So the host
fetches the key unversioned, as the dispatch does, and the arm binds the object to the minted
version by content: host sha256 == minted sha256, or the arm fails.

## Answers to the face's "state which"

- **Member names:** ALL NINE are named by repo path, **including the four that were flat**
  (`directory_runner.py`, `holdings_snapshot.py`, `ids.py`, `trading_calendar.py`). Under R-45's
  unpack (extract at `$W` by member name), a flat name lands at `$W/<name>`, where
  `directory_runner` does not derive, so none of the four could keep its name.
- **The dispatch as deployed, until IB-rtc-3 lands its unpack:** `refresh.runner_script`
  extracts into the runner's own directory and looks for `$R/directory_runner.py`. With repo-path
  names, the runner now sits at `$R/data/assets/.../directory_runner.py`, so a 09:00 ET fire's
  build fails at "file not found" instead of later, at the missing closure. It failed before this
  mint as well (rows S59, W2-S51); the failure point moves earlier and the outcome is the same
  (BUILD_ENDED_UNSUCCESSFUL). IB-rtc-3 is the cell that closes it.

## Four things the gates made me do, each on the record

1. **The naming gate refused the first stamp-key names** (`runner-common-49f-sha256` and the like:
   "NEW hand-kept carrier", LGIC_ENFORCE DEC-6). The keys are now numbered `runner-common-1/2/3`
   in sorted repo-path order, with the mapping in a comment. I did not import the naming registry
   into the deploy guard to spell the token through `lookup()`: every deploy would then depend on
   the registry loading, for the sake of a key name.
2. **The lane gate refused the flag's test file** (`.tools/tests/` is TOOL_BATTERIES). The
   order's `<paths>` grants it, but the validator honours a `<paths>` grant only for worker
   serials. It landed under the audited `GIT_COMMIT_AUTHOR_OVERRIDE=TOOL_BATTERIES`, one lane and
   one file (row `IRPT_BCKEND-S64`).
3. **The halt gate listed 7 routine messages** from the BASE serial's inbox, 17-21 days old: a
   closed merge window and relays of an old revert incident. None is STOP-class. I reviewed them
   and passed each safe-deploy call with `HALT_ACK=1`. I did not drain another serial's inbox.
4. **The row-id form:** the face again asks for `IRPT_BCKEND-D-S<k>`, which the schema refuses
   (row S30). These rows use the seat form from the measured maximum S62, which is the same on
   this branch and on CLOUD `1ca5067f6e`.

## R32-AC2 -- facts for `3.0.0_SA_CVO` (no verdict)

- **The flag's shape:** it is the guard's own idiom, not a second mechanism. It is one key on the
  member spec, read by `is_distribution_spec()` inside the SAME X-iii loop, which was factored
  unchanged into `route_bundle_members()` so the tests can run it without S3. Both legs are the
  existing `mint_bundle()` and `deploy_file()`, and each verifies its own bytes as before. The
  guard does NOT itself compare the two legs after a deploy. That cross-leg comparison lives in
  `consistency_ib_rtc_2.py`, beside this record. Whether the guard should run it on every
  distribution deploy is a question this cell leaves open.
- **What the mutant advanced:** the bundle leg only, on the production bundle key, through the
  guard's own mint from a stale tree. The COT loose key's version history shows no write in the
  window.
- **Did a firm's served module move by anything other than the guard's own routing during (c)?**
  No. The COT loose key moved exactly once, via `safe-deploy.sh --commit-range`
  (`DEPLOYED [cot] ...`, `VERIFY OK comp-pipescript`). The 49F and INF loose keys kept their
  VersionIds (`jnnxQWbV...`, `z_WDDmx6...`) throughout. The bundle moved only through the guard's
  own mint: explicit, deploy-routed, mutant, restore.
- **The 49 Financial module on the host, without 49 Financial data:** `Firm49F()` instantiated
  IMPORT-OK from the repo-shaped extract. The audit hook recorded **0** network events across the
  import and all three instantiations, and a loopback positive control in the same process proved
  the counter fires. Module level in `runner_common.py` binds constants and a lazy client; no
  object in `opal-data-49financial` was read. This proves the code is importable at repo shape
  under the host's own python 3.9 and dependencies. It says nothing about whether a BUILD can read
  49F's dimensions: that is R-44's principal, which is IB-rtc-6's subject.

## Rows filed in this pass (2)

| id | class | one line |
|---|---|---|
| `IRPT_BCKEND-S63` | OBSERVATION | the bundle packer reads the worktree while the loose leg serves the blob; the JSON members carry CRLF on an autocrlf box |
| `IRPT_BCKEND-S64` | OBSERVATION | a task order's `<paths>` grant reaches the lane gate only for a `0.9.0_WK_*` worker, not the seat it is handed to |
