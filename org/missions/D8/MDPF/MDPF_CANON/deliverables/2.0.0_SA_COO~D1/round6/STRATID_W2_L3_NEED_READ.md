# MDPF_STRATID W2 L3 -- what it actually needs from the runner (fork of 2.0.0_SA_COO~D1, 2026-10-13 ~11:3xZ)

Read-only. Input: CTO msgs 4773 and 4776 ("Read W2 L3's actual need; Stage 6 output means M10, an import path means a named-file lib sync").
Searched: `org/missions/D8/MDPF/MDPF_STRATID/` (ledger/ 4 files, task-orders/ W2 set, decompositions/MDPF_STRATID_DECOMP_W2.md, deliverables/2.0.0_SA_COO~S1/,
surprise-channel/investigations/INVESTIGATION_v1.md), `org/critical_paths/.open_deploys/mdpf-stratid-w2-wiring-silver.json`, the dispatch
`infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh`, `data/assets/scripts/gold/build_cottonwood_mdpf_slice.py`, and head/list reads of
`s3://opal-data-mdpf/code/scripts/{silver,assets_gold,gold}/`.

## 1. What "W2 L3" is

- A leg of deploy ledger `mdpf-stratid-w2-wiring-silver` (sentinel `.open_deploys/mdpf-stratid-w2-wiring-silver.json`, status HELD-SOVEREIGN-GATED, device dell1,
  author `0.7.0_AE_CloudOps~DELL1`). Its text (sentinel legs[2]):
  - kind `verify`; target: "next scheduled MDPF run after L2: the slice path reads the S3 list and serves the same figures";
  - proof_required: "runner log shows no strategy-config error; served Cottonwood by_model sma members equal the prior run's member set"; proof null.
- Owner: `2.0.0_SA_COO~S1` (the issuer's read of a scheduled run, not an act of the applier; `TO-APPLY-W2-b` division of labour, sentinel `gate.ref`).
  L1 and L2 are CLOSED with proof (matcher first-mint 15:05:53Z, schemas 15:06:59Z, both sha256 equal to `ff8b8452f0`).
- It has TWO halves:
  - served half: the served Cottonwood by_model sma member set equals the prior run's. READ AND EQUAL (0 of 493 cells differ, row D1-S10 `world_is`;
    `L8_PACKET.round2.partial.md:134`; `R2_RUN_READ_20261012.md:57`);
  - runner-log half: a runner dispatch log that shows no strategy-config error. OPEN.

## 2. What the runner-log half needs

The line that says so: `INVESTIGATION_v1.md:580` (row D1-S10 `world_is`): "L3 re-points to the first dispatch whose log carries '6d COTTONWOOD legs
complete' or a 6d error line, which needs S5 disarmed first." and `L8_PACKET.round2.partial.md:136-137`: "L3's runner-log read un-parks when that sync makes
Stage 6 reach 6d; the reader is this seat, the first dispatch after the sync is the read."

What executes on the runner and loads the S3 strategy list: step 6d (`mdpf-daily-dispatch.sh:547-556`), `build_cottonwood_mdpf_slice.py --upload`, which
imports `rebalancer_schemas` (:124) and `opal_unidentified` (:132) and, through them, `opal_strategy_matcher` (:1256) reading
`s3://opal-data-etfs/config/etf_universe.json` (`TO-W2-2:49`). No other dispatch step runs the slice (grep of the dispatch for
`build_cottonwood_mdpf_slice|rebalancer_schemas|opal_strategy_matcher|etf_universe`: 3 hits, all in 6d's comment and call; denominator 1 file).

6d is reachable only through `revamp_stage()`, which runs 6a, 6b, 6c in order with `|| return 1` before it. So the runner-log half needs a dispatch in which 6a, 6b
and 6c have passed. That is NOT an import-path problem alone:
- 6a dies at `lib.opal_naming` today (14 logs since 2026-09-21), and behind it at C2 AccessDenied `s3:ListBucket` on `opal-data-assets` and the cross-axis gate
  (`TAXSMA_S5_STAGE6_READ.md` @7de2c1aa99, last green Stage 6 2026-08-14);
- 6d's own slice has the same chain at run time: `build_cottonwood_mdpf_slice.py:1209` imports `dim_mdpf_aggregate_aua_timeseries`, which imports
  `taxsma_assets` (`:76`), which imports `lib.opal_naming` (`:95`). A named-file lib sync is necessary for 6d and not sufficient.

## 3. Which of (i), (ii), (iii)

- (i) Stage 6 output: TRUE for the runner-log half AS WRITTEN. The input is a dispatch whose Stage 6 reached 6d. That is Stage 6 resuming, which the CTO
  has ruled is M10's work, not a sync.
- (ii) `lib.opal_naming` importable: NECESSARY (6a and 6d's :1209), NOT SUFFICIENT: two more failures stand behind it (C2 AccessDenied, the cross-axis gate on the
  runner's older code).
- (iii) neither: TRUE FOR THE OUTCOME L3 VERIFIES ("the slice path reads the S3 list and serves the same figures"), which is already shown without the runner:
  - the production Cottonwood slice is built by the gold lambda (`run_cottonwood_family`); its run read the S3 list and served the same members
    (`R2_RUN_READ_20261010.md:36`, `R2_RUN_READ_20261012.md`);
  - the in-memory QA ran the DEPLOYED silver bytes from `code/scripts/silver/` through `build_composed(s3)` against live S3:
    `STRATEGY_CONFIG_SOURCE = s3://opal-data-etfs/config/etf_universe.json`, 16 of 16 keys equal, 0 model_value differences, verdict L3-QA PASS
    (`L3_ADHOC_QA_SILVER_WIRING_20261009.md:26-34`; the page itself says the scheduled run stays the acceptance).

## 4. Already satisfied another way, or waiting on?

- Served half: satisfied (above).
- Runner-log half: not satisfied by anything, and cannot be satisfied by the lib sync. The one open input is a dispatch log carrying the 6d line.
- The silver/gold modules the slice needs are in place: `code/scripts/silver/` holds `rebalancer_schemas.py`, `opal_strategy_matcher.py`,
  `opal_unidentified.py` (row D1-S7's absent module is now present); `code/scripts/assets_gold/` holds `build_cottonwood_mdpf_slice.py`. So 6d's own
  module set resolves; what stops it is upstream (6a) and :1209.

## 5. Owner and state

`2.0.0_SA_COO~S1` reads L3 (ledger `mdpf-stratid-w2-wiring-silver`, entry `org/critical_paths/change_management/20261009T1444Z_mdpf-stratid-w2-wiring-silver_deploy_completion.md`);
the sentinel is HELD, window held, nothing owed by the applier. `L8_PACKET.round2.partial.md:135-137` records S5 re-owned to `2.0.0_SA_COO~D1` (CTO msg
4774) with L3 parked "until the sync makes Stage 6 reach 6d".

## 6. The minimum act, stated plainly

- To satisfy L3 AS WRITTEN: Stage 6 must reach 6d on a scheduled dispatch. That is the full revival (nine keys under `code/scripts/gold/`, an IAM change on
  `mdpf-daily-runner-ec2-role` for `s3:ListBucket`, the runner's older code against today's inputs, and a priced change of the frontier counts). The CTO's
  ruling (msg 4776) says no revival: the dispatch chain retires at M10.
- To satisfy L3's INTENT without a runner act: the ledger leg's owner (S1) re-scopes the runner-log half as EXCLUDED-BY-ORDER with Stage 6 (as the CTO did for
  FWD-5's stage-6 readers), closing L3 on the served half plus the in-memory QA, and un-parks the runner-log read at M10. That is a ledger amendment, not a
  runner act; it is S1's and the CTO's to make, not this seat's.
- A named-file lib sync (nine keys) alone changes nothing about L3: 6a still dies at C2 before 6d.
