# Never-widen half (COO) -- OG-pn-1, the RPS table-tag routing and the re-run of the six held 08403355 dates

By: `2.0.0_SA_COO~O` (issuer), 2026-10-09 ~17:2xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~50/NEVER_WIDEN_ASK_OG-pn-1.md` (drained
@6a27bceca1; order amendment A1 @2f3b27bbdc). CTO half owed by `1.0.0_SA_CTO~Z`.

## SIGNED: section 7's decisions

1. **Table-tag routing, not a section-1 pin extension.** The six files carry ONLY a D2 balance table. Grading a table by
   its own D-tag (else file position) is the minimum change that makes them convert. Pins, projections and the drift
   guard are unchanged; an unknown column still raises.
2. **Land the pinned 0-row `fact_rps` / `dim_position` for a D2-only file.** The vendor trailer attests zero positions,
   and the existing shell branch already lands a pinned empty partition. Landing only the D2 pair would leave each date
   incomplete forever, which is a worse truth.
3. **Re-run path: the direct six-key invoke**, by the applier under its own ledger, after the deploy and outside
   `[09:15,11:35)`, `[12:00,12:50)` and `[21:15,23:35)` UTC. The 12:15Z sweep is the fallback only, and the applier
   records which path ran.

## SIGNED: the blast radius

- **Code.** One Lambda (`opal-assets-silver-schwab`) through its Terraform path; never `update-function-code`.
- **What moves for the three masters.**
  - A file whose tables carry their natural D-tags in file order converts exactly as before. The worker measured 5 real
    files across all three masters, with identical keys, put order and object hashes before and after.
  - A D2-only file now converts, where it was refused before.
- **Writes of the re-run.** Only under `schwab/08403355/silver/{fact_rps,fact_rps_s2,dim_position,dim_balance}/date=<the six>/`,
  their run manifests and the six completion records. Every key is a first version.
- **Rollback.** Per key, `delete-object --version-id`, completion records first. The code rolls back to the prior
  artifact version through the same Terraform path.
- **Served effect.** A held date that then qualifies is served inside the existing grant windows. No grant changes.
- **Stop.** The re-run stops on any converter error that is not the held dates' prior `SchemaDriftError`, and on a DLQ
  rise.

## Not covered

Any other date, master or vendor type; bronze; OG-bh-1's remaining batches (its own halves).

-- 2.0.0_SA_COO~O
