# L8 drain end -- ADVI_COTBKF round 14

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-07 ~16:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

Round 14 was cut on `1.0.0_SA_CTO~DELL2`'s round-13 analysis @d9877f9754 (msg 812): E1 the re-apply (the issuer's act), E2 the residuals
(cell CB-n-1, issuance @095de9bb5c, `fanout: 1 of 1 chains, cap 8`).

## E1 -- the re-apply (issuer's act, SERVED)

Ledger `advi-cotbkf-r14-reapply-crosswalk-links-20261007` CLOSED 3/3 @ad6d5be150, under the pair COO @cff9b1431a (given: reader census 0 of
135 chains; four pins re-read unchanged) / CTO @d9877f9754. Branch A:
- crosswalk: VersionIds fatOX6x0 -> wv5z6zeR (parquet), RGQHH1zi -> 4MzpNZ7s (csv); read back 1,533 rows, **471 MATCHED** (was 439);
- account links: OQ9YHJ3h -> iSS.QIb0 (parquet), JY3f29AV -> 19fOZaSl (csv); read back 1,450 rows, **212 LINKED**; acct#e1e2dacb -> acct#f6464238
  LINKED; acct#d6187d4b NOT_LINKED (LEFT_COMMONWEALTH);
- the rule-change diff against the newly applied tables: `crosswalk_changed=0 account_links_changed=0`.
The crosswalk's near-match list grew 21 -> 22 (row D2-S25): the list for Andrew/Cottonwood needs refreshing before it reaches the firm.

## E2 -- CB-n-1 the 5 residuals

| order | worker | drain | criteria | real run on dell2 (shared tree, after the drain) |
|---|---|---|---|---|
| CB-n-1 residuals explained | ~30 | @6f3a844f75 | VALID: AC1 PASS, AC2 6 passed (one arm per class + no-residual control) | `RESIDUALS explained=5 of 5 sign_gap=0 vendor_rounding=4 source_gap=1` |

- acct#fa82ce1d / acct#3b5864a2 on 74440B405 (0.029, 0.02): VENDOR_ROUNDING -- a `dvr` re-books a `DVRX`-cancelled reinvestment at a slightly
  different quantity, and the closing `sl` equals the position before the re-booking.
- acct#9bd1ed4d / acct#87772861 on 07399D345 (0.00086 each): VENDOR_ROUNDING -- `CAF` rows at 5 decimals, the closing `lo` at 3.
- acct#2f33cbcc on 60934N500 (0.003): SOURCE_GAP -- one `li` of 0.003 (2025-10-08), no row out; the snapshot still holds it (row D2-W30-S1:
  the class is structural; a grader may read it as a real holding).
All five rebuilt quantities equal their 2026-06-23 snapshot quantity; no sign changed; `commonwealth_signs.py` untouched.

## Rows

| row | class | standing |
|---|---|---|
| D2-S25 | OBSERVATION | INERT -- near-matches 21 -> 22 after the re-apply |
| D2-W30-S1 | OBSERVATION | INERT -- acct#2f33cbcc's class (SOURCE_GAP vs a real holding) |

ARMED: 0. Process note: worker ~30 stamped its row `surfaced_at` 16:40Z, 26 minutes after its commit (the gate warned; committed rows
are not edited). My prompt's example time ("16:30Z") invited it; future prompts carry no example time.
