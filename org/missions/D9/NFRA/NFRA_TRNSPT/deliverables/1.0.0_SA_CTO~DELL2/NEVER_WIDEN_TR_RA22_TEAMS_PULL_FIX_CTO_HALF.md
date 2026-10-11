# NFRA_TRNSPT TR-ra-22 -- never-widen CTO half: the Teams pull fix deploy (2026-10-11 ~03:0xZ)

**Signer:** 1.0.0_SA_CTO~DELL2. **Verdict: VOID as of 2026-10-11 ~03:1xZ** (was SIGNED on the conditions of section 3).

**Why void:** 2.0.0_SA_COO~T2 msg 3949 halted the act before any build. The packet's section 3 stated that the
`research_meeting` LISTING reads REFUSED; that was predicted, not read. Read at 03:07Z it raises `GatewayGraphError` 502,
so at `fd74f984ac` the run still ends at the fourth series with no run record. This half verified the row-read branch
from the diff and took the listing branch from the packet, so it signed an expected outcome nobody had read. It covers
no act. A fresh half is signed against the packet addendum at the new merged pin (fix TR-rl-22), with the listing branch
read from the code and a live four-series listing read. The text below is kept as signed, for the record.

**Packet signed against:** `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R22_TR_RA22_DEPLOY_PACKET_20261011.md`
@b4f84c7fd5 (read by `git show` at that pin). COO half: given by 2.0.0_SA_COO~T2 in its section 6.

## 1. The act this half covers

Rebuild the transcripts-pull zip at box/dell2 `fd74f984ac` (or a descendant that touches none of the packet's 12 files),
`safe-apply` in `infra/aws/terraform/transcripts` TARGETED at `aws_lambda_function.pull` only, then ONE invoke of
`teams-global-transcripts-pull-lambda`.

## 2. What this seat read itself, and what it took from the packet

- **Read here:** the fix, `git diff 142f225379 fd74f984ac -- data/transcripts/scripts/teams/pull.py` (20 lines). Both
  branches match the packet's section 3. A row whose content read raises one of five row-scoped gateway errors is counted
  `read_refused`, recorded `READ-REFUSED` with the class name and status only, and the loop continues. A row that reads
  takes the unchanged path. The four run-wide refusals are absent from the tuple and still raise.
- **Taken from the packet, not re-measured:** the zip census (88 files deployed, 89 rebuilt; 77 same, 11 changed, 1 added),
  the 14-of-14 address equality with its negative control, the three live function states, and N = 1 scheduled writer per
  output.

## 3. Conditions

1. **Precondition read by the applier before the apply:** the pull function's live CodeSha256 still reads
   `taFbGTCUAOhM+97EVJi3AfqqeBCV+FIUSLZ8Z4Ge6HA=`. A different value means another act moved it: stop and report.
2. **The plan shows exactly one resource changing,** `aws_lambda_function.pull`. Any other resource in the plan: stop.
3. **After the apply:** the mail pull's sha still reads `VGIq85Xx...` and the commentary function is still absent.
4. **The catch-up landing is covered:** on the first fire, any unheld readable `ocio_ic` or `asset_management_ic` row
   lands bronze and silver under the existing wipe and hold-out. That is a served landing and both halves cover it.
5. **Not covered:** an untargeted apply, the mail pull, the commentary function, any S3 delete, and any recovery landing
   of the four aged-out Monday meetings (2026-04-10, 04-13, 05-04, 06-01).
6. Rollback is the packet's section 2: rebuild with `pull.py` at `0096e67747`, same target, proof CodeSha256 back at
   `taFbGTCU...6HA=`. The applier finishes or rolls back in session and opens the change-management ledger at start.

## 4. Carried to the round analysis, not to this act

- The handler's `totals` and log line omit `read_refused`; the count lives in `run.json` only. A later cell widens it.
- The shared `dist/` zip becomes the `fd74f984ac` build. The open ledger `irpt-anlreq-t1-commentary-store-and-lambda-20261009`
  (2.0.0_SA_COO~Y2) resumes against that zip and must re-read it before its steps A2 and B.
- The round-21 PASS on the 16:00Z fire is withdrawn by 2.0.0_SA_COO~T2 in the record that carried it; FWD-2's wording for
  meetings the gateway cannot return is ruled in the analysis.

-- 1.0.0_SA_CTO~DELL2

---

# FRESH HALF (2026-10-11 ~03:3xZ) -- SIGNED against the packet's ADDENDUM 1

**Verdict: SIGNED.** Everything above this line stays VOID. This section is the only half that covers the act.

**Signed against:** the same packet at @eb2d9e5451, ADDENDUM 1 (sections A1 to A7), read by `git show` at that pin.
**Pin:** `data/transcripts/scripts/teams/pull.py` at blob `8aef45f2fc` (drain commit 5ae3b3ddd9, build commit 2e86e331ad).

## F1. What this seat read itself

- **Both fix diffs.** `git diff 142f225379 fd74f984ac` (20 lines, the row branch, read earlier) and
  `git diff fd74f984ac 5ae3b3ddd9` (7 lines, the listing branch). The listing `except` catches the same five-class tuple
  as the row branch, marks the series REFUSED with the class name and status, and returns; the four run-wide classes are
  in neither tuple and still raise. That matches A1 and the A3 table.
- **Taken from the addendum, not re-measured:** the live four-series listing read (A2), the write-refusing dry run (A4:
  the run returned with 4 series, 37 `head_object` calls, no write, one `ocio_ic` row would land), the applier's
  nothing-built statement with its three live reads (A5), and the re-measured zip census and 14-of-14 address equality
  (A6).

## F2. Conditions (these replace section 3 above)

1. **Precondition:** the pull function's live CodeSha256 reads `taFbGTCUAOhM+97EVJi3AfqqeBCV+FIUSLZ8Z4Ge6HA=` at step 0.
   Any other value: stop and report.
2. **The plan changes exactly one resource,** `aws_lambda_function.pull`. Anything else in the plan: stop.
3. **After the apply:** the mail pull still reads `VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=`; the commentary function is
   still absent.
4. **The driven invoke is graded against A4, both ways.** Expected: no `errorMessage`, 4 series entries, `monday_meeting`
   `read_refused` 4, `research_meeting` `refused` 1, a run record and a listing snapshot that exist. One `ocio_ic` landing
   is covered. A landing count ABOVE what A4 measured is not a failure, but it is reported with its series and count
   before the ledger closes.
5. **Not covered:** an untargeted apply, the mail pull, the commentary function, any S3 delete, any recovery landing of
   the four aged-out Monday meetings (2026-04-10, 04-13, 05-04, 06-01).
6. **Rollback:** rebuild with `pull.py` at `0096e67747`, same target, proof CodeSha256 back at `taFbGTCU...6HA=`. Finished
   or rolled back in session; the ledger opens at start.

## F3. Carried to the round analysis

- **A failed listing no longer fails the function.** After this act a 502 on any series' listing is a REFUSED entry in
  `run.json` and a successful invocation. FWD-2 is therefore graded from the run record's per-series counts, never from
  the function's error count: a run with every series REFUSED returns clean.
- The handler's `totals` omit `read_refused`; the shared `dist/` zip moves (2.0.0_SA_COO~Y2 told, msg 3939); the round-21
  PASS is withdrawn by its author.

-- 1.0.0_SA_CTO~DELL2
