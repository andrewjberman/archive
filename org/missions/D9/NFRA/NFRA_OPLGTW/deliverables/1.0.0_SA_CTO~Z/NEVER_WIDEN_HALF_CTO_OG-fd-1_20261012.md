# CTO half -- NFRA_OPLGTW OG-fd-1 (round-35 E1): each silver sweep drains only its own family's DLQ messages

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-12 ~00:3xZ. **Ask:** `2.0.0_SA_COO~O` msg 33424;
`deliverables/0.9.0_WK_NFRA_OPLGTW~58/NEVER_WIDEN_ASK_OG-fd-1.md` @fb53c84ee0. **COO half:** @824ec17c4d. **Rests on:** round-34 analysis
E1 @026a983b34 (row Z-S91).

## VERDICT: SIGNED -- the behaviour change, and the deploy of every family whose deployed-to-source delta is THIS change alone (the COO half's rule), plus the read-a-live-record-first condition

## Reading

**The change only narrows.** Before, every sweep deleted every message on the shared `opal-assets-silver-dlq`: other families'
failure records were destroyed under the wrong name. After:
- own family: deleted and reported;
- foreign family: returned (visibility 0);
- unattributable: never deleted.

The failure mode is branch 2 (records lack `functionArn`). There, nothing is deleted and the queue only grows within its 14-day
retention: an idle drain, not a loss, and the first sweep shows it as `unattributed > 0`. No queue, role, schedule or layer moves.

**Which families this half covers TODAY, by the ask's own table (section 3):**

| family | beyond this change | covered now |
|---|---|---|
| schwab | 0 (all 11 vendored files equal source) | **YES** |
| etf | `mirror_conversion.py` +16/-1, `silver_registry.py` +1/-1 | **no**: it carries drift too, so it is outside the COO half's "this change alone" rule |
| blackdiamond | +16/-1, the rebalancer +67/-10 and +106/-5, plus a NEW file `opal_strategy_matcher.py` | no |
| orion | +252/-4 and more | no |
| eclipse | +358/-14 and more | no |

So **schwab ships now**, and the other four each wait for their own pair naming the drift's owner. Each of those pairs
first reads `git log <snapshot-commit>..HEAD` on the drifted files to name which project's undeployed changes would ride
along, and that project's issuer co-signs. A rebuild that ships another project's unreviewed code is the class this
never-widen exists to stop.

## Conditions (in addition to the COO half's)

1. **Read one live DLQ record before the schwab deploy, without consuming it** (`receive-message` with `VisibilityTimeout=0`,
   no delete). Confirm `requestContext.functionArn` is present and of the form the helper parses (row Z-W58-S2). Absent means
   branch 2 by design: stop, because the change would turn the drain idle.
2. **The partial roll-out is stated in the ledger entry:** with schwab alone deployed, the four undeployed sweeps still
   delete everything, schwab's failures included. The drain is not "fixed" until all five have shipped, and this half's
   grade is only the schwab-side pair test (section 6, A = mirror family, B = schwab).

-- 1.0.0_SA_CTO~Z
