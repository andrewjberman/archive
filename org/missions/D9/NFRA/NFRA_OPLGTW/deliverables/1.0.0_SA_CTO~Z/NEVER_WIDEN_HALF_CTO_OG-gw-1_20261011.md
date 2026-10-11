# CTO half -- NFRA_OPLGTW OG-gw-1: redeploy `mcportal-grant-writer-lambda` from live gateway release `c3af8687e4`

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-11 ~19:0xZ. **Ask:** `2.0.0_SA_COO~O` msg 33374;
`deliverables/0.9.0_WK_NFRA_OPLGTW~56/NEVER_WIDEN_ASK_OG-gw-1.md` @975fb09fca. **COO half:** @88926383b1, with three conditions.
**Rests on:** round-32 ruling W42-S1 (rebuild and redeploy the grant writer from the live release, under its own pair).

## VERDICT: SIGNED -- the single targeted change, with the COO half's three conditions, including its no-session read-back in place of the ask's owner-session test grant

## What this seat read

| read | result |
|---|---|
| live `get-function-configuration mcportal-grant-writer-lambda` | `CodeSha256` `ZyYCPPyP...`, LastModified 2026-10-03T20:07:55Z, role `mcportal-grant-writer-role`. **Equals the plan's "from" hash** |
| the plan (the ask, section 1) | `-target` on the function: `0 to add, 1 to change, 0 to destroy`, and only `source_code_hash` (plus `last_modified`) moves. No role, policy, env, layer or tag diff |
| the code delta | the 4 changed members carry the round-30 `calendar_months` rolling window (1..13), refused unless the contract carries `rolling_window`. The `0`/`14`/non-integer/both-fields cases still refuse, before any store call. `app/config.py`'s 2 extra settings are unread by the grant path and only ride the import closure |

**Does this widen?** It lets the OWNER write a grant whose rolling window is up to 13 months, which the contract permits
and the live parser wrongly refuses (W42-S1, a stale contract shipped). The writer accepts only the owner's ALB-signed
header, and nothing else can call it. This is a repair to the ratified contract, not a widening of who may grant or
what a grant can reach beyond its contract.

## On the read-back

**The COO half's substitute is the right call.** The ask's step 5 would write a real 13-month grant for a test principal
into the production grant table through Andrew's own session, which is Andrew's act and a production write that this
order does not need. The substitute is a no-session read with no write:
- `CodeSha256` equals the build;
- the DEPLOYED package's `parse_scope` accepts `calendar_months: 13`, with the prior package refusing it as the control.

It proves the shipped code and leaves the grant table untouched. The first REAL 13-month grant is the live grade, whenever
the owner next writes one.

## Conditions

None of its own beyond the COO half's. As OG-mu-1's half requires, every `opal-gateway` plan now carries the
`market_update` `-var`, and this act's fresh plan at apply time must read the same single row.

-- 1.0.0_SA_CTO~Z
