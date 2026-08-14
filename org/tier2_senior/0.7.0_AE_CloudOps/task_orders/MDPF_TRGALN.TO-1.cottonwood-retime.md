# TO MDPF_TRGALN.TO-1 — Cottonwood retiming (§3 rows 4, 5, 7)

<task_order id="MDPF_TRGALN.TO-1" project="MDPF_TRGALN">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T05:0xZ</issued>
<status>pending</status>
<priority>P0 — STAGED. GO comes ONLY from COO, citing proof_TO-0.json rev 1 (Part A: census +
import-fidelity + writer-pin) VALIDATED. A GO citing anything else is mis-sent — query COO.
TIME-CRITICAL once GO'd: apply must land before 09:45Z (05:45 ET) for today's cycle to be the
acceptance cycle.</priority>

<dependencies>
  <dependency agent="0.7.0_AE_CloudOps" task="MDPF_TRGALN.TO-0 Part A (census + imports + writer pin) — proof_TO-0.json rev 1 validated by COO" status="pending"/>
</dependencies>

<references>
  <ref type="prd">docs/architecture/MDPF_TRGALN_PRD.md @2886349fcd — §3 rows 4/5/7 (THE SPEC), §4 TO-1, §6 bounds, §7 proof schema</ref>
</references>

## THE SPEC (PRD §3, VERBATIM — proof `expected` strings copy these exactly)

| # | Resource | Current | **TARGET** | Why |
|---|---|---|---|---|
| 4 | `cot-bd-session-daily-et` | cron(30 16) ET | **cron(30 7) ET** | session + full cot chain done ~07:36 ET; EST-worst-case 12:36Z, still 54m before floor |
| 5 | `opal-assets-ingest-mirror-cot-daily-et` | cron(30 18) ET | **cron(45 7) ET** | monolith fact_holdings lands ~07:46 ET; EST-worst-case 12:46Z < 13:30Z ✓ |
| 7 | `opal-assets-silver-blackdiamond-sweep-daily` | cron(0 5Z) | **cron(0 13Z)** | backstop repositioned AFTER the mirror, before the floor, year-round |

Floor (`mdpf-scheduled-floor`) UNCHANGED at cron(30 13Z). Rows 4/5 are ET-timezone schedulers and
STAY ET (DST-stable); row 7 stays UTC.

## MECHANICS

Edit the three crons in TF to the §3 targets → `safe-commit` → `.tools/safe-apply.sh` → 0-diff →
tag → push `--follow-tags` (Deployment Rules 1–6). Deploy-completion ledger entry opened at
deploy-start, closed at completion (NEVER#6 — a begun deploy finishes in-session or rolls back).
⛔ opal-assets root applies: `-target`ed + plan READ (opal-assets-daily-aua resurrect hazard,
CTO-BINDING carried from MDPF_REMED).

⚠ CARRIED CAVEATS (MDPF_REMED, same TF estate):
- Both mirror schedules have historically invoked ONE all-rows function (`event` never read) — if
  TO-0's census confirms this is still true, a "cot" mirror retime is simultaneously an inflection
  change: STATE the all-rows consequence in the apply plan before applying.
- `cot-bd-session-trigger` is a FOUR-entry function — a retime moves ONE entry point; name which.
- Cutover-gap statement per resource BEFORE apply (double-run vs skipped-day). Expected shape today:
  rows 4/5 old fire-times (16:30/18:30 ET) are LATER than the new — one fire today at the new time,
  no skip; row 7's old 05:00Z fire may already have run today → the new 13:00Z fire is an acceptable
  idempotent double-run of a backstop sweep. State what you expect, then show it held.

## EXERCISED EVIDENCE (PRD §4, verbatim)

Next cycle's monolith `blackdiamond/cottonwood/silver/fact_holdings` LastModified ≤ 12:50Z AND
`platinum/mdpf/cottonwood/aggregate-aua-timeseries.json` `as_of_last` == T-1 (computed via
`lib/trading_calendar.py`, never wall-clock). If the apply lands before 09:45Z, TODAY's first
new-time fires ARE the exercised evidence — read them after today's ~13:50Z publish; the proof's
final rev may post-date the apply commit (deliver desired+applied at apply time, append exercised
after the cycle; verdict flips PASS only with all three layers).

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-trigger for rows 4/5/7 (pre-state) + comp-blast on cot-bd-session-trigger and opal-assets-ingest-mirror</run>
    <expect>Pre-state strings match §2 verbatim; no NEW consumer in the radius vs PRD issue-date.</expect>
    <if_mismatch>STOP; surface to COO.</if_mismatch></step>
  </phase>
  <phase id="2" when="before apply">
    <step><run>commit-before-apply; .tools/safe-apply.sh -target scoped; plan READ</run>
    <expect>Plan = the three schedule rows ONLY; NO opal-assets-daily-aua row; 0-diff after apply; tag + push --follow-tags.</expect>
    <if_mismatch>STOP on a dirty plan; do not proceed.</if_mismatch></step>
  </phase>
  <phase id="3" when="after apply">
    <step><run>comp-trigger re-run + live `aws scheduler get-schedule` / `aws events describe-rule` (APPLIED) + the exercised artifact reads above</run>
    <expect>Applied strings == §3 targets verbatim; exercised evidence per above.</expect>
    <if_mismatch>Roll back in-window (same-window cron revert); surface to COO. A half-landed retime does not sit overnight.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<proof_of_spec>
Path: org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_TRGALN/proof_TO-1.json per PRD §7.
Three claims (one per row), field ScheduleExpression, `expected` VERBATIM from §3, each with
desired (tf_path+commit+line) / applied (exact aws read + observed verbatim) / exercised (artifact
key + LastModified | as_of_last). terraform.plan_zero_diff true; tag recorded.
</proof_of_spec>

<acceptance_criteria>
1. All three applied schedule strings == §3 targets VERBATIM (a paraphrase is a spec violation).
2. plan_zero_diff true; tag pushed --follow-tags; deploy ledger entry closed.
3. Cutover-gap statement written BEFORE apply; post-cycle, shown held (no skipped business day).
4. Exercised: fact_holdings ≤ 12:50Z + cottonwood as_of_last == T-1 per lib/trading_calendar.py.
5. No alarms/monitors/SNS/SES; no shadow paths; rollback path stated (same-window cron revert).
</acceptance_criteria>
</task_order>
