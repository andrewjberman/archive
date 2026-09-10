# SPEC_SECTION_social -- the Social Discussion panel (for AMGT-s-5's DESIGN_SPEC.md)

*Produced by AMGT_RESAPP.TO-AMGT-s-13 (`0.9.0_WK_AMGT_RESAPP~6`), to be folded verbatim
into the Security Analysis page's DESIGN_SPEC.md as its own section, per AMGT-s-5's
worker face ("Fold in the SPEC_SECTION_*.md files the wire cells produced ... verbatim
as sections").*

## What the panel shows

A "Social Discussion" panel, one per security, listing `social_items` records
(`lib/research/social/schema.json`) admitted by the item rule
(`lib/research/rules/item.py`, AMGT-s-11). Each row shows:

- the platform and posting account's handle
- the account's official status (`MEASURED` / `INFERRED` / `UNRESOLVED`) as a small
  badge next to the handle -- an `UNRESOLVED` account is visibly marked as such, never
  silently treated as confirmed
- the post text, timestamp, and a link to the original
- the item rule's verdict badge: `PASS` (green, "ABOUT the security"), `PROVISIONAL`
  (amber, "cannot yet determine aboutness"), or `REFUSE` (never rendered as a row --
  a refused item does not appear in the panel at all)
- on hover/expand, `rule_reason` -- the exact sentence an analyst points at to answer
  "why was this admitted" (FWD-11's bar)

## The disclosure line's placement on the page

**The `source_line` renders as a single small-print line directly under the panel's
own header ("Social Discussion"), above the first item row -- not in a footnote, not
collapsed behind a tooltip.** For this account its text is F13's disclosure verbatim:

> general-social plus finance-adjacent; the cashtag-native venue (StockTwits) carries
> 0 datasets on this account

This placement is deliberate: `source_line` is a REQUIRED field in `schema.json` (not
optional decoration), and `validator.validate_item` refuses any record whose
`source_line` is missing or blank before it would ever reach this panel. The
disclosure sits at the top of the panel precisely because it qualifies *every* row
below it, not any single one -- an analyst reads the caveat once, before the feed,
not once per item.

## C-RULE-MUST-EXIST: the panel is held back until the rule has its distribution

The item rule is `held_back` at this cut (`lib/research/rules/__init__.py`:
`threshold=None`, `distribution=None`, `produced_by="AMGT-s-4/-b4/-13"`) -- no
qualification threshold exists yet, because the measurement that would produce one
(`MEASUREMENT_PLAN.md`, this same cell) has not been triggered (G-24: no vendor word).
Until that distribution exists:

- every admitted item in the panel carries `admitted: PROVISIONAL`, never a hard
  `PASS`, because the rule cannot yet tell "ABOUT the security" from "not yet
  determined" with confidence
- the page holds the Social Discussion panel's class-level display back accordingly
  (C-MARK-NOT-DEGRADE): it is shown as a labelled, honestly-provisional panel, never
  silently upgraded to look like a finished feed
- the panel's own empty/held state reads: *"Social discussion measurement not yet
  triggered -- see AMGT_RESAPP.TO-AMGT-s-13's MEASUREMENT_PLAN.md. No feed is shown
  until Andrew's per-use word arrives and the first measurement runs."*

## Identity dependency (C-IDENTITY-RESOLVED)

The panel never shows an item's `account.official: UNRESOLVED` state next to another
already-resolved source on the same page as though they were equally confirmed
(`lib/research/identity/resolver.py`'s `render_together()` is the mechanical form of
this rule for the identity layer generally; `validator.attach_to_security` is this
cell's own instance of it for social items specifically -- an `UNRESOLVED` item is
never attached to the security at all, so it cannot appear mixed in with confirmed
sources).

## Vintage

Every displayed number/record on the panel carries its own `posted_at` and (once
triggered) the measurement's own retrieval timestamp, per the page's general
vintage rule (pre-brief notes s.5) -- consistent with every other panel on the page.
