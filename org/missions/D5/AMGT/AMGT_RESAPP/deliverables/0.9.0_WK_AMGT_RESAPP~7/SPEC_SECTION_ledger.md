# SPEC_SECTION_ledger -- for AMGT-s-5's design spec

TO: `AMGT_RESAPP.TO-AMGT-s-14` (cell AMGT-s-14, outcome FWD-12, manifest row S14). Worker
`0.9.0_WK_AMGT_RESAPP~7`. This is the data face's own read of what a page renders from
`read_ledger(security_key)` (`lib/research/ledger/ledger.py`) -- it does not draw the page
(C-DESIGN-SPEC-FIRST: no `.tsx` until AMGT-s-5's spec is approved); it hands AMGT-s-5 exactly
what the library returns and how it is meant to read on screen.

FWD-12's bar, verbatim: *"An analyst can see where each input came from and re-run any one
alone. DONE WHEN EXERCISED -- one input has actually been re-run by itself while the others
stayed where they were. ACCEPT: For each kind of input -- market data, filings, news, social,
web -- the page shows where it came from, when it last ran, and whether that run worked; and
any one can be re-run on its own. A single button that refreshes everything under one
timestamp does not count."*

## 1. One row per class, three columns, always six rows

For a given covered name, the section renders EXACTLY the six rows of `ledger.CLASSES`
(`market_data`, `filings`, `news`, `social`, `web`, `sa`) -- never fewer, never a row that
only appears once something has run. Each row carries three columns:

| column | where it comes from |
|---|---|
| **source** | `ledger.CLASSES[class]["source"]` -- a label ("bloomberg", "seekingalpha"), or blank/dash when no source is named yet |
| **last run** | `read_ledger(security_key)[class]["stamp"]`, rendered as a date/time -- or the THIRD state below when there is no entry |
| **outcome** | `read_ledger(security_key)[class]["outcome"]` (`OK` / `FAILED` / `SKIPPED`) -- or the THIRD state below |

## 2. THREE states per row, not two -- "not wired" is not "never run"

A naive read of `read_ledger()`'s output sees only two things: a class either has an entry or
it does not. The library actually carries a THIRD, independent fact per class -- whether a
`stage` is registered at all (`ledger.CLASSES[class]["stage"] is not None`) -- and the page
MUST distinguish all three, because they mean different things to Adam:

1. **NOT WIRED** -- `stage is None` (today: `filings`, `news`, `social`, `web`). No button, no
   re-run control, and the row says so in words ("not wired yet") -- never rendered as a blank
   last-run/outcome pair, which would look identical to a class that IS wired but has simply
   never been asked to run. `C-STAGE-PERSISTS` names these classes explicitly at this cut, and
   the page repeating that honesty is the point: a class that reads "fine" when it is actually
   unbuilt is the exact failure this order's own bound would leave invisible.
2. **WIRED, NEVER RUN** -- `stage is not None` but `read_ledger()` has no entry for this
   security's this class yet. The re-run control IS present and enabled; last-run/outcome read
   "never run" (a value, not a blank -- the same `C-MARK-NOT-DEGRADE` discipline AMGT-s-7's
   freshness view already applies to `NEVER`).
3. **WIRED, HAS RUN** -- an entry exists. Last-run/outcome render from that entry directly;
   the re-run control is present and enabled (running it again is exactly the ACCEPT bar).

At this cut, `market_data` and `sa` are WIRED (both retrofitted in this cell); `filings`,
`news`, `social`, `web` are NOT WIRED. `market_data` for the exercised security (`SAP GY
Equity` / `SAP_GY_Equity`) is in state 3 (`last run` = the exercise's own stamp, `outcome
OK`); `sa` for that same security is in state 2 at this vintage (no entry yet for
`SAP_GY_Equity` specifically, even though the class itself is wired).

## 3. One re-run control per row, and it calls exactly one class

Each of the three ROWS in state 2 or 3 carries its OWN re-run control (a button, an icon --
AMGT-s-5's call), and activating it calls `ledger.rerun(security_key, that_row's_class)` --
nothing else. `AC4` is the mechanical guarantee behind this: no function anywhere in
`lib/research/ledger/` re-runs more than one class, so there is nothing FOR a "refresh all"
control to even call if one were drawn. **Do not draw one anyway.** FWD-12's own ACCEPT line
rules this out explicitly: *"A single button that refreshes everything under one timestamp
does not count."*

## 4. What re-running shows, exercised for real

This order's own exercise (item c) re-ran `market_data` alone for `SAP_GY_Equity`
(`ledger_before.json` / `ledger_after.json` in this deliverables folder; `check_rerun.py`'s
own read: `RERUN market_data on SAP_GY_Equity: classes moved 1 (market_data), classes
unchanged 5, outcome OK`). On the page, the visible effect of pressing ONE row's control is:
that row's last-run stamp and outcome update; every other row's three columns are
byte-for-byte the same as before the click. If a future build ever makes two rows change
from one click, that is the single-timestamp violation FWD-12 names, and it is a regression
in the page, not a new feature.

## 5. Deliberately not built here

No `.tsx` (`C-DESIGN-SPEC-FIRST`). No schedule, alarm or automatic re-run of any class (`G-20`
-- a re-run is a person pressing a control on THIS page, never a timer). No vendor call from
this document or from `lib/research/ledger/` itself (`G-24`) -- the ledger reads and writes
its own store artifact; the actual vendor calls live in the two retrofitted sibling modules,
outside this cell's library.
