# SPEC SECTION -- the check face (for AMGT-s-5)

**Author:** `0.9.0_WK_AMGT_RESAPP~3` | **Cell:** AMGT-r-10 (round 2, FWD-10; supersedes the
marker portion of `0.9.0_WK_AMGT_RESAPP~8`'s AMGT-s-10 section of the same name, whose s.4
explicitly deferred the marker choice to this cell -- read that section for the data face and
count-preservation contract, unchanged) | **Status:** data face + print-path render + MARKER
WIRED; NO PAGE YET (C-DESIGN-SPEC-FIRST -- this is the section AMGT-s-5 folds into the approved
spec before any `.tsx` is written).

## 0. WHY THIS SECTION EXISTS (FWD-10)

AMGT-s-10's original section named the three states correctly but left the PROVISIONAL marker
as `[PROVISIONAL]` bracket text ALONE. The L9 judgment on that section's own AC6 FAILED it:
`'12345 [PROVISIONAL]'` skims, on a fast read, as "a number, fine" -- the held-back verdict
lived in the DATA (`check_face.json`'s `verdict` field) and was too easy to miss in the READING
(the rendered text). This section names the fix: a distinct, machine-readable MARKER per
verdict, landed in the data face BEFORE any PROVISIONAL figure is served on a page.

## 1. THE THREE STATES, AT A GLANCE -- NOW WITH THEIR MARKER

Every figure on the page carries exactly one of three verdicts. None of them is a blank, a
zero, or a row that is simply absent -- absence is not a state this system produces. Each
verdict now also carries a `marker`: `{colour_token, icon}`, a machine-readable pair the `.tsx`
BINDS (a CSS class, an icon component) rather than a string it has to parse out of prose.

| Verdict | colour_token | icon | What Adam sees in place of / beside the value | Meaning |
|---|---|---|---|---|
| **PASS** | `green` | `OK` | the value, plain -- no marker text on the print path | unit and sign are MEASURED; the figure is defensible as printed |
| **REFUSE** | `red` | `BLOCKED` | `[REFUSED: <reason>] [BLOCKED]` **replacing** the value | the figure's unit or sign was never established -- the value is never shown as if trusted, even though it is still recorded (see s.3) |
| **PROVISIONAL** | `amber` | `WARN` | the value **with** `[PROVISIONAL] [WARN]` beside it | the unit/sign ARE measured but a live caveat (e.g. a cross-check that does not reconcile) has not been resolved -- "we do not know for certain" is shown, never silently folded into PASS |

**THE SET IS CLOSED AND DISTINCT PER VERDICT** -- `(colour_token, icon)` is a different pair for
each of the three verdicts (`lib/research/checkface/markers.py`'s `MARKERS`, checked against
`lib.research.rules.VERDICTS` and for pairwise collision AT IMPORT TIME, so a future edit that
collides two verdicts onto one marker fails loud rather than shipping quietly). A scheme where
PROVISIONAL and PASS share a marker is the round-1 defect unfixed, not a valid instance of this
section.

**At a glance, on the page (`.tsx` guidance, not yet built):**
- A **REFUSE** figure's cell should look **BROKEN** -- bracketed, no number visible where a
  number is expected, in the `red`/`BLOCKED` treatment. That is deliberate; FWD-10's bar is
  that a failed check is VISIBLE as failed, not merely logged.
- A **PROVISIONAL** figure's cell should look **NORMAL but flagged** -- the number is there (the
  analyst is not blocked from seeing it), and the flag is the `amber`/`WARN` treatment: a
  DIFFERENT colour AND a DIFFERENT icon from REFUSE's `red`/`BLOCKED`, so the two never read the
  same at a glance, and different again from PASS's absence of any flag at all.
- A **PASS** figure's cell carries NO marker on the print path and (informatively, in the
  `.tsx`) MAY carry the `green`/`OK` marker for symmetry -- but the print-path render
  deliberately leaves PASS unmarked, on the reasoning that a marker on every row habituates the
  eye exactly the way BABA_US_Equity's 103-of-196 PROVISIONAL rows (s.2 below) already risk
  doing; PASS's silence is itself part of what makes a REFUSE/PROVISIONAL row register as a
  genuine departure on a fast scan.

## 2. WHAT PRODUCES EACH STATE (measured, on the three real blocks AMGT-s-1 landed)

| Block | figures | PASS | REFUSE | PROVISIONAL |
|---|---|---|---|---|
| SAP GY Equity | 203 | 203 | 0 | 0 |
| BA US Equity | 179 | 169 | 10 | 0 |
| BABA US Equity | 196 | 93 | 0 | 103 |

- **BA US Equity's 10 REFUSE** are all `IS_DIV_PER_SHR` (dividend per share), fiscal years
  2016-2025 -- the figure's own `unit` field reads *"SEE field_map.json (per-field,
  per-security MEASURED unit -- not yet built)"*. The per-security unit map F4 warned about
  (absolute vs millions vs percent, one sign inverted) does not yet cover this security/field
  pair, so the figure rule correctly refuses rather than guessing. Each now renders with the
  `BLOCKED` marker appended, per s.1.
- **BABA US Equity's 103 PROVISIONAL** all carry a `currency_caveat`: a real, measured
  reconciliation gap (the fiscal-year-2025 merged-row naive P/E disagrees with Bloomberg's own
  `PE_RATIO` by a factor consistent with several uneliminated causes -- currency basis,
  fiscal/calendar row-split, or ADR ratio). The unit and basis ARE known; what is NOT known is
  whether the printed value is on the basis Adam expects, so it renders flagged (`WARN`) rather
  than plain. **Declared, not resolved (carried from AMGT-s-10's own AC6 finding):** 103 of 196
  rows (53%) carrying the same tag on one security is a lot of ink, and a reader scanning
  quickly across that many tagged rows may still habituate to the tag even with a distinct
  colour/icon -- the marker fixes "does a single PROVISIONAL row read as PASS" (it no longer
  can: `WARN` != `OK` != `BLOCKED`, checked by AC1's difference-arm test), it does not by itself
  fix "does the 53rd WARN in a row still register" -- that is a volume/layout question for the
  `.tsx`, not this section.
- **SAP GY Equity's 100% PASS** is the clean case: every figure's unit and sign were
  established with no open caveat, and every row renders unmarked.

## 3. THE VALUE IS NEVER LOST

A REFUSE's underlying value stays in `check_face.json` beside the verdict, the reason AND the
marker -- `render_print.py` only decides what the PRINT PATH shows. The eventual `.tsx` should
expose the refused value on hover/expand (never as the headline figure), so an analyst who wants
to see what Bloomberg actually returned still can, without it being presented as trusted. This
is the same discipline C-MARK-NOT-DEGRADE names for the pack as a whole, applied at the single-
figure grain.

## 4. WHAT THIS SECTION DOES NOT SPECIFY

No layout or component is chosen here -- C-DESIGN-SPEC-FIRST holds until this section is folded
into the approved spec. `colour_token`/`icon` ARE named here (that is exactly what round-1's
section deferred and round-2 exists to supply): `green`/`OK`, `amber`/`WARN`, `red`/`BLOCKED`
are the tokens the `.tsx` binds -- to a CSS class, a design-system colour, an icon component --
of ITS choosing; this section fixes the TOKEN NAMES and their per-verdict DISTINCTNESS, not the
literal pixels. The `[REFUSED: ...] [BLOCKED]` / `[PROVISIONAL] [WARN]` bracket text above is
the PRINT-PATH (Markdown/plaintext) rendering this cell ships; the page's own visual treatment
(icon glyph, colour swatch, hover target) is AMGT-s-5's decision to make when it writes the
`.tsx`, informed and BOUNDED by this section (the tokens must stay distinct per verdict) rather
than pixel-dictated by it.
