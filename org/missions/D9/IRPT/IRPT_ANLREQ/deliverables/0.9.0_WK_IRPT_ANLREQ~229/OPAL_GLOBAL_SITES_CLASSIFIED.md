# OPAL_GLOBAL equality sites under infra/aws/lambda -- classified (AR-tz-65, round 50, workstream ~TX)

**Worker:** `0.9.0_WK_IRPT_ANLREQ~229` on `wk-IRPT_ANLREQ-229`, read at HEAD `927be44c0a`. READ cell: no source file was edited.
**Enumeration:** native Grep for the literal `OPAL_GLOBAL` under `infra/aws/lambda`, excluding every `tests/` folder (`ops/tests` included), keeping the lines where `==`, `!=`, `in (...)` or `not in` sits on the same line; every hit read in its function. Verdict key: `ADMITS` = the site lets an OPAL_GLOBAL principal read or write a record without comparing the principal's firm to the record's firm first (a global admission); `REFUSES-TESTED` = refuses OPAL_GLOBAL and a test names the refusal; `NOT-APPLICABLE` = anything else, reason in the evidence cell.

| surface | path:line | verdict | evidence |
|---|---|---|---|
| `_ViewerInput.__init__`: owner shape gate before the authorizer callback | `infra/aws/lambda/investor-reporting/_scope/maintained_sources.py:163` | NOT-APPLICABLE | `owner.get("principal_class") not in ("OPAL_GLOBAL", "FIRM_ADVISOR", "FIRM_OPERATIONS")` -- constructor shape refusal; the access decision is the caller's authorizer callback at line 187 |
| `_ViewerInput.__init__`: an OPAL_GLOBAL owner must carry home_firm_id | `infra/aws/lambda/investor-reporting/_scope/maintained_sources.py:165` | NOT-APPLICABLE | `(owner.get("principal_class") == "OPAL_GLOBAL"` -- refuses an OPAL_GLOBAL owner without a home firm; no admission |
| `_ViewerInput.__init__`: viewer shape gate | `infra/aws/lambda/investor-reporting/_scope/maintained_sources.py:175` | NOT-APPLICABLE | `self.viewer.get("principal_class") not in ("OPAL_GLOBAL", "FIRM_ADVISOR", "FIRM_OPERATIONS")` -- refuses a viewer whose class is outside the three; no admission |
| `_owner_binding`: binding dict for an owner | `infra/aws/lambda/investor-reporting/_scope/maintained_sources.py:205` | NOT-APPLICABLE | `if owner.get("principal_class") == "OPAL_GLOBAL":` -- adds home_firm_id to the binding (attribution metadata) |
| `_snapshot_viewer_profile.read`: profile source choice | `infra/aws/lambda/investor-reporting/_scope/maintained_sources.py:238` | NOT-APPLICABLE | `if actor["principal_class"] == "OPAL_GLOBAL":` -- an OPAL_GLOBAL viewer's profile is read from its home organization instead of the firm and partner readers; a source choice, no record admitted |
| `snapshot_custody_profile_sources`: custody owner precondition | `infra/aws/lambda/investor-reporting/_scope/maintained_sources.py:334` | NOT-APPLICABLE | `owner.get("principal_class") != "OPAL_GLOBAL"` -- requires an OPAL_GLOBAL custody owner; the principal firm and id comparison is in its authorize (lines 343-346) |
| `authorize_current`: interactive viewer rule | `infra/aws/lambda/investor-reporting/_scope/interactive_access.py:115` | ADMITS | `if current["principal_class"] == "OPAL_GLOBAL":` -- returns True before any firm comparison; this is register row G1 |
| `prospect_owner`: create-input firm check | `infra/aws/lambda/investor-reporting/_scope/interactive_access.py:131` | ADMITS | `if actor["principal_class"] != "OPAL_GLOBAL" and firm != actor["firm_id"]:` -- an OPAL_GLOBAL actor may create input attributed to any storage firm; a write without firm comparison; NOT a register row (G1 names authorize_current, a view) |
| `prospect_owner`: home_firm_id attribution | `infra/aws/lambda/investor-reporting/_scope/interactive_access.py:137` | NOT-APPLICABLE | `if owner.get("principal_class") != "OPAL_GLOBAL":` -- drops home_firm_id from a non-OPAL owner (schema attribution) |
| `resolve_for_request`: Opal firm selection | `infra/aws/lambda/investor-reporting/_scope/global.py:180` | ADMITS | `if principal_class == "OPAL_GLOBAL":` -- an OPAL_GLOBAL principal selects any permitted firm; no principal firm exists to compare, and the binding check (line 219) compares only the binding to the selected firm; NOT a register row |
| `resolve_for_request`: catalogue input | `infra/aws/lambda/investor-reporting/_scope/global.py:256` | NOT-APPLICABLE | `if principal_class == "OPAL_GLOBAL" else None))` -- passes the permitted-firm catalogue to the resolver for an Opal principal only (selector input) |
| `resolve_for_request`: census flag | `infra/aws/lambda/investor-reporting/_scope/global.py:261` | NOT-APPLICABLE | `census["selection_honoured"] = (principal_class == "OPAL_GLOBAL")` -- a census flag written to the log scope |
| `current_selection`: custody ports selection check | `infra/aws/lambda/investor-reporting/_scope/custody_ports.py:106` | NOT-APPLICABLE | `if not isinstance(scope, dict) or scope.get("principal_class") != "OPAL_GLOBAL":` -- refuses a non-OPAL scope; firm equality against the owner is at line 110 |
| `validate_owner`: custody owner record shape | `infra/aws/lambda/investor-reporting/_scope/custody_binding.py:67` | NOT-APPLICABLE | `or owner["principal_class"] != "OPAL_GLOBAL"` -- owner record shape (OPAL_GLOBAL, home opal-capital); refusal of a malformed record |
| `_current_selection_owner`: custody owner build | `infra/aws/lambda/investor-reporting/_scope/custody.py:76` | NOT-APPLICABLE | `if refusal is not None or scope.get("principal_class") != "OPAL_GLOBAL":` -- refuses a non-OPAL scope before building the owner; the decision is resolve_now at line 75 |
| `guard_owner_read.retained`: retained-record owner check | `infra/aws/lambda/investor-reporting/_scope/owner_reads.py:29` | ADMITS | `principal.get("principal_class") != "OPAL_GLOBAL"` -- for OPAL_GLOBAL the owner firm and principal id comparison (lines 30-31) is skipped; only authorize_record_owner (line 32) remains; NOT a register row |
| `resolve` (_scope), UNKNOWN branch: is_global argument | `infra/aws/lambda/investor-reporting/_scope/resolve.py:438` | NOT-APPLICABLE | `principal_class == "OPAL_GLOBAL")` -- is_global only gates the permitted-firm catalogue in _build (line 569) |
| `resolve` (_scope): firm population for Opal and firm operations | `infra/aws/lambda/investor-reporting/_scope/resolve.py:445` | ADMITS | `if principal_class in ("FIRM_OPERATIONS", "OPAL_GLOBAL"):` -- an OPAL_GLOBAL principal is granted the whole population of the firm handed in (firm_id, bound by the caller); no principal firm is compared; NOT a register row |
| `resolve` (_scope): return of the scope | `infra/aws/lambda/investor-reporting/_scope/resolve.py:550` | NOT-APPLICABLE | `principal_class == "OPAL_GLOBAL")` -- is_global argument to _build, catalogue display only |
| `resolve` (holdings copy), UNKNOWN branch | `infra/aws/lambda/investor-reporting/holdings/resolve.py:438` | NOT-APPLICABLE | `principal_class == "OPAL_GLOBAL")` -- same is_global catalogue flag as _scope/resolve.py:438 |
| `resolve` (holdings copy): firm population | `infra/aws/lambda/investor-reporting/holdings/resolve.py:445` | ADMITS | `if principal_class in ("FIRM_OPERATIONS", "OPAL_GLOBAL"):` -- same admission as _scope/resolve.py:445 in the holdings copy; NOT a register row |
| `resolve` (holdings copy): return | `infra/aws/lambda/investor-reporting/holdings/resolve.py:550` | NOT-APPLICABLE | `principal_class == "OPAL_GLOBAL")` -- is_global catalogue flag, as _scope/resolve.py:550 |
| `compose_frozen_request`: Opal branch flag | `infra/aws/lambda/investor-reporting/ycharts/generate/submission.py:132` | NOT-APPLICABLE | `opal = owner.get("principal_class") == "OPAL_GLOBAL"` -- selects the Opal-specific checks; they refuse with EXACT_PROSPECT_OWNER_REQUIRED at line 145 and admit nothing |
| `_descriptor`: recipe configuration binding | `infra/aws/lambda/investor-reporting/ycharts/generate/recipe_snapshot.py:69` | NOT-APPLICABLE | `if owner["principal_class"] == "OPAL_GLOBAL":` -- binding attribution; refuses only when home_firm_id is missing (line 71) |
| `validate_bindings`: frozen owner binding | `infra/aws/lambda/investor-reporting/reports/request_composition.py:40` | NOT-APPLICABLE | `if owner["principal_class"] == "OPAL_GLOBAL":` -- binding and shape validation of an already-resolved owner; ownership was decided upstream |
| `validate_bindings`: input binding | `infra/aws/lambda/investor-reporting/reports/request_composition.py:86` | NOT-APPLICABLE | `if input_owner["principal_class"] == "OPAL_GLOBAL":` -- adds home_firm_id to the input binding (attribution) |
| `validate_bindings`: home attribution of profile fields | `infra/aws/lambda/investor-reporting/reports/request_composition.py:133` | NOT-APPLICABLE | `if owner["principal_class"] == "OPAL_GLOBAL" and key in ("prepared_by", "organization"):` -- refuses CUSTODY_ACTOR_HOME_ATTRIBUTION (line 136) when the source firm differs from the home firm |
| `RetentionPolicy._allow`: retention owner access | `infra/aws/lambda/investor-reporting/reports/retention.py:105` | ADMITS | `principal.get("principal_class") != "OPAL_GLOBAL")` -- an OPAL_GLOBAL principal skips the firm comparison; only self.authorize (line 106) remains; NOT a register row |
| `ReportRepository._allow`: report access | `infra/aws/lambda/investor-reporting/reports/repository.py:181` | ADMITS | `principal.get("principal_class") != "OPAL_GLOBAL")` -- an OPAL_GLOBAL principal skips the firm comparison; only self.authorize (line 182) remains; NOT a register row |
| `ArtifactRepository._allow`: artifact access | `infra/aws/lambda/investor-reporting/reports/repository.py:386` | ADMITS | `principal.get("principal_class") != "OPAL_GLOBAL")` -- same pattern; only self.authorize (line 387) remains; NOT a register row |
| `make_authorize.authorize`: resident read rule | `infra/aws/lambda/investor-reporting/reports/resident_installed.py:260` | ADMITS | `if principal.get("principal_class") == "OPAL_GLOBAL":` -- returns True for any owner's record; this is register row G2 |
| `make_principal_for.principal_for`: accepted actor class | `infra/aws/lambda/investor-reporting/reports/resident_installed.py:283` | NOT-APPLICABLE | `global_actor = evidence["scope"] == "OPAL_GLOBAL"` -- derives the principal class from the decided scope; the admission it feeds is row 31 (line 260, G2) |
| `custody_report_persist`: persister class | `infra/aws/lambda/investor-reporting/export/custody_persist.py:152` | NOT-APPLICABLE | `if principal.get("principal_class") != "OPAL_GLOBAL":` -- refuses every non-Opal persister (CustodyPersistNotOpal); narrows, admits nothing |
| `_validated`: custody input owner shape | `infra/aws/lambda/investor-reporting/intake/custody_portfolio.py:151` | NOT-APPLICABLE | `owner["principal_class"] == "OPAL_GLOBAL"` -- owner record shape check (custody-owner-v1, home opal-capital) |
| `upload_csv`: OPAL_GLOBAL owner without an interactive viewer port | `infra/aws/lambda/investor-reporting/intake/upload_entry.py:56` | REFUSES-TESTED | `elif owner.get("principal_class") == "OPAL_GLOBAL":` -- raises NotImplementedError INTERACTIVE_VIEWER_PORT_REQUIRED at line 57; asserted by `infra/aws/lambda/investor-reporting/ops/tests/test_opal_consumers.py:172-173` (cited for the test, not a row) |
| `_internal_for_allowed_firm`: on-behalf create | `infra/aws/lambda/investor-reporting/intake/uploads.py:341` | NOT-APPLICABLE | `if (principal.get("principal_class") != "OPAL_GLOBAL"` -- the on-behalf admission needs the owner firm inside the actor's allowedFirmIds (line 349), a firm comparison made first |
| `freeze_parsed_portfolio`: lane branch | `infra/aws/lambda/investor-reporting/intake/portfolio.py:195` | NOT-APPLICABLE | `opal = owner.get("principal_class") == "OPAL_GLOBAL"` -- selects the prospect and custody branches; the prospect branch refuses at line 204 |
| `freeze_template_portfolio`: owner shape | `infra/aws/lambda/investor-reporting/intake/portfolio.py:439` | NOT-APPLICABLE | `opal = owner.get("principal_class") == "OPAL_GLOBAL"` -- refuses an Opal owner with an advisor id or no home firm (line 441) |
| `Enforcer._resolve_render_delegate`: delegator roster | `infra/aws/lambda/investor-reporting/_authz/enforce.py:572` | NOT-APPLICABLE | `roster = (frozenset([delegator]) if delegator_class == "OPAL_GLOBAL"` -- builds the Opal roster for the delegator's own resolve; the admission it enables is row 18 (resolve.py:445), bound to the tenant directory |
| `Enforcer.covers`: advisor branch | `infra/aws/lambda/investor-reporting/_authz/enforce.py:790` | NOT-APPLICABLE | `if scope["principal_class"] in ("FIRM_OPERATIONS", "OPAL_GLOBAL"):` -- reached only after the verified-firm ownership-map membership test (lines 781-788) for every class; widens to any advisor of that firm |

DENOMINATOR: 40 sites (23 with ==, 14 with != or not in, 3 with in), from the native Grep described above; read in full. Not counted as comparisons: docstrings and comments, dict literals and mint returns (interactive_access.py:88, custody.py:35, resident_installed.py:285, resolve.py:282), constants and data files (grant.py:43, resolve.py:150, templates.json, ResolvedScope.schema.json), and the mint assignment at ycharts/generate/current_authority.py:130, which keys OPAL_GLOBAL on firmId and userType rather than comparing a principal class.

## Counts by verdict

- ADMITS: 10 (rows 7, 8, 10, 16, 18, 21, 28, 29, 30, 31)
- REFUSES-TESTED: 1 (row 35)
- NOT-APPLICABLE: 29
- REFUSES-UNTESTED, SURFACES-ON-TICKET, SILENT, UNREAD: 0

## ADMITS sites not in the register

Register rows G1 (interactive_access.py:115) and G2 (resident_installed.py:260) are covered. The other 8 ADMITS sites are not named in `R19_GLOBAL_ADMISSIONS_REGISTER.md`:

- `_scope/interactive_access.py:131` (prospect_owner, a create-in-any-firm write; G1 names only the view)
- `_scope/global.py:180` (resolve_for_request, Opal firm selection)
- `_scope/owner_reads.py:29` (guard_owner_read)
- `_scope/resolve.py:445` (firm population for an OPAL_GLOBAL principal)
- `holdings/resolve.py:445` (the same admission in the holdings copy)
- `reports/retention.py:105` (RetentionPolicy._allow)
- `reports/repository.py:181` (ReportRepository._allow)
- `reports/repository.py:386` (ArtifactRepository._allow)

Rows 16, 28, 29 and 30 defer the final decision to a caller callback; the callback may be G1 or G2, but the exemption at each site is not named in the register. These are findings for `2.0.0_SA_COO~V2`, not fixes made here.

## Other notes

- The cell premise cites 21 sites in 12 non-test files for the round-47 test. At HEAD `927be44c0a` the exact `== "OPAL_GLOBAL"` form counts 23 sites in 13 files (this record's `==` rows; the resident evidence comparison at row 32 is included), and all comparison forms count 40 sites in 21 files. Filed as a surprise row.
- G3 (ticket_center `_profile_scope`) does not use the OPAL_GLOBAL literal and sits outside this enumeration.
