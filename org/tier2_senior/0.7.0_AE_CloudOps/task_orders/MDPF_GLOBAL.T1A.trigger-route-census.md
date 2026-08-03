<task_order>
<to_id>MDPF_GLOBAL.T1A.trigger-route-census</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<date>2026-08-03</date>
<status>complete</status>
<priority>P1 (Andrew-direct GO 2026-08-03 ~20:15Z, recorded @3e2b23ebb3 -- "we are ready to begin"; first-wave parallel census on the MDPF_GLOBAL dependency spine)</priority>

<title>T1.A: Trigger + route census -- enumerate EVERY trigger touching MDPF artifacts, disposition each, diff against the 07-29 trigger map</title>

<context>
MDPF_GLOBAL PRD Addendum C (docs/architecture/MDPF_GLOBAL_PRD.md s.C.2/C.4). The live defect this
census grounds: `mdpf-daily-refresh-trigger` carries ScheduleExpression=None and fires ONLY on INF's
completion sentinel (s3://opal-data-inf/gold/meta/pipeline-complete.json). INF wrote
`pipeline-failed.json` at 10:50 ET on 2026-08-03, so the runner chain never fired and the Global view
regressed -- the memo's anti-pattern reproduced same-day (NEVER#4: a pipeline whose only trigger is
another pipeline's success has no schedule and is a defect). Meanwhile the scheduled accrual family
(`mdpf-accrual-bridge-daily` cron(45 15 UTC) -> `mdpf-accrual-trigger`) DID run.

This census is the denominator for T2.B (producer unification ruling, CTO), T1.B (code-store
migration), and T5.A (legacy kill-list). It must be complete or the downstream rulings rest on a
partial map.

SCOPE OF ENUMERATION (every surface, all four MDPF scopes {49financial, inflection, cottonwood,
global}, BOTH platinum planes (hyphen `aggregate-aua-timeseries.json` + underscore
`aggregate_aua_timeseries.json`), legacy `json/mdpf/*` routes):
- EventBridge RULES (aws events list-rules -- token-walked; 142-rule estate measured 07-31)
- EventBridge SCHEDULER schedules (aws scheduler list-schedules -- a SEPARATE surface; both required)
- S3 bucket notification configurations (opal-data-mdpf, opal-data-inf, opal-data-portal-v2, and any
  bucket the comp-estate chains name)
- SSM associations / the runner dispatch path (mdpf-daily-dispatch.sh pull from opal-data-mdpf/code/)
- CloudWatch-side triggers only as they EXIST (moratorium: nothing new gets built)

COO grounding already run (2026-08-03 20:0xZ, reproduce at Phase 1, do not inherit):
- comp-estate mdpf: 2 chains (event-gated runner chain via mdpf-daily-trigger; accrual/scheduled
  family) + mdpf-freshness-checker cron(45 16) exists.
- comp-routes trace: /api/general/mdpf/* -> platinum/mdpf/* (DESIRED plane); serve reads the HYPHEN
  artifact.
- comp-blast mdpf_aggregate_aua: 13 corpus HOLD claims incl.
  org/critical_paths/DO_NOT_DECOMMISSION_portal-v2_json_mdpf_49financial_20260722.md -- any resource
  named in a HOLD doc is dispositioned CANONICAL-or-UNKNOWN, NEVER LEGACY-KILL-CANDIDATE, until the
  cited doc is read and the disposition carries that citation.
</context>

<scope>
1. Enumerate every trigger per the surfaces above. Print the DENOMINATOR per surface and the
   pagination method used (the `--query length()` page-count trap is banked law: the CLI applies
   --query PER PAGE; use --no-paginate or explicit token walking, and say which you used).
2. Disposition EVERY entry: {CANONICAL / ACCELERATOR / LEGACY-KILL-CANDIDATE / UNKNOWN-loud}.
   UNKNOWN is legal and loud, never silent. HOLD-doc-named resources per the context rule.
3. Diff the census against docs/briefs/TRIGGER_GRAPH_AND_RUNTIME_MAP.md (07-29 vintage); enumerate
   every drift (zero drift is also an explicit finding, not silence).
4. Deliverable: one machine-readable census table (JSON or YAML) + a human doc, committed under
   org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_GLOBAL_T1A/. (s.C.4 suggests an
   org/tier1_exec/ home; owned-paths makes your own deliverables folder the safe canonical home --
   COO ferries a pointer to CTO at acceptance. CTO may redline the location.)
5. READ-ONLY census: no trigger is created, modified, disabled, or deleted in this WS. No alarms,
   no monitors (standing moratorium).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before census">
    <step>
      <run>comp-estate mdpf</run>
      <expect>2 chains: event-gated runner chain (mdpf-daily-trigger -> SSM -> mdpf-daily-runner EC2) + accrual/scheduled family; mdpf-freshness-checker cron listed. Chain prose seeds the bucket list for the S3-notification surface.</expect>
      <if_mismatch>STOP. If the estate map names chains or buckets this TO's surface list omits, WIDEN the census scope first and note the addition to COO.</if_mismatch>
    </step>
    <step>
      <run>comp-blast mdpf_aggregate_aua</run>
      <expect>HOLD claims present (13 at COO's 2026-08-03 run) naming DO_NOT_DECOMMISSION + MDPF_EXECUTION_PLAN critical-path docs.</expect>
      <if_mismatch>If HOLD count differs, read the new/removed claims before dispositioning anything they name.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="during census, before commit">
    <step>
      <run>aws events list-rules --no-paginate ... # rail-checked: T1.A live trigger census; comp-estate/comp-aws seeded the map, live enumeration is the census act itself</run>
      <expect>Full rule list with denominator printed; every MDPF-relevant rule captured with its state (ENABLED/DISABLED) + targets (aws events list-targets-by-rule per rule, token-walked).</expect>
      <if_mismatch>STOP. A truncated or page-counted enumeration is not a census. Re-derive with explicit token walking.</if_mismatch>
    </step>
    <step>
      <run>aws scheduler list-schedules --no-paginate ... # rail-checked: same census act, Scheduler surface</run>
      <expect>Scheduler surface enumerated separately from EventBridge rules (they are different APIs); denominator printed.</expect>
      <if_mismatch>STOP. Missing surface = incomplete denominator.</if_mismatch>
    </step>
    <step>
      <run>diff census vs docs/briefs/TRIGGER_GRAPH_AND_RUNTIME_MAP.md</run>
      <expect>Every drift enumerated with direction (map-has/live-lacks vs live-has/map-lacks); zero-drift stated explicitly if so.</expect>
      <if_mismatch>N/A -- drift IS the deliverable content, not a failure.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>report to COO + CTO with per-surface denominators + disposition counts</run>
      <expect>MCP report cites the committed census path + commit hash; UNKNOWN count named loud.</expect>
      <if_mismatch>A report without denominators is REWORK.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Read-only census; no shared writes. Shared READ surfaces with T3.A (0.7.0_AE_CloudOps~F, CloudFront
distribution config) and T2.A (0.2.0_DS_PortfolioAnalytics, producer code) -- disjoint deliverables,
no coordination gate needed. Your census feeds T1.B (your own likely follow-on), T2.B (CTO ruling),
and T5.A. If the census surfaces a trigger ANOTHER live TO is mutating, MCP that owner before
dispositioning it.
</cross_domain_coordination>

<acceptance_criteria>
Verbatim s.C.4 (CTO validates at close):
1. Denominator printed + token-walked pagination (the `--query length()` page-count trap is a
   banked law).
2. EVERY entry dispositioned {CANONICAL / ACCELERATOR / LEGACY-KILL-CANDIDATE / UNKNOWN-loud}.
3. Diffed against docs/briefs/TRIGGER_GRAPH_AND_RUNTIME_MAP.md (07-29 vintage) with drift enumerated.
Plus standing norms (s.C.4 header): scheduled-run evidence only where run evidence is cited; every
causal claim cites file:line @ commit or is labeled INFERRED; no new alarms/monitors.
Plus: session log includes a Compiler Tools section reproducing every <run> from
<compiler_tools_mandate> with observed output and explicit pass/fail vs <expect>. Missing rows =
REWORK, not COMPLETE.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/MDPF_GLOBAL_PRD.md (Addendum C, s.C.2 T1 + s.C.4 T1.A row)</ref>
  <ref type="memo">docs/references/MDPF_ARCH_CLEANUP_ANDREW_MEMO_20260803.md</ref>
  <ref type="baseline">docs/briefs/TRIGGER_GRAPH_AND_RUNTIME_MAP.md (07-29 vintage diff baseline)</ref>
  <ref type="go">Andrew-direct GO @3e2b23ebb3 (memo-doc s.5); CTO relay 20260803T200329Z</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
