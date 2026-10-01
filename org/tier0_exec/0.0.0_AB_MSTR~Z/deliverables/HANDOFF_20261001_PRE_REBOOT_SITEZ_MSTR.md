# 0.0.0_AB_MSTR~Z pre-reboot handoff -- 2026-10-01

Session: 2026-09-29 crash recovery through the 2026-10-01 pre-reboot parity. Andrew-direct: "you and MSTR~Z working
out a clean /integrate parity into a reboot" (relayed by laptop 0.0.0_AB_MSTR, bus 1a6a0ec8).

## Parity (fill the final hash at the last commit)

- Step 2: origin/CLOUD 1b05464432 -> 85159f8d1c and origin/DEV 970d5c75 -> b336b141, both pushed by site Z (ls-remote read).
- Final round: laptop pushed 4053e6c255 then 171bcc4da8; site Z merged both (9346dacc9f, 21017fbccc; 0 dropped) after
  2.0.0_SA_COO~RV and 2.0.0_SA_COO~O exited (02:56:03Z). This file's commit is the last site-Z commit before the reboot;
  both devices read one origin/CLOUD hash after it. portal DEV b336b141 == origin/DEV on site Z.
- Read-only plans at 9346dacc9f: opal-assets No changes; mdpf-pipeline No changes; opal-gateway 0 destroy / 7 add.
- Open deploy entries at HEAD opened 09-30: site Z's etfs-rivalfunds-round2 (ETFS_RIVALS, stays OPEN with its state
  written @4f67a6cc80); the other five are laptop seats' (COO~P x2, COO~M x2, CRO mdpf_taxsma-tx-r-1).
- Capacity research for Andrew (Dell expansion) sent on the bus at 02:5xZ (efa8ffe1); scripts in session scratch only.

## Standing holds the next session must keep

- Gateway Terraform (`infra/aws/terraform/opal-gateway`) and gateway releases are applied from SITE Z ONLY.
  Andrew-direct ~02:0xZ; record
  `org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261001_020xZ_GATEWAY_TF_TO_SITEZ_TAXSMA_FINISHES_ON_LAPTOP_CRO_CHECKPOINT_THEN_REBOOT.md`.
- `mdpf-pipeline` and `opal-assets` are driven from the LAPTOP by 4.0.0_SA_CRO (MDPF_TAXSMA). Before any site-Z apply
  of either, pull origin and read-only plan; an apply from a tree missing the laptop's commits deletes or rolls back
  live resources (four instances of this class 2026-09-30/10-01).
- Read-only plan form: `terraform plan -lock=false -input=false`; opal-gateway needs
  `-var mcportal_owner_key_claim=... -var mcportal_owner_key=...` placeholders; never keep a plan output file.

## Open items routed, not owned here

- MDPF_TAXSMA TX-r-2 (gateway release with the Tax route, capability OFF):
  `org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/4.0.0_SA_CRO/SITEZ_GATEWAY_RELEASE_REQUEST_TX-r-2.md`, routed to
  1.0.0_SA_CTO~O at 02:19Z; Andrew may park it across the reboot.
- NFRA_MCPMSP-Z-W2-S3 (safe-apply ignores -target): relayed to laptop 1.0.0_SA_CTO, the gate owner; ruling pending there.
- opal-gateway plans 7 to add (NFRA_MCPINDEX bd_read and firm-deny config, not yet applied): the owning round's act.

## Device state

- Python: site Z standardized on 3.14 (Andrew "go 3.14", record ANDREW_DIRECT_20260930_17xxZ_GO_PYTHON_314_SITEZ.md);
  3.11 kept for blpapi, kuzu and great_expectations, and scheduled tasks pin the 3.11 full path.
- Disk: 122G free of 474G after the crash cleanup (record ANDREW_DIRECT_20260929_1755Z_POST_CRASH_RESIDUE_CLEANUP_AND_WORKTREE_ASSESSMENT.md).
- On relaunch: /watcher 0.0.0_AB_MSTR~Z, then /agentbus (one consumer per device).
