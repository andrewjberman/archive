# AMGT_RESAPP -- carried from round 86 to round 87 (`2.0.0_SA_COO~R1`)

Inputs for the CTO~DELL1 round-86 analysis, beside `round86/DRAIN_END_PACKET.md` @64c5f8d6fe section 5.

1. **D1-S18:** the scoped watchlist route ignores `selected_tenant` (200 with the caller's own list); refuse an off-list selector like
   the other scoped routes.
2. **AMGT_CORPUS dossier.py redeploy -- CORRECTED by `2.0.0_SA_COO~C1` msg 2970 (CTO~DELL1 msg 2968):** do NOT carry METHOD /8 (ruled
   never served, `AMGT_CORPUS/ledger/NEVER_WIDEN_ROUND41_AQ5_CTO_HALF.md` ADDENDUM 1). The redeploy cell carries `dossier.py` at METHOD
   /9 once AMGT_CORPUS round 42 lands it; C1 sends the hash. Until then the deployed package stays at /7. Supersedes packet section 5
   item 2's /8 reference.
3. **AMGT_RESAPP-S3:** `lib/research/corpus/library.py` skips a SET but nonexistent `OPAL_RESEARCH_LIBRARY_ROOT`; a set override that
   does not exist should refuse.
4. FWD-16 waits on Andrew's 2026-09-15 hold; the model key rotation is Andrew's act.
