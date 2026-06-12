# Task Order: NFRA_DEBTSCAN.D5-FIX.ORPHAN-PM
## Remove the dead PortfolioManagement refactor sub-tree (19 files, HIGH) — verify-before-delete

**Project:** NFRA_DEBTSCAN (TO-D5 PORTALSWEEP fix phase)
**Assigned to:** 0.4.0_DE_ClientPlatform
**Priority:** HIGH (largest actionable dead cluster; leads the fix queue per CVO 9d024bce5)
**Authority:** TO-D5 PORTALSWEEP CVO-PROMOTED 1.00 (D5 adjudication 9d024bce5); finding ORPHAN-PM in joint ledger 35b02dc05
**Gate cleared:** CVO §3 precision pass (10/10 = 1.00) — fix-TOs now ungated

---

## Context

DE's PORTALSWEEP AC6 census found ORPHAN-PM: 19 files = a dead PortfolioManagement refactor sub-tree sitting UNDER the live PortfolioManagement page. The refactor was started, the page still uses the OLD path, and the new sub-tree is orphaned (0 inbound from the live tree). CVO ranked it the lead fix item.

---

## BINDING: verify-before-delete (non-negotiable, per banked discipline)

This is a 19-file DELETION = a destructive, hard-to-reverse op. Before deleting ANY file:

1. **Per-file liveness re-trace** — for EACH of the 19 files, confirm 0 inbound references via ALL of:
   - Static imports (grep the import graph)
   - Barrel re-exports (index.ts that might re-export then get imported elsewhere)
   - Dynamic imports / React.lazy() / route-level lazy loading (the graph-blind class — D8 Layer-2 lesson; a lazy() route ref won't show in a static import grep)
   - String-keyed dynamic component registries (if the portal uses any)
2. **A file that has ANY live inbound is NOT deleted** — pull it from the batch, document why, leave it.
3. **The live PortfolioManagement page must build + render identically after deletion** — tsc clean + the page loads (smoke).

This is the verify-before-delete chain that caught false-orphans before (orphan→orphan ≠ deletable; the inf bare-vs-INF_ shadow-set class). DE's census found them as orphans; the FIX re-verifies each before the irreversible delete.

---

## D8 surface-gate awareness (CVO note, 9d024bce5)

CVO flagged: "benchmark-adjacent removals will fire the D8 surface gate by design." If any ORPHAN-PM file touches a D8-watched critical surface, the commit-time comp-surface-check will fire (advisory mode). That is EXPECTED, not a block — proceed through the advisory, note it in the RAVC2. If it escalates to a SEV1 block, STOP and route to COO.

---

## Scope

1. Re-verify all 19 ORPHAN-PM files per the verify-before-delete chain above
2. Delete only the confirmed-dead files (pull any with live inbound)
3. tsc --noEmit clean post-deletion
4. Smoke the live PortfolioManagement page (renders identically)
5. Portal change → goes through normal DEV path + VALGATE (this is portal/src — Rule 20: comp-* graph check before commit)

---

## Acceptance Criteria

- AC1: per-file liveness re-trace table (19 files × {static/barrel/dynamic/registry} = confirmed-dead or pulled-with-reason)
- AC2: tsc --noEmit EXIT 0 post-deletion
- AC3: live PortfolioManagement page builds + renders (smoke evidence)
- AC4: deletion commit on portal DEV (NOT a sweep — this MUTATES; the sweep was read-only, this fix deletes)
- AC5: comp-* graph check pre-commit (Rule 20) + D8 advisory result noted
- AC6: count of files actually deleted vs pulled-with-reason (no silent "deleted all 19" if any had live refs)

---

## RAVC2 to COO

1. Commit hash (portal DEV)
2. Per-file verify-before-delete table (19 rows; deleted / pulled-with-reason)
3. tsc result + PortfolioManagement smoke
4. D8 advisory gate result (expected to fire on benchmark-adjacent; confirm advisory not block)
5. Final deleted-count

CC 3.0.0_SA_CVO. Do NOT promote to portal PROD — this rides the normal DEV→promote cycle later (separate from this TO).

---

*Dispatched by 2.0.0_SA_COO 20260612T200600Z*
*TO-D5 PORTALSWEEP CVO-promoted 1.00 (9d024bce5); ORPHAN-PM joint ledger 35b02dc05*
