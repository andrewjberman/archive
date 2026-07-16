# FILLED-VIA-HISTORY-ARTIFACTS — window-pull acceptance artifact

**Author:** 0.4.0_DS_ClientPlatform~B · **Date:** 2026-07-16 18:36–18:45Z
**Authorization:** CTO GO 20260716T164833Z (5 conditions) on the WP1 census recommendation
(`ECLIPSE_ENDPOINT_CENSUS_WP1_CLOSE_20260716.md`); ORION standing egress lift covers the calls.
**Census JSON (machine):** `eclipse_history_census_2026-07-13_2026-07-15.json` (this dir) — full
per-call census + landed-key/ETag/size listing.

## Verdict

The 07-13..07-15 hole's event history is LANDED as real vendor bytes: **55 calls, 55/55 HTTP 200,
55 keys** written additively under `s3://opal-data-inf/bronze/eclipse/_history/` in the vendor's own
four shapes. No parse-down, no re-serialization — each object is the raw HTTP response body (17a).
Door-adjacent state untouched: nothing outside `_history/` written; pre-listing proved the prefix
EMPTY (KeyCount=0) before the first call.

## Call census (denominator enumerated at run time)

| Type | Calls | 200s | Landed | Content |
|---|---:|---:|---:|---|
| auditlog_portfolio (per changed id, fromDate/toDate) | 18 | 18 | 18 | ALL non-empty (376–810B); the 3 created (1419/1420/1421) carry Insert+Update rows |
| auditlog_model (full 18-model roster, same window) | 18 | 18 | 18 | ALL honest-zero `[]` — "models static across the hole" now EXERCISED roster-wide (was single-probe M1) |
| closed_trades (one window call) | 1 | 1 | 1 | 11,737,710 B — the 2,937-row trade ledger w/ at-trade portfolio values |
| trade_instances (per changed id, startDate/endDate) | 18 | 18 | 18 | 3 non-empty (portfolios 165, 468, 1381 — one rebalance instance each); 15 honest-zero |
| **Total vendor calls** | **55** | **55** | **55** | +2 setup: SMOKE `/v1/modeling/models` (200, 18 rows) + held-bronze discriminator read (S3, not vendor) |

Vendor-call count for the egress record (GO: "log the count anyway"): **56 total** (55 window + 1 SMOKE),
standing Eclipse JWT via SM `orion/eclipse_jwt/current` (remaining 15,897s at load; no re-exchange).

**Empty-file semantics:** 33 of 55 objects are 2-byte `[]` — the vendor's own clean-zero answer for
that id/window (exercised negative), not failures. ETag d7517139... recurs because md5("[]") is
constant. They are load-bearing: the model-roster zeros upgrade the census's M1 single-probe claim to
roster-wide vendor-surface grade.

## CORRECTION landed on the proposal's arithmetic (union vs sum)

The proposal said **~45 calls / 21 portfolios ("18 edited + 3 created")**. Measured at run time from
the same held discriminator source (`bronze/eclipse/2026-07-16/portfolios_simple.json`):
|edited∩window| = 18, |created∩window| = 3, **created ⊂ edited** (1419/1420/1421 were created AND
edited in-window). The changed set is the UNION = **18**, byte-matching the census's own printed ID
list. "21" summed overlapping sets. The gate that caught it: the run-time denominator derivation
aborted on mismatch BEFORE any vendor call; re-run proceeded only after the overlap was measured and
the gate re-anchored to the census's printed ID list (the stronger anchor). True call total: 55
(18+18+1+18), same magnitude as proposed.

## Conditions discharged

1. **Vendor shapes only, four types, no parse-down** — raw response bytes per object; types exactly
   `{auditlog_portfolio, auditlog_model, closed_trades, trade_instances}`.
2. **Census + landed listing as acceptance** — this doc + the machine JSON; listing via
   ListObjectsV2 (key+ETag+size), never HeadObject; denominators printed at run time.
3. **Additive only** — pre-listing EMPTY; all 55 keys new under `_history/`; zero writes elsewhere;
   nowhere near `gold/meta/*` held keys. (One accidental re-invocation at 18:45:48Z aborted AT the
   additive gate with zero vendor calls and zero writes — verified: key count still 55, newest
   LastModified 18:44:43Z.)
4. **Manifest amendment** — routed to 0.7.0_AE_CloudOps for authorship on this evidence (their lane
   per the GO), message 2026-07-16T18:4xZ.
5. **Catalog-pointer doc amendments in-window** — landed at `b06048dd5` (endpoints/README.md +
   DOMAIN.md + AUTHENTICATION.md banners, 0.7.0-authored text, my commit per owned-paths routing);
   D3 arch-spec pointer routed separately to CTO (his lane, by 0.7.0).

## What this closes and what it does not

- CLOSES: the manifest's genuinely-unknown residual — the 18 changed portfolios' intermediate paths
  through the hole now exist as exercised vendor artifacts (audit rows + trade ledger + instances).
- STANDS: the honest-holes rejection of labeled copies — no `2026-07-1{3,4,5}/` standard-shape
  partitions exist or ever honestly can (no as-of on the snapshot endpoints).
- UNTOUCHED: the daily 4-file cadence; my silver leg stays today-forward.
