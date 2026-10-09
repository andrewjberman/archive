# MP-r-2 PRE-ACT RECORD -- STOPPED AT STEP 2, nothing opened and nothing deployed

**Seat:** `0.7.0_AE_CloudOps~MP`
**Task order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-r-2.cp2-gateway-release.md`
(`pending`, workstream CP2, `<risk>WORLD</risk>`, GO msg 32920)
**Record lives here, not in the ledger entry:** AMENDMENT 4. `deploy_ledger.py` regenerates the entry on
`hold` and `close-leg` and drops appended prose (rows Z-S24 / Z-S25). In this cell no entry exists at all,
because the cell stopped before step 4.

---

## VERDICT: STOP. Step 2's load condition is breached.

`admin_fabric_overlap._compute(6)` read **31.611 s** against the order's **30 s** bar (half the ALB's
60-second idle timeout). Step 2: *"Any one over 30 s ... STOP with a BLOCKING row naming the time. The
issuer re-cuts."* BOUNDS 1: *"no handler is edited in this cell. A load-condition failure stops it, it
does not tune."*

So: **no ledger was opened, no artifact was built or uploaded, no SSM deploy was dispatched, no handler
was touched.** Row **`NFRA_MCPORTAL-Z-S30`**.

## The measurement

On the host under the instance role
`arn:aws:sts::313476888478:assumed-role/opal-gateway-role/i-07dccb1615503ac99`, SSM
`c6cc7a81-0465-42df-801a-22c71d74ce87` (Status=Success), running the RELEASE's three handler modules plus
`app/refs/overlap_rules.json` in a scratch copy of the live `app/` package under
`/opt/opal-gateway/.venv/bin/python`. Local -> S3 -> host pull per Rule 12; no Python inlined into an SSM
command, nothing written on the VM, scratch removed by a trap. **Three samples, each a fresh interpreter,
so each in-process cache is empty by construction.**

| handler | call | s1 | s2 | s3 | worst | bar | verdict |
|---|---|---|---|---|---|---|---|
| `admin_fabric_overlap` | `_compute(6)` | **31.611** | 24.508 | 22.333 | **31.611** | 30 | **OVER -- margin -1.611 s, headroom 0.95x** |
| `admin_fabric_gitstate` | `_compute()` | 5.135 | 3.680 | 3.546 | 5.135 | 30 | inside, margin 24.865 s, 5.84x |
| `admin_fabric_calls` | `_compute('open')` | 0.460 | 0.427 | 0.459 | 0.460 | 30 | inside, margin 29.540 s, 65.22x |

overlap scanned `records_scanned` 4543 / 4544 / 4546 with `records_skipped` 0; gitstate returned 4 boxes;
calls returned 4 boxes and 18 calls. **All three imported and returned real bodies** -- this is a LOAD
finding, not an import or wiring failure.

## Two things worth saying about that table

**It straddles the bar, which is the dangerous shape.** Two of three overlap samples (24.508, 22.333) are
UNDER 30 s. A cell taking ONE pre-act sample had roughly a 2-in-3 chance of reading a pass and shipping a
page whose first open can exceed half the ALB idle timeout. The order's "any one over 30 s" combined with
three samples is what caught this; a single-sample gate would not have.

**This is Z-S27's mechanism arriving on a second handler.** `overlap` reads the same fabric activity store
as `admin_fabric`, over the same rolling 6-hour window, and that window has been filling all day:

| time | handler | records | cold |
|---|---|---|---|
| 14:0xZ | admin_fabric | ~3,150 | 13.6-16.8 s |
| 15:5xZ | admin_fabric | ~3,790 | 18.1-24.4 s |
| 16:2xZ | admin_fabric (x4.AC3) | 4,040 | 24.2 s |
| ~17:xxZ | admin_fabric (issuer's x4.AC3 re-run) | -- | 27.4 s |
| 18:3xZ | **overlap** | **4,543-4,546** | **22.3-31.6 s** |

On that reading overlap is not pathological: it costs about what `admin_fabric` costs per record, on a
larger count. The corollary matters for the fix -- **`admin_fabric`, which is already LIVE from MP-x-4,
will cross the same bar at roughly the same store size.** Narrowing only `overlap` would leave the live
handler a short time behind it.

## Steps 0, 1 and 3 are complete and hold

The re-cut does not start from nothing.

**Step 0 -- route hookup.** `app/admin_api.py` on `wk-mcportal-cp2-r2` @`354d58bc30`: three imports
(`admin_fabric_calls`, `admin_fabric_gitstate`, `admin_fabric_overlap`) beside `admin_fabric`, and the
order's four route lines verbatim after `Route("/fabric/boxes", ...)`. Diff is 7 insertions, 0 deletions,
0 CR, 0 non-ascii. Tests: `tests/test_admin*.py tests/test_entitlement_admin.py` -> **58 passed**, 0
failed, matching the 58 the issuer measured with exactly these lines. Amendment 2 moved this hookup here
because the issuer's own commit was refused by the owned-paths gate -- `app/admin_api.py` is lane
CLOUD_OPS_OR_ETL and this seat holds the grant.

**Step 1 -- release tree.** `rel-nfra-mcportal-cp2` @`74d2522f22`, cut from the LIVE `deployed_commit`
`1e32562729` (MP-x-4's release), read from `EC2_MANIFEST.json` and not assumed.

*Census, the order's STOP gate -- PASSES:* 8 gateway files, 1,581 insertions, **0 files outside**
`infra/aws/ec2/opal-gateway/`, and **0** `.xlsx`/`.pptx` (the GO's E2 and pptx exclusions hold by
construction). The eight: `app/admin_fabric_overlap.py`, `app/refs/overlap_rules.json`,
`tests/test_admin_fabric_overlap.py` (MP-o-1); `app/admin_fabric_gitstate.py`,
`tests/test_admin_fabric_gitstate.py` (MP-s-1); `app/admin_fabric_calls.py`,
`tests/test_admin_fabric_calls.py` (MP-k-1); `app/admin_api.py` (step 0).

*Applied BY PATH, not cherry-picked, and here is why.* A straight `git cherry-pick 604ea0e089` (MP-s-1)
CONFLICTS: `DU` on
`org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-g-1.fabric-gitstate-handler.md`. The
conflict is not in gateway code -- the gateway files apply cleanly. These are TRUNK commits that also
carry org/ bookkeeping (a proof instance, a status flip), and the release base is an off-trunk commit that
predates those files, so git sees delete-versus-modify. 604ea0e089 carries 2 non-gateway paths and
5bdf8e1a3e carries 3; none belongs in a gateway artifact, and other seats' deliverables and task-orders
are outside this cell's `<paths>` anyway. So each remaining commit's gateway paths were taken with
`git checkout <commit> -- <paths>`, which cannot conflict, and the result was verified byte-for-byte:
md5 of each file in the tree EQUALS md5 of the same path at its source commit. MP-o-1 638b8ae057 was
cherry-picked whole, because it carried zero non-gateway paths.

*Manifest:* `mcportal_commit` set to `bc37107` (MP-p-2, branch `nfra-mcportal-cp2-p2`, a descendant of
`d60b4e0`), one line changed. `bc37107` verified present in this box's mcportal store.

*bun cache pre-check* against `bc37107`'s OWN lockfile (30,903 bytes, extracted with `git show`):
**77 of 77, rc=0** -- no package would be fetched.

**Step 3 -- rollback, proven before any act.** The live base's own artifact is in S3 and was
content-verified during MP-x-4 and re-read since:
`s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-1e32562729.tar.gz`, 518,165 bytes,
ETag `b96315a523842ec46579b146c450faa9`, `Metadata.git-ref` = `1e32562729...`, equal to the live
`deployed_commit`. Nothing has been uploaded by this cell, so `opal-gateway-latest.tar.gz` still carries
the same bytes and git-ref; a rollback would still name the VERSIONED key, never `latest`. A from-scratch
rebuild is NOT offered in its place and that is stated rather than skipped: tar/gzip metadata and the bun
build are not bit-reproducible, so a rebuilt tarball could not be compared to the deployed one and a
mismatch would prove nothing.

```
# rollback (unexercised; nothing to roll back, since nothing was deployed)
aws s3 cp s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-1e32562729.tar.gz \
  /tmp/rb.tar.gz --region us-east-1
sudo -u ec2-user tar -xzf /tmp/rb.tar.gz -C /opt/opal-gateway
sudo systemctl restart opal-gateway && curl -fsS localhost:8080/health
```

## World state, verified after the measurement

`/opt/opal-gateway/app/admin_fabric_overlap.py` still **ABSENT** (the CP2 release is not live), service
`active`, MainPID **864717** unchanged from MP-x-4's release. No POST was ever made to
`/api/admin/fabric/calls/close` -- BOUNDS 2 reserves the one real close for Andrew in MP-q-1. No entry
exists for slug `nfra-mcportal-cp2-release`.

## One honest note on the release tree's test run

The full admin/fabric suite does NOT pass from the release tree (53 passed / 5 failed, improving to 56/2
once the issuer's `cp2/fixtures/` was materialised read-only and then removed again). Every failure is
`FileNotFoundError` on a repo path the release BASE predates -- the issuer's
`cp2/fixtures/s3_capture_20261009T0728Z.json`, `org/devices/DEVICES.json`, `.tools/open-calls-scan.py`.
The release-base lineage chains from prior release commits, so its NON-gateway tree is stale by design.
That is why step 0's test requirement was measured on the `box/sitez` worktree -- **58 passed**, the same
environment the issuer's own 58 came from -- and why it is not a product signal. Test files are
source-only and never ship to the host. The materialised fixture was removed before any commit; the
release tree's only uncommitted change is the intended `mcportal_commit` edit.

## What the re-cut should expect

1. **The live base will have moved again.** The gateway queue is MX-r-9 -> MP-r-2 -> OG-rl-16
   (`2.0.0_SA_COO~O` msg 32919), one release in flight. `deployed_commit` must be re-read at the act and
   the tree re-cut on whatever MX-r-9 leaves live; `1e32562729` above will be stale.
2. **Re-measure all three handlers, not just overlap** -- and expect the numbers to depend on the hour,
   since the window empties overnight and fills through the working day.
3. **Whatever fix is chosen for `overlap` probably belongs on `admin_fabric` too**, which is already live.

Commits this cell produced, all LOCAL (`box/*` is pushed by an MSTR or `box-sync`):
`354d58bc30` (step 0 hookup, `wk-mcportal-cp2-r2`), `5788114563` + `74d2522f22` (release payload,
`rel-nfra-mcportal-cp2`), and the row commit in the shared tree.
