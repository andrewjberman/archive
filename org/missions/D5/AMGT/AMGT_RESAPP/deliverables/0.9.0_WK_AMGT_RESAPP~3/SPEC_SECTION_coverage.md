# SPEC SECTION -- Coverage panel, for AMGT-s-5's design spec (THE PRINT RENDERER)

Author: `0.9.0_WK_AMGT_RESAPP~3` (AMGT-s-4, the coverage reader). Consumed by: `AMGT-s-5`'s design
spec for the Security Analysis page (F1's four template blocks). **This section describes the DATA
SHAPE and the HONEST-STATE rendering rules; it prescribes no `.tsx` (C-DESIGN-SPEC-FIRST) and no
implementation.**

## What AMGT-s-4 hands the page

Per security, one `coverage_items_<security_key>.json`:

```json
{
  "security_key": "BABA_US",
  "items": [
    {
      "item_id": "...", "source_class": "ir|publication|sa",
      "source_domain": "...", "title": "...", "published_at": "YYYY-MM-DD",
      "url": "...", "display_domain": "bare.domain",
      "admitted": "PASS|REFUSE|PROVISIONAL", "rule_reason": "...", "mentions": 1
    }
  ],
  "identity_dropped": [
    {"source_class": "ir|sa", "item_ref": "...", "reason": "..."}
  ]
}
```

Ranked already (recency desc, then `mentions` desc) -- the panel renders in array order and does
not re-sort.

## Rendering rule for `admitted` -- SAY THE STATE, NEVER HIDE IT

FWD-4's bar is "an analyst reads what has recently been said ... and followed it out" -- the panel
must let the analyst see what the reader COULD NOT confirm, not silently filter it away (that is
exactly the confident-looking-map failure AC7/AC6 (AMGT-s-12) exist to catch on the identity
layer; the coverage panel must not reintroduce it on the coverage layer).

| `admitted` | Suggested treatment |
|---|---|
| `PASS` | Rendered plainly, full weight in the list. |
| `PROVISIONAL` | Rendered, with a visible marker (e.g. a dotted underline or a small "unconfirmed" tag) carrying `rule_reason` on hover/expand -- **never hidden and never rendered identically to PASS.** This is the honest majority state at this cut (AMGT-s-11's item rule is `held_back`, no threshold). |
| `REFUSE` | NOT rendered in the main list (the item rule found it merely CONTAINS the ticker string, not ABOUT the company) -- optionally surfaced in a collapsed "excluded" affordance so the count is auditable, never silently dropped from the JSON (it stays in the file; the panel's own choice not to headline it is a presentation decision, not a data one). |

`identity_dropped` entries (an item whose source's identity key was UNRESOLVED, e.g. every
`ir`-class item today since `ir_domain` has no vendor word yet) are **not** list items at all --
they never reached `items[]`. The panel's honest state for the IR channel today: an empty or
near-empty IR section with a stated reason ("investor-relations channel identification pending a
live directory scan"), not a blank space that reads as "nothing to show."

## The three source classes, what the panel can promise about each, today

- **`publication`** -- independent, allowlisted (AMGT-s-15) editorial coverage. Not identity-gated.
  Populated from **FIXTURES** at this cut (no G-24 word for a live SERP scan) -- `run_summary.json`'s
  `ir_publication_source` field states this; AMGT-s-5's spec should NOT claim these are live until a
  later order lands the word and this note is removed from the upstream deliverable.
- **`ir`** -- the company's own investor-relations channel, located by SERP (`display_link`, never
  `link` -- F11). Identity-gated on `ir_domain`, which is `UNRESOLVED` for every one of the 89 names
  at this cut (AMGT-s-12 bound d). **Zero `ir`-class items will appear in the panel today, and that
  is correct, not a bug** -- `ir_scan.py` is built and exercised on its fixture only; it is not run.
- **`sa`** -- Seeking Alpha raw JSON, read (never fetched) from what `AMGT-s-b4` has landed under the
  live store. At this cut: **0 keys, every security** -- `AMGT-s-b4`'s one attempt failed at the
  proxy's TLS handshake (row `AMGT_RESAPP-Z-W9-S2`, infrastructure, not a code fault).
  `run_summary.json`'s `sa_raw_keys_found` carries the honest count. **The panel's SA section should
  render an explicit "no Seeking Alpha content landed yet" state, not an empty list a reader cannot
  distinguish from "nothing has ever been written about this company."**

## The unscoped pass, and why AMGT-s-5 should surface it

`reader.check_no_shared_item_sets()` refuses the WHOLE RUN if any two securities carry an identical
attached item set (C-SHARED-DEFECT, the F6 shape on this axis). If a future run of AMGT-s-4 (or a
successor) ever fails this pass, `run_summary.json`'s `unscoped_pass` field will read
`"REFUSED: ..."` instead of `"PASS: ..."` and NO `coverage_items_*.json` will have been written for
that run. AMGT-s-5's page should treat a stale/missing `coverage_items_<key>.json` as "coverage not
available this cycle" rather than falling back to a previous run's file silently -- a page that
serves last cycle's data as if it were current is the same failure mode F6 measured on peer sets,
moved to the presentation layer.
