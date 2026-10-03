# GW2_BEHAVIOUR_DIFF -- what the grant writer does differently once redeployed from af2d762970 (OG-gw-2 PHASE A, step 2)

Author: `0.9.0_WK_NFRA_OPLGTW~26`, round 15. Branch `wk-NFRA_OPLGTW-26-r15` at CLOUD `4b6afce2d2` (carries OG-gw-1's pinned builder
`22d6f8436b`). This file is what the CVO grades; nothing here is applied. No variable or secret value appears anywhere in it.

## 1. What was compared, and how

- **Deployed:** `aws lambda get-function --function-name mcportal-grant-writer-lambda`, `Code.Location` fetched and unzipped IN MEMORY.
  `CodeSha256` `nhz+dwJsDJLO9X3o1exvKdQ+OYE+PraxZSop2BJt9zI=`, 54650 bytes, `LastModified` 2026-09-30T10:58:57Z, `State`/`LastUpdateStatus`
  `Active`/`Successful`. The bytes were saved outside the repo (rollback source), sha256
  `9e1cfe77026c0c92cef57de8d5ec6f29d43e39813e3eb6b1652a29d8126df732`.
- **Staged:** `build_package.py --out ...` at this worktree printed `build_package.py: staging from deployed_commit af2d762970` (rc 0). The manifest at
  HEAD names `af2d7629702528c050860314a7867d8ea0cecfbf` for `services.opal-gateway`.
- **Denominator:** 11 files deployed, 11 staged, same 11 names. **8 SAME, 3 DIFF, 0 only-deployed, 0 only-staged.**

| file (repo-relative, inside the zip) | deployed sha256[:16] | staged sha256[:16] | bytes deployed | bytes staged | verdict |
|---|---|---|---|---|---|
| `infra/aws/ec2/opal-gateway/app/__init__.py` | e3b0c44298fc1c14 | e3b0c44298fc1c14 | 0 | 0 | SAME |
| `infra/aws/ec2/opal-gateway/app/access_state.py` | daf8d8c44c0c14b5 | daf8d8c44c0c14b5 | 27640 | 27640 | SAME |
| `infra/aws/ec2/opal-gateway/app/config.py` | 7244283c201a2eca | 3128d463bd6f5e42 | 27507 | 29788 | **DIFF** |
| `infra/aws/ec2/opal-gateway/app/context.py` | be7c21110bb1a761 | be7c21110bb1a761 | 4651 | 4651 | SAME |
| `infra/aws/ec2/opal-gateway/app/data_entitlement.py` | c12839d856ec2f57 | a9eafa664374b93d | 31834 | 32133 | **DIFF** |
| `infra/aws/ec2/opal-gateway/app/graphql_plumbing/__init__.py` | a6e7da7d80b0fe4d | a6e7da7d80b0fe4d | 216 | 216 | SAME |
| `infra/aws/ec2/opal-gateway/app/graphql_plumbing/catalog_gate.py` | 632300715a30943a | 632300715a30943a | 7612 | 7612 | SAME |
| `infra/aws/ec2/opal-gateway/ops/__init__.py` | e3b0c44298fc1c14 | e3b0c44298fc1c14 | 0 | 0 | SAME |
| `infra/aws/ec2/opal-gateway/ops/schwab_entitlement_admin.py` | f9bb800408af303a | f9bb800408af303a | 27887 | 27887 | SAME |
| `lambda_function.py` | 7e80d43598591426 | 7e80d43598591426 | 22040 | 22040 | SAME |
| `org/standards/NFRA_OPLGTW_CONTRACT.json` | f47703a611e5bf6f | a86f7e667cfc3ec8 | 8806 | 9189 | **DIFF** |

**The blob ids (row `NFRA_OPLGTW-Z-W26-S1`).** `TF_ROOT_FIX.md` s.1 and the order call `c19f86c295`, `aac92bdff8`, `c2f5d5a071` "the deployed blobs"; they are
COMMIT ids. Resolved: `c19f86c295:.../app/config.py` = blob `b3a9609fad`, `aac92bdff8:.../app/data_entitlement.py` = `e5db4d307d`,
`c2f5d5a071:org/standards/NFRA_OPLGTW_CONTRACT.json` = `848ec665d8`. `git hash-object` of the three deployed-zip members equals those three blob ids exactly, so the
deployed bytes are the older committed blobs (the control holds). The staged blobs equal `git rev-parse af2d762970:<path>`: config `864536c8bb`,
data_entitlement `c25f71c7ba`, contract `2d9181f8bc`. The diffs below are blob to blob (`git diff <deployed blob> <staged blob>`).

## 2. The grant writer's actual call sites (the trace every change below is held against)

The Lambda's import closure is `lambda_function.py` + `app.access_state` + `ops.schwab_entitlement_admin` and what those import (11 files above).

- `lambda_function.py` (`handle`, lines ~335-365): `admin.prepare(st, candidate, contract or admin.load_contract())`, `admin.activate(...)`,
  `admin.current_state(...)`, `admin.revoke(...)`, `admin._scope_to_raw`, `admin._audit_id`; `acs.store()`, `acs.Key`, `acs.Op`. It catches
  `admin.AdminRefused` -> `{"verdict": "REFUSED", "reason": "ADMIN-REFUSED"}` and `acs.ConditionFailed` -> `STALE-REVISION`.
- `ops/schwab_entitlement_admin.py` -> `app.data_entitlement` as `de`: `de.parse_scope`, `de.parse_profile`, `de.parse_grant`, `de.profile_key`, `de.grant_key`,
  `de.profile_item`, `de.grant_item`, `de.profile_put_op`, `de.grant_put_op`, `de.operator_audit_op`, and the constants `de.GRANT_DATE_MODES`, `de.OPERATIONS`,
  `de.DISABLED_OPERATIONS`, `de.PORTAL_DIMENSION`. -> `app.context` as `context`: only `context.make_principal` (admin line 158). -> `app.access_state` as `acs`.
- The contract: `admin.load_contract()` opens `org/standards/NFRA_OPLGTW_CONTRACT.json` (path climbs `parents[5]` to the package root, which the mirrored layout satisfies).
  `admin.validate_candidate` reads exactly SIX keys of it: `fields`, `forbidden_field_classes`, `grant_date_modes`, `operations`, `disabled_operations`, `portal_grant`
  (lines 166-195). No other key is read anywhere in the closure (a regex sweep for `contract[`/`contract.get(` over `lambda_function.py`, the admin and `data_entitlement.py`
  found only those).
- Nothing in the closure calls `get_config`, `authorized_tenants`, `tenant_authorized`, `Config(`, `validate(`, `classify`, `decide`, `tool_denial`, `visible_tools`,
  `allowed_tools`, `NATIVE_TOOLS`, `INDEX_TOOLS`, `INTEGRATION_TOOLS` or `TOOL_CLASSES`. Searched in `lambda_function.py`, `access_state.py`, `data_entitlement.py`, `ops/schwab_entitlement_admin.py`
  and `context.py` (the only hits are the definitions inside `context.py` and `data_entitlement.py` themselves).

## 3. `app/config.py` -- deployed blob b3a9609fad -> staged blob 864536c8bb

```diff
diff --git a/b3a9609fad b/864536c8bb
index b3a9609fad..864536c8bb 100644
--- a/b3a9609fad
+++ b/864536c8bb
@@ -220,6 +220,30 @@ class Config:
     # coarse label 'ms'. Derive vs ms-ingest-liveness are told apart by endpoint, not by this label.
     MS_INGEST_BEARER_LABELS: str = os.environ.get("MS_INGEST_BEARER_LABELS", "")
     MS_INGEST_IDENTITY: str = os.environ.get("MS_INGEST_IDENTITY", "")
+    # --- NFRA_OPLGTW OG-hr-1 (PRD v1.3 C7): the headless meeting-transcript routes under /hx/transcripts
+    # (app/transcript_route.py). Their OWN static capability bearer (whitespace/comma list; accepted ONLY on that
+    # prefix -- the /ms/* bearer is refused there and this one is refused on /ms/*), labels positionally aligned
+    # (misaligned/absent -> "transcripts"), and the meeting-id allowlist. EMPTY allowlist = every meeting refused.
+    # The routes read with the SAME fixed identity as /ms/* (MS_INGEST_IDENTITY). Unset bearer => unconfigured (503).
+    TRANSCRIPT_BEARER: str = os.environ.get("TRANSCRIPT_BEARER", "")
+    TRANSCRIPT_BEARER_LABELS: str = os.environ.get("TRANSCRIPT_BEARER_LABELS", "")
+    TRANSCRIPT_MEETING_ALLOWLIST: str = os.environ.get("TRANSCRIPT_MEETING_ALLOWLIST", "")
+    # --- NFRA_OPLGTW OG-hr-2 (PRD v1.3 C7): the headless mail routes under /hx/mail (app/mail_route.py). Their OWN
+    # static capability bearer (accepted ONLY on that prefix; the transcripts and /ms/* bearers are refused there),
+    # labels positionally aligned (misaligned/absent -> "msgpull"), the SENDER TABLE (whitespace/comma list of sender
+    # addresses; EMPTY = every message refused; values arrive at OG-rl-1, none is committed) and the PDF byte cap.
+    # Same fixed identity as /ms/* (MS_INGEST_IDENTITY). Unset bearer => unconfigured (503).
+    MAIL_BEARER: str = os.environ.get("MAIL_BEARER", "")
+    MAIL_BEARER_LABELS: str = os.environ.get("MAIL_BEARER_LABELS", "")
+    MAIL_SENDER_TABLE: str = os.environ.get("MAIL_SENDER_TABLE", "")
+    MAIL_PDF_MAX_BYTES: str = os.environ.get("MAIL_PDF_MAX_BYTES", "")
+    # --- Andrew's Teams assistant (Andrew-direct 2026-10-02): the headless Teams routes under /hx/teams
+    # (app/teams_route.py). Their OWN static capability bearer (whitespace/comma list; accepted ONLY on that prefix,
+    # and refused while its value is also another route's bearer), labels positionally aligned (misaligned/absent ->
+    # "teamsassist"). The value lives in Secrets Manager as gateway/teams/bearer. Same fixed identity as /ms/*
+    # (MS_INGEST_IDENTITY). Unset bearer => unconfigured (503).
+    TEAMS_BEARER: str = os.environ.get("TEAMS_BEARER", "")
+    TEAMS_BEARER_LABELS: str = os.environ.get("TEAMS_BEARER_LABELS", "")
 
     # --- Estate-graph READ capability path (NFRA_CLDGRPH CG-s-5; mirrors the MS_INGEST/OTP
     # Option-A static-capability-bearer). /graph/cypher + /graph/health proxy ONE read-only Cypher
```

**Changed symbols:** nine new class attributes on `Config`: `TRANSCRIPT_BEARER`, `TRANSCRIPT_BEARER_LABELS`, `TRANSCRIPT_MEETING_ALLOWLIST`, `MAIL_BEARER`, `MAIL_BEARER_LABELS`,
`MAIL_SENDER_TABLE`, `MAIL_PDF_MAX_BYTES`, `TEAMS_BEARER`, `TEAMS_BEARER_LABELS`. Each is `os.environ.get(NAME, "")` with a string default. Nothing else in the file moved (no
`_req`, no `validate()` change, no int/float parse).

**Trace to the grant writer:**
- `config.py` enters the closure through `app/context.py` line 18, `from .config import get_config`, which `ops.schwab_entitlement_admin` imports (line 52) for
  `context.make_principal`. Importing `app.config` runs the class body once (the new `os.environ.get(..., "")` calls) and `load_dotenv()`; it instantiates nothing.
- The only function in the closure that calls `get_config()` is `context.authorized_tenants()` (line 60), reached only through `tenant_authorized()`. The grant writer calls neither
  (it calls `make_principal`, which uses `canonical_guid` only).
- Therefore `Config()` is never constructed by the grant writer, `validate()` is never called, and the nine attributes are never read.

**Behaviour change for the grant writer: NONE.**
- Admits/refuses differently: no grant.
- **Config keys it now needs: NONE new.** The nine names are optional with an empty default and are read by the gateway's `/hx/transcripts`, `/hx/mail`, `/hx/teams` routes
  (`app/transcript_route.py`, `mail_route.py`, `teams_route.py`), not by the grant writer. The function's environment stays at the three keys it has (`MCPORTAL_CHANGES_TABLE`,
  `MCPORTAL_OWNER_KEY`, `MCPORTAL_OWNER_KEY_CLAIM`; before-record `GW2_ENV_BEFORE.json`, 3 keys); the plan leaves `environment` unchanged.
- An import-time failure is not introduced: no new attribute parses its value, so no env content can raise at import.
- Measured: both closures were imported and the class inspected (section 6): deployed `Config` has no `MAIL_BEARER`/`TEAMS_BEARER`; staged has both; `import lambda_function` succeeds on both.

## 4. `app/data_entitlement.py` -- deployed blob e5db4d307d -> staged blob c25f71c7ba

```diff
diff --git a/e5db4d307d b/c25f71c7ba
index e5db4d307d..c25f71c7ba 100644
--- a/e5db4d307d
+++ b/c25f71c7ba
@@ -93,13 +93,15 @@ SCHWAB_TOOLS = {
 # Every tool the Gateway registered at OG-z-1's cut (7f1ab996a0): the 35 native tools of app/tools.py and the 9
 # tools of the three buildable integrations. They keep their existing gates for principals without a profile.
 NATIVE_TOOLS = frozenset({
-    "whoami", "list_recent_email", "search_email", "read_email", "list_email_attachments",
-    "save_email_attachment_to_site", "create_draft", "send_email", "reply_email", "list_calendar", "list_onedrive",
+    "whoami", "list_recent_email", "list_email_filtered", "search_email", "read_email", "list_email_attachments",
+    "inspect_email_attachment", "save_email_attachment_to_site", "create_draft", "send_email", "reply_email",
+    "list_calendar", "list_onedrive",
     "search_files", "read_file", "find_sharepoint_site", "list_site_files", "read_site_file", "profile_site_file",
     "validate_ssavail_attachment", "upload_text_to_site", "read_site_workbook", "read_workbook", "search_site_files",
     "get_item", "get_site_item", "list_site_drives", "read_document", "list_chats", "read_teams_attachment",
     "read_chat_messages", "read_chat_message_images", "send_chat_message", "list_teams", "list_channels",
     "read_channel_messages", "send_channel_message", "poll_addressed_teams_messages", "opal_asker_query",  # OA-t-5
+    "find_online_meeting", "list_meeting_transcripts", "read_meeting_transcript",   # OG-tx-1 (PRD C7), read class
 })
 INTEGRATION_TOOLS = frozenset({
     "ycharts_freshness", "ycharts_snapshot_metrics", "ycharts_time_series", "ycharts_fund_series",
@@ -112,9 +114,10 @@ INTEGRATION_TOOLS = frozenset({
 # gates, and a restricted (Schwab-grant) principal is denied them exactly as it is every other non-Schwab tool.
 INDEX_TOOLS = frozenset({
     "mdpf_get_aum_metrics", "mdpf_get_account_distribution", "mdpf_get_aggregate_aua",   # portal_index
-    "mdpf_get_model_benchmarks",                              # portal_index, NFRA_MCPINDEX MX-t-9 (row Z-W15-S2)
+    "mdpf_get_model_benchmarks", "etfs_get_positioning",      # portal_index, NFRA_MCPINDEX MX-t-9 / MX-t-10 (row Z-W15-S2)
     "gateway_query_catalog",                                  # portal_index, NFRA_MCPINDEX MX-q-3 (query_v0 as a tool)
     "opal_discover", "opal_describe",                         # opal_discover
+    "blackdiamond_list_fees",                                 # blackdiamond, NFRA_MCPINDEX MX-t-13 (round 5), DORMANT
 })
 CLASS_LEGACY = "legacy"
 CLASS_SCHWAB = "schwab"
```

**Changed symbols (all three are module constants; no function body, parser or enum moved):**
- `NATIVE_TOOLS` +5: `list_email_filtered`, `inspect_email_attachment`, `find_online_meeting`, `list_meeting_transcripts`, `read_meeting_transcript`.
- `INDEX_TOOLS` +2: `etfs_get_positioning`, `blackdiamond_list_fees`.
- `TOOL_CLASSES` (derived, line 124 `{... for t in NATIVE_TOOLS | INTEGRATION_TOOLS | INDEX_TOOLS}`) therefore gains 7 `CLASS_LEGACY` entries.
- NOT changed (checked in the diff; the two hunks above are the whole change): `DATASETS` (already `dim_position, dim_balance, dim_asset, dim_transaction` in the DEPLOYED blob),
  `MASTERS`, `OPERATIONS`, `DISABLED_OPERATIONS`, `GRANT_DATE_MODES`, `SCOPE_DIMENSIONS`, `SCHWAB_TOOLS`, `parse_scope`, `parse_profile`, `parse_grant`, `_strings`, every `*_item`/`*_op` builder.

**Trace to the grant writer:** the writer's uses of `de` are the list in section 2 -- `parse_scope`, `parse_profile`, `parse_grant`, the key/item/op builders and four constants. None of them reads
`NATIVE_TOOLS`, `INDEX_TOOLS` or `TOOL_CLASSES`. Those three feed only `classify()`, `decide()`, `tool_denial()`, `visible_tools()`, `route_denial()` (gateway request-time tool gating in
the same module), which nothing in the closure calls.

**Behaviour change for the grant writer: NONE.**
- A candidate the writer admitted or refused before, it admits or refuses identically after (the parse path, the dataset list, the operation list and the scope shape are byte-identical).
  Existing grants and profiles parse identically.
- Config keys needed: none.
- What the change DOES decide, and where (outside this Lambda): the 7 tools become `legacy`-classified at the gateway, so the gateway stops answering `tool_unclassified` ("denied to every
  principal until it is classified") for them. The gateway on the released ref already carries the same constants (this is af2d762970's own file), so redeploying the writer brings the writer's
  copy of the module level with the gateway's. A restricted (Schwab-grant) principal is still denied every non-Schwab tool by `decide()` (`access.restricted` -> only `access.tools`), the 7 included.
  So no grant gains or loses a tool through this diff.

## 5. `org/standards/NFRA_OPLGTW_CONTRACT.json` -- deployed blob 848ec665d8 -> staged blob 2d9181f8bc

```diff
diff --git a/848ec665d8 b/2d9181f8bc
index 848ec665d8..2d9181f8bc 100644
--- a/848ec665d8
+++ b/2d9181f8bc
@@ -10,7 +10,8 @@
   "datasets": [
     "dim_position",
     "dim_balance",
-    "dim_asset"
+    "dim_asset",
+    "dim_transaction"
   ],
   "operations": [
     "list",
@@ -184,6 +185,23 @@
       "maturity_date",
       "prod_code",
       "prodcatg_code"
+    ],
+    "dim_transaction": [
+      "account_ref",
+      "business_date",
+      "trade_date",
+      "settlmnt_date",
+      "tr_cd",
+      "sb_cd",
+      "transaction_category",
+      "tran_srcde",
+      "debit_credit",
+      "cusip",
+      "ticker_symbol",
+      "quantity",
+      "price",
+      "gross_amount",
+      "net_amount"
     ]
   },
   "additive_fields": {
@@ -203,7 +221,8 @@
       "bank_sweep_ibf",
       "bank_cash"
     ],
-    "dim_asset": []
+    "dim_asset": [],
+    "dim_transaction": []
   },
   "quantity_sum_required_groups": [
     "cusip",
```

**Changed keys:** `datasets` +`dim_transaction`; `fields.dim_transaction` (new, 15 columns: `account_ref, business_date, trade_date, settlmnt_date, tr_cd, sb_cd, transaction_category,
tran_srcde, debit_credit, cusip, ticker_symbol, quantity, price, gross_amount, net_amount`); `additive_fields.dim_transaction` = `[]`.

**Trace to the grant writer:** of those three, only `fields` is read (`validate_candidate`, line 166: `fields_catalog = contract.get("fields", {})`; per dataset
`approved = set(fields_catalog.get(dataset, ()))`, any requested column outside it -> `CandidateRejected`, a subclass of `AdminRefused`, so the Lambda returns `REFUSED` /
`ADMIN-REFUSED`). `datasets` and `additive_fields` are not read by the writer (the writer's dataset check is `de.DATASETS`, line 259, which already held `dim_transaction`).
None of the 15 columns is in `forbidden_field_classes` (`raw_account_id, account_title, tax_identifier, mailing_address, hidden_filter_operand, hidden_group_operand,
hidden_sort_operand`): checked, 0 of 15.

**THE ONE BEHAVIOUR CHANGE (a widening): `narrow` / `widen` candidates naming the `dim_transaction` dataset go from always REFUSED to ADMITTED.**
- Before: `de.parse_scope` already accepted `dim_transaction` as a dataset (DATASETS unchanged), and requires its `columns` to be a non-empty list; the deployed contract has no
  `fields.dim_transaction`, so EVERY column is "unapproved" and EVERY such candidate is refused with `scope.columns[dim_transaction] names unapproved field(s) [...]`.
  No dim_transaction grant could be written by this Lambda.
- After: a candidate whose `scope.columns.dim_transaction` is a non-empty subset of the 15 listed columns passes `validate_candidate`; then `admin.prepare` / `admin.activate` write the
  grant and profile records. A column outside the 15 is still refused (a control below). Other datasets (`dim_position`, `dim_balance`, `dim_asset`) are unchanged: their `fields`
  blocks are untouched in the diff.
- It is a grant-admission change in the CVO's sense: `data_entitlement` and the contract decide whom grants admit, and after the apply the owner can write a restricted principal a grant
  that reaches transaction rows (including `cusip`, `ticker_symbol`, `quantity`, `price`, `gross_amount`, `net_amount`, `account_ref`). The writer still requires the verified owner
  (`NOT_OWNER` otherwise), the masters stay `08242234`/`08335338`, accounts stay per-master explicit, operations stay `list/describe/query/download_filtered`. Whether the READ side serves
  `dim_transaction` is the gateway's affair (the gateway on af2d762970 already holds this contract); this order does not exercise it.
- Revoke is unaffected (it reads no contract key). Existing grants are unaffected (no record is rewritten by the apply).
- Config keys needed: none.

## 6. Measured, in-process, no store and no grant (probe `grant_writer_probe.py.txt`, in this folder (a text copy: ruff gates .py files))

`ops.schwab_entitlement_admin.validate_candidate` (pure; `catalog_channels` passed explicitly, no AWS call, synthetic GUIDs `1111...`/`2222...`, master `08242234`) run against each
closure: the DEPLOYED one is the deployed zip extracted; the STAGED one is the build from af2d762970. Output verbatim:

```
### DEPLOYED closure (deployed zip extracted)
closure c12839d856ec admin.CandidateRejected subclass of AdminRefused: True
Config attrs MAIL_BEARER present: False TEAMS_BEARER present: False
  dim_position/account_ref             ADMITTED
  dim_transaction/cusip                REFUSED: scope.columns[dim_transaction] names unapproved field(s) ['cusip'] (not in the contract's field catalog)
  dim_transaction/15 listed cols       REFUSED: scope.columns[dim_transaction] names unapproved field(s) ['account_ref', 'business_date', 'cusip', 'debit_cred
  dim_transaction/gross_amount+bogus   REFUSED: scope.columns[dim_transaction] names unapproved field(s) ['bogus_col', 'gross_amount'] (not in the contract's 
contract fields.dim_transaction columns: 0 | account_ref in dim_position fields: True

### STAGED closure (build_package.py from af2d762970)
closure a9eafa664374 admin.CandidateRejected subclass of AdminRefused: True
Config attrs MAIL_BEARER present: True TEAMS_BEARER present: True
  dim_position/account_ref             ADMITTED
  dim_transaction/cusip                ADMITTED
  dim_transaction/15 listed cols       ADMITTED
  dim_transaction/gross_amount+bogus   REFUSED: scope.columns[dim_transaction] names unapproved field(s) ['bogus_col'] (not in the contract's field catalog)
contract fields.dim_transaction columns: 15 | account_ref in dim_position fields: True
```

Reading: the `dim_position/account_ref` control is ADMITTED on both (nothing else moved); the three `dim_transaction` rows flip REFUSED -> ADMITTED exactly where the columns are in the
15-column catalog, and `bogus_col` stays REFUSED on the staged side.

## 7. Summary for the CVO

| changed file | changed symbol(s) | grant-writer call site | admits/refuses differently? | config keys now required |
|---|---|---|---|---|
| `app/config.py` | 9 new `Config` attrs (TRANSCRIPT_*, MAIL_*, TEAMS_*) | none: reached only via `context` import; `get_config()` not called by the writer | no | none |
| `app/data_entitlement.py` | `NATIVE_TOOLS` +5, `INDEX_TOOLS` +2, `TOOL_CLASSES` +7 | none: only `classify/decide/tool_denial/visible_tools` read them; the writer uses `parse_*` and the item/op builders | no | none |
| `NFRA_OPLGTW_CONTRACT.json` | `fields.dim_transaction` (15 cols), `datasets`, `additive_fields` | `admin.validate_candidate` reads `fields` | **yes: a `dim_transaction` grant is admitted (was refused)**; `datasets`/`additive_fields` unread | none |

Net: ONE admission change (dim_transaction grants, via the contract's `fields`), zero new required keys, no change to the function's environment, role, layer or any other resource.
The grant writer's own `lambda_function.py` is byte-identical to the deployed one (SAME in section 1).
