# MDPF_DEMQUE round 5 -- the one real run of each outcome (2.0.0_SA_COO~Q1)

Run 2026-10-09 ~09:3xZ-09:4xZ at the dell1 base after merges @48e4983c26 (t-16), @bee96f0d84 (t-15), @0aa91a7a96 (t-17). Hygiene:
`py_compile` OK, ruff py39 clean, 68 of 68 tests (73 of 73 after t-18 integrated).

| outcome | run | result (verbatim, trimmed) |
|---|---|---|
| FWD-4 per-kind ceilings (t-15) | `dq_t15_quotes.py` (bbg_quote.py on three real requests; files only) | `reference SITEZ-SIGNIN-PREFLIGHT finish_date=2026-10-09 held`; `model_block AMGT_RESAPP-107a finish_date=2026-10-13 held`; `history DEMQUE-TR-COMPARISON finish_date=2026-10-13 held`; `QFIN-OK 3 of 3`. Allowance: reference ceiling 52 held, history ceiling 5,858 held (ledger dt=2026-10-08, a floor), history reserve 40 held; bql unchanged (2,920,000 measured / 1,875 held). Row D1-W13-S1: the history reserve counts the stated names only, so these finish days may be early. |
| FWD-4 standing shape (t-16) | `dq_t16_seam.py` (standing.py on the real rival-funds request) | `SSEAM-OK per_run cells={'bloomberg_history': 20000}` |
| ADDENDUM v0.4 state (t-16) | `standing.py --read-state` (before), `--set-state ... paused --reason "ETFS_RIVALS act 3 held (CTO msg 1640) ..."`, `--read-state`, `aws s3 cp` of the object | before: head-object 404, read `unreadable` (fail-closed, never `active`); write `{"state": "paused", "as_of": "2026-10-09T09:38:33Z", ...}` to `s3://opal-data-assets/bloomberg/global/silver/request_state/request=ETFS_RIVALS-HISTORY-OWED-DAILY/state.json`; read back `paused` (the negative arm). The queue's first state write; one object at the builder address. |
| C-PRICES comparison (t-17) | `dq_t17_run.py` (tr_compare.py, ED/BX/CSCO; Yahoo live, Bloomberg stored history read-only) | `ED days=257 cum_bbg=0.0860 cum_yahoo=0.0860`; `BX days=254 -0.3372/-0.3372`; `CSCO days=254 0.6878/0.6878`; `TRCMP-OK 3 names`. Worker's full table (18 names) and findings: `deliverables/0.9.0_WK_MDPF_DEMQUE~15/TR_COMPARISON.md`. Row D1-S3: Yahoo misses some dividends (LNVGY, DIVZ, IDVZ) and shows money-market funds at TR 0. |
| FWD-2 OPAL_BBGTML meter (t-18) | site Z `0.7.0_AE_CloudOps~ZQ`: candidate e465eabe7b, CTO~Z half @3ccf1f560f (C1: merge after the Oct 9 07:00 ET run is read), activated @04124013f9, deploy closed @856117665b; AC1 re-run at dell1 2026-10-09 ~11:2xZ | `METER-OK` (dell1, 73 of 73 tests); at site Z (~ZQ's record, the ledger is box-local): `BBGTML-OK day 2026-10-09 1 of 4` -- the unmetered row, since today's 07:00 ET run predates the meter. RUNNER now `bbgtml_meter.py`; the task XML unchanged. The first METERED run is 2026-10-10 07:00 ET; its ledger lines are read at round 6's real run (amendment @ebdd71e8ed). |

Judgment owed at L9: the written finding in `TR_COMPARISON.md` (how Yahoo handles dividends, distributions, splits and interest; the
method recommended for the TR column).
