# AMGT_RESAPP round-83 PREP -- why ASML NA's business text never reached the served /thesis (row D1-W324-S1, T3)

Grounding fork of `2.0.0_SA_COO~R1`, 2026-10-09 ~08:5xZ. READ-ONLY: stored objects read by VersionId (no model call, no write).
Objects: the silver part `date=2026-10-09/part-20261009T082333Z.parquet` (k3bWqFRP), the analysis `X5YQ7V_E` and the drafting
`MZN0U0Q6` (both non-latest after gg-2's rollback), bucket `opal-data-harvest`.

## The excerpt was right

The repaired cutter delivered all three items, in order: `ITEM 4.B. BUSINESS OVERVIEW` at offset 0, `ITEM 3.D. RISK FACTORS` at
60,030, `ITEM 5.` at 114,023 (145,654 chars; Item 4.B truncated to 60,000 of 91,976 by the excerpt cap).

## Cause 1 (the T3 failure): the passage map drops almost all of Item 4.B

`lib/research/filings/passages.py:221-233` `build_passage_map` makes ONE passage per excerpt LINE and treats every line shorter
than `_MIN_PASSAGE_CHARS = 60` (`:177`) as a heading. ASML's 20-F business section is laid out in narrow columns:

| item | non-blank lines | median line | lines >= 60 | passages | chars covered |
|---|---|---|---|---|---|
| 4.B Business Overview | 1,739 | 38 | 8 | **8** | **627 of 58,260 (1.1%)** |
| 3.D Risk Factors | 989 | 61 | 602 | 602 | 38,930 of 52,980 (73.5%) |
| 5 OFR | 943 | 27 | 55 | 55 | 5,890 of 30,636 (19.2%) |

`analyze.py:411` sends the model ONLY the passage map as content blocks, so the model saw 8 lines of the business section
(23,978-24,087 and 59,507-59,595 are two of them). Every served citation then had to come from Risk Factors or OFR: the 5 served
sentences cite P0641/P0611, P0180-P0184, P0027-28, P0640, P0637 -- 0 from Item 4.B, which is AC2 T3's 0 of 11.

## Cause 2 (the 14 refusals): cross-line quotes fail the one-passage gate

The model's citations span consecutive one-line passages. The citations API concatenates the cited blocks with NO separator, so
a quote reads `continue torise` where the filing has `continue to` / `rise`. `lib/research/drafting/pipeline.py:150-159` checks
each span against EACH cited passage separately (`verbatim.check_against_sources`, `verbatim.py:113-127`).
Measured over the analysis's 83 citations: verbatim in one cited passage **19 of 83**; in the cited passages joined with a space
19 of 83; joined with `""` **83 of 83**. All 14 refused sentences cite 2-4 consecutive passages (`dropped_reasons`), and 391 of 488
adjacent passage pairs end and start on a letter or digit, so a `""` join glues a word.
The draft's denominators: 40 drafted, 5 served (all on span), 21 held with no span, 14 refused.

## Smallest repair

One change in `build_passage_map` fixes both causes: build passages at PARAGRAPH grain. Join each wrapped line into the passage
it continues, with a single space, and keep its start and end offsets. A line is a continuation when the passage so far does
not end in sentence-final punctuation (`. ! ? :`) and the line does not stand alone as a heading. Treat a short line as a heading
only when it is followed by a new paragraph. ASML's business text then becomes passages, and a quote spanning wrapped lines is a
substring of ONE passage, so the gate needs no change. `passages.py` is a site-Z producer path only while an active site-Z producer
imports it; the analyzer task is disabled (CTO msg 1267 rule), so the merge needs the usual check, not assumed.

Not the repair: loosening the gate to accept a `""` join. That would admit `torise`, which is not in the filing.

## Offline check for the round-83 cell

`round83_prep/checks/r83_passages.py --crit AC1` reads only the stored silver part (by VersionId, or `--cache`) and runs
`build_passage_map` in-process:
- P1: Item 4.B passage coverage of at least 50%. Base: 1.1%.
- P2: 0 adjacent passage pairs that glue a word under `"".join`. Base: 391 of 488.

Base verdict: **R83 PASSAGES AC1: NO**, exit 1, on py3.12 and py3.14. ruff py39 is clean.
The served proof (`r81_store.py` AC2 T3) still needs the store half re-run after the repair, with one model call per name.

## The offline run (the proof a round-83 cell gives BEFORE any store write)

Run in the worker's worktree, after the `build_passage_map` repair, with `py -3.12` (anthropic SDK 0.84). No SEC fetch: the input is
the round-82 parser-2.0.0 excerpt already stored (silver part `part-20261009T082333Z.parquet`, VersionId `k3bWqFRPQhvTephepe01vjYL0sPgTcky`,
superseded by the rollback part but kept by versioning). The passage map is rebuilt from that excerpt inside the analyzer, so the
repair is what the model sees.

1. The source object, read only (no write):
   ```
   cd <worktree> && mkdir -p .scratch/r83_offline && .tools/aws s3api get-object --bucket opal-data-harvest \
     --key sec/harvest/silver/filing_source/date=2026-10-09/part-20261009T082333Z.parquet \
     --version-id k3bWqFRPQhvTephepe01vjYL0sPgTcky .scratch/r83_offline/silver.parquet
   cd <worktree> && PYTHONPATH="$(pwd)" py -3.12 -c "import io,json,pyarrow.parquet as pq; from lib.research.harvest import filings as hf; r=[x for x in pq.read_table('.scratch/r83_offline/silver.parquet').to_pylist() if x['security_key']=='ASML_NA_Equity'][0]; json.dump(hf.source_object_from_row(r), open('.scratch/r83_offline/source.json','w',encoding='utf-8'))"
   ```
2. The analysis and the draft, ONE call, the key read into that call's environment and never printed:
   ```
   cd <worktree> && ANTHROPIC_API_KEY="$(comp-secrets get anthropic-api-key --reveal --value-only)" PYTHONPATH="$(pwd)" \
     py -3.12 -m lib.research.filings.analyze --security-key ASML_NA_Equity \
     --source-json .scratch/r83_offline/source.json --no-fetch --no-cache --out-dir .scratch/r83_offline/out
   ```
   It ends `NOT-UPLOADED (no --write-pool): ...` for both objects. Output files:
   `.scratch/r83_offline/out/filings_v1_ASML_NA_Equity_000162828026011378.analysis.json` and
   `.scratch/r83_offline/out/drafting_v1_ASML_NA_Equity.json`.
3. The grade:
   ```
   cd <worktree> && PYTHONPATH="$(pwd)" py -3.12 org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1/round83_prep/checks/r83_offline.py --crit AC1 \
     --analysis .scratch/r83_offline/out/filings_v1_ASML_NA_Equity_000162828026011378.analysis.json \
     --draft .scratch/r83_offline/out/drafting_v1_ASML_NA_Equity.json --excerpt .scratch/r83_offline/silver.parquet
   ```
   and `r83_nokey.py <worktree>/.scratch <worktree>/org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~<n>` reads YES.

**Why no store write happens** (read at HEAD):
- `analyze.py:1568-1570`: `--source-json` returns the file's object before any pool read, cache or fetch, and `--no-fetch` is belt and
  braces.
- `analyze.py:1698`: the UNRESOLVED-SOURCE state put runs only under `--write-pool`.
- `analyze.py:1717`: `--no-cache` sets `cache_dir` None, so `save_pass_1` (`:455`, a LOCAL file) is not called (`:1415`).
- `analyze.py:1609-1655` `write_outputs`: `--out-dir` writes local files (`:1639-1645`), and `crosswalk.write_pool` runs only when
  `write_pool` is true (`:1648-1650`); without the flag each receipt is `uploaded: False`.
- `analyze.py:1770`: `main` passes `write_pool=args.write_pool`.
- The drafting document is built in-process by `build_drafting_document` (`main`, before `write_outputs`); no separate drafting step
  or splice is needed for the proof.

**Base dry-run** on the rolled-back round-82 objects (analysis X5YQ7V, draft MZN0U0Q6, excerpt from the silver part):
O1 FAIL 0 of 5 served sentences cite Item 4.B (the 4.B band has 8 of 665 passages); O2 PASS 5 of 5; O3 FAIL served 5, held 21,
refused 14 of 40; `R83 OFFLINE AC1: NO`, exit 1. `r83_nokey.py` on round83_prep: YES (7 files, 0 values); on a planted file: NO.
Cost of one offline run: two model calls, about USD 0.47 at round 82's measure.

Side observation, not in scope: the stored excerpt carries split words from the PDF-like layout (`Th e`, `r esulting`); a quote
across such a split still matches only if the model copies it as stored.
