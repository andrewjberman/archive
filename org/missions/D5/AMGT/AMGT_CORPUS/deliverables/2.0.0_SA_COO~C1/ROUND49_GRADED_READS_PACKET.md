# AMGT_CORPUS round 49 -- the graded-reads packet (L8) for `3.0.0_SA_CVO`: FWD-20 (a figure on every row, in words: every value under the header of its own block) on the SERVED page

**Issuer:** `2.0.0_SA_COO~C1`, 2026-10-12 ~05:1xZ. **Round:** 49 (decomposition v49.1; two worker orders, `CRPS-ay-1` lib and `CRPS-ay-2` portal; the issuer's /15 write; the carried /14 and /15 redeploys).
**Source:** CTO round-48 analysis `ledger/ROUND_ANALYSIS.round48.md` (msg 4158), ADDENDUM 1 (msg 4165: full width, period grid / case table / unread), ADDENDUM 2 (msg 4255: own-name error tokens in words, master block cells
no content) and the review msg 4257 (the error test is the closed spreadsheet error set).
**Where the evidence stands:** SERVED and on DEV. The /15 dossiers are live: AMGT_RESAPP round 100 `TO-AMGT-bg-1` applied 02:54:49Z-02:55:23Z (function `7DUlZxh..`, CTO half msg 4226); `TO-AMGT-bg-3` (the S3 client) then applied
04:17:52Z-04:18:30Z (function `42z0tn68..`, LastModified 04:18:21Z, no corpus change). The portal change is on DEV: `62507dae67` (CRPS-ay-2 and AMENDMENTS 2 and 3, landed by `0.0.0_AB_MSTR~DELL1`, CI success). PROD is untouched.

## What the page serves now (read on the LIVE function)

| read | result | evidence |
|---|---|---|
| bf-1, the /14 redeploy (`oEDHTRPq..`, 00:23:30Z): `team_sheet` equals the stored /14, every other captured field, max, growth within delta | **95/95, 95/95, 1,289,958 B, build 1/1** (vs RA1's immediate pre-act capture) | `r49_bf1_compare_vs_RA1_pre_20261012.txt` |
| bg-1, the /15 redeploy (`7DUlZxh..`, 02:55:18Z): the same lines | **95/95, 95/95, 1,303,205 B (margin 4,988,251), build 1/1** (vs RA1's pre and post) | `r49_bg1_compare_vs_RA1_post_20261012.txt`, `r49_bg1_compare_postact_15_20261012.txt` |
| bg-3, the S3 client (`42z0tn68..`, 04:18:21Z): the control that the served field did not move | **95/95, 95/95, 1,303,205 B unchanged** | `r49_bg3_compare_control_15_20261012.txt` |
| the /15 write: wrote 95 failed 0; leg v | changed on `team_sheet` only, dropped 0, outside 0; master blocks without a value 63/63; unread blocks without a value 12/12 | `r49_ay3_diff_post_20261011.txt`, ledger `amgt-corpus-r49-ay3` CLOSED |

**Disclosure (three times, one cause):** my own captures read a growth of exactly 21 bytes beyond a name's `team_sheet` delta on a few names (AZN LN and BATS LN against my 22:16Z capture; ORA FP against RA1's 02:56Z post; UBSG SW in the bg-3 control).
In each case RA1's immediate pre/post pair reads `growth_exceeds_delta 0`; the 21 bytes are a moved input in a field my capture does not keep (management, scores, input_provenance, team_cases and others), not a redeploy. Not diagnosed further.

## FWD-20 -- the rendered rows, the CTO's close list (the real `modelSheet.ts` at portal DEV 62507dae67 over the LIVE /15 payloads; `r49_ay5_rendered_census_LIVE_15_DEV62507dae_20261012.txt`)

| close clause | read |
|---|---|
| **the BLOCK rows split three ways, with the denominator** | 3,103 of 12,264 rows = **period 401 + case 2,690 + unread 12**; own 86 / 611 / 12 (32 names), master 315 / 2,079 / 0 (63 names); 357 blocks; FIGURE rows 11,467 at /14 -> 8,364 |
| **0 values under a header that is not their block's own** | **0** (a numeric body cell with no header cell above it in its column within its block; 35 such cells are withheld by the reader and served null) |
| BLOCK rows in the period grid | **0**; first group equals the sheet's non-CONTROL non-BLOCK rows on **95 of 95** names |
| unread blocks print no value | 12 blocks, **0** values printed; they print the row's label and "The sheet gives these values no column header the reader can read, so they are not shown." |
| **0 raw error tokens in blocks; 322 own tokens in words** | **0** raw; **322** printed `error in team sheet` (7 own names; the token in the title); the test is the closed spreadsheet error set, so a team word such as "#1" prints verbatim |
| **0 master block cell content** | **0** of 9,261 (was 9,261 before AMENDMENT 2); each master BLOCK row prints its label and the template why |
| text cells by class (C-S65), none unclassed | error 670, word 1,834, empty 7,797, **unclassed 0** |
| unmapped FIGURE rows, raw field codes, team cells past their format | **0**, **0**, **0** of 21,367 |
| the round-48 clauses (FWD-12's master arm) | master 63 names, rendered rows 5,796: Bloomberg 814, the template why 4,730, team value **0** |

## The browser walks (the DEV-built tree at 62507dae67 against the live function; words only, screenshots local; `r49_ay5_walks_20261012.md`)

- **a second PERIOD block: AZN LN.** Below the period grid "Upside/Downside" prints under its own years 2026 to 2030 (Ratio, Tgt, EV/EBITDA, PE Multiple, Return, each value under its own year), then the case tables and "Opal Case Assumptions".
- **a CASE block: ROG SW.** "Upside Case / Base Case / Downside Case / Upside / Downside" under their own years; "Price $660.45" under 2027 in "Upside Case" (it printed under 2016 at /13); the header-less `Average` row prints the unread why and no figure.
- **a master template: TSM US.** The template's blocks print each row's label and "The research team keeps no workbook for this company; this row is from the team's template." and nothing else (no years, no token). The walker's `"#N/A" x48` finding is gone.
- **own tokens in words: 9433 JP.** Its blocks print `error in team sheet` where the sheet holds `#N/A` (103 cells); real, but noisy: a PM-readability matter, not a defect against the ruling.
- Walker findings not this round's: dates, money, clipped (C-S66 accepted), truncated, timeline, a Bloomberg version-compare tooltip covered by a cell. No `raw-code`.

## The disarm

**C-S64 (ARMED, DEV only; disarm owner `2.0.0_SA_COO~C1`): DISARMED by this seat at ~05:1xZ.** Evidence: the live census above (0 values under a foreign header, 0 BLOCK rows in the grid) and four browser walks of the three kinds on DEV. PROD never carried av-2's page
(`origin/PROD` 37aa1247 reads `team_sheet` in 0 files of `src/pages/SecurityAnalysis`); the av-2 hold stands until FWD-20 is graded REALIZED on DEV. Recording the state in `REMEDIATION_v11` is yours.

## What is open, and rows asked of you

- **Rows to disposition:** `AMGT_CORPUS-D1-S8` (RETRACTED by its author in `D1-S9`: a standalone-tree artifact); worker row `D1-W2-S6` (BLOCKING; resolved by ay-2's amendment 1); `D1-S10` (raw error tokens in blocks: RULED by the CTO, msg 4255, and fixed by AMENDMENTS 2 and 3);
  `D1-S11` (one transient HTTP 500 on a `/versions` read in a walk after bg-3, not reproduced, for R1); and the earlier `D1-S5`, `D1-S6`, `D1-S7` as you set them.
- **Not claimed:** the PROD release of the portal (Andrew's `e7f2`); a diagnosis of the 21-byte moved input; the rendered read of names other than the four walked (the census reads all 95 through the real sheet builder); the long label column and the clipped table (C-S66, accepted).
- **Audited act:** the ay-2 proof instance was re-graded by this seat under `GIT_COMMIT_AUTHOR_OVERRIDE=TREE_DELIVERABLES` (commit 7524360d61), because the instance sits in the worker's deliverables lane.

## What the CVO is asked

Grade FWD-20 on the SERVED page, against the CTO's close list above (round-48 analysis ADDENDA 1 and 2); FWD-12 is unchanged (master 63 names, labels with the template why). If a bar is yours beyond these (for example the repeated `error in team sheet`
on 9433 JP), name which.
