# MDPF evidence freeze + rollback baseline + schema baseline

**TO:** `MDPF_CANRTE.P0-1.evidence-freeze-rollback-baseline` · **Owner:** `0.7.0_AE_CloudOps~Z`
**Captured:** 2026-08-06T20:45:23Z (plane) / 2026-08-06T21:01Z (schema) · **Account:** 313476888478 · **Region:** us-east-1
**Read-only.** No AWS resource, S3 object, schedule, Lambda, IAM policy or served artifact was modified.

One artifact serving two purposes, per COO~Z: this **is** `04_VALIDATION_ROLLBACK_AND_OPEN_HOLES.md` §4's
rollback capture. It was not built twice.

## Contents

| File | What it is |
|---|---|
| `evidence_freeze.json` | Live plane at 20:45:23Z — Lambda config/SHA/layers/roles/env, IAM policy documents, schedules + classic rules + targets, S3 versioning + VersionId/ETag per served key, EC2 + volume + snapshot inventory, SSM documents |
| `schema_baseline.json` | Observed field set + types for every undated served object plus the newest dated partition per family — the before-image for doc 04's "platinum preserves each artifact's schema contract" |
| `capture_evidence_freeze.py` | The capture, re-runnable |
| `capture_schema_baseline.py` | The schema capture, re-runnable |
| `landing_census.py` | 30-day per-feed landing-clock census (H1/H2 denominator; feeds the P0-2/P0-3 probe design) |

## Method, and the discipline that is load-bearing

- **boto3 with explicit pagination.** Page counts are printed. A count that was never paginated is a page
  size wearing a total's clothing.
- **Timestamps are tz-aware UTC serialised with `+00:00`.** No `aws s3 ls` column appears anywhere in this
  capture — see *Instrument hazards* below.
- **Every retrieval failure is recorded as a structured value, never swallowed.** A retrieval failure
  returns a VALUE; a swallowed one reads as absence.

## What was captured

| Surface | Denominator |
|---|---|
| Lambdas | 5 requested, 4 captured — `mdpf-freshness-checker` **does not exist** (ResourceNotFoundException, recorded) |
| IAM roles | 4, inline + attached policy documents in full |
| Scheduler | 3 MDPF schedules, all ENABLED, matching `01_VERIFIED_FINDINGS.md` §4 byte-for-byte |
| Classic rules | 139 across 2 pages, 1 MDPF-matching |
| `platinum/mdpf/` | 461 objects — 22 undated served keys frozen in full, newest 3 dated |
| `json/mdpf/` | 10 objects, all frozen (the do-not-touch bell) |
| `portal/gold/mdpf/` | 52 objects |
| `gold/mdpf_revamp/_aggregate_aua/` | 440 objects |
| S3 versioning | `opal-data-assets` Enabled · `opal-data-portal-v2` Enabled |
| EC2 | `i-02448edb624a7a7cf` stopped, sole volume `vol-071d4d9e2d169bbb9` (50 GiB gp3, encrypted), **`DeleteOnTermination=True`** |
| SSM | 19 self-owned documents across 2 pages, **0 MDPF-matching** — the chain uses an AWS-owned document, so there is no custom SSM document to retire |

## Findings

**1. `count_as_of` exists on exactly one served key.** `platinum/mdpf/global/aggregate-aua-timeseries.json`
carries `count_as_of`; its **twelve siblings do not**. A cutover that builds every aggregate-aua-timeseries
artifact through one uniform firm-parameterized path — which is what is being built — drops a field from
precisely one served key, the global one. **A spot-check sampling one key per artifact family would pass.**
The uniformity being introduced is the mechanism that breaks it, and the natural verification shape is blind
to it by construction.

**2. The served surface has SEVEN as-of field families, not two.**

| Family | Count | Where |
|---|---|---|
| `as_of_first, as_of_last, dates, n_dates` | 12 | aggregate-aua-timeseries, both spellings |
| `generated_at` | 9 | account-distribution, non-model-assets |
| `dates, last_updated` | 6 | aum-metrics |
| `as_of_last` | 4 | etf_ownership_timeseries DIVZ/IDVZ/PFDE/PFOE |
| `as_of_by_partner, as_of_date, generated_at` | 2 | dated aggregate_aua |
| `assignment_date, generated_at, value_date` | 1 | cottonwood/account-units |
| `as_of_first, as_of_last, count_as_of, dates, n_dates` | 1 | global/aggregate-aua-timeseries |

**3. `as_of_date` — the field the brief names as *the* platinum convention — appears in 2 of 23 sampled
objects.** Aligning the surface to the documented convention would rename the as-of field on 21 served
objects.

**4. Both spellings of the aggregate timeseries are served.** `49financial` and `inflection` each serve
`aggregate-aua-timeseries.json` **and** `aggregate_aua_timeseries.json`, same schema family. Recorded,
untouched — NEVER#3 and the H6 bound both apply.

**5. Snapshot retention is 30 days, measured.** `infrastructure-snapshot-daily` `cron(0 7 * * ? *)` →
`infrastructure-daily-snapshot`; `REAPER_RETENTION_DAYS = 30`, `REAPER_TAG_KEY='Purpose'`,
`REAPER_TAG_VALUE='DailySnapshot'` at `lambda_function.py:40-42`, corroborated by the measured window
(31 dailies, oldest 2026-07-07). **The existing daily snapshots are not permanent, and naming them
DO-NOT-DELETE in a document does not protect them — the reaper reads tags, not deliverables.**

## ⛔ This is a BEFORE-IMAGE, not a spec

Per open hole **H6**: the seven as-of families, the duplicate spellings, `firm_id`, and `scope=null` are
**facts to preserve, not defects to reconcile.** Nothing here is a cleanup backlog. A schema migration is
out of scope and separately tested if ever in scope. The four OWNTS objects are baselined even though their
disposition is removal — a retirement still needs a before-image for rollback.

## Scope limits — what this does NOT close

- It captures the **plane and the served surface**, not the EC2's on-disk state. That is P0-7, whose
  enumeration runs during the production-initiated 09:00 ET window.
- The orchestrator tie (`mdpf-daily-dispatch.sh` deployed == repo, sha256
  `cc3c6b56d40f12b4a87edada0a2263d2d19aff7e4fbd191ceeb10d1d93836ff7`, 688 lines, diff 0) **narrows H8 for
  that one file and closes nothing else** — it says nothing about the `.py` modules or site-packages.
  A narrowing is not a closure.
- The landing census bounds the **current pipeline clock**. Silver `LastModified` is when the converter
  wrote, not when the vendor made data available. It does **not** close H1 or H2.

## Instrument hazards found while producing this

Three separate instruments returned confident wrong answers during this capture. All three were caught by a
control, none by care, and each produced a **clean, plausible result** rather than an error.

1. **`aws s3 ls` prints LastModified in LOCAL time; `s3api` returns UTC.** On this ET box a UTC-labelled
   parse of the `s3 ls` column shifts every reading by the offset. A first pass read the Eclipse feed
   landing at 06:16 ET instead of 10:16 ET — which would have collapsed open hole H1 entirely. Caught by
   head-object vs `s3 ls` on one identical object. **Any clock claim cites the s3api ISO-8601 value with its
   `+00:00`.**
2. **`--no-paginate` returns only the FIRST PAGE.** `lambda list-functions` returned 50 of 196 — a 74%
   shortfall — showing one `smartx` Lambda where seven exist. One step from reporting a fabricated
   production outage ("enabled schedules firing at non-existent targets"). Caught by per-target checks with
   a positive **and** negative control. The failure shape is a **clean empty/short result**, indistinguishable
   from a real absence.
3. **A multi-alternation `grep` returned zero matches on a file containing the token** (MSYS de-escapes the
   pattern into something valid-but-different). Caught only by an independent expectation from a docstring.
   `comp-grep` prints its denominator and routed correctly throughout.

The common shape: **each returned the more interesting answer, and each would have been recorded as a
finding.** A result that would delete an open question is the one most worth a second oracle.
