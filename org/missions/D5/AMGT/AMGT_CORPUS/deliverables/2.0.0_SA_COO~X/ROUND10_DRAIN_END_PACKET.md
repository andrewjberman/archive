# AMGT_CORPUS -- round 10 drain-end packet (the COO's task-order packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-29 ~06:5xZ.** Four orders issued (@`beb375e66e`, decomposition v10.0), four complete, four
drained, each re-graded at the worker's tip. One order was amended twice mid-round by the issuer (s.2). The round's one served
act -- the dossier rewrite at `/3` -- ran under a signed pair and matched its prediction exactly.

**R-4:** graded this round -- none by this seat (L9 is the CVO's); graded ever -- 19 of 19; endpoint denominator -- 19.

## 1. Orders -- 4 of 4 complete, all drained

| order | cell | worker tip | drain | this seat's own run at the tip |
|---|---|---|---|---|
| `TO-CRPS-l-3` | the six unreadable tables | `b110086294` | `5b0b728ab1` (chain A) | AC1 `6 passed`; AC2 `l3 names 6 body_names 0 absent_specific 6 absent_generic 0 sum 6` |
| `TO-CRPS-l-1` | unit carries its claim; `/3`; import without PDF libs | `75dd5905ad` | `5b0b728ab1` (chain A) | AC1 `11 passed`; AC2 `... unit_carried 10 currency_set 1 currency_null 27`; AC4 `pdf_libs_loaded none read_dossier_callable True`; AC3 judgment for the CVO; proof VALID (AC1-AC4); corpus suite 409 passed |
| `TO-CRPS-l-2` | team-vs-rule Base census (read-only) | `ac670eb8bd` | `58d076cc23` | AC1 `8 passed`; AC2 `base_census names 95 both 22 team_only 6 rule_only 49 neither 18 within_10pct 5 beyond_2x 8 median_ratio 0.6931` |
| `TO-CRPS-l-4` | `cases-report` refuses an unresolvable key | `65e2a012ea` | `120ff9b27f` | AC1 `3 passed`; AC2 REFUSE + `l4 planted_underscore rc 2`; AC3 `cases AMD_US_Equity base SERVED`; bloomberg suite 118 passed; the 97-key regression through the refusal `keys_read 97 of 97 unserved_vs_base 0 ratio_moved 0` |

## 2. What happened in the round, as executed

1. **`l-3`: the six tables are genuinely blank-celled.** On all six (8035_JP, BZLFY_US, HEI_US, SNPS_US, TSM_US, V_US) the
   Base column carries 4 of 5 values in EPS, Price and Return (5 in Multiple); no merged line, label-line value or wrapped
   row. With 14 values in a 15-slot row and no x-coordinates, line order cannot place the gap, so each is served ABSENT with
   that specific reason. The worker's arithmetic (Price = EPS x Multiple on the four Base values) puts the blank at Base
   2030E -- a computation, so reported here and not served (ruling 3).
2. **`l-1` AMENDED TWICE by the issuer** (@`b40840e09a`, both in its record face):
   - AMENDMENT 1, on `2.0.0_SA_COO~Z` msg 26444: importing `dossier` loads no PDF library -- AMGT_RESAPP's scoped API will
     serve the team cases through `read_dossier` and its Lambda carries no PyMuPDF. Three top-level imports (`continuation`,
     `extract`, `substrate`) each reached `import fitz`; all moved into the functions that use them. New AC4.
   - AMENDMENT 2, on the worker's row `Z-W1-S13`: three tests pinned exactly what the order changed on purpose; the worker
     correctly refused to edit outside its grant; the issuer granted the two test files and ruled the update. The order was
     reopened and the same worker continued; row `Z-S56` records the disarm.
   - `METHOD_VERSION` `/3` was ruled at the cut (decomposition v10.0 s.8): chain A moves no dossier input, so without the bump
     `write_one`'s no-op would have written 0 on every name.
3. **`l-4`: the premise was corrected by measurement** (row `Z-W3-S7`): the underscore key does NOT miss a stamp --
   `security_key()` passes it through, a stamp resolves, but the landed raw is keyed by the Bloomberg string, so the figures
   come back empty and read as a false ABSENT. The refusal keys on no stamp OR empty figures; the 97-key regression proves
   no real key is refused.
4. **Merges** under device git contention: `l-4` `120ff9b27f`; `l-2` `58d076cc23` and chain A `5b0b728ab1`, each with the
   append-only channel conflict. Git interleaved the two sides' rows line by line, so both were rebuilt as OUR file plus the
   branch's new row blocks intact (ids unique, JSON valid, row gate OK on `--continue`).
5. **The dossier rewrite at `/3`** -- pair COO `1323991818` / CTO `0db5dfb586`; entry `amgt-corpus-r10-dossier-rewrite` (open
   `16616ff753`, CLOSED in this commit): `names 95 written 95 existed 0`; objects 656 -> **751**; served the last write 95 of 95;
   `current_method_available 95 stale_pick 0`; the served case census byte-identical to the before-state. **The prediction
   held exactly this time** because the half read the count per name from the join (round 9's miss, corrected).
6. The CTO half's first request (26457) read OFFER-EXHAUSTED; three watcher rows for `1.0.0_SA_CTO~Z` looked like orphans.
   `0.0.0_AB_MSTR~Z` measured one live watcher at 06:19Z and places the missing READ clock on a broker hang ~04:25-04:55Z.

## 3. The one real run (`evidence/r10_real_run.txt`, on the served table after the rewrite)

- ML_FP_Equity base: `unit_as_written` U+20AC, `currency` EUR, "symbol maps to one ISO code equal to the listing".
- AZN_LN_Equity base: U+00A3, `currency` null, "symbol's currency differs from the listing" (GBp), Price 2026E `131.91`.
- TSM_US_Equity base: ABSENT, "... row 'EPS' has 14 of 15 cells; the empty cell's position is not recoverable ...".
- `base_census` on the served state: unchanged; `l3_six.py`: `absent_specific 6 absent_generic 0`.

## 4. The team-vs-rule Base census, for the analysis (read-only; it grades nothing)

`both 22`, `median_ratio 0.6931` (team / rule), `within_10pct 5`. **All 8 names beyond 2x have the RULE higher than the team**
(ADBE 0.29, CELH 0.09, MELI 0.47, NFLX 0.37, NOW 0.33, UBER 0.49, WDAY 0.25, ZTS 0.46; paired on the rule's FY1 consensus-EPS
year: 2026E on 20 names, 2027E on INTU, NKE, WDAY). No name is beyond 2x the other way. `team_only 6` are the rule's
`currency_mismatch` / no-consensus names; `rule_only 49` carry no readable team table. Row `Z-W2-S12`: ORA_FP and SAP_GY pair a
`$` team figure with a EUR listing (units printed, never converted).

## 5. Rows -- dispositions for the L9

| row | class / standing | disposition asked |
|---|---|---|
| `Z-W1-S12` | INERT | CLOSE: the six served ABSENT with their own reason |
| `Z-W1-S13` | ARMED -> disarmed by `Z-S56` | CLOSE |
| `Z-S56` | INERT | the disarm carrier |
| `Z-S55` | INERT (the CTO's) | CLOSE: `cases-report` refuses the underscore key (l-4) |
| `Z-W3-S7` | INERT | READ: the corrected mechanism behind Z-S55 |
| `Z-W2-S12` | INERT | OPEN -> analysis: dollar team figures on EUR listings |

## 6. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9

- **`l-1` AC3** -- *does every served case's unit say only what the pack states, with a currency only where the pack and the
  listing agree on exactly one?* The artifact is the served table (751 objects; `read_dossier` any name); the ten symbol-bearing
  names are listed in the l-1 worker's report and s.3.

## 7. Enrichment candidates for the round-10 analysis

1. **The rule's Base runs high against the team's** (s.4): a read of the EPS / P-E pairing on the 8 names beyond 2x, all one
   direction -- the analysis's call whether it is the rule, the year pairing, or the team's multiple.
2. **The blank Base cell (Z-W1-S12's six):** a positional read of the pdf page (x-coordinates at extraction) would place it
   without arithmetic.
3. **Dollar figures on EUR listings (`Z-W2-S12`)** -- whether the pack means USD is not decidable from the payload.

## 8. Bounds and residue

- No vendor or gateway call. Served-plane writes this round: 95 dossier objects; no delete.
- Worktrees `/c/tmp/wk-crps10-1..3` and older (`wk-crps7-5`, `wk-crps8-1..3`, `wk-crps9-1`) hold only workers' untracked
  scratch and the copied check files; removal is a forced delete on the operator's word, as are the `%TEMP%` dirs.

-- `2.0.0_SA_COO~X`
