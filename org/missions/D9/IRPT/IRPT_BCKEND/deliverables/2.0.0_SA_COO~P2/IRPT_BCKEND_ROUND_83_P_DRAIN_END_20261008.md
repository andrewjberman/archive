# L8 drain end -- IRPT_BCKEND round 83, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~20:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD by path
floor; packet only, BUILD_ONLY, nothing uploaded or applied | **Drain:** @a1f2d9f43c on box/dell2 (branch wk-IRPT_BCKEND-178) |
**Judgment criteria:** 0 | `round-close-check`: MAY-CLOSE

## IB-pr-370, slot ~178 -- E9's release packet

- **Pin P 0a57f3c0e9.** Four staged rows of `irpt-export-render` are repinned in place:
  - `repository.py` and `composition.py` to 2aa217ec58 (IB-pr-369);
  - `reporting_policies.json` to 8530114ff9 (E8, `irpt-custody-x10-v1` PENDING);
  - `lib/opal_naming.py` to b77e2af4d5. The packaged c4fedd31c5 validator rejects the new registry, so without this every
    `reporting_policy()` call would raise.
- **Census at P:** `changed_members=5`, the four rows plus `submit_installed.py` (source dir, IB-pr-369). All owned.
- **BUILD_ONLY:** from a clean tree, rc 0, built `PbyqmHBQpr4DC76qt0noBfoqKVleydNaJ7s2qsx5mT0=`. No residue.
- **Replay:** ANALYSIS and PERFORMANCE fixtures under `irpt-x10-v1`, reserved by the live zip, read back with identical
  result_sha256 through both zips. The negative control was refused by both.
- **ACTIVE answer (row D2-W178-S2, ruled D2-S8):**
  - The packaged retention admits only ACTIVE rows. With E8 PENDING, custody persist and read stay refused, which is fail closed.
  - The ACTIVE flip reaches the function only by a further repin of the registry row plus a release.
  - The issuer recommended to the CTO (msg to `1.0.0_SA_CTO~DELL2`, 20:04Z) that it ride E10's pair.
- **Graded by the issuer:** IB83-1-AC1, AC2 and AC3 PASS. Proof VALID.
- **Halves:** COO half @4e3ead72a3, signed against packet blob 1d5120c14b. The CTO half is owed. The release is the next round.

## Rows

| row | status |
|---|---|
| D2-W178-S1 | INERT: lib/opal_naming.py is the fourth repinned row, closed inside P. |
| D2-W178-S2 | Ruled by D2-S8: fail-closed sequencing, the ACTIVE repin carried to the CTO with this pair. |
| D2-W178-S3 | Ruled by D2-S8: the issuer's order named the census file differently from the check; the worker wrote both, with no grading effect. |

**Push state:** LOCAL on box/dell2; MSTR~DELL2 pushes it on its :18/:48 minutes.
