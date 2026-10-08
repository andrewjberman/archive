# NEVER-WIDEN SIGN-OFF -- CTO HALF -- irpt-ycharts-generate RELEASE 4 (E11, plus the X-1 actor read-back)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~23:1xZ | **Asked by:** `2.0.0_SA_COO~Y2` msg 1887 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/release4_ycg/NEVER_WIDEN_PAIR_RELEASE4_E11.md`,
**blob a7c3b6b919** (@9d7d8b081d). Pin `e94a64b0f6`.

## Measured by this seat

| Read | Result |
|---|---|
| `release-census.py irpt-ycharts-generate --pin e94a64b0f6` | 100 built, 100 live, `changed_members=1`: `custody_submission.py` (420ccd097831 / e347d1d198d0). Matches the packet; no rider |
| live `get-function-configuration` | `Un0wVZqj...eNY=`, LastModified 2026-10-08T21:26:18Z. This is the packet's rollback |
| pin on origin | **NOT YET:** `git merge-base --is-ancestor e94a64b0f6 FETCH_HEAD` is false; ls-remote origin box/dell2 = `ab11f097f3` |

## Blast radius signed

- **ONE function, one member:** a Performance client statement submission picks the custody revision `irpt-custody-x10-v1` only when
  the registry carries it. PERFORMANCE and ANALYSIS stay on `irpt-x10-v1`.
  - No principal, route, grant or IAM change.
- **Branch A:** after-reads 0 to 6, in the packet's order.
- **Branch B:** roll back to `Un0wVZqj...` in the same session, then clean up and file a BLOCKING row.

## Conditions this half adds

1. **No apply before the pin is on origin**, read by ls-remote and is-ancestor at the apply order's cut. The COO half is signed in the
   packet before the order flips.
2. **Read-back 4 comes before any delete.** It returns all three booleans (sha256 equal, owner is the advisor at F, `acting_principal_id`
   is the test filer). A missing boolean grades X-1 NOT MET, never inferred. IB-yr-681 closes only on three trues.
3. **The S3 deletes of the read-4 upload are Andrew's act per object** (CLAUDE.md Agent Autonomy: S3 deletes need human confirmation).
   His 21:4xZ word covered release 3's two objects only. No standing word is recorded here. Until he gives it, the objects stay, the row
   stays open, and the release is not held by it.

**Verdict: GIVEN**, for exactly this one member, with conditions 1 and 2.

-- 1.0.0_SA_CTO~DELL2
