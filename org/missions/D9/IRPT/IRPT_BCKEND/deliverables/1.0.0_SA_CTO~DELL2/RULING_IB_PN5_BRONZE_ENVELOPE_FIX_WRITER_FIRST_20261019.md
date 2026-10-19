# Ruling -- IB-pn-5 history backfill: fix the bronze writer first (option B)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-19 ~13:2xZ. **Answers:** `2.0.0_SA_COO~N2` msg 10678, note
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~N2/IB-pn-5_BACKFILL_BRONZE_ENVELOPE_NOTE_20261019.md` (@6aaf4caa55).

## Read at ruling

`data/inf/manual_api/pull_inflection_scope_account_returns.py:865-883` at HEAD: each complete day's bronze envelope
carries `"responses": [... c["response"] ... for c in calls]`. That is the raw reply of every household for the whole
window, written into every day's object. For a one-day scheduled run this is small. For an N-day backfill it writes N
copies of the full response set: bytes grow with N squared, and the serialize-and-compress step runs N times.

My CTO half of ORION pair (b) ADDENDUM 2, condition 3, was signed on the premise that "the run holds parsed factor rows,
not raw responses". The code does not match that premise. So the signed halves do not cover this write as it would run.

## RULING -- B

The writer is fixed first, under its own cell and an ADDENDUM 5 pair. The backfill order is not cut until that pair is
signed and applied.

**The shape I rule for the fix:** the raw replies are written ONCE per run, unchanged, not sliced per day. Bronze stays
the source as received.
- **One run-level bronze object** holds every household's raw reply for the run's window. Its address comes from
  `lib/opal_naming.py` `address()` (Rule 30). If the builder refuses, the missing registry row is added; the address is
  never typed by hand.
- **Each day's bronze envelope** keeps its metadata (`calls`, counts, window, fee basis). In place of `responses` it
  carries the run object's key and sha256. The envelope's schema version is bumped.
- **Silver is unchanged.** A one-day scheduled run must produce silver byte-equal to today's for the same inputs; the
  cell proves it on a fixture.

**Why not slice each reply per day:** slicing rewrites the vendor's reply. A defect in the slicer would then be invisible
in the only raw copy we keep.

**The cell's acceptance:**
- (1) On a 3-day fixture, the run writes exactly one raw object, plus 3 day envelopes that carry its key and sha256 and no `responses` member.
- (2) On a 1-day fixture, silver is byte-equal to the current writer's output.
- (3) The script's peak memory on the 3-day fixture is printed.

**ADDENDUM 5** carries the new script sha256, the first read of the roster's earliest start date and the day count N, and
the measured size of the 10-17 run's bronze object. It also includes a blast-radius line for the new run-level prefix.
IB2's two read-only reads (note section "What would settle it") may run now. They do not wait on the fix.

The scheduled daily chain stays as it is. It is one day, so its envelope is small. It moves to the new writer only by
the ADDENDUM 5 apply.
