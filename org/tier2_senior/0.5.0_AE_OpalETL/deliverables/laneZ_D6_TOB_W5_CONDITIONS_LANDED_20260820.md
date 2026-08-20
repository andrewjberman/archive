# D6 TO-B / W5 — the SIX certification conditions + merged-definition amendments (i)–(vii): LANDED

**Seat:** `0.5.0_AE_OpalETL~Z` · **Date:** 2026-08-20 (13:0x–13:4xZ) · **archetype:** IMPLEMENT
**Against:** CVO~Z CERTIFIED-CONDITIONAL verdict + co-sign, `org/tier1_exec/3.0.0_SA_CVO/deliverables/CVOZ_W5_V02_CERT_AND_MERGED_DEFINITION_COSIGN_20260820.md` @9b859ca898 (six conditions, each with its one-line re-read test; seven amendments, each measured). Nothing here is a new gate: the conditions are measured defects, corrected; the port contract executes unchanged on the corrected artifact.

## The re-read tests, run here as one script (CVO~Z's own one-liners)

| # | condition | CVO~Z re-read test | result here |
|---|---|---|---|
| 1 | `vintage_field` = FIELD / DOTTED PATH / explicit `NONE -- L-11 reason`, never a prose pointer | rows with `vintage_field` starting `SEE-` == 0 | **PASS — 0 of 36** (explicit `NONE -- L-11` on 5: manifests, archive, json/mdpf legacy, news history x2; field census = `data_as_of`, `as_of`, `as_of_date`, `as_of_last`, `as_of_month`, `generated_at`, `period`, `value_date`, `_provenance.source_vintages...`). AUTHORED for 13 rows from a LIVE top-level-keys read of the artifacts (2026-08-20): ft.02/ft.03/mac.03/mkt.02/cor.01 carry `data_as_of`; mac.02 members carry `as_of` (gzip body; PRD 8.2 confirmed); news.03 singletons carry `generated_at`; mp.12 = `value_date` (L-8). **The emitter now REFUSES (rc 2) any row without one** — mutant control FIRED. |
| 2 | twin rows bear the LATEST certified twin's cells; superseded twins named | for each `same_object_as` row: row entity == latest stamp in the set; `twin_semantics_superseded` lists the others | **PASS — 3/3**: `json/positioning/positioning_data.json` → `att.04@1834Z` (pos.01@1818Z superseded) · `json/positioning/holdings_attribution_data.json` → `att.02@1834Z` (pos.02 superseded) · `json/portfolios/aum-metrics.json` → `ft.04@1855Z` (pos.03@1818Z, att.03@1834Z superseded); `pages:` UNION (`/attribution, /positioning[, /factor-tilts]`); `twin_resolution:` names the rule and the differing fields. The holdings_attribution row's canonical name now carries the key's real basename; the aum-metrics row's consumer set is the K8-informed one. |
| 3 | L-1 mutual disambiguation on the aum-metrics pair | both rows' text contains the other key | **PASS** — `disambiguation:` on `platinum/mdpf/{scope}/aum-metrics.json` names `json/portfolios/aum-metrics.json` and vice versa. |
| 4 | `accessors:` as a LIST field | present on 36/36; aum-metrics lists both accessors with modules | **PASS — 36/36** (12 empty-by-measurement: rows no portal accessor names); `json/portfolios/aum-metrics.json` → `[getAUMMetrics (@/api/endpoints/aum), getAUMSummary (@/api/endpoints/aum \| @/api/portal-proxy)]` — L-2's two accessors; names resolved against portal/src/api exports (125 across 14 endpoint modules + portal-proxy), every exporting module named, unresolved names carried as `accessors_unresolved` (0 today). |
| 5 | `census_ref` per row + `semantics_provenance` carrier | count(present or explicit NONE) == 36; carrier present | **PASS — 36/36** (30 `{file, page, key}` by KEY PRESENCE in the page census; 6 explicit `NONE -- uncensused (L-14)`: smartx daily/monthly (pages []), mkt.01/mkt.02 (/market uncensused), archive, json/mdpf legacy) + `semantics_provenance:` header block (authority / serial / merged_definition / andrew_verbatim_outranks) + per row 36/36 (certified run + substrate incl. `correction:` where applied). |
| 6 | TO-B proof-of-spec instance VALID rc=0 positional | instance path named; checker rc=0 unpiped; id set printed | **AUTHORED** `deliverables/D6_ANALYST.TO-CDBFG-SITEZ_PROOF_OF_SPEC.json`, ids D6-1..D6-6 — checker rc recorded below at commit time. |

## The merged definition, as re-run (amendments i–vii)

`python workflows/atom_decomposition/lift_catalog_v02.py --report` (git HEAD at run; byte-identical across two runs):
```
entities=46 rect_cells=460 rect_planeBC_MEASURED=250 rect_planeBC_NOT_MEASURABLE=2 rect_planeBC_UNMEASURED=24 rect_planeBC_OTHER=0
sidecar_cells=156 sidecar_placed=0 sidecar_blocked_equal=156 sidecar_blocked_differ=0 nm_vs_sidecar=0 sidecar_vs_sidecar=0
correction_cells=2 cross_plane=0 malformed=0 named_exceptions=0
MERGED COUNT = 89 of 276 resolved Plane-B/C cells
PREDICATE    = resolved Plane-B/C cell whose evidence.instrument / evidence.locator / evidence.provenance / cell.provenance
               matches /CVO.{0,3}DELEGATED|CVO~Z delegated/i (STRUCTURAL named-evidence-field test, amendment vi)
CORRECTIONS APPLIED (2 -- their own substrate class, NOT named exceptions): cor.01 analyst_serve_verdict + vintage_semantics
TWIN-SUPERSEDES DECLARATIONS (amendment v explicit override; 0)
NAMED EXCEPTIONS (0)
```
Every number equals the certifier's measured basis (156/156 blocked value-equal, 0 NOT_MEASURABLE targets, 0 cross-plane, 2 correction cells, proxy 89/276 — now structural); `named_exceptions=0` beside a correction list of 2 is now **honest** (the two applications print under their own heading). Corrections key on the STRUCTURED `supersedes` array; a payload≠named set, a missing named file, or missing keys **REFUSES THE UNIT** (three synthetic cases fire). A cross-unit `supersedes` item is a twin-supersedes DECLARATION handed to the emitter (amendment v's explicit override) — implemented, 0 live instances, exercised on a synthetic unit.

## Exercise ledger (all re-run AFTER the changes)
- synthetic merged-definition battery `workflows/atom_decomposition/tests/test_merged_definition.py`: **12/12 OK** (every amendment's refusal/naming path on a constructed unit).
- query→route battery: **40/40 rc=0** (incl. the W6 scope-family-firm case).
- LIVE S3 validate: **rows=36 concrete_ok=26 concrete_missing=0 family_ok=10 family_mismatch_or_error=0 rc=0**.
- determinism: **emit byte-identical x2; lift report byte-identical x2**; `git status runs/` = **0** (certified artifacts untouched).
- condition-1 mutant (drop one authored `VINTAGE_FIELD`, in-process, scratch OUT): **rc=2 REFUSED, nothing written, real catalog sha256 unchanged**; positive control rc=0, scratch emission sha256 == staged catalog.
- commit-gate: clean on lift / emit / tests (py_compile + ruff py39).

## Stated, not silent
- The first patch run **truncated `emit_catalog_v02.py` to 0 bytes** (`open(p,'w',newline=...)` truncates before validating `newline`); restored from HEAD, corrected patch applied — no content lost.
- `getAUMSummary` is exported by TWO modules; the row carries both rather than a first-pick.
- The TO-C/TO-D report's "16 channels" was wrong — **15**; the emitter prints its count.
- Condition 6's checker rc: see below.
- What this does NOT do: no port (laptop lane), no catalog_gate change, no monitors, no widening.

## Checker result (condition 6)
`python .tools/proof-of-spec-check.py org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D6_ANALYST.TO-CDBFG-SITEZ_PROOF_OF_SPEC.json D6-1,D6-2,D6-3,D6-4,D6-5,D6-6` -> **rc=0 (unpiped), structural=jsonschema, acceptance rows=6, violations=0, VALID**. (First run rc=1: artifact-coverage -- the emitter was not NAMED in any acceptance row's invocation; the D6-1 invocation now names the emit command. The checker did its job: a row that exercised the emitter without naming it would have read as uncovered.)
