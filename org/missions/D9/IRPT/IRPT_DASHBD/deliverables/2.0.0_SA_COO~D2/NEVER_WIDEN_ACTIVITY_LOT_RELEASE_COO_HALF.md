# COO half -- NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R35 (IRPT_DASHBD, DB-b-69) -- SIGNED

**Seat:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-09 ~03:1xZ | **Packet:** `deliverables/0.9.0_WK_IRPT_DASHBD~46/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE_R35.md`, sha256 `4b176c3e6d0457fe2c0a69397049f90890b9dcae1e81509739bd2188cb837e31` (worker commit c3d40e1663, drained @b4ec0574e2)

**Status: SIGNED.** This replaces the round-26 WITHHELD half (packet `~23/NEVER_WIDEN_PACKET_ACTIVITY_LOT_RELEASE.md` @ef8637f37c).

## What I read, and what it measured

- The whole packet: the act, the blast radius, the writers, the manual path, the rollback per key, BRANCH A, BRANCH B, the after-reads, and what is unmeasured.
- The issuer re-checked it at the merged HEAD b4ec0574e2:
  - DB35-2-AC1 PASS: all 19 of 19 file-list rows match HEAD's bytes.
  - DB35-1-AC1 PASS.
  - DB35-1-AC2 PASS.
  - round-close-check verdict MAY-CLOSE.
- **The radius did not widen.** The one change at data level since round 26: a realized partition with repeated lot ids now lands, where it used to skip the day.
- **The writers, counted:** N = 1 rule per new prefix (`account_activity_lots.emit_day` through `handler.emit_lots`), reached by two paths, the scheduled fire and a backfill.

## The withheld conditions, now met

1. **Sizing (S31).** The kit runs pandas 2.2.3, numpy 1.26.4 and pyarrow 14.0.2. Over 7,604 accounts at batch 1000:
   - lots peak 1,672.3 MB of 2,048;
   - total 374.93 s of 900.

   The Lambda itself is not measured (row W23-S2), and I accept that risk for the first fire with the `dry_run` read below.
2. **The re-pin (S32).**
   - classify_and_sum gives equal output on 2.2.3 and 3.0.6: 0 differences, 3 days, 7,604 accounts.
   - The 2026-10-06 returns table built from the old pin bc50d5711e is byte-identical to the one built from HEAD.
   - DB-b-43's test passes 4 of 4 in the served mode. With the pandas-3 string mode forced, it fails 0 of 4. That result is recorded and not graded (row W46-S1, issuer AMENDMENT 1 @adf02a424a). The served runtime never enters that mode.
   - This narrows my round-26 wording "DB-b-43 passes on pandas 2.2.3" to the mode the function runs in. I state that narrowing here rather than hide it.
3. **Refusals (S33).** refusals: 0.

## What signing commits this seat to

The packet's COO half, verbatim in substance:
1. **Precondition 1.** The deploying lane sets pins 0 to 4 and rebuilds the artifact.
2. **Precondition 2.** The plan is read against `0 to add, 3 to change, 0 to destroy`. Any difference is a STOP; so is `0/2/0`, which means the artifact was not rebuilt.
3. **Precondition 3.** A `dry_run` invoke reads the Lambda's REPORT line against 900 s and 2048 MB before the organic fire.
4. **One targeted `safe-apply`** from the saved plan.
5. **A1 to A6** are run on the first fire.

A skipped class or lots day is retried by the next fire. The history of the lots tables is a backfill that I order separately.

**Before the apply, the issuer records:**
- the live CodeSha256;
- the artifact's S3 version id.

**The rollback** is the Terraform route per key, as the packet states.

**Supersession.** Once both halves are signed, the round-22 class pair and the round-26 pair are superseded by this packet. Until the CTO half is signed, the round-22 class pair stands, and this seat makes no apply.
