# OA-t-4 -- blocker 2 (`33 of 33 reads failed, warm and cold`) diagnosed from the code path

`0.9.0_WK_NFRA_OPALAI~4`, 2026-09-24. Source measurement:
`org/tier0_utility/0.0.3_BG_BBGTerminal/logs/2026-09-24/teams_watch_two_blockers_and_a_dark_owner_1145-1315Z.md:53-59`
records blocker 2 as **MEASURED, cause UNKNOWN**, and offers one **untested HYPOTHESIS**: `teams-watch.py`
"may present that MCP-gateway token directly to `graph.microsoft.com` -- wrong audience".

## 1. The hypothesis is inconsistent with the code path -- REFUTED, not merely unconfirmed

`teams-watch.py` never calls `graph.microsoft.com`. Every read (`poll`, `read_chat`, and the new tool
`read_teams_attachment`) goes through `_gateway_call()`, which POSTs to `GATEWAY =
"https://mcp.opalinvest.dev/mcp/"` with the client's own Bearer token
(`.claude/skills/teams-assist/teams-watch.py:357-361` at the pre-move HEAD).

Server-side, `infra/aws/ec2/opal-gateway/app/tools.py`'s `_run()` chokepoint (the function every
`@mcp.tool()` runs through) resolves the Graph token itself, independently of the caller's Bearer:
`_user_token()` at `:102-106` calls `get_token(email)` from `app/token_broker.py`, and `graph.call()`
(`app/graph.py:22-57`) is invoked with **that** server-derived token, never the client's MCP Bearer. So
the client's token audience cannot be the cause of a Graph-side failure: it never reaches Graph at all.
This is GROUNDED (code read, not inferred): `app/tools.py:719-724` (`read_chat_messages` calls
`graph.call(t, ...)` where `t` comes from `_user_token()` inside `_run`, not from the request's own
Authorization header).

## 2. The evidence-consistent mechanism: a GraphError on `$select` reads as "read failed" client-side

`_run()`'s own contract (`app/tools.py:164-170`): on `graph.GraphError`, it returns `{"error": str(ge)}`
-- a dict with **no `"value"` key**. `teams-watch.py`'s `fresh_messages()` treats exactly that shape as
"the chat was NOT read" (`if not isinstance(page, dict) or "value" not in page: return None`), which the
main loop reports as `read failed for chat {cid} -- cursor HELD, retry next cycle` -- the literal string
the Analyst's log shows 33 times, across all four chats, every cycle, warm and cold.

This localizes the defect to whatever makes `graph.call()` raise inside `read_chat_messages` /
`read_channel_messages` specifically (not `poll_addressed_teams_messages`, which uses a different,
narrower `$select` and is not failing).

## 3. The prime candidate: `_TEAMS_MSG_FIELDS`, added un-exercised against live Graph

Both readers share one `$select` list, `_TEAMS_MSG_FIELDS` (`app/tools.py:664-667`), added in commit
`684e7eb90a0631c0a87486698484549cc960fb27` (2026-09-11). That commit's own message says, verbatim:
"NOT VERIFIED, AND NOT CLAIMED: the new tool has NOT been exercised against live Graph... this is
COMPILED AND REASONED, NOT RUN" and "NOT DEPLOYED. The gateway runs on EC2; this commit changes the
record only." `poll_addressed_teams_messages`'s own Graph call (`app/tools.py:794-798`) uses a disjoint,
narrower `$select` (`id,topic,chatType`) on a different endpoint (`/me/chats`, not `/chats/{id}/messages`)
and is unaffected by whatever in `_TEAMS_MSG_FIELDS` a live Graph tenant rejects.

**NOT ESTABLISHED, AND NOT CLAIMED**: which exact field in `_TEAMS_MSG_FIELDS` a live Graph 500/400s on,
or whether this exact code is what the running EC2 box currently serves (no live-box read is in this
cell's declared egress class, and this cell does not deploy). What IS established from the record alone:
(a) the client-side symptom is EXACTLY the shape `_run`'s GraphError branch produces; (b) the one `$select`
change in this code path was landed explicitly un-verified against live Graph; (c) the "wrong audience"
hypothesis cannot be true given the server always substitutes its own token.

## 4. What this cell built regardless

The auth rewrite (own OAuth refresh family, see the commit message) closes blocker 1 (the coupling to
Claude Code's own MCP activity) independently of blocker 2's cause. Blocker 2 is a gateway-side (Graph
`$select`) defect outside this cell's `<paths>` (`infra/aws/ec2/opal-gateway/app/tools.py` is Read-only
here) and outside its egress class (no live gateway tool call is authorized in this session beyond the
one declared metadata GET). The live read is proven at the round's close run, per the task order.
