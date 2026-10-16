<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-R34POOL.classification-table-export-aq2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-16</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- a READ ONLY order: one describe-table and one paginated scan of the canonical classification table with a three-attribute projection (ticker, asset_class, sub_asset_class); no write, no policy, no queue, no secret, no host, no Lambda. The three columns are Opal's own reference data (no client figure, no account identifier, no firm label).
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: RUN-AS-A-READ -- step 1 asks whether YOUR principal may scan the table; the resident role's own grant (GetItem only) is not touched and no IAM change is made. If your principal is denied the scan, STOP: nothing is tried through another principal.
comp-adversary: RUN -- by reading the CTO's ADDENDUM 5 (msg 8714: the pool is a dated snapshot of ticker, asset_class and sub_asset_class only, claim held, no IAM change) against this cell; the lens: a scan read as complete when it was a page (the order requires the page count and the absence of LastEvaluatedKey as the denominator), a projection that leaks another attribute (the export is checked for exactly three attribute names per item), a snapshot dated to a time other than the read, a count taken from describe-table (approximate) instead of the scan. NOT seen: the live row count until step 2; denominator: one table, three attributes per item.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R26_G.md</decomp_doc> round 26, workstream ~G: the pool snapshot input for resident release r34.
<owned_cells>AR-g-106</owned_cells>
</decomp_ref>

  <objective>
    READ the canonical classification table once, whole, and write its three class columns to one export file; build the swap pool snapshot from it with the repository's own builder; commit both files; report ONCE to 2.0.0_SA_COO~G2. Change NOTHING in AWS.
  </objective>

  <context>
    Load /cloud-ops first. The pool is the class-matched candidate set of the backend swap (C-SWAP step 4): CTO ADDENDUM 5 of `CTO_RULING_DELL2_IRPT_ANLREQ_FOUR_LANES_END_TO_END_20261015.md` (msg 8714) rules it a dated snapshot shipped in the resident package, with `pool_as_of` and the claim `held`, and no IAM change (the resident role holds `dynamodb:GetItem` on `etf-classifications` only). The table is `etf-classifications` (hash key `ticker`, us-east-1). The builder is `infra/aws/lambda/investor-reporting/ycharts/research/build_swap_pool.py` (merged; cell AR-g-98): `python build_swap_pool.py --items <export.json> --as-of YYYY-MM-DD --out <pool.json>` reads a JSON list of items or an `aws dynamodb scan` answer, keeps ONLY ticker, asset_class and sub_asset_class, counts what it skips, reads its own output back through `swap_pass.load_pool`, and prints a last line `SWAP-POOL rows=.. skipped=.. classes=.. max_class=.. max_requests_per_holding=.. as_of=.. sha256=..`.
  </context>

  <the_act>
    GO. Start at step 1; stop on any step that reads wrong and tell 2.0.0_SA_COO~G2.
    1. THE READ. `dynamodb describe-table` on etf-classifications: print the table status, ApproximateItemCount and whether it has a customer-managed key. Then the scan, whole, paginated until the answer carries no LastEvaluatedKey: `scan` with `--projection-expression "ticker, asset_class, sub_asset_class"` (use `--expression-attribute-names` if a name is reserved), Select SPECIFIC_ATTRIBUTES; print the page count, the item count per page summed, and that the last page had no LastEvaluatedKey. A denied scan (an AccessDenied for your principal): STOP, write the single line `DENIED <code>` to org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/POOL_RESULT.txt, report once, and do not try another principal. Record the UTC date of the scan (`date -u +%F`) as AS_OF.
    2. THE EXPORT. Write the pages, merged into one JSON object `{"Items": [...]}` with the DynamoDB-typed attributes exactly as the scan returned them, to org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/etf_classifications_export.json (UTF-8). Check that every item has no attribute other than ticker, asset_class and sub_asset_class (print the count of items with another attribute: it must be 0; if it is not, STOP, delete nothing, report).
    3. THE POOL. In your worktree run `python infra/aws/lambda/investor-reporting/ycharts/research/build_swap_pool.py --items org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/etf_classifications_export.json --as-of <AS_OF> --out org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/swap_pool.json`; its last line must begin `SWAP-POOL rows=`. A line beginning `SWAP-POOL-REFUSED`: STOP and report with the line. Print the builder's line in the report; the skipped count with its reasons (call `build_rows` on the export in a python one-liner to print the reason dict) is part of the report.
    4. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/POOL_RESULT.txt with ONE line each, exactly: `POOL_ROWS <n>`, `POOL_SKIPPED <n>`, `POOL_CLASSES <n>`, `POOL_MAX_CLASS <n>`, `POOL_REQUESTS_PER_HOLDING <n>`, `POOL_AS_OF <YYYY-MM-DD>`, `POOL_SHA256 <64 hex>` (the values of the builder's line). Commit the three files (export, pool, result) in one commit. Report ONCE to 2.0.0_SA_COO~G2 with the lines and the commit.
  </the_act>

  <bounds>
    One table, read only: one describe-table and one paginated scan. No write of any kind to AWS, no item, key, policy or capacity change, no export to S3, no second principal. The export carries three attributes per item and nothing else. Not in this order: building the release, the resident host, any Lambda, enabling anything.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/IRPT_ANLREQ.TO-READ-R34POOL.classification-table-export-aq2.proof_of_spec.json`.
    <criterion id="R34POOL-AC1" cell_refs="AR-g-106">The result file carries the seven lines of a completed read, or the single denial line.<invocation>grep -c -E '^(POOL_ROWS [0-9]+|POOL_SKIPPED [0-9]+|POOL_CLASSES [0-9]+|POOL_MAX_CLASS [0-9]+|POOL_REQUESTS_PER_HOLDING [0-9]+|POOL_AS_OF [0-9]{4}-[0-9]{2}-[0-9]{2}|POOL_SHA256 [0-9a-f]{64}|DENIED .+)$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/POOL_RESULT.txt</invocation><expect>^(7|1)$</expect></criterion>
    <criterion id="R34POOL-AC2" cell_refs="AR-g-106">The committed pool loads through the swap pass and claims held.<invocation>python -c "import sys; sys.path.insert(0, 'infra/aws/lambda/investor-reporting/ycharts/research'); import swap_pass; p = swap_pass.load_pool('org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/swap_pool.json', '2099-12-31'); print('POOL-LOADS', p['rows_count'], p['pool_claim'])"</invocation><expect>^POOL-LOADS [0-9]+ held$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-g-106 is the issuer's, as for TO-READ-R31.
