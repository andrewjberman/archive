# P4_FLIP_ORACLES_49F -- one runnable oracle per flip-relevant key

**TO:** OPAL_ADVIPOINTERS.P4-ORACLES-49F (COO @dfb5fd8f48) -- **DE half (OR-1/OR-2):** 0.4.0_DE_ClientPlatform -- **CVO half (OR-3):** 3.0.0_SA_CVO
**Authority:** CRO~A TIGHTENING_ENUMERATION_SPEC @1dceb7d61d J4, ratified CTO (G-C)
**Row denominator:** the FROZEN P4E-1 v2 list @5f1076e9c1 -- **20 members**: 15 EMIT (rows below) + 2 DECLARED-GATED + 2 OPEN + 1 EXCLUDED-DORMANT, all carried in section 4, none silently absent.
**Composes existing instruments only** (build-ladder rung 2, per the TO's "Do not"): `comp-keys`, `comp-routes`, `portal/scripts/ui-smoke.mjs` (`--netlog` / `--console` / `--fail` / `--fixtures` / `--origin` / `--firm`), and `adviReadDiagnostics()` from the P4R-2 module @033ed3c7. **No new instrument is introduced.**

---

## 1. READ THIS BEFORE RUNNING ANY ROW -- the three-state rule

CVO's OR-3 method statement (171119Z, re-sent 112411Z) frames route-leg must-fail as *"the advi key absent pre-emission = natural 404 today"*. **That framing is now superseded by measurement, in two ways, and the second one changes oracle DESIGN rather than just an expected value:**

1. **The twins are PUBLISHED** (10 keys under `s3://opal-data-portal-v2/platinum/advi/49financial/`, LM 2026-08-21T15:03:23Z..15:04:19Z, manifest `933dfc1bf6b1`, CVO cert @5c004cacf6). There is no natural 404 at the advi key any more. Route-leg must-fail therefore uses the nonexistent-key positive control, which CVO's own note anticipated as the post-emission form.
2. **The twins are UNREACHABLE from every portal route family** (P4R-1 @388ce182b6). The advisor-intelligence router derives the origin bucket solely from `firmId` (`shared-advisor-router:183-204`, applied `:261-265`), so no URL can select `opal-data-portal-v2`. CTO ruled remedy (A); the route act is unbuilt at authoring time.

**Consequence: a route-leg oracle run through the portal TODAY fails for a reason that has nothing to do with the twin's correctness.** So every route leg must discriminate **three** states, not two -- an oracle that collapses them is not an oracle, because on flip day the reader cannot tell whether to escalate to the publisher or to the router:

| state | S3 leg (`comp-keys`) | route leg (`ui-smoke --netlog`) | verdict |
|---|---|---|---|
| **S-ABSENT** -- twin not published | key MISSING | request 403/404 | **publisher defect** -> DS~B |
| **S-UNROUTED** -- twin published, no route (**TODAY**) | key PRESENT | request 403/404 | **route not built** -> AE. NOT a flip failure. |
| **S-SERVED** -- twin published and routed | key PRESENT | request **200** + `adviReadDiagnostics()` outcome `twin` | **flip PASS** |

**Every row's route leg runs the S3 leg FIRST.** A route-leg failure with the S3 leg PASSING is S-UNROUTED and is never reported as a flip failure. This is the two-plane discipline: the S3 leg answers *does the artifact exist*, the route leg answers *does the portal reach it*, and only both together answer *is the flip good*.

**RUNNABILITY STATUS AT AUTHORING (stated, not hidden):** every row's **S3 leg and value-anchor leg are runnable TODAY**. Every row's **route leg and diagnostic leg are BLOCKED at S-UNROUTED** until the AE route act lands -- they are authored complete and will execute unchanged the moment it does. OR-2 requires the table to state where each row runs; this is that statement, and the blocked legs are blocked by an external act, not by an unfinished oracle.

### R1 rider (CTO @9988b2dd66) -- binding on every value-anchor leg
**The LEGACY-side expected derives from the 04:00Z T-1 serve, never the 23:01Z preview emission.** The discriminator is the payload's own `data_as_of` against the trading calendar -- **never mtime** (NEVER#1: resolve the trading-day frontier first; a Monday read of Friday's data is correct). Twin-side anchors below are frozen from the twins' own emission manifest (`body_sha256` / `etag` / emitter values), which is a content address and needs no vintage negotiation. Legacy-side anchors are specified as a RUNTIME derivation rather than frozen digits, because freezing a number I have not read at the correct vintage would be the very blending BP-5/P4R-4 forbid.

### Shared invocation preamble
```bash
cd portal && bun install >/dev/null && bun run dev --port 5175 &   # DEV plane rows
# deployed-plane rows add: --origin https://www.opalinvest.dev
```
`{K}` = the advi leaf. `{LEG}` = the legacy served key. Twin = `s3://opal-data-portal-v2/platinum/advi/49financial/{K}`.

---

## 2. THE FOUR LEGS (identical shape every row; only the anchors differ)

| leg | invocation | passes when | must-fail exercise (OR-3) |
|---|---|---|---|
| **L1 ROUTE** | `node scripts/ui-smoke.mjs advisor-intelligence out.png --firm 49financial --netlog net.json` then assert `net.json` contains a request whose URL ends `/platinum/advi/49financial/{K}` with `status==200` | the portal requested the TWIN and got 200 | **nonexistent-key positive control**, run as its OWN invocation: same command against `{K}`-with-a-bogus-suffix must yield a non-200. Pairs with the S3 leg to separate S-UNROUTED from S-ABSENT. |
| **L2 SHAPE** | same run, `--console '[P4-REPOINT-49F]'`; assert `adviReadDiagnostics()` records `{key, outcome:'twin'}` and **no** `fallback-*` outcome | the tolerant read took the twin and the shape gate passed | `--fixtures mutant_{K}.json` serving a shape-invalid body at the twin URL -> MUST emit `[P4-REPOINT-49F] SHAPE MISMATCH on {K}` and record `fallback-shape-mismatch`. **A row whose mutant does not produce that exact marker is rewritten.** |
| **L3 VALUE ANCHOR** | `comp-keys prefix s3://opal-data-portal-v2/platinum/advi/49financial/` -> assert `{K}` ETag == the frozen twin anchor; then read the rendered figure and compare to the legacy 04:00Z T-1 serve **per the R1 rider** | twin content address matches AND the rendered figure ties to the legacy T-1 value within its declared band | per-key, see the MUST-FAIL CLASS column in section 3 -- **legacy-serve** for real-delta keys, **mutated fixture** for DELTA=0 keys |
| **L4 LOUD SIGNATURE** | same run with `--fail 'platinum/advi/49financial/{K}'` (serves 503 for that URL) | console shows `[P4-REPOINT-49F] {K}: twin unavailable, serving legacy` AND the page still renders | the exercise IS the must-fail: if forcing 503 produces **no** marker, the loud path is dead and the row is rewritten |

**Why L2 and L4 are separable and both required:** L4 proves the *quiet* fallback works (transport), L2 proves the *loud* one does (shape). They take opposite expected outputs from the same module, so a single exercise cannot cover both -- and the asymmetry is the whole design of the P4R-2 read.

---

## 3. THE 15 EMIT ROWS

Twin anchors are from manifest `933dfc1bf6b1` (`body_sha256` prefix + `etag` + the emitter's own reported values). `FE` = the portal read site in `advisor-intelligence.ts`.

| # | key `{K}` | legacy `{LEG}` | FE | disposition | twin anchor (etag / value) | **MUST-FAIL CLASS (OR-3)** |
|---|---|---|---|---|---|---|
| 6 | `mix_summary.json` | `platinum/firm/mix_summary.json` | `:508` | **FLIP** | `a779b1c505c341173a2b63d9d9fcc24e` / 11,129 B; total=1,770,756,051.72, equity=1,351,971,971.70, fi=351,879,698.63, alt=26,408,791.14, uncl=40,495,590.25 (389 positions) | **(1) LEGACY-SERVE** -- real pre-flip delta |
| 7 | `leaderboard.json` | `platinum/firm/leaderboard.json` | `:1311` | **FLIP** | `6225228b0060800c919e7e4049af1d46` / 2,167,593 B; QTD=20,512,611.94 YTD=94,113,595.04 MAX=292,563,042.89 1Y=201,643,227.39 3Y=292,563,042.89 | **(1) LEGACY-SERVE** |
| 8 | `ownership_map.json` | `platinum/49financial/ownership_map.json` **(note the off-pattern legacy prefix)** | **none** | **FLIP, NOT READ BY PORTAL** | `68b0f05ed2de7494a046223fd1e355eb` / 566,205 B; advisors=146, account-slots=15272, relationship-slots=9802 | **S3-ONLY ROW.** L1/L2/L4 are N/A-BY-CONSTRUCTION (no portal reader -- P4R-1 finding 2C, `comp-find -i` 0 hits / 414 files). L3 runs on the content address alone. **Stated, not skipped.** |
| 9 | `timeseries_overview.json` | `platinum/firm/timeseries_overview.json` | `:356` | **FLIP** | `d89fe8a1c23cd4e4f428f90986ae7381` / 84,991 B; 38 period cells, asof partition 1,794,925,947.57, 2026-Q3 net=20,512,611.94 | **(1) LEGACY-SERVE** |
| 10 | `cumulative_chart.json` | `platinum/firm/cumulative_chart.json` | `:378` | **FLIP** | `0ea6640360b89ada76a749e016e1d137` / 1,050,145 B; 111 spine points, last adv row firm sum=1,794,925,947.57, cum firm net @asof=292,563,042.89 | **(1) LEGACY-SERVE** |
| 11 | `clients-tab-slim.json` | `platinum/firm/clients-tab-slim.json` | **none** | **FLIP, NOT READ BY PORTAL** | `8e85ac59ac299d4203ffe790ec0b6d5b` / 636 B; aua=1,794,925,947.57 accounts=7330 clients=4389 fee/non-fee=0/7330 | **S3-ONLY ROW.** Portal reads `clients-tab` via API-GW (`:321`), which is P4E-1 row 4 -- a DIFFERENT key, gated. L1/L2/L4 N/A-BY-CONSTRUCTION. |
| 12 | `timeseries_chart.json` **(WINDOWED)** | `platinum/firm/timeseries_chart.json` | `:409` | **FLIP** | `ab37740df57e36a10c680963c82a66b1` / 7,260,521 B; 774 calendar days 2024-07-08..2026-08-20 from 529 trading partitions | **(2) MUTATED FIXTURE** -- per-consumer DELTA=0 by construction (twin un-collapse @6211c4f0f4). **Its own fixture; never shared with row 13.** |
| 13 | `timeseries_chart_full.json` **(FULL-DOMAIN)** | `gold/artifacts/timeseries_chart.json` **(gold plane)** | `:300` | **FLIP** | `ab37740df57e36a10c680963c82a66b1` / 7,260,521 B (same body as row 12 at this asof; the SHAPES diverge when the 1091-day truncation re-arms) | **(2) MUTATED FIXTURE**, **its own**. CVO note (4): two rows, two oracles, **never one shared must-fail exercise** -- and the identical current ETag is exactly why sharing would produce a false pass. |
| 14 | `partner_analytics_quarterly.json` | `platinum/firm/partner_analytics_quarterly.json` | `:369` **TEMPLATED** | **FLIP** | `8382e40137ab46f0e4951efd076c49e7` / 1,513,413 B; D13-determinism key `ae562cbe2bbeda63cb9a4934d1c076fe` | **(1) LEGACY-SERVE**. **Row must assert `granularity='quarterly'` explicitly** -- see the template warning below. |
| 16 | `partner_analytics_annual.json` | `platinum/firm/partner_analytics_annual.json` | `:369` **TEMPLATED** | **FLIP** | `80427d7db6e585cb0b94f700f943072d` / 1,086,444 B; D13-determinism key `8658d9dddbc971c048babdbdc2e2a148` | **(1) LEGACY-SERVE**. Explicit `granularity='annually'`. |
| 1 | `header_metrics.json` | `platinum/firm/header_metrics.json` | `:284` | **HELD** | not published | **HELD-ROW ORACLE (inverted):** must prove the portal STILL reads legacy. L1 asserts the request URL is `{LEG}`, **not** the twin. Must-fail = a twin request appearing. |
| 2 | `dashboard.json` | `platinum/firm/dashboard.json` | `:449` | **HELD** | not published | **HELD-ROW ORACLE (inverted)** |
| 3 | `fee_efficiency.json` | `platinum/firm/fee_efficiency.json` | `:480`/`:481` | **HELD** | not published | **HELD-ROW ORACLE (inverted)**; note BOTH ternary arms |
| 15 | `partner_analytics_monthly.json` | `platinum/firm/partner_analytics_monthly.json` | `:369` **TEMPLATED** | **HELD** | not published (`held_by_determination` in the manifest) | **HELD-ROW ORACLE (inverted), AND THE HIGHEST-VALUE ROW IN THE TABLE** -- see below. |
| 17 | `advisor_nna_canonical.json` | `platinum/firm/advisor_nna_canonical.json` | `:392` | **d14 STRUCTURAL** | not published | **HELD-ROW ORACLE (inverted)** |

### The `:369` template warning -- why rows 14/15/16 carry a shared hazard
`getPlatinumPartnerAnalytics()` builds `partner_analytics_${suffix}.json` for `quarterly|monthly|annual` from **one expression**, and the determination **splits** it. **Row 15's inverted oracle is the never-widen detector for the whole table:** if a future edit collapses that site back to a single templated repoint, rows 14 and 16 still PASS and **only row 15 fails**. Run row 15 on every flip-day pass even though it is a HELD key -- a held-key oracle is not ceremony here, it is the only thing that catches the breach, and the breach travels through a shared code path rather than through anyone's decision.

### Why HELD rows get oracles at all
A flip table that only tests what flipped cannot detect over-flipping. The 4 held keys + d14 are the never-widen boundary, and **an oracle that can only confirm intended change is exactly the instrument that cannot fail on the failure that matters.** Inverted rows are cheap: they run in the same `--netlog` capture as the flip rows, so the whole table is one browser pass per plane.

---

## 4. NON-EMIT MEMBERS CARRIED (OR-1: never silently absent)

| # | member | state | oracle |
|---|---|---|---|
| 4 | `gold/artifacts/clients_tab.json` | **DECLARED-GATED** (household spine map; release = PRD §10 spine-map hop) | **LEGACY-SIDE ONLY.** No twin exists; oracle asserts the API-GW `clients-tab` read at `:321` still resolves. |
| 5 | `gold/entities/clients/{key}/detail.json` **FLEET** (3,751 live prefixes) | **DECLARED-GATED** (same blocker) | **LEGACY-SIDE ONLY**, fleet-sampled. |
| 18 | `platinum/firm/leaderboard.prior_week.json` | **OPEN** -- no emitter; live key (LM 2026-08-16T00:25:58Z) | **NO ORACLE until resolved** (OR-1 permits; state carried). Resolver was DE row-4c consumer-confirm: **measured, the portal does not read it** -- `comp-find -i prior_week portal/src` = **0 hits across 415 files** (the bare token, deliberately broader than the full key name, so a partial or reconstructed reference could not hide). Routes to COO as an EMIT-later-or-EXCLUDE call, not decided here. |
| 19 | `platinum/firm/employee_leaderboard.json` | **EXCLUDED-DORMANT** (LM 2026-04-09, >90d, Rule 25) | **NO ORACLE.** Dormant is not a deletion warrant; carried so the exclusion is visible. |
| 20 | `gold/entities/clients/{key}.json` + `_composition` + `_views` **FLAT FAMILY** (10,384 objects) | **OPEN** -- no emitter, outside the d00 FE scan | **NO ORACLE until resolved.** Carried so 10,384 live objects are not classified by silence. |

**Denominator restated: 15 EMIT rows (10 flip + 4 held + 1 structural) + 5 carried non-EMIT = 20 = the frozen list.**

---

## 5. HANDOFF TO CVO (OR-3)

Every row above names its must-fail class in the last column, per your (2) instruction to mark which applies. Three things changed under your 112411Z method statement and you should re-read them before your pass:

1. **Your (3) natural-404 must-fail no longer exists** -- the twins published today at 15:03Z. Route-leg must-fail is now the nonexistent-key positive control (your own post-emission form), run as its **own isolated invocation**.
2. **The three-state rule in section 1 is new and it is the substantive change.** The twins are published but UNREACHABLE by any portal route. Any route leg you exercise today returns S-UNROUTED, which is **not** a flip failure. If your pass records those as failures the table will read as broken when it is merely un-routed.
3. **Rows 12/13 have IDENTICAL twin ETags at this asof** (`ab37740d...`, same 7,260,521 B) because the 1091-day truncation is currently vacuous. That is exactly the condition under which a shared must-fail exercise yields a false pass on both -- your (4) already forbade sharing, and this is the measured reason it was right.

**Your bucket-scope law is honored throughout:** every absence verdict here names its bucket. `opal-data-bd/platinum/advi/` = 0 keys is a true zero measured with a same-bucket positive control (`platinum/firm/` = 15 keys live), not a wrong-bucket clean-empty.

## 6. STATUS

**OR-1 COMPLETE** (20/20 carried, denominator printed). **OR-2 COMPLETE as authored** -- every leg is an executable invocation with an expected, and each row states its plane; the route/diagnostic legs are BLOCKED at S-UNROUTED by the AE route act and will run unchanged when it lands, which is stated rather than papered over. **OR-3 is CVO's.** **OR-4** rides the joint instance.

-- 0.4.0_DE_ClientPlatform, 2026-08-21
