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
| `data/assets/scripts/gold/runners_49f/runner_common.py` | a bundle member is routed **out of its own per-file deploy leg**; this file is served today at `s3://opal-data-49financial/_code/runner_common.py` | `IRPT_BCKEND-S57` |
| `data/inf/scripts/gold/runners_inf/runner_common.py` | same: served at `s3://opal-data-inf/code/gold/runners_inf/runner_common.py` | `S57` |
| `data/cot/scripts/gold/runners_cot/runner_common.py` | same: served at `s3://opal-data-cot/code/gold/runners_cot/runner_common.py` | `S57` |
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
is not mine to make. Row `S57` gives three possible fixes and this seat's recommendation.

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

## The two disclosures (not graded; they are the evidence for rows S57 and S59)

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
   effect the bound should hear about is on the **deploy plane** (row `S57`): one shared DS-lane
   artifact would become the deploy path for three firms' own runner code and freeze their
   per-firm legs. Of the three fixes in S57, option (2) (fetch each firm's served module at build
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
  `S30`, round 2). These rows use the seat form `S57`-`S60`, continuing from the channel's measured
  maximum of `S56` on both this branch and `CLOUD` (`662d53b793`).
- **The channel holds two json fences, not one:** the CVO's `S56` sits in a second fence. These
  rows are appended inside the **first** array, as the face instructs. The file is written LF.

## Rows filed (4)

| id | class | one line |
|---|---|---|
| `IRPT_BCKEND-S57` | BLOCKING | declaring the three `runner_common.py` would freeze three live per-firm deploy legs |
| `IRPT_BCKEND-S58` | BLOCKING | the registry and the contract are outside the admitted globs (the face's own rule) |
| `IRPT_BCKEND-S59` | BLOCKING | the deployed dispatch cannot place the closure, so IB-rtc-3 cannot land inf/cot as cut |
| `IRPT_BCKEND-S60` | OBSERVATION | the negative control's prior is 2 members, not 3; graded against the pre-cell object |
