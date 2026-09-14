# M365-MCP-Login redirect correction

- Seat: 0.7.0_AE_CloudOps
- Authorization: Andrew, Codex user message, "Ok fix it now."
- Context: The live M365-MCP-Login callback still ended in an encoded backtick; Andrew authorized correcting it.
- Execution: 2026-09-14T20:46:19Z; verified 2026-09-14T20:47:09Z.
- Status: LIVE correction applied and verified.

The application web redirect changed from `https://mcp.opalinvest.dev/oauth2/idpresponse%60` to `https://mcp.opalinvest.dev/oauth2/idpresponse`. Microsoft Graph returned HTTP 204, request ID `20b82a05-3bc6-4a05-adf2-ea841ae2b0b5`. The enterprise application's reply URL synchronized automatically.

The application client ID is `53360468-0a38-4e56-a1ed-3db6914461cd`, application object ID `0ecdcd9e-339a-49a3-a816-8b3a2f976054`, and service principal ID `dff7d86b-c789-4bfd-821c-6ada1725dc4f`, in tenant `6810043e-d171-4adc-9975-068b35e179da`.

Fresh reads confirmed the clean callback on both objects. Entra also synchronized its derived `web.redirectUriSettings`. Home page, logout URL, implicit-grant settings, SPA redirects and public-client redirects matched the pre-change values. The single PATCH body contained only `web.redirectUris`.

An unauthenticated GET of `https://mcp.opalinvest.dev/sprint` returned HTTP 302 to this tenant's Microsoft authorization endpoint, with the expected client ID and the exact corrected callback. Interactive sign-in was not exercised.

The initial verification script flagged the expected derived `redirectUriSettings` update as a difference. Follow-up checked that field explicitly and passed all relevant checks; no second mutation was needed.

Compiler routing attempted `comp-which` before inspection; its unscoped fallback timed out after 90 seconds. Bare `comp-find 'idpresponse%60' -- 'infra/aws/ec2/opal-gateway/IT_REQUEST.md'` found the documented typo in both duplicate incident entries. Live verification used the existing Windows Azure CLI login and Microsoft Graph.

[Sanitized before/after evidence](./evidence.json) contains the API receipt and final readback. No access tokens, cookies or authorization state were retained.
