<task_order>
<to_id>ADHOC.inf-etf-halflanded-deploy-regularization</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<date>2026-08-03</date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "ADHOC" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged</status>
<priority>ELEVATED (CTO adjudication request 212224Z; NEVER-rule remediation -- a stranded deploy leg is RED-ALERT material, not a follow-up. Slots ALONGSIDE T2.C: do the T2.C clock DECLARATION first (doc-only), then this BEFORE any T2.C apply -- it is the posture guard for your own applies.)</priority>

<title>Regularize the half-landed inf-etf-ownership deploy: live schedule + uncommitted TF -- verify 0-diff against the EDITED tree, commit, tag, ledger</title>

<context>
YOUR OWN T1.A FINDING F2, CTO-adjudicated to this seat (COO adjudication 2026-08-03 ~21:25Z on
CTO rec 212224Z): inf-etf-ownership-daily-schedule is LIVE (born since 07-29; its event rule
deleted) while the matching edits sit UNCOMMITTED in the shared tree:
  M  infra/aws/terraform/inf-pipeline/inf-etf-ownership-daily.tf
  M  infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/lambda_function.py
  ?? (vendored copies) dedup_core.py + trading_calendar.py under the lambda source dir
Authorship context: ~E built the inflection scheduled floor during the ETFS weekend (seat now
stood down) -- the deploy's COMMIT LEG is stranded, violating the half-landed NEVER (a begun
deploy FINISHES every leg or rolls back + escalates).

LIVE RISK (why elevated): an untargeted inf-pipeline apply from committed HEAD would DELETE the
live schedule and silently revert the zero-gaps fix. STANDING POSTURE UNTIL THIS CLOSES:
inf-pipeline is TARGETED-APPLIES-ONLY (broadcast to MSTR; your own T2.C applies honor it too).

RULE-3 NOTE (Lambda Layers): the two vendored .py copies are inline vendoring, which needs
explicit approval. The regularization commits the APPLIED reality under CTO's adjudication (that
message is the approval context for the commit) -- but annotate the commit that layer-migration
is the standing debt, and surface it in your report so CTO can queue or waive it explicitly.

CTO DISPOSITION (212643Z, recorded here so it cannot silently become a ratified pattern):
LAYER-DEBT QUEUED, NOT WAIVED -- migrate both vendored copies to a Lambda Layer at the NEXT code
touch of inf-etf-ownership-daily; no standalone TO now. INTERIM OBLIGATION FOLDED INTO THIS TO
(completion of the F2 leg, not new scope): trading_calendar.py is already under the ETFS-weekend
vendored-copy parity CI; VERIFY dedup_core.py is ALSO parity-covered and state it in the report
-- if NOT covered, ADD it to that CI in the same regularization commit.
</context>

<scope>
1. VERIFY APPLIED == EDITED TREE: terraform plan for the inf-pipeline root against the CURRENT
   working tree (the edited files in place), expecting 0-diff on the inf-etf resources. A
   non-zero diff = the working tree does NOT match applied state -- STOP, capture the diff,
   escalate to CTO+COO before committing anything (committing a tree that diverges from applied
   would manufacture a THIRD state).
2. COMMIT all four files (safe-commit, your author line) with the annotation: the ETFS-weekend
   deploy citation (~E's inflection scheduled floor), CTO adjudication 212224Z + COO dispatch,
   and the Rule-3 vendoring debt note.
3. TAG per Deployment Rule 6 (re-derive the inf-pipeline tag series first: git tag -l
   "inf-pipeline-v*" | sort -V | tail); push --follow-tags via integrator discipline (MSTR).
4. LEDGER: open + close a deploy-completion ledger entry in
   org/critical_paths/change_management/ covering the now-completed commit leg (the NEVER rule's
   required artifact; cite the original apply window as best known + this regularization).
5. REPORT to CTO + COO: 0-diff evidence, commit hash, tag, ledger path, and the Rule-3 debt
   surfaced. Then the targeted-applies-only posture LIFTS (say so explicitly in the report).
   <!-- SUPERSEDED 2026-08-03 by CTO ruling 215051Z (COMMIT ALL / APPLY NOTHING): the posture
        does NOT lift at this TO's close -- the committed-declared-unapplied increment ARMS on
        any code deploy, so TARGETED-APPLIES-ONLY on inf-pipeline CONTINUES until CTO
        deliberately lands or retires the parked increment. AE correctly reported the
        continuation explicitly (221020Z). Closed @001a73530a + v1.7.95 + ledger
        20260803T2200Z (opened+closed same session); L4 green-run observation rides MSTR's
        push per the observed-green-run law. -->

</scope>

<compiler_tools_mandate>
  <phase id="1" when="before commit">
    <step>
      <run>terraform plan (inf-pipeline root, edited tree in place) via the safe-apply flow's plan leg # rail-checked: verifying applied-vs-tree parity IS the task</run>
      <expect>0-diff on the inf-etf resources (schedule present, event rule absent, lambda source hash matching).</expect>
      <if_mismatch>STOP. Capture the full diff; escalate CTO+COO; commit NOTHING.</if_mismatch>
    </step>
    <step>
      <run>comp-blast inf_etf_ownership (or the census-named fn) + .tools/commit-gate.sh on the .py files</run>
      <expect>Consumers known; commit-gate passes (py_compile + ruff) incl. the vendored copies.</expect>
      <if_mismatch>STOP on gate failure -- a regularization commit must not land broken code even if applied works (fix-forward with CTO word only).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="commit + tag">
    <step>
      <run>safe-commit the four files; tag inf-pipeline-v{next} -a; coordinate push --follow-tags with MSTR</run>
      <expect>Commit annotation carries all three citations; tag lands on the regularization commit.</expect>
      <if_mismatch>REWORK -- an unannotated regularization is indistinguishable from ordinary drift.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after">
    <step>
      <run>ledger entry open+close; report to CTO+COO with 0-diff evidence + posture-lift statement</run>
      <expect>Ledger closed same-session (an unclosed entry at session end = COO alarm per the NEVER rule).</expect>
      <if_mismatch>Do not end the session with the ledger open -- escalate loud instead.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
The four files are RESERVED for this TO's commit -- MSTR notified (cotenant-sweep hazard: nobody
else's commit may sweep them). Your own T2.C shares the tree: declaration first, this second, any
T2.C apply third. The inf-pipeline targeted-applies-only posture binds fabric-wide until your
Phase-3 report lifts it.
</cross_domain_coordination>

<acceptance_criteria>
1. Plan-vs-edited-tree 0-diff evidence captured verbatim (or the STOP path taken with the diff).
2. Commit with the three-citation annotation; tag on the correct series; push coordinated.
3. Deploy-completion ledger entry opened AND closed, path cited.
4. Rule-3 vendoring debt explicitly surfaced in the report.
Plus: session log includes a Compiler Tools section reproducing every <run> with observed output
and explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="finding">Your T1.A F2 @389c528ddb</ref>
  <ref type="adjudication">CTO 20260803T212224Z (rec) + this COO dispatch</ref>
  <ref type="never">CLAUDE.md half-landed-deploy NEVER (deploy-completion ledger) + Deployment Rules 3/6</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
