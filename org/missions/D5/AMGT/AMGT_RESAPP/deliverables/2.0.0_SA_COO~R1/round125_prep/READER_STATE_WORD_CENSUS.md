# AMGT_RESAPP round 125 -- census of every printed line kind that carries a reader state word (the denominator of cell `AMGT-cg-1` and `AMGT-cg-2`)

Issuer: `2.0.0_SA_COO~R1`, 2026-10-19 ~22:3xZ. Ordered by the CTO's round-124 analysis (`ledger/ROUND_ANALYSIS.round124.R1.md`, msg 8560) item 1: *"Census first. Every line kind printing a reader state word, with its writer count, across export, PDF and page. The census is the denominator, and any kind it finds that this list misses joins the cell."* Read-only; every number below was measured at the stated instrument and vintage.

## 1. The surfaces and the instrument

- **Rich export and PDF, live:** `C:/dev/ui-walk-evidence/r124-full-live-after.json` (live `opal-amgt-scoped-api` CodeSha256 `keJ3wDa8..`, after `AMGT-cf-4`; 101 of 101 names read, 0 errors; both formats, full text). A "state word" is any of `ABSENT SERVED READ_FAILED INVALID REFUSED REFUSE HELD PRESENT CONFIRMED NOT_SEARCHED SEARCHED_NOTHING_FOUND SEARCHED_LINKS_UNREADABLE SEARCH_FAILED NOT_WRITTEN UNREADABLE_OBJECT NOT_PASSED PASSED STALE UNMEASURED MACHINE-EMPTY PENDING` as a whole word; a second, generic scan (any `UPPER_SNAKE` token or `ABSENT/SERVED/INVALID/REFUSED/READ_FAILED/PRESENT/HELD/UNMAPPED/EMPTY/STALE/PENDING` outside table rows) found 23 distinct tokens in the export and **0 in the PDF**.
- **Code:** `lib/research/print/render_pack.py` at HEAD `3573dd735b` (the file served by `rel-amgt-cf4`), the writers read by the native Grep tool for `ABSENT|REFUSED` (48 lines), each classified as a WRITER (prints), a LOGIC line (compares) or a COMMENT.
- **Page:** `portal/src/pages/SecurityAnalysis/**/*.tsx` at the portal repository's `DEV` `a48fa073c2`: the native Grep tool for `ABSENT|REFUSED` (74 hits in 18 files) and for visible interpolations of a raw status (`${...status...}`, `(read `). A hit is VISIBLE only when it is JSX text or a template that reaches the reader; `data-*` attributes, comments and comparisons are not visible.

## 2. The PDF: 0 kinds

The PDF pack (`build_pack`, `_print_*`) prints no state word: live 0 lines on 101 names; in the code the `ABSENT` literals at lines 590, 847, 1120-1122, 1221, 1231, 1454 are a comment, a plain sentence constant (`POSITIONING_ABSENT_SENTENCE`, no state word in its text), a comparison and a comment. **PDF writers: 0.** (The `*_markdown` builders are called only from `build_rich_text`; the `rel-amgt-cf4` census read the PDF byte-identical.)

## 3. The rich export: 8 kinds, 11 writers, 317 live lines on 101 names

`cf-2` (merged `6f65da85da`, live since 20:54Z) already moved the Peers absent-column lines and the chart line. What is left (live lines counted at the vintage above):

| # | kind (the printed line) | live lines (names) | writers in `render_pack.py` (line, function) | what the page shows for the same state (visible text) |
|---|---|---|---|---|
| K1 | `Posture: ABSENT -- <reason>` and `Posture: ABSENT -- <reason>. Nothing is rendered in its place.` | 134 (67) | 2027 and 2029 (`_posture_markdown`) | `No call on this name yet` plus one plain reason (`PostureTab.tsx:96` `NO_CALL_WORDS`, `LeadPanel.tsx:265`) |
| K2 | `ABSENT -- no call was made: <reason>` (and with the machine disclaimer) | 50 (25) | 2037 and 2041 (`_posture_markdown`) | the same designed empty state (`No call on this name yet`) |
| K3 | `y/y growth rows: ABSENT -- the block carries none and this page computes none.` | 101 (101) | 2130 (`_model_sheet_notes_markdown`) | no visible state word: a `data-model-absence` attribute only (`ModelTab.tsx:965`); the harness `exportCompare` reads it |
| K4 | `<years>E: ABSENT -- the block carries fiscal years <a> to <b> only.` | 2 (2) | 2140 (`_model_sheet_notes_markdown`) | `<years>: no consensus estimates are served for this name; the model block carries fiscal years <a> to <b>.` (`ModelTab.tsx:950-951`) |
| K5 | `Description: ABSENT -- <reason>` | 1 (1) | 1703 (`_drafted_section_markdown`) and 1800 (`_header_description_lines`): 2 writers | `PanelEmpty` designed state (`ThesisTab.tsx` CompanyDescriptionNotServed) |
| K6 | `Exec Management: ABSENT (<words>).` | 2 (2) | 1887 (`_management_markdown`) | `PanelEmpty` designed state (`ExecManagementTab.tsx`) |
| K7 | `<Name> case: <STATE> -- <detail>` (every state incl. `SERVED`) | 0 live (no print path: `bv2_quote_blocks.json` `functions_on_no_print_path`) | 2075 and 2096 (`_model_case_line`, called by `_model_cases_markdown` L2100, not called by `build_rich_text`) | plain `The research team has no <side> case for this name yet...` (`ModelTab.tsx:457`) |
| K8 | `<MNEMONIC>: REFUSED -- <reason>` | 27 (16) | 2173 (`_refused_figures_markdown`) and 2430 (`build_rich_text`, the Model Notes line): 2 writers | one status icon and ONE navy sentence, the reason alone, no state word (`ModelTab.tsx:351-371`) |
| (done) | Peers absent-column lines; the chart line | 1128 (94); 9 (9) | 1971-1975; 2190 | closed by `cf-2`/`cf-4` |
| (also) | `ABSENT -- no peer set supplied to this export` | 0 live | 1928 (`_peers_markdown`, `if not peer_set`) | `No peer set for this name yet.` (`PeersTab.tsx:399`) |

Totals: live ABSENT lines **290** = K1 134 + K2 50 + K3 101 + K4 2 + K5 1 + K6 2 (134 + 50 + 101 + 2 + 1 + 2 = 290); live REFUSED lines **27** = K8; together 317. The generic scan's other tokens are the `UPPER_SNAKE` mnemonics that LABEL the K8 lines (a field code as the line's label, kept: the export's own R5 rule admits a mnemonic as its own line label) and the `> cites:` provenance lines (`<key>/F:<MNEMONIC>:<year>`, a citation not a state word, outside this census).

## 4. The page: visible raw state words, 5 sites in 4 files

| # | site | what it prints | note |
|---|---|---|---|
| P1 | `PeersTab.tsx:406` | ` (read ${data.peer_read.status})` after the Peers reason when `basis` is `absent` and the read is not the `ABSENT` empty state: e.g. `(read READ_FAILED)` | the export prints the same suffix in plain words via `_read_status_words` (`READ_FAILED` to `failed`, `SERVED` to `served`, `ABSENT` to `absent`, `render_pack.py:1616`) and the harness `peersReadFailed.harness.cjs` pins the page word; the file's own comment (L20) says the distinction "is load-bearing and stays verbatim" |
| P2 | `PrintExportAction.tsx:135` and `:165` | `[REFUSED: <error>]` for a failed export and a failed print | a state word in a reader-facing error. The same bracket convention lives in `refusalPresentation.ts:15,42` (a helper; its consumers are `join.harness.mjs` and `exportCompare.harness.cjs`; `ModelTab` prints the reason alone): the consumer census of that helper is step A of `cg-2`, and any page site it finds that prints the token joins the cell |
| P3 | `GenerationCaption.tsx:38` and `:45` | `generation: none -- <status>` and `read <status>` (a raw ranking/point status) | the staff-facing system-fact caption of a ranking; SAUX-26 keeps system facts out of the resting page. **Not changed in this round; put to the CTO** |
| P4 | `InputProvenance.tsx:81` | ` -- <status>` after an input's name | the same system-fact class. **Not changed in this round; put to the CTO** |
| P5 | `postureCites.ts:343` and `:372` | `<management block> is <status lowercased>` inside a sentence | lowercase, inside a plain sentence; not an uppercase token. **Not changed** |

Page `data-*` attributes, comments and state comparisons that carry `ABSENT`/`SERVED` (the other ~60 of the 74 hits) are not visible text and are out of this census. The parity instrument `portal/src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs` reads the export's `ABSENT -- <reason>` words for K3, K4 and K7 (23 `ABSENT` literals in the file): it moves with the export, in the portal cell.

## 5. What this fixes for the two cells

- **`AMGT-cg-1` (workspace repo, `render_pack.py`):** K1 to K8 and the no-peer-set line: 11 writers (+ 1). The target words, one rule: the state word becomes `Not available` (the fixed words `cf-2` set, constant `NOT_AVAILABLE_WORDS`), the reason or tail unchanged; K8 becomes `<MNEMONIC>: Not available -- <reason>` (the reason already says the check did not pass and no value is shown; the label stays); K7 prints `<Name> case: Not available -- <reason>` for an absent case and `<Name> case: <detail>` (no state word) for a served one. A present value prints unchanged.
- **`AMGT-cg-2` (portal repo, `src/pages/SecurityAnalysis/`):** P1 (`(read failed)`/`(read served)`/`(read absent)`, the export's own words) and P2 (`The document could not be made: <error>`), plus `exportCompare.harness.cjs` and `peersReadFailed.harness.cjs` moved to the new words. P3 and P4 are listed for the CTO, not changed.
