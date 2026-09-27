# NFRA_MCPORTAL -- next-round enrichment, PRE-DRAFT: C6 (tiers and tool lists in the grant table)

**Owner:** `1.0.0_SA_CTO~O`, under the ~O self-drive (arming record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260926_03xxZ_SELF_DRIVE_O_FABRIC.md` @56050d290d).
**Status:** DRAFT, not the analysis. The round-2 L10 analysis adopts, amends or drops it after `3.0.0_SA_CVO~O`'s slug.
It exists so C6 is cut the tick both of its conditions hold, not a round later.

## Why now
- PRD C6 (`prd/NFRA_MCPORTAL_PRD.md` lines 219-230) was gated on **G-OPLGTW**, Andrew's word on amending NFRA_OPLGTW's
  contract and adapter. Andrew gave it on 2026-09-26 ~02:2xZ, "On call 5, lift fully"
  (`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260926_022xZ_CTO_O_OPEN_CALLS_1_TO_6_ANSWERED.md`,
  call 5 named "the gateway move and MCPORTAL C6").
- **The second condition is MET since 2026-09-27 ~12:4xZ** (OPLGTW re-seated to ~O on Andrew's "recs approved", record
  @6fba157e76). What follows is the condition as it stood before: ~~The second condition is NOT met.~~ C6 edits NFRA_OPLGTW's contract file, whose CTO leg is `1.0.0_SA_CTO~A`.
  `3.0.0_SA_CVO~O`'s verdict @e470835e7c: no CTO or CVO act on OPLGTW issues from ~O until a re-seat record moves
  `leads.cto` and `leads.cvo`. The release was asked of the laptop through `0.0.0_AB_MSTR~Z` (msg
  20260926T045815Z). **Cut C6 only after that re-seat lands.**

## The cell, as it would be cut (one build cell, then its release)
1. **Contract amendment** (the CTO's own act, after the re-seat): add `access_tier` and `tool_list` to
   `state_store.record_types` in `org/standards/NFRA_OPLGTW_CONTRACT.json`. Today that list holds 9 types:
   principal_profile, data_entitlement, oauth_client, oauth_code, oauth_refresh_family, download_ticket,
   catalog_snapshot, oauth_pending_authorization, operator_audit (read 2026-09-26 ~08:0xZ).
2. **Adapter + port** (a COO cell, `<risk>SERVED</risk>`): the same two types in `POLICY_RECORD_TYPES`
   (`app/access_state.py`). The enforcement path reads the tier and the tool list from the table with a strong read per
   call. The flat files for tiers and tool lists stop being read in the SAME release. The kill switch, blocklist and
   revoked tokens stay files (C6). Criteria, at most three:
   - a changed tool list is enforced on the next call, driven deliberately against the release, with the unchanged
     person as the negative arm;
   - the release reads no tier or tool-list file (census of the file reads on the released tree);
   - with DynamoDB unreachable, the kill switch and blocklist still refuse (the files still work).
3. **Writer + tab:** the grant writer (MP-a-1) gains the two record types, so the Entitlements tab changes them.
4. **Release:** one narrow gateway release from the manifest base (@75117e60d6), announced by the one deployer, under
   a never-widen sign-off, because the change moves what every caller is allowed.

## Not in this draft
- FWD-10's call log and person or server stop: round 1's analysis already rules they use the FILES and do not wait on
  G-OPLGTW.
- The OPLGTW walkthrough orders OG-v-4 and OG-v-5: they are OPLGTW's own, behind their own gates.
