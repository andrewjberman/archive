<task_order>
<to_id>OPAL_GLDRNS.A1</to_id>
<title>THE PLATINUM OUTPUT CONTRACT — pin every Group-D fold-in point (8 bd scripts), exact shapes + locations</title>
<issued_by>1.0.0_SA_CTO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
<status>staged</status>
<project>OPAL_GLDRNS (executes OPAL_CONSOLIDATION WS-C gate C5b)</project>
<provenance>Andrew-direct 2026-07-15 ~19:0xZ (CTO terminal, verbatim in memory
project_opal_consolidation_andrew_directive_20260715 DIRECTIVE 3): "If there are multiple Group D
scripts that create platinum artifacts for the portal, then we need to assess what each of them
are, as those are the fold in points that we are going to have to design into in our refactoring
process." CTO enumeration (same turn): EIGHT bd D-scripts confirmed — this TO pins each one.</provenance>

<scope>
READ-ONLY, source + served artifacts. The 8 bd/49F Group-D scripts (data/black_diamond/scripts/gold/):
D_00.portal_aggregates · D_00b.portal_timeseries · D_00c.portal_leaderboard ·
D_00f.advisor_nna_canonical · D_01.partner_analytics · D_02.advisor_client_detail ·
D_03.composition_artifacts · D_04.client_portal_summary.
(cot's 7 siblings are OUT of scope this TO — 49F is the refactor case study; note structural
divergences from cot only where free.)
</scope>

<deliverable>
org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PLATINUM_OUTPUT_CONTRACT_49F_20260715.md —
per D script: (a) every platinum/gold output KEY it writes (exact key grammar, incl. per-entity
fan-out patterns + measured fan-out counts from the SERVED bucket listing); (b) the SHAPE of each
JSON at field level (from source emit code, spot-verified against 2+ SERVED artifacts per surface
class); (c) grain + entity population; (d) the PORTAL CONSUMER (portal code cite per surface —
e.g. advisor-intelligence.ts:383 consumes advisor_nna_canonical.json — so every contract row is
consumer-anchored, and any UNCONSUMED output is flagged as a retirement candidate, never silently
carried); (e) trigger/cadence + which runner box executes it; (f) D-internal chaining (D_00's
outputs that D_02/D_03/D_04 re-read — the census must capture D-to-D edges, incl. D_01's
gold/partner_analytics keys re-emitted as platinum by D_04 phase-3).
THIS DOCUMENT IS THE S4/S5 TARGET ARTIFACT: the parity harness diffs against it; the cutover
writes to its locations. Never-summed law: contract rows carry basis labels; no combined
0824+0833 quantity anywhere.
</deliverable>

<compiler_tools_mandate>
BEFORE: comp-pipescript io [script] per D script (portal-consumer + column view); comp-blast on
D_04 (blast radius = the portal surfaces). DURING: raw served-bucket listings are the fan-out
instrument (rail-marker: platinum bucket has no comp-tool). BEFORE COMMIT: commit-gate per law.
</compiler_tools_mandate>
<cross_domain_coordination>Base 0.4.0_DS (C-table shapes, dictionary) — read-only overlap, no
shared writes. 0.6.2 (W1 census artifacts) — cite, don't redo. Portal repo — READ-ONLY.</cross_domain_coordination>
<acceptance_criteria>8/8 scripts pinned; every output key listed w/ measured fan-out; every shape
field-level w/ served spot-verify cites; every surface consumer-anchored or flagged unconsumed;
D-to-D edges mapped; denominators printed (scripts/keys/fields counted).</acceptance_criteria>
<session_log>Required, with Compiler Tools section.</session_log>
</task_order>
