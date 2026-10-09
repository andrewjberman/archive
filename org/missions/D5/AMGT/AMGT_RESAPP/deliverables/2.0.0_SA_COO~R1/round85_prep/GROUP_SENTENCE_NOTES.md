# AMGT_RESAPP round-85 PREP -- machine sentences doubled and run together (CTO~DELL1 round-84 analysis item 1)

Grounding fork of `2.0.0_SA_COO~R1`, 2026-10-09 ~12:1xZ. READ-ONLY: live /thesis bodies read through the function, NU's drafting
(`drafting/v1/NU_US_Equity.json`, VersionId xe0hxE3l...) and analysis (`filings/v1/NU_US_Equity/000129281426002166.analysis.json`,
AWjDrLYs...) read by get-object. No model call, no write.

## What is served (live 66MDfT5i, `drafted_sections[].sentences[].text`)

| name | served sentences | glued boundary | states one fact twice (figures) |
|---|---|---|---|
| ASML_NA_Equity (capture 004's key) | 21 | 0 | 0 |
| BABA_US_Equity | 20 | 0 | 0 |
| NU_US_Equity | 38 | **25** | **14** |
| PBR_US_Equity | 26 | 0 | 0 |
| SAP_GY_Equity | 18 | 0 | 0 |

The shape (NU, every one of the 25): a model paraphrase, then -- no space -- the filing's own sentence stating the same fact:
"Total revenue reached US$15,774.8 million in 2025, up US$4,257.8 million or 37.0% from US$11,517.1 million in 2024.Total revenue for
the year ended December 31, 2025 was US$15,774.8 million, an increase of ...". 14 of the 25 repeat two or more of the same figures; the
other 11 restate in words (e.g. a risk heading sentence then the verbatim risk sentence). ASML's capture 004 shows a different, smaller
artifact: the cited PASSAGE (evidence) text, not the sentence, carries the running-header lead-in and spaces before punctuation
("billion , primarily") -- that is the filing's own extracted text and is not this item.

## Cause -- the PRODUCER, not the serve path

`lib/research/filings/analyze.py` joins the model's response text blocks with NO separator:
- `:643` `annotated = "".join(annotated_parts)` -- the pass-1 annotated text (stored as `pass_1_text`, then split into `items`);
- `:427` and `:502` `"text": "".join(text for text, _ in blocks)` -- the raw pass-1 / pass-2 text.

With the citations API the model emitted an UNCITED block (its paraphrase, ending "...in 2024.") followed by a CITED block (the
filing's sentence, echoed verbatim). Joined with "", one numbered item line becomes "paraphrase.Verbatim [P0563]". The glue is stored at
every layer measured: NU's analysis `items/{risks 13, guidance 8, segments 8, commentary 7}[].text`, `pass_1_text`, and the drafting
document's `sections[].sentences[].text` and `.text_original` (25 each). The serve path (`scoped_amgt.py`) passes the stored text through
unchanged. Why only NU: the same analyzer ran ASML (round 83) and BABA/SAP/PBR (round 84) and the model did not emit the
paraphrase-then-quote pair there -- it is a reply shape the joiner does not guard against, so any future re-analysis can hit it.

## Smallest repair (producer) and what it costs

1. `analyze.py`: join adjacent response text blocks with ONE space when neither side ends/starts with whitespace (`:427`, `:502`,
   `:643`) -- removes every glued boundary.
2. "Served once": when an item line is an uncited sentence immediately followed by a cited block restating it (identical after
   normalisation, or sharing two or more figures), keep the CITED block -- it is the verbatim text the drafting gate checks
   (`quoted_spans` must lie inside the sentence) -- and drop the uncited lead. Keeping the paraphrase instead would fail the verbatim
   gate, because the quoted span would no longer be in the sentence text.
3. **Re-store:** the stored `pass_1_text` has lost the block boundaries, so NU's stored drafting cannot be repaired by re-joining; NU
   needs ONE re-analysis (one model run) through the repaired analyzer, under a store-half pair with the four-prefix write trace
   (conditions 5-7). The other four names serve 0 glued and 0 restated: no re-store owed. No redeploy: the function serves stored text.

## Check

`round85_prep/checks/r85_sentences.py --crit AC1 [--where deployed|stored|local]` -- S1 restated, S2 glued, S3 no name below its base
sentence count (`r85_sentences_base.json`, recorded at the base: ASML 21, BABA 20, NU 38, PBR 26, SAP 18). Base reads (deployed and
stored agree): S1 FAIL 14 of 123, S2 FAIL 25 of 123, S3 PASS, `R85 SENTENCES AC1: NO`, exit 1. Controls: the NU shape reads restated;
two distinct figure sentences and a "U.S." abbreviation do not.
