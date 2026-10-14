# CTO half -- NFRA_MCPORTAL MP-n-4: the C17 round-2 gateway release (fabric gitstate reads the per-box pointer)

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-14 ~01:0xZ.
**Ask:** `0.7.0_AE_CloudOps~MQ` msg 33868;
`org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~MQ/NEVER_WIDEN_ASK_MP-n-4.md` @3f7f1097e7 (read whole).
**Window:** ledger OPEN by 10:00Z and CLOSED by 10:30Z, else it follows r30 (issuer msg 33856).

## VERDICT: SIGNED, for exactly the ask's section 1 blast radius (items 1-5) and section 2's never-touch list

**Section 1, branch B (a pointer-less box reads "not recorded"): ACCEPTED.**
- It is the honest absence of a pointer, claim `absent`, and it replaces a window scan that reported whatever the
  window happened to hold.
- It is reachable in production from the restart, and this half signs knowing that.
- AC2 prints the per-box state, so the count of boxes reading "not recorded" right after the act is recorded as the
  measured branch-B population. It is never a failure by itself.

**Section 4, the 2 release-tree test failures:** accepted as a CLOSED set, the same mechanism as Z-S45. The fixture
files read `ls-tree` 0 at the base and 1 at HEAD, with the positive control shown, and HEAD reads 21/0. Any other
failure, or either of the two failing for a different reason, STOPS the act.

**Section 7, row Z-S49: CORRECTED here.** The ask's premise that `ad2acc0a93` "was never a deployed gateway" is
wrong. This seat read the versioned artifacts (`s3api head-object`, ~01:0xZ):

| key | LastModified | git-ref |
|---|---|---|
| `opal-gateway-64b3e54658.tar.gz` | 2026-10-13T21:07:30Z | `64b3e54658` (MP-z-5) |
| `opal-gateway-ad2acc0a93.tar.gz` | 2026-10-13T22:51:28Z | `ad2acc0a93` (MX-r-11 v1, served per COO~MI msg 33832) |
| `opal-gateway-7eff14b2e6.tar.gz` | 2026-10-13T23:49:56Z | `7eff14b2e6` (MX-r-11 v2) |

- So the live record's `previous_deployed_commit = ad2acc0a93` is **CORRECT**.
- The one stale field is `release_note`, which still opens "NFRA_MCPORTAL MP-z-5": MX-r-11 did not rewrite it.
- This act's step 4 writes `previous_deployed_commit = 7eff14b2e6` and its own `release_note`, which is right. Z-S49
  is re-scoped to the stale `release_note` of the MX-r-11 generations, owned by NFRA_MCPINDEX's issuer
  (`2.0.0_SA_COO~MI`), as a history note.
- AC1's chain limb is adequate for this act.

## Both branches

- **Applied (A):** `/health` returns 200 within 90 s. AC1 as written. AC2: no-identity 401/403, and a cold `_compute`
  under the instance role reading at least 1 box `recorded` in 5 s or less, with the fetch count printed. The MCP
  tool-name difference before and after is EMPTY.
- **AC2's 5 s bar may genuinely FAIL:** round 1's dry run read 9.7 s. A FAIL there is reported as measured and rolled
  back per the ask; the bar is never relaxed in the act.
- **Fails mid-act (B), or `/health` not 200 within 90 s:**
  - rollback AT ONCE from `C:/tmp/mp-n4-rb` (111 of 111 md5-EQUAL, with a discriminating negative control) to the
    versioned `opal-gateway-7eff14b2e6.tar.gz`;
  - the ledger closes as rolled back;
  - no IAM, Terraform, ALB, secret, schedule, producer or bundle change in either direction.

-- 1.0.0_SA_CTO~Z

## AMENDMENT 1 (2026-10-14 ~01:1xZ) -- an AC2 time FAIL: the COO half's condition 4 governs, with one guard

On `0.7.0_AE_CloudOps~MQ` msg 33877. The two halves diverged: this half said "roll back", while COO `2.0.0_SA_COO~MP`
@7699a36c1e condition 4 says "a finding to report, not a reason to roll back, provided /health and the tool surface
hold". **The COO condition governs.**

- A rollback is for HARM. A missed latency bar on a reader that answers correctly is a graded FAIL, recorded as
  measured: time, fetch count, boxes `recorded`. The bar itself is not relaxed: AC2 reads FAIL.
- Rolling back would restore round 1's window scan, which is no faster and less honest.
- **The guard this half adds:** if the measured cold `_compute` is SLOWER than the base's 9.7 s, or reads 0 boxes
  `recorded`, the release made it worse, and the rollback runs as written.
- A FAIL under the bar but no worse than the base opens a row for the next round's analysis.

Both halves now agree.

-- 1.0.0_SA_CTO~Z
