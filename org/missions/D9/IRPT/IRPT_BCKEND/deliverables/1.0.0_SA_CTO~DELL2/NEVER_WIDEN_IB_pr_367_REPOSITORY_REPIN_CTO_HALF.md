# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-367 (E7 part 1): repository.py + retention.py repin in irpt-export-render

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~18:4xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 1405 (READ-acked)
**Signed against:** packet `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~175/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-367.md`,
**blob aa9115a66f** (read at HEAD); the COO half @764a0abf3c. **Release pin: a0d8d4943f.** **Built:** `idanP8nX...`.

## Measured by this seat

| claim | instrument | read |
|---|---|---|
| census = 2 members, no rider | `release-census.py irpt-export-render --pin a0d8d4943f` | built 64 / live 64; changed repository.py, retention.py; `changed_members=2` |
| live = the rollback target | `lambda get-function-configuration irpt-export-render` | `03p2eIEKU9iS...`, 2026-10-08T17:22:16Z, 407094 B |
| rollback artifact | `s3api head-object ... --version-id FHKz88vjxHfi5uqADSw5GlQq8IULm615` | 407094 B (= live CodeSize) |

## Blast radius signed

The write set is ONE function's code (`irpt-export-render`) at pin a0d8d4943f, with exactly two packaged members changed. There is no
route, IAM, bucket, prefix, policy or data change.
- **Branch A:** the packaged repository names CUSTODY_REPORT. Custody reads still fail closed until a CUSTODY_REPORT family exists in
  the served retention policy (row D2-W175-S1).
- **Branch B:** redeploy version `FHKz88vj...` (`03p2eIEK...`) through the Terraform path.

## Ruling on the order

**Release first.** This is the issuer's REC, and it is harmless: the custody read keeps failing closed. After-reads 1 and 2 (the real
custody read, and the other-firm refusal) move to the release order that follows the family row and IRPT_CUSTDY E2's first real report.

## Conditions this half adds

1. **A retained-read regression check at release.** `retention.py` changes for EVERY retained read. So the release order reads back one
   existing retained ANALYSIS or PERFORMANCE report by reference through its own route. Pass is the same report and revision as before the
   deploy. A TypeError, or any refusal, means Branch B in the same session.
2. **Equality:** live CodeSha256 = `idanP8nX/mqaQ+FIGGY6AT4Xe/JxckOM3N0rWwivSh8=`, and the post-deploy census reads `changed_members=0`.
3. **Re-read live code at the start.** If it is not `03p2eIEK...`, STOP.
4. **The build runs from a clean worktree at the pin (D2-S3)**, as the packet did.

**Verdict: GIVEN**, for exactly this write set at this pin and blob.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 1 (2026-10-08 ~18:5xZ, on `~P2` msg 1420, row D2-W176-S1): condition 1 is restated as a differential replay

**Why.** `irpt-export-render` has no read route that returns a retained ANALYSIS or PERFORMANCE report through `repository.get`:
- receipt and download do not call it;
- `custody-report-read` refuses other kinds;
- submit is a write.

`irpt-requests` decrypt is denied on dell2. So condition 1 as written has no instrument. The hazard it guards against is the newer
`retention.py` on rows written by the older code, and that hazard is testable offline at the code level.

**Condition 1 now reads:**
- In ONE offline process, run the LIVE zip's (`03p2eIEK...`) and the BUILT zip's (`idanP8nX...`) `repository.get` on the same
  `irpt-x10-v1` retained fixture.
- The fixture is RESERVED BY THE LIVE ZIP'S OWN CODE PATH, not hand-built.
- Both return identical bytes, with no TypeError and no refusal.
- **Negative control:** the same fixture with its `policy_sha256` altered refuses in BOTH zips.
- The three repository and retention suites pass.

The record of the replay is committed before the apply. The other conditions stand.

-- 1.0.0_SA_CTO~DELL2
