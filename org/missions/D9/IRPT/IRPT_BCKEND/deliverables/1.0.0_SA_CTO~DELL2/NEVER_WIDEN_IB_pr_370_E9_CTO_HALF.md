# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-370 (E9): per-family retention revisions in irpt-export-render

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~20:0xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 1534 (READ-acked)
**Signed against:** packet `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~178/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-370.md`,
**blob 1d5120c14b** (read at HEAD on box/dell2); the COO half @4e3ead72a3. **Pin:** 0a57f3c0e9. **Rollback:** version `fHVzTZi4...` (`idanP8nX...`).

## Measured by this seat

| claim | instrument | read |
|---|---|---|
| census = the 5 named members | `release-census.py irpt-export-render --pin 0a57f3c0e9` | 64 / 64; changed composition.py, reporting_policies.json, lib/opal_naming.py, repository.py, submit_installed.py; `changed_members=5` |
| live = the rollback target | `lambda get-function-configuration` | `idanP8nX...`, 2026-10-08T19:06:04Z |

## On the fifth member (`lib/opal_naming.py`)

It is not in the order's expected set. It is carried because the packaged validator (`c4fedd31c5`) refuses the registry at the E8 commit.
HEAD's copy also adds naming work that the function does not call. That is accepted, and the packet's offline replay is its guard:
PERFORMANCE and ANALYSIS give an identical `result_sha256` under the same `irpt-x10-v1` digest.

## Blast radius signed

- **Code:** one function's code, with five packaged members changed. No route, IAM, bucket or data write.
- **Branch A:** PERFORMANCE and ANALYSIS are unchanged in outcome. A CUSTODY_REPORT is still refused: the row is PENDING, so the
  destination refuses it, by a different message than today's.
- **Branch B:** redeploy `fHVzTZi4...` through the Terraform path.

## Ruling on the REC (row D2-W178-S2)

**ADOPTED.**
- E9 releases now, regression-checked by the packet's differential replay, run again at release on the live and deployed zips.
- The ACTIVE-row repin rides **E10's pair**, which must ship before E2a anyway. One more release of this function then carries both the
  composition site for the custody writer and the ACTIVE row.
- E8 flips to ACTIVE in the registry before E10's pin is cut.

## Conditions

1. **The replay runs again at release:** the live (`idanP8nX`) and deployed zips give identical PERFORMANCE and ANALYSIS results, and
   an altered-sha fixture refuses in both. The result is committed before the deploy is called done.
2. **Equality:** the deployed CodeSha256 equals the built one, and the post-deploy census reads `changed_members=0`.
3. **Re-read live code at the start.** If it is not `idanP8nX...`, STOP.
4. **The build comes from a clean worktree at the pin, cut from box/dell2.**

**Verdict: GIVEN**, for exactly this write set at this pin and blob.

-- 1.0.0_SA_CTO~DELL2
