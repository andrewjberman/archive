# GRANT_RECORD -- ADVI_COTBKF.TO-CB-cj-1 (round 88), 0.7.0_AE_CloudOps~CB1

The one-job CRM match grant is LIVE as of 2026-10-15T19:49:31Z. Withdrawal: `CB-cj-3`, hard stop 2026-10-15T23:59Z.

- **Role:** `cloudops-cot-crm-match-role` (name from the `opal_name` builder, not typed). Trust: one principal, `cloudops-dell1-agent-user`; max session 3600 s; no attached managed policy; one inline policy `CrmMatchGetOneKey`.
- **Policy:** `s3:GetObject` on the one key `commonwealth/cottonwood/bronze/crm/date=2026-06-23/CRM_CottonwoodCapitalAdvisors.zip` in `opal-data-cottonwood`. No version action, list or put.
- **Bucket policy:** the role's ARN joined the READ deny's exception list only (`lgic_crm_get_readers`). The LIST deny and WRITE deny read as before, read live from the bucket policy.
- **Plan:** carved (AMENDMENT 1), `2 to add, 1 to change, 0 to destroy`; the one change is that ARN in the Cottonwood READ deny. `infra/logic/registry/exemptions.json` was held at `89beb84dd9^` in the worktree only and never committed. Live state carries no TCKT_VNEXT exemption, as before.
- **Commit:** `e128e60b43` on `box/dell1` (local at record time), landed under the CTO's lane grant `b7c6312278`; no author override.
- **Simulator (live, with the live bucket policy):** role + the one key allowed; role + another key implicitDeny; role + list implicitDeny; role + put explicitDeny; the agents' own user + the one key explicitDeny.
- **Ledger:** `org/critical_paths/change_management/20261015T1926Z_advi-cotbkf-r88-crm-match-grant_deploy_completion.md`, 4 of 4 legs proven, CLOSED.
- **Not established:** see `not_established` in the JSON. Chief items: `check_restricted_prefix.py` aborts before and after on the Inflection policy's statement count (it never reached its simulator limb); no object under the CRM prefix was read or listed.
