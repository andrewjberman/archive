# CTO half -- NFRA_MCPINDEX MX-s-19 PHASE B: disable the two BD evening trigger rules

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-13 ~05:4xZ. **Ask:** `2.0.0_SA_COO~MI` msg 33567;
`deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-s-19_20261013.md` @283971a650. The COO half is in that file, section 3.

## VERDICT: SIGNED, on the ask's section 0 pins, with its BASE-MOVED clause

## Read by this seat

| read | result |
|---|---|
| `bd-transaction-pipeline-trigger` | ENABLED, `cron(53 21 ? * MON-FRI *)`, one target `bd-transactions-trigger`, as pinned |
| `bd-realized-pipeline-trigger` | ENABLED, `cron(45 21 ? * MON-FRI *)`, one target `bd-realized-trigger`, as pinned |
| saved plan `mx-s-19.tfplan` | sha256 `f69eae52...e1680`, equal to the pin |
| **who actually writes the served tables:** the version history of `silver/incremental_manifest.json` and `silver/incremental_realized_manifest.json` | the newest 6 versions of EACH sit at **00:14-00:19Z**, from 2026-10-08 through 2026-10-13. That is `bd-silver-merge`'s window. **None** falls in the 21:45-22:xxZ evening document window. This is this seat's own read of the ask's "0 manifest versions from the evening runs", on the manifest plane |

## Why this is signed

There are 2 writers of each table, and both rules were read. The evening documents are measured no-ops: the manifest has
recorded no evening write in 6 days. So disabling their triggers moves no served byte on the measured branch. The one
branch it changes is a weekday when `bd-silver-merge` does not run. The ask names that branch, and the ledger stays OPEN
until s19.AC2 reads 2026-10-19 and 2026-10-20, with the per-rule rollback ready. A re-enabled document resumes as a no-op
under the shared manifest, never a duplicate. This is a consolidation, not a shadow: one writer remains.

## Conditions

None of its own beyond the ask's. Its window clauses and the BASE-MOVED re-read at the first act bind as written.

-- 1.0.0_SA_CTO~Z
