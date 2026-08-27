<task_order>
<id>MDPF_3FIRMS.3F-S5</id>
<title>Rebalancer-family provenance columns — FORWARD canonicalization (Rule-17-sensitive; never rewrites landed data)</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-S (Silver)</workstream>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T21:15Z</issued_at>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project MDPF_3FIRMS, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending</status>
<authorization>Your own 3F-S4 finding D4 -> CTO ruling 211330Z item 3 (AUTHOR 3F-S5, DS lane, Rule-17-sensitive, normal gates; CTO gates any schema change).</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md v1.14 §3.2 layer contracts; §8.5</ref>
  <ref type="predecessor">Your 3F-S4 contract @4d58357d5 — divergence D4, named by you as the priority forward-canonicalization candidate</ref>
  <ref type="law">CLAUDE.md Rule 17 (silver = dedup + dtype ONLY) · Rule 17a (bronze is raw and untouched)</ref>
</references>

<scope>
**This TO exists because YOU found it.** 3F-S4's divergence register D4: the **rebalancer family carries ZERO
provenance columns** while the other silver families carry them. That asymmetry means a rebalancer row
cannot answer *"which bronze object produced me, and when?"* — and the rebalancer family feeds
`dim_model_portfolio`, which feeds Cottonwood's served model AUM.

**DELIVERABLES:**
(a) **Design** the provenance column set for the rebalancer family, canonical with what the other
    families already carry (do not invent a new shape — match, then justify any deviation).
(b) **Name every affected table and converter**, with the schema delta per table.
(c) **A FORWARD-ONLY migration plan** with its reprocess scope stated.
(d) **Route the schema change to CTO for his gate BEFORE implementing.** He said so explicitly.

⛔ **FORWARD CANONICALIZATION ONLY. NEVER REWRITE LANDED DATA.**
- **17a: bronze is RAW and UNTOUCHED.** Nothing in this TO writes to bronze, ever.
- **Landed silver partitions are NOT retroactively rewritten** to add columns. A historical partition
  without provenance columns is a partition that predates the contract — that is honest. **Backfilling a
  provenance value you did not observe is fabrication wearing a metadata hat.**
- The series must stay **additive and non-conflicting with data that arrives later** (§8.1).

⚠ **THE RULE-17 QUESTION IS THE INTERESTING PART AND I AM NOT PRE-DECIDING IT.** Rule 17 says silver is
**dedup + dtype standardization ONLY** — never field-slimming, never fillna, never dropping bronze
columns. **ADDING a provenance column is none of those prohibited things**, and provenance is not a
business-logic judgment about field relevance. **But it IS a schema change to a silver table, and Rule
17's spine is that each layer does exactly one job.** State the argument explicitly in your design and
let CTO rule. **Do not assume it is permitted because it is useful.**

⚠ **A CONSUMER CAVEAT THAT MUST RIDE THE DESIGN:** once the columns exist forward-only, **older
partitions will lack them.** Any consumer must treat their absence as *"this partition predates the
contract,"* NOT as *"provenance unknown/failed."* **That is tonight's silent-absence class in advance** —
design the semantics so an absence cannot be misread, and state the cutover date explicitly.
(Precedent from 0.6.2's B5: `_complete/` sentinels only exist from 06-23 onward, and consumers reading
sentinel-absence before that as failed delivery would be wrong.)
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Empirical parquet inspection of the rebalancer family AND of two families that DO carry provenance columns, at stated partition vintages</run>
      <expect>The existing provenance shape documented from FILES, not docstrings; the rebalancer delta stated per table.</expect>
      <if_mismatch>Auto-rule 7 — a docstring is a claim about a file; the file is the fact. State the partition vintage you read or the claim is not a citation.</if_mismatch>
    </step>
    <step>
      <run>Enumerate consumers of every affected table — text sweep + your own 3F-S4 contract doc</run>
      <expect>Complete consumer list with the denominator stated.</expect>
      <if_mismatch>⚠ `comp-blast` returns NOT-FOUND on monolith silver artifacts (your own S4 finding (c) — they are not graph nodes) and `comp-pipescript io` is blind to silver reads (your finding (b)). **PRD v1.14 explicitly authorizes text sweeps + your S4 contract as the substitute until 0.8.0 closes the gaps. Do NOT report a clean comp-blast as coverage — it cannot see this surface.**</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/commit-gate.sh on every .py touched</run>
      <expect>py_compile + ds-precommit-check + ruff clean; `from __future__ import annotations` present.</expect>
      <if_mismatch>STOP. Do not commit.</if_mismatch>
    </step>
    <step>
      <run>Route the schema delta to CTO for his gate</run>
      <expect>Explicit CTO word on the Rule-17 question and the column set BEFORE any converter change lands.</expect>
      <if_mismatch>⛔ CTO gates any schema change (his 211330Z). A design that proceeds without it is out of scope regardless of merit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Verify a NEW partition carries the columns and an OLD partition is BYTE-IDENTICAL to its pre-change state</run>
      <expect>Forward-only proven on both sides: new partition has provenance; a landed partition is unchanged, verified by ETag/size against its pre-change value.</expect>
      <if_mismatch>⛔ ANY change to a landed partition is a forward-only violation — STOP and escalate. This check is the whole guarantee; run it as a positive AND negative control, not as a formality.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>**FORWARD-ONLY BY DESIGN — this is the defining constraint, not a convenience.**
  Historical partitions are NOT reprocessed to add provenance columns. A partition without them predates
  the contract, and that is the honest state. **Reprocessing to synthesize provenance for rows whose
  actual provenance was never observed would fabricate the exact metadata the columns exist to
  guarantee.** The cutover date is stated explicitly in the design so consumers can distinguish
  predates-contract from missing.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="rebalancer silver family + its converters" shared_with="0.7.0_AE_CloudOps">
    He flagged this as a likely sidecar touching his infra half and has it noted-not-started. MCP him
    before committing anything converter-side.
  </resource>
  <resource path="dim_model_portfolio + build_cottonwood_artifact" shared_with="0.4.0_DS (3F-G3, 3F-G8)">
    Your own downstream. A rebalancer schema change reaches the Cottonwood served model AUM —
    sequence against G8 so a schema change does not land mid-build.
  </resource>
  <resource path="rebalancer bronze pull" shared_with="0.6.2_AE_PartnerETL~A (3F-B6)">
    His B6 liveness signal reads `rebalancer_model_detail`. Confirm your change cannot disturb that
    signal's inputs.
  </resource>
</cross_domain_coordination>

<dependencies>
  <dependency type="gate" name="CTO ruling on the Rule-17 question + column set" status="required" blocking="true">
    Design and route FIRST; implement only on his word.
  </dependency>
</dependencies>

<acceptance_criteria>
1. Provenance column set DESIGNED and canonical with the families that already carry them — deviations
   justified, not silent.
2. Every affected table + converter named, with the schema delta per table, from EMPIRICAL inspection at
   stated partition vintages.
3. A FORWARD-ONLY migration plan with its reprocess scope stated and its cutover date explicit.
4. **The Rule-17 argument stated explicitly and routed to CTO — permitted-because-useful is not an
   argument.** No converter change lands before his word.
5. **Forward-only PROVEN on both sides**: a new partition carries the columns; a landed partition is
   byte-identical to its pre-change state (ETag/size verified).
6. Consumer semantics designed so column-absence reads as PREDATES-CONTRACT, never as
   provenance-unknown — with the cutover date published to consumers.
7. Consumer enumeration carries its DENOMINATOR, and does NOT rest on a `comp-blast` pass (blind here).
8. **Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail vs
   `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>
Report to 2.0.0_SA_COO; CTO gates the schema change. Escalate immediately if any landed partition
changes, or if the design cannot satisfy forward-only without a reprocess.
</escalation>
</task_order>
