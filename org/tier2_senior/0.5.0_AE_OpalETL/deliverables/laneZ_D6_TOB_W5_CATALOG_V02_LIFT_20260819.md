# D6_ANALYST.TO-CDBFG-SITEZ row TO-B — the W5 index build (DATA_CATALOG v0.2, staged)
**seat:** 0.5.0_AE_OpalETL~Z · **date:** 2026-08-19 (~20:10–20:45Z) · **TO vintage:** @030b55b295 · **W5 supersede:** @9c7b59f9df · **archetype:** IMPLEMENT
**Binding spec (per the CTO~Z rider 201643Z — the spec rides the artifact):** OPAL_ANALYST_PRD.md §9.6 + §10.1(a–d) + §9.11, PRD @36a7fbd70e-lineage; D6 acceptance rows D6-1/D6-2/D6-3/D6-6.

## What shipped (4 artifacts + 2 markers, all committed to this lane, no push)

| artifact | what it is |
|---|---|
| `workflows/atom_decomposition/lift_catalog_v02.py` | deterministic lift (stage A): verdict-keyed unit resolution over the DECLARED 16-unit denominator; final.certified-only reads; loud refusals; substrate resolution under the merged definition (CVO~Z co-sign pending); §10.1(d) transliteration on read |
| `workflows/atom_decomposition/emit_catalog_v02.py` | stage B: resolved views + authored EMISSION_MAP → the staged catalog; v0.1 routing surface PRESERVED (EXTEND per §8.2); coverage-checked (unmapped entity or stale map entry = refuse to emit) |
| `workflows/atom_decomposition/catalog_v02/DATA_CATALOG.v0.2.staged.yaml` | THE STAGED PORT ARTIFACT — 13 channels (12 preserved + `capital_markets` widening @d2f2e01d9), 36 artifact rows (21 serve-with-caveat / 4 serve / 9 deny / 2 held-at-andrew), F4 named correction, firm first-class key, YAML-parse verified, ASCII-clean by construction |
| `workflows/atom_decomposition/validate_catalog_v02.py` + `catalog_v02/validation_report.json` | stage C LIVE validation: **36/36 rows reachable-by-read; 0 missing; 10/10 families EXACT vs declared** (79/79 macro slugs, 360/360 ×2 news families, 4/4 ×3 MDPF scopes, 2/2 singletons) |
| `workflows/atom_decomposition/battery_catalog_v02.py` | the §9.6 query→route battery: **30/30 pass** (22 positive incl. the widening channel, 2 verdict-gate, 6 negative incl. resolver-floor + loud-refusal controls); misroute class found-and-fixed (stray-token routing → whole-phrase keyword matching) |
| `RUN_DISPOSITION.json` ×2 | the §10.1(c)-authorized markings: cma/1729Z SUPERSEDED-BY-1801Z; security-scanner/0158Z CERTIFIED-ATTEMPT-2 with consume-only-final.certified rule |

## The ruled assertions (D6 acceptance)

- **D6-2 RESOLVER FLOOR — ASSERTED:** the v0.2 catalog contains **ZERO ticket/DDB ticket-surface rows** (battery structural check = 0, exercised), and the staged file's header carries the prohibition verbatim: none may be added until D7 §7.3 lands. Ticket-surface asks measured off-catalog (2 battery negatives, score 0).
- **v0 = TOOLING/YAML over JSON/operational surfaces ONLY** — the catalog rows bind exactly the operational S3/JSON surfaces; **no parquet resolver, no parquet row** (sovereign backing @1e0ec3b079; the D6-3 assertion proper rides TO-E where the resolvers land).
- **THE THREE APPROVED WIDENINGS AND NO OTHERS:** `capital_markets` channel landed in the staged catalog; the PORTAL_RETRIEVAL.md + BUCKET_ALLOWLIST.yaml explicit-line edits are named PORT ACTS in the staged header (they touch live BG refs and land at the certified port). Nothing else widens; `json-tiered/` deliberately NOT added (see finding 2).
- **FIRM AS FIRST-CLASS KEY (§10.8):** every row carries `firm:` derived from the PREFIX (per-scope/global/cottonwood/opal-internal), never a bucket name; routing_procedure step 3 states the sovereign visibility law (Opal sees all; a firm sees itself).
- **LOUD-REFUSAL NEGATIVE CONTROL:** 5 refused units ride the catalog as `refused_units` rows with reasons; battery negatives prove a refused unit's page does not route.

## Findings (surfaced, not chased)

1. **The correction-supersede catch (measured, live consequence avoided):** portal-page-correlations' CERTIFIED rectangle carries the two cor.01 cells its CORRECTION sidecar re-verified as FALSE at the served artifact. A rectangle-wins lift ships false serving semantics. Resolution clause added + applied + named (2 correction cells in the resolved view). Rides the CVO~Z co-sign (amendment 202622Z).
2. **NO SERVABLE MARKET-RETURNS SOURCE:** mkt.01 (the live PRIMARY tiered leg, fresh today) sits on `json-tiered/` — NOT on BUCKET_ALLOWLIST; mkt.02 (`json/market/all_returns.json`) is DENY (LastModified 2026-04-15, live-confirmed; self-reports fresh per L-13). A market-returns ask gets the honest denial until Andrew widens or the fallback is repaired. Carried as a named block in the staged catalog; **decision at Andrew, routed via COO.**
3. **"Never-merged sidecars / overlap zero" reads stale on the live tree:** the 9 sidecar-carrying liftable units' rectangles already carry CVO-delegated Plane-B/C cells (156 sidecar cells block as duplicate-echoes). Surfaced to CVO~Z with the co-sign request; not adjudicated here.
4. **security-scanner certified with semantics ABSENT** (24 UNMEASURED Plane-B/C cells incl. canonical_name) — ships as `absent_semantics_units`, no routable rows until the CVO pen writes the cells.
5. **json/mdpf/ legacy tree is down to 1 object** (live listing) — the v0.1 "older serving mirror" note is nearly moot; hazard note retained.

## Counts (PROVISIONAL until the CVO~Z co-sign)
Resolved view: 46 entities · 460 rectangle cells · 0 sidecar placements · 2 correction cells · 156 duplicate-echo blocks · 2 named exceptions (both = the correction applications). Transliteration: 400+7 replacements over 8+1 codepoints, 0 unknown.

## Port contract (no-shadow law: build → port → delete the stage)
The live `refs/DATA_CATALOG.yaml` was NOT touched. At CVO~Z's W5 certification: staged content replaces the live file + the two sibling widening edits land + the staged file is DELETED. Until then the live catalog is v0.1 and nothing changed live routing tonight.

## Open on this row
- CVO~Z merged-definition co-sign (requested 201927Z, amended 202622Z) — semantics counts finalize on it; structural content does not depend on it.
- TO-F convergence: the resolver-floor + guardrail surfaces here are W6 inputs; coordinate with CTO~Z before authoring TO-F (one artifact serves both).
