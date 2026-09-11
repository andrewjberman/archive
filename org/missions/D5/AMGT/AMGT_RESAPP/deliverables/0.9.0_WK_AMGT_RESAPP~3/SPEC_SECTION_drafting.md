# SPEC SECTION -- Drafting face, for AMGT-s-5's design spec (THE PRINT RENDERER)

Author: `0.9.0_WK_AMGT_RESAPP~3` (AMGT-s-9, the drafting face). Consumed by: `AMGT-s-5`'s design
spec for the Security Analysis page (F1's four template blocks). **This section describes the
VISUAL MARKING requirement and the data shape it renders from; it prescribes no `.tsx`
(C-DESIGN-SPEC-FIRST) and no implementation.**

## FWD-9's bar, restated as a rendering requirement

"Machine-written prose is never mistaken for a firm view... An analyst can tell at a glance which
sentences a machine wrote and which the firm owns, and the machine-written ones sit next to the
evidence behind them. They are a starting point someone edits, not a finished claim." Three
consequences for the page:

1. **Every machine sentence is visually distinct from firm-authored text, at a glance, with no
   hover/click required to discover it.** A caption in a footnote is not "at a glance."
2. **The evidence sits BESIDE the sentence, not behind a separate link.** An analyst reading the
   sentence sees, in the same visual unit, what it was drawn from.
3. **The page must invite editing.** A machine sentence is a draft, not a claim -- the affordance
   (an edit icon, a click-to-replace, whatever the visual language chooses) must be present on
   every machine sentence, not just theoretically available.

## What the drafting face hands the page

Per security, `drafted_sections_<security_key>.json`:

```json
{
  "sections": [
    {
      "section": "company_description|investment_thesis|risks|ceo_bio|recommendation",
      "sentences": [
        {
          "text": "the full drafted sentence, including its quoted span inline",
          "generated": true,
          "evidence": ["item_id or figure_id, ..."],
          "quoted_spans": ["the exact verbatim substring(s) this sentence quotes"],
          "verbatim_check": "PASS"
        }
      ]
    }
  ]
}
```

Five section objects are ALWAYS present, in this order (Andrew's ruling, brief O9): company
description (with segments), investment thesis, risks, CEO bio, recommendation. **A section with
an empty `sentences` array is a real, honest state -- "no evidence exists for this limb yet" --
and must render as a visibly empty/placeholder limb an analyst can fill by hand, never as a
missing block that looks like a page-rendering bug.**

## The marking, concretely

| Element | Rendering requirement |
|---|---|
| `generated: true` | The sentence carries a persistent visual marker (e.g. a distinct background tint, a left-border rule, an icon) that is present for EVERY machine sentence and for NO firm-authored text -- never a marker that fades after first read, never one only visible on hover. |
| `evidence` | Rendered adjacent to the sentence (not a separate tab/section): each id resolves to a coverage item (title, source, link) or a figure (mnemonic, value, vintage) the analyst can expand inline. An id that does NOT resolve is a page defect, not a silent blank -- AC2 exists precisely so this never ships. |
| `quoted_spans` | The verbatim span(s), rendered with a quotation treatment (e.g. italics or a quote glyph) distinguishing "words lifted exactly from the source" from the sentence's own connective prose. |
| `verbatim_check` | NEVER rendered to the analyst as a value (it is a build-time/pipeline gate, not a reader-facing field) -- its only visible effect is that a `REFUSE`d sentence never appears on the page at all (dropped upstream, per C-VERBATIM-GATE). |
| edit affordance | Every machine sentence carries an inline edit control (replace/accept/delete) -- the page's default state assumes every machine sentence will be touched by an editor, not shipped as-is. |

## What is NOT resolved yet, and how the page should show it

At this cut, `evidence` on every shipped sentence is a coverage `item_id` (AMGT-s-4) -- AMGT-s-1's
figures are not yet cited as evidence (a data-shape gap on the figures side, filed as
`AMGT_RESAPP-Z-W3-S4`, not a page concern). **Practically: `company_description`, `ceo_bio` and
`recommendation` will render EMPTY today for every security**, because no figure or coverage
evidence resolves for them yet. The page must treat an empty limb as "not drafted yet, add your
own" -- a manual-entry affordance identical in shape to the machine-sentence editor, just starting
from a blank sentence instead of a machine-drafted one. This is not a defect the page should hide;
it is the honest state FWD-9 exists to prevent from being papered over.
