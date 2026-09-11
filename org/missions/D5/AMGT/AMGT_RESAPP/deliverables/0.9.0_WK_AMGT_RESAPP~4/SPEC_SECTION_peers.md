# SPEC_SECTION_peers -- the Peer Comparison panel (for AMGT-s-5's DESIGN_SPEC.md)

*Produced by AMGT_RESAPP.TO-AMGT-s-8 (`0.9.0_WK_AMGT_RESAPP~4`), to be folded verbatim
into the Security Analysis page's DESIGN_SPEC.md as its own section, per AMGT-s-5's
worker face ("Fold in the SPEC_SECTION_*.md files the wire cells produced ...
verbatim as sections").*

## FWD-8's bar

"The comparison block is about the company on the page. DONE WHEN EXERCISED -- an
analyst who distrusted it has stopped. ACCEPT: The list of comparable companies is
genuinely about the company being shown. Where a sensible comparison cannot be worked
out, the page says so rather than showing another company's list."

**The measured defect this bar answers:** 48 of 54 one-pager workbooks in the
research corpus carry KPN's unmodified 12-ticker telecom peer set on ASML,
AstraZeneca, BP, Boeing, Costco, Hermes and 42 others (F6, re-measured by this
worker at the time recorded below, matching the CRO's own citation exactly). The
corpus is never a source of truth for this panel.

## What the panel shows

One `peer_set` record per security (`lib/research/peers/engine.py`'s `peers()`), with
exactly three possible `basis` values -- never a bare list with no basis attached
(A VALUE MUST CARRY ITS CLAIM):

- **`basis: "analyst"`** -- a peer set an analyst entered directly. Rendered as an
  ordinary comparison table (ticker, name if resolvable), with a small badge reading
  "analyst-entered" next to the panel header. Not subjected to the engine's own
  comparability test.
- **`basis: "derived"`** -- a peer set the engine computed: same classification field
  (see "The test," below) as the subject, and a market-cap band within 0.2x-5x of the
  subject. Rendered as the comparison table with a badge reading "derived" and, on
  hover/expand, the `test` string verbatim -- the exact rule that put each name on the
  list.
- **`basis: "absent"`** -- **no table is rendered.** In its place, the panel shows the
  `reason` string verbatim, in ordinary body text, e.g.: *"candidate universe not
  classified; a quota decision (F2) precedes derivation -- subject's own
  GICS_SECTOR_NAME='Consumer Discretionary' is known, but no other covered name in the
  corpus has been classified by the same field, so no candidate can be tested for
  membership."* This is FWD-8's bar made literal: the page says so, rather than
  showing another company's list, another company's set, or a blank space that reads
  as "no comparison exists" when the truth is "not yet derivable."

Every record also carries `vintage` (when the engine ran) -- shown in the panel's
small-print line, consistent with every other panel on this page.

## The test, stated for the panel (and for whoever derives it next)

*comparable = same Bloomberg industry classification AND a market-cap band within
0.2x-5x of the subject.*

At this cut the finest classification field AMGT-s-1's landed record carries is
`GICS_SECTOR_NAME` (sector-level) -- a true subgroup-level field (e.g.
`GICS_SUB_INDUSTRY_NAME`) was not mapped for any of the three securities landed so
far. The engine's `test` string names this explicitly rather than silently promising
subgroup-level precision it cannot currently deliver: **a second engineer re-deriving
this panel once a finer classification field is landed reads the current field name
in the string itself, not just a generic word "classification."**

## Why every panel today reads `absent`

A `derived` peer set additionally needs a **candidate universe** -- other covered
names, each classified by the same field, to test for membership. Classifying the
research universe (up to 89 names) is itself a quota decision the brief flags
directly (F2: "the binding constraint is UNIQUE SECURITIES TOUCHED"; "the limit
itself is unmeasured") and this cell does not spend it. So today, for all three
securities AMGT-s-1 has landed (BABA US, BA US, SAP GY), the panel reads `absent`
with the reason naming that quota decision by name -- not a defect in the panel, the
honest state of the estate at this cut.

## C-SHARED-DEFECT: the panel's own guard against the F6 shape

Before any run's peer sets reach the page, `lib/research/peers/shared_defect.py`'s
`check()` runs over the WHOLE BATCH (never one name at a time): it REFUSES if any two
subjects in **different** classifications carry the identical member set (the F6
shape -- KPN's set on a semiconductor company AND a pharma company, verbatim), and
ADMITS the legitimate twin (two subjects of the SAME classification, e.g. two
telecoms, genuinely sharing a set is not a defect). A REFUSE from this pass blocks
that run's panels from publishing at all -- the panel would rather show nothing than
repeat F6.

## The corpus is never a source

Neither `engine.py` nor `shared_defect.py` opens a workbook, a CSC sheet, or any
`*.xlsx`/`*ONE PAGER*` file. F6 itself is re-measured by re-running AMGT-s-12's
`f6_remeasure.py` (this cell's own AC1), never by a code path inside the panel's
engine.

## Identity (C-IDENTITY-RESOLVED)

A member of a `derived` or `analyst` peer set is always named by the identity
layer's key (a Bloomberg ticker string, e.g. `"KPN NA"`, matching
`lib/research/identity/resolver.py`'s `bloomberg_ticker` convention) -- never a bare
company name that could resolve to a different issuer.

## Vintage

Every panel state (including an `absent` reading) carries the `vintage` the engine
stamped when it ran, per the page's general vintage rule.
