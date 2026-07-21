# Andrew-direct egress grant -- cot BD live read-only investigation (WS-E / MDPF endpoints)

**Recorded by:** 0.6.2_AE_PartnerETL · **Channel:** Andrew-direct, this session (Claude Code terminal, direct to 0.6.2_AE_PartnerETL)
**Time:** 2026-07-21T192455Z (~15:24 ET / EDT)
**XXX.md compliance:** durable record + broadcast (COO/CTO/MSTR), same turn. VERBATIM below -- the phrasing is the ruling; I do not adjudicate scope, I surface.

## VERBATIM (Andrew, sovereign)

> "You have my word for egress, please investigate freely on Cot BD through the method you used for your last brief to assess the necessary endpoints for our work on MDPF."

## What this grants (as I read it -- surfaced, not adjudicated)

- **Egress GRANTED** for cot Black Diamond investigation (my prior per-use grant @b5af1e929 was SPENT; this is a FRESH word).
- **"through the method you used for your last brief"** = the WS-E discovery method: cot READ-ONLY + LOCAL, GET/read-only calls, mint a Rebalancer bearer from the cot OIDC session (`blackdiamond/cot/session`), probe/characterize endpoints. NO mutating call, NO writes to BD/cot, NO cross-firm (never `blackdiamond/49f`).
- **"assess the necessary endpoints for our work on MDPF"** = purpose is endpoint assessment for the MDPF model-portfolio fold-in -- specifically the open item from my WS-E deliverable Sec.8/Sec.9: the explicit per-account -> model ASSIGNMENT endpoint (roster gives per-model counts; the account->model list is the missing piece).

## Boundaries that STILL bind (the egress word lifts the wire, not these)

- cot READ-ONLY throughout; zero writes; cookie/bearer in-memory only (never logged/echoed/committed).
- Firm-clean: cot only, never read the `blackdiamond/49f` partition or any bd/49F/Schwab surface.
- TRAP (banked): SSM doc `opal-cot-bronze-run` `DryRun=true` does a FULL REAL PULL + WRITES S3 -- NEVER use it; live probe is a read-only script.
- Scope of the WORD is THIS cot-BD MDPF-endpoint investigation. Any OTHER vendor egress still needs its own per-use word.

## Disposition

Investigation started this session. Findings -> WS-E deliverable update + report to CTO (WS-E production PRD input) + Andrew.
