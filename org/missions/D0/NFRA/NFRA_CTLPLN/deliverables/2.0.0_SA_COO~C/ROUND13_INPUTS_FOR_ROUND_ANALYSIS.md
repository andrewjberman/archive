# NFRA_CTLPLN round 13 -- inputs for the CTO's round-13 analysis (issuer 2.0.0_SA_COO~C, 2026-10-13 ~23:1xZ; updated as the round closes)

Not the analysis. What round 13's own work surfaced or left open, each with its row or record, so the ENRICHMENT LIST needs no re-measurement. Round 13's orders: `CT-ac-1` (complete, merge `2bf798e271`), `CT-ac-2` (complete, `e7d28c398b`), `CT-ac-3` (complete, `e581a6975c`), `CT-ac-4` (complete: census re-saved 233 -> 238, listing committed `76bd3d4dcf`, seat commit `e0dcb80218`), `CT-ac-5` (dell1 FWD-11 record; window Wed 2026-10-14 14:30-14:45Z, restart only when Andrew is at the box).

## A. Open after round 13, by owner

| item | owner | condition that un-parks it |
|---|---|---|
| FWD-11 exercise (`CT-ac-5`) | `0.0.0_AB_MSTR~DELL1`, Andrew's console sign-in | the manager announces ~13:30Z and restarts only if Andrew is at the box; otherwise the next hour he is |
| FWD-9 | `1.0.0_SA_CTO` | a real lease (C-LEASE is unbuilt; the Dells hold no vendor lease) -- PARKED, no order |
| FWD-27: muse's key on dell2 | `0.0.0_AB_MSTR~DELL2` | the read of the key (COMM_ASSIST FWD-6 needs it); the three boxes otherwise read 3 of 3 (`FWD27_READBACK_20261013.txt`) |
| FWD-27: the laptop local account | Andrew | his word ("another time") |
| S9119, the broker heartbeat writer | `0.0.0_AB_MSTR~DELL2` | a read taken while `~CB2`, `~TR2` or `~DELL2` is live names the writer. MSTR~DELL2's correction (msg 109004): the 14 orphan-parent pollers are NOT all on old code (4 started before the fix `5948c06a4f`, the rest after); the first seat-end read (`~C2` stood down ~00:47Z) left its MCP server and poller not running while `liveness.json` still held the pid with last_seen 00:47:56Z; whether the poller exited itself or died with the kill is unread; the writer is still unnamed |
| `W77-S3`, three IAM policy descriptions name removed Denies | the next apply of the identity root | rides that apply (CTO ruling) |
| reached-roles census freshness against the 5 functions `CT-ac-4` added | a CloudOps seat | `derive_reached_roles.py --check-fresh` (no `--check` exists) did not finish within 200 s offline; read it with a longer bound or fix the check |

## B. Round-14 batch candidates (each INERT; one repair cell)

| row | what |
|---|---|
| `W87-S2` | `infra/aws/terraform/nfra-ctlpln-identity/routes.tf` comments at about :23 and :30 still name the deleted `simulate_policy.py` |
| `W87-S3` | `crossbox-call.py` has no `project` key, so the OPEN-CALL arm's project-field match can only fire from `open_calls` rows |
| `W89-S2` | the fence check's premise drifted: the pre-rows scopes lack `restricted_prefix_hosts`; the registry holds 10 real scoped rows and `grants` |
| `W89-S3` | the lgic fence files never append `fence_scoped_allow_statements`; inflection carries 0 of 4 Allow statements |
| `W88-S1` (ruled) | the kill-agent floor is the unreadable-command-line limb only; the serial-less native helper case is deliberately not refused |
| `S9117`/`S9118` | `kill-maint.ps1` still refuses on a foreign seat (its `taskkill /T` cannot stop at a descendant): a stop-at-descendant for the reaper is the remaining half of the row |

## C. Process facts

- `safe-merge.sh` was run from a copy once (`CT-ab-13`) so the running script was not rewritten under itself; `CT-ab-13` removed the checker-bootstrap class from `1249b0d2d6` on.
- A Tier-2 seat cannot commit a path whose lane names only the CTO and the COO (`NFRA_CTLPLN_FAST_C` over the identity root): the issuer commits such a path; the seat's `<paths>` grant does not override a lane (it does for workers). The cut should not name such a path in a seat's order, or the lane should list the seat.
- A proof instance whose artifact row reads `PENDING-THIS-COMMIT` for a file an EARLIER commit carried is INVALID once committed (CCX class). Workers hit it twice (`~89`, `~U7`); the order's worker face could say "pin each artifact row to the commit that carried it" so no worker reports it again.

## D. Owned ARMED rows still OPEN after the CVO's two passes (a0723efcf58 pass 2: W6-S17, W73-S2, W14-S2 REMEDIATED and DISARMED)

Each is a repair this seat owns the disarm of; none serves an ungraded FWD, so none is cut this round. Candidates for the round-14 batch or their own cells:

| row | what | note |
|---|---|---|
| `W8-S7` | `dell_fence_census.py` (about :33, :730) defaults `--out` to the baseline file that `check_dell_fence_join.py` and `check_fence_scoped_rows.py` read, so a `--live` re-take silently changes the baseline | small, LOCAL |
| `Z-S3` | `lib/trading_calendar.py` fallback covers 2010-2027 only; its own text says regenerate (`lib/tests/gen_nyse_closures.py --write`) before 2028 | needs `pandas_market_calendars` (the FWD-15/18/19 package route is carried) |
| `W12-S1` | the three Lambda-vendored byte-copies of `lib/trading_calendar.py` differ from the lib file (163 lines vs 304) | one chain after `Z-S3`; the copies are code in deployed Lambdas, so the sync rides a deploy |
| `S9103` | `org/devices/kit_terraform_providers.py` has no replace-not-merge step for the Dell mirror and no dell2 readback | no commit to it since 2026-10-09 |
| `S9118`, `S9120`, `S9122` | see the CVO's `a5261ded52` (unchanged, unchanged, CLOSED_UNREMEDIATED to 2026-11-10) | `S9118` is the reaper's stop-at-descendant, a CTO-scope call |
