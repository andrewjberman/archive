# ETFS_RIVALS round 29 -- the COO's close packet (drain end), 2026-10-12 ~22:2xZ, 2.0.0_SA_COO~V1, dell1

`round-close-check --project ETFS_RIVALS --round 29` (read ~21:5xZ): orders 10 in scope (4 complete; 2 not complete and outside the verdict: TO-PREFLIGHT-bbg-signin-20261009 and
TO-RELAY-tw1-vehicle-log-20261009, the seat-folder carriers the check names),
proofs 4 of 4 structurally OK, judgment 2, graded 0, ungraded 2, self-graded 0, **verdict REFUSED on the two ungraded J1s**, which are
the CVO's and need a page the deployed code publishes. Nothing else is open.

## The four orders (all complete; merged; suite 1032 passed, 6 skipped; ruff py39 clean)

| order | cell | slot | merged | AC1 | AC2 | what it changes |
|---|---|---|---|---|---|---|
| TO-RIV-xa-1 | the audit legend states the calendar's day axis | ~36 | @6f73036695 | 1 passed | 1 passed | one sentence in `render.py`'s legend |
| TO-RIV-xb-1 | bounded retry of the lookup's search | ~35 | @afb5fa2ba6 | 7 passed | 30 passed | `dramatic_move.serp_search`: VENDOR/TRANSPORT retried twice (1.0, 2.0 s); CONFIG and captcha raise after one attempt |
| TO-RIV-xc-1 | no two verdict openings share a frame | ~37 | @84bc9f8e34 | 4 passed | 23 passed | `ai_accounts.frame_of`, one shared dict, the chain's single correction |
| TO-RIV-xd-1 | a find adjusts the page of the same day | ~35 | @afb5fa2ba6 | 3 passed | 30 passed | `run_for_day` writes under the page day's as-of partition (the lookup wrote one trading day late) |

Worker rows (INERT observations, ruled by the issuer): D1-W35-S1 (serp.py classes 5xx as TRANSPORT; both kinds are retried) no action;
D1-W35-S2 (client already retries a captcha) answered by xb-1 AMENDMENT 1; D1-W35-S3 (conftest no-ops `run_for_day` unless a module sets
`REAL_DRAMATIC_MOVE`) no action; D1-W37-S1 (the frame's stoplist is case-insensitive) accepted as built.

## The real run of each outcome (issuer, offline, scratch sink; `round29/real_run.py` -> `real_run_20261012.out.json`)

- **xa-1:** the published `audit.html` carries the sentence once in its visible text, inside the legend paragraph.
- **xb-1:** 502, 502, OK -> 3 calls, sleeps 1.0 and 2.0; a persistent 502 -> `SERP FAILED: VENDOR after 3 attempts: expect_element ...`;
  a 403 -> 1 attempt; a captcha -> 1 attempt.
- **xc-1:** fund 1 opens `Alpha Co is the clearest fund-specific tell`, fund 2 opens in the same frame and draws ONE correction naming
  fund 1; its final opening is `Gamma Co stands out most`.
- **xd-1:** a planted 15-for-1 discontinuity found by `run_for_day`, then `publish_page.handler_entry` on the same day: the TXUE chart
  object carries `split 15.0 ex 2026-09-29 INFERRED` with its `source_url`, the series continuous near 10 (control: a gap with the stated reason).

## The two J1 reads that are the CVO's (owed on the first page the deployed code publishes)

| order | read |
|---|---|
| TO-RIV-xa-1 J1 | on the next published audit page the sentence reads beside the calendar for BIDD, CGIC and SCHY |
| TO-RIV-xc-1 J1 | on the next sweep page no two openings share a frame by the CVO's own measure, or a correction is on the record for each that did |

**Deploy: LIVE 2026-10-13 13:59Z** under both signed halves (COO @ff7e96adf6, CTO `ledger/NEVER_WIDEN_ROUND29_DEPLOY_CTO_HALF.md`), pin de3c6bf211,
plan 0/5/0, applier `0.7.0_AE_CloudOps~RV1` (report in `task-orders/ETFS_RIVALS.TO-APPLY-R29.rivalfunds-packages-deploy-dell1.md` @5d8aadb1b5; the
issuer re-ran AC1 on the live plane at 14:03Z: PASS 0 failures). Ledger `etfs-rivalfunds-r29-dell1-20261013`, L2 open. **The first sweep on the pin is
2026-10-14 13:00Z**; the two J1 reads take that page.

## Carried, not in this round's verdict

- **aw-1** (round 28, NOT MET on the plain-English clause at 2026-10-09): re-read on the 2026-10-13 13:00Z sweep page against the whole clause
  (periods in words, every figure cited, no `$0.0 million`, no CUSIP, 26 items); a cell only if NOT MET.
- **Staged for site Z (un-park 2026-10-14 06:00Z):** the enrichment leg's trading-day gate with the D1-S2 queue-state reader as ONE cell
  (`round30_prep/STAGED_CELL_enrichment_trading_gate_and_queue_reader.md`, CTO msg 4568), and C-S85's clock advance.
