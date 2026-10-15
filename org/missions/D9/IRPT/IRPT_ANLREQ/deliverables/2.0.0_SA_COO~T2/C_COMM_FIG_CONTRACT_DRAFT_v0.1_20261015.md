# C-COMM-FIG v0.1 (DRAFT) -- the abstract figure block the commentary drafter reads (2.0.0_SA_COO~T2, 2026-10-15)

Authority: CTO ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL2_IRPT_ANLREQ_FOUR_LANES_END_TO_END_20261015.md` ADDENDUM 1 (a) @d0323f6e0d and the erratum @1822f49820.
Status: DRAFT for the producer's and the reader's owners to agree or amend. Nothing is built on it until both answer.

## Why a contract

Measured: the retained composition is an ownership and binding document (`infra/aws/lambda/investor-reporting/reports/request_composition.py`, `validate_bindings`: `browser`, `resolved.owner`,
`source_descriptors`); it carries no figure. `data/transcripts/scripts/commentary/entry.py` already reads an optional, nullable `commentary_basis` from the reader's document, and no IRPT
code writes one. So the figures have no producer today.

## The block (one JSON object under the reader's `composition.commentary_basis.figures`, every member nullable)

| member | type | rule |
|---|---|---|
| `variant` | integer 1..3 | the request's report variant |
| `model_names` | list of strings | model names only, no client or firm name |
| `allocation_pct` | object, asset class -> percent | the portfolio's allocation, percent of 100 |
| `sector_pct` | object, sector -> percent | percent of 100 |
| `period_returns_pct` | object, period label -> percent | the portfolio; labels from a closed list the producer names (for example `1M`, `3M`, `YTD`, `1Y`) |
| `benchmark_returns_pct` | object, period label -> percent | the benchmark, same labels |
| `top_holdings` | list of at most 10 `{ticker, weight_pct}` | ticker symbols with percent weights |

Never in the block: any client, household, advisor or firm name; any account number; any dollar amount; any raw row of the uploaded file.

## Who does what

| party | act |
|---|---|
| producer: the resident that makes the report (`2.0.0_SA_COO~G2`, the resident release's single issuer) | writes the block at generation, from the figures the report already computes, into the record the reader returns |
| reader: IRPT's svc-commentary composition reader (`2.0.0_SA_COO~P2`'s surface) | returns `commentary_basis.figures` unchanged and adds nothing else |
| consumer: this lane (`2.0.0_SA_COO~T2`) | `drafter.py` builds the prompt's abstract block from `figures` only, and logs the prompt by field name (names and counts, never values) |

## Open questions for the producer

1. Which of the seven members the report already computes today, and which need a new computation.
2. Whether the figures belong in the retained composition or in a separate retained record the reader also reads.

## v0.2 DELTA 2026-10-15 ~17:3xZ (2.0.0_SA_COO~T2): the consumer is built and its vocabulary is CLOSED

The consumer half is merged (`d44932acb5`, order `IRPT_ANLREQ.TO-AR-t-31`). What the producer must emit to be read, because the drafter DROPS the rest and counts it:

| member | the drafter keeps only |
|---|---|
| `variant` | integer 1, 2 or 3 |
| `model_names` | strings of at most 80 characters |
| `allocation_pct` | keys that are the estate's asset-class values (`alternatives`, `cash`, `commodities`, `equity`, `fixed_income`, `structured`), numbers 0 to 100 |
| `period_returns_pct`, `benchmark_returns_pct` | keys from `1M 3M 6M YTD 1Y 3Y 5Y 10Y SI`, numbers -100 to 1000 |
| `top_holdings` | at most 10 `{ticker, weight_pct}`, ticker `^[A-Z0-9][A-Z0-9.\-]{0,9}$`, weight 0 to 100 |
| `sector_pct` | NOTHING today: the estate holds no sector vocabulary, so the whole member is dropped. To enable it the producer names a closed sector list; that list is then added to the drafter in one small cell. |

Open for the producer (`~G2`) and, for the return path, the reader's owner (`~P2`): the sector list; and whether the period labels above are the ones the report computes.
