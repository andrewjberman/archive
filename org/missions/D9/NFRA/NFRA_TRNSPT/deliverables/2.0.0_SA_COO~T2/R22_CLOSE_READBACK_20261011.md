# NFRA_TRNSPT round 22 -- the issuer's close readback (2026-10-11T03:4xZ)

Seat: 2.0.0_SA_COO~T2. Every figure here is the issuer's own read of live state, not the applier's report. Counts,
statuses, hashes and dates only.

## 1. TR-ra-22: the deployed pull, read live at 03:42Z

| read | value |
|---|---|
| `r22_checks.py ra22` | `R22-RA22-OK pull=AI4UQD0M local_zip=AI4UQD0M mail=VGIq85Xx commentary=ABSENT` |
| Teams pull CodeSha256 | begins `AI4UQD0M`: equals the rebuilt local zip, differs from the pre-fix `taFbGTCU...` |
| mail pull CodeSha256 | begins `VGIq85Xx`: unmoved |
| commentary function | absent |

## 2. The ONE real run: the applier's driven invoke at 03:38:50Z, read from the function's log and from S3

Function log since 03:15Z (4 events): one START at 03:38:50Z, one REPORT at 03:40:09Z (79.3 s), NO `[ERROR]` and no
Traceback. The 21 invocations before it (2026-10-09 16:00Z to 22:03Z) each ended in `[ERROR] GatewayGraphError`.

Run record `teams/transcripts/state/pull_runs/run=2026-10-11T03:38:57Z/run.json` (written 03:40Z; the first since
`run=2026-10-09T15:00:15Z`) and its listing snapshot under `state/listing_snapshots/` both exist (5 keys each).

| series | listed | landed | held | read_refused | refused | detail | against the A4 dry run |
|---|---|---|---|---|---|---|---|
| `monday_meeting` | 20 | 0 | 16 | 4 | 0 | `GatewayGraphError status=502` | equal |
| `ocio_ic` | 8 | 1 (`LANDED`, `SILVER-WRITTEN`) | 7 | 0 | 0 | | equal: the one row A4 said would land |
| `asset_management_ic` | 7 | 0 | 7 | 0 | 0 | | equal |
| `research_meeting` | 0 | 0 | 0 | 0 | 1 | `list GatewayGraphError status=502` | equal |

Verdict against the fresh CTO half's condition 4: MET on every count; no landing above A4's.

**What this does and does not prove.** It proves the deployed code completes a run over all four series, lands a new
readable transcript and writes its record, when invoked by a seat. It does NOT prove the SCHEDULED trigger: the next
EventBridge fire is Monday 2026-10-12 13:00Z. That fire is read by its `run.json` per-series counts, never by the
function's error count, because a refused listing now returns a clean invocation (CTO fresh half F3).

## 3. TR-rv-22: the four Monday meetings are ABSENT

The gateway lists these four `monday_meeting` transcripts and refuses their content (502). They were never landed in
bronze or silver, and no gateway route returns them:

| meeting created | state |
|---|---|
| 2026-04-10 | ABSENT |
| 2026-04-13 | ABSENT |
| 2026-05-04 | ABSENT |
| 2026-06-01 | ABSENT |

Cause (inferred, not confirmed by Microsoft): content ages out of Graph at about 120 days while the listing keeps the
row; measured bracket 118 to 125 days. A fifth, 2026-06-08, has aged out since it landed and is HELD in bronze and
silver. No recovery landing was made or is covered by the pair. Another source (a SharePoint copy) would be the only
recovery; none is located (`R22_RESEARCH_SHAREPOINT_READ_20261011.md`).

**Standing consequence:** every listed meeting ages out the same way. A meeting not landed within about 120 days of
its creation is lost to this route. With the pull now completing on every fire that is covered for admitted series;
it is NOT covered for `research_meeting`, whose listing is refused today.

## 4. Open at round close

| item | state | owner |
|---|---|---|
| `research_meeting` (FWD-2, 1 of 4 series): listing 502; the SharePoint folder Andrew named is not located by the gateway's site tools | open call queued on dell2 (the folder's link or site name) | Andrew; then the issuer |
| The handler's `totals` and log line omit `read_refused` | carried to the round analysis | CTO |
| Monday 13:00Z scheduled fire | read at the first tick after it | issuer |
| `test_eod_voice.py` fails to collect (imports a sibling test module by bare name); not touched by this round | noted; a later repair cell | issuer |
| Round-21 PASS on the 16:00Z fire | WITHDRAWN in its own record @cf7c22bcbb | done |
