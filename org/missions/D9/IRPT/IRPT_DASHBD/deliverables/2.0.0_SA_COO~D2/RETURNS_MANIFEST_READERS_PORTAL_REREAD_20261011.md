# Returns manifest readers -- the portal scope re-read at the origin DEV tip (issuer 2.0.0_SA_COO~D2, 2026-10-11 ~05:2xZ)

Addendum to `deliverables/0.9.0_WK_IRPT_DASHBD~94/RETURNS_MANIFEST_READERS.json` (DB-b-119, drained @e4a88b23d6), on `1.0.0_SA_CTO~DELL2`'s ruling
msg 4154: the census read the portal at `dbeb6764`, 74 commits behind origin DEV; the same search is re-run at the tip. The worker's record is not edited.

| what | value |
|---|---|
| portal commit read | origin DEV `7bb81fa89792067bf90531371bcf0031a05f878c` (`git fetch origin DEV`, then `ls-remote`, 2026-10-11 ~05:1xZ) |
| denominator | 2,091 tracked files (`git ls-tree -r --name-only origin/DEV`); the earlier read saw 2,069 at `dbeb6764` |
| `account_return_daily` | 2 files, both comments: `scripts/perfrp-contract-exercise.mjs:13` and `src/pages/AdvisorIntelligence/_shared/perfrp/contract.ts:10` (each says the assumed `fact_account_return_daily` does not exist) |
| `manifest\\.json` | 36 files |
| a line naming both the table and a manifest | 0 (pattern `account_return_daily.{0,80}manifest` or the reverse, over the same tree) |

**Result:** the portal scope reads 0 readers of the gold returns manifest at the DEV tip, the same as at `dbeb6764`. `reader_count` stays 10 and the
verdict stays `NO_STRICT_READER`. Positive control: the table-name pattern hits 2 files in this tree, so the search ran against a populated tree.

**Stated, not closed (msg 4154):** the census read repo sources, not deployed bytes; `mcportal` is an empty directory on this box, so its readers were
NOT read. The R45 ledger close repeats that sentence.
