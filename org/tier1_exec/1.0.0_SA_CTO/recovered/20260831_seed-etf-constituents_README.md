# RECOVERED, UNLANDED: seed-etf-constituents.py (ETFS_POSITIONING / D4)

**Captured:** 2026-08-31 ~21:4xZ by `1.0.0_SA_CTO~Z`
**Patch:** `20260831_seed-etf-constituents_uncommitted.patch` (2,396 B)
**Target:** `infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-constituents.py`

## Why this patch exists instead of a commit

The work is REAL and it is NOT LANDED. `1.0.0_SA_CTO~Z` **cannot** land it: the path is owned by
lane `YANG_PIPELINE_DEPLOY`, whose `permitted_agents` are the AE `CLOUD_OPS_OR_ETL` set plus
`0.2.0_DT_PortfolioAnalytics`, `0.8.0_AE_CloudComp` and `0.2.0_DS_PortfolioAnalytics`. This seat is
in none of them, and `safe-commit.sh` refused (audited BLOCK, 2026-08-31T21:38:37Z).

**The refusal is CORRECT and was NOT overridden.** `GIT_COMMIT_AUTHOR_OVERRIDE` exists for exactly
this, and it was deliberately not used: this seat is the CTO **arch-gate** for that lane, and a seat
bypassing a lane it gates is self-dealing regardless of whether the change is good. The lane's own
doctrine also says a REPEAT override for a standing action is a **coverage gap to close**, not an
escape to keep using.

## Provenance of the work

Authored by this seat's predecessor before the 2026-08-31T17:04:47Z reboot; found dirty on the shared
worktree by `0.0.0_AB_MSTR~Z`'s 21:13Z integrator sweep. It had already survived one restart by luck.
Independently backed up by MSTR~Z (their copy and this patch agree at 2,396 B).

## What it contains

1. **The canonical cash line.** Andrew-direct 2026-08-25, verbatim in the code: *"it should always be
   managed the same way: Fixed Income for Asset Class, Ultra Short Duration for Sub Asset, CASH for
   ticker, and Cash & Cash Equivalents for Name"*. Collapses the CASH / CASH&OTHER split onto one row.
2. **An empty-string drop in the batch writer.** `sub_asset_class` backs the `sub-asset-class-index`
   GSI and DynamoDB refuses an empty string for an indexed key attribute; the predecessor recorded
   *"measured: ValidationException on the first real write"*. A real production defect fix.

## What was VERIFIED before capture (so the next seat need not redo it)

Exercised by importing the module, not read off the comment:

```
clean_name("Cash&Other", "Cash & Other") -> 'Cash & Other'
clean_name("CASH",       "whatever")     -> 'Cash & Cash Equivalents'
```

The lookup uppercases (`NAME_CORRECTIONS.get(ticker.strip().upper())`), so the deleted `CASH&OTHER`
row **was** live for the mixed-case `Cash&Other` ticker present in the pull artifacts -- removal is
not trivially a no-op. It is nonetheless **behaviour-preserving**, because the fallback
(`normalise_trailing_article(issuer_name)`) returns the exact string the deleted correction supplied.
**The served name is unchanged for that ticker under both truth values of the comment's claim.**

## What is NOT verified -- do not launder this into the record

The shipped comment asserts *"the producer normalises BOTH the derived residual row and the issuer
sentinel onto this ticker, so CASH&OTHER no longer reaches the served artifact"*. That was **NOT**
confirmed against the served artifact. It is not load-bearing (see above), but it is an unproven
claim living in a code comment. The producer's own source at
`data/etfs/scripts/gold/etf_positioning_gold.py:1367-1370` says something narrower: the DERIVED row
is deliberately ticker `CASH` and deliberately NOT the issuer's `CASH&OTHER`, to keep given-vs-derived
distinguishable. That is about the derived row and does not establish the sentinel's disappearance.

## Scope -- committing is not deploying

`seed-etf-constituents.py` is a **hand-run seeder** (`def main() -> int`, `if __name__ == "__main__"`),
not a scheduled Lambda handler. Landing it changes **no served behaviour**. Running it against the
live `etf-classifications` table is a separate deliberate act, and no seat has taken it.

## An audit gap found while checking this, NOT resolved

`org/git-author-override-audit.log` carries four **BLOCK** rows for this exact path on 2026-08-25
(17:38:49 / 17:39:23 / 17:39:53 / 17:40:13Z) and **no OVERRIDE row**. Commit `b3d830094c` then landed
at 17:41:12Z on this path under the `1.0.0_SA_CTO~Z` author line -- about one minute after the last
block. **The route it took is UNDETERMINED and I am not naming one.** An unlogged override and a
non-wrapper commit are byte-identical in this log, which is the point: a negative result that cannot
show its own observation is indistinguishable from a missing observation. Surfaced, not chased.

## How to land it

A seat in `YANG_PIPELINE_DEPLOY` applies and commits:

```
git apply org/tier1_exec/1.0.0_SA_CTO/recovered/20260831_seed-etf-constituents_uncommitted.patch
```

Alternatively `2.0.0_SA_COO~Z` (grantor; SoD -- the grantee never commits its own grant) may close
the lane-enumeration gap, with CTO arch-gate. **At capture time no live seat on site Z was in that
lane** -- the fabric was MSTR~Z, CTO~Z, COO~Z and none is a member.
