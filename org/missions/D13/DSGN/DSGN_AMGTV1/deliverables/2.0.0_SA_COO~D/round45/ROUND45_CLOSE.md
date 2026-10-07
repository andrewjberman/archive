# DSGN_AMGTV1 -- ROUND 45 CLOSE (2.0.0_SA_COO~D, 2026-10-07 ~03:0xZ; issued by hand, no loop)

**Rectangle:** AMGT_RESAPP `ledger/ROUND_ANALYSIS.round75.md` @326aea63b3 rulings 2-3 (the top-of-page band and the provenance panel),
`ROUND_ANALYSIS.round76.md` @c8bbeeac10 ruling 6 (the FWD-18 page repairs) and ADDENDUM 1 item 4 @a7b2c3e0ba (CTO msg 30491: the repairs and
the removal of the /refresh control ride round 45).

| step | evidence |
|---|---|
| issue | @8584035eb0 (decomposition v45, two cells, `fanout: 2`). `round45/checks/r45/r45.cjs` 1 of 5 at base DEV 34803ef6 on deployed-OVpDhfwD fixtures, 5 of 5 on scratch reference components. `r77_ba5.py` (COO~Z @7daf7c5677) AC1-AC3 NO at base |
| worker ~106, `AV-zw-1` | portal 3e79986f: NEW `TopBand.tsx`, `InputProvenance.tsx`, `topBandTypes.ts`; mounts in `SecurityAnalysis.tsx`; the re-run hook, props and button removed; `posture.harness.cjs` and `shell.harness.cjs` (row Z-W106-S1: its purple-fill count was the removed button, 1 -> 0). r45 5/5, battery29 ALL PASS, proof VALID |
| worker ~107, `AV-zw-2` | portal 8ecb62ba (4 files, +166/-29): the open state keyed on the point; NEW `PassageTable.tsx`; a y-axis tick formatter; one heading per segment; `plain_reason` on an ABSENT chart. AC1 5/5, AC2 10/10, AC3 6/6 clauses; battery29 ALL PASS; proof VALID |
| row Z-W107-S1 | the round-44 check read 2 of 5 on the new markup. Re-anchored by the issuer @ce6e53b828 (point-keyed open state; a segment name read from its heading). It now reads 5 of 5 on the new markup and 2 of 5 on base DEV |
| drains | @5b6cbb0493 (~106, 4 of 4 files). @f953449753 (~107) carried 1 of 4 files after a conflicted `--continue`; the other 3 landed unchanged @aa7dee9340. Row Z-S22 @9a2613e0c5 |
| candidate | portal **0aa353a6** (branch `dsgn-r45-onto-dev` in `C:/tmp/wk-dsgn-amgtv1-92/portal`) = DEV 34803ef6 + the two commits (12 files, +380/-62; a fast-forward of DEV). On it: r43 5/5, r44 5/5, r45 5/5, `r77_ba5` AC1-AC3 YES, battery29 ALL PASS (14 of 14 harnesses, tsc 0, eslint 0) with the current outer |

## The one real run (localhost:5174 = 0aa353a6 on the live API; walker 02:53-03:01:33Z, DISARMED)

`round45/walk/reads45.mjs` -> `round45/walk/read-20261007T025306Z/` (6 of 6 PASS).

- **Top of the page, BA:** the served one-line description; no item today, so the served reason; the social sentence. **MSFT:** the
  served reason in place of a description.
- **Where the data comes from:** 4 rows on each name. Dates read in words ("October 6th, 2026, 9:23a ET -- Worked"); a never-read input
  shows its served reason. No raw stamp, no "landed", no "NEVER".
- **No re-run control** on either name.
- **Driver chart, BA:** 3 points; one press opens 1 passage, drawn as a table with columns 737, 747, 767, 777, 787, Total; a press on
  another point leaves 1 open; a second press closes it. **ASML NA** (three points, one shared passage): 1, 1, 0.
- **Segments, BA:** 3 headings (Commercial Airplanes; Defense, Space & Security; Global Services) over 11 rows with 11 folded cites.
  **MSFT:** the reason, no heading.

## What the run did NOT establish, and what the reviewer should see

- **No news item was read on a real page.** 0 of 95 covered names served one at the cut; the item list is graded on planted items in
  r45 only. RESAPP round 77 changes the news-day rule (round-76 ruling 5).
- **The y-axis probe matched no tick element** (it returned an empty list), so the axis is not measured by the walk. The capture
  `driver-once-ASML-NA.png` shows ticks 400M, 300M, 200M, 100M, 0, read by eye; r77_ba5 AC2 grades the formatter (393,421,721 -> "393.4M").
- **Placement:** the band and the panel sit under the name header (after its timeline and word cloud) and above the tabs, as the order
  said. On a 900 px screen they are below the fold (`page-top-BA-US.png`). Whether "the top of the page" wants them higher is the
  CTO's judgment (AC3).
- **Served words on the page, producer side (RESAPP):** the items reason prints ISO dates ("2026-10-06"); two source labels start in
  lower case ("web search results ...", "the research pack ..."). The page prints what is served.
- **ASML's opened passage** is the served text of a table with no `passage_table`, so it reads as a column of lines. Round-76 ruling 7
  refuses that chart at the producer.

## AMENDMENT 1 and 2 (2026-10-07 ~03:1xZ-04:0xZ) -- the CTO's render review, NOT YET on 0aa353a6

Review: `ledger/CTO_RENDER_REVIEW_ROUND45_0aa353a6.md` @e3d1e62b06 (msg 30533). Two changes, issued as amendments @3d900890f0.

| change | evidence |
|---|---|
| **No figure under the wrong header** (`AV-zw-2`) | ~107 portal 49a9bf37 (`PassageTable.tsx` +18/-4): a row whose figure count differs from the header count is a line beneath the table, outside the grid. NEW check `round45/checks/r45b/r45b.cjs`: 2 of 4 on 0aa353a6, 4 of 4 after. On BA neither served row matches (5 and 8 figures, 6 labels), so both are lines |
| row Z-W107-S2 | COO~Z's check clause AC2/C3 required every figure inside the table. Re-anchored in a DSGN copy `round45/checks/ba5/r45_ba5.py` @0b28e723d0 (YES on 49a9bf37, NO on 0aa353a6); AC2 re-pointed to it in the same commit as ~107's re-written proof (the gate refuses the order edit alone) |
| **The description leads the page** (`AV-zw-1`) | ~106 portal dacc0126 (`TopBand.tsx`, `SecurityOverlay.tsx`): `CompanyLine` in the name header, under the identity card and above the key figures; `TopBand` no longer draws it. `r45.cjs` amended: 2 of 5 on 0aa353a6, 5 of 5 after |
| drains | @cfef60d7eb (~106, 3 of 3 files), @c4da1ea85e (~107, 4 of 4 files); `--verify` dropped 0 on both |
| **candidate** | portal **659104f4** (`dsgn-r45-onto-dev`) = DEV 34803ef6 + 4 commits (12 files, +408/-62; a fast-forward). On it: r43 5/5, r44 5/5, r45 5/5, r45b 4/4, `r45_ba5` AC1-AC3 YES, battery29 ALL PASS (14 of 14, tsc 0, eslint 0) |

**The real run on 659104f4** (localhost:5174, live API; walker 03:42-04:00:15Z over two runs, DISARMED): `round45/walk/read-20261007T035152Z/`,
6 of 6 PASS (the 03:42Z run, `read-20261007T034224Z/`, also 6 of 6; it was repeated only to take the page-top capture unscrolled).
- **BA's page top** (`page-top-BA-US.png`): the description sits directly under the BA US name card, at 274 px, above the key figures,
  the recent news and the timeline. MSFT shows its served reason in the same place.
- **BA's opened passage** (`driver-once-BA-US.png`): the header row 737, 747, 767, 777, 787, Total with no row beneath it; then
  "Cumulative deliveries 8,528 1,573 1,303 1,727 1,110" and "Deliveries 396 (9) 1 32 (14) 26 73 528" as lines; the note; the cite.
  Nothing sits under "Total".
- Still not established: a real news item on a page, and the y-axis by probe (read by eye: 600, 450, 300, 150, 0 on BA).

## Next

**Round 45: 2 of 2 orders terminal (after two amendments).** The candidate goes to the CTO for review from the renders (`0.9.0_WK_DSGN_AMGTV1~106/RENDER_ZW1.md`,
`0.9.0_WK_DSGN_AMGTV1~107/RENDER_ZW2.md`) and the captures above. The DEV push is Andrew's word; PROD is his separate word.
Backlog: row Z-S21 (case value and currency attributes on `ModelTab.tsx`).
