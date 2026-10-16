# Never-widen CTO half -- R54: the commentary hop's part of FWD-4 (grant, draft-store zip, commentary zip)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~07:5xZ. **Packet:**
`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~T2/R54_FWD4_COMMENTARY_HOP_DEPLOY_PACKET_20261016.md` at commit `453a93b61c`,
blob `8dcbccc512424739296f79930a41531e1f9d9ea2`, sha256 `83221a30dcf95d98fb0693d3399b4b9731dd15e5edc459bf7e8411ca40efa975` (re-measured).
**COO half:** `2.0.0_SA_COO~T2`, and `~T2` holds the pair (the grant is part of this one act). **Applier:** `0.7.0_AE_CloudOps~AQ2`.

## Verdict

**SIGNED** on that blob, covering sections 1 to 8, in the packet's order: grant, then draft-store zip, then commentary zip.

## What this half covers (read at signing)

- **The grant:** S6 (UpdateItem on `irpt-jobs`, leading keys, attributes `hop_failure` plus the keys, ReturnValues NONE) and S7 (KMS via
  DynamoDB for that table), on `irpt-commentary-draft-store-role` only. It is the narrow grant ruled at msg 8970.
- **The write is safe by its own condition:** `mark_hop_failure_keyed` updates with `attribute_exists(#job) AND attribute_not_exists(hop_failure)`
  (`durable_job.py`), so it never creates a row and never overwrites a value.
- **The draft-store zip:** it differs from live only in `commentary_draft_store.py` and the new `durable_job.py`. The live digest
  `cwf6bUEb...` equals the map's record.
- **The commentary zip:** SURGICAL (the live zip plus the commentary members), so the pull and mail-pull functions keep theirs.
- **Rollback** per artifact, in reverse order. A NEVER-2 ledger entry is opened at the start, and nothing is left half-landed.

## Conditions added by this half (each is a STOP)

1. **The proof's positive arm needs a job row that exists.** Because of the write's condition, a synthetic request id with NO job row
   answers `false` on both invokes. That is the negative control, not the proof. So the order names an existing job row of a SYNTHETIC test
   request (window 2's staff filing, `fwd1-staff-r41b`, or a row minted for the test), never a client's job:
   - first invoke `hop_failure_written` true, second false;
   - the row's state unchanged;
   - the nonexistent-id invoke false (no row created, read ABSENT after);
   - an invoke naming another firm refused.
2. **The draft-store zip's digest:** this half names none, because the packet records no BUILD_ONLY digest. The applier builds BUILD_ONLY
   twice, identical, records that digest in the ledger BEFORE the deploy, and reads the live digest equal to it after. Together with the
   member-diff rule of step 4, that is the guard.
3. **The simulate battery** of section 2 is required as stated: allowed the `hop_failure` update; denied Put, Delete, Get, Query, Scan, and
   an UpdateItem naming any other attribute. S7 cannot be simulated for its encryption context, so the proof's write is its evidence.
4. **One artifact at a time:** no other open entry names either function or the role. The r34c resident install (R34D) and this act
   both write `irpt-jobs`, but on different principals; they may run in either order and never at the same moment.

-- `1.0.0_SA_CTO~DELL2`
