# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-44 (round-43 tenth batched release: the access-log repair, Z-S395)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED on the ask's sections 1-8**, 2026-10-18 ~19:0xZ.

**Bound to:**
- ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-44.md`, sha256
  `29959e4b1fee93bf47bcc35f087c94969e9ebc3fbdc516f979daa80388764797` (re-hashed at signing);
- release `eff517546eeea48811cf13f3de38926c5944c6df` on live `a0c83303ee48c95c16a61c0d5e8bd186b1083b66`.

## What I measured myself

- `git log -1 eff517546e`: its parent is `a0c83303ee`, the live ref.
- `git diff --stat a0c83303ee eff517546e`: 2 files, +142/-2 (`probe_listener.py` and a new test `test_og_pr5.py`).
- At the release, `harvest_research` 845a3416, `harvest_figures` 98bceb90, `harvest_identity` f5bc0b80, `harvest_keys` 25b44841 and
  `graph.py` 93c42279 are all equal to live.
- **The `probe_listener.py` diff:** the four `uvicorn*` loggers (level, handlers, propagate, disabled, filters) are snapshotted
  before the probe's `uvicorn.Config` is built and restored in a `finally`, so the service's access log is no longer silenced. This
  is the repair I ruled (msg 35769), done at the cause.

## Accepted

- **Nothing widens.** The service's own access lines come back.
- **Z-S397 as amended by the COO (A1):** the listener's own requests now also write access lines. They are counted separately, and
  the count must equal the probe requests made, which is 0 in this order because there is no arming.

## Conditions of this half

- **CT1 (base):** a live marker other than a0c83303ee at Phase B is a STOP and a re-cut.
- **CT2 (carried files):** Phase B prints the host md5 of the four dell1 harvest files and `graph.py` beside the release's. Any
  mismatch is a rollback.
- **CT3 (the repair, measured on two sources):** over the 30-minute read-back, the journal's POST /mcp line count and the audit
  lake's record count for the same window are both printed.
  - The journal must be non-zero whenever the audit lake is.
  - A journal reading 0 against a non-zero audit lake is a FAIL, not a quiet window.
  - This is the second source my earlier halves lacked; Z-S395 shows what that cost.
- **CT4 (at rest):** no lease through the close; a 200 from `/probe/` is a rollback trigger, as before.
