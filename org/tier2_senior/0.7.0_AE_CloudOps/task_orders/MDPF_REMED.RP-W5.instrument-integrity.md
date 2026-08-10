# TO MDPF_REMED.RP-W5 — INSTRUMENT INTEGRITY: we cannot currently SEE failures

<task_order id="MDPF_REMED.RP-W5" project="MDPF_REMED">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-10T23:4xZ</issued>
<status>pending</status>
<priority>P1 — executable NOW, independent of RP-W1/RP-W3's gates. Andrew has spawned you for this plan.</priority>

<references>
  <ref type="plan">org/tier1_exec/1.0.0_SA_CTO/deliverables/MDPF_REMEDIATION_PLAN_20260810.md @dbbbfa9cd3 (W5, §3 corrected D-24)</ref>
  <ref type="context">COO decomposition Addendum 4-I (bronze ownership ruled: cot-rebalancer-runner OWNS blackdiamond/cottonwood/bronze; the mirror's guard is NOT broken)</ref>
</references>

## SCOPE — four items, each with a hard boundary

### 1 · D-16 — the mirror's 14-day hard-fail: NARROW THE ASSERTION, NEVER DISABLE THE GUARD
`opal-assets-ingest-mirror` has hard-failed every invocation for 14 days (81 raises) on ALIEN
SURPLUS of 687 keys, because `cot-rebalancer-runner` (ruled OWNER) writes `{table}/{date}/*.json`
into the mirror's dst_prefix while the mirror writes `{table}/*.xlsx`. **The guard has been
correctly detecting a real second writer for 14 days — it is the only reason we know one exists.**
Remedy: scope `_assert_landed_membership` (`:449`) to the mirror's OWN key grammar (xlsx rows), so a
GENUINE new failure becomes distinguishable from the standing one. ⛔ Never widen an allowlist, never
disable, never "fix" the guard. ⚠ The meta-templates row (`:153`) is a DIFFERENT artifact that has
NEVER run — it must not be silently retired by your scoping fix; state its post-fix status explicitly.

### 2 · SMARTX ONTO THE ESTATE PATTERN — corrected D-24. ADD NO SCHEDULES.
8 of 8 S3 notification configs on opal-data-assets are silver converters firing on bronze OBJECT
CREATION — event-driven silver IS the estate pattern and a scheduled converter would be the defect
(Andrew's architectural read, CTO-measured). **smartx alone fires on A PROCESS RETURNED CLEAN
(OnSuccess; no S3 notification exists for smartx).** Measured consequence 08-10: the pull wrote
5,222,424 B of bronze at 13:36:31Z then raised DirtyRunError — under the estate pattern that landing
converts; under OnSuccess it did not (silver came only from a retry that skipped all 9,762 objects).
Remedy: add the S3 ObjectCreated notification for smartx bronze → its silver converter, matching the
other 6. Belt-and-braces (keep OnSuccess too, like cot-rebalancer-runner) unless CTO rules otherwise.
All converters carry OnFailure → opal-assets-silver-dlq already; do not build new alerting
(moratorium: NO new alarms/SNS/SES — a gate or owned blocking item is the legal landing shape).

### 3 · D-5 — the 49F limb-(v) skip
Limb (v) — the exact limb that fails inflection — is SKIPPED for 49financial (`:1562-1567` of the
gate; 205 disagreements across 33 dates printed and unchecked). Remedy: un-skip / surface it so a
49F PASS means what it says. If un-skipping makes 49F FAIL loudly, THAT IS A FINDING, not a
regression — report it, do not re-skip.

### 4 · GLOBAL's zeroed-but-PASS aggregate
An identity check that cannot fail on an empty artifact (`0 == 0+0+0`; all-zero aggregate emitted
daily since 08-09 with reconciliation: PASS). Remedy: make the reconciliation discriminate — a check
that passes on the confirming limb only is not a control. Gate the PRECONDITION (non-empty legs),
not the output identity.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-blast opal-assets-ingest-mirror</run>
      <expect>Known radius (mdpf-daily-refresh-trigger, inf-*/cot-* rules, served guards, 36 IAM policies). No surprises.</expect>
      <if_mismatch>STOP; surface new consumers to COO.</if_mismatch>
    </step>
    <step>
      <run>aws s3api get-bucket-notification-configuration --bucket opal-data-assets (via .tools/aws shim)</run>
      <expect>8 existing silver-converter configs; NONE for smartx bronze prefix (re-confirm the gap at your HEAD before building).</expect>
      <if_mismatch>If a smartx notification already exists, the premise moved — surface before adding a duplicate trigger.</if_mismatch>
    </step>
    <step>
      <run>comp-iam service &lt;smartx silver converter lambda&gt; + live simulate-principal-policy for the S3-invoke permission on the exact new notification path</run>
      <expect>Invoke permission + read path GRANTED on live primitives. ONE --resource-arns per call; positive control as a SEPARATE invocation.</expect>
      <if_mismatch>Close via Terraform iam.tf before apply; comp-iam alone is NOT sufficient for a new resource and FAILS GREEN.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before apply/commit">
    <step>
      <run>.tools/safe-apply.sh for all TF; safe-commit for all code. Commit before apply.</run>
      <expect>Plan scoped to items 1-4 only; 0-diff post-apply; tag + push --follow-tags.</expect>
      <if_mismatch>STOP on dirty plan.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after apply">
    <step>
      <run>EXERCISE each control: (1) drop a mirror-grammar-alien key in a QA-safe location or replay the standing surplus — guard still fires on genuine alien keys, no longer fires on rebalancer-owned grammar; (2) land a bronze smartx object (ad-hoc QA run is legal) — converter fires on ObjectCreated; (3) run the gate on 49F — limb (v) evaluates; (4) feed the reconciliation an empty-legs artifact in QA — it FAILS.</run>
      <expect>All four controls fire on the defect event, and each was shown ABLE TO FAIL (mutant/negative control per check).</expect>
      <if_mismatch>A control that cannot fail is not a control — rework before reporting complete.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
opal-assets-ingest-mirror shared with RP-W3 (your own lane; RP-W3 is staged/double-gated — do not
fold retime work into this TO, and do not let this TO's fix be credited to the retime or vice
versa). Item 2 touches the smartx OnSuccess chain that RP-W3 relies on (G-1a): keep OnSuccess
intact. cot-rebalancer-runner is OWNER of the bronze prefix per CTO ruling — do not alter its
writes.
</cross_domain_coordination>

<acceptance_criteria>
1. Each of the four items EXERCISED per Phase 3 — the test that fails if the claim is false, with a
   negative control each. Config reads are not acceptance (Rule 22a).
2. Guard narrowing shown to still detect a planted/replayed genuine alien key (positive control) and
   to pass on rebalancer-grammar keys (the standing 687 no longer raise).
3. Meta-templates row (`:153`) post-fix status stated explicitly (runs / still-never-runs + why).
4. No new alarm/SNS/SES/monitor resources (moratorium). No schedules added anywhere.
5. Session log Compiler Tools section reproduces every &lt;run&gt; + output + pass/fail. Missing rows = REWORK.
</acceptance_criteria>
</task_order>
