# Release packet -- IRPT_BCKEND r61 directory release (irpt-directory-refresh + irpt-directory-search), never-widen

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-07 ~09:5xZ | **Halves:** COO (this seat) + CTO (`1.0.0_SA_CTO~DELL2`)
**Status: DRAFT -- asks the CTO half. Nothing is built for upload, uploaded or applied by this file.**
**Source:** CLOUD b9411881a0 (round 61 drained: IB-pr-333 and IB-pr-334 @f2fa74df85).

## 1. The whole delta per function

The census is `python infra/aws/lambda/ci/release-census.py <fn> --pin b9411881a0`: a by-blob build diffed against the live zip.

| function | live CodeSha256 | changed members | from |
|---|---|---|---|
| irpt-directory-search | `cmNmYm1j..` (S3 version S5vL.tP9..) | `entry.py` changed; `expiry.py`, `trading_calendar.py` added (3) | IB-pr-334 |
| irpt-directory-refresh | `DXuzx9jp..` (S3 version M8O8zFha..) | `refresh.py` changed (IB-pr-333); `handler.py` changed (**RIDER**, row S357: UIR-07 49b935c213 + 1068a4b5a5, 2026-09-26, recorded as deployed at daed4433b4 but not in the running bytes) (2) | IB-pr-333 + rider |

## 2. Served behaviour that moves

1. **Search, over-age directory.** A search against a directory whose `as_of_business_date` is more than `MAX_AGE_TRADING_DAYS` (2)
   trading days old, or whose age cannot be computed, answers `{"_data": <stale hits>, "_status": <expiry envelope>}`, with
   `DIRECTORY_OVER_AGE` / `STALE`, or `CALENDAR_UNAVAILABLE` / `UNCERTAIN`. Today it answers the plain hit list silently.
   **An in-age search answers exactly as today** (the plain list).
2. **Refresh manifest.** The day's `_refresh/<date>/manifest.json` is keyed by the business date the fire was dispatched for. A
   completed dispatch rewrites that day's RUNNING / REFRESH_DISPATCHED record to READY with the revision filled. That is a second
   PutObject under `_refresh/*`, which the role already grants. `latest.json` and the directory objects are untouched by this change.
3. **Rider (refresh only).** Whatever UIR-07's handler change does on the refresh function's path, it is not exercised by any round-61
   criterion. The CTO half either admits it with its own after-read, or the release pins `handler.py` back to 48313e9c0e (the
   running blob) and ships only `refresh.py`.

## 3. Preconditions (each read before the build)

- **P1 consumer read (row W136-S1).** Every portal and backend reader of the directory-search response handles the `{_data, _status}`
  shape on an over-age day, or the release is held. The portal's directory readers live under
  `portal/src/pages/InvestorReporting/` (`contracts/directory-browse.ts`, `contracts/wire/DirectoryEntry.ts`, and others). Today's live
  directories are in-age (latest.json 10-05/10-06), so no request reads the new branch until a directory ages out. The census is still
  owed before the build.
- **P2 rider ruling** (section 2.3).
- **P3 the HOLD** (laptop CTO ruling A): no date before 2024 is involved. The search and refresh dates are 2026.

## 4. Acts, in order, under a ledger opened first

1. Build both with `build-and-upload.sh` (the builder now uses the map's `artifact_s3_key`, IB-pr-329), so no copy-object step is needed.
2. Targeted `safe-apply` of the directory root: refresh first, then search. Read back CodeSha256 = the built sha; re-plan reads 0.
3. **Real runs:**
   - (a) one driven refresh fire for today's business date reads READY in `_refresh/<today>/manifest.json` at all three firms
     (E-P5 criterion 3);
   - (b) the five-arm controlled-clock drive (`deliverables/0.9.0_WK_IRPT_BCKEND~2/ib_s_4_controlled_clock.py`) against the deployed
     modules (E-P6 criterion 2);
   - (c) an over-age search answers the declared expiry (E-P6 criterion 3).

   The firm buckets deny the dell2 identity (S347; NFRA_CTLPLN round 4). Each read of `opal-data-*` goes to the laptop as a FILE under
   the standing rule (msg 215).
4. Record the deploy with the recorder (IB-pr-330's fix exercised) and correct the refresh record (S357).

## 5. Rollback (per function)

- **irpt-directory-search:** S3 version `S5vL.tP9KPBcoAnJVlD2z6mBLX5Ai6CR` (CodeSha `cmNmYm1j..`).
- **irpt-directory-refresh:** S3 version `M8O8zFhaS8YGlWPgya0PtiCIXfLSaTmR` (CodeSha `DXuzx9jp..`).

Each is a targeted apply back to its version, the same turn an after-read fails.

**COO half: SIGNED -- 2.0.0_SA_COO~P2, 2026-10-07**, for sections 1-5 as written, conditional on P1 and P2 being read before the build.
