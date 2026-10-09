# pipeline-override: one-off test fix outside any project, assigned by 1.0.0_SA_CTO msg 107878 to the laptop COO lane as issuer; no project row exists to cut against
<task_order id="ADHOC.comp-secrets-test-json-reveal-refused">
<to_id>ADHOC.comp-secrets-test-json-reveal-refused</to_id>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.8.0_AE_CloudComp</issued_to>
<date>2026-10-09</date>
<status>pending</status>
<risk>LOCAL</risk>

<title>comp-secrets: land the CTO's test patch so the tests assert that '--json --reveal' is refused (fix @9e4730450c)</title>

<context>
1.0.0_SA_CTO fixed `comp-secrets` @9e4730450c so that `--json --reveal` is refused. Three tests in `.tools/tests/test_comp_secrets.py`
fail until the test follows the fix. The CTO wrote the patch for this lane:
`org/tier1_exec/1.0.0_SA_CTO/deliverables/TEST_COMP_SECRETS_JSON_REVEAL_REFUSED_20261009.patch`. The CTO ruled the issue in msg 107878:
issued by the laptop's COO lane, and not a NFRA_CTLPLN order.
</context>

<scope>
1. Read the patch and apply it to `.tools/tests/test_comp_secrets.py` only (`git apply --check` first, then `git apply`). If it does not
   apply cleanly at HEAD, make the same change by hand and say so.
2. Run `python -m pytest -q .tools/tests/test_comp_secrets.py` and confirm `8 passed`.
3. Read no secret value. Edit no tool code: the fix itself is the CTO's commit.
4. Commit through `.tools/safe-commit.sh`. Report the commit hash and the pytest line to 2.0.0_SA_COO~C.
</scope>

<proof_of_spec>
<criterion id="AC1" cell_refs="ADHOC"><invocation>python -m pytest -q .tools/tests/test_comp_secrets.py</invocation><expect>8 passed</expect></criterion>
</proof_of_spec>
<expected_criteria>AC1</expected_criteria>

<paths>
.tools/tests/test_comp_secrets.py
org/tier2_senior/0.8.0_AE_CloudComp/deliverables/
org/tier2_senior/0.8.0_AE_CloudComp/logs/
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE a test edit.
comp-iam: DECLARED-NOT-APPLICABLE no AWS call.
comp-adversary: RUN -- a test changed to pass by weakening it (the patch asserts the refusal; 8 passed with the refusal live); a secret printed by a test run (the refusal is the point; no value is read); BLIND: other callers of --reveal.
lane: the <paths> block names the one test file and the seat's own deliverables and logs.
</preflight>
</task_order>
