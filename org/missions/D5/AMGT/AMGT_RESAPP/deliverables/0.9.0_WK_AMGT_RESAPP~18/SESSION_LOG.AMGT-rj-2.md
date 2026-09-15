# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~18, AMGT_RESAPP.TO-AMGT-rj-2

DRAFTED SENTENCES BESIDE THEIR EVIDENCE. Worktree `C:/tmp/wk-amgt-11-1`, superproject
branch `wk-amgt_resapp-11-1` (tip at spawn `8940b7320c`), portal worktree on
`wk-amgt_resapp-11-1-portal` (tip at spawn `ad275969`). 2026-09-15, ~11:5xZ to ~12:3xZ.
This is the SECOND order on this worktree; `AMGT-rj-1` is complete and drained, and a
first attempt at this order was terminated by an API limit before any edit.

## 1. The bar, then the premises

`git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-11-1`; `org/` and `.tools/` present.
TREE-OK, no BLOCKING row. `git status` matched the identity line exactly: no diff under
`lib/` or `portal/src/`, the `M portal` line the expected checkout offset, the gitlink at
`e85f6eb8`.

Every premise the order states was re-grounded against live state before any edit:

- **The seam is where the order says it is, at a moved line.** The cell names
  `scoped_amgt.py:680` for the hardcoded `"drafted_sections": []`; at `8940b7320c` it is
  at `:877` (rj-1 added the route boundary above it). Same statement, same function, one
  occurrence in the file -- so the splice anchored on the BYTES, not the line number, and
  asserted its anchor count was exactly 1 before editing.
- **INTERFACE D-1 is landed and readable.** All five objects fetched from
  `s3://opal-data-harvest/drafting/v1/`: 109540 / 88475 / 84313 / 99745 / 102534 bytes.
  BA's bytes hash to `684197b8861424f9...`, the digest `0.9.0_WK_AMGT_RESAPP~20` recorded
  for the object it served -- so the object read IS the object served, not a same-named
  successor.
- **The library's validator is callable and public.** `pipeline.records_by_id`,
  `pipeline.validate_evidence`, `pipeline.passage_texts_for` and
  `verbatim.check_against_sources` are all module-level; only `_gate_sentences` is private,
  and it is a composition of the four. Nothing under `lib/research/drafting/` needed to
  change, and nothing did (AC5: drafting-diff-lines 0).
- **The component is where the order says it is**, and its `title={sentence.evidence}`
  carrier was still present at portal `ad275969`.
- **ONE PREMISE FAILED** and is row `AMGT_RESAPP-Z-W18-S8`: the cell's D-1 description and
  the decomposition's D-1 interface row both name `held_uncited`, and 0 of 5 landed objects
  carry the key. It is F-1's field. See section 4.

## 2. What was built

**THE ROUTE** (`lib/research/api/scoped_amgt.py`, READ 5). `read_drafted_sections()` reads
`drafting/v1/<key>.json` from the pool (boto3, us-east-1, bucket from
`crosswalk.POOL_BUCKET` rather than a second literal), or from a directory when
`AMGT_DRAFTING_ROOT` is set -- read at CALL time, so a test setting it needs no module
reload. THREE validations, all three the drafting library's:

1. the marking contract (`lib/research/drafting/schema.json`, located from this module's
   own path, applied with jsonschema);
2. `pipeline.validate_evidence` per sentence -- EXISTENCE, ASSOCIATION and SOURCE VERSION,
   with the document's own accession and `document_sha256` as the source the ids must
   belong to; an empty evidence list refuses before any of them;
3. the verbatim gate RE-RUN against the passage, and its outcome compared with the
   `verbatim_check` the object shipped. A stored PASS the gate does not reproduce is a
   REFUSAL, not a warning -- "never trust a producer's self-report" applies to an artifact
   this route did not write.

Then the ids are RESOLVED to `{id, passage, source}` once, here, where the validator
already has the records indexed. That is the whole repair: the component that fell back to
a tooltip is the one that was handed ids and asked to quote a filing.

Status domain: `SERVED` / `ABSENT` / `INVALID` over one question (did a validated drafted
document reach this response), with `drafting_source` `pool` / `local` / `none` beside it,
and `drafting_read_completed` false when the surface was unreadable -- an unreadable pool
is not an undrafted name, and the three-value domain has no fourth slot for it.

**THE PAGE** (`portal/src/pages/SecurityAnalysis/tabs/ThesisTab.tsx`, `types.ts`).
`DraftedSentence.evidence` was `evidence?: string`; it is now `DraftedEvidence[]`. Each
drafted sentence renders its `machine` marker inline, its `verbatim_check` as the estate's
own `CheckFaceBadge`, and then -- before the next sentence -- every cited PASSAGE quoted as
text in a `<blockquote>` with its id, accession and location. No `title=` evidence carrier
survives in the file. The held-uncited count is a LINE, never a quotation.

**THE RENDER CHECK** (`__harness__/drafting.harness.cjs`). The actual component, the actual
`react-dom/server`, over a fixture that is the verbatim return of
`read_thesis_bundle('BA_US_Equity')` against the pool object. The walk is anchored on
`data-drafted-sentence` indices rather than on the sentence text, because a drafted
sentence is frequently a substring of a passage printed above it and a naive `indexOf`
would come out true for the wrong reason; the marker count is checked against the bundle's
own sentence count FIRST, so a walk that found nothing could not make the rest vacuously
true.

## 3. The controls

- **The mutant is the shipped component, not a synthetic mutation.** Pre-edit
  `ThesisTab.tsx` (portal `ad275969`, extracted with `git -C portal show`) rendered against
  the SAME fixture with the SAME checks: 0 sentence markers, 0 of 48 passages in the HTML,
  `title="Evidence: [object Object]"` present, no held-uncited line. Against 38 of 38 and
  48 of 48 on the committed component. Run off-repo in `.scratch/`; no committed file was
  mutated at any point.
- **The route's negative arms have a positive control beside them.** AC2's `goodroot` is
  the pool's own bytes read back through the local-root path, so `badroot`/`badroot2`
  INVALID cannot be the read path failing.
- **Determinism.** AC1 twice, byte-identical. AC4's deciding block twice, byte-identical.
- **Type check.** `tsc --noEmit` rc=0, zero output -- `vite build` does not typecheck, and
  the type of `evidence` is exactly what changed.

## 4. Surprises

- **`AMGT_RESAPP-Z-W18-S8`** (OBSERVATION / INERT). INTERFACE D-1 carries no
  `held_uncited` field: 0 of 5 landed objects, and the marking contract does not declare
  it either. It is produced on F-1 (`lib/research/filings/analyze.py:610 @8940b7320c`) and
  tabulated there by rj-6 (SAP 6 held, the other four 0). So `held_uncited_count` is served
  as 0 for all five names, beside `held_uncited_basis: ABSENT_ON_OBJECT` -- zero BY
  ABSENCE, which for SAP is genuinely not the same number as the measurement. Both clean
  remedies live in files this cell is bounded off.
- **`AMGT_RESAPP-Z-W18-S9`** (OBSERVATION / INERT). AMGT-rj-1's identifier-conversion
  guard scans the whole module text for `replace("_", " ")` and refused a SECTION LABEL
  with a message asserting the line "converts an identifier form". The guard is right to be
  over-broad for an identifier contract; the message is what will cost the next reader. Not
  changed -- it is rj-1's contract surface. This cell's `_section_label` moved to
  split/join instead, and the suite went 83 passed / 1 failed -> 84 passed / 0 failed.

## 5. Criteria, as measured

| AC | deciding output | denominator |
|---|---|---|
| AC1 | `drafting_status SERVED drafting_source pool sections 5 sentences 38 with-passages 38 generated-true 38 verbatim-PASS 38 held_uncited_count 0` | 38 of 38 on all three per-sentence arms; 48 evidence records |
| AC2 | `ABSENT 0` / `goodroot SERVED 5` / `badroot INVALID 0` / `badroot2 INVALID 0` | 4 of 4 arms, one object, one field apart |
| AC3 | `title-evidence-carrier 0 title-Evidence-any 0 passage-render 5 source-label 8 blockquote-or-list 2 machine-marker 2 held-uncited-line 4` | 7 of 7 token bars; both zero-bars meaningful (pre-edit: 1 and 1) |
| AC4 | `sentences_checked 38 of 38` + 7 CHECK lines true + `CHECKS-OK 7 of 7` | 38 of 38, equal to AC1's count; node's own rc measured unpiped = 0 |
| AC5 | `84 passed` + `drafting-diff-lines: 0` | 84 collected (60 pre-existing + 24 new), 0 failed, 0 errors |
| AC6 | `rc=0 / js-assets 55 / TOKEN machine 3 / TOKEN control 0 / ffeb4840 / gitlink: t e85f6eb8` | 55 assets; control token in 0 of 55; gitlink unchanged |

`python .tools/proof-of-spec-check.py <instance> AC1,AC2,AC3,AC4,AC5,AC6` -> `VALID (rc=0)`,
violations=0, invocation-alignment 6/6, surprises 2/2 resolving to channel rows.

## 6. What was NOT done

No byte under `lib/research/drafting/` or `lib/research/filings/`. No model call, no vendor
call, no install. Nothing promoted, nothing pushed, no merge, no rebase. The portal gitlink
was not moved and no commit of this cell stages a `portal` path. rj-1's guard was not
re-worded and no other cell's test was touched.

## 7. Commits (LOCAL)

- superproject `6cf202d134` on `wk-amgt_resapp-11-1` -- the adapter, the 24 tests, the two
  channel rows.
- portal `ffeb4840` on `wk-amgt_resapp-11-1-portal` -- the component, the types, the render
  check and its captured fixture.
- superproject (this commit) -- the proof-of-spec instance, the ASCII build log, this log,
  and the order's `<status>` flip to `complete`.
