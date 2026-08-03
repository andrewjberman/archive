# MDLP_MONPUB W4 producer-side trace: the 0730 wrong-instrument mechanism, the login-scoped Bloomberg block, and the clean sitez production path

**archetype:** TRACE
**Author:** `0.0.0_AB_MSTR~Z` · 2026-08-03 · Requested by `1.0.0_SA_CTO` (via base MSTR, bus msg 6b6851d5, "after promote, not blocking")
**Evidence class per Rule 22/22a: every claim below is labeled SOURCE / ARTIFACT / LIVE / INFERRED.**

---

## 1. Scope

Three producer-side questions the fix order (W1-W4) depends on but does not itself answer:

1. Why did the 2026-07-30 data.pkl carry a garbage `.ST Index` series that BUILT SUCCESSFULLY (the
   W1 near-miss), while the 2026-07-31 pkl crashed loudly on a different defect?
2. Is the Bloomberg `-4003 LIMIT/REVIEW` refusal universal or login-scoped?
3. Is the sitez production path (Alyssa's daily run on the Opal Bloomberg box) clean?

## 2. The 0730 wrong-instrument finding

**ARTIFACT (local pkls, cma-env load, denominators printed):** in `data 20260730 v1.pkl`,
`return_daily` rows for `bbg_ticker == '.ST Index'` number **1449**, spanning **2021-01-04 ->
2026-07-30**, price level ~1.83-2.09, daily-return std 1.48pct (max daily +13.37pct). In the 0727
and 0731 vintages the same ticker has **672/676 rows from 2023-12-29** (custom-index inception,
base 100), price ~112.5, std 0.13pct — and those two vintages agree digit-for-digit on all 669+
shared dates. `.ST_BMK Index` is CLEAN in all three vintages including 0730 (672 shared dates,
max diff 0.0) — which is exactly why benchmark columns looked right on the portal while the model
column was garbage.

**ARTIFACT -> SERVED linkage:** the rogue series' 07-30 daily return is **+2.216187**, and the
13:12:19Z build published ST MODEL 1D = **+2.22** (S3 version `JTV0rndkN387Qf5UhKe3zAMu1p0V08Ak`).
Vol scale matches (daily 1.4757 * sqrt(252) ~ 23.4 vs published 20.79-27.79 across periods). The
Lambda faithfully built garbage from a garbage input; execution success said nothing about content.

**SOURCE (notebook, `src/market_indices_data_pull.ipynb`, OneDrive live copy):** the `return_daily`
request window is `start = date_end + YearEnd(-6)` = **2020-12-31** (cell 16). The rogue series'
span IS the request window; the legit custom index simply has no data before 2023-12-29. Same code,
same window, both runs — the DIFFERENCE was what Bloomberg resolved `.ST Index` to at request time.

**Mechanism class (two candidates, one discriminating test open):**
- **(a) Per-login CIX resolution** — custom Bloomberg indices are user-scoped; `.ST` on the
  Friday-pull login resolved to a different definition. Supported by: the sitez login returning the
  correct 676-row series for the identical window (LIVE probe, 15:31Z); Yang's own history of
  hand-patching the ST series in the notebook (commented May + June patch blocks fabricating
  'Short Term' rows from 'Ultra Short Term' + hand-keyed returns, price rebased 112.52 — SOURCE).
- **(b) Transient redefinition** — `.ST` was broken/redefined Friday evening and fixed by Monday
  on the same login.
- **Discriminating test (OPEN, needs Yang):** the same `.ST Index` PX_LAST pull, window
  2020-12-31 -> now, from YANG'S login. 1449-ish rows -> (a); 676 rows -> (b).

**Attribution boundary (INFERRED, stated deliberately):** the Friday 17:05 pull is ATTRIBUTED to
Yang's machine but NOT proven — the `c:\Users\YangLiu\...` kernel path in the notebook's stored
outputs belongs to TODAY'S 09:08 interactive session (monotonic exec counts 14-24, one kernel),
not Friday's run; and this box's own `blppersist2.db` shows terminal activity Friday 17:15 local.
Do not treat the machine attribution as settled; the mechanism finding does not depend on it.

## 3. The Bloomberg -4003 block — login-scoped, with basis

**SOURCE (stored notebook outputs, saved 13:08Z today):** the re-pull attempt in the YangLiu-kernel
session died with `responseError: code -4003, category LIMIT, subcategory REVIEW, "Access pending
review. [nid:52865]"` on the `return_daily` request (84 tickers x 5.5y daily x 2 fields).

**LIVE (this box, same day):** three request scales all SUCCEEDED from the sitez login:
- probe: `.ST`/`.ST_BMK` full-window daily (15:31Z);
- medium: `AAPL US Equity` PX_LAST 2024-08-03 -> 2026-08-03, ~500 rows incl. today's intraday
  (15:50Z — Yang's exact BDH diagnostic, API path);
- **full production scale: Alyssa's 08:03 local run of the identical 84-ticker request completed
  and produced the 0731 pkl** (ARTIFACT: the pkl exists with fresh data through 07-31).

**Conclusion:** the block is **login-scoped** (Yang's), not firm-wide, not code-related, and not
request-size-dependent on the sitez login. Whether it is size-triggered ON YANG'S login is unknown
(one observation). **Excel-path caveat:** Yang's Excel BDH test is UNTESTABLE-HEADLESS from an
agent session — `bxlafct.exe` (the process that services BDH) does not spawn under COM automation;
the formula resolves and sits at `#N/A Requesting Data...` indefinitely. That is an automation
artifact, not a deny. A human at this desk can settle the Excel channel in 30 seconds.

**Escalation path:** Yang raises `nid:52865` with the Bloomberg rep against his UUID. The sitez
seat's UUID artifacts on this box are 32265165 (recent) / 33343590 (older) — UUID->name not
resolvable from the API side.

## 4. The sitez production path — clean, evidenced

- The daily production pull runs on this box (Alyssa, `run_daily_pull.bat` -> cma env) and its
  08:03 output was verified: `.ST` return_daily digit-identical to the verified 0727 vintage on all
  shared dates + plausible 07-28..07-31 tail matching the live terminal (07-31 close 112.503).
- Its ONLY defect was the month-end double-append (W4 proper): SOURCE-confirmed at notebook cell 16
  — the one-day DAILY snapshot appended to MONTHLY frames collides with the month-end row.
  Census: price_monthly 60 dup rows of 30,250 (value-identical); return_monthly 168 of 29,079
  (NOT value-identical — the appended daily row is NaN in valuation fields and carries a 1-DAY
  return; a naive `.last()` dedup destroys data). Yang's own guard (`... and end_date !=
  df['date'].max()`) landed in the live notebook 13:08Z and prevents recurrence at source.
- The corrected artifact promoted under W4 was derived from the byte-verified S3 upload of that
  08:03 run (source md5 == S3 ETag `961a1f5a...`; output ETag/md5 `2a470346...`; scripts committed
  at `deliverables/MDLP_MONPUB_W4/` @ 12a17b857; interval content gate PASS with a
  methodology-control run that reproduced the served 07-27 row to 2dp first).

## 5. Standing hazards this trace leaves on the record

1. **A wrong-instrument pkl is dup-free and builds successfully** — it passes every guard in the
   current fix order (W2 monotonic guard included: `data_as_of` advances). The W4 acceptance now
   carries the ST content gate (inception 2023-12-29, ~676 rows, price ~112.5) — that gate, or a
   diff-vs-prior-vintage check, should ride EVERY future pkl promote, not only this incident's.
2. **Custom (CIX) tickers are resolution-fragile** — any pipeline requesting `.X`-style custom
   indices inherits per-login/redefinition risk invisible to code review. The notebook's manual
   patch history shows this has been absorbed by hand, silently, at least twice before.
3. **kill-agent.ps1:155 hardcodes the laptop path** and fails its KILL audit write on site Z
   (observed live today; line appended manually). Device-portability class, same family as the
   watcher-skill hardcoded `/c/` prefix. Owner: whoever next touches `.tools` population scripts.

## 6. Open items

| Item | Owner | State |
|---|---|---|
| `.ST` pull from Yang's login (discriminates per-login vs transient) | Yang (+ Andrew) | OPEN |
| `nid:52865` review with Bloomberg rep | Yang | OPEN |
| Identify the rogue instrument behind the 1449-row series (bonus, not load-bearing) | any | OPTIONAL |
| Interactive Excel BDH on this desk (closes the Excel-channel cell of the matrix) | human at sitez desk | OPTIONAL |
| Post-publish serve verify vs the pinned interval table (bus msg b5655d76) | CVO/CTO witness + my independent check | PENDING publish confirm |
