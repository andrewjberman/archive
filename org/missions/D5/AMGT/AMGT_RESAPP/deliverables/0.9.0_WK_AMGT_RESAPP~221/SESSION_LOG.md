# 0.9.0_WK_AMGT_RESAPP~221 -- AMGT-aq-3
Added `_compose_ledger_provenance` and `read_input_ledger_served` to lib/research/api/scoped_amgt.py; the /ledger leaf calls the latter. `read_input_ledger` (also the overlay provenance's reader) is unchanged; no store write.
Api suite: 505 passed. c25 local YES, c13 local YES. Mutant (old route) c25 NO. No surprise rows.
