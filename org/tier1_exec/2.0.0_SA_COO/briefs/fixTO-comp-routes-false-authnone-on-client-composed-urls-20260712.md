# fix-TO: comp-routes/comp-pii FALSE `auth:NONE` on client-composed URLs -> report UNRESOLVED, never NONE

**`2.0.0_SA_COO`, 2026-07-12.** *comp-tool-effectiveness track (Andrew's #1). NON-URGENT but a REAL-GAP (a tool
asserting a posture it cannot determine) -> gets a fix-TO now, not parked. Routed per `1.0.0_SA_CTO` (`011547Z`),
who gates the fix. Grounded in the auth-integrity CLOSE package (`499cb50ef`) + the `getPlatinumAdvisorSummary` case.*

---

## THE GAP (a tool-honesty defect, same class as the false-assurance CTO fixed in `2094d30c9`, INVERTED)

`comp-routes` (and `comp-pii`, which consumes its route resolution) emits **`auth:NONE` / `S3-direct` / `BLANK
origin`** for `getPlatinumAdvisorSummary` -- a route whose upstream auth is **SOUND** (proven: exercised
`499cb50ef`, anon -> 401 at `auth-validator-edge`, pre-resource, on a real 168KB resource).

The `auth:NONE` is FALSE. Its true cause: the tool **cannot statically resolve** the route URL, because the URL is
**client-composed** at runtime -- `PLATINUM_BASE = '/api/scoped/advisor-intelligence/platinum'` + a template path
built in the FE adapter (`advisor-intelligence.ts:666-683`), never a static literal the tool can grep to a CF
behavior. Unable to map it, the tool defaults to `auth:NONE / blank-origin`.

**Why this is the same honesty class as `2094d30c9`:** that fix stopped comp-pii reporting CLEARTEXT as "hashed"
(false ASSURANCE). This is the INVERSE -- reporting a SOUND gate as "no auth" (false ALARM) -- but the identical
root: **a tool asserting a posture it cannot actually determine.** `auth:NONE` reads as "OPEN GATE." The truth is
"**UNRESOLVED** -- client-composed URL, cannot map to a CF behavior." A determinable-vs-undeterminable distinction
collapsed into a false determinate verdict.

**Why it matters (both directions):** this instance CRIED WOLF (drove a full audit to prove the gate sound). The
WORSE direction is symmetric -- a false `auth:NONE` on a route whose auth is genuinely absent would read identically,
so the tool cannot be trusted to flag a REAL open PII gate either. A verdict that is wrong when the gate is sound is
equally wrong when the gate is open; the tool's `auth:NONE` is **non-discriminating** on client-composed URLs.

## THE FIX (direction; owner scopes the implementation)

`comp-routes` must report a **statically-unresolvable / client-composed** route URL as **`UNRESOLVED` /
`CANNOT-DETERMINE`**, NEVER as `auth:NONE`. `comp-pii` (consumer) must surface the same -- an unresolved route is
NOT a no-auth route. Same "honest-when-you-cannot-determine" shape as `2094d30c9`'s cleartext-honest posture.

- Detect the client-composed / template-URL case (a base-constant + runtime-composed path; no static literal that
  maps to a CF behavior) and emit `UNRESOLVED` with the reason (`client-composed PLATINUM_BASE template`), not a
  default `auth:NONE`.
- Preserve a genuine `auth:NONE` for a route that IS statically resolvable to a behavior carrying no auth -- do NOT
  blanket-relabel everything `UNRESOLVED` (that would just move the dishonesty).

## EXIT CRITERION (CTO gates -- honest-UNRESOLVED, non-vacuous fixture)

- `comp-routes` emits `UNRESOLVED` (not `auth:NONE`) for the `getPlatinumAdvisorSummary` / client-composed
  `PLATINUM_BASE` case; `comp-pii` surfaces it as unresolved, not no-auth.
- **Non-vacuous fixture (mutation-proven, both directions):** (1) a client-composed URL yields `UNRESOLVED`, NOT
  `NONE` -- and a mutant that regresses it to `NONE` REDDENS; (2) a genuinely statically-resolvable open route
  still yields `NONE` -- so the fix discriminates, it does not blanket-relabel. (The negative control that proves
  the tool didn't just learn "always say UNRESOLVED.")
- CTO gates the fix like the other tool-honesty fixes.

## OWNER / PRIORITY / GROUNDING

- **Owner:** the `comp-routes` owner (comp-pii consumes it -- coordinate the consumer surface). *(COO to confirm
  the exact owner from the tools registry + route; hand dispatch to CTO/MSTR if the lane is unspawned.)*
- **Priority:** NON-URGENT (CTO). No security exposure -- the actual gate is SOUND (`499cb50ef`). This is a
  reporting-honesty correctness fix, not a broken-gate fire. But it is a REAL-GAP (Andrew's harness-vs-tool law:
  a TOOL not working correctly gets a fix-TO now, never a resting park) -- so it is opened, not deferred-indefinitely.
- **Grounding:** the auth-integrity CLOSE package `org/tier1_exec/2.0.0_SA_COO/briefs/auth-integrity-exercise-grounded-package-20260711.md`
  (`499cb50ef`) + the exercised `getPlatinumAdvisorSummary` case (anon 401, gate SOUND).

**Attribution:** finding surfaced by `2.0.0_SA_COO` + `0.4.0_DS_ClientPlatform` inside the auth-integrity close;
classified as a tool-honesty gap + routed by `1.0.0_SA_CTO` (`011547Z`); fix-TO authored by `2.0.0_SA_COO`.
