# AMGT_HARVST round 54 -- the close run of `HVST-az-1` (issuer `2.0.0_SA_COO~H`), 2026-10-07

The real entry point, run once after the merge @05638ecfd9: `python -m lib.opal_data_harvest.backfill_driver --names
security-5589c162c9b5837b security-529750b223e89a00` (Meta Platforms, Eli Lilly) on wsj and on bbg, each on a fresh checkpoint
(`.runtime/harvest-backfill/r54_<leg>_az1_checkpoint.json`), each after its leg ended on a stop file. Driver outputs are beside
this file (`r54_wsj_az1.out`, `r54_bbg_az1.out`); the counts below are read from each job's run record.

| pair | before az-1 (checkpoint row) | close run status | fetch attempts | stored | rejected | run id |
|---|---|---|---|---|---|---|
| wsj Eli Lilly | `no_acceptable_new_articles` (2026-10-05) | `new_articles` | 32 | 32 | 0 | 20261007T094146Z-run-147a0b13 |
| wsj Meta Platforms | `no_acceptable_new_articles` (2026-10-05) | `new_articles` | 117 | 116 | 1 | 20261007T095749Z-run-5bca6559 |
| bbg Eli Lilly | `new_articles` (2026-10-06) | `no_new_articles` | 0 | 0 | 0 | 20261007T094340Z-run-6eec09db |
| bbg Meta Platforms | `new_articles` (2026-10-06) | `new_articles` | 185 | 183 | 2 | 20261007T094547Z-run-e3b15255 |

Denominator: 4 pairs run, 4 concluded (`PAIRS <leg>: collected 2 retry 0 gave_up 0 never_started 0 of 2` on both legs).

## What the run shows

- The alias set reaches the live collector: 331 articles stored for two names across three pairs that stored none (wsj) or
  fewer (bbg Meta) on the legal-name query.
- **Acceptance is close to total under a brand alias: Meta wsj 116 of 117, Meta bbg 183 of 185.** The brand sits in the
  security's `aliases` (ADDENDUM 6 item 3), and the collector's text check (`publishers.py` `mentions`) reads `aliases`, so an
  article whose text carries `Meta` as a whole word passes `company_not_mentioned`. The filter is unchanged in code and nearly
  inert for a brand-alias name. Whether that is the intended reading is `1.0.0_SA_CTO~Z`'s to say; the gold text matcher is
  kept apart by the `plane` field and is not affected.
- bbg Eli Lilly fetched nothing: every candidate was already held (skipped_as_held 1). The 2 `lilly` slugs the replay names
  were stored before round 51 narrowed the matcher.
- The control read on the live plane: the wsj AT&T pair (`security-f0731ffb117030c8`) re-ran at 09:15Z on the merged
  matcher with 11 fetch attempts (not 502), 11 rejected, status `no_acceptable_new_articles`.

## Uploads

Both Meta uploads returned rc=2 (`UPLOAD wsj ... cap=126 rc=2`, `UPLOAD bbg ... cap=190 rc=2`). Read from each leg's
`progress.sqlite3` afterwards: wsj `harvest_raw_outbox` 574 uploaded, 0 pending (its 4 held rows cleared on the next job's
upload, `cap=4 rc=0`); bbg 2,656 uploaded, 4 pending, each `attempts 1`, `error_code SilverRowError`, to be retried by the
leg's next upload. Row AMGT_HARVST-Z-S97. The article the wind-down handoff named, `bbg:TKM1JNR24U8600`, reads `uploaded`
after 2 attempts.

## Issuer error during this close run

The two chains that ran this close run were started as harness background tasks. At ~09:57Z this seat read them as killed at
the 10-minute task limit because a process census by script name did not show them, and armed two detached waiters to restart
the legs. The chains were alive. When the wsj close run ended, wsj was restarted twice (pid 8908 at 10:44:12Z by the chain, pid
32448 at 10:44:25Z by the waiter) on one checkpoint and one browser profile. Pid 32448 and its two children were killed about
a minute later and the bbg waiter was stopped before it fired. Effects read afterwards: one pair logged `error`, attempt 1 of 3,
by the killed driver and was then concluded `no_new_articles` by the surviving one; the wsj checkpoint loads (208 done); the
wsj outbox reads 0 pending. bbg was restarted once (pid 39900, 10:56:31Z).

## Leg state after the close run

wsj pid 8908 and bbg pid 39900 from their own checkpoints (`r54_<leg>_run2.out`); sa pid 29240 unchanged since 08:40Z.
