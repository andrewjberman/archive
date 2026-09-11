# AMGT_RESAPP.TO-AMGT-s-3 -- THE PROVENANCE FACE: session record

**Worker:** `0.9.0_WK_AMGT_RESAPP~1` | **Cell:** AMGT-s-3 | **Outcome:** FWD-3 | **Manifest row:** S3

## What was built

- `lib/research/provenance/schema.json` -- the JSON Schema (a): required
  `source, basis.mnemonic, basis.definition, vintage, unit, sign`; `unit_status`/`sign_status`
  constrained to the closed set `INFERRED|MEASURED|UNRESOLVED` when present.
- `lib/research/provenance/validate.py` -- validates a landed `model_block.json` against the
  schema; DERIVES `unit_status`/`sign_status` at read time (a persisted figure carries its
  already-resolved unit/sign string, or AMGT-s-1's stated `SEE field_map.json ...` placeholder
  when unresolved -- there is no literal `unit_status` key on a figure, by AMGT-s-1's own design,
  which this cell's text itself says: "AC5 proved every figure has the six fields", i.e. value,
  unit, sign, basis, vintage, source -- not eight).
- `lib/research/provenance/render_print.py` -- the print-path fragment: one line per figure,
  `"<value> <unit> · <mnemonic> (<definition>) · as of <vintage> · Bloomberg"`, with
  `[UNRESOLVED UNIT]` in place of the unit wherever it is not resolved (C-MARK-NOT-DEGRADE) --
  never a blank, never a dropped figure. Rendered all three of AMGT-s-1's landed model blocks
  (the cell asked for one; rendering all three cost nothing further -- no vendor call, pure
  local computation over already-persisted bytes -- and gave AC6 a real cross-security example).
- `SPEC_SECTION_provenance.md` -- the design-spec section, text only, for AMGT-s-5.

## No second read

Neither `validate.py` nor `render_print.py` imports the estate's Bloomberg client or opens a
session to the local terminal -- both read only the `model_block.json` bytes AMGT-s-1 already
landed. AC4's negative grep verified this directly.

**A self-caught authoring bug, not a spec-vs-world mismatch, so not filed as a surprise row:**
the first draft of both modules' own docstrings, explaining in prose that they make no second
vendor read, used the literal words the grep itself forbids ("no DAPI call, no blpapi import")
-- a case of a negative-mention sentence tripping the same pattern it was written to disclaim,
the same shape flagged by this project's own doctrine (a criterion cannot tell "we use this" from
"we say we don't use this"). Caught by running AC4's exact invocation before finalizing (per this
worker's standing practice of exercising a criterion against the world, never assuming a drafted
check passes), reworded without the forbidden tokens, re-verified at 0.

## AC6 (judgment) -- answered here, graded at L9

**The figure: `IS_DIV_PER_SHR` (dividend per share), same mnemonic, three securities, one
fiscal year (2016) shown for concreteness -- the same pattern holds across all ten years.**

- `SAP GY Equity`: `1.25 PER SHARE (local trading/reporting currency) · IS_DIV_PER_SHR
  (Dividend per share.) · as of 2026-09-10T23:20:18Z · Bloomberg`
- `BA US Equity`: `4.69 [UNRESOLVED UNIT] · IS_DIV_PER_SHR (Dividend per share.) · as of
  2026-09-10T23:20:18Z · Bloomberg`
- `BABA US Equity`: (resolved, `PER SHARE (local trading/reporting currency)`, same shape as SAP)

**Why BA differs:** AMGT-s-1's field map samples ONE representative value per security per
mnemonic (the most recent fiscal year) to classify the field's unit. Boeing suspended its
dividend in 2020, so every fiscal year from 2020 onward carries `0.0` for this mnemonic; the
sampler's most-recent-year pick landed on a zero, which cannot discriminate a per-share scale
from any other, so the field classified `UNRESOLVED-ON-BA US Equity` -- and because the
classification is per-security (not per-fiscal-year), that status applies to ALL ten of Boeing's
`IS_DIV_PER_SHR` figures, including the pre-2020 years (1.25, 1.40, 1.50 ... real dividends that
WERE paid and could, in principle, have been classified had the sampler picked one of those
years instead). This is a real, disclosed limitation of AMGT-s-1's per-security (not
per-fiscal-year) sampling, inherited here rather than re-derived (bound: never composed from a
second read) -- this cell's job is to MARK it faithfully, which it does.

**Does the line answer "where from, what basis, as of when" without a spreadsheet?** For SAP and
BABA: yes, completely -- value, unit, mnemonic, Bloomberg's own definition, and a vintage
timestamp, all on one line. For BA: the line still answers "where from" (`IS_DIV_PER_SHR`,
Bloomberg) and "as of when" (the vintage), and it visibly FLAGS that "what basis" (the unit) is
not yet established for this specific security -- which is the honest answer, not a wrong one.
An analyst reading `[UNRESOLVED UNIT]` beside `4.69` cannot quote a per-share figure with
confidence, and the marker tells them that directly rather than letting them assume `4.69` means
dollars per share. That is what C-MARK-NOT-DEGRADE is for: the line never claims more precision
than the record actually has.

**Is the per-security difference recorded, not smoothed?** Yes -- `render_print.py` renders
each security's figures independently from that security's own persisted `unit` value; nothing
here imposes one shared convention across securities, and the marker is the visible artifact of
that difference rather than a suppressed one.
