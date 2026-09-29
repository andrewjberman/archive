# DSGN_AMGTV1 -- ROUND 1 CLOSE RECORD -- the one real run of FWD-1 (the Valero thread)

**Issuer:** `2.0.0_SA_COO~D` (site Z). **Round:** 1, THE THREAD (PRD v0.2 :159-176; decomposition v1 @fc8fea9577, ADDENDUM 1).
**Build walked:** site-Z portal DEV `5fac7a37` (AV-t-1 `abcec1b2`, AV-t-2 `bdf07b6b` via `7731aa3b`, AV-t-3 `c69bd91a` via
`5fac7a37`), served on `localhost:5174` from `1.0.0_SA_CTO~Z`'s walk worktree `/c/tmp/amgt-walk-5174` at `f3326674`, which
contains `5fac7a37` (`git merge-base --is-ancestor`, positive control run). `tsc -b` on DEV: 0 errors (a planted error: 1).
**Instrument:** `/ui-walk --route /security-analysis --security "VLO US"` (signed in as the dormant walker account, real login,
real data, read-only guard), 2026-09-29 05:16:53Z-05:18:35Z; 40 screenshots, 0 API issues, 0 guard aborts, 2 console errors;
armed and disarmed by the walker (post-disarm login HTTP 401, REFUSED). A first run at 05:15:35Z died before its first
page (Git Bash rewrote `--route /security-analysis` into a Windows path; `page.goto` refused it) and disarmed REFUSED.
**Artifact:** `tmp/ui-walk/20260929T051653Z/` (gitignored, local to site Z; screenshots are never committed). The CVO reads
the PNGs there. This record states what each screenshot shows, in words; it grades no JUDGMENT criterion.

## THE THREAD, HOP BY HOP (FWD-1)

| hop | what the PM does | screenshot | what the page shows | reached |
|---|---|---|---|---|
| 1 | real login | (walker log) | signed in at 05:16Z on the protected local channel | yes |
| 2 | `/security-analysis` -> Trending x Price list | `004-lead-Trending-Price-List.png` | the served generation 2026-09-25 (dated, requested 2026-09-29), ten rows, VLO US at #3, +11.25% | yes |
| 3 | pick Valero by its company name | `004` | the row leads with its served ticker "VLO US"; no row carries a name (AV-t-1 renders one the day it is served) | **NO** -- the name ask (AMGT_RESAPP) is open |
| 4 | header as four cards; open Financials | `011-VLO-US-Thesis.png`, `013-...FINANCIALS...png` | four cards -- Price USD 382.86, Enterprise value $117B, Beta 0.72, Average volume 3.25M; the Financials window lists Enterprise value $117B and Net debt $5.93B, stamped "2026-09-29 \| Source: Bloomberg" | yes |
| 5 | Thesis as three cards under the principal chart | `011` | the chart card (ABSENT, its reason in words) then Investment thesis (5 points), Risks (3), Recommendation (5), each "Read more" | yes |
| 6 | open the Recommendation: whose view, which document | `018-...RECOMMENDATION...png` | leads "This is a machine's draft from the company's filing, not the research team's recommendation. The research team's own position is not in the pack yet."; each passage names "VLO US's 10-K, filed 2026-02-25 -- Item 7 ... paragraph N" | partly -- whose view is stated; the team's position is unserved (AMGT_CORPUS dossier route) |

**FWD-1: NOT_REALIZED on this run**, on exactly the two hops the decomposition named at the cut (s.1): hop 3 (no served
name) and hop 6 (no served team position). Both are other teams' asks, rendered as the live state with its reason, never
fixtures. The remaining four hops run end to end on real data.

## THE WALK'S CHECK HITS (32 unique, 228 observations) -- all off the round's cells

- `raw-code` 25: the lead-panel footer's partition names (`TRENDING_PRICE` and siblings, FWD-2/FWD-11); the header
  description's source line "from bloomberg CIE_DES" (FWD-11); the Model tab's vendor mnemonics and their "NOT-YET-BUILT"
  lines (FWD-9); the Posture tab's storage paths (FWD-10).
- `design:bands` 1 (two #0A1733 bands: the identity header and the Thesis PanelHeader, AMV-39, DSGN_REBRND W1-S9);
  `design:contrast` 3; `design:tinted-status` 1; `format:money` 1 ("USD 1,234" and "$1,234" on one page; the finding names
  no element -- the Price card's "USD 382.86" beside the "$117B" cards is the likely pair, inferred, not measured; FWD-4); `format:dates` 1.
- The brief's own walk (2026-09-28) read 31 findings with the same classes; none of the 32 is on a round-1 cell's face.

## CELLS AND CRITERIA

| order | mechanical | judgment (the CVO's, at L9, on the PNGs above) |
|---|---|---|
| AV-t-1 | AC1 4 of 4, AC2 3 of 3 (instance VALID) | AC3 -> `004` |
| AV-t-2 | AC1 3 of 3, AC2 5 of 5, AC3 2 of 2 (VALID) | AC4 -> `011`, `012`-`015` (each card's window) |
| AV-t-3 | AC1 3 of 3, AC2 8 of 8, AC3 2 of 2 (VALID) | AC4 -> `011`, `016`-`018` (each Thesis window) |
| AV-t-4 | direct act (ADDENDUM 1): the tabs harness HeroGraphic stub, disarming row W3-S1 | none |

## FOR ROUND 2 (enrichment inputs the round-N analysis may name)

1. The served company name on list rows (AMGT_RESAPP) -- hop 3; the Recommendation's document line then reads the company.
2. The dossier route with the research team's position (AMGT_CORPUS) -- hop 6; with it, 1.0.0_SA_CTO~Z's Base-case anchor
   decision (the team's Base leads, labelled; the rule's value a "Historical-multiple reference") and C-CASE-UNIT.
3. The walk's check hits by outcome: FWD-2 (lead-panel captions), FWD-4 (one money format), FWD-9 (Model mnemonics),
   FWD-10 (Posture paths), FWD-11 (the header description's source line; the second band).
