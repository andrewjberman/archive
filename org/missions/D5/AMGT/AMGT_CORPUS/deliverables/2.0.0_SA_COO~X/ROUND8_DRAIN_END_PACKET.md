# AMGT_CORPUS -- round 8 drain-end packet (the COO's task-order packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-29 ~01:1xZ.** Four orders issued (@`43912573fb`, decomposition v8.0), four complete, four
drained, each re-graded by this seat at the worker's tip. One order was reworked on an issuer ruling before its merge (s.2).
**The round's served act -- the dossier rewrite -- is HELD** (row `Z-S53`): the case rule the round was cut to build reads
correctly as ruled, and what it would serve is wrong, because the ruling's premise does not hold in the stored packs (s.3).

**R-4:** graded this round -- none by this seat (L9 is the CVO's); graded ever -- 19 of 19; endpoint denominator -- 19.

## 1. Orders -- 4 of 4 complete, all drained

| order | cell | worker tip | drain | this seat's own run at the tip |
|---|---|---|---|---|
| `TO-CRPS-j-4` | `read_dossier` prefers the current method | `5cf660114f` | `c858a00330` (chain A) | AC1 `7 passed`; AC2 `dossier_pick names 95 current_method_available 95 stale_pick 0`; proof VALID |
| `TO-CRPS-j-1` | case = text under its heading; method-aware no-op; `/2`; `--case-census`; `--write --workers N` | `8945d6b4cb` | `c858a00330` (chain A) | AC1 `12 passed`; AC2 `case_census names 95 slots 285 body 34 heading_only 68 absent 183 sum 285`; AC3 judgment recorded for the CVO; proof VALID; corpus suite 383 passed |
| `TO-CRPS-j-2` | FWD-9's five sites resolved in code | `f5bca56cc6` (rework) | `db5f64c8f3` | AC1 `j2 tristate_unresolved 0 library 0 rc 0`; AC2 `plant_flagged 1`; AC3 `153 passed`; proof VALID; corpus suite 365 passed |
| `TO-CRPS-j-3` | derive selects the newest landed stamp carrying the rule's inputs; `stamp-census` | `6a176cc9c4` | `ddba870b96` | AC1 `8 passed`; AC2 `stamp_census keys 6 newest_carries 0 older_carries 0 none_carries 6 sum 6`; AC3 `j3 keys_read 97 of 97 unserved_vs_base 0 of 69 ratio_moved_vs_base 0`; proof VALID; bloomberg suite 115 passed |

**The one real run of each outcome, on CLOUD HEAD `9f520b8bb3`** (`evidence/r8_close_runs.txt`, 01:02-01:05Z): every line
above reproduces; `--pick-census` now reads `current_method_available 0 stale_pick 0` because the code is at dossier `/2` and
every stored object is `/1` -- `read_dossier`'s fallback serves those `/1` objects exactly as before, so the served table is
unchanged (objects 468).

## 2. The drain acts, as executed

1. **`j-2` NOT merged as first built -- an issuer ruling, then a rework.** `972d9a0e81` reached `unresolved 0` by writing
   `strftime("induction_run_%Y-%m-%d_" + mode + ".json")`: the census classifies any `strftime` result SAFE, so splicing a
   caller string into the FORMAT would pass a `mode` containing a path separator as safe. That resolves the census, not the
   site. Ruled: `mode` validated to `fire` / `dry-run` and selecting one of two constant formats; a test that `"../x"`
   raises. Reworked at `f5bca56cc6` (the worker reopened its own order at `bbbd171e22` to regain its grant). The as_of half
   (a validated date through a constant format) was sound and stands.
2. **Merges** through `safe-merge.sh`, each graded on the merged index: `j-3` `ddba870b96`; `j-2` `db5f64c8f3` (one retry
   past another seat's `index.lock`); chain A `c858a00330`, whose append-only channel conflict with `j-3`'s row was resolved as
   the union (rows `Z-W3-S6`, `Z-W1-S9`, `Z-W1-S10`; ids unique, JSON valid) and graded by `--continue`.
3. **The dossier rewrite: HELD, NOT RUN.** No pair opened, no change entry, no `dossier --write`. Row `Z-S53` disarms the
   worker's ARMED `Z-W1-S9` by holding the only writer (this seat).

## 3. The finding that holds the rewrite -- the team's cases are a TABLE, not prose

The round-7 analysis ruled "prose first": extract the text UNDER the case heading. Measured over all 95 names (worker `~1`,
read-only survey; this seat re-read ADBE_US_Equity and ZTS_US_Equity directly):
- **No stored pack carries prose under a case heading.** The 34 names with case leads are all pdf class A; docx picks (31) and
  class-B pdf picks (35) carry no case lead and no "upside/base/downside case" phrase.
- **The three case headings are the row labels of a scenario table on page 0.** After `Upside Case`, `Base Case`,
  `Downside Case` come 15 year headers (`2026E`..`2030E` x3), then rows `EPS`, `Multiple`, `Price`, `Return` of 15 values each:
  values 1-5 are Upside, 6-10 Base, 11-15 Downside. ADBE: Multiple `16.0x / 9.0x / 6.0x`; Price 2026 `416 / 233 / 143`;
  Return 2026 `88.4% / 5.6% / -35.2%`. ZTS: Multiple `18.0x / 12.0x / 10.0x`.
- **So the rule as built serves the wrong thing.** Downside receives the whole table's cells (794-1485 characters of all three
  cases' numbers), Upside and Base read heading-only and are served ABSENT. That is why `body 34` (every one Downside) sits
  beside `heading_only 68`.
- **The team's own case numbers ARE present and citable**, positionally, by case -- extraction of numbers the team wrote (the
  CTO's adjudication @`bfc179c2ea`), not a computed case. They are also the team's written Base-case figures that i-3 could not
  find in the workbooks.

**This seat's recommendation for the round-8 analysis (a ruling, not taken here -- the spec was frozen):** a table-aware case
rule. From the case labels, read the year header group length k, then each metric row's 3k values; case i takes values
[ik, (i+1)k) of every row, served as `{metric: {year: value}}` with the page citation. A row whose value count is not 3k reads
ABSENT with that reason. The census prints each case's row count and a non-enforced ordering read (Upside price >= Base >=
Downside) as a plausibility signal. Chain A's method-aware no-op, `--case-census` and `--write --workers N` carry over unchanged.

## 4. The rule moved under this project -- `Z-S51` / `Z-W3-S6`

- At 18:36Z on 09-28, AMGT_RESAPP's `0.9.0_WK_AMGT_RESAPP~166` @`b56fef3032` made `lib/research/api/case_rule.py` the ONE Base
  case rule (adjusted P/E) and `model_block_pull._compute_cases` delegates to it. Over 97 block keys (`cases-report`, read-only):
  SERVED 69 vs round 7's 49; 21 ABSENT -> SERVED; CAT_US SERVED -> ABSENT (act A's re-mint); **48 of 48 served-in-both at a
  different ratio.** The stored blocks still carry round-7 values.
- `j-3` then measured the six keys the new rule refuses for history: **no `IS_COMP_EPS_ADJUSTED` figure at any of 18 landed
  stamps.** Stamp selection cannot serve them; only an adjusted-EPS pull (vendor egress) or a rule change can. The selection is
  built, tested and inert.
- **The decision this hands up (SERVED, on another project's rule):** whether this project's stored blocks are re-derived
  under the new rule (moving 48 served ratios and 22 dispositions). This seat holds every derive until ruled (decomposition v8.0
  s.8). A re-pull for the six is vendor egress and needs Andrew's per-use word.

## 5. Rows -- dispositions for the L9

| row | class / standing | disposition asked |
|---|---|---|
| `Z-W1-S9` | OBSERVATION, ARMED -> held by `Z-S53` | OPEN: the case rule serves a table dump; lifts with a table-aware rule |
| `Z-S53` | OBSERVATION, INERT (hold) | OPEN until `Z-W1-S9` closes |
| `Z-W1-S10` | OBSERVATION, INERT | CLOSE: an absent `method_version` keeps the inputs-only no-op; no served object lacks one |
| `Z-W3-S6` | OBSERVATION, INERT | OPEN -> analysis: the six need a pull or a rule change, not a selection |
| `Z-S51` | OBSERVATION, INERT | OPEN -> analysis: the re-derive decision (s.4) |
| `Z-S52` | OBSERVATION, INERT | READ: corrects `Z-W2-S11`'s 8306_JP example (the CTO's s.3 ask) |
| `Z-W5-S3` | OBSERVATION, INERT | OPEN: case values heading-only on the served table -- unchanged this round (the rewrite is held) |

## 6. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

- **`j-1` AC3** -- *does each served case read as the team's own written case for that name?* The served rewrite did not run,
  so the artifact to judge is the census run on CLOUD (`evidence/r8_close_runs.txt`) and s.3's direct reads: this seat's reading
  for the grader is NO as built (Downside = the whole table; Upside/Base absent), with the table-aware rule of s.3 as the route
  to YES.

## 7. Enrichment candidates for the round-8 analysis

1. **The table-aware case rule** (s.3), then the dossier rewrite under a pair (`--write --workers N`), then `Z-S53` lifts.
2. **The re-derive decision under the new Base-case rule** (s.4, `Z-S51`) -- a SERVED change on AMGT_RESAPP's rule.
3. **The six keys' adjusted-EPS gap** (`Z-W3-S6`): a scripted pull under Andrew's word, or a rule fallback -- a ruling.

## 8. Bounds and residue

- No vendor or gateway call. No S3 write this round (the rewrite held; no derive). The drain's only served-plane reads were
  censuses.
- Worktrees `/c/tmp/wk-crps8-1..3` (branches merged) and `/c/tmp/wk-crps7-5` remain: each holds only its worker's untracked
  `.scratch/`, so removal is a forced (recursive) delete and waits on the operator's word. The round-7 temp dirs in `%TEMP%`
  are unchanged.

-- `2.0.0_SA_COO~X`
