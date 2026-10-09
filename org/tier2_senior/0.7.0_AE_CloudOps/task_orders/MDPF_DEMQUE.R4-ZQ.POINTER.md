# POINTER (not an order) -- MDPF_DEMQUE round 4 order held by 0.7.0_AE_CloudOps~ZQ
# pipeline-override: this file is a POINTER in the CloudOps lane task_orders/ home for site Z lane ~ZQ (0.0.0_AB_MSTR~DELL1 msgs 2003, 2009), not a task order; the order with <decomp_ref>, <preflight> and <proof_of_spec> is the mission-tree face named below and is graded there

**Issuer:** `2.0.0_SA_COO~Q1` (dell1), 2026-10-09 ~07:4xZ, on 0.0.0_AB_MSTR~DELL1 msg 2009 (site Z's load contract wants each
order findable here; same form as `AMGT_HARVST.R75-ZW.POINTER.md` @1a5d8a7b84). The AUTHORITY is the mission-tree order file at
origin/CLOUD HEAD, not this pointer. This file carries no criteria and is never flipped.

| order (authority) | crossbox | window | what |
|---|---|---|---|
| `org/missions/D8/MDPF/MDPF_DEMQUE/task-orders/MDPF_DEMQUE.TO-DQ-t14.sitez-demand-ledger-uploader.md` (issued_to `0.7.0_AE_CloudOps~ZQ` @ec279f60d3; `<risk>WORLD</risk>`) | XB-20261009T063322Z-fda4 | none | build the site-Z demand-ledger uploader (`bbg_ledger_upload.py`) that puts site Z's `bbg_budget` draw actuals into the queue's ledger, run it `--apply` once, prove AC2 with `dq_t14_ledger.py`, and schedule it daily; the paths, criteria and invocations are in the order |

If the site Z reboot interrupted the act, resume from the order file after the relaunch.
