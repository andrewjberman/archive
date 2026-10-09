# irpt-ycharts-generate RELEASE 5b -- never-widen pair DRAFT (E11 + the E9 report modules, shipped whole; X-1 actor read-back)

**Deployer:** `2.0.0_SA_COO~Y2`. **Applier:** `0.7.0_AE_CloudOps~DELL2`. **Supersedes** release 5 (`NEVER_WIDEN_PAIR_RELEASE5_E11.md`, blob
553de57d42). Release 5 rolled back at 01:52:26Z on row `IRPT_BCKEND-D2-S18`:
- `RetentionPolicy.reference()` received 4 arguments against 3;
- the cause was that rider `f60e6f1d2a` shipped split, because `retention.py` lagged at `3f29017cfc`;
- round 73 (IB-yr-731, drained @328b73d536) re-pinned `retention.py`, the packaged registry and `ExportBundle.schema.json` to
  `2f3ee8c15b`.

DRAFT: no half signed.

## 1. Pin and artifact

- **Pin:** box/dell2 `328b73d536`. LOCAL when drafted; origin box/dell2 read `5baf94294f`. It must be on origin before the apply.
- **Built** (BUILD_ONLY at 328b73d536, this seat): `5FRkux2oSNN1jB4xJEibio+F9F2ofl9mgcuH9jN/JrY=`.
- **Live now / ROLLBACK:** `Un0wVZqjqpwKhpYyFeBRW3fVFddrlHR0BtHjYuP5eNY=` (release 3).

## 2. Three gates, run by this seat at the pin

| gate | reading | what it catches |
|---|---|---|
| census | `changed_members=6`: composition, ExportBundle.schema.json, custody_submission, reporting_policies.json, repository, retention | an unnamed member |
| `checks/r73/cochange_closure.py` | `rows=84 commits_checked=33 split=0` | a commit shipped half (release 5's defect) |
| `checks/r71/symbol_closure.py` on the BUILT zip | `modules=62 pairs=273 missing=0` | an imported name the packaged module lacks (release 4's defect) |

## 3. Every changed member, and its owner's confirmation

| member | built / live | carries | confirmed |
|---|---|---|---|
| `custody_submission.py` | 420ccd097831 / e347d1d198d0 | E11 (IB-yr-691) | Y. No live importer yet (~G2 msg 2012), so there is no served effect until release 6 wires it. |
| `composition.py` | 5b896004af77 / 6d2c3696d030 | E9 + `f60e6f1d2a` | ~P2 msg 2011 (E9); ~G2 msgs 2012/2166 (inert) |
| `repository.py` | f01fcf549e8e / f255335beb26 | E9 + `f60e6f1d2a` + `b13bab7495` | ~P2 msgs 2011/2171; ~G2 msg 2166 |
| `retention.py` | f7540e355241 / bdd74e5f9b90 | `f60e6f1d2a` (`reference(..., policy_revision)`) | ~G2 msg 2166 |
| `infra/logic/registry/reporting_policies.json` | dc0eccfde861 / cdc1f2c40a1f | `c6c3c0b674`, `e923e0f463`, `f60e6f1d2a` (~G2); `0798635fec` (Y: ycdgen research row); `8530114ff9`, `0c35aeeaa8` (~M2: `irpt-custody-x10-v1` ACTIVE) | ~G2 msg 2166 (the default `irpt-x10-v1` row sha `e0046398` is unchanged); ~M2 msg 2163 (additive only) |
| `contracts/ExportBundle.schema.json` | 1dda12f2df77 / cac4470a174d | `239b895bc7`, `b13bab7495` | ~P2 msg 2171 (admits kind CUSTODY_REPORT; PERFORMANCE and ANALYSIS unchanged) |

**Widens:** no principal class, route or grant. **Moves:** one function. **Does not move:** IAM and every other function.

## 4. After-reads (order fixed; the release-5 conditions carry over)

0. Live re-read at start is `Un0wVZqj...`; otherwise STOP.
1. Re-run the symbol closure on the UPLOADED zip (downloaded back by version): `missing=0`, or STOP before the apply.
2. After apply: live == `5FRkux2o...`; re-plan 0. Import census `failed: {}` GATES the rest.
3. E11 offline at the pin: 3 passed; custody suites 66 passed, 2 skipped.
4. **X-1 actor:** ONE upload-only, template-lane, on-behalf upload with `advisor_email` (the `adv-` label = first 12 hex of sha256 of
   the lowercased email). The laptop reads back BEFORE any delete and returns all three booleans. Closes row `IRPT_BCKEND-D2-S17`.
5. Refusals hold: an unlisted-firm advisor; a firm not on the filer's list.
6. Cleanup, every branch: dell2 deletes the test row; the laptop deletes the admit's records and every S3 version AFTER read-back 4.
   The S3 deletes need Andrew's word.

**Branch B:** any of 0-2, 4 or 5 fails -> roll back to `Un0wVZqj...` the same session, then cleanup, then a BLOCKING row.
**Lesson from release 5's halt:** read the failing call's CloudWatch line BEFORE halting a live release.

## 5. Owed before signing

- The CTO half.
- Pin `328b73d536` on origin.
- Andrew's word on the S3 deletes of the read-4 upload.
