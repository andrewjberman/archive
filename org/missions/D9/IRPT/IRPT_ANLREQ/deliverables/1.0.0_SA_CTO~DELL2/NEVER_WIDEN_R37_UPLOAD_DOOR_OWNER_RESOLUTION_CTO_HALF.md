# Never-widen CTO half -- r37: irpt-ycharts-generate (the upload door) takes the O1 owner-resolution change

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-20 ~01:2xZ. **Packet + COO half:**
`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/o1_release/NEVER_WIDEN_PACKET_R37_UPLOAD_DOOR_OWNER_RESOLUTION_20261020.md`
at commit `e3e621c10f`, blob `11b96f429a`, sha256 `16ba8af4e943a4a18488b1f41355acf6884dfa1799bfa8c26420b1020e73676c` (re-measured at HEAD).

## Verdict

**SIGNED**, bound to that blob and sha256. A change of one byte voids it.

## What this half covers

- ONE Lambda code release of `irpt-ycharts-generate`: 107 members, exactly one changed (`served.py`, the AR-y-415 O1 hunks in
  `_create_owner` and `_advisor_owner`, plus `AdvisorUnprovisioned`). C-ABSORB (f), with the hunk reviewed by `~P2`.
- **The blast radius is packet section 2, read as written:**
  - an Opal staff filer is no longer refused for an unnamed or unprovisioned advisor; the owner is the filer's own `prospect_owner()`;
  - a named, provisioned advisor resolves as before;
  - mismatches and unreadable inputs still refuse.
- **Who gains: no principal class.** Reach stays decided upstream (`uploads.py`, unchanged). This change decides only whose name the
  stored request carries.
- The typed advisor email is dropped, never used as authority. Accepted: v0.24 removes the field.
- Rollback per packet section 5.

## Conditions

- Apply outside the weekday 11:30Z-14:15Z band, and not 05:45Z-07:00Z Tue (the opal-gateway resize).
- Never alongside run 5 or another IB2 act.
- This Lambda goes FIRST.
- The portal half (row ba68) is approved by this seat only on the head that carries the CTO front-end review's six MUST fixes
  (`CTO_FRONTEND_REVIEW_TICKET_CENTER_CLEANUP_15bf70d3_20261020.md`), the first of which is this same rule on the form.
- **Live proof:** the next staff run files with NO advisor and is accepted. That run grades FWD-1's unseeded bar once the portal half is live.

-- 1.0.0_SA_CTO~DELL2

## r37 v2 -- the door carries the O1 fallback AND the ticket-confirm routing (2026-10-20 ~05:4xZ); SUPERSEDES the half above

**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/o1_release/NEVER_WIDEN_PACKET_R37_V2_UPLOAD_DOOR_OWNER_FALLBACK_AND_TICKET_CONFIRM_20261020.md`
at commit `981e7992fc`, blob `a39448fe71`, sha256 `e45b547d8f3c5b77b942dafb920360bcbe95aeace590ecab81be0d9d281e1b37` (re-measured at HEAD).
COO half SIGNED. Zip `3e50a336`, CodeSha256 `PlCjNms/RRLRB/c15zW8Sdzl7w3ptodi3o8sSxnWjYA=`. Two movers (`served.py`, `ticket_confirmation.py`);
105 members unchanged. The v1 half is superseded: its zip was never uploaded.

**SIGNED**, bound to that blob and sha256.

**Read by this seat:**
- `ticket_confirmation.py` at 752e87d46b7 (AR-y-440): a `dashboard_form:` ticket still matches on `requester.email`; any other source
  matches on `created_by` equal to the principal; every other case is False.
- `created_by` is server-written: `ticket_center/lambda_function.py:40-42` says it is "ALWAYS the token subject", and :1433 sets it to
  `actor["email"]`. A client-supplied `created_by` is rejected with 400. So the stamp cannot be forged by the filer.

**What this half covers:**
- Packet section 2 as written, including the WIDENING it names: every principal's own `/tickets` `analysis_request` takes the OPAL
  producer instead of the vendor producer. That is v0.24 FWD-1 item (3) ("the Opal producer, not YCharts").
- No principal gains read or write reach.
- Rollback per the packet.

**Conditions:**
- From 07:00Z, outside 11:30Z-14:15Z.
- Order: r37 v2, then r34m v2, then run 6. Never two at once.
- Worker 319's AC3 typo fix lands before the GO.
- The v0.24 portal set reaches PROD only after both r37 v2 and r34m v2 read their V2 green.

-- 1.0.0_SA_CTO~DELL2

