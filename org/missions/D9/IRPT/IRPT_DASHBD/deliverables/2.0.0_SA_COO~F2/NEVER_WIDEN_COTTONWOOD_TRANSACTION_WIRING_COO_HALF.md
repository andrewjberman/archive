# NEVER-WIDEN, COO HALF -- the Cottonwood landing function: ONE CODE RELEASE (the late-posting returns reader and settle step, the transaction table read through the late-posting window), the write statement, the new bundle, two dry runs, the first one-day write and a bounded range (IRPT_DASHBD rounds 138 to 139)

**Signer:** 2.0.0_SA_COO~F2. **Status:** SIGNED (REVISION 2). **Date:** 2026-10-17 ~17:1xZ. This half replaces the REVISION 1 half whole; the halves signed on REVISION 1 (this seat @511122931b, the CTO @04175d4e4a, SUSPENDED before apply) do not cover these bytes.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_TRANSACTION_WIRING.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_COTTONWOOD_TRANSACTION_WIRING.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_COTTONWOOD_TRANSACTION_WIRING.md`, committed at `5cb1dc9403`), sha256 `5d7350ea8a92ee8e20eb8dfac83f53eae6a915cdcb1708800cf4d3a933eecc5c`
(computed by this seat on the file and on the committed blob, equal; 20,019 bytes; git blob `0983fdb848d3`). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's three questions (section 9). **Nothing is built, uploaded, applied or invoked until both halves are SIGNED on this sha256.**

## 1. What this half covers

Eight acts, in order, each with its stop. (1) The rollback-target read (the VersionIds of the returns days the first scheduled fire may overwrite; the bucket is versioned) and the bundle build and upload of `irpt-cot-account-return-daily-lambda` as a NEW VERSION of its artifact key (base64 sha256 `pa5JdBfOL2GUA6b/UU5sp9upDcj0JGjCQ4+xCOass9g=` or STOP; rollback target the current version `6tFJSAqDjN0GqFkYj.DgT6.TkSmlwAuh`). (2) ONE `safe-apply` of `infra/aws/terraform/investor-reporting/account-return-daily/`, plan exactly 0 add / 2 change / 0 destroy: the role's inline policy gains ONE new statement `WriteTheAccountTransactionGoldPrefixOnly` (Allow, `s3:PutObject` only, on the one Cottonwood `account_transaction` gold prefix, no condition) and the function's code is replaced (memory, timeout, handler, runtime, role, layer and environment unchanged; no read or list grant). (3) Two DRY RUNS that write nothing: the transaction-only event for the newest writable day, and the scheduled path (`{"dry_run": true}`, settle included). (4) The first one-day WRITE of the transaction event. (5) A bounded RANGE of at most 25 trading days, transaction-only, each day written once and only on a full D..D+14 window. (6) The first scheduled fire after the apply READ. (7) The receipt, naming the newest writable day.

## 2. What this seat measured and re-ran, and what it did not

- **Re-run by this seat on the release tree (`36da4e101f`, box/dell2, LOCAL), all PASS:** the transaction window cell `DBF139-6-AC1` to `AC3` (the window reader and dedup, the once-and-full-window stage on its own owed days, the scheduled-fire wiring, the landing function's tests directory 52 passed 0 failed); the bundle criteria `DBF138-6-AC1` to `AC3` (the entry's pins, the attribute closure, the packaged-layout import smoke). The build-only package was built TWICE by this seat with the same base64 sha256 above, equal to `2.0.0_SA_COO~D2`'s final build (msg 10622). `2.0.0_SA_COO~D2` reports its returns-reader criteria (p199) and release criteria (p200) PASS on the same tree, and that 2026-07-24 sums 277 distinct ids; this seat did not re-run those.
- **Measured read-only on the silver (counts only, `R139_COTTONWOOD_PARTITION_OVERLAP_FINDING.md`):** 125 of 127 partitions hold a row of another business day; a business day's rows repeat across about ten partitions; none of the 14 columns the transaction producer reads varies across partitions for one TransactionID; a day is complete by lag 4 (median) and lag 14 (every full-window day). **Live state:** the function, role policy, schedule, artifact versions and the empty new prefix as the packet's section 3; the served bucket's versioning ENABLED.
- **Graded by the CVO:** the Cottonwood transaction producer, COT-J-R138, PASS 20 of 20 on contract 0.5.1 (v152); the window reader changes which rows reach the same producer and is not re-graded (the CVO's sample from the written prefix is a later round's judgment criterion).
- **NOT done by anyone:** a `terraform plan` of this root with the new statement; the in-Lambda duration and memory of the NEW full path (Act 3(b) is its first measure); the first scheduled fire's settle against live served objects; whether the first fire after the apply precedes `2.0.0_SA_COO~D2`'s all-days rewrite pair.

## 3. Writers of the changed properties, counted

One rule writes the Cottonwood `account_transaction` prefix (`emit_transactions` through the producer's `emit_transaction_day`), N = 1, entered by the scheduled fire and the transaction event only; the new statement is one. The returns prefix: one writer (`run_day`) entered by three paths (the owed days, the settle step, the explicit rewrite event); the explicit rewrite pair is not in this packet.

## 4. Blast radius, and the limits this half signs under

- Acts 1 to 5 as the packet's section 4: an artifact version, one write statement, the code replaced, one new transaction partition and up to 24 more at an empty prefix. **Unlike REVISION 1, the SERVED output moves:** from the first scheduled fire after the apply, owed returns days are derived with the late-posting reader and up to five landed returns days per fire (none before 2026-07-10) are overwritten with their full-window values, so the served Cottonwood flow term is corrected (row S137: inflated 8 to 13 times). Visible only to Opal staff in Global view; no advisor holds a grant (CTO msg 10592). **Blast radius: the owed days plus at most five settled days per fire under the one returns prefix; no other key, firm or table. Per-key rollback: a copy of the VersionId recorded in Act 1 over the key (a copy, no delete),** after the code rollback.
- **Honest limits, signed on:** no plan has run; the new full path has never run inside Lambda (the dry run of Act 3(b) and the first fire's read are its evidence); a transaction day with no rows stays unwritten; the new transaction table has no reader.
- **Not covered:** the all-days rewrite from 2026-07-10 and the republish (a separate pair); any transaction day before Act 5's range; the Inflection and 49 Financial sides; the schedule; any reader; any read or list grant; any delete of any object or version; the filled-report function.

## 5. Both branches

As the packet's section 6: A as stated; B (a denied write) stops with the policy read-back first; C (the producer refuses a day) stops and reports the text; D (memory or time, or Act 3(b) above 80 percent) stops with the measured peak and nothing written; E (the first scheduled fire slowed, or a failed settle) is condition 6 and `settle_failed`; F (a repeat) reports `already landed` and rewrites nothing; G (a window-complete day with no rows) stays unwritten and is named.

## 6. Rollback, per key

As the packet's section 7: the code by a copy of the previous artifact version over the key (no delete) and a `safe-apply`, by the applier with the CTO's word, the write statement leaving with that apply; each overwritten served returns object by a copy of its recorded prior VersionId; the new transaction partitions are NEW keys with no prior version, and their removal is Andrew's act, never done here.

## 7. Conditions this half signs under

The packet's section 8 as written, in particular: the order of firms (Monday's 49 Financial first-fire read, then the Inflection pair, then this pair; one firm changes per fire day; never with another IB2 apply); the ledger entry first, bound to the packet sha256, with every live worktree's `.open_deploys/` read and the denominator printed, and the suspended re-land ledger dispositioned first (an open rewrite ledger on the root STOPS Act 2); every write act outside the weekday band 11:30Z to 14:15Z and clear of the daily fire; no delete, no bare `terraform apply`, no `update-function-code`, no schedule change, no read or list grant; stop at once on the listed conditions; the first scheduled fire after the apply is READ, and over 80 percent of the limits or a timeout takes the rollback with the CTO's word.

## 8. Signature

I, `2.0.0_SA_COO~F2`, sign this half on the packet sha256 above. This signature authorizes nothing until `1.0.0_SA_CTO~DELL2`'s half is SIGNED on the same bytes, and it covers only what section 1 lists under the limits of section 4, including the served-output movement of section 4 under its stated blast radius and per-key rollback.

-- 2.0.0_SA_COO~F2
