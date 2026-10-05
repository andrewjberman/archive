# DSGN_AMGTV1 -- ROUND 40 CLOSE (2.0.0_SA_COO~D, 2026-10-05 ~15:3xZ)

**Rectangle:** one direct act, `AV-zr-1`. It carries out Andrew-direct 2026-10-05 ~15:0xZ: Security Analysis is visible to every Opal employee
through `requireInternal`, with no Dev or admin gate. Record:
`org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20261005_150xZ_SECURITY_ANALYSIS_ALL_OPAL_EMPLOYEES_REQUIREINTERNAL_LEADPANEL_LOAD_TO_COO_Z.md`.

| step | evidence |
|---|---|
| issue | @807405bae0 (decomposition v40; check `round40/checks/access/access40.cjs`, 2 of 4 at base 71097b53, 4 of 4 on a scratch green copy) |
| worker ~102 | portal e6ab82ad (App.tsx +6/-9); access40 4/4; battery29 ALL PASS; proof VALID |
| drain | @793c52cb25 |
| CTO review | APPROVED @63c40d60af (msg 29642) |
| DEV push | MSTR~Z on Andrew's "push it" (record df1f9f8786): DEV 71097b53 -> e6ab82ad (msg 29643); CI run 37332239294 success (msg 29646). PROD untouched at c69b4747 |
| access40 on DEV e6ab82ad | 4 of 4 (the negative arm read after the push, msg 29641) |

## The one real run (live, localhost:5174 = portal DEV e6ab82ad, walker armed 15:24:51Z, disarmed 15:30:17Z)

`round37/walk/reads37.mjs --names "BA US"` -> `round37/walk/read-20261005T152449Z/` (READS 5: PASS 4, FAIL 1, ERROR 0).

- **The owed r39 dated end line (CTO msg 29614):** `fwd11-security-analysis-1440.png` ends "End of Security Analysis. Data as of October 2nd,
  2026." That is the served day with no invented clock. The same line appears on `fwd19-no-permission-security-analysis-page.png`.
- **The r40 access change, read live:** the `fwd19-no-permission` arm rewrites the walker's own `userType` to null in this browser only
  (a simulated non-Dev viewer). On DEV e6ab82ad the page renders: identity card true, no `[data-panel-state="no-permission"]`. The arm
  reports FAIL because it was written against the Dev gate that Andrew's ~15:0xZ word removed. Its FAIL is the expected inversion and is
  the evidence that a non-Dev Opal viewer reaches the page.
- **Ruling (issuer, inside its own decomposition):** the `fwd19-no-permission` arm of reads37 is RETIRED. It tests a gate that no longer
  exists. A future no-permission read targets a page that still carries a gate.
- **Not run:**
  - the non-ADMIN half live. The walker account is admin, and the simulation rewrites `userType` only. The admin removal is
    graded statically (access40 arms 1-2 on DEV).
  - a live walk as a non-admin, non-Dev Opal employee. It waits on an account Andrew grants (CTO msg 29642).
- **FWD-5 markers and own-first, and FWD-19 panels on BA US:** PASS (unchanged surfaces, re-read on the new head).

## Routed, not cut

The Lead Panel's slow chatter/price load went to `2.0.0_SA_COO~Z` (message 15:03Z), per Andrew: "make a note of this for COO~Z to pursue in
depth". DSGN changes no producer.

**Round 40: 1 of 1 orders terminal; 0 rows open.** Worktree `C:/tmp/wk-dsgn-amgtv1-102` and branches `wk-DSGN_AMGTV1-102` and
`dsgn-r40-zr1` remain; their removal waits on Andrew's word.
