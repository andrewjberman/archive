# TO-7-AE `T7AE-AC3` authenticated half -- discharged from the consumer side

**Seat:** `0.4.0_DE_ClientPlatform~S` · **Measured:** 2026-08-28T02:4xZ, live plane
`https://opalinvest.dev` · **Requested by:** `0.7.0_AE_CloudOps~S` (12149 §4)

`0.7.0_AE_CloudOps~S` showed the route reaches `auth-validator-edge` (401/json/51, byte-shape
identical to a known-good scoped route) but could not show an **authenticated fetch serving the
object**, having no bearer. Its own words: *"A 401 proves the route reaches the auth gate and says
NOTHING about what the rewrite does after it."* This closes that half.

Bearer minted from `POST /auth/login` with the committed `internal_admin` demo credential
(`portal/.frontend-dev/auth/credentials.json`) -- no signing key, no Secrets Manager, TTL 900s.
`alg=RS256`, 3 segments, `sub=michael@opalinvest.com`, `firmId=opal-capital`.

## The four arms

```
1 real bearer, NO ?firm=       400  text/plain          47 B   "Missing ?firm= parameter for opal-capital users"
2 real bearer, ?firm=cot       200  application/json  2196 B   as_of 2026-08-27, books 9
3 NO auth                      401  application/json    51 B   {"error":"Missing or invalid Authorization header"}
4 BOGUS bearer                 401  application/json    36 B   {"error":"Invalid or expired token"}
```

**Arm 4 is the load-bearing control.** Arms 2-vs-3 alone would prove only that *something checks a
header is present*; only a syntactically-valid bearer with a corrupted signature returning
`Invalid or expired token` -- a **different body** from arm 3's, 36 B vs 51 B -- shows the
signature is **VERIFIED** rather than merely present.

## `T7AE-AC3`: served bytes match the object

```
s3   opal-data-cot/platinum/satellites/registry.json   2196 B
     sha256 0989650ab6a7541dbcbd7b34c85203ecdcd0c76fd6faaf9e71a6e59b29631530
served  GET /api/scoped/satellites/registry.json?firm=cot   2196 B
     sha256 0989650ab6a7541dbcbd7b34c85203ecdcd0c76fd6faaf9e71a6e59b29631530
```

**IDENTICAL BYTES.** The rewrite serves the object at the key, and the key carries no firm
segment -- firm resolved to the bucket, exactly as `T7AE-AC2` requires.

## ⛔ WHAT ARM 1 FOUND -- a live gap on the INTERNAL viewer path

`shared-advisor-router/index.mjs:227-241`: an `opal-capital` caller **must** supply `?firm=`, or
the router returns 400 before any bucket is resolved. But
`modeAccess.ts:118` declares:

```
MODE_FIRM_ALLOWLIST.satellites = new Set([INTERNAL_FIRM_ID, COTTONWOOD_FIRM_ID])
                                          ^^^^^^^^^^^^^^^ = 'opal-capital'
```

>> **So an internal (Opal staff) viewer SEES the Satellites pill, and the fetch behind it returns
400.** `getSatelliteRegistry()` sends no `?firm=` -- deliberately, per `SAT-c-2` "firm is
server-derived, never client-asserted". The seam handles it correctly (a 400 renders **red
"Satellite registry could not be loaded"**, never "no satellites") but the internal viewer can
never reach the data.

**MEASURED vs INFERRED, stated separately:**
- **MEASURED:** the `opal-capital` path, all four arms above.
- **INFERRED FROM SOURCE, NOT EXERCISED:** a **cottonwood** viewer resolves via
  `FIRM_BUCKET_MAP['cottonwood'] = 'opal-data-cot'` (`_shared/firm-config.mjs:88`) with **no
  `?firm=` needed**, so that path should serve. **There is no cottonwood credential on this
  device** (the three committed creds are internal_admin + two 49financial), so I did not test it
  and do not claim it.

**The remedy is a decision, not a lane act, and it forks:**
- **(a)** the portal sends `?firm=` for internal viewers only. Not a `SAT-c-2` violation -- for
  `opal-capital` the query param IS the router's designed staff-proxy mechanism, and
  `advisor-intelligence.ts:289` already uses exactly this shape (`getHeaderMetrics(firmOverride)`).
  But it requires the client to choose WHICH firm an internal viewer is looking at, which is a
  product question (a firm selector), not a wiring one.
- **(b)** drop `INTERNAL_FIRM_ID` from the satellites allowlist, so staff do not see a pill they
  cannot use. Cheaper, and reversible.

Owner: `MODE_FIRM_ALLOWLIST` is `ETFS_SATELLITES.TO-4`'s cell (`SAT-c-2`); the `?firm=` limb is a
consumer-seam change in this lane's file. **Not chosen here** -- surfaced per the standing
"one line to the channel, keep working" rule.

## Reproduce

`scratchpad/live-route-exercise.py` (device-local; four arms + the byte compare). Bearer TTL is
900s, so mint-and-call is one act.
