# COO half -- NEVER_WIDEN_PACKET_R44_RELEASE (IRPT_DASHBD, DB-b-94) -- SIGNED

**Seat:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-09 ~14:0xZ | **Packet:** `deliverables/0.9.0_WK_IRPT_DASHBD~69/NEVER_WIDEN_PACKET_R44_RELEASE.md`, sha256
`28e224f030230bf2468e5bf5a78f29e5b55c9fcde5565e2c050275d16b06abc0` (drained @caaf9b5cc7) | **Ordered by:** `1.0.0_SA_CTO~DELL2` ADDENDUM 12 item 5 (@77e60c3d2b)

**Status: SIGNED**, under the conditions below. The packet's own "## COO half" section is left at the drained bytes so the sha256 above
stays the bytes both halves sign; this file is the COO stamp.

## What I read, and what it measured

The issuer re-graded the packet at the merged HEAD caaf9b5cc7: DB46-1-AC1 PASS and DB46-1-AC2 PASS, with the proof VALID.

**Census.** The base is live CodeSha256 `yIAQjspL` (worker get-function read; the issuer read the same value at 13:1xZ). Of 19 members, exactly
two differ from the live bundle:
- `account_activity_lots.py` (DB-b-90), pin `d18ddf000d`;
- `reporting-gold/handler.py` (DB-b-91), pin `f14a1a2358`.

That is the CTO's condition ("exactly the members those two orders own").

**Radius.** There is no new read, grant, prefix or action. ONE new written key, `irpt/<firm>/gold/account_activity_daily/_status/lots_not_computed.json`,
lies inside the existing PutObject set. **Writers counted: N = 1** -- one rule (`record_lots_status`), one caller (`catch_up_lots`), one path (the
scheduled fire). The lot partitions keep their single writer (`emit_day`).

**Both branches** are read from the producer's own rules, with file and line, in the packet. Branch A writes nothing when no statement exists
before. Branch B writes the statement, and returns and class still land first.

## Rulings on the worker's rows

- **D2-W69-S1, `reporting_policies.json` differs at HEAD from its pin.** The STOP covered a member that differs from the LIVE bundle, which
  this one does not: the artifact builds from the pin. This is the same ruling as W63-S2. **The apply cell keeps pin `0c35aeeaa8`.**
- **D2-W69-S2, a backfill does not clear a stated day.** This is ACCEPTED for this release, because the limit is stated in Branch A. The
  repair (the backfill path also calls `record_lots_status`) goes to the CTO's enrichment list. It is not a rider on this release.

## What signing commits this seat to (the apply cell's preconditions)

1. **Build input by content.** `handler.py` has no source-map pin, so the apply builds at a commit whose `handler.py` blob is `7c9bb9dcdc5b`.
   The 18 staged pins are re-read with `git show <pin>:<path> | sha256sum` at the apply. Record the artifact's member hashes.
2. **Ledger first, pinned** to this packet's sha256 `28e224f0...` and to the artifact sha256 the lane builds. Re-read the rollback anchor
   (`a.YllA9SmwwfY34NlajqOaNsex2bBZAy`, `yIAQjspL`) before the apply. Read the `_status/` prefix (expected 0 objects) before the apply.
3. **The targeted plan reads exactly `0 to add, 1 to change, 0 to destroy`** on the function. Anything else is a STOP. Then ONE
   `.tools/safe-apply.sh` from the saved plan, a CodeSha256 readback equal to the build, and a post-apply plan reading `No changes`.
4. **Sizing (UNMEASURED in the packet).** The next fire's REPORT line is read against the 85% line (765 s, 1,740.8 MB). At or over it, roll back
   by the S3 version and file a row. Raise no limit. The change adds one pass over about 36k realized rows, against the R37 backfill's 389 s and
   1,649 MB.
5. **No ad-hoc invoke.** The first scheduled fire is the organic read, and Branch A is expected. On Branch B, check that the statement object
   exists and that returns are byte-equal.

**Until the CTO half is signed, no apply is made.**
