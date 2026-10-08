# DSGN_AMGTV1 -- ROUND 51 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-08 ~12:1xZ)

**Round:** PRD v0.18 @9a07662460 rows SAUX-37 to SAUX-40 (CTO msg 31675). Issuance @e26aa28d30, decomposition v51.
**Orders:** 2 of 2 complete (137 of 137 on the project). Drain: @72a8f58569 and @b1e3499b0a through `.tools/safe-merge.sh`.
**Portal candidate:** `bfba701f` in `C:/tmp/wk-dsgn-amgtv1-113/portal` = DEV d1b21c97 + `18a43db5` (AV-zzc-1, ~113) + `060d0025`
(AV-zzc-2, ~114). LOCAL; not pushed; 9 product files, no script file.

## 1. WHAT WAS READ, AND BY WHOM

| read | result | reader |
|---|---|---|
| `round51/checks/r51a/r51a.cjs` on the candidate | 4 of 4 arms | this seat |
| `round51/checks/r51b/r51b.cjs` on the candidate | 3 of 3 arms | this seat |
| `round29/checks/battery29.sh`, no skip, on the candidate | ALL PASS (0 skipped); 14 of 14 harnesses; tsc and eslint rc 0 | this seat |
| the close walk, `round51/walk/walk51.mjs`, candidate served on localhost:5174 against the live function | 16 of 16 reads PASS, 0 ERROR | this seat |

Walk evidence: `round51/walk/read-20261008T114652Z/` (16 read files, 24 full-page captures). Names: BA US, AMD US, BP/ LN, MSFT US.
The walker account was armed by the script and read disarmed after (`status=disabled`, `armed=no`); the dev server was stopped
and port 5174 read at 0 listeners.

## 2. PER ROW, FROM THE WALK

- **SAUX-37 (one statement of inputs).** On all four names the block above the tabs draws 5 of the 5 rows the live `/thesis`
  serves, in the served order, and no view draws an input ledger. BA's filings row reads "company filings read for this name --
  10-K filed January 30th, 2026 -- used for the filing passages, the written sections, the segment table, the driver chart, the
  officer list". AMD, BP/ LN and MSFT read the served never-read sentence.
- **SAUX-39 (the coverage sentence).** MSFT US: served `outside_coverage`; the sentence is drawn once, under the header. BA, AMD
  and BP/ LN: served `covered` with no sentence; nothing is drawn.
- **SAUX-38 (officers as served).** BA 12 of 12, AMD 25 of 25, BP/ LN 10 of 10, each name for name in the served order. BP/ LN
  now opens with the chief executive, then the chief financial officer. MSFT: 0 served, 0 drawn.
- **SAUX-40 (two phrases).** BA and AMD: "The research team's thesis pillars: no research-team report for this security."

## 3. THE CTO'S TWO READS (msg 31695)

1. **What stands on the Model tab where the ledger stood.** Nothing replaces it. The tab now ends with its last panel and the
   "About these figures" control: on BA the three "The research team has no ... case for this name yet" lines; on BP/ LN the
   research team's three cases. The only uppercase headings left are "What changed" and, where served, the three case headings.
2. **Whether "research-team report" appears where the function still serves "research pack" for the team's document.** The
   function serves the bare words "research pack" in one value only, the built pack's `source` ("the research pack built for this
   name"). It does not serve those words as a name for the team's document. But see finding F1.

## 4. FINDINGS

- **F1 -- SAUX-40 is NOT fully met; this seat's L5 choice left a third phrase standing.** The research team's own file on BP/ LN is
  named "BP plc Research Pack 2026 04 03_v1" (served `citation.report_key`), and the page prints it: "Source: BP plc Research
  Pack 2026 04 03_v1" (Thesis, Exec) and "Source: the research team's pack, BP plc Research Pack 2026 04 03_v1" and "as written
  in the team's pack" (Model). So after this round the page names the team's document three ways: "research-team report" (reason
  sentences), "the research team's pack" (the Model tab's source lines, not in this round's files) and the file's own name
  "Research Pack". The built pack is still "the research pack built for this name". A reader of BP/ LN sees "research pack" for
  both things on one screen. **This seat's reading:** the team itself calls its document a Research Pack, so the cleaner rule is
  the reverse of the one cut: the team's document is "the research team's pack" everywhere on the page, and the BUILT pack's
  served name changes at the producer. That is the CTO's to rule at the analysis; nothing was changed after the walk.
- **F2 -- AMD's filings row reads never-read** ("No company filing has been read for this name yet") on the live `/thesis`. The
  page draws what is served. Whether AMD's page uses a filing is the producer's statement; named for AMGT_RESAPP.
- **F3 -- superseded checks, stated at the cut:** `round47/checks/r47/r47.cjs` (the Model ledger's wording) and
  `round29/checks/tabs/tabwords.cjs` arm 1 (the page's own officer sort) no longer describe the page. Neither is in battery29.
- **F4 -- `r51a.cjs` arm 2 and the mount line of arm 3 are source reads.** The walk is their real run: the block was read fed
  from `/thesis` (5 rows against the overlay's 4) and the coverage element was read on the live page.
- **F5 -- a worker's line-ending note:** ~113 saw git warn "LF will be replaced by CRLF" on `ModelTab.tsx` and the new
  `CoverageNote.tsx`. Read by this seat: `ModelTab.tsx` carries 832 CR lines at the base and 722 after a 112-line deletion, so
  the file was not rewritten.

## 5. WHAT IS OPEN

- CTO review of candidate `bfba701f` and the ruling on F1; then ONE DEV push on Andrew's word.
- SAUX-41, SAUX-42 and the segment-table row (CTO msg 31707) are not cut: each waits on AMGT_RESAPP round 79.
- Unchanged at Andrew: the PROD promote word; his own signed-in walk on PROD (FWD-1).
