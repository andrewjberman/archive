<task_order>
<to_id>ADHOC.cot-snapshot-lag1-parity-and-shell-trace</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-03</date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "ADHOC" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged</status>
<priority>P1 (CTO DISPATCH-NOW ruling 225311Z item 2: measured defect, proven fix exists, every scheduled day can mint another shell. Sequencing WITHIN your seat is yours -- before or after the T4.A Schwab tranche; same-session target. The C1 derivation at 0.2.0_DS is NOT to be interrupted -- which is why this is at YOUR seat.)</priority>

<title>cot snapshot LAG=1 parity + THE MANDATORY SHELL-PROPAGATION TRACE: has a shell day ever reached a served cottonwood number?</title>

<context>
Your own T4.A tranche-3 measurement @bd9a298559 realized the WS-1 named risk: cot fact_allocations
partitions alternate full/near-empty (07-27: 3 / 07-28: 1,525 / 07-29: 1 / 07-30: 1,525 / 07-31:
1,534) -- ~99.9% content collapse on alternating days behind a GREEN landing-conservation check.
Mechanism (your WS-1 row): BD snapshot-as-of-not-yet-completed returns a 0-row shell; the 49f
runners configure LAG=1 around it (the PROVEN correct configuration); the cot snapshot tables run
LAG=0.

CTO RULING (225311Z item 2, verbatim spine): dispatch now; DS lane; config fix = LAG=1 parity with
the 49f runners. AND THE HALF THAT MATTERS MORE (mandatory, the TO must not close on the config
fix alone): "HAS A SHELL DAY EVER PROPAGATED INTO A SERVED COTTONWOOD NUMBER? Nobody has traced
that... I am NOT ruling that served values are wrong, because the gold layer may consume only the
latest non-empty partition or dedup across days, and that is unmeasured. The answer decides scope:
gold ignores shells -> fix-forward only; gold ever consumed one -> historical impact assessment,
and it reaches a partner-facing surface."

RELATED-CHECK (bounded, diagnose-only -- CTO item 4 connection note): the cottonwood monolith
silver plane frontier-stops at 07-31 while the firm bucket carries labels through 08-03. This is a
SILVER-mirror lag and NOT the 6c family (6c was GOLD-stage starvation, repaired 21:24Z) -- do not
assume the 6c repair covers it. Check the mirror leg (opal-assets-ingest-mirror) on its own
evidence: lagging or by-design? Diagnose + report; no fix without a further word.
</context>

<scope>
1. CONFIG FIX: bring the cot snapshot tables to LAG=1 parity with the 49f runners (the proven
   configuration). Cite the 49f config file:line as the pattern source; deploy per Rule 13.
2. THE MANDATORY TRACE (scope-deciding, close-blocking): trace whether any shell-day partition has
   EVER been consumed into a served cottonwood number. Read the gold-layer consumption at source
   (latest-non-empty selection? cross-day dedup? per-date read?) and check the served artifacts'
   values against the shell-day dates. Two outcomes, pre-registered: (a) gold provably ignores
   shells -> fix-forward only, close with the mechanism cite; (b) any shell ever consumed ->
   STOP at that finding, report to CTO+COO for the historical-impact scope call (partner-facing
   surface) -- do NOT begin an impact assessment without the word.
3. RELATED-CHECK per context: mirror-leg lag diagnosis, report-only.
4. NO alarms/monitors (moratorium). The LAG fix + the trace are the deliverables.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read the cot snapshot puller config + the 49f LAG=1 pattern at source (file:line both); comp-pipescript io --pipeline mdpf / hand-derive on the gold consumers of fact_allocations (assets-tree blindness applies -- label hand-derivations)</run>
      <expect>Both configs cited; the gold consumption mechanism identified at source.</expect>
      <if_mismatch>STOP. A consumption mechanism you cannot find is outcome (b)-adjacent -- surface before fixing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="trace + fix, before deploy">
    <step>
      <run>shell-propagation trace: gold consumption mechanism vs the measured shell dates; served-value spot-check on the alternating-day window</run>
      <expect>Outcome (a) or (b) per the pre-registered pair, evidence verbatim.</expect>
      <if_mismatch>Outcome (b) = STOP + report; the config fix may still deploy (it is correct regardless) but the TO does not close.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>deployed MATCH verify + ledger + report to COO + CTO: config diff, trace outcome with mechanism cite, mirror-leg diagnosis</run>
      <expect>Report carries all three; the trace outcome is the headline, not the config fix.</expect>
      <if_mismatch>A close on the config fix alone is REWORK per the CTO ruling.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
cot firm-separation binds (NEVER#2): all work inside the cot tree + opal-data-assets boundary.
T1.C (0.2.0_DS) consumes cot outputs downstream -- if outcome (b) fires, their parity evidence
window may need the same historical lens; the STOP-and-report covers that routing. Your own T4.A
BD-family verdicts share the evidence base -- cross-cite, do not re-measure.
</cross_domain_coordination>

<acceptance_criteria>
1. LAG=1 parity deployed with the 49f pattern cited (file:line both sides); MATCH + ledger.
2. THE TRACE ANSWERED with mechanism cite + served-value evidence: (a) closes fix-forward;
   (b) STOPs at the finding for the CTO/COO scope call. A close without the trace = REWORK
   (CTO: "require the trace, do not let it close on the config fix alone").
3. Mirror-leg lag diagnosis reported (diagnose-only).
Plus: session log Compiler Tools section reproduces every <run> with observed output and explicit
pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="ruling">CTO 20260803T225311Z items 2 + 4 (dispatch-now + trace-mandatory + mirror connection)</ref>
  <ref type="measurement">Your T4.A tranche 3 @bd9a298559 (the alternating-partition evidence) + WS-1 @438a3c69b3 (the 0-row-shell mechanism + 49f LAG=1 row)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
