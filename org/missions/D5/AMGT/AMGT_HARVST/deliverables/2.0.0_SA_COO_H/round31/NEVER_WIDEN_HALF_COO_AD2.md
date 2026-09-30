# NEVER-WIDEN -- COO HALF: Seeking Alpha batch 1 -- 10 resolved names, `--no-sign-in`, stop at the first challenge (`HVST-ad-2` PHASE A)

**Signer:** `2.0.0_SA_COO~H`, 2026-09-30 ~21:4xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Rulings served:**
- `ROUND_ANALYSIS.round30.md` @`6adebef352` ruling 1 (measured-first; Andrew's quota word);
- PRD v0.10/v0.11 (stop at the first `bot_check`, `unclassified` or 402; never a sign-in);
- the CRO playbook @`7bcc258369` (no traffic to bbg, wsj or barrons).

**Vendor authority:** R-21 @`b390c36444`; the collector script is the mechanism.
**Code pin:** CLOUD `9e68057327`. It carries `ad-2` A0 (`run --no-sign-in`, @`93ddc953c1`), `ac-1` (`bot_check`), `ab-1`
(token-first) and `ab-3` A0. Package: 363 passed on the trunk. The act prints `git diff --stat 9e68057327 HEAD --
lib/opal_data_harvest lib/research/harvest` and STOPs on any line.

## ROUND-25 RULING 1

`<SEC key>` = `org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round31/ad2_securities/<key>.security.json`. Each file
is the collector's resolved-universe row, copied verbatim (`universe(config)`, the first 10 with `sa_symbol`). `<RT>` = the main
tree's runtime root.

| # | command | puts |
|---|---|---|
| 0 | `python org/.../round31/checks/ad-2.before.py` must print `ACT-START GATE: OK` | 0 |
| 1..10 | Per name, in plan order: `python -m lib.opal_data_harvest run --harvest-grammar --retrieval-mode backfill --floor 2026-01-01 --new-only --no-sign-in --security-json <SEC key> --publishers sa --max-jobs 1 --runtime-root <RT>` | **1** each (the persisted run record) |
| stop | After ANY invocation whose job status is `bot_check`, `unclassified`, `account_or_harvester_unavailable`, `sign_in_refused` or `throttled`: NO further invocation | 0 |
| 11 | Print the outbox's pending count, then `upload-harvest --max-objects <that count> --retrieval-mode backfill --runtime-root <RT>`. A count above 2,000 is a STOP. A count of 0 means no upload (the uploader refuses 0; `ab-3`'s lesson). | Per queued sa row: bronze plus silver |
| 12 | Write `~88/ad2_runs.json` (the run-record keys, each argv, its rc and the job status, the stop if any); run AC1 and AC2 | 0 |

**The positive arm (the analysis's "the serializing dry run's put count per name"):**
- Per name, the puts are exactly 1 run record at the run, plus 2 per newly stored article (bronze and silver) at the upload.
- **This cannot be serialized before the act.** A run that fetches nothing has nothing to upload, and a stub run is not the
  publisher.
- **Stub evidence for both put paths:** `test_o1_run_record_reach.py` (the run record) and `ab-2` / `aa-2`'s upload receipts
  (bronze plus silver per row).
- The 2,000 cap bounds the upload.

**Config the argv leaves unset:**
- `max_listing_pages` 25;
- `minimum_request_seconds` 15 and `jitter_seconds` 10;
- the throttle bound: 5 attempts, 120 s;
- the token is the NEWEST stored sa token (the saved-session file, per `ac-2`).

**Timing:**
- The ceiling is 250 listing pages plus article fetches, at 15-25 s each: several hours at worst.
- **The act must END by 08:00Z 2026-10-01.** If it has not, the next invocation does not start, and the stop is recorded as
  `time_bound`.
- First light is 09:00Z.

## VERDICT: SIGNED

- **Blast radius:** up to 10 run records, and sa bronze and silver for these 10 securities only.
- **No-write roots:** 0 objects on bbg, wsj, barrons, ft, `chatter_daily` and `article_security_mention`.
- **Excluded:** NO sign-in (`--no-sign-in`), NO delete, NO gold write, NO other publisher.
- **Rollback:** forward only.

## 1. BEFORE -- measured at signing (`round31/ad2_signing_before.json`)

| root | objects |
|---|---|
| sa | 106 |
| bbg | 1,007 |
| wsj | 84 |
| barrons | 30 |
| ft | 28 |
| run_record | 14 |
| chatter_daily | 11 |
| article_security_mention | 8 |

- The outbox holds 0 pending rows.
- **Pre-run print** (`round31/ad2_plan_signed.json`): 10 names x 25 = **250 listing pages**, DEFAULT on all 10. The bound is
  2026-01-01 for 9 names; Boeing's is 2026-09-12 (its watermark).

## 2. EXPECTED OUTCOME, BOTH BRANCHES

**Branch A (sa answers):**
- Per name: a `reached_span`, a listing-page count at or below 25, and `skipped_pre_floor` for dated pre-floor hits.
- New sa articles land on the sa root.
- AC2 prints the MEASURED pages per name and the re-based ceiling for the other 79 names (DEFAULT would be 1,975).

**Branch B (a STOP status):**
- The batch ends at that name, with the class recorded and the body kept.
- No sign-in, and no further request.
- AC2 passes on a recorded stop.

**Known and carried:** `Z-W87-S2`. The pre-`ad-1` sa account check read the literal account id, not this token's own. The
collector's listing path calls `check()`, and on the trunk it now uses the session's own `user_id` (`ad-1` A0 merged).

## 3. ROLLBACK

Forward only: every put is never-overwrite. A delete is a human word.
