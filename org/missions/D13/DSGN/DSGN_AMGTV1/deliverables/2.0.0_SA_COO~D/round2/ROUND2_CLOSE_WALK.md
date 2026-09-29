# DSGN_AMGTV1 -- ROUND 2 CLOSE RECORD -- the one real run (signed-in walk, Valero and INTU)

**Issuer:** `2.0.0_SA_COO~D` (site Z). **Round:** 2 (decomposition v2 @9d2ee3f59e, ADDENDUM 2 @779f16a309).
**Build walked:** site-Z portal DEV `1a1e8162` (AV-e-3 `1af0878d`, AV-e-2 `b6373fa7`, AV-e-5 `57c764d7`, AV-e-6 `fc6e9c1b`,
AV-e-1 `eea64485`, AV-e-4 `1a1e8162`), served on `localhost:5174` from `1.0.0_SA_CTO~Z`'s walk worktree at `ae3eaa45`, which
contains `1a1e8162` (`merge-base --is-ancestor`). `tsc -b` on DEV: 0 errors after every merge.
**Instrument:** `/ui-walk --route /security-analysis --security "VLO US" --security "INTU US"`, 2026-09-29 08:26:19Z-08:29:29Z;
71 screenshots; 125 observations, 8 unique findings (round 1: 32); 0 guard aborts; disarm REFUSED (HTTP 401).
**Artifact:** `tmp/ui-walk/20260929T082619Z/` (gitignored, local to site Z; never committed). The CVO reads the PNGs there.
**Live-payload note:** the scoped API Lambda does not yet serve `model.team_cases` (AMGT_RESAPP vv-4, the redeploy, is
pending), so on the live walk INTU's Recommendation and Model read the designed ABSENT sentence. The SERVED rendering is
proven offline on INTU's captured adapter bytes (AV-e-2 AC1 3 of 3, AV-e-4 AC2 arm C); its live read waits on vv-4.

## THE ROUND'S CELLS ON THE PAGE

| cell | outcome | screenshot(s) | what the page shows |
|---|---|---|---|
| AV-e-1 | FWD-11 | `042-INTU-US-Thesis.png`, `011`-series for VLO | the Thesis panel header is WHITE (one band above it); the chart card reads "The series for the thesis driver, ... is not in the model data yet." / "No chart is drawn until its numbers are there ... The research data team adds the series."; the footer reads "The drafted document does not say how many claims were held back uncited."; the header description reads "Company description" |
| AV-e-2 | hop 6, FWD-6 | `049-INTU-US-Thesis-open-RECOMMENDATION-...png`, card on `042` | live: "The research team's Base case is not in this pack yet. The research team fills it in." above the machine-draft line and the drafted sentences (vv-4 pending, see note) |
| AV-e-3 | FWD-4 | `042`, `043`/`044` (INTU card windows), `030` (VLO) | "Price USD 277.13", "Enterprise value USD 75.28B"; VLO "Price USD 382.86", "Enterprise value USD 117B" |
| AV-e-4 | FWD-9 | `030-VLO-US-Model.png` | lines named in words ("Revenue per share", "Free cash flow yield", "Return on tangible assets" ...); each of the 18 refused lines reads "REFUSED -- The number is in the pack, but this page cannot show it yet because its unit convention is not built."; the team's-Base sentence leads the cases |
| AV-e-5 | FWD-2 | `004-lead-Trending-Price-List.png` | the footer reads "Showing the Trending x Price list (movement is measured)."; row #4 reads "BP LN" (NG LN is outside the ten rows on screen) |
| AV-e-6 | FWD-10 | `035-VLO-US-Posture.png` | the absences read as sentences ("No drafted thesis for Williams Companies, Inc. yet -- the research team's pack does not include one"); still on the face: the comparable line's "identity UNRESOLVED: the form 'WMB_US_Equity' matches no ... crosswalk/v1 ..." (row W8-S2's residual), and the Posture panel header is a dark band |

## THE WALK'S CHECK HITS (8 unique) -- round-3 inputs, none on a round-2 cell's own surface

- `raw-code` 1: "Exec Management: ABSENT (ZERO_OFFICERS)." (the Exec Management tab, FWD-7, not cut yet).
- `design:bands` 1: the Model and Posture tabs' panel headers are still dark bands (AV-e-1 cut the Thesis panel's only).
- Seen on `035`, not a check hit (the check's pattern misses it): the Posture comparable line's raw identity text (W8-S2).
  **Instrument blind spot, the issuer's:** `round2/checks/raw.cjs`'s mnemonic class (`\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b`) cannot
  match a mixed-case security key such as `WMB_US_Equity` (no word boundary between `E` and `q`), so AV-e-6's AC1 read 0 with
  that key on the live face; round 3's census adds a key class.
- `format:money` 1: "USD 1,234" and "$1,234" on one page -- the header is one form now; the other "$" form sits on a surface
  this round did not cut (not localised by the finding; inferred, not measured).
- `format:dates` 1, `design:contrast` 3, `design:tinted-status` 1.
- Also seen, not a check hit: the live rule case still reads "Base case: SERVED -- 743.36 USD" (the served label changes
  with AMGT_RESAPP's round-47 served-text cell and vv-4).
- API: one HTTP 500 on `GET /api/scoped/advisor-intelligence/clients-tab` at the step that selected INTU (an Advisor
  Intelligence read, not a Security Analysis route); 4 console errors (2 login-probe 401s, the 500 twice).

## FWD-1 ON THIS RUN

Hops 1, 2, 4, 5 reached as in round 1. Hop 3: the rows still carry no served name (AMGT_RESAPP round 48). Hop 6: the page
now renders the team's case where served; on the live payload no name serves it yet (vv-4), and Valero's dossier carries no
team case at all (row Z-S1). **FWD-1 NOT_REALIZED**, on hops 3 and 6, both on served data.

## CELLS AND CRITERIA

| order | mechanical (worker's run; re-run by the issuer on DEV 1a1e8162) | judgment (CVO, L9, on the PNGs above) |
|---|---|---|
| AV-e-1 | AC1 thesis 0 hits, AC2 header 0 hits, AC3 4 of 4 | AC4 |
| AV-e-2 | AC1 3 of 3, AC2 3 of 3, AC3 2 of 2 | AC4 |
| AV-e-3 | AC1 3 of 3, AC2 2 of 2 | AC3 |
| AV-e-4 | AC1 model 0 hits, AC2 3 of 3, AC3 2 of 2 | AC4 |
| AV-e-5 | AC1 0 hits, AC2 3 of 3, AC3 3 of 3 | AC4 |
| AV-e-6 | AC1 posture 0 hits, AC2 4 of 4 | AC3 |
| AV-e-7 | direct act (ADDENDUM 2): shell harness re-anchored to the new money form | none |
