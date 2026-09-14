# Review of Claude Remote MCP Requirements Brief

Archetype: design review
Date: 2026-09-14
Seat: 0.7.0_AE_CloudOps
Verdict: **Keep the opal-gateway architecture. Revision 2 of the spec incorporates material omissions; it is ready to guide implementation, with deployment acceptance still outstanding.**

Reviewed the complete body and table text of the exact supplied [Word document](C:/Users/AndrewBerman/Downloads/Claude_Remote_MCP_Requirements_Brief.docx), SHA-256 **87b0d6ea29020894169ab890d4c1885e1c0a7418c213c2f943a766b13d582e52**. The original DOCX was not modified. Compatibility claims affecting this design were cross-checked against the linked current Anthropic documentation, checked-in gateway code and fresh read-only ALB/HTTP observations.

## Material changes incorporated

| Finding | Assessment | Revision 2 action |
| --- | --- | --- |
| Original 256 KiB chat limit versus Claude's approximately 150,000-character limit | Concrete mismatch: an ASCII response within the old byte cap could exceed the client limit | Cap the entire serialized MCP response at both 100,000 characters and 128 KiB; count duplicate structured/text content and envelope |
| Public-client refresh token protection | The checked-in handler returns a new refresh JWT but does not invalidate the presented JWT; existing operator revocation is a different control | Require atomic durable rotation, grant/client/resource binding, reuse detection, family revocation and restart/concurrency tests |
| ALB browser OIDC versus MCP OAuth | Needs an explicit route/auth contract; live routes already implement the separation | Preserve MCP/OAuth/discovery forward rules, keep bearer enforcement in the gateway and browser authentication for downloads |
| Separate authentication deadlines and proxy timeout | Query deadline alone did not cover OAuth or ALB behavior | Add auth latency budgets and idle-stream tests; keep the 30-second query target under the measured 60-second ALB idle timeout |
| Real Claude setup and diagnostics | Original acceptance criteria were too general | Add actual web/desktop connector testing, Inspector, network/header/origin checks, complete owner/member walkthrough, external-link confirmation and reconnect procedure |
| Entra and optional enterprise features | Generic options in the document could be mistaken for required changes | Keep the gateway as OAuth issuer; identify direct-Entra requirements, Managed Auth and tunnels as conditional choices |

The response limit is documented in [Claude runtime specifications](https://claude.com/docs/connectors/building). Refresh protection is required for public clients in [OAuth security guidance](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.14.2). New source findings describe checked-in code; deployed source parity and refresh behavior have not been exercised.

## Cross-check against the supplied document

| DOCX topic | Disposition |
| --- | --- |
| Cloud-origin requests, public IPv4 DNS, egress IPs, WAF and redirects | Added to edge acceptance; operator-origin probes do not prove Anthropic-origin connectivity |
| Streamable HTTP versus legacy SSE | Explicit Streamable HTTP at /mcp; no /sse endpoint required |
| Client result/timeout limits and supported features | Corrected response cap; five tools need no sampling, subscriptions or draft capabilities |
| 401 discovery and 403 scope step-up | Retained 401 handshake; distinguish OAuth scope deficiency from a data entitlement denial to avoid repeated login |
| Exact metadata resource/issuer and discovery paths | Live documents agree with the canonical URL; the 401 points to the working root metadata path |
| DCR, CIMD and pre-registered OAuth clients | DCR remains v1; alternatives are not cumulative requirements |
| Hosted callback, PKCE and form/JSON encoding | Exact hosted callback already required; parsing/latency/refresh requirements made explicit |
| Direct-Entra API identifier and audience | Conditional: Claude currently discovers the gateway issuer, not Entra; do not unnecessarily change Entra API identifier URIs |
| Lazy authentication and discovery caching | All Schwab tools remain protected. During metadata changes allow cache expiry and test a fresh connection; do not weaken authentication to obtain a Connect card |
| Owner/member GUI flow and per-chat enablement | Added concrete onboarding/install form and reconnect behavior |
| Static request headers and tool controls | No shared credential stands in for Menachem; client controls and annotations supplement server authorization |
| Install links and directory review | Added prefilled organization link; no directory submission needed; download links may prompt external-link confirmation |
| Enterprise Managed Auth | Optional follow-on; requires additional trust/token exchange and compatible registration, not merely existing SSO |
| Enterprise tunnels | Unnecessary for the current public ALB; relevant only to a future private-network requirement |
| Inspector, real client, clientInfo and diagnostics | Added explicit acceptance and support evidence requirements |

The source document carefully states that ALB compatibility was not inspected. This review supplies that missing deployment observation. The sample HTTP challenge has explicit Word line breaks; its formatting is valid.

No other material contradiction was found in the requirements relevant to our chosen path. This is not a certification of every optional product feature or of the live Claude workspace configuration.

## Fresh deployment evidence

[Machine-readable evidence](requirements-review-evidence.json), measured **2026-09-14T18:43:46Z**:

- ALB opal-gateway is internet-facing and IPv4, with access logging enabled.
- Priority 10 forwards /mcp, /mcp/*, /register, /authorize and /token.
- Priority 20 forwards /callback and the published OAuth/JWKS discovery paths.
- The default action set still includes browser OIDC.
- Unauthenticated GET /mcp: **401**, correct Bearer resource_metadata challenge, **93 ms**, no redirect.
- Protected-resource and authorization-server metadata: **200**, **110/109 ms**.
- Resource is https://mcp.opalinvest.dev/mcp; issuer is https://mcp.opalinvest.dev; public-client DCR and S256 are advertised.
- ALB idle timeout: **60 seconds**. This seat's resolver returned two globally routable IPv4 addresses.

No OAuth registration, token exchange, replay attempt, authenticated data call or configuration change was performed. No credentials, cookies or source customer rows were collected. Existing 41 IAM simulations remain valid for the unchanged draft IAM policy; they were not rerun for a document/response-limit change.

## What remains before activation

Resolve Menachem's immutable identity and approve the proposed fields/date/account scope; implement the gateway additions including hosted callback and refresh lifecycle; measure authenticated protocol behavior from Claude; pass the expanded acceptance criteria. Both masters, CSV-first downloads and the gateway entitlement architecture remain the confirmed scope.

The original 4-7 day estimate predates this explicit refresh lifecycle gap. Carry durable token state, migration and regression testing into the implementation estimate; do not treat that number as a committed delivery date.
