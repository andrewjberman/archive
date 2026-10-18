# AMGT_RESAPP round 122 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO` and `1.0.0_SA_CTO~DELL1`

**STATE: DRAFT, 2026-10-18 ~19:2xZ. NOT SENT. Sections 1 to 3 are measured; section 4 (the live function after the redeploy `AMGT-cd-4`) is filled after SC1 applies it (SC1 starts about 21:00Z to 21:40Z, after the batch COO's timed dossier run, msg 8222) and the issuer's reads are taken.** Push state of every commit named: LOCAL on box/dell1, unread.

Round 122 is the CTO's round-121 analysis for the R1 track (`ledger/ROUND_ANALYSIS.round121.R1.md`, msg 8200, `@48c576b954`), issued at `db4fbe1394` (decomposition s.131): the CVO's finding C-S203 (the PDF's CEO sentence falls back to words that read as never written), one live read under a real login, then the R1 endpoint read if the round closes with 0 graduated.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-cd-1` | `_ceo_profile_sentence` has a branch for every known state; a plain reason prints byte-identically, a NON-plain reason prints the state's own fixed sentence (`SEARCHED_NOTHING_FOUND`, `NOT_SEARCHED`, `SEARCHED_LINKS_UNREADABLE`, `SEARCH_FAILED`), an unknown reading prints `the state of this profile is not recognised by this document`, the fixed fallback `no public profile is on file yet` is removed | complete | worker ~524; merged `7a7a773265`; AC1 39 passed (the new file read 23 failed, 16 passed at the base), AC2 `1 failed, 471 passed` (floor 440), seven existing CEO files 143 passed before and after, no test re-scoped, proof VALID; rows `W524-S1` and `S2` INERT |
| `AMGT-cd-2` | the issuer's 101-name census of the printed CEO line (PDF and rich export) | the issuer, done (section 2) | `round122_prep/checks/r122_ceo_line_census.py`; `round122_prep/CEO_LINE_CENSUS_LIVE_BASE.md` `cab11e50aa` |
| `AMGT-cd-3` | the live hop: TSM US and HD US under a real login (no stub) | the issuer, done (section 3) | `round122/LIVE_HOP_REAL_LOGIN_D729EE6D.md` `b1569d7f7e` |
| `AMGT-cd-4` | the pack redeploy: ONE member, no never-widen pair | order `831871bc82` sent to `0.7.0_AE_CloudOps~SC1` (read-acked 19:03Z, queued behind the batch COO's timed dossier run) | release pin `rel-amgt-cd4` `d9cdd74096` (parent `107fae40e9`; `render_pack.py` `e83f9618952c` to `5d031ab30a55`, sha256 `2f60c311f595` to `9de710064415`); rollback = the `ca-5` artifact `041tkPU3afZLQr_JrKu_vuEo3hX6Z4qe` |
| `AMGT-bp-5` | (carried) the G4 positive-arm read | NOT DUE: Mon 2026-10-19 after the 11:30Z fire | `round109_prep/checks/r109_g4_positive_arm_read.py` |

## 2. The 101-name census of the printed CEO line (the CTO's grade; `cd-2`)

- **Live base** (the `ca-5` build, 101 of 101 read, 0 errors): 72 names print no CEO line (a cleared management passage prints instead), 24 the not-written sentence, 5 a served plain reason or a confirmed link, **0 the fixed fallback**; the export equals the PDF on all 101.
- **The candidate** (this checkout's handler over the same live pool, after the `cd-1` merge) against the live base: **`COMPARE: 101 names in both captures, 100 byte-identical (pdf and rich), 0 MOVED, 1 skipped`; `DELTA: 0`.** HD US, BA US and TSM US are byte-identical. The skipped name `WALMEX*_MM_Equity` answers 500 from the handler on WINDOWS only (a `*` in a temp file name; the live function answers 200 and prints NO CEO line for it, so the change cannot move it).
- By the CTO's ruling (`ROUND_ANALYSIS.round121.R1.md` section 4 item 1) DELTA=0 needs no never-widen pair; the CLAUDE.md hard stop agrees (verified DELTA=0 needs no hold). The per-state behaviour is graded by the cell's test (39 tests; each state with a non-plain reason), since no covered name holds a non-plain reason today.
- The merged tree (print, api, management folders in the full tree): `9 failed, 1701 passed` (the same nine failures as every round since 116).

## 3. The live hop under a real login (`cd-3`)

The `/ui-walk` walker (the dormant UI walker account, armed under its lease and DISARMED after each of two runs, the post-disarm login HTTP 401, the account `status=disabled armed=no`) on a local `dev:live` build of PROD `d729ee6d` reaching the live data and the live login: **TSM US prints `CEO public profile: No CEO profile has been written for this company yet.`; HD US prints `CEO public profile (EDWARD P. DECKER): searched, nothing found -- The CEO web search returned 10 url(s), none of them on ir.homedepot.com, ...`**, with the real data loaded (the screenshots were read). **The PDF under the same login:** the print route answers 200 to the real session (TSM US pdf 107766 B, HD US pdf 124242 B, TSM US rich 76535 B) and 401 without the headers; **the PDF's CONTENT under the login was NOT read** (the instrument keeps no 2xx body and does not download a file); the printed lines of the two names are read from the same function by direct invocation (section 2). The corrupt case stays a fixture (round 121).

## 4. The live function after the redeploy -- PENDING (filled after SC1's report and the issuer's reads: the live census must read `DELTA: 0` against the base)

## 5. For your judgment -- PENDING

For the CVO's L9: `W518-S2` and C-S203 close when the builder cell grades: the per-state test (39 tests), the census DELTA 0 and the live function serving it. The R1 endpoint read follows if round 122 closes with 0 graduated: FWD-5 and the surface-parity outcomes.

**Process findings (seat errors named):** my order's rule (c) forbade the words `has been written` in a fixed sentence, which the not-written sentence itself contains: the worker applied it to the new sentences only (its reading is right); the unstick peek of SC1's window failed to take focus three times (the desktop is in use): the order reached SC1 by mail and it read it at 19:03Z (msg 8222).

## 6. Open and carried

`AMGT-bp-5` Mon 2026-10-19 after the 11:30Z fire; A4 step 1 not before Tue 2026-10-20; the Lusha plan tier (Andrew); row `S57` (the portal manager's).
