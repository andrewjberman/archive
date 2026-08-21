<to_id>ADHC_GLDINC.SS4c</to_id>
<project>ADHC_GLDINC</project>
<title>SS4c — periodic-oracle re-validation for the GLDINC P1 load_flows cutover (the standing verifier the L3-cleanup retired)</title>
<assigned_to>0.6.0_AE_PartnerETL</assigned_to>
<co_assignees>0.7.0_AE_CloudOps — runner-scheduling + cost-safety consult (the full_scan runs on the c6i gold runner = 34% of the cloud bill; the cadence/compute-footprint must be CloudOps/NFRA_COSTAWS-sane before the schedule deploys)</co_assignees>
<issued_by>2.0.0_SA_COO (CVO 06-17 action item 143909Z -> CTO scope-bless 144451Z; single-router dispatch)</issued_by>
<issued_date>2026-06-17</issued_date>
<status>superseded 2026-08-21T14:4xZ by the ISSUER (COO), on AE's 64682 recommendation. PARENT-DEAD: its program parent ADHC_GLDINC.P1 was flipped superseded @bd6195b34e as the 2026-08-04 Andrew shadow/comparator COMPLETE-VETO class (shadow harness + standing gold/_parity comparator + daily scorecard). A periodic-cadence revalidation TO for an oracle whose parent build is vetoed has no subject to revalidate. SECOND, INDEPENDENT REASON: "periodic oracle revalidation" is itself cadence-shaped QA machinery and needs testing against the 2026-07-28 monitoring moratorium before any GO -- I am not re-confirming it, so it does not survive on that ground either. Age at supersede: 65d pending. THE UNDERLYING I/O-CUT NEED SURVIVES AND IS NOT STRANDED (lib/nna_flows.py:87 full-scans silver/transactions ~4x/night); per AE it re-forms as build-correctly-and-port needing FRESH COO/CTO endorsement -- and if that re-forms, any oracle-revalidation need re-forms WITH it, scoped then, not carried forward on this file. NO BUILD WORK STRANDED: build endorsement was never granted.</status>
<!-- GROUNDED STATUS 2026-06-25 (0.6.0_AE, COO GO): the oracle is BUILT+DEPLOYED+WIRED+RUNNING,
NOT unbuilt -- gldinc_ss4c_weekly.py @ opal-data-bd/code/gold (06-22), Wed leg in gold_dispatch.sh:1349-69
(CloudOps-signed placement), TIER-1 canary live (gldinc-ss4c-canary), TIER-2 alarms exist, parity
scorecards landing (gold/_parity/load_flows/ss4c/06-23,24/). BUT it was BLIND: WeeklyScorecardClean=0
datapoints/30d (absence alarm firing on a working verifier). Two root breaks FIXED: (1) IAM -- runner role
bd-exporter-ec2-role had NO cloudwatch:PutMetricData -> GLDINC/SS4c AccessDenied; GRANTED ns-scoped + APPLIED
(commit 3ad886929, comp-iam clean). (2) _emit float(None) crash on a clean DELTA=0 scorecard; fix authored +
unit-verified, handed to DS as a patch (Rule-13 gold-script lane; DS accepted+queued, deploys at next
breakpoint, metric lands the 07-01 Wed nightly). NOT cost-gated (zero compute change; placement already
CloudOps-signed). REMAINING: watch-the-watcher (#2, register ss4c-weekly-absence sub-presence into
comp-surface-check/D8 -- offered to author through 0.7.0/base-AE owner, awaiting COO sequencing) + cost-model
NFRA_COSTAWS §7 line (#3, CloudOps). The verifier-emits-and-alarms CORE is one DS-deploy from DONE. -->

<priority>NEAR-TERM, not a fire. The GLDINC P1 cutover is clean by EMPIRICAL basis (9-night 06-08..06-16 windowed-vs-full_scan DELTA=0 + fresh 06-17 canary + shadow-free deploy) — but post-L3-cleanup there is NO LIVE oracle verifier on the runner, so the DELTA=0 guarantee now rides BY-CONSTRUCTION only. The retired gate (windowed-vs-full_scan via shadow.py) is the entrypoint-delegation-tautology class (a cutover that repoints/retires its own oracle defeats the gate). Build the standing verifier before that guarantee rides indefinitely. GO-at-capacity for 0.6.0_AE (its morning-surge loops are closed); behind any real interrupt (e.g. an Andrew "chase the BD-source stall" call).</priority>

<references>
  <ref type="design-authoritative">CVO SS4c/§4c design = cert **cvo_1330Z** (06-16, ACCEPTED-CVO of PRD §4c) — THE authoritative build-spec (CVO provided this pointer 144616Z; no need to chase). This TO is the governance wrapper; cvo_1330Z is the mechanism. CVO owns design + scope + re-cert at build (per the §8 close-gate fold), NOT the hands-on build. CVO is heads-down on TO-3 — do not block it; the §4c scope is ready-to-hand in cvo_1330Z.</ref>
  <ref type="cutover-context">GLDINC P1 L4 CVO cert 143909Z (GREEN deploy-completion; honest could-not-exercise-fresh-number gap -> SS4c is the fix). Deployed gold_dispatch ETag e643bc51 (shadow-free); nna_flows.py md5 9ab99533 (deployed==committed).</ref>
  <ref type="discipline">memory/reference_entrypoint_delegation_defeats_name_based_oracle_harness_tautology + reference_verify_alert_egress_and_absence_coverage_not_topic_exists (a periodic oracle that only signals success can't detect a frozen/diverged producer — it MUST emit a genuine DELTA + alarm on divergence/absence).</ref>
  <ref type="cost-constraint">memory/feedback_no_adhoc_gold_runs_validate_on_scheduled_nightly + reference_bd_gold_qa_runner_c6i16xlarge_purpose_kept_prod_isolation — NO ad-hoc heavy gold runs to validate; the c6i runner is 34% of the bill. SS4c must be cost-safe by design (piggyback the scheduled nightly's artifacts / lightweight cadence), NOT a manufactured heavy full_scan run.</ref>
</references>

<scope>
Build the runner-side scheduled full_scan-vs-served re-validation that produces a GENUINE periodic DELTA for the GLDINC P1 load_flows cutover — restoring the live oracle the L3-cleanup removed, WITHOUT manual heavy compute. Per CVO's accepted design (authoritative). The job: on a scheduled cadence, compute the full_scan (or its design-equivalent) result and diff it against the SERVED windowed output -> emit a real DELTA metric; alarm on divergence (DELTA != 0 beyond tolerance) AND on absence (the re-validation didn't run / produced no datapoint — a frozen verifier is itself a finding).

DO: pull + implement CVO's accepted design; schedule cost-safe (Terraform-managed EventBridge/cadence; piggyback the scheduled nightly's heavy artifacts rather than a manufactured run — coordinate the compute-footprint with CloudOps); emit a DELTA metric + a divergence alarm + an absence/staleness alarm (egress-verified per the absence-coverage discipline).
DO NOT: trigger ad-hoc heavy gold/full_scan runs to validate (NFRA_COSTAWS / Andrew compute-discipline); build a success-only signal (must emit a real DELTA + catch divergence AND absence); deploy the schedule before CloudOps signs the runner-cost-footprint.

MUST FOLD — the 3 unknown-unknowns CVO surfaced in cvo_1330Z (these are build requirements, not options):
1. CADENCE = DAILY cheap structural/dtype canary on the cache parquet (closes the weekly-value-diff blind window — a daily light check catches a structural break fast) + WEEKLY full value-diff (the genuine DELTA). Not a single cadence — the cheap-daily + heavy-weekly split is what keeps it cost-safe AND closes the blind window.
2. WATCH-THE-WATCHER: register the re-validation's absence-alarm SUBSCRIBER-PRESENCE into comp-surface-check / the critical-surface registry, so a later subscriber-removal RE-FLAGS — do NOT recreate the globgrph 0-sub-topic class one level up (a verifier whose own alarm has no subscriber is silently blind). NOTE: this folds into 0.7.0_AE_CloudOps's D8 critical-surfaces registry (it's actively re-working that infra in NFRA_GRAPHS.D8-FP) — author this limb through base-AE owner-review (cross-tool, LD-0193: author-by-anyone, review+commit-through-owner).
3. COST-MODEL: add the standing verifier to NFRA_COSTAWS §7 as a PERMANENT recurring line + STAGGER the per-phase weekly oracles (don't bunch the heavy weekly diffs). CloudOps co-owns this (NFRA_COSTAWS).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before build">
    <step>
      <run>comp-pipescript io load_flows (+ the nna_flows windowed transform) — confirm the full_scan vs windowed entry points + the served artifact the DELTA diffs against</run>
      <expect>The full_scan oracle path + the served windowed output are both identified; the DELTA is full_scan-equivalent vs SERVED (not windowed-vs-windowed = the tautology to avoid). Point the harness at the preserved full_scan, NOT the delegating name.</expect>
      <if_mismatch>If the only available oracle is the delegating windowed name (windowed-vs-windowed), that's the tautology — STOP, the DELTA would be vacuous; reconcile with CVO's design (which addresses this) before building.</if_mismatch>
    </step>
    <step>
      <run>comp-iam service {the SS4c runner/Lambda identity} — any new perms for the scheduled re-validation (S3 reads of served + full_scan compute)</run>
      <expect>Existing runner/role perms cover the reads; new schedule trigger perms via Terraform only.</expect>
      <if_mismatch>Add via Terraform + comp-iam gaps at Phase 2.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before deploy">
    <step>
      <run>comp-iam gaps (if iam.tf changed) + CloudOps cost-footprint sign-off on the cadence/compute</run>
      <expect>No new IAM gap; CloudOps confirms the schedule's compute-footprint is NFRA_COSTAWS-safe (no manufactured heavy run; piggyback or lightweight).</expect>
      <if_mismatch>Resolve before apply (Terraform-only); do NOT deploy a schedule CloudOps hasn't cost-signed.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>Verify the SS4c re-validation FIRES on its cadence + emits a genuine DELTA + a SYNTHETIC divergence test alarms</run>
      <expect>The scheduled job runs, produces a real full_scan-vs-served DELTA datapoint (DELTA=0 on the clean cutover), AND a synthetic injected divergence FIRES the alarm (egress-verified — not success-only), AND an absence (job-didn't-run) also alarms.</expect>
      <if_mismatch>If it only emits on success / doesn't catch a synthetic divergence or absence, it's a positive-only signal (the blind spot it exists to close) — fix before RAVC.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- PULL CVO's accepted SS4c design FIRST (authoritative mechanism) — this TO is the governance wrapper, not the mechanism spec. Coordinate with 3.0.0_SA_CVO (on TO-3; async).
- CloudOps (0.7.0_AE) cost/scheduling consult is BINDING before the schedule deploys: the full_scan runs on the c6i gold runner (34% of the bill) — the cadence + compute-footprint must be NFRA_COSTAWS-safe (piggyback the scheduled nightly artifacts, not a manufactured heavy run). CloudOps signs the footprint.
- Deploy-completion (the L4 ledger close, DS, separate) vs ongoing-verification (this SS4c) are DISTINCT — closing L4 does NOT wait on SS4c; SS4c does not block the L4 close. They are independent per CVO's framing.
</cross_domain_coordination>

<acceptance_criteria>
- A scheduled (Terraform-managed) runner-side re-validation that emits a GENUINE full_scan-vs-served DELTA on its cadence (DELTA=0 on the clean cutover), restoring the live oracle the L3-cleanup retired.
- Divergence alarm (DELTA beyond tolerance FIRES) AND absence/staleness alarm (verifier-didn't-run FIRES) — egress-verified via a synthetic test, NOT a success-only signal.
- Cost-safe: NO ad-hoc heavy gold/full_scan run; CloudOps cost-footprint sign-off recorded.
- Built to CVO's accepted design; points the oracle at the preserved full_scan (not the delegating windowed name = the tautology).
- Deployed via Terraform; comp-iam gaps clean if iam.tf changed. Session-log Compiler Tools section reproduces every <run> + pass/fail. RAVC2 to COO (CC CTO + CVO — CVO owns the design + re-cert).
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Adds a read-only re-validation job + its schedule + alarms; reads existing served + full_scan-equivalent artifacts. No pipeline/data re-emit; no change to the load_flows transform.</no_reprocess_needed></data_reprocess_scope>
