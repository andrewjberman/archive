# DSGN_AMGTV1 round 63 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~11:4xZ)

| item | value |
|---|---|
| list | `ledger/ROUND_ANALYSIS.round62.md` @4b7ce964a2 section 2, items 1-5, in three cells by file surface (decomposition v63) |
| issuance | @7b812a2000, fan-out 3 of 3; the orders are LF only |
| orders | `TO-AV-zzo-1` -> ~135: drained @e469fa1021, REOPENED (AMENDMENT 1 @564849742f), re-seated, drained @7610bacd3a. `TO-AV-zzo-2` -> ~136: drained @2f97a04cc8, REOPENED (AMENDMENT 1 @fdf096a27e), re-seated, drained @1c5eee00fe. `TO-AV-zzo-3` -> ~137: drained @bf2c5e0b62. All three instances VALID. |
| checks | r63a 3/3, r63b 5/5 (arm 4 amended), r63c 5/5 (arm 4 ONE BAND added), all re-run by the issuer; battery29 ALL PASS on both candidates |
| DEV | candidate `f043b827` = origin DEV `ce3b0cc4` + 5 SA-only commits (`cand/dsgn-amgtv1-r63-dev`) |
| PROD | candidate `f8ec0937` = PROD `2e41c008` + the same 5 (`cand/prod-dsgn-r63`); 0 files outside `src/pages/SecurityAnalysis/`; the SA tree equals the DEV candidate's |
| rows | none from the workers |
| round-close-check | owed: the three AC3 judgments go to the CVO |

## Why two orders were reopened

The first close walk (`tmp/ui-walk/20261009T111310Z`, `...T112329Z`) found two outcomes that passed their checks but missed on the
page. Both checks were amended to read the miss, and both orders were re-seated, because the first workers could not be resumed.

- **AV-zzo-2 (event labels):** rows were assigned, but each label was still drawn at `cy - 22 - row * 14`, relative to its own marker's
  bar. NVDA's titles collided as before. AMENDMENT 1 draws them in one band.
- **AV-zzo-1 (figure press):** the served `quoted_spans` are phrases, not figures, so per-span buttons left "EUR 2.9 billion"
  unpressable. Each `inline-block` button also broke its sentence onto a new line. AMENDMENT 1 makes the whole sentence one press.

## The real run (signed-in `dev:live` builds of the DEV candidate's SA tree; the walker disarmed and its login is refused, 401, each time)

| criterion | walk | what the screenshots show |
|---|---|---|
| `TO-AV-zzo-3` AC3 | `tmp/ui-walk/20261009T111310Z` shot 050 | Typing "ASML" reads "2 companies match 'ASML'; type the ticker." with two buttons, "ASML Holding NV (ASML_US_Equity)" and "ASML NA (ASML_NA_Equity)", plus "Back to all names". "No security found" is no longer shown. |
| `TO-AV-zzo-2` AC3 | `tmp/ui-walk/20261009T113121Z` shot 004 | NVDA's spine draws the event titles in one band above the plot, in two rows, with none overlapping ("China Tells Alibaba, Tech Firm...", "GTC effect...", "Global funds lead biggest on...", "Nvidia Introduces First PCs D...", "Nokia, Nvidia Unveil AI-Powe...", "Nvidia Partner Hon Hai's Sale...", "China May Let Alibaba Buy N..."). The text is 11px. No tick joins a title to its marker. |
| `TO-AV-zzo-1` AC3 | `tmp/ui-walk/20261009T113527Z` shot 008 (ASML_NA_Equity, Investment-thesis window) | The window is headed "COMPANY DESCRIPTION" (the served label), and no "No company description is on file yet." line remains. Each sentence reads as one run of text, e.g. "In Logic, net sales increased by EUR 2.9 billion, primarily driven by leading-edge foundry growth in support of strong AI demand.", with its served span underlined. The whole sentence, including the figure, is the press to its passage. |

## Seen on the walk, not of this round (for the round-63 analysis)

- **The MACHINE chip now sits on its own line above each sentence** (shot 008). Chrome lays out a `<button>` as inline-block even with
  `display: inline`, so the sentence button takes its own line. A focusable `<span role="button">` would flow with the chip.
- **The event titles stand in a band with nothing pointing to their markers.** The order allowed a 1px tick; the worker did not add one.
- **The ASML candidate panel says "type the ticker" beside buttons that make typing unnecessary.** The words are the route's (served);
  the collapse rule in AMGT_RESAPP round 84 may retire the panel for ASML.

## Carried

- **FWD-1:** Andrew's own signed-in walk on PROD (open-calls 2caa).
