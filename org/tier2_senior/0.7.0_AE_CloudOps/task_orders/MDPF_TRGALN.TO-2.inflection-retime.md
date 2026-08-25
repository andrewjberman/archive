# TO MDPF_TRGALN.TO-2 — Inflection retiming (§3 rows 8–15, 6): uniform −2h15m family shift + mirror

<task_order id="MDPF_TRGALN.TO-2" project="MDPF_TRGALN">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T05:0xZ</issued>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project MDPF_TRGALN, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending</status>
<priority>P0 — STAGED. GO comes ONLY from COO, citing proof_TO-0.json rev 1 validated (TO-1 GO and
TO-2 GO may be issued together or in close sequence; row order within this TO is yours).
TIME-CRITICAL once GO'd: apply before 09:45Z (05:45 ET) — note row 8's NEW fire time is 09:50Z,
minutes after the deadline; land the family as one apply so today's chain runs whole.</priority>

<dependencies>
  <dependency agent="0.7.0_AE_CloudOps" task="MDPF_TRGALN.TO-0 Part A — proof_TO-0.json rev 1 validated by COO (esp. import of #6 opal-assets-ingest-mirror-inf-daily if unmanaged)" status="pending"/>
</dependencies>

<references>
  <ref type="prd">docs/architecture/MDPF_TRGALN_PRD.md @2886349fcd — §3 rows 8–15 + 6, §4 TO-2, §6 INF-variance tolerance, §7 proof schema</ref>
</references>

## THE SPEC (PRD §3, VERBATIM — proof `expected` strings copy these exactly)

| # | Resource | Current | **TARGET** | Why |
|---|---|---|---|---|
| 8 | `opal-inf-jwt-fetch` | cron(5 12Z) | **cron(50 9Z)** | whole INF family shifts a uniform **−2h15m**, preserving every internal offset |
| 9 | `inf-api-reps-daily` | cron(17 13Z) | **cron(2 11Z)** | " |
| 10 | `inf-accounts-v2-daily` | cron(22 13Z) | **cron(7 11Z)** | " |
| 11 | `opal-inf-bronze-runner-cron` | cron(30 13Z) | **cron(15 11Z)** | " |
| 12 | `inf-api-assets-v2-daily` | cron(32 13Z) | **cron(17 11Z)** | " |
| 13 | `inf-api-eclipse-daily` | cron(33 13Z) | **cron(18 11Z)** | " |
| 14 | `inf-api-positions-daily` | cron(37 13Z) | **cron(22 11Z)** | " |
| 15 | `inf-api-txn-daily` | cron(47 13Z) | **cron(32 11Z)** | " |
| 6 | `opal-assets-ingest-mirror-inf-daily` | cron(5 15Z) | **cron(5 13Z)** | expected sentinel ≈12:44Z → 21m slack to mirror, 25m mirror→floor margin |

All UTC crons (their ET wall-time shifts seasonally — pre-existing behavior, preserved; §6). The
shift is UNIFORM −2h15m for rows 8–15: verify each target preserves the family's internal offsets.

## MECHANICS

TF homes per PRD §2 (rows 8–15 all in `infra/aws/terraform/inf-pipeline/`; row 6 import lands in
TO-0 if unmanaged). Same mechanics as TO-1: edit crons to §3 targets → safe-commit → safe-apply →
0-diff → tag → push --follow-tags; deploy ledger opened/closed (NEVER#6); opal-assets-root portions
(row 6) `-target`ed + plan READ (daily-aua resurrect hazard).

⚠ Mirror caveat carried: if the mirror function is still all-rows (TO-0 census), the row-6 retime
moves ALL firms' mirror — state the consequence in the apply plan (COT's mirror is row 5 / TO-1;
sequence so neither apply silently re-times the other's leg — name the interaction in both plans).

Cutover-gap statement BEFORE apply. Expected shape today (apply ~09:0xZ): rows 9–15 old fire-times
(13:17–13:47Z) replaced by new (11:02–11:32Z) — one fire each today at the new time, no skip. Row 8
old 12:05Z → new 09:50Z: if the apply lands before 09:50Z, today fires at 09:50Z only; if it lands
09:50Z–12:05Z, TODAY'S JWT FIRE IS SKIPPED under the new string — state which case occurred and, in
the skip case, run one ad-hoc QA jwt-fetch invoke (QA-legal, run-and-read) so today's downstream
family has a fresh token; record it as QA, never as production evidence.

## EXERCISED EVIDENCE (PRD §4, verbatim)

Sentinel `gold/meta/pipeline-complete.json` (opal-data-inf) LastModified ≤ 13:00Z; monolith
orion/eclipse silver LastModified ≤ 13:10Z; `platinum/mdpf/inflection/...` `as_of_last` == T-1.
Today's first new-time chain IS the exercised evidence if applies land pre-09:45Z; read after the
~13:50Z publish; proof final rev may post-date the apply commit.

## DECLARED TOLERANCE (PRD §6 — surface, do not self-amend)

If the first cycles show sentinel variance > the 21m slack, the AMENDMENT (mirror +10m → 13:15Z,
still 15m floor margin) is COO's to issue — report the measured variance and await the amended GO;
do not redesign.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-trigger for rows 8–15+6 (pre-state) + comp-blast on inf-* target Lambdas and opal-assets-ingest-mirror</run>
    <expect>Pre-state strings match §2 verbatim; no NEW consumer vs PRD issue-date. ⚠ The legacy convergence path (mdpf-daily-refresh-trigger on the INF sentinel) WILL appear in the radius — it is OUT OF SCOPE (PRD §6, surfaced debt): after this TO it fires ~12:44Z, harmless to serving; do NOT touch it, do NOT report it fixed.</expect>
    <if_mismatch>STOP; surface to COO.</if_mismatch></step>
  </phase>
  <phase id="2" when="before apply">
    <step><run>commit-before-apply; .tools/safe-apply.sh; -target where opal-assets root is touched; plan READ</run>
    <expect>Plan = the nine schedule rows ONLY; NO opal-assets-daily-aua row; 0-diff after apply; tag + push --follow-tags.</expect>
    <if_mismatch>STOP on a dirty plan.</if_mismatch></step>
  </phase>
  <phase id="3" when="after apply">
    <step><run>comp-trigger re-run + live `aws events describe-rule` / `aws scheduler get-schedule` (APPLIED) + exercised reads above</run>
    <expect>All nine applied strings == §3 targets verbatim; exercised evidence lands per above.</expect>
    <if_mismatch>Roll back in-window; surface to COO. If the cycle shows INF still T-2 with the retimes correctly applied, that is the VENDOR-WINDOW FORK — route per TO-0's table (escalate to Andrew, option: ET-scheduler migration), never a unilateral fallback.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<proof_of_spec>
Path: org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_TRGALN/proof_TO-2.json per PRD §7.
Nine claims (rows 8–15 + 6), field ScheduleExpression, `expected` VERBATIM from §3, each
desired/applied/exercised; plan_zero_diff; tag.
</proof_of_spec>

<acceptance_criteria>
1. All nine applied strings == §3 targets VERBATIM; internal family offsets preserved (−2h15m uniform).
2. plan_zero_diff true; tag pushed; deploy ledger closed.
3. Cutover-gap statement pre-apply incl. the row-8 skip case; post-cycle shown held or handled per plan.
4. Exercised: sentinel ≤ 13:00Z, monolith orion/eclipse ≤ 13:10Z, inflection as_of_last == T-1.
5. Variance > slack reported to COO for the declared +10m amendment — never self-applied.
6. No alarms/monitors/SNS/SES; no shadow paths; legacy convergence path untouched.
</acceptance_criteria>
</task_order>
