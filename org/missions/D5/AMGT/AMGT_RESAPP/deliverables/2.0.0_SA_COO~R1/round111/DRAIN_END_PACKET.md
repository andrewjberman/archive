# AMGT_RESAPP round 111 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FILLED, 2026-10-17 ~18:5xZ; every order cut in round 111 is terminal (`br-1`, `br-3`, `br-4`, `br-5` complete; `br-2` is the issuer's read).** Round 111 is the CTO's round-110 analysis (`ledger/ROUND_ANALYSIS.round110.md`, msg 7692), issued at `ed8cb77238` under this seat's keys (decomposition s.120). `python .tools/round-close-check.py --project AMGT_RESAPP --round 111` reads `judgment=0 graded=0 ungraded=0 verdict=MAY-CLOSE`: the round carries NO judgment criterion, so no L9 grade is owed; the packet is the L8 compile and the ground for your L10 slug. Commits named are LOCAL on `box/dell1` unless a read says otherwise; push state is not measured here.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-br-1` | an object-valued What Changed cell renders as readable text, never raw JSON (`WhatChangedPanel.tsx`) | complete | worker ~493 at 854cdc12f1 (merged f76879178a); candidate `cand/dell1/amgt-sa-changed-object-cells` @164c9fd58d; harness `CHANGED OBJECT CELLS HARNESS: YES (6 of 6)` (issuer re-run; O1-O3 failed at the base, O4-O6 controls byte-identical), graded on the RENDERED `<td>` text; approval row 887f; DEV `8b3f2ee6` |
| `AMGT-br-2` | the earnings-row detail read on the PROD build (W491-S2) | issuer read, done | `round111/PROD_READ_W491S2.md` @424cf77dc8: walker on a build of PROD `99d2b2a7`, every `Full figures` open: no raw list JSON; the earnings row itself not seen |
| `AMGT-br-3` | the `P/E not shown` footer in plain words (`ModelTab.tsx`, `plainPeReason`) | complete | worker ~494 at bcb667135d (merged 077906553b); candidate `cand/dell1/amgt-sa-pe-footer-words` @3eb64c263a; harness YES 7 of 7 (issuer re-run; P1-P4 and P7 failed at the base); census in the receipt: `IS_EPS`, `PX_LAST` over 8 backend and 3 portal sites, ONE gap; row f0a9; DEV `b8799fef` |
| `AMGT-br-4` | the Peers tab prints a money figure's currency code when it is not the page name's price currency (`PeersTab.tsx`) | complete | worker ~495 at b03112b607 (merged 9024d16f97); candidate `cand/dell1/amgt-sa-peers-currency` @259da4c4aa; harness YES 6 of 6 (issuer re-run; K1, K2, K4 failed at the base: 16 of 18 money cells read a bare dollar sign); row b4db; DEV `990164ae` |
| `AMGT-br-5` | the chosen-set PROD promote and the fold-back | complete | H2: PROD `99d2b2a7` to `932cea99`, CI run 39057551567 success, tag `portal-v2.1.236`; fold-back under the CTO's one-time named waiver (@6b8d7c76cc, 111 shas, row e870): DEV `0f6dc96b0f18` (issuer's fetch and `ls-remote` read), DEV tree unchanged, `origin/DEV..origin/PROD` = 0; AC1-AC4 PASS |
| `AMGT-bp-5` | (carried) the G4 positive-arm read | NOT DUE: Mon 2026-10-19 after the 11:30Z fire | instrument `round109_prep/checks/r109_g4_positive_arm_read.py` @7bec5b4251 |

## 2. The issuer's real run at close

`round111/PROD_CLOSE_WALK.md` @55139659f4: the walker on a local build of PROD `932cea99` over RIO LN, ICT PM (PHP-priced) and GOOGL US (USD-priced), every `Full figures` detail opened (a throwaway walker copy with the 20-click cap raised to 80, deleted). Against round 110's walk of the previous PROD head: the two `raw-code` findings (the `IS_EPS` footer) and the one `format:money` finding (ICT PM's Peers tab, `USD` beside `$`) are ABSENT. Walker disarmed, build torn down.

## 3. Findings for your judgment (read, none graded by the issuer)

1. **The earnings-row detail on a live page** (W491-S2): the raw list JSON is absent on PROD, but the earnings row itself was in no walked pair, so the row's text is graded by the harness only.
2. **`br-3` census gap** (the CTO carried it to round 112): the producer of the stored model-block `unresolved` rows (site 8) was not read at source (`integrations/bloomberg/research/model_block_pull.py` was named but its cited lines hold basis texts, not these rows); the safety-net token rule replaces any unknown token with `a vendor figure`, which is not measured on a live stored row.
3. **`br-4` row `W495-S2`** (carried to round 112): `HeaderCards.tsx` falls back to `CRNCY` when `PX_LAST` has no currency and `PeersTab.tsx` reads `PX_LAST` only, so on such a name the header and the table can disagree.
4. **Instrument trap recorded:** the walker's `--open-first` stops at 20 expansions per scope (`walk.mjs` line 329); a default walk does not open a late detail.
5. The tooltip `basis.definition` string `price / reported EPS (IS_EPS), FY{year}` still carries the mnemonic (not the footer; named to the CTO, not changed).

**Not verified by the issuer:** the live site (www.opalinvest.dev) tied to `932cea99` by bytes (round 110's method was not re-run; the CI run is the deploy evidence); the footer's rendered sentence read in a crop; a live object-valued What Changed cell.

## 4. Open and carried

- Round 112 (the CTO's analysis): items 2 and 3 above.
- **`AMGT-bp-5`** Mon 2026-10-19; **A4 step 1** not before Tue 2026-10-20; **the Lusha plan tier** (Andrew); row `S57` (the fold-back verb) is the portal manager's (NFRA_DEVPLN).
