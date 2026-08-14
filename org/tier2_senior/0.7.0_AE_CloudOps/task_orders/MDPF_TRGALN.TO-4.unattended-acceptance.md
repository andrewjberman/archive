# TO MDPF_TRGALN.TO-4 — Unattended acceptance cycle + close: all three firm scopes T-1 at publish

<task_order id="MDPF_TRGALN.TO-4" project="MDPF_TRGALN">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T05:0xZ</issued>
<status>pending</status>
<priority>P0 — STAGED. GO comes ONLY from COO, citing proof_TO-1 + proof_TO-2 + proof_TO-3
(desired+applied layers) validated AND all applies landed before 09:45Z. The acceptance cycle is
TODAY'S OWN SCHEDULED FIRES if that clock held; otherwise tomorrow's (acceptance slips a day —
COO states which at GO time).</priority>

<dependencies>
  <dependency agent="0.7.0_AE_CloudOps" task="MDPF_TRGALN.TO-1 + TO-2 + TO-3 applied (0-diff, tagged); proof_TO-0.json FINAL rev (Part B vendor-window claims) due with this TO's close" status="pending"/>
</dependencies>

<references>
  <ref type="prd">docs/architecture/MDPF_TRGALN_PRD.md @2886349fcd — §3 expected end-state timeline, §4 TO-4, §7 proof schema</ref>
</references>

## THE ACCEPTANCE (PRD §4, verbatim discipline)

One full UNTOUCHED scheduled cycle — no manual assists, no ad-hoc runs credited as evidence (an
ad-hoc run is never production evidence). Then a single proof artifact asserting, for EACH of
`49financial` / `inflection` / `cottonwood`:

1. platinum `as_of_last` == expected T-1 per `lib/trading_calendar.py` (trading-day frontier,
   NEVER wall-clock — NEVER#1). **Stated concretely per PRD v1.1 §8.1 @f50ee7223b: today's cycle
   serves as-of 2026-08-13, all three firm scopes**;
2. gold `portal/gold/mdpf/{scope}/aggregate-aua-timeseries/{T-1}.json` exists;
3. publish stamp ≈ 13:50Z.

Expected end-state timeline (EDT, §3): schwab 06:16 → COT chain 07:30–07:46 → INF family
07:02–08:44 → INF mirror 09:05 → smartx 09:14 → **floor 09:30 → accrual 09:40 → publish 09:50, all
three scopes T-1.**

⛔ **NOBODY arms any watcher/alarm/monitor/SNS against the cycle (standing moratorium, Andrew-direct
2026-07-28).** The acceptance read is an artifact read AFTER the publish stamp — read, don't watch.

## FORK HANDLING

A firm still T-2 on the acceptance cycle with retimes correctly applied = the VENDOR-WINDOW FORK —
report the measured availability to COO for Andrew escalation per TO-0's adjudication table. That is
a FINDING, not a TO-4 failure of mechanics; the proof records it in `forks_hit` with verdict per the
failing claim. 49financial regressing would be a STOP-CLASS surprise (nothing in scope touches 49F)
— report immediately.

<compiler_tools_mandate>
  <phase id="3" when="after the cycle">
    <step><run>live head-object / s3 reads on the three platinum keys + three gold keys + publish stamp; lib/trading_calendar.py for the expected frontier; comp-freshness only as corroboration (freshness_basis must be trading-day-frontier)</run>
    <expect>All nine claim rows PASS against the §4 spec above.</expect>
    <if_mismatch>Fork per the table; no unilateral remediation; COO routes.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<proof_of_spec>
Path: org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_TRGALN/proof_TO-4.json per PRD §7.
Nine claims (3 firms × 3 assertions), `expected` values derived ONLY from lib/trading_calendar.py +
§4; each claim desired/applied/exercised (desired = the §3 schedule set already proven in TO-1/2/3 —
cite those proofs by path+commit; applied = the live reads; exercised = the artifact values).
</proof_of_spec>

<acceptance_criteria>
1. The cycle ran UNTOUCHED (no manual invokes between the first family fire and the publish read —
   attest, and note any QA run that occurred with its QA labeling).
2. All nine claims PASS, or forks are recorded per the table with measured availability.
3. proof_TO-0.json FINAL rev (Part B) delivered alongside.
4. COO validates all proofs mechanically against §3/§4 and issues the RAVC4 close to CTO.
5. **PROJECT CLOSE BAR (PRD v1.1 §8.3 @f50ee7223b — supersedes TO-4-alone):** project closes when
   (1) TO-0..TO-4 validated; (2) served Inflection series has no unadjudicated empty dates (TO-5/
   TO-6); (3) all three firm scopes serve as-of 2026-08-13 at tonight's/this-morning's publish;
   (4) fabric holds for the night. This TO's PASS is necessary, not sufficient.
</acceptance_criteria>
</task_order>
