# CTO rulings 2026-10-20 ~15:2xZ: the Opal model source for FWD-10/11, the swap model leg, the audit record

**Seat:** 1.0.0_SA_CTO~DELL2.
**Inputs:**
- `4.0.0_SA_CRO~TCKT` research `RESEARCH_FWD10_OPAL_MODEL_WEIGHTS_SOURCE_20261020.md` @c05a6b6841 (design fork, routed at
  15:00Z per the self-drive call routing).
- Its items file `TCKT_BACKEND_ITEMS_SWAP_AND_AUDIT_20261020.md` @15cfc42950.
- `2.0.0_SA_COO~G2` msg 11369.

**Landing:** each ruling goes into IRPT_ANLREQ PRD v0.25 CONTRACTS beside FWD-10/11 (draft
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ENDPOINT_FORWARD_IRPT_ANLREQ_REPORT_ENGINE_20261020.md`), once Andrew confirms the
DONE WHEN lines. No cell is cut before v0.25.

## R1. The Opal model data for the report engine (design fork, ruled on the CRO's research)

- **Returns, risk and the cumulative chart (FWD-10):** read the firm-neutral, registered model return series. That is source C
  of the research: `model-portfolio-timeseries.json` under `opal-data-portal-v2` `yang/global/platinum/benchmarks/`, the same
  numbers the Performance tab shows.
  - The act is one read grant (GetObject on that one key) on the resident policy, by Terraform `safe-apply`, under a COO+CTO
    never-widen pair like the 10-20 commentary grant.
- **Asset allocation in FWD-10:** read the models' CURRENT weights from the registered, firm-neutral positioning surface
  (source B), stated on the page "as of" the report's T-1 frontier.
  - The report's as-of is always that frontier (C-PRICES v0.16), so current weights are the window's weights, except across a
    rebalance on the boundary day. The page states that date.
  - This departs from the research's "Core needs no weights": FWD-10 as drafted includes asset allocation side by side.
- **Parity (FWD-11) weights by date:** a dated JSON extract `{as_of: {model_code: {ticker: weight}}}`, written by the yang job
  that already reads the model holdings.
  - Its address is `lib/opal_naming.py address()` output after a new registry row in `infra/logic/registry/` (rule 30); no
    hand-typed key.
  - The resident reads the JSON and never unpickles.
- **Rejected:** the MDPF composition tables and the gateway composition tool. They are keyed by firm, so a report for one firm
  would read another firm's partition (CLAUDE.md section 5).
- **Required in either case:** the model-code map (UST, ST, INT, LT, ULT to the catalogue's five Opal models) is written down
  once, as a committed contract artifact that the reader carries. Today it lives only in a display-name match (trace Q6, row
  W304-S1).

### R1 correction (~15:2xZ, on `2.0.0_SA_COO~G2` msg 15:15Z; re-read here)

- **The key in R1 was wrong.** `yang/global/platinum/benchmarks/model-portfolio-timeseries.json` reads 404 on
  `opal-data-portal-v2`.
- **The series is `json/benchmarks/model_portfolio_timeseries.json`.** Read here: 780,910 bytes, last modified
  2026-10-20T11:06:27Z.
- **Shape** (`~G2`'s read): rows `{date, model_code, model_return, benchmark_return, rfr}` for UST, ST, INT, LT and ULT, starting
  2024-04-30.
- **The one-key read grant names this key.**
- **Consequence for FWD-10:** a model comparable's common window cannot start before 2024-04-30, and the page states the window
  rule.

## R2. Item A, the swap model leg: placed under FWD-2 (C-SWAP as written)

- `swap_pass` passes a literal `[]` for model proposals and does no classification, so an unknown ticker always reads
  NO_REPLACEMENT.
- The fix wires classification and model proposals as C-SWAP already specifies:
  - the model widens the pool and classifies, and never decides the pick;
  - a pick below 0.80 is flagged;
  - vendor egress is per C-SWAP's existing ruling, with no new vendor.
- It is driven once on purpose: a filing whose holding is unknown, with the filer pressing No, ends in a report naming the proxy
  (`proxy_for`, `proxy`, `method`, `confidence`, `sources`).
- Owner: `2.0.0_SA_COO~Y2`'s next cut after v0.25.

## R3. Item B, the audit record

- **(b) New family or extend:** a NEW `analysis-report` family beside `ycharts_runs`, made through the builder with a registry
  row, at a builder-made address in each firm's bucket.
  - `run.json` stays as it is; renaming its home would be a migration, never a rider (LGIC R19).
  - The record has a published JSON Schema and carries the four linkages: the ticket, the form as filed, the filer, and the
    package and commentary pointers. A consumer rejects a malformed record.
- **(a) Retention:** 2,555 days (seven years) from the filing date, with no unreferenced-expiry rule.
  - This is the existing ceiling of `irpt-retention-v1` and longer than the five years an adviser's books-and-records rule asks.
  - Andrew stated no period ("Retention: not stated", record @f2581e90b9). This is the driver's ruling under the self-drive call
    routing, and his word changes it.
- Owner: `2.0.0_SA_COO~Y2`'s next cut after v0.25.
