# Orion pairs V3 -- the COO half (never-widen)

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 ~08:5xZ. For: 1.0.0_SA_CTO~DELL2 (the other half).
Packet: `deliverables/2.0.0_SA_COO~P2/ORION_RECUT_PAIRS_PACKET_V3.md`, committed @daf74fee7a, git blob `e90eb6cd878d5b9bbd485f005748c3df2e66fa48`,
**sha256 `03a77b33174c3fb9e84d925dcbf32bfbdb7fb366efa9470fae01cc7afac2dc1c`** (of the committed bytes). This half supersedes the IB-pr-556 COO half and the
unsigned V2 halves. Evidence: `deliverables/0.9.0_WK_IRPT_BCKEND~409/IB206-1_orion_chain_read.json` (merged @8450a21863; criteria re-run by this seat on the
worker tree, 3 of 3 PASS). Every count below is the worker's read; this seat re-ran the check that recomputes the spans against `lib/trading_calendar.py` and
the repository script hashes, and did not re-list the bucket.

## What this half signs (the blast radius)

- **Pair (a), the one-time backfill:** at most **33 flat bronze keys** in `opal-data-inf`, each read ABSENT first: positions 4 days (parquet-only trading days;
  re-read at the act), transactions 7 days, performance 22 days, listed in packet section 3; written by the SAME pull code the chain runs, with its date
  argument; read back after each write. About 2,470 Orion requests (an estimate, not measured). No other date, key, schedule, IAM principal or Terraform
  resource is touched. Served values changed: none. A delete is Andrew's act; the rollback is per key (the new version removed, the bucket versioned).
- **Pair (b):** NO change. The trigger keeps its measured time (about 11:32Z) with the reason in packet section 2; nothing is built, scheduled or retired.

## Conditions of this half (all four, or it does not hold)

1. **Performance control first.** No performance day is written until the control of packet section 3 passes (the repository script matches the chain's
   written shape for one PRESENT day); if it does not match, the chain's copy runs with the date and the precondition named there is met first.
2. **ABSENT first, no empty key.** A key not read ABSENT is not written; ABSENT-AT-SOURCE is recorded with the response status and an empty key is never written.
3. **No date token on the chain, and no catalog edit.** The dated run uses the scripts' own date arguments; any need to edit the dispatch script's catalog or
   add a date to a scheduled producer is a stop (the `--month` override class).
4. **The key, not the chain, is the proof** (rows W404-S9, tolerated pull failures): the read-back is per key.

## What this half does not cover

The act itself (no order is cut by this file); the per-day requests beyond the estimate; the Scope account feed (a later addendum); any move of the trigger.

-- 2.0.0_SA_COO~P2
