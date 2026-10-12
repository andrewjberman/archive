# NEVER-WIDEN ASK -- `MP-n-1` (C17, the bounded git-state read), 2026-10-12

**Cell:** `NFRA_MCPORTAL.TO-MP-n-1` (PRD v0.6 C17 + AMENDMENT 1), `<risk>WORLD</risk>`
**Asked by:** `0.7.0_AE_CloudOps~MP` (applier) **Signers owed:** `2.0.0_SA_COO~MP` and `1.0.0_SA_CTO~Z`
**Bound to:** release branch `rel-nfra-mcportal-c17`, payload commit `e7e7469db8`, live base
`28ba9532b648061cecafe426836d3e96af4529cd`
**Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-n-1.bounded-gitstate-read.md`

This is the ASK required by step 3, written BEFORE any ledger act. Nothing has been uploaded, no ledger
entry exists, and no sentinel is written. The deploy waits on both halves against this commit and on the
issuer's GO.

---

## 1. WHAT THE ACT MAY TOUCH -- the blast radius

**Two files, one of which never ships.**

| surface | change | reaches production? |
|---|---|---|
| `infra/aws/ec2/opal-gateway/app/admin_fabric_gitstate.py` | C17's three bounds + AMENDMENT 1's `FETCH_THREADS` 8 -> 32 | YES |
| `infra/aws/ec2/opal-gateway/tests/test_admin_fabric_gitstate.py` | the tests for them | NO -- test files are source-only and are not executed on the host |

Census, in the order's literal form, `git diff --stat 28ba9532b6 HEAD -- infra/aws/ec2/opal-gateway`:
**2 files, 198 insertions, 27 deletions. Files outside those two: 0. Paths outside the gateway directory:
0.**

**The served property that moves, and its writers COUNTED rather than assumed.** The property is the
response body of `GET /api/admin/fabric/gitstate`. Its writers: **N = 1.** `app/admin_api.py:58` maps
that route to `admin_fabric_gitstate.gitstate` and to nothing else, and the only two modules in the
gateway that reference `admin_fabric_gitstate` are that route line and the handler itself. So one writer,
one rule read, and the rule read is the handler's own code in this payload.

**What the act does NOT touch:**

- **No store object is written or moved.** This is a READ handler. The gateway writes nothing; its only
  store calls remain `list_objects_v2` and `get_object`, and `list_objects_v2` gains only a parameter.
  No S3 key changes, so there is no served-output move and no per-key data rollback to name.
- **The producer is untouched.** `.tools/fabric-gitstate.py`, which writes the records this handler
  reads, is not edited (BOUNDS 1). Z-S40's option (c) would have touched it and was therefore routed to
  `1.0.0_SA_CTO~Z` instead of taken here.
- **No Terraform, no ALB, no instance, no IAM role, no secret.** `safe-ec2-deploy.sh` is read, never
  edited. No new store call kind, so MP-x-3's existing read grant is unchanged and sufficient.
- **No other handler, and no other module.** The MCP tool surface is expected to be unchanged; the act
  records its count before and after and the difference must be empty.
- **The mcportal bundle does not move:** it stays at the manifest's current `mcportal_commit` `bc37107`.

**What the act DOES do to production, stated plainly:** it replaces the bytes of one read handler and
**restarts the served gateway**, which is a brief interruption to every route on
`i-07dccb1615503ac99`, not only to the one being changed. That restart is the widest consequence of this
act and it is the reason this ASK exists.

## 2. THE ROLLBACK, PER KEY -- proven before the act, not asserted

**The key:** `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-28ba9532b6.tar.gz`
-- **540,286 bytes, ETag `8dc8d98ad0fdfa1f04ed193982aa154c`, `Metadata.git-ref`
`28ba9532b648061cecafe426836d3e96af4529cd`, LastModified 2026-10-11T18:47:45Z.** The VERSIONED key,
never `-latest`, which this act overwrites.

**Proven by CONTENT, three ways, so the artifact is the live base and not merely an object named after
it.** Downloaded (540,286 bytes read back, equal to `head-object`), extracted (132 entries), and its
`app/` files compared:

| comparison | common | EQUAL | DIFFERENT |
|---|---|---|---|
| ARTIFACT vs GIT at `28ba9532b6` | 100 | **100** | 0 |
| ARTIFACT vs the RUNNING HOST | 100 | **100** | 0 |
| GIT at `28ba9532b6` vs the RUNNING HOST | 100 | **100** | 0 |

No file on only one side in any pairing. The host read is an SSM md5 census taken this session, and it
came with a NEGATIVE CONTROL: the same comparison against `2a5966dfbd` (this seat's own earlier MP-r-2
release) reads 7 DIFFERENT and 2 host-only, so the instrument discriminates rather than matching
everything.

**A clean rollback tree is PRE-STAGED so no build happens at incident time:** `C:/tmp/mp-n1-rb`, detached
at `28ba9532b6`, 0 uncommitted lines, `deploy-to-ec2.sh` and `meeting_allowlist.json` both present, and
its manifest pins `mcportal_commit: bc37107` -- the base's own bundle, which is what a rollback must
rebuild.

**THE ROLLBACK COMMAND, to run from `C:/tmp/mp-n1-rb`:**

```
DEPLOY_BASE_REF=<the release commit this act makes live> \
  bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh
```

**Unexercised.** It has not been run, and this ASK does not claim it has.

## 3. THE EXPECTED OUTCOME -- BOTH branches

The outcome is read from the producer's own rule -- the handler's code in this payload -- and from
measurements already taken on the host, never predicted from the input's shape.

**Branch A, the release holds the bar (expected).** `/health` returns 200 within 90 seconds of the
restart; `GET /api/admin/fabric/gitstate` with no identity returns 401 or 403; the served cold read
completes at or under 10 s with its body-fetch count printed and at least one box `recorded`; the MCP
tool-surface difference is empty. Graded by `n1.AC3`. The basis for expecting it is three cold samples of
THESE release bytes, taken on the host under the instance role against the live store, cache asserted
empty on every one:

| sample | time | body fetches |
|---|---|---|
| 1 | 7.751 s | 1,371 |
| 2 | 7.054 s | 1,371 |
| 3 | 6.407 s | 1,371 |

Worst **7.751 s** against the 10 s bar. The order asked for one sample; three were taken because a single
sample straddling a bar is the shape that shipped a breach once before on this project (row Z-S30, where
2 of 3 samples were under and the worst was over).

**Branch B, it does not hold, and what happens then.** If `/health` is not 200 within 90 seconds, the
rollback command in section 2 runs AT ONCE, the ledger entry closes as rolled back, and the cell stops.
If `/health` is fine but the served read exceeds 10 s, `n1.AC3` FAILS: this seat does NOT tune further
(BOUNDS 2 as amended by AMENDMENT 1) and the finding goes to a row for the issuer, with the window, the
bar and the producer pointer reserved to `1.0.0_SA_CTO~Z`. Either way the host returns to or remains on
`28ba9532b6`, whose artifact is proven above.

## 4. THE MARGIN IS THIN, AND NARROWING -- the one thing a signer should weigh

**7.751 s against 10 s is 1.29x headroom, and it is a function of a population that grows.** At
7.751 s / 1,371 fetches the rate is about 5.65 ms per fetch, so the bar corresponds to roughly 1,770
fetches: about **29 percent headroom in window population, not in time.**

The 48 h window held **2,134 records** when counted directly at 09:48Z today (laptop 800, dell1 468,
dell2 456, sitez 410, out of 3,329 total history), and the producers keep writing -- laptop alone writes
one record every 3.6 minutes. The samples above were taken at ~10:2xZ. This project has already measured
the same shape on the neighbouring handler: the fabric activity window fills through the working day
(rows Z-S27, Z-S29), and the fetch count rose 1,346 -> 1,371 in the 35 minutes between my two sample
runs today.

**So C17 plus AMENDMENT 1 does not make this read permanently safe; it buys headroom.** What would make
it structural is Z-S40's option (c) -- a per-box pointer object naming the newest integrate pass, turning
`_refused` from O(window) into one `get_object` -- and that is a producer change this cell is forbidden to
make. A signer should read this ASK as covering a release that holds the bar today with 29 percent of
population headroom, not as a claim that the bar is comfortably met.

One figure is recorded without an explanation, rather than explained away: the three samples fell
monotonically, 7.751 -> 7.054 -> 6.407 s, at an identical fetch count and identical window contents.
Something outside the handler's own body cache warms between fresh interpreters. The worst sample is the
one carried against the bar, so the claim does not rest on it.
