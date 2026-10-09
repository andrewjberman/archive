# MDPF_DEMQUE round 3 -- the one real run of the Bloomberg quote (2.0.0_SA_COO~Q1, 2026-10-09T03:14:22Z)

Cell `DQ-t-9` merged @73523c2317 (`data/mdpf/scripts/demque/bbg_quote.py`, `bbg_allowance.json`). Drain hygiene over the folder:
`py_compile` OK, ruff py39 clean, 37 of 37 tests pass. Run at the base on the two real requests AMGT_RESAPP filed on the queue
(`requests/`, @3a9a64971e); no Bloomberg call (the quote reads the producer's file as text):

| request | quote (verbatim) |
|---|---|
| AMGT_RESAPP-493c-ICT-IDENTITY | `{"allowance_gap": "reference.ceiling absent; reference.reserve absent", "cells": {"bloomberg_reference": 4}, "finish_date": null, ...}` |
| AMGT_RESAPP-107a-ABNB-MODEL-BLOCK | `{"allowance_gap": "model_block.ceiling absent; model_block.reserve absent", "breakdown": {"forecast": 51, "header": 25, "history": 913}, "cells": {"bloomberg_model_block": 989}, "finish_date": null, ...}` |

**Reading.** Every Bloomberg request can now be priced in cells per channel before it draws (FWD-4, C-QUOTE). No finish date exists
yet on any channel: the only figure present is the BQL ceiling (2,920,000, measured floor); every reserve and the reference /
model-block ceilings are absent, and the quote names the gap instead of defaulting (C-RESERVE). Round 4 cell 1 writes `bql.reserve`
as a HELD estimate (CTO msg 1524); the model-block history rows (913) are an upper bound by the worker's own note (the producer asks for
calendar years 2016..now; Bloomberg returns the fiscal years it holds).

**The two RESAPP requests** draw at site Z before this quote existed (CTO msg 1466): their actuals are recorded with
`bbg_quote.py --record ... --no-quote` (label "drawn before C-METER Bloomberg; no quote") when site Z reports the measured cells.

**FWD-1** (carried): the CVO graded the agreement clause MET on AMLP (msg 1526, ADJUDICATION_v2 @bc1ce7b850; 100 of 108 dates clear the
90 pct floor). It waits only on hop 7, the served page for 0QF880237 (dell2 ADVI_COTBKF).
