# NFRA_OPSWKF resume packet -- the 12 open surprise rows dispositioned, the held scope named and uncut

**By:** `2.0.0_SA_COO~O2`, 2026-10-14 ~13:1xZ. **For:** `1.0.0_SA_CTO~DELL2` (round-N analysis at resume) and the CVO (fold sign-off).
**Basis:** CTO ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL2_UB151E_NFRA_OPSWKF_HOLD_UNTIL_RESUME_20261014.md` item 2
(msg 7655); Andrew-direct 2026-10-13 ~18:4xZ, verbatim: "Yes I think all of this can be folded into the OPSWKF project which we will deal with in
a couple weeks." **Resume:** ~2026-10-27, or his earlier word. This packet cuts nothing, sizes nothing, and edits no row (the channel is
append-only; the marks below are this packet's, not a row disposition).

Measured at the time of writing: PRD v0.11 both halves signed; task orders 10 of 10 complete; comp-surprise reads 12 open, 0 armed, 0 defects
(denominator: 18 investigation items, 3 adjudication rows, 1418 files). Rows live in
`org/missions/D9/NFRA/NFRA_OPSWKF/surprise-channel/investigations/INVESTIGATION_v1.md`.

## The 12 rows

| row | mark | reason and evidence |
|---|---|---|
| D2-S1 | enrichment: FWD-1 (repair batch) | pytest over trade-workflow-handler/tests: 3 errors from test_actor_identity.py's `__main__`-only fixture. No cell owned it in round 1. One small LOCAL repair at resume. Not re-run today. |
| D2-W1-S1 | no action | The typed-create `KeyError 'firm'` was OW-l-1's. The joint ticket release went live 2026-10-09 (msg 3229), and Andrew's 2026-10-13 smoke created TCK-20261013-5c5c3916 through that create path. Inferred from those two facts; the row was not re-reproduced. |
| D2-W5-S1 | no action, read first by the 409 investigator | The worker face's `type` was shorthand for `ticket_type`; no deviation. The recorded 409 ("not a trade_request ticket") is a field-or-route mismatch of the same family, so the investigator reads this row before anything else. |
| D2-W5-S2 | enrichment: FWD-1 (external trade request) | The form's firm field starts blank and an internal login's firm id is `opal-capital`. It needs the firm-scoped client and account search of the external design below. |
| D2-S2 | enrichment: FWD-1 (repair batch) | `parquet_exporter.py` imports pyarrow at module top; the function's only layer is openpyxl-layer:3 (817,805 bytes). Predates OW-d-1. Whether the import is reached on any live path is unmeasured. |
| D2-S3 | no action | `ses:DescribeConfigurationSet` for the dell2 CloudOps principal was granted by NFRA_CTLPLN amendments 29/30, applied 2026-10-09 12:21Z (msgs 3329, 3333). Taken from those messages, not re-read from IAM. |
| D2-S4 | enrichment: FWD-1, UNMEASURED | `iam:SimulatePrincipalPolicy` and `dynamodb:GetResourcePolicy` were missing on that principal when the row was filed. This packet did not read whether they have since been granted. The round-N analysis reads it first (`comp-iam`) before any deploy cell relies on a simulate. |
| D2-S7 | no action for this project | data-refresh admits firm id `opal-capital` on every route, write routes included. The owner ruled K1 stays (msg 5698); the 2026-10-12 code read (795eb0348a) extends it to every surface using the estate's rule. A fix would be the estate rule's own project, not this one. |
| D2-S8 | enrichment: FWD-1 (external trade request) | FWD-9 refuses a partner-firm advisor that FWD-1's ACCEPT lets file. Owner: `1.0.0_SA_CTO~DELL2` (msg 5817). This is the external trade request below, restated. |
| D2-S11 | no action | The second HTTP API's public endpoint was closed; FWD-10 graded REALIZED by `3.0.0_SA_CVO` (15532793cb), the setting read true by the applier, this seat and the CVO. |
| D2-S12 | enrichment: FWD-1 (hygiene), needs an owner's word | `infra/aws/terraform/trade-pipeline/secrets.auto.tfvars` (80 bytes, 2026-10-09 local mtime) was still on disk in the shared main checkout when read today. It is gitignored (`infra/aws/terraform/.gitignore:5`) and was never tracked. This seat did not open, move or delete it. Whether to delete or rotate it before ~10-27 is the CTO's call. |
| D2-S14 | no action | The FWD-10 probes lacked the API stage; the pair's AMENDMENT 1 carried `/prod` and the door was closed and graded (see D2-S11). |

Count: 6 no action, 6 enrichment (S1, W5-S2, S2, S4, S8, S12), of which S4 is unmeasured and S12 waits on an owner.

## The held scope (named, unsized, uncut)

1. **External trade request.** A partner-firm advisor files for clients, needing firm-scoped client and account search of the kind Investor
   Reporting uses (the directory search, including the last-four lookup live since 2026-10-13 ~17:35Z).
2. **Internal trade request.** Opal portfolio managers, for the Opal ETFs DIVZ, IDVZ, PFDE and PFOE. The direct trade submission tool and
   dashboard page already cover this route.
3. **The 409 defect.** The form's engine submit answers 409 "ticket ... is not a trade_request ticket" on a ticket that reads
   `ticket_type trade_request` and `status open`, per Andrew's 2026-10-13 smoke (record
   `ANDREW_DIRECT_20261013_183xZ_TICKET_CENTER_TRADE_REQUESTS_EXTERNAL_VS_INTERNAL.md`). Cause not investigated.

## What resume runs

`python .tools/drive-mode.py full NFRA_OPSWKF`, then the CTO's round-N analysis cut from this packet, then one issuance by this lane.
