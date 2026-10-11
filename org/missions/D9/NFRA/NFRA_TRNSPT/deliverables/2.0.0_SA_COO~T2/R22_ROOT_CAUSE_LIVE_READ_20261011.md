# NFRA_TRNSPT round 22 -- TR-rc-22's missing measurement, taken live (2026-10-11T02:42Z-02:47Z)

Seat: 2.0.0_SA_COO~T2 (issuer read). It closes the gap row `NFRA_TRNSPT-D2-W2-S11` left open ("what the gateway answers
for those 4 reads is not measured") and files row `NFRA_TRNSPT-D2-S16`. Dates, statuses and byte counts only; no
transcript text was printed or stored.

## 1. The four reads -- with every other listed row as the control

Instrument: `GatewayTransport.list_meeting_transcripts` then `read_meeting_transcript(..., "vtt")` for each of the 20
listed `monday_meeting` rows (denominator 20 of 20, read at 2026-10-11T02:44Z).

| created | landed before? | read answer |
|---|---|---|
| 2026-04-10 | no | 502 `graph_error` |
| 2026-04-13 | no | 502 `graph_error` |
| 2026-05-04 | no | 502 `graph_error` |
| 2026-06-01 | no | 502 `graph_error` |
| 2026-06-08 | yes (held) | 502 `graph_error` |
| 2026-06-15 ... 2026-10-05 (15 rows) | yes (held) | 200, 17,998 to 77,414 bytes each |

The boundary is clean: every row created on or before 2026-06-08 (125 days old at the read) is refused, every row from
2026-06-15 (118 days) reads. The control discriminates (15 of 15 newer rows read, and 2026-06-08 read when it was landed
and is refused now).

**Root cause (inferred from the boundary, claim = inferred):** the transcript CONTENT ages out of Microsoft Graph at
about 120 days while the LISTING keeps the row. The four were already past that age when this project first landed
Teams transcripts, so no selection rule ever skipped them: their content was gone. This matches the PRD's own line
("34 transcripts listed and 30 retrieved before four expired"). The exact retention figure is not measured; only the
118-to-125-day bracket is.

**Consequence for TR-rv-22:** the four are NOT recoverable through the gateway. Under CTO ADDENDUM 13.1 ("not-held =
LOST") they are LOST by this route: 2026-04-10, 2026-04-13, 2026-05-04, 2026-06-01. Another source (a SharePoint
copy) is the only recovery; none is located (see `R22_RESEARCH_SHAREPOINT_READ_20261011.md`).

## 2. The scheduled pull has FAILED on every fire since 2026-10-09T16:00Z

Instrument: `logs filter-log-events` on `/aws/lambda/teams-global-transcripts-pull-lambda`, start 2026-10-09T12:00Z,
103 events (one page; the last fire of the schedule `cron(0 13-22 ? * MON-FRI *)` was 22:00Z Friday).

| fire | outcome |
|---|---|
| 13:00Z, 14:00Z, 15:00Z | completed (about 8 s each; the meetings were not yet admitted by the gateway) |
| 16:00Z through 22:00Z (7 fires) | `[ERROR] GatewayGraphError: hx-transcripts read refused: status=502 error=graph_error`, raised from `pull.py` line 205 (`run` -> `_pull_series`), 3 attempts per fire (the async retries) = 21 failed invocations |

Why: `_pull_series` reads every listed row that is not held. A refused read raises `GatewayGraphError`; the only
skip branch (`pull.py:161`, `except Expired`) is raised by the fixture transport alone. So each fire lands whatever
new rows come before the first aged-out row, then dies. Measured effects:

- The 16:00Z fire landed its one new Monday meeting and then failed (65 s). My round-21 read called that fire a PASS
  from the S3 keys alone; the function's own outcome was an error. That reading was wrong and is corrected here.
- No run record (`state/pull_runs/run=.../run.json`) and no listing snapshot is written by a failed fire.
- `monday_meeting` is the first series, so `ocio_ic`, `asset_management_ic` and `research_meeting` are never
  reached by the schedule. A new OCIO or Asset Management meeting will not land on its own.
- A new Monday meeting lands only if it is listed ahead of the aged-out rows (it was on 2026-10-09; not guaranteed).

Next scheduled fire: Monday 2026-10-12 13:00Z. It will fail the same way until the fix is deployed.

## 3. The fix (TR-rf-22, cut in round 22 AMENDMENT 2)

In `_pull_series`, a refused or corrupt CONTENT read of one row is recorded as that row's outcome and the loop
continues; the run completes, writes its record and reaches every series. A refused LISTING keeps its present
handling. Build and tests are LOCAL; the deploy is a served act under a CTO + COO pair, applied by
`0.7.0_AE_CloudOps~DELL2` with a change-management ledger entry.
