# Site Z landmine census -- `0.0.0_AB_MSTR~Z` (bus 978b9bd5, 2026-10-01 00:52Z), asked at Andrew's direction ~00:3xZ

Asked by `0.0.0_AB_MSTR` (bus d8bc779b + addendum eacdc0bd). Verbatim reply below; the carrier adjudicates nothing.

```
[AGENTBUS -> laptop] [id 978b9bd5-7f24-4396-90c7-782ca09a4e65] [2026-10-01T00:52:11Z] [from 0.0.0_AB_MSTR~Z] CENSUS for Andrew (re d8bc779b + eacdc0bd), from 0.0.0_AB_MSTR~Z, measured 00:4x-01:2xZ. ONE LANDMINE FOUND, the mirror you predicted.

(1) site-Z CLOUD vs origin 85a765dbcd: 118 ahead / 0 behind. Site Z's own tree is not stale.

(2) Read-only `terraform plan -lock=false`, no init, from the site-Z shared tree:
- opal-assets: Plan 0 add / 0 change / 1 DESTROY -> aws_iam_role_policy.mdpf_egress_publisher_taxsma_control ("not in configuration"; inline policy mdpf-publisher-taxsma-control-read-policy on opal-assets-mdpf-egress-publisher-role, s3:GetObject on opal-data-mdpf/mdpf/global/state/taxsma_control/current.json). It is LIVE but its config exists only on your unpushed bf643a0530. LANDMINE: any site-Z apply of opal-assets before your push deletes it. Disarms when your push lands and site Z pulls.
- harvest: no changes (57 refreshed). bd-pipeline: no changes (203 refreshed).
- opal-gateway: 0 destroy, 0 replace; 6 add (bd_read role + policies + external-id secret = in-flight NFRA_MCPINDEX config not yet applied) and 1 in-place (mcportal_grant_writer source_code_hash differs from deployed). Plan needed 2 vars with no tfvars; run with placeholders that only feed Lambda env.
- mdpf-pipeline: NOT MEASURED -- "Module not installed" (iam.tf:948 module irpt_49f_directory_read_role_name); needs terraform init, not run. Your +271 Tax roles @8baf85002e stay a possible destroy until measured or pushed.
- etfs-rivalfunds: NOT MEASURED -- providers not initialized in the shared tree.
(3) ARMED surprise rows: 1357 estate-wide (comp-surprise --armed); 590 minted on site Z (id carries -Z-); 312 whose one_line names terraform/destroy/apply/stale/worktree (keyword class -- over-inclusive). Two of exactly this class: ADVI_FIRMBKTS-S2 (owner 0.0.0_AB_MSTR: a full shared-infra apply from any checkout older than 9f3fd2cf4a plans the org audit trail's DESTROY) and ETFS_POSITIONING-S3 (owner 0.7.0_AE_CloudOps: any shared-infra apply drops the live CloudFront read grant for platinum/advi/*).
(4) Open deploy-ledger entries: 21 (22 at the comp-schedule read; union across 62 trees, 113 stale worktree copies dropped, 0 worktree-only). Mostly laptop seats' (COO~P IRPT x11, COO~M SECCLASS/COT x6); site-Z: nfra-mcpindex-bd-playwright-strip (HELD), d12 SMS pair, leadpanel-price-producer-schedule.
(5) Stale-tree-shaped: of 61 site-Z linked worktrees, the tree copy differs from site-Z CLOUD in opal-gateway 56, harvest 39, bd-pipeline 39, etfs-rivalfunds 24, shared-infra 19, opal-assets 2, mdpf-pipeline 1 ("differs" = stale OR in-flight). A full apply from a stale one plans destroys exactly like the laptop's tree. Scheduled producers on site Z pin Python 3.11 by full path and run the shared tree, which is current.
ASK: push bf643a0530 (and the mdpf-pipeline Tax roles) when Andrew gives the word; until then site Z must not apply opal-assets. I am telling site-Z CTOs now.
```

## Laptop side, measured by `0.0.0_AB_MSTR` 00:4xZ

- Laptop CLOUD 881af50a86: 152 ahead / 864 behind origin 85a765dbcd; merge-tree 0 conflicts.
- Terraform roots changed on origin and absent on the laptop: etfs-rivalfunds (10 files), harvest (5), opal-gateway (4).
- Terraform roots changed on the laptop and not on origin: mdpf-pipeline iam.tf (+271, @8baf85002e, bb9a291faa), opal-assets mdpf_egress_publisher.tf (+37, @bf643a0530).
- Laptop ARMED row: MDPF_TAXSMA-S7 (disarm owner 0.0.0_AB_MSTR), disarms on the laptop pull.
