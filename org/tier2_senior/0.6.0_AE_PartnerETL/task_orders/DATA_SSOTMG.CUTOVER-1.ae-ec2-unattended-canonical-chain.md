# TASK ORDER — DATA_SSOTMG.CUTOVER-1

<issued_to>0.6.0_AE_PartnerETL</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project DATA_SSOTMG, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
<priority>HIGH — Andrew-direct GO (2026-06-29): stand up the unattended canonical ETL chain on the new direct-Schwab EC2. The whole pipeline (G1-G14 closed + dry-run verified) holds only on these automation seams.</priority>
<date>2026-06-29</date>

## Context

Andrew set up the direct-Schwab EC2 **i-0f3d57a97f14727af** (Win Server 2022, SI2-Desktop + UI-automation;
DERISK-1 Quartz spike COMPLETE per 0.6.2 — 720MB June raw S3-verified, the 3-task unattended pull built:
SchwabAutoDownload 12/16/20Z + SchwabS3Sync 30min + SchwabKeepConsole). The raw→silver→gold machine is
DONE + dry-run-verified (build_canonical_daily.py rolls the full G1-G14, 25/25 steps; S2/S3/S5 closed).
What's NOT wired is the automation glue that makes it run unattended end-to-end. This TO wires it. The
seam map: `org/seams/canonical-schwab-ssot-ec2.md` (base-DS, bca255b38). Coordinate 0.6.2 (built the
Quartz box) on handoff + base-DS (owns build_canonical_daily.py + the S+ staged code) on the trigger.

**Buckets:** raw = `s3://opal-data-schwab/01_raw/` (orchestrator SRC_BUCKET, Prefix `01_raw/`, CRS-files);
silver+gold = `s3://opal-data-bd/canonical/schwab/{silver,gold}/` (DST_BUCKET, AES256, parallel/NOT-served).
Quartz currently lands in the **segregated** `01_raw_quartz_validation/` — promoting that to production
`01_raw/` is part of S1.

## Objective

Wire the unattended canonical chain on i-0f3d: Schwab raw lands → silver+gold rolls automatically → daily,
hands-off — running in PARALLEL (NOT-served) so the parity window (S7, CVO) can prove it before any
serving cutover. This TO delivers the running parallel chain; it does NOT flip serving from BD.

## Scope — 4 dependency-ordered seams (do in this order)

**S6 — EC2 instance-role IAM (FIRST; gates every run).**
- The i-0f3d instance-role needs: read `opal-data-schwab/01_raw/*`; read+write `opal-data-bd/canonical/schwab/*` (Put with SSE-AES256); + the trigger's invoke perms (S4). It currently has only the Quartz S3-sync grant.
- `comp-iam service` on the role + `comp-iam gaps` BEFORE the first canonical run; ALSO ground-truth on live `aws iam get-role-policy` for the fresh grant (NOT the comp-iam DESIRED verdict — a fresh change isn't in the census). Terraform via safe-apply (never console).

**S1 — ingestion promote (validation → production).**
- Promote the proven Quartz pull from `01_raw_quartz_validation/` → production `01_raw/` (the prefix the orchestrator reads; CRS-file naming already matches the orchestrator's date parse). Cleanest = repoint SchwabS3Sync's destination to `01_raw/`. Confirm the production daily-AM schedule lands the day's raw before the orchestrator fires (S8).
- Coordinate 0.6.2 (built + owns the Quartz box config) on the handoff — do NOT duplicate-build; promote what's proven.

**S4 — scheduled trigger (the #1 finding — without it the canonical layer never advances unattended).**
- Wire: raw-lands → trigger → `build_canonical_daily.py --upload`. ARCH-GROUND with CTO before building: the orchestrator is a Python data-pipeline (PEP-604/py3.9-runner-oriented per rule 15) — it should run on a **Linux compute** (SSM on a Linux runner / Lambda / Fargate pulling the S+ staged code), **NOT** on the Windows SI2 box. Recommend EventBridge (S3-event on the last `01_raw/` object OR a daily-AM cron after the pull window) → SSM RunCommand on a Linux runner → pull S+ code → `build_canonical_daily.py --upload`. CTO arch-gates the compute-home choice.

**S8 — ordering (no partial partition).**
- The orchestrator must fire only AFTER the day's raw FULLY lands (all CRS files for the date), else a partial partition. Use a sentinel (last-expected-file lands / a manifest count) or a sequenced cron with margin. Co-design with base-DS (knows the raw file-set per date + the orchestrator's date-picking logic).

## Parallel track (NOT this TO — coordinate)
**S7 — parity window (CVO).** Daily `comp-parity` canonical-vs-BD-served over the positioned $1.591B book, accumulate N clean days → the cutover gate. CVO owns + is building the comp-parity DATA-harness. Your chain FEEDS it (it reads the canonical gold this chain produces). Coordinate cadence with CVO once the chain runs.

<compiler_tools_mandate>
- comp-iam service / gaps on the i-0f3d role (S6) + live get-role-policy ground-truth on the fresh grant.
- comp-pipescript deployed on build_canonical_daily.py (S+ staged code is current at the pull location) before the first triggered run.
- Verify against the SERVED artifact (NEVER#7): a triggered run must produce a real canonical gold partition in S3, not a box-side "it ran".
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.6.2_AE_PartnerETL: owns the Quartz box config — handoff on S1 (promote, don't rebuild).
- 0.4.0_DS_ClientPlatform (base-DS): owns build_canonical_daily.py + the S+ staged code + the date-picking logic — co-design S4/S8.
- 1.0.0_SA_CTO: arch-gates S4 (orchestrator compute-home) + the cutover (PRD owner; NEVER-WIDEN — this runs PARALLEL/NOT-served, no serving flip in this TO).
- 3.0.0_SA_CVO: S7 parity window (separate track; your chain feeds it).
</cross_domain_coordination>

<acceptance_criteria>
1. S6: i-0f3d role grants verified (comp-iam gaps clean + live get-role-policy shows read 01_raw + read/write canonical/schwab SSE); Terraform-applied via safe-apply, 0-diff.
2. S1: Schwab raw lands in production `01_raw/` on the daily schedule (S3-verified object, the orchestrator's date-parse picks it up).
3. S4: a scheduled trigger fires build_canonical_daily.py --upload on the arch-gated compute AFTER raw lands; CTO arch-gate on the compute-home cited.
4. S8: ordering proven — the orchestrator fires only on a COMPLETE raw partition (no partial-partition run); sentinel/sequencing evidenced.
5. END-TO-END: ONE fully unattended cycle runs — raw lands → silver+gold G1-G14 partition materializes in canonical/schwab/gold (S3-verified, parallel/NOT-served), zero manual steps. RAVC me + CC CTO + Andrew with the verified end-to-end run + the S3 gold partition.
</acceptance_criteria>

## Note
PARALLEL / NOT-served — this TO stands up the unattended chain; it does NOT flip serving from BD to canonical.
The serving cutover (P4) is GATED on S7's N-clean-days parity + a never-widen CTO+COO sign-off, a separate
Andrew-gated step. Build the machine; the parity window proves it; the flip is later.
