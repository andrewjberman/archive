# Menachem's Schwab access through opal-gateway

Archetype: implementation specification
Owner: 0.7.0_AE_CloudOps
Date: 2026-09-14
State: PROPOSED; investigation complete; no access grant or deployment performed.
Revision: 2, incorporating the supplied Claude Remote MCP requirements document; [review and evidence](REQUIREMENTS_REVIEW.md).
Authority: [Andrew's verbatim request and clarifications](ANDREW_DIRECT.md).

## Recommended experience

Extend the existing **opal-gateway MCP server** with a Schwab integration and a data entitlement on Menachem's account. An Opal workspace owner adds the gateway connector once. Menachem connects with his work login, enables the connector in Claude, and asks questions or follows a download link. He needs no terminal, AWS account, access key, or local MCP installation. Team and Enterprise support organization custom connectors and individual user authentication. [Claude setup](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)

Examples:

- "What Schwab data can I access, and how current is it?"
- "Show the largest holdings in the SmartX master on the latest available date."
- "Show the BlackDiamond master separately for the same date."
- "Download that BlackDiamond result as a CSV."

Use the existing endpoint, **https://mcp.opalinvest.dev/mcp**. The gateway authenticates the caller, resolves their entitlement, executes bounded server-side queries, and returns small results with source references. File contents are data, never instructions to expand permissions. A small authenticated download page belongs to the gateway.

| Confirmed by Andrew | Design consequence |
| --- | --- |
| Opal Team or Enterprise workspace | Owner-managed remote connector; per-user work login |
| Both questions and downloads | Query tools plus browser download flow |
| Filtered CSVs initially; originals later | Original-file capability disabled in the initial profile |
| Both masters, kept separate | Every call, result, export and cache entry carries one master |
| Manage through opal-gateway and his entitlement | Extend gateway integration and authorization |
| Read-only, gradually expandable | Explicit data grants; no source writes, deletes or bucket administration |

## Observations and gaps

Read-only AWS observations were made in account **313476888478** on 2026-09-14 at 18:08-18:11 UTC. Evidence: [metadata and footer inventory](observed-metadata.json). No customer rows were loaded.

| Observation | Implication |
| --- | --- |
| Versioning enabled, AES256 encryption, all four public-access blocks enabled, bucket policy status non-public | Preserve these settings |
| SmartX master: schwab/08242234/; BlackDiamond master: schwab/08335338/ | Explicit, independent namespaces |
| Both have silver/dim_position, silver/dim_balance and silver/dim_asset Parquet datasets | Useful initial query scope |
| Latest observed partitions of those datasets: 2026-09-11 | Report business date; upload time is a separate fact |
| Latest position files: 102,421 and 105,074 rows, approximately 2.45 and 2.58 MB | Query on the server; return bounded results |
| Account schema includes ssn_tin_number and mailing details; balance dimension includes account titles | Silver/dimension files are not automatically safe to expose in full |
| Gateway OAuth discovery endpoints return 200 and advertise /mcp, S256 and /register | Discovery works; Claude application login was not exercised |
| Checked-in OAuth registration and redirect validation allow only HTTP loopback callbacks | Add Claude application's HTTPS callback support before rollout |

The gateway already has authenticated request context, read-only tiers, identity tool allowlists, audit logging and Terraform for employee/purpose-specific assumed roles. However:

- **entitlements.py** governs write classes by tier, not per-user dataset/field permissions.
- **identity_scope.py** restricts listed identities; unlisted identities pass through to other gates. Deleting a scope entry must not become the revocation mechanism.
- **tools.py::_run** eventually fetches a delegated Microsoft Graph token. Schwab tools need shared authentication and authorization without requiring unrelated mail/file permissions.
- **query_v0.py** reads cataloged JSON from opal-data-portal-v2; its internal-domain classification is too broad for this user-specific Schwab grant.
- The checked-in Tax SMA IAM module describes email + operation -> employee role -> S3. Reuse this pattern with a dedicated Schwab read role. Scoped source searches found no aws_entitlements map or STS assume_role dispatch in the gateway app. This requires implementation, not merely a new configuration row. [Live IAM readback](gateway-role-readback.json) confirms the gateway employee-role assumption policy; the proposed Menachem role does not exist under its exact proposed name.

Source references, relative to repository root: infra/aws/ec2/opal-gateway/app/{oauth_as,context,tools,entitlements,identity_scope,query_v0}.py; infra/aws/terraform/opal-gateway/taxsma_gateway_iam.tf; data/assets/scripts/silver/{schwab_schemas,schwab_projections}.py; infra/aws/terraform/opal-assets/monolith.tf.

## Architecture and authorization

~~~mermaid
flowchart LR
  U["Menachem in Claude"] --> G["Existing opal-gateway /mcp"]
  G --> A["Verified identity + current data entitlement"]
  A --> Q["Schwab query and export integration"]
  Q --> R["Menachem Schwab read role"]
  R --> S["08242234 approved silver prefixes"]
  R --> B["08335338 approved silver prefixes"]
  U --> D["Gateway download page + browser SSO"]
  D --> A
~~~

**Application entitlement:** who can use which tool, master, dataset, account, date, column and download format.

**AWS role:** a ceiling on source objects and operations. S3 IAM cannot filter rows or columns inside Parquet. The gateway remains a trusted processor of full source objects and must enforce projection and row filters before returning results or exports.

Resolve the verified work identity to an immutable principal key, preferably Entra tenant ID + object ID. Keep **menachem@opalinvest.com** as the operator-facing label. Current gateway JWT subjects and request context use email; add a verified principal binding during login and propagate it through the signed gateway token/context. Never trust a caller-supplied email or infer access from a company-domain suffix. Existing email-based clients remain compatible; new Schwab access requires the verified binding. [Microsoft claim validation](https://learn.microsoft.com/en-us/entra/identity-platform/claims-validation)

Use a versioned server-side entitlement store, checked on every request. Missing, unreadable, disabled, expired or revoked profiles deny access. Grant changes are operator actions; Claude cannot change its own entitlement. Cache keys include identity, policy revision, master, query and pinned source versions. Old results, sessions or tickets cannot bypass a changed policy.

Menachem's account has a persistent restricted profile. Both tool discovery and direct invocation enforce the same allowlist; hiding a tool is insufficient. New Schwab tools default to denied for every other identity until explicitly granted. Preserve unrelated existing user grants; this entitlement adds no mail, file-write, administrative or other AWS tools.

## Proposed first entitlement

Fields, date window and account coverage below are **recommendations**, not user-confirmed grants. The JSON is deliberately disabled with unresolved identity IDs: [proposed entitlement](menachem-entitlement.proposed.json).

| Dimension | Proposed initial value |
| --- | --- |
| Identity | Verified Menachem work identity; read-only gateway tier |
| Masters | 08242234 SmartX and 08335338 BlackDiamond |
| Datasets | Positions, balances and security reference |
| Account scope | All accounts within each selected master, subject to operator approval; support explicit subsets |
| History | Latest complete business date plus preceding 29 calendar days |
| Fields | Explicit allowlist; opaque account references; selected holdings, values and security descriptions |
| Hidden initially | Tax IDs, addresses, account titles, raw account identifiers, unlisted columns |
| Downloads | Filtered CSV by default; original-object permission separate |
| Cross-master behavior | No joins, combined exports or summed totals; separately labeled results may be compared |

Generate stable keyed account aliases from master + account ID server-side. Raw IDs may enforce account filters internally but must not appear in output, links, errors or logs unless granted. Column permissions also govern filtering, grouping and sorting, preventing probes of hidden fields.

Expand older dates, selected accounts, transactions, columns and whole-file downloads independently. Profile changes within the IAM ceiling need no new Claude setup. Adding a dataset beyond that ceiling also requires an IAM update. Keep each master as its own entitlement entry.

## Claude application login

The gateway remains Claude's OAuth issuer; Entra supplies the upstream work identity. The brief's direct-Entra Application ID URI requirements apply only if Claude is changed to discover Entra directly. No such issuer migration is required for this design.

Retain the gateway authorization server and extend its OAuth flow. Claude's hosted application uses **https://claude.ai/api/mcp/auth_callback**; Claude Code uses loopback redirects. Allow the exact hosted callback at registration and authorization, bound to the registered client and code. Retain S256 PKCE, state validation, one-use codes, token audience/issuer checks and refresh revocation. Reject arbitrary HTTPS callbacks and wildcard Claude domains. Unauthenticated MCP requests return 401 with protected-resource metadata. [Claude authentication contract](https://claude.com/docs/connectors/building/authentication)

Preserve existing Code clients and exercise both flows. The work-login leg must establish identity without requiring unrelated Microsoft mail or file-write consent. Factor authentication from Graph-token acquisition for the data integration.

DCR can remain the registration mechanism. Registration/code state currently lives in process memory: use one active instance for the pilot or add shared state before multiple workers/replicas; test reconnect after restart. Verify the deployed artifact before treating the source callback restriction as a measured production failure. Discovery alone does not prove login.

**Refresh correction:** checked-in server.py validates the incoming refresh token and mints a replacement without consuming the old token. Add atomic, durable refresh-token rotation with client/scope/resource binding, replay detection and token-family revocation. A replacement token alone is insufficient. Test concurrent refreshes, replay, restart and revoked users; return invalid_grant for unusable refresh tokens. The store must survive deploys and coordinate every worker. [OAuth refresh-token protection](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.14.2)

Accept form-urlencoded token/refresh requests and JSON registration. Validate the requested resource against the canonical MCP URL and bind it to the grant. Budget OAuth discovery, registration and initial token responses below 10 seconds, and refresh below 30 seconds; these are separate from the data-query deadline. [Claude OAuth requirements](https://claude.com/docs/connectors/building/authentication)

Use 401 plus a Bearer challenge for missing/expired authentication. Reserve 403 plus insufficient_scope for an actual OAuth scope step-up. An account entitlement denial is a terminal access-denied result; repeated sign-in cannot grant a dataset. All five Schwab tools require identity, including access/file metadata; no anonymous Schwab catalog is proposed. [Authentication error handling](https://claude.com/docs/connectors/building/lazy-authentication)

## Network and front-door contract

Use Streamable HTTP at the exact /mcp endpoint. Preserve Authorization, WWW-Authenticate, protocol/session headers and streaming responses through the ALB and any WAF/proxy. MCP and OAuth/discovery paths reach the application without the ALB's browser-cookie login gate; the gateway enforces bearer authorization. The download page uses the browser SSO path and independently checks the bound identity and current entitlement. Changes to routing and application guards must be deployed together.

[Measured at 18:43:46Z](requirements-review-evidence.json): the live internet-facing IPv4 ALB already forwards the MCP/OAuth paths under priority 10/20 rules. An unauthenticated GET /mcp returned 401 with the correct resource_metadata challenge in 93 ms, without redirect; both discovery documents returned 200 in about 110 ms. The metadata identifies the gateway as issuer. Default browser OIDC remains present. This does not exercise Claude's network or authenticated transport.

Validate public IPv4 DNS, globally routable answers, no cross-host redirect, and WAF/proxy preservation from the actual Claude connection. Where network filters apply, permit the current Anthropic outbound range, 160.79.104.0/21, on required MCP/OAuth paths; keep work-browser login/download reachability. An IP range never establishes user identity. [Network compatibility](https://claude.com/docs/connectors/building/troubleshooting), [published egress](https://platform.claude.com/docs/en/api/ip-addresses)

The measured ALB idle timeout is 60 seconds. Keep the 30-second query deadline; bound export preparation and avoid idle streaming gaps. Do not assume Claude's longer tool timeout overrides the load balancer. Verify Host/Origin behavior with Claude while retaining origin validation where applicable; clientInfo names and versions are telemetry only. [Connector testing](https://claude.com/docs/connectors/building/testing)

## Tool and query contract

| Tool | Contract |
| --- | --- |
| schwab_get_access | Accessible master labels, datasets, fields, dates, operations and entitlement revision |
| schwab_list_files | One master/dataset, bounded dates; authorized catalog IDs, dates, format, size and download types |
| schwab_describe_dataset | Authorized field names, types, units and metric definitions |
| schwab_query | One master/dataset/date; validated filters, columns, grouping, aggregation and ordering |
| schwab_prepare_download | Authorize a file or query result and issue an identity-bound download reference |

Tools accept logical identifiers, never arbitrary buckets, S3 keys, SQL, code, role ARNs or external URLs. Resolve file IDs through the authorized catalog; reject encoded traversal and unknown IDs. MCP read annotations are descriptive; code and IAM enforce permissions.

Read selected Parquet objects with a bounded local query engine, such as PyArrow plus DuckDB. No S3 Select dependency or ingestion/silver rewrite is needed. Pin VersionIds before execution. List only approved prefixes; choose complete partitions using existing producer completion semantics. Missing or inconsistent completion evidence yields "unavailable", not guessed freshness.

Each response includes master ID/label, business date, dataset, source/version references, applied scope, matched/returned row counts and truncation status. Preserve decimal precision. Do not invent a cash total by adding overlapping vendor balance fields.

Positions and balances are snapshots: aggregate within one date. Date comparisons return separate snapshots/deltas, not their sum. Requests about both masters execute independent calls and present independent results. Security-reference joins, when introduced, require the same master, compatible date and a tested unique join key.

Initial operating limits to benchmark: 30-second query deadline, 12 source objects/64 MiB per request, 500 rows and BOTH 100,000 characters/128 KiB per complete serialized MCP response, 250,000 rows/50 MiB per export. Count all content blocks, structured results and envelope; duplicated text/structured representations share the same budget. This replaces the original 256 KiB cap, which could exceed Claude's approximately 150,000-character limit. Its published tool deadline is 240 seconds; our lower query deadline still applies. [Claude runtime limits](https://claude.com/docs/connectors/building)

Reject or narrow oversized requests; never report a total calculated from only the first page. Pagination binds identity, scope, master and versions. Run queries outside the gateway event loop with bounded concurrency to protect existing tools. The five tools need no sampling, subscriptions, draft capabilities or binary-in-chat export feature.

## Downloads and revocation

Claude returns a gateway HTTPS link. Menachem opens a simple page, signs in with his work identity if needed, and clicks **Download CSV**. The gateway rechecks the entitlement and streams the authorized projection. A five-minute opaque ticket identifies the export and requires the matching browser identity; the URL alone grants nothing. Use a separate browser SSO callback, secure cookies, no-store responses and safe filenames.

Custom-connector links can show Claude's external-link confirmation before the browser page; include that step in onboarding. [Custom connector behavior](https://claude.com/docs/connectors/building/directory-vs-custom)

CSV applies the same row/field policy as queries, including spreadsheet-formula escaping for text cells while preserving numeric types. Include master, date and field definitions alongside the export. Gateway audit writes and ephemeral export state are separate from source access.

**Original files:** Andrew confirmed filtered CSVs initially and original-file access later. A separate download_original capability requires authorization for every row and field in the object. Partial-row/column grants cannot receive the original Parquet or bronze ZIP. Keep it disabled in v1; subsequently approved originals can be streamed unchanged without write permission.

Avoid raw S3 presigned URLs in v1. They are bearer links usable by holders until expiry or credential invalidation; removing an application entitlement does not immediately invalidate an issued URL. [AWS presigned URL behavior](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html)

Revocation blocks subsequent calls and download starts, including old tickets. Downloaded files and data already returned to Claude cannot be recalled; do not promise to stop bytes already delivered in-flight. Selected results enter the organization's Claude chat environment and retention settings. Commercial training defaults do not mean zero transfer. [Claude commercial data handling](https://privacy.claude.com/en/articles/7996885-how-do-you-use-personal-data-in-model-training)

## AWS permissions and validation

Proposed role: **opal-mcp-emp-menachem-schwab-read**. Trust only opal-gateway-role with a dedicated ExternalId. Allow the gateway to assume this exact role with that value. The existing wildcard employee-role grant uses the Tax SMA ExternalId: verify live interactions rather than reusing that value or broadening the namespace. Use server-derived session/audit identity; users never select a role.

Attach [the source-reader policy](reader-role-policy.proposed.json) **only to the assumed reader role**, not to the operational gateway role:

- GetObject and GetObjectVersion on the three approved dataset prefixes under each master.
- ListBucket on opal-data-assets only with approved s3:prefix values.
- Explicit denies for all other actions, object paths and listing scopes.

Prefix-limited listing and object-read resources are separate controls. [AWS policy keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazon-s3-policy-keys.html) Current-object metadata provides VersionIds without ListBucketVersions. IAM admits historical objects/versions in approved prefixes; the application enforces the narrower date/version catalog.

All Schwab source access uses assumed-role credentials, with no fallback to gateway credentials. Do not attach the existing bucket-wide opal-assets-read role to Menachem or the gateway. Current AES256 objects need no KMS decrypt grant; encryption changes require review of the exact key grant.

**41/41 IAM custom-policy simulations passed.** [Results](iam-simulation-results.json); [read-only reproducer](validate_proposed_policy.py). Positives cover both masters' six dataset prefixes and version reads. Negatives cover other datasets/buckets, root/malformed listing, writes/deletes/ACLs/tags, bucket administration and role chaining. Negative S3 cases add an intentionally broad s3:* allow to verify explicit denies win.

This is policy-model evidence. It establishes no deployed grant, role trust, resource policy, organizational control, authentication or application filter. [AWS simulator limitations](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html)

## Implementation and acceptance

For owner setup, prepare [this prefilled organization connector form](https://claude.ai/admin-settings/connectors?modal=add-custom-connector&connectorName=Opal%20Gateway&connectorUrl=https%3A%2F%2Fmcp.opalinvest.dev%2Fmcp). It only prefills settings; it grants no access. Reuse an existing organization connector when appropriate. Give Menachem a short Connect / enable in chat / try a sample query / download walkthrough. Custom connectors need no directory listing. [Install-link contract](https://claude.com/docs/connectors/building/directory-vs-custom)

Preserve existing connector settings during the pilot. Changing stored OAuth credentials or request headers requires removing/recreating the connector and reconnecting members; treat that as a planned migration if needed. Shared static headers are not Menachem's identity. [Connector settings](https://claude.com/docs/connectors/custom/remote-mcp)

Enterprise Managed Auth is an optional future simplification for Team/Enterprise: it needs trusted identity assertions, JWT-bearer exchange and compatible client registration; current DCR alone does not support it. It is not implied by existing Entra login. [Managed authentication](https://claude.com/docs/connectors/building/enterprise-managed-auth) Private MCP tunnels are unnecessary for the existing public gateway; revisit only if network policy changes. [Tunnel applicability](https://claude.com/docs/connectors/mcp-tunnels/overview)

Implement in the existing gateway: principal context and hosted callback support; a default-deny data-entitlement module; Schwab catalog/query integration; authenticated download route; dedicated Terraform role. Enforce discovery and dispatch, classify tools in existing guards/audit, and keep data tools independent of Graph-token acquisition.

Use the checked-in employee-role security review and normal gateway release process. This artifact authorizes neither apply nor a user grant. Before rollout, resolve Menachem's immutable identity, confirm proposed initial fields/date/account scope, verify workspace connector controls, and measure gateway headroom. Initial filtered CSVs are confirmed.

Acceptance must demonstrate:

1. Claude application connection without CLI; expiry, refresh, reconnect and logout.
2. Existing Code clients and other gateway users retain their working flows.
3. Unknown identities, forged headers and missing/revoked profiles yield no Schwab data.
4. Discovery is restricted and direct calls to unlisted tools are denied.
5. Masters remain separate across queries, filters, totals, caches and exports.
6. Account/column filtering precedes queries, aggregation, caching and export; hidden-field probes fail.
7. Actual representative data questions and full authorized CSV downloads work.
8. Snapshot totals match independent fixtures, preserve decimals and never add dates together.
9. Pinned-version references, incomplete/missing/stale data and oversized requests are explicit.
10. Copied links fail for other identities; expiry and policy changes invalidate old tickets.
11. Originals fail under partial-object grants and succeed only with whole-object permission.
12. Prompt-like file content cannot invoke tools, expand scope or modify grants.
13. Deployed permissions are measured; test disallowed operations with safe isolated fixtures/live-policy evidence, never destructive probes against production data.
14. Concurrent queries/exports fit gateway limits; audit principal, operation, master, dataset, policy/version, counts and outcome without copying sensitive values or tokens.
15. Revocation/rollback disables the new grant/integration while source data and ingestion remain intact.
16. Actual Claude web/desktop handshake preserves the Bearer challenge, headers, negotiated protocol and transport through the deployed edge; validate first with MCP Inspector, then the real custom connector.
17. Refresh atomically invalidates the prior token, rejects replay/wrong client/wrong resource, revokes the affected family on reuse and survives restart/concurrency. Existing Code clients pass the same regression checks.
18. Complete serialized responses stay within both character and byte limits, including Unicode and duplicated structured/text content; paginated totals remain correct.
19. Auth endpoint latency meets its separate deadlines; query/export traffic respects ALB idle behavior and cancellation. No user is sent into an OAuth loop for a denied data entitlement.
20. The owner/member walkthrough covers external-link confirmation, reconnect and troubleshooting. Record tool, UTC timestamp, connector URL and sanitized server correlation; collect an ofid_ reference if Claude supplies one for a connection failure.

Original planning estimate: **4-7 engineering days**, before the explicit refresh lifecycle gap identified in revision 2. Re-estimate after scoping durable token state, migration and regression testing; this is not a committed delivery date. Measure latency, export sizes, CPU/memory, S3 requests and operating cost during the pilot.

All changes in this package are local specification and evidence files.
