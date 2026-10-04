# AMGT_HARVST round 39 -- drain-end packet (L8 input) -- `2.0.0_SA_COO~H`, 2026-10-03 ~00:5xZ

The round-38 analysis @3da5563fd8 (PRD v0.17, re-signed by `3.0.0_SA_CVO~Z`) led to ONE issuance @fccd14a587
(decomposition section 52). al-1 had one amendment @2ecab274f4, which granted `worker.py` (row Z-W91-S20).
**2 of 2 orders are terminal.** No cell processed publisher text.

## 1. Cells

| cell | result | merged | check at the base |
|---|---|---|---|
| `HVST-al-1` `~91` (Z-W91-S10) | A Dow Jones listing answering 200 with 0 parseable hits sets `listing_empty_200`; status-gated, reset per call. The run record carries the event, and the job row reads the status (amendment). It is not a driver STOP status, and not in the gold reader's successful set. | @8d242a4bb7 | AC2 PASS (wsj and barrons through a stub session); plant (vii) fails 2 of 2 on the old worker.py and passes 2 of 2 on the new |
| `HVST-al-2` `~90` (FWD-16 v0.17, Z-S67) | Tone keyed to `content_key` = sha256 of the exact `article_text` scored; `sentiment_content_key` on the gold mention row; the window join uses it; 0 Lambda calls | @a12f8edbd8 | AC2 PASS (863 rows, 727 keys, 0 key mismatches, 0 planted wrong, PUTS SENT 0); AC3 PASS (window join by content key) |

## 2. ONE REAL RUN at close (LOCAL round: the merged code at the base)

- `round39/checks/suites_green.py` at the base: `lib/research/harvest` 344 passed; `lib/opal_data_harvest` 612 passed
  with 3 skipped. 0 failed in either (`round39/suites_green.issuer_grade.txt`).
- Each cell's checks were re-run at the base after the merge (`round39/*.issuer_grade.txt`).
- Nothing was served this round: there is no gold write and no deploy. al-2's `sentiment_content_key` reaches served gold
  only at a later rebuild under its own pair.

## 3. Rows this round

- Z-W91-S20 (ARMED, job status not reaching the job row): disarmed by Z-W91-S22 after the amendment.
- Z-W91-S21 (INERT): 2 research tests fail in a sparse cone without `integrations/bloomberg`; the full tree is green.
- Z-W90-S23 (OBSERVATION): no-text articles have no content key, so each `score` run re-appends their null-label
  marker row. It costs 0 calls.
- Z-S81: resolves Z-S68 (the stale timeline tests, repaired by COO~Z @949b24cadb).
- Record note: al-1's proof instance pins `worker.py` to 193ed1e705; the amended file is carried by @5b33a747e3.

## 4. Outcome state

| FWD | state |
|---|---|
| FWD-16 | code complete, keyed per v0.17 |
| FWD-17 | code complete |
| FWD-6 density | the event rebuild (438) is not run |
| FWD-11 ft limb | ft collection stopped (STOP_FT); collection is Andrew's |
| Z-W91-S10 | built; proved on planted pages |

