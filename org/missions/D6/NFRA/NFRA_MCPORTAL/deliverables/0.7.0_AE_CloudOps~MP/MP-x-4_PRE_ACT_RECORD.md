# MP-x-4 PRE-ACT RECORD -- the durable copy

**Seat:** `0.7.0_AE_CloudOps~MP`  |  **Entry:** `nfra-mcportal-r5-control-plane-release`

This lives HERE, not only in the ledger entry, because `deploy_ledger.py hold` (and, by the same
mechanism, `close-leg`/`close`) REGENERATES the entry from its structured state and silently discards
any prose appended to the file. Measured: the hold at `b8fc617e2e` removed 115 lines of this record
from the entry and returned rc=0 with `OK: ... -> HELD-PRE-APPLY`. Recovered from `ca9b6c05f0`.
Surprise row: `NFRA_MCPORTAL-Z-S24`. The entry keeps only a short pointer to this file.

---

## PRE-ACT RECORD (MP-x-4 steps 1-3, all measured BEFORE the act)

**This order's path:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-x-4.control-plane-release.md`
(`<status>pending</status>`, round 5, `<risk>WORLD</risk>`, issued by `2.0.0_SA_COO~MP`, GO msg 32756).

**Release tree.** `rel-nfra-mcportal-r5-control-plane` at `C:/tmp/mp-x4-rel`, cut from the LIVE
`deployed_commit` `91811b648ab119e73e22f8d401dd09f45b8ab19b` (NFRA_OPLGTW r29), read from
`infra/aws/ec2/EC2_MANIFEST.json` at the act and NOT taken from the GO message. MP-x-1 `06bfb80b54`
cherry-picked (`cb41cf1c8f`); `mcportal_commit` set to `d60b4e0` (`d1bc9dfbe3`, one line changed,
measured 1 insertion / 1 deletion). The release branch stays local and unmerged, as every prior gateway
release branch has; this trunk branch `wk-mcportal-r5-x4` carries the ledger and the manifest RECORD,
per the r29 precedent (`91811b648a` lives only on `rel-nfra-oplgtw-r29`; its ledger and manifest landed
on the trunk at `5f1400c4a2`).

**CENSUS (the order's STOP gate).** `git diff --stat 91811b648a HEAD -- infra/aws/ec2/opal-gateway`
names EXACTLY the four files MP-x-1 carries, and nothing else:

| file | change |
|---|---|
| `app/admin_fabric.py` | new, 175 lines |
| `app/refs/fabric_boxes.json` | new, 8 lines |
| `tests/test_admin_fabric.py` | new, 279 lines |
| `app/admin_api.py` | +2 |

4 files, 464 insertions. Files changed OUTSIDE `infra/aws/ec2/opal-gateway/`: **0**. The two lines in
`admin_api.py` are the one route line `Route("/fabric/boxes", admin_fabric.boxes, methods=["GET"])` plus
its required `from . import admin_fabric` import -- the order's "one route line", not a second behavior.

**bun cache pre-check.** `ops/bun_cache_precheck.py` against d60b4e0's own lockfile (30,903 bytes,
`lockfileVersion 1`, extracted with `git show d60b4e0:bun.lock`): **77 of 77, rc=0**. No package will be
fetched, so step 1's miss-STOP does not fire.

**COLD READ on the host (R-13's 30 s bar) -- FOUR independent samples, not one.** Measured over SSM under
the instance role `arn:aws:sts::313476888478:assumed-role/opal-gateway-role/i-07dccb1615503ac99`, running
the RELEASE's `app/admin_fabric.py` (plus its new `app/refs/fabric_boxes.json`) in a scratch copy of the
live `app/` package under the host venv `/opt/opal-gateway/.venv/bin/python`. Per CLAUDE.md Rule 12 the
driver went local -> S3 -> host pull; no Python was inlined into an SSM command and nothing was written on
the VM.

| sample | cold `_compute(6)` | records scanned | skipped |
|---|---|---|---|
| 1 | 16.767 s | 3141 | 0 |
| 2 | 15.336 s | 3154 | 0 |
| 3 | 13.964 s | 3154 | 0 |
| 4 | 13.615 s | 3154 | 0 |

n=4, min 13.615, max 16.767, mean 14.921, spread 3.152 s (23.2% of min). **Worst sample is 13.233 s under
the 30 s bar -- 1.79x headroom.** Warm reads 0.765-0.839 s. All 4 roster boxes reporting (dell2 611,
dell1 598, sitez 265, laptop 111), `unrostered` empty.

**No load change was made.** The order's remedy (narrow the default window 6 -> 2 hours, or warm the body
cache at boot) fires only above 30 s. It did not fire, so `app/admin_fabric.py` is deployed EXACTLY as
MP-x-1 wrote it and no re-run of `tests/test_admin_fabric.py` is owed.

Two honest notes on this figure. (i) The issuer's 04:2xZ reading was 21.3 s with 3,004 records -- ABOVE
every sample here despite scanning FEWER records, so that figure reflects a slower moment (S3 latency or
host load), not record-count scaling; four samples at the release time are what the order says counts.
(ii) The 6-hour window does grow with daytime commit volume: at ~3,150 records the mean is 14.9 s, so on a
linear read the bar would be reached near ~6,300 records in the window. That is headroom, not a defect, and
it is the figure a future enrichment should re-measure rather than assume.

**ROLLBACK, proven before the act.** The live base's own artifact is already in S3 and was CONTENT-verified,
which is a stronger instrument than a from-scratch rebuild (a rebuilt tarball would not be byte-comparable:
tar/gzip metadata and the bun build are not bit-reproducible, so a mismatch would prove nothing):

- `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-91811b648a.tar.gz`
- 514,461 bytes; ETag `3157ad0796dae6f9ad26dea7a1e46469`; `Metadata.git-ref` =
  `91811b648ab119e73e22f8d401dd09f45b8ab19b`, exactly the live `deployed_commit`; uploaded 2026-10-09T12:31:08Z
  by r29's own deploy.
- Downloaded and verified: local size 514,461 == S3, local md5 `3157ad0796dae6f9ad26dea7a1e46469` == the ETag.
- Contents are provably the PRE-RELEASE base: `app/admin_fabric.py` occurrences **0**,
  `app/refs/fabric_boxes.json` occurrences **0**, with positive control `app/admin_api.py` = 1 (so the
  archive is readable and the grep discriminates). Top level: `app`, `dashboard`, `deploy`,
  `identity_tool_allowlist.txt`, `requirements.txt`.

**Rollback command, per key.** Re-install the VERSIONED key, never `latest` -- this act overwrites
`opal-gateway-latest.tar.gz`, which right now is byte-identical to the base (same size, same ETag, same
git-ref) and will not be after the upload:

```
aws ssm send-command --instance-ids i-07dccb1615503ac99 --document-name AWS-RunShellScript \
  --region us-east-1 --parameters file://<params.json>   # params pull and install:
#   aws s3 cp s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-91811b648a.tar.gz \
#     /tmp/rb.tar.gz --region us-east-1
#   sudo -u ec2-user tar -xzf /tmp/rb.tar.gz -C /opt/opal-gateway
#   sudo systemctl restart opal-gateway && curl -fsS localhost:<port>/health
```

Blast radius, per the never-widen pair (CTO half R-13, COO half this issuance): the gateway's `/` bundle;
one new owner-gated route `GET /api/admin/fabric/boxes`; no `.env` key and no IAM. Terraform, the ALB, the
host, its role and its secrets are untouched; `safe-ec2-deploy.sh` is READ, never edited.

**HALT-GATE PRE-FLIGHT, measured from the release worktree (not assumed).** `halt-gate-check.sh` standalone
with `OPAL_AGENT_SERIAL=0.7.0_AE_CloudOps~MP`: **rc=0, admitted.** The GO warned that a sparse cone omitting
`org/tier2_senior/0.7.0_AE_CloudOps~MP` fails `SERIAL RESOLVES TO NO KNOWN AGENT` (rc=3). That remedy is
aimed at the wrong check for this serial: that LANE folder does not exist anywhere in the repo (0 paths under
it), yet the gate admits, because `halt_gate_validate_serial` matches the BASE by substring
(`*"$base"*`) against `org/tier*_*/*/` and this worktree carries 20 folders matching `0.7.0_AE_CloudOps`.
The second check, `lane-no-inbox`, reads the SHARED root's `org/mcp/inbox/0.7.0_AE_CloudOps/~MP`, which
exists. So the real requirement is "materialise at least one folder matching the BASE", which a no-cone
`org/` list satisfies -- not "create the lane folder", which would add a directory the tree does not have.
Nothing cited a HALTGT pass as evidence of not being halted (per /cloud-ops, a `~lane` serial is unhaltable
and no HALTGT pass is cited by anyone).

**MCP TOOL SURFACE, BEFORE.** 66 registered tool names, read on the host from the same registry the running
process builds (`app/server.py:507`, `mcp._tool_manager.list_tools()`), via the S3 -> host path, printing
names and the count only and never an env value (52 env keys loaded by name). `tool_count = 66`, rc=0,
MainPID 857046. This matches r28's recorded `tools 66 -> 66` baseline. The after-count and the name
difference are L4's proof.

**World state immediately before the act:** `app/admin_fabric.py` ABSENT from `/opt/opal-gateway/app`
(confirmed on three separate SSM runs), service `active`, MainPID 857046 unchanged across every pre-act
read, live tree mtime 1791513383 unchanged. Nothing has been deployed, uploaded or restarted by this cell.


---

# POST-ACT RECORD -- the release is LIVE

**Act:** 2026-10-09T16:12:05Z, `safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
from the release tree, with `DEPLOY_BASE_REF=c97232408d72bc649c92da7e4e711c0ebf0a3950`.
**Release commit:** `1e32562729495695c6addaed05f047e46090776f` over `c97232408d72bc649c92da7e4e711c0ebf0a3950`.

## The base changed under this cell, and that is the headline

The hold (issuer msg 32796) put OG-ap-4/OG-tl-1 ahead of this release; it landed, and the live base moved
`91811b648a` -> `c97232408d`. The recorded base was NOT reused. Everything downstream was re-done, not
carried:

| re-done | result |
|---|---|
| live `deployed_commit` re-read from `EC2_MANIFEST.json` | `c97232408d` (matches the GO, but read from the manifest, not taken from it) |
| release tree re-cut, old branch deleted | `rel-nfra-mcportal-r5-control-plane` @ `1e32562729` |
| census re-run vs the NEW base | 4 files, 464 insertions, **0 outside** `infra/aws/ec2/opal-gateway/` |
| cold read re-measured | 24.443 / 19.728 / 18.118 s (see below) |
| rollback target re-pointed | `opal-gateway-c97232408d.tar.gz`, not the old base's |
| tool surface BEFORE re-read | 66, name-for-name identical |

**Two things a stale-base deploy would have hit, both caught by the re-cut:**

1. **The deploy script itself changed.** OG-tl-1 modified `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
   (+13/-3) -- the script this cell RUNS -- adding a precondition that reads
   `data/transcripts/scripts/teams/meeting_allowlist.json` under `$WORKSPACE_ROOT` and REFUSES (exit 1,
   before any upload) on an unreadable file or a count other than 4. The cell's sparse list had no
   `data/`, so the deploy would have refused. Added `data/transcripts/`, then evaluated the script's own
   expression in the worktree: 4 ids, shape matches its regex, precondition PASSES. So "OG-ap-4 is
   env-only with no code change" is true of what SHIPS, and false of the deploy path.
2. **A stale-base deploy would have SILENTLY REVERTED OG-tl-1.** The old script hardcoded
   `TRANSCRIPT_MEETING_ALLOWLIST=` (EMPTY) in the rendered `.env`; the new one writes the 4 ids. The
   `.env` is RENDERED by the script, never merged, so building on `91811b648a` would have blanked an
   allowlist that landed 15 minutes earlier -- and this cell's never-widen blast radius says "no `.env`
   key", which would have been FALSE. Measured after the act: `.env`
   `TRANSCRIPT_MEETING_ALLOWLIST` still non-empty (grep count 1), and the script's own
   `ENV_KEYS_BEFORE`/`ENV_KEYS_AFTER` lists are identical at 52 keys.

## The act, and the guard that fired first

The FIRST invocation was REFUSED outright, before any upload:
`ERROR: REFUSED (no upload): DEPLOY_BASE_REF is required -- declare the commit this release was cut on`,
rc=1. That is the stale-base guard doing its job; nothing was built or uploaded. The act then ran with
the ref declared, rc=0, and the script's own read-back printed `OK: opal-gateway active`, `{"ok":true}`,
`OK: AS metadata serves`, `/mcp unauth -> 401 (expect 401)`.

**rc=0 is cited nowhere as proof.** Every figure below is an INDEPENDENT read taken after the act (SSM
command `a356c9bf-5140-48e0-8c6a-b205dcd47a3d`, Status=Success).

## Read-back

| read | value |
|---|---|
| `/health` | **200**, body `{"ok":true}` (well inside the order's 90 s bar, so the named rollback was NOT run) |
| new route, NO identity | **401**, `{"error":"no verified identity"}` -- owner-gated as designed |
| service | `active`; MainPID **862375 -> 864717**, so the restart demonstrably happened |
| deployed `app/admin_fabric.py` | md5 **`caa21f671e60c21e4b0a77c566c18149`** = the release module's md5 |
| `app/refs/fabric_boxes.json` | present (both files were ABSENT live on three separate pre-act reads) |
| `dashboard/index.html` | present -- the mcportal `d60b4e0` bundle shipped |
| MCP tool surface | **66 -> 66**, 0 added, 0 removed, **difference EMPTY**, name-for-name |

The md5 equality is the point of that row: it compares DEPLOYED BYTES to the BUILD INPUT, which is the
CLAUDE.md 22a CODE layer. A filename match would have proved nothing.

## Artifacts and rollback, measured AFTER the act

| key | bytes | ETag | `git-ref` |
|---|---|---|---|
| `opal-gateway-1e32562729.tar.gz` (uploaded) | 518165 | `b96315a523842ec46579b146c450faa9` | `1e32562729...` |
| `opal-gateway-latest.tar.gz` | 518165 | `b96315a523842ec46579b146c450faa9` | `1e32562729...` |
| `opal-gateway-c97232408d.tar.gz` (ROLLBACK) | 514278 | `16c5f801b546836ddf577696c69d597d` | `c97232408d...` |

`latest` MOVED to this release, exactly as predicted before the act -- which is why the rollback names
the VERSIONED key. The rollback target is **intact and distinct** after the act, so recovery is still
available and remains unexercised:

```
aws iam  # (no IAM in this act)
# rollback: pull the versioned artifact and restart, never latest
aws s3 cp s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-c97232408d.tar.gz \
  /tmp/rb.tar.gz --region us-east-1
sudo -u ec2-user tar -xzf /tmp/rb.tar.gz -C /opt/opal-gateway
sudo systemctl restart opal-gateway && curl -fsS localhost:8080/health
```

## Cold read on the shipped base, and why nothing was changed

3 samples before the cutover: **24.443 / 19.728 / 18.118 s** over 3788-3793 records, 0 skipped; warm
0.986-1.096 s. Worst-case margin **5.557 s** under R-13's 30 s bar, **1.23x** headroom. AC3's own
post-deploy read: **24.2 s over 4,040 records**.

**No load change was made.** The order's remedy (narrow the 6h window to 2h, or warm the body cache at
boot) fires only ABOVE 30 s. It did not fire, so `app/admin_fabric.py` shipped exactly as MP-x-1 wrote it
and no criterion was repaired. Narrowing it un-triggered would have changed product behaviour the order
does not authorise.

The margin is nevertheless TIGHTENING: 13.6-16.8 s over ~3,150 records at 14:0xZ, 18.1-24.4 s over
~3,790 at 15:5xZ, 24.2 s over 4,040 at 16:2xZ -- headroom 1.79x -> 1.23x in about two hours, ~5.5
ms/record, bar near ~5,460 records. Filed as row **`NFRA_MCPORTAL-Z-S27`** for the enrichment list. The
ALB idle timeout is 60 s and the 30 s bar is the order's half-margin, so at 24.4 s the page is ~2.5x from
a user-visible timeout and ~1.23x from the policy bar.

## Manifest record

Written BY HAND on the trunk branch `wk-mcportal-r5-x4` (6 fields; a guard refused to write unless the
trunk's pre-act `deployed_commit` read `c97232408d`): `deployed_commit=1e32562729`,
`previous_deployed_commit=c97232408d`, `mcportal_commit=d60b4e0`, `deployed_at`, `deployed_by`,
`release_note`.

**The deploy script's own auto-record is wrong and is not the authority.** On the release branch it set
`previous_deployed_commit=2c0f84966d` -- the value that tree's manifest carried from its own vintage, not
what was live. That branch is never merged (as every prior gateway release branch), so the trunk entry
above is authoritative, and the error is named in the `release_note`.

## Acceptance criteria

| criterion | result |
|---|---|
| **AC1** | **PASS** -- `entry files at HEAD=1; sentinel at HEAD=no; listed OPEN/HELD=0; SCAN DENOMINATOR: 20 of 20 sentinel(s) scanned` |
| **AC2** | **FAIL as run from this worktree** -- see below. REFUSED with its measurement, not repaired |
| **AC3** | **PASS** -- `status=Success; /health=200; /api/admin/fabric/boxes (no identity)=401; compute_s=24.2 reporting=4 scanned=4040` |

**AC2, stated honestly.** Three of its four clauses pass:
`deployed=1e32562729... previous=c97232408d... descends=yes; gateway app/tests files changed=4, outside
MP-x-1's set=0`. The fourth prints the self-contradictory `mcportal_commit=d60b4e0 contains d60b4e0=no`.

Cause: the clause is `git -C mcportal merge-base --is-ancestor d60b4e0 "$MCP" 2>/dev/null`, and
`_root.sh` cds to the CALLING worktree -- where `mcportal` does not exist, because git checks a nested
repo out in the MAIN tree only. The command fails for a missing path, `2>/dev/null` hides why, and the
`&&` chain leaves `mok` at its initialised `no`. An absent repo and a genuinely wrong commit are
indistinguishable in that output.

The substance is TRUE, verified with a discriminating control: from the main tree,
`is-ancestor d60b4e0 d60b4e0` exits 0, while the control `is-ancestor d60b4e0 d60b4e0~1` exits non-zero.
And AC2's logic run VERBATIM from the main tree against this branch's manifest prints
`... contains d60b4e0=yes` -> **WOULD BE: PASS**. So the issuer's post-drain run from the merged index is
expected to pass, and this refusal is scoped to running it from a linked worktree before the drain.

Per BOUNDS 3 the criterion was NOT repaired and the check was NOT edited (section 3 makes it
read-never-write). Filed as row **`NFRA_MCPORTAL-Z-S28`**, with the same root cause as the
`data/transcripts/` gap above; `deploy-to-ec2.sh:40-44` already carries the `_main/mcportal` fallback AC2
lacks.

## Commits

| commit | what |
|---|---|
| `1e32562729` | release branch: `mcportal_commit=d60b4e0` on the re-cut tree (step 1) |
| `019b139450` | release branch: the deploy script's own auto-record (NOT authoritative) |
| `48fff5205a` | trunk: hold released -> OPEN |
| `e9a1bf5127` | trunk: 4 legs closed with proof, ledger CLOSED, manifest recorded |
| `d9a121832e` | shared tree: rows Z-S27 + Z-S28 |

Ledger `20261009T1414Z_nfra-mcportal-r5-control-plane-release_deploy_completion.md`: **CLOSED**, all 4
legs proven, sentinel removed, closed BEFORE the AC reads as the order requires.
