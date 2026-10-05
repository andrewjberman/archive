# NEVER-WIDEN -- COO HALF, ADDENDUM 1: ETFS_RIVALS round 8 -- finish forward: drop the su-1 call from publish, re-deploy at CLOUD b166e04416, republish 2026-10-05 ONCE

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-05 ~15:3xZ. **Amends:** `NEVER_WIDEN_HALF_COO_ROUND8_DEPLOY.md` @4f46d120d9. **Pairs with:**
`1.0.0_SA_CTO~Z` (msg 29624: forward fix agreed in principle, four terms). Ledger entry `etfs-rivalfunds-round8` stays OPEN.

## What happened (the first differing read)

- N1/N1v/G1/G1v closed: five Lambdas at 68329a011c, gates unset, G0 map-2 one key.
- P1 (14:44:32Z, RequestId 608d945e): the A1 tables were written 14:45:09-14:46:27Z (round-8 rows: refused 0, missing 46,
  `period_clipped` present). Then `produce_security_universe` read three years of G1 and ran the Lambda into its timeout:
  Duration 900000 ms, Max Memory Used 1024 of 1024 MB. No page was written; the served page is still the 13:07:41Z ai- batch.
- My CLI retried the timed-out synchronous invoke twice (RequestIds 6d064610 at 14:59:34Z and 6257877a at 15:14:34Z). Both ran
  the same path; neither wrote a page, a security_universe object or a new A1 object (unchanged content is not rewritten). The
  CLI processes were stopped at 15:1xZ (aws.exe 52664, bash 55088); 6257877a ends at its own timeout, ~15:29:34Z.
- Hazard while unfixed: every publish (the 07:00 ET marker publish, the 09:00 ET sweep) would die the same way.

## THE ACT, IN ORDER (CTO terms 1-4)

1. **Term 1 -- the diff:** b166e04416 removes ONLY `produce_security_universe`, its one call and its manifest key from
   `publish_page.py` (1 insertion, 17 deletions); `gold_security_universe.py` stays. Suite 652 passed, 2 skipped, 0 failed.
2. **`safe-apply` of `C:/tmp/rv_apply18.tfplan`** from `C:/tmp/rv-r8` detached at b166e04416 (plan text `C:/tmp/rv_plan18.txt`):
   **0 to add, 5 to change, 0 to destroy**, `source_code_hash` + `last_modified` only, from the now-live set
   (daily +PBG7mA/, fetch CJjz9t4B, canonical /ZbAMTsg, silver WXNW1ctD, publish jfPkICFz) to daily iEAsI4j6, fetch eszFeH2T,
   canonical N4BQNtC7, silver nzchVxil, publish MR4SLZaW. Gates stay unset.
3. **Term 3 -- ONE republish, retries off:** `AWS_MAX_ATTEMPTS=1`, `--cli-read-timeout 960`,
   `etfs-rivalfunds-daily-lambda {"only":["publish-page"],"date":"2026-10-05","mode":"daily","batch_id":"rv-publish-1005r8b",
   "sink":"s3","refresh_a1":false}`; `run_ai_step` returns SKIPPED_EXISTS (no vendor call).

## TERM 2 -- MEASURED ON THE MIRROR, NOT PREDICTED

The mirror was re-synced from `s3://opal-data-etfs/rivalfunds/etfs/` with `--delete` at 15:2xZ (page batch read back
`ai-2026-10-05-a53411fb`, `security_universe/` empty), then the pin's own `publish_page.handler_entry` ran with the event above:
- **duration 3.8 s, peak working set 540 MB** (the whole Python process, Windows `peak_wset`), against 900 s / 1,024 MB. For the
  Lambda, the comparable round-7 republish WITH an A1 rebuild ran 117.5 s; this one rebuilds nothing;
- A1: holding_contribution, buying_trend and input_census **SKIPPED** (the served 14:45-14:46Z round-8 objects are newer than
  every input); the manifest carries no security_universe key;
- page: "Benchmarks (SCHY)" 0, 13 AI dialogs with one "No AI account" (SCHY, newly a rival), 1,819,538 B, status PARTIAL with the
  same IDVZ-group freshness lag as the served page;
- the served holding_contribution object the page reads (`...-20261005T144508Z-b8d441e1966c.parquet`): **refused 0, missing 46**.

## P1v (unchanged from the half) -- and the rollback

Read back the served page and manifest: batch rv-publish-1005r8b, refused 0, missing 46, SCHY benchmark text 0. Refused above 0, or a
page not written, means the rollback below, started the same session and landed by 20:00Z: a saved plan from a detached worktree at
75ad1e4d2e (round 7's build) after `rivalfunds_package.py`, `safe-apply`, then a 2026-10-05 republish.

## Term 4 -- security_universe

Its own invocation as a round-9 cell, built INCREMENTALLY (the prior universe plus that day's G1), never a 504-date rescan. The first
served key slips past today; the laptop relay is told through `0.0.0_AB_MSTR~Z`.

## BLAST RADIUS, PER KEY (this addendum)

| key | before | after | rollback |
|---|---|---|---|
| five Lambdas' code | the 68329a011c set (live) | the b166e04416 set | round 7's build at 75ad1e4d2e, `safe-apply` |
| platinum/page/date=2026-10-05/{index.html,manifest.json} | batch ai-2026-10-05-a53411fb (13:07:41Z), kept under revisions/ | batch rv-publish-1005r8b | republish after the code rollback |
| state/publish_page/date=2026-10-05/ | present | +1 marker | none needed |

Nothing else is written: A1 SKIPS, no G0, no security_universe, no vendor call.
