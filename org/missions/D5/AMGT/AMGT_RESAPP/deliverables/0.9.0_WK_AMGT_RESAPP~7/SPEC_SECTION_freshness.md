# SPEC_SECTION_freshness -- for AMGT-s-5's design spec

TO: `AMGT_RESAPP.TO-AMGT-s-7` (cell AMGT-s-7, outcome FWD-7, manifest row S7). Worker
`0.9.0_WK_AMGT_RESAPP~7`. This is the data face's own read of what a page renders from
`coverage_freshness.json` -- it does not draw the page (C-DESIGN-SPEC-FIRST: no `.tsx`
until AMGT-s-5's spec is approved); it hands AMGT-s-5 exactly what the JSON carries and
how it is meant to read on screen.

FWD-7's bar, verbatim: *"Adam can see which covered companies have gone stale. DONE WHEN
EXERCISED -- Adam has used it to find a stale name. ACCEPT: Adam looks in one place, sees
every company the team covers with the date its research was last refreshed, and finds
one that has gone stale without opening any folders."*

## 1. One place, one list

Every row of `coverage_freshness.json["rows"]` renders as ONE list, in ONE place on the
page -- not a per-name detail view, not a tab, not a folder tree. A person opens the page
and the whole coverage set is already in front of them: name, last-refreshed date, and the
rot signal, together.

## 2. Sort order: stale-first

The list sorts by `last_refreshed` ASCENDING with `"NEVER"` sorted to the TOP (a name with
no research at all is the most stale thing on the list, ahead of any dated stamp -- it has
gone the longest without a look, by definition). Among dated rows, the oldest stamp leads;
the most recently touched name sits at the bottom. This is what makes the ACCEPT bar
mechanical rather than a search: the stalest name is always the first thing Adam's eye
lands on, with no scrolling, sorting or filtering required on his part.

## 3. `NEVER` is a state on the list, never its own row and never a blank

A name whose `last_refreshed` reads `"NEVER"` renders EXACTLY like every other row --
same columns, same list, same sort participation (per section 2, at the very top). It is
NOT:
- a separate "not yet researched" section, callout, or accordion;
- an empty cell, a dash, or an omitted value where a date would go;
- excluded from the list, from a count, or from the rot signal display.

The word `NEVER` (or an equivalent plain-English rendering such as "never refreshed")
appears in the date column exactly where a date would otherwise appear. `C-MARK-NOT-
DEGRADE` (this order's BOUNDS): a name with no research is ON the list, not off it, and
saying so is a value, not an error state.

## 4. The rot signal sits beside the list, not apart from it

Each row carries a `rot` field. Three shapes exist in the JSON today and the design must
read all three the same way, in the SAME column (never a separate panel):
- an actual signal string from AMGT-s-15's list register, when that register has landed
  and names this security;
- `"no rot entry for this name at this vintage"` -- the register has landed but has
  nothing for this particular name;
- `"no rot signal at this vintage"` -- the register itself has not landed yet.

None of the three is an error to the reader; all three are states this field can honestly
hold, rendered as plain text beside the row it describes. `G-20` (this order's BOUNDS,
absolute): the rot signal is READ and DISPLAYED here -- it is never the trigger for a
push, an alert, or anything that runs on its own. "Somebody is told" is satisfied entirely
by this view existing and being opened; nothing pages, mails or schedules a check.

## 5. Per-input clocks, one level down

`per_input` (`bloomberg`, `seekingalpha`, `serp` at this vintage -- the set can grow) holds
each vendor's own last-refreshed stamp, independent of the row's overall `last_refreshed`
(which is the latest of all of them, or `NEVER` if all inputs read `NEVER`). This is a
secondary read, not the headline: the page's main list shows the ONE `last_refreshed` date
per section 1-2; `per_input` is available as a detail (an expandable row, a tooltip, a
second column group -- AMGT-s-5's call) for the case where Adam wants to know WHICH input
is stale on a name that shows a recent overall date from a different vendor. FWD-12's
clocks differ by input, and this is where that shows without cluttering the primary scan.

## 6. `security_key` may be absent -- render the name anyway

A universe entry whose identity layer (AMGT-s-12) could not resolve a Bloomberg ticker
carries `security_key: null` in this JSON. Its row still appears (section 3: every
universe entry appears), with `last_refreshed: "NEVER"` and every `per_input` entry
`"NEVER"` -- there is no store key to look anything up under, so nothing can ever have
landed for it, and that reads identically to "the store has genuinely nothing for a name
that DOES have a key." The page does not need to distinguish the two cases to satisfy
FWD-7's bar (a stale name is a stale name either way); if a later cut wants to
distinguish them, that is a new field, not a repurposing of `last_refreshed`.

## 7. Generation is on demand, never a running process

`generated_at` on the JSON's root is the one timestamp on the whole page that is allowed
to describe "when this snapshot was built," visible somewhere on the view (a small caption
is enough) so Adam knows how current the list itself is. This is the ONLY freshness-of-the-
view-itself signal; it is not a per-row field, and it does not imply anything runs
automatically to keep it current (`G-20`: a person, or a page build step a person triggers,
runs `python -m lib.research.freshness.build_view` -- nothing in this project schedules
that run).
