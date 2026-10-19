# IB-cw-4 notes (worker 0.9.0_WK_IRPT_BCKEND~460)

**The change.** `directory_runner.py` gains `rekeyed_keys(previous_entries, entries)`, placed just above
`carry_forward_removed`. A previous key the build lacks is retained when all of its previous entries name account ids
and the union of those ids is non-empty and a subset of ONE current entry's account ids; the function returns the
retained keys sorted and unique. `carry_forward_removed` drops retained keys from the gone set before the source test,
so a retained key is neither held nor carried TERMINATED, also when `source_ids` is None. Its signature and 2-tuple
return are unchanged. `run_firm` adds one line after the `carry_forward_removed` call:
`carry_info["rekeyed"] = len(rekeyed_keys(body.get("entries") or [], entries))`. Nothing else in `run_firm` changed.
The new test file holds the eight named tests. No other source file, no AWS, no S3, no deploy, no push.

**Interpretation (surprise row IRPT_BCKEND-D2-W460-S2).** Rule 1's union over all previous entries and rule 3's
"account-less previous entry is NOT retained" disagree for a key with one account-less entry. The code treats any
account-less previous entry of a key as making that key not retained.

**Test counts, folder `data/assets/scripts/gold/investor_reporting/tests`.**
- Before: 108 failed, 401 passed, 1 error.
- After: 108 failed, 409 passed, 1 error (+8 passed, the new file).
- Failing and error set: identical before and after (109 ids; diff empty; sets in `.scratch/base_fail_460.txt` and
  `.scratch/after_fail_460.txt`, scratch only).
- The neighbouring runner tests (`test_directory_runner_terminated.py`, `test_directory_runner_refuse_drop.py`): 27 passed.

**Criteria.** AC1 PASS (8 of 8 named tests pass). AC2 FAIL before the commit by construction: it diffs committed
`HEAD~1` against `HEAD`, which is still the base until the commit (surprise row IRPT_BCKEND-D2-W460-S1). Its post-commit
verdict is reported in the worker report. AC3 is run after the commit.

**Controls.** Mutant: retention disabled (`retained = set()`, an in-place edit restored byte-equal, verified by cmp):
2 failed, 6 passed; the two failing tests are the retained-key and missing-source tests, so the rule is what they
grade. Determinism: the new file run twice, 8 passed both times.
