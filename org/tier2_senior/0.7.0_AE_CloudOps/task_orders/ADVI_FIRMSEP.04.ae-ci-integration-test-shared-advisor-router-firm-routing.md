<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_FIRMSEP.04</id>
    <project>ADVI_FIRMSEP</project>
    <title>CI integration test for shared-advisor-router firm-routing — block deploy on routing regression</title>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <completed_date>2026-05-07</completed_date>
    <completed_by>0.7.0_AE_CloudOps~B</completed_by>
    <priority>high</priority>
    <estimated_effort>~0.5d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FIRMSEP.md §4.4 + §6 Phase 1</ref>
    <ref type="oq7">PRD §7 OQ7 — runner: Mocha + Sinon (matches existing Lambda@Edge stack; minimal new toolchain). Default approved.</ref>
    <ref type="risk_addressed">PRD §2 G3 — shared-advisor-router is the SOLE structural barrier between Inflection requests and 49F's bucket. No CI test today.</ref>
    <ref type="sentinel_for_onboarding">cottonwood test case is EXPECTED to fail until Phase 3 ships — failure is a sentinel for missed onboarding step (intentional design).</ref>
  </references>

  <context>
    A regression in shared-advisor-router's request.origin.s3.domainName swap would silently
    serve cross-tenant data. Manual smoke covers it today; that becomes 3-firm manual smoke
    when Cottonwood lands. Mocha integration test makes the routing logic structurally
    asserted at every Lambda@Edge build.

    Per OQ7: Mocha + Sinon (matches existing patterns). CI gate via build-nodejs-lambda.sh
    pre-deploy hook — test failure exits non-zero, blocks Lambda@Edge zip upload.

    cottonwood test case design: included from day 1, EXPECTED to fail until Phase 3 adds
    cottonwood to FIRM_BUCKET_MAP. The expected-fail flips green at Phase 3 ship. If the test
    passes prematurely → someone added cottonwood without going through the playbook
    (caught early). If the test stays red after Phase 3 ship → onboarding missed a step
    (caught at deploy gate).
  </context>

  <scope>
    <step>
      Create test file infra/aws/lambda-edge/shared-advisor-router/test/firm-routing.spec.mjs.
      6 test cases (per PRD §4.4):
        1. X-Firm-Id "49financial" → request.origin.s3.domainName === "opal-data-bd.s3.us-east-1.amazonaws.com"
        2. X-Firm-Id "inflection" → "opal-data-inf.s3.us-east-1.amazonaws.com"
        3. X-Firm-Id "cottonwood" → "opal-data-cot.s3.us-east-1.amazonaws.com" (EXPECTED FAIL — sentinel until Phase 3)
        4. X-Firm-Id "opal-capital" + ?firm=inf → "opal-data-inf.s3.us-east-1.amazonaws.com"
        5. X-Firm-Id "opal-capital" (no ?firm=) → 400 status
        6. Missing X-Firm-Id → 403 status
      Use Sinon to mock the CloudFront event shape + assert the mutated request.origin.
    </step>
    <step>
      Mark test 3 (cottonwood) with mocha .skip or pending tag with comment:
        // SENTINEL: this test is intentionally pending until ADVI_FIRMSEP.10 ships cottonwood onboarding.
        //   Flips to active green when FIRM_BUCKET_MAP gains cottonwood entry.
        //   Premature green = onboarding bypass; flag to Andrew + COO.
    </step>
    <step>
      package.json adjustments (or create infra/aws/lambda-edge/shared-advisor-router/package.json
      if absent):
        - "scripts": { "test": "mocha test/**/*.spec.mjs" }
        - devDependencies: mocha + sinon (latest stable; no version creep beyond what existing
          Lambda@Edge stack uses).
        - npm install (will create node_modules; gitignore it).
    </step>
    <step>
      Update infra/aws/lambda/ci/build-nodejs-lambda.sh:
        - Detect test/ directory in function path.
        - Run npm install + npm test before zipping.
        - Exit non-zero on test failure → blocks zip upload + terraform plan.
    </step>
    <step>
      Local test pass:
        - Run npm test in shared-advisor-router/.
        - Tests 1, 2, 4, 5, 6 should pass; test 3 pending/skipped.
        - Zero failures.
    </step>
    <step>
      Empirical CI gate verification:
        - Temporarily break the FIRM_BUCKET_MAP in a test branch (sed bd → wrong-bucket).
        - Run build-nodejs-lambda.sh — confirm npm test fails + script exits non-zero.
        - Revert before commit.
    </step>
    <step>
      Commit + tag bump portal-auth-v1.X.Y. Push --follow-tags. record-terraform-deploy.sh.
    </step>
    <step>
      RAVC2 to COO: test file + npm test output (5 pass, 1 pending), build script update, gate
      empirical evidence (intentional break + caught), tag.
    </step>
  </scope>

  <compiler_mandate>
    <tool>npm test output attached to RAVC — 5 pass, 1 pending</tool>
    <tool>build-nodejs-lambda.sh empirical fail-fast verification (intentional break)</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">test/firm-routing.spec.mjs landed with 6 cases (5 active + 1 pending/sentinel).</criterion>
    <criterion id="AC2">npm test green for active 5 cases.</criterion>
    <criterion id="AC3">cottonwood test marked pending with sentinel comment (will flip to active green at Phase 3).</criterion>
    <criterion id="AC4">build-nodejs-lambda.sh exits non-zero on test failure (intentional break verified + reverted).</criterion>
    <criterion id="AC5">Tag bump + push --follow-tags + record-terraform-deploy.sh.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None — independent. Preferred to ship before TO-FIRMSEP.03 (extraction) so the gate catches extraction regressions.</upstream>
    <downstream>TO-FIRMSEP.10 Phase 3 flips cottonwood test from pending to active green.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~19:55Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Mocha + Sinon per OQ7 default. Cottonwood test is intentional sentinel — pending until Phase 3.</message>
  </go_signal>
</task_order>
