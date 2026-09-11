# AMGT-r-12 -- session log

Worker `0.9.0_WK_AMGT_RESAPP~4`, task order `AMGT_RESAPP.TO-AMGT-r-12.identity-coverage-pass.md`,
worktree `wk-amgt-2-4` on branch `wk-AMGT_RESAPP-2-4`, cut by hand from SITEZ @3730474e77.

## Sequence

1. Tree check (`TREE-OK`), status flipped `staged` -> `pending` on the task order file.
2. Read the landed round-1 identity module (`resolver.py`, `build_universe.py`, `self_test.py`) and the
   landed `universe.json` (32 MEASURED / 32 distinct / 57 UNRESOLVED of 89, at
   `deliverables/0.9.0_WK_AMGT_RESAPP~3/universe.json`) and `sa_ids.json` (3 keys: BABA, BA, COST, at
   `deliverables/0.9.0_WK_AMGT_RESAPP~9/sa_ids.json`).
3. Checked source (i) (sa_ids.json) against the current UNRESOLVED set directly: all three sa_ids keys
   are sa_symbol roots already derived from an ALREADY-MEASURED bloomberg_ticker (Alibaba/Boeing/Costco)
   -- there is no key to look an UNRESOLVED entry up by without already knowing its ticker. Confirmed 0
   new resolutions from this source, not assumed.
4. Checked source (iii) directly: the only other device-local artifact keyed by these identity values
   (`coverage_items_BABA_US.json` / `_BA_US.json` / `_COST_US.json`, AMGT-s-4) keys on the same three
   tickers. 0 new resolutions.
5. Re-read every one-pager workbook behind the 16 folders round-1's AC7 pass downgraded (the shared
   `'AAPL US'` template placeholder), across EVERY non-excluded sheet of EVERY one-pager file (not just
   the first 4 sheets / first file build_universe.py's per-folder scan stops at): 14 of the 16 carry no
   second clean source (only the same unfilled `Model` template plus a FactSet-format, non-Bloomberg-
   shaped identifier on the excluded `Model NEW VERSION` sheet, e.g. `CLX-US`, `SAP-DE`). TWO --
   `SAP GY` and `Imperial Brands IMB LN` -- carry a SECOND one-pager file (`... International Dividend
   One Pagers.xlsx`) with a genuine `Overview` sheet the original scan never reached: `Identifier` /
   `Ticker:` reads `SAP GY EQUITY` / `SAP GY` and `IMB LN EQUITY` / `IMB LN` respectively -- real
   workbook cells, not the directory's own name (the directory's name and the workbook's own answer
   happen to agree, which is what a correctly-named research directory looks like; the directory's name
   was never read as a source).
6. Also re-read Rio Tinto RIO LN's workbook (the one UNRESOLVED-with-workbook folder outside the
   shared-placeholder set) across all 3 of its sheets: the `Model` sheet's own ticker cell is a stale
   `HESAY-US` / `#N/A Invalid Security` artifact (rejected by the same hyphen-excluding shape guard that
   protects against exactly this class of defect); `Sheet1`/`CSC` carry no identifier label at all.
   Stays UNRESOLVED, reason named.
7. Wrote `lib/research/identity/coverage_pass.py` (a pass beside `build_universe.py`, per the cell's
   "(or a pass beside it)"): sources (i)/(iii) verified-null as above; source (ii) implemented as the
   full-sheet, full-file re-scan with three refusal rules (a value equal to a known shared placeholder
   is never accepted; two conflicting candidate values for one entry is refused, not guessed between; a
   candidate colliding with any value already MEASURED elsewhere is refused) plus a DEFENSIVE re-run of
   `build_universe.py`'s own whole-population AC7 downgrade pass over the post-resolution entry list
   (0 reintroductions this run). `Model NEW VERSION` stays excluded -- unchanged from round 1.
8. `python -m lib.research.identity.coverage_pass`: `COVERAGE PASS: newly MEASURED 2 (source ii);
   source i confirmed 3 already-MEASURED entr(y/ies), 0 new; source iii found 3 device-local file(s)
   keyed on the same tickers, 0 new; partition {'MEASURED': 34, 'UNRESOLVED': 55} of 89; residual
   UNRESOLVED 55`. Writes the regenerated `universe.json` and the per-folder `RESIDUAL_REPORT.md` (55
   lines, one per still-UNRESOLVED folder, summing to 55).
9. Wrote `DESIGN_QUESTION_identity_fallback.md`: states the directory-name-derived fallback mechanism
   precisely (what it would read, applied concretely to the 14 remaining shared-placeholder folders +
   Rio Tinto), its ceiling (INFERRED, never MEASURED), and its two measured failure modes (a renamed/
   generic directory silently produces a wrong-but-plausible value with no independent check; an
   ambiguous trailing token, live example `Nokia FH`) -- takes no position on whether Andrew should
   authorize it.
10. `python -m lib.research.identity.self_test`: unchanged, still PASS (this pass touches no resolver.py
    behaviour).
11. `bash .tools/commit-gate.sh lib/research/identity/coverage_pass.py`: OK, pre-commit gate clean for
    1 of 1 file.

## What each acceptance criterion reads, verbatim

- AC1: `MEASURED 34 | distinct 34 | shared 0 | partition {'MEASURED': 34, 'UNRESOLVED': 55} of 89`.
- AC2: `UNRESOLVED 55 | every one carries a reason True | newly MEASURED cite a source True`.
- AC3: `folder-name fallback coded in module False | design question written True`.
- AC4: judgment, see `DESIGN_QUESTION_identity_fallback.md` and this log.

## Declared, not chased

- Source (i) and source (iii) both verified to contribute 0 new resolutions -- recorded as findings
  (the code paths that would populate them are asserted empty, not merely absent from the output).
- The 40 no-workbook folders (PDF-only research material, checked directly) and Rio Tinto's stale
  `#N/A Invalid Security` workbook artifact are out of reach for a workbook-cell source; extracting an
  identifier from a PDF would be a new parse step this order does not carry the word for (G-24 in
  spirit: no new capability this order's bound did not name).
- `Model NEW VERSION` stays excluded for every folder, including the two now-resolved ones, which is why
  the coverage pass reads its answers from `Overview`, never from that sheet.
