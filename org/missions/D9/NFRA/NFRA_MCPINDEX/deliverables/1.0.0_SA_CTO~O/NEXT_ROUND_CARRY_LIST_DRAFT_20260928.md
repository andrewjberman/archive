# NFRA_MCPINDEX -- next-round CARRY LIST, pre-draft (not the analysis)

**Owner:** `1.0.0_SA_CTO~O`, 2026-09-28 ~14:5xZ, written while `3.0.0_SA_CVO~O` compiles the L8 slug.
**Status:** DRAFT. The round analysis grades FWD-1..FWD-10 from the slug. This list holds ONLY the items this round
already established, so none is lost between the close (@4ce47993e4) and the recut. The slug may add, drop or reorder
items.

## Carried items

1. **MX-s-10 PHASE B, re-cut as its own order.**
   - Both never-widen halves are signed: CTO @82f48b4fc7, CVO @73e884bbbb.
   - The order carries s10.AC1-AC3, the ask @471c840a0a and both GO-guard sets.
   - The acceptance stays the next scheduled 22:10Z weekday fire.
2. **Exit honesty of the other four BD SSM documents** (row Z-S47's stated boundary).
   - Z-S47 measured the fees document: 69 of 121 runs failed while SSM read Success, because the failure branch has no
     exit.
   - Z-S17 measured only the shutdown ORDERING of the other four.
   - First cell: MEASURE. For each document, read the failure branch and exit, and compare SSM Status with its log
     outcome over the last N runs, with the denominator printed.
3. **Least privilege on `bd_exporter_additional`.** AE~I named `opal/bd/credentials` (the portal login) in the same
   Resource list as dead once PHASE B retires the Playwright path (@5d7d1769e3). A caller census comes first; the
   removal goes through Terraform with a NEVER-2 ledger.
4. **Did the 42 cusip deltas already reach transactions silver?**
   - The dim rebuilt by MX-s-6 (07:xxZ) is served, and `merge-daily-incremental.py:57` joins it for cusip enrichment on
     every daily run.
   - This seat's earlier sentence, "the cusip deltas reach served output only via MX-s-2", was written about GOLD. It
     may be false for SILVER transactions. Measure before any grade relies on it.
5. **The 28 round-1 cells superseded onto opal_ai paths** (the "its gateway paths move into opal_ai" note). They re-cut
   only after NFRA_OPALAI E9 (G-MOVE) lands. This is a dependency to state, not a cell to cut now.
6. **MX-c-4's 5 Schwab tools, held "behind the OPLGTW stop".** Andrew lifted that stop fully (~02:2xZ, call 5, the
   NFRA_OPALAI E9 record). The hold's premise is gone. Re-cut them with the Schwab tool class, graded by FWD-3.

## Not carried

- **Row Z-S47 itself:** it is disarmed by PHASE B's retirement of the fees leg; `bronze/fees` stays current through
  the REST runner.
