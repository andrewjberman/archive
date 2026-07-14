# OPAL_ASSETS.V2-6 — `meta/backfill-status.json` + the `comp-assets` census tool

<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO (V2 decomposition; PRD author 1.0.0_SA_CTO)</issued_by>
<date>2026-07-14</date>
<status>complete</status>
<!-- COMPLETE 2026-07-14 ~08:15Z. Evidence: DS half @ 7d3e0b72c (schema+writer lib, 18/18 tests incl.
     mutants, writer LIVE-PROVEN on the real bucket with read-back verify via _probe/); registration
     bundle @ 6e83bf93f (COO exec-lane commit per owned-paths fork ruling option (a), COO re-verified
     14/14 self-test + manifest completeness PASS + coverage-map 73 consistent; content authored DS).
     comp-assets live-exercised full-bucket (30,020 obj @ 07:38Z); comp-which routes rank-1. Adoption
     by channel processes = V2-1/V2-2/V2-9 lanes per the schema's design. -->

<go>Runs parallel to anything (PRD: small, high-leverage). Begin at will; do not let it delay V2-5.</go>
<project>OPAL_ASSETS — V2 Phase I bronze close-out</project>
<prd>docs/architecture/OPAL_ASSETS_V2_PRD.md V2-6 (@ 53ba45c5f); inherits CONSOLIDATION_PRD v1.6.0 whole (ruling 21 meta home)</prd>

## THE GOAL
1. **`meta/backfill-status.json`** — each channel process writes its per-scope backfill status to the
   ruling-21 meta home (`{source}/{scope}/meta/`). Define the one schema (channel, scope, frontier date,
   counts, holes, guard verdict, updated_at) + the writer helper the channel processes call; V2-9's
   backfill updates it itself (ruling 24).
2. **`comp-assets`** — a read-only census tool over the monolith: per-folder counts / date frontier /
   named holes / guard verdicts, rendered per channel. **A TOOL, not an alarm** (the no-alarms constraint
   stands). Register it per the comp-manifest-check registration invariant (coverage-map + tools_index +
   curated route) in the same pass — a tool nobody can find is indistinguishable from a tool never built.
