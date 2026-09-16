# Portal repo: cross-fabric integration plan, and the localhost login defect

**Author:** 0.0.0_AB_MSTR~Z (site Z integrator).
**Version:** v2, 2026-09-14 ~21:0xZ. It folds in the laptop's census (bus 5cd68b32, 0.0.0_AB_MSTR) and the
L1 execution (msg 22925). v1 was @3168aa9dfb.
**Asked by:** Andrew, at the 1.0.0_SA_CTO~Z terminal ~20:1xZ, referred to this seat in msg 22917, and in
parallel at the 0.0.0_AB_MSTR terminal ~20:0xZ (bus 799eb895). Both MSTRs agreed this is ONE plan, from this
seat.
**Status:** PLAN ONLY, except L1 below, which 1.0.0_SA_CTO~Z executed device-locally with no commit. Nothing
was merged, pushed, promoted or published. The portal freeze stands. Every act below waits for Andrew's
word, one act at a time.

## The ask, verbatim

> "On this device we are still having an issue with the login from the localhost not going to the proper
> cloudfront. I realize that what this really entails is that there also needs to be an /integrate merge
> action of the Portal Repo, not just the ajb_workspace repo. This may be a bit complicated because there has
> been a lot of portal work on the laptop fabric, so we need to figure out a plan on how to properly execute
> this integration, please refer this matter to MSTR~Z (there is no portal-specific branch for sitez vs
> laptop as far as I am aware)."

## 1. The login defect was not a portal-merge problem, and it is fixed on the site-Z view

**Cause, read at source.** The dev server picks its auth host from one environment variable:

| file | line | reads |
|---|---|---|
| `src/contexts/AuthContext.tsx` | 76 | `VITE_AUTH_API_URL ?? 'https://7k3ed8px20.execute-api.us-east-1.amazonaws.com'` |
| `src/api/api-client.ts` | 17 | the same variable and the same fallback |

| env file (tracked, identical on both fabrics) | `VITE_AUTH_API_URL` | effect |
|---|---|---|
| `.env.production` | set, EMPTY | production calls `/auth/*` same-origin, through CloudFront `d2n2nzpeqf34ge` |
| `.env.development` | NO LINE | every localhost dev server calls API Gateway directly, CROSS-ORIGIN |

Cross-origin, the refresh cookie that `/auth/mfa/verify` sets is a third-party cookie, so the browser can drop
it and login fails or does not stick. Portal commit `89ecfd89` (2026-08-31, already inside the pin) states this
defect in its own message. It added the same-origin `/auth` dev proxy to `vite.config.ts` and committed nothing
else; its author launched dev with the variable set empty by hand.

**Why a merge could not fix it.**
- **No difference anywhere in git.** `vite.config.ts`, `AuthContext.tsx`, `api-client.ts`, `.env.development` and `.env.production` have 0 diff lines between the pin `e85f6eb84f`, `origin/DEV` and `origin/PROD`.
- **No site-Z change touches them.** No local-only site-Z portal ref modifies those five paths.
- **The laptop's own `vite.config.ts` drift is unrelated.** Local DEV differs from origin by 17 lines, all `cacheDir` and comments, with the same three proxy hosts.

**Why the laptop works: CONFIRMED by 0.0.0_AB_MSTR (bus 5cd68b32, key state only, no values).**
- **Main checkout:** laptop `portal/.env.local` is untracked and gitignored. It carries `VITE_AUTH_API_URL` SET EMPTY, added 2026-09-11 ~05:55Z; the backup written that minute has no auth line.
- **The server Andrew has used all afternoon:** `.worktrees/d13-visual-elevation/portal`, on `::1:5173/5174`. It has its own `.env.local` with the same empty line.
- **Why it never showed up here:** a device-local file like this never travels by any merge.
- **Side note for its owner:** laptop `portal/.env.local.bak-20260911` is untracked but NOT gitignored, so a broad `git add` would commit it.

**L1 EXECUTED on site Z (1.0.0_SA_CTO~Z, msg 22925, device-local, no commit).**
- The `:5173` view was restarted with `VITE_AUTH_API_URL` empty; the served `AuthContext.tsx` reads `""`.
- Exercise: `POST localhost:5173/auth/login` returned `400 {"error":"Email and password are required"}`, md5 `9e285e9a068e`, byte-identical to `opalinvest.dev`.
- Reach: this covers only that view. Any other dev server started without the variable, on either device, repeats the defect.

**L2, still Andrew's call.** Commit `VITE_AUTH_API_URL=` (empty) into the tracked `.env.development`. Then no
dev server on any device depends on a hand-made local file.
- **Blast radius:** `.frontend-dev/runners/category-views-fixture-proxy.mjs` relays `/auth/*` to vite, and vite's `/auth` proxy reaches CloudFront, so it keeps working. Its header comment ("it uses VITE_AUTH_API_URL -> the real gateway") goes stale and should be edited in the same commit.
- **Cleanup that becomes safe:** the laptop `.env.local` lines become redundant but harmless.
- **Freeze:** it is one portal commit. It is not a promote and does not move the gitlink.

## 2. The portal work that does need integrating

There is no per-fabric portal branch; both sides confirmed.
- **Trunk:** `origin/DEV 5b959f63ca` is the shared trunk; `origin/PROD b1389c8575`.
- **Gitlinks:** both superprojects (`origin/CLOUD`, `origin/SITEZ`) pin portal `e85f6eb84f`, an ancestor of `origin/DEV`, 5 behind it.

| fabric | ref | ahead of origin/DEV | based on | paths | project | measured by |
|---|---|---|---|---|---|---|
| laptop | local `DEV` 35797660 | 90 | origin/DEV (0 behind) | 273 | IRPT_FNTEND (2.0.0_SA_COO~F 39, workers 51) | 0.0.0_AB_MSTR |
| laptop | `feature/d13-visual-elevation` 9b69f790 | 37 | origin/DEV (0 behind); 86 behind laptop DEV | 202 | DSGN_REBRND | 0.0.0_AB_MSTR |
| laptop | 15 `wk-irpt_fntend-*`, 3 `wk-dsgn_rebrnd-*` | 29..89 | on the two lines above | - | worker branches | 0.0.0_AB_MSTR |
| site Z | `refs/drains/rg-2-portal` a845a8be75 | 9 | origin/DEV tip (0 behind) | 28: 26 `src/pages/SecurityAnalysis`, `src/api/endpoints/amgt-lead-panel.ts` (new), `src/App.tsx` | AMGT_RESAPP (contains `rg-1-portal`) | this seat |
| site Z | `refs/drains/posn-5-portal` 6c0deebd91 | 2 | pin e85f6eb84f (5 behind) | 1 so far: `src/lib/chartColors.ts`; round 5 will add Positioning-page files | POSN_ASTTAX, round 5 IN FLIGHT | this seat |
| site Z | local `DEV` 30ca034bba | 0 (19 behind) | stale | none | - | this seat |

### The overlap set

- **Laptop local-only paths: 420.** That is the union of 273 on DEV and 202 on d13, with 55 in both.
- **Site-Z local-only paths: 29.** That is 28 on rg-2 plus 1 on posn-5, with 0 in both.
- **Cross-fabric overlap: exactly 1 path, `src/App.tsx`.**
  - `src/api/endpoints`: 0. Site Z adds `amgt-lead-panel.ts`; the laptop touches `aum.ts` and `investor-reporting.ts`.
  - `src/pages/SecurityAnalysis/**`: 0.
  - `src/lib/chartColors.ts`: 0.
- **`src/App.tsx` is a MECHANICAL UNION, measured on both sides against base `5b959f63ca`** (laptop ranges from bus 8cd9dab4):
  - site-Z rg-2: four pure insertions at `-26,0`, `-53,0`, `-104,0` and `-429,0` (lazy import, import block, `NAV_SECTIONS` entry, route);
  - laptop DEV (IRPT_FNTEND): no hunks;
  - laptop d13 (DSGN_REBRND): 17 hunks, all inside base lines 157-389.

  The sets are disjoint and not adjacent: the nearest pairs are 104 against 157, and 389 against 429. No owner is needed, and the union lands in the d13 leg.
- **POSN's later leg WILL meet the laptop rebrand.**
  - The laptop d13 line modifies three Positioning files: `src/pages/Positioning/Positioning.tsx`, `panels/PositioningSummary.tsx` and `tabs/HoldingsTab.tsx`.
  - POSN round 5's F2 cell edits `HoldingsTab` and `PositioningSummary` (1.0.0_SA_CTO~Z breakdown, msg 22837), so at least two files are shared.
  - `src/api/portal-proxy.ts` and `src/lib/chartColors.ts` are untouched by the laptop.
  - Per-hunk ranges get measured when that leg is real. Filed as a surprise row on POSN_ASTTAX's own channel, so the round-5 owners see it before integration.
- **The largest integration is inside the laptop:** DEV (IRPT_FNTEND) and d13 (DSGN_REBRND) share 55 paths, and d13 is 86 behind laptop DEV. That, not the cross-fabric seam, is where the real conflict work is.
- **v2.2 update, laptop-internal leg only** (0.0.0_AB_MSTR bus 81f1575c; source 1.0.0_SA_CTO msg 96785, adjudication @46664e15f4, IRPT_FNTEND FE-s-45 RULING B). `vite.config.ts` and `package.json` join the DEV-vs-d13 reconcile:
  - **DEV line, will change:** the vite runner loader in `vite.config.ts` (`fileURLToPath` at `:13` and `:16`) and the config-loading scripts in `package.json`.
  - **d13 line, already changed:** `vite.config.ts` (`6eb5582c` routes `/api/scoped/security-scanner` through CloudFront; `8274a955` adds `manualChunks`), and it lacks FE-s-38's `cacheDir` block. `git diff --stat DEV feature/d13-visual-elevation -- vite.config.ts` reads 23 lines today.
  - **Site Z touches neither file** (paths measured above), so the cross-fabric overlap is still exactly `src/App.tsx`.
- **d13's Scanner proxy change bears on localhost.** Once the laptop lines merge, the Security Scanner is proxied through CloudFront in dev. That is a likely factor in the laptop-localhost Security Scanner 403 reported separately below. Not measured here.

**What each push does in CI, read from `.github/workflows`:**
- push to `DEV` runs `ci.yml`: lint, typecheck, build, and an artifact upload. It deploys nothing.
- push to `PROD` runs `deploy.yml`, which is the production deploy: S3, CloudFront invalidation and tag.
- `promote-to-prod.yml` is manual only.
- Pushing any other branch runs nothing.

**A green DEV CI run is not typecheck evidence.** `ci.yml:56` runs `bun run tsc --noEmit`. The portal's own
CLAUDE.md measured that bare form compiling an EMPTY file set and passing on code with deliberate type errors.
The integration's typecheck must be `bun run typecheck` (the `tsc -b` form), run locally, with one deliberate
error first to prove it can fail. Fixing `ci.yml` is a separate portal commit and is not proposed here.

## 3. Proposed sequence

Each numbered step is its own act and waits for Andrew's word. Merge, never rebase. One resolution per
conflict, applied by whoever merges first.

0. **Login.** L1 is done on the site-Z view. L2 (commit the one env line) is the durable follow-up.
1. **Make the work visible on the remote, without merging it.** Each fabric publishes its local-only tips as
   named non-trunk branches on portal origin:
   - laptop: `laptop/irpt-fntend` and `laptop/d13-visual-elevation`;
   - site Z: `sitez/amgt-resapp-rg2`.

   These trigger no CI and no deploy. A path is not reviewable across fabrics until it is on the remote.
2. **Reconcile the laptop's two lines first, inside the laptop fabric.** IRPT_FNTEND and DSGN_REBRND share 55
   paths and d13 is 86 behind. That merge belongs to the laptop seats that own those projects, since the
   resolutions are their content, and it is the step most likely to need real adjudication.
3. **One integration branch off `origin/DEV`,** merged in order:
   - the reconciled laptop line;
   - site-Z AMGT_RESAPP `rg-2`, whose one shared path is `src/App.tsx`, per-hunk and a union if disjoint.

   Then run, locally:
   - `bun run typecheck` in the `tsc -b` form, proven able to fail;
   - `bun run build`;
   - `/frontend-dev` screenshots of Investor Reporting, the rebranded pages, and SecurityAnalysis.
4. **Land the integration branch on `DEV`.** CI validation runs; nothing deploys.
5. **POSN_ASTTAX joins after its round-5 L10, not before.** Round 5 is mid-flight on `posn-5-portal` from the
   pin, and its spec and decomposition are frozen mid-round; moving its base now invalidates the running
   workers' premises. After the round closes, publish `sitez/posn-asttax-r5` and merge it into DEV the same way.
6. **Promote and gitlink move stay separate.** `DEV -> PROD` only on Andrew's separate word, via `/prod-deploy`
   (DT lane; this is the production deploy). The superproject gitlinks on CLOUD and SITEZ move to the promoted
   commit only after that, one leg per fabric.

## 4. Calls for Andrew

| # | call | recommendation |
|---|---|---|
| C1 | L2: commit the empty `VITE_AUTH_API_URL` line into tracked `.env.development` (L1 is already done) | yes |
| C2 | Does the portal freeze permit publishing named non-trunk branches (step 1), and later landing integrated work on `DEV` (step 4), with no PROD promote and no gitlink move? | step 1 now; step 4 after the laptop reconcile and a clean `tsc -b` typecheck and build |
| C3 | Order: laptop IRPT + d13 reconciled first, then site-Z AMGT, POSN after round 5 closes | as written |
| C4 | Who executes each leg? | each fabric's MSTR publishes its own refs; the laptop reconcile by the laptop project owners; the integration merge by the laptop fabric (by far the larger delta); promote by DT via `/prod-deploy` |

## Not measured, and why it matters

- Laptop-side refs, counts and paths are 0.0.0_AB_MSTR's measurement, and cannot be re-derived from this device.
- The laptop's `src/App.tsx` hunk ranges are not yet received, so "mechanical union" is expected, not shown.
- POSN's later surfaces have not been checked against the laptop's 420.
- The laptop's d13 worktree `vite.config.ts` differs from origin by 38 lines whose content was not read. Its proxy hosts are the same three.
- A separate localhost item, not part of this plan: 2.0.0_SA_COO~D reports the Security Scanner returns 403 on laptop localhost while PROD is fine (relayed by 0.0.0_AB_MSTR). Not measured here.
