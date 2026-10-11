# MP-r-2 PRE-ACT RECORD -- the CP2 gateway release, re-cut on the live base after MX-r-9

**Cell:** `MP-r-2` (NFRA_MCPORTAL, workstream CP2, round 1) -- `<risk>WORLD</risk>`
**Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-r-2.cp2-gateway-release.md`
**Applier:** `0.7.0_AE_CloudOps~MP` **Issuer:** `2.0.0_SA_COO~MP`
**Release branch:** `rel-nfra-mcportal-cp2-v2` @ `1db8382aac`, worktree `C:/tmp/mp-r2-rel2`
**Ledger slug:** `nfra-mcportal-cp2-release`

The AMENDMENT 5 measurement history (12 of 12 cold samples, the Z-S32 driver defect, the toolchain hold)
lives in the EARLIER record on branch `wk-mcportal-cp2-r2` @ `73547dcfd1`. This file is the record of the
act itself, re-cut on a new base after MX-r-9's ledger closed. It does not restate that history.

---

## 1. The live base, read from the HOST by md5 -- NOT from a label

The issuer's ruling (msg 33000, relayed 33004) is that the artifact's `-latest` label was MISLABELLED and
the base must come from the host by content. So it did.

Over SSM, md5 of every non-`__pycache__` file under `/opt/opal-gateway/app`: **94 files**.

| compared against | EQUAL | DIFFERENT | git-only | host-only |
|---|---|---|---|---|
| `d3c31e972e` (candidate) | **94** | **0** | 0 | 0 |
| `1e32562729` (NEGATIVE CONTROL) | 92 | **2** | 0 | 0 |

The negative control's two differing files are exactly MX-r-9's two shipped files,
`app/integrations/opal_discover/integration.py` and `app/refs/DATA_CATALOG.yaml`. **So the instrument
discriminates** -- it is not matching everything -- and the live base is `d3c31e972e` BY BYTES, which is
also what `EC2_MANIFEST.json` now claims. The manifest was read, never taken: had the two disagreed, the
bytes would have won.

Service at the read: `active`, MainPID **915778**, `/health` **200**.

## 2. The payload, and why each file was taken the way it was

Cut: `git worktree add --no-checkout --detach ... d3c31e972e`, then a NO-CONE sparse list
(`/*`, `!/data/*`, `/data/transcripts/`) per row Z-W5-S2.

> **A trap worth banking:** the first sparse write went through `git sparse-checkout set --no-cone
> '/data/transcripts/'` and MSYS rewrote the leading-slash pattern to
> `C:/Program Files/Git/data/transcripts/`. The re-include silently never applied, and
> `meeting_allowlist.json` -- which `deploy-to-ec2.sh` REFUSES without -- was absent while
> `git sparse-checkout list` happily printed the mangled pattern. Writing the pattern file directly at
> `$(git rev-parse --git-dir)/info/sparse-checkout` is the fix; in a linked worktree `.git` is a FILE, so
> the naive `.git/info/...` path fails with "Not a directory".

Files taken with `git checkout <commit> -- <paths>` rather than cherry-pick, because these are trunk
commits carrying `org/` bookkeeping the off-trunk release base predates (the earlier cut conflicted `DU`
on another seat's task-order file). **Every file verified byte-for-byte against its source commit: 9
EQUAL, 0 DIFFERENT, denominator 9.**

| source commit | cell | files |
|---|---|---|
| `638b8ae057` | MP-o-1 | `app/admin_fabric_overlap.py`, `app/refs/overlap_rules.json`, `tests/test_admin_fabric_overlap.py` |
| `604ea0e089` | MP-s-1 | `app/admin_fabric_gitstate.py`, `tests/test_admin_fabric_gitstate.py` |
| `5bdf8e1a3e` | MP-k-1 | `app/admin_fabric_calls.py`, `tests/test_admin_fabric_calls.py` |
| `354d58bc30` | step 0 / AMENDMENT 2 | `app/admin_api.py` |
| `ea58e3662d` | AMENDMENT 5 | `app/admin_fabric.py` |

**The two PRE-EXISTING files were diffed against the base before being taken wholesale**, because their
source commits sit on `box/sitez` and the base does not -- taking them blind could have imported an
unreleased trunk change, and for a file already present in the base the census would NOT have caught it:

- `app/admin_api.py`, base -> `354d58bc30`: **7 insertions, 0 deletions** -- exactly the 3 imports and the
  4 route lines, nothing else.
- `app/admin_fabric.py`, base -> `ea58e3662d`: **6 insertions, 2 deletions** -- exactly AMENDMENT 5's
  `FETCH_THREADS` 8 -> 32 and the `max_pool_connections` config, nothing else.

### Census (the order's literal form)

`git diff --stat d3c31e972e HEAD -- infra/aws/ec2/opal-gateway`: **9 files, 1587 insertions, 2 deletions.
Files outside the CP2 set: 0.** The only path changed outside the gateway dir is
`infra/aws/ec2/EC2_MANIFEST.json`, this order's own `<paths>` entry, set to
`mcportal_commit: bc37107` (MP-p-2, a descendant of `d60b4e0`) so `deploy-to-ec2.sh` builds the bundle
from it.

### Bun cache pre-check

`ops/bun_cache_precheck.py` against `bc37107`'s own lockfile (30,903 bytes, read with
`git -C mcportal show bc37107:bun.lock`): **77 of 77 present, rc=0. No package is fetched.**

## 3. The load condition, re-measured at the act -- PASS, and the denominator is the story

Driver: one handler per interpreter, on the host, host venv, instance role, bundle pulled from S3 per
Rule 12, scratch removed by a trap. SSM `517db393-f6c9-4e11-9d49-13086399f984`, Status=Success. The
bundle's three key modules were md5-checked on the host against the release tree before timing, so the
probe timed the BUILD INPUT and not some other copy.

Row Z-S32's constraint is honoured: **coldness is per-CACHE, not per-process** -- `overlap` reads through
`admin_fabric._BODY_CACHE`, a module-level dict -- so the driver asserts the relevant cache is empty and
prints the count it asserted on. `cache_at_start` was **0 on all 8 samples**; a non-empty cache would have
voided the sample (rc=3) rather than reported a fast one.

| handler | samples (s) | max | bar | records scanned |
|---|---|---|---|---|
| `admin_fabric._compute(6)` | 0.730 / 0.690 / 0.690 | **0.730** | 30 s | 85 |
| `admin_fabric_overlap._compute(6)` | 1.087 / 0.813 / 0.821 | **1.087** | 30 s | 85 |
| `admin_fabric_gitstate._compute()` | 10.586 | **10.586** | 30 s | n/a (1,640 cache entries) |
| `admin_fabric_calls._compute('open')` | 0.636 | **0.636** | 30 s | n/a |

**All 8 samples at or under 30 s. The bar is MET and no sample STOPS the cell.**

### The honest reading of those times

`records_scanned` is **85**, against **4,543-4,699** in every earlier measurement of this cell. A number
that good deserves suspicion, so the population was measured directly rather than inferred:

| partition | objects (auto-paginated, counted client-side) |
|---|---|
| `fabric/activity/v1/dt=2026-10-10/` | **87** |
| `fabric/activity/v1/dt=2026-10-09/` | **4,972** |
| `fabric/activity/v1/dt=2026-10-08/` | 2,250 |

So the probe reads the right source and the fabric genuinely wrote ~57x fewer activity records today;
`_list_keys` lists by whole-DAY partition, so `records_scanned` is a day's object count, not six hours'.
The store is live (newest key written 2026-10-10T22:45:46Z, i.e. during the measurement).

**Therefore this sample alone does NOT retire Z-S27's trend, and is not offered as if it did.** What
bounds the inference is a MECHANISM plus a second measurement, not this denominator: the SAME remedied
bytes were measured ~1.5 h earlier at **4,695-4,699 records** and read **13.828 s worst of 12 samples**.
The bar is therefore met at BOTH ends of the observed population range -- 85 records at 1.087 s and 4,699
records at 13.828 s -- which is the claim, and the only claim, the evidence supports.

**One handler moved the wrong way and is flagged, not buried:** `gitstate` read **10.586 s** today against
**3.854 s** yesterday, a 2.7x INCREASE while every activity-store handler got ~19x faster. Its population
is git history, which grows monotonically and does not drain overnight like a rolling window. It is well
inside the bar now; it is the handler whose margin will erode. Filed for the enrichment list.

## 4. Rollback, proven BEFORE the act

`s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-d3c31e972e.tar.gz` --
**525,792 bytes, ETag `8e81c94230a54ef80a88d03950e93c81`, `Metadata.git-ref`
`d3c31e972e8c6fdb26dda98a1d9ff55ced0ced89`.** The VERSIONED key, never `-latest`, which this act
overwrites.

Downloaded (525,792 bytes read back, equal to `head-object`) and extracted: 125 entries, top level
`app dashboard deploy identity_tool_allowlist.txt requirements.txt`, including **3 dashboard files**.
Its `app/` contents were then compared THREE ways:

| comparison | common | EQUAL | DIFFERENT |
|---|---|---|---|
| ARTIFACT vs GIT at `d3c31e972e` | 94 | **94** | 0 |
| ARTIFACT vs the RUNNING HOST | 94 | **94** | 0 |
| GIT at `d3c31e972e` vs the RUNNING HOST | 94 | **94** | 0 |

No file on only one side in any pairing. **So the rollback artifact IS the live base** -- byte-identical
to both the base commit and the bytes now serving -- rather than merely an object named after it. That is
a stronger proof than a from-scratch rebuild, which would only show that something reproducible exists.

A clean rollback tree is **pre-staged** so no build happens at incident time: `C:/tmp/mp-r2-rb`, detached
at `d3c31e972e`, 0 uncommitted lines, same sparse list, `deploy-to-ec2.sh` and `meeting_allowlist.json`
both present, and its manifest pins `mcportal_commit: d60b4e0` -- the BASE's bundle, which is what a
rollback must rebuild.

**THE ROLLBACK COMMAND, to run from `C:/tmp/mp-r2-rb`:**

```
DEPLOY_BASE_REF=<the release commit this act makes live> \
  bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh
```

## 5. The MCP tool surface BEFORE the act

**42 names**, read from the LIVE registry (`app.tools.mcp._tool_manager.list_tools()`), rc=0, names
captured in full for the after-comparison. Count AND names are recorded, because two different surfaces
can share a count and a count-only compare would pass an equal-sized swap.

**What this instrument measures, stated so nobody over-reads it:** it imports the app in a FRESH
interpreter and lists what is registered at import. MP-x-4's record reads **66** for the same concept.
That difference is an INSTRUMENT difference, not something this act caused -- 42 is the native tool set
(`app/tools.py`, which the gateway's own `_graph_using_tools` docstring also calls "all 42"), and the
larger figure includes integration tools that a fresh import does not register. The comparison that
matters is before-vs-after **through this same reader**, and the expectation is 42 -> 42 with an identical
name list, because this release adds HTTP routes and no MCP tool.

> Probe defect caught and fixed before it reached a number: the first read returned
> `ModuleNotFoundError: No module named 'app'` despite `cd /opt/opal-gateway`, because Python puts the
> SCRIPT's directory on `sys.path[0]`, not the cwd -- the same shape the issuer hit on its first AC3 dry
> run. Fixed with `PYTHONPATH=/opt/opal-gateway`. An unreadable registry prints ERROR and exits 1; it is
> never reported as an empty surface.

## 6. What the act will do, in order

1. `deploy_ledger.py open --slug nfra-mcportal-cp2-release` with four legs: bundle build; release build
   and upload; SSM pull and restart; manifest record. ONE pointer line to this file in the entry
   (AMENDMENT 4: the tool regenerates the entry and drops appended prose, rows Z-S24/Z-S25).
2. Commit the entry AND its sentinel `org/critical_paths/.open_deploys/nfra-mcportal-cp2-release.json`.
3. ACT from the release tree with ITS scripts:
   `bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`,
   `DEPLOY_BASE_REF=d3c31e972e8c6fdb26dda98a1d9ff55ced0ced89`. The stale-base guard must read the live ref
   unchanged at both reads.
4. Poll `/health` immediately after the restart. **Not 200 within 90 seconds -> run the rollback command
   in section 4 AT ONCE**, close the entry as rolled back, stop.
5. Tool surface AFTER, same reader; the name difference must be EMPTY.
6. Manifest record on the release branch: `deployed_commit` = the release commit,
   `previous_deployed_commit` = `d3c31e972e...`, `mcportal_commit` = `bc37107`, plus a `release_note`.
7. Close every leg with its proof and commit the close BEFORE the AC reads.

**BOUNDS held throughout:** no Terraform, no ALB, no host, role or secret change; `safe-ec2-deploy.sh`
read and never edited; no handler edited beyond AMENDMENT 5's two lines; and **no live POST to
`/api/admin/fabric/calls/close`** -- the one real close is Andrew's, in MP-q-1.
