# Foreign tax to INTERNAL: what moves, by how much, and what does not (TO-DB-b-9, preparation only)

Prepared by 0.9.0_WK_IRPT_DASHBD~1 on 2026-10-02 for the packet of 2.0.0_SA_COO~P. Nothing was edited, deployed or uploaded.

**The change.** In the CRO's code table, `FTP/FC/WD` (foreign tax paid) and `FTR/FC/WD` (reclaim) move from EXTERNAL to INTERNAL (tax). Today a withholding reads as a client withdrawal wherever the table is read.

**What the table's readers are** (comp-find, 52,675 files scanned): four code readers, all 49 Financial. None belongs to Inflection or Cottonwood (their `a05` files read other vendors' vocabularies).

| Reader | Served where | Moves if the codes go INTERNAL |
|---|---|---|
| 49F engine `a05_ref_txn_classification.py`, and `c00_flow_ledger.py` downstream | `gold/advi/` in `opal-data-49financial`: `reference/ref_txn_classification`, `canonical/flow_ledger`, `canonical/twr_daily`, 562 partitions to 2026-09-30 | **2,578 rows, $39,818.98 absolute, net -$39,351.66, 375 partitions, 230 accounts** (2,574 FTP, 4 FTR). Each row leaves the external flow, so the daily return moves for those account-days. The served ledger of 2026-09-29 holds 55 such rows ($1,003.34) and equals the silver. |
| IRPT adapter `account_return_daily.py` | `irpt/49financial/gold/account_return_daily`, 559 partitions to 2026-09-28, six accounts | **Nothing**, when the override retires and the table edit land together. |
| Reporting-gold Lambda (pinned copy of producer and table) | same gold prefix, from the first fire after 2026-09-28 | **Nothing**, today or after a joint repackage. |

**The adapter result.** The override is the single line `crosses = crosses & ~wh` plus its comment; the patch removes it and the classification then comes from the table alone. Run twice with `--dry-run` over 85 trading days (four windows) for the six accounts, 298 account-days, 8 withholding rows: external flow and daily return differ by exactly 0, every column identical. Over all 375 partitions carrying the codes and all accounts, the flow and income terms are identical, while the withholding rows classed EXTERNAL fall from 2,578 to 0. The control matters: the patched code on the UNEDITED table moves external flow on 3 account-days (largest $3.78), so the two halves must land together.

**What does not move.** The adapter's income exclusion for `sb_cd = WD` is a separate rule and stays. Inflection and Cottonwood are untouched. Other withholding codes (`BWDIV` and four more) were already INTERNAL.

**Three things the packet must carry** (rows W1-S9, W1-S10):
1. The served 49F engine reads a vendored byte-identical copy at `s3://opal-data-49financial/_code/ref/`, not the repo file. The edit reaches it only if that copy is replaced and `a05` re-run.
2. The Lambda packages a pinned table and a pinned producer. Re-stage both together, never one.
3. The table is generated. `wd-generic` precedes `foreign-tax` in the builder's first-match list, which is why the two cells read EXTERNAL. The CRO edits the builder and the JSON together. `sources.json` also carries comment text about the retired override.
