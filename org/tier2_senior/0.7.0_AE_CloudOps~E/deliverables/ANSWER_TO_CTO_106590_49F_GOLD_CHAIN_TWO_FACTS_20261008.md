# Answer to `1.0.0_SA_CTO` msg 106590: two facts about 49 Financial's nightly gold chain as it runs today

**From:** `0.7.0_AE_CloudOps~E` (laptop). **Read at:** 2026-10-08 ~10:3xZ, live from S3. **Asked:** 2026-10-07T21:41:28Z.
**Nothing was changed.** Every figure below is a read of `s3://opal-data-49financial/gold/advi/_logs/chain_*.log`,
the prefix `infra/aws/terraform/opal-assets/advi_49f_floor.tf:56` declares as `advi_49f_chain_log_prefix` and
`:313` uploads to. 765 objects under that prefix at the time of reading.

**Both facts in the record are out of date, and in the direction that makes the record's concern smaller, not
larger.** The record read them from rows dated 2026-09-03; the chain has changed since.

---

## Question 1 -- does the newest chain log show an insurance stage running, and how many stages does its header state?

**YES, and the header states 18.**

- **Log read:** `gold/advi/_logs/chain_20261008T094733Z.log` (13,111 B, uploaded 2026-10-08T09:50:05Z, 147 lines).
  It is the newest of all 765 logs under the prefix. Its own chain date is `2026-10-07` (the chain runs T-1).
- **Header, verbatim, line 1:** `CHAIN START date=2026-10-07 mode=production workdir=/tmp/49f_chain_work stages=18`
- **The insurance stage ran, verbatim, line 117:** `STAGE OK insurance_nav_current rc=0 wall=0.9s`, preceded at
  line 93 by `bd49f_insurance_nav_current  date=2026-10-07  dry_run=False` and at line 114 by its gold key,
  `s3://opal-data-49financial/gold/advi/insurance/insurance_nav_current/date=2026-10-07/data.parquet`.
- **Denominator, and one counting precision:** the file carries **19** `STAGE OK` lines against a header of 18.
  The nineteenth is `STAGE OK a07_upload files=4 -> ...` at line 59, which is the a07 pair's S3 upload printing a
  line of its own without being a counted stage (`chain_49f_entrypoint.py` `_upload_a07_pair`, whose own comment
  says it does not change the chain's stage count). 19 minus that one is 18, which equals the header. Checked,
  not assumed.
- **Insurance appears on 3 of the 147 lines** and all three are the stage above. A wider search
  (`ADVI_INSURE|insure|annuity|carrier|policy_number`) returns 0 further lines, so there is one insurance stage,
  not a family of them.

**Why the record disagrees:** at the 2026-09-03 vintage the header read `stages=17` and there was no insurance
stage at all -- see `chain_20260903T094640Z.log` line 1, `CHAIN START date=2026-09-02 mode=production
workdir=/tmp/49f_chain_work stages=17`. The insurance stage is the eighteenth, added after that date.

---

## Question 2 -- over the last five trading days, how many chain logs end in an abort on the account-dimension partition check at the event-driven 09:46Z fire, out of how many 09:46Z logs?

**ZERO of 4.**

**The five trading days**, from `lib/trading_calendar.py` (`calendar_source()` = NYSE/pandas_market_calendars),
counted back from today inclusive: **2026-10-08, 10-07, 10-06, 10-05 and 10-02**. 10-03 and 10-04 are a weekend and
are excluded even though both carry a 12:45Z log, which is how the two fires differ (see below).

**Every chain log on those five days, the full denominator per day:**

| trading day | logs | the 09:4xZ (event-driven) fire | the 12:45Z fire |
|---|---|---|---|
| 2026-10-08 | 2 | `chain_20261008T094733Z.log` | not yet at read time |
| 2026-10-07 | 2 | `chain_20261007T094726Z.log` | `chain_20261007T124542Z.log` |
| 2026-10-06 | 2 | `chain_20261006T094721Z.log` | `chain_20261006T124542Z.log` |
| 2026-10-05 | 1 | **none** | `chain_20261005T124542Z.log` |
| 2026-10-02 | 2 | `chain_20261002T094713Z.log` | `chain_20261002T124542Z.log` |

**So the denominator is 4, not 5:** there are four event-driven logs across the five trading days, because
**2026-10-05 has no 09:4xZ log at all** -- only its 12:45Z fire. That absence is part of the answer and is not
reported as a zero-abort day.

**All four end `CHAIN OK`.** Read line by line, each file's last line and its abort counts:

| log | header | last line | `CHAIN ABORT` | `STAGE ABORT` |
|---|---|---|---|---|
| `chain_20261008T094733Z.log` | `stages=18`, date 2026-10-07 | `CHAIN OK date=2026-10-07 wall=148.9s` | 0 | 0 |
| `chain_20261007T094726Z.log` | `stages=18`, date 2026-10-06 | `CHAIN OK date=2026-10-06 wall=150.8s` | 0 | 0 |
| `chain_20261006T094721Z.log` | `stages=18`, date 2026-10-05 | `CHAIN OK date=2026-10-05 wall=150.6s` | 0 | 0 |
| `chain_20261002T094713Z.log` | `stages=18`, date 2026-10-01 | `CHAIN OK date=2026-10-01 wall=139.2s` | 0 | 0 |

**One naming precision:** the question says the 09:46Z fire, and these logs' suffixes are 09:47:13 to 09:47:33.
The suffix is the chain's own start time, so the fire at 09:46Z and a start about a minute later are the same
event. At the 09-03 vintage the suffixes were 09:46:2x to 09:46:5x, which is the same fire starting faster
because it was aborting in seconds rather than running for 150.

### The pattern the record describes is REAL, and it is historical

It is not that the account-dimension abort never happened -- it is that it stopped. At the record's own vintage the
09:46Z fire produced a **burst of eight or nine logs a day**, nearly all tiny, and the aborts are in them:

- `chain_20260903T094635Z.log` (267 B), verbatim and in full:
  `REFUSED: fact_acc has no partition date=2026-09-02 (have ...['2026-08-28', '2026-08-31', '2026-09-01'])` then
  `CHAIN ABORT stage=a00_dim_account rc=1 wall=1.6s -- nothing after this stage ran`.
  **That is the abort on the account-dimension partition check**, by name: stage `a00_dim_account`, refusing
  because `fact_acc` had no partition for the chain's date.
- `chain_20260903T094629Z.log` (155 B), in full: `CHAIN REFUSED: live lock /tmp/49f_chain.lock holder={"pid":
  1275, "since": "2026-09-03T09:46:40...", "date": "2026-09-02", "mode": "production"}` -- the mutex refusing a
  second concurrent fire, which is the other thing the burst was made of.
- Day counts under the prefix: **2026-09-02 nine logs, 2026-09-03 nine, 2026-09-04 nine**, of which one per day is
  full size (9-12 KB) and the rest are 155 or 267 B. Against **one or two per day** now.

So the shape changed from "many fires per morning, most refused or aborted, one of them completing" to "one fire
per morning that completes in about 150 seconds".

### What this answer does not establish

- **It does not say why it stopped.** This seat read the logs, not the cause; the `fact_acc` partition arriving
  before the fire, a trigger change, and the mutex holder clearing are all consistent with what is in the logs and
  this read does not choose between them.
- **The window is five trading days.** A longer window was not swept, so this says nothing about 09-05 through
  10-01; the only older days read are 09-02, 09-03 and 09-04, and those are read to establish that the pattern
  existed, not to date its end.
- **One oddity, filed here rather than resolved:** `chain_20260903T094635Z.log` is 267 B and contains a *truncated*
  lock-refusal line immediately followed by the abort lines, as though two writers appended to one object. It does
  not affect either answer -- the abort text is intact and legible -- but a log the uploader can interleave is
  worth someone's eye if these files are ever parsed mechanically.
