# CHANNEL_READ_SCOPES_MEASURED -- NFRA_CTLPLN.TO-CT-i-11 (0.9.0_WK_NFRA_CTLPLN~39)

Question: which Microsoft Graph delegated scopes is the gateway's token for `MS_INGEST_IDENTITY` requested with, which
scopes do the three new Graph paths need, and which needed scopes does the request not carry.

All file:line below are read at the base of branch `wk-NFRA_CTLPLN-39`, under `infra/aws/ec2/opal-gateway/app/`.

## 1. The scopes the token is requested with (from the code)

The route gets its token with `get_token(get_config().MS_INGEST_IDENTITY)` (`teams_route.py`, `_graph`, line 109). In
`token_broker.get_token` (lines 192-229) the scope list is decided in this order:

1. `tier = _machine_tier(display)` (line 217; a fixed server-held identity has no principal). `_machine_tier` (lines
   162-177) returns MASTER_ADMIN or STANDARD_EMPLOYEE only when the provider is signature-verified AND the identity is
   in `MASTER_ADMIN_EMAILS` or `WRITE_CAPABLE_EMAILS`; every other case, and every exception, is READ_ONLY.
2. `scopes = _scopes_for_tier(tier)` (line 218). `_scopes_for_tier` (lines 141-147): STANDARD/MASTER get
   `config.GRAPH_SCOPES`; READ_ONLY and anything unknown get `config.READ_ONLY_GRAPH_SCOPES`.
3. `consented = identity_scope.consent_scopes(display)` (line 219); if it is not None the list is cut to the scopes
   in it (line 223: `scopes = [s for s in scopes if s in consented] or ["User.Read"]`). `consent_scopes`
   (`identity_scope.py` lines 121-143) returns None for an unscoped identity, otherwise the union of
   `graph_scope_map.TOOL_GRAPH_SCOPES` over its allowed tools plus `graph_scope_map.CALLER_GRAPH_SCOPES` over the
   non-tool callers whose configured identity is this one.
4. `app.acquire_token_silent(scopes, ...)` (line 225).

The two lists (`config.py`):

- `GRAPH_SCOPES`, lines 61-69 (the full envelope): `User.Read Mail.Read Mail.Send Mail.ReadWrite Calendars.ReadWrite
  Files.ReadWrite.All Sites.Read.All Chat.ReadWrite ChatMessage.Send Team.ReadBasic.All Channel.ReadBasic.All
  ChannelMessage.Read.All ChannelMessage.Send OnlineMeetings.ReadWrite OnlineMeetingTranscript.Read.All
  Presence.Read.All Notes.ReadWrite.All` (the Teams line is line 66).
- `READ_ONLY_GRAPH_SCOPES`, lines 98-103: `User.Read Mail.Read Sites.Read.All Team.ReadBasic.All
  Channel.ReadBasic.All ChannelMessage.Read.All OnlineMeetingTranscript.Read.All Presence.Read.All`
  (Teams scopes on line 101).

Both lists can be overridden by the environment variables of the same name (`os.environ.get`, lines 62 and 99); the
host's environment is not readable from here.

## 2. The scope each of the three Graph paths needs

| Graph path (all GET) | Scope needed | Where the claim comes from |
|---|---|---|
| `/me/joinedTeams` | `Team.ReadBasic.All` | The code's own comments: `tools.py:1115` (Teams section header) and `tools.py:1119-1122` (`list_teams` calls this exact path); `graph_scope_map.py:33` (`"list_teams": {"Team.ReadBasic.All"}`). Microsoft's "List joined teams" page, from memory (no web fetch was made): delegated least-privileged `Team.ReadBasic.All`. |
| `/teams/{team_id}/channels` | `Channel.ReadBasic.All` | `tools.py:1126-1130` (`list_channels` calls this exact path); `graph_scope_map.py:35`. Microsoft's "List channels" page, from memory: delegated least-privileged `Channel.ReadBasic.All`. |
| `/teams/{team_id}/channels/{channel_id}/messages` with `$expand=replies` | `ChannelMessage.Read.All` | `tools.py:1134-1138` (`read_channel_messages` calls this path, without the expand); `graph_scope_map.py:37`. Microsoft's "List channel messages" page, from memory: delegated `ChannelMessage.Read.All`. The existing replies path in `teams_route.py` is attributed to the same scope at `graph_scope_map.py:94-95`. |

The `$expand=replies` and the `$top` page size are query options on the messages path; the order's contract names
them. This file does not measure whether Graph accepts `$top` on `/me/joinedTeams` or on `/teams/{id}/channels`
(see the surprise row W39-S3).

## 3. What the request carries and what it lacks

Per list, against the three needed scopes:

- `GRAPH_SCOPES` (line 66): carries `Team.ReadBasic.All`, `Channel.ReadBasic.All`, `ChannelMessage.Read.All`.
  Needed scopes missing: none.
- `READ_ONLY_GRAPH_SCOPES` (line 101): carries all three. Needed scopes missing: none.

So whichever tier `_machine_tier` returns for `MS_INGEST_IDENTITY`, the base request list carries every needed scope.
No change to either list is needed or made.

One place in the code can still remove them. `graph_scope_map.CALLER_GRAPH_SCOPES["teams_route"]`
(`graph_scope_map.py` lines 98-99) is the scope set the consent filter (section 1, step 3) unions in for this route. It
reads `User.Read, Chat.ReadWrite, ChatMessage.Send, ChannelMessage.Read.All, ChannelMessage.Send`. It does NOT list
`Team.ReadBasic.All` or `Channel.ReadBasic.All`. Whether that matters depends on a fact this worker cannot read: whether
`MS_INGEST_IDENTITY` is a SCOPED identity in the overlay `identity_scope._load_overlay()` reads.

- If the identity is unscoped, `consent_scopes` returns None and nothing is cut: no missing scope.
- If the identity is scoped, line 223 cuts the request to the overlay's union, and `Team.ReadBasic.All` and
  `Channel.ReadBasic.All` are absent from it unless a tool on its allowlist maps to them (`list_teams`,
  `list_channels`, `graph_scope_map.py:33,35`). In that case the two list routes would ask for a token without them
  and Graph would refuse. `ChannelMessage.Read.All` survives (line 99).

`graph_scope_map.py` is outside this order's `<paths>`, so it is not edited; filed as surprise row
NFRA_CTLPLN-W39-S1.

## 4. What this worker cannot read

- The live consent: which delegated permissions the tenant has actually consented for the gateway's app registration
  (the "App-2" registration of the config.py comment, lines 42-60). `config.py:56-60` says each string was verified
  against the consent screen at a past date; that is a claim in a comment, not a read of today's consent.
- The host's environment overrides of `GRAPH_SCOPES` and `READ_ONLY_GRAPH_SCOPES`, the host's `MASTER_ADMIN_EMAILS` and
  `WRITE_CAPABLE_EMAILS`, and the identity-scope overlay. These decide the tier and whether the filter applies.
- Whether the cached refresh token for `MS_INGEST_IDENTITY` was minted with the Teams scopes; a token minted before
  they were consented would return NeedsLogin (409 from these routes).

Nothing was deployed, no AWS call was made, and no Graph call was made; every statement above is a read of the
files cited.
