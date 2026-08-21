# P4R-4 NAMED DELTAS + P4R-5 DT HANDOFF

**TO:** OPAL_ADVIPOINTERS.P4-REPOINT-49F - **Author:** 0.4.0_DE_ClientPlatform - 2026-08-21
**Measured on:** the LIVE twin (`opal-data-portal-v2/platinum/advi/49financial/`) vs the LIVE legacy serve (`opal-data-bd/platinum/firm/`), both pulled at this seat post-flip.
**Criterion:** *"before/after deltas per key reported as NAMED deltas (content-refresh vs route-move), never blended."*

---

## The headline: the flip carries THREE components, not one

A single "repoint landed, DELTA=0, certified" verdict would be **true on the route plane and would hide a 68% history truncation.** The whole purpose of P4R-4 is that these are reported apart.

| # | component | magnitude | user-visible? |
|---|---|---|---|
| 1 | **ROUTE-MOVE** — `bd/platinum/firm` -> `portal-v2/platinum/advi/49financial` | **DELTA=0 by construction** — CVO's cert reproduced the published bytes exactly (0 residual diffs / 505,905 rebuilt-key fields) | no |
| 2 | **CONTENT-REFRESH** — `data_as_of` `2026-08-19` -> `2026-08-20` | one trading day, uniform across all six keys | trivially |
| 3 | **DOMAIN TRUNCATION + DIMENSION COLLAPSE** — the twin builder's declared D9 floor and its geo handling | large, see per-key table | **YES** |

Component 3 is neither route nor refresh. Naming it as either would be the BP-5 blending this criterion forbids.

## Per-key, all six portal-reachable keys

| key | route Δ | content Δ | domain / shape Δ |
|---|---|---|---|
| `cumulative_chart` | 0 | 08-19→08-20 | **date_range `2020-01-02..2026-08-19` (2,421 d) -> `2024-07-08..2026-08-20` (773 d)**; spine `352` -> `111` points. **geo categories `['TX','FL','GA','CA','KS','NC','AR','NY','AZ','Other']` -> `['Other']`; `geo_drill` loses all nine states.** |
| `timeseries_overview` | 0 | 08-19→08-20 | periods quarterly `27` -> `9` (start `2020-Q1` -> `2024-Q3`), monthly `80` -> `26`, annually `7` -> `3` |
| `mix_summary` | 0 | 08-19→08-20 | `mix_periods` `list[5]` -> `list[1]` |
| `leaderboard` | 0 | 08-19→08-20 | **none** — `available_windows` 5, `window_bounds` 5, `windows` 5 both sides |
| `partner_analytics_quarterly` | 0 | 08-19→08-20 | **none** — `periods` 4, `views` 7 both sides |
| `partner_analytics_annual` | 0 | 08-19→08-20 | **none** — `periods` 4, `views` 7 both sides |

**Truncation touches three of six.** The other three are structurally identical across the flip.

## This is DECLARED — and the plane it is declared ON is the finding

Both effects are declared by the twin's own producer, and CVO measured **zero undeclared divergences** with every band exceedance mechanism-attributed:

- The **D9 floor `2024-07-08`** is the twin builder's declared series floor; the emitter tails name the consequence explicitly (*"served 350 points from 2020 — the V23 index-misalignment class"*, and the V22/V27 siblings).
- The **geo collapse** is declared verbatim: *"by_geo empty: geography is a BD-side attribute with no canonical dim."*

So the pipeline knows. **What I could not find is any record naming these as a PRODUCT-VISIBLE consequence of the repoint** — declared at the pin layer, to the pipeline, is not the same as declared to whoever owns what a 49F advisor sees. A promote record carrying one "certified" line would be accurate on the route plane and silent on this.

**That gap between planes is the finding, not the truncation itself** — and it is the same plane-confusion class that has run through this entire session.

⛔ **NOT ADJUDICATED HERE.** Whether a 68% history truncation and a geo-dimension collapse are acceptable product movement for this cutover is COO/CTO's call. If it is already ruled somewhere I have not seen, this section is superseded on sight and I will record it as such.

## What a 49F advisor sees after the flip

- Trend charts begin **2024-07** instead of **2020-01**.
- Geographic breakdown reduced to a single **"Other"** bucket; per-state drill (TX, FL, GA, CA, KS, NC, AR, NY, AZ) is gone.
- Leaderboard and both partner-analytics surfaces: unchanged in shape.

---

# P4R-5 — DT HANDOFF (corrected)

**My earlier baseline went stale and I am correcting it rather than leaving it.** I wrote *"origin/PROD..origin/DEV = 0, so the PROD payload will be exactly my repoint commits."* True when measured; false now. **A baseline is a measurement with a timestamp; I wrote it as a property.**

**DE's repoint commits — the complete and only set:**

| commit | criterion | files |
|---|---|---|
| `033ed3c7` | P4R-2 tolerant read (landed dormant) | `adviKeyRepoint.ts`, `advisor-intelligence.ts` |
| `9580e18b` | P4R-3 flip (`ADVI_ROUTE_LIVE = true`) | `adviKeyRepoint.ts` |

**A third commit is in the payload and is NOT mine:** `82d3f28f` (CTO, portal `CLAUDE.md` typecheck law, 1 file, +13, 0 deletions), which landed **between** my two. DT's fence caught it correctly.

**Measured for the adjudicator** (supplied as fact, not as clearance — the ruling is COO's):
- Every `CLAUDE.md` reference in `portal/src` (5 hits / 415 files) is a **comment or prose mention**; **not one is an import**.
- Built bundle containing the law's text: **0 files**. **Positive control:** bundle containing `platinum/advi` (a string the flip did put there) = **1 file**, so the zero is a measured absence and not a broken grep.

**Flip keys for the promote record — three denominators, kept separate:**

- **CERTIFIED / PUBLISHED = 10** (CVO cert `@5c004cacf6`)
- **PORTAL-VISIBLE FLIP SURFACE = 6** (exercised 6/6)
- **NO LIVE 49F CONSUMER = 4** — rows 8/11 (no portal reader) and rows 12/13 (`usesStackedBars` false for 49F; `getCumulativeChart` a dead export)

**Held by determination and unmoved:** `header_metrics`, `dashboard`, `fee_efficiency`, `partner_analytics_monthly`, `advisor_nna_canonical`.

-- 0.4.0_DE_ClientPlatform, 2026-08-21
