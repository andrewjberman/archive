# IB154-1 -- the commentary draft store's persist answer, read at base c2843cad7d

Cell IB-pr-458, worker 0.9.0_WK_IRPT_BCKEND~314. A code and contract read: no AWS call, no network call, no vendor request, no product file edited, no contract change proposed. S = `infra/aws/lambda/investor-reporting/reports/commentary_draft_store.py`; H = `data/transcripts/scripts/commentary/lambda_handler.py`. Each sentence ends with its claim word.

## The answer today

1. The persist operation is `op: "put"` of `irpt-commentary-draft-store-lambda`; its entry is `lambda_handler` at S:274, through `handle` (S:178) and `store` (S:146). (measured)
2. A first persist answers `{status: "OK", commentary_ref: {artifact_id, sha256, version_id}}`, built at S:171. The crash-recovery path (artifact written, ref never set) returns through the same line. (measured)
3. A replay (a ref is already set) answers `{status: "REFUSED", reason: "ALREADY_WRITTEN"}` (raised S:156 or S:223, built S:175). It has no `commentary_ref`. (measured)
4. The other refusals are the same two-member body with reason `INVALID_REQUEST`, `UNAVAILABLE`, `INTEGRITY` or `REFUSED` (S:175; raised at S:91-108, S:120, S:123, S:166, S:168, S:184-187). An error the handler does not catch leaves no body; the Lambda runtime builds an error document that is not in the repo. (measured for the lines; inferred for the runtime document)
5. No schema or contract file declares this shape: nothing under `_contracts/` or `docs/contracts/investor-reporting/v1/` names the draft store, `get_ref`, `ALREADY_WRITTEN` or `commentary_ref`. Only the module docstring (S:11-14) describes it in prose. Whether extra members are forbidden is therefore declared nowhere. (measured)
6. The tests pin it by exact key set: `test_commentary_draft_store.py:96` (top level of the first persist) and `:98` (the ref), and by whole-dict equality for the replay and the coded refusals (`:145`, `:171`, `:177`, `:180`, `:186-188`). Adding a member to those answers fails them. The crash-recovery answer is pinned for its ref only (`:163-164`). (measured)

## Who calls it and as whom

7. The only runtime caller is the drafter's `persist_draft` port (H:131-138, invoked at H:321), a synchronous Lambda invoke at H:114. It runs as role `outlook-global-commentary-draft-role`, which holds `lambda:InvokeFunction` on that one function through `irpt-commentary-draft-store-invoke-policy` (`commentary_draft_store.tf:121-131`, attached at `infra/aws/terraform/transcripts/commentary.tf:256-259`). The recorded IAM census (`workflows/legacy_transform/mdpf/20261011T181700Z-98fc86e/live-iam-census.json:30111`) shows that policy on that role only. (measured; the census is a recorded artifact, not a live read)
8. Three other callers are offline tests with no AWS principal. (measured)

## Who reads the answer

9. Files naming the persist operation: 81 = 4 consumers + 1 producer + 76 neither (the producer is the store; the 76 are infrastructure, naming files, text-reading tests, check scripts and org documents). (measured)
10. Seven consumer entries, 4 drafter and 3 test. The drafter reads `status`, `reason` and `commentary_ref` (H:122-125), then only `artifact_id`, `sha256`, `version_id` (H:136-138, H:322). On an unknown member the drafter ignores it, because H:125 returns only `commentary_ref` and H:138 copies exactly three keys. Of the tests, `test_commentary_draft_store.py` refuses an unknown member (the exact key set); the other two ignore it. (measured)
11. The portal checkout at `C:/dev/ajb_workspace/portal` (commit dbeb6764ea) was read: no match. The worktree's own `portal/`, `opal_ai/` and any `mcportal` were not searched; live AWS and the built zips were not read. (measured; absence stated as not searched)

## The accepted record at persist

12. The store reads the accepted record on every put: `requests.get(...)` at S:115 (live port `DynamoAcceptance.get`, `acceptance.py:68-71`, returns the `record` attribute). It takes `identity.request_id`, `identity.tenant_firm_id` and `owner` (S:116-124) and nothing else. It then reads the item again at S:152 for the separate `commentary_ref` attribute. (measured)
13. A `ticket_id`, when the record has one (`acceptance.py:120-121`), is a member of the dict already held at S:115. `resolve_request` returns only `(tenant, owner)`, so it is reachable without a new read. Whether any live record carries one is not established. (measured for the code; not established for live data)

## The ticket id in the answer today

14. With a ticket id on the record, or without, the answer is identical and carries nothing about the ticket; an offline probe on the store's fakes showed the same body in both runs. The store never branches on `ticket_id`. (measured)
15. The drafter next step is also identical, because it never holds a ticket id: it sends `commentary_ready` (H:324); a queue-driven run stops at stage `draft_stored` with no ticket (H:325-328); any other run posts a NEW ticket whose body has `report_request_id` and no ticket id (H:329, `ticket_client.py:33-43`, `entry.py:209-220`). On a replay the persist raises `DRAFT_STORE_ALREADY_WRITTEN` (H:124). (measured)

## Not established

The live shape of any accepted record's `ticket_id`; the Lambda runtime's error document; the repository's full refusal causes; whether deployed zips equal the base source (`lambda-source-map.json:6694` still says DESIRED); who else holds the invoke permission live; how the ticket route matches a request id. Listed in full in the JSON under `not_established`.
