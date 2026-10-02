# Never-widen sign-off packet -- foreign tax paid to INTERNAL (CTO ADDENDUM 1 A4; IRPT_DASHBD round-2 analysis E3)

Author `2.0.0_SA_COO~P`, 2026-10-02 ~09:5xZ. Measurements: TO-DB-b-9 (`0.9.0_WK_IRPT_DASHBD~1`, merged @cb250a7c2c), records
`deliverables/0.9.0_WK_IRPT_DASHBD~1/FTP_INTERNAL_BLAST_R3.{json,md}`, `FTP_ADAPTER_EQUIVALENCE_R3.json`,
`ADAPTER_OVERRIDE_RETIREMENT_R3.patch`. The table owner's edit is LANDED: `4.0.0_SA_CRO` @3cb9f9b6d5 (builder rule order and the JSON;
`FTP/FC/WD` 2,449 rows and `FTR/FC/WD` 4 rows move `wd-generic` EXTERNAL -> `foreign-tax` INTERNAL; the diff is those 2 rows). Halves
owed: `1.0.0_SA_CTO` and `2.0.0_SA_COO~P`. The act has TWO legs, and they are not the same kind of move.

## Leg (a) -- the IRPT side: output-neutral (this seat's)

1. Commit `ADAPTER_OVERRIDE_RETIREMENT_R3.patch` to `data/assets/scripts/gold/irpt_reporting/account_return_daily.py` (removes
   `crosses = crosses & ~wh` and its comment; the income exclusion for `sb_cd = WD` stays). Lane: open to this seat at HEAD.
2. Re-pin `irpt-reporting-gold-lambda`'s `staged_from` (producer AND table, together, never one) to the commit carrying both, rebuild
   with `build-and-upload.sh investor-reporting irpt-reporting-gold-lambda`, ONE targeted `safe-apply` of the reporting-gold root
   (expect 0 to add, 1 to change: the function's code), read back CodeSha256 = the map's new `artifact_sha256`, re-plan No changes.
3. When: AFTER the root's first scheduled fire (07:41 ET 2026-10-02) lands, so that ledger's A1 is read on the code it deployed.

**Blast radius, by the producer's own rule:** the adapter's output does not move. MEASURED: two dry runs over 85 trading days (four
windows), six accounts, 8 withholding rows -- "today" (HEAD code, old table) and "after" (patched code, edited table) -- differ by 0
in `external_flow` and `total_return_daily`; a second pass over all 375 partitions carrying the codes is also identical. Control:
the patch ALONE on the old table moves `external_flow` on 3 account-days (up to 3.78), which is why the patch never lands without the
table edit (it is landed). Served readers of the adapter's gold: the read route serves platinum as of 2026-09-28 and the publisher
is unapplied, so nothing a page shows moves.

**Rollback (a):** revert the patch commit and re-pin to the previous pins (artifact sha `7eCQtWhsWpReBrPzPULoVMLuS/pvymKg2XS9BAP37HQ=`),
the same targeted apply.

## Leg (b) -- the 49F engine: a SERVED change, not this seat's alone

**What moves (MEASURED by TO-DB-b-9 from landed silver):** the served 49F engine (`data/assets/scripts/gold/runners_49f/a05_ref_txn_classification.py`
-> `c00_flow_ledger.py` -> `twr_daily`, gold `gold/advi/` in `opal-data-49financial`: `reference/ref_txn_classification`,
`canonical/flow_ledger`, `canonical/twr_daily`) would carry the two codes as INTERNAL: **2,578 rows, 39,818.98 USD absolute, net
-39,351.66 USD, 375 partitions, 230 accounts** leave the external flow, so 49F NNA and daily returns move (about 15 USD a row, CTO
A4). Inflection's and Cottonwood's `a05` do not read this table.

**How it would move:** the engine reads a vendored copy, `s3://opal-data-49financial/_code/ref/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json`
(64,794 bytes, version `KZ51y7kMaHdneYLJ4yc5aZRBUBzDdW.j`, last written 2026-08-19; read 09:4xZ: it is the OLD table with CRLF line
endings, LF-normalized equal and parse-equal to the pre-edit repo file -- DB-b-9's "byte-identical" holds as content, not bytes). Replacing
it with the edited table (repo sha256 `8b803eec...`) changes the engine from its next run.

**Two questions this seat does not rule, for `1.0.0_SA_CTO`:**
1. **Andrew's D2 hold.** `canonical/twr_daily` feeds the served ADVI 49F performance figure; the D2 hold on ADVI_PERFRP stands until
   Andrew lifts it, and FAST relaxes no hold (STATUS~P "Standing Andrew words"). If leg (b) is inside that hold, it is RESERVED to him
   and waits; this packet cannot sign it.
2. **Forward only, or a restatement.** Replacing the copy moves new days only; the 375 historical partitions keep the EXTERNAL reading
   unless the engine re-runs them. Forward-only leaves a break in the series at the switch date; a restatement moves served history.
   Either is the engine owner's run plan under its own ledger, not this seat's (`runners_49f` is not in this seat's write claims).

**Rollback (b):** restore version `KZ51y7kMaHdneYLJ4yc5aZRBUBzDdW.j` of the vendored copy (the bucket is versioned) and re-run the
engine over whatever was re-run.

## COO half -- 2.0.0_SA_COO~P

SIGNED for LEG (a) ONLY, 2026-10-02 ~09:5xZ, on this packet's bytes at the commit that carries it: the write set is one source file, one
source-map entry and one function's code; the output-neutral reading is measured both ways with a control; the rollback is stated.
NOT signed for leg (b): it is held on the two questions above.

## CTO half

OWED -- leg (a), and a ruling on leg (b)'s two questions.
