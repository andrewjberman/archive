# DSGN_AMGTV1 -- ROUND 42 CLOSE (2.0.0_SA_COO~D, 2026-10-05 ~17:1xZ)

**Rectangle:** CTO countersign @f5d6919117, ROUND 42 items 1-3, plus item 4 as Andrew re-set it ~16:3xZ (record
`org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20261005_163xZ_SECURITY_ANALYSIS_NO_NO_PERMISSION_SCREEN_SIDEBAR_INVISIBLE_FOR_NON_OPAL.md`).
Item 4 means: no "no permission" screen; a non-Opal viewer sees no Security Analysis sidebar item; no route, redirect or backend work.
**Parity hold** (MSTR~Z msg 29688): every commit of this round sits on branch `wk-DSGN_AMGTV1-r42-issue` and drains to CLOUD at PARITY
CLOSED.

| step | evidence |
|---|---|
| issue | @96f917ca3c (decomposition v42; `round42/checks/r42/r42.cjs` 2 of 5 at base e6ab82ad, 5 of 5 on scratch reference edits) |
| worker ~103 (`AV-zt-1`) | portal 1135984d (HeaderCards.tsx + ExecManagementTab.tsx, +43/-7); r42 5/5; battery29 ALL PASS; proof VALID |
| drain (onto the round-42 branch) | @cc9daff4f5 |
| issuer read (`AV-zt-R`) | `round42/walk/reads42.mjs` -> `read-20261005T165842Z/` @989403dabf |
| CTO review | APPROVED (msg 29719; the CTO's record commits after PARITY CLOSED) |
| DEV push | owed: MSTR~Z on Andrew's word. PROD held (Andrew-direct 15:5xZ, @645602063f) |

## The one real run (live, localhost:5174 = candidate 1135984d, walker armed 16:58Z, DISARMED 17:00:30Z)

- **sidebar-opal-control PASS:** the walker as itself (opal-capital) on /market has 34 sidebar links, 2 of them to /security-analysis
  (the probe sees the item when it is there).
- **sidebar-non-opal PASS:** `firmId` was rewritten to `inflection` in 2 of the walker's own auth responses, in this browser only. On
  /market the sidebar has 14 links, 0 of them to /security-analysis, and no "Security Analysis" text. This is Andrew's item-4 read.
- **rog-header FAIL (producer):** ROG SW shows 3 tiles and 0 reasons. The page renders a served reason (r42 arm 1). The CTO's diagnosis
  (msg 29719): `_header_figures` adds reasoned nulls only when a stored model block exists ("no stored block still serves []"). That is
  a RESAPP round-72 cell; FWD-4 completes when it lands, with no page change.

## Grades moved by this round (for the next countersign)

- **FWD-13:** the full-precision value is in the tooltip, formatted (r42 arm 2). Expected REALIZED on DEV after the push.
- **FWD-19:** Andrew's sidebar read passes, and the other states were already REALIZED on every panel in round 41. Expected REALIZED.
- **FWD-27:** the Exec "yet:" run-on is fixed. The served vendor names and the Model vendor line remain RESAPP's, so FWD-27 stays
  NOT_REALIZED.
- **FWD-4:** stays NOT_REALIZED until the producer serves reasons for blockless names.

**Round 42: 1 of 1 orders terminal; 0 rows open.** Worktrees `C:/tmp/wk-dsgn-amgtv1-103` and `C:/tmp/wk-dsgn-amgtv1-r42i` remain;
their removal waits on Andrew's word, after the round-42 branch drains.
