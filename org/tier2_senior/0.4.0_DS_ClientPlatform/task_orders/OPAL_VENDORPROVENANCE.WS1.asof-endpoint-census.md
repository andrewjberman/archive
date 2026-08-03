<task_order>
<to_id>OPAL_VENDORPROVENANCE.WS1.asof-endpoint-census</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-03</date>
<status>staged</status>
<priority>P1 (Andrew-direct GO 2026-08-03 ~20:15Z @3e2b23ebb3; Andrew-explicit prerequisite to the silver dedup/completeness canon -- MDPF_GLOBAL T4.A certification waits on your exemplar rows)</priority>

<title>OVP WS-1: Vendor as-of endpoint census -- an As-Of Contract Registry row for EVERY (vendor, endpoint) feeding the estate, grounded or loudly UNKNOWN</title>

<context>
OPAL_VENDORPROVENANCE PRD v1.0 (docs/architecture/OPAL_VENDORPROVENANCE_PRD.md), the sibling
project Andrew explicitly bucketed out of MDPF_GLOBAL: per-(vendor,endpoint) as-of contracts as a
NECESSARY PREREQUISITE to the silver dedup/completeness canon, then NYSE calendar sync.

THE ARTIFACT (PRD 3.1): one machine-readable registry, one entry per (vendor, endpoint/feed) that
ingests into any Opal bucket, fields: vendor / endpoint / asof_field / asof_semantics /
label_offset / pull_schedule / dedup_stable_key (Task-4 output, leave TODO here) /
completeness_rule / grounding. `UNKNOWN` is a LEGAL, LOUD value -- an endpoint whose as-of
semantics cannot be established is recorded as such and becomes a named risk, never a silent
assumption.

SCOPE OF CENSUS (PRD WS-1 + D-2 recommendation): every (vendor, endpoint) feeding
`opal-data-assets` AND the three legacy partner buckets (`opal-data-bd`, `opal-data-inf`,
`opal-data-cot`). D-2 (whether the registry BINDS the legacy buckets) is an open CTO/Andrew
decision -- you CENSUS them regardless; binding is decided at acceptance.

PRIORITY ORDER (D-3 recommendation + sibling-project need): (1) Orion (semantics already sealed in
data/inf/scripts/silver/_orion_vendor_asof.py -- cheapest exemplar), (2) SmartX + Black
Diamond/cot (they feed MDPF -- MDPF_GLOBAL.T4A consumes these rows), (3) Schwab-0824, (4)
Eclipse, (5) everything else. Land rows incrementally in that order; do not hold early rows
hostage to the long tail.

REGISTRY HOME (D-1 open): draft at the PRD-proposed
`data/_contracts/vendor_asof_registry.yaml`, header-marked DRAFT-pending-D-1. CTO may relocate at
acceptance; content survives relocation.

EGRESS (PRD s.7, binding): the census reads OUR buckets, code, and existing pull records ONLY.
Any probe requiring a NEW call to a vendor endpoint routes through standing egress rules (lifted:
Orion, SmartX, cot-BD, Eclipse -- each per its recorded scope; ycharts and everything else HELD,
explicit Andrew per-use word required). Availability is not authorization.
</context>

<scope>
1. Derive the DENOMINATOR from the live ingest inventory, not memory: enumerate every
   bronze-writing ingest path into the four buckets (pullers, Lambdas, EC2 jobs, manual feeds like
   the OneDrive Schwab delivery) -- the WS-1 gate is CTO accepting registry completeness against
   exactly this inventory. Print it, with the enumeration method.
2. One registry row per (vendor, endpoint/feed): all PRD 3.1 fields; `dedup_stable_key` = TODO
   (WS-4's output, not yours); every claim in `grounding` cites file:line @ commit or an exercised
   probe. "The docstring says" is not an exercise (Rule 22).
3. UNKNOWNs enumerated LOUD in a dedicated section: endpoint + what was tried + what would resolve
   it (a vendor doc, an egress-gated probe, an Andrew question).
4. Deliverable: the DRAFT registry file + a census doc in your deliverables folder
   (org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/OVP_WS1/) with the denominator table.
5. Report incrementally: Orion rows first (target: first report same session), then the
   MDPF-feeding vendors -- MCP COO + CTO at each tranche so T4.A research can start in parallel
   (Andrew-explicit: key RESEARCH may parallelize; CERTIFICATION waits on your rows).
6. OUT OF SCOPE: WS-2 calendar work, WS-3 stamps, any silver script edits, any new vendor calls
   outside lifted scopes, anything that alarms/monitors (moratorium).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before census">
    <step>
      <run>comp-estate --list ; then comp-estate &lt;vertical&gt; for each vendor-feeding vertical the list names</run>
      <expect>Chain context per vertical: which pullers/converters feed which buckets -- seeds the ingest inventory (it is a SEED, not the denominator; the denominator is derived live per scope item 1).</expect>
      <if_mismatch>Census-vintage staleness is expected -- note drift, ground live.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io &lt;script&gt; for every silver converter your inventory touches</run>
      <expect>READS/WRITES per converter enumerated -- grounds each row's endpoint->table mapping.</expect>
      <if_mismatch>A converter the tool cannot resolve gets a manual source-read with file:line cites; note the tool gap.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-blast &lt;fn&gt; on any shared helper your census code/notes touch (expected: none -- read-only census)</run>
      <expect>No shared-helper writes; if any tooling you write for the census lands in-repo, blast it first.</expect>
      <if_mismatch>MCP the owning agent before committing anything in a shared radius.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-validate where a validate config exists for touched artifacts (expected: N/A for a registry draft); MCP tranche report to COO + CTO</run>
      <expect>Tranche report cites registry path + commit + rows landed + UNKNOWN count + denominator coverage so far.</expect>
      <if_mismatch>A tranche report without the denominator-coverage line is REWORK.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
New file (data/_contracts/) -- single writer, you. Read surfaces overlap MDPF_GLOBAL T1.A/T2.A
(read-only both sides, no gate). Your SmartX/BD-cot/Orion/Eclipse/Schwab-0824 rows are the
Andrew-explicit prerequisite for MDPF_GLOBAL.T4A certification (DS lane, likely also you or a
sibling seat) -- tranche-report promptly so T4.A research overlaps. The Schwab OneDrive->S3 ingest
is AE-owned (49-schwab-conv skill, SSE deny on DS) -- census it from code/records; do not run it.
</cross_domain_coordination>

<acceptance_criteria>
Verbatim PRD s.4 WS-1 row (CTO validates at close):
1. As-Of Contract Registry rows for EVERY (vendor, endpoint) feeding opal-data-assets + the three
   legacy partner buckets; each row grounded (source cite or exercised probe); UNKNOWNs enumerated
   loud.
2. Gate: CTO accepts registry completeness (denominator = live ingest inventory, not memory).
Plus PRD s.7 constraints verbatim: Rule 17/17a untouched; no monitors/alarms; egress rules per
scope; Rule 22 grounding per row.
Plus: session log includes a Compiler Tools section reproducing every <run> from
<compiler_tools_mandate> with observed output and explicit pass/fail vs <expect>. Missing rows =
REWORK, not COMPLETE.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/OPAL_VENDORPROVENANCE_PRD.md (s.3.1 registry schema, s.4 WS-1, s.6 D-1/D-2/D-3, s.7 constraints)</ref>
  <ref type="sibling">docs/architecture/MDPF_GLOBAL_PRD.md Addendum C s.C.4 T4.A (consumes your exemplar rows)</ref>
  <ref type="sealed-exemplar">data/inf/scripts/silver/_orion_vendor_asof.py (Orion semantics, cheapest first row)</ref>
  <ref type="go">Andrew-direct GO @3e2b23ebb3 (memo-doc s.5); CTO relay 20260803T200329Z</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
