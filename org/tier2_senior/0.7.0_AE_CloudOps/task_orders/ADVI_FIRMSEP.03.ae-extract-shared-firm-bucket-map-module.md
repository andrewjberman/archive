<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_FIRMSEP.03</id>
    <project>ADVI_FIRMSEP</project>
    <title>Extract shared FIRM_BUCKET_MAP module — close TODO comment, single source for both Lambda@Edge functions</title>
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
    <ref type="prd">docs/architecture/ADVI_FIRMSEP.md §4.3 + §6 Phase 1</ref>
    <ref type="duplicate_today">infra/aws/lambda-edge/auth-validator-edge/index.mjs:97-105 + infra/aws/lambda-edge/shared-advisor-router/index.mjs:175-179 — identical FIRM_BUCKET_MAP literal + comment "TODO: extract to shared config module once we have >2 partners"</ref>
    <ref type="trigger_met">Cottonwood = 3rd partner. TODO trigger met.</ref>
    <ref type="lambda_edge_constraints">No Layers, no env vars at runtime, build-time-constant only. Build pipeline must copy _shared/ into each function zip.</ref>
  </references>

  <context>
    Both Lambda@Edge functions hardcode FIRM_BUCKET_MAP. The TODO comment explicitly waits for
    the >2-partner trigger; Cottonwood meets it. Shared-module extraction closes the
    "update both files" footgun structurally — Cottonwood becomes a single-line edit instead
    of a 2-file edit (which is the failure mode that matters: a missed second edit ships a
    cross-tenant routing inconsistency).

    Lambda@Edge has constraints — no Layers, no Parameter Store at request time. The shared
    file must be COPIED into each function's deploy zip at build time. The build wrapper
    (build-nodejs-lambda.sh) needs to honor the _shared/ path.

    This TO PREFERS to ship after TO-FIRMSEP.04 (CI test) so the test catches any extraction
    regression mechanically — but the dependency is preference, not strict.
  </context>

  <scope>
    <step>
      Create infra/aws/lambda-edge/_shared/firm-bucket-map.mjs:
        export const FIRM_BUCKET_MAP = {
          "49financial": "opal-data-bd",
          "inflection":  "opal-data-inf",
          "mockadv":     "opal-data-bd",
        };
      (Match exact key/value pairs from current inline maps — 49financial / inflection / mockadv → bd | inf. Do NOT add cottonwood here yet — that lands in Phase 3 TO-FIRMSEP.10.)
    </step>
    <step>
      Update auth-validator-edge/index.mjs:
        - Replace inline FIRM_BUCKET_MAP literal (lines 97-105) with: import { FIRM_BUCKET_MAP } from "../_shared/firm-bucket-map.mjs";
        - Verify all references to FIRM_BUCKET_MAP still resolve.
    </step>
    <step>
      Update shared-advisor-router/index.mjs:
        - Same import replacement at lines 175-179.
        - Verify references.
    </step>
    <step>
      Update infra/aws/lambda/ci/build-nodejs-lambda.sh (or whichever wrapper builds Lambda@Edge zips):
        - Detect _shared/ path siblings to the function dir.
        - Copy _shared/* into the zip's relative ../_shared/ before zipping.
        - Verify zip parity post-build (both function zips contain the same _shared/firm-bucket-map.mjs SHA256).
    </step>
    <step>
      Local node test: import from each function's path resolves the shared module
      (node -e "import('./infra/aws/lambda-edge/auth-validator-edge/index.mjs').then(...)" — or equivalent build-time syntax check).
    </step>
    <step>
      build + deploy auth-validator-edge:
        - bash infra/aws/lambda/ci/build-nodejs-lambda.sh portal-auth auth-validator-edge
        - terraform plan in portal-auth — should show source_code_hash change for both functions.
        - apply.
        - Lambda@Edge replication takes ~5-10min — wait for "Function deployed" status.
    </step>
    <step>
      build + deploy shared-advisor-router (same pattern).
    </step>
    <step>
      Empirical post-deploy:
        - 49Financial smoke test (curl with 49F JWT against advisor-intelligence route → 200 + correct payload).
        - Inflection smoke test (same with Inflection JWT).
        - mockadv smoke test (same with mockadv JWT — internal Opal staff route).
        - Missing X-Firm-Id (after JWT strip) → expect 403.
    </step>
    <step>
      Tag bump portal-auth-v1.X.Y (per git tag -l "portal-auth-v*" | sort -V | tail -3). Push --follow-tags.
    </step>
    <step>
      RAVC2 to COO: zip parity SHA256, plan + apply, all 4 smoke tests, replication confirmation, tag.
    </step>
  </scope>

  <compiler_mandate>
    <tool>zip parity SHA256 — _shared/firm-bucket-map.mjs identical in both function zips</tool>
    <tool>comp-iam service auth-validator-edge — verify scope unchanged post-deploy</tool>
    <tool>comp-iam service shared-advisor-router — same</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">_shared/firm-bucket-map.mjs is single source; both function inline maps replaced with imports.</criterion>
    <criterion id="AC2">build-nodejs-lambda.sh copies _shared/ into each function zip; SHA256 parity verified.</criterion>
    <criterion id="AC3">Both Lambda@Edge functions deploy successfully + replicate.</criterion>
    <criterion id="AC4">All 4 smoke tests green (49F, Inflection, mockadv, missing-firm-id → 403).</criterion>
    <criterion id="AC5">portal-auth tag bumped + push --follow-tags + record-terraform-deploy.sh.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>PREFERRED (not strict): TO-FIRMSEP.04 ships first so its CI gate catches extraction regressions.</upstream>
    <downstream>TO-FIRMSEP.10 Cottonwood onboarding becomes a single-line edit on _shared/firm-bucket-map.mjs.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~19:55Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Lambda@Edge extraction with build-toolchain wire-up. Coordinate ordering with .04 if possible. RAVC2 with parity SHA + 4 smoke tests.</message>
  </go_signal>
</task_order>
