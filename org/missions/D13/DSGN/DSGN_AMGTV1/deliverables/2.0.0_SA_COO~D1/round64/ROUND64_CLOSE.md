# DSGN_AMGTV1 round 64 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~12:2xZ)

| item | value |
|---|---|
| list | `ledger/ROUND_ANALYSIS.round63.md` @f7d74e6665 section 2: item 1 is AV-zzp-1; items 2-3 are this close walk, enabled by AV-zzp-2 |
| issuance | @65856dd4b8, fan-out 2 of 2, LF only |
| orders | `TO-AV-zzp-1` -> ~138, drained @0a9cbe8163 (r64a 4/4). `TO-AV-zzp-2` -> ~139, drained @af9d8b1a31 (r64b 4/4, node --check rc=0). Both instances VALID. |
| issuer check fixes | r64b GUARDED read a comment, so it was fixed to read the press code @4a5f10c15c (a negative control with the guards removed fails). r63b arm 2's `heading={description.label}` clause was SUPERSEDED by the round-63 analysis @6c539063d4. |
| checks on both candidates | r62 6/6, r63a 3/3, r63b 5/5, r63c 5/5, r64a 4/4; battery29 ALL PASS |
| DEV | candidate `686ced10` = origin DEV `f043b827` + `52c2e584` (`cand/dsgn-amgtv1-r64-dev`) |
| PROD | candidate `c6c1eb2a` = PROD `2e41c008` + the 5 round-63 commits + `52c2e584` (`cand/prod-dsgn-r63-64`, rounds 63 and 64 together, per the analysis). 0 files outside `src/pages/SecurityAnalysis/`; the SA tree equals the DEV candidate's. No PROD half is asked until the CVO grades every order the candidate carries. |

## The real run -- 12:14Z-12:17Z, `tmp/ui-walk/20261009T121451Z`, signed-in `dev:live` build of `686ced10`

The walk ran `--security "ASML" --security-press "[data-security-choice='ASML_NA_Equity']" --window-press "[data-sentence-press]"`:
37 screenshots, 0 guard aborts. The walker disarmed and its login is refused (401). All 6 API issues are on the key `ASML` itself, the
404 the picker answers.

| criterion | shot / record | what it shows |
|---|---|---|
| Item 3, zzo-3 carried: one ASML listing pressed | 004 (before), **005 after the press** | The press on "ASML NA (ASML_NA_Equity)" opens that listing's page: header "ASML NA", Information Technology -- NL, price EUR 1593.20, and the Thesis tab with the research team's pillars and notes. |
| `TO-AV-zzp-1` AC3 / item 1: the served description under its heading | **008** (Investment-thesis window) | "COMPANY DESCRIPTION" heads the served dossier text ("...ASML is a capital equipment company with a dominant position in deep ultraviolet (DUV) lithography machines and sole manufacturer of extreme ultraviolet (EUV) lithography machines..."). The Item 5 lines ("In Logic, net sales increased by EUR 2.9 billion, ...") follow under "FROM THE FILING". |
| Item 2, the figure press walked | **009 after the press**; `window-press.json` | Pressing the first sentence (the one carrying "EUR 2.9 billion") moves focus to its cited passage: `focused = BLOCKQUOTE#thesis-passage-0-0`, `data-thesis-passage = P0405`, `focused_in_view = true`. In the shot the pressed sentence is underlined, and its passage ("Total net sales growth (in billions) In Logic, net sales increased by EUR 2.9 billion ...", ITEM 5 > PARAGRAPH 31) is open directly under it. |
| `TO-AV-zzp-2` AC3: the walker shows the result | 005, 009, `window-press.json` | Both presses ran, each with an after-shot, and the window press wrote its focus record. |

## Seen on the walk, not of this round (for the round-64 analysis)

- **The served description text itself begins "COMPANY DESCRIPTION:"**, so the label reads twice (the heading, then the text's own
  prefix). The text is served verbatim (C-PRESENTATION-ONLY), so this is producer side.
- **The MACHINE chip still sits on its own line** above each sentence (`round64/PREP.md` item 1, carried).
- **A press moves focus to the passage that already sits under the sentence,** so the page barely changes. The record proves the move,
  but a reader sees only the underline.

## Carried

- `round64/PREP.md` items 1-3.
- **FWD-1:** Andrew's own signed-in walk on PROD (open-calls 2caa).
