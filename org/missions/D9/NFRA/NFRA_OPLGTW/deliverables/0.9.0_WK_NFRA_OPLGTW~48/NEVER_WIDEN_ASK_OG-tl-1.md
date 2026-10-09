# NEVER_WIDEN_ASK_OG-tl-1 -- the 4 NFRA_TRNSPT meetings onto TRANSCRIPT_MEETING_ALLOWLIST (three halves: 1.0.0_SA_CTO~Z, 2.0.0_SA_COO~O, 3.0.0_SA_CVO~Z)

Pin: built on `91811b648a` (r29; the host still reads r28 `aa75078e1b`, 97 of 97 md5, SSM 1b5e2c57-3ff5-4ee7-9247-2340aea60adb at Phase A); stage commit `4514246d65` (the json only); release commit on `rel-nfra-oplgtw-tl1`: `78afad428389a4665aed267ac7f44e76533be59a` (one file, `deploy-to-ec2.sh`; committed under the audited `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL` per OG-tl-1 A1 @9ba3e56d87, resolving row NFRA_OPLGTW-Z-W48-S1; the applier's `DEPLOY_BASE_REF` is the host's live ref, not the stage commit). Phase B re-cuts on whatever is live at deploy time (MP-x-4 deploys between r29 and this cell). Authority: `1.0.0_SA_CTO~Z` ruling `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/1.0.0_SA_CTO~Z/CTO_RULING_HX_TRANSCRIPTS_HOST_ALLOWLIST_4_MEETINGS_20261009.md` @261e2c42a0.

## 13. BLAST RADIUS
**The 4 meetings by name and value** (meeting ids, not secrets; read from `data/transcripts/scripts/teams/meeting_allowlist.json`, blob d57e815a7c, never typed in the script):

| # | series | Teams subject | online_meeting_id |
|---|---|---|---|
| 1 | monday_meeting | Morning Meeting | `MSozY2Y2ZTE2MS1iY2UzLTRlNDctYTMyZi02ZTRjOTY0NjM3Y2EqMCoqMTk6bWVldGluZ19ORGxrTWpFek1HUXRZVEptTnkwME1qVTRMVGd4T1RZdE1UY3lNakV4WmpZeFpUQTNAdGhyZWFkLnYy` |
| 2 | ocio_ic | OCIO IC | `MSozY2Y2ZTE2MS1iY2UzLTRlNDctYTMyZi02ZTRjOTY0NjM3Y2EqMCoqMTk6bWVldGluZ19ObVprWmpZeFpqRXRPVEV3WWkwMFpEZ3lMVGs0TmpJdE9XWm1aV1U1TnpWa1pHVm1AdGhyZWFkLnYy` |
| 3 | asset_management_ic | Asset Management IC | `MSozY2Y2ZTE2MS1iY2UzLTRlNDctYTMyZi02ZTRjOTY0NjM3Y2EqMCoqMTk6bWVldGluZ19ZMlF5T1RKallXVXROakF5WVMwMFlXWXhMV0UzWldFdE56ZGpNMkZqWkRFelkyUmpAdGhyZWFkLnYy` |
| 4 | research_meeting | Research Team Meeting | `MSplNDRkNDI5Yi1iNjI5LTQwMzUtYjA5Yi00NDdlOTc4MzIyZGIqMCoqMTk6bWVldGluZ19NakJrTW1RMFpESXRNalkzTXkwME5UQXpMV0V4WlRVdFpUUXhOVGd5WkdGa01EWXlAdGhyZWFkLnYy` |

**What a caller can newly read.** Before: `TRANSCRIPT_MEETING_ALLOWLIST=` is empty and `/hx/transcripts/meetings/{meeting_id}/transcripts[/{transcript_id}]` answers 403 `meeting_not_allowed` for every meeting. After: for each of the 4 ids, the holder of the transcript bearer (`TRANSCRIPT_BEARER`, label `trnspt`, one holder, unchanged) can GET that meeting's transcript list and each transcript's text/vtt content, read through the one fixed identity the machine routes already use. Same bearer, same GET-only verbs, same answer shape (`{meeting_id, rows, count}` and `{..., byte_count}`); any other meeting id still answers 403. No code, route, bearer, IAM or other env value changes; the audit still carries ids and byte counts, never content.

**Writers of the property** "the allowlist": **N = 1** -- `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`, which renders `.env`'s `TRANSCRIPT_MEETING_ALLOWLIST` (read by `app/transcript_route.py meeting_allowlist()`, **N = 1** reader). The script computes the comma-joined values in file order and refuses with exit 1 before any upload or `.env` write on an unreadable json or a count other than 4 (tested: 4 ids pass, 3 ids refuse, missing file refuses).

**Both branches.** (a) The id is admitted and Graph answers: the list and content are served (200). (b) The id is admitted and Graph answers 403: the route returns 502 `graph_error` with status 403 and nothing is served. Expected 3 of 4 readable; Research Team Meeting (row 4) reads 403 from Graph's side until its organizer grants access (the ruling's own note) -- that is branch (b) by design, not a failure.

**The restart.** One service restart (MainPID changes); `.env` changes exactly one value (`TRANSCRIPT_MEETING_ALLOWLIST`, 51 names unchanged); no tool, route or secret is added.

**Rollback (one act).** Redeploy the base (the live ref read at Phase B) from its tree with `DEPLOY_BASE_REF=<this release sha>`; the allowlist returns to empty and every meeting is refused again. **Triggers:** `/health` off 200; tools off their count; any `.env` value hash changed other than `TRANSCRIPT_MEETING_ALLOWLIST`.

## 14. Halves owed
- `1.0.0_SA_CTO~Z` -- the code that runs (one script, the allowlist read and the count-4 refusal).
- `2.0.0_SA_COO~O` -- the act, its order in the host queue (r29, MP-x-4, then this cell), and the one restart.
- `3.0.0_SA_CVO~Z` -- what a caller can newly read (the 4 meetings above).

Phase B is the applier's; this worker deploys, uploads and restarts nothing.
