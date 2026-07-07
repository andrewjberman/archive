# NFRA_SILVERFRESH -- silver-dim freshness alarm (proposal)

**Author:** 0.4.0_DS_ClientPlatform~A | **2026-07-07** | **Status:** DRAFT -> RAVC COO -> CTO (COO-elevated)
**Origin:** ADVI_INFREF.REPOINT-COMPLETE geo diagnosis -- `silver/api_dims/household` silent-froze
**2026-04-28** and served stale geo for ~2 MONTHS before anyone noticed (surfaced only because the
repoint audit's completeness gate forced a per-consumer source-freshness check).

## The gap (why existing alarms MISS this class)
The freeze was invisible to every alarm we have because they watch the WRONG layer:
- **Producer-liveness / bronze alarms MISS it.** The upstream bronze KEPT FLOWING -- `bronze/orion-api/
  {date}/unified_account_dim.csv` is fresh through 07-06. A producer can PARTIALLY work (one output
  fresh, another output's build silently stops) -- so "is the pull alive?" answered YES while the
  household-geo silver dim was 2 months stale.
- **Gold/platinum freshness watch (D8) MISSES it.** It asserts the SERVED artifact is fresh -- but a
  served gold artifact reading a STALE silver dim is still "fresh" (it re-emits daily with stale
  inputs). Staleness one layer up is invisible to a served-output freshness check.
- **No alarm watches a SILVER DIM's OWN freshness vs its cadence.** That's the hole.

## The insight (COO/CTO-elevated)
**Watch the SILVER DIM's own latest-partition age against its expected cadence -- not the producer's
liveness, not the served output.** A daily-cadence silver dim whose newest partition is >N days old is
FROZEN, regardless of whether its producer is "alive" or its consumers still emit. This catches a build
that stops while its source flows (the exact 04-28 case) and a producer that partially-works.

## Proposal
A `comp-silverfresh` check + a scheduled CloudWatch alarm, per registered critical silver dim:
1. **Registry** (`org/modules/graph/silver-freshness-contracts.yaml`): each critical silver dim ->
   `{prefix, cadence_days, staleness_alarm_days, owner}`. Seed set (the dims served gold consumes):
   - `silver/api_dims/accounts_v2/` (daily, alarm >2d) -- the REST canonical
   - `silver/api_dims/household/` (daily, alarm >2d) -- **the one that froze**
   - `silver/api_dims/assets_v2/` (daily, alarm >2d)
   - `silver/accounts_dim/latest.parquet` (was daily; now DEPRECATED post-repoint -> either
     de-register or alarm to confirm it stays intentionally-frozen, not silently-relied-on)
   - `silver/transactions/` (daily, alarm >2d)
2. **Check:** newest partition's `snapshot_date` (or LastModified for `latest.parquet`) vs today;
   `age > staleness_alarm_days` -> ALARM (Namespace `Inflection/SilverFreshness`, dim=SilverDim,
   Reason=stale). Loud, per the WS-5 "loud half" doctrine.
3. **Schedule:** a daily EventBridge -> a tiny Lambda (or fold into an existing daily monitor) that
   evaluates the registry + emits per-dim staleness metrics + fires the alarm.
4. **Gate tie-in:** the ADVI_INFREF NFRA_GLDINV repoint-completeness invariant already asserts "no
   served D-script reads a frozen dim" at COMMIT time; NFRA_SILVERFRESH is the RUNTIME complement --
   it catches a dim that freezes AFTER the invariant passed (a live producer stopping), which a
   commit-time gate structurally cannot.

## Why it's the right durable (not a bigger hammer)
- It's the SAME fail-silent class as WS-1; the fix is a freshness CONTRACT per silver dim, cheaply
  evaluated (one head/list per dim/day).
- It does NOT require producer-side instrumentation (which we don't own for the dead geo pull) -- it
  observes the OUTPUT, so it works even for a producer we can't see.
- Bounded scope: only the silver dims that FEED served gold (the registry), not every silver key.

## Open / next
- The exact `comp-silverfresh` home (new tool vs extend `comp-freshness` with a `silver` subcommand --
  `comp-freshness` already has chain/script/artifact/ddb; a `silver` mode fits).
- Owner for the daily evaluator Lambda (DT/AE infra).
- RAVC COO -> CTO for the invariant-family placement (runtime complement to NFRA_GLDINV).
