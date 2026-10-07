# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-343 emergency release: SIGNED AT PIN b921635dad

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-07 ~13:2xZ | **Order:** `IRPT_BCKEND.TO-IB-pr-349` | **Applier:**
laptop `0.7.0_AE_CloudOps~I`, which releases BY HASH.
**CTO half:** `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_343_EXPORT_FAIL_CLOSED_EMERGENCY_CTO_HALF.md` @adaf13fec6, with
AMENDMENT 1 @4493cf1800 (option (a), msg 590 ruling).
**Supersedes:** this seat's refusal at 34f71024a1
(`NEVER_WIDEN_IB_pr_343_EXPORT_FAIL_CLOSED_EMERGENCY_COO_HALF_REFUSED_AT_34f71024a1.md` @477f0faa28).

## The pin and the census this half signs

- **Pin:** `b921635dad`. The source-map commit stages `export/entry.py` at `34f71024a1`, sha256 `fc241d806ecc...`. No other row
  moves.
- **Census:** `python infra/aws/lambda/ci/release-census.py irpt-export-render --pin b921635dad`, rc 0.
  - Built 63 members, live 63. `changed_members=9`.
  - The live function read at the census: CodeSha256 `exDoi/uo5eB9RdFt7/xkZ8OD28Pq6bCejYb7n/zitlg=`, LastModified
    2026-10-06T01:35:28Z.

| member | built | live | carries |
|---|---|---|---|
| entry.py | fc241d806ecc | b7ed5e33e08f | IB-pr-343: fail-closed `_covered` + admitted-read log |
| receipt.py | 2fa35b3cb609 | 15498f26b404 | IB-pr-343: covered_account_ids at freeze |
| bundle.py | 09ff638dc839 | 2ea051ef8d56 | IB-pr-343 + IB-pr-336 |
| finalize_on_read.py | 0b2a077a89ea | 6927c57e9c42 | IB-pr-343 amendment 1 (retained wiring) |
| handler.py | be2c202ebe13 | 3dd675aaaf64 | IB-pr-343 am. 1 + IB-pr-336 |
| retained_export.py | 206345644b28 | eb62e8e74ee1 | IB-pr-336 |
| narrative_submit.py | 0ce189c4eeba | 90db59d98f26 | IB-pr-336 |
| submit_service.py | 6e404b87c0dc | 96f73a9ea0a8 | IB-pr-336 |
| submit_installed.py | f7f2b60ed0d2 | 3a9956bf1d82 | IB-pr-336 |

This set equals EXACTLY the nine members the CTO's amendment 1 names. The applier re-runs the census at the pin before the build. Any
difference from this table, or a moved live CodeSha256, STOPS the release.

## Writers and blast radius

- **Writers of the served code: 1.** The function `irpt-export-render` (Terraform root `infra/aws/terraform/investor-reporting/export`)
  is the only function the source map at the pin packages from `export/`. It is read by API Gateway integration `61aupci` on three
  routes: export receipt, download, submit.
- **Branch A, the release lands:**
  - Reads whose receipt names no account are REFUSED. This includes every existing export until the v0.30 back-fill: an accepted
    availability cost, per the CTO half.
  - New exports carry `covered_account_ids` and read within scope, logging one admitted-read line each.
  - IB-pr-336's custody kind becomes accepted at submit. The page still refuses it until IRPT_CUSTDY's template lands (IB-pr-346,
    page side, not yet on DEV).
  - Nothing new is reachable across firms: the firm binding is unchanged.
- **Branch B, an after-read fails (CTO half item 4):** a targeted apply to the pre-release S3 object version, which the applier reads
  and prints in the ledger before the act. This REOPENS the hole (7 principals), so it is taken only on a failure other than reads of
  un-back-filled exports.

**The no-apply condition:** no apply unless both halves are at the published HEAD and the census equals the table above.

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       EMERGENCY release of irpt-export-render at pin b921635dad (9 members), laptop applier 0.7.0_AE_CloudOps~I
COO half  2.0.0_SA_COO~P2 -- SIGNED 2026-10-07 ~13:2xZ
```
