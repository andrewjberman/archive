# IRPT_ANLREQ workstream T -- what the commentary drafter reads today, measured (2.0.0_SA_COO~T2, dell2, 2026-10-15 ~15:3xZ)

Cause: CTO ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL2_IRPT_ANLREQ_FOUR_LANES_END_TO_END_20261015.md` (msg 8378), lane COMMENTARY: "the drafter reads the
produced report's figures and a non-empty transcript source". Read-only; nothing written outside this file.

## What the drafter's prompt carries (code read at HEAD)

| input | where | reading |
|---|---|---|
| request fields | `data/transcripts/scripts/commentary/drafter.py:30` `PROMPT_FIELDS` | `yc_variant`, `comparison_keys`, `account_type`, `themes`, `holdings_categories` only |
| themes | `drafter.py:83` | always sent as an empty list; the real count goes to `withheld` |
| report figures | the composition (`entry.py:169` `abstract_request`) | the abstract request carries holdings as category WEIGHTS; no performance or return figure reaches the prompt |
| precedent texts | `drafter.py:109-110` from `gold_rows` | `lambda_handler.py:282` wires `"gold_rows": lambda: []`, its own docstring says "empty today": so every draft says NO PRECEDENT |

## What the stores hold (S3 `opal-data-transcripts`, listed 2026-10-15 ~15:3xZ)

| prefix | objects | note |
|---|---|---|
| `teams/transcripts/silver/` | 91 | positive control: the listing works |
| `teams/transcripts/gold/` | 0 | no Teams gold tier |
| `outlook/gold/` | 0 | the commentary gold C-GOLD-FIELDS names (Manav's emails) |
| `outlook/silver/` | 0 | |

## Why this is a contract question, not a cell

- PRD C-KIMI (`org/missions/D9/NFRA/NFRA_TRNSPT/prd/NFRA_TRNSPT_PRD.md`) limits the model input to abstract fields. A report FIGURE (a return, a weight) is a client figure; which ones may go to the outside model is the contract's.
- PRD C-SLICE draws precedents from the commentary gold (emails). The transcript source the ruling names is the Teams silver, a different corpus under C-WIPE-GATE and the hold/held-out rules.
- Sent to `1.0.0_SA_CTO~DELL2` as one ask; no order is cut until it is answered.

## Addendum 2026-10-15 ~15:2xZ: what the 91 Teams silver objects are (key names only, no content read)

Listing of `teams/transcripts/silver/`, counted by first path segment: `research_meeting` 29, `chat_threads` 28, `monday_meeting` 17, `asset_management_ic` 9, `ocio_ic` 8 (sum 91).
These are object counts, not row counts and not a count of rows clear of the held-out flag; the hold and held-out state is in the rows, which this read did not open.
