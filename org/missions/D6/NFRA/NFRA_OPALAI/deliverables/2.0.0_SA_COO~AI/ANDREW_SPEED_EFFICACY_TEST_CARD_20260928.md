# Andrew's speed and efficacy test card -- before Alyssa gets Menachem's entitlements

For: Andrew, in your own Claude (server `opal-gateway`, https://mcp.opalinvest.dev/mcp). Prepared by
`2.0.0_SA_COO~AI` on `1.0.0_SA_CTO~O` msg 26223, 2026-09-28 ~5:45 PM ET. Every fact below was measured against the
live gateway, not recalled.

## 1. What is live for you right now

The gateway serves commit `6a98a0553a` (OG-s-1; CORRECTED from `fe94911257`, an ancestor with identical app files, on
`1.0.0_SA_CTO~O` msg 26242 and `2.0.0_SA_COO~O`'s measurement @e992df46c4). The live integration switch is `ENABLED_INTEGRATIONS=ycharts opal_portal
globgrph`, read over SSM from `/opt/opal-gateway/.env`, the service's only environment file.

| Group | Live now | Tools |
|---|---|---|
| Teams, email, files, calendar (native) | YES, 37 tools | `whoami`, email (9), OneDrive/SharePoint (16), Teams (10), `opal_asker_query` |
| Portal answers scoped to a Teams asker | YES | `opal_asker_query` (needs a Teams `chat_id` + `message_id`; it scopes to that message's SENDER) |
| YCharts | YES, 6 | `ycharts_search`, `_snapshot_metrics`, `_time_series`, `_fund_series`, `_risk_return_scatter`, `_freshness` |
| Estate graph | YES, 2 | `graph_cypher`, `graph_status` |
| Data refresh upload | YES, 1 | `opal_data_refresh_upload` |
| **Schwab account data (NFRA_OPLGTW)** | **NO** | `schwab_get_access`, `schwab_list_files`, `schwab_describe_dataset`, `schwab_query`, `schwab_prepare_download`: `schwab` is not in the switch |
| **Discovery and index (NFRA_MCPINDEX)** | **NO** | `opal_discover`, `opal_describe`, `mdpf_get_aum_metrics`, `mdpf_get_account_distribution`, `mdpf_get_aggregate_aua`: not in the switch |

Your identity is unscoped: the tool allowlist never includes your key (`app/identity_scope.py:12-14`), and you have no
entitlement profile, so every legacy tool passes. **Even after `schwab` is switched on, a user with no profile sees
no Schwab tool** (`app/data_entitlement.py:41-42`). To test Menachem's kind of question at the account level, two
steps come first: the switch is turned on (OPLGTW's switchover), and you hold a grant like his.

**So today, "which clients hold which Opal assets" can be answered only at the PORTAL level:** model and account
distribution, and account units, through `opal_asker_query` on the catalog keys
`platinum/mdpf/{scope}/account-distribution.json`, `platinum/mdpf/global/non-model-assets.json` and
`platinum/mdpf/cottonwood/account-units.json`. It cannot reach client accounts.

**One catch, checked by `2.0.0_SA_COO~AI` in the code:** `opal_asker_query` scopes the answer to the SENDER of the
Teams message, and it refuses a sender with no active profile (`app/asker_scope.py:160-167`, code `asker_no_profile`).
You have no profile, so a question YOU post is refused. That is the correct refusal, not a fault. To time Q1-Q3 for
real, pick one:
- (a) you get your own portal-only grant through the existing operator path, the same shape as Alyssa's (the COO
  writes it on your word); or
- (b) Alyssa, whose portal-only grant is ACTIVE today, posts Q1-Q3 in a chat with you, and you ask Claude to answer
  her messages.
Either way, first post one question yourself and time the refusal. That is Q0 below.

## 2. Questions to type (Menachem's kind)

Q1-Q3 use `opal_asker_query`: the question is posted in a Teams chat by a PROFILED sender (see the catch above), then Claude answers that message. Q4-Q5 test
the account level; today the correct result is a plain "not available", given fast.

| # | Type this | Expected tool | A correct answer shows |
|---|---|---|---|
| Q0 | Post Q1 yourself, then ask Claude to answer it | `opal_asker_query` | today: refused `asker_no_profile`, with the how-to-get-access line, fast |
| Q1 | "How many accounts hold each Opal model portfolio, by firm?" | `opal_asker_query`, key `account-distribution` | counts per model per firm, the as-of date, and "source: portal MDPF platinum" |
| Q2 | "Which Opal assets do <a firm you know> clients hold outside the models?" | `opal_asker_query`, key `non-model-assets` | assets with amounts, the as-of date, and the firm scope named |
| Q3 | "How many units of each model do Cottonwood accounts hold?" | `opal_asker_query`, key `cottonwood/account-units` | units per model, the as-of date, and the source |
| Q4 | "Which of <a client you know>'s accounts hold <an Opal model>?" | `schwab_query` (not live) | today: says plainly that account-level Schwab data is not available; never guesses |
| Q5 | "List every client holding <an Opal fund>, with their position size" | `schwab_query` (not live) | today: the same plain decline, naming who to ask |

## 3. What to time, per question

Start the clock when you press Enter.

| # | (a) sec to first tool call | (b) sec to full answer | (c) tool calls | (d) as-of date + source named (y/n) | (e) correct vs what you know (y/n) |
|---|---|---|---|---|---|
| Q0 | | | | | |
| Q1 | | | | | |
| Q2 | | | | | |
| Q3 | | | | | |
| Q4 | | | | | |
| Q5 | | | | | |

## 4. What happens next

Your timings feed E8 (the stage-by-stage speed read, OA-e-8). Once you are satisfied, Alyssa's grant widens to the same
entitlements as Menachem's approved G-E grant (your G-ASKER word). Q4-Q5 are re-run once `schwab` is switched on.
