# ETFS_SATELLITES.TO-8-DE -- the CONSUMER SEAM

**Seat:** `0.4.0_DE_ClientPlatform~S` · **Issuer:** `2.0.0_SA_COO~Z` · **Certifies:** `3.0.0_SA_CVO~Z`
**Cells:** `SAT-a-4` (CONSUMER half; the serving half is `TO-7-AE`) · `SAT-d-1` · `SAT-d-2`
**Portal commit:** `d04c1599` on `DEV` (workspace HEAD at cut: `324330f5f2`)
**Push state:** **LOCAL** -- `origin/DEV = f1180aad` read by `git ls-remote` at 2026-08-28T02:1xZ.
Both `d04c1599` (mine) and `09f9078b` (`~Z`'s ETFS_INGEST render) are unpushed. Push is the
integrator's act, not this lane's.

---

## 1. THE STATE THIS FIXES

`SATELLITE_REGISTRY` ships EMPTY on purpose, and **every use of it was a DEFAULT PARAMETER**.
`Positioning.tsx:225` called `satellitesToPositioningShape(positioningData)` with ONE argument,
so the registry always resolved to the compile-time constant. **The producer could run correctly
on a schedule forever and this page would still render nothing.** Census carried from
`0.4.0_DE_ClientPlatform~Z` (11540) as THEIRS, not re-derived.

## 2. WHAT LANDED

| | file | |
|---|---|---|
| `+` | `src/api/endpoints/satelliteRegistry.ts` | the scoped read; one self-contained deletable file |
| `M` | `src/pages/Positioning/Positioning.tsx` | passes the FETCHED books; derives the notice state |
| `M` | `src/pages/Positioning/shared/satelliteSet.ts` | retires `SATELLITE_PENDING_NOTICE` |

## 3. ⛔ THE ROUTE PATH IS MEASURED AT SOURCE, NOT RELAYED

The wire shape reached this seat as
`/api/scoped/advisor-intelligence/platinum/satellites/registry.json`. **That path is WRONG.**

```
shared-advisor-router/index.mjs:95   SATELLITES_PREFIX        = "/api/scoped/satellites/"
                          :96        SATELLITES_REGISTRY_LEAF = "registry.json"
                          :101       SATELLITES_REGISTRY_KEY  = "platinum/satellites/registry.json"
                          :358       request.uri = "/" + SATELLITES_REGISTRY_KEY
```

A DEDICATED prefix, deliberately not nested under `advisor-intelligence` on `1.0.0_SA_CTO~Z`'s
B1 Rule 24(iii) intent-coherence ruling. **Building against the relay would have stood up a
second route.** The correction is recorded in the new file's header so the next reader cannot
repeat it. Key carries NO firm segment: firm resolves to the BUCKET from the JWT-injected
`X-Firm-Id` (`index.mjs:97-100`).

## 4. ACCEPTANCE CRITERIA

### `T8DE-AC1` -- the fetched registry reaches the adapter · **MET**

`Positioning.tsx:280 @d04c1599` passes `satelliteRegistry?.books ?? []`.

**MODELS/ETFS BYTE-UNCHANGED, as a did-not-move control rather than an assertion:**
every removed line in the diff is satellites-only, and the only appearance of `positioningData`
in the diff is as an argument to the satellites adapter. Corroborated at a SECOND layer, with a
different instrument: a models-mode render **matched 1 of 2 fixtures** -- the registry was never
requested, because `enabled: isSatellites` gates the query. `T8DE_render_models.png` shows Models
mode intact (5 books, Benchmark/Relative/Custom toggles, no satellites notice).

### `T8DE-AC2` -- a fetch failure is not an empty registry · **MET, EXHIBITED**

Separated at the **READ SEAM**, where the difference is still visible. The fetcher RAISES on a
non-object body, on `books` absent or not-an-array, and on a null `as_of`. **Anything reaching
the adapter as `[]` is therefore a SERVED empty.** The render then selects its copy from the
QUERY STATUS, never from the emptiness -- which cannot tell the two apart.

| state | evidence | rendered |
|---|---|---|
| served-populated | `T8DE_render_populated.png` | 9 real books |
| served-empty | `T8DE_render_empty.png` | blue: "No satellites to show." |
| fetch failed | `T8DE_render_failed.png` | red: "could not be loaded" -- **never** "no satellites" |

### `T8DE-AC3` -- publish empty, never delete · **MET**

No fallback beneath the read. `?? []` is "nothing fetched yet", not a fallback. An **unexplained**
absence (settled, not errored, no data) is deliberately read as `fetch-failed`: **the axis fails
toward "could not load", never toward "no satellites."**

### `T8DE-AC4` -- `as_of` non-null always, a null RAISES · **MET, EXERCISED**

Fixture: `as_of: null` on an otherwise-valid registry **with all NINE VALID BOOKS present**.

```
sha256  T8DE_render_asofnull.png  92225d65f302069f...  \  BYTE-IDENTICAL
sha256  T8DE_render_failed.png    92225d65f302069f...  /
sha256  T8DE_render_empty.png     e02b1764dfb1fd5b...     distinct
sha256  T8DE_render_populated.png cf9e542541dddd2e...     distinct
```

**The test discriminates:** without the raise, the null-`as_of` fixture is indistinguishable from
`state-populated`. With it, it is byte-identical to a transport failure -- which is the correct
answer, because both are "could not be loaded". Four-way separation provable by hash rather than
by reading the images.

### `T8DE-AC5` -- rendered, not grepped · **MET**

Five screenshots READ, via `/frontend-dev`'s `scripts/ui-smoke.mjs`. Canvas law holds: every
notice is dark text on a light tint, all content sits inside dark Panels, no light text or
ghost-white fill on the silver canvas.

## 5. EVIDENCE VINTAGE

```
registry  opal-data-cot/platinum/satellites/registry.json
          2196 B · ETag c056874e69aa048a616f4e21100cf74a · as_of 2026-08-27 · 9 books
          LastModified 2026-08-28T01:38:46Z   (banked verbatim as registry_artifact_as_served_*.json)
models    opal-data-portal-v2/json/positioning/positioning_data.json  (gzipped, the LIVE served key)
          data_as_of 2026-08-26 · books UST/ST/INT/LT/ULT · current_holdings present
```

⚠ **A FIXTURE ERROR I MADE AND CORRECTED, recorded because the render looked plausible.** I first
used `positioning/positioning_data.json` (no `current_holdings`, non-canonical `LTC`/`LTA` codes)
and before that a hand-written fixture. The hand-written one rendered `AGG 4600.0%` and
`GRAND TOTAL 10000.00`. **That was my fixture's unit error, not a code defect** -- the real
artifact carries `allocation` as PERCENT and `holdings[].weight` as FRACTIONS, mixed units in one
payload, verified at source before attributing anything.

## 6. ⭐ INDEPENDENT ARITHMETIC CHECK -- a different instrument from the screenshot

Every **100%-single-constituent** satellite must reproduce its model book EXACTLY. Measured
across the two renders:

```
Satellite 15  = 100% ST   ->  82.6 / 17.4   ==  Models "Short-Term"        82.6 / 17.4   OK
Satellite 60  = 100% INT  ->  32.8 / 67.2   ==  Models "Intermediate-Term" 32.8 / 67.2   OK
Satellite 80  = 100% LT   ->  12.7 / 87.3   ==  Models "Long-Term"         12.7 / 87.3   OK
Satellite 90  = 100% ULT  ->   8.1 / 91.9   ==  Models "Ultra Long-Term"    8.1 / 91.9   OK
Satellite 15 holdings table:  Fixed Income 82.63 + Equity 17.37 = GRAND TOTAL 100.00
```

The 9-book ladder is monotonic 82.6 -> 8.1 across 15..98, which is what a ST->ULT blend predicts.
**The producer's percentage units are consumed without a client-side conversion**, per the ruling
that the producer converts and the consumer does not move; the consumer's sum check (which
correctly refused all nine books before `48c6a7700f`) still runs and now passes.

## 7. GATES

```
tsc -b --noEmit                  rc=0   -- AND PROVEN ABLE TO FAIL: a planted error in the new
                                          file gave TS2322 rc=2; restored byte-identical (diff -q)
eslint (3 changed files)         rc=0
non-ASCII                        0 lines across all 3 files
commit-gate                      checked 0 of 3 -- it reads only .py/.sh/.tf/org/projects/*.json.
                                 NOT cited as validation; the language-appropriate instruments above are.
```

## 8. NOT DONE, AND NOT MINE

⛔ **The route is committed but NOT DEPLOYED.** Router pinned at v24 (2026-08-21) while the
satellites branch committed 2026-08-27T22:42Z; 0 of 26 cache behaviors mention satellites. So
**against the live plane this seam renders `fetch-failed` today -- correctly.** That is why the
distinction was built now rather than after the apply. Deploy is `POSN_TENANCY.TO-4-AE`, and
`2.0.0_SA_COO~Z`'s 11910 `[STOP]` currently halts it (wiring the route to v24 would ship it DEAD
while every instrument reads GREEN).

Also not mine: the producer · the PROD promote (DT, Rule 19 / `SAT-f-3`) · `D1_CATVIEWS` ·
`ETFS_INGEST`'s condition-(ii) render at `0.4.0_DE_ClientPlatform~Z`.

## 9. SURFACED, NOT CHASED (surprise channel -- OBSERVATION, INERT)

**The adapter's second parameter keeps its default `= SATELLITE_REGISTRY`.** A NEW call site that
omits the registry silently reproduces exactly the defect this TO fixed, and nothing fails --
no compiler error, no runtime error, just an empty page. Removing the default was outside the
ruled seam shape (`TO-8-DE` §2: use the seam, do not redesign it), so it is **recorded at
`satelliteSet.ts` rather than changed.** Owner would be whoever holds the adapter contract.
