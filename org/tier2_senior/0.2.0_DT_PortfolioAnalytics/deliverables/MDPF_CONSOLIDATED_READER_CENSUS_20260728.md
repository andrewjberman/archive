# CONSOLIDATED READER CENSUS — A / B / C

**Author:** `0.2.0_DT_PortfolioAnalytics` · **Date:** 2026-07-28 ~21:5xZ
**GO:** CTO 213509Z (Andrew-surfaced). Gates the producer re-point (Ruling 1).
**Scope:** census only. No writes, no fixes, no promote.

---

## PREDICATE (stated before the SET, per the GO)

**A "READER" = a code path or live consumer that RETRIEVES the object's CONTENT.**
Counted: `get_object` / `download_file` / `s3 cp` (in) / `aws s3 sync` (in) / an `apiRequest`-family fetch
whose CloudFront path resolves to the key / a configured instrument that reads the object.
**NOT counted as readers** (reported separately): writes, `head-object`, `list-objects`, prose/doc mentions,
operator verification one-liners in runbooks.

**SET, not count** — every reader carries `file:line` (or resource id).
**Absence is a finding** — a prefix with no reader is reported as ZERO with its predicate, never blank.

### METHOD BOUNDS — read these before using any number here
| family | method | completeness |
|---|---|---|
| **A** portal side | RUNTIME capture, deployed PROD, 7 named contexts | strong; **401-gated residual, see below** |
| **A** non-portal side | SOURCE search | **FLOOR** |
| **B, C** | SOURCE search only | **FLOOR BY CONSTRUCTION** |

> **THE RENDER-BACKWARDS METHOD DOES NOT TRANSFER TO B AND C.** It worked for the portal because the
> consumer is a browser I can drive. `platinum/mdpf/*` consumers are BACKEND — there is no render to work
> backwards from. **A source-side enumeration reports completeness over its own pattern**, which is the
> exact class that moved today's count 4 → 5 → 8 → 23. **B and C are FLOORS. Do not read them as complete.**
> **⚠ 401 RESIDUAL, OPEN, STRUCTURAL:** every request in the runtime capture 401s at the edge, so **a fetch
> gated behind a SUCCESSFUL response is invisible to the method.** This is the one hole that could still
> hide a reader. Not closed.

---

# A — `json/mdpf/*` + `json/portfolios/*` (gates the producer re-point)

## A.1 PORTAL READERS — 23-key union, 6 namespaces (delivered `ef18a5fac`)
`json/mdpf/` 8 · `json/portfolios/` 4 · `json/benchmarks/` 2(+1 source-only) · `json/peers/` 1 ·
`json/latest/` 1 · `/api/scoped/advisor-intelligence/` 6.

## A.2 NON-PORTAL READERS — **9 found. THIS IS THE BLAST RADIUS OF THE PRODUCER RE-POINT.**

| # | reader | key read | class |
|---|---|---|---|
| 1 | `data/analysis/fy2025_aggregate_opal_return.py:47` | `json/portfolios/aum-timeseries.json` | **analysis — computes a RETURN figure** |
| 2 | `data/analysis/q1_2026_aggregate_opal_return.py:50` | `json/portfolios/aum-metrics.json` | **analysis — computes a RETURN figure** |
| 3 | `infra/aws/ec2/smartx-exporter/ai-supervisor.py:132` | `json/portfolios/aum-metrics.json` | EC2 supervisor |
| 4 | `infra/aws/ec2/smartx-exporter/ai-supervisor-v2.py:296` | `json/portfolios/aum-metrics.json` | EC2 supervisor |
| 5 | `infra/aws/lambda/infrastructure_monitor/lambda_function.py:90` | `json/portfolios/aum-metrics.json` | monitoring |
| 6 | `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py:569` | `json/mdpf/{firm}/aggregate-aua-timeseries.json` | producer reads the SERVED key |
| 7 | `data/mdpf/scripts/probes/rc1_version_concordance_check.py:63` | `json/mdpf/{firm}/aggregate-aua-timeseries.json` | probe |
| 8 | `data/mdpf/scripts/gold/mdpf_revamp_count_source_audit.py:54` | `json/mdpf/{firm}/aggregate-aua-timeseries.json` | audit |
| 9 | `data/mdpf/scripts/backfill/build_mdpf_count_backfill_pre0518.py:58` | `json/portfolios/aum-timeseries.json` (noncurrent versions) | backfill |
| — | `data/served_freshness_config.yaml:28` | `json/mdpf/aggregate-aua-timeseries.json` | **instrument — SEE A.3** |

> **THE TWO ANALYSIS SCRIPTS ARE THE ONES I WOULD NOT HAVE PREDICTED.** `fy2025_` and `q1_2026_
> aggregate_opal_return.py` compute **firm return figures** off SERVED PORTAL KEYS. A producer re-point
> that changes those keys' basis silently changes a return number in an analysis nobody re-runs.
> **This is the "who else reads the file" gap, and it is not empty.**
> **FLOOR:** source-side only. A notebook, a scheduled job, or an external consumer would be invisible.

## A.3 >> INSTRUMENT-INTEGRITY FINDING: THE SERVED-TIER FRESHNESS CHECK WATCHES A KEY THE PORTAL DOES NOT READ <<

`data/served_freshness_config.yaml:20-28`, verbatim:
```yaml
# WS-4 content-mode on the SERVED tier (json/mdpf/, what the portal actually reads) --
- pipeline: mdpf
  artifact_id: mdpf_served_aggregate_aua_timeseries
  s3_key_prefix: s3://opal-data-portal-v2/json/mdpf/aggregate-aua-timeseries.json   # <-- SCOPE-LESS
  notes: "MDPF served aggregate-AUA timeseries (CloudFront-served tier the portal reads)..."
```

**MEASURED, both halves:**
1. **The portal does NOT read the scope-less key.** Its scope-less client
   (`portal-proxy.ts:505` → wrapper `aum.ts:470`) has **ZERO component callers** — every `.tsx` call is the
   **ByFirm** variant, including `getMdpfAggregateAUATimeSeriesByFirm('global')`
   (`ModelPortfolios.tsx:484,497`) → `json/mdpf/global/aggregate-aua-timeseries.json`.
   The runtime capture confirms: `/api/general/mdpf/global/...` fires; the scope-less path never does.
2. **The scope-less key IS being written** — `json/mdpf/aggregate-aua-timeseries.json`,
   447,154 B, LastModified **2026-07-27T15:10:34Z** — the **~1500Z clobber signature**.

> **So the instrument built to catch the mtime-fresh/content-stale trap on the MDPF custody surface is
> pointed at an object the portal does not serve — and that object was being refreshed daily by the
> clobberer during the exact window the SERVED per-scope artifacts were wrong.** An instrument reading
> FRESH on a key nobody reads, through an incident on the key everybody reads.
> **This is not a freshness-threshold question and it is not alarm wiring** — it is the *"a rigorous
> instrument on the WRONG AXIS survives review"* class (verification law 6), and it is the second time
> today an instrument's own correctness has been the thing hiding the defect (`comp-clobber`
> `ACTIVE_CLOBBER=False` was the first).
> **CTO has already ruled the scope-less key = `global` and re-pointed to `platinum/mdpf/global/...`.
> That ruling silently re-points this instrument too. It should be re-pointed DELIBERATELY, not as a
> side effect** — and someone should decide whether it should watch the per-scope keys instead.
> **I am not adjudicating; the moratorium forbids me building or rewiring monitoring.**

---

# B — `platinum/mdpf/aggregate_aua/{date}.json` · **434 objects** · FLOOR

**READERS FOUND: 1.**
- `data/mdpf/scripts/backfill/build_aggregate_aua_timeseries.py:2` — *"Build the portal-consumed time-series
  rollup of `platinum/mdpf/aggregate_aua/`"* — re-reads the date-keyed set to produce the rollup.
  Corroborated by `data/mdpf/scripts/RUNBOOK_AE_mdpf_daily_chain.md:81` (*"Rollup (Stage 4) re-reads every
  `platinum/mdpf/aggregate_aua/{date}.json`"*).

**NOT readers** (excluded per predicate): `.tools/comp-freshness:1424,1431` (test-fixture strings in a
classifier self-test), `.tools/pipescript:16` (a comment), `RUNBOOK:158-159` (operator verify one-liners),
`.mdpf_restore/legacy0727.json:9635` (a restore manifest recording a source prefix).

> **CTO measured ONE consumer (the DDB emitter) and called it a floor. I independently find ONE (the Stage-4
> rollup). Whether these are the same component I have NOT established** — if they are different, the floor
> is 2. **Reporting the discrepancy rather than reconciling it by assumption.**

# C1 — `platinum/mdpf/etf_ownership_timeseries/{TICKER}.json` · **4 objects** (DIVZ, IDVZ, PFDE, PFOE)

## **READERS FOUND: ZERO.** This is a result, not a blank.
- **Writer only:** `data/mdpf/scripts/gold/build_mdpf_etf_ownership_timeseries.py:70`
  (`OWNERSHIP_PREFIX`, `--upload`), run daily per `RUNBOOK:65-67`.
- **No portal reference.** No `infra/aws/lambda` reference to this prefix.
- **NOT served by CloudFront:** no behavior matches `platinum/*`; the `/api/general/*` behavior rewrites to
  `/json/*`.
- **The `etf_ownership*` hits in `infra/` are a DIFFERENT product** — `etf_ownership_dashboard` /
  `bd_49f_etf_ownership_daily` / `cot_etf_ownership_daily` read `opal-data-etfs/platinum/...`, a different
  bucket and artifact. **Name collision, not a consumer.**

> **4 artifacts produced daily that nothing in the estate reads.** ⚠ **My unauthenticated edge probes
> returned 401 and I am NOT citing them as evidence** — a 401 fires before routing and cannot discriminate a
> real key from a fake one (DE's exercised finding). The **route analysis** is the evidence, not the probe.
> **FLOOR:** an external/manual consumer would be invisible to a source search.

# C2 — bare product-level `platinum/mdpf/aggregate_aua_timeseries.json` · 1 object, 448,246 B

**READERS FOUND: 0 live; 1 PROPOSED, never landed.**
- `data/mdpf/scripts/backfill/HANDOFF_AE_lambda_route.diff:12` / `.md:25` propose
  `serve_s3_json('platinum/mdpf/aggregate_aua_timeseries.json', ...)` — **a handoff diff, not deployed code.**
- Written by `build_aggregate_aua_timeseries.py:10`.
- **The portal client that would have consumed it is the scope-less function — which has ZERO component
  callers (A.3).** So the proposed route's consumer does not exist either.

> **448,246 B is CTO's fourth byte-size** in the aggregate-AUA concept spread. **This is the member with no
> live reader and no landed route** — a product-level artifact whose serving path was drafted and never
> completed, still produced.

## Scoped siblings (completeness of the 446)
`platinum/mdpf/{global,49financial,inflection}/aggregate_aua_timeseries.json` — 3 objects.
**⚠ NO `cottonwood/` under `platinum/mdpf/`. Fourth surface today where cottonwood is absent.**
`platinum/mdpf/_g6_fixture/` — 4 test fixtures (`fresh-all`, `mixed`, `one-stale`, `one-missing`);
**fixtures living in a production prefix**, flagged not adjudicated.
**SET RECONCILES: 434 + 4 + 1 + 3 + 4 = 446** — matches CTO's independent enumeration.

---

## SUMMARY FOR RULING 1's GATE

| family | objects | readers found | class |
|---|---|---|---|
| A `json/mdpf/*` + `json/portfolios/*` | — | **portal 23-key union + 9 non-portal + 1 instrument** | **NOT EMPTY — the gate is real** |
| B `platinum/mdpf/aggregate_aua/` | 434 | **1** (possibly 2, see discrepancy) | FLOOR |
| C1 `etf_ownership_timeseries/` | 4 | **ZERO** | FLOOR |
| C2 bare `aggregate_aua_timeseries.json` | 1 | **ZERO live** (1 proposed, never landed) | FLOOR |

**The producer re-point's non-portal blast radius is at least 9 readers, two of which compute return
figures.** That is the answer to *"nobody has enumerated who those other readers are."*
