# SPEC SECTION -- Provenance (for AMGT-s-5's DESIGN_SPEC.md)

**Owner of the fold-in:** AMGT-s-5 (the design spec). This section is text, describing PAGE
BEHAVIOUR in the design-spec vocabulary; it names no component, no `.tsx`, no portal path
(C-DESIGN-SPEC-FIRST -- no `.tsx` may exist until the spec this section feeds is approved).

## What backs this section

`lib/research/provenance/schema.json` is the data contract every figure on the page must
satisfy before it is eligible to render at all: `source`, `basis.mnemonic`, `basis.definition`,
`vintage`, `unit`, `sign` all present and non-empty. `lib/research/provenance/validate.py`
is how a consumer checks a landed `model_block.json` against that contract before trusting it.
`lib/research/provenance/render_print.py` is the reference implementation of the print-path text
below, run against AMGT-s-1's three landed model blocks
(`provenance_render_SAP_GY_Equity.md`, `provenance_render_BA_US_Equity.md`,
`provenance_render_BABA_US_Equity.md`, this deliverables folder).

## 1. Beside every figure, always

Every number the page ever renders carries, without the reader having to ask:

- the **value** and its **unit**, in the unit the record actually states for THAT figure on
  THAT security (never a page-wide default -- Bloomberg's own units differ across field
  families and, per AMGT-s-1's F4 re-measurement, can differ per security for the same field);
- the **basis** -- the vendor mnemonic and Bloomberg's own definition of it, never a
  paraphrase and never another vendor's normalization reconstructed to look like it;
- the **vintage** -- when this figure was derived, not when the underlying period ended;
- the **source** -- which vendor/instrument answered ("Bloomberg" for everything this project
  lands; the field exists so a later, second source is never silently indistinguishable from
  this one).

**Reference text, exactly as `render_print.py` produces it:**

> `<value> <unit> · <mnemonic> (<definition>) · as of <vintage> · Bloomberg`

## 2. On hover

The full line above is the hover/tooltip content for every figure on the page, verbatim from
`render_print.render_figure_line()` -- never a shortened version and never composed fresh from
a second lookup. A hover that shows less than the print line shows less than an analyst needs
to defend the number; there is no reason for the two to diverge.

## 3. In the printed pack

The same line, printed beside (not instead of) the number itself, exactly as
`render_print.render_model_block()` lays it out per figure: one line per figure, grouped by
header scalars first, then by fiscal year. This is what makes FWD-3's bar reachable -- Adam
defends a number in a meeting by reading the line already on the page, not by opening a
terminal or a spreadsheet.

## 4. When a unit could not be resolved -- MARK, NEVER DEGRADE

`C-MARK-NOT-DEGRADE`: if AMGT-s-1 could not resolve a field's unit for a given security (its
own field map records this per field, per security, as `UNRESOLVED-ON-<security>`), the page
renders the literal marker `[UNRESOLVED UNIT]` in the unit's place -- **never** a blank space,
**never** a silently-dropped row. A blank reads as "nothing to see here"; a dropped row is
invisible entirely; the marker is the only one of the three that tells the reader something is
actually missing and where to look. Measured example (this order's own data): `BA US Equity`'s
`IS_DIV_PER_SHR` (dividend per share) carries this marker on every one of its ten fiscal-year
figures, because AMGT-s-1's field map could not resolve that field's unit for Boeing from the
single sampled value it read (Boeing's dividend was suspended from 2020 onward, and the sampled
year happened to be a zero); `SAP GY Equity` and `BABA US Equity` carry a real resolved unit
(`PER SHARE (local trading/reporting currency)`) for the identical mnemonic. The page must be
able to show BOTH states for the SAME field, on different securities, side by side, without
either one silently vanishing.

## 5. What this section deliberately does not specify

Layout, typography, component boundaries, and any portal-side state management are out of
scope here -- those are AMGT-s-5's to design once this section is folded in. This section
specifies the CONTENT and the FAILURE-MODE BEHAVIOUR (mark, never degrade) the design must
carry, not the pixels.
