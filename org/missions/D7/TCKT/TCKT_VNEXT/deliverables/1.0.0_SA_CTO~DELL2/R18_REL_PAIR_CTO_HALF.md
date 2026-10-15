# TCKT_VNEXT round 18 -- the ticket service release (meeting route, trade-form routes, permission): CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-14 ~20:3xZ. **Bound to:** the COO half
`deliverables/2.0.0_SA_COO~V2/R18_REL/R18_REL_PAIR.md`, **blob `210f07d3c6`** (this seat's `git hash-object`; commit b1c51aa581). A different blob
voids this half.

**It rests on:** PRD v0.6 (FWD-10, FWD-11; C-TRADE-REQUEST, C-MEETING-REQUEST, C-ATTACH, C-FIRM-CHOICE), and Andrew-direct 2026-10-14
~17:3xZ and ~18:3xZ (Oct 24; dell2 keeps all three channels).

## Decided

1. **SIGNED: section 2 is the whole widening.** Three things are added:
   - two internal-only route families, the meeting act and the presigned trade-form PUT and GET (300 s, at most 10 MB, PDF/XLSX/CSV,
     after `_create_firm_allowed` and the read fence);
   - the `meeting_request` primary set to `jeanette@opalinvest.com` alone (this seat read her users PROFILE row, ~18:4xZ);
   - one role statement: Put and Get on the three firms' `ticket_attachments/trade-form/` prefix, from the builder, with no List and no
     Delete.
   No client login gains anything.
2. **The preconditions in section 3 are gates, as written.** The laptop's bucket policy and CORS read back first, under that ruling and
   its own pair: snake_case prefix, exact origins, no `*`. A Dell writes no bucket policy (C-DEPLOY).
3. **The plan in section 4 is exact. Any other resource or attribute is a STOP before apply.** Rollback goes per key, as in section 5.

## Conditions added

1. **The synthetic run (`TO-R18-RUN`) uses the coordinator window ruled in msg 7832.** A synthetic internal coordinator is the SOLE
   `meeting_request` primary for one run window if the create path mails the primary, so the test never mails Jeanette. Routing is read
   back before and restored to Jeanette after, and the identity is deleted and read ABSENT. That window is the RUN pair's widening, not
   this one.
2. **The prior routing (`manav@`, `alyssa@`) is recorded in the release result,** so a rollback restores it exactly.
3. **The portal candidate `dell2-20261014T202745Z-2131` is Opal-internal, as registered.** This seat read `portal/src/App.tsx`:
   `/ticket-center` is behind `ProtectedRoute requireInternal`, and the partner firm allowlist omits the path. The building box's CTO
   approves it here. It lands on DEV by `portal-merge-forward.sh`. PROD is a chosen-set promote after the release's `REL-OK` and the
   run's after-read.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `210f07d3c6`, covering both branches of COO section 4.

-- 1.0.0_SA_CTO~DELL2
