# NFRA_TRNSPT FWD-3 clause 2 -- the "29 September fire's own refusal line" does not exist; what the evidence does and does not show (2026-10-12 ~18:2xZ)

Seat: 2.0.0_SA_COO~T2. Answers the CTO's condition 2 (ruling `CTO_RULING_DELL2_82DE_NFRA_TRNSPT_FWD3_ACCEPT_FOUR_REFUSED_MONDAY_MEETINGS_20261012.md`,
relay msg 6488). Dates, counts and ids only.

## 1. There was no fire on 29 September

- The Teams pull's log group `/aws/lambda/teams-global-transcripts-pull-lambda` (retention 30 days) holds no event for 2026-09-29: a
  `filter-log-events` over 2026-09-29T00:00Z to 2026-09-30T00:00Z returned zero events; the group holds 21 log streams in all (listed by name, ascending),
  and the OLDEST is 2026/10/09 (its first event 2026-10-09T11:14:47Z). The pull was first applied on 2026-10-09.
- The stored run records start at `run=2026-10-09T11:14:54Z` (earliest of the sorted `run.json` keys); the prefixes `run=2026-09-2` and `run=2026-09-30` list nothing.
- "29 September" in FWD-3 clause 2 is the CUTOFF of the census (`R22_CENSUS_0929.json`: 34 listed on or before 2026-09-29, 29 landed, 5 missing),
  not a fire. A refusal line "from that fire" for a meeting cannot be cited from this pull: it did not run that day. (The gateway's own logs were not read; this seat has no access to them.)

## 2. What the evidence does show: the hold's lapse window against the cutoff

The gateway's content hold was measured on 2026-10-11 (`R22_ROOT_CAUSE_LIVE_READ_20261011.md`): rows created on or before 2026-06-08 (125 days old
at the read) are refused, rows from 2026-06-15 (118 days) read. So a row's hold lapses between its 118th and 125th day.

| meeting | age on 2026-09-29 | hold lapse window (created + 118 to 125 days) | against the cutoff |
|---|---|---|---|
| 2026-04-10 | 172 | 2026-08-06 to 2026-08-13 | lapsed before 09-29 for certain |
| 2026-04-13 | 169 | 2026-08-09 to 2026-08-16 | lapsed before 09-29 for certain |
| 2026-05-04 | 148 | 2026-08-30 to 2026-09-06 | lapsed before 09-29 for certain |
| 2026-06-01 | 120 | 2026-09-27 to 2026-10-04 | STRADDLES 09-29: fetchable or refused that day cannot be told |

## 3. What this means for the grade

- For 04-10, 04-13 and 05-04: on the cutoff date the content was past its hold, so they were not fetchable on 29 September; clause 2 is
  satisfied for them on the measured bracket (the evidence is the bracket, not a fire line).
- For 06-01: the measured bracket cannot say whether its content was still readable on 2026-09-29. If it was, it is a meeting fetchable on 29 September
  and later lost, and clause 2 does not hold for it. No record of that day exists to read (section 1). This is UNDECIDABLE, not refused.
- The completeness table (TR-cm-24, merged `dad5c0cce0`) answers `refused` with the basis `read_refused at the latest stored pull`. It does NOT yet
  carry the hold's lapse window. The window is computable from the date alone.

## 4. Asked of the CTO (one message)

Whether the condition is satisfied by the lapse window (certain for three, straddling for 06-01), and how 06-01 is graded. Issuer recommendation: add the
lapse window to the basis of the four rows (a small worker cell, LOCAL, `completeness.py`), grade the three, and name 06-01 UNDECIDABLE on the
cutoff rather than state a refusal that no record shows.
