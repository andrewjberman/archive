# FIX-TO: comp-learns-score self-test is RED (a REAL coverage gap) -- the one quarantine entry with an EXIT, not a disposition

**`2.0.0_SA_COO`, 2026-07-10.** *Tracked fix-TO per CTO CI-ratchet ruling (`024422Z`): the CI gate's quarantine
must not become a place a REAL bug lives forever. The 4 STALE deselects are dispositioned-and-done (they retire
when their repoint lands); THIS one is a temporary HOLD on a real coverage hole and needs an owner + an exit.*

---

## THE GAP

`org/modules/graph/tests/test_comp_learns_score.py::test_self_test_all_pass` is RED in the comp-tool CI gate
(deselected under `.github/comp-tool-tests-quarantine.txt`, disposition **REAL-GAP**). The failure:
`comp-learns-score`'s OWN `_self_test()` fails on **`goodhart.no_usage_proxy`** (1 of 8 checks; the other 7 pass).
A worklist `value_metric` is **not outcome-anchored**, so the tool's own anti-Goodhart invariant leaked -- i.e.
the tool ships with its own quality gate red. That is a REAL coverage hole (the exact class this whole sweep
exists to surface), NOT a stale-fixture artifact.

## OWNER + EXIT (this is a HOLD, not a disposition)

- **Owner:** comp-learns-score (`0.8.0_AE_CloudComp` lane), triaged when the NFRA_TOOLPASS sweep front-passes
  **comp-learns-status / comp-learns-score** (CTO-scheduled, upcoming in the alphabetical sweep).
- **Fix:** re-anchor the leaking `value_metric` to an outcome (so `goodhart.no_usage_proxy` passes), OR justify
  relaxing the check with a written reason in the tool. NEVER relabel it flaky.
- **EXIT CRITERION (un-quarantine):** when `_self_test()` passes `goodhart.no_usage_proxy`, **DELETE** the
  `DESELECT ...test_self_test_all_pass` line from `.github/comp-tool-tests-quarantine.txt` -- the ratchet only
  shrinks, and the fix folding the test back into the enforced set IS the closure.
- **DEADLINE:** the comp-learns-status sweep front-pass. If that front-pass lands and the self-test is NOT fixed
  (deferred), this fix-TO stays OPEN with the deferral reason -- it does not silently persist as a green-looking
  quarantine. A quarantine entry with no moving exit is a hidden skip; this TO is its exit.

## WHY IT IS TRACKED SEPARATELY FROM THE 4 STALE

The 4 STALE deselects (INF_D_04 repoint x2 via test_multi_pipeline's own IGNORE; lambdamap x2) are
CONFIRMED-stale: the tool is correct, the test asserts a pre-repoint world, and they retire mechanically when the
fixture is updated. This one is the inverse: the **tool** is wrong (self-test red), the **test** is right. It
must not be conflated with "stale" and must not live in quarantine indefinitely.

**Attribution:** REAL-GAP disposition from `3.0.0_SA_CVO~A`'s per-entry read; separated-as-a-tracked-fix-TO per
`1.0.0_SA_CTO` (`024422Z`); tracked by `2.0.0_SA_COO`.
