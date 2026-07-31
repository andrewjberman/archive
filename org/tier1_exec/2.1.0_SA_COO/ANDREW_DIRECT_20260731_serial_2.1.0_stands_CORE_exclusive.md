# ANDREW-DIRECT -- 2026-07-31, COO terminal (site Z). Serial ruling + fabric scope.

**Recorded by:** `2.1.0_SA_COO`. **Channel:** direct, at my terminal, mid-turn.
**Recorded same turn as received**, per `org/XXX.md` "Andrew-direct instructions -- RECORD + BROADCAST".

## VERBATIM

> "Yes MSTR shoudlve spawned you as 2.0.0_SA_COO~Z but they used the extra 2.1.0_SA_COO identity, which
> is fine, no need to change that at this point just run it as 2.1.0_SA_COO as youre already running.
> With that said, yes you are exclsively on the CORE side of NFRA_VELOCITY, 2.0.0_SA_COO is handling the
> other fabric on the ESTATE side."

## What this settles

1. **My serial is `2.1.0_SA_COO` and it STANDS.** The site-Z convention would have produced
   `2.0.0_SA_COO~Z`; MSTR used a separate identity instead. Andrew has ruled that acceptable and
   explicitly declined a re-spawn or rename. **Do not "correct" this serial.**
2. **Scope: NFRA_VELOCITY_CORE, exclusively.** `2.0.0_SA_COO` holds NFRA_VELOCITY_ESTATE on the main
   fabric. Two COO seats, two fabrics, one program. This matches LD-0365 ("COO respawn + formal
   TO-decomposition, both NFRA_VELOCITY fabrics").
3. **I authored one commit attempt as `2.0.0_SA_COO~Z` before this ruling and it did not land** (blocked
   by the owned-paths gate). That serial belongs to a LIVE PEER working ESTATE. The attempt was wrong;
   it is recorded here rather than quietly dropped. Nothing was committed under it.

## What this does NOT settle -- the live blocker, now escalated

`2.1.0_SA_COO` is a **pre-existing CompLearns (COMP/CL) fabric serial**, and two independent gates still
classify me as CL:

| Gate | Location | Behavior |
|---|---|---|
| COMP branch isolation | `.tools/git-hooks/install-mstr-ledger-check.sh:65` -- `comp_re` literally lists `2\.1\.0_SA_COO` beside `1\.1\.0_SA_CTO` / `3\.1\.0_SA_CVO` | `BLOCKED: COMP-serial author '2.1.0_SA_COO' must commit to COMP branch (currently on 'CLOUD')` |
| owned-paths lane | owned-paths registry | `org/tier1_exec/2.1.0_SA_COO/` -> `lane=COMP_LEARNS`; a non-CL agent is refused, and so is a CL agent writing CORE content on CLOUD |

**Both gates are behaving correctly against a stale premise.** They encode "2.1.0_SA_COO is CompLearns,
CL is paused (LD-0222), CL content stays on COMP." Andrew's ruling makes the serial a site-Z CORE seat on
CLOUD. **The gates have not been told.**

**This is a grantor action and I am the grantee -- I do not amend the gate that governs me** (the SoD
MSTR itself applied at `0e696c4eb`: "CRO grantee / MSTR grantor -- SoD"). Requested of `0.0.0_AB_MSTR~Z`:

- add `2.1.0_SA_COO` to the CORE/site-Z lane in owned-paths (`org/tier1_exec/2.1.0_SA_COO/**`, plus the
  AE task_orders paths a COO must write TOs into), and
- remove `2\.1\.0_SA_COO` from `comp_re`, or carve it explicitly, so the branch-isolation rule stops
  claiming a serial Andrew has re-pointed at CORE.

Until that lands, COO commits on CLOUD require an audited override -- which is a record, not a fix.
