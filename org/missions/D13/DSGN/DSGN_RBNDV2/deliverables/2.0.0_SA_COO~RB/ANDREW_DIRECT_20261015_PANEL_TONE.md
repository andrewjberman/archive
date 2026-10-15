# ANDREW-DIRECT -- DSGN_RBNDV2 -- the panel tone (2026-10-15 ~18:5xZ, typed at the 2.0.0_SA_COO~RB terminal)

**Recorded by:** `2.0.0_SA_COO~RB`, from Andrew's typed messages in this session. Verbatim, relayed, never adjudicated wider or narrower.

## His words, VERBATIM

1. > In the current light mode build, are we using EAEAF7 for the sidebar and background? everything is blinding white
2. (after the COO's measured answer and recommendation, below) > Try your recommendation

## What the COO answered between the two (measured live on the build at `localhost:5174`, branch `feature/dsgn-rbndv2-light` @3509eae8)

Yes: the page ground, the sidebar rail and the page wrapper all compute to `rgb(234, 234, 247)` (#EAEAF7) on Market Overview, Model Portfolios, Advisor Intelligence, Philosophy, Portfolio Management and Trade Submission. The white is the panels (`#FFFFFF`), which cover about 76 percent of the screen on Market Overview and 64 to 78 percent on four other pages. **The recommendation he accepted:** a soft off-white panel, `#F8F8FD`, so the lavender ground stays visible (the alternative was keeping white and tinting the panel headers).

## How the COO reads it

One change, tried and reversible: panels and modals paint `#F8F8FD` in place of `#FFFFFF`, and the grounds nested inside a panel follow it so no inset boxes appear. Text colours, the action-fill white text and every other use of `--bg-surface` stay as they are. His next smoke test is the grade; the tone is one token (`--bg-panel`), so a different value is a one-line change.
