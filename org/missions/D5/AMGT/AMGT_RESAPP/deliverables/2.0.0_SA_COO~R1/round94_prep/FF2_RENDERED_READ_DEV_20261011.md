# AMGT-ff-2 -- the rendered read of the landed peers heading and Ticker cell on the DEV build (issuer act, round 94)

**Reader:** `2.0.0_SA_COO~R1`, 2026-10-11 ~13:40Z. **Source:** CTO review `ledger/CTO_REVIEW_R94_FF_2_PORTAL_CANDIDATE.md` ("the issuer's browser walk of the
rendered page follows the landing"); CTO round-93 analysis items 2 and 3.

**What was read:** portal `origin/DEV` @1f0b1d68c5 (a fetched read; it carries `AMGT-ff-2` as 582ffe6eb8, an ancestor of this head; two later merges of other lanes are
above it) in a detached worktree; its real `PeersTab.tsx` server-rendered by `react-dom/server` (the loader of `peersPattern.harness.cjs`, cut at its fixture marker) over
the LIVE served `/peers` and `/overlay` payloads of ASML, ROG and BA (`fixtures/peers_and_header_figures_ASML_ROG_BA_20261011.json`, read 2026-10-11). A server render,
not a browser walk: markup and text, not CSS or hover. The CVO's browser walk of the DEV build remains the L9.

**Check:** `checks/r94_peers_units.cjs`, run from the DEV worktree root. Base (DEV c96efe17 and 11f25102dd): H1 and T1 FAIL. At DEV 1f0b1d68c5:

```
PASS H1 the Mkt Cap heading names the codes its figures carry  [ASML "Mkt Cap (EUR, USD)", ROG "Mkt Cap (CHF, USD)"]
PASS H2 control: one code reads that code  [BA "Mkt Cap (USD)"]
PASS T1 a member with no held ticker prints "no ticker held", not a company name  [4 rows read, wrong: []]
PASS T2 control: a MEASURED member prints its house-form ticker  [INTC US]
PASS T3 control: the Name cell of every member row still prints the served company name  [12 rows]
   arms passed 5 of 5
R94 PEERS UNITS: YES
```

**Reading:** round-93 item 2 (a heading that said "(local)" over USD peer values) and item 3 (company names in the Ticker column for Tencent, SK hynix, Samsung and Novo)
are both repaired on the DEV build. No value is converted; the scale stays in each cell's own format. PROD is unchanged at 37aa1247 (ls-remote read at 13:3xZ).
The CVO grades.
