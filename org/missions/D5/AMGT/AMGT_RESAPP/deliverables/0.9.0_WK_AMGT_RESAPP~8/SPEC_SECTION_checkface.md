# SPEC SECTION -- the check face (for AMGT-s-5)

**Author:** `0.9.0_WK_AMGT_RESAPP~8` | **Cell:** AMGT-s-10 | **Status:** data face + print-path
render WIRED; NO PAGE YET (C-DESIGN-SPEC-FIRST -- this is the section AMGT-s-5 folds into the
approved spec before any `.tsx` is written).

## 1. THE THREE STATES, AT A GLANCE

Every figure on the page carries exactly one of three verdicts. None of them is a blank, a
zero, or a row that is simply absent -- absence is not a state this system produces.

| Verdict | What Adam sees in place of / beside the value | Meaning |
|---|---|---|
| **PASS** | the value, plain | unit and sign are MEASURED; the figure is defensible as printed |
| **REFUSE** | `[REFUSED: <reason>]` **replacing** the value | the figure's unit or sign was never established -- the value is never shown as if trusted, even though it is still recorded (see s.3) |
| **PROVISIONAL** | the value **with** `[PROVISIONAL]` beside it | the unit/sign ARE measured but a live caveat (e.g. a cross-check that does not reconcile) has not been resolved -- "we do not know for certain" is shown, never silently folded into PASS |

**At a glance, on the page:** a REFUSE figure's cell looks BROKEN (bracketed, no number visible
where a number is expected) -- that is deliberate; FWD-10's bar is that a failed check is
VISIBLE as failed, not merely logged. A PROVISIONAL figure's cell looks NORMAL but flagged --
the number is there (so the analyst is not blocked from seeing it), and the flag is a
DIFFERENT visual marker (a distinct tag/colour in the eventual `.tsx`, not the bracket text a
REFUSE gets) so the two never read the same at a glance.

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
  pair, so the figure rule correctly refuses rather than guessing.
- **BABA US Equity's 103 PROVISIONAL** all carry a `currency_caveat`: a real, measured
  reconciliation gap (the fiscal-year-2025 merged-row naive P/E disagrees with Bloomberg's own
  `PE_RATIO` by a factor consistent with several uneliminated causes -- currency basis,
  fiscal/calendar row-split, or ADR ratio). The unit and basis ARE known; what is NOT known is
  whether the printed value is on the basis Adam expects, so it renders flagged rather than
  plain.
- **SAP GY Equity's 100% PASS** is the clean case: every figure's unit and sign were
  established with no open caveat.

## 3. THE VALUE IS NEVER LOST

A REFUSE's underlying value stays in `check_face.json` beside the verdict and the reason --
`render_print.py` only decides what the PRINT PATH shows. The eventual `.tsx` should expose the
refused value on hover/expand (never as the headline figure), so an analyst who wants to see
what Bloomberg actually returned still can, without it being presented as trusted. This is the
same discipline C-MARK-NOT-DEGRADE names for the pack as a whole, applied at the single-figure
grain.

## 4. WHAT THIS SECTION DOES NOT SPECIFY

No colour, layout or component is chosen here -- C-DESIGN-SPEC-FIRST holds until this section
is folded into the approved spec. The `[REFUSED: ...]` / `[PROVISIONAL]` bracket text above is
the PRINT-PATH (Markdown/plaintext) rendering this cell ships; the page's own visual treatment
(icon, colour, hover target) is AMGT-s-5's decision to make when it writes the `.tsx`, informed
by this section rather than dictated by it.
