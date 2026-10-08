# PREPARED, NOT APPLIED -- move `opal-gateway-bbg` from every site-Z session to the one seat that does the concierge's duty

By `0.0.0_AB_MSTR~Z`, 2026-10-07 ~23:2xZ, asked by `1.0.0_SA_CTO~Z` msg 31466 (ruling on row NFRA_OPLGTW-Z-S67).
Nothing below has been run. It changes Andrew's own Claude Code setup on site Z, so it is applied on his word, and
BEFORE he signs `opal-gateway-bbg` in again.

## State today, measured

- `C:\Users\Opal Bloomberg\.claude.json`, top-level `mcpServers` (user scope, so EVERY Claude session of this Windows user
  loads them): `bloomberg` (stdio), `opal-gateway-bbg` (http, `https://mcp.opalinvest.dev/mcp/`), `brightdata` (http),
  `opalgateway` (http, `https://mcp.opalinvest.dev/mcp`). No project-scoped `mcpServers` entry exists in that file.
- The repo's `.mcp.json` carries `opal-agent-comms`, `deck-generation`, `playwright`. Neither gateway entry is there.
- 14 `claude.exe` sessions were running on site Z at 18:5xZ; `1.0.0_SA_CTO~Z` reports 12 sessions holding the sign-in.
- `.tools/ajb.ps1` already has one block that runs for `0.0.3_BG_BBGTerminal` only (lines 262-277: it sets
  `ENABLE_TOOL_SEARCH` and pins the session id). That block is where a seat-only entry goes.

## The move, in order

1. STOP the Bloomberg seat's session (`/mstr-kill 0.0.3_BG_BBGTerminal`, or close its window). Its Teams watch is
   already down, so nothing is lost by this.
2. Remove the user-level entry. One command, as Andrew's user, from any shell:
   `claude mcp remove opal-gateway-bbg -s user`
   Read back: `claude mcp list` no longer names it; `.claude.json` top-level `mcpServers` has three keys.
3. Add the seat-only entry: a new file `org/mcp/bg-gateway.mcp.json`:
   ```json
   { "mcpServers": { "opal-gateway-bbg": { "type": "http", "url": "https://mcp.opalinvest.dev/mcp/" } } }
   ```
4. Have the launcher hand it to that seat only. In `.tools/ajb.ps1`, inside the existing
   `if ($base -eq '0.0.3_BG_BBGTerminal') {` block, after the `--session-id` line:
   ```powershell
   $bgMcp = Join-Path $ws 'org\mcp\bg-gateway.mcp.json'
   if (Test-Path -LiteralPath $bgMcp) { $claudeArgs += @('--mcp-config', $bgMcp) }
   else { Write-Host "[ajb] WARN: $bgMcp is missing -- the BG seat launches WITHOUT opal-gateway-bbg" -ForegroundColor Yellow }
   ```
5. Relaunch the Bloomberg seat through the launcher. In ITS window, Andrew runs `/mcp` and signs
   `opal-gateway-bbg` in (the MFA prompt goes to his phone). Check: its `whoami` answers as the Bloomberg account.
6. Check the other direction: in any other site-Z session, `opal-gateway-bbg` is absent from `/mcp`, and
   `opalgateway` still answers as Andrew.

Running sessions keep the servers they loaded at start. The other seats stop holding the entry as each relaunches;
none needs to be restarted for step 5 to work.

## Rollback

`claude mcp add --transport http -s user opal-gateway-bbg https://mcp.opalinvest.dev/mcp/`, revert the `ajb.ps1` hunk,
delete `org/mcp/bg-gateway.mcp.json`, relaunch the seat.

## Not measured -- each is a reason step 5 could surprise

- Whether a server supplied by `--mcp-config` keeps its OAuth record in `~/.claude/.credentials.json` under the same key
  as the user-level entry of the same name and URL. If it does not, the old record is orphaned and the sign-in of step
  5 is simply a fresh one.
- Whether `--mcp-config` ADDS to the user and project servers or replaces them. It must add: the seat also needs
  `bloomberg` and `opal-agent-comms`. Read `/mcp` in the relaunched seat before anything else. (`--strict-mcp-config`
  is the replacing form and is NOT in the hunk.)
- Whether `bg-teams-assist` step 0 or the seat's `prompt.md` names the server in a way this changes. Row
  OPAL_BBGTML-Z-S10 (the `--identity` pin) is a separate, still-open defect in the same arm line.
- The laptop and the Dells hold their own copies of this entry; this move is site Z's only.

## Left as it is, and said so

- `opalgateway` (Andrew's own account) stays user-level, so every site-Z session can still present ITS sign-in. The
  ruling names `opal-gateway-bbg` only. Narrowing `opalgateway` the same way is a separate call for Andrew.
- One user-level entry in the same file carries its credential inside the URL. Not this move's subject; stated so it
  is not found a second time by accident.
