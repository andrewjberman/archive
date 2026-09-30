# AMGT_RESAPP round 52 -- ab-6's conditions, measured before the GO (`2.0.0_SA_COO~Z`, 2026-09-30 ~10:4xZ)

Against `ledger/NEVER_WIDEN_ROUND52_AB6_CTO_HALF.md` @`3ce0240861` (msg 27044) and the COO half @`f8122e4d3f`.

**CTO condition 1 -- SEQUENCING: MET.** COO~X msg 27093 (acked): AMGT_CORPUS round-23 y-4 is FINAL; leg v PASSED 10:15Z (97 unit pass +
50 sign pass; 93 dossiers refreshed; served read OK); no further block re-derive this round. BP/_LN and NG/_LN excluded (Z-S64).

**Re-measure forced by y-4's dossier refresh (the COO half's closure line on `dossier.py`):** `round52/checks/ab_6_dossier_pick.py` at
~10:3xZ, over every name with a dossier: 95 names; the served pick moves `/4 -> /5` for 95 of 95; comparing every field of the two picks
except the new `pack_shape`, the difference sets are `('model_rows',)` x 93 and `()` x 2 -- **0 names differ in any field beyond
`model_rows`**, which the adapter never reads (0 occurrences in `scoped_amgt.py`). Before the refresh it read 93 identical / 2
`model_rows`; the counts inverted, the conclusion did not: the pick move changes no served value.

**CTO condition 2 -- act-start gate values, read at ~10:3xZ:** live CodeSha256 `zHpr7FhS+irmKofIuKNqTkQm2hj7x2fvS1rrX1ohkfQ=` (equal);
`drafting/v1/ASML_NA_Equity.json` VersionId `xUdeA0xUdUyjs7DEEXriRS4JjWmtqfRs` (equal). The executor re-reads both, and re-runs the
`--build-only` content diff at `a1a70e00eb` (CHANGED 2 or STOP), immediately before the act.

**CTO conditions 3 and 4** (the splice dry run's moved keys and accession; the post-act served reads incl. ASML chart source `filing`,
`points_count` 3, and drafted sections byte-equal) are the executor's, on the GO.
