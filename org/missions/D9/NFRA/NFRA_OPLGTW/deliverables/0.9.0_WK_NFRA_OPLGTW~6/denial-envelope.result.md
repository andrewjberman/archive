# NFRA_OPLGTW.TO-OG-z-4 -- denial-envelope result

**Changed line:** `infra/aws/ec2/opal-gateway/app/tools.py:83-91` (`_PolicyGuardedMCP.call_tool()`, at
commit `f49ea6ce48d82b28b85304980cab0cbd38656595`) -- the denial branch, which used to `return denial` (the
bare dict), now returns:

```python
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(denial, indent=2))],
                structuredContent=denial,
                isError=True,
            )
```

The MCP low-level server's `call_tool` handler (`mcp/server/lowlevel/server.py`) renders a returned `dict`
as `isError=False` unconditionally (the "structured content only" branch); it returns a returned
`types.CallToolResult` verbatim, so this is the one place `isError` can be set `True` while the body stays
byte-identical to the dict `data_entitlement.tool_denial()` already built (same `error`, `guard_denied`,
`code`, `error_code` keys; same contract `error_codes` value). `data_entitlement.py`'s decision (WHICH
calls are denied) and the audit line (`audit.log_call(..., "denied", ...)`) are untouched.

**Docstring after the change (`app/tools.py:58-63`, quoted verbatim, unchanged by this cell):**

```
"""NFRA_OPLGTW OG-z-1: the per-principal policy guard on DISCOVERY and DISPATCH of every tool on this server --
native (below), integration (app/integrations) and any tool registered later -- before the tool function runs,
so before any credential fetch. The decision is app/data_entitlement.py's, from a strong read of the request
principal's current profile and grant (off the event loop). A denied call returns the structured denial as the
tool result (a terminal tool error: never a 401, never a login)."""
```

The docstring's claim ("a terminal tool error") did not need editing: the code now makes it true (OGZ4-AC5
reads both and confirms agreement).

## Criteria measured (all at commit `f49ea6ce48d82b28b85304980cab0cbd38656595`, run twice each -- once
during build/diagnosis before the commit, once after, identical deciding values both times)

- **OGZ4-AC1** PASS -- `test_ogz4_ac01`: a denied `schwab_query` call (no profile at all) through OG-v-2's
  real live-app harness returns `isError=True`, body `{'error': "tool 'schwab_query' needs an active data
  entitlement; this principal has none", 'guard_denied': True, 'code': 'entitlement_denied', 'error_code':
  'ENTITLEMENT_DENIED'}` -- `error_code` is the contract's unchanged `ENTITLEMENT_DENIED` value. `1 passed`.
- **OGZ4-AC2** PASS -- `test_ogz4_ac02`: (difference) a permitted `schwab_query` call in the same harness
  returns `isError=False`; the contrasting denied call in the same test prints `isError=True`. `1 passed`.
- **OGZ4-AC3** PASS -- `og_z4.py AC3` (mutant control): a depth-mirrored scratch copy of `app/` with the
  `isError=True` return replaced back to `return denial` makes `test_ogz4_ac01` FAIL (`1 failed`) while
  `test_ogz4_ac02` still PASSES (`1 passed`) -- the fix, and only the fix, discriminates. `git status
  --porcelain` before/after identical (only the untracked `.scratch/`/`.venv-og/` directories, both times).
- **OGZ4-AC4** PASS -- `tests/test_data_entitlement_guard.py`, unedited: `12 passed` -- OG-z-1's own guard
  module (WHICH calls are denied, discovery filtering) is unaffected by this cell.
- **OGZ4-AC5** PASS -- `og_z4.py AC5`: the live worktree's class docstring claims "a terminal tool error"
  and the denial branch sets `isError=True` -- both printed, and they agree.

## Bounds honored

`app/data_entitlement.py` untouched; `tests/acceptance/**` untouched (read only, per `test_ogv2_a06`);
the audit line unchanged; `list_tools()` untouched; no other tool's behaviour changed; nothing deployed
(moto harness only); no dependency added, `mcp==1.28.0` unchanged.

## Surprise channel

No new row filed. Row `NFRA_OPLGTW-W5-S18` (the defect this cell fixes, per the task order's own RECORD
FACE) is ARMED with `disarm_owner: 1.0.0_SA_CTO`, disarming on this cell's drain per the issuer's own text
-- not this worker's to disarm.
