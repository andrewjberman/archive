# ADVI_FIRMBKTS round 8 -- eight proof instances copied under the order's whole-stem name (`2.0.0_SA_COO~B1`, 2026-10-16 ~17:0xZ)

**What happened.** `python .tools/round-close-check.py --project ADVI_FIRMBKTS --round 8` read `proof_ok=0 proof_bad=8`, verdict REFUSED, with eight lines `no proof instance named <whole order stem>.proof_of_spec.json under deliverables/`. The check finds an instance by the order's WHOLE file stem (`.tools/round-close-check.py` `proof_state`: `deliverables/*/<stem>.proof_of_spec.json`). The round-8 order faces, written by this seat, told their executors to write the instance as `ADVI_FIRMBKTS.TO-FB-<id>.proof_of_spec.json`, without the slug. All eight executors followed the face; the instances exist, are committed, and passed their own checker. The defect is the issuer's (this seat's order text), not the executors'.

**The remedy, and its bound.** For each of the eight orders, a BYTE-IDENTICAL copy of the executor's committed instance is placed in this seat's own folder under the whole-stem name. No executor's file is moved, edited or deleted; no instance content is authored or changed here. The check's structural limb then reads each copy's `to_id`, that every criterion has an acceptance row, and that no row is FAIL, which is the same content the executor produced. Result after the copies: `proof_ok=8 proof_bad=0`, verdict MAY-CLOSE.

| order stem (after `ADVI_FIRMBKTS.`) | source instance (under `deliverables/`) @ last commit touching it | sha256 (first 16) of source = copy | bytes |
|---|---|---|---|
| `TO-FB-l-1.move-plan-inflection` | `0.9.0_WK_ADVI_FIRMBKTS~81/ADVI_FIRMBKTS.TO-FB-l-1.proof_of_spec.json` @`98815701f7` | `8bf2f69034bf3cb4` | equal |
| `TO-FB-l-2.move-plan-cottonwood` | `0.9.0_WK_ADVI_FIRMBKTS~82/ADVI_FIRMBKTS.TO-FB-l-2.proof_of_spec.json` @`515e60fe4c` | `993548a05a383a77` | equal |
| `TO-FB-l-3.retirement-census` | `0.9.0_WK_ADVI_FIRMBKTS~83/ADVI_FIRMBKTS.TO-FB-l-3.proof_of_spec.json` @`42b428e9b1` | `ce7b498ecb763d4f` | equal |
| `TO-FB-l-4.one-real-retirement` | `0.7.0_AE_CloudOps~FB1/ADVI_FIRMBKTS.TO-FB-l-4.proof_of_spec.json` @`4618ae2254` | `c7137e439d282217` | equal |
| `TO-FB-l-5.first-moved-trigger` | `0.7.0_AE_CloudOps~FB1/ADVI_FIRMBKTS.TO-FB-l-5.proof_of_spec.json` @`b8b7754645` | `4b9f8d498ccaf0ec` | equal |
| `TO-FB-m-1.readiness-halt-guard` | `0.9.0_WK_ADVI_FIRMBKTS~84/ADVI_FIRMBKTS.TO-FB-m-1.proof_of_spec.json` @`478097d425` | `f16900b4ea826417` | equal |
| `TO-FB-m-2.deploy-readiness-halt` | `0.7.0_AE_CloudOps~FB1/ADVI_FIRMBKTS.TO-FB-m-2.proof_of_spec.json` @`a93a84d45d` | `eb8ca7277a78117c` | equal |
| `TO-FB-n-1.trade-form-fence-apply` | `0.7.0_AE_CloudOps~TF/ADVI_FIRMBKTS.TO-FB-n-1.proof_of_spec.json` @`2185cb53bd` | `a8cfef769c1c7f2f` | equal |

Copies live at `org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables/2.0.0_SA_COO~B1/<order stem>.proof_of_spec.json`.

**Not established by this act.** That each instance's criteria were met: that is the executor's grader run and, for the WORLD orders, the issuer's and the CTO's reads (`FB-n-1` and `FB-l-5` have their own read records in `ledger/`). The close check run was the structural mode, as for round 7; `--deep` was not run.

**Going forward.** Every order face this seat cuts names its instance by the order's whole file stem. This is the defect's only fix on the issuer's side; the check was right.
