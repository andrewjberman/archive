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

## ADDENDUM A -- COO half EXTENDED (2026-10-04 ~21:5xZ; request @55bb66278d, msg 29255)

**EXTENDED** to the one served re-run `{"date": "2026-10-04"}` on the new image and its three named keys:
- the 2026-10-03 seed watermark (a NEW writer: the builder by hand, once, with read-back, before the invoke);
- the 2026-10-04 two pages (overwritten);
- the 2026-10-04 watermark (NEW, written last by the function).

Each outcome is read from `cut_window` @dc86c2b2cd.

**Measured at signing:**
- watermark keys under `daily-reports/`: 0;
- the 2026-10-04 device censuses present: `sitez.json` (LastModified 21:05:45Z) and `laptop.json` (21:35:15Z);
- commits on any ref with commit time in [2026-10-03T22:15:00Z, 22:16:00Z): 0 (`git log --all` after a fetch); control
  [22:00Z, 22:15Z): 12. So the seed cut neither drops nor double-counts a commit against the served 2026-10-03 page.

**The branch the addendum leaves implicit, covered here:** `limit` in `cut_window` depends on WHEN the invoke runs.
- **Invoke while it is still 2026-10-04 in New York (before 2026-10-05T04:00Z):** `limit = run_at`. Then
  `end = min(each 2026-10-04 census generated_at, run_at)`, about 21:05Z on today's files.
- **Invoke after 04:00Z:** `limit = 16:10 ET of 2026-10-04 = 20:10Z`, so `end = min(census stamps, 20:10Z) = 20:10Z`. Commits
  between `end` and the run fall in 2026-10-05's window, which starts at this `end`. It stays contiguous and loses nothing.

In both cases `start` = the seed's `window_end`, 2026-10-03T22:16:00Z, and the window is under the 7-day cap.

**Not covered:**
- a `{"date": "2026-10-03"}` invoke on the new image, which would REUSE the seed and republish 10-03's pages;
- a second 2026-10-04 invoke that is anything other than the rollback;
- any key outside the three.
