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

## R-2 (2026-09-25 ~16:2xZ) -- the two reads came back (MX-q-2 @d9db4d7395): input to the round-2 analysis

**Measured by the round-2 read cell** (drain @e9cb3d257a):
- **Eclipse (C-S12):** 5 distinct rep ids in live silver, 0 outside the Inflection allowlist.
- **Black Diamond (C-S13):** 14,367 of 3,185,260 silver transaction rows since 2026-04-14 carry a null cusip (about
  0.45%), and 1 of 3 served figures that join on cusip already carries nulls.

**Ruled here so the round-2 analysis inherits it:**
1. **Eclipse:** single tenancy is RECORDED with this read as its evidence, and C-S12's gate is lifted. An Eclipse tool
   may be cut. Every Eclipse tool still carries a firm-scope assertion that FAILS LOUD if a rep id outside the
   allowlist ever appears, because single tenancy is a measured fact about today, not a guarantee.
2. **Black Diamond:** R-2 (3)'s gate is lifted WITH DISCLOSURE. A Black Diamond tool that answers by cusip states, in
   its answer, how many of the rows it read had no cusip and that they were excluded. It never silently drops them or
   shows a partial sum as whole.
3. **The served figure with nulls is a live defect, not a tool question.** It is routed with C-S13 (2), the unscheduled
   bridge builder, to the Black Diamond pipeline's DS owner. It is parked with that owner until a DS seat is live. The
   round-2 analysis names which served figure it is.

## R-3 (2026-09-25 ~20:2xZ) -- ruling D-4 (2.0.0_SA_COO~O msg 25916): the portal tools read the legacy served keys under LEGACY-READ waivers

**Asked** (`org/tier1_exec/2.0.0_SA_COO~O/deliverables/ROUND1_DECISIONS_ASKED_20260925.md` @626067831a, D-4):
- MX-t-8's 10 portal tools read the objects the portal serves today in `opal-data-portal-v2`:
  `platinum/mdpf/{scope}/*.json`, `platinum/etfs/positioning_data.json` and `platinum/advi/49financial/*.json`;
- those objects exist ONLY at those legacy keys, and `address()`'s canonical keys are absent from the bucket;
- the naming gate refuses 19 literals, and its one waiver is a per-literal, per-call-site LEGACY-READ entry under a CTO
  authority record.

**Ruling: (a).** The authority record is `LEGACY_READ_AUTHORITY_MX-t-8_20260925.md`, beside this file.
- **Why (a):** C5 (portal parity) and Andrew's answer 5 ("There are precomputed tables for the Portal that we're
  already pointing at") REQUIRE the tools to read the SAME objects the portal reads. The canonical keys hold nothing.
  A read of a live legacy key is not a mint, and moving those keys is MDPF_CANON's migration, not a rider here. This is
  exactly the case the waiver exists for, and IRPT-M-LEGACY-READ-01 is the precedent.
- **Why not (b):** an R20 departure is for a NEW name that departs from the canon. Nothing is named here; a live key
  is read. **Why not (c):** it would be a wait on another directive's migration.
