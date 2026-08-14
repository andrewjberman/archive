# TO MDPF_TRGALN.TO-0 — Verify windows + pin residual writer + Terraform coverage census (imports only; NO retime edits)

<task_order id="MDPF_TRGALN.TO-0" project="MDPF_TRGALN">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T05:0xZ</issued>
<status>active</status>
<priority>P0 — GO ON RECEIPT. Part A (census + imports + writer pin) executes NOW. Part B (vendor-window
probes) executes LATE (~09:00–10:30Z) or FOLDS into today's first scheduled fire as the oracle (CTO
risk-frame 20260814T044742Z). TIME-CRITICAL: TO-1/2/3 applies must land before 09:45Z (05:45 ET) for
today's cycle to be the acceptance cycle — do not let Part B block Part A.</priority>

<dependencies>
  <dependency agent="none" task="First in sequence. TO-1/TO-2/TO-3 GO gates on this TO's Part A proof (rev 1); TO-4 close gates on the final rev (Part B window claims)." status="n/a"/>
</dependencies>

<references>
  <ref type="prd">docs/architecture/MDPF_TRGALN_PRD.md @2886349fcd — §2 current state, §3 THE DETERMINISTIC SPEC, §4 TO-0, §7 proof schema</ref>
  <ref type="context">CTO handoff 20260814T044542Z + CTO risk-frame 20260814T044742Z (probe-late sequencing; retimes cannot make any firm staler than today)</ref>
</references>

## PART A — BLOCKING, EXECUTE NOW

**A1. Terraform coverage census over every §3 row.** Resolve each of the 13 §3 resources (+ the
unchanged floor) in `terraform state list` — NEVER text-grep alone. ⚠ Known instrument defect
(MDPF_REMED RP-W3, carried): comp-trigger reports TF-DESIRED "not found" for INTERPOLATED resource
names (e.g. `${local.mirror_name}-cot-daily-et`, opal-assets mirror.tf) — read the .tf file before
concluding a resource is unmanaged.

**A2. Import each genuinely-unmanaged resource BEFORE any retime edit.** Candidates per PRD §2:
- #3 `opal-assets-mdpf-portal-publisher-daily` (scheduler)
- #5 `opal-assets-ingest-mirror-cot-daily-et` (scheduler)
- #6 `opal-assets-ingest-mirror-inf-daily` (events-rule)
- #7 `opal-assets-silver-blackdiamond-sweep-daily` (events-rule)

`terraform import` into the owning module + a `plan` proving **0-diff import fidelity** before any
edit. Import commits ride Rule 14a mechanics (safe-commit, `-F` msgfile). ⛔ CTO-BINDING carried from
MDPF_REMED (000333Z): every TF apply in the opal-assets root is `-target`ed AND its plan output READ
before apply — the root plan has carried a re-create of `opal-assets-daily-aua` (a table Andrew
DELETED 08-07); an un-targeted apply RESURRECTS it.

**A3. Pin the `blackdiamond/cottonwood/gold/dim_model_portfolio` writer.** It wrote date=2026-08-13
at ~15:01Z; hypothesis (INFERRED, unconfirmed): invoked off the INF-sentinel event path. Pin via
CloudWatch invocation trace of the writing Lambda. If its timing does NOT already fall before the
floor under the §3 targets, SURFACE to COO for a TO-1 scope amendment — do not self-amend.

## PART B — LATE OR FOLDED (CTO risk-frame; ad-hoc = QA-legal, run-and-read, NEVER production evidence)

> **AMENDED per PRD v1.1 §8.1 @f50ee7223b (Andrew-direct, sovereign vendor ground-truth): Black
> Diamond refreshes by ~01:02 ET, other vendors "likely not long after" — it is past 01:02 ET, so
> B1/B2 may run NOW as CONFIRMATIONS, not open questions. The §4 fork table stands; its expected
> outcome is (a). Timing below is superseded; run the probes whenever they fit your Part-A pace.**

**B1. COT vendor window:** one ad-hoc QA session run (`cot-bd-session-trigger` invoke) in the
07:30 ET window (11:30Z), OR fold into today's first scheduled fire at the new time (post-TO-1) as
the oracle. Read the pulled holdings vintage — must be T-1 per `lib/trading_calendar.py`. cot
converters are date-partition idempotent; a later scheduled run re-lands identical partitions.

**B2. INF vendor window:** one ad-hoc non-destructive Orion/Eclipse pull probe at the worst-season
wall-clock of cron(2 11Z) (≈06:02 ET EST / 07:02 ET EDT — tonight: as late as feasible, ~09:50Z+),
OR fold into today's first scheduled fire (post-TO-2). Read returned max-date == T-1. Design the
probe non-destructively (bronze is date-partitioned + idempotent; nothing standing).

## PRE-REGISTERED ADJUDICATION TABLE (PRD §4, verbatim; decided BEFORE evidence)

- (a) both vendor windows PASS → TO-1..TO-4 proceed as specced.
- (b) COT passes, INF fails → TO-1 proceeds; INF leg halts; escalate to Andrew with the measured
  earliest INF availability + the ET-scheduler migration option (rule→`aws_scheduler_schedule`
  ET-timezone, precedent `cot-pipeline/schedule-et.tf`).
- (c) COT fails → halt COT+INF legs; escalate to Andrew with measured earliest availability.
  **Do NOT unilaterally fall back to moving the MDPF trio later — that inverts the directive.**
- TO-3 (accrual/publisher −30m) proceeds under ALL outcomes; it is independent of vendor windows.

## COO SEQUENCING RULING (recorded for audit; per CTO risk-frame 044742Z)

TO-1/TO-2/TO-3 GO gates on **Part A proof only** (`proof_TO-0.json` rev 1: census + import-fidelity +
writer-pin claims). Part B claims are APPENDED to `proof_TO-0.json` (final rev) and gate the TO-4
close, not the retime applies. Rationale (CTO, verbatim class): landing the retimes cannot make any
firm staler than today — worst case COT/INF pull yesterday's vintage at the new hour and serve
exactly the T-2 they serve now; rollback is a same-window cron revert. If today's cycle then shows a
firm still T-2, that IS the vendor-window fork — escalate per the table with measured availability.

<compiler_tools_mandate>
  <phase id="1" when="before any import">
    <step><run>comp-trigger &lt;resource&gt; for every §3 row (pre-state) + comp-blast on any touched Lambda name</run>
    <expect>Pre-state schedule strings match PRD §2 verbatim; blast radius carries no NEW consumer vs PRD issue-date.</expect>
    <if_mismatch>STOP. Surface the delta to COO before any import.</if_mismatch></step>
  </phase>
  <phase id="2" when="imports">
    <step><run>commit-before-apply → .tools/safe-apply.sh (never bare terraform apply), -target scoped, plan READ</run>
    <expect>Plan = expected-rows-only; import fidelity 0-diff BEFORE any edit; NO opal-assets-daily-aua row. comp-iam not required (no new boto3, no IAM edits); if an import touches IAM, run comp-iam gaps before apply.</expect>
    <if_mismatch>STOP on a dirty plan; surface to COO.</if_mismatch></step>
  </phase>
  <phase id="3" when="after">
    <step><run>terraform state list re-read + live `aws scheduler get-schedule` / `aws events describe-rule` (APPLIED layer)</run>
    <expect>Every §3 row resolves in TF state; applied schedule strings still match §2 (imports change nothing).</expect>
    <if_mismatch>Roll back in-window; surface to COO.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<proof_of_spec>
Path: org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_TRGALN/proof_TO-0.json per PRD §7.
Rev 1 (gates TO-1/2/3 GO): census claim per §3 row (field: tf_state_address; expected: managed),
import claims (plan_zero_diff true), writer-pin claim (CloudWatch trace evidence + timing verdict vs
floor). Final rev (gates TO-4 close): + B1/B2 window claims. `expected` strings VERBATIM from §3;
every claim carries desired/applied/exercised; forks land in `forks_hit`.
</proof_of_spec>

<acceptance_criteria>
1. Every §3 resource resolves in `terraform state list` (census table in proof, denominator printed).
2. Each unmanaged candidate imported with plan_zero_diff BEFORE any retime edit; commit hash recorded.
3. dim_model_portfolio writer pinned with invocation-trace evidence; before/after-floor verdict stated.
4. Part B window claims carry all three grounding layers; any fork routed per the table (to ANDREW),
   never a unilateral fallback.
5. No alarms/monitors/SNS/SES built anywhere; no shadow paths; nothing standing (moratorium, Andrew-direct 2026-07-28).
</acceptance_criteria>
</task_order>
