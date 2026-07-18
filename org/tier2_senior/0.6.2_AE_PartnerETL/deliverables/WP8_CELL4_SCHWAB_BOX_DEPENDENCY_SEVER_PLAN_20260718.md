# WP8 CELL-4 — Schwab Box opal-data-schwab dependency-sever plan (before the BUCKET delete)

**Author:** 0.6.2_AE_PartnerETL | **Date:** 2026-07-18 ~01:0xZ | **For:** CTO (apply gate) + 0.5.0 (WP8 lead, bucket census). CC COO.
**Scope reminder (Andrew-direct):** WP8-DECOM deletes the **`opal-data-schwab` S3 BUCKET only**. The EC2 **Schwab Box** (`i-0f3d57a97f14727af`) is ESSENTIAL infra and STAYS. CELL-4 = sever the box's remaining RUNTIME ties to the dying bucket so the delete can't break the live puller — NOT a box action. Grounded on live IAM + live S3 + on-box SSM.

---

## 0. Headline

**The Schwab Box has NO actively-exercised WRITE to opal-data-schwab left** — its data now goes to the monolith (`-Target monolith`), its code is re-homed (cell-3). What remains is **vestigial grants + one live-firing-but-NO-OP GUI sync**. The `01_raw/` writer Andrew asked about is **NOT the Schwab Box** — it is a separate OneDrive sync (off-box). And there is a **live `01_raw/` READER (`canonical-schwab-runner`) that the bucket-delete would break** unless repointed first — the load-bearing new finding.

---

## 1. The 01_raw writer — GROUNDED (it is not the Schwab Box)

- **WRITER = `data/black_diamond/scripts/bronze/sync_schwab_onedrive_to_s3.py`** (`:12` "syncs to `s3://opal-data-schwab/01_raw/`, uploads any missing files"). Runs in a **OneDrive-attached context (off the SDD box)** — the SDD box has NO 01_raw writer (on-box SSM grep found only `01_raw_quartz_validation/` in `sync-to-s3.ps1`, plus a no-op comment in the puller). This IS 0.5.0's census row-2 writer ("retires outright in L5b"). The 07-16 writes (CRS20260709-15, 01:38 + 10:00Z) are this sync's; last write **2026-07-16, nothing since** (deprecating, per Andrew).
- Setup/one-shot scripts (`data/schwab/aws/{upload-data,setup-bucket,deploy}.sh`) also target 01_raw/ but are manual, not live.

## 2. The 01_raw READER — the bucket-delete risk (NEW, surface to 0.5.0/CTO)

- **`canonical-schwab-runner`** (a SEPARATE EC2, not the SDD box): `run-canonical.sh:8,22,59` `RAW_PREFIX=01_raw/` — reads `opal-data-schwab/01_raw/` as its canonical-build **INPUT** ("production 01_raw/… feeds CVO parity; parallel/NOT-served"), and `s8_gate.py --prefix 01_raw/` gates on it. **This is a LIVE consumer** — the bucket delete breaks it unless it is first repointed to the monolith copy of 01_raw (`opal-data-assets/schwab/08242234/bronze/…`, per 0.5.0's census-3 copy). 0.5.0's 01_raw census row covers the COPY + retain-read-only, but does NOT name canonical-schwab-runner as the reader-to-repoint — **flagging it so the sever-before-delete is complete.**

---

## 3. The Schwab Box (i-0f3d57a97f14727af) opal-data-schwab footprint (my CELL-4) — grounded

| # | Dependency | Grant (role `quartz-si2-spike-role`) | Live at runtime? | Sever |
|---|---|---|---|---|
| 1 | Code-pull `_ops/canonical-schwab-si2/*` (GetObject) | `SchwabOpsCodeRead` | **RE-HOMED (cell-3)** -> monolith `code/` | remove grant + delete old objects (D5) |
| 2 | GUI sync -> `01_raw_quartz_validation/*` (write) via task `SchwabS3Sync` (`sync-to-s3.ps1`) | `SchwabRawWrite` | **FIRING but NO-OP** — GUI delivery folder frozen 07-02; last write 07-10 | retire the dead GUI channel (below) + remove grant |
| 3 | `01_raw/*` (write) | `SchwabRawWrite` (same stmt as #2) | **UNUSED by the box** (writer is off-box, sec.1) | remove (drop 01_raw/* from the stmt) |
| 4 | Staging `08242234/bronze/*` + `08335338/bronze/*` (write) | `SchwabBronzeWrite` | **VESTIGIAL** — `-Target staging` escape-hatch; daily pull is `-Target monolith`; staging frozen 07-13 | remove grant; drop/inert the `-Target staging` path |
| 5 | `backfill/08335338/*` (write) | `SchwabBackfillWrite` | **VESTIGIAL** — backfill done 07-13 | remove grant |
| 6 | `opal-data-schwab` ListBucket x3 | `SchwabRawList` / `SchwabBronzeList` / `SchwabBackfillList` | serve #2-#5 | remove with them |

**The only ACTIVELY-FIRING opal-data-schwab path on the box is #2** (SchwabS3Sync, twice-daily via the `canonical-schwab-si2-download-schedule` rule) — and it lands NOTHING (frozen GUI). Everything else is a grant with no exercising code path.

---

## 4. Sever sequence (Schwab Box) — gated (CTO apply + 0.5.0 sequencing; box keeps running throughout)

1. **Retire the dead GUI channel** (the only firing write path): the `canonical-schwab-si2-download-schedule` EventBridge rule + the box tasks `SchwabAutoDownload` (click-download.ps1) + `SchwabS3Sync` (sync-to-s3.ps1). Coordinate with **0.7.0** (owns the rule + its L7-schwab alarm teardown) + **0.5.0**. This is the REST-vs-UI split already established — retiring the dead UI channel does NOT touch the live `-daily-pull` REST rules (0.5.0 confirmed separable).
2. **Strip the box role's opal-data-schwab write grants** in `iam.tf` (`SchwabRawWrite`, `SchwabBronzeWrite`, `SchwabBackfillWrite` + the 3 ListBucket) — one iam.tf change; plan must show ONLY removals, zero other change; CTO gate. Keep `SchwabOpsCodeRead` until its own D5 step.
3. **Remove the old `SchwabOpsCodeRead`** code grant + delete the old `_ops/canonical-schwab-si2/` objects (the existing D5 cleanup, task #6).
4. **Optionally** strip the `-Target staging` branch from `sdd-daily-pull.ps1` (or leave it inert — once the grant is gone it would fail-loud if ever invoked, which is acceptable).
5. **Verify (Rule 22a):** `simulate-principal-policy` shows the box role has ZERO opal-data-schwab access on every prefix (allowed only on the monolith code + its monolith-write). Exercise a supervised `-Target monolith` daily pull post-sever to confirm the box is unaffected.
6. **THEN the bucket is Schwab-Box-clean.** The remaining bucket-delete prerequisites (sec.1-2 writer/reader, 0.5.0's other census rows) are 0.5.0's to close.

---

## 5. Asks

- **[0.5.0]** confirm sec.1 writer (`sync_schwab_onedrive_to_s3.py`) is your L5b retirement, and **add sec.2 reader (`canonical-schwab-runner` reads `01_raw/`) to the bucket-delete repoint list** — it must read the monolith copy before delete.
- **[0.7.0]** the dead GUI channel retirement (download-schedule rule + SchwabAutoDownload/SchwabS3Sync) — coordinate; box + its `-daily-pull` REST rules are off-limits.
- **[CTO]** gate the iam.tf grant-strip (sec.4 step 2) + confirm CELL-4 = this dependency-sever (box stays).
- Execution HELD to CTO apply + 0.5.0 sequencing. This doc is the grounded plan; nothing executed.
