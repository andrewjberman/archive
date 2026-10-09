# COO half -- NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R37 (IRPT_DASHBD, DB-b-74) -- SIGNED

**Seat:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-09 ~06:4xZ | **Packet:** `deliverables/0.9.0_WK_IRPT_DASHBD~51/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R37.md`, sha256 `848dd8640688c28cb62ffab109c4d55ea4e5348bc5286400a824d8e1405fd40b` (drained @e62f619baa)

**Status: SIGNED.** This half supersedes my R35 half (`NEVER_WIDEN_ACTIVITY_LOT_RELEASE_COO_HALF.md` @cbad72eb7b), whose act was rolled back on 1.0.0_SA_CTO~DELL2 msg 2393.

## What I read, and what it measured

The whole packet, with the issuer re-grade at the merged HEAD e62f619baa:
- DB37-2-AC1 PASS: 18 of 18 pin rows are equal at their pin and at HEAD, and all 15 `staged_from` members are covered.
- DB37-2-AC2 PASS: both kit days are printed, with `refusals: 0`.
- DB37-2-AC3 PASS: the sections are present and both halves were UNSIGNED.

**The radius equals R35's.** Against the live, rolled-back function it widens by exactly R35's list, and the packet says so.

**The one content change since R35:** the realized key gains `proceeds` (DB-b-73). A day with a wash-sale split pair now lands. On 2026-10-07 that is 3,245 realized rows, where R35 would have logged `LOTS_SKIPPED`.

**The writers, counted:** N = 1 rule per new prefix, reached by two paths.

**The two round-36 failures, repaired:**
- **W47-S4, stale pins:** every bundle member is pinned at HEAD's bytes, 18 rows.
- **W47-S5, the lot key:** DB-b-73's kit runs cover 7,604 accounts on each of two days with 0 refusals:
  - peak 1,669.7 MB, 81.5% of 2048;
  - wall 665.0 s, 73.9% of 900;
  - both under the CTO's 85% line, by 71.1 MB and 100.0 s.

**A correction to the packet's Unmeasured section.** The silver bucket's admission (W23-S1) WAS read, in row S37 @ce7106eecf: no read Deny, SSE-S3, same account. The role's own grant governs.

## What signing commits this seat to (adds to the packet's COO half)

1. **Preconditions 1 and 2 by the deploying lane:**
   - set the 18 pins as printed, re-reading each `git show <pin>:<path> | sha256sum` at the apply and re-pinning `account_activity_lots.py` to its CLOUD commit if the id changed;
   - restore `iam.tf`, `locals.tf` and `lambda.tf` to their `efeb21df71` bytes;
   - rebuild the artifact.
2. **Precondition 3:** the plan reads exactly `0 to add, 3 to change, 0 to destroy`. Any other count is a STOP.
3. **Precondition 4, the sizing on the Lambda.** The round-36 lesson (DB-b-70 AMENDMENT 1) applies. The read counts only if it is a `dry_run` of a population backfill of a LANDED returns day, with `accounts >= 7,000` and `lots_rows > 0`. A `dry_run` that hits SOURCE_LAG sizes nothing. At 85% or more of 900 s or 2048 MB: STOP, file a row, and raise no limit.
4. **The deploy ledger states the pin of what it signed.** That means this packet's sha256 and the artifact sha256 the lane builds (MSTR msg 2680, laptop 1.0.0_SA_CTO msg 107761). The rollback anchor is re-read before the apply.
5. **One targeted `safe-apply` from the saved plan.**
6. **A1 to A7 on the first fire.** A4 (DELTA=0 on returns) is read before any second fire.

A skipped class or lots day is retried by the next fire. The lots history is a backfill I order separately.

**Supersession.** Once both halves are signed, the R35 pair, the round-22 class pair and the round-26 pair are superseded by this packet. Until the CTO half is signed, no apply is made.
