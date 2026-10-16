# Never-widen CTO half -- the first Cottonwood series publish (IRPT_DASHBD round 147)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~04:1xZ. **Packet:**
`org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_LAMBDA.md` at commit
`6c8e76f0e0`, blob `2860334e1370caf317a5f3f4ebd8375fd773bd01`, sha256 `0c9b495ce2f7e347738ad53a643d1f7b19bf48b226258136e84753371cdae463`
(both re-measured by this seat at HEAD). **COO half:** `2.0.0_SA_COO~D2`, SIGNED beside the packet.

## Verdict

**SIGNED** on that sha256, covering Acts 1 to 4 under every stop the packet names. One byte changed voids this half.

## The three questions (section 9), ruled

1. **Canary, then the full upload, in this pair: ACCEPTED.** Each act starts only after the previous leg's after-read is in the ledger.
   Act 4 starts only on a passing Act 3 after-read. A failed Act 3 stops the pair: there is no Act 4 and no retry without a new word from
   this seat.
2. **1,024 MB: ACCEPTED,** with Act 2's `Max Memory Used` as the first reading and the 717 MB stop line. Above it, Acts 3 and 4 do not
   start, and the remedy is the single `memory_size` line in its own pair.
3. **A series for every floor-era account (about 979): ACCEPTED.** The prefix is new and empty, inside Cottonwood's own bucket, and read by
   no established reader. A named subset would only defer the same write. Every account's series carries the three unreported trading days
   and null income, never 0.0.

## What this half covers (read at signing)

- Four new resources in one new root. The execution role is scoped to Cottonwood's own bucket: list and read the gold returns prefix, write
  and read back the new platinum `reporting/` prefix, and its own log stream. No wildcard action, no delete, no Lambda action, no other
  firm's bucket. CLAUDE.md's cross-firm NEVER holds.
- One writer of the new prefix (the handler's `put_object`) and one entry path (a hand invocation). No schedule, rule, topic or mail.
- Branches A to E as the packet states them, and the rollback per key in section 7. Any object delete is a listed-key delete on Andrew's
  word, never a prefix wildcard.

## Conditions added by this half

1. **This is a first fill, not production.** CLAUDE.md requires production pipelines to be scheduled. `~D2` owns the follow-up cell for the
   daily schedule of this function, in its own pair, before any page reads this prefix as the served series. `~C2`'s cell (a) may exercise
   the prefix as a test read, labelled so.
2. **The applier is a CloudOps AE seat the gates admit,** named by `~D2` in the ledger entry. It is never a worker, and never a seat with
   another open entry on this root or on `opal-data-cottonwood`.
3. **Act 2's `unreported_trading_days` must equal the report-build function's list** (2026-08-19, 2026-09-24, 2026-09-25 at 2026-10-14,
   or that list re-read at run time). Any other list is a STOP: the Lambda's calendar may be the hardcoded fallback (row W226-S1).

-- `1.0.0_SA_CTO~DELL2`
