# ANDREW'S ACT -- wall the agent accounts off Bloomberg DAPI 8194 (NFRA_OPALAI OA-f-10)

**Carded by:** `2.0.0_SA_COO~AI`, 2026-10-01. **Authority:** `1.0.0_SA_CTO~O`,
`CTO_RULING_20261001_OPAL_AGENT_DAPI_8194_WALL.md` @ff362bfa86. Under R2.2 the apply is an admin act on Andrew's
account (isolation design R1 class: OS-account and host administration), because this fabric's seats run non-elevated.
Msg 27829 amends R2.1: the acceptance measurement, taken after the apply, is the falsifier.
**This is an act, not a decision.** The ruling places it in the same sitting as G-PUSH.

## Why

`Opal_Agent`, and `Opal_MSP` on the same box, can open `127.0.0.1:8194` (DAPI) directly (OA-e-6, @5abe4f6c86). DAPI
draws on the signed-in Terminal user's limits and refuses no second OS user. The agents' sanctioned Bloomberg path
is the view server on `127.0.0.1:8790`, and that port stays open.

## The act (one elevated PowerShell, about a minute)

The script is on the local round-2 opal_ai branch, at `C:\tmp\oa-dev` @9c0a80b, built and graded under OA-f-10 (AC2
PASS). It creates no other rule and touches no account.

```powershell
# 1. In an ELEVATED PowerShell (Run as Administrator):
& 'C:\tmp\oa-dev\opal\runtime\provision\wall-dapi-8194.ps1' -Plan
#    expect exactly two lines:
#    PLAN: RULE opal_runtime_block_dapi_8194_Opal_Agent OUTBOUND BLOCK TCP 127.0.0.0/8,::1 REMOTEPORT 8194 LOCALUSER S-1-5-21-...-1007
#    PLAN: RULE opal_runtime_block_dapi_8194_Opal_MSP   OUTBOUND BLOCK TCP 127.0.0.0/8,::1 REMOTEPORT 8194 LOCALUSER S-1-5-21-...-1008
& 'C:\tmp\oa-dev\opal\runtime\provision\wall-dapi-8194.ps1'
#    expect: VERIFY: opal_runtime_block_dapi_8194_Opal_Agent OK
#            VERIFY: opal_runtime_block_dapi_8194_Opal_MSP OK
```

**Rollback, per rule:** `Remove-NetFirewallRule -DisplayName opal_runtime_block_dapi_8194_Opal_Agent`, and the same
for `_Opal_MSP`.

## After the act (not Andrew's)

`2.0.0_SA_COO~AI` respawns slot ~25 for AC3. It needs the Terminal up, and it re-measures as Opal_Agent, as Opal_MSP
and as the operator.
- **REFUSED on 8194, with 8790 OPEN and operator 8194 OPEN:** the wall stands, and the item-0 close run is unblocked
  on this precondition.
- **OPEN on 8194:** loopback is exempt here. `1.0.0_SA_CTO~O` re-rules to a raw WFP filter, and the rule is removed or
  left inert.
