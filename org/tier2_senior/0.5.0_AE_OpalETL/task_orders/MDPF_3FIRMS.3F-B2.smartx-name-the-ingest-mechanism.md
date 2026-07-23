<task_order>
<id>MDPF_3FIRMS.3F-B2</id>
<title>49F/SmartX bronze leg — NAME the ingest mechanism (no smartx-named EventBridge rule exists, yet partitions are current)</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-B (Bronze)</workstream>
<issued_to>0.5.0_AE_OpalETL</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:23Z</issued_at>
<status>pending</status>
<!-- RECONCILED 2026-07-23T14:4xZ (0.5.0_AE_OpalETL re-provisioned session, XXX.md Step-2b): status
     was stale at `staged` vs delivered work. GO received 20260722T2033Z (COO). AC1-AC4 + AC6 DELIVERED
     @0f4bce90d (mechanism named: Scheduler smartx-assets-daily-pull-daily 09:30 ET -> OnSuccess dest
     opal-assets-silver-smartx -> sweep rule 16:00Z; failure path bronze=NOTHING, silver=unwatched DLQ)
     + @695af1a7f (exercised end-to-end: DirtyRunError->58s self-heal observed, USD 1,434,172,228 @ D-1).
     AC5 (post-TO scheduled-fire verify, fire 2026-07-23 13:30Z) dispatched by CTO to 0.6.2~A (read-only)
     while this lane was orphaned -- NOT hand-fired, covered there. Close to COO on AC5 evidence. -->
<authorization>LD-0333 am.1 @2eef569d2 -> CTO cascade 200805Z -> COO decomposition.</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md §2.2 (49F-model row); §4 WS-B row 3F-B2; §9 (the events list-rules census that created this TO)</ref>
</references>

<scope>
**The finding that created this TO:** a full `aws events list-rules` census this session found **NO
EventBridge rule matching `smartx`** — yet `smartx/platform/silver/fact_model_aum_daily` partitions are
CURRENT THROUGH TODAY. **Something fires this ingest and we cannot name it.**

**An unnamed ingest mechanism has no freshness contract, no failure notification path, and no owner.**
It is currently working, which is exactly why nobody has noticed — and it will be invisible when it
stops.

Deliverables:
(a) **NAME THE MECHANISM** with applied-truth evidence: rule ARN, EC2 cron, SSM association, Step
    Function, Lambda schedule, or an upstream producer writing on its own cadence — whatever it actually
    is, cited concretely.
(b) **Document the schedule** (cadence + expression + timezone).
(c) **Document the FAILURE NOTIFICATION PATH** — what signals if it stops. If the answer is "nothing,"
    that is the finding and it is stated plainly, not softened.
(d) **Depth statement** for `fact_model_aum_daily` (note: run-date partitioned, with full history INSIDE
    each partition — do not read the partition count as the series depth; they are different axes).

⚠ **"NOT FOUND" IS NOT A MECHANISM.** An empty `list-rules` result is a LEAD, not a conclusion. The PRD
binding principle applies directly: never conclude something doesn't exist from the shape of the search
you happened to run. Enumerate the other possible firing surfaces before asserting absence.

⚠ This leg feeds the **49F model_aum** term — one of the three components of the Global fee-basis
radial (§1.3). A silent stall here understates Global AUM with no alarm.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-which "what fires the smartx model aum ingest"</run>
      <expect>A routed comp tool, or an on-rails comp-grep/comp-glob run. Record the output even if NO CURATED RULE MATCHED.</expect>
      <if_mismatch>If nothing routes, record the coverage gap and proceed to primitives — a repeat override for one intent means a tool should be built.</if_mismatch>
    </step>
    <step>
      <run># rail-checked: applied-truth enumeration across candidate firing surfaces
aws events list-rules --query 'Rules[?contains(Name,`smartx`)||contains(Name,`model-aum`)].{N:Name,S:State,C:ScheduleExpression}'</run>
      <expect>Either a named rule, or an empty result you treat as "not EventBridge-fired" — never as "not fired".</expect>
      <if_mismatch>Empty is a lead. Continue to EC2 cron (EC2_MANIFEST.json), SSM associations, Lambda schedules, and upstream producers before concluding.</if_mismatch>
    </step>
    <step>
      <run>comp-freshness</run>
      <expect>The smartx leg entry resolves on freshness_basis: trading-day-frontier.</expect>
      <if_mismatch>Flat-hours fallback WILL false-alarm; record the gap without raising staleness (NEVER#1).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Observe ONE scheduled fire post-TO and evidence it (invocation log / new partition with explicit-Z stamp)</run>
      <expect>A fire observed on the named mechanism, tying mechanism to artifact.</expect>
      <if_mismatch>⛔ Do NOT hand-fire to produce this evidence. BLOCKED-ON-SCHEDULE is the correct interim report.</if_mismatch>
    </step>
    <step>
      <run>aws s3api list-objects-v2 --bucket opal-data-assets --prefix smartx/platform/silver/fact_model_aum_daily/ (explicit-Z)</run>
      <expect>Current through today; depth stated on the CORRECT axis (run-date partitions vs in-partition history are different denominators — say which).</expect>
      <if_mismatch>⛔ never bare `aws s3 ls` for a load-bearing time. Enumerate what the number is OF before quoting it.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Re-verify the named mechanism still resolves and the partition census holds, denominators printed</run>
      <expect>Stable.</expect>
      <if_mismatch>Surface to COO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>Discovery and documentation only; no script patched, no data written.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="smartx/platform/silver/fact_model_aum_daily/" shared_with="0.4.0_DS_ClientPlatform (3F-S2 census; the model crosswalk)">
    The 5 archetypal models resolve via `data/mdpf/scripts/gold/mdpf_revamp_model_crosswalk.py`. MCP DS
    before touching anything crosswalk-adjacent.
  </resource>
</cross_domain_coordination>

<dependencies><dependency type="none">Independent.</dependency></dependencies>

<acceptance_criteria>
1. The ingest mechanism is NAMED with concrete applied-truth evidence (ARN / cron / association / owning
   process). **"No rule found" does not satisfy this.**
2. Schedule documented (cadence + expression + timezone).
3. Failure-notification path documented — including an explicit "none exists" if that is the truth.
4. Depth statement that names WHICH AXIS it is measuring (run-date partitions vs in-partition history).
5. One scheduled fire observed post-TO, evidenced — with NO hand-fire.
6. **Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail vs
   `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>
Report to 2.0.0_SA_COO. Escalate immediately if the mechanism cannot be named after exhausting the
candidate surfaces — an unnameable producer feeding a fee-basis component is a standing risk, not a
documentation gap.
</escalation>
</task_order>
