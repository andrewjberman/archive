<task_order>
  <metadata>
    <id>TRSB_LEDGER.017</id>
    <slug>ae-section11b-executed-email-recipient</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.5.0_AE_OpalETL~B</issued_to>
    <date>2026-05-20</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>HARD GATE: TRSB_LEDGER.015 (§11 probe) must report first -- §11-B's SES step (§11.2-C) depends on the probe's P2 SES-verification-state finding (whether a menachem@ verification step is needed before the email change is deliverable). COO~B flips to pending + GO once .015's findings land. Can run in parallel with .016 (independent change surface -- DDB seed vs Lambda email path).</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P2 -- TRSB §11-B (+ §11-C SES). Routes every executed-trade email to menachem@. Together with §11-A (.016) discharges §11.</priority>
    <sla>~1-2h AE wall -- a trade-workflow-handler email-path edit + terraform deploy, plus a possible one-click SES verification.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md §11.2-B (executed-trade email recipient) + §11.2-C (SES deliverability) + §11.4 (independent of the TradeSubmission portal PROD promotion).</prd>
    <gate_input>TRSB_LEDGER.015 probe P2 output -- the SES verification state for opalinvest.com domain / menachem@ identity.</gate_input>
    <pipeline_rule>Rule 1 -- the trade-workflow-handler Lambda code change deploys via terraform apply ONLY. Pipeline tag after 0-diff. SES production access stays OUT of scope (§4) -- this TO works within the sandbox + verified-identity model.</pipeline_rule>
  </references>

  <context>
    The trade-workflow-handler execution path emails on EXECUTED -- currently to andrew@opalinvest.com, hardcoded (SES sandbox). §11-B adds menachem@opalinvest.com as a recipient of every email the execution path emits (the executed / trade-complete notification and any brokerage-handoff email), so Menachem receives the final executed email + its data artifact (the Vident-template Excel). §11-C: SES is in sandbox -- a recipient must be verified (or the domain verified); the .015 probe establishes the current state.
  </context>

  <scope>
    <step>P1 -- enumerate the emails. Read email_utils.py (and the trade-workflow-handler execution path) to enumerate EVERY email the EXECUTED / execution path emits -- the executed/trade-complete notification and any brokerage-handoff email + its attached/linked data artifact. List them explicitly before editing.</step>
    <step>P2 -- add menachem@opalinvest.com as a recipient of every enumerated execution-path email. Mirror exactly how andrew@ is currently wired -- if andrew@ is hardcoded, add menachem@ alongside (a 2-element recipient list); preserve the existing andrew@ delivery. Do NOT change submission/approval-path emails -- execution path only, per §11.2-B.</step>
    <step>P3 -- SES (§11.2-C). Per the .015 probe's P2 finding: if the opalinvest.com domain OR menachem@ is already verified, no SES action -- record that. If neither holds, verify menachem@opalinvest.com (a one-click identity verification). Do NOT request SES production access (§4 -- out of scope).</step>
    <step>P4 -- deploy via terraform apply (Rule 1): commit -> terraform plan -> apply -> 0-diff verify -> pipeline tag (trade-pipeline-v*). No console-side Lambda update.</step>
    <step>P5 -- verify + RAVC2 to 2.0.0_SA_COO~B (CC 1.0.0_SA_CTO~B): the enumerated email list, the recipient-addition diff, the SES disposition, the deploy transcript + tag. Session log with Compiler Tools section.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Every email the trade-workflow-handler EXECUTED / execution path emits has menachem@opalinvest.com as a recipient; the existing andrew@ delivery is preserved; submission/approval-path emails unchanged.</ac>
    <ac id="AC2">SES disposition recorded -- either already-covered (domain/identity verified per the .015 probe) or menachem@ verified by a one-click identity verification. No SES production-access request.</ac>
    <ac id="AC3">Deployed via terraform apply, 0-diff plan verified, pipeline tag applied. No console-side deploy.</ac>
    <ac id="AC4">No emoji. Session log with Compiler Tools section. RAVC2 to COO~B CC CTO~B.</ac>
  </acceptance_criteria>

  <out_of_scope>
    trade-users seed (§11-A / .016). Portal-auth account (§11-D). SES production-access migration (§4). Submission / approval path emails -- execution path only. The TradeSubmission portal PROD promotion (§11.4 -- independent, must not gate or be gated by §11-B).
  </out_of_scope>

  <deliverables>
    - trade-workflow-handler execution-path emails route to menachem@ + andrew@; SES disposition; terraform deploy + tag; RAVC2 to COO~B CC CTO~B; session log.
  </deliverables>
</task_order>
