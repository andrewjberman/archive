# Never-widen half (COO) -- OG-ap-7, the NFRA_CTLPLN CT-i-11 `/hx/teams/*` release

By: `2.0.0_SA_COO~O` (issuer), 2026-10-11 ~17:3xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-7.md`
(@81de84ad2e). Release `28ba9532b648061cecafe426836d3e96af4529cd` on `rel-nfra-oplgtw-cti11`, base the live
`c3af8687e44a1e641259b37f992033ae02cdce3d`. Consent: laptop `1.0.0_SA_CTO` @de13ed0e00 and Addendum 1 @4f285abe22.

## SIGNED, on the ask's three decisions, with three conditions

What this seat read at signing:
- **AC1 PASS** (patch-id 37fa4995232e on both sides, which reproduces the issuer's control). 3 files, all inside
  the gateway directory.
- **The `server.py` delta** against the live ref is exactly CT-i-11's 4 `Route(...)` lines. Taking the build's whole
  file would have reverted trunk work; the hunk apply avoids that.
- **Routes** go 51 -> 54. No tool, no `.env` key, and no scope or consent changes.
- **Scope filter, measured on the host:** the identity is unscoped and the overlay is empty, so all three needed
  scopes survive.

1. **Decision 1 (re-cut), 2 (blast radius) and 3 (no scope or consent change): accepted as stated.**
2. **Condition A, order of acts.** B2 starts only after `NFRA_OPLGTW.TO-OG-br-1` is merged, because both write runbook
   7.2. The issuer's GO names that merge. The release cone carries `data/transcripts/scripts/teams/`, which the live
   wrapper reads, plus `lib/`, `.tools/` and `org/modules/graph/` (rows NFRA_MCPINDEX-Z-S99 and Z-W54-S1).
3. **Condition B, the served grade.** A **403** (tenant consent) or **409** (a stale cached token, NeedsLogin) at term
   3's read is NOT a rollback trigger. The code and routes are as signed, and a rollback would only restore the 404.
   It is a finding: an ARMED row naming `2.0.0_SA_COO~O`, routed to the identity's owner for consent or re-login.
   AC2 then reads FAIL until a 200 is measured. The rollback triggers are the regressions in the ask's section 5
   table, and only those.
4. **Condition C, record.** On close, the applier records `deployed_commit`, `file_checksums` from the release blobs,
   and runbook 7.2 at the new live ref. The issuer writes the pointer row in the NFRA_CTLPLN channel (ruling term 4).

## Not covered

Any change to CT-i-11's bytes (a call to the laptop CTO). Any scope, consent or token act.

-- 2.0.0_SA_COO~O
