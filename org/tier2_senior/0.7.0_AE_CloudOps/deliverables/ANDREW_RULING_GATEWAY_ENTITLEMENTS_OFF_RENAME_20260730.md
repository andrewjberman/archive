# Andrew-direct ruling — gateway entitlements OFF, rename proceeds unconditionally

**Received:** 2026-07-30 ~22:2xZ, site-Z terminal, direct to `0.7.0_AE_CloudOps~Z`
**Channel:** Andrew typing at the site-Z Claude Code terminal (sovereign, direct-to-worker)
**Recorded by:** `0.7.0_AE_CloudOps~Z` — same turn, per `org/XXX.md` "Andrew-direct instructions —
RECORD + BROADCAST, same turn"

## VERBATIM

> *"nobody is using this mcp anyway, we'll keep entitlements off for this gateway and rename the
> gateway anyway so it doesnt matter"*

**The phrasing IS the ruling. Do not paraphrase this into a plan and then cite the plan.**

## What it settles

Three things, and the third is the one that changes work already scoped:

1. **Usage premise inverted.** `NFRA_BBGMCP_PRD.md` §3 rests on *"this is a live OAuth endpoint
   serving real users"* and derives its whole sequencing caution from that. Andrew states nobody is
   using it. **The blast radius the caution was sized against does not exist.**
2. **Entitlements stay OFF for this gateway.** A standing configuration decision, not a temporary
   state to be "fixed" later. Anyone finding entitlements off should NOT read it as drift.
3. **The rename proceeds unconditionally** — *"rename the gateway anyway so it doesnt matter."*

## Consequence for work already committed to

I had taken **option (b)** — client-side re-registration on ONE device to prove the shape, then the
fleet — and MSTR~Z backed it (`20260730T213553Z`). That choice was justified *entirely* by
protecting live users mid-rename. **With no live users, option (b)'s justification is gone.** The
two-step is now ceremony purchased with delay, not risk reduction.

**This does NOT make the rename unconditionally trivial, and the distinction matters:** "nobody is
using it" is a statement about *client sessions*, not about *deploy mechanics*. The rename still
goes through the EC2 deploy path (`safe-ec2-deploy.sh` + `EC2_MANIFEST.json`) rather than an inline
edit, and historical session logs remain records that are not rewritten. What collapses is the
**client re-registration sweep**, not the deploy discipline.

## Scope — SURFACED, NOT ADJUDICATED

Per XXX.md, the receiving agent does not adjudicate scope. Two open questions I am explicitly
**not** deciding, and have routed to MSTR~Z:

- Whether *"nobody is using this mcp"* covers the **m365 tools Alyssa uses via the same gateway**
  (`/bbg-daily`, `/tax-pt1` and the teams-assist surface all route through `mcp__m365__*`), or only
  the Bloomberg/ycharts integrations. The tools are namespaced under the server being renamed, so
  the answer changes whether anything at all needs re-registration.
- Whether "entitlements off" is scoped to the rename window or is the standing posture.

Both were raised to MSTR~Z the same turn. **Neither blocks the rename itself.**

## Cross-reference

- PRD (MSTR-owned, to be amended by MSTR): `org/tier0_exec/0.0.0_AB_MSTR/deliverables/NFRA_BBGMCP_PRD.md` §3, §6
- Gateway server-name defect: `infra/aws/ec2/m365-mcp-gateway/app/tools.py:37` — `FastMCP("m365-gateway")`
