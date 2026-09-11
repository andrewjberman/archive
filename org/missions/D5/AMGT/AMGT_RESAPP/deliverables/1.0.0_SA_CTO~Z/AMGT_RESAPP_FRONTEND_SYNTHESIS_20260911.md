# AMGT_RESAPP -- FRONTEND SYNTHESIS (CTO fold of the CRO's deep brief into the build)

**author** `1.0.0_SA_CTO~Z` · **2026-09-11** · for `AMGT_RESAPP` (D5/AMGT, site-z)

**Andrew's task to this seat, verbatim:** *"I'm having CRO go deeper on this matter for the frontend
security analysis page, they will basically do a big brief and your job is basically going to be how to
synthesize it into what is being built."* This is that synthesis.

**Inputs, all read in full at source:**
- `4.0.0_SA_CRO` full-stack vision `org/tier1_exec/4.0.0_SA_CRO/deliverables/AMGT_RESAPP_FULLSTACK_VISION_20260911.md@3e25edc3e1` (Parts A-E).
- `CHATTER_VOLUME_DAILY_REFRESH_MECHANISM_20260911.md` (30-day window, 0-100 normalized score, TOP_N=10, weekly floor -- via CRO msg 21256).
- Andrew-direct design rulings 2026-09-11 ~07:2xZ (star=marker not trigger; refresh=explicit action; price+chatter both 30-day; separate `opal-amgt-articles` table, server-side computed) -- carried in the CRO doc Parts B2/C2a/E.
- The PRD `org/missions/D5/AMGT/AMGT_RESAPP/prd/AMGT_RESAPP_PRD.md@v0.3` (14 FWDs, surface manifest S1-S15).
- The unapproved `DESIGN_SPEC.md` (`0.9.0_WK_AMGT_RESAPP~1`, 6-tab shell) -- Part C amends its shell.
- This seat's round-1 L10 grade @`4d31cf4caa` (0 of 14 REALIZED -- 13 need an EXERCISED surface; zero `.tsx` exists; the gate is DESIGN_SPEC approval).

**Supersedes** the mappings in this seat's `AMGT_RESAPP_FRONTEND_FRAMEWORK_20260911.md` where they differ
(that doc predates the CRO's deep brief and Andrew's ~07:2xZ corrections -- notably star-triggers-refresh,
now REVERSED).

---

## 1. THE SYNTHESIS IN ONE PARAGRAPH

Almost all of the CRO's frontend vision maps onto outcomes the PRD already names -- the three tabs, print,
freshness, lists, refresh and the chatter feed each fold into an existing FWD, and the backend gaps B1/B2/B4
are plumbing and constraints for surfaces that already exist. **Exactly ONE piece is genuinely new ground:
the Lead Panel's universe-level Trending/Breakout discovery surface** -- every one of the 14 FWDs is a
*per-security-page* outcome, and none names a *cross-universe triage* capability. That is proposed here as
**FWD-15**, to be confirmed by Andrew when he approves the DESIGN_SPEC (his reserved L2 step), and its Price
axis is the one new backend surface (B3). Nothing here touches round 2 (draining now); it is all round-3
(surface-build) material, gated -- as the round-1 grade already found -- on Andrew's DESIGN_SPEC approval.

## 2. THE COVERAGE CALL (the CTO judgment this synthesis exists to make)

**13 of 14 FWDs are UNCHANGED. One new outcome (FWD-15) is proposed. No FWD is retired or renumbered.**

| CRO Part-C / Part-B element | Maps to | New? |
|---|---|---|
| **Thesis tab** (analysis + why good/bad; model figures + provenance render within) | FWD-9 (S9 drafting) + FWD-1/S1 + FWD-3/S3 | fold |
| **Peers tab** (peer set + competitive advantages) | FWD-8 (S8) | fold |
| **Coverage tab** (public news; star = pure marker) | FWD-4 (S4); star surfaces in Lead Panel | fold |
| **Print** (export of Thesis, upper-right action, not a tab) | FWD-5 (S5) | fold |
| **Freshness & Lists** (folded into Lead Panel List view) | FWD-7 (S7) + FWD-14 (S15) | fold |
| **Model tab CUT** (figures rehome to Thesis / Security mode) | FWD-1/S1 data unchanged; only the standalone tab is gone | fold (removal) |
| **Refresh** (explicit action; queues the harvesters for one name) | FWD-2 (S2 on-demand pull), extended to article harvesters | fold |
| **Chatter axis** of the Lead Panel | FWD-11 (S13 social feed) + the chatter-volume gate | fold |
| **Starred mode** (PM saved-view filter) | small new per-user/per-firm starred list; a sub-feature of the Lead Panel (below), NOT FWD-14 (which is list-ROT, a different thing) | fold (under FWD-15) |
| ⭐ **Lead Panel -- universe Trending/Breakout x Price/Chatter, List/Chart, Security overlay** | **NONE of the 14** -- a discovery/triage surface across the universe, distinct from every per-security-page outcome | **NEW -> FWD-15** |
| **B2 `opal-amgt-articles` store** | backend plumbing for FWD-4 (S4) + FWD-11 (S13) | fold (constraint) |
| **B3 price-ranking** | the new backend surface serving FWD-15's Price axis | new surface under FWD-15 |
| **B1 harvester compute / B4 orchestration** | infra serving FWD-4/FWD-11 | fold (constraint/infra) |

**Proposed FWD-15 (for Andrew to confirm as an L2 DONE WHEN -- plain English, no jargon):**
```
  FWD-15  A PM can see which covered names are worth looking at right now,
          without opening each one -- ranked by how much they are moving or
          being talked about, and can jump straight to any name
          DONE WHEN  EXERCISED -- a PM has actually opened the page, read the
                     ranked list, and clicked through to a name it surfaced
          ACCEPT     Adam or Lauren opens the page cold, sees a short ranked list
                     of names that are moving in price or spiking in discussion,
                     and follows one into its full page -- a decision about WHERE
                     TO LOOK that they would otherwise have made by gut or by
                     scrolling a spreadsheet.
```
⚠ FWD-15 is a PROPOSAL, not yet minted. Minting is the CTO's L4 act, taken at the round-3 boundary (s.5),
once Andrew confirms the bar with the DESIGN_SPEC approval -- not mid-round-2, and not before his word on the
surface itself (it is the centerpiece of his walkthrough, so this is confirming, not inventing).

## 3. THE AMENDED DESIGN_SPEC SHELL (Part C, folded onto the worker's `DESIGN_SPEC.md` sections 2-3)

The worker's `DESIGN_SPEC.md` (`0.9.0_WK_AMGT_RESAPP~1`) is the approval gate; its §2 (Header Panel) and §3
(6-tab shell) are what Part C moves. The shell precedent is unchanged and real:
`PageThemeProvider > PageHeaderCleanBadge > [NEW] LeadPanel (sticky) > TabNavigation > tab content`, canvas
law and per-figure vintage unchanged. Charting stays `recharts` (already the estate's library -- not a new
dependency). The amended shell:

- **§2 becomes the LEAD PANEL** (replaces the single-security header panel; the Bloomberg session-state
  badge and per-figure vintage survive, now inside it):
  - Dropdown+search upper-right: `Trending | Breakout | Starred | -- | (search any ticker)`. Default Trending.
  - **Summary mode** (a mode, not a security): two orthogonal axes `{Trending, Breakout} x {Price, Chatter}`;
    two view modes **List** (ranked top-5 + newest headline per name = the old "Freshness & Lists") and
    **Chart** (time series of the selected metric, top names overlaid).
  - **Starred mode**: same List/Chart, filtered to the PM-starred set; pure saved-view filter, no ranking math.
  - **Security mode** (a ticker selected): overlays that name's price + chatter, and against its peers (S8).
  - **Refresh** is an explicit upper-right action with an in-flight toast (spinner + disclaimer, resolves
    green) -- it queues the harvesters for the shown name; it is NOT wired to starring. Starring is a pure
    marker (Andrew-direct ~07:2xZ, REVERSING this seat's earlier star-triggers-refresh guess).
- **§3 becomes THREE tabs** left-to-right: **Thesis** (was Drafting -- the five prose sections, each machine
  sentence marked beside its evidence per S9/C-VERBATIM-GATE; model figures + provenance render here),
  **Peers** (S8), **Coverage** (S4 news + the star control). **Model tab CUT** ("doesn't mean anything to
  me"); its figures rehome into Thesis and the Security-mode overlay -- FWD-1 the DATA is unchanged.
  **Print** leaves the tab bar and becomes an upper-right export action (S5 `render_pack.py`).

⚠ The `DESIGN_SPEC.md` file lives in a worker's deliverable subtree (owner-in-path lane), so this seat does
not edit it directly. This section IS the amendment for Andrew's approval; on approval, round 3 cuts a cell
to land it into `DESIGN_SPEC.md` alongside the `.tsx` build (or the CRO/worker folds it under its own lane).

## 4. BACKEND GAPS -> SURFACES + CONSTRAINTS (round-3 material)

Proposed new constraints (mint at the round-3 boundary with FWD-15, not now):
- **C-AMGT-ARTICLES-STORE** (Andrew-direct ~07:2xZ) -- per-ticker article content lands in a NEW DynamoDB
  table `opal-amgt-articles`, SHAPED like `opal-news-articles` (title/source/url/published_at/sentiment)
  plus `ticker`/`security_key` (via S12 identity) and `platform` (sa/ft/bloomberg/wsj). It is GENUINELY
  SEPARATE from the general-market `opal-news-articles` (not that table with a filter) and from
  `opal-data-research` (which stays S1's model-block + S5's print-snapshot home). Serves S4 (FWD-4) + S13
  (FWD-11).
- **C-SERVER-SIDE-RANKING** (Andrew-direct ~07:2xZ) -- Trending/Breakout/Price/Chatter are computed
  SERVER-SIDE by daily backend jobs and written as pre-computed per-ticker rows; the Lead Panel READS them
  and never re-derives a ranking from raw counts at render time. Chatter axis = the committed chatter-volume
  gate (30-day, 0-100 normalized, TOP_N=10). Price axis = B3.
- **C-PRICE-RANKING-BOXSIDE** (B3) -- the price axis reads Bloomberg historical/intraday and therefore needs
  the BOX-SIDE puller shape (the ETF-daily-pull shape, A3), not a Lambda calling Bloomberg; 30-day window
  (Andrew unified price + chatter to 30). This is the one new backend SURFACE under FWD-15.
- **C-HARVESTER-COMPUTE** (B1/B4) -- the four harvesters (Playwright + real browser + captcha headroom) run
  on a NEW EC2 box in `infra/aws/terraform/amgt-resapp/` (does not exist yet), following the ASTN_WSJFT
  SHAPE (stopped-between-runs, SSM-woken) but with AMGT_RESAPP's OWN IAM role and write access to
  `opal-amgt-articles` -- explicitly NOT the ASTN_WSJFT box (cross-project isolation). ONE shared box for all
  four (CRO lane decision, non-sovereign); credentials/sessions stay isolated by secret + process. B4: one
  orchestrator ties gate -> active-monitor set -> harvesters -> store -> Coverage.

## 5. SEQUENCING + TIMING (the load-bearing part -- do not disturb round 2)

- **Round 2 is draining under `2.0.0_SA_COO~ZZZ`** (five defect-fix workers spawned @`3730474e77`); it builds
  NO surface and is FROZEN mid-round. Nothing in this synthesis touches it. Adding FWD-15 or a constraint now
  would not halt in-flight workers (LIMB 6 gates issuance, not execution) but would be needless churn under a
  live round -- so it WAITS.
- **The pivot is Andrew's DESIGN_SPEC approval** (the round-1 grade's named single gate for all 14 FWDs
  reaching EXERCISED). This synthesis + the CRO vision are what he approves. Approval does not need B1-B3
  finished -- it needs the SHAPE agreed.
- **On approval, at the round-3 boundary** (after round-2's L10): this seat mints FWD-15 into the PRD (next
  unused number, per the permanent-id contract), adds the four constraints above, updates the surface
  manifest (S16 price-ranking under FWD-15; S13/S4 gain `opal-amgt-articles` as their store), and re-opens
  the two L4-R sign-offs ONCE for that bundle. Then round 3 cuts the surface-build cells.
- **Build order (CRO Part D, ratified as the recommendation):** B2 (`opal-amgt-articles` + write path) FIRST
  -- Coverage has nothing real without it, and it is where the 30-day backfill lands; B1 (harvester compute)
  in parallel (proven scripts, packaging not new logic); B3 (price ranking) independent, start if Andrew
  wants the Price axis at launch vs Chatter-only first; C1/C2 `.tsx` on approval of the shell.
  Backfill note: the one-time 30-day backfill does NOT need B1's scheduled EC2 -- it runs once ad hoc against
  the proven scripts, but needs B2's table to land in.

## 6. WHOSE CALL EACH REMAINING ITEM IS

- **ANDREW (sovereign / L2):** (1) approve the amended DESIGN_SPEC shell (§3 -- the pivot); (2) confirm
  FWD-15's DONE WHEN (§2); (3) the standing per-project gates still open from the PRD -- the social-vendor
  word (S13/FWD-11, C-LISTING-NOT-CAPABILITY), the drafting-model word (S9), the peer quota (S8), the list
  owners (S15/C-LIST-OWNER); (4) NEW: the go on standing up AMGT_RESAPP's own AWS infra (the EC2 harvester
  box + `opal-amgt-articles` table) -- real spend/infra, his call, and the CRO's B1-B4 name it precisely.
- **THIS SEAT (CTO, L4):** this synthesis; mint FWD-15 + the four constraints + manifest rows at the round-3
  boundary; route the DESIGN_SPEC.md amendment to its owner; grade round 2's L10 when its slug lands.
- **`4.0.0_SA_CRO` (lane-level, done / decided):** the vision (delivered); one-shared-box for the four
  harvesters; fix S8 (peer set, 88.9% stale) BEFORE the Security-mode peer overlay ships.
- **BUILD LANES (AE/infra, round 3):** B1-B4 per the constraints above.

**Push state:** LOCAL at write time. `0.0.0_AB_MSTR~Z` pushes.
