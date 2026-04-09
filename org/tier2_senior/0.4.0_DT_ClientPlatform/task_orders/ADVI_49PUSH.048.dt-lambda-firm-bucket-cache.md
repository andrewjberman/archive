<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-048-dt</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-09</date>
    <status>staged</status>
    <project_code>ADVI_49PUSH</project_code>
    <phase>Books Tab Performance</phase>
    <priority>HIGH</priority>
    <pipeline>partners-api</pipeline>
    <current_tag>partners-api-v1.15.4</current_tag>
  </metadata>

  <objective>
    Add a module-level dict cache to get_firm_bucket() in opal-partners-data
    lambda_function.py. Eliminates a redundant DynamoDB get_item call on every
    warm L2/L3 Books tab invocation. Deploy as partners-api-v1.15.5.
  </objective>

  <context>
    Every Books tab advisor drill (L2) and client drill (L3) routes through
    opal-partners-data Lambda. The current get_firm_bucket() implementation
    (lambda_function.py:~171) calls users_table.get_item() unconditionally on
    every invocation to look up the S3 bucket name for a firm_id.

    Firm bucket names never change between Lambda restarts. A module-level cache
    eliminates this call on warm invocations.

    Measured cost: 15-40ms per L2/L3 request on warm Lambda.

    This fix is independent of ADVI_49PUSH.047 (DS clients-tab payload rebuild).
    Both can deploy in parallel. If DS.047 produces a Lambda routing change handoff,
    that will be a separate DT task after DS completes their investigation.

    comp-blast opal-partners-data: no downstream consumers found -- safe to modify
    lambda_function.py without cross-agent coordination.
  </context>

  <change>
    File: infra/aws/lambda/opal-partners-data/lambda_function.py

    Add at module scope (near existing module-level globals, before any handler):

      _bucket_cache: dict[str, str] = {}

    Replace the get_firm_bucket function body with:

      def get_firm_bucket(firm_id: str) -> Optional[str]:
          if firm_id in _bucket_cache:
              return _bucket_cache[firm_id]
          try:
              response = users_table.get_item(
                  Key={'PK': f'FIRM#{firm_id}', 'SK': 'META'}
              )
              item = response.get('Item')
              if item and item.get('s3Bucket'):
                  _bucket_cache[firm_id] = item['s3Bucket']
                  return _bucket_cache[firm_id]
          except Exception as e:
              print(f'ERROR: get_firm_bucket failed for {firm_id}: {e}')
          return None

    No other changes to lambda_function.py.
    Note: the HMAC key cache (_key_cache in pseudonymizer.py) is already correct
    at module scope -- do not touch it.
  </change>

  <deployment_sequence>
    1. Read lambda_function.py -- confirm current get_firm_bucket location and signature
    2. Apply the change above
    3. Verify no other callers of get_firm_bucket exist that would break (grep the file)
    4. Commit:
         git commit --author="0.4.0_DT_ClientPlatform <0.4.0_DT_ClientPlatform@opal.agent>" \
           -m "perf(opal-partners-data): cache get_firm_bucket in module scope -- skip DynamoDB on warm hits"
    5. Run build-and-upload.sh for opal-partners-data
    6. terraform plan -- confirm 1 resource changes (Lambda source hash)
    7. terraform apply
    8. Verify 0-diff plan
    9. Tag: partners-api-v1.15.5
    10. Push --follow-tags
  </deployment_sequence>

  <cross_domain_coordination>
    comp-blast opal-partners-data returned: no downstream consumers.
    This Lambda is consumed by the portal frontend only (CloudFront -> API GW -> Lambda).
    No other gold scripts, Lambdas, or pipelines read from it.
    No MCP coordination required before committing.
  </cross_domain_coordination>

  <compiler_tools_mandate>
    Before writing:
      comp-trace opal-partners-data --direction both
        -- Confirm no shared callers of get_firm_bucket outside lambda_function.py

    Before committing:
      grep -n "get_firm_bucket" infra/aws/lambda/opal-partners-data/lambda_function.py
        -- Confirm only one definition, all call sites unchanged

    After deploy (verify fix landed):
      Check CloudWatch logs for opal-partners-data after an L2 Books tab request.
      First invocation: DynamoDB call present in logs (cache miss -- expected).
      Second invocation same firm_id: no DynamoDB call in logs (cache hit -- expected).
      Log the before/after timing in your session log.
  </compiler_tools_mandate>

  <acceptance_criteria>
    1. get_firm_bucket definition contains early-return on _bucket_cache hit
    2. No other changes to lambda_function.py
    3. partners-api terraform apply reaches 0-diff
    4. Tag partners-api-v1.15.5 exists and is pushed
    5. CloudWatch confirms cache hit on second same-firm invocation (no DynamoDB call)
    6. Session log documents: line numbers changed, timing observed before/after if measurable
  </acceptance_criteria>

</task_order>
