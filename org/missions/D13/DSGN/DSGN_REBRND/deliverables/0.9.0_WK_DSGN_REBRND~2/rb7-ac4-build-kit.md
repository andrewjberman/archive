# RB7-AC4 BUILD KIT -- the brief a fresh builder receives

**For:** `RB7-AC4` of `DSGN_REBRND.TO-RB-s-7` (graded at L9 by `3.0.0_SA_CVO`; no verdict here).
**Prepared by:** `0.9.0_WK_DSGN_REBRND~2`, the contract's author, which is exactly why it is NOT
the builder (row `DSGN_REBRND-W2-S10`). **Owed by:** whoever `2.0.0_SA_COO~D` seats as the builder.

The criterion: *"a worker subagent that has never seen the portal builds ONE new page from the
contract alone and it lands inside the system. The build record and the page are in the
deliverables."* This file is that worker's whole brief. Hand it over verbatim.

---

## THE BRIEF (verbatim to the builder)

**Your only design input is one file:** `portal/DESIGN.md` at portal commit `000478c9` (branch
`wk-dsgn_rebrnd-2b`). Read it with `git show 000478c9:DESIGN.md` from the portal repo, or from the
worktree `C:/tmp/wk-dsgn-2b/portal/DESIGN.md` if it is still at that commit.

**You may NOT read:** anything under `portal/src/`, `portal/design/`, `design/brand/`,
`deck_generation/`, any other `DESIGN.md` revision, any screenshot of the portal, or any page of
opalinvest.com. If the contract does not tell you something, **do not go and find it -- write the
question down** (see the build record below). Those questions are the finding. A page that looks
right because its builder looked elsewhere tests nothing.

**Build ONE page:** a self-contained HTML file (inline CSS, no external requests, nothing
third-party vendored; font stack `Lato, sans-serif` -- the machine may or may not have Lato, and
you record which rendered). Subject: **"Model Portfolio Summary"** for an advisor, carrying:

1. a page title and one line of description;
2. the page's one deliberate band, holding a headline figure (for example total assets under
   management) with its label;
3. a two-column area: a short summary on one side and a detail table on the other;
4. the five duration models, each with a year-to-date return, a one-year return and an allocation
   weight (FIXTURE numbers below, not market data);
5. exactly one primary action ("Download factsheet");
6. one secondary action and one text input (for example a search box);
7. one panel that has nothing to show yet;
8. one warning-level notice (for example "Holdings as of the prior trading day");
9. a visible keyboard focus state on every interactive element.

FIXTURE (not market data, invented for the build):

| model | YTD | 1Y | weight |
|---|---|---|---|
| Ultra-Short Term | +2.1% | +4.3% | 12% |
| Short Term | +3.4% | +5.9% | 18% |
| Intermediate | +5.2% | +8.1% | 30% |
| Long Term | -1.3% | +6.4% | 25% |
| Ultra-Long Term | -3.8% | +2.7% | 15% |

**Deliver into your own deliverables folder** (`org/missions/D13/DSGN/DSGN_REBRND/deliverables/<your serial>/`):
- `rb7-ac4-page.html` -- the page;
- `rb7-ac4-page_1440.png` -- a capture of it at 1440 px wide, read by you before you finish;
- `rb7-ac4-build-record.md` -- for every element above, the clause number(s) of `DESIGN.md` you
  built it from (`C1`..`C12`, `C5.1`..`C5.8`); every place the contract did NOT answer your question
  and what you chose instead; and every value you used that the contract does not name.

---

## WHAT L9 READS (for the grader, not the builder)

"Lands inside the system" is read clause by clause against the page: light canvas and white
panels with a hairline, and one band only (C3); the five models in UST-ST-INT-LT-ULT order with the
canon hexes and a label on every canon mark (C4); no translucent value (C5.8); status and data
kept apart (C6); one purple element (C8); ratios at or above the C9 floors on the actual backdrop;
C10 spacing; C11 radii, no shadow and a `:focus-visible` ring; a 40/60 split and a designed EMPTY
state (C12); Lato with tabular figures and a sign on every change value (C1, C2). The build
record's list of unanswered questions is the contract's own gap list and belongs in the L10 slug.
