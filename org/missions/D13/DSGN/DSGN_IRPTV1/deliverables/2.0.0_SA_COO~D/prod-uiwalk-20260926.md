# DSGN_IRPTV1 -- round 5 drain act: the signed-in admin + Dev PROD walk, 2026-09-26

**Walker:** 2.0.0_SA_COO~D. **Packet:** v3 blob 07b7a000 (CTO @b70ede1756, CRO @a157c45762; Andrew "Agent on an admin+dev
login" @e2eae53ae3). **Principal:** irpt-uiwalk-1790430787@opal.test, created by 2.0.0_SA_COO~P 13:53:14Z, deleted 14:22:22Z.
**Site:** https://opalinvest.dev (PROD 36a37afc = portal-v2.1.188). **Login:** 13:59:21Z; walk ended 14:14Z; the post-delete
reload landed on /login at 14:23:48Z (shots/w15). C: 19G free before login.

## HAR and the route-graded audit

`prod-uiwalk-20260926.har` (this folder, on disk in the repo tree; `*.har` is gitignored at .gitignore:353, so it is NOT committed -- read it in place; sha256 `6b51023cefc04fb200ae52273b6a8de8261f192a4c6477672b6e09fe6727fe96`, 17.7 MB), HAR 1.2, 350 entries, written SCRUBBED IN-STREAM by `owner3.mjs` (every entry scrubbed in
memory before its line was appended; no raw HAR touched disk). Leak checks: the owner's (password / JWT / Bearer: none) and an
independent grep (JWT-shaped strings 0, "Bearer <token>" 0, unredacted Authorization 0).

**A browser-side WRITE GUARD** aborted every non-GET/HEAD/OPTIONS request outside the packet's admitted writes before it left
the browser. It fired 160 times, all `POST .../prod/analytics/ingest` (the portal's own telemetry, every 10 s, from login);
none of those reached the network, so none is in the HAR.

| class (denominator 350) | count |
|---|---|
| GET / HEAD / OPTIONS | 335 |
| POST /auth/refresh | 8 |
| POST /auth/login | 1 |
| POST /api/scoped/investor-reporting/directory/resolve | 3 |
| POST /api/scoped/investor-reporting/selections (K3) | 3 |
| **outside the admitted classes** | **0** |
| any `/auth/admin/` request | 0 |

No export, no POST /analysis, no upload, no vendor call by this walker.

## Grades (each names its FWD and criterion)

| criterion | FWD | grade | evidence |
|---|---|---|---|
| FWD-1 thread | FWD-1 | PARTIAL: sign-in -> page -> keyboard pick -> Holdings served to securities: REALIZED for those hops; Performance NOT_REALIZED (refused SELECTION_UNSUPPORTED for a relationship on both firms tried) | w02, w03-w06, w13 |
| IVE9-AC4 picker look | FWD-3 | PASS at 1440 (portal dropdown, readable ink, names unclipped, combobox + listbox + options present); the 390 header clipping is graded under IVE20 | w02a, w02 |
| IVE11-AC4 model colours | FWD-12 | PASS for the canonical model: Opal Intermediate-Term green on IR = Model Portfolios' Intermediate-Term rgb(16,185,129). Note: "Rebalancer strategy: Opal Satellite 60" (not a canonical model) draws red, label-derived -- IV-e-31 retires that path | w06, w10 |
| IVE12-AC4 asset classes | FWD-13 | PASS: the securities map colours Fixed Income green, Equity blue, Cash light green, Alternatives orange; Positioning's Fixed Income rgb(16,185,129) and Equity rgb(59,130,246) match | w06, w11 |
| IVE13-AC4 drill | FWD-14 | PASS: total -> account -> Satellite 60 -> Opal Intermediate-Term (20 positions) -> securities map and table; no chart broke at any depth | w04-w06 |
| IVE20-AC4 once-over | FWD-18 | FAIL: (1) the level-1 pie labels both slices "Unknown"; (2) Performance prints the raw code `SELECTION_UNSUPPORTED` on the body; (3) after clearing the search the identity card reads "No client selected" beside the previous client's $287,274.21; (4) at 390 the header row (Browse, Firm) is clipped at the right edge; (5) Analysis shows the red "Enter the report recipient" error at rest, and the included accounts read "Account" with no name | w03, w02, w08, w12b, w07 |
| IVE21-AC4 account narrowing on Performance | FWD-2 | FAIL: with a 2-account (Cottonwood) and a 3-account (49financial) relationship chosen, no account filter renders on Performance (`[data-slot*=account-filter]` absent); Performance itself answers SELECTION_UNSUPPORTED | w02, w13 |
| IVE22-AC4 Analysis at rest | FWD-7/8/16 | PASS: with a client, the three variant cards come first; title/recipient/comparisons sit in a closed disclosure; one Generate; the prospect upload is one click away ("Analyze a prospect portfolio instead"). The at-rest error and nameless accounts are graded under IVE20 | w07 |
| IVE23-AC4 firm names | FWD-15 | FAIL: the firm token prints on the body -- identity card "cottonwood -- Relationship" / "49financial -- Relationship", the Holdings chip "cottonwood", every picker option suffix, and the firm menu "49financial / cottonwood / inflection" | w02, w03, w12b |
| IVE25-AC4 colours + keyboard | FWD-12/13/3 | PASS: a client picked by ArrowDown + Enter from the typed search; model and asset-class colours as IVE11/IVE12 | w02, w06 |
| IVE26-AC4 export | FWD-9 | NOT GRADED: an export is outside the packet's limit | -- |
| IVE30-AC3 AI Cottonwood drill colours | FWD-13 | NOT_EVALUATED: the client drill (Anna Thiessen, $46M) renders Fixed Income green, Equity blue, Alternatives orange; no `cash` or `other` class is served yet (M's C_06 run is Monday 2026-09-28, bd-securities Part 2 after) | w14b |
| IVE31-AC3 model colour by code | FWD-12 | NOT YET: IV-e-31 is on the worker branch, not PROD | -- |

## Surprises

- The AI advisor/client drill reads (`perfrp_*`, `platinum/accounts/*/summary.json`, `platinum-summary`) answer 403 even to this
  SUPERADMIN principal, while the client drill still renders from other reads: row S16's "Opal-class only" reading is wrong --
  the refusal is not principal-class (S16 amended by a new row).
- Relationship-level Performance answers SELECTION_UNSUPPORTED on both firms walked (Cottonwood, 49financial).
- The portal POSTs telemetry to `/prod/analytics/ingest` every 10 s from login; any bounded-principal packet that admits only
  named writes must expect it (here the guard kept it off the network).

Screenshots: `prod-uiwalk-20260926.shots/` (w01..w15).
