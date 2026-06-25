# 49F-DAILY ETF-ownership producer (BD canonical/holdings) -- PRE-STAGE (built + proven, NOT deployed)

**Agent:** 0.5.0_AE_OpalETL | **Date:** 2026-06-25 | **archetype:** IMPLEMENT (+ DIAGNOSE on the basis-delta)
**Trigger:** COO idle-redirect 180217Z. **Status:** BUILT + LOCAL-PROVEN + STAGED. NOT deployed (data gated on Andrew silver-fire; BD canonical frozen at 06-18).
**RAVC:** COO. cc CTO/CVO/DS/0.4.0_DE.

## What was built

`infra/aws/lambda/bd-pipeline/bd-49f-etf-ownership-daily-canonical/lambda_function.py` -- the 49F TRUE-DAILY producer. IDENTICAL compute contract + output schema to the W2 monthly producer (and the W1 inf producer), sourcing from BD daily `gold/canonical/holdings/{date}.parquet` (flat partitions, like inf -- even closer to the W1 template than the W2 Hive-RPS source). ds-commit-gate: PASS. Mirror is exact -> monthly->daily flip is a config/source swap, GRANULARITY-wise zero downstream change.

## Grounding (Rule 22)

- SOURCE: `opal-data-bd/gold/canonical/holdings/` (B_00 output, comp-freshness `bd_gold_canonical_holdings`). Frozen at 06-18 (partitions 06-11..06-18 present; the silver-fire un-freezes it). Schema: `date, account_id, asset_name, units, price, market_value, source, bd_units, schwab_units, ticker` -> clean map (ticker/market_value/account_id/date), 4 Opal ETFs present.
- PROVEN on 06-15..06-18 (staged to `opal-data-etfs/daily/_stage_49f_canonical/`, NOT the live daily/49financial/ -- did not clobber the live W2 monthly slices). 4 valid daily slices/date, source_as_of=true vintage.

## KEY FINDING -- the monthly->daily flip is NOT value-neutral (~4% basis step)

The overlap check (COO-requested "match the monthly totals") surfaced a CONSISTENT, SYSTEMATIC delta: BD canonical/holdings runs **~3.5-4.4% BELOW** the W2 monthly RPS across ALL 4 ETFs and ALL 4 overlap dates:

| date | canon total | RPS(monthly) total | delta |
|---|---|---|---|
| 06-15 | $503.67M | ~$523.7M | ~-3.8% |
| 06-16 | $501.08M | ~$523.2M | ~-4.2% |
| 06-17 | $497.46M | ~$517.8M | ~-3.9% |
| 06-18 | $499.10M | $519.49M | ~-3.9% |

Per-ETF 06-18: DIVZ -3.53%, IDVZ -4.09%, PFDE -4.13%, PFOE -4.17%. Consistency = STRUCTURAL, not noise/bug.

### Mechanism (grounded; one residual could-not-verify)

- canonical/holdings is the BD-RECONCILED view: `source` col = reconciled (5280) / schwab_override (21) / schwab (2); account-ID scheme is BD's `z0812152081`. RPS is the RAW Schwab record-of-record: Schwab account numbers `0010023253`. **Different account-ID systems -> not directly joinable without the BD<->Schwab account crosswalk.**
- UNITS are ~equal (canonical `units` = `schwab_units` = 4,464,396; `bd_units` only ~0.17% lower) -> the gap is NOT a share-count difference.
- ACCOUNT UNIVERSE differs: canonical 5303 accts vs RPS 5457 (~154 fewer, ~2.8%) -- the BD-reconciled universe is narrower than raw Schwab custody.
- COULD-NOT-VERIFY (honest): the exact split of the ~4% gap between "missing accounts" vs "per-account valuation (BD `price` vs Schwab `closing_price`)" needs the BD<->Schwab account crosswalk (the ID schemes differ). Grounded bound: ~2.8% account-universe + a pricing/mix residual.

### Implication (the flip decision -- for COO/DS/0.4.0_DE)

source_as_of handles the GRANULARITY label (monthly->daily), but NOT this BASIS shift. If 49F flips to the canonical/holdings source, the served 49F ETF-ownership STEPS DOWN ~4% at the switchover (RPS-basis $519M @06-18 -> canonical-basis $499M). That is a visible AVGCAP/report discontinuity. DECISION NEEDED: which basis is canonical for 49F-daily -- raw-Schwab-custody (RPS, what W2/the live monthly uses) or BD-reconciled (canonical/holdings, daily-capable)? They are ~4% apart by design. (Ties to the broader RPS-vs-BD-reconcile basis question -- cf. the Schwab-raw-native canonical rebuild + the MDPF WS-E Schwab-only v0.9 basis.)

## Remaining (when the silver fire clears -> deploy-and-go)

1. IAM delta: the daily variant reads `opal-data-bd/gold/canonical/holdings/*` (the W2 role only grants `schwab/silver/rps/*`) -> add one ReadOwnFirmCanonicalHoldings Sid (same bucket, no cross-firm widen). comp-iam-verify.
2. TF (mirror bd-49f-etf-ownership-daily.tf; env HOLDINGS_PREFIX=gold/canonical/holdings/) + source-map + build-and-upload + safe-apply.
3. Resolve the BASIS decision (above) BEFORE flipping -- it's not a silent swap.
4. Trigger: could event-chain on the BD canonical/holdings refresh (daily-capable) once live -- vs the W2 monthly's no-trigger. CTO/COO call at flip.

## Cleanup note

Staging prove-artifacts at `opal-data-etfs/daily/_stage_49f_canonical/{06-15..06-18}.json` (NOT a partner prefix -> AVGCAP-invisible; AVGCAP reads daily/{partner}/). Regenerable. Confirm cleanup (S3 delete needs the human-confirm gate) -- I left them rather than self-delete.

## Compiler Tools

| Tool | Call | Result |
|---|---|---|
| comp-freshness | artifact bd_gold_canonical_holdings (source verify) | PASS (frozen @06-18, B_00) |
| ds-commit-gate | the canonical producer .py | PASS |
| comp-iam | (W2 role reviewed; the daily read-path delta noted for deploy) | DEFERRED to flip-deploy |

Gap: same pipescript MDPF/ETFS non-registration; the source-basis delta was grounded by direct parquet read (source/units/account-id cols), not a graph tool.
