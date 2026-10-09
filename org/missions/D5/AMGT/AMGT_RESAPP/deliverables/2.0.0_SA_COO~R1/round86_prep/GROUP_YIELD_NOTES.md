# AMGT_RESAPP round-86 PREP -- the fresh-draw yield (row AMGT_RESAPP-D1-W338-S1)

Grounding fork of `2.0.0_SA_COO~R1`, 2026-10-09 ~14:1xZ. READ-ONLY: no model call, no store read beyond the committed offline draft, no
write. **Instrument limit:** the 11 cached pass-1 replies the round-85 jj-1 worker drew were in its worktree's `.scratch`, removed at the
merge; only its offline draft survives (`deliverables/0.9.0_WK_AMGT_RESAPP~338/offline/draft.json`, one draw). Every count below is over
that one draft, not the 11.

## Why a paraphrase-only reply is held

1. **The item text is the model's own prose.** Pass 1 sends the excerpt as a citations document and asks for a prose answer
   (`analyze.py:477-523`). The prompt says *"Where you quote the filing, put the quoted words in quotation marks ... and copy them EXACTLY"*
   (`analyze.py:176-178`) -- quoting is optional; a finding may be pure paraphrase as long as it is cited.
2. **The citation's `cited_text` is the PASSAGE, not a sentence the model wrote.** Content-block citations echo the cited block; the
   resolver only checks `cited_text` lies in the passage to map passage ids (`analyze.py:614-635`, `:681-700`). `cited_text` is never
   carried into the item's `text`.
3. **The drafting gate needs a verbatim run in the item TEXT.** `drafting_build.quoted_spans` (`drafting_build.py:205-220`) takes the
   model's quotation marks, else `longest_verbatim_run` of the text against the excerpt with `MIN_QUOTE_TOKENS = 8` /
   `MIN_QUOTE_CHARS = 12` (`drafting_build.py:~193-200`). A paraphrase ("Total revenue for 2025 was US$15,774.8 million, up ...") shares no
   8-token run with the filing ("Total revenue for the year ended December 31, 2025 was US$15,774.8 million ..."), so `quoted_spans` is
   empty and the sentence is HELD-NO-SPAN (`pipeline.py:50-51`).

**Why earlier runs had spans:** the round-83 ASML run and the stored NU draft drew replies whose CITED block echoed the filing's sentence
right after the paraphrase. Glued with "" (the defect jj-1 fixed), the item text carried an 8-token verbatim run, so it served -- as a
paraphrase-plus-verbatim pair. The yield came from the model's echo, a draw-dependent behaviour, not from the pipeline.

## Measured on the one surviving fresh draw (NU, round 85 jj-1)

- served 22, held 17, refused 1 (of 40 drafted); 0 served glued.
- **Every served sentence is only PARTLY verbatim:** r86_yield Y2 -- the whole sentence text verbatim in a cited passage -- reads 0 of 22.
  Today's gate passes a sentence on one 8-token run, so a served sentence is a paraphrase that contains a run.
- **15 of 17 held items cite a passage that holds the filing's own sentence for the same fact:** 6 by exact figure match (every
  non-year figure of the item appears in one sentence of a cited passage -- measured); 9 narrative items by word overlap of >= 4 long
  words (INFERRED, a heuristic -- each needs reading before it is trusted). Substituted, 37 of 40 would serve (floor 38: one short).

## Repair candidates

| | what it moves | risk |
|---|---|---|
| A. prompt: "state each finding AS the filing's own sentence, quoted" | the model's text; still draw-dependent | the yield stays a model behaviour; a re-run can still come back paraphrase-only |
| **B. drafting serves the filing's sentence**: for an item whose text has no span, select the sentence of its cited passage that carries the item's figures (or, for a narrative item, the cited block's own sentence) and serve THAT as the text, `generated: false`, with the paraphrase kept as a note | `drafting_build` (and the analysis keeps the model text); deterministic given the passages | a narrative item can pick the wrong sentence -- needs a grading rule (figures must all match; narrative needs a stricter test than word overlap) |
| C. both | | |

**Recommended: B, figures-first.** It removes the draw dependence the row is about, makes every served sentence the filing's own text (the
bar the CTO set for NU in round 85: 100% verbatim), and is provable OFFLINE on stored analyses with no model call. Phase it: figure-carrying
items first (measured: 6 of 17 here), narrative items only under a stricter match proved on planted decoys.

## Check

`round86_prep/checks/r86_yield.py --crit AC1 --draft <path> [--floor 38]`: Y1 served >= floor; Y2 every served sentence wholly verbatim
in a cited passage (the pipeline's `verbatim.check_against_sources` on the sentence text); Y3 0 restated / glued (r85_sentences' rules).
Base on the offline NU draft: **NO** -- Y1 22 of 38, Y2 0 of 22, Y3 PASS. ruff py39 clean.

## Not done

The 11 cached replies are gone; a fuller measurement (per-reply `cited_text` vs text) needs a re-draw or the worker's cache, which this
fork does not have and was told not to make.
