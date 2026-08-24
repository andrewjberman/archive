# TO ETFS_POSITIONING.TO-5 — the ETF producer's **LAMBDA + SCHEDULE** (the infra half of `ETFS-d-1`)

<task_order id="ETFS_POSITIONING.TO-5" project="ETFS_POSITIONING">
<decomp_ref>workflows/atom_decomposition/runs/etfs-positioning/20260821T194927Z/DECOMP.md — cell ETFS-d-1 (producer plane), INFRA HALF. The scripts half is discharged under ETFS_POSITIONING.TO-1.</decomp_ref>
<certification>Decomp **CERTIFIED** by `3.0.0_SA_CVO` @59f2c95115 (§6 refused, rewritten @f7c719b56d, discharged). **Not uncertified-on-face** — cut after certification.</certification>
<issued_to>AE-class (infra / Terraform / triggers). Seated: `0.7.0_AE_CloudOps`.</issued_to>
<executor_class>AE-class</executor_class>
<seating_trigger>SEATED. ⛔ **SEQUENCED BEHIND TO-2's remaining leg** (router branch + `qualified_arn` pin drop + `ETFS-TO2-AC8`). Do not interleave with an in-flight portal-auth apply.</seating_trigger>
<placement>LAPTOP (Rule 26) — the apply runs on the device that owns the work.</placement>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-21T21:00Z</issued>
<status>⛔ **ACTIVE — THE CRITICAL PATH. THE HOLD'S PRECONDITION IS DISCHARGED (22:1xZ): the corrected invocation contract IS IN HAND** (`…/deliverables/ETFS_POSITIONING_TO-1_INVOCATION_CONTRACT_FOR_TO-5.md`, verified at the COO seat — all FOUR parts of CTO~Z's ruling present: env SET NEITHER `:167` · stage-1 PutObject `opal-data-etfs/gold/*` `:175` · stage-1 ListBucket **prefix `gold/` added** `:176` · stage-2 GetObject+ListBucket `opal-data-etfs/gold/*` `:180`). ⚠ The prior status read "queued behind TO-2's remaining leg" — **that was an ETFS_POSITIONING round-1 reference and it is STALE**; it is not what gates this. **NOTHING GATES THIS NOW.**</status>
<priority>P1 — ⛔ **ON THE CRITICAL PATH TO ANDREW'S DONE.** PRD s.11.1: ETF mode renders *"from **SCHEDULED** production artifacts."* **The schedule is IN the definition of done, not an operational follow-up.**</priority>
<authority>PRD s.11.1 + s.11.5 (production = SCHEDULED, ad-hoc = QA only). CLAUDE.md Rule 13 (infra/PROD triggers are the AE/DT lane), Rule 1 (Terraform is the only Lambda deploy mechanism), Rule 4 (source map), Rule 5 (size deliberately), NEVER#4 (`safe-apply`, never bare).</authority>
</task_order>

## ⛔ WHY THIS TO EXISTS — a mis-cut criterion, mine, corrected rather than argued

`ETFS-TO1-AC4` (the schedule) was placed on **DS's** TO. **DS routed the seam instead of assuming it:**
*"the producer scripts are my Rule-13 lane; the Lambda + schedule Terraform is infra (AE/DT). Routing
the seam to COO as issuer, not assuming it."* **They were right; the TO was wrong.**

**It was also MECHANICALLY BLOCKING them:** `proof-of-spec-check.py`'s coverage diff is bidirectional, so
an expected id with no row **refuses the whole instance** — DS could not have closed TO-1 at all while an
infra criterion sat in their expected set. **AC4 is removed from TO-1 and lands here. A REASSIGNMENT, not
a waiver: the schedule remains mandatory and remains on the critical path.**

## WHAT ALREADY EXISTS — do not rebuild it (BUILD LADDER rung 2)

DS's TO-1 landed **both stages, tested, `commit-gate` clean** (`71265d372e`; I re-ran the suite at my own
seat: **23/23 PASS**, mutants firing):

| stage | file | writes |
|---|---|---|
| gold | `data/etfs/scripts/gold/etf_positioning_gold.py` | (a) plane → **GOLD PARQUET** |
| publisher | `data/etfs/scripts/gold/etf_positioning_publisher.py` | gold parquet → **platinum JSON** (`platinum/etfs/positioning_data.json`) |

⛔ **THE SCRIPTS ARE DS'S LANE. DO NOT EDIT THEM.** If you need a change in either, route it to DS —
`data/**` is theirs under Rule 13. **Your lane is the Lambda packaging, the Terraform, and the trigger.**

⛔ **TWO STAGES MEANS THE SCHEDULE HAS A SHAPE DECISION, AND IT IS YOURS TO MAKE WITH EVIDENCE:** one
Lambda running both stages, or two with an ordering edge. **State which and why.** Note the publisher's
`OPAL_ETFS_PUBLISH_GRANT=1` requirement and `_assert_write_boundary()` are DS's **runtime refusals**, not
approval gates — do not "helpfully" remove them to make a deploy simpler.

## ⛔ THIS IS NOW THE ONLY THING BETWEEN A PROVEN CAPTURE AND A RENDERED PAGE (22:1xZ)

**MEASURED AT THE COO SEAT, third independent census after DE~Z (serving end) and AE~Z (rules end):**
`comp-trigger etf-positioning-producer` → **NO MATCH**, denominator **136 events-rules + 18 schedules** ·
`get-function-configuration etf-positioning-producer` → **the function does not exist on the applied plane** ·
`platinum/etfs/positioning_data.json` → **76,149 B, 2026-08-24T12:30:47Z — UNMOVED** (s3api/UTC).

> **BRONZE: exercised. SILVER: exercised, 187 rows, four funds. GOLD: NEVER RUN. PLATINUM: UNMOVED.**
> **THE SERVED SURFACE IS VERIFIED BY NOBODY**, and the schedule that would move it is *this TO*.

⛔ **AND THE HOLD THAT STOPPED IT WAS MINE AND WAS CORRECT.** Applied as originally written, the
contract's ENV error would have silently reverted Andrew's C2 gold home while its IAM error failed
loud — **the two cancelling into a green pipeline where his ruling did not happen** — and
`_assert_write_boundary` is keyed to the CONFIGURED values, so **the runtime guard would have
VALIDATED the reverted target.** I would place that hold again.
**But a correct hold left standing is still a stopped pipeline.** The precondition is discharged;
**the hold is lifted and this is the top item in the round.**

⚠ **This is CLAUDE.md's scheduled-vs-ad-hoc NEVER, verbatim, and the mdpf six-day freeze in
miniature: fresh inputs sitting unused because the only trigger is one nobody applied.**

**Rule 26 binds — whoever built it applies it, on THIS box, under `safe-apply`. No ferry.**
**NEVER#6 — a begun deploy finishes in-session or rolls back loud; open the ledger at start.**

## ⛔ THE LAW THAT DEFINES THIS TO — read it as the spec, not as background

**A PRODUCTION PIPELINE MUST HAVE A SCHEDULE.** (Andrew-direct 2026-07-24.) Verbatim from CLAUDE.md, and
it is the entire reason this criterion is P1:

> ***"A pipeline whose only trigger is another pipeline's success has no schedule and is a defect — it
> freezes silently and invisibly when its upstream breaks."***

**Measured instance the day that was ruled:** `mdpf-daily-refresh-trigger` had `ScheduleExpression: None`,
fired only on an upstream completion marker, and when that upstream died **the client-facing Model
Portfolios product froze for six days with perfectly fresh inputs sitting unused, and no instrument
reported it.**

⛔ **SO: EVENT-DRIVEN IS PERMITTED ONLY AS AN ACCELERATOR ON TOP OF A REAL SCHEDULE.** An event-only
trigger off the L1 BBG landing **is the defect this rule names**, however natural it looks — and it will
look natural, because the producer genuinely wants that data.

## AMENDMENT (2026-08-24 21:4xZ) -- DO NOT APPLY OFF THE CURRENT INVOCATION CONTRACT

**Found and routed by `0.4.0_DS_ClientPlatform~Z` BEFORE the apply; ruled by `1.0.0_SA_CTO~Z` (who ruled C2 and whose ruling this would have silently reverted); premises verified at the COO seat.**

`.../deliverables/ETFS_POSITIONING_TO-1_INVOCATION_CONTRACT_FOR_TO-5.md` was written **before** C2 was ruled. Verified wrong at three lines:

| contract | says | now |
|---|---|---|
| `:153` ENV | `ETFS_GOLD_BUCKET`/`ETFS_GOLD_ROOT` = `opal-data-assets` / `portal/gold/etfs/positioning` | **FAILS SILENT** |
| `:161` IAM stage 1 | `s3:PutObject` on `opal-data-assets/portal/gold/etfs/positioning/*` *"this prefix only"* | **FAILS LOUD** |
| `:165` IAM stage 2 | `s3:GetObject` + `s3:ListBucket` on the same old prefix | **FAILS LOUD** |

**The mechanism:** `os.environ.get(NAME, default)` means **a set env WINS** -- so setting those vars **overrides the re-pointed defaults and sends the producer back to the OLD home**, which is exactly where the stale IAM grants permit.

> **APPLIED TOGETHER THE TWO ERRORS CANCEL: green pipeline, landed artifacts, healthy instruments -- AND ANDREW'S C2 RULING SILENTLY DID NOT HAPPEN.** A **half**-applied contract would have failed visibly; the **fully**-applied one fails invisibly. **Completeness is what hides the defect.**

### WHAT TO APPLY INSTEAD -- CTO~Z's ruling, which ADOPTED DS~Z's sharpening over its own earlier wording

- **ENV: SET NOTHING.** Neither `ETFS_GOLD_BUCKET` nor `ETFS_GOLD_ROOT` appears in this TO's Terraform. **Setting a var to its own default is not neutral -- it re-creates the two-sources-of-truth surface that F2 is this project's first act because of.** *A default that nothing overrides is the only configuration with one source of truth.*
- **IAM:** stage 1 `PutObject` -> **`opal-data-etfs/gold/*`** (**DROP** the `opal-data-assets/portal/gold/etfs/positioning/*` grant) - stage 1 `ListBucket` -> **add prefix `gold/` on `opal-data-etfs`** (the as-of resolution paginates) - stage 2 `GetObject` + `ListBucket` -> **`opal-data-etfs/gold/*`**.
- **`INGEST-INV-4` IS STRENGTHENED:** verify defaults == deployed by verifying the deployed function **carries NO override at all** (`get-function-configuration` -> `Environment.Variables` contains neither key). **Cheaper, stricter, and it cannot pass on a coincidence.**

**HOLD UNTIL DS~Z's CORRECTED CONTRACT IS IN HAND** (their deliverable, their lane, authorized by CTO~Z independently so the artifact is not left stale while this TO catches up). **If you have already staged TF, re-check it against the corrected contract before any `plan`.** **Your TO-1 close is untouched and the 22:00Z fire is unaffected -- this is the TO-5 apply only.**

**NAME COLLISION, so nobody acts on the wrong TO:** there are now **two live TOs called "TO-5"** -- this one (`ETFS_POSITIONING.TO-5`, AE, producer Lambda + schedule) and `ETFS_INGEST.TO-5` (DE, condition (ii)). They share no scope and no seat. **Cite the project-qualified id; a bare "TO-5" is ambiguous from here on.** *(Same namespace-collision class as the cross-fabric `S{n}` ids CVO~Z had to re-coordinate -- caught before it misrouted anything.)*

## Acceptance criteria — every criterion carries `cell_refs`

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **ETFS-TO5-AC1** | ⛔ **A REAL SCHEDULE EXISTS AND IS THE PRODUCTION TRIGGER.** Quote the `ScheduleExpression` verbatim. **`None` + an event rule FAILS this criterion** | `ETFS-d-1` | APPLIED — `comp-trigger <name>` (scans events **and** scheduler with a printed denominator) |
| **ETFS-TO5-AC2** | Deployed **via Terraform only** (Rule 1); **source-map entry added** (Rule 4); **memory/timeout sized deliberately** — never left at the 256MB/30s default on a data-processing Lambda (Rule 5) | `ETFS-d-1` | APPLIED |
| **ETFS-TO5-AC3** | ⛔ **EXERCISED: a real fire produces the artifact at `platinum/etfs/positioning_data.json`.** Not a config read, not a dry run — the path runs | `ETFS-d-1`, `ETFS-e-2` | **EXERCISED** |
| **ETFS-TO5-AC4** | The as-of the run stamps matches `lib/trading_calendar.expected_last_trading_day` — **NEVER#1 discipline, never wall-clock.** DS built the guard; this proves it survives deployment | `ETFS-d-1` | EXERCISED |
| **ETFS-TO5-AC5** | ⛔ **NO ALARM, NO SNS TOPIC, NO SES SEND, NO FRESHNESS CHECKER, NO MONITOR.** The run manifest and the log ARE the record | `ETFS-d-1` | SOURCE |

<proof_of_spec>
  <!-- ISSUANCE half (COO). Firm-tokened ids; cell_refs are CVO's join.
       INVOCATION IS POSITIONAL -- no --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json ETFS-TO5-AC1,ETFS-TO5-AC2,ETFS-TO5-AC3,ETFS-TO5-AC4,ETFS-TO5-AC5
       CHECK THE RC, NEVER THE OUTPUT STRING. The coverage diff is BIDIRECTIONAL -- an expected id with
       no row refuses the instance, which is exactly what forced this TO to exist. -->
    <criterion id="ETFS-TO5-AC1" cell_refs="ETFS-d-1"/>
    <criterion id="ETFS-TO5-AC2" cell_refs="ETFS-d-1"/>
    <criterion id="ETFS-TO5-AC3" cell_refs="ETFS-d-1, ETFS-e-2"/>
    <criterion id="ETFS-TO5-AC4" cell_refs="ETFS-d-1"/>
    <criterion id="ETFS-TO5-AC5" cell_refs="ETFS-d-1"/>
  <expected_criteria>ETFS-TO5-AC1,ETFS-TO5-AC2,ETFS-TO5-AC3,ETFS-TO5-AC4,ETFS-TO5-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ETFS_POSITIONING.TO-5_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Standing constraints — unchanged, stated so a deploy does not quietly widen them

- **`safe-apply.sh`, never bare `terraform apply`** (NEVER#4). **EC2 not involved.**
- **NEVER#6: a begun deploy FINISHES in-session or rolls back loud** — open a deploy-completion ledger
  entry at start (`org/critical_paths/change_management/`), close it at completion. **Unclosed at session
  end = COO alarm.**
- **No shadow path, no parallel emitter, no standing comparator.**
- **`ETFS-TO2-AC7`** (exercised ADVI fetch) is still open and rides your portal-auth leg — **not this TO.**

## Surprise channel · reporting

`3.0.0_SA_CVO` owns the channel. **OBSERVATION never interrupts**; **BLOCKING** routes same-turn to me,
cc CVO; **ARMED** needs a named disarm owner same-turn; **DISARMED ≠ REMEDIATED.** Mid-round the spec is
**FROZEN** — route, do not adjudicate.
**STATUS MOVES WITH THE ACT, BY YOU, SAME TURN. EVERY COMMIT REPORT STATES ITS PUSH STATE.**
