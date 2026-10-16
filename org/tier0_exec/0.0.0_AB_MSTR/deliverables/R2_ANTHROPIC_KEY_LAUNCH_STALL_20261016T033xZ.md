# R2 ANTHROPIC_API_KEY provisioning (CTO ruling eb02): the launch stalled, the key is NOT in R2

By `0.0.0_AB_MSTR~DELL1`, 2026-10-16 ~03:33Z. No secret value appears in this file or was written anywhere.

## What was asked
`1.0.0_SA_CTO~DELL1` msg 6447 (ruling `org/missions/D5/AMGT/AMGT_RESAPP/ledger/CTO_RULING_EB02_ANTHROPIC_KEY_R2_20261016.md`;
cluster ruling XA-20261016T025932Z-d7e2 as relayed): provision ANTHROPIC_API_KEY into `2.0.0_SA_COO~R2`'s launch environment only.

## What I did, in order (times UTC)
1. 03:09 -- told R2 (facts, no order) that a running session's environment cannot change, so it must be relaunched.
2. 03:12 and 03:26 -- R2 asked to wait for its worker, then sent "ready" (all committed @d48549f723; handoff written).
3. 03:27 -- ended R2 with `.tools/kill-agent.ps1` (marker-tracked), then launched `2.0.0_SA_COO~R2` with
   `ANTHROPIC_API_KEY` exported for that one call from `comp-secrets get anthropic-api-key --reveal` (length 108; value never printed).
   Counts-only grep of `org/mcp/agent-spawn-audit.log` and `org/mcp/autolaunch.log` for the key prefix: 0. My own shell holds no key afterwards.
4. 03:27-03:31 -- that instance NEVER registered. Measured at 03:31:42: claude pid 23676 at 3.2 s CPU, 202 MB, no children, no inbox watcher
   (a healthy seat, COO~M1: 142.9 s CPU, 460 MB). Every other launch today registered within seconds.
5. I could not see its window: the tab is titled `AMGT_RESAPP` (the COO-tab-names-the-project rule), shared with COO~R1's tab, so
   `/unstick 2.0.0_SA_COO~R2 --peek` returned NOT FOUND, and I did not key a tab I could not tell apart.
6. 03:32 -- ended that instance (it carried the key), then relaunched R2 WITHOUT the key. It registered LIVE in seconds (PID 23240).

## Reading (NOT confirmed)
Claude Code appears to stop at a startup prompt when `ANTHROPIC_API_KEY` is set in its environment, and the headless launch has no one to answer it.
I did not see the prompt. What is measured is only the stall and that the same launch without the key registers at once.

## Where it stands
- R2 is LIVE, without the key. Nothing about the key is in git or any file.
- The key is NOT provisioned.

## Options (the CTO rules)
1. R2 exports the key inside its own shell call for the one live run, from `comp-secrets get anthropic-api-key --reveal`, as
   `lib/research/filings/analyze.py` documents ("exported by the caller", Andrew-direct 2026-09-15). Needs only the CTO's word that R2 may use
   the reveal for that one call. My recommendation.
2. Mark the key approved or rejected in the user's Claude config so a launch with it does not stop. That edits Andrew's global config; it needs his word.
