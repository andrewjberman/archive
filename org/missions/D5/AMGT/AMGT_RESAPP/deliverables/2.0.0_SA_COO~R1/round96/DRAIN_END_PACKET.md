# AMGT_RESAPP round 96 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-11 ~19:3xZ. One order, terminal: `AMGT-bc-1`, a READ (nothing served, nothing changed, no Bloomberg call).** Round 96 implements the CTO~DELL1 round-95 analysis
`ledger/ROUND_ANALYSIS.round95.md` section 3 (item 1; msg 4075, ADDENDUM 1 msg 4080); decomposition s.104; issuance @54fd0c8c7d. `round-close-check.py --round 96`: orders 1,
proof_ok 1 of 1, judgment 1, graded 0, **verdict REFUSED on exactly that one ungraded judgment (`bc-1` AC2, the CVO's); the mechanical criterion is YES.** `dep_stage` is left at
EXECUTING until the CVO grades it.

## 1. Orders, cells and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-bc-1` | 1: READ whether the stored Bloomberg-fed data for the exchange-qualified listing of SAN FP and CSL AU carries a sector or industry field | complete, merged @91ad4b03f2, status @e9be0639c6; **AC2 is the CVO's judgment** | worker ~392 @60a45d6d6c, proof VALID; the reading `deliverables/0.9.0_WK_AMGT_RESAPP~392/BC1_LISTING_SECTOR_READING_20261011.md` |
| `AMGT-bc-2` | the serve (a withheld listing serves its own model block's sector, source named) | NOT in this round: ready for the CTO's round-96 analysis (section 6) | the order drafted and its census dry-run; see section 3 item 1 |
| `AMGT-bc-3` | the DEMQUE answer's reader (pp-4) | STAGED, no order | no quote, no answer |

## 2. The issuer's ONE REAL RUN at close

- **bc-1: the issuer re-read the stored objects itself (S3 GET), not the worker's report.** The newest stored model block of each key, `figures[3]`:
  `derived/model_block/SAN_FP_Equity/20261011T130935Z` `{mnemonic GICS_SECTOR_NAME, value 'Health Care', source bloomberg-dapi}`; `derived/model_block/CSL_AU_Equity/20260930T093804Z` the same
  value; the control `derived/model_block/BA_US_Equity/20261011T130241Z` 'Industrials'. The shape check `r96_sector_reading_check.py` reads 8 of 8, YES (the base read NO).
- **OUTCOME: SECTOR-SERVED** (both listings). What the reading states about its own limits: the field dictionaries hold exactly one sector-class mnemonic (`GICS_SECTOR_NAME`; no
  `GICS_INDUSTRY_*`, BICS or `INDUSTRY_SECTOR`); the reading's first sweep, over key names only, read the control as matched 0 and was discarded because the model block stores each field as
  a `{mnemonic, value}` record; **NOT read: bestdata, segments, identity, exec_officers, histdata, silver/listing_hit, and the equity reference tables of opal-data-assets**; CSL AU's stored
  objects end 2026-09-30 (model block) and 2026-09-19 (refdata). The reading also records that the crosswalk folder names SAN FP's issuer 'Sanofi SAN FP' while the table row `SAN` names
  'Banco Santander S.A. ADR' (the round-94 collision; the page behaviour is not the reading's to decide).
- **Nothing was written and no Bloomberg call was made** (`WRITES: none`, `BLOOMBERG CALLS: none`; S3 GET and DynamoDB GetItem only).

## 3. What the issuer got wrong, and what it cost (the CVO's L9 read)

1. **A conditional serve cannot be cut as a new order mid-round.** The CTO's item was "read first; if yes, serve it under its own pair". I staged the serve as `bc-2` with no order; when the
   read came back SECTOR-SERVED I wrote the order and the gate REFUSED it: ONE ISSUER PER ROUND is keyed to the round (Rule 27), and round 96 already had its issuance. The correct
   cut, which round 94 used for `aa-5`, is to write the staged order AT the issuance with its condition on its face. Cost: the serve moves to round 97's issuance (one L9 and one analysis),
   which the CTO's own wording ("by round 96's close") had not expected. I did not take the audited `# pipeline-override`: the cost of waiting is a round, not a served byte.
2. **Before the order was refused I had re-based two reused checks** (`r95_classification_census.py` K1-K3 and K6, `r94_display_name.py` D10) so that "no field of the TABLE row is
   served" holds for a null classification OR the listing's own model-block sector: the lesson of round 95's D10 applied in advance. They are committed (both read as before at the base).

## 4. JUDGMENT for L9

**One judgment criterion: `AMGT_RESAPP.TO-AMGT-bc-1` AC2 -- the outcome (SECTOR-SERVED) follows from the evidence, the control and the named surfaces.** Offered for the CVO's own re-run:
`r96_sector_reading_check.py` on the reading; the S3 read above (three objects); `r96_sector_serve_census.py --where deployed` (the live base: K1-K4 FAIL because nothing is served yet).

## 5. Rows filed this round

Worker: `D1-W392-S1` (the order named `resolve_identity` in `crosswalk.py`; the module has `resolve()`), `S2` (a key-name sweep is blind to the model block's mnemonic-record plane and to the
table's derived sector; the corrected run is the one reported), `S3` (CSL AU's stored objects end 2026-09-30 and 2026-09-19): all OBSERVATION, INERT. RA1: none. Issuer: none new.

## 6. For the next round (the ENRICHMENT LIST's inputs; the CTO's ruling at msg 4080)

1. **`AMGT-bc-2`, the serve (ready):** a security whose table row is withheld serves its own model block's `GICS_SECTOR_NAME` in the three places the classification is withheld (ranked
   row, rank series, collected-chatter row), `sector_source` `model_block.GICS_SECTOR_NAME` and `sector_as_of` the block's vintage, `asset_class` and `sub_asset_class` null, a failed or
   empty read staying withheld with the round-95 reason. Drafted at `deliverables/2.0.0_SA_COO~R1/round96_prep/BC2_ORDER_DRAFT_FOR_ROUND97.md`; `r96_sector_serve_census.py` reads
   K1-K4 FAIL at the live base and 6 of 6 against a throwaway candidate (2 ranked rows, 2 rank series, 3 chatter rows served 'Health Care'; 186 and 186 control rows unchanged).
2. **`AMGT-bc-4`, its redeploy (ruled, msg 4080):** it rides the redeploy that carries AMGT_CORPUS's /13 files (one redeploy, two pairs, each admitted by blob), which also retires the
   scratch pin `b3512d18fb`; if that has not happened by the close of the round that merges bc-2, a scratch pin parented on `b3512d18fb` plus only bc-2's files, under its own pair
   (a pin from `15b7af1601` again is refused).
3. **CSL AU's sector would read as of 2026-09-30** (its newest stored model block): the served `sector_as_of` says so. Whether a stale vintage is served or withheld past some age is the CTO's
   call, not a cell I cut.
4. **ss-7 / pp-4** when the DEMQUE answer lands. `AMGT-nn-6`, the portal PROD promote (`dell1-20261011T033643Z-e7f2`: the breakdown is delivered; Andrew's answer is his), FWD-16 and the model
   API key stay Andrew's.

checked 1 of 1 orders terminal, 1 of 1 proofs VALID, 1 judgment criterion ungraded (the CVO's)
