# SPEC_SECTION_lists -- where the rot signal appears on the page

**For:** `AMGT-s-5` (THE PRINT RENDERER, the Security Analysis page's design spec owner --
`C-DESIGN-SPEC-FIRST`: no `.tsx` is written on any portal cell, including `AMGT-s-7`, until a
design is approved). **From:** `AMGT-s-15` (THE LIST REGISTER), which owns the two lists and the
rot signal, never the page. This section is an INPUT to the design AMGT-s-5 approves, not a
design itself -- no `.tsx` file is written by this cell (the bound this task order carries).

## What exists to render

`rot.py` (`lib/research/lists/rot.py`) writes `rot_signal.json` beside the two owned lists
(`publishers.json`, `social_accounts.json`). Its shape, exactly:

```json
{
  "computed_at": "<when rot.py last ran>",
  "lists": {
    "publishers": {"owner": "...", "owner_status": "UNASSIGNED", "reviewed_at": "...",
                   "review_interval_days": 90, "entries_total": 2, "entries_stale": 0,
                   "list_stale": false, "unresolvable_count": 0, "unresolvable_domains": []},
    "social_accounts": {"owner": "...", "owner_status": "UNASSIGNED", "reviewed_at": "...",
                        "review_interval_days": 30, "entries_total": 267, "entries_stale": 0,
                        "list_stale": false, "unresolvable_count": 0, "unresolvable_domains": []}
  }
}
```

A frontend component reads this file (a static read, never a live computation in the browser)
and renders it. `rot.py` itself is invoked by a person, or by a build/generator step that
produces the committed artifact -- never by a runtime schedule, alarm or push channel inside the
portal (`G-20`, the alerting moratorium, binds `AMGT-s-7` and `AMGT-s-15` together per the
decomposition's own bounds table).

## Where: inside AMGT-s-7's coverage-freshness view, not a new page

`AMGT-s-7` is "every covered name with its last-refreshed date, in one place a person OPENS. A
view, never a monitor, alarm or scheduled checker" (decomposition row S7). The two owned lists
are not per-name data, so they do not belong inside the per-name table `AMGT-s-7` already
renders. Proposed placement: **one small panel above or beside that per-name table**, titled
something like "List health" or "Source lists," rendered from `rot_signal.json` on every page
load (a normal GET of a static/generated artifact -- not a poll, not a subscription):

- **One row per owned list** (`publishers`, `social_accounts`), each showing:
  - the owner, rendered EXACTLY as `rot_signal.json` carries it -- at this cut that is the
    literal string `UNASSIGNED -- Andrew names the owner (C-NO-CONTACT: not Adam's team
    directly)`, never a placeholder name, never blank (`C-LIST-OWNER`: no list renders without
    its owner field, and an unassigned owner is a stated fact, not a gap left silent).
  - `entries_stale of entries_total stale (>review_interval_days days)`, plus, for publishers
    only, `unresolvable_count unresolvable` -- the same two sentences `rot.py` prints to a
    terminal, reused verbatim so the page and the person running the script by hand are reading
    the SAME claim rather than two descriptions that can drift apart.
  - `computed_at`, so a reader can see how fresh the rendered rot check itself is (a rot signal
    with no vintage would be exactly the silent-lapse failure `C-LIST-OWNER` exists to prevent,
    one level up).
- **This panel is a rendering of a file, never a live check.** It carries no button that
  triggers a fetch, no auto-refresh timer, and no alert state (red/amber/green iconography is
  fine -- an alarm is a PUSHED notification, a coloured badge on a page a person already opened
  is not one). If `entries_stale > 0` or `unresolvable_count > 0` for a list, the row is the
  thing that tells the person; nothing pages anyone.

## What this section does not decide

The exact panel layout, its position relative to the per-name table, and its visual treatment
are `AMGT-s-5`'s call as the design-spec owner -- this section states the DATA SOURCE
(`rot_signal.json`, its shape above) and the ONE BOUND (`G-20`: render-on-open, never a monitor)
that a design must satisfy, not the pixels.
