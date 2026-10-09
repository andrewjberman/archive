# ADVI_BILLING -- proposed SURFACE MANIFEST for PRD v0.1 (from the round-1 decomposition)

Proposed by `2.0.0_SA_COO~B2` 2026-10-09 for `1.0.0_SA_CTO~DELL2` to place in the PRD as a top-level `## SURFACE MANIFEST`
section. The issuance of round 1 is refused by `.tools/to-pipeline-gate.py` LIMB (c) until the PRD carries one. Every row is taken
from `decompositions/ADVI_BILLING_DECOMP.md` section 0 (measured 2026-10-09) and builder output (rule 30). It adds no outcome and
changes no ENDPOINT text.

## SURFACE MANIFEST

| surface | kind | location | access | owner | serves |
|---|---|---|---|---|---|
| Schwab 0833 positions/values | S3 silver (read) | `s3://opal-data-assets/schwab/08335338/silver/fact_rps/` | read | ADVI 49F runners | FWD-1, FWD-3 |
| Schwab 0833 transactions (TPFEE, SMFEE debits) | S3 silver (read) | `s3://opal-data-assets/schwab/08335338/silver/fact_trn/` | read | ADVI 49F runners | FWD-1 |
| 49F flow ledger | S3 gold (read) | `s3://opal-data-49financial/gold/advi/canonical/flow_ledger/` | read | ADVI 49F runners | FWD-1, FWD-3 |
| 49F households | S3 gold (read) | `s3://opal-data-49financial/gold/advi/dimensions/dim_relationship/` + crosswalk `rel_to_z_mapping.json` | read | ADVI 49F runners | FWD-1 |
| Black Diamond fee lines (secondary reference, C-SHAPE) | S3 silver (read) | `s3://opal-data-bd/silver/fees/` | read | BD silver pipeline | FWD-1, FWD-4 |
| SMArtX statements, Opal Billing Master | SharePoint (read, by a seat) | `Shared/Documents/Billing/` | read | Opal operations | FWD-1, FWD-2, FWD-5 |
| Fee recompute | code (new) | `data/assets/scripts/gold/advi_billing/fee_quarter.py` | write | ADVI_BILLING | FWD-1 |
| Fee-quarter object | S3 gold (new) | `address("advi","49financial","gold","advi_billing","quarter=<q>","<client_key>.json")` | write | ADVI_BILLING | FWD-1, FWD-3 |
| Seam contract | standard (new) | `org/standards/ADVI_BILLING_FEE_QUARTER_CONTRACT.json` | write | ADVI_BILLING | FWD-1, FWD-3, FWD-4 |
| Read route | Lambda + API route (new) | `name("advi","49financial","billing-read","lambda")` = `advi-49f-billing-read-lambda`; `GET /api/scoped/partners/books/relationship/{clientKey}/fee-quarter/{quarter}`; root `infra/aws/terraform/advi/billing-read/` | write (apply by the issuer) | ADVI_BILLING | FWD-1, FWD-3 |
| Advisor fee panel | portal (new files; DEV only, client-facing page) | `portal/src/pages/AdvisorIntelligence/_shared/AdvisorBookFeePanel.tsx`, `portal/src/api/endpoints/advi-billing.ts` | write | ADVI_BILLING | FWD-1, FWD-3 |
| Schwab fee file | file (later round) | not yet placed | write, never uploaded (C-NO-UPLOAD) | ADVI_BILLING | FWD-5 |
