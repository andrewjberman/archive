# OPAL_ANALYST.TO4d — News DDB: scope proposal, then artifact census + /draw (vertical 4)

<task_order>
<id>OPAL_ANALYST.TO4d</id>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued_to>0.5.0_AE_OpalETL~Z</issued_to>
<date>2026-08-10</date>
<status>complete</status>
<!-- Stage 0 DISCHARGED 2026-08-10: proposal @a263a0ad6 (options A/B/C with per-option
     denominators); Andrew RULED scope C ("C on this call", ~1927Z at the CTO~Z terminal,
     record @1624238b3) -- union: visual plane + labeled ddb_sources section, no new grammar
     level. Stage 1 census proceeding under the ruled scope. -->

<priority>P1</priority>

<!-- ACCEPTED complete 2026-08-10 ~2145Z by 2.0.0_SA_COO~Z (first-hand validation per the
     4b/4c pattern): census @ddd918d8c (independent yaml parse CLEAN; Q7 scope-C citation
     verified in header; denominator printed), /draw @7f35c7476 (6 findings, delivered
     MSTR~Z cc COO~Z), session log @40838d5e9 (Compiler Tools section reproduces runs),
     F2 zero-component-callers spot-checked via comp-find (3/3 hits are the endpoint fn
     itself, no callers). Findings routed as findings only -- moratorium + no-inferred-gates
     honored. Four-vertical census baseline COMPLETE. -->

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §8.1 grammar @7753e1caf</ref>
  <ref type="ruling">Andrew verticals-2-4 GO @95b3e2852; plan @6c1161075 (News deliberately LAST — "its scoping is an open question to be considered when reached — do not pre-scope it now")</ref>
</references>

<dependencies>
  <dependency agent="0.5.0_AE_OpalETL~Z" task="OPAL_ANALYST.TO4c" status="complete"/>
</dependencies>

<scope>
Vertical 4, TWO stages by Andrew's own design:

**Stage 0 — SCOPING (his open question, answered when reached = now-ish):** News DDB is the
broadest/most abstract vertical (4 DDB tables per PORTAL_RETRIEVAL; query-only news table per
the build). Derive a SCOPE PROPOSAL: what counts as a "portal-served News artifact" at census
grain (tables? query patterns? rendered panels only?), with the denominator implications of
each option. Send to CTO~Z (grammar owner) who carries it to Andrew via MSTR~Z. **PROCEED ON
THEIR WORD — this hold is Andrew's own design from the plan, not a manufactured gate.**

**Stage 1 — census + /draw under the ruled scope:** `refs/census/ARTIFACT_CENSUS_NEWS.yaml`
(same grammar, five rules, ratified choices) + complete-findings /draw to MSTR~Z cc COO~Z.
</scope>

<compiler_tools_mandate>
Stage 0: read refs/PORTAL_RETRIEVAL.md news-DDB census + .tools/comp-estate news thread
(provenance header; --refresh if stale) — the proposal states each scope option WITH its
denominator. Stage 1: same triad as TO-4b/c under the ruled scope.
</compiler_tools_mandate>

<cross_domain_coordination>
Same pattern as TO-4b/c. The news DDB is DATA-plane read-only (query-only table discipline
from the build stands — no scans; portal_lookup.py is the sanctioned mechanism).
</cross_domain_coordination>

<acceptance_criteria>
1. Stage-0 scope proposal delivered to CTO~Z with per-option denominators; ruled scope cited
   in the census header.
2-5. Same as TO-4b (census five rules; /draw complete; no inferential work; log section).
</acceptance_criteria>

<notes>
Sequential batch member: begins on TO-4c completion (Stage 0 immediately; Stage 1 on the
scope word). Completes the four-vertical baseline — after acceptance, the program moves to
Andrew's semantic pass + DATA_CATALOG v0.2 per the plan's Steps 3-6.
</notes>
</task_order>
