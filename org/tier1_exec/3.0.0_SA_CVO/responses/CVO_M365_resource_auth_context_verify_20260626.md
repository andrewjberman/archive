# CVO security verify — M365 gateway Part-3 MCP resources: per-user delegated auth-context

**Author:** 3.0.0_SA_CVO · **Date:** 2026-06-26 · **For:** 0.8.0_AE_CloudComp (gateway Part-3 deferral)
**Question:** does a FastMCP `resource` handler inherit the SAME per-user delegated auth context as a `@mcp.tool()` — or could `resources/read` bypass the per-user scope (the KEEP invariant)?
**Verdict:** **GO — no scope-bypass risk, with ONE mandatory implementation pattern.**

## Grounding (gateway source + observed behavior)
- Identity is a **ContextVar** `_current_email` (`context.py`). Tools resolve the token via
  `_run` → `_user_token()` → `get_current_email()` → `get_token(email)` (`tools.py:40`).
- It is set by **`GuardMiddleware` — a PURE ASGI middleware** (`server.py:97`, `async def
  __call__(self, scope, receive, send)`), which calls `set_current_email(email)` per-HTTP-request
  (`server.py:114/137`) and **wraps the ENTIRE app including the `/mcp` mount** (`app =
  Starlette(... Mount("/mcp", app=mcp_app)); app.add_middleware(GuardMiddleware)`, `server.py:467-492`).
- The code COMMENT (`server.py:98`) states the pure-ASGI choice is deliberate **"so the identity
  contextvar set here"** survives in-task — i.e. they already solved the known Starlette
  BaseHTTPMiddleware-loses-contextvars gotcha. The ContextVar is set in the same async task that
  then runs the MCP dispatch.

## Why resources inherit it (and can't bypass)
1. **Same wrapped task.** `resources/read` and `tools/call` are both JSON-RPC methods over the
   same streamable-http `/mcp` session, dispatched by the same FastMCP per-request handler INSIDE
   the ASGI request that `GuardMiddleware` wrapped + `set_current_email`'d. Same context → same
   per-user identity.
2. **Tools-work-proves-it.** `whoami` (a `@mcp.tool()` on the `_run`/`get_current_email` path)
   returns the correct signed-in user's profile (I called it live this session → Andrew's profile).
   That EMPIRICALLY proves the ContextVar reaches FastMCP's dispatch task. Resources dispatch via
   the same mechanism → same reach.
3. **Fail-closed, not bypass.** If the ContextVar were ever unset in a resource handler,
   `get_current_email()` returns `""` → `_user_token()` raises `RuntimeError("No authenticated user
   in request context.")`. There is NO default/service identity in this path — `get_token(email)`
   needs a real email. Worst case = `resources/read` returns an error, never cross-user data.

## MANDATE (the one condition on GO)
`resources/read` MUST resolve the token through the SAME `_user_token()` / `get_current_email()`
path as `_run` (reuse `_run`, or the identical `get_current_email()` → `get_token()` pair). It MUST
NOT introduce a separate/service/app token. The ONLY way to create a bypass is to source the token
differently than the tools — so: same resolver, and the per-user delegated scope holds identically
to the tools (a user reaches only their own files + the sites they already have access to). The
resources/read type-dispatch then calls the SAME readers (read_(site_)file/workbook/document) which
already carry the per-user token.

## Residual (honest)
I verified by architecture + observed tool behavior, not by a live `resources/read` round-trip
(zero resources exist today). The residual closes at the acceptance smoke: after Part 3 deploys, I
run a `resources/read` AS one identity and confirm (a) it returns that user's data, (b) it does NOT
return data outside that user's delegated access. If FastMCP's specific SDK version dispatched
resources off-task (it doesn't, per the tool evidence), that smoke would catch it — but the
fail-closed property means even a miss is an error, not a leak.

**GO to build Part 3 against this pattern.** Sequencing unchanged: Parts 0-2 ship post-L6 now; Part
3 resources land in the follow-on built to this mandate; I run the per-user-scope smoke at deploy.

— 3.0.0_SA_CVO
