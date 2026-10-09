# Account-id census -- ADVI_COTBKF files committed 2026-10-09 (CTO msg 3626)

**Issuer:** `2.0.0_SA_COO~C2` | **Read:** ~16:1xZ at HEAD | **Lists file paths and COUNTS only -- no account id is reproduced here.**

- **Denominator:** 327 files committed today in COTBKF scope (`ADVI_COTBKF`, `commonwealth_*`, `data/cot/`, the irpt `sources.json`, `legacy_addresses`); 324 present at HEAD.
- **Pattern:** Commonwealth/cot account-id shapes `[A-Z0-9]{2}[A-Z]\d{6}`, `[A-Z]\d{8}`, `\d[A-Z]{2}\d{6}`, `[A-Z]{3}\d{6}`. A spot check of the code hits confirms they are real account numbers (e.g. sweep-list and trace accounts).
- **Hits after the removal @ec17302888:** 73 files, 209 distinct ids.

## Already removed (same class as the CTO's @cb16f8b2f9)

- `deliverables/0.9.0_WK_ADVI_COTBKF~74/ard_cottonwood_manifest.json`: by the CTO @cb16f8b2f9.
- `deliverables/0.9.0_WK_ADVI_COTBKF~70/ard_cottonwood_manifest.json` and `~66/ard_cottonwood_manifest.json`: by the issuer @ec17302888. Bytes are kept at `C:/dev/_cotbkf_private_evidence_20261009/~70` and `~66`.

## Remaining hits, by class (a ruling is needed; the removal as worded is not feasible for every class)

| ids | file | class |
|---|---|---|
| 99 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~62/sweep_regrade.md` | deliverable / record |
| 82 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~53/run1_pre_continuity/sweep_regrade.md` | deliverable / record |
| 81 | `org/missions/D8/ADVI/ADVI_COTBKF/surprise-channel/investigations/INVESTIGATION_v1.md` | surprise-channel (append-only) |
| 80 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~53/sweep_regrade.md` | deliverable / record |
| 75 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~47/unlisted/sweep_regrade.md` | deliverable / record |
| 72 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~47/dividends/sweep_regrade.md` | deliverable / record |
| 71 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~47/levels/sweep_regrade.md` | deliverable / record |
| 70 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~48/asf/sweep_regrade.md` | deliverable / record |
| 70 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~48/census/sweep_regrade.md` | deliverable / record |
| 70 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~50/sweep_regrade.md` | deliverable / record |
| 70 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~52/sweep_regrade.md` | deliverable / record |
| 70 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~54/sweep_regrade.md` | deliverable / record |
| 63 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/PRICE_NEED/COTTONWOOD_PRICE_NEED_RANKED.csv` | deliverable / record |
| 45 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~48/census/nonmatch_census.md` | deliverable / record |
| 45 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~50/diff_trace.md` | deliverable / record |
| 45 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~54/diff_trace.md` | deliverable / record |
| 7 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~47/ADVI_COTBKF.TO-CB-y-2.carried-levels.proof_of_spec.json` | deliverable / record |
| 6 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~62/ADVI_COTBKF.TO-CB-ah-2.as-traded-basis-build.proof_of_spec.json` | deliverable / record |
| 5 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~62/evidence_four_months_schb_schz.txt` | deliverable / record |
| 5 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/ADVI_COTBKF_ROUND_25_DRAIN_END_20261009.md` | deliverable / record |
| 5 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/EXDATE_REQUEST_DELL1_DATA_QUEUE_20261009.md` | deliverable / record |
| 4 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~48/asf/asf_source.md` | deliverable / record |
| 4 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~62/ac2_dry_run.log` | deliverable / record |
| 4 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/ADVI_COTBKF_ROUND_28_DRAIN_END_20261009.md` | deliverable / record |
| 4 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/ADVI_COTBKF_ROUND_34_DRAIN_END_20261009.md` | deliverable / record |
| 4 | `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_ADVI_COTBKF_ROUND_24_20261009.md` | other seat file |
| 3 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.7.0_AE_CloudOps~CB2/fwd3_astraded_remint.md` | other seat file |
| 3 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~53/ADVI_COTBKF.TO-CB-ab-1.split-dvr-inkind-repair.proof_of_spec.json` | deliverable / record |
| 3 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~53/ac4_dry_run.txt` | deliverable / record |
| 3 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_R34_FWD3_ASTRADED_REMINT_COO_HALF.md` | deliverable / record |
| 3 | `org/missions/D8/ADVI/ADVI_COTBKF/surprise-channel/remediations/REMEDIATION_v19.md` | surprise-channel (append-only) |
| 3 | `org/missions/D8/ADVI/ADVI_COTBKF/surprise-channel/remediations/REMEDIATION_v26.md` | surprise-channel (append-only) |
| 3 | `org/missions/D8/ADVI/ADVI_COTBKF/task-orders/ADVI_COTBKF.TO-CB-ab-1.split-dvr-inkind-repair.md` | deliverable / record |
| 2 | `data/assets/scripts/silver/commonwealth_div_dating_trace.py` | code |
| 2 | `data/assets/scripts/silver/commonwealth_scale_trace.py` | code |
| 2 | `data/assets/scripts/silver/commonwealth_sweeps.py` | code |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/decompositions/ADVI_COTBKF_DECOMP.round30.md` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.7.0_AE_CloudOps~CB2/fwd3_serve_mint.md` | other seat file |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~49/ENDPOINT_READ_20261009.md` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~50/ADVI_COTBKF.TO-CB-aa-1.trace-512.proof_of_spec.json` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~54/ADVI_COTBKF.TO-CB-ab-3.trace-at-committed-cap.proof_of_spec.json` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~55/ADVI_COTBKF.TO-CB-ac-2.dividend-dating-trace.proof_of_spec.json` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~55/div_dating_trace.md` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~57/ADVI_COTBKF.TO-CB-ad-1.scale-factor-trace.proof_of_spec.json` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~57/scale_trace.md` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R27_FWD3_SERVE_CTO_HALF.md` | other seat file |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/ADVI_COTBKF_ROUND_29_DRAIN_END_20261009.md` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/ADVI_COTBKF_ROUND_30_DRAIN_END_20261009.md` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/NEVER_WIDEN_R27_FWD3_SERVE_COO_HALF.md` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/ROUND_30_DRAFT_20261009.md` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/surprise-channel/remediations/REMEDIATION_v20.md` | surprise-channel (append-only) |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/surprise-channel/remediations/REMEDIATION_v21.md` | surprise-channel (append-only) |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/task-orders/ADVI_COTBKF.TO-CB-ac-1.fwd3-serve-mint.md` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/task-orders/ADVI_COTBKF.TO-CB-ac-2.dividend-dating-trace.md` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/task-orders/ADVI_COTBKF.TO-CB-ad-1.scale-factor-trace.md` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/task-orders/ADVI_COTBKF.TO-CB-ae-1.split-level-probe.md` | deliverable / record |
| 2 | `org/missions/D8/ADVI/ADVI_COTBKF/task-orders/ADVI_COTBKF.TO-CB-y-2.carried-levels.md` | deliverable / record |
| 2 | `org/tier1_exec/3.0.0_SA_CVO/deliverables/ADVI_COTBKF_ROUND_28_L9_GRADE_20261009.md` | deliverable / record |
| 2 | `org/tier1_exec/3.0.0_SA_CVO/deliverables/ADVI_COTBKF_ROUND_29_L9_GRADE_20261009.md` | deliverable / record |
| 1 | `data/assets/scripts/silver/commonwealth_asf_source.py` | code |
| 1 | `data/assets/scripts/silver/tests/test_commonwealth_asf.py` | code |
| 1 | `org/missions/D8/ADVI/ADVI_COTBKF/decompositions/ADVI_COTBKF_DECOMP.round29.md` | deliverable / record |
| 1 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~48/ADVI_COTBKF.TO-CB-z-1.asf-source.proof_of_spec.json` | deliverable / record |
| 1 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~52/ADVI_COTBKF.TO-CB-aa-3.fwd3-serve-builder.proof_of_spec.json` | deliverable / record |
| 1 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~52/dry_run_ac2.log` | deliverable / record |
| 1 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~52/fwd3_manifest.json` | deliverable / record |
| 1 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~53/fwd3_build.txt` | deliverable / record |
| 1 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~62/ac2_build_run.log` | deliverable / record |
| 1 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~65/bond_custodian_price.md` | deliverable / record |
| 1 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/ADVI_COTBKF_ROUND_26_DRAIN_END_20261009.md` | deliverable / record |
| 1 | `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/AMLP_CONSUMER_READ_MDPF_DEMQUE_20261009.md` | deliverable / record |
| 1 | `org/missions/D8/ADVI/ADVI_COTBKF/surprise-channel/adjudications/ADJUDICATION_v28.md` | surprise-channel (append-only) |
| 1 | `org/missions/D8/ADVI/ADVI_COTBKF/task-orders/ADVI_COTBKF.TO-CB-y-1.unlisted-types.md` | deliverable / record |

## Why the issuer stops and asks (ADDENDUM 18: infeasible as worded = STOP and ask)

- **Surprise channel:** `INVESTIGATION_v1.md` (and REMEDIATION files) is append-only. The row gate refuses in-place edits, so a removal there is not a seat's act.
- **Code:** the `commonwealth_*.py` scripts and their tests embed accounts as rule data or test fixtures (e.g. the sweep list, the traced months). Removing them changes behaviour, so each needs a replacement such as an external fixture file referenced by sha256.
- **Other seats' files** (the CTO's round analysis, the CloudOps reports) are outside this lane.
- **History:** every listed file is already on origin and CLOUD. Untracking does not remove history, and a history purge is destructive git, Andrew's act.
- **The deliverable reports** (`sweep_regrade.md`, `diff_trace.md`, `nonmatch_census.md`, the price-need CSV, the proof instances) are this project's own records. They can be redacted to counts or moved outside the repo by sha256 reference. That is a project-wide cell, not a one-tick removal.
