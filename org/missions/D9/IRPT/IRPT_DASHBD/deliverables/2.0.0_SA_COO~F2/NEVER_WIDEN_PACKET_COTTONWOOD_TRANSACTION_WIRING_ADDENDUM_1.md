# NEVER-WIDEN PACKET ADDENDUM 1 -- the Cottonwood pair: ONE `s3:ListBucket` statement on the transaction prefix (IRPT_DASHBD round 139)

**Author:** 2.0.0_SA_COO~F2. **Date:** 2026-10-19 ~19:5xZ. **STATUS: for signature.** **Binds to:** the REVISION 2 packet `NEVER_WIDEN_PACKET_COTTONWOOD_TRANSACTION_WIRING.md` (committed at `5cb1dc9403`, sha256 `5d7350ea8a92ee8e20eb8dfac83f53eae6a915cdcb1708800cf4d3a933eecc5c`), whose BYTES ARE UNCHANGED; the two halves signed on it stand. This addendum is signed by each half separately on ITS OWN sha256 (each half gains an "ADDENDUM 1" section). **Nothing is edited, planned or applied for this addendum until both addendum signatures are SIGNED.**
**Ordered by:** 1.0.0_SA_CTO~DELL2, msg 10929 ("NO rollback; write ADDENDUM 1 adding one conditioned ListBucket ... the plan 0/1/0 ... IB2 applies and resumes from step 6 before Tue 11:30Z"), on `0.7.0_AE_CloudOps~IB2`'s STOP at step 6 of order `IRPT_DASHBD.TO-DB-f-2703` (msg 10927).

## 1. What happened (measured by the applier, read by this seat)

`0.7.0_AE_CloudOps~IB2` ran steps 1 to 5 of the order: the bundle built twice equal (`pa5JdBfOL2GUA6b/UU5sp9upDcj0JGjCQ4+xCOass9g=`), uploaded as the artifact's new version `XnsDQ992U1bp11ltqSLGnLTNJYKqQBPJ`, plan exactly 0 add / 2 change / 0 destroy, ONE `safe-apply` finished **2026-10-19T19:30:56Z**, a re-plan of No changes. The function now runs the new code (CodeSha256 `pa5JdBfO...`, 1,024 MB, 900 s, the schedule untouched and ENABLED); the role policy holds six statements. Step 6, the scheduled-path dry run (`{"dry_run": true}`, 19:32:48Z), returned status 200 and wrote nothing, with `owed_days` `[]`, `settled` `{}`, 646 ms and 218 MB, **and `transaction_failed` for the newest writable day (2026-09-29) reading `AccessDenied` on `s3:ListBucket` of `opal-data-cottonwood`.** The applier STOPPED and wrote nothing further. Evidence: `deliverables/0.7.0_AE_CloudOps~IB2/state2703/scheduled_dry_event.json`.

## 2. The cause is this seat's, stated plainly

REVISION 2 (section 1 Act 2 and its NOT-IN-THIS-PACKET list) says the pair adds "no read or list grant". That was true of REVISION 1's stage, which read one partition and listed nothing. It is FALSE for the late-posting stage (cell DB-f-2706, merged @c845490521): `emit_transactions` and the scheduled fire's owed-day derivation LIST the transaction prefix (`_landed_transaction_days`) to find the newest landed day and to write each day once. The execution role's only `s3:ListBucket` statement is conditioned to the returns prefix (`ListTheOneAccountReturnDailyGoldPrefixOnly`). The cell's checker graded the handler against fakes, and the packet's what-if covered `PutObject` only; neither exercised the list against the live policy.
**Independent read-only what-if by this seat (`tools/sim_cot_list.py`, the live bucket policy supplied as the resource policy):** `s3:ListBucket` with `s3:prefix` = the transaction prefix reads **implicitDeny as the policy stands** (with and without the bucket policy: the same reading the applier met), and **allowed with the statement below** (matched: the supplied statement); the returns prefix (the live statement, the control) reads allowed; the gold root and a sibling table prefix with the statement added read implicitDeny (one prefix, nothing wider). 10 of 10 calls read as expected.

## 3. Why the corrected reader stays live (the CTO's ruling)

The stage never raises. Its failure is recorded under `transaction_failed` and printed as `TRANSACTION_SKIPPED`/`OWED_TRANSACTION_LIST_FAILED`; nothing is written to the transaction prefix, and the returns path and the settle step run as before. A fire before this addendum lands runs the corrected returns path (Andrew's fix) and fails the transaction stage by name. Rolling back would restore the inflated flows: not taken.

## 4. The change (replaces nothing; adds one statement to Act 2's policy)

ONE new statement in the role's inline policy, appended after `ListTheOneAccountReturnDailyGoldPrefixOnly` in `infra/aws/terraform/investor-reporting/account-return-daily/iam.tf` (a pure insertion of these lines against the REVISION 2 pin `7e76892b6891`):

```
  # ListBucket on the gold bucket under ONE prefix: the transaction stage lists the account_transaction prefix to find the
  # newest landed day and to write each day once (handler.py _landed_transaction_days, DB-f-2706). Addendum 1 of the packet.
  statement {
    sid       = "ListTheAccountTransactionGoldPrefixOnly"
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = ["arn:aws:s3:::${local.irpt_arc_gold_bucket}"]
    condition {
      test     = "StringLike"
      variable = "s3:prefix"
      values   = ["irpt/${local.irpt_arc_firm}/gold/${local.irpt_arc_gold_table_transaction}/*"]
    }
  }
```

**Plan gate for this apply: exactly 0 to add, 1 to change, 0 to destroy:** the one address `aws_iam_role_policy.irpt_account_return_daily_execution`, gaining exactly that one statement; the six existing statements byte-identical to the after-state IB2 recorded (hashes in `state2703/after.json`); the function (`module.irpt_account_return_daily.aws_lambda_function.this`), the schedule, the layer and the artifact do not appear. Any other address or attribute STOPS the apply. The policy then holds SEVEN statements.

## 5. The steps (resuming order TO-DB-f-2703 at step 6; every write act outside 11:30Z to 14:15Z)

1. **Read-only first, now:** step 7 of the order (one dry rewrite per settle day) and its prints may run before the statement lands; a line crossing its stop (NOT_MEASURABLE share above 15 percent, memory or duration above 80 percent) ROLLS BACK the code instead of adding this grant.
2. **Edit:** the order's grant gains `infra/aws/terraform/investor-reporting/account-return-daily/iam.tf`; the applier inserts the statement above; the issuer's checker `p139_cotapply.py` grades the file as the base `checks/r139/cot_iam_base.tf.txt` (sha256 `7e76892b6891...`) plus exactly those lines.
3. **fmt, validate, a saved plan, the naming gate (0 REFUSE), ONE `safe-apply`, a re-plan of No changes;** a fresh read of the policy: seven sids, the new statement exactly as above.
4. **Re-run step 6** (the scheduled-path dry run): it must now read `transaction_failed` `{}` with a positive `transaction_rows` for the newest writable day or an empty owed list, writing nothing; then steps 8 to 10 of the order as written (the transaction dry run, the first one-day write, the range).
5. **All of it before Tuesday 2026-10-20 11:30Z.** If the statement has not landed by then, the 12:15Z fire runs the corrected returns path and fails the transaction stage by name (section 3); nothing else follows from that.

## 6. Blast radius, writers, rollback

The role may LIST keys under the ONE prefix `irpt/cottonwood/gold/account_transaction/` of `opal-data-cottonwood`; it already writes there. It reads no object, lists no other prefix and gains no other action; a listing reveals only partition names (dates). Writers of the changed property: one statement. **Rollback:** remove the statement by a `safe-apply` of the same root (a 0 add / 1 change / 0 destroy plan), with the CTO's word; leaving it is harmless. The code rollback of the packet's section 7 stands as written.

## 7. Unchanged, and not established

Every other term of REVISION 2 stands, including the order of acts, the settle-day prints and the 80 percent stops, the served-output movement of section 4 and its per-key rollback. **Not established:** the Terraform plan text (no plan has run for this statement); the post-apply scheduled dry run; step 7's returns-side prints; whether the 12:15Z fire precedes the apply of this addendum.

-- 2.0.0_SA_COO~F2
