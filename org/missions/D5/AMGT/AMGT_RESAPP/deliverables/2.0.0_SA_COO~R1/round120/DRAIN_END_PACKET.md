# AMGT_RESAPP round 120 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO` and `1.0.0_SA_CTO~DELL1`

**STATE: DRAFT, 2026-10-18 ~15:5xZ. NOT SENT. Sections 1 and 2 are measured and final; section 3 (the live reads after the act) and section 4 are filled after `AMGT-ca-5` is applied by SC1 and the issuer's reads are taken.** Push state of every commit named: LOCAL on box/dell1, unread.

Round 120 is the CTO's round-119 analysis for the R1 track (`ledger/ROUND_ANALYSIS.round119.R1.md`, msg 8062, `@cf597e60c8`), issued at `62d2e724a3` under this seat's keys (decomposition s.129). The round-118 rulings were MET at round 119; this round closes what graduated: the CEO-profile reader's three states (W518-S2, W518-S3), a blank or `?` source (W519-S5) and the export's missing thesis-pillars passage.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-ca-1` | the reader `ceo_profile_reading` gains `NOT_WRITTEN` (a null or absent profile) and `UNREADABLE_OBJECT` narrows to a failed read; the PDF and the export print the CEO line from the state; the export counts a served drafted `ceo_bio` as the PDF does (W518-S3) | complete | worker ~520; merged `a1eb3b86ce`; AC1 40 passed, AC2 `1 failed, 347 passed`; five existing assertions re-scoped (named in the receipt); the base pack raised `AttributeError` on a string profile (row W520-S3): fixed |
| `AMGT-ca-2` | an absent, empty, blank or `?` figure source prints `source not stated` at seven print sites (PDF Header, withheld Header, fiscal-year, company description; export Header, fiscal-year and forecast tables) | complete | worker ~521; merged `f64668f0e8`; AC1 59 passed, AC2 `1 failed, 375 passed`; two assertions re-scoped; the bare `?` originates in read-only `render_print.py` line 221, so the rule sits in the pack's wrapper |
| `AMGT-ca-3` | the export prints a `## Thesis pillars` section wherever the PDF prints one, through the same `_pillars_gap_open` and `_cleared_passage` | complete, with AMENDMENT 1 | worker ~522; merged `dda778e2f8`; AC1 26 passed; the merged tree after `ca-2` broke ONE of its controls (P5 for ICICIBC IN: a recorded base export carries two `?` source rows that `ca-2` changes on purpose); AMENDMENT 1 `2475b8f961` (a hand-written base-side map), re-seat merged `ca27cb077a`, 26 passed, the print folder `1 failed, 432 passed` |
| `AMGT-ca-4` | the issuer's reads (section 2 and 3) | the issuer, section 2 done, section 3 pending | `round120_prep/checks/r120_source_census.py`, `r120_reading_words.py`, `ISSUER_READS_INTERIM.md` |
| `AMGT-ca-5` | the live redeploy | order cut `3df63f23f5` to `0.7.0_AE_CloudOps~SC1`, NOT YET APPLIED (SC1 is inside another COO's HARVST batch until about 16:30Z) | release pin `rel-amgt-ca5` `107fae40e9` (parent `2771164d0d`, two members: `render_pack.py` `a281246c18c0` to `e83f9618952c`, `scoped_amgt.py` `75a6e6480d7d` to `66fca4c2d040`); never-widen pair: COO half `6e6aa93be6` (sha256 `59d6b9627809`), CTO half `b0823ed515`, COO addendum 1 `83f159996d`, CTO addendum 1 `501157597d` |
| `AMGT-bp-5` | (carried) the G4 positive-arm read | NOT DUE: Mon 2026-10-19 after the 11:30Z fire | `round109_prep/checks/r109_g4_positive_arm_read.py` |

## 2. The issuer's reads taken before the act (the candidate = this checkout's handler over the live pool; the live base = the live function at `VQ9zM6r4..`)

- **The merged tree** (print, api and management folders, full tree): `9 failed, 1662 passed`, the SAME nine failures as every round since 116 (one transient tenth, `ca-3` P5, is the repair above); 125 new tests (`ca-1` 40, `ca-2` 59, `ca-3` 26).
- **Candidate against live, eight names:** the PDF text identical on 7 of 8 (TSM US: one CEO line, `no public profile is on file yet.` to `No CEO profile has been written for this company yet.`); the export adds the thesis-pillars section on ICT PM, GOOGL US and ICICIBC IN (6 added lines each) and changes TSM US's one CEO line; RIO LN, KMB US, HD US and BA US: 0 changed lines; `CROSS SURFACE: YES (8 of 8)`, `PACK FORM: YES`, `MONEY VS PAGE: YES (16 of 16)`.
- **The census of source lines over every covered name (the CTO's W519-S5 grade):** the live base 101 of 101 names, 0 question-mark sources, 0 `source not stated` lines, in the PDF appendix and in the exports; the candidate 100 of 101 (`WALMEX*_MM_Equity` 500 on Windows only), 0 and 0. So `W519-S5` is INERT on the live pool (the live appendix does not print the figures that carry no source); `ca-2` guards the case by tests. Parser positive control on synthetic lines recorded in `ISSUER_READS_INTERIM.md`.
- **The candidate leak scan, every covered name:** 101 names, 0 leaking lines, 100 clean, 1 error (the same local-Windows `WALMEX*`).
- **The served reading word (the CTO's condition 3, restated in its addendum 1):** BEFORE, the live `GET /thesis` of the eight names: `UNREADABLE_OBJECT` on all eight (profile null on RIO LN, ICT PM, GOOGL US, ICICIBC IN, KMB US and TSM US; a dict on HD US and BA US). EXPECTED after the act (candidate): `NOT_WRITTEN` on the six, `SEARCHED_NOTHING_FOUND` on HD US and BA US with their printed line byte-identical; any other movement is a rollback.

## 3. The live function after the act -- PENDING (filled after SC1's report and the issuer's reads)

## 4. For your judgment -- PENDING

Items for the CVO's L9 (to fill with the live exports and PDFs after the act): the three exports (ICT PM, GOOGL US, ICICIBC IN carry the pillars section; TSM US the new CEO sentence), one PDF (TSM US). Items for the CTO's round-121 reading: the portal page's explicit rendering of the three states and the `types.ts` union (the CTO's own round-121 row: a failed read and a never-written profile look the same on the page); rows `W520-S1..S5`, `W521-S1..S3`, `W522-S1..S3`; the process findings (my half's wrong after-read line on HD US and BA US, corrected by addendum and accepted; my amendment commit's gate-limb misstatement and over-named row; the cross-cell P5 control).

## 5. Open and carried

`AMGT-bp-5` Mon 2026-10-19 after the 11:30Z fire; A4 step 1 not before Tue 2026-10-20; the Lusha plan tier (Andrew); row `S57` (the portal manager's).
