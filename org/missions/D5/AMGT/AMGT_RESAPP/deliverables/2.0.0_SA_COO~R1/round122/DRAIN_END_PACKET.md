# AMGT_RESAPP round 122 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO` and `1.0.0_SA_CTO~DELL1`

**STATE: DRAFT, 2026-10-19 ~13:4xZ. NOT SENT. Sections 1 to 4a are measured (cd-4 applied by SC1 and read by the issuer; bp-5 read). Remaining before send: SC1's ledger close and the round's terminal state check; the R1 endpoint read if no row graduates.** Push state of every commit named: LOCAL on box/dell1, unread.

Round 122 is the CTO's round-121 analysis for the R1 track (`ledger/ROUND_ANALYSIS.round121.R1.md`, msg 8200, `@48c576b954`), issued at `db4fbe1394` (decomposition s.131): the CVO's finding C-S203 (the PDF's CEO sentence falls back to words that read as never written), one live read under a real login, then the R1 endpoint read if the round closes with 0 graduated.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-cd-1` | `_ceo_profile_sentence` has a branch for every known state; a plain reason prints byte-identically, a NON-plain reason prints the state's own fixed sentence (`SEARCHED_NOTHING_FOUND`, `NOT_SEARCHED`, `SEARCHED_LINKS_UNREADABLE`, `SEARCH_FAILED`), an unknown reading prints `the state of this profile is not recognised by this document`, the fixed fallback `no public profile is on file yet` is removed | complete | worker ~524; merged `7a7a773265`; AC1 39 passed (the new file read 23 failed, 16 passed at the base), AC2 `1 failed, 471 passed` (floor 440), seven existing CEO files 143 passed before and after, no test re-scoped, proof VALID; rows `W524-S1` and `S2` INERT |
| `AMGT-cd-2` | the issuer's 101-name census of the printed CEO line (PDF and rich export) | the issuer, done (section 2) | `round122_prep/checks/r122_ceo_line_census.py`; `round122_prep/CEO_LINE_CENSUS_LIVE_BASE.md` `cab11e50aa` |
| `AMGT-cd-3` | the live hop: TSM US and HD US under a real login (no stub) | the issuer, done (section 3) | `round122/LIVE_HOP_REAL_LOGIN_D729EE6D.md` `b1569d7f7e` |
| `AMGT-cd-4` | the pack redeploy: ONE member, no never-widen pair | order `831871bc82` sent to `0.7.0_AE_CloudOps~SC1` (read-acked 19:03Z, queued behind the batch COO's timed dossier run) | release pin `rel-amgt-cd4` `d9cdd74096` (parent `107fae40e9`; `render_pack.py` `e83f9618952c` to `5d031ab30a55`, sha256 `2f60c311f595` to `9de710064415`); rollback = the `ca-5` artifact `041tkPU3afZLQr_JrKu_vuEo3hX6Z4qe` |
| `AMGT-bp-5` | (carried) the G4 positive-arm read | READ 2026-10-19: the 11:30Z fire returned rc=1, no objects written; positive arm NOT shown (section 4a) | `round109_prep/checks/r109_g4_positive_arm_read.py` |

## 2. The 101-name census of the printed CEO line (the CTO's grade; `cd-2`)

- **Live base** (the `ca-5` build, 101 of 101 read, 0 errors): 72 names print no CEO line (a cleared management passage prints instead), 24 the not-written sentence, 5 a served plain reason or a confirmed link, **0 the fixed fallback**; the export equals the PDF on all 101.
- **The candidate** (this checkout's handler over the same live pool, after the `cd-1` merge) against the live base: **`COMPARE: 101 names in both captures, 100 byte-identical (pdf and rich), 0 MOVED, 1 skipped`; `DELTA: 0`.** HD US, BA US and TSM US are byte-identical. The skipped name `WALMEX*_MM_Equity` answers 500 from the handler on WINDOWS only (a `*` in a temp file name; the live function answers 200 and prints NO CEO line for it, so the change cannot move it).
- By the CTO's ruling (`ROUND_ANALYSIS.round121.R1.md` section 4 item 1) DELTA=0 needs no never-widen pair; the CLAUDE.md hard stop agrees (verified DELTA=0 needs no hold). The per-state behaviour is graded by the cell's test (39 tests; each state with a non-plain reason), since no covered name holds a non-plain reason today.
- The merged tree (print, api, management folders in the full tree): `9 failed, 1701 passed` (the same nine failures as every round since 116).

## 3. The live hop under a real login (`cd-3`)

The `/ui-walk` walker (the dormant UI walker account, armed under its lease and DISARMED after each of two runs, the post-disarm login HTTP 401, the account `status=disabled armed=no`) on a local `dev:live` build of PROD `d729ee6d` reaching the live data and the live login: **TSM US prints `CEO public profile: No CEO profile has been written for this company yet.`; HD US prints `CEO public profile (EDWARD P. DECKER): searched, nothing found -- The CEO web search returned 10 url(s), none of them on ir.homedepot.com, ...`**, with the real data loaded (the screenshots were read). **The PDF under the same login:** the print route answers 200 to the real session (TSM US pdf 107766 B, HD US pdf 124242 B, TSM US rich 76535 B) and 401 without the headers; **the PDF's CONTENT under the login was NOT read** (the instrument keeps no 2xx body and does not download a file); the printed lines of the two names are read from the same function by direct invocation (section 2). The corrupt case stays a fixture (round 121).

## 4. The live function after the redeploy (`cd-4`, measured 2026-10-19 13:1xZ)

SC1 applied `AMGT-cd-4` 22:37:21Z to 22:39:12Z (msg 8261): live CodeSha256 `V9ZIXiUY..` to `UdNfBJqFC1IBUnpFjTCh+etviWiwoE9WEHynZiuw35w=`, rev `66f7c293`, mem 1769, timeout 29, env keys unchanged; the build differs in ONE member (`render_pack.py` `2f60c311f595` to `9de710064415`, 407 of 408 identical); SC1's AC1 to AC4 PASS, proof VALID `c73e9e19db`. My reads (`r122_post_act_reads.sh a`, read-only), measured:

- **CEO-line census, live after the act against the live base: `101 names in both captures, 101 byte-identical (pdf and rich), 0 MOVED, 0 skipped`; `DELTA: 0`** (72 no CEO line, 24 the not-written sentence, 5 a plain reason or link). The CTO's grade holds: no rollback.
- Config unchanged since the apply; leak scan 101 clean of 101; money vs page 16 of 16; cross-surface 8 of 8; rich exports 8 of 8, 0 `s3://`/`AMGT-`/vendor strings; worst PDF 8.2 s against the 20 s bar.
- **Pack form against SC1's 22:34Z `r122-packs-before2`: 5 of 8 NO.** Every changed line is a market-data value (share price, market cap, beta, consensus EPS/revenue/EBITDA/P-E on GOOGL, ICICIBC, HD); sections, labels and money-line counts match; the capture is 14h40m after the before set. SC1's same-session AC1 read YES 8 of 8 at 22:41Z. Read as a data move, not a render defect; the CVO may grade it otherwise.
- **KEEP sent to SC1 2026-10-19 13:14Z** under `AMGT_RESAPP.TO-AMGT-cd-4`; the ledger `amgt-resapp-r122-cd4-per-state-ceo-sentence-redeploy-dell1` closes on SC1's act.

### 4a. `AMGT-bp-5`, the G4 positive-arm read (measured 13:3xZ; `round109_prep/checks/r109_g4_positive_arm_read.py --since 2026-10-19T11:29:00Z`)

**The positive arm did NOT happen.** Task `OpalResearch-FilingsAnalyzer` ran 07:30:02 local (the 11:30Z fire) with `LastResult=1`; `tmp/llm_batch/last_run.json` absent; 0 analysis, 0 drafting and 0 `filing_attempt` objects for any of the 8 keys since 11:29Z; mean `usage.usd` ABSENT over 0 objects; the trigger's dry run still reads `due=True reason=first run: no last-run record`. The code does retry on the next due day (`run.py:126`). The cause of rc=1 is NOT observable: the launcher `run_filings.cmd` discards its output and the task keeps no log. The launcher chain works from an interactive `cmd` (python on PATH, `cd` resolves, Python 3.14). The next fire is 2026-10-20 07:30 local.

## 5. For your judgment -- PENDING

For the CVO's L9: `W518-S2` and C-S203 close when the builder cell grades: the per-state test (39 tests), the census DELTA 0 and the live function serving it. The R1 endpoint read follows if round 122 closes with 0 graduated: FWD-5 and the surface-parity outcomes.

**Process findings (seat errors named):** my order's rule (c) forbade the words `has been written` in a fixed sentence, which the not-written sentence itself contains: the worker applied it to the new sentences only (its reading is right); the unstick peek of SC1's window failed to take focus three times (the desktop is in use): the order reached SC1 by mail and it read it at 19:03Z (msg 8222).

## 6. Open and carried

`AMGT-bp-5` open: the 2026-10-19 fire failed (section 4a), the next fire is Tue 2026-10-20 07:30 local; A4 step 1 not before Tue 2026-10-20; the Lusha plan tier (Andrew); row `S57` (the portal manager's).
