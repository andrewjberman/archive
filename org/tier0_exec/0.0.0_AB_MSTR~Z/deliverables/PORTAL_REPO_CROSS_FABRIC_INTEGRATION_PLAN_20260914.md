# Portal repo: cross-fabric integration plan, and the localhost login defect

**Author:** 0.0.0_AB_MSTR~Z (site Z integrator). **Date:** 2026-09-14, measured 20:19-20:4xZ.
**Asked by:** Andrew, at the 1.0.0_SA_CTO~Z terminal ~20:1xZ, referred to this seat in msg 22917, and in
parallel at the 0.0.0_AB_MSTR terminal ~20:0xZ (bus 799eb895).
**Status:** PLAN ONLY. Nothing here was merged, pushed, promoted, published or restarted. The portal freeze
stands. Every act below waits for Andrew's word, one act at a time.

## The ask, verbatim

> "On this device we are still having an issue with the login from the localhost not going to the proper
> cloudfront. I realize that what this really entails is that there also needs to be an /integrate merge
> action of the Portal Repo, not just the ajb_workspace repo. This may be a bit complicated because there has
> been a lot of portal work on the laptop fabric, so we need to figure out a plan on how to properly execute
> this integration, please refer this matter to MSTR~Z (there is no portal-specific branch for sitez vs
> laptop as far as I am aware)."

## 1. The login defect is not a portal-merge problem

**Cause, read at source.** The dev server picks its auth host from one environment variable:

| file | line | reads |
|---|---|---|
| `src/contexts/AuthContext.tsx` | 76 | `VITE_AUTH_API_URL ?? 'https://7k3ed8px20.execute-api.us-east-1.amazonaws.com'` |
| `src/api/api-client.ts` | 17 | the same variable and the same fallback |

| env file | `VITE_AUTH_API_URL` | effect |
|---|---|---|
| `.env.production` | set, EMPTY | production calls `/auth/*` same-origin, through CloudFront `d2n2nzpeqf34ge` |
| `.env.development` | NO LINE | every localhost dev server calls API Gateway directly, CROSS-ORIGIN |

Cross-origin, the refresh cookie that `/auth/mfa/verify` sets is a third-party cookie, so the browser can drop
it and login fails or does not stick. Portal commit `89ecfd89` (2026-08-31, already inside the pin) states this
defect in its own message. It added the same-origin `/auth` dev proxy to `vite.config.ts` and committed nothing
else; its author launched dev with `VITE_AUTH_API_URL=` (empty) set by hand.

**Why a merge cannot fix it.** Across `vite.config.ts`, `AuthContext.tsx`, `api-client.ts`, `.env.development`
and `.env.production` there are **0 diff lines** between the pin `e85f6eb84f`, `origin/DEV` and `origin/PROD`.
No site-Z local-only portal ref touches any of those five paths. Neither site-Z dev checkout
(`portal/`, `/c/tmp/portal-posn-view`) has a `.env.local`. The only dev server running on site Z is port 5173
from `/c/tmp/portal-posn-view`, and it has the same env files.

**Why the laptop probably works.** Most likely a gitignored `.env.local` or `.env.development.local` on the
laptop sets the variable to empty, or dev is launched with it set. That would never travel by any merge.
**NOT YET CONFIRMED:** asked of 0.0.0_AB_MSTR over the bus (7e1db614), key names only.

### Fix options

| | act | what it touches | reach |
|---|---|---|---|
| **L1** | restart the site-Z dev server with `VITE_AUTH_API_URL=` (empty), by env var or a gitignored `.env.development.local` | no commit, no push, no freeze question | this device only |
| **L2** | commit `VITE_AUTH_API_URL=` into the tracked `.env.development` | one portal commit | every device's dev server goes same-origin, matching production |

- **L1 check it worked:** the check `89ecfd89` used. POST an obviously invalid email to `localhost:<port>/auth/login`; it must return the auth handler's `{"error": ...}` body, byte-identical to `opalinvest.dev/auth/login`, not API Gateway's `{"message": ...}`.
- **L2 blast radius:** `.frontend-dev/runners/category-views-fixture-proxy.mjs` relays `/auth/*` straight to vite, and vite's `/auth` proxy reaches CloudFront, so it keeps working. Its header comment ("it uses VITE_AUTH_API_URL -> the real gateway") would go stale and should be edited in the same commit.
- **L2 freeze question:** a portal commit lands on a drain ref or DEV. It is not a promote and does not move the gitlink.

**Recommendation:** L1 now, by whichever seat owns the running view (1.0.0_SA_CTO~Z started it). L2 next, as
one small portal commit, so no device depends on a hand-set variable.

## 2. The portal work that does need integrating

There is no per-fabric portal branch; both sides confirmed. `origin/DEV 5b959f63ca` is the shared trunk;
`origin/PROD b1389c8575`. Both superprojects (`origin/CLOUD`, `origin/SITEZ`) pin portal `e85f6eb84f`, which is
an ancestor of `origin/DEV`, 5 behind it.

| fabric | ref | ahead of origin/DEV | based on | paths | project | source |
|---|---|---|---|---|---|---|
| laptop | local `DEV` 35797660 | 90 | origin/DEV (0 behind) | not yet received | IRPT_FNTEND (2.0.0_SA_COO~F + workers) | laptop-measured, not verified here |
| laptop | `feature/d13-visual-elevation` | local-only | not yet received | not yet received | DSGN_REBRND | laptop-measured |
| site Z | `refs/drains/rg-2-portal` a845a8be75 | 9 | origin/DEV tip (0 behind) | 28: 26 `src/pages/SecurityAnalysis`, 1 `src/api/endpoints`, 1 `src/App.tsx` | AMGT_RESAPP (contains `rg-1-portal`) | measured here |
| site Z | `refs/drains/posn-5-portal` 6c0deebd91 | 2 | pin e85f6eb84f (5 behind) | 1 so far: `src/lib/chartColors.ts` | POSN_ASTTAX round 5, IN FLIGHT | measured here |
| site Z | local `DEV` 30ca034bba | 0 (19 behind) | stale | none | - | measured here |

Site-Z overlap `rg-2` vs `posn-5`: **0 paths**. The cross-fabric overlap set (laptop IRPT + d13 against site-Z
AMGT + POSN) is **not yet computed**; 0.0.0_AB_MSTR has site Z's path list and is computing it. Likely
hotspots: `src/App.tsx` (routes), `src/api/endpoints/*`, `src/api/portal-proxy.ts` (POSN F2's grant names
`:969`), any shared nav or sidebar config.

**What each push does in CI, read from `.github/workflows`:**
- push to `DEV` runs `ci.yml`, validation only;
- push to `PROD` runs `deploy.yml`, which is the production deploy: S3, CloudFront invalidation and tag;
- `promote-to-prod.yml` is manual only.

**A green DEV CI run is not typecheck evidence.** `ci.yml:56` runs `bun run tsc --noEmit`. The portal's own
CLAUDE.md measured that bare form compiling an EMPTY file set and passing on code with deliberate type errors.
Step 4's typecheck must be `bun run typecheck` (the `tsc -b` form), run locally, with one deliberate error
first to prove it can fail. Fixing `ci.yml` is a separate portal commit and is not proposed here.

## 3. Proposed sequence

Each numbered step is its own act and waits for Andrew's word. Merge, never rebase. One resolution per
conflict, applied by whoever merges first.

0. **Unblock login (L1).** Device-local, no git.
1. **Overlap census.** 0.0.0_AB_MSTR prints the cross-fabric overlap set with its denominator. Nothing moves.
2. **Make the work visible on the remote, without merging it.** Publish the site-Z drain tips as named,
   non-trunk branches on portal origin (`sitez/amgt-resapp-rg2`, later `sitez/posn-asttax-r5`). The laptop does
   the same for its local DEV and d13 work (`laptop/irpt-fntend`, `laptop/d13-visual-elevation`). A path is not
   reviewable across fabrics until it is on the remote. These branches trigger no CI and no deploy.
3. **One integration branch** off `origin/DEV`, merged in order:
   - laptop IRPT_FNTEND (largest, based on DEV, 0 behind);
   - site-Z AMGT_RESAPP `rg-2` (based on the DEV tip);
   - `d13` if Andrew wants it in this pass.

   Resolve only the overlap set. Then `bun run typecheck` (the `tsc -b` form; bare `tsc --noEmit` checks
   nothing here), `bun run build`, and `/frontend-dev` screenshots of the pages each project touched.
4. **Land the integration branch on `DEV`** as a merge or fast-forward. CI validation runs; nothing deploys.
5. **POSN_ASTTAX joins after its round-5 L10, not before.** Round 5 is mid-flight on `posn-5-portal` from the
   pin, and its spec and decomposition are frozen mid-round; moving its base now invalidates the running
   workers' premises. After the round closes, merge `posn-5-portal` into DEV the same way.
6. **Promote and gitlink move stay separate.** `DEV -> PROD` only on Andrew's separate word, via `/prod-deploy`
   (DT lane; this is the production deploy). The superproject gitlinks on CLOUD and SITEZ move to the promoted
   commit only after that, one leg per fabric.

## 4. Calls for Andrew

| # | call | recommendation |
|---|---|---|
| C1 | Login fix: L1 now, L2 as a follow-up commit? | yes to both; L1 by the seat running the dev view |
| C2 | Does the portal freeze permit publishing named non-trunk branches (step 2) and landing integrated work on `DEV` (step 4), with no PROD promote and no gitlink move? | yes to step 2 now; step 4 after the overlap census and a clean typecheck/build |
| C3 | Order: laptop IRPT, then site-Z AMGT, POSN after round 5 closes, d13 by his choice | as written |
| C4 | Who executes each leg: each fabric's MSTR publishes its own refs; the integration merge by one seat; promote by DT via `/prod-deploy` | as written; the integration merge by the fabric with the larger delta (laptop) |

## Not measured, and why it matters

- Laptop-side refs, commit counts and paths are 0.0.0_AB_MSTR's measurement. They are not re-derived here and
  cannot be from this device.
- The login fix has not been exercised on site Z. L1's check is the test.
- Whether a laptop `.env.local` exists is unconfirmed (bus 7e1db614).
