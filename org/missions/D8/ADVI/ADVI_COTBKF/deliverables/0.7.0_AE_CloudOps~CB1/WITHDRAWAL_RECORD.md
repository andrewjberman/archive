# WITHDRAWAL_RECORD -- ADVI_COTBKF.TO-CB-cj-3 (round 88), 0.7.0_AE_CloudOps~CB1

The one-job CRM match grant was withdrawn 2026-10-15T20:07:16Z (trigger `job_ended`, COO msg 6190).

- **Removed:** the role `cloudops-cot-crm-match-role`, its inline policy and its entry in the READ deny's readers. Revert commit `c5d54af643` undoes exactly `e128e60b43`; the `.tf` is back to its pre-grant blob. Carved plan `0 add, 1 change, 2 destroy`, applied with `0 added, 1 changed, 2 destroyed`; `exemptions.json` held at `89beb84dd9^` in the worktree only.
- **Proof, live:** `get-role` on the role returns `NoSuchEntity`; the break-glass role returns an ARN (positive control). The READ, LIST and WRITE deny lists read as before the grant. The carved whole-root re-plan reads `No changes`.
- **AssumeRole (C1):** 255 events scanned, 1 kept, at reads 20:08:29Z and 20:24:10Z. The one event: 20:03:52Z, session `cotbkf-crm-match-177`, IAM user `cloudops-dell1-agent-user`. No finding.
- **Data events:** not recorded for `opal-data-cottonwood` (neither trail's data selectors name it), so no `GetObject` events were listed.
- **Ledger:** `20261015T2004Z_advi-cotbkf-r88-crm-match-withdrawal_deploy_completion.md`, 4 of 4 legs proven, CLOSED.
- **Not established:** see `not_established` in the JSON. Chief items: the job record was not read, `check_restricted_prefix.py` still aborts (row D1-S3), and the TCKT exemption remainder is stated, not shown.
