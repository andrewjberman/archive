# CTO half -- NFRA_OPLGTW OG-ap-14, the r30 gateway release (OG-pf-1 + OG-tg-1 + OG-bd-2 + OG-sh-1)

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-14 ~01:3xZ.
**Ask:** `0.7.0_AE_CloudOps~Z`, `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-14.md`
@c832d025b2 (read whole).
**COO half:** `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-ap-14_20261014.md` @d8119a4d7a (read whole).
**Question:** msg 33887.
**Authority:** this seat's ruling `ledger/CTO_RULING_R37_ONE_RELEASE_PF1_TG1_BD2_SH1_20261013.md` @8f236865cc, and the
round-36 analysis R1.

## VERDICT: SIGNED at `release_sha` `db3d1972bc`, on base live `7eff14b2e6`, with the COO's C1-C3 as written

**Re-read by this seat:**

| read | result |
|---|---|
| `merge-base --is-ancestor 7eff14b2e6 db3d1972bc` | TRUE |
| `git diff --stat 7eff14b2e6 db3d1972bc` | 18 files, +1262/-136, all under `infra/aws/ec2/opal-gateway/` (0 outside) |
| the four excluded `app/` files (`harvest_read.py`, `admin_fabric_gitstate.py`, `family_depth.py`, `refs/silver_families.json`) | each byte-equal between base and release: none rides |

## Who gains and who loses, as this half signs it (the ask's section 2, with C1)

| cell | direction | who |
|---|---|---|
| OG-pf-1 | WIDENS | the 1 active restricted profile (`2c61471b14`): confined on the data-grant family only, and back to each non-data tool's own gate |
| OG-tg-1, sender gate | NARROWS | every non-Opal sender to the Bloomberg concierge is refused (Andrew 10-09: "should not even respond at all"); Teams reads record the sender's identity |
| **OG-tg-1, unscoping (C1)** | **WIDENS** | the Bloomberg principal's tool set becomes Andrew's (PRD v2.3 item 2). Today it is denied 8 of 8 gateway data tools. Andrew's word covers it: "opal-gateway-bbg should be an exact copy of opal-gateway for now". **Signed as named.** The ask's section 2 is corrected before B2 |
| OG-bd-2 | NARROWS | `blackdiamond_list_fees` is denied to unprofiled, non-`master_admin` callers (Andrew 140xZ call 3, "Yes that is fine") |
| OG-sh-1 | ADDS one READ tool | `list_shared_folder`, under each caller's own delegated token; no new scope |

## Bound

- **C2 binds:** the served read shows `bbg_identity_admitted_8` = 8 through the installed code. This is the positive
  arm this seat ruled (msg to COO~O, 00:3xZ). A value below 8 is a STOP and a redeploy of the base.
- **Tools:** +1 by name (`list_shared_folder`), 0 removed, on the `@mcp.tool()` set. `.env` names are unchanged.
  After B2, host md5 equals the release tree.
- **Suites:** 46/1, and the 1 (`test_ogz1_ac08`) fails identically at the live ref. Any other failure STOPS the act.
- **The non-ASCII WARN** (7 em-dash lines in `app/tools.py`) is pre-existing and unchanged. It is not fixed inside this
  release.
- **C3 binds:** if MP-n-4 lands first (its window closes at 10:30Z; B2 opens at 11:00Z), this half does NOT carry.
  B1 re-cuts on the new `deployed_commit`, AC1 re-runs, and both halves re-sign at the new `release_sha`.
- **Rollback:** redeploy live `7eff14b2e6` (105 of 105 md5 measured), or MP-n-4's commit if C3 re-cuts. No grant,
  profile, policy or Terraform state moves.
- **Not covered:** the two r30 grant writes (OG-mg-1, its own pair), OG-hv-2, and any other gateway change.

-- 1.0.0_SA_CTO~Z

## ADDENDUM 1 (2026-10-14 ~02:0xZ) -- C3 fired: RE-SIGNED at `92698aea8c` on live `b0c75d24f1`

MP-n-4 moved the live gateway. On `2.0.0_SA_COO~O` msg 33901 (COO re-sign ADDENDUM 1 @f58d3d1652).

**Re-read by this seat:**

| read | result |
|---|---|
| live base | `EC2_MANIFEST.json` `deployed_commit` = `b0c75d24f1` (prev `7eff14b2e6`); S3 `opal-gateway-latest.tar.gz` `git-ref` = `b0c75d24f1...`, two planes agreeing |
| `merge-base --is-ancestor b0c75d24f1 92698aea8c` | TRUE |
| `git diff <base> <release> -- infra/aws/ec2/opal-gateway \| git patch-id --stable` | v1 (`7eff14b2e6`..`db3d1972bc`) **eac7550c45** = v2 (`b0c75d24f1`..`92698aea8c`) **eac7550c45** |
| `git diff --stat b0c75d24f1 92698aea8c` | 18 files, +1262/-136; 0 outside the gateway dir |

**VERDICT: RE-SIGNED at `92698aea8c`.** The change is byte-identical to the one signed above, so every term carries:
C1 (the Bloomberg unscoping, a named widening), C2 (`bbg_identity_admitted_8` = 8), the suites' closed set, and the
non-ASCII WARN. **Rollback moves to the new live base `b0c75d24f1`.** C3 binds again: if the base moves before B2, this
is re-cut and re-signed. B2 opens at 11:00Z or later.

-- 1.0.0_SA_CTO~Z

## ADDENDUM 2 (2026-10-14 ~04:3xZ) -- C3 fired again: RE-SIGNED at `90967e39ba` on live `43088464f5`

NFRA_MCPINDEX MX-r-12 v1 and v2 moved the live gateway. On `2.0.0_SA_COO~O` msg 33984 (COO ADDENDUM 2 @ab3eda5984).

| read | result |
|---|---|
| live base | manifest `deployed_commit` = `43088464f5`; S3 `-latest` `git-ref` = `43088464f5...`, two planes agreeing |
| `merge-base --is-ancestor 43088464f5 90967e39ba` | TRUE |
| patch-id of the gateway diff | **eac7550c45**, identical to v1 and v2 |
| `git diff --stat 43088464f5 90967e39ba` | 18 files, +1262/-136, 0 outside the gateway dir |

**VERDICT: RE-SIGNED at `90967e39ba`.** Every term carries unchanged. **Rollback is now `43088464f5`.** C3 binds again.
MCPINDEX queues no further gateway release (COO~O). B2 opens at 11:00Z or later.

-- 1.0.0_SA_CTO~Z
