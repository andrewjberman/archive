# U1 -- where Claude Code exposes the signed-in account and the 5-hour / weekly limits (site Z)

Measured on site Z (this box) only. The laptop, dell1 and dell2 were not reachable from this cell; every figure below is
UNMEASURED on those three boxes (the file layouts are the same install, so they are expected to match, but that is an inference).

## Finding

**Account (email, plan, organization): measured, no credential needed.** `claude auth status` (default JSON output, local,
non-interactive) printed `loggedIn`, `email`, `orgId`, `orgName`, `subscriptionType` ("max") and no token. The same fields
are in the `oauthAccount` object of `~/.claude.json` (keys include `emailAddress`, `organizationName`, `organizationType`
= claude_max, `billingType` = stripe_subscription, `organizationRateLimitTier`, `userRateLimitTier`, `seatTier`). A build cell
reads `~/.claude.json` `.oauthAccount` (or runs `claude auth status`) and copies only those named non-secret fields.
`~/.claude/.credentials.json` holds the tokens (key names only: `claudeAiOauth` with an access token, refresh token, expiry,
scopes, `rateLimitTier`, `subscriptionType`; and `mcpOAuth`). A build cell must never open it.

**5-hour and weekly remaining: NOT readable from a file or a command without a credential on this box.** The installed
`claude.exe` (269 MB, strings read; no value seen) shows two routes, both inferred. (1) The status-line command receives a JSON
object on stdin whose `rate_limits` member holds `five_hour` and `seven_day`, each `{used_percentage, resets_at}`, built from
the usage endpoint's `utilization` and `resets_at`. This is the best credential-free route: a status-line script runs inside
the box's own session and sees only percentages and reset times, never a token. No `statusLine` is configured in this box's
`~/.claude/settings.json`, so it was not exercised; remaining = 100 - used_percentage. A build cell would ship a status-line
script that writes `rate_limits` to a small local file per box. The member is only present for a subscription login after the
first API response, so absence of the member is itself a claim to carry. (2) The Anthropic API response headers
`anthropic-ratelimit-unified-5h-utilization`, `-5h-reset`, `-7d-utilization`, `-7d-reset` (plus `-status`, `-representative-claim`,
`-overage-*`) are named in the binary; reading them needs a live API call, so they are not usable by a read-only box probe.
The interactive `/usage` and `/status` views presumably show the limits; the cell cannot type a slash command, so what they
print is unmeasured. The usage endpoint behind the status line needs the OAuth token, so a poller of our own would hold a
credential and is rejected as a source.

**Repository:** no `.tools` or `org/mcp` file mentions `oauthAccount`, `anthropic-ratelimit` or `rate_limits` (native Grep, 0 files in each).
The repo-wide `comp-find -i 'ratelimit|rate_limit|usage|oauthAccount' --files --limit 30` did not finish in 120 s (filed as a
row), so the whole-repo sweep is UNREAD, not zero.

```json
{"sources": [
 {"source": "claude auth status (CLI, JSON output)", "exposes": ["account"], "how_read": "run `claude auth status` under timeout 20; read email, orgName, subscriptionType from stdout JSON", "box_measured": "sitez", "claim": "measured", "reason": "returned loggedIn true with email, orgId, orgName and subscriptionType max on site Z; no token field in the output"},
 {"source": "~/.claude.json oauthAccount object", "exposes": ["account"], "how_read": "parse the file as JSON and read only emailAddress, organizationName, organizationType, billingType from .oauthAccount", "box_measured": "sitez", "claim": "measured", "reason": "keys seen on site Z; organizationType claude_max, billingType stripe_subscription; the file is world-readable and holds no token in this object"},
 {"source": "Claude Code status-line stdin JSON (rate_limits.five_hour / seven_day)", "exposes": ["limit_5h", "limit_weekly"], "how_read": "configure a statusLine command in settings; it receives JSON on stdin with rate_limits.five_hour and rate_limits.seven_day each carrying used_percentage and resets_at; the script writes those two members to a local file for a probe to read", "box_measured": "none", "claim": "inferred", "reason": "field names read in the installed claude.exe strings (used_percentage, resets_at, five_hour, seven_day, rate_limits, rate_limits_available); no statusLine is configured on site Z so no value was seen; the member may be absent before the first API response"},
 {"source": "Anthropic API response headers anthropic-ratelimit-unified-5h/7d-*", "exposes": ["limit_5h", "limit_weekly"], "how_read": "headers on the model API response (5h-utilization, 5h-reset, 7d-utilization, 7d-reset); only a live API call returns them", "box_measured": "none", "claim": "inferred", "reason": "header names appear in the installed claude.exe; reading them needs a network call with a credential, which this cell may not make, and a box probe should not hold"},
 {"source": "~/.claude/.credentials.json", "exposes": [], "how_read": "NOT to be read: key names only (claudeAiOauth, mcpOAuth)", "box_measured": "sitez", "claim": "absent", "reason": "holds tokens, not account or limit figures; excluded as a source"},
 {"source": "claude --help and auth subcommand help", "exposes": [], "how_read": "claude --help; claude auth --help (login, logout, status)", "box_measured": "sitez", "claim": "absent", "reason": "no usage or limits subcommand; interactive /usage and /status output unmeasured because a slash command cannot be typed from this cell"},
 {"source": "this repository (.tools, org/mcp)", "exposes": [], "how_read": "native Grep for oauthAccount, anthropic-ratelimit, rate_limits", "box_measured": "sitez", "claim": "absent", "reason": "0 files in .tools and 0 in org/mcp; whole-repo comp-find timed out, so wider absence is unread"}
]}
```
