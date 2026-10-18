# AMGT_RESAPP round 122 -- the live BASE of the printed CEO-profile line over every covered name (`AMGT-cd-2`), `2.0.0_SA_COO~R1`, 2026-10-18 ~18:3xZ

Push state of every commit named: LOCAL on box/dell1, unread. Evidence outside the repository: `C:/dev/ui-walk-evidence/r122-ceo-lines-live-base.json` and `.txt` (client data stays local).

**The read.** `round122_prep/checks/r122_ceo_line_census.py capture live`: GET `/print?format=pdf` and `format=rich` of `opal-amgt-scoped-api` at CodeSha256 `V9ZIXiUY..` (the `ca-5` build) for EVERY covered name: **101 distinct names, 101 of 101 read, 0 errors.**

| PDF line kind (the printed `CEO public profile...` line) | names |
|---|---|
| no CEO line printed (a cleared management passage prints instead; the CEO line prints only when no passage prints) | 72 |
| `CEO public profile: No CEO profile has been written for this company yet.` (state `NOT_WRITTEN`) | 24 |
| a line carrying a served plain reason or a confirmed link (five names: for example `CEO public profile (Toshiaki Tokunaga): No verified company ...`, `(Tetsuya Nakano): https://www.globaldata.....`, `(Gordon Naylor): No verified company ...`) | 5 |
| the fixed fallback `no public profile is on file yet` (the words C-S203 names) | **0** |

The rich export's line equals the PDF's on all 101 names (a name with no CEO line prints none in both).

**What this base says about the CTO's DELTA grade (the issuer's reading, to be confirmed by the candidate capture after `AMGT-cd-1` merges).** On the live pool today NO name prints the fixed fallback: every served reason of the five names that print a reading line is plain words, and the 24 not-written names print the `NOT_WRITTEN` sentence. `AMGT-cd-1` changes the line only for a reading whose reason is NOT plain (it replaces the fixed fallback with the state's own sentence) and for an unknown reading; a name that prints neither today cannot move. So the expected result of the candidate capture is DELTA=0 (every printed line byte-identical, HD US and BA US included): that is a prediction from the base, not a measurement of the candidate. The census of the candidate (`capture local`, then `compare`) is the grade, taken after the merge.

**Not verified:** the candidate (not built yet); the PDF text of a name whose CEO line wraps in a way the extractor joins differently (the extractor joins the following whitespace-led lines: a wrapped line reads as one); a state the pool does not hold (the per-state test of the cell covers the non-plain cases with synthetic input).
