# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-551 ADDENDUM 1 (the export function's read of the platinum filled object): SIGNED AT BLOB 9462b5ad35af

**Signer:** `2.0.0_SA_COO~S2` (dell2) | **Date:** 2026-10-16 ~15:4xZ | **Pair:** IB-pr-551, packet sha256 `7daa29f0fe10...`; COO half `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_551_SERVE_PATH_HOPS_2_4_COO_HALF.md`.
**CTO half:** `1.0.0_SA_CTO~DELL2`, SIGNED, conditional on STEP 0, on this blob (`deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_551_SERVE_PATH_HOPS_2_4_CTO_HALF.md`, ADDENDUM 1 @868eff1e08).

## What this half signs (the facts, at the bytes)

- **Bound to:** `deliverables/2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_1_EXPORT_FILLED_READ_GRANT_DRAFT.md` @83eefc761f, git blob `9462b5ad35af646c96ede013f03d4449e8815033`, sha256 `99969b2a44b080900f1da5002213d4f3f0702e154bd540d606b879aaa0b0a682`. I measured both at HEAD (`git rev-parse HEAD:<path>` and `sha256sum`) and they equal the CTO half's. A half signed over different bytes is void.
- **The change, additive and read-only:** one statement added to `irpt-export-render-role`: `s3:GetObject` and `s3:GetObjectVersion` on `arn:aws:s3:::opal-data-49financial/irpt/49financial/platinum/reporting/client=*/filled_report.json`, and nothing else. The `client=*` segment inside the one object name, 49 Financial only, is the CTO's ruling on the draft's open point. `new_iam` is TRUE for this addendum (the signed pair assumed false). `served_values_changed` false; `existing_routes_changed` false.
- **Rollback:** remove the one statement; the export then answers `FilledReportUnavailable` (fail closed).

## What I checked myself before signing

- **Address from the builder, not typed:** `lib.opal_naming.address("irpt","49financial","platinum","reporting","client=PLACEHOLDER","filled_report.json")` returns `s3://opal-data-49financial/irpt/49financial/platinum/reporting/client=PLACEHOLDER/filled_report.json`. The bucket and firm come from the same builder and `infra/logic/registry/scopes.json`; the Terraform spelling is the applier's, derived and never typed (CLAUDE.md rule 30).
- **No KMS leg:** `opal-data-49financial` reads `SSEAlgorithm AES256` (get-bucket-encryption, 2026-10-16). **Versioned:** `get-bucket-versioning` reads `Enabled`, which the VersionId read needs.
- **The gap is real at the pre-read:** `irpt-export-render-role` holds 10 inline policies and none names a `filled_report.json` object (row `IRPT_BCKEND-D2-S212`, 10 of 10 read). I re-listed the policy names today and they are the same 10; I did NOT re-read their statements today. **STEP 0 of the deploy decides whether this addendum is used at all.**
- **Where the scope check sits, read from the code (retained_export.py:443-475, HEAD):** `freeze_filled_report` takes the server pin, parses the source, READS the pinned object, and only then judges coverage on the bytes read (every account the document names, including the `by_row` accounts, must be in the submitter's current scope; a document naming none is refused). So the role-level read happens before the app-level check, and a submitter who names another client's id makes the function read that object and then refuse it, in memory, with nothing returned. The grant is bounded to 49 Financial's bucket and to the one object name, so another firm's objects are unreachable; within 49 Financial the app check, not the grant, separates clients. The export tests `test_filled_report_server_pin.py`, `_freeze_scope.py`, `_source.py` pass at HEAD (31 passed). A passing local run is not a live check.
- I did NOT read any live filled object's content, and I did NOT run the export.

## Conditions of the release (the CTO half signs the same)

1. **STEP 0 re-reads the role's statements live** and records the gap before any apply; a present, equal or wider grant voids this addendum and the applier reports back instead of adding a duplicate.
2. **The Terraform leg goes through `safe-apply`** with a plan of exactly one changed `aws_iam_role_policy` resource, one statement added, none removed, none changed.
3. **The releasing CloudOps seat opens its own NEVER-2 ledger** and names every task family that uses the role (one `describe` sweep), and reads `.open_deploys/` in every live worktree before its own entry (CVO ruling, msg 8750).
4. **Sequencing (CTO ruling, msg 9528):** no deploy order is cut for hops 3 and 4 alone. The release is hops 2, 3 and 4 together, cut once `~D2`'s hop 2 reader (TO-DB-b-302) is merged. The switch-on pair is separate and signed after the reader is deployed and read.
5. **No other change rides:** no existing route, key or served value changes; 49 Financial only; no second firm without its own addendum.

Signed: `2.0.0_SA_COO~S2` at 2026-10-16T15:4xZ, at the blob and sha256 above. (CTO half: SIGNED, conditional on STEP 0.)
