# AMGT_RESAPP -- FRONTEND FRAMEWORK (Andrew's design vision, structured)

**author** `1.0.0_SA_CTO~Z` · **2026-09-11** · for `AMGT_RESAPP` (D5/AMGT, site-z)

**Andrew-direct 2026-09-11:** *"review this i want to fold in more frontend design work to give a clear
framework for the actual frontend for AMGT_RESAPP."* **Source:** his frontend design transcript
`Front end security analysis_3367 1.txt` (a Whisper transcript in `1.0.0_SA_CTO~Z`'s downloads, read in
full; NOT in the repo -- its substance is carried here). This is the CLEAR FRAMEWORK; the DESIGN_SPEC
worker details it and the surface cells build to it. Where I INTERPRETED his stream-of-consciousness, it
is marked ">> INTERPRETED" so he can correct.

## 1. THE PAGE SHELL -- three fixed regions

Every security's page has the same shell:
1. **A PERSISTENT TOP PANEL** ("the headline section") -- always visible, unchanged by which tab is
   active. This is the most distinctive piece and s.2 details it.
2. **A TAB GROUP** below it -- three tabs, left to right: **Thesis, Peers, Coverage** (s.3).
3. **PRINT / DRAFTING in the UPPER-RIGHT** of the main panel, above the tab group (s.4).

## 2. THE PERSISTENT TOP PANEL

- **An overview title** plus a **dropdown in the upper-right**: `Trending` | `Breakout` | -- (divider) --
  | every security, with a **search box** to type a ticker and jump to it rather than scroll.
- **TWO VIEW TYPES (the top-level split):**
  - **SUMMARY** -- the top list for the selected section (Trending or Breakout).
  - **SECURITY** -- one company. Here the signature feature: **overlay the company's PRICE and CHATTER,
    and overlay them against the company's PEERS** (peers come from the Peers engine, FWD-8).
- **TWO ORTHOGONAL AXES on the Summary side:** `(Trending | Breakout)` x `(Price | Chatter)`. So a reader
  can see consistent price uptick, most chatter, chatter uptick, consistent chatter trend, or a chatter
  breakout -- the same four combinations Andrew named. **Defaults to Trending.**
- **TWO VIEW MODES within a selection:** `Summary view` (the top ~5 laid out with their price/chatter and
  "some stuff going on with them") and `Chart view` (a time series -- chatter relative to others, and
  chatter relative to stock price). A toggle flips between the ranking list and the chart.
- **"Lots of cool charts"** is the stated headline requirement, not a decoration.

>> INTERPRETED: "Summary vs Security" is the HIGHER split; "Summary view vs Chart view" is a display
toggle WITHIN a selection. Andrew stated both and I have nested them this way; if he meant them as one
axis, this is the line to correct.

## 3. THE TABS (left to right: Thesis, Peers, Coverage)

- **THESIS (first)** -- all the analysis: the summary, what is going on with the company, why it is good
  or bad. "All the analysis stuff that Adam wants." (engine: FWD-9 drafting/analysis; the model figures
  FWD-1 and their provenance FWD-3 render here -- see s.5.)
- **PEERS (second)** -- the peer set and each peer's competitive advantages. (engine: FWD-8; the same
  peer set feeds the top panel's Security overlay.)
- **COVERAGE (third)** -- public news on one side (engine: FWD-4), and a **STAR / WATCHLIST feature**:
  the PMs (Adam, Lauren) can STAR a company; a starred/watchlisted company triggers DEEPER research --
  "deep alternative research, not obvious" -- so Coverage grows richer for watched names. (the watchlist
  owner + rot are FWD-14; the deeper social/alt research is FWD-11.)

## 4. PRINT = AN EXPORT OF DRAFTING (one thing, not two)

Andrew: *"drafting and print are really the same thing -- print is just an export version of drafting."*
So the earlier separate "drafting" and "print" tabs COLLAPSE into one: a **print/drafting control in the
upper-right** that assembles EVERYTHING for the shown company into one document. (engines: FWD-9 drafting
+ FWD-5 print; the displacement test FWD-5 names is met by this export.)

## 5. CANCELLED, and the one placement it forces

- **The "model" TAB is cancelled** -- Andrew: *"model that doesn't mean anything to me."*
- >> INTERPRETED, needs his read: the model TAB is gone, but the model FIGURES (FWD-1, the mechanical
  one-pager numbers) are still a built outcome and need a home. The natural one is INSIDE Thesis (the
  analysis defends the numbers) and/or the Security view of the top panel. I have NOT given them their own
  tab. Confirm that is what he means by cancelling "model".

## 6. MAP TO THE BUILT ENGINES (so the framework is not free-floating)

| framework region | serves / renders |
|---|---|
| Top panel -- Chatter axis, Trending/Breakout | FWD-11 (social) + the CRO chatter-volume refresh selector (`CHATTER_VOLUME_DAILY_REFRESH_MECHANISM`) -- the two rolling-7-day rankings ARE Trending + Breakout |
| Top panel -- Price axis, Security overlay | market data (FWD-1 inputs) + FWD-8 peers for the overlay |
| Top panel -- search / jump to any security | FWD-2 (the on-demand pull -- typing an uncovered ticker fetches it) |
| Thesis tab | FWD-9 (drafting/analysis); FWD-1 figures + FWD-3 provenance render within |
| Peers tab | FWD-8 |
| Coverage tab | FWD-4 (news) + FWD-11 (social) + the star/watchlist (FWD-14 owner/rot; deeper alt research) |
| Print/Drafting (upper-right) | FWD-5 (print export) + FWD-9 (drafting) |
| across all figures | FWD-10 (check face -- a failed check shows marked) + FWD-3 (basis beside the number) |

>> OPEN PLACEMENTS (flagged, not invented): FWD-6 (what-changed / versions) and FWD-12 (the per-input
ledger + re-run) have no explicit home in the transcript -- likely a control within the Security view or
a footer, but that is the DESIGN_SPEC worker's to place, and I am not inventing it here.

## 7. HOW THIS FOLDS IN -- and the timing that avoids disrupting round 2

This framework is the CTO's design DIRECTION; it binds two downstream surfaces:
- **The DESIGN_SPEC** (the worker deliverable pending Andrew's approval, C-DESIGN-SPEC-FIRST): it details
  this framework into the actual .tsx spec. Andrew's approval of the DESIGN_SPEC -- the gate that unblocks
  every surface FWD -- should be given against a spec that reflects THIS framework.
- **The AMGT_RESAPP PRD**: this framework folds in as a constraint (proposed `C-FRONTEND-FRAMEWORK`,
  citing this doc) at the **surface-build round**, NOT round 2. Round 2 is the defect-fix round
  (checkface, impostor, SA re-run, s-12, W1-S2) and builds no surface, so folding a frontend constraint
  into it would only re-block COO~ZZZ's in-flight round-2 issuance over work that round does not do. The
  framework binds when the surface cells are cut, which follows Andrew's DESIGN_SPEC approval.

So the sequence Andrew's five design decisions imply: he approves the DESIGN_SPEC (reflecting this
framework) -> the surfaces become buildable -> the surface-build round cuts cells against
`C-FRONTEND-FRAMEWORK` + the CRO data mechanisms -> the EXERCISED bars become reachable.
