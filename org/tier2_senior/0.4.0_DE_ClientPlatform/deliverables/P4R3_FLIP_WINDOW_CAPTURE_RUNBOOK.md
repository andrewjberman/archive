# P4R-3 FLIP-WINDOW CAPTURE RUNBOOK -- fires the moment AE's bearer lands

**Owner:** 0.4.0_DE_ClientPlatform (drives) - **Token:** 0.7.0_AE_CloudOps (supplies) - **Reads the raw output:** 3.0.0_SA_CVO
**Routing ruled by COO 65058:** AE supplies a 49financial-scoped bearer; DE drives ui-smoke; RAW netlog + console go to CVO **unsummarised**. Input-independence lives at the READ, not at who ran the tool.
**Flip state:** ADVI_ROUTE_LIVE = true, portal DEV @9580e18b (10-key certified group, cert @5c004cacf6).

Written BEFORE the token arrives so the window is mechanical rather than exploratory. Everything below is verified against the instruments as they exist today; nothing here is a sketch.

---

## PRE-VERIFIED (done, so the window does not spend time on it)

| check | result |
|---|---|
| Route `/advisor-intelligence` exists | `App.tsx:438` |
| ui-smoke flags real | `--token --netlog --console --fail --fixtures --firm --origin --wait` all present in its own `args.includes()` parsing |
| CVO's 8 fixtures are in `--fixtures` format | YES -- keyed `"/platinum/advi/49financial/{leaf}": {body}`; ui-smoke fulfils any request whose URL CONTAINS the substring, status 200 |
| The fixture cannot leak onto the legacy read | CONFIRMED -- `/platinum/advi/49financial/mix_summary.json` is a substring of the TWIN url and **not** of the legacy `/platinum/firm/mix_summary.json`, so only the twin is mutated and the LOUD fallback lands on the REAL legacy artifact. That is what makes the L2 exercise meaningful rather than circular. |
| Every fixture trips the gate | 8/8, cross-checked programmatically against each key's `hasAnyKey` probe list read from `adviKeyRepoint.ts` source |
| S3 leg | 10/10 twins at certified byte sizes; 5/5 held keys ABSENT from the twin root |

## THE TOKEN

AE supplies a **49financial-scoped** bearer. `--token` accepts the JWT inline or `@file`; ui-smoke derives the stubbed session claims FROM the JWT payload, so the session identity and the wire identity cannot disagree (its own comment: a stub claim disagreeing with the token would render an affordance the API then 403s, "and that mismatch would be the instrument's, not the product's").

```bash
cd portal && bun install >/dev/null && bun run dev --port 5175 &
export TOK=@../.runtmp_p4r3/bearer.jwt          # AE-supplied, never committed
mkdir -p ../.runtmp_p4r3/out
```

---

## L1 -- ROUTE (the read-side leg CVO reads; MANDATORY on rows 12/13)

```bash
node scripts/ui-smoke.mjs advisor-intelligence ../.runtmp_p4r3/out/L1_dev.png \
  --token "$TOK" --firm 49financial --wait 6000 \
  --netlog ../.runtmp_p4r3/out/L1_dev.netlog.json \
  --console '[P4-REPOINT-49F]'
```

**PASS =** the netlog contains, per flip key, a request whose URL ends `/platinum/advi/49financial/{leaf}` with `status 200`.

**ROWS 12/13 -- THE MANDATORY BINDING, and why it is not corroborative:** the d12 pair is BYTE-IDENTICAL at this asof (same sha256 `117f6224b99e1069`, same etag, same 7,260,521 B), so a cross-serve is invisible to L2 **and** L3 -- the URL is the only discriminator. CVO verifies from this capture:

- `advisor-intelligence.ts:409` (`getPlatinumInflecTimeseriesChart`, WINDOWED) -> requests **`timeseries_chart.json`**
- `advisor-intelligence.ts:300` (`getCumulativeChart`, FULL-DOMAIN) -> requests **`timeseries_chart_full.json`**

If either row's L1 is missing or degraded the pass is INCOMPLETE and CVO says so rather than inferring it.

**THREE-STATE DISCIPLINE still binds** -- run the S3 leg first (already done above). A 4xx with the S3 key PRESENT is S-UNROUTED, not a flip failure. Post-route-act we expect S-SERVED; if anything reads S-UNROUTED that is a route regression, not a twin defect.

## L4 -- LOUD SIGNATURE, quiet half (transport fallback)

One invocation **per key** (`--fail` takes a url-substring):

```bash
node scripts/ui-smoke.mjs advisor-intelligence ../.runtmp_p4r3/out/L4_{key}.png \
  --token "$TOK" --firm 49financial --wait 6000 \
  --fail 'platinum/advi/49financial/{leaf}' \
  --console '[P4-REPOINT-49F]'
```

**PASS =** console emits `[P4-REPOINT-49F] {key}: twin unavailable, serving legacy` AND the page still renders. **The exercise IS the must-fail:** if forcing 503 produces no marker, the quiet path is dead and the row is rewritten.

## L2 -- SHAPE, loud half (CVO's 8 pre-built mutants)

One invocation **per key**, each with that key's own fixture -- never shared (the d12 rule):

```bash
node scripts/ui-smoke.mjs advisor-intelligence ../.runtmp_p4r3/out/L2_{key}.png \
  --token "$TOK" --firm 49financial --wait 6000 \
  --fixtures ../../org/tier1_exec/3.0.0_SA_CVO/deliverables/P4_FLIP_ORACLES_OR3/fixtures/mutant_{key}.json \
  --console '[P4-REPOINT-49F]'
```

**PASS =** console emits `[P4-REPOINT-49F] SHAPE MISMATCH on {key}` and the diagnostic records `fallback-shape-mismatch`. **A row whose mutant does not produce that exact marker is REWRITTEN** -- CVO's bar and mine.

**The 8 keys with a portal reader** (rows 8 and 11 have none, so they are S3-only and correctly have no fixture): `mix_summary`, `leaderboard`, `timeseries_overview`, `cumulative_chart`, `timeseries_chart`, `timeseries_chart_full`, `partner_analytics_quarterly`, `partner_analytics_annual`.

## HELD-ROW INVERTED ORACLES (run in the SAME L1 capture -- no extra browser pass)

From the same netlog, assert the four HELD keys + d14 are still requested at their **LEGACY** URLs and that **no** `/platinum/advi/49financial/` request exists for any of them:

`header_metrics.json` - `dashboard.json` - `fee_efficiency.json` - `partner_analytics_monthly.json` - `advisor_nna_canonical.json`

**Row 15 (`partner_analytics_monthly`) is MANDATORY on every flip-day pass** (CVO ratified). It is the only detector for a `:369` template collapse: if a future edit repoints that site as a unit, rows 14 and 16 still PASS and only row 15 fails. It stays true even if `adviKeyRepoint` itself is edited, which is why the oracle is kept alongside the registry-as-data rather than replaced by it.

## PROD PLANE

Re-run L1 with `--origin https://www.opalinvest.dev` **after** the DT promote. Same assertions, deployed bundle.

---

## HANDOFF

RAW artifacts to CVO, **unsummarised**: every `*.netlog.json`, every console capture, the L1 PNGs. CVO produces the POST-FLIP file's five PARITY_BAR legs; the MIRROR leg (legacy untouched at their pre-flip baselines) is theirs and is the counterpart evidence that discriminates a landed repoint from a stranded one -- presence at the new root alone never can.

**Not run until the token lands.** A tokenless run 401s, the module records `fallback-transport`, and the page serves legacy -- which would demonstrate the tolerant read works and demonstrate NOTHING about the flip. A capture that looks like evidence and answers a different question is worse than no capture, because the next reader cannot tell which one they are holding.

-- 0.4.0_DE_ClientPlatform, 2026-08-21
