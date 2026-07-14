# TASK ORDER — ADVI_SCHWABAUTO (finish-the-box, fetch-by-date self-heal)

<issued_to>0.6.2_AE_PartnerETL</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete</status>
<date>2026-07-02</date>
<priority>HIGH — Andrew ruled Option A (automate the Schwab ingest); closes the 4th-stall class (manual /49-schwab-conv silent-stall) + WS-3 MDPF-custody manual-single-point</priority>

> **CLOSED SATISFIED-BY-C3 (acceptance flex, TO_COMPILER_GATE Rule 7: COO pre-flag 173219Z -> CTO NO
> REDLINE 173520Z). The flex triple on the record:**
> - **ORIGINAL expect:** contention-immune daily CRS on the SI2 box -> N=5 clean-day accrual -> prod
>   repoint retiring the manual /49-schwab-conv OneDrive stopgap.
> - **SUBSTITUTED observation:** the box-automation OBJECTIVE is satisfied by a different,
>   Andrew-ordered mechanism -- the A-PRIME REST mechanism this TO pivoted to BECAME the C3 daily REST
>   pattern: live BOTH masters, first scheduled fires landed-verified (0833 7/7 @ 09:45Z, 0824 8/8 @
>   10:15Z manifest 101519Z failed 0), C3(c) scheduled-path acceptance CLOSED both masters.
> - **REASONING:** the TO's objective was the mechanism-class (durable automated daily Schwab CRS),
>   not the specific box; C3 IS that mechanism, landed and verified. The remaining PROD-REPOINT tail
>   (repointing the OLD opal-data-schwab flow) crosses the new-territory rule (monolith built
>   ALONGSIDE, no modifying existing flows) and rides the when-does-mdpf-feeding-gold-move question
>   -- **explicitly RE-SCOPED/PARKED under OPAL_RUNNERS scoping (with CTO).** The manual
>   /49-schwab-conv stopgap therefore remains legal until OPAL_RUNNERS retires it deliberately.
> Lineage: 0.6.2 hygiene surface 173100Z -> COO flex pre-flag 173219Z -> CTO no-redline 173520Z.

## Objective

Make the `canonical-schwab-si2` box (`i-0f3d57a97f14727af`) daily download CONTENTION-IMMUNE, so it
produces a COMPLETE daily CRS set (incl the MDPF-critical RPS) regardless of the manual desktop SI2
client — enabling N=5 clean-day accrual → the held validation→prod repoint → the box becomes prod's
automated Schwab-raw source, retiring the manual OneDrive `/49-schwab-conv` stopgap.

**Root cause (exercise-confirmed 2026-07-02, Rule 22a):** the box + Andrew's manual desktop are 2 SI2
clients on the SAME 08242234 enrollment that STARVE each other via shared "download all new files"
state (whichever downloads a date first consumes its new-flag; the other misses it). Evidence: RPS
complementary split 0-overlap/5 dates; within-06-30 the manual took EXACTLY RPS + the box EXACTLY the
other 12; box CAN download RPS on non-contended dates; manual 13:39 fetch preceded the box's 20:37 miss.

**Mechanism (CTO-finalized 20260702T201456Z):** daily "download all new" (bulk) + an EXPECTED-SET-DRIVEN
"download specific" (search-by-date) SELF-HEAL pass → contention-IMMUNE. Decouples box correctness from
Andrew quiescing (quiesce = eventual cleanup, NOT a correctness prerequisite). Design: `docs/briefs/
schwab-ingest-automation-ws3-prescope-20260702.md` (commits f925d3033, 83ff0ea67).

> **MECHANISM PIVOT — 2026-07-02 (ANDREW-RATIFIED): the fetch-by-date-via-GUI mechanism above is SUPERSEDED
> by A-PRIME (fetch-via-REST).** Rule-22a EXERCISE of the GUI-driver FAILED: the SI2 app is UIAutomation-
> OPAQUE for data entry (only top-level named buttons scriptable, not the date/type/master wizard fields;
> coordinate-clicking = too fragile for prod). Non-GUI spike then found the SI2 REST backend
> (`REST_SI2Desktop = https://si2.schwabinstitutional.com/fileservices/SDDServices/`; auth = OAuth via the
> Schwab **LMS SSO gateway** `sws-gateway.schwab.com`, `LMS_ClientId=SDD`, + Windows Credential Manager).
> **A-PRIME MECHANISM (Andrew-directed):** RIDE the box's STANDING authenticated SI2 session → call
> SDDServices REST directly (list + download by date/type/master), no re-login/MFA/OTP/GUI. Same live-
> session-REST pattern as 0.6.0's bd `.bd.identity` fix + 0.7.0's OAuth-gateway technique (reuse, firm-sep
> binding: technique shared, auth NEVER). This SUPERSEDES both the GUI-driver (unviable) AND Option-B
> sole-client (moots Andrew's manual-pull cessation — no sovereign gate). LEG 0/1 GUI-driver legs below
> are RETIRED; the LEG-1 build is now the REST-ingest. **BINDING GUARDRAILS:** (a) firm-sep — reuse the bd
> technique, never bd creds/session/data; (b) SESSION-LIVENESS fail-LOUD alarm built INTO it (WS-4-class —
> the standing-auth is a single-point-of-freshness); (c) CTO arch-gate BEFORE any live REST call; (d) prod
> repoint stays Caution-B N=5-gated. RAVC MSTR + CTO. The IAM code-deploy path + console-session + daily-
> bridge prereqs still stand. New design section to be authored on 0.6.0/0.7.0 pattern input.

## Authorization + context

- **Andrew ruled OPTION A** (automate — "that's the entire point of the box"), COO GO 20260702T194245Z.
- **CTO arch-FINALIZED** the fetch-by-date self-heal mechanism (20260702T201456Z), 4 build gates below.
- SI2 date-pull CAPABILITY GROUNDED (UI-source, box PID 7044): "Download specific files" + a
  "Download Specific Files — Search Results" pane EXISTS, distinct from "Download all new files".
- 0.5.0 (WS-3 MDPF-custody-durable) consumer contract CONFIRMED: RPS within 2 trading days; the
  upstream per-date alarm + their downstream leg-2/Stage-2.5 gate layer cleanly.
- The sync-race that missed same-cycle files is ALREADY fixed (schedule.tf v1.1.0, 0.6.2 2026-07-02).

## Scope (legs — build design-ready; EXECUTION gates at the bottom)

**LEG 0 — RULE-22a EXERCISE-CONFIRM (the build gate; the TO does NOT rely on the self-heal until this passes).**
Controlled "Download specific files" run for a KNOWN PAST-DATE's already-consumed RPS (e.g. a date the
manual client took) → PROVE search-by-date RE-DOWNLOADS regardless of the new-flag. Run in a CONTROLLED
window (AFTER a scheduled 8,20 UTC cycle, before the next — never mid-cycle; the app must return to the
dashboard/"Download all new files" view for click-download.ps1). Capture the search UI flow (fields:
date/account/file-type) to drive LEG 1 automation. RAVC CTO the result → CTO arch-signs the reliance.

**LEG 0 grounded prerequisites (2026-07-02 exercise-confirm attempt surfaced two hard infra gaps — both block LEG 1):**
- **PREREQ-A (code-deploy path):** the box role `quartz-si2-spike-role` grants ONLY `s3:ListBucket`
  (opal-data-schwab) + `s3:PutObject` (01_raw/*, 01_raw_quartz_validation/*) — **NO `s3:GetObject`**. The
  box CANNOT pull code from S3 (why the existing scripts are hand-placed). LEG 1 (deploying the self-heal
  script) + LEG 0 (the exercise) both REQUIRE granting the role `s3:GetObject` on a scoped code prefix
  (TF/IAM change, CTO arch/sec-gate). Until then there is NO sanctioned S3→box deploy on this box.
- **PREREQ-B (console-session):** session-0 SSM UIAutomation CANNOT see the SI2 GUI (session isolation);
  the automation MUST run as a scheduled task in the Administrator console session (proven: cloning
  `SchwabAutoDownload`'s principal into a temp task runs in the console session). LEG 1's self-heal runs
  this way, not via direct session-0 SSM.

**LEG 1 — EXPECTED-SET-DRIVEN self-heal pass** (CTO gate 1). The box asserts the EXPECTED file/date set
for the run (RPS for the expected trading date + the CORE 12 types), and self-heals ANY missing member
via "download specific" (search-by-date) — "download all that SHOULD be here," not "whatever's new".
RPS is the priority member. Extends the EventBridge cycle (schedule.tf SSM orchestration) AFTER the
existing "download all new" + quiesce-wait, BEFORE the sync. UI-automation mirrors click-download.ps1
(UIAutomation on the "Download specific files" pane).

**LEG 2 — COMPLETENESS ALARM (CTO gate 3, load-bearing backstop).** After the self-heal, verify the
expected CORE set (incl RPS) is present; a still-missing member fires LOUD. Distinguishes contention-
missing (self-heal fixed → no alarm) from VENDOR-ABSENT (self-heal CAN'T fix → genuine vendor non-
publish → alarm + daily-bridge covers that day + escalate). Calendar-aware (weekends/holidays skip),
threshold tied to the WS-3 2-TRADING-DAY SLA (fire before MDPF DEFERs).

**LEG 3 — TEMPORARY DAILY BRIDGE through the N=5 accrual (prod-continuity; CTO gate 4, 3 reqs).**
Automated validation→prod promote+convert daily (the 2026-07-02 one-off bridge, automated + time-boxed)
so prod stays fed WHILE the box proves out. (a) PER-PROMOTE PARITY VERIFY: each promote confirms box
validation == manual-path-equivalent BEFORE landing in prod (never-widen-safe DELTA=0 source-swap).
(b) TIME-BOXED AUTO-RETIRE at repoint. (c) FAIL-LOUD on a bridge-MISS.

**LEG 4 — N=5 CLEAN-DAY ACCRUAL.** "Clean day" = full CORE set incl RPS, byte-parity-consistent, from
the contention-immune box. Accrue 5 consecutive clean trading days; the LEG-2 alarm is the tracker (a
miss resets). RAVC the N=5 proof to CTO+COO.

**LEG 5 — REPOINT (HELD).** Repoint `sync-to-s3.ps1` validation→prod `01_raw/` (+RPS→`bronze/rps/`).
**EXECUTION-GATED on ALL of:** N=5 accrual proof + CTO+COO never-widen 3-way sign-off (verified DELTA=0
source-swap; CTO is one signer) + Andrew Caution-B pace (MSTR carrying). Then retire the daily bridge;
retire the manual OneDrive pull (eventual cleanup — Andrew's convenience, not correctness-blocking).

**LEG 6 — CONVERTER + CANONICAL automation** (brief sec 2B/2C). Event-driven off the prod raw landing:
the 6 converters + `build_canonical_daily` headless. **PREREQUISITE: C3 (TRN-A→S3, DS~A, CTO-approved)**
— `convert_schwab_trn_to_parquet.py` must read S3 `01_raw/`, not local OneDrive, or it no-ops headless.

## Firm-separation (NEVER#1)
schwab-only, 08242234-scoped throughout. `opal-data-schwab` + `opal-data-bd/schwab/*`. No cot/bd-other
bucket. The repoint moves the raw SOURCE, same data + same scope (never-widen).

## Execution gates (design is ready NOW; execution waits on these)
1. LEG-0 exercise-confirm PASS (Rule 22a — self-heal reliance).
2. Andrew Caution-B pace answer (MSTR carrying) — governs WHEN N=5 accrual + repoint proceed.
3. CTO+COO never-widen 3-way sign-off on the repoint (LEG 5).
4. C3 (TRN-A→S3) for LEG 6.

## RAVC
CTO (arch-signs LEG-0 result + the build) + COO (owner) + 0.5.0 (WS-3 consumer SLA). Ledger a
deploy-completion entry per landing leg (never-half-deploy).
