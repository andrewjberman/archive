# AMGT_RESAPP round 72 -- `AMGT-av-8` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-05 ~23:0xZ

**The act (THREE legs, in this order)** for `opal-amgt-scoped-api`, under ONE NEVER-2 entry. Executor `0.7.0_AE_CloudOps~A`.
Order: `task-orders/AMGT_RESAPP.TO-AMGT-av-8.the-code-redeploy-and-legs.md`, with AMENDMENTS 1 and 2.

1. **Grant leg.** Two edits in `infra/aws/terraform/harvest/scoped-amgt-api.tf`, then ONE `safe-apply` targeted at
   `aws_iam_role_policy.scoped_amgt_api_grants`. The plan must be ONE in-place update of that policy; anything else is a STOP.
   - Add `"filings/v1/",` back to `local.scoped_amgt_pool_prefixes`, with its comment updated. The removal note (AMGT-rk-91 M2)
     says it left only because no reader remained; av-4's `read_segment_breakdown` is that reader now.
   - Add `"dynamodb:BatchGetItem"` to the statement granting `dynamodb:GetItem` on `table/etf-classifications` (~`:354`).
   - Then `round72/checks/r72_grant_av8.sh` must read `R72 AV8 GRANT: YES`.
2. **Code leg.** ONE artifact at build commit `7889ef1ae4` (or a descendant with the same CONTENT-DIFF), then ONE code-only
   `safe-apply`. `memory_size` stays 1769. Right after it, run `round71/checks/leadpanel_cold_warm.py --label after`.
3. **Drafting splice leg.** Run `round72/checks/drafting_evidence_splice.py --keys BA_US_Equity,ASML_NA_Equity --write
   --pre-act-dir <dir>`. This is NOT `drafting_build --rebuild-pool` (AMENDMENT 2).

## THE BASE, read live at signing (22:58:32Z) -- the rollback per key

| object | value | rollback |
|---|---|---|
| function CodeSha256 | `wbIT0PHvxKIgJvgVy+u0XhLuSXFK5dUE/wypJPDcf8o=` (round 71 au-7) | prior artifact version, one code-only safe-apply |
| function MemorySize | 1769 | unchanged |
| grants policy | `filings/v1/` absent; etf-classifications GetItem only | revert the two tf lines, one targeted safe-apply |
| `drafting/v1/BA_US_Equity.json` | VersionId `.zSrn_broPgdErEesbpfY8lJH5RMBCSb`, 105,318 B, sha256 `79d0113d...` | re-put the pre-act bytes |
| `drafting/v1/ASML_NA_Equity.json` | VersionId `kQZePsmgbJlF1Tnvf3t2ljwqNnW9wrYX`, 13,039 B, sha256 `e80df9eb...` | re-put the pre-act bytes |
| open NEVER-2 entries on this function | none in the shared tree (read 22:58Z); the executor reads every live worktree | -- |

## THE CONTENT-DIFF, measured by the issuer at signing

A detached worktree at `7889ef1ae4`, `--build-only`, then `content_diff.py --zip` against the deployed `wbIT0PHv`.

| class | files |
|---|---|
| CHANGED | `lib/research/api/scoped_amgt.py`, `lib/research/api/monthly_chatter.py`, `lib/research/print/render_pack.py` |
| ADDED | `lib/research/peers/numeric_tickers.py` |
| REMOVED | none |
| IDENTICAL | 361 of 365 |

- **Size:** 253,961,459 B against 262,144,000 B (96.9%).
- **VERIFY-SCOPE:** cold-start FATAL [] and request-time break [].
- **Any other file is a STOP.**

## NEW READ PATHS AND ACTIONS (CTO round-67 ruling 4), simulated at signing

`round72/checks/r72_grant_av8.sh` on the live role:
- controls allowed: sec filing_source GetObject and ListBucket, etf-classifications GetItem;
- **C1 GetObject `filings/v1/<key>/<acc>.analysis.json`: implicitDeny;**
- **C2 ListBucket prefix `filings/v1/<key>/`: implicitDeny;**
- **C3 `dynamodb:BatchGetItem` etf-classifications: implicitDeny.**
All three must read `allowed` after the grant leg and before the code leg is LANDED.

## WRITERS OF WHAT MOVES (NEVER-1)

- **The function's code: N = 1 writer,** this act.
- **The grants policy: N = 1 writer,** this act, through the harvest Terraform.
- **`drafting/v1/<key>.json`: N = 2 writers.** One is `drafting_build --rebuild-pool` / `--splice-driver` / `--hold-unspanned` and
  `analyze --write-pool`, all hand-run by this project's seats and none scheduled. The other is this splice.
  - Read from the producer's own rule: a FULL rebuild would ALSO add `anchored` / `text_original` to every BA sentence and DELETE
    ASML's `thesis_driver_provenance` (measured 23:0xZ). That is why the leg is the narrow splice.
  - The splice's diff is EXACTLY `.evidence_records` (BA +P0276/P0277/P0278, 86 -> 89; ASML +P0086, 11 -> 12) and
    `.denominators.evidence_records`.
  - It is serialized with the stored object's own options (indent 2, non-ASCII kept, trailing newline: round-trips the stored
    bytes).

## EXPECTED OUTCOMES (both branches)

| check | before (wbIT0PHv) | expected after | if not |
|---|---|---|---|
| r72 c39 / c41 / c43 / c44 / c45 | FAIL (137 / 2,389 tokens / 0 / 94 / 680) | YES each (all YES on the shared tree, local) | rollback of the code leg |
| r72 c42 | 0 of 6 | 6 of 6, after the splice leg | restore the 2 keys; the code stays (it serves a plain `passage_reason` without them) |
| r72 c43 on deployed | -- | 12 names with rows, only once C1/C2 read allowed | without the grant, the route serves its plain "could not be read" reason (no 500), and the act is NOT LANDED |
| r71 c34/c36/c38, r70 c30-c33 | YES | YES (no regression) | rollback of the code leg |
| cold first read (leadpanel `after`) | chatter 5.3-10.0 s | reported only: lower expected (60/72 calls from 153/167) | not a rollback trigger; values unchanged (EQUAL 15/15) |

## SIGNED

`2.0.0_SA_COO~Z`, 2026-10-05 ~23:0xZ. The CTO half is owed at `ledger/NEVER_WIDEN_ROUND72_AV8_CTO_HALF.md`.
