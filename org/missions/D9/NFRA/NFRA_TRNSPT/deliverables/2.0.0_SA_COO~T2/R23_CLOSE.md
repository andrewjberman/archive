# NFRA_TRNSPT round 23 -- close record: one digest on all three functions, the mail pull on the root, the drafter's closed lists and its route switch live; Monday's scheduled fire ran clean and landed nothing (2.0.0_SA_COO~T2, dell2, 2026-10-12)

Issuance `bf4a4a2cdc` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R23.md`, CTO round-23 analysis @b8a07a7e17). Amendments: AMENDMENT 1
@cc264e5f2e (TR-cl/ca/cn-23), AMENDMENT 2 @2a282ec3db (TR-sw/sa-23). `round-close-check --round 23`: MAY-CLOSE (14 orders in scope, 14 complete,
proofs 14 of 14 structural OK, 0 judgment). Every figure below is the issuer's own read at 2026-10-12T13:2xZ unless it names a record.

| cell | merged / act | what exists |
|---|---|---|
| TR-tt-23 (FWD-2) | drain 5374271f5c | `read_refused` in `pull.totals` and the `PULL-DRY` line; `test_eod_voice.py` collects. Re-run `R23-TT23-OK` 36 passed |
| TR-tv-23 (FWD-8) | TO-APPLY-tv23 flipped @0d910671a9 | `readers.auto.tfvars` holds the applied second-reader trust (1 principal), no variable default, 0-change plan. Re-run `R23-TV23-OK declared=1 live=1 equal` |
| TR-mp-23 (FWD-7) | TO-APPLY-mp23 flipped @2b6c7a6e2b; pair CTO half @f4ec64d888 | the mail pull runs the root's one zip. Disarms D2-S22 read 1 |
| TR-om-23 (FWD-3) | `R23_TR_OM23_FOUR_MONDAYS_OTHER_ROUTE_20261011.md` @a7412e21d8 | the four Monday meetings NOT FOUND by another route: a FAILED RETRIEVAL (the organizer's OneDrive is unreadable by the gateway's file tools), not an absence |
| TR-cl-23 | drain 615010e8bf | the drafter's prompt carries account type and category names only from the estate's closed lists, never themes. Re-run `R23-CL23-OK` 21 passed |
| TR-ca-23 | TO-APPLY-ca23 flipped @c7b0c108bd | closed lists and totals live on the root's three functions. Re-run `R23-CA23-OK` |
| TR-cn-23 | read @d95b48ecf0 (PART 2c) | a firm cannot free-name a comparison model; the composition's writer enforces its closed schema |
| TR-sw-23 | drain 2fab656082, issuer fix c942202bf9 | the drafter posts its stored draft to the request's own ticket, one attempt, one `COMMENTARY-POST` line; `post_census.py` counts the unposted. Re-run `R23-SW23-OK` 63 passed |
| TR-sa-23 | TO-APPLY-sa23 flipped @03bbf8b084; pair CTO half @ee3efa0504 | deployed: three functions, one digest `xC1GDXXp`, `TICKET_API_BASE` at the front door. Signed step 7(c) read 400 `application/json` naming `probe_extra_key` (post 2 at 01:31:04Z; post 1 read 404 on an issuer-defective id, row D2-S33) |
| TR-mf-23 (FWD-1, FWD-2) | this record | the 2026-10-12 13:00Z scheduled fire, read below |

## Live reads at close (issuer, 13:1xZ to 13:2xZ)

| read | value |
|---|---|
| `r23_checks sa23` | `R23-SA23-OK digests=1 live=['xC1GDXXp'] local_zip=xC1GDXXp base_is_front_door=True` |
| `r23_checks ca23`, `mp23` | `R23-CA23-OK`, `R23-MP23-OK` (teams, mail and commentary functions all `xC1GDXXp`) |
| `post_census.py --live --since 2026-10-12T01:31:00Z` | `lines=0 with_ticket=0 posted=0 unposted=0 no_ticket=0` -- no draft has run since the switch |

## TR-mf-23: Monday's scheduled fire, read from the log and `run.json`

Function `teams-global-transcripts-pull-lambda`, log since 12:55Z (4 events): one START 13:00:08Z, END, one REPORT `Duration: 34458 ms`,
`Memory Size: 1024 MB`, `Max Memory Used: 101 MB`. No `[ERROR]`, no Traceback.
Run record `teams/transcripts/state/pull_runs/run=2026-10-12T13:00:09Z/run.json` (started 13:00:09Z, ended 13:00:42Z, transport gateway):

| series | listed | landed | held | read_refused | refused |
|---|---|---|---|---|---|
| `monday_meeting` | 20 | 0 | 16 | 4 (`GatewayGraphError status=502`: 2026-06-01, 05-04, 04-13, 04-10) | 0 |
| `ocio_ic` | 8 | 0 | 8 | 0 | 0 |
| `asset_management_ic` | 7 | 0 | 7 | 0 | 0 |
| `research_meeting` | 0 | 0 | 0 | 0 | 1 (`list GatewayGraphError status=502`) |

Equal to the 2026-10-12T01:07:58Z driven run on listed and held for every series. The scheduled trigger on the fixed bytes is PROVEN to complete
all four series and write its record (the R22 carry, closed). NOT proven: a scheduled fire that LANDS a transcript, so `Max Memory Used` on a
landing run is still UNMEASURED (101 MB is the peak of a run that landed nothing; the decomposition's bar is "on a run that lands a transcript").
Row D2-S16 stays as it stands on that limb; this read does not close it.

## Open at round close

| item | state | owner |
|---|---|---|
| `research_meeting` (FWD-2, 1 of 4 series): listing 502 on the scheduled fire too | open call queued on dell2 (the SharePoint folder's link) | Andrew; then the issuer |
| FWD-3: 4 Monday meetings | NOT FOUND by the organizer-OneDrive route (a failed retrieval); absent from the gateway's content read | CTO to rule the FWD wording |
| First landing under a scheduled fire, with its `Max Memory Used` | UNEXERCISED; waits on a new readable transcript | issuer, at that fire |
| Draft route: a real draft's `COMMENTARY-POST` line and a 200 from the route; the stream path's create through the front door | UNEXERCISED LIVE | issuer, at the first draft |
| Rows D2-S27, S25, S28, S29, S30, S31, S32 | OBSERVATION, INERT; D2-S22 DISARMED by S28 on both reads; D2-S33 BLOCKING resolved by TR-sa-23's signed PASS | CVO compile |
