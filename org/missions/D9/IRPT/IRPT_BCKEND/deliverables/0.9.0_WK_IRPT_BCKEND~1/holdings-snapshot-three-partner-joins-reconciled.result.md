# IB-s-12 RESULT -- THE HOLDINGS SNAPSHOT: three partner joins, reconciled

**TO:** `IRPT_BCKEND.TO-IB-s-12` | **worker:** `0.9.0_WK_IRPT_BCKEND~1` | **branch:** `wk-irpt_bckend-1-1`
**base commit:** `95a34541f8` (HEAD of `CLOUD` at hand-off, carrying IB-s-1's directory runner)
**This cell APPLIED infrastructure and landed real data.** 3 resources added on the shared
`directory` root, three real QA `HoldingsSnapshot` objects uploaded, one code-deploy leg
attempted and correctly BLOCKED (filed).

## Criteria

| id | verdict | invocation | deciding line |
|---|---|---|---|
| `S12-AC1` | **PASS-by-output** | `timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/battery_ib_s_12.py` | rc=0, `arms: 6 of 6 evaluated; arms holding: 6 of 6; assertions failed: 0` then `IBS12-HOLDINGS-RECONCILED` |
| `S12-AC2` | **RECORDED (judgment)** -- no verdict | evidence assembled for `3.0.0_SA_CVO` at L9 | in the proof-of-spec instance under `UNVERIFIABLE-BY-INSTRUMENT` |

Transcripts committed beside this file: `IB-s-12_S12-AC1_battery_output.txt`,
`IB-s-12_directory-root_0diff_plan_output.txt` (supplementary evidence for arm (f), not a
separate criterion -- this order names only two).

## The joins, live, real, reconciled

| firm | this cell's own join | PRD-dated figure (context) | reconciled (before == after) |
|---|---|---|---|
| 49financial | 7,453 of 7,453 map rows processed | 7,431 of 7,453 (directory cross-check) | `$1,512,877,206.80` == `$1,512,877,206.80` |
| inflection | 790 of 845 | 658 of 663 | `$189,351,736.50` == `$189,351,736.50` |
| cottonwood | 946 of 950 | **946 of 950 -- reproduced exactly** | `$474,077,865.15` == `$474,077,865.15` |

Every number above is a real read against already-landed SILVER Parquet in `opal-data-assets`
(SmartX platform silver + BD Rebalancer/cottonwood silver), `opal-data-inf` (Eclipse silver +
`accounts_v2`) -- no fixture, no synthetic data, no live vendor call.

## The join identity, empirically verified before it was relied on

`opaque_id()` reuses `directory_runner.py`'s exact formula. Verified against the REAL, already
-landed directory: 5 of 5 sampled 49F `fact_acc` account numbers reproduce an id present in the
directory's `account_ids` set (then 7,431 of 7,453 at scale). The SAME check for INF and COT
returns 0 matches -- their directory entries evidently derive from a different raw key. Changed
BEFORE any apply: the directory intersection is **informational only** (`manifest.
directory_cross_check`, never a hard gate); each firm's own natural silver-to-silver join is
the resolved-scope population. Filed as `IRPT_BCKEND-W1-S7`.

## The recursive expansion mechanism, and the mutants that proved it

`expand_model()` is this cell's own mechanism, **not** `build_dim_model_portfolio.decompose()`
-- deliberately: `decompose()` returns `[]` on a cycle hit, silently dropping the branch's
weight, which the PRD names invalid. `expand_model()` applies every edge weight EXACTLY ONCE,
retains a cycle's or a missing node's weight as UNRESOLVED MASS, and never renormalizes a
surviving sibling to compensate -- a lost 30% branch leaves the survivor at its ORIGINAL 70%.
**Four red-first mutants, 4 of 4 fired**: reintroducing `decompose()`'s invalid `[]`-on-cycle
shape failed 2 tests; disabling the never-renormalize guarantee failed 2; double-applying an
edge weight failed 2; disabling `assert_bases_not_spliced` entirely failed 1. All four restored
byte-for-byte, 22 of 22 tests green before and after.

## A real design bug the tests caught in MY OWN code, fixed rather than argued with

The first `build_inf` construction put an OBSERVED "excluded value" node and an ASSIGNED
"model" node as SIBLINGS under one account -- exactly the spliced-basis pattern S12-AC1 arm (c)
exists to refuse, and `assert_bases_not_spliced` correctly raised on my own real data (not a
fixture). Restructured so `managed`/`excluded` are two OBSERVED siblings and the ASSIGNED model
view descends from `managed` alone, in its own pie. Tested explicitly
(`test_13_inf_managed_and_excluded_are_preserved_as_separate_observed_siblings`).

## The rule-13 code deploy: attempted once, correctly BLOCKED

Per the issuer amendment, the deploy was attempted through the guard's own explicit first-mint
mechanism: `.tools/safe-deploy.sh --mint-bundle holdings_snapshot` -> `"ERROR: no bundle named
'holdings_snapshot' declared (declared: ['accrual_bridge'])"`. The ordinary push-gate path
confirms the same shape row `IRPT_BCKEND-W2-S5` measured for IB-s-1's sibling script: rc=0,
`SKIP-NOT-MEMBER ... 404 ... NOTHING WAS DEPLOYED`. The **artifact**, not the exit code, was the
oracle: `head-object s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/
holdings_snapshot.py` -> 404. Declaring a bundle requires editing `.tools/safe_deploy_core.py`,
outside this order's `<paths>`. **BLOCKED, filed as `IRPT_BCKEND-W1-S8`** -- exactly the outcome
the criterion's own text names as legitimate, and it does not withhold `IBS12-HOLDINGS-
RECONCILED`.

## Rows filed

- `IRPT_BCKEND-W1-S7` (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~B`) -- the directory-
  population cross-check resolves for 49F only; INF/COT use a different raw key this cell did
  not trace.
- `IRPT_BCKEND-W1-S8` (**BLOCKING**, ARMED, disarm owner `2.0.0_SA_COO~B`) -- the guard's
  explicit first-mint mechanism has no declared bundle for this project, and the file that
  would need one is outside every IRPT_BCKEND worker's `<paths>`.

## Bounds observed

No live vendor call anywhere -- every read is an already-landed SILVER Parquet object. No
model's global AUM (Eclipse `model_composition.model_aum`) was ever opened. No parallel
position/asset table was unioned; COT duplicates deduplicated only under the equal-value/null
policy, with one incompatible pair carried as an explicit exception (tested, not hit in real
data). `vendor_account_supervised` carried in its own field, never read as `fee_taking_status`.
The MDPF insurance-view exclusion was not touched (this cell never imports that module). No
monitor, alarm, SNS or SES send -- the schedule is applied DISABLED with an inert SQS target.
No credential in any artifact. No served output touched -- the only writes are this cell's own
new schedule resources, the three real QA snapshots, and this worker's deliverables. Every path
written is inside the order's `<paths>` grant. No existing surprise row edited.
`.tools/commit-gate.sh` rc=0 on all three `.py` files. Every invocation ran under `timeout`.
