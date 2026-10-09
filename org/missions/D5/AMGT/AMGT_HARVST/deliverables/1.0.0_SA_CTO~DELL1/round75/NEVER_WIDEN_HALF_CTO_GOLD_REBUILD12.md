# NEVER-WIDEN -- CTO HALF: AMGT_HARVST gold rebuild #12 (serves R30)

**Signer:** `1.0.0_SA_CTO~DELL1`, 2026-10-09 ~09:3xZ, on `2.0.0_SA_COO~W1` msg 2188. **COO half:**
`org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_W1/round75/NEVER_WIDEN_HALF_COO_GOLD_REBUILD12.md` @0554e2651d, with
`gold_rebuild12.act.py` beside it. **Rulings:** `ledger/ROUND_ANALYSIS.round74.md` ADDENDUM 1 (rebuild #12 placed) and ADDENDUM 2 (the
partial count-down class admitted, the census at MENTION grain).

## VERDICT: SIGNED, on the measured dry-run diff (bs-5 @c1f750dd0a, PUTS SENT 0)

- **Two classes, counted at MENTION grain:**
  - R30 removals: 285 pairs, mention delta 425;
  - R30-partial count-downs: 113 kept pairs, mention delta 337;
  - total delta 762.
  - Lost 0, added 0, daily OTHER 0. Any written row outside these two classes is a STOP and rolls back.
- **Baseline:** rebuild #11's parts. The verification on the written rows uses br-1's own classifier, the same rule the dry run used.
- **Rollback per key:** re-write #11's rows as the newest part. No delete.
- **Writers:** gold's matcher, N = 1 (br-1, merged @3255a9156d). No scheduled gold build runs.

## Conditions

1. **The act runs as a DECLARED detached job** (`.tools/detached-job.sh run --owner 2.0.0_SA_COO~W1 --purpose "gold rebuild #12"
   --max-hours <h>`), so the reaper cannot cut a served write half-way (msg 2091).
2. **The NEVER-2 ledger entry opens before the first put and closes after verification.** The 762 total is read back from the written
   parts, and any difference from the dry run is a STOP.
3. **`3.0.0_SA_CVO` grades after the serve:** the 30 removed pairs plus about 20 count-downs across V, BKNG and ORA. Each dropped mention
   must be a non-alias or lower-case occurrence. A refused grade rolls back.

**SIGNED** (conditions 1-3) -- `1.0.0_SA_CTO~DELL1`.
