# TO 3F-B6 (LIVENESS PORTION) — Feed-Level Liveness Signal for the COT Rebalancer Feed

**Agent:** 0.6.2_AE_PartnerETL~A · **Date:** 2026-07-22 ~21:1xZ · **Scope:** deliverable (a) only — the
TEMPORAL-vs-CURRENT probe is sequenced LAST per COO 204647Z / CTO 204557Z (PRD v1.8) and is NOT run here.
**This portion gates 3F-G8.**

## The signal

**Nightly vendor-revaluation drift in `rebalancer_model_detail`.** Black Diamond's Rebalancer re-marks
every composite model's component weights (`relativeAllocation` / `absoluteAllocation`) and stamps
`updatedAt` in a vendor-side nightly batch (~05:01Z — CRO's A5 observation, now mechanism-confirmed as a
revaluation, not a config edit). Those weights are **market-priced quantities**: they move when the vendor's
data plane is alive, regardless of whether any assignment changes.

**Liveness check (per trading-day pair D-1 -> D, evaluated on already-landed bronze):**
```
ALIVE   <=> at least one common model_detail payload differs (or max updatedAt advanced)
FROZEN  <=> all model_detail payloads byte-identical across a TRADING-day pair
```
NOT a roster diff: the discriminating fields are valuation marks, not assignments. The check reads
`blackdiamond/cottonwood/bronze/rebalancer_model_detail/{date}/` — **no new endpoint, no producer change,
no extra vendor calls.**

## Demonstrated discrimination (the two live pulls, denominators printed)

Pulls: 2026-07-21T23:31:2xZ (deploy-day run) and 2026-07-22T06:00:4xZ (first scheduled cron(0 6) fire —
schedule exercised). Note these bracket ZERO trading sessions (Tue post-close -> Wed pre-market), which
makes the result sharper:

| Surface | 07-21 vs 07-22 | Verdict |
|---|---|---|
| `rebalancer_models` (roster) | 1/1 page byte-identical (md5) | assignment STABLE |
| `rebalancer_accounts` (book) | 5/5 pages byte-identical (md5) | assignment STABLE |
| `rebalancer_model_detail` | **20/25 models differ**; field classes: `relativeAllocation` 473 leaves, `absoluteAllocation` 473, `updatedAt` 31 | feed ALIVE |

Both states measured simultaneously on the same pull pair: **the roster read "no change" while the feed
proved itself alive** — precisely the case CRO §7.4 says storage cannot discriminate. The refinement to
§7.4: that indistinguishability is a property of the ASSIGNMENT surfaces (`models`/`accounts`); the SAME
feed's `model_detail` surface carries a per-day vendor heartbeat, and it is already in our bronze.
(The weights moved across a no-market-hours window because the ~05:01Z batch re-marks to the prior close —
the signal keys on the vendor's BATCH running, which is exactly "the data plane is alive.")

## Honest limits

1. **5/25 models static across the pair** (simple/single-component models with structural weights, incl.
   pinned 1.0 compositions). The check is fleet-level (ANY model moved), never per-model.
2. **Market-closed-day pairs:** weights may legitimately freeze when the prior close is unchanged
   (calendar-first, NEVER#1 — evaluate on trading-day pairs only). Whether `updatedAt` still advances on
   closed days is UNDETERMINED until the feed's first weekend (07-25/26) is observed; until then closed-day
   pairs are simply not evaluated.
3. The signal covers the REBALANCER app's data plane (where weights recompute). A broader BD-platform
   canary (the DataMining HOLDINGS_DAILY file, which changes every delivery — measured in 3F-B5) is
   corroborating but is a different feed; the model_detail signal is the feed-level one this TO demands.
4. Two data points exist today (the feed is 2 days old — that is its age, not a gap). The signal's
   false-alarm rate accrues measurement for free with every daily pull.

## Carried bindings (per the TO)

- **Fingerprint BAN carried:** holdings-basket fingerprinting stays banned by measurement (pairwise cosine
  0.62–0.98, mostly >0.90) — nothing here weakens it.
- **~05-28 structural depth ceiling stands** regardless of any probe outcome: no Opal-model series can
  predate the models' creation (2026-05-28..07-17).
- **Zero backfill executed; forward-only stands.** The TEMPORAL probe (with its mandatory positive
  control — CRO churn data supports construction: 5-of-296 new accounts since 06-08, models created on
  07-06 for a quarter of the book) runs LAST in the sequence, per the consolidated order.

## Phase-3 denominators (bronze re-list)

`rebalancer_models`: 1 page/day x 2 days · `rebalancer_accounts`: 5 pages/day x 2 days (rows 911/911
via manifest totalResultCount) · `rebalancer_model_detail`: 25 files/day x 2 days, 25/25 common ·
`meta/pulls/{date}/`: 2 manifests/day x 2 days. Series is 2 days old because it STARTED 07-21 — not a gap.

## Probe prep (added ~21:47Z — the control is constructed BEFORE the probe runs, per the TO's hard gate)

**15 positive-control candidates identified and banked**: Opal-assigned accounts in today's rebalancer
book (295 Opal of 911 total) that are ABSENT from the 2026-06-09 `fact_holdings` book (680 distinct
accounts) — their assignment necessarily changed (none -> Opal) between the probe windows. First eight:
`658508703` (Sat 50), `658508963` (Sat 40), `658509261` (Sat 60), `658508828` (Sat 60),
`638432512` (66% LT/34% UST), `Z40493496` (Cash+Sat 50), `658509146` (Sat 60), `658509145` (Sat 80).
The control can fail in BOTH directions: a TEMPORAL surface must return these absent/unassigned for the
06-09 window; a CURRENT-stamped surface returns them carrying today's Opal strategy under a 06-09 label.
The probe itself runs LAST in the consolidated sequence, after tonight's qt1 template dump (CRO reads the
dims), per COO 204647Z.

## For CRO (A5 residual, now determined)

CRO's "whether updatedAt movement is composition edits or a system touch is not determined": **determined —
it is a nightly revaluation batch.** The updatedAt advances ride WITH 473 re-marked weight leaves across a
window containing no human edit and no market session; a config-edit explanation cannot produce that
signature across 20 models simultaneously at 05:01Z.
