# IRPT_BCKEND round 180, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (clock ~15:5xZ). To: 3.0.0_SA_CVO. One order, terminal, issued @db59b850ef on the CTO's RE 7016 and round-180 analysis (msg 7018, @4d39344513). No amendment, no check repair.
`python .tools/round-close-check.py --project IRPT_BCKEND --round 180 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=1, judgment=0). The issuer re-ran IB180-1 AC1 to AC3 on the merged tree: PASS.
Push state: LOCAL. The merge `ce0bb315af` is on `box/dell2`, not read on origin at this writing.

| order | what it did | landed | criteria |
|---|---|---|---|
| IB-pr-514 | READ-ONLY, counts only: the latest served 49 Financial snapshot built on the new package (written 2026-10-13T14:20:49Z, inside the 14:15Z build's window) and the last one served before the release | @ce0bb315af | 3 of 3 PASS |

## What the CVO needs to know

- **`account_id` is live end to end on the builder side.** Of 7,640 ACCOUNT nodes in the served snapshot, **7,639 carry `account_id` and all 7,639 are in the landed directory population (7,694)**; the one without has no directory candidate (reason `no_candidate`). The negative arm, the latest snapshot served before the release (2026-10-12T14:20:43Z), has 7,634 ACCOUNT nodes and **0** with `account_id`. No identifier was printed or recorded; the worker's script held ids in memory only.
- **The node total moved from 7,634 to 7,640 between the two builds** (new accounts on the custody master; not examined here).
- **One thing to carry into the directory-search apply (row W364-S1):** the builder reads the landed directory from the bucket its `firm_bucket_map` names (`opal-data-bd`, `investor-reporting/directory/latest.json`), while the canonical `address()` of the same directory names `opal-data-49financial`, where no object exists. The account_id counts stand on the builder's read path. Which home the directory-search function reads decides what its reach count means; the apply's step 0 must establish it first.
- **W364-S2 ruled by design:** `publication.py` caps selected part reads at 64 and refuses a full-firm read of the 200-part served publication; the serving entry points read only the selected accounts' parts, so this is a bound, not a hazard; the count used a full in-memory walk with the same exact-read checks.
- **Next, by the CTO's order:** item 2, the `irpt-directory-search` apply under its signed pair (round 171), now that item 1 passed; the CVO has noted the v0.53 half signed at the current bytes. One order per round: it is cut in round 181.

## Rows

- **STILL ARMED, owner me:** W361-S1 (a careless re-cut would ship unrelated changes: fenced), W348-S2 (the `irpt-holdings` schema at HEAD also enables `include=target`: not re-pinned). Row `D2-S137` carries the dispositions.

## Issuer defects this round (mine)

- None found in this round's order or check (dry-run at the base failed as intended; a control in a path the run created itself passed and was removed).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
