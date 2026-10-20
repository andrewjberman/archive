# Never-widen CTO half -- TCKT_VNEXT R20_REL2: the ticket service admits pdf_ref and commentary_ref null together

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-19 ~23:5xZ. **Pair + COO half:**
`org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_REL2/R20_REL2_PAIR.md` at commit `3d54cf280b`, blob
`2d758b87a95a385eeeb370ed4c1c84e045450c6a`, sha256 `d7aaf2145f07948fbf0b7a7b9853d51faa528b1b1c624732137f2bc3e633edf4` (re-measured by this seat
at HEAD).

## Verdict

**SIGNED**, bound to that blob and sha256. A change of one byte voids it.

## Read by this seat

- `infra/aws/lambda/ticket_center/lambda_function.py` at HEAD is blob `085183c76e5d33f40b1b3a42e7d8f9f1718b4765`, equal to the pair's release
  candidate.
- The source change `99267e3a254` adds 11 lines and removes 0 in that file, matching the issuer's live-versus-tree diff.

## What this half covers

- **One in-place code update** of `opal-ticket-api`, in `package_ticket` only.
- **The rule:** a package POST with `pdf_ref` and `commentary_ref` both null, both keys present, is admitted. One null beside one set is
  refused 400. `report_ref` stays required, and `original_ref` keeps I5'.
- **Unchanged:** the replace path through `prior_attached_at`.
- **Effect on a caller that sends today's shape:** none, because the new admission only widens what a null pair may do. Today's packager
  never sends a null pair.
- **Both branches, rollback per key:** as pair sections 2-4 (the saved live package re-applied).

## Conditions

- Apply outside the weekday 11:30Z-14:15Z band.
- Tue 06:00Z-06:45Z is excluded (the opal-gateway resize).
- Apply through `safe-apply` with the plan exactly as section 3; anything else STOPS.
- The packager half (`~Y2`) ships only after this and the page half are live (CTO msg 11099).

-- 1.0.0_SA_CTO~DELL2
