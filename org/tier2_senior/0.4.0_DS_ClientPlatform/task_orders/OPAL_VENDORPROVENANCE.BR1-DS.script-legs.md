<task_order>
<to_id>OPAL_VENDORPROVENANCE.BR1-DS.script-legs</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-04</date>
<status>staged</status>
<priority>P1 (implementation leg 1 of the sovereign retire ruling @6f4ad98db; THE PLAN @7538cbc5f IS THE SPEC -- this TO binds its execution, it does not restate it)</priority>

<title>BR1-DS: the three script legs -- Eclipse puller content, completion-emitter content, overlap-compare harness -- staging-prefix writes ONLY until the G3 cut</title>

<context>
Your own execution plan @7538cbc5f (all three gates + CTO's floors-per-consumer condition + the
staging-prefix overlap design) is the authoritative spec, embedded by reference at that pinned
commit. This TO authorizes the DS script-content legs per the plan's lane table: (1) the Eclipse
puller (5 REST calls, JWT ladder mirrored, prior-evening landing preserved), (2) the completion-
emitter (verifies the ported required-dim contract, emits _BRONZE_COMPLETE, single writer),
(3) the overlap-compare harness (field-exact, >=5 trading days, sidecar rows_per_artifact as
CONTRACT). Rule 13 deploy cycle is yours end-to-end for these scripts.
</context>

<scope>
1. Implement the three scripts per the plan's own specifications -- deviations from the plan are
   plan AMENDMENTS (committed + CTO/COO notified), never silent drift.
2. HARD BOUNDARY, the plan's own load-bearing line: the new path writes bronze/eclipse_qa/
   (staging) ONLY until the G3 change window -- a production dual-write during cutover would
   rebuild R-1 inside its own fix. Zero production-key writes from any new code before the cut.
3. The overlap harness's daily compare output is the G1 acceptance evidence -- committed per run,
   field-exact verdicts, denominators printed.
4. AE's infra legs (Lambda TF x2, silver floor, rule live-verify) ride their own TO staged behind
   the v3 apply; coordinate contracts (env names, prefixes, cron values) through the plan doc,
   amending it as the single source.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io on each script as it lands (hand-derive where tool-blind, labeled) + the plan's own contract table re-read at @7538cbc5f</run>
      <expect>READS/WRITES match the plan's table exactly; eclipse_qa staging prefix confirmed as the ONLY write target.</expect>
      <if_mismatch>STOP -- a write outside staging pre-cut is the R-1 rebuild; fix before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="exercise">
    <step>
      <run>puller exercised against live Eclipse (lifted egress) into staging; emitter exercised in scratch against a synthetic incomplete-dim state (must REFUSE) + a complete state (must emit); harness exercised on day-1 real pair</run>
      <expect>All three captured verbatim; the emitter's refusal leg proves the contract check is live.</expect>
      <if_mismatch>An unexercised refusal = an unproven gate; keep working.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after">
    <step>
      <run>Rule 13 deploys (commit-gate, safe-deploy, MATCH) + report to COO + CTO + AE with the day-1 overlap verdict</run>
      <expect>The >=5-TD overlap clock starts on day-1's clean compare.</expect>
      <if_mismatch>A dirty day-1 compare is a FINDING on the pattern mirror, not a reason to widen tolerance.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Per the plan's lane table: AE holds TF/infra + the G3 stop; the EC2 keeps running untouched
through the whole overlap; firm separation binds (inf tree). The plan doc is the single contract
source between your legs and AE's -- amend it, never side-channel values.
</cross_domain_coordination>

<acceptance_criteria>
1. Three scripts implemented + exercised per Phase 2 (refusal leg mandatory), deployed per Rule 13.
2. Zero production-key writes pre-cut (staging only) -- audited by the harness itself.
3. Day-1 overlap verdict reported; the 5-TD clock running.
Plus: session log Compiler Tools section reproduces every <run> with observed output and explicit
pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="plan">BR1_EXECUTION_PLAN_retire_inf_bronze_runner.md @7538cbc5f (THE SPEC)</ref>
  <ref type="ruling">Andrew @6f4ad98db (+time-correction @83beb6ddc); CTO concur + floors condition 042600Z</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
