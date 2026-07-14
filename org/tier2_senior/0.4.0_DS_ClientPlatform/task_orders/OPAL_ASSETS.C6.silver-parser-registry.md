# OPAL_ASSETS.C6 — Silver parser registry (event-driven, Rule 17 strict)

<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>1.0.0_SA_CTO (OPAL_ASSETS owner)</issued_by>
<date>2026-07-14</date>
<status>pending</status>
<state date="2026-07-14 ~05:0xZ" by="2.0.0_SA_COO (reconciliation)">LANDED: inc-1 Schwab CRS reader on
real 0824 bytes (44a5328ce, 30/30 + guard mutated) + inc-2 raw Orion/Eclipse/INF reader refusing .parquet
under bronze/ (37752c64f, 45/45) -- both RAVC-closed; ruling 11a (T1 hard-raise) binds; conservation-guard
audit ALL SOUND. REMAINING: Orion/Eclipse parser completion + monolith event WIRING (with 0.7.0) + the
completeness law across remaining sources. Pending is correct (assignee-held, external-gated legs).</state>
<hold>ANDREW HOLD 2026-07-14 ~00:25Z, verbatim: "Wait to dispatch until I give the go, I want to respawn the workers first." LIFTED 2026-07-14 ~01:06Z: CTO GO issued to the respawned, roster-verified serial per Andrew's begin-on-readiness protocol (C7 = author half only; C11 remains gated on C3+C6).</hold>
<project>OPAL_ASSETS — Grand Consolidation P2</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4 (TO-C6)</prd>

## Scope
The one parser registry (keyed source+TYPE) converting landed bronze → silver parquet
`silver/{source}/{scope}/{feed}/date=YYYY-MM-DD/data.parquet`. Parsers: Schwab CRS (both masters),
CBUGL **on first real 0833 bytes**, Orion, Eclipse (adds the missing parquet conversion), cot, issuers.
Event-wiring lands when the bucket exists (C1). **Authoring already STARTED per CTO GO 2026-07-14
~00:08Z** — `silver_registry.py` core committed (your `c6ceb25a2` report, 9/9 exercised incl. the
scope_mismatch mutant) — this TO formalizes the record; keep going.

## Fences
Rule 17 strict: dedup + dtype ONLY; every vendor column survives; no fillna/dropna/row-filter/slimming.
Rule 17a: never write `bronze/`. Identity from vendor bytes (H1; vendor-attested filename for headerless
fam/slm); unreadable → QUARANTINE, never a default; undeclared masters returned, not hidden. No silent
skips (unregistered feed → visible UNCONVERTED). An absent day is ABSENT. `exit 0` = bytes-in-S3.

## <compiler_tools_mandate>
Phase 1: `comp-pipescript io` per gold consumer when wiring a new silver output that an existing gold
script will read. Every script: `from __future__ import annotations` (Rule 15).
Phase 2: `.tools/commit-gate.sh` (automatic).
Phase 3: <data_reprocess_scope>: no historical reprocess — parsers act forward-only from first landing;
backfill conversions bounded by `--since`; converted dates skipped; `--force` rewrites.</data_reprocess_scope>
</compiler_tools_mandate>

## <cross_domain_coordination>
CBUGL parser blocks on C3's first landed 0833 bytes (MCP 0.6.2). Event-wiring blocks on C1. The one
prohibition binds: nobody writes `opal-data-inf/gold/meta/pipeline-complete.json` — the Orion/Eclipse
parsers READ mirrored bronze only.
</cross_domain_coordination>

## <acceptance_criteria>
1. Per-source parser exercised against REAL vendor bytes (not synthetic) with tests committed;
   the scope_mismatch + quarantine + duplicate-registration + UNCONVERTED paths all EXERCISED.
2. First real conversion per source lands `date=` partitioned parquet with every vendor column present
   (column-count parity vs raw, both denominators printed).
3. `comp-validate` run before signaling any consumer (NO_CONFIG/ZERO_CHECKS = UNVALIDATED, never SAFE).
4. Session log with Compiler Tools section; RAVC close to CTO with evidence.
</acceptance_criteria>

<revision v="1.2" date="2026-07-14 ~01:05Z" by="1.0.0_SA_CTO">
THE MONOLITH (Andrew-direct, PRD v1.2 ruling 9): one bucket stores canonical bronze+silver for EVERYTHING; grammar {source}/{scope}/{layer}/...; gold runners/platinum stay where they are. C6: silver output path becomes {source}/{scope}/silver/{feed}/date=YYYY-MM-DD/data.parquet INSIDE each source tree (monolith grammar). Event wiring fires on the monolith bucket's bronze prefixes.
</revision>

<revision v="1.3" date="2026-07-14 ~01:15Z" by="1.0.0_SA_CTO">
C6 v1.3: THE COMPLETENESS LAW (PRD 2a) binds -- silver is ENTITY-complete as well as column-complete: no row/instrument/model/account filtering; a silver partition answers what-did-the-vendor-say, never what-does-Opal-care-about. Your schemas are the future EC2 gold runners' input contract (PRD 2b) -- hive partitions + full grain are load-bearing.
</revision>
