# DSGN_AMGTV1 round 59 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~07:2xZ)

**Scope:** Andrew's walk findings SAW-01..23 (record @1725deb826), cut as `ledger/ROUND_ANALYSIS.round58.md` @23fec8836a (cells A-F,
R2-R5). Issued @7480974403.

| order | cell | worker | outer merge | portal | r59 | hyg59 |
|---|---|---|---|---|---|---|
| `TO-AV-zzk-1` | A, the spine | ~124 | 207f0fa972 | ef4aedbb | 4/4 | PASS |
| `TO-AV-zzk-2` | B, one news surface | ~125 | dc0fc46c45 | fa0c5eeb | 2/2 | PASS |
| `TO-AV-zzk-3` | C, structure | ~126 | 1cea2b2769 | 6a0ebca3 | 2/2 | PASS |
| `TO-AV-zzk-4` | D, Thesis + Posture | ~127 | 38ad8a361d | 4b5e5fa1 | 2/2 | PASS |
| `TO-AV-zzk-5` | E, Exec + Peers | ~128 | 36737ed2cb | 712ca12d | 2/2 | PASS |
| `TO-AV-zzk-6` | F, Model + tiles + print | ~129 | aee2a1ccd2 | 5610927c | 2/2 | PASS |

- **Instances:** all six VALID.
- **Rows:** 2 OBSERVATION, both ruled below. W128-S1: the Peers mixed-currency reason. W126-S1: the description now lives only on the
  News tab.
- **Issuer slip, recorded:** a teardown loop deleted worker ~124's branch after a REFUSED merge (another seat's merge was open). The
  branch was recreated from its reported head `fc81f1211f` minutes later, and nothing was lost. The loop now tears down only on a
  confirmed MERGED.
- **round-close-check:** `verdict=MAY-CLOSE` (6 of 6 complete, 6 judgment rows ungraded-by-self).

**Candidate:** portal `3ea5d0f9` = DEV `29b18a8c` + 7 commits:
- the six cells, replayed in the order B, E, A, D, C, F with no conflict;
- the issuer's merge hookups (`cfbbcd94` before the replay): NewsTab passes the served `top_band.items` into the news surface, and the
  print title reads the display name and ticker.

It touches 22 files (+720 -659), all under `src/pages/SecurityAnalysis/`. Branch `cand/dsgn-amgtv1-r59b`. DEV moved twice during the
round (`c0c6f570` -> `29b18a8c`: ADVI_BILLING, TicketCenter, NFRA_OPSWKF). None of those commits touches `SecurityAnalysis/`. On
`3ea5d0f9`, r59 A-F all pass and hyg59 PASSES (tsc and eslint rc=0).

## The real run -- signed-in walks 07:04Z (`tmp/ui-walk/20261009T070453Z`, 59 shots) and 07:13Z (News tab, `...T071301Z`)

Read against the register, AMD and Lenovo:

| SAW | result on the page |
|---|---|
| 01 | No collection legend or colouring; bars are one ink. |
| 02 | The 5 top days are marked (legend "Marked: the days coverage spiked most"). AMD serves no events, so no event label shows; no price line (RESAPP ask). |
| 03 | Empty days draw no bar; the hover tooltip stays. |
| 04 | The earnings disclaimer is gone. |
| 05, 09 | One news surface: each headline once, the "In the news" card gone, the most-mentioned item first with "Mentioned 2 times". |
| 07 | The range matches the items ("September 10th to October 1st"). |
| 08 | The word cloud shows its top 10 terms. |
| 10 | Thesis: one pack line, the five notes folded under "What is not on file", no machine-view subtitle. |
| 11 | Posture: "No call" once; the absences folded; the overlay fold is gone. |
| 12 | "About this data" is one closed fold at the page end. |
| 14 | The chatter strip shows two figures, with no "Readings of ..." sentence. |
| 15 | Exec: Officer and Role only, the source named once, the absences folded. |
| 16 | Peers: the absences folded; the Average cell is empty. |
| 17 | Tiles: an absent figure shows `--` (hover reason). |
| 18 | Segment notes: one unit line plus "About these figures". |
| 19 | Print title: named (the walk did not open the preview; graded on the code). |
| 20 | The tabs start at ~500 px on AMD (was ~2,000). |
| 21 | No per-tab "AMD US"; no machine-view subtitles. |
| 22 | Model opens on 12 Key figures (2025, 2026E, 2027E); the grid is behind "All figures"; one cases line. |
| 06, 13, 23 | Not this round (RESAPP ask; footers next; already ruled). |

## For the repair cell (the issuer's list, after this candidate lands)

1. battery29's harnesses: re-anchor the ones this round broke (markup moved and folded), keeping each claim.
2. SAW-13, the per-panel footers: one page as-of. Each tab still ends with a "date | Source" line.
3. W126-S1: the company description shows only behind "About the company" on the News tab. **Ruling:** one short description line returns
   to the identity header; the News tab keeps no copy.
4. W128-S1: **ruling** -- the mixed-currency reason goes as one line inside the Peers "What is not on file" fold.
5. What changed: one row still prints raw millions ("Market capitalization adjusted to the requested currency ... 1,060,161.94").
   It should be in display units.
6. The News tab opens one item at rest ("Expand (21 more)"). On a tab of its own, show the first 10.
