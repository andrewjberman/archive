# DSGN_AMGTV1 -- ROUND 43 CLOSE (2.0.0_SA_COO~D, 2026-10-06 ~04:4xZ; issued by hand, no loop)

**Rectangle:** CTO countersign + list @0bcdb77515 (msg 29884): FWD-8 (no bare number as a peer ticker) and FWD-27 (display_name
wherever row.name is printed) NOT_REALIZED page-side. The deployed producer 2lUlZomo serves the fields (census
`round42/fwd8-27-census/` @662434b2cf).

| step | evidence |
|---|---|
| issue | @a5b11b640e (decomposition v43; `round43/checks/r43/r43.cjs` 2 of 5 at base DEV 4fa0312e on deployed-payload fixtures, 5 of 5 on scratch reference edits) |
| worker ~104 (`AV-zu-1`) | portal 704bb387: cscTable.ts, PriceBars.tsx, RankedList.tsx, postureCites.ts, types.ts; r43 5/5; AC2 red on one harness check |
| AMENDMENT 1 | @792557decf. The red was `tabs.harness short_read_control_served`. It is green on the old outer and red on current CLOUD with NO round-43 change: RESAPP au-6's `served_cache` pointer (60 s, keyed by axis+date) is shared across the adapter's two in-process scenarios. Granted the harness plus `served_cache.clear()` per scenario (portal b886851b). The re-seated ~104 (the first seat could not be resumed) gave r43 5/5, battery29 ALL PASS, proof VALID; row Z-W104-S1 |
| drain | @dd2c2191b4 |
| candidate | portal **c123c5a0** = DEV bacc2a22 + the two commits re-applied (fast-forward; author ~104, committer COO~D). r43 5/5 on it. battery29 ALL PASS on it, run in worktree 104 with the current outer (tsc 0, eslint 0) |

## The one real run (localhost:5174 = c123c5a0 on the live API; walker 04:25-04:33:21Z, DISARMED)

`round35/walk/closewalk35.mjs --no-officer "ASML NA" --names "MSFT US,BA US"` -> `round35/walk/read-20261006T042513Z/` (19 reads: 17 PASS, 2 FAIL).

- **FWD-8, read live.** MSFT's Peers tab shows Taiwan Semiconductor as `TSM US` (the resolved key). Samsung (common and preferred) and SK
  hynix show "This listing has only an exchange number; we have no company match for it yet." No bare number. GOOG and GOOGL are
  unchanged.
- **FWD-27, read live.** `fwd2-price.png`: the price face prints Synopsys Inc, Cadence Design Sys Inc, Tokyo Electron Ltd, Global Payments
  Inc, Halliburton Co, Hermes International, Adobe Inc and Clorox Company. 0 vendor capitals. The display-name census holds one string
  per name on MSFT and BA.
- **The 2 FAILs, both instrument-side:**
  - `r35-faces BA US`: the dividends-per-share 0.01 -> 0.00 "-100.0%" row, a consistent move to zero, accepted since round 36.
  - `nonusd-header`: ROG SW now shows **7 tiles**. Four of them are the served-reason tiles of round 42, which this round-35 grader
    expects to carry a currency and an as-of. A reason tile carries neither, by design.

## Grades this round moves (for the countersign)

- FWD-8 -> REALIZED on the candidate's DEV push. The producer serves 94 of 94 with a key or reason; the page now prints them.
- FWD-27 -> REALIZED on the candidate's DEV push. The served vendor names and the Model vendor line are gone; Exec plain words came in
  round 42.

**Round 43: 1 of 1 orders terminal.** The DEV push and the PROD promote are each Andrew's word.
