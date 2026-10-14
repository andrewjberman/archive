# Never-widen half (COO) -- OG-mg-1, the r30 grant writes (R1 Andrew, R2 the Bloomberg mirror)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-14 ~02:4xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-mg-1.md` @189bbbb8d2 (Phase A under
A1-A3; mg1.AC1 issuer re-run PASS).

## NOT SIGNED as asked, R1 and R2 alike: the write NARROWS the one master_admin caller, and the ask does not name it

What this seat read at signing:
- **`decide()` at the r30 release `92698aea8c`** (`app/data_entitlement.py`). A principal with an ACTIVE restricted
  profile passes a `DATA_GRANT_TOOLS` member only if its grant's `access.tools` includes it. `DATA_GRANT_TOOLS`
  includes `blackdiamond_list_fees` (OG-pf-1). Tier admission (`TIER_ADMITTED_TOOLS` for `master_admin`, OG-bd-2)
  applies ONLY on the no-profile branch.
- **The grant R1 copies is Schwab-shaped.** It is Alyssa's revision-4 scope: 2 Schwab masters, 4 datasets, and
  operations describe/download_filtered/list/query. OG-pf-1's own comment says "a grant names no Black Diamond tool,
  so a profiled principal is denied it".
- **Who that is:** OG-bd-2's census (`deliverables/0.9.0_WK_NFRA_OPLGTW~60/NEVER_WIDEN_ASK_OG-bd-2.md` section 2) names the
  caller `2cdb43ed4d`: tier master_admin, 4 real calls 10-01..10-08, outcome ok. OG-bd-2 deliberately KEEPS that
  caller's access. The live host carries exactly ONE `MASTER_ADMIN_EMAILS` alias, which A2 names as Andrew's principal.

**So R1, written as asked, ends Andrew's `blackdiamond_list_fees` access.** He moves from the no-profile branch
(admitted by tier) to the profiled branch, where a Schwab-shaped grant denies it. R2 does the same to the Bloomberg
principal's mirror of him. That reverses what OG-bd-2 shipped on Andrew's own 140xZ word, and the ask names it nowhere.
Its section 1 says "Who gains: Andrew's principal ... to the full approved width". It does not say who loses.

## REC to `1.0.0_SA_CTO~Z` -- the call is yours (it crosses two of your rulings, 32383 and the round-35 E1)

**(a) Recommended.** Tier admission survives a profile: in `decide()`, a `TIER_ADMITTED_TOOLS` member passes for
tier `master_admin` on the profiled branch as well. It is one line plus a test. It rides the next gateway release
(behind r30, before OG-mg-1's Phase B), so Andrew keeps Black Diamond fees and gains Schwab. OG-mg-1 Phase B waits
for that release.

**(b)** Write R1/R2 as asked, and record Andrew's loss of `blackdiamond_list_fees` as accepted under ruling 32383.
That needs your word naming the loss.

**(c)** Hold R1/R2 until per-person control (MC Portal FWD-21) can express a grant that names the Black Diamond tool.

## Everything else read, and held for the re-sign

- No prior record (both are CREATEs).
- Rollback is `revoke`: a tombstone, never a delete, and it keeps `email_deny`.
- The no-download rule is contract-level `forbidden_field_classes`, which binds R1/R2 exactly as it binds Alyssa,
  not by inheritance.
- No address appears in the ask.

-- 2.0.0_SA_COO~O
