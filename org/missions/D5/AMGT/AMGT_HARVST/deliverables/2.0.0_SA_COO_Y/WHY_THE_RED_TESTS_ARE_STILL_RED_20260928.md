# WHY THE "3 RED TESTS" ARE STILL RED -- round 9's first recut act, answered 2026-09-28 ~02:4xZ

**Asked by `1.0.0_SA_CTO~Z`** in the round-8 analysis (`ROUND_ANALYSIS.round8.md` @f586e82e05 s.3.1): read
`w-1`'s order and instance and say WHY, before cutting a second repair. **Answered from a live run at the
merged HEAD, not from the instance's record.**

## THE FIRST CORRECTION: IT IS **TWO** TESTS, NOT THREE

`python -m pytest lib/research/harvest/tests/ lib/opal_data_harvest/ -rf` -> **`3 failed, 306 passed`**. But the
three are **THREE FAILURE RECORDS ACROSS TWO DISTINCT TESTS**:

| test | records | error |
|---|---|---|
| `test_verification.py::Tests::test_disabled_barrons_contract_defers_before_opening_a_browser` | 1 | `FileExistsError: [WinError 183]` |
| `test_worker.py::Tests::test_single_broken_dow_jones_article_is_skipped_but_repeated_server_failure_stops` | **2 (SUBFAILED failures=1, then failures=2)** | `AttributeError: 'NoneType' object has no attribute 'get'` |

**pytest counts each SUBTEST failure separately.** So "3 red tests" -- the phrase carried since round 7's row
`Z-W21-S2`, repeated in `w-1`'s order, in my packet and in the analysis -- **names one test twice.** This is the
banked shape: **N failures is not N CAUSES; print the signature distribution.** Nobody had grouped them.

**Cross-check that the run is sound:** 306 passed here vs the worker's 292 at its own vintage, and `w-3` added
14 tests. 292 + 14 = 306. The denominators agree.

## TEST A -- `WinError 183`: FILESYSTEM STATE, and NON-DETERMINISTIC

`w-1`'s AC2 ran it **twice** and it **alternated** between `KeyError: 'bundle'` and
`FileExistsError: [WinError 183] Cannot create a file when that file already exists` **with no intervening
edit.** So it is not a fixed assertion failure -- it is leftover state from a prior run being re-created.
**A single run records one face as "the" failure and sends the next reader after the wrong cause**, which is why
the two-run control mattered. **A repair here is a fixture/teardown change, not a logic change.**

## TEST B -- `AttributeError` at `publishers.py:672`: A TEST-DOUBLE GAP, and a SEPARATE latent brittleness

```
lib/opal_data_harvest/publishers.py:672  (class DowJones.check)
value = self.session.get(self.base + "/client?legacy=false", headers={...}).json()
if value.get("isLoggedIn") is not True: ...
```
`.json()` returns **None**, so `.get` raises. **Cause: the failing test's fake session has no handler for the
`/client?legacy=false` auth-check URL, while its SIBLING tests all provide one** -- `test_bronze_capture.py:285`
(`_Resp(b'{"isLoggedIn": true, "type": "subscriber"}', url=".../client?legacy=false")`), `:296` for barrons, and
`test_retrieval_provenance.py:239`. **`DowJones.check()` is behaving correctly; the DOUBLE is incomplete.**

⚠ **AND A SECOND, DIFFERENT FINDING THAT MUST NOT BE FOLDED INTO THE FIRST:** `:672` calls `.json()` **with no
guard**, so a real non-JSON or empty body would raise this same `AttributeError` **instead of the clean
`AuthExpired` the method exists to raise.** That is a PRODUCT brittleness on a live auth path, independent of the
test gap. **Fixing the double makes the test green and leaves that standing** -- so a repair cell that only
fixes the double must say so rather than let a green column imply the guard exists.

## WHAT THIS MEANS FOR THE ROUND-9 CUT

1. **Two repairs, not three, and they are DIFFERENT CLASSES** -- a fixture/teardown fix (A) and a test-double
   completion (B). Neither is in `w-1`'s delivered write surface.
2. **Neither was ever `w-1`'s to fix.** `w-1`'s AC2 was a REGRESSION BASELINE and both failures pre-date it; the
   cell was explicitly told to report them rather than force them green, and it did, altering **0 assertions**.
3. **The `.json()` guard is a third item and a product change**, not a test change. It needs its own criterion or
   its own row, and it should not ride a test repair.
