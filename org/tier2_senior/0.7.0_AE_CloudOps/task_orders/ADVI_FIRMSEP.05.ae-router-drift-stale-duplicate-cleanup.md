<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_FIRMSEP.05</id>
    <project>ADVI_FIRMSEP</project>
    <title>ROUTER-DRIFT absorption — stale duplicate directory cleanup + CloudTrail audit</title>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <completed_date>2026-05-07</completed_date>
    <completed_by>0.7.0_AE_CloudOps~B</completed_by>
    <priority>medium</priority>
    <estimated_effort>~0.25d</estimated_effort>
    <folded_scope>tier-router-edge dead-code removal — per COO RAVC1 ack 2026-05-07T20:05Z. Stale duplicate dir cleanup (TO base scope) was already shipped by AE 0.7 base lane in commit 59919e763 (15:13 EDT, pre-session). FIRMSEP.05 ~B closeout work = (a) verify base lane cleanup is structurally complete + (b) execute folded tier-router-edge removal.</folded_scope>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FIRMSEP.md §4.8 + §6 Phase 1</ref>
    <ref type="absorbs">ADVI_INFETL.ROUTER-DRIFT — already assigned to AE 0.7 primary; data-path reconciliation already shipped (per AE 0.7 RAVC); FIRMSEP.05 absorbs the remaining stale-duplicate-directory cleanup + CloudTrail audit.</ref>
    <ref type="canonical_source">infra/aws/lambda-edge/shared-advisor-router/index.mjs (current, v13)</ref>
    <ref type="stale_target">infra/aws/lambda/shared-advisor-router/ (older copy without firm-routing logic; cause of RD INFETL.007 audit confusion)</ref>
  </references>

  <context>
    AE 0.7 primary already shipped the data-path reconciliation portion of ROUTER-DRIFT
    (deployed Lambda code + canonical Terraform alignment). FIRMSEP.05 closes out the remaining
    cleanup: delete the stale duplicate directory + CloudTrail audit to identify creation
    history.

    Why it's still in scope: as long as infra/aws/lambda/shared-advisor-router/ exists, future
    audits may misread it as canonical (the RD INFETL.007 audit incident happened exactly
    this way). The directory has no live AWS Lambda function backing it — it's pure repo
    debt — but the file's mere existence creates a structural footgun.

    CloudTrail audit is best-effort. The file is months old; CloudTrail retention may not
    cover its creation. Document the audit attempt + finding (or dead-end).
  </context>

  <scope>
    <step>
      Pre-cleanup verification:
        - git grep -rE "lambda/shared-advisor-router" — should be 0 hits in code (only in
          paths that point inside the directory itself, which we're about to delete).
        - Search Terraform for any reference to lambda/shared-advisor-router (NOT the
          lambda-edge/ path):
            grep -rE "lambda/shared-advisor-router" infra/aws/terraform/
        - Search build wrappers + CI:
            grep -rE "lambda/shared-advisor-router" infra/aws/lambda/ci/ .tools/ .github/
        - All hits should be paths inside the directory or zero. If any external reference
          exists → stop, RAVC1 with the reference, do not delete.
    </step>
    <step>
      AWS-side verification: confirm there is NO Lambda function deployed from this path.
        aws lambda list-functions --query 'Functions[?contains(FunctionName,`shared-advisor-router`)].{Name:FunctionName,Code:CodeSha256}'
      The only live one should be the Lambda@Edge function deployed from lambda-edge/ —
      identifiable by region us-east-1 + ARN containing :function:shared-advisor-router.
      Confirm the deployed CodeSha256 matches a build of the lambda-edge/ source, not the
      lambda/ source.
    </step>
    <step>
      CloudTrail audit (best-effort):
        aws cloudtrail lookup-events \
          --lookup-attributes AttributeKey=ResourceName,AttributeValue=shared-advisor-router \
          --start-time 2025-08-01T00:00:00Z --end-time 2026-05-07T00:00:00Z \
          --max-results 50 \
          --query 'Events[].{Time:EventTime,User:Username,Event:EventName,Source:EventSource}'
      Look for early UpdateFunctionCode / CreateFunction / s3:PutObject events on the path.
      If CloudTrail retention truncates → document as "history pre-dates retention; dead-end".
      If a creator can be identified → document.
    </step>
    <step>
      Delete the stale directory:
        git rm -r infra/aws/lambda/shared-advisor-router/
      via .tools/safe-commit.sh per CLAUDE.md rule 14a (POD4_OR_AE lane). Author:
        --author "0.7.0_AE_CloudOps~B &lt;0.7.0_AE_CloudOps~B@opal.agent&gt;"
        -m "chore(ADVI_FIRMSEP.05): delete stale shared-advisor-router duplicate dir (canonical at lambda-edge/)"
        -- infra/aws/lambda/shared-advisor-router/
    </step>
    <step>
      Post-delete verification:
        - git grep -rE "lambda/shared-advisor-router" → 0 hits.
        - Build-and-deploy a Lambda@Edge function (pick a small unrelated one) to confirm
          CI/build pipelines unaffected.
        - Smoke test: Inflection + 49F portal routes still serve correctly (canonical
          lambda-edge/ source unaffected).
    </step>
    <step>
      Push CLOUD. (No tag bump — pure repo cleanup, no infra change.)
    </step>
    <step>
      RAVC2 to COO + close ADVI_INFETL.ROUTER-DRIFT TO with FIRMSEP.05 absorption note:
        - Pre-cleanup grep results.
        - AWS-side verification (no live function from stale path).
        - CloudTrail audit finding (creator identified | dead-end documented).
        - Commit hash + repo-clean post.
        - Smoke test post-delete.
    </step>
  </scope>

  <compiler_mandate>
    <tool>git grep "lambda/shared-advisor-router" — pre + post (both 0 external hits)</tool>
    <tool>aws lambda list-functions — confirm no live function from the stale path</tool>
    <tool>aws cloudtrail lookup-events — best-effort audit history</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">infra/aws/lambda/shared-advisor-router/ deleted from CLOUD.</criterion>
    <criterion id="AC2">git grep returns 0 external references post-delete.</criterion>
    <criterion id="AC3">No live Lambda function backed by the stale path.</criterion>
    <criterion id="AC4">CloudTrail audit completed (creator | dead-end documented).</criterion>
    <criterion id="AC5">Inflection + 49F portal smoke tests green post-delete.</criterion>
    <criterion id="AC6">ADVI_INFETL.ROUTER-DRIFT TO closed out with FIRMSEP.05 absorption note.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>ADVI_INFETL.ROUTER-DRIFT data-path portion already shipped by AE 0.7 primary.</upstream>
    <downstream>None.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~19:55Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Pure repo cleanup. Verify no external references before delete; CloudTrail best-effort.</message>
  </go_signal>
</task_order>
