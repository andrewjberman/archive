# SATELLITES SCOPED PATH -- WHAT IS REUSABLE, WHAT MUST BE ADDED

**Author:** `0.7.0_AE_CloudOps~Y` · 2026-08-27 ~22:2xZ · **archetype:** TRACE
**Requested by:** `1.0.0_SA_CTO~Z` msg 10485 -- *"Reading the applied policy and naming exactly which
of its properties the Satellites path can reuse, and which it must add, is useful now and does not
depend on the amendment."*
**Governing ruling:** Andrew-direct ~22:1xZ `@834bfafebb` -- a NEW firm-scoped API path for Satellites
only; `positioning_data.json`, models and etfs UNTOUCHED.

⛔ **THIS IS NOT A DESIGN AND NOT A SPEC.** No round-2 TO exists; `PT-a-1`'s amendment is uncertified.
This is an inventory of what the estate already provides, so whoever is seated does not rebuild it.
**Every row carries its plane.**

---

## 1. REUSABLE -- ALREADY BUILT, ALREADY APPLIED

| # | thing | plane | what it gives the Satellites path |
|---|---|---|---|
| R1 | **`auth-validator-edge` at `viewer-request`** | **EXERCISED** | `X-Firm-Id` injected from the validated JWT. `index.mjs:388` is a plain **assignment**, destroying any client value. Exercised this session: **5 forged header values, all ignored**, server echoed the JWT firm. **Attaches to any `/api/scoped/*` behaviour.** Discharges `PT-a-2`'s mechanism. |
| R2 | **Cache policy `opal-scoped-advisor-by-firm`** `45eb7514-712c-42c5-9fd6-40909b9f0347` | **APPLIED** (live `get-cache-policy`) | `HeaderBehavior: whitelist ['X-Firm-Id']` + `QueryString: whitelist ['firm']`, TTL def 60. ⭐ **`PT-a-3` needs this BOUND to a new behaviour, not authored.** |
| R3 | **`shared-advisor-router` at `origin-request`** | APPLIED + SOURCE | **FIRM-PARAMETRIC origin selection** -- the bucket is chosen per requesting firm from `FIRM_BUCKET_MAP` (`../_shared/firm-config.mjs`). `comp-routes` refuses to name a single `s3_bucket` for this family precisely because it is per-firm. **This is the mechanism that makes a scoped path firm-scoped.** |
| R4 | **`shared-advisor-router-response` at `origin-response`** | APPLIED + SOURCE | The **firm-isolation guard**: independently re-derives the expected bucket from `X-Firm-Id` and compares it against the bucket actually served, blocking a CONFIRMED cross-firm mismatch. **Defence-in-depth that already exists** -- the shared OAI is granted on every firm bucket with no firm condition, and this guard is what catches a mis-route. |

>> ⭐ **THE HEADLINE FOR WHOEVER IS SEATED: THIS IS WIRING ON EXISTING INFRASTRUCTURE, NOT NEW
   INFRASTRUCTURE.** All four limbs of a firm-discriminated serving path -- identity injection, a
   firm-keyed cache, per-firm origin selection, and a cross-firm guard -- **are built, applied, and in
   live use on `/api/scoped/advisor-intelligence/*` today.** <<

---

## 2. ⛔ THE DESIGN LEVER NOBODY HAS NAMED: **THE PATH PREFIX DECIDES HOW MUCH IS REUSE**

`shared-advisor-router` and its response guard are bound to the
**`/api/scoped/advisor-intelligence/...`** behaviours, and the router's rewrite chain keys on that
prefix. **So:**
```
Satellites UNDER /api/scoped/advisor-intelligence/...   -> R1 R2 R3 R4 all inherit. Least new code.
                                                           But it files Positioning data under an
                                                           "advisor-intelligence" name -- a TAXONOMY
                                                           cost, not a technical one.
Satellites under a NEW prefix (e.g. /api/scoped/positioning/...)
                                                        -> R1 and R2 still attach (they are behaviour
                                                           -level). R3 and R4 DO NOT: the router's
                                                           branch chain does not match the prefix, so
                                                           it either gets extended or a sibling router
                                                           is written -- and a SIBLING ROUTER IS A
                                                           SECOND COPY OF THE FIRM-ISOLATION GUARD.
```
⚠ **Two copies of a firm-isolation guard is a divergence surface on the access boundary itself** --
`shared-advisor-router-response` already documents that its re-derivation *"MUST mirror"* the router's.
**A third mirror is a third thing that can drift.** ⛔ **Naming the trade-off; not choosing it. That is
`2.0.0_SA_COO~Z`'s cell and `1.0.0_SA_CTO~Z`'s arch call.**

---

## 3. MUST BE ADDED -- NOT PRESENT ANYWHERE TODAY

| # | gap | plane | note |
|---|---|---|---|
| A1 | **The behaviour itself** -- path pattern, origin, policy bindings, L@E associations | absent | Terraform, `safe-apply`, never a console edit. |
| A2 | **The Satellites payload at a served key** | **MEASURED ABSENT** | `0.4.0_DS_ClientPlatform~L` (TO-2-DS, `PT-b-3`): Cottonwood has a data HOME (6,599 objects in `opal-data-cot`) and **0 Positioning objects in it**. **The path can exist and serve nothing.** Producer is `PT-c-1`, blocked on `PT-b-2`. |
| A3 | **The explicit-empty contract (`PT-c-2`)** | **MEASURED, and it is the sharp one** | On a Satellites-only path, **3 of 4 firms have no payload on day one.** Measured on the scoped family today: a valid bearer + absent artifact returns **`403 artifact_forbidden`** -- **byte-identical to a genuine refusal**, because the server deliberately does not enumerate. **So "no Satellites" and "not permitted Satellites" are indistinguishable at the transport layer.** A `200` + explicit empty is the only thing that separates them. |
| A4 | **A `null`-firm arm on the new path (`PT-inv-3`)** | **NEVER EXERCISED** | Carried in the decomp `@6a07d17cbb`. Needs a **credential grant** (firmless JWT), not code. It lands on the new path too. |

---

## 4. ⛔ THE TRAP, AND IT IS ONE COPY-PASTE AWAY

```
/api/general/*   ->  opal-api-general-5min-cache   HeaderBehavior NONE, TTL 300, Cache-Control public
/api/scoped/...  ->  opal-scoped-advisor-by-firm   HeaderBehavior whitelist ['X-Firm-Id'], TTL 60
```
**A new behaviour cloned from the neighbouring Positioning route inherits the FIRST one** -- no firm in
the cache key, 300s, publicly cacheable. **Same page, adjacent behaviour, opposite property, and the
result would pass every test that does not specifically read the cache policy.** ⭐ **`AC3`'s remedy is
therefore "bind R2", and its failure mode is "bound the neighbour's".**

---

## 5. WHAT MAY NOT BE INHERITED BY ASSERTION

⚠ **"R1 and R2 attach to any `/api/scoped/*` behaviour" is a PREDICTION from the applied config, not a
measurement of the new path** -- the new path does not exist. **`AC7` requires both re-exercised on it:
a forged `X-Firm-Id` refused, and two firms on one path producing distinct cache entries.**
**`PT-inv-2` is precisely the standing constraint that should refuse a new path on which the header
turns out to be client-assertable.**

⚠ **Plane discipline for §2's router claim:** the behaviour->router bindings are **APPLIED** (live
`get-distribution-config`); the router's *internal branch chain* is **SOURCE** (`comp-routes` declares
its own plane DESIRED and warns a pinned stale edge version reads identical). **A security-critical
branch on the new path grounds on the deployed artifact, per Rule 22a.**

---

## 6. NOT ASSERTED

- **No path prefix chosen. No origin named. No Terraform written.** No round-2 TO exists.
- **Nothing here amends `PT-a-1`** -- that is `2.0.0_SA_COO~Z`'s write, certified by `3.0.0_SA_CVO~Z`,
  and this note is deliberately readable before or after that lands.
- **This note does not claim the four reusable limbs are SUFFICIENT** -- only that they exist and are
  applied. Whether they compose correctly on a new prefix is A2/A3-dependent and unmeasured.
