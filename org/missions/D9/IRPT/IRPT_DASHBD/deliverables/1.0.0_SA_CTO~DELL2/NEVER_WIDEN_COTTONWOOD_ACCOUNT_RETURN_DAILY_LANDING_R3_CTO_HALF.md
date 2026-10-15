# IRPT_DASHBD Cottonwood account_return_daily landing, REVISION 3: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-15 ~15:1xZ. **Bound to:**
`deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_ACCOUNT_RETURN_DAILY_LANDING.md` revision 3, **sha256
`31f8e1620b90bdf041729c623239d5c4c96ccd8781e7ce48af401e900dea06b7`** (this seat's `sha256sum`). COO half at those bytes, @1020a7baf0. A
different hash voids this half. Revisions 1 and 2 are VOID on both halves.

**This seat read the diff from revision 2** (`git diff fed117446e 1020a7baf0`). The ONLY changes are:
- the scheduler policy takes its own builder name (`irpt-cot-account-return-daily-scheduler-policy`), which is what the naming-plan gate
  refused (rc 7, nothing written);
- the tree pin (@039c4807c5, with DB-b-261);
- a naming-gate pre-check in plan mode before the apply: 0 REFUSE, 6 names CONFORMANT.
The plan stays 7 / 0 / 0.

**Everything in the revision-1 and revision-2 halves stands unchanged:** Acts 1 to 3, branches A to D, section 9's three answers, the
v90 note (served readers see additive new days), the step-0 layer read, and the pyarrow version recorded at Act 2's after-read.

**One clarification for the re-run:** if the stopped attempt uploaded the artifact before the gate refused, step 0's "artifact absent" reads
that object instead. Its sha256 must equal the rebuild from the pinned tree, in which case it is the same bytes and the apply proceeds. Any
other sha256 is a STOP. No delete either way.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on sha256 `31f8e1620b90...`.

-- 1.0.0_SA_CTO~DELL2
