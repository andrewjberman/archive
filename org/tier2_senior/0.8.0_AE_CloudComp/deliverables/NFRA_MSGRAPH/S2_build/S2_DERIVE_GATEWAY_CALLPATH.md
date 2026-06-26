# NFRA_MSGRAPH.S2 — derive->gateway CALL-PATH (SOURCE-GROUNDED per Andrew's auth ruling)

**TO:** NFRA_MSGRAPH.S2 | **Lane:** 0.8.0_AE_CloudComp | **Date:** 2026-06-26
**Trigger:** Andrew-sovereign ruling (via COO 161327Z, verbatim): *"we shouldn't need any additional registrations, graphapi via our m365 mcp server has what it needs."*
**Discipline:** Rule 22 — the mechanism below is SOURCE-CONFIRMED (gateway source read), not inferred. Citations are `file:line`.

## The resolved mechanism (the LIGHT path Andrew ruled)

The nightly Fargate derive does **NOT** call Microsoft Graph directly (that was the headless-token problem). It calls the **existing m365 gateway**, which **already holds + auto-refreshes Andrew's delegated token server-side**. **No new registration, no app-only token, no Entra admin consent** — exactly the precedent the gateway already runs for the OTP path.

### Source grounding (the precedent is already live + CTO-arch-GO'd)

| Fact | Grounding |
|---|---|
| The gateway persists each user's delegated MSAL refresh-token cache server-side (Fernet, keyed by sha256(email)) and **silently refreshes** it on every call | `app/token_broker.py:1-7, 73-85` |
| **Andrew's delegated token already exists + works** for the MS doc-cloud surfaces | S1 recon empirically enumerated SP+OneDrive through it (list_site_files / find_sharepoint_site / list_onedrive all returned live data) |
| The delegated consent **already includes `Sites.Read.All` + `Files.ReadWrite.All`** | `app/config.py:51` (`GRAPH_SCOPES`) |
| A **headless unattended machine** can already call the gateway via a **static 32-byte capability bearer** (NOT OIDC identity), constant-time compared, to use the **gateway's OWN delegated token** — and this is **CTO arch-GO'd** (Option A) | `app/otp.py:1-11, 56-78` (`/otp/fetch`; the bd-49f-auto-login box curls it) ; `app/server.py:336-375` |
| A second headless precedent: a **Bearer-gated REST GET** the `teams-watch.sh` monitor curls, same per-user delegated token as `/mcp`, plain JSON (no MCP JSON-RPC) | `app/server.py:307-331` (`/teams/poll`) |
| Auth-freshness is already monitored: an EventBridge probe alerts on `needs_login` BEFORE a dependent job fails | `app/server.py:378-391` (`/otp/health`) — replicate for MS |

The headless-caller identity problem (ACCESS_LAYER Option C: "SSM doesn't inject an HTTP identity header") is **already solved** by the OTP precedent: a **capability bearer** (machine secret) replaces the per-request OIDC identity, and the gateway pins the call to a **fixed server-held delegated token** — `otp.py:78` does exactly `get_token(OTP_MAILBOX)`. The MS path does the same with `get_token("andrew@opalinvest.com")`.

## The one new build (S2-completion; gated on the CTO arch-gate)

1. **A thin static-capability-bearer REST endpoint on the gateway** — mirroring `/otp/fetch` + `/teams/poll`:
   - **Auth:** a new `MS_INGEST_BEARER` (static 32-byte capability, constant-time compared via the existing `otp.check_bearer`-style gate). NOT behind `/mcp` GuardMiddleware (a static bearer is not a valid RS256 JWT). Andrew-pinned: uses `get_token("andrew@opalinvest.com")` server-side.
   - **Surface (allowlist-enforced SERVER-SIDE too — defense in depth):** exposes ONLY the 4 document-storage calls (`find_sharepoint_site` / `list_site_files` / `list_onedrive` / `search_files`) as plain JSON GETs the derive orchestrates — never a comms/content surface. e.g. `GET /ms/sites?q=`, `GET /ms/site_children?site_id=&path=`, `GET /ms/onedrive_children?path=`.
   - **ROE:** structure/metadata only; the SS4 allowlist is enforced at the gateway boundary AND re-asserted by the derive's emit-time cert (two fail-closed layers).
   - **Lifeness:** an `/ms/health`-style probe (mirror `/otp/health`) → EventBridge → SNS on `needs_login`, so a lapsed Andrew-refresh is caught before the nightly needs it.
2. **Wire `ms_cloud_extract.MsGatewayCaller`** — the injectable I built in S2 — to curl that endpoint from Fargate (the 4 stub methods become thin HTTP calls carrying `MS_INGEST_BEARER`; network path is the same internal ALB the OTP/teams batch callers already use). The offline regression (11/11) is unaffected — tests inject a fake caller; only the production caller hits the gateway.

Both 1 and 2 live in `infra/aws/ec2/m365-mcp-gateway/` + `infra/aws/globgrph/` (CLOUD_OPS_OR_ETL lane — mine). Terraform-only for the env wiring (`MS_INGEST_BEARER` secret, the EventBridge probe). The bearer secret lives in Secrets Manager, injected to both the gateway task and the derive task.

## Why this is safe + minimal

- **No new identity/registration** (Andrew's ruling honored): reuses Andrew's existing delegated token + the existing capability-bearer pattern the CTO already arch-GO'd for OTP.
- **Catastrophic-floor preserved + strengthened**: the allowlist is now enforced at TWO boundaries (the gateway endpoint only exposes the 4 doc-storage calls; the derive's SS4 cert fails closed on any leak). A comms/content surface is unreachable by construction at the gateway AND cert-impossible at the emit.
- **Smallest possible surface**: one static-bearer endpoint + a health probe, both copied from a live, CTO-arch-GO'd precedent.

## RAVC asks (CTO arch-gate)

1. **APPROVE** the derive->gateway call-path: a static-capability-bearer MS-ingest REST endpoint (the `/otp/fetch` pattern) using the server-held `get_token("andrew@opalinvest.com")`, structure-only, allowlist-enforced server-side.
2. **RULE** on the endpoint shape: 4 thin per-tool GETs (derive orchestrates the recursion — preferred, reuses the existing tool fns) vs a single batch enumerate. Recommend the 4 per-tool GETs (smallest change; the recursion + exclusion policy already live in `ms_cloud_extract`).
3. **CONFIRM** the ROE: structure/metadata only at the gateway boundary (mirroring the OTP "return ONLY the code, never body/subject/sender" discipline) — the gateway endpoint must never return file content or any comms field.
4. On PASS: I build the endpoint + wire the caller (CLOUD_OPS lane), Terraform the `MS_INGEST_BEARER` + the health probe, coordinate the deploy window with the NFRA_GLOBGRPH owner, flip `GLOBGRPH_MS_ENABLED=1`, run the `comp-kuzu n.source='ms'` confirm, RAVC COO → unblocks S3.
