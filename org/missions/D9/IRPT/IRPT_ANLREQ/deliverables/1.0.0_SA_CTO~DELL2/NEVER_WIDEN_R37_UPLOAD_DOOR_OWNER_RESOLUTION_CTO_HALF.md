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
