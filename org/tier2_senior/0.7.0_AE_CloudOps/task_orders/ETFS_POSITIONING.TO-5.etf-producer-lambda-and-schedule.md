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
<status>AWAITING CERTIFICATION -- **THE EXECUTOR ACT IS DISCHARGED. UPDATED 2026-08-28 ~19:2xZ by `2.0.0_SA_COO~Z` (issuer) under Andrew's *"completely wrap up D4"*.** The proof-of-spec instance is FILED by `0.7.0_AE_CloudOps~P` and reads rc=0 VALID **6 of 6**, 0 violations @`f32d343133` (**LOCAL** at filing -- push is the integrator's act). **ZERO re-applies, re-plans or invokes**; no ledger opened, because filing an instance touches no deployed surface. ⛔ **`ETFS-TO5-AC4` WAS RE-CUT IN THIS SAME TURN -- SEE THE CRITERIA TABLE. THE ORIGINAL WORDING WAS THE ISSUER'S DEFECT**, unsatisfiable by any correct build AND wrong if satisfied: it demanded `as_of == expected_last_trading_day` when `as_of` is T-1 by construction forever, and equality would have demanded the degenerate guard the producer explicitly rejects. The executor scored PASS on the operative clause with the falsification written inside the row, left the face UNEDITED, and routed the re-cut to the issuer. **That is the correct handling of an issuer defect and it is recorded as such.** ⚠ AC7 was found by **enumerating all 13 log streams** rather than querying an expected date, and record and artifact agree on a full sha256 rather than a byte count -- this producer has been seen republishing a live key at an IDENTICAL size with a different ETag. ⛔ **THE LINE BELOW SAYING "NOT AWAITING CERTIFICATION" WAS TRUE WHEN WRITTEN AND IS NOW SUPERSEDED** -- `3.0.0_SA_CVO~Z` refused this TO pending an EXECUTOR act, and that act now exists. ⛔ Nothing here stamps `ETFS_POSITIONING` or D4 closed; Andrew ruled "D4 is done" a READ, not a close order. ⚠ **ORIGINAL STATUS FOLLOWS, APPENDED AND NOT REPLACED** (a bulk edit at @4253643625 once replaced seven status bodies wholesale and destroyed 21,000 characters; nothing below this line is new). ~~pending~~ -- ⛔⛔ **NOT AWAITING CERTIFICATION. THIS FACE SAID IT WAS AND THAT IS FALSE.** `3.0.0_SA_CVO~Z` ADJUDICATED this TO @`e3d86ad9d1` and **REFUSED it pending an EXECUTOR ACT**: **NO INSTANCE EXISTS -- nothing was ever filed**. ⛔ **NO AMOUNT OF CERTIFIER TIME MOVES THIS.** A valid proof-of-spec instance is a BUILD-side act and it is what is missing.

⚠ **AND THE ISSUER TOLD THE CERTIFIER THE OPPOSITE, THREE TIMES.** `2.0.0_SA_COO~Z` wrote *"nothing on this list is blocked on anything but you"* in three separate briefs. **It was false for this TO every time.** `3.0.0_SA_CVO~Z` named the cost precisely: **a seat told it is the sole blocker does not go looking for another owner** -- so this would have sat behind a certifier who cannot move it. ⭐ **This correction is written the moment the author had a trigger to return, which is the whole remedy for the stale-face class measured today (7 of 12 read uncertified while their certificates sat on origin).**

**OWNER: `2.0.0_SA_COO~Z` as issuer, to RE-SEAT or DISPOSE.** No live lane; a seat request is with `0.0.0_AB_MSTR~Z` and Andrew's word governs. ⛔ **NOT a certification item and must not be counted as one.**

⚠ **ORIGINAL `<status>` PRESERVED VERBATIM BELOW -- APPENDED, NOT REPLACED.** (An earlier bulk edit at @4253643625 replaced seven status bodies wholesale and destroyed 21,000 characters; restored @2ee8375f02. Nothing below this line is new.)

queued -- for `3.0.0_SA_CVO~Z` CERTIFICATION. **NO EXECUTOR ACT IS PENDING AND NO SEAT IS NEEDED.**

⛔ **`queued` IS NOT A DISCHARGE CLAIM.** The acceptance criteria on this TO were **NEVER CERTIFIED**,
and this office will not buy a terminating register by asserting one. **The lead word says only what is
true: the build is done in the world and the next act is a CERTIFICATION, which belongs to
`3.0.0_SA_CVO~Z` and to no executor.**

**RE-FACED 2026-08-28 ~04:0xZ by `2.0.0_SA_COO~Z` (issuer). WHY THE LEAD WORD CHANGED, AND IT IS A
DEFECT THIS OFFICE ALREADY FIXED ONCE TONIGHT AND DID NOT CARRY ACROSS:** this face led with an emoji
(or a bare word), so `to-check.py` -- which classifies on the FIRST TOKEN ONLY -- read it **`ACTIVE`**.
⛔ **An `ACTIVE` face is an instruction to spend a seat**, and the seat it named is DEAD: `<issued_to>`
carries a BASE serial (`0.4.0_DS_ClientPlatform` / `0.7.0_AE_CloudOps` / `0.4.0_DE_ClientPlatform`) and
**no base serial is registered** -- only lettered lanes are live. **The same lead-word defect was fixed
on `ETFS_POSITIONING.TO-4` earlier tonight and NOT applied to its four siblings.**

⚠ **`<issued_to>` IS DELIBERATELY LEFT UNCHANGED.** It is the historical record of who executed this,
and rewriting it would erase that. **It is NOT a live assignment and must not be read as one.**

---

**ORIGINAL STATUS, PRESERVED VERBATIM BELOW:**

✅ **OBJECTIVE MET IN THE WORLD — THE SCHEDULE FIRED.** `cron(0 13 * * ? *)` UTC has fired `run_class: scheduled` on 2026-08-25, 08-26 and 08-27; the newest manifest carries `run_class: scheduled` / `producer: etf_positioning_gold` / `books_full 4` / `books_shell 0`, and served platinum moved 2026-08-27T13:01:25Z. ⛔ **THE FACE PREVIOUSLY READ "ACTIVE — THE CRITICAL PATH ... NOTHING GATES THIS NOW" AND THAT WAS THREE DAYS STALE** — it was the carrier that let *"GOLD HAS NEVER RUN"* be relayed by two seats on 2026-08-28 about a plane that had been running since 08-25. Disposition set by the issuing office 2026-08-28 ~02:0xZ on `1.0.0_SA_CTO~Z`'s measurement (11371/11743), **carried as THEIRS and labelled — not re-run, because re-running the same instrument is repetition, not corroboration.** ⚠ **NOT an AC-level certification** (`3.0.0_SA_CVO~Z`'s act); what is settled is that **this face is NOT WAITING ON A SEAT**.</status>
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
| **ETFS-TO5-AC4** | ⚠ **RE-CUT 2026-08-28 ~19:2xZ by `2.0.0_SA_COO~Z` (issuer). THE ORIGINAL WORDING WAS UNSATISFIABLE BY ANY CORRECT BUILD, AND SATISFYING IT WOULD HAVE BEEN WRONG.** ~~The as-of the run stamps MATCHES `lib/trading_calendar.expected_last_trading_day`~~ — that clause demanded EQUALITY. Measured by `0.7.0_AE_CloudOps~P` across 4 of 4 scheduled fires: `expected_frontier=D`, `as_of=D-1`, `trading_days_behind=1`. **as_of is T-1 BY CONSTRUCTION, forever**, because `trading_calendar.py:101-105` returns today-if-trading while both inputs' newest partition is D-1 (silver netassets fires 22:00Z on D; the bbg pull writes `bbg/D-1/`). ⭐ **AND EQUALITY WOULD BE THE DEGENERATE GUARD THE PRODUCER DELIBERATELY REJECTS** — `etf_positioning_gold.py:486-493` states the design intent: `expected` from the CALENDAR, `as_of` from the DATA, independent on purpose, because *"a guard whose two sides are the same expression over the same clock has no input that makes it fire."* CLAUDE.md NEVER#4 agrees T-1 is the norm. **THE CRITERION, AS IT NOW BINDS:** the run DERIVES as_of from the DATA and RECONCILES it against the calendar — it computes `trading_days_behind` against `expected_last_trading_day` and STAMPS that lag, which must be a small NON-NEGATIVE integer, **never wall-clock**. A wall-clock as_of and a broken calendar are both still caught; only the false equality is gone. | `ETFS-d-1` | EXERCISED |
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
> ⛔ **MANDATORY DISCLOSURE BEFORE FIRING — REWRITTEN 01:2xZ ON ANDREW-DIRECT. THE PREVIOUS VERSION
> OF THIS CHECK WOULD HAVE CERTIFIED THE WRONG FIX AS CORRECT.**
> It asked *"is `mmkt` in `CASH_NAME_MARKERS`?"* — so adding that marker would have flipped it to
> **YES / green while routing SALXX to `Cash`, the answer Andrew REJECTED for its sibling.**
> **A check keyed on the PATH, certifying an outcome it never looked at.**
>
> ✅ **ANDREW-DIRECT ~01:21Z, VERBATIM: *"Just fix it now and once its fixed lets rerun the pulls and
> lock this in."*** Authorization to fix AND to re-run; no further call needed on either.
> ⛔ **RULED (`1.0.0_SA_CTO~Z`, withdrawing their own `"mmkt"` recommendation): BOTH money-market
> funds classify as `Fixed Income` / `Ultra Short Duration`** — his FXFXX ruling applied to the class.
> **Two changes, not one: FXFXX must STOP resolving to `Cash` (it fires `treasury obligation` today);
> SALXX must START resolving there (it falls through to `Equity`).**
> ⚠ **The CASH path stays for real cash: silver `is_cash=True` (4 rows tonight, filepoint's
> `MoneyMarketFlag=Y`) is UNTOUCHED and must remain `Cash`.**
>
> ⛔⛔ **THIS CHECK IS INSUFFICIENT — IT IS A UNIT READ AND IT WOULD PASS A DEFECTIVE BUILD.**
> `0.4.0_DS_ClientPlatform~Z` found (and I confirmed at source) that `@0c03c359f2` fixes `classify()`
> and leaves **three book-level aggregations keyed on the RAW `is_cash` flag**:
> `:691 cash_w` · `:692 eq_w` · `:697` the sector map. **So the ROW renders `Fixed Income` while its
> WEIGHT stays in `alloc_cash` (PFOE 2.34%, PFDE 0.33%) and `Ultra Short Duration` never enters the
> sector map.** ⛔ **The four cells below all PASS on that build** — they exercise the function, not
> the artifact. **Rule 22a's layer rule, and my check is on the wrong layer.**
> ✅ **THE SUFFICIENT CHECK IS ARTIFACT-LEVEL: read the emitted book — `alloc_cash`, `alloc_equity`,
> `alloc_fixed_income` and the sector map — NOT `classify()`'s return.**
> ⛔ **AND IT NEEDS A GUARD (`3.0.0_SA_CVO~Z`, falsifying their own oracle): `alloc_cash = 0.00`
> CANNOT DISTINGUISH "the defect fired" FROM "the book is a SHELL" — and the shell state is TODAY's
> CORRECT state.** DIVZ/IDVZ read `holdings=0, alloc_cash=0.0` right now with `Z-S35` NOT fired.
> **A reader checking tomorrow against an unfixed partition would read 0.00 and report the defect
> CONFIRMED on two empty books.**
> ```
> GUARD FIRST:  DIVZ.holdings > 0 AND IDVZ.holdings > 0   (holdings_status == "full")
> THEN:         alloc_cash ~= 0.58 / 0.89 -> correct  ·  ~= 0.00 -> Z-S35 fired
> GUARD FAILS:  shells. The partition fix has not landed and Z-S35 is UNMEASURABLE --
>               not absent, not confirmed. REPORT THE GUARD, NOT THE NUMBER.
> REFERENCE (instrument works on a full book): PFDE alloc_cash 0.36 · PFOE 2.35
> ``` Not written here because the
> build is on hold and the aggregations will change; **whoever resumes writes it against the emitted
> JSON.**
> ✅ **CONTAINED: `@0c03c359f2` is LOCAL, NOT DEPLOYED** — deployed package measured independently at
> my seat: `Ultra Short Duration` 0, `Fixed Income` 0, `cash_sentinel` 0, negative control fired.
> **The defect cannot become live without a deploy. DO NOT DEPLOY.**

> ```
> CHECK THE OUTCOME -- and CALL classify() WITH ITS REAL SIGNATURE:
>     classify(is_cash, gics, cash_sentinel)      <- THIRD ARG, defaults True. Omit it and
>                                                    FXFXX returns Cash and looks BROKEN.
>   FXFXX (True, None, cash_sentinel=False) -> Fixed Income / Ultra Short Duration   MUST PASS
>   Cash&Other (True, None, True)           -> Cash / Cash & Cash Equivalents        MUST PASS
>   AAPL  (False, 'Information Technology') -> Equity / Information Technology       MUST PASS
>   SALXX (unflagged)                       -> Equity  *** EXPECTED. DEFERRED HALF. NOT A FAIL ***
> ```
> ⛔ **SALXX IS NOT A MUST-PASS AND THIS LINE IS THE CORRECTION.** The ruling split the work:
> **FXFXX is a MAPPING (issuer already flagged it — landed @0c03c359f2); SALXX is a DETECTION and
> was explicitly deferred.** An earlier version of this block listed SALXX as must-pass and **would
> have FAILED A CORRECT BUILD.**
> ⚠ **VERIFIED BY EXECUTION at 01:4xZ against the tree: FXFXX / Cash&Other / AAPL all PASS;
> `SUB_ASSET_CLASS_VOCAB` now contains `Ultra Short Duration`.**
> ⛔ **AND THE SIGNATURE TRAP IS REAL — I FELL IN IT: calling `classify(is_cash, gics)` with two args
> takes `cash_sentinel=True`, returns Cash for FXFXX, and reads as the fix being broken.** I reported
> 2-of-4 FAIL on a correct, ratified commit before catching it. **Pass the third argument.**

> ⛔ **CORRECTED 01:3xZ — the 4th cell previously read "a silver `is_cash=True` row -> Cash", AND
> FXFXX **IS** ONE OF THOSE ROWS** (2 of the 4: PFDE 0.3300, PFOE 2.3400; the other two are
> `Cash&Other`). **Cells 1 and 4 contradicted each other on the same security.** I transcribed the
> ruling's own contradiction into the check instead of testing it against data I had already
> measured. ⭐ **Naming `Cash&Other` fixes it AND makes the set strictly stronger: the two
> issuer-flagged rows now differ in EXACTLY ONE property — money-market vs actual cash — so the pair
> discriminates the ruling instead of merely illustrating it.**
> ⭐ **Per `1.0.0_SA_CTO~Z`'s resolution: silver's `is_cash=True` STAYS TRUE and authoritative. This
> changes where a true cash flag PRESENTS, never the flag** — Rule 17 and CONV-1 both intact.
> **WHOEVER FIRES MUST STATE WHICH BRANCH THEY FIRED UNDER.** *(Still information, not a gate — but
> the sovereign question that made it a disclosure is now ANSWERED, so the branches are pass/fail.)*
>
> ⛔⛔ **AND A SEPARATE GUARD ON HIS OWN RE-RUN INSTRUCTION: THE AD-HOC L1 RE-RUN IS **DROPPED ENTIRELY** — NOT MOVED TO 04:15Z.** *(RULED `1.0.0_SA_CTO~Z` 02:24Z.)* **MEASURED: the ONLY consumer of `bbg/` is `etf-positioning-producer-daily` = `cron(0 13 * * ? *)`. Gold fires 13:00Z; NOTHING reads `bbg/` before then, and the SCHEDULED 11:00Z L1 pull writes `bbg/2026-08-24/` two hours ahead of it.** So an ad-hoc run **cannot move Andrew's clock by one minute**, and the scheduled pull overwrites the same key anyway — **the ad-hoc artifact is not even durable.** *It was priced "a free option" and it was never free.*
> ⛔ **AND THE ARITHMETIC THAT KILLED THE 04:00Z OPTION, KEPT SO NOBODY RESURRECTS IT: 04:00Z IS EXACTLY LOCAL MIDNIGHT (UTC-4). 03:59:59Z -> as-of 2026-08-21 WRONG; 04:00:00Z -> 08-24 OK. ZERO SECONDS OF MARGIN** — one second early writes the same wrong prefix from the same clock bug **and reads as the fix having failed rather than the clock.** (`0.4.0_DS_ClientPlatform~Z` ran the arithmetic five seats had quoted for four hours; `0.0.0_AB_MSTR~Z` hit exactly this at 00:49Z.) At
> 01:2xZ local is still MONDAY, so an L1 re-run lands under `bbg/2026-08-21/` **again** — the same
> wrong key — **and would OVERWRITE the 170-row characteristics artifact everything currently relies
> on.** **His authorization is real; the timing is not safe yet.** Gold fix + exercise now (no run
> needed). **NO ad-hoc L1 re-run at all — the SCHEDULED 11:00Z pull is the path.**

> ⚠ **DO NOT fire while `bbg/2026-08-24/` is absent** — the producer steps back to 08-21, publishes a
> further identical-looking artifact, and adds another ad-hoc decoy to a prefix already carrying
> three at one as-of (all 76,149 B, three ETags). **That is the only thing the hold protects.**
> ⭐ **`bbg/2026-08-24/` is written by the **SCHEDULED 11:00Z pull**, with NO code change — the
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

> ⛔⛔ **AND THE 11:00Z PULL IS NOT CLOUD-SCHEDULED — READ THIS BEFORE DIAGNOSING AN EMPTY PAGE.**
> ```
> EventBridge: 137 rules auto-paginated · rules at hour 11 ......... NONE
>   etf-positioning-producer-daily  cron(0 13)  ENABLED   <- GOLD. In AWS. Fires regardless.
> LOCAL Windows task on THIS BOX:
>   OPAL_BBGTML_daily_pull   Ready   next run 2026-08-25 07:00 LOCAL (= 11:00Z)
> ```
> **GOLD FIRES FROM AWS; ITS INPUT DEPENDS ON THIS DESKTOP BEING AWAKE AT 07:00 LOCAL.**
> ⛔ **If the box is down, the failure is INDISTINGUISHABLE FROM TONIGHT:** `skipped_no_bbg=
> ['2026-08-24']`, as_of steps back to 08-21, **two shells and a well-formed artifact, with a log
> line saying the guard worked.** **So if the books are empty at 13:00Z, THE FIRST QUESTION IS "did
> `OPAL_BBGTML_daily_pull` run at 07:00 local?" — not "what is wrong with the producer."**
> ⚠ *(This box has been restarted on the MSP's schedule before — planned N-able RMM restarts, six
> seats down 5h10m, on someone else's calendar. Not a prediction; a stated single point of failure.)*
> ⚠ **AND THAT TASK RUNS THE WORKING TREE** — so any edit landing in `etf_daily_pull.py` before
> 07:00 local **IS a deploy into the delivery run.** Second reason `:1375` is correctly carded for
> daylight.

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
