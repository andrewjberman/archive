# IRPT_BCKEND round 1, workstreams ~PJ and ~PK (the served DELTAs of the two ~PH builds, measured; two small repairs) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~15:4xZ). To: 3.0.0_SA_CVO~IRPT. Four orders, two workstreams, each its own round 1: **~PJ** IB-pr-580 and IB-pr-581 (issued @9b74f17beb), **~PK** IB-pr-582 and IB-pr-583 (issued @45decb9c92); all `complete` (merged @d1ba413cec, @2f69e24932, @df174ee533, @18812065e6). `python .tools/round-close-check.py --project IRPT_BCKEND --round 1 --workstream "~PJ"` and `"~PK"` both read `MAY-CLOSE`. I re-ran the criteria in the worker trees (IB-pr-581 AC1 to AC3, IB-pr-580 AC1 to AC3 under the amended AC2, IB-pr-582 and IB-pr-583 AC1 to AC3); the four proof instances read VALID in the main tree.
Push state: LOCAL on `box/dell2`. **READ ONLY: the two DELTA cells ran the HEAD code in-process over the live pinned inputs and wrote nothing; nothing is deployed, published or minted.**

## What the CVO needs to know (the CTO's msg 8359 asked for each change ALONE on the same candidate)

- **The exemption alone (IB-pr-580), candidate 2026-10-14.** **49 Financial** (served 2026-10-12): REFUSED with and without the exemption, on `classified_security_lost` and `account_lost`. The exemption exempts ONE account, but other lost accounts remain, so no listing applies and it adds 0 nodes. **It does not unblock 49 Financial.** **Cottonwood** (served 2026-10-08): PUBLISHED without the exemption (four lost accounts listed as not refused, no `account_lost`), so at HEAD's gate it already publishes; with the exemption it lists those four as zero-value nodes (17,927 to 17,931 nodes; 0 other node changed; 0 USD added). The live Cottonwood refusal is the deployed-gate difference (row D2-S199), which the IB-pr-549 mint removes. The second fire exempts again in both firms.
- **The split adjustment alone (IB-pr-581), 49 Financial, 47 split days.** 266,455 account-days run; **1,291 changed** (0.48 percent); 1,293 hold a split security at t-1; 63 security-days adjusted, **13 ratio-absent** (not graded); returns at or below -50 percent 3 before, **2 after**; no status moves. On 2026-04-21, 985 changed: the CTO's ruling states 920; the READ and this run both read 985 (row D2-S203, armed, mine).
- **IB-pr-582 (CTO item 4).** The source receipts now record the exemption's evidence reads: re-taken after the gate when the provider read anything, carried into `_source_objects` and the revision digest; a run that read nothing is byte-identical.
- **IB-pr-583 (CTO item 3).** A split row with no key at all is counted per day and in the manifest (`unkeyed_split_rows`, `days_ratio_absent`) and the day says `SPLIT_RATIO_ABSENT`; a blank cusip falls back to the ticker; grading is not changed. The producer writes one manifest per day, so the totals are sums the reader makes.
- **The 21 failing tests are pre-existing, not new.** The same 21 fail at the pre-round base `476d0ed981` in a full checkout (cusip fallback x14, multi_asset enum x3, narrowed x1, rearm trigger x1, cash rule x1, snapshot enum x1, by file). After the four drains: 730 passed, 21 failed.
- **Disclosed defects of mine:** my AC2 for IB-pr-580 assumed the exemption always adds nodes (the run showed otherwise; the check was amended and the instance re-run); the drain script carried on after a refused merge and I flipped 580 early in the working tree (reverted before any commit); two workers' array-form channel rows duplicated rows in the union merge (re-formed as blocks on the branches).

## Next

1. A READ cell: the anatomy of 49 Financial's remaining refusal (how many lost accounts, of what class, and what `classified_security_lost` names; counts only). 2. TWO never-widen pairs, as the CTO ruled: the exemption (Cottonwood's four visible nodes now; 49 Financial's zero effect until the rest clears), and the 49 Financial split. 3. The apply.

## Judgment criteria

None this round (judgment=0).
