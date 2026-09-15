# NFRA_OPLGTW.TO-OG-z-1 -- the persistent policy model and its guard -- result

Worker `0.9.0_WK_NFRA_OPLGTW~3`, worktree `/c/tmp/wk-oplgtw-1-3e`, branch `wk-nfra_oplgtw-1-3e`, cut from `CLOUD` at
`7f1ab996a0` (OG-a-3 merged). Code commit `d88cd32d0c` (LOCAL). Nothing deployed, pushed, merged or rebased.

## Premises re-grounded at 7f1ab996a0

| order's premise (certified L4 rectangle @5dd24300f7) | live read | holds |
|---|---|---|
| 35 native `@mcp.tool` functions in tools.py call `_run` | 35 registered on `app.tools.mcp` (list below); each body returns `_run(...)` | yes |
| identity_scope restricts only identities in its map; unlisted pass through | `identity_scope.check` returns None for an unmapped email (identity_scope.py :88-103) | yes |
| entitlements.py is tier-to-write-class only; no master/dataset/account/date/column policy | entitlements.py :63-77 | yes |
| global native/integration registration, no `list_tools` implementation, no per-principal discovery filter | FastMCP's own `list_tools` (mcp 1.28.0 fastmcp/server.py :315-330); `registry.register_enabled` onto the shared `mcp` | yes |
| /teams/poll and /query/v0 validate a bearer and the blocklist, then bypass both tool chokepoints | server.py :493-549 (the handlers call `token_broker.get_token` / `query_v0_mod.handle` directly) | yes |
| query_v0 derives opal-internal access from the opalinvest.com/.dev email domain, then reads portal JSON with default boto3 credentials | query_v0.py :64, :82-91, :94-105 | yes |
| "27 source-declared server routes" (PRD C2) | 29 declarations (Route 28, Mount 1). The PRD's 27 predates OG-a-3's two browser-OIDC routes. | the number is context; 29 is the population used |

## What was built

- `app/data_entitlement.py` (new): the model and the guard. It defines:
  - the `principal_profile` record at `POLICY#<tid>#<oid>` / `principal_profile`, with profile_kind `restricted`, a status (pending | active | revoked), a revision and a grant_revision;
  - the `data_entitlement` record at `data_entitlement#<revision, 10 digits>`, written once per revision, carrying a status and a scope of masters, datasets, accounts per master, dates (fixed_dates or rolling_complete_window), columns per dataset, and operations;
  - strict parsing, where anything malformed denies;
  - the per-dimension `check_scope` / `authorize`;
  - the tool classification table: 35 native plus 9 integration tools `legacy`, and the contract's 5 tools `schwab`;
  - the operator-side record builders, with an optimistic revision condition and write-once grant revisions.

  A revoked profile is a tombstone: the adapter refuses any POLICY delete, and a principal with any profile record is restricted.
- Enforcement, in each case before any credential fetch or data read:
  - `tools.py` `_PolicyGuardedMCP` filters discovery (`list_tools`) and guards dispatch (`call_tool`) for every tool on the served surface, including tools registered outside both chokepoints.
  - `_run`, the native chokepoint, and `integrations/base.py` `run_integration_tool`, the integration chokepoint, check first, ahead of identity_scope, tier and credential.
  - `integrations/registry.py` reports any unclassified tool it registers.
  - `server.py` checks `/teams/poll` and `/query/v0` after bearer validation and before any token fetch or catalog read.
  - `query_v0.handle` checks the profile ahead of the email-domain internality.
- The decision, per request, from a strong read of the request principal's profile and grant (never cached across requests):

  | principal | decision | code |
  |---|---|---|
  | no principal | every tool and guarded route denied | `principal_required` |
  | store unavailable or a record malformed | denied | `entitlement_unavailable` / `UNAVAILABLE` |
  | no profile | legacy tools pass on to the existing gates, unchanged; Schwab tools hidden and denied | `entitlement_denied` |
  | a profile | exactly the Schwab tools its active grant's operations allow; every other tool and both REST routes denied | `entitlement_denied` |
  | any principal, tool not classified | denied | `tool_unclassified` |

- `identity_scope.py` is not edited. The restricted profile does not depend on it, which is what OGZ1-AC12 shows.

## Tool inventory (the served MCP surface in the tests)

Denominator: **49 registered** = 35 native + 9 integration + 5 Schwab stand-ins. The five Schwab tools are not built at the cut (row W3-S23). The native and integration counts are the same as a direct offline read at 7f1ab996a0.

| class | tools | n |
|---|---|---|
| legacy / native (tools.py, via `_run`) | create_draft, find_sharepoint_site, get_item, get_site_item, list_calendar, list_channels, list_chats, list_email_attachments, list_onedrive, list_recent_email, list_site_drives, list_site_files, list_teams, poll_addressed_teams_messages, profile_site_file, read_channel_messages, read_chat_messages, read_document, read_email, read_file, read_site_file, read_site_workbook, read_teams_attachment, read_workbook, reply_email, save_email_attachment_to_site, search_email, search_files, search_site_files, send_channel_message, send_chat_message, send_email, upload_text_to_site, validate_ssavail_attachment, whoami | 35 |
| legacy / integration (via `run_integration_tool`) | ycharts_freshness, ycharts_snapshot_metrics, ycharts_time_series, ycharts_fund_series, ycharts_risk_return_scatter, ycharts_search (ycharts); opal_data_refresh_upload (opal_portal); graph_cypher, graph_status (globgrph) | 9 |
| schwab (contract `tools`, operation needed) | schwab_get_access (any active grant), schwab_list_files (list), schwab_describe_dataset (describe), schwab_query (query), schwab_prepare_download (download_filtered) | 5 |
| unclassified | none at the cut; any new tool is denied to every principal until classified (row W3-S24) | 0 |

Restricted profile, all four operations granted: 5 of 49 discoverable and callable. The other 44 are denied over MCP (44 of 44) and at the chokepoints (35 via `_run` + 9 via `run_integration_tool`), with 0 credential fetches (OGZ1-AC7). A principal with no profile sees 44 of 49, every tool except the 5 Schwab ones (OGZ1-AC6), exactly as before (OGZ1-AC11).

## Route inventory (app/server.py, 29 declarations)

The restricted profile's own gateway token was presented on every route, in OGZ1-AC8's run at d88cd32d0c. Class names are those of `tests/test_principal_cutover.py` ROUTE_CLASS, which is not edited here.

| class | routes and the restricted profile's status | n | guard |
|---|---|---|---|
| MCP | /mcp: 200. Its discovery is its 5 Schwab tools; every other tool is denied per call. | 1 | tool-level (discovery + dispatch) |
| access (non-MCP) | /teams/poll 403, /query/v0 403, `entitlement_denied` | 2 | `data_entitlement.route_denial`, before the token fetch / catalog / S3 |
| capability | /otp/fetch, /otp/health, /ms/sites, /ms/site_children, /ms/onedrive_children, /ms/search, /ms/health: 401 | 7 | their own static-bearer / capability gate; an access token never satisfies it |
| static-exchange | /otp/token, /ms/token: 401 | 2 | same |
| static | /graph/cypher, /graph/health: 401 | 2 | same |
| access-layer | /login, /sprint, /sprint/, /sprint/archive, /sprint/{day}: 401 | 5 | the ALB OIDC header; the gateway token is no identity there. The same person's ALB session is row W3-S22 (ARMED). |
| public | /health 200, /.well-known/oauth-protected-resource 200, /.well-known/oauth-authorization-server 200, /.well-known/jwks.json 200, /register 201, /authorize 400, /token 400, /callback 400, /schwab/download/login 503, /schwab/download/callback 400 | 10 | none; the bearer changes no status on 10 of 10 |

Credential or data reads during the 28 non-MCP probes: 0. The recorders covered the delegated Graph token, silent MSAL acquisition, code redemption, Graph, the Teams poll, the catalog, S3, OTP, MS ingest, graph read, the capability mint and the sprint pages.

Positive control: a principal with no profile got /teams/poll 200 and /query/v0 200, with 5 reads recorded.

## Criteria (verbatim invocations, from /c/tmp/wk-oplgtw-1-3e at d88cd32d0c)

| id | output | rc |
|---|---|---|
| OGZ1-AC1 | 1 passed in 1.86s | 0 |
| OGZ1-AC2 | 1 passed in 1.75s | 0 |
| OGZ1-AC3 | 1 passed in 1.95s | 0 |
| OGZ1-AC4 | 1 passed in 1.84s | 0 |
| OGZ1-AC5 | 1 passed in 1.88s | 0 |
| OGZ1-AC6 | 1 passed in 2.19s | 0 |
| OGZ1-AC7 | 1 passed in 2.96s | 0 |
| OGZ1-AC8 | 1 passed in 1.58s | 0 |
| OGZ1-AC9 | 1 passed in 1.88s | 0 |
| OGZ1-AC10 | 1 passed in 1.51s | 0 |
| OGZ1-AC11 | 1 passed in 2.64s | 0 |
| OGZ1-AC12 | 1 passed in 3.24s | 0 |
| OGZ1-AC13 | 11 passed in 5.97s | 0 |
| OGZ1-AC14 | VERDICT: PASS-OGZ1-AC14 | 0 |

Each criterion's printed denominator line is in the proof instance's `output_evidence`.

## Controls

- **Mutants.** In-process monkeypatches via `.scratch/og_mutants.py`, loaded with `-p og_mutants`; the committed bytes are untouched.

  | mutant | criteria run | result |
  |---|---|---|
  | `guard_off` (decide always allows) | AC4, AC7, AC11 | 3 failed, rc=1 |
  | `routes_off` (route_denial always allows) | AC8, AC9 | 2 failed, rc=1; AC8 names `['catalog:load', 'catalog:gate', 's3:query_v0']` reached |
  | `cached_read` (the profile read memoised across requests) | AC2 | 1 failed, rc=1 |

- **Determinism.** The 12 `OGZ1-AC` denominator lines of a whole-module run (12 passed, pre-commit, with the gateway tree byte-equal to d88cd32d0c) against the 12 verbatim single-test runs at d88cd32d0c: identical, 12 of 12.
- **Regression census.** Every existing Gateway module was run in its own process, 14 of 14 green:

  | module | passed | module | passed |
  |---|---|---|---|
  | test_access_state | 7 | test_ratelimit | 6 |
  | test_attachment_tools | 5 | test_schwab_audit | 7 |
  | test_browser_oidc | 7 | test_schwab_engine | 13 |
  | test_identity_scope | 6 | test_sprint_view | 8 |
  | test_jwt_cve_lock | 6 | test_ssavail_contract | 8 |
  | test_min_tier_gate | 3 | test_teams_format | 35 (+34 subtests) |
  | test_oauth_durable | 18 | test_principal_cutover | 11 |

- **Commit gate.** `OK: pre-commit gate clean for 8 of 8 file(s)`. The WARN on non-ASCII in tools.py concerns lines present at the cut base; the added lines are ASCII.

## Rows filed

| row | class, hazard | what it records |
|---|---|---|
| NFRA_OPLGTW-W3-S22 | OBSERVATION, ARMED (disarm 1.0.0_SA_CTO) | The ALB-email routes and the legacy-consent callback cannot see the tid/oid profile before a read. The same person can reach /sprint* and the /login consent through an ALB session. |
| NFRA_OPLGTW-W3-S23 | OBSERVATION, INERT | No Schwab tool is built at the cut, so the criteria run against stand-ins carrying the contract's names. The operation map is this cell's choice. |
| NFRA_OPLGTW-W3-S24 | OBSERVATION, INERT | "Denied until classified" binds every principal. Later orders that add a tool need app/data_entitlement.py in their paths. |

## Declared exclusions

- **The real Schwab tools (OG-q-2).** They must call `data_entitlement.authorize()` before filtering, projection, grouping, totals, cache lookup and export, and must register under the five classified names.
- **The operator administration command (OG-z-2).** This cell supplies the record builders it uses: `profile_put_op`, `grant_put_op`, `operator_audit_op`.
- **The keyed account_ref alias (OG-z-3).** Denial reasons here never carry raw account ids.
- **Closing the ALB-email residual.** Row W3-S22. The candidate fixes all lie outside this grant: a roster config, an ALB rule, or an email-keyed deny index.
- **Deploy, push, merge, rebase.** Forbidden by the order.
