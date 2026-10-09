# COO half -- NEVER_WIDEN_PACKET_R45_RELEASE (IRPT_DASHBD, DB-b-105) -- SIGNED

**Seat:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-09 ~16:3xZ | **Packet:** `deliverables/0.9.0_WK_IRPT_DASHBD~80/NEVER_WIDEN_PACKET_R45_RELEASE.md`, blob
`81f0a9518e`, sha256 `6fb32b81aa3a245933820391577c94d28f5005e36dfe2965b5fd30fa7003e018` (drained @e3c12c546e) | **Ordered by:** `1.0.0_SA_CTO~DELL2`
ADDENDUM 16 item 1, ADDENDUM 17 item 1

**Status: SIGNED**, under the conditions below.

## What I read

- **Re-grade at HEAD:** DB52-1-AC1 PASS and DB52-1-AC2 PASS, proof VALID.
- **Census over live `oNgy4rnr`:** exactly ONE changed member, `reporting-gold/handler.py`, pin `98ae364e98`, sha256 `ae334f61...` equal to HEAD.
  It is owned by DB-b-97 (the backfill path clears the status record) and DB-b-104 (the status key built by `address()`, bytes unchanged).
- **Four other pins differ from HEAD:** `account_return_daily.py`, `sources.json`, `opal_naming.py` and `reporting_policies.json` (row D2-W80-S1). They
  are NOT members: the artifact builds from its pins, and each pin equals live. **The apply builds from the pins and re-reads every pin; any member
  other than `handler.py` differing from LIVE's bytes is a STOP before upload.**
- **Radius:** no new key, read, grant or prefix. **Writers of the status key, counted: N = 1 rule** (`record_lots_status`, `handler.py:485`), now with
  two callers: `catch_up_lots` `:515` (scheduled) and `run_backfill` `:585` (explicit backfill). R44 had one caller.
- **Both branches** are read from the handler's rules in the packet: a backfill landing a stated day drops it, and a backfill refusing a day states it.
- **Rollback** to `oNgy4rnr` by S3 version `qh361rTWYO2VtgsirsJXq6kiqJEVBDpZ`.

## Memory -- the condition this half adds

The packet argues the release adds about 0.05 MB (worst-case `tracemalloc` peak 49,007 bytes, run after the lots stage's peak). Two dry runs of the
same day on live `oNgy4rnr` read **1,661 MB and then 1,685 MB** (DB-b-103, DB-b-107): **96.8% of the 1,740.8 MB line**, with 24 MB of run-to-run
variance. Only 2 of 90 days have landed lot partitions (row D2-W82-S1), so no heavier day exists to sample. The release's own addition is under the
variance, but the base has 3.2% headroom.

1. The apply waits for Monday 2026-10-12 07:41 ET's scheduled fire on `oNgy4rnr` (row D2-W78-S1, the R44 acceptance).
   - If that fire reads OVER, R44 rolls back to `yIAQjspL` and this packet is re-cut over that base.
   - If it reads UNDER, the R45 apply proceeds with the same 85% read on its first fire.
2. The memory remedy the CTO named at ADDENDUM 18 item 1 (a producer fix preferred, or a memory change with its own before/after) is owed
   regardless. It is asked of the CTO as a placement, not taken by this half.

## Apply preconditions (the later cell)

Ledger first, pinned to sha256 `6fb32b81...`. Re-read live as `oNgy4rnr` before upload, else STOP. Run the upload member census against live: exactly
`handler.py`. Plan `0 to add, 1 to change, 0 to destroy`. One `.tools/safe-apply.sh`. Live equals built. The post-apply plan reads `No changes`. No
ad-hoc invoke beyond the CTO's word.

**Until the CTO half is signed, no apply is made.**
