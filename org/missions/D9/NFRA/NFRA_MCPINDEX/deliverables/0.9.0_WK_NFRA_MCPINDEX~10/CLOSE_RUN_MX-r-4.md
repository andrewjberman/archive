# CLOSE_RUN_MX-r-4 -- NOT RUN by the worker: no legitimate route to the tools

Worker 0.9.0_WK_NFRA_MCPINDEX~10, 2026-09-29 ~03:0xZ, after the deploy of `0bce8d322a` (gateway pin `3371f18803`).
The order (step 9) asks for one live question per portal surface, through the gateway, with the tool that answered, the
figure and as-of date it returned, and the portal's own figure and as-of date. **The worker ran none of the four.**
The issuer runs it (per the GO: "no legitimate route means you write CLOSE_RUN_MX-r-4.md saying so").

## Why there is no route

- The tools are MCP tools. A caller reaches them only through the gateway's authenticated MCP route, where
  `IDENTITY_PROVIDER=alb_oidc` resolves the principal from the ALB's signed OIDC header. The worker holds no such
  session and no Entra identity.
- Measured on the host after the deploy (ssm:556c333d-2bc5-4cdb-b078-85b0a10e3abc): `curl 127.0.0.1:8080/mcp` with no
  identity returns **401**. `/health` returns 200.
- The only other way to call a tool from the host is to import `app.server` in a shell and invoke the tool function
  with a principal the shell supplies. That would answer with a principal the caller invented, and the firm gate
  (`catalog_gate` on `query_v0._principal(email)`) is what the close run is meant to exercise. It was not done, and it
  is not a substitute for a call through the gateway.

## What the worker DID measure (not a close-run answer)

| item | value | source |
|---|---|---|
| host `.env` ENABLED_INTEGRATIONS | `ycharts opal_portal globgrph opal_discover portal_index`, exact | ssm:556c333d, read from the host |
| tool-name list | 46 before, 51 after; 0 removed, 5 added | probe `probes/list_tools_probe.py`, fresh `app.server` import off the real `.env` |
| tools added | `opal_discover`, `opal_describe`, `mdpf_get_aum_metrics`, `mdpf_get_account_distribution`, `mdpf_get_aggregate_aua` | same |
| on-host integrations line | `enabled: ['ycharts', 'opal_portal', 'globgrph', 'opal_discover', 'portal_index']` | the probe's stderr |

## The four surfaces (A2 denominator), for the issuer's run

| surface | question | tool that answered | figure and as-of | the portal's own figure and as-of |
|---|---|---|---|---|
| `platinum/mdpf` | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| `platinum/etfs` | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| `platinum/advi` | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| `json/*` | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

Two facts the issuer may want before choosing the questions (read from the shipped code, not from a call):
- `portal_index` holds three tools, all `mdpf_*`, so only `platinum/mdpf` has a purpose-built tool. The other three
  surfaces would be answered by `opal_discover` naming a dataset and `query_v0` as the next tool, or by an existing tool.
- The gateway role reads `opal-data-portal-v2/json/*` and `platinum/*` only (live `get-role-policy`, G-A G4). A
  `json-tiered/` key is not readable, and the catalog already marks that row BLOCKED-BY-ALLOWLIST.

This record grades nothing. J1 belongs to `3.0.0_SA_CVO~O`.
