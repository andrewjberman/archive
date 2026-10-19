# IB-pn-4 close record -- the one real run (2.0.0_SA_COO~N2, 2026-10-19 ~13:2xZ)

Order `IRPT_BCKEND.TO-IB-pn-4` (workstream ~PO round 10), WORLD, executed by `0.7.0_AE_CloudOps~IB2`: apply commit `a33c047a68`, first-run read commit `d7a0605435` (both LOCAL on box/dell2 when read). Under Orion pair (b) ADDENDUM 4 (blob `22172a052e`, both halves signed) and AMENDMENT 1 (`101582033a`: the dispatch file at commit `e7d5361cf9`, not HEAD).

Re-run by this seat on the record at HEAD, from the repository root:

| invocation | output |
|---|---|
| `python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~N2/checks/r4/pn4_cells.py . IBN4-AC1` | `IBN4-AC1 PASS` |
| the same file, `IBN4-AC2` | `IBN4-AC2 PASS` |
| the same file, `IBN4-AC3` | `IBN4-AC3 PASS` |

Proof instance `deliverables/0.7.0_AE_CloudOps~IB2/IRPT_BCKEND.TO-IB-pn-4.apply-addendum-4-scope-feed-region.proof_of_spec.json`: `python .tools/proof-of-spec-check.py` reads VALID (rc 0).

What the first scheduled chain (2026-10-18 11:33Z) showed, as IB2 read it from the STEP LOG and the files (not the chain exit): exit 0, no TOLERATING, no SKIPPED, DAYS complete=1 skipped=0; 294 of 294 households ok (bound 294); coverage 863 = 795 RETURNED + 68 ABSENT (39 NO_START_DATE_AT_SOURCE, 17 GROUP_NO_SERIES, 12 NO_GROUP); 0 zero returns; `daily_factor` stored; calcGrossOfFees false; exactly 2 keys, both under `orion/inflection/`. The 2026-10-19 chain skipped both keys as existing (no overwrite). No rollback.

Limits: this seat re-ran the record checks, not the S3 objects or the step log; those reads are IB2's, so the corroboration is one seat deep. The first run covers one pull date (DAYS complete=1); the history backfill (ADDENDUM 2) is not yet run. Row `D2-W404-S9` (the dispatch tolerates a failed pull step) stays ARMED, outside this lane's write surface.

Ledger `irpt-scope-feed-region-script-ibn4-20261017` closed by this seat via `deploy_ledger.py close` (5 of 5 legs; sentinel removed). Order `<status>` flipped to `complete`. Superseded: `TO-IB-pn-2`.

Next: the history backfill order (ADDENDUM 2, ~PO round 11) with the IBN5 checks.
