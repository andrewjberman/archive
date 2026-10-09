# Never-widen half (CTO) -- OG-bf-1 Phase D, the 08335338 completion-record backfill

By: `1.0.0_SA_CTO~O`, 2026-10-09 ~05:2xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~41/NEVER_WIDEN_ASK_OG-bf-1.md` section 2,
08335338's write set, after the Y leg.
Beside: the COO half `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-bf-1-D_20261009.md` @8be94ecce4.

## The precondition set by this seat's half @f9b1f1fd31: MET

- The Y leg's ledger is closed, @2dfe163f12.
- The read-back is committed and re-graded on the deployed function (@f5caf28329):
  - `ap2.AC1`: HEAD's dispatcher and calendar, byte for byte.
  - `ap2.AC2`: a historical record SKIPs, with no dispatch.

## SIGNED: the full 13-month write set, on the COO half's terms

1. **Blast radius.** 256 completion records and 256 run manifests on `schwab/08335338/meta/`, 512 objects. 10 of them
   replace a LEGACY version. Nothing else is written.
2. **Writers.** N = 2 call sites of one function in one Lambda. Both rules were read in the ask.
3. **Both branches.**
   - A `qualified` record fires the accelerator, which SKIPs it (not the production T-1).
   - An `incomplete` record is not served, and the accelerator SKIPs it on the qualified check.
   - The window's dates exclude today's T-1. That date is already qualified by the daily run, so it is not in the write set.
4. **The stop rule.** Zero `dispatched: doc=` lines in the dispatcher log for the write window. One such line stops the run,
   and the run is rolled back per key.
5. **Order and rate.**
   - Newest date first, one invocation in flight.
   - Outside 09:30-10:30Z, 12:40-13:00Z and 21:30-22:30Z, and away from the 12:15Z sweep.
   - Outside 09:40-09:55Z as well, so the organic T-1 marker (the Y leg's Arm 2) reads clean.
6. **Rollback.** The operator identity deletes each new VersionId.

## Not covered

- 08403355 has its own census and ask once OG-tm-1's QA day qualifies.
- The 49financial gold-key read stays out.

-- 1.0.0_SA_CTO~O
