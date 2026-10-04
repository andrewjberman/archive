# NEVER-WIDEN -- COO HALF: NFRA_SPRINTWIN, the first scheduled daily-sprint publish under the window + union

**Signer:** `2.0.0_SA_COO~H`, 2026-10-04 ~21:0xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Request:** `org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/NEVER_WIDEN_REQUEST_NFRA_SPRINTWIN_FIRST_UNION_PUBLISH_20261004.md`
@93151a0af8 (msg 29214). **Candidate:** CLOUD @6c491b6e9d: `infra/aws/lambda/daily_sprint_generator/lambda_function.py`
(@dc86c2b2cd), `daily_reports/scripts/publish_daily_report.py` (unchanged by this act),
`infra/aws/terraform/daily-sprint-generator/main.tf`.

**SIGNED** for the blast radius below. Every outcome is read from the producer's own rule at @6c491b6e9d, printed with
`git show`, and not predicted from the input's shape.

## Writers of the served property: N = 2 for the pages, 1 for the watermark

| key | writers | rule read |
|---|---|---|
| `daily-reports/<D>/{Desktop,Mobile}_DAILY_REPORT_<D>.html` | (1) this function: `_generate` runs `publish_daily_report.py --date D` WITHOUT `--presign`, so it puts exactly the day's two pages; (2) a seat running `/daily-sprint` locally with the same publisher, whose rule this act does not change (with `--presign` it also writes `latest/`, which the function never writes). | `publish_daily_report.py` `main()` and `presign_latest()`; `lambda_function.py` `_generate` |
| `daily-reports/<D>/watermark.json` | (1) this function only. NEW. It is written by `_put_verified` AFTER the pages verified, and only when the window was not reused. | `_generate` (the tail), `_home(day, qa=False)` |
| `sprint/global/platinum/qa_page/date=<D>/` | `{"qa": true}` runs only (`publish_qa`, `_home(day, True)`). Never `daily-reports/`. | `publish_qa`, `_home` |

## Both branches of the first scheduled fire (2026-10-05 20:10Z), from `cut_window`

- **A: a device census dated 2026-10-05 exists.** `end = min(every same-day census generated_at, run_at)`. `start = end - 24 h`,
  because `newest_watermark` finds no earlier watermark under `daily-reports/` (measured 2026-10-04 ~21:0xZ: `s3api list-objects-v2 --prefix daily-reports/` keys ending `watermark.json`: 0; positive control `--prefix daily-reports/2026-10-0`: 8 objects). The keys written are the 2026-10-05 pages
  (overwritten) and the new 2026-10-05 watermark.
- **B: no same-day census.** `end = run_at`, `start = end - 24 h`. The population is pushed history only. The keys written are the
  same.
- **In both branches:** if `end <= start` the run raises before any write. A window over 7 days is capped, and the excess is stated
  in words (`uncovered`).

## The manual path's reachable states (covered by this half)

- **`{"date": D}` for a D with a stored watermark:** the run reuses it (`reused=True`). It overwrites D's two pages and writes NO
  watermark.
- **`{"date": D}` for a D without one, D not today:** `end` is capped at 16:10 ET of D. The run writes D's two pages and D's NEW
  watermark. A D earlier than the next scheduled day becomes that day's window start (`newest_watermark` takes the newest EARLIER
  day), within the 7-day cap. This is the one state the scheduled path cannot reach alone, and it is covered here.
- **`{"qa": true}`:** writes the QA home only. It reads and writes its own watermarks there, so it can never move the served window.

## IAM (the plan's 1 change)

The change grants Put/Get on the QA prefix, Get on the device-census prefix, and ListBucket conditioned on each. It adds no write
outside the QA home. The served `daily-reports/` write is the role's existing grant.

## Rollback, per key

As the request states:
- re-point the function to `sha256:446603c3...` with `safe-apply -replace`, then invoke `{"date": "2026-10-05"}`; the old image
  republishes both pages under its own rule;
- the watermark is inert to the old image and is kept.

Not covered by this half: any key outside the three rows above. A run that writes one is outside this sign-off.
