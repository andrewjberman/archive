# OPAL_ASSETS.C12 — Legacy prefixes INVENTORIED, not cleaned (doc only)

<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>1.0.0_SA_CTO (OPAL_ASSETS owner)</issued_by>
<date>2026-07-14</date>
<status>pending</status>
<state date="2026-07-14 ~05:0xZ" by="2.0.0_SA_COO (reconciliation)">LANDED: the full inventory
(fb31f3586 -- 249,663 objects / 8 buckets / 125 prefixes, zero deletions) + the 257 finding (Andrew ruled
migrate-then-retire, executing via C3's Glacier leg) + the 01_raw disposition fold. REMAINING (ruled
additions post-delivery): the orion legacy-prefix set-difference (v1.4.4, the 257 treatment -- coordinate
w/ 0.7.0) + coerced-only-survivor labels (ruling 16). Pending is correct.</state>
<hold>ANDREW HOLD 2026-07-14 ~00:25Z, verbatim: "Wait to dispatch until I give the go, I want to respawn the workers first." LIFTED 2026-07-14 ~01:06Z: CTO GO issued to the respawned, roster-verified serial per Andrew's begin-on-readiness protocol (C7 = author half only; C11 remains gated on C3+C6).</hold>
<project>OPAL_ASSETS — Grand Consolidation P3</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4 (TO-C12)</prd>

## Scope
A written inventory (deliverables doc) of every legacy prefix the consolidation strands across the six
buckets: what it holds, object counts + date ranges (denominators printed, no sampling), which TO/router
row replaced it, and its disposition class. **INVENTORY, NOT CLEANUP** — deletion is a deletion-class
action requiring explicit human sign-off, and it is NOT in this project.

## The one entry that must be in bold — REVISED at PRD v1.1 (§3 ruling 6)
`opal-data-schwab/01_raw/` (7,142 objects, 257 pre-REST-floor): **Andrew has ruled it disposable**
(*"we do not care about 01_raw, that entire folder can be deleted... what we are getting here is more
important, and will be the canonical form"*) and 0.6.2's measurement disqualifies it from bronze
migration (unzipped GUI-era artifacts, no master in the filename, lossy provenance). The inventory
marks it `Andrew-ruled disposable — retirement SEQUENCED, not deleted`: live consumers exist
(`build_canonical_daily.py:130,155` paginates it; `mdpf011_rematch.py:68` reads it), so the sequence is
finish bronze → verify → repoint consumers → THEN delete under the normal deletion-class protocol with
a final Andrew confirm. **This TO still performs zero deletions.**

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

<revision v="1.2" date="2026-07-14 ~01:05Z" by="1.0.0_SA_CTO">
THE MONOLITH (Andrew-direct, PRD v1.2 ruling 9): one bucket stores canonical bronze+silver for EVERYTHING; grammar {source}/{scope}/{layer}/...; gold runners/platinum stay where they are. C12: add opal-data-schwab {master}/bronze trees to the inventory as STAGING -- MIGRATED TO MONOLITH (after C3a lands; cross-reference the remap evidence). Still zero deletions.
</revision>

<revision v="1.3" date="2026-07-14 ~01:15Z" by="1.0.0_SA_CTO">
C12 v1.3: add an end-state-disposition column per prefix (PRD 2b): migrates-to-monolith / stays-as-platinum-home (the ADVI portal partner buckets -- the ONLY permanent stay-puts) / retire-sequenced. The inventory is the checklist for the eventual moves.
</revision>
