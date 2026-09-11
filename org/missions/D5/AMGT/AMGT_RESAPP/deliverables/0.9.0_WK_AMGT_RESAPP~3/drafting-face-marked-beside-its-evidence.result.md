# AMGT-s-9 -- session log

Worker `0.9.0_WK_AMGT_RESAPP~3`, task order
`AMGT_RESAPP.TO-AMGT-s-9.drafting-face-marked-beside-its-evidence.md`, same worktree/branch
(`wk-AMGT_RESAPP-1-3`, fast-forwarded to SITEZ @bd93b43b44), third in the `AMGT-s-12 -> AMGT-s-4
-> AMGT-s-9` chain.

## Sequence

1. Tree check, status flipped `staged` -> `pending`.
2. Read the dependencies: `AMGT-s-1`'s three `model_block_*.json` files (BABA_US_Equity,
   BA_US_Equity, SAP_GY_Equity) and my own three `coverage_items_*.json` files (BABA_US, BA_US,
   COST_US) from AMGT-s-4. Measured the overlap: BABA_US/BABA_US_Equity and BA_US/BA_US_Equity
   have BOTH figures and coverage landed; SAP_GY_Equity has no coverage; COST_US has no figures.
3. **Found the figure_ids gap** (filed as `AMGT_RESAPP-Z-W3-S4`): AC2's checker reads a top-level
   `figure_ids` key from each `model_block_*.json`; none of AMGT-s-1's three files carries that
   key (measured: their keys are `security, security_key, raw_stamp_used, fiscal_years,
   fiscal_year_row_count, orphan_price_rows, figures, unresolved`; each figure is identified by a
   `(scope, fiscal_year, mnemonic)` tuple, not a flat id). Consequence: AC2's resolvable id-space
   is coverage item_ids ONLY -- a sentence citing a figure would never resolve under AC2 exactly
   as written. Chose the honest route the cell text's own "item_id|figure_id" OR permits: cite
   only coverage evidence; leave `company_description`/`ceo_bio`/`recommendation` as empty limbs
   rather than cite an id that would fail resolution. Did not edit AMGT-s-1's landed files.
4. Built `lib/research/drafting/schema.json` (the marking contract, part a): sections array,
   required `text/generated/evidence/verbatim_check` per sentence, `generated: true` fixed,
   `evidence` non-empty.
5. Built `lib/research/drafting/verbatim.py` (C-VERBATIM-GATE, part b): `normalise()` (curly
   quotes straightened, case folded, whitespace collapsed -- nothing else, stated exhaustively);
   `check_against_sources()` -- a span not verbatim in ANY cited source's text REFUSES the whole
   sentence.
6. Built `lib/research/drafting/producer.py` (part c): the `Producer` interface and
   `FixtureProducer` (the only implementation) -- hand-written templates, each quoting a literal
   substring of its own evidence's `title`, never inventing content beyond the template. Docstring
   states the three literal substrings AC3 checks for. Excludes `admitted: REFUSE` coverage items
   from drafting (AMGT-s-11's item rule integration).
7. Built `lib/research/drafting/pipeline.py` (part d): `run_pipeline()` -- always emits the five
   limbs (Andrew's ruled order), gates every sentence through the verbatim check, regenerates
   (re-drafts) a refused section up to 2 attempts before dropping any sentence that still refuses
   -- never shipped with a warning.
8. Wrote `lib/research/drafting/tests/test_drafting.py`, AC1's four behaviours as four pytest
   functions (including a curly-quote/case/whitespace normalisation exercise in the difference
   arm) -- PASSED on the first correct run (`4 passed`).
9. Built `lib/research/drafting/run_drafting.py`: reads `coverage_items_BABA_US.json` (evidence)
   and `model_block_BABA_US_Equity.json` (figures, read for transparency only, never cited),
   runs the real pipeline, writes `drafted_sections_BABA_US.json` and
   `drafting_run_summary.json`. Result: 5 sections, 1 sentence (investment_thesis, drawn from the
   PROVISIONAL-admitted Reuters item; the REFUSE-admitted Bloomberg roundup correctly excluded),
   4 empty limbs (honest -- no evidence resolves for them at this cut).
10. AC1-AC5 all PASS-by-output on the first correct run of each (AC4 run in its own Bash call
    per the coordinator's rail note).
11. Wrote `SPEC_SECTION_drafting.md` (part e) for `AMGT-s-5`: the marking requirement (persistent,
    at-a-glance, never hover-only), evidence-beside-sentence rendering, the edit affordance, and
    why four of five limbs render empty today (a real state to show, not a bug to hide).

## AC6 (judgment) -- read for the CVO

The one shipped sentence: `Recent coverage notes that "revenue growth as AI demand accelerates"
(Reuters).` -- the quoted span is verbatim from the Reuters item's own title; the lead-in phrase
("Recent coverage notes that...") is plainly a machine's hedge, not a firm claim ("Alibaba's cloud
revenue accelerated" would read as a firm view; "coverage notes that..." does not). An analyst
reading this would recognise it as a pointer to a news item, not an analytical conclusion --
consistent with FWD-9's bar. The normalisation is exhaustive and narrow (three named
transformations only) -- tested directly against a curly-quote source and a case/whitespace
variant, both cleared correctly; a genuine paraphrase (different words, same meaning) is refused
by construction, since paraphrase is not a substring match under any of the three named
transformations.

## What is NOT done (declared, not hidden)

- The model producer: not wired (bound: no G-24 word for this project). `FixtureProducer` is the
  only producer; its templates are hand-written, not model-generated.
- Figure-cited evidence: not resolvable under AC2 as written (`AMGT_RESAPP-Z-W3-S4`) -- figures
  are read and reported, never cited.
- No `.tsx`: `SPEC_SECTION_drafting.md` is a rendering-behaviour spec only (C-DESIGN-SPEC-FIRST).
- Nothing sent to Adam (C-NO-CONTACT).
