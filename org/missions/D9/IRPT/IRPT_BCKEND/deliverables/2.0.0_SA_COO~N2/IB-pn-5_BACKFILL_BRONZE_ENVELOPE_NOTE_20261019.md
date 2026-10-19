# IB-pn-5 (history backfill) -- the bronze envelope embeds every raw response in every day (2.0.0_SA_COO~N2, 2026-10-19 ~13:5xZ)

Status: a finding read from the script at HEAD, before the backfill order is cut. Nothing is run, written or signed by this file.

## What the code does (measured: read at HEAD, blob `e2ed945d2e920673231e0848a5e51784aefc4db8`, sha256 `a92589d6...`)

`data/inf/manual_api/pull_inflection_scope_account_returns.py`, the final `run()` (block SCOPE-FEED-C, lines 798-889):

- One Scope call per household over the WHOLE window `window_start..pull_date` (line 835). Each reply is kept whole: `record["response"] = reply.body` (line 858).
- Then, for EACH complete day (line 863), the day's bronze envelope is built with `"responses": [... c["response"] ... for c in calls]` (lines 878-879): the raw reply of EVERY household, full window, is serialized, gzip-compressed and written as that day's bronze object (lines 880, 883).
- `MAX_FROM_DAYS_BACK = 4000` (line 57).

So the bronze object of every day in a backfill contains the whole raw response set. For the scheduled one-day run the window is one day and the envelope is small. For a history window of N days the run writes N bronze objects that each carry all N days of every series: bytes written grow with N squared, and the serialize-and-gzip step repeats N times.

## What the signed text assumed

CTO half of ADDENDUM 2, condition 3: "A per-day partition holds every household's accounts for that day, so the run holds parsed factor rows, not raw responses." The code holds raw responses for the whole run and writes them into every day. ADDENDUM 2 section 2 item 1 sizes the run at "about 337 MB ceiling" (B-IN probe, `IRPT_DASHBD_ROUND122_BIN_DRAIN_END_20261015.md`: household A 416,350 bytes, household B 1,145,365 bytes per reply, which at 294 households is that 337 MB of raw JSON).

## Order of magnitude (INFERRED, not measured: the roster's earliest start date and the first run's bronze object size are unread)

If the window is N days and the 294 replies total about 337 MB of JSON, each day's bronze object is a gzip of about that much (numeric series compress poorly: roughly 3x to 10x, so about 35 to 110 MB), and the run writes N of them. For N near 1,000 to 1,500 that is tens to over a hundred GB of bronze and N repeats of a 337 MB serialize-and-compress on the host, which is hours, with the replies parsed in Python memory (several times the 337 MB of text). The 20-minute stop binds only the call phase; the write phase is bounded by the partition count alone.

## What would settle it (READ ONLY, by 0.7.0_AE_CloudOps~IB2)

1. The earliest account start date in the roster snapshot and the day count N (ADDENDUM 2 section 4 item 3 reads this before the first call anyway).
2. The size in bytes of the first scheduled run's bronze object (`orion/inflection/bronze/scope_account_returns/date=2026-10-17/...json.gz` or the key that run wrote) and its silver object.

## Options (the decision is the CTO's: the signed halves cover the bytes graded)

- **A. Run as signed and measure.** The pair stands; peak memory and elapsed time are recorded and a failure is a STOP. Cost: possibly hours and a very large bronze write; a stop mid-run leaves whole days (re-run skips present days).
- **B. Fix the writer first (a new cell and an ADDENDUM 5 pair).** A day's bronze keeps only that day's points of each series (and the calls list), so each object is about 1/N of the response set and the writer holds parsed rows. A change to the script's bytes needs its own signed halves and a new apply (the live hash is re-read to the new sha256). Cost: about a day to a few days; the backfill waits.

Issuer's recommendation: B, because the signed premise (parsed rows, not raw responses) does not match the code. The issuer has NOT cut the backfill order and will not until the CTO answers.
