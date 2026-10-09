# irpt-ycharts-generate RELEASE 5 -- never-widen pair DRAFT (E11 with the E9 report modules, plus the X-1 actor read-back)

**Deployer:** `2.0.0_SA_COO~Y2`. **Applier:** `0.7.0_AE_CloudOps~DELL2` (Andrew-direct ~22:0xZ, MSTR msg 1759). **Supersedes** release 4
(`NEVER_WIDEN_PAIR_RELEASE4_E11.md` @9d7d8b081d), which rolled back at 00:28:52Z.
- **Why it rolled back:** `custody_submission.py` could not import `CUSTODY_POLICY_REVISION` (row `IRPT_BCKEND-D2-S16`).
- **The fix:** round 71 (IB-yr-711, drained @2f3ee8c15b) re-pinned the staged `composition.py` and `repository.py` to carry E9.
- **The new guard:** a symbol-closure check of the built zip, `checks/r71/symbol_closure.py`.

The X-1 actor read-back (CTO msg 1877) moves here unchanged. DRAFT: no half signed.

## 1. Pin and artifact

- **Pin:** box/dell2 `2f3ee8c15b`, on origin (fetch + is-ancestor, ~01:0xZ).
- **Built** (BUILD_ONLY at 2f3ee8c15b, this seat): `4HEH1aDNa39+vwLFK24SldMOBit/hiBKF4aQjlsU1zk=`. Import-closure OK (63 .py);
  **symbol closure `modules=62 pairs=273 missing=0`**.
- **Live now / ROLLBACK:** `Un0wVZqjqpwKhpYyFeBRW3fVFddrlHR0BtHjYuP5eNY=` (release 3).

## 2. Every changed member (`release-census.py irpt-ycharts-generate --pin HEAD`; changed_members=3)

| member | built / live | what changes and why | owner / half |
|---|---|---|---|
| `custody_submission.py` | 420ccd097831 / e347d1d198d0 | E11 (IB-yr-691): statement submissions request `irpt-custody-x10-v1` through the registry probe | Y |
| `composition.py` | 5b896004af77 / 6d2c3696d030 | carries E9 (`CUSTODY_POLICY_REVISION`, `additional_policy_revisions`, @2aa217ec58) **plus rider** `f60e6f1d2a` (YCD-l-6: the Opal PDF retained under its own policy row) | E9: ~P2 (live in export since E9); rider: **~G2** |
| `repository.py` | f01fcf549e8e / f255335beb26 | carries E9 (per-family policy revisions) **plus riders** `f60e6f1d2a` (~G2, as above) and `b13bab7495` (IB-pr-336: one-line custody naming) | E9: ~P2; riders: **~G2**, **~P2** |

The riders are exactly the commits to those two files since `3f29017cfc`, other than E9 (`git log 3f29017cfc..2f3ee8c15b`):
- `composition.py`: E9 and `f60e6f1d2a`;
- `repository.py`: E9, `f60e6f1d2a` and `b13bab7495`.

**Widens:** no principal class, route or grant. The changes choose retention revisions and policy rows on existing paths.
**Moves:** one function. **Does not move:** IAM and every other function.

## 3. After-reads (order fixed)

0. Live re-read at start is `Un0wVZqj...`; otherwise STOP.
1. Equality: live == `4HEH1aDN...`; re-plan 0.
2. Import census: a direct invoke `{"irpt_import_census": true}` returns `failed: {}`. This is the read release 4 failed.
3. E11 offline at the pin: 3 passed; custody suites 66 passed, 2 skipped.
4. **X-1 actor (CTO msg 1877):**
   - one template-lane on-behalf upload by a test filer (no login identity) for a verified advisor of F;
   - the laptop reads back BEFORE any delete and returns all three booleans: body sha256 match, owner is the advisor, actor is the
     filer;
   - the one YCharts `securities_info` resolution is authorized (Andrew-direct ~21:1xZ).
5. Refusals hold: an unlisted-firm advisor; a firm not on the filer's list.
6. Cleanup, every branch:
   - dell2 deletes the test row;
   - the laptop deletes the admit's records and every S3 version AFTER read-back 4. The S3 deletes need Andrew's word per object.

**Branch B:** any of 0-2, 4 or 5 fails -> roll back to `Un0wVZqj...` the same session, then cleanup, then a BLOCKING row.

## 4. Owed before signing

- `~G2`: DONE (msg 2012). Rider `f60e6f1d2a` is INERT on the live path: `generate_installed.py:224` passes no additional revisions,
  and publisher/opal_producer are reached only from the resident. ~G2 also notes `custody_submission.py` has 0 non-test importers at
  HEAD. So **E11 changes nothing served until a composer imports it** (IRPT_CUSTDY E2a / E10 path); read 3 stays offline.
  ~G2's second point (default policy drops `OPAL_REPORT_PDF`) does NOT apply to this release, as MEASURED by this seat:
  - no policy in `infra/logic/registry/reporting_policies.json` carries that family, now or at `3f29017cfc`;
  - the census changes only the 3 named members, so the packaged registry bytes are identical live vs built.
- `~P2`: DONE (msg 2011), confirmed by content at the pin: E9 composition 5/5 lines and repository 6/6; rider `b13bab7495` 1/1.
- The CTO half.
- Andrew's word on the S3 deletes of the read-4 upload.
