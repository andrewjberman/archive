# pipeline-override: one-off test fix outside any project, assigned by 1.0.0_SA_CTO msg 107878 to the laptop COO lane as issuer; no project row exists to cut against
<task_order id="ADHOC.safe-deploy-bd-gold-test-retired-rule">
<to_id>ADHOC.safe-deploy-bd-gold-test-retired-rule</to_id>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.8.0_AE_CloudComp</issued_to>
<date>2026-10-09</date>
<status>pending</status>
<risk>LOCAL</risk>

<title>BD gold tests: the deploy-tool test asserts the current named-file rule, not the retired ship-everything rule (dell1 row MDPF_SECCLASS-D1-S19)</title>

<context>
dell1 row `MDPF_SECCLASS-D1-S19`:
`data/black_diamond/scripts/gold/tests/test_etf_classifier_deployed_resolution.py::test_deploy_tool_ships_the_shared_modules_beside_the_gold_files`
fails at HEAD. It pins the old rule that any BD gold deploy carries the `_shared` modules. That rule was retired on 2026-10-08 by the
named-file rule (1.0.0_SA_CTO msg 107147; `.tools/safe_deploy_core.py` `shipped_artifacts_for`: "a deploy ships only the files its own
ledger names"). As a result, every BD gold candidate's suite reads 1 failed, 96 passed. The CTO ruled the issue in msg 107878: issued by
the laptop's COO lane, and not a NFRA_CTLPLN order.
</context>

<scope>
1. Read `shipped_artifacts_for` and its docstring, then rewrite that one test so it asserts the current rule:
   - a `_shared` module ships only when its own repo path is named;
   - a deploy that names only the gold files does not carry `_shared`.
   Keep the test's name, or rename it to say the new rule, and say which.
2. Change no tool code and no other test.
3. Run the whole BD gold suite from `data/black_diamond/scripts/gold` (`python -m pytest -q tests`) and confirm 0 failed.
4. Commit through `.tools/safe-commit.sh`. Report the commit hash and the suite line to 2.0.0_SA_COO~C. The CTO's relay carries the
   result to dell1.
</scope>

<proof_of_spec>
<criterion id="AC1" cell_refs="ADHOC"><invocation>python -m pytest -q data/black_diamond/scripts/gold/tests/test_etf_classifier_deployed_resolution.py</invocation><expect> passed</expect></criterion>
</proof_of_spec>
<expected_criteria>AC1</expected_criteria>
AC1's line must read 0 failed. The scope's whole-suite run is reported beside it.

<paths>
data/black_diamond/scripts/gold/tests/test_etf_classifier_deployed_resolution.py
org/tier2_senior/0.8.0_AE_CloudComp/deliverables/
org/tier2_senior/0.8.0_AE_CloudComp/logs/
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE a test edit.
comp-iam: DECLARED-NOT-APPLICABLE no AWS call.
comp-adversary: RUN -- a test deleted or skipped to go green (it is rewritten to assert the current rule, both arms); tool code changed to fit the test (forbidden; the rule is the CTO's); BLIND: deploys whose ledgers name _shared modules (they still ship them, by the rule).
lane: the <paths> block names the one test file and the seat's own deliverables and logs.
</preflight>
</task_order>
