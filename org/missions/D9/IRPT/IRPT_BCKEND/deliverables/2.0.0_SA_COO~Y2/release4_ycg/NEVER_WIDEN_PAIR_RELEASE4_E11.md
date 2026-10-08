# irpt-ycharts-generate RELEASE 4 -- never-widen pair DRAFT (E11, plus the X-1 actor read-back owed from release 3)

**Deployer:** `2.0.0_SA_COO~Y2` (the function's lane). **Applier:** `0.7.0_AE_CloudOps~DELL2`, per Andrew-direct ~22:0xZ (MSTR msg
1759: dell2 deploys go to dell2's own applier). **Rulings:**
- `1.0.0_SA_CTO~DELL2` ADDENDUM 10: E11 rides the release after E6.
- msg 1877: X-1's actor is graded on THIS release's after-read. The read-back is taken BEFORE any cleanup delete, and IB-yr-681
  closes on it.

DRAFT: no half signed, nothing applied.

## 1. Pin and artifact

- **Pin:** dell2 box/dell2 `e94a64b0f6`. LOCAL when drafted; origin box/dell2 read `ab11f097f3`. The pin must be on origin before
  signing.
- **Built** (BUILD_ONLY at e94a64b0f6, gates passed, this seat ~23:0xZ): `emzWWzrR0TUf7sHDbEeDeedc1EnTeaXAMl5kSHYLU7E=` (100 members;
  import-closure OK, 63 .py).
- **Live now / ROLLBACK:** `Un0wVZqjqpwKhpYyFeBRW3fVFddrlHR0BtHjYuP5eNY=` (release 3, LastModified 2026-10-08T21:26:18Z).

## 2. Every changed member (`release-census.py irpt-ycharts-generate --pin HEAD`; changed_members=1; `CENSUS_e94a64b0f6.txt`)

| member | built / live | owner | what it does |
|---|---|---|---|
| `custody_submission.py` | 420ccd097831 / e347d1d198d0 | Y (IB-yr-691 = E11, @128b6f7db1, drained @b1ba475229) | A Performance client statement submission builds its retained repositories with the custody revision `irpt-custody-x10-v1`, but only when the reporting-policy registry carries it (E9's probe). PERFORMANCE and ANALYSIS stay on `irpt-x10-v1`. |

**Widens:** no principal class, route or grant. It is a storage-revision choice on an existing path; the access checks are
unchanged. **Moves:** one function. **Does not move:** IAM, every other function, the resident.

## 3. After-reads (order fixed)

0. Live re-read at start is `Un0wVZqj...`; if not, STOP.
1. Equality: live == `emzWWzrR...`; re-plan 0.
2. Import census: `failed: {}`.
3. **E11, offline proof:** `tests/test_custody_submission_revision.py` (3 passed) and the custody suites (66 passed, 2 skipped) at
   the pin. A live statement submission is NOT run here. Its served proof is IRPT_CUSTDY's E2a, which retains one real statement
   through E10's function (ADDENDUM 10 order).
4. **X-1 actor (msg 1877):**
   - A test OPAL_GLOBAL filer (no login identity; `allowedFirmIds` = [F]) makes ONE template-lane on-behalf upload for a verified
     advisor of F, as in release 3.
   - The laptop then reads back, BEFORE any delete, and returns as booleans: the stored original's sha256 equals the sent body; the
     UPLOAD# row's owner is that advisor at F; the UPLOAD# row's `acting_principal_id` is the test filer. Opaque ids only.
   - The YCharts `securities_info` resolution for that one upload is authorized (Andrew-direct ~21:1xZ, record @5c9df0ead7).
5. **Refusals hold:** an unlisted-firm advisor is refused; a firm not on the filer's list is refused.
6. **Cleanup, every branch:** the test row is deleted on dell2. The admit's records and every S3 version are deleted on the laptop
   AFTER read-back 4, each re-read NOT_FOUND. The S3 deletes need Andrew's word per object, as before.

**Branch B:** if any of 0-2, 4 or 5 fails, roll back to `Un0wVZqj...` the same session, then cleanup; file a BLOCKING row.

## 4. Still owed before signing

- Pin `e94a64b0f6` on origin.
- The CTO half.
- Andrew's word on the S3 deletes of the read-4 upload (or a standing word, if the CTO records one).
