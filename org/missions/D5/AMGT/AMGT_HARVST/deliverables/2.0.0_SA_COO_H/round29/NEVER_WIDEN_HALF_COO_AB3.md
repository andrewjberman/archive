# NEVER-WIDEN -- COO HALF: backfill batch 1 -- 10 names x {bbg, wsj, sa} + Lenovo x {barrons, ft}, token-first (`HVST-ab-3` PHASE A)

**Signer:** `2.0.0_SA_COO~H`, 2026-09-30. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed). Phase B (the schedule) is signed separately,
after phase A's after-reads.
**Rulings served:**
- `ROUND_ANALYSIS.round28.md` ruling 3 (measured-first; Andrew's quota word, brief `:129-130`);
- PRD v0.9 `C-HV-TRUST-TOKEN`;
- CTO msgs 27155 (barrons and ft) and 27212 (sa).
**Vendor authority:** R-21 @`b390c36444`, on its mechanism: the collector script.
**Code pin:** CLOUD `ffe564672b`, carrying:
- `ab-1` (A1: pre-floor hits are not fetched; A2: token-first, bounded 429 backoff, attempts in the run record; A3: the newest
  stored token);
- `ab-3` phase A0 (a 402 keeps its body and gets one in-job fresh-session retry).

The act prints `git diff --stat ffe564672b HEAD -- lib/opal_data_harvest lib/research/harvest` and STOPs on any line.

## ROUND-25 RULING 1 -- every command that reaches a put

`<SEC>` = `org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round29/ab3_securities/<key>.security.json`. These
files are copied VERBATIM from the gold universe rows in `~46/securities.universe.json`. `<RT>` =
`"C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest"`. Every `run` carries
`--harvest-grammar --retrieval-mode backfill --floor 2026-01-01 --new-only --runtime-root <RT>`.

| # | command | puts |
|---|---|---|
| 0 | `python org/.../round29/checks/ab-3.before.py` must print `ACT-START GATE: OK`: every root equals signing, the outbox is empty, and the plan equals the signed plan | 0 |
| 1 | **The sa account-check probe:** `run ... --security-json <SEC 2317_TT_Equity> --publishers sa --max-jobs 1` | 1 run record. A 402 keeps its body and gets ONE in-job fresh sign-in (A0). If the job still ends `account_or_harvester_unavailable`, that is a **persisting 402**: a finding, recorded, and sa leaves steps 2-3. |
| 2 | `run ... --security-json <SEC 2317_TT_Equity> --publishers bbg wsj --max-jobs 2` | 1 run record |
| 3 | For each of the other 9 names, in file order: `run ... --security-json <SEC key> --publishers bbg wsj sa --max-jobs 3` (`bbg wsj --max-jobs 2` after a persisting 402) | 1 run record each |
| 4 | `run ... --security-json org/.../0.9.0_WK_AMGT_HARVST~65/o5_lenovo.security.json --publishers barrons ft --max-jobs 2` | 1 run record |
| 5 | Print the outbox's pending count, then `upload-harvest --max-objects <that count> --retrieval-mode backfill --runtime-root <RT>`. A pending count above 5,000 is a STOP. | Per queued row: bronze plus a silver row on the bbg/wsj/sa/barrons/ft roots |
| 6 | Write `~83/ab3_runs.json` (every new run-record key, `sa_402_persisted`, each argv and rc); run AC1 and AC2 | 0 |

- Articles and listings queue locally until step 5.
- Each `run` makes exactly ONE S3 put, its persisted run record (`_persist_run_record`).
- Stub evidence: `test_o1_run_record_reach.py`, `test_ab1b_trust_token_and_backoff.py`, `test_ab3_account_402_fresh_session.py`.

**Config defaults the argv leaves unset:**
- `jobs_per_run` 1, so `--max-jobs` is set per step;
- `minimum_request_seconds` 15 and `jitter_seconds` 10;
- `max_listing_pages` 25;
- `throttle_max_attempts` 5, `throttle_max_total_wait_seconds` 120 and `throttle_base_seconds` 2;
- `auth_confirm_retries` 1;
- the token source is the NEWEST stored token (A3).

**Pacing:** 15-25 s per request. The printed ceiling of 800 listing pages is a worst case of about 4-5 hours. The measured
bound-stop and the pre-floor skip (A1) are expected to spend far fewer pages. The act runs each invocation to its end, and
no invocation is retried.

**Token sources, from `ab-1`'s census (names only):**

| publisher | stored token | credentials |
|---|---|---|
| sa | the newer of `seeking-alpha/session` and `sa.dpapi` | `seeking-alpha/credentials` |
| bbg | the newer of `bloomberg/session` and `bbg.dpapi` | `google/andrew-goldengate/credentials` |
| ft | the newer of `astn/ft/session` and `ft.dpapi` | `astn/ft/credentials` |
| wsj | `wsj.dpapi` (no Secrets session) | `dowjones/credentials` |
| barrons | `barrons.dpapi` (no Secrets session) | `dowjones/credentials` |

## VERDICT: SIGNED (on the code pin above)

- **Blast radius:** new never-overwrite bronze and silver objects on the five publisher roots, for these 11 securities only.
- **Run records:** exactly 12 persisted: the probe, name 1's bbg/wsj run, 9 name runs, and the Lenovo run. The A0 retry
  happens inside the probe's job, so it adds none.
- **No-write roots:** 0 objects on `chatter_daily` and `article_security_mention`.
- **Excluded:** NO delete, NO gold write, NO deploy, NO other security.
- **Rollback:** forward only.

## 1. BEFORE -- measured at signing (`round29/ab3_signing_before.json`)

| root | objects |
|---|---|
| bbg | 1,007 |
| wsj | 84 |
| sa | 106 |
| barrons | 30 |
| ft | 28 |
| run_record | 2 |
| chatter_daily | 10 |
| article_security_mention | 8 |

The outbox holds 0 pending rows.

**Pre-run print** (`round29/ab3_plan_signed.json`, the collector's own `plan`, with no publisher request):
- 32 (name, publisher) pairs x 25 pages = **800 listing pages**;
- basis DEFAULT on 32, MEASURED on 0;
- bound 2026-01-01 on every pair.

## 2. EXPECTED OUTCOME, BOTH BRANCHES

**Branch A (the publishers answer):**
- Each concluded job carries a `reached_span` from its hits' dates (A1/wsj `timestamp`), a listing-page count at or below
  25, and `skipped_pre_floor` for dated pre-floor hits.
- New articles land on each publisher's root after the upload.
- AC2 prints the MEASURED pages per publisher, the re-based ceiling for the other 180 names (DEFAULT would be 13,500 over
  {bbg, wsj, sa}), and the names REACHED (phase B's set).

**Branch B (a refusal), per job:**
- Recorded with its class and never retried outside the bounded backoff.
- A 429 is backed off within its bound, then the job ends `throttled` with the token kept.
- A persisting 401 means ONE sign-in.
- A persisting 402 (sa) removes sa from later steps.
- A 403 keeps its body under the runtime `rejected_bodies/`.
- One publisher's refusal does not stop another's job.
- AC2 passes on a fully recorded refusal. The refusal is FWD evidence either way.

**ft's "kept 403 body":** no body exists before this act. The runtime has no `rejected_bodies/`, because ft has not run since
`q-6` F1 built the keeper. So the ft job's own refusal, if any, is the body AC2 reads (`ab-3` AMENDMENT 3).

## 3. ROLLBACK

Forward only: every put is never-overwrite, and readers take the newest. A delete is a human word.
