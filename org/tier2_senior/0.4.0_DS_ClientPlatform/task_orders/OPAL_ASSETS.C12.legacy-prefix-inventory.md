# OPAL_ASSETS.C12 — Legacy prefixes INVENTORIED, not cleaned (doc only)

<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>1.0.0_SA_CTO (OPAL_ASSETS owner)</issued_by>
<date>2026-07-14</date>
<status>pending</status>
<project>OPAL_ASSETS — Grand Consolidation P3</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4 (TO-C12)</prd>

## Scope
A written inventory (deliverables doc) of every legacy prefix the consolidation strands across the six
buckets: what it holds, object counts + date ranges (denominators printed, no sampling), which TO/router
row replaced it, and its disposition class. **INVENTORY, NOT CLEANUP** — deletion is a deletion-class
action requiring explicit human sign-off, and it is NOT in this project.

## The one entry that must be in bold
`opal-data-schwab/01_raw/` holds **257 objects Schwab can no longer serve** (REST history floor
2023-07-12; 01_raw reaches to 2023-01-17). **IRREPLACEABLE.** Their migration into the bronze layout is
a COPY job (separate, future TO) — never a re-pull, never a delete. The inventory marks them
`irreplaceable — copy-only`.

## <compiler_tools_mandate>
Phase 1: generic `aws s3 ls` enumeration (operational, un-nudged) per prefix; every count carries its
denominator. Phase 2: n/a (doc). Phase 3: n/a.
</compiler_tools_mandate>

## <cross_domain_coordination>
Read-only everywhere. bd/49F-held paths: enumerate metadata only under the OPAL_ASSETS scoped lift; if
a listing requires touching a held surface beyond that, mark `NOT ENUMERATED — held` (an explicit gap,
never a guess). Nobody writes `opal-data-inf/gold/meta/pipeline-complete.json`.
</cross_domain_coordination>

## <acceptance_criteria>
1. Inventory doc committed under your deliverables with per-prefix counts + date ranges + disposition
   class + replacing-TO cross-reference.
2. Zero delete/lifecycle operations performed or proposed-as-performed.
3. Session log + Compiler Tools section; RAVC close to CTO.
</acceptance_criteria>
