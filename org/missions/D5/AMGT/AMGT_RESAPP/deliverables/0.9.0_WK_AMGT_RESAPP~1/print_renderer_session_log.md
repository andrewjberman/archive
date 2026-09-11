# AMGT_RESAPP.TO-AMGT-s-5 -- THE PRINT RENDERER: session record

**Worker:** `0.9.0_WK_AMGT_RESAPP~1` | **Cell:** AMGT-s-5 | **Outcome:** FWD-5 | **Manifest row:** S5

## What was built

- `DESIGN_SPEC.md` (deliverables folder) -- 15 surface sections (S1-S15), the header panel's
  Bloomberg session-state indicator, an empty approval block. Follows the F10 precedent's own
  section grammar (owner/status/date header, numbered sections, an acceptance/approval gate at
  the end). Folds in verbatim the eight `SPEC_SECTION_*.md` files the wire cells produced
  (provenance, coverage, drafting, peers, social, freshness, ledger, check-face, lists); writes
  S1, S2, S5, S6, S11, S12 itself from the decomposition/PRD's own manifest text where no
  `SPEC_SECTION` file exists (S2 in particular is explicitly stated as design-only: no
  `AMGT-s-2` artifact has landed, so this section states the REQUIRED BEHAVIOUR from the PRD's
  own row rather than inventing a schema).
- `lib/research/print/render_pack.py` -- Adam's artifact. Renders one security's landed
  `model_block_<security_key>.json` into a PDF reproducing the template's four blocks in order
  (model block / RECOMMENDATION + COMPANY DESCRIPTION / THESIS | RISKS / bio), each undrafted
  section marked `[MACHINE-EMPTY: ...]`. Library choice, stated per the bound: `matplotlib`
  (`PdfPages`) for page generation and `pypdf` for text extraction -- both already importable
  under `python`; `reportlab`/`fpdf`/`weasyprint`/`python-docx` are NOT installed (measured,
  all four `ModuleNotFoundError`), so this is a real constraint the render works around, not an
  arbitrary preference.
- `pack_SAP_GY_Equity.pdf` / `pack_SAP_GY_Equity.txt` -- the rendered pack and its extracted
  text, for SAP GY Equity (the control security AMGT-s-1/-s-3 also used).

## The template, read read-only

`lib/research/print/render_pack.py`'s `read_template_block_headers()` opens the blank `.docx`
template as a zip (stdlib `zipfile` + `xml.etree.ElementTree` -- `python-docx` is not installed)
and confirms F1's own citation exactly: 11 paragraphs, 3 tables, 1 image. The template is never
written to; this function only reads. The exact wording recovered: title
`"[COMPANY NAME] [TICKER] Research Note"`, `"[PASTE EXCEL OUTPUT]"`, Table 1
`RECOMMENDATION` / `COMPANY DESCRIPTION:`, Table 2 `INVESTMENT THESIS:` /
`RISKS AND CONSDIERATIONS:` (F1's shared misspelling, confirmed present verbatim in the template
itself), Table 3 (bio), and `"Management/Board 80"` -- the four blocks this render reproduces.

## A real filled pack, read for comparison (read-only)

`Asset Management/Research/SAP GY/SAP Research Pack 2026 06 12_v1.pdf` -- Adam's own filled
pack for the same control security -- was read (via `pypdf`, no write) for AC6's comparison
below: 12 pages, a dense header/financial-summary page 1, then multi-page prose (company
description, positives/negatives, a CEO bio with named claims, a custom "IMPACT OF ARTIFICIAL
INTELLIGENCE" section beyond the four floor blocks, and a peer comparison table).

## AC6 (judgment) -- answered here, graded at L9

**Would Adam forward this one unreformatted, or does it read as a screenshot of a dashboard?**

Neither, exactly -- and the honest answer is the third thing this order names: it reads as the
**skeleton** the task order's own bound calls out by name ("a render that fills the four blocks
and calls the pack done has reproduced the skeleton"). Concretely, beside SAP's real filled
pack:

- **What matches:** the document shape. `pack_SAP_GY_Equity.pdf` is a 9-page, letter-sized,
  text-flowing PDF with the SAME section labels in the SAME order the real pack uses
  (`RECOMMENDATION:`, `COMPANY DESCRIPTION:`, `INVESTMENT THESIS:`,
  `RISKS AND CONSIDERATIONS:`, `Management/Board`), each starting its own page -- it is a
  DOCUMENT, not a UI capture; nothing about it reads as "a screenshot of a dashboard" (no chrome,
  no browser furniture, no interactive controls rendered as static pixels).
- **What does not match, and should not be hidden:** the real pack's pages 2-9 carry Adam's own
  ~9,000 characters of prose -- a company description, a bull/bear case, a named CEO with sourced
  biographical claims, a custom AI-impact section, a peer table. This render's equivalent pages
  carry five `[MACHINE-EMPTY: ...]` markers and nothing else, because no engine in this project
  has drafted that content yet (`SPEC_SECTION_drafting.md`'s own admission: these sections render
  empty for every security today). **Adam would not forward this one as-is** -- not because it
  looks broken or machine-generated in a way that embarrasses the firm, but because it is
  honestly, visibly INCOMPLETE, and an incomplete pack is not what FWD-5's EXERCISED bar ("Adam
  has actually forwarded one") asks for. That gap is this project's remaining work (the drafting
  face, S9), not a defect in this render -- the render's job was to reproduce the skeleton
  faithfully and mark what it could not fill, which is exactly what C-MARK-NOT-DEGRADE asks for
  and exactly what "the template is a floor, not the pack" (this cell's own bound) predicts.
- **What IS forwardable today, and matches the real pack closely:** page 1's model block. Every
  header scalar and fiscal-year line item AMGT-s-1 landed for SAP renders with its full
  provenance line (value, unit, mnemonic, Bloomberg's own definition, vintage, source) --
  MORE provenance detail per figure than the real pack's own page 1 shows (the real pack's
  financial-summary table carries bare numbers with no per-cell basis/vintage at all). On the
  narrow question of "can Adam defend a specific number from this page in a meeting," this
  render's page 1 is already stronger than the circulated document it would replace.

**Does the spec say, for every surface, what the page shows when that surface is NOT there?**
Yes -- every one of `DESIGN_SPEC.md`'s 15 surface sections states an UNRESOLVED/FAILED/HELD BACK
(or, where the surface has no direct page representation, an honest absence-with-reason)
behaviour, never a silent gap:
- S1: a field the map could not resolve renders the check-face REFUSE state, `[REFUSED: ...]`.
- S2: the whole on-demand-pull affordance is disabled with a stated reason until its own design
  is built and approved.
- S4: three source classes, each with its own honest empty/absent state named plainly (fixtures
  only for `publication`; zero `ir` items; "no Seeking Alpha content landed yet" for `sa`).
- S6/S11/S12: stated absences-with-reason -- these are backend engines with no direct tab, and
  the section says so rather than inventing a tab.
- S7: `"NEVER"` renders in the date column exactly where a date would go, never a blank.
- S8: `basis: "absent"` renders the `reason` string verbatim, no table at all.
- S9: an empty `sentences` array renders as a visible, fillable placeholder limb.
- S13: the entire panel's held-back state has its own literal copy, quoted in the section.
- S14: three explicit states (NOT WIRED / WIRED-NEVER-RUN / WIRED-HAS-RUN), never collapsed to
  two.
- S15: the owner field's literal UNASSIGNED string is named, never blank.

This is not incidental -- it is the SAME discipline (C-MARK-NOT-DEGRADE) both of this cell's own
deliverables apply: the design spec states it in prose per surface, and `render_pack.py` applies
it in the rendered PDF for the one artifact this cell actually builds.
