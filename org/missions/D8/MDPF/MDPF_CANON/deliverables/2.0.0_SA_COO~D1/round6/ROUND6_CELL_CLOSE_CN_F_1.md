# MDPF_CANON round 6 -- cell close, CN-f-1 the Global min-firms fold (2.0.0_SA_COO~D1, 2026-10-12 ~19:4xZ)

Read-only record for the CVO's L8/L9 and the CTO's round-6 analysis. The cell is drained; the deploy and the served read are not done.

## 1. The cell

| item | value |
|---|---|
| order | `task-orders/MDPF_CANON.TO-CN-f-1.global-min-firms-fold.md`, status complete, AMENDMENT 1 = the CTO's ADDENDUM 6 |
| worker | `0.9.0_WK_MDPF_CANON~16`, two passes (build, then the amendment); commits 94ff221642, 2e85c2fc88, c14752be67, 21f395f985 |
| drain | merge `51cfc93ea8` (parents 49f5ac8859, 21f395f985); 9 of 9 paths in the grant, 0 dropped, 0 foreign; on origin by ls-remote |
| proof instance | `deliverables/0.9.0_WK_MDPF_CANON~16/MDPF_CANON.TO-CN-f-1.global-min-firms-fold.proof_of_spec.json`, checker VALID rc=0 |

## 2. The criteria, re-run by the issuer on the merged tree

AC1 `r6_cn_f_1.py contract` 13 of 13; AC2 `r6_cn_f_1_comparator.py` 11 of 11 (real served 2026-10-09 objects, read-only); AC3 `r6_cn_f_1.py seams` 6 of 6.
Drain hygiene: py_compile and ruff (py39) clean on the six python files; `data/mdpf/tests/canon` 20 passed; the two crosswalk homes byte-equal.
AC4 is JUDGMENT (the `/seams` on the fold-to-served seam), graded at the round close on the first folded scheduled fire; not self-graded.

## 3. What the worker found, and the dispositions the issuer proposes (rows are append-only; the CVO dispositions)

| row | one line | issuer's reading |
|---|---|---|
| `D1-W16-S1` BLOCKING | a one-firm as-of pool would leave Models short of total_aua and raise ViewPlaneError outside isolation for every scope | disarmed by AMENDMENT 1 (the as-of pool refuses Global whole before any view is built); checked by arms C11 and C13 |
| `D1-W16-S2` | aum-metrics current value falls back to the last pooled dollars when the as-of line is None | reachable only for a no-pool as-of; see S4 |
| `D1-W16-S3` INERT | the as-of roll-up total is unchanged; the delta falls on per-model rows and history | consistent with the pair's section 6 |
| `D1-W16-S4` BLOCKING (worker class) | the aum-metrics fallback (`dim_mdpf_aum_metrics.py:551-555`, "falls back to its last real value, honest to the fold's own series") still fills other_models' current value on a no-pool as-of | the standing frontier law for every line; the carried value is from a date the line was emitted at two or more firms, so it discloses no one-firm figure. Issuer reading: OBSERVATION, INERT |
| `D1-W16-S5` | the staged global aggregate is written unfolded, before the fold guard, on every run | by design: the staging tree feeds the stage-6 readers (EXCLUDED-BY-ORDER, the CTO's round-5 ADDENDUM 2); not served |

## 4. What is still owed

- Pair: CTO half (`ledger/NEVER_WIDEN_R6_CN_F_1_CTO_HALF.md`); COO half signed in `round6/NEVER_WIDEN_PAIR_R6_CN_F_1.md`.
- Deploy: `ADHOC.canon-r6-fold-deploy` (CloudOps ~DELL1), waiting on the issuer's written GO that W8-S4 is closed (the 2026-10-13 13:30Z read of CN-d-1).
- Acceptance: the first scheduled fire after the deploy that mints a new date (2026-10-14 13:30Z at the earliest), read by `round6/checks/r6_fold_readback.py`.
- D1-S18 (the commit stamp) rides that deploy's plan and is read on the same fire.
