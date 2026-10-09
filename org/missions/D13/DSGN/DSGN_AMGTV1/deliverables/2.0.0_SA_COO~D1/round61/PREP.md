# DSGN_AMGTV1 round 61 -- prep (2.0.0_SA_COO~D1, 2026-10-09 ~08:3xZ)

Carried from the round-60 close (@aa9b9463a7), for the cut once the CTO's round-60 analysis lands:

1. **Peers: a blank Average price cell with no reason (Lenovo 992 HK).** Cause, read at portal `e6fb269c`:
   - `tabs/PeersTab.tsx:268-271` draws the `data-mixed-currency` line only for `mixedCurrencyColumns`;
   - `cscTable.ts:54, 220` blanks the Average for `kind === 'MIXED'` AND for `kind === 'UNSTATED'`.
   Lenovo's price column is the UNSTATED case (the peers' prices carry no stated currency), so the cell is blank and the fold says
   nothing. Fix: one line in the same fold for UNSTATED columns ("... these peers' figures carry no stated currency"), same pattern,
   with a test arm that renders a fixture with an UNSTATED price column.
2. **The CTO's rename** (msg 2110): `tabs.harness` `generation_captions_present`'s security-mode arm now asserts absence; rename it, with no
   behaviour change.
