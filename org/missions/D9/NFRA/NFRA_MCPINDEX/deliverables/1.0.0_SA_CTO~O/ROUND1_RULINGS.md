# NFRA_MCPINDEX -- round-1 rulings by the program's CTO lane

**Owner:** `1.0.0_SA_CTO~O` (the ~O fabric holds NFRA_MCPINDEX since the re-seat @23bbeff325). They enter the round-1
analysis. **Append-only.**

## R-1 (2026-09-25 ~05:3xZ) -- ruling D-3 (2.0.0_SA_COO~O msg on MX-c-4): supersede as cut, and split the 14 by owner

**Asked** (`org/tier1_exec/2.0.0_SA_COO~O/deliverables/ROUND1_DECISIONS_ASKED_20260925.md` D-3): under the amended
two-limb AC11, MX-c-4 still FAILS. `destructive_ops.classify` fails 14 of 49 registered tools: 9 ycharts, opal_portal
and globgrph tools, and 5 schwab tools whose own `integration.py` declares no per-tool class. That is pre-existing,
because AC6 shows 0 of 49 changed class. The fix lives in four integration directories outside the order's `<paths>`.

**Ruling:**
1. **MX-c-4 is SUPERSEDED as cut**, citing this ruling. It cannot complete without a grant it does not hold. Its build
   (branch `wk-nfra_mcpindex-1-1d`, @119a49eef0 / @7e1347ee8c) is the BASE of the re-cut cell, and it is carried, not
   rebuilt.
2. **The re-cut cell** (MCPINDEX round 2) is granted the ycharts, opal_portal and globgrph integration directories and
   declares per-tool classes for those **9** tools. It drains the held branch with them, so `read_teams_attachment`'s
   SAFE change ships with the classifications. It is released NARROW, under the same rule as NFRA_OPALAI @592e319a06.
   The CVO grades MX-c-4's AC8 judgment at that cell's L9.
3. **The 5 schwab tools are HELD, not cut.**
   - `app/integrations/schwab/` is NFRA_OPLGTW's code, and that project is under Andrew's 2026-09-22 stop ("do not go
     further with it").
   - The tools are registered but NOT enabled (Act 2 was never switched on), so an unclassified schwab tool is not
     reachable. The hold carries no live exposure.
   - AC11's denominator in the re-cut is **49**, graded as **44 classified + 5 HELD (G-OPLGTW)**. It is never "44 of
     44": the five stay in the count, labelled with why.
   - They join the same Andrew call as G-MOVE and G-OPLGTW.
4. **The interpreter pin** (row W1-S6: `py -3.12` against a box that registers only 3.11) is the issuer's own amend,
   to a device-neutral interpreter. It is noted here only so the re-cut does not inherit the pin.
5. **Why not all 14 in one cell:** the cell would write into a stopped project's integration. That is Andrew's word
   to give, not this lane's to assume.
