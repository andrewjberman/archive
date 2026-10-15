# DSGN_RBNDV2 round 8 addendum 4 -- RV-q-1 and RV-r-1 drained, read live (2026-10-15 ~23:2xZ)

Seat: 2.0.0_SA_COO~RB. Direct acts (round-less, LOCAL); the COO's live read is the close and Andrew's smoke test is the grade. RV-s-1 (worker ~30) is still in flight and is recorded when it drains.

## Drain (measured)

- RV-q-1, worker ~28: portal cc368d50 (PanelHeader.tsx, 35 lines changed, and the new test); merge into feature/dsgn-rbndv2-light 7b84bc81; workspace merge 5d414efa14. Real tsc rc=0, 0 diagnostic lines; tests 52 pass 0 fail in 37 files; eslint clean; non-ASCII bytes added 0.
- RV-r-1, worker ~29: portal c2e0802f (RSIModal.tsx, 4 lines, and the new test); merge 5fbc527a; workspace merge eddd38ed3d. Real tsc rc=0; tests 54 pass 0 fail in 38 files; eslint clean; non-ASCII bytes added 0.
- Worktrees 28 and 29 and their branches removed. Nothing pushed.

## Live read (5174, rbndv2-int @5fbc527a)

- Panel titles (/market): Trending Topics, Top / Bottom Performers, Daily Cloud and Global RSI each hold the help icon inside the title element, right of the text (offsets 128 of 142, 198 of 212, 96 of 110, 84 of 98 px), with the 2px underline; none draws a help icon in the right-hand group.
- Global RSI modal, Spotlight cards: three Hottest and three Coldest cards, each with a 1px rgb(196,203,219) outline; HOTTEST labels rgb(20,113,59), COLDEST labels rgb(187,27,48); the modal title holds its icon.

## Issuer rulings

- DSGN_RBNDV2-W28-S1 and -W29-S1 (the order names no commit instrument for the portal repo, which has no `.tools/`; each worker committed the portal files through the workspace `safe-commit.sh` run from inside `portal/`): OBSERVATION, INERT. Ruled: valid; the next order's bounds name the instrument.

## Open

- Census (not yet done as a measurement): 16 other files draw a `HelpCircle` themselves outside `PanelHeader` (an earlier count by file name); which of them sit on a panel title is unmeasured. Goes to Andrew as a list at the next drain, not as a rider.
- RV-s-1 (Trending Topic drilldown) in flight; call laptop-20261015T230503Z-bea4 (rank numbers and arrows) queued at Andrew.
