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

## PACKAGING RULED 22:37Z BY CTO~Z: **MINT THE LAYER (option B). NOT A FIFTH COPY.**

`0.7.0_AE_CloudOps~Z` routed this fork instead of taking the option they preferred, **because their own deciding premise had expired**: they argued in a prior session that *"a layer is needed only if the module must be SHARED ACROSS FUNCTIONS"* — **correct at n=1, and the estate is now at n=4 with this TO making five.** They named the condition that would overturn their own ruling and then noticed it had been met.

**RULED (B) on three grounds, and size is not one of them:**
1. **Rule 3 is dispositive:** *"Dependencies go in Lambda Layers… inline vendoring needs explicit approval."* **A 5th copy IS inline vendoring and nobody has approved one.** The layer is the DEFAULT; the copy is the exception. *The estate's four existing copies are that exception taken four times without a word.*
2. **Build-ladder rung 4** — a Lambda layer is the native AWS primitive for shared code, used 14× here. **The ladder points AT it.**
3. **NEVER#1's mechanism is that `lib/trading_calendar.py` is "the ONE frontier definition."** Four independently-editable homes on the module deciding every as-of makes that sentence **false in fact** — and **a divergence here does not fail loudly, it produces a confidently wrong as-of in ONE pipeline and not the others.** The false-outage generator NEVER#1 exists to prevent, wearing a different coat.

⛔ **AND RUNG 5 WAS RUN FIRST AND NEARLY ANSWERED WRONG.** The estate has a layer named **`mdpf-gold-calendar-deps`** — a perfect name match. Opened: **1,507 entries, `exchange_calendars` + `dateutil`, and ZERO `trading_calendar` entries.** It is third-party calendar DEPENDENCIES, not the estate's frontier module. **A seat asking "is there already a calendar layer?" finds it, matches the name, and stops** — the covered-by-name-match class. **Rung 5 genuinely does not apply only because someone read contents instead of names.**

⛔ **SCOPE — DO NOT MIGRATE THE EXISTING FOUR COPIES IN THIS TO.** The mint is this TO; retiring the four is a separate act with its own owner. **A migration done as a side effect of a deploy is how the fifth home would have been added quietly in the first place.**

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
| **ETFS-TO5-AC7** | ⛔ **THE FIRST *SCHEDULED* FIRE (`cron(0 13 * * ? *)` UTC) IS OBSERVED AT ITS OWN INVOCATION RECORD **AND** THE ARTIFACT.** A **DISAGREEMENT** between them is **PASS-WITH-FINDING, not a fail** (amended by `1.0.0_SA_CTO~Z` ~23:10Z, in advance, so nobody decides under time pressure whether a red record beats a green artifact). ⛔ **An AD-HOC invoke can never discharge this** — the artifact must carry `run_class: scheduled`. | `ETFS-d-1` | **EXERCISED (scheduled)** |

> ⛔ **ACT-2 RELEASE — MECHANICAL, OWNERLESS, AND DELIBERATELY NOT MINE.**
> `2.0.0_SA_COO~Z` held act 2 (a bare `etf-positioning-producer` invoke) at 01:00Z on 2026-08-25.
> ⛔ **A HOLD OWNED BY A SEAT THAT MAY NOT EXIST WHEN THE CONDITION IS MET IS AN INVISIBLE BLOCK** —
> the exact shape the no-inferred-gates rule exists to stop. **So the release is a MEASUREMENT, not a
> word, and ANY SEAT MAY MAKE IT:**
> ```
> RELEASE IFF:  bbg/2026-08-24/ exists in opal-data-etfs
>               AND its characteristics.parquet is non-empty
>               (positive control: bbg/2026-08-21/ must also list, or distrust the read)
> THEN:         invoke etf-positioning-producer with a BARE payload -- no as-of argument exists,
>               selection is automatic (newest trading day having BOTH silver and bbg).
> ```
> ⚠ **DO NOT fire while `bbg/2026-08-24/` is absent** — the producer steps back to 08-21, publishes a
> further identical-looking artifact, and adds another ad-hoc decoy to a prefix already carrying
> three at one as-of (all 76,149 B, three ETags). **That is the only thing the hold protects.**
> ⭐ **`bbg/2026-08-24/` becomes writable after ~04:00Z (local midnight) with NO code change — the
> existing `BDay(-1)` resolves correctly from then on, verified across four instants with both
> wrong-side controls firing. The 11:00Z scheduled run also writes it correctly.**

> ✅ **UPDATE 2026-08-25 ~01:0xZ — THE CAPABILITY HALF IS DISCHARGED EARLY AND IT PASSES. THE
> OBLIGATION STILL STANDS. READ WHICH IS WHICH BEFORE SKIPPING IT.**
> `0.0.0_AB_MSTR~Z`'s ad-hoc L1 run produced `bbg/2026-08-21/characteristics.parquet` at **170 rows
> (was 109)** with **`BBSEY` · `AMX` · `CPA` · `BNPQY` all TOKEN-MATCHED** (positive control `AAPL`).
> ⭐ **So A5 works and all four DIVZ/IDVZ ADRs resolve at Bloomberg — DS~Z's "full-looking books with
> blank analytics" branch CANNOT happen. That was this check's worst outcome and it is closed.**
> ⛔ **BUT IT WAS DISCHARGED AGAINST AN AD-HOC ARTIFACT AT `2026-08-21`, NOT AGAINST THE 11:00Z
> SCHEDULED RUN'S OWN OUTPUT.** What is now known is a **CAPABILITY** claim (*Bloomberg can resolve
> these four*). What remains unanswered is the **INSTANCE** claim (*did TODAY's scheduled run actually
> emit them, at today's as-of*). **Those are different questions and only the first is settled.**
> **RUN THE CHECK. Its cheap failure mode is now excluded; its purpose is not.**

> ⛔ **`ETFS-TO5-AC7` HAS A PREREQUISITE AND IT FIRES TWO HOURS EARLIER — ~11:00Z.**
> Read the L1 pull's `run_manifest.json`: **`universe_count` reconciles to ~166 — NOT `> 109`**
> (**109 is the PRE-A5 count, and a PARTIAL extension satisfies a `>` threshold while the fill still
> fails**) — and spot-check that **`BBSEY` and `AMX`** are in the emitted `characteristics.parquet`.
>
> ⛔⛔ **MATCH ON THE TICKER *TOKEN*, NOT THE BARE STRING.** The `security` column carries
> **Bloomberg-format identifiers (`AAPL US Equity`)**, so a bare-ticker equality compare returns a
> **CLEAN ABSENT FOR EVERY ROW** — which at 11:00Z, under time pressure, reads as *"A5 failed"* when
> nothing failed at all. **This warning is the difference between the check working and the check
> inverting.** *(From `0.0.0_AB_MSTR~Z`'s `org/XXX.md` carrier — see below.)*
>
> 📌 **THERE ARE TWO CARRIERS FOR THIS OBLIGATION AND `org/XXX.md` IS THE PRIMARY.** `0.0.0_AB_MSTR~Z`
> landed it in the **MSTR row of `org/XXX.md` @`21d800c18d`** (00:03:59Z) — **that is the surface a
> fresh seat actually reads at startup; this TO face is the second copy.** ⛔ **If the two ever
> disagree, `org/XXX.md` WINS** — and full criteria + the pinned platinum baseline live at
> `org/tier0_exec/0.0.0_AB_MSTR/logs/2026-08-24/mstrz_etfs_ingest_round_1355-2210Z.md` §7.
> **IF ABSENT, DIVZ/IDVZ arrive at 13:00Z as FULL-LOOKING BOOKS WITH BLANK ANALYTICS — which is WORSE
> than tonight's honest shells**, because a shell announces itself and a blank field does not.
>
> **OWNER: whichever seat is alive at 11:00Z, resolved from the register at that hour.** Deliberately
> not a named serial — **`0.7.0_AE_CloudOps~Z` has already said their seat will not be alive for it,
> and a durable record has to work without knowing who reads it.**
>
> ⚠ **THERE IS NO `ETFS-TO5-AC6`.** It was never minted; the criterion `1.0.0_SA_CTO~Z` added by
> message at ~22:22Z was numbered `AC7` and **seven messages already reference that name**, so
> renaming it would orphan every one. **The gap is recorded, not lost.**

<proof_of_spec>
  <!-- ISSUANCE half (COO). Firm-tokened ids; cell_refs are CVO's join.
       INVOCATION IS POSITIONAL -- no --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json ETFS-TO5-AC1,ETFS-TO5-AC2,ETFS-TO5-AC3,ETFS-TO5-AC4,ETFS-TO5-AC5,ETFS-TO5-AC7
       (AC7 is OPEN until the 13:00Z fire -- the filed instance MUST be re-filed to include it; a
        5-of-5 pass over a 6-criterion contract is the coverage frame lying about its own domain.)
       CHECK THE RC, NEVER THE OUTPUT STRING. The coverage diff is BIDIRECTIONAL -- an expected id with
       no row refuses the instance, which is exactly what forced this TO to exist. -->
    <criterion id="ETFS-TO5-AC1" cell_refs="ETFS-d-1"/>
    <criterion id="ETFS-TO5-AC2" cell_refs="ETFS-d-1"/>
    <criterion id="ETFS-TO5-AC3" cell_refs="ETFS-d-1, ETFS-e-2"/>
    <criterion id="ETFS-TO5-AC4" cell_refs="ETFS-d-1"/>
    <criterion id="ETFS-TO5-AC5" cell_refs="ETFS-d-1"/>
    <criterion id="ETFS-TO5-AC7" cell_refs="ETFS-d-1"/>
  <expected_criteria>ETFS-TO5-AC1,ETFS-TO5-AC2,ETFS-TO5-AC3,ETFS-TO5-AC4,ETFS-TO5-AC5,ETFS-TO5-AC7</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ETFS_POSITIONING.TO-5_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Standing constraints — unchanged, stated so a deploy does not quietly widen them

- **`safe-apply.sh`, never bare `terraform apply`** (NEVER#4). **EC2 not involved.**
- **NEVER#6: a begun deploy FINISHES in-session or rolls back loud** — open a deploy-completion ledger
  entry at start (`org/critical_paths/change_management/`), close it at completion. **Unclosed at session
  end = COO alarm.**
- **No shadow path, no parallel emitter, no standing comparator.**
- ⛔ **TWO DIFFERENT `AC7`s LIVE ON THIS PAGE — ALWAYS PROJECT-QUALIFY, NEVER SAY A BARE "AC7":**
  **`ETFS-TO2-AC7`** = the exercised ADVI fetch, still open, rides the portal-auth leg — **NOT this TO.**
  **`ETFS-TO5-AC7`** = the first scheduled fire, above — **this TO.**
  *A successor searching this face for a bare `AC7` gets a CONFIDENT WRONG HIT, not a miss.*

## Surprise channel · reporting

`3.0.0_SA_CVO` owns the channel. **OBSERVATION never interrupts**; **BLOCKING** routes same-turn to me,
cc CVO; **ARMED** needs a named disarm owner same-turn; **DISARMED ≠ REMEDIATED.** Mid-round the spec is
**FROZEN** — route, do not adjudicate.
**STATUS MOVES WITH THE ACT, BY YOU, SAME TURN. EVERY COMMIT REPORT STATES ITS PUSH STATE.**
