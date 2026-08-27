# TO MDPF_TRGALN.TO-3 — MDPF trio tighten (§3 rows 2, 3): accrual + publisher −30m; floor untouched

<task_order id="MDPF_TRGALN.TO-3" project="MDPF_TRGALN">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T05:0xZ</issued>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project MDPF_TRGALN, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending</status>
<priority>P0 — STAGED. GO comes ONLY from COO, citing proof_TO-0.json rev 1 validated (the #3
publisher import is the gate; vendor-window outcomes do NOT gate this TO — per PRD §4 it proceeds
under ALL adjudication outcomes). TIME-CRITICAL once GO'd: apply before 09:45Z (05:45 ET).</priority>

<dependencies>
  <dependency agent="0.7.0_AE_CloudOps" task="MDPF_TRGALN.TO-0 Part A — specifically the #3 opal-assets-mdpf-portal-publisher-daily import (import-first, PRD §4)" status="pending"/>
</dependencies>

<references>
  <ref type="prd">docs/architecture/MDPF_TRGALN_PRD.md @2886349fcd — §3 rows 2/3, §4 TO-3, §7 proof schema; §0 Andrew verbatim: "i dont think we need to wait until 10:10 and 10:20, seems like both of those could be pushed 30 min earlier"</ref>
</references>

## THE SPEC (PRD §3, VERBATIM — proof `expected` strings copy these exactly)

| # | Resource | Current | **TARGET** | Why |
|---|---|---|---|---|
| 2 | `mdpf-accrual-bridge-daily` | cron(10 14Z) | **cron(40 13Z)** | Andrew: 30 minutes earlier |
| 3 | `opal-assets-mdpf-portal-publisher-daily` | cron(20 14Z) | **cron(50 13Z)** | Andrew: 30 minutes earlier — page publishes 09:50 ET (EDT) with all three firms T-1 |

⛔ Floor (`mdpf-scheduled-floor`, cron(30 13Z)) is UNCHANGED BY DECLARATION — a plan showing a floor
row is a dirty plan. End-state ordering: floor 13:30Z → accrual 13:40Z → publish 13:50Z.

## MECHANICS

Row 2 TF home: `infra/aws/terraform/mdpf-pipeline/accrual-bridge.tf`. Row 3: post-import home from
TO-0 (import-first; editing an unimported resource is the drift NEVER this project exists to close).
Same mechanics: edit → safe-commit → safe-apply → 0-diff → tag → push --follow-tags; deploy ledger
opened/closed (NEVER#6); opal-assets-root portions `-target`ed + plan READ (daily-aua resurrect
hazard).

Cutover-gap statement BEFORE apply. Expected shape today (apply ~09:0xZ): both old fire-times
(14:10Z/14:20Z) replaced by earlier new times (13:40Z/13:50Z) — one fire each today at the new
time, no skip, no double-run. State it, then show it held.

## EXERCISED EVIDENCE (PRD §4, verbatim)

Platinum publish LastModified ≈ 13:50Z, all four scopes written in the same pass. (Firm T-1
correctness is TO-4's claim set — this TO's exercised layer is the trio's ORDERING+STAMP, not the
vendor outcome; do not hold this proof for firm staleness.)

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-trigger for rows 2/3 (pre-state) + comp-blast on mdpf-accrual-trigger and opal-assets-mdpf-portal-publisher</run>
    <expect>Pre-state strings match §2 verbatim (cron(10 14Z) / cron(20 14Z)); no NEW consumer vs PRD issue-date.</expect>
    <if_mismatch>STOP; surface to COO.</if_mismatch></step>
  </phase>
  <phase id="2" when="before apply">
    <step><run>commit-before-apply; .tools/safe-apply.sh; -target scoped; plan READ</run>
    <expect>Plan = the two schedule rows ONLY; NO floor row; NO opal-assets-daily-aua row; 0-diff after apply; tag + push --follow-tags.</expect>
    <if_mismatch>STOP on a dirty plan.</if_mismatch></step>
  </phase>
  <phase id="3" when="after apply">
    <step><run>comp-trigger re-run + live `aws scheduler get-schedule` (APPLIED) + today's publish stamp read</run>
    <expect>Applied strings == §3 targets verbatim; publish stamp ≈ 13:50Z, four scopes same pass.</expect>
    <if_mismatch>Roll back in-window (same-window cron revert); surface to COO.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

## TONIGHT-REFRESH STEP (ADDED per PRD v1.1 §8.1 @f50ee7223b — after this TO's proof delivers)

One ad-hoc FULL-CHAIN exercise run tonight (vendor pulls → mirrors → floor → accrual → publisher)
so the SERVED data reads **as-of 2026-08-13** before session end. Run-and-read QA exercising the
retimed path — NOTHING STANDING, and it is never production evidence: the scheduled morning cycle
remains the unattended TO-4 acceptance. Read the served platinum series for all three firms after
the run and report the as-of values to COO with the proof_TO-3 close.

<proof_of_spec>
Path: org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_TRGALN/proof_TO-3.json per PRD §7.
Two claims (rows 2/3), field ScheduleExpression, `expected` VERBATIM from §3, each
desired/applied/exercised; plan_zero_diff; tag. Tonight-refresh read reported alongside (QA-labeled,
not a §7 claim).
</proof_of_spec>

<acceptance_criteria>
1. Both applied strings == §3 targets VERBATIM; floor untouched (plan proves it).
2. plan_zero_diff true; tag pushed; deploy ledger closed.
3. Exercised: platinum publish stamp ≈ 13:50Z, all four scopes written in the same pass.
4. No alarms/monitors/SNS/SES; no shadow paths.
</acceptance_criteria>
</task_order>
