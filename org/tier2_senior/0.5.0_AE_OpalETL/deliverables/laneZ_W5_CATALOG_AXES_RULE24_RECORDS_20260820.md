# DATA_CATALOG v0.2 — Rule-24 records for the FIVE labeled axes the staged catalog enumerates

**Seat:** `0.5.0_AE_OpalETL~Z` · **Date:** 2026-08-20 ~13:5xZ · **Why now:** Andrew-direct ~1315Z widened Rule 24 to ALL schema enumeration incl. value-adds + adoption (@1ab080d864; cite from the ref @44266af516). CVO~Z's W5 re-read @609182ae0d holds the v0.2 PORT on these five records + condition 7. **Law:** CLAUDE.md Rule 24 — (i) MECE · (ii) same grain · (iii) intent coherence · (iv) state coherence (a stability frame: name the values that do NOT move together). A violating schema is a defect, not a style choice — **and a record that NAMES the failure, the remedy and the consumer is a complete Rule-24 act even when the remedy is sequenced** (COO~Z 2249, CTO~Z 2252, CVO~Z 2255).

**Consumers, grounded at source (this is the line CVO~Z asked for, and it corrects one premise):** `infra/aws/ec2/opal-gateway/app/graphql_plumbing/catalog_gate.py` READS **four** of the five axes — `verdict_class` (rule 2, `:90-93`: only `serve`/`serve-with-caveat` pass), `allowlist` (rule 3, `:94-95`: must start with `ALLOWLISTED`), `firm` (rule 5, `:96-115`: `per-scope` → key-scope branch; else `row_firm != principal_firm` → deny), and `family.axis` (`:70-71`: `"{scope}" in key and axis == "scope"` → per-key expansion at the gate). My own TO-F proof's mutant (`mkt.02 verdict_class deny→serve` → `allowed=True`) measured the verdict_class coupling on 08-19. **Only `vintage_grain` has no gate consumer** (consumer: the Analyst concierge, TEAMS_DUTY vintage-on-every-figure). So any reshape of verdict_class / firm / family.axis / allowlist is a gate-predicate touch by construction → versioned, consumers-first, battery + CTO~Z P1/P2/P7/P8 re-exercised at port.

**Token-hygiene census (word boundary, `python .tools/comp-estate --definitions`, 67-line ratified SYSTEM_DEFINITIONS registry, 20 tokens probed):** 18 of 20 tokens = 0 hits. **`scope` = 2 hits, and it is a REAL collision with a `reserved_ratified` term** — registry line 13: *"Scope [reserved_ratified] +a_token_cannot_carry_its_rail — the set an assertion ranges over, the type_tuple sense ONLY; enum [estate, tree, …]"*. The catalog's `family.axis: scope` / `firm: per-scope` use the token in the MDPF PATH-GRAMMAR sense — the `{scope}` segment of `platinum/mdpf/{scope}/…` — which is itself estate-ratified (CLAUDE.md 17b: `…/gold/{product}/{scope}/`). **Two ratified senses of one token, pre-existing at the estate level; the catalog inherits the path grammar's token and cannot rename a key segment. FLAGGED to the definitions owner (CVO~Z / CTO~Z) as a registry-level collision, not resolved here** — the remedy for the `firm` axis below (`per-scope` → `firm_resolution: key-scope-segment`) removes the `per-scope` coinage from the firm axis but the family axis keeps `scope` because the PATH carries it. `serve` = 1 hit (appears inside a definition's prose, not as a ratified term — read, benign). `global` is a common English token, not a ratified term; the `firm` remedy re-declares its ROLE (`opal-internal` + `scope: all-firms-aggregate`), which also retires the loose token from the firm axis. All tokens ASCII kebab/UPPER; none new at this port.

---

## Axis 1 — `verdict_class` · values {serve 4, serve-with-caveat 21, deny 9, held-at-andrew 2} · 36/36 rows
**Intent:** *may the Analyst serve from this row, and under what caveat.*
| postulate | test | verdict |
|---|---|---|
| (i) MECE | every row carries exactly one; derived mechanically (`verdict_class()` from the CVO cell: RIDES TO ANDREW → held-at-andrew; DENY/BLOCKED → deny; SERVE-WITH-CAVEAT → serve-with-caveat; SERVE → serve; else UNCLASSIFIED(…) which would FAIL the emit on sight). | PASS |
| (ii) same grain | all four are per-ARTIFACT-ROW dispositions. | PASS |
| (iii) intent coherence | **FAIL, NAMED:** `serve` / `serve-with-caveat` / `deny` are DISPOSITIONS; `held-at-andrew` is a routing STATE (who decides) carrying an implicit disposition (not servable until his word) — the rule's own type specimen (*state with disposition*). |  **FAIL (iii)** |
| (iv) state coherence | the three dispositions are RULED (terminal at this vintage); `held-at-andrew` is PENDING — one remedy (his one-line confirm) moves only it. The values do NOT move together. | split NAMED |
**Remedy (RCG-v2 two-field pattern):** `verdict_class ∈ {serve, serve-with-caveat, deny}` + `verdict_state ∈ {ruled, pending-andrew}` (a held row = `deny` + `pending-andrew`, which is what the gate does with it today — rule 2 refuses everything but the two serve values, so the gate's behaviour is UNCHANGED by the split). **Consumer: catalog_gate.py rule 2 (`:90-93`) + the battery's VERDICT-GATE cases (`held-at-andrew` expected on mp.08/mp.12) → co-move in the SAME versioned change.** **SEQUENCED: next versioned change (v0.3), NOT this port** — rationale in the closing section. Until then the record stands as the declared defect; the L-9 `held_at_andrew:` section already carries the two rows explicitly, so no reader is misled about who decides.

## Axis 2 — `firm` · values {opal-internal 30, per-scope 4, global 1, cottonwood 1} · 36/36 rows
**Intent (sec.10.8):** *which principal may see this row — Opal sees all, a firm sees only itself.* **Load-bearing:** catalog_gate rule 5 (CTO~Z O-1; P7 mutant; the w6-scope-family-firm battery case).
| postulate | test | verdict |
|---|---|---|
| (i) MECE | every row carries exactly one, derived from the PREFIX (never the bucket). | PASS |
| (ii) same grain | **FAIL, NAMED:** `opal-internal` / `cottonwood` / `global` are ARTIFACT-grain labels; `per-scope` is a FAMILY-grain RESOLUTION RULE (“the firm is the `{scope}` segment of each member key”) — a rule beside labels. | **FAIL (ii)** |
| (iii) intent coherence | **FAIL, NAMED (CVO~Z's doubt confirmed):** four kinds on one axis — a PRINCIPAL TIER (`opal-internal`), a FIRM (`cottonwood`), an all-firms SCOPE LABEL (`global` — the non-model-assets aggregate, which no single firm may see, so functionally it is Opal-internal visibility with a different name), and a TEMPLATE-RESOLUTION RULE (`per-scope`). | **FAIL (iii)** |
| (iv) state coherence | the gate treats them by three different code paths (`per-scope` branch / `== principal_firm` / everything else denied to firms) — the values do NOT move together under one remedy. | split NAMED |
**Remedy (shape):** `firm` carries principal-tier-or-firm values only: `{opal-internal, cottonwood, 49financial, inflection, …}`; `global` → `opal-internal` + `scope: all-firms-aggregate` (declares the intent: an aggregate no firm may see); `per-scope` → `firm_resolution: key-scope-segment` on the family rows (and `firm:` omitted or `per-member`). **Consumer: catalog_gate.py rule 5 (`:96-115`) — the `row_firm == "per-scope"` branch would read `firm_resolution` instead; P1/P2 (cross-firm member DENY), P7 (firm relabel mutant), P8 (pairwise-disjoint surfaces) + the w6-scope-family-firm case re-exercise at port.** **SEQUENCED: v0.3, WITH the gate, consumers-first** — the gate is the consumer, the catalog the one truth, and they move in ONE versioned change or not at all. At this port the axis is UNCHANGED and the gate's exercise set (40/40 + CVO~Z 4/4 per-scope + CTO~Z P1-P8) guards it as measured.

## Axis 3 — `vintage_grain` · values {date, month, year} + explicit `NONE -- L-11: …` / `NOT_MEASURABLE -- …` · 36/36 rows (condition 7, landed in the same commit)
**Intent (sec.8.2):** *the precision of the artifact's TRUE vintage — the concierge quotes at that grain and never implies day precision the artifact does not carry.*
| postulate | test | verdict |
|---|---|---|
| (i) MECE | one value per row; the three precisions are disjoint and exhaustive over the measured set (L-4: eight field FORMS, three GRAINS — `as_of_month` is month, `assumptions.json` is year, the rest day). | PASS |
| (ii) same grain | per artifact; a family's members share one grain by construction (one producer, one emit). | PASS |
| (iii) intent coherence | precision only; the FIELD name is a different axis (`vintage_field`), the display state (bound / mis-bound / unbound) lives in `vintage_semantics` + the L-11 marker. | PASS |
| (iv) state coherence | `NONE --` (no field exists) and `NOT_MEASURABLE --` (not traced) are ABSENCE/UNKNOWN markers beside three VALUES — the PRD's own convention (L-3: *named explicitly, or the row is incomplete*; L-11) and the rectangle's `status` vocabulary one layer up; they take a different remedy (build a surface / trace the grain) from a value's (none). Named. | split NAMED, by design |
**Consumers:** the concierge only (TEAMS_DUTY: every figure carries its vintage at its grain); no gate predicate. **At this vintage: 36/36 by VALUE** (after this commit's emitter change: the 19 prose cells are carried verbatim as `vintage_grain_notes:`; the value is authored from each cell and cited — CVO~Z's test re-runs clean).

## Axis 4 — `family.axis` · values {slug 1, scope 3, keyword 2, manifest 1, archive 1, legacy 1, singleton 1} · 10 family rows of 36
**Intent:** *how a family's member keys vary — which template segment enumerates the members.*
| postulate | test | verdict |
|---|---|---|
| (i) MECE | each family row carries one. | PASS |
| (ii) same grain | all FAMILY grain. | PASS |
| (iii) intent coherence | **FAIL, NAMED (CVO~Z's doubt confirmed):** `slug` / `scope` / `keyword` name the varying TEMPLATE SEGMENT (the intent); `manifest` / `archive` / `legacy` are CONTENT CLASSES of a `**` prefix-family; `singleton` is a CARDINALITY (an enumerated 2-key list). Three kinds on one axis. | **FAIL (iii)** |
| (iv) state coherence | `validate_catalog_v02.py` expands `{segment}` templates by listing and `**` prefixes by listing — the same mechanism; but the gate's `:70-71` per-key expansion fires ONLY for `axis == "scope"`, so the axis carries a gate-consumed value beside non-consumed ones. Named. | split NAMED |
**Remedy (shape):** `family.axis ∈ {slug, scope, keyword, key-path, key-list}` — `key-path` for `**` prefix families (manifests/archive/legacy: the content class is already carried by the key prefix + `never_serve` + the row's verdict), `key-list` for the enumerated singletons (`declared_members: 2`). **Consumers: catalog_gate.py `:70-71` (the `axis == "scope"` expansion — unchanged by this remedy since `scope` stays), the battery's `w6-scope-family-firm` case (reads `axis == "scope"` — unchanged), `validate_catalog_v02.py` (reads `declared_members` + the key template, not the axis token).** **SEQUENCED: v0.3 with the other reshapes** (no gate predicate moves for this one; bundled so the catalog grammar changes once).

## Axis 5 — `allowlist` · values {ALLOWLISTED 35, BLOCKED-BY-ALLOWLIST 1} · 36/36 rows (reason split out in this commit)
**Intent:** *is the row's key prefix on BUCKET_ALLOWLIST (the permission axis; the catalog cannot grant).*
| postulate | test | verdict |
|---|---|---|
| (i) MECE | binary, derived from the prefix. | PASS |
| (ii) same grain | per row. | PASS |
| (iii) intent coherence | WAS folding a REASON into the value (`BLOCKED-BY-ALLOWLIST (json-tiered/ … needs an Andrew widening)`) — **FIXED IN THIS COMMIT**: `allowlist: BLOCKED-BY-ALLOWLIST` + `allowlist_reason: '…'`. | PASS (after fix) |
| (iv) state coherence | one remedy moves a blocked row (an Andrew widening). | PASS |
**Consumers: catalog_gate.py rule 3 (`:94-95`, `startswith("ALLOWLISTED")` — unchanged by the split) + the battery's VERDICT-GATE `BLOCKED-BY-ALLOWLIST` prefix test (unchanged).** Exercised: battery 40/40 after the split.

---

## Sequencing recommendation (CTO~Z decides; COO~Z flagged the coupling)
**Ride THIS port:** condition 7 (grain by value) + the `allowlist` split — no gate predicate moves, the battery/validate/gate exercise set is unchanged, and both are pure row-grammar corrections of the same class as conditions 1–5.
**Sequence to v0.3 (the next versioned change), consumers-first, WITH catalog_gate:** the three (iii)-failing axes — `verdict_class` (+ `verdict_state`), `firm` (+ `firm_resolution`, `global` re-declared), `family.axis` (`key-path`/`key-list`). Rationale: (a) three gate-consumed axes reshaped inside a port whose contract is *"content REPLACES the live catalog"* would be a gate change riding a content port — exactly the silent-catalog-edit-under-a-banner shape COO~Z and CTO~Z both named; (b) the v0.2 port's value is the six conditions + the EXTEND, certified; (c) each record above is complete now (defect named, remedy shaped, consumer named, exercise set named), so nothing is hidden by sequencing — the catalog's `semantics_provenance` and this record point at each other. If CTO~Z rules the reshape rides this port, the change is: emitter + catalog_gate rule 5/2 + battery VERDICT-GATE/w6 cases in ONE commit, P1-P8 + 40/40 re-run before the port.
