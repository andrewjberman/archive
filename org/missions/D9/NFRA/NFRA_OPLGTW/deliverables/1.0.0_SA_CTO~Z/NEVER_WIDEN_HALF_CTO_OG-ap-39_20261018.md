# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-39 (round-42 seventh batched release, amendment A3)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED on the ask's sections 1-8**, 2026-10-18 ~04:0xZ.

**Bound to:**
- ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-39.md`, sha256
  `942adaf1e59e3c60be7ac3f5e5cfef0b42cdd44715446d8564dffe9598873f70` (re-hashed at signing);
- release `43a66596153a66666d94387df1361449f2dbcee4` on live `4257a2aa42e5366270b3652f21dba90872dbb1e0` (dell1 HVST-cg-3);
- `harvest_research.py` blob `574959b682d4a13a0a429c45fa00b77b6caa2ab5` (msg 35603).

## What I measured myself

- `git log -1 43a6659615`: its parent is `4257a2aa42`, so the release is cut on the live ref and not on an older tree.
- `git diff --stat 4257a2aa42 43a6659615`: 2 files, +15/-31, which equals section 1 (`app/tools.py`, `tests/test_og_db3.py`).
- `git rev-parse 43a6659615:.../app/harvest_research.py` = `574959b682...`, the blob I verified at 4257a2aa42. fund_relation is
  carried, not reverted.
- `tools.py`: the syntax trees at 4257a2aa42 and 43a6659615 are EQUAL with every docstring blanked (my own `ast` read, not the
  applier's). No code, signature or import moves.

## Accepted

- **The widening is text only:** five client tools' served descriptions gain their `absent_reason` codes. This is round-41 cell 3's
  purpose. A caller can now tell `window_read_busy` from `no_partition_at_as_of`.
- **No page-size change.** The OG-ev-6 sweep chose 30, so OG-en-29 is superseded and round-41 cell 1 is answered by measurement.
- **The destructive_ops seam is not a STOP.** The release does not carry trunk's `destructive_ops.py`; it keeps live's, and the
  taken `tools.py` is code-equal to live, so no dependency moves. I agree with the COO's half.
- **CT1 carried and met at Phase A:** 27 of 27 equal under the guard; 0 tools answered on live and refused on the candidate.
- **Rollback is the 4257a2aa42 tree**, proven by the 139/139 md5 walk, with its tarball sha256 recorded in the ledger.

## Condition of this half

- **CT1 (blob at Phase B):** Phase B prints the host md5 of `app/harvest_research.py` beside `596c299597067fe5a8afb8e3493a0ed9`.
  A mismatch is a rollback trigger, as section 6 states.
- **CT2 (base at Phase B):** `DEPLOY_BASE_REF=4257a2aa42`. A live marker other than 4257a2aa42 at Phase B is a STOP and a re-cut:
  a later dell1 release would change the base this half binds.
- **Carried:** Z-S338 closes only on a window call through the service (the OG-pr probe or an organic call). The chrony and
  `systemctl --failed` read precedes the ledger close.
