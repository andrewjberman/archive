# MP-n-1 PRE-ACT RECORD -- the C17 bounded git-state read, released on live base `d9f2ebded9`

**Cell:** `NFRA_MCPORTAL.TO-MP-n-1` (PRD v0.6 C17 + AMENDMENT 1) -- `<risk>WORLD</risk>`
**Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-n-1.bounded-gitstate-read.md`
**Applier:** `0.7.0_AE_CloudOps~MP` **Issuer:** `2.0.0_SA_COO~MP`
**Release branch:** `rel-nfra-mcportal-c17-v2` @ `b5e61b5d86`, worktree `C:/tmp/mp-n1-rel2`
**Live base:** `d9f2ebded95b638d4de9a701e1123bfbf051a5c1`
**Ledger slug:** `nfra-mcportal-c17-gitstate-release`
**Halves:** COO @`11aa382562` (condition C-1) and CTO @`0d546c5381` (condition CTO-1), both SIGNED.
**ASK:** `deliverables/0.7.0_AE_CloudOps~MP/NEVER_WIDEN_ASK_MP-n-1_20261012.md` @`bf627dd9bb`

---

## 1. What C17 changes, and what it gives up

The served `GET /api/admin/fabric/gitstate` cold read was 22.8 s with 2,771 body fetches against a 30 s
bar, rising daily, because the cost was a function of HISTORY LENGTH: the listing walked every key a box
had ever written, and the refusal scan stopped only AT a refusal, so a box with no refusal on record
fetched its entire history. Three bounds now hold -- the listing starts at the window (`StartAfter`), the
refusal scan stops at the first INTEGRATE PASS whatever its outcome, and the first-seen scan stops at the
first record whose trunk head differs -- plus AMENDMENT 1's `FETCH_THREADS` 8 -> 32.

**Deliberately given up, and stated where it is served:** history older than 48 h is no longer read, so
`integration_refused` and `trunk.first_seen` can only see inside the window. The new
`integration_refused_basis` field says so per box, so "not recorded" cannot be over-read as "nothing was
ever refused".

**A semantic change rides with the bound:** the newest integrate pass now decides, so a refusal that a
later successful integrate cleared reads "not recorded". The pre-C17 test asserted the opposite, and was
split into two arms rather than quietly flipped.

## 2. The live base, read from the HOST by md5

| compared against | EQUAL | DIFFERENT | git-only | host-only |
|---|---|---|---|---|
| `d9f2ebded9` (candidate) | **100** | **0** | 0 | 0 |
| `28ba9532b6` (NEGATIVE CONTROL, the superseded base) | 97 | **3** | 0 | 0 |

The three differing files are `app/destructive_ops.py`, `app/integrations/advi_billing/site_to_s3.py` and
`app/tools.py` -- OG-ap-10's payload. So the base is `d9f2ebded9` BY BYTES, the instrument discriminates,
and the world did move under this cell between the first cut and this one.

Service at the read: `active`, MainPID **990802**. SSM `28a0ebde-8831-411b-ae9b-2477fc3d9ebd`.

## 3. The re-cut, and CTO-1's four pre-signed terms

OG-ap-10 shared this cell's original base and landed first (ledger closed 2026-10-12T11:58:46Z). CTO-1
says whichever release acts second re-cuts and does not declare a base it has not re-cut on. The original
cut on `28ba9532b6` is therefore **discarded, not reused**.

| term | requirement | measured |
|---|---|---|
| 1 | the diff is exactly the same 2 files | 2 files, 198 insertions, 27 deletions; outside the two **0**; outside the gateway dir **0** |
| 2 | both blobs still read `a134916e01` and `6b5ac530f5` | **both MATCH** |
| 3 | the rollback key becomes `opal-gateway-d9f2ebded9.tar.gz`, proven by the ASK's content check | **proven**, section 4 below |
| 4 | one fresh host cold sample at or under 10 s | **7.899 s**, section 5 below |

Payload taken with `git checkout 8e89e97b3e -- <paths>`, which lifts that commit's exact blobs and cannot
conflict; term 2 is written on the blob ids, and they are what the result is checked against.

**C-1 (the COO's condition) is why the payload is COMMITTED and not merely staged.**
`deploy-to-ec2.sh:203` sets `FULL_SHA="$(git rev-parse HEAD)"`, and both the artifact NAME and its
`git-ref` metadata derive from it. Had HEAD still sat at the base, the act would have written the release
bytes to `opal-gateway-d9f2ebded9.tar.gz` -- the very key term 3 proves as the rollback -- and stamped it
with the base's ref. That is the Z-S92 class, which cost MX-r-9 a versioned-copy restore and a second
deploy. HEAD now names the release, so the artifact will be `opal-gateway-b5e61b5d86.tar.gz`.

## 4. Rollback, proven for THIS base before the act

`s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-d9f2ebded9.tar.gz` --
**542,107 bytes, ETag `18b56591a0201d43857c5adf3d955026`, `Metadata.git-ref`
`d9f2ebded95b638d4de9a701e1123bfbf051a5c1`, LastModified 2026-10-12T11:24:59Z.** The VERSIONED key, never
`-latest`, which this act overwrites.

Downloaded (542,107 bytes read back, equal to `head-object`) and its `app/` files compared three ways:

| comparison | common | EQUAL | DIFFERENT |
|---|---|---|---|
| ARTIFACT vs GIT at `d9f2ebded9` | 100 | **100** | 0 |
| ARTIFACT vs the RUNNING HOST | 100 | **100** | 0 |
| GIT at `d9f2ebded9` vs the RUNNING HOST | 100 | **100** | 0 |

Plus a NEGATIVE CONTROL: the same artifact against the superseded base reads **3 DIFFERENT of 100**. So
the artifact IS this base, not merely an object named for it, and the check can fail.

**Pre-staged clean rollback tree:** `C:/tmp/mp-n1-rb2`, detached at `d9f2ebded9`, 0 uncommitted lines,
carrying `deploy-to-ec2.sh`, `meeting_allowlist.json`, `lib/opal_naming.py`,
`org/standards/NAMING_SCHEMA.json` and `infra/logic/registry` -- the full input set this base's deploy
script needs.

**THE ROLLBACK COMMAND, from `C:/tmp/mp-n1-rb2`:**

```
DEPLOY_BASE_REF=b5e61b5d86c4fe3482e3f367c25ab7fc798a0c47 \
  bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh
```

Unexercised.

## 5. The load samples, and the margin named honestly

All on the host under the instance role against the live store, on the RELEASE bytes, each a fresh
interpreter with the body cache **asserted empty** (the probe exits 3 and voids the sample otherwise --
row Z-S32: coldness is per-CACHE, not per-process). The bundle's module was md5-matched on the host to
the release tree before timing, beside the served module's contrasting md5, so each sample provably timed
the bytes about to ship.

| sample | base | time | body fetches | SSM |
|---|---|---|---|---|
| pre-AMENDMENT 1 (STOPPED the cell) | 28ba9532b6 | **16.661 s** | 1,346 | ec31a13d |
| after AMENDMENT 1, run 1 | 28ba9532b6 | 7.751 s | 1,371 | 53d0261d |
| after AMENDMENT 1, run 2 | 28ba9532b6 | 7.054 s | 1,371 | b8f02c72 |
| after AMENDMENT 1, run 3 | 28ba9532b6 | 6.407 s | 1,371 | 0643d61b |
| **CTO-1 term 4, on the re-cut** | **d9f2ebded9** | **7.899 s** | **1,381** | 2ad814d6 |

**The bar is met and the margin is thin.** 7.899 s against 10 s is 1.27x. At ~5.72 ms per fetch the bar
corresponds to roughly 1,750 fetches, so the real headroom is about **27 percent in WINDOW POPULATION**,
not in time -- and that population grows: the 48 h window held 2,134 records when counted directly at
09:48Z (laptop 800, dell1 468, dell2 456, sitez 410, of 3,329 total history), and the fetch count has
risen 1,346 -> 1,371 -> 1,381 across today's samples. C17 plus AMENDMENT 1 buys headroom; what would make
this structural is a per-box pointer object naming the newest integrate pass, which is row Z-S40's option
(c), a producer change this cell is forbidden to make and which sits with `1.0.0_SA_CTO~Z`.

## 6. The census and the bundle

`git diff --stat d9f2ebded9 HEAD -- infra/aws/ec2/opal-gateway`: **2 files, 198 insertions, 27 deletions.
Files outside those two: 0. Paths outside the gateway directory: 0.**

`mcportal_commit` stays **`bc37107`**, unchanged. Bun cache pre-check against that commit's own lockfile:
**77 of 77 present, rc=0.** No package is fetched.

**This base CHANGES the deploy script this act runs**, which the CTO-1 terms do not cover and which bit
MP-x-4 once: `d9f2ebded9` adds a fail-closed `ADVI_MARKET_UPDATE_S3_ROOT` check that calls
`lib.opal_naming.address()` from the release tree and exits 1 BEFORE any upload on a wrong shape. It was
tested against **this base's own bytes** -- not the main tree's, whose `lib/opal_naming.py` and
`infra/logic/registry` both differ, so a main-tree result would not have transferred -- and both that
check and the pre-existing `ADVI_FEE_STATEMENT_S3_ROOT` resolve to their correct `/bronze/<table>/` roots
at rc=0.

## 7. What the act does, in order

1. ACT from the release tree with ITS scripts: `bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway
   infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`, `DEPLOY_BASE_REF=d9f2ebded9...`. The stale-base guard
   must read the live ref unchanged at both reads.
2. Poll `/health`. **Not 200 within 90 seconds -> run the rollback in section 4 AT ONCE**, close the entry
   as rolled back, stop.
3. L1's proof reads back BOTH the new versioned key AND the rollback key, which must still be ETag
   `18b56591a0201d43857c5adf3d955026` (C-1's second limb).
4. Tool surface before and after through one reader; the difference must be empty. The BEFORE read is
   taken on this base, not reused from an earlier one -- `app/tools.py` changed in `d9f2ebded9`.
5. Manifest record on the release branch AND on `box/sitez`, the latter written on top of box/sitez's
   current `EC2_MANIFEST` with `previous_deployed_commit = d9f2ebded9` (msg 33482), never from the release
   tree's vintage copy.
6. Close every leg with its proof and commit the close BEFORE the AC reads.

**BOUNDS held:** no Terraform, ALB, host, role or secret change; `safe-ec2-deploy.sh` read never edited;
no module touched but `admin_fabric_gitstate.py` and its test; the producer `.tools/fabric-gitstate.py`
untouched; and the gateway still writes nothing to the store.
