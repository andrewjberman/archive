# AMGT_RESAPP round 90 -- the issuer's reads (`AMGT-oo-2`, `AMGT-oo-4`, and the measurements behind decomposition s.98a)

Each read answers its question; a read that finds a defect becomes a later-round cell, never a mid-round one. Scripts and result
files: `round90_prep/reads/` (read-only: GETs of `opal-data-portal-v2` scanner universes, `opal-data-harvest` crosswalk and filings
objects; nothing written). Run 2026-10-11 ~05:3xZ on dell1.

## oo-4 / D1-S14 non-US rows -- how many does the identity pool resolve? (CTO ruling, analysis section 2)

Scanner: six universes, asOf 2026-10-02 on all six, 2,854 distinct tickers: 1,038 United States alphabetic tickers (the DEMQUE
request's rows) and 1,816 others. Identity pool: `crosswalk/v1/<latest>` holds **243 records, all MEASURED: 188 under a `US`
Bloomberg form and 55 non-US** (LN 11, FP 7, JP 7, SW 5, MM 4, HK 3, NA 2, BZ 2, CN 2, IM 2, PM 2, TT 1, IN 1, SM 1).

| question | count | denominator |
|---|---|---|
| non-US scanner rows the pool resolves on the scanner's own ticker | **0** | 1,816 |
| non-US scanner rows whose ticker equals a pool non-US root (resolvable only after an exchange-suffix form is BUILT from the row's country) | **7** | 1,816 |
| United States alphabetic rows the pool resolves under `<T> US` | 138 | 1,038 |
| alphabetic tickers whose country is not United States (ADR-shaped) resolving under `<T> US` | 0 | 92 |

**Answer.** The pool is the held set (243 names), and the model-block pool states CRNCY only for the names we hold (round 89, s.97a).
So "a row the pool resolves gets its currency from the price source on its pool identity" is ALREADY what nn-2 plus
`price_currency.price_currency_fields` do for the 138 resolvable US rows; for the non-US rows the pool resolves none on its own
forms and at most 7 after a form is built (a country-to-exchange builder is the parser the ruling refuses). Each non-US member
already serves its plain reason (`REASON_NO_RECORD`). **No build cell is cut: it would move 0 of 1,816 rows.** The decision this
leaves is the CTO's (one message): accept the honest absence for non-US rows, or widen the DEMQUE request once an identifier form
for the 1,816 is stored. Side finding: 138 of the 1,038 rows in the filed request are held names whose currency is already served.

## oo-2 / Z-W266-S3 -- BABA, PBR, SAP: which lost driver points are LOCATOR and which are EXCERPT?

Stored objects read: `filings/v1/<key>/<accession>.analysis.json` (the driver, its `points` and `held_uncited`) and
`.source.json` (the exact excerpt the verifier received, `excerpt.text`). For each held point: (a) is the emitted period token in
the excerpt, (b) does the value occur as a whole number anywhere in it, and what does the surrounding text say.

| name (excerpt chars) | period, value | verifier's reason | the value in the excerpt | class |
|---|---|---|---|---|
| BABA 000119312526231755 (150,078) | FY2025, 118,028 | no period label for FY2025 | 4 occurrences, in the table row `Cloud Intelligence Group \| 106,374 \| 118,028 \| 158,132`; the period appears as `2025` and `March 31, 2025`, never as `FY2025` | LOCATOR (label form) |
| BABA | FY2026, 158,132 | no period label for FY2026 | same row; the period appears as `2026` and `March 31, 2026` | LOCATOR (label form) |
| SAP 000110465926020058 (113,823) | 2023, 13,745 | value not found as a whole number inside the block carrying the 2023 label | once, inline: `to <euro sign> 18,078 million in 2024 (2023: <euro sign> 13,745 million)`; the 2023 token's block (to the next located label) does not contain that sentence | LOCATOR (block model) |
| SAP | 2025, 21.05 | value not found as a whole number inside the block carrying the 2025 label | twice: `<euro sign> 21.05 billion ... in 2025 (2024: <euro sign> 18.08 billion)`; `_WHOLE_NUMBER_RE` tokenizes `21.05` as `21` and `05`, so a decimal can never equal | LOCATOR (decimal) |
| PBR 000129281426002168 (70,023) | 2025, 2.99 mboed | value not found as a whole number inside the block carrying the 2025 label | 0 occurrences of `2.99`, `2,99` or `2.9`; the series name `Total oil and gas production` also occurs 0 times in the excerpt | EXCERPT |

**Count per class: LOCATOR 4, EXCERPT 1, of 5 held points on 3 names** (SAP also carries 1 verified point, 2024 = 18,078,
span 129709-129715). Code: `lib/research/filings/analyze.py` `_WHOLE_NUMBER_RE` and `_find_value_span` (:1068-1080),
`locate_period_labels` (:1083-1096), `verify_points_against_excerpt` (:1146-1177), `_apply_point_verification` (:1282-1357).

**Owner.** The four LOCATOR defects are in `analyze.py`, which this project's decomposition cites 7 times and edits; the tree holds
three AMGT projects (AMGT_HARVST, AMGT_CORPUS, AMGT_RESAPP) and no AMGT_FILINGS, so the write surface is this project's. Per the
analysis, they become a ROUND-91 cell (not cut now: the round-90 list is frozen at the cut). The cell's discriminating checks
already exist in this table: each of the four values must verify against its own excerpt, PBR's must stay held with its reason,
and a value that is in no block must still be refused (the verifier must not become a free-text match). A stored-object
re-verification (`reverify_stored_thesis_driver`) is the producer-side act that makes BABA, SAP and the other names' charts
change; no redeploy of the served function is needed for it.

(The excerpt prints SAP's currency sign as a replacement character in a cp1252 terminal; the filing reports in euros.)

checked 2 of 2 issuer reads (D1-S14 non-US, Z-W266-S3)
