# TO MDPF_REMED.RP-W3 — CADENCE ⛔ DOUBLE-GATED: RP-W1 COMPLETE + ANDREW'S CLOCK RULING. NEVER ALONE.

<task_order id="MDPF_REMED.RP-W3" project="MDPF_REMED">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-10T23:4xZ</issued>
<status>staged</status>
<priority>P0 once un-gated. ⛔ STAGED BY DESIGN — see the gate block. A GO for this TO comes ONLY
from COO, and COO issues it ONLY after BOTH gates read true. If you receive a GO that does not cite
both gates, treat it as mis-sent and query COO.</priority>

<dependencies>
  <dependency agent="0.4.0_DS_ClientPlatform" task="MDPF_REMED.RP-W1" status="complete"/>
  <dependency agent="ANDREW" task="floor/pull clock re-ruling (his (B) predates the premise change; see plan §2-W4 note + COO decision memo)" status="pending"/>
</dependencies>

<references>
  <ref type="plan">org/tier1_exec/1.0.0_SA_CTO/deliverables/MDPF_REMEDIATION_PLAN_20260810.md @dbbbfa9cd3 (W3, §0 D-19)</ref>
  <ref type="context">org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_REMED_DECOMPOSITION_AND_SEQUENCE_20260810.md — Addendum 3 (cot census: cot-bd-session-trigger is a FOUR-entry function; a retime moves ONE entry point), §0 (both mirror schedules run ALL FOUR rows — a "cot" mirror move is an inflection change), Track A cutover-gap precedent (ce99054e44 manufactured the 08-06 hole)</ref>
</references>

## ⛔ WHY THIS TO CANNOT BE PICKED UP ALONE — D-19, measured end to end, carried verbatim
Move the floor later OR the pulls earlier ON ITS OWN and the frontier becomes 2026-08-07, WHICH
ECLIPSE HAS. 08-06 stops being the frontier, both legs go None, THEY AGREE, and limb (v) STOPS
FIRING. Under the run-date ruling that cycle then PUBLISHES ONE TRADING DAY MISLABELLED INSTEAD OF
REFUSING. **The label offset (RP-W1) must land BEFORE this. If you execute this TO with RP-W1
incomplete, you have not "started early" — you have recreated the defect and silenced the only guard
keeping a wrong number off the served plane.**

## SCOPE (once un-gated)
Current order is backwards: floor reads 13:00Z; smartx silver 13:40:47Z (AXIS SOURCE), orion
14:16:05Z, eclipse 22:31:08Z land after. **THE BOTTLENECK IS THE MIRRORS, NOT THE VENDORS** —
eclipse data sits in `opal-data-inf` by ~14:48Z and waits ~7.5h for the 22:30Z mirror.
- Proposed shape (CTO; final numbers subject to Andrew's clock ruling): mirrors → ~13:45Z (after the
  pulls land) → eclipse/orion silver ~13:46Z; floor → 14:00Z; bridge + publisher shift behind it.
- **The smartx leg needs NO new trigger** — chained to the pull's OnSuccess (G-1a): moving the pull
  moves the conversion. (RP-W5 separately moves smartx onto the S3-object pattern; coordinate — see
  cross-domain block.)
- ⚠ Both mirror schedules invoke ONE all-rows function (`lambda_function.py:353`, `event` never
  read) — any mirror move is simultaneously an inflection change. If RP-W4's firm selector (route b)
  lands first, retime per-firm; if not, state the all-rows consequence in your apply plan.
- ⚠ EVERY RETIME STATES ITS CUTOVER-GAP PLAN BEFORE IT APPLIES (double-run vs skipped-day): the
  ce99054e44 apply manufactured the 08-06 missing partition — the precedent is in THIS function.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-blast opal-assets-ingest-mirror</run>
      <expect>Radius includes mdpf-daily-refresh-trigger, inf-* event rules, cot-* event rules, opal-*-served-guard-on-write. Any NEW node vs this TO's issue-date radius = re-ground before proceeding.</expect>
      <if_mismatch>STOP. Surface the new consumer to COO before any schedule edit.</if_mismatch>
    </step>
    <step>
      <run>comp-trigger --list (mdpf + cot + inf filters)</run>
      <expect>Current schedule state enumerated. ⚠ KNOWN INSTRUMENT DEFECT: comp-trigger reports TF-DESIRED "not found" for INTERPOLATED resource names (e.g. "${local.mirror_name}-cot-daily-et", mirror.tf:138-149). A not-found here is NOT console drift — read the .tf file before concluding anything.</expect>
      <if_mismatch>Read infra/aws/terraform/opal-assets/mirror.tf + schedule-et.tf directly; never conclude console drift from this tool on this estate.</if_mismatch>
    </step>
    <step>
      <run>comp-iam service opal-assets-ingest-mirror (if any boto3/resource change rides along)</run>
      <expect>No gaps on the retimed path. NECESSARY NOT SUFFICIENT — new bucket/table/ARN needs live simulate-principal-policy, one --resource-arns per call, positive control in a separate invocation.</expect>
      <if_mismatch>Close the gap in iam.tf via Terraform before apply.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before apply">
    <step>
      <run>.tools/safe-apply.sh (never bare terraform apply); commit before apply per Deployment Rule 2</run>
      <expect>Plan shows ONLY the scoped schedule/trigger changes; 0-diff after apply; tag + push --follow-tags.</expect>
      <if_mismatch>STOP at the HALTGT checkpoint discipline; do not proceed on a dirty plan.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after apply">
    <step>
      <run>one full SCHEDULED cycle observed (ad-hoc runs are QA, never production evidence)</run>
      <expect>Every consumed silver partition's C1 precedes the floor's read, measured on that scheduled cycle.</expect>
      <if_mismatch>Roll back within the same window per the deploy-completion ledger discipline; surface to COO. A half-landed retime does not sit overnight.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
opal-assets-ingest-mirror is shared with RP-W5 (same owner — you). Sequence within your lane:
RP-W5's assertion-narrowing must not be conflated with this retime, and this retime must not be
credited with fixing the mirror's 14-day failure (D-16 is RP-W5's). mdpf-daily-refresh-trigger is in
the blast radius — its OnSuccess chain semantics are load-bearing for the smartx leg. RP-W4 (naming/
firm-selector) is BLOCKED ON ANDREW; if route (b) lands first it changes your retime mechanics —
check with COO at GO time.
</cross_domain_coordination>

<acceptance_criteria>
1. Every consumed silver partition's C1 precedes the floor's read, MEASURED ON ONE SCHEDULED CYCLE
   (not ad-hoc).
2. Cutover-gap plan stated in writing BEFORE the apply; post-apply, show the gap did not occur (no
   skipped business day, no double-run) or was handled per plan.
3. Session log Compiler Tools section reproduces every &lt;run&gt; + observed output + pass/fail.
4. Do NOT report inflection or global fixed by this TO — a schedule fix moves two of four scopes.
</acceptance_criteria>
</task_order>
