# AMGT_RESAPP round 90 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-11 ~06:0xZ. Both orders of the round are complete and MERGED (box/dell1 @69d5fea1a9, @a423f1d667, LOCAL).** Round 90
implements the CTO~DELL1 round-89 analysis `ledger/ROUND_ANALYSIS.round89.md` @34a0c14300 (items 1-5; msg 3518); issuance @4f8811dd0b,
decomposition s.98, record corrections @424ec54c89 (s.98e AMENDMENT 1). `round-close-check.py --round 90`: orders 2, complete 2, proof_ok 2,
proof_bad 0, judgment 0, verdict MAY-CLOSE. No round-90 cell reaches the served function: SERVED reach waits for a redeploy that a later
product cell needs. Risk class of every cell: LOCAL.

## 1. Orders, cells and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-oo-1` issuer act | 5: whole-page read, FWD-8 and FWD-38 | DONE, filed | `round90_prep/OO1_WHOLE_PAGE_READ_20261011.md`, script `reads/r90_whole_page_read.py` |
| `AMGT-oo-2` issuer read | 3: Z-W266-S3, LOCATOR or EXCERPT | DONE, filed | `round90_prep/ISSUER_READS.md`: LOCATOR 4, EXCERPT 1 of 5 held points on 3 names |
| `AMGT-oo-3` | 4: the mass-deletion gate exempts a merge in a linked worktree | complete, merged @69d5fea1a9 | worker ~361 @fc55fbc4a9, instance VALID |
| `AMGT-oo-4` | 2: a non-US peer a held company's exact name names serves that identity | READ CORRECTED; BUILD CELL DEFERRED TO ROUND 91 | row `AMGT_RESAPP-D1-S20`; s.98e; the gate refused a second round-90 issuance |
| `AMGT-oo-5` | 1: a US peer the DEMQUE answer covers serves its currency as MEASURED, the PURE half | complete, merged @a423f1d667 | worker ~362 @34167321f0, instance VALID |
| `AMGT-oo-6` | 1: the answer's reader and wiring | STAGED, no order | waits on the DEMQUE answer (request @b6e42f51a8: no quote, no answer) and on oo-4's merge (same file) |
| `AMGT-nn-6` (round 89) | mm-2 to PROD | PARKED at Andrew | call `dell1-20261011T033643Z-e7f2` |

## 2. The issuer's ONE REAL RUN at close (merged tree, box/dell1 @424ec54c89)

- **oo-3** `r90_merge_head.sh` against the merged hook (not a candidate): PASS B1 (a merge with 4 staged deletions in a linked worktree:
  exit 0, no BLOCKED row), PASS B2 (a plain 4-file deletion in the same worktree: exit 1, a new BLOCKED row), PASS B3 (the main
  worktree's merge stays exempt); `R90 MERGE HEAD: YES (3 of 3)`; base for contrast `NO (2 of 3)`. `bash -n` rc 0; the round-89 audit-root
  check still `YES` (A1-A4). The fix: `git rev-parse --git-path MERGE_HEAD` and `CHERRY_PICK_HEAD`, each tested only when non-empty.
- **oo-5** `r90_currency_answered.py` on the merged module: C1-C5 PASS, `R90 CURRENCY ANSWERED: YES`. Against the LIVE ASML peers
  object (12 members), with a map labelled HYPOTHETICAL (`{CSCO, ORCL, BMMV2K: USD}`, NOT a DEMQUE answer): CSCO and ORCL (United
  States, no record key) serve `USD` as `measured`; BMMV2K (Hong Kong) is NOT served although it is in the map (the country gate);
  AMD and NFLX keep the currency their own records already state. The function is not wired: nothing the served function returns
  changes until oo-6 and a redeploy.
- Drain checks, once per merge: `py_compile` rc 0; ruff clean; 122 passed (the peers folder, `test_peer_price_currency.py`,
  `test_peer_listed_identity.py`); the new test file 149 lines, 42 passed with `test_peer_price_currency.py`.

## 3. The whole-page read (oo-1), what it measured

Names: ASML_NA_Equity, BA_US_Equity, ROG_SW_Equity; live function, GET only; every denominator is printed in the file.
- **FWD-8 identity: agrees on 3 of 3.** Subject key and crosswalk vintage (2026-10-09) equal on /thesis and /peers; 0 leaked, 0 wrong,
  0 resolvable-but-unserved, 0 rows without a resolution (ASML 7 of 7 resolvable served; BA 6 of 6; ROG 7 of 7, three by company name).
- **FWD-38 vintages: not met as worded.** Figure vintages within one trading day of the header's: **4,764 of 4,803**; the 39 outside
  are each name's `peers.members[].cap_vintage` (12 at 2026-08-06, 45 trading days behind) and `peers.vintage` (2026-09-24, 11
  behind). Object as-of dates (posture, scores, management, peers): **0 of 34**, each carrying its own date.
- The peers object was built on scanner database vintage 2026-08-06; the live scanner universes read asOf 2026-10-02.

## 4. JUDGMENT for L9

None in the code cells (every criterion is mechanical). Offered for the CVO's own re-run: oo-1's script (one command, three names)
and the oo-4 correction's measurement (`reads/r90_measure_nonus3.py`).

## 5. Rows filed this round

`AMGT_RESAPP-D1-S20` (issuer, OBSERVATION / INERT): the non-US read's undercount and the deferral of its cell (above). No worker filed
a row (~361 and ~362: none). Round 89's rows were dispositioned in `ADJUDICATION_v109`.

## 6. For the next round (the ENRICHMENT LIST's inputs)

1. **oo-4, a build cell, FIRST:** the numeric rule's exact-name arm extended to non-digit non-US tickers: 23 of 1,047 rows (ceiling 52 of
   1,816 with the 29 served today; 1,764 keep plain reasons; no parser). Check `checks/r90_name_match.py` and a drafted order exist.
2. **The LOCATOR cell** (4 of 5 held points; `ISSUER_READS.md` table): period label forms (`FY2025` against `2025`), inline
   parentheticals outside a label's block, decimals split by `_WHOLE_NUMBER_RE`; PBR's value is not in its excerpt (EXCERPT, stays held).
3. **oo-6** when the DEMQUE answer lands. Open question for the DEMQUE owner, not this project: 138 of the 1,038 requested rows are
   held names whose currency is already served.
4. **The peers object's refresh**: the page's peer caps carry 2026-08-06 against a scanner now at 2026-10-02. A producer rebuild, not a
   served-function change.
5. **A standard for FWD-38**: figures against the header (met but for the peer caps) or every object's own as-of (not met by design).
6. **One redeploy** of `opal-amgt-scoped-api` for whatever the served cells are by then (oo-4, oo-6; nn-5's `crosswalk.py` by blob).
7. `AMGT-nn-6` stays Andrew's.

checked 3 of 3 issuer reads and acts (oo-1, oo-2, oo-4 corrected)
