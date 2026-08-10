# MDPF_CANPLAT.P0-2R — H1/H2 vendor early-clock probe, 2026-08-07

**archetype:** VALIDATE · **Author:** `0.7.0_AE_CloudOps~Z`
**Authorization:** Andrew-direct per-use egress ("You have egress"), Orion Assets + Eclipse,
READ-ONLY, this morning only. **SmartX was NOT named in his word and was NOT called** — H2 took
the pre-approved S3-side fallback (criterion 1 of the adopted P0-3).
**Window discipline:** all vendor calls **08:10:15–08:13:58 EDT**, i.e. at or after the
08:05 ET floor and inside 08:40. Nothing fired below the floor.

---

## 1. THE FLOOR, GROUNDED ON THE PLANE — and the 93 seconds that matter

`aws events describe-rule opal-inf-jwt-fetch` → **`cron(5 12 * * ? *)`, no TZ field, ENABLED.**
UTC-fixed 12:05Z = **08:05 ET in EDT** (regime confirmed EDT, offset −0400).
**The Clock-v3 record's 12:15Z is WRONG and the plane is cited here, per criterion 1.**
**Criterion 1a: THE MINT WAS NOT MOVED and nothing in this TO proposes moving it.**

⚠ **NEW, MEASURED, AND IT SHARPENS THE FLOOR:** the cron *fires* at 12:05Z but the mint
**completed at 08:06:33.831 ET** (`describe-secret orion/jwt/current` LastChangedDate) — **~93
seconds after the cron.** I read the secret at 08:06:34, one second after it landed.

> **A probe firing at 08:05:10 ET — legally past the stated floor — would have read YESTERDAY'S
> token inside its 10h TTL and recorded a false PASS.** This is the 12-second race of Amendment 1,
> alive today at ~93 seconds. **The floor is not "the cron fired"; it is "the mint LANDED," and
> only the secret's own LastChangedDate discriminates them.** Recommend the operational floor be
> stated as *08:05 ET **and** `orion/jwt/current` LastChangedDate ≥ today's mint* — a clock alone
> is not sufficient. Usable window today was therefore **08:06:34 → 08:40 = ~33.4 min**, not 35.

## 2. H1 — ORION ASSETS: **EARLY-VALID (on the day probed)**

**Endpoint:** `GET /api/v1/Portfolio/Clients/{clientId}/Assets/{MM-DD-YYYY}` (the assets_v2
binding route). **Denominator: 3 clients × 2 dates = 6 calls, 6/6 HTTP 200, 0 failures.**

| client | request | rows | currentValue | costBasis | shares | asOfDate | called (ET) |
|---|---|---|---|---|---|---|---|
| 123 | **TODAY 08-07** | 208 | **503,549.57** | 0.00 | 63,948.55 | 2026-08-07 | 08:10:15 |
| 123 | PRIOR 08-06 | 208 | 503,549.57 | 0.00 | 63,948.55 | 2026-08-06 | 08:10:16 |
| 35 | **TODAY 08-07** | 67 | **1,165,849.95** | 0.00 | 52,159.63 | 2026-08-07 | 08:10:17 |
| 35 | PRIOR 08-06 | 67 | 1,165,849.95 | 0.00 | 52,159.63 | 2026-08-06 | 08:10:17 |
| 546 | TODAY 08-07 | 72 | 0.00 | 0.00 | 0.00 | 2026-08-07 | 08:10:18 |
| 546 | PRIOR 08-06 | 72 | 0.00 | 0.00 | 0.00 | 2026-08-06 | 08:10:18 |

**VERDICT: the binding Orion input carries REAL SETTLED MONEY at 08:10 ET — 30 minutes before
the 08:40 bar.** TODAY and PRIOR return **identical values (delta +0.0000%)**, which is exactly
the contract's documented `run-date-echo-of-prior-settled` semantics: the request date is echoed
into `asOfDate` while the payload carries the prior-settled basis (normalized downstream by
`_orion_vendor_asof.orion_normalize_as_of`, label_offset −1 trading day).

**Client 546 is an HONEST ZERO, not a failure:** it reads 0.00 on BOTH dates, so it is that
client's state, not a freshness artifact. Reported rather than dropped. **2 of 3 probed clients
carry non-zero value; 1 is structurally empty.**

### ⚠ TWO INSTRUMENT TRAPS THIS PROBE HIT — both would have produced a confident wrong answer

1. **`asOfDate` ECHOES THE REQUEST.** Asking for 08-07 returns `asOfDate: 2026-08-07` *whatever
   the data is*. **An agent checking the date field alone records EARLY-VALID unconditionally.**
   The only sound oracle is the VALUES, which is why the TODAY-vs-PRIOR value comparison above
   is the actual test.
2. **MY OWN FIRST READ WAS A FALSE ZERO.** I initially summed a field named `value` — which does
   not exist on these rows — and got "TODAY total 0.00" for every client. The real money field is
   **`currentValue`**. `dict.get()` on an absent key returns None → 0.0 silently, so the
   instrument reported a clean, confident, entirely wrong zero. Caught only by dumping the row
   keys and running the positive control. *Same class as the `grep -c` counting an error message.*
3. Equal payload SIZE is not equal content: TODAY/PRIOR were byte-length-identical per client
   yet **sha256-different** (the `asOfDate` string differs). A size check would have called them
   the same object.

## 3. ECLIPSE: **EARLY-VALID for the surface probed** (and one more trap)

`GET https://www.orioneclipse.com/v1/modeling/models` → **HTTP 200 `application/json`, 18 rows,
08:13:58 EDT**; `/v1/modeling/models/9` → 200 JSON, 1,972B, 08:13:57 EDT. Auth `Session {jwt}`.

⚠ **THE TRAP: my first Eclipse call returned "HTTP 200" that was the SPA's HTML shell**
(`/api/v1/modeling/models` → `text/html`, `<!doctype html>`, 55,603B). My probe treated 200 as
success and broke out of its retry loop — **a false PASS that I recorded and then caught only by
inspecting the body.** The correct base path carries no `/api` prefix. **A 200 is not a data
response; content-type + a JSON-parse check is the discriminator.**

**SCOPING LIMIT, STATED HONESTLY:** I probed the **modeling** surface, establishing Eclipse is
reachable and serving real JSON inside the window. I did **NOT** specifically probe the
`fact_portfolios_full` source route — **that row is NOT-PROBED**, not EARLY-VALID. It is also not
the binding constraint: the 30-day census has Eclipse missing the 08:40 bar **1 of 21 days**
(normal landing 23:30 ET prior day, 9.2h early), against **Orion missing 20 of 21**.

## 4. H2 — SMARTX: **EARLY-INVALID on the current clock** (S3-side fallback, NO vendor call)

Andrew's word named Orion + Eclipse. **It did not name SmartX, and a grant for one vendor is not
a grant for another** — so no SmartX endpoint was touched. Pre-approved S3-side fallback,
**s3api ISO-8601 with `+00:00`** per criterion 8 (never `aws s3 ls`, which prints local time):

| table | 08-04 | 08-05 | 08-06 |
|---|---|---|---|
| `fact_model_aum_daily` | 13:41:37+00:00 | 13:41:34+00:00 | 13:40:01+00:00 |
| `fact_allocation_valuation` | 13:42:08+00:00 | 13:42:04+00:00 | 13:40:28+00:00 |

13:40–13:42Z = **09:40–09:42 ET — misses the 08:40 bar by ~60 min, 3 of 3 days**, corroborating
the 24/24 census. No single landing minute carries >1 partition, so **no bulk-backfill exclusion
applies** (criterion 9).

⚠ **METHOD LIMIT, CARRIED VERBATIM (criterion 10): silver LastModified measures WHEN THE
CONVERTER WROTE, not when the vendor made data available. This census BOUNDS THE CURRENT PIPELINE
CLOCK; it does NOT prove SmartX data is unobtainable earlier.** The unproven residual stays an
**OPEN OBLIGATION**, not silently upgraded to a proof (criterion 7).

## 5. VERDICTS — third state present and used

| Feed | Verdict | Basis |
|---|---|---|
| Orion Assets (assets_v2) | **EARLY-VALID** | real settled money at 08:10 ET, value-compared |
| Eclipse modeling surface | **EARLY-VALID** | 200 JSON at 08:13:58 ET, content-verified |
| Eclipse `fact_portfolios_full` route | **NOT-PROBED** | route not resolved inside the window |
| SmartX (both silver legs) | **EARLY-INVALID** *on the current clock* | S3-side, converter-bound |

**CLASS A′ LANGUAGE HELD (criterion 5):** every verdict above is asserted **ON THE ONE DAY
PROBED (2026-08-07), n=1**. These are vendors we do not control; **no reserved word
(proof/provably/definitively/source-confirmed) is used about vendor behavior.** The design must
not depend on this sample generalizing — Clock v3's labeled-carry rule already provides that.

## 6. WHAT THIS AUTHORIZES — and what it does NOT

- **Orion's pull can move earlier** into 08:06:34–08:40 ET: the data is there and settled.
  **The mint does NOT move** (criterion 1a). **The pull adapts to the floor; the floor does not
  adapt to the pull.** ⚠ And the real floor is mint-LANDED (§1), so any earlier pull must gate on
  the secret's LastChangedDate, not the wall clock.
- **SmartX: shifts land on probe PASS. This is not a pass, so NOTHING SHIFTS** — vendor lateness
  surfaces as **labeled carry** (2 TD window, every carried point labeled), never a held publish
  (H12, already ruled). A negative probe is a COMPLETE outcome; I am not inventing a compensating
  path. ⚠ And per the adopted criterion 0, the SmartX remedy — if ever pursued — must target
  **`smartx-assets-daily-pull-daily` (09:30 ET)**, whose OnSuccess chain produces the binding
  silver; doc 03's JWT + rest-pull move would change nothing while reading as delivered.
- **NOTHING WAS APPLIED.** No schedule, JWT, or infra was changed (criterion 6, and this TO's
  do_not list). The Wave-B move-as-a-unit design decision goes to COO~Z with this evidence.
