# ADVI_PERFRP.TO-R1-AE / PRFR1AE-AC3 (cell PRF-c-2) -- THE KEY->URL MAPPING

**Author:** `0.7.0_AE_CloudOps~G` · **Date:** 2026-08-31 ~23:0xZ · **Plane:** DESIRED (source), NOT edge-verified

AC3's amended form requires the mapping to be STATED as part of the evidence, "because that mapping IS
the claim." This file is that statement. It discharges AC3's MODEL half only. AC3 stays BLOCKED: the
EXERCISED half is an authenticated DEV fetch returning 200 + body, which needs a published leaf (GATE A).

## 1. The two sides, each read at source

| side | source | value |
|---|---|---|
| PRODUCER key | `data/assets/scripts/gold/runners_49f/d_publisher_port.py` `SERVE_BUCKET` / `SERVE_ROOT` | `opal-data-portal-v2` / `platinum/advi/49financial` -> key `platinum/advi/49financial/{leaf}` |
| CONSUMER URL | `portal/src/api/endpoints/advisor-intelligence.ts:489` `PLATINUM_BASE` | `/api/scoped/advisor-intelligence/platinum` |

Portal PERFRP fetchers (portal @`be39451b`, DEV), all added @`9f8d10fa` (2026-08-28, `0.4.0_DE_ClientPlatform~D`, TO-R1-DE AC3/AC4):

| line | leaf(s) | URL built |
|---|---|---|
| `:1618` | `perfrp_performance_{account,relationship}` | `{PLATINUM_BASE}/perfrp/perfrp_performance_{level}.json` |
| `:1700` | `perfrp_book_advisor` | `{PLATINUM_BASE}/perfrp/perfrp_book_advisor.json` |
| `:1765` | `perfrp_gainloss_{account,relationship}` | `{PLATINUM_BASE}/perfrp/perfrp_gainloss_{level}.json` |
| `:1863` | `perfrp_allocation_{account,relationship}` | `{PLATINUM_BASE}/perfrp/perfrp_allocation_{level}.json` |

7 of the 11 registered EMITTERS families have a portal fetcher. Of the remaining 4:
`perfrp_transactions_relationship` is DEFERRED by ruling (s.11 #6 / CTO 67106(2));
`perfrp_activity_{account,relationship}` and `perfrp_roster_relationship` have no consumer today.

## 2. MEASURED MISMATCH -- the fetcher resolves to a key the publisher never writes

`comp-routes trace --json`, one path segment the only variable:

```
  .../platinum/perfrp/perfrp_performance_account.json
      outcome RESOLVED   s3_key  platinum/perfrp/perfrp_performance_account.json      <-- NOT WRITTEN

  .../platinum/advi/49financial/perfrp_performance_account.json
      outcome RESOLVED   s3_key  platinum/advi/49financial/perfrp_performance_account.json   <-- the publisher's key
```

Both carry `behavior /api/scoped/advisor-intelligence/*.json`, `rewrite_rule
/api/scoped/advisor-intelligence/platinum/ -> platinum/`, `auth true`, edge chain
`auth-validator-edge` (viewer-request) -> `shared-advisor-router` (origin-request) ->
`shared-advisor-router-response`.

**Router confirmation:** `perfrp` occurs ZERO times in
`infra/aws/lambda-edge/shared-advisor-router/index.mjs`. Its only ADVI canonical class is
`PLATINUM_ADVI_PREFIX = "platinum/advi/"` (v14, OPAL_ADVIPOINTERS P4R-3 remedy (A): keys under
`platinum/advi/{firm}/` resolve to `opal-data-portal-v2`). `"platinum/perfrp/"` does not start with
`"platinum/advi/"`, so `platinumAdviFirm` stays null and the request never takes the portal-v2 path.

**CONSEQUENCE:** a CORRECT publish would still leave the four panels empty. The failure would present
as "publish succeeded, panels still empty" and invites misdiagnosis as a producer or data problem.
Closable inside the BUILD-ONLY cap; does not touch the publish.

## 3. THE CANONICAL MAPPING (what AC3 asserts)

```
  s3://opal-data-portal-v2/platinum/advi/49financial/{leaf}
      <->  /api/scoped/advisor-intelligence/platinum/advi/49financial/{leaf}[?firm={bucketSuffix}]
```

## 4. LIMITS -- stated so no reader takes this wider

- **DESIRED plane only.** `comp-routes` PARSES the same router source this file reads: those are ONE
  METHOD, not corroboration. The independent instrument is an authenticated DEV fetch, and it is the
  half AC3 gates on a published leaf. NOT claimed here.
- **The BUCKET half is not claimed.** The origin is firm-parametric and resolved inside the router; the
  static model emits the KEY and refuses to name a bucket (`s3_bucket: null`). The KEY difference is
  measured; the portal-v2 resolution is asserted by the router's own v14 comment, read but not exercised.
- Leaf CONTENTS and shapes were not opened. Key routing only.
- `RESOLVED` is a claim about the model, never a grant.
