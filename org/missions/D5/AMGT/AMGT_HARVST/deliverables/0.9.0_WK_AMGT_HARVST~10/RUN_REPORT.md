# AMGT_HARVST HVST-h-10 -- RUN_REPORT (Phase 1, the THIRD granted act, 2026-09-23)

Issuer: `2.0.0_SA_COO~Y`. Assignee: `0.9.0_WK_AMGT_HARVST~10`. Grant: `1.0.0_SA_CTO~Z` msg 24464,
conditional on the Phase 0b rehearsal (verified independently by the issuer and shown to the CTO).
Same bound as the second act: bbg, ft, wsj, barrons, plus an SA pass that persists the received
bytes.

## Sizing (printed before the run, item 3)

`plan.json`: 5 publishers x 25 planned listing pages each = **125 total planned listing pages**.
Saved before item 4.

## The ONE live run (item 4)

Invocation (never wrapped in `timeout`):
```
python -m lib.opal_data_harvest run --runtime-root <main-worktree>/.runtime/opal-data-harvest \
  --publishers sa bbg ft wsj barrons --retrieval-mode backfill --floor 2026-01-01 \
  --security-json lenovo.security.json --bbg-symbol-probe --harvest-grammar --max-jobs 5
```
Run once, at 2026-09-23T00:23:01Z. rc=2 (main()'s own success check requires every job status in
`{complete_candidates, new_articles, no_new_articles}`; three jobs ended in `error`/`request_rejected`
below, which is why rc is not 0 -- this is NOT a crash, and NOT the uncaught-exception failure the
Phase 0b fix targets: **every one of the five publishers plus the probe reached `job_finished` /
its own recorded verdict, exactly as the fix requires.**

### Bloomberg symbol probe

**UNRESOLVED-CHALLENGED** -- real vendor call to bloomberg.com, real verification challenge
(`transport.VerificationRequired`). Caught cleanly by the Phase 0b fix; the run continued into
`Worker.run()` for all five publishers immediately afterward.

### Per-publisher table

| publisher | status | planned pages | accepted | rejected | stop reason |
|---|---|---|---|---|---|
| sa | upstream_unavailable | 25 | 24 | 6 | HTTP 502 from seekingalpha.com stopped further paging. Of the 24 accepted, only **3 were genuinely new** (raw_bytes captured, harvest mode wrote them); the other 21 replayed from the legacy catalog's prior (pre-harvest-mode) fetch. |
| bbg | error | 25 | 0 | 0 | `HTTPError` -- a real verification challenge on the job's own first fetch (separate from the CLI probe's own challenge), triggering a real verification-repair attempt that did not complete before the retry budget re-raised. |
| ft | request_rejected | 25 | 0 | 0 | HTTP 403 from www.ft.com/search. |
| wsj | complete_candidates | 25 | 11 | 0 | Session had expired; a real re-authentication succeeded, then the replayed job accepted 11 new articles cleanly. |
| barrons | request_rejected | 25 | 0 | 0 | Session had also expired; a real re-authentication succeeded, but the replayed job's own first real attempt hit a verification challenge and was rejected. |

**Every challenged, logged-out, throttled or rejected publisher above is a RECORDED outcome, and
the run continued to the next one -- confirmed directly: all five publishers reached
`job_finished`.** This is the whole point of the Phase 0b fix, and this run is its first real-world
proof.

### Unplanned/unexpected calls (recorded per the CTO's residual, not absorbed)

Three real vendor-touching events occurred beyond the plain listing/article fetch, all legitimate
existing harvester retry/repair mechanisms firing because the ~7.6-day-old sessions were genuinely
stale (one already known-challenged from the second act):
1. **bbg**: a real verification-repair attempt (`verification_started`), did not complete.
2. **wsj**: a real re-authentication (`reauth_started` -> `reauth_succeeded`,
   `network_auth_corroborated: true`), succeeded; wsj's job then completed.
3. **barrons**: a real re-authentication (`reauth_started` -> `reauth_succeeded`,
   `network_auth_corroborated: true`), succeeded; barrons's job was still rejected on the replay.

None of these is a governance breach -- each is a cost to this act's own yield, not a governance
issue -- but each is named here rather than silently folded into the plain per-publisher
accounting above.

## Upload (item 5, the CLI path)

`upload-harvest --retrieval-mode backfill --max-objects 1000`, run twice (the second confirming
determinism): `remaining_pending` stayed **11** both times. sa's 3 new articles, wsj's 2 listing
pages and 3 of a group both uploaded cleanly; **all 11 of wsj's new articles' bronze objects wrote
successfully, but their GROUPED silver_append step failed** with `SilverRowError` both times,
identically -- a genuine production defect in `silver_from_bronze`'s WSJ extractor (it pulls WSJ's
entire `__NEXT_DATA__` frontend config blob wholesale, and one page's config held a string where
sibling pages held a boolean, breaking pyarrow's schema inference across the grouped batch). Filed
as row `AMGT_HARVST-Z-W10-S8` (ARMED). **The 11 bronze objects are safe and already confirmed
present** (see Verify below); only their silver rows are missing, recoverable by a future code fix
re-running upload-harvest against the same pending outbox rows, no further vendor call needed.

## Phase 0c -- the silver rebuild (row `AMGT_HARVST-Z-W10-S8`, NO vendor call)

Fixed `lib/opal_data_harvest/silver_from_bronze.py`'s `_extract_wsj`, per the issuer's
`C-HV-SILVER-FROM-BRONZE` contract reading: the article-bearing field (`articleData`) stays a
single nested struct, typed exactly as before; every OTHER `pageProps` key (the frontend config --
ads config, feature flags, optimizely/statsig config, etc. -- the actual source of the mixed-type
conflict) is now kept VERBATIM in one JSON TEXT column (`page_config_json`) instead of being
spread across unstable top-level columns. Nothing dropped, nothing summarised; bronze was, and
remains, the untouched original either way. Two new arms added to `test_silver_from_bronze.py`
(14 -> 16): `test_page_config_mixed_type_key_still_writes` (reproduces the exact
string-where-sibling-holds-boolean conflict across a grouped `pa.Table.from_pylist([...])` batch;
now writes) and `test_no_key_loss_from_bronze_to_silver` (every top-level bronze `pageProps` key is
recoverable from the silver row; `no_key_loss_recovered 7 of 7 missing []`).

**Rebuild, no vendor call:** `python -m lib.opal_data_harvest upload-harvest --retrieval-mode
backfill --max-objects 1000` against the SAME main runtime (the already-held bronze raw files and
the already-existing bronze objects -- `put_article_bronze` found every key already present and
skipped the write; only the now-fixed `silver_from_bronze` extraction and the S3 silver write ran).
Result: `remaining_pending 11 -> 0`, all 11 previously-stuck `wsj:<article_id>` rows now
`status=uploaded`.

## Verify (item 6, RE-MEASURED after the Phase 0c rebuild)

- (a) **bronze_reread 14 of 14, mismatch 0** -- unchanged; bronze was always safe. Every bronze key
  this run put (3 sa + 11 wsj articles) re-reads from S3 and matches its locally-recorded sha256
  exactly.
- (b) **silver_article_rows 14, bronze_articles 14 -- EQUAL**, after the Phase 0c fix and rebuild
  (was 3 vs 14 before the fix).
- (c) Planned vs actual listing pages: 25 planned for every publisher; actual pages are not
  separately counted by `run_job` (it counts accepted/rejected articles, not raw page fetches) --
  sa fetched enough pages to yield 24 accepted + 6 rejected before its 502; wsj fetched enough for
  11 accepted; bbg/ft/barrons fetched 0 pages worth of content before their respective stops.

## The second same-day run, network refused (item 7)

Same command repeated with `HARVEST_REFUSE_NETWORK=1`, same UTC date (2026-09-23, both
00:23:01Z and 00:45:27Z). rc=2. `http_events 0` (confirmed: 0 new "http" events in the delta).
`network_refused_hits 4`, honestly not 0: the bbg probe, and the sa/bbg/ft jobs, each hit the
refuser (`RuntimeError('network refused')`) because none of them had a replayable path for what
this run needed (a live session-check or a fresh session build). **wsj correctly replayed all 11
of its accepted articles from the legacy catalog with zero network calls** (`complete_candidates`).
barrons short-circuited on its own cooldown state (set by item 4's `request_rejected` result)
before reaching any session/network code at all.

## Silver prefixes written

`seeking-alpha/harvest/silver/article/date=2026-09-23/` (3 rows, sa's new articles).
`wsj/harvest/silver/listing_hit/date=2026-09-23/` (2 rows, wsj's listing pages).
`wsj/harvest/silver/article/date=2026-09-23/` (11 rows, written by the Phase 0c rebuild -- 0 before
the fix, per the issuer's own live-bucket measurement).

## Stage-9 line (verbatim, for `AMGT_RESAPP`'s driver)

**stage 9 publications for 992_HK_Equity: 14 articles in silver, run 2026-09-23T00:23:01Z**

(14, matching bronze_articles exactly -- Phase 0c's fix and no-vendor-call rebuild landed the 11
WSJ articles that row `AMGT_HARVST-Z-W10-S8` had blocked.)

## Bottom line

The Phase 0b fix is proven correct under real, adversarial conditions: a real vendor challenge on
the probe, a real verification-repair attempt on bbg, two real re-authentications, and three
different terminal per-publisher outcomes (error, request_rejected x2) all occurred in ONE
invocation, and **every publisher still reached its own recorded outcome and the run never
crashed.** The residual gap was NOT in the handler this order fixed -- it was a separate defect in
WSJ's silver extraction (row `AMGT_HARVST-Z-W10-S8`), surfaced for the first time by this run's
real WSJ content, fixed entirely offline in Phase 0c (bronze was always safe), and closed by a
no-vendor-call rebuild through the same uploader path: silver now holds all 14 of this run's new
articles, matching bronze exactly.

No second live vendor-call invocation was made, in Phase 1 or in Phase 0c. The ONE-RUN RULE was
honored throughout.
