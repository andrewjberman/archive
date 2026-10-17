# NEVER-WIDEN, COO HALF -- the Cottonwood landing function: the transaction table (the write statement, the new bundle, a transaction-only dry run, the first one-day write and a bounded range) (IRPT_DASHBD rounds 138 to 139)

**Signer:** 2.0.0_SA_COO~F2. **Status:** SIGNED (REVISION 1). **Date:** 2026-10-17 ~08:2xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_TRANSACTION_WIRING.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_COTTONWOOD_TRANSACTION_WIRING.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_COTTONWOOD_TRANSACTION_WIRING.md`, committed at `dc56f78c7d`), sha256 `c5b7d756c11edb2d767a02dcaab86f2eb209fe5714a69044a53d0a49410db156`
(computed by this seat on the file; 15,153 bytes; git blob `d27780167d52`). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's two open questions (section 9). **Nothing is built, uploaded, applied or invoked until both halves are SIGNED on this sha256.**

## 1. What this half covers

Six acts, in order, each with its stop. (1) The bundle build and upload of `irpt-cot-account-return-daily-lambda` as a NEW VERSION of its artifact key (base64 sha256 `6IrkQGalZOejYzTlB/LAQaYh9aTtbj8JMrzJgLZgUMI=` or STOP; rollback target the current version `6tFJSAqDjN0GqFkYj.DgT6.TkSmlwAuh`, whose bytes this seat hashed to the live CodeSha256). (2) ONE `safe-apply` of `infra/aws/terraform/investor-reporting/account-return-daily/`, plan exactly 0 add / 2 change / 0 destroy: the role's inline policy gains ONE new statement `WriteTheAccountTransactionGoldPrefixOnly` (Allow, `s3:PutObject` only, on the one Cottonwood `account_transaction` gold prefix, no condition) and the function's code is replaced (memory 1,024, timeout 900, handler, runtime, role, layer and environment unchanged). (3) A transaction-only DRY RUN of one day: nothing is written. (4) The first one-day WRITE of the same event. (5) A bounded RANGE of at most 25 trading days, transaction-only. (6) The receipt.

## 2. What this seat measured and re-ran, and what it did not

- **Re-run by this seat on the landed tree (box/dell2, LOCAL), all PASS:** the Terraform cell `DBF138-4-AC1` and `AC2`; the handler cell `DBF138-5-AC1` to `AC3` (the landing function's tests directory 35 passed: 16 at the base and 19 new); the bundle cell `DBF138-6-AC1` to `AC3` (the attribute closure over the pinned blobs and the packaged-layout import smoke). The build-only package was built TWICE (and once more today) with the same base64 sha256 above.
- **Live state, read by this seat today (read-only):** the function at CodeSha256 `+iYXakKx7zhK33lv6W0jDAY1QsLYUNqNCuHHIA7owD0=`, 1,024 MB, 900 s, the one layer, no environment; the role policy's five statements; the schedule ENABLED at 08:15 New York on weekdays; the artifact key's current and prior versions; the new prefix at 0 objects.
- **Graded by the CVO:** the Cottonwood producer, COT-J-R138, PASS 20 of 20 on contract 0.5.1 (v152), 19 measured and 1 inferred claims.
- **Source of the plan:** the Terraform text is two pure insertions (a table constant in `locals.tf`, the new statement in `iam.tf`); `lambda.tf`, `main.tf` and `schedule.tf` are byte-identical to the base by sha256; the existing five statements are unchanged.
- **NOT done by anyone:** a `terraform plan` of this root with the new statement (the plan's exact resource addresses are the applier's to print); the in-Lambda read of `fact_transactions` (the local read took 0.3 s); the stage's memory over a 25-day event; whether the live artifact was built from exactly the 15 pins now in the entry.

## 3. Writers of the changed properties, counted

One rule writes the Cottonwood `account_transaction` prefix (`emit_transactions` through the producer's `emit_transaction_day`), N = 1; the new statement is one.

## 4. Blast radius, and the limits this half signs under

- Act 1 adds an artifact version. Act 2 adds one write statement to a role policy and replaces the function's code, so the next scheduled fire (12:15Z) runs the new stage as its LAST step. Act 3 writes nothing. Act 4 writes ONE new partition at an empty prefix. Act 5 writes up to 24 more NEW partitions and overwrites no existing key. **No existing gold table (`account_return_daily` included), the filled report, the published series or any read or list grant is written or changed;** a stage failure cannot alter the returns result (graded offline by DBF138-5-AC2, a planted failure leaves it byte-equal).
- **Honest limits, signed on:** no plan has run; the stage has never run inside Lambda; the scheduled fire could be slowed (sizing says about 3 s a day on a fire of about 11 s and 331 MB of 1,024): condition 6 reads the first fire and the rollback is the previous artifact version; the new table has no reader.
- **Not covered:** any day before Act 5's range (earlier history waits on a CVO sample from the written prefix); the Inflection and 49 Financial sides; the schedule; any reader; any read or list grant; any delete of any object or version; the filled-report function.

## 5. Both branches

As the packet's section 6: A as stated; B (a denied write) stops with the policy read-back first; C (the producer refuses a day) stops and reports the text, never worked around; D (memory or time) stops with the measured peak; E (the first scheduled fire slowed) is condition 6; F (a repeated Act 4 or 5) writes the same keys and bytes except a manifest's build time, acceptable.

## 6. Rollback, per key

As the packet's section 7: the code by a copy of the previous artifact version over the key (no delete) and a `safe-apply`, by the applier with the CTO's word, the write statement leaving with that apply; the new partitions are NEW keys with no prior version, and their removal is Andrew's act, never done here.

## 7. Conditions this half signs under

The packet's section 8 as written, in particular: the order of firms (Monday's 49 Financial first-fire read, then the Inflection pair, then this pair; one firm changes per fire day; never with another IB2 apply); the ledger entry first, bound to the packet sha256, with every live worktree's `.open_deploys/` read and the denominator printed; Acts 2 to 5 clear of 12:10Z to 12:30Z on trading weekdays; no delete, no bare `terraform apply`, no `update-function-code`, no schedule change, no read or list grant; stop at once on the listed conditions; the first scheduled fire after the apply is READ, and over 80 percent of the limits or a timeout takes the rollback with the CTO's word.

## 8. Signature

I, `2.0.0_SA_COO~F2`, sign this half on the packet sha256 above. This signature authorizes nothing until `1.0.0_SA_CTO~DELL2`'s half is SIGNED on the same bytes, and it covers only what section 1 lists under the limits of section 4.

-- 2.0.0_SA_COO~F2
