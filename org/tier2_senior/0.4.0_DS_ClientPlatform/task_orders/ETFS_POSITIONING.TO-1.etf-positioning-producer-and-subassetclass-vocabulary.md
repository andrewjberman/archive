# TO ETFS_POSITIONING.TO-1 — the ETF Positioning PRODUCER (a MINT) + the `sub_asset_class` VOCABULARY ACT

<task_order id="ETFS_POSITIONING.TO-1" project="ETFS_POSITIONING">
<decomp_ref>workflows/atom_decomposition/runs/etfs-positioning/20260821T194927Z/DECOMP.md — cells ETFS-d-1, ETFS-d-2 (reads ETFS-a-1..a-6; constrained by ETFS-a-7/a-8 boundaries)</decomp_ref>
<certification>⛔ **UNCERTIFIED DECOMP.** This TO was cut before `3.0.0_SA_CVO` certified the stage-3 decomp, under Andrew's 19:3xZ priority word and CTO's explicit instruction to cut UNCERTIFIED-on-face rather than idle a seat. Permitted by the pipeline, disclosed here by the issuer, never silent. If CVO's cert returns a DECOMP-INVALIDATING item, this TO's premises are re-derived by the issuer — the executing seat does not adjudicate that.</certification>
<issued_to>DS-class (data plane / producer). Seated: `0.4.0_DS_ClientPlatform` — universe-config owner (`config/etf_universe.json` names "0.4.0_DS_ClientPlatform (ETFS_SETUP DS-contract lane)"), `data/**` lane per Rule 13.</issued_to>
<executor_class>DS-class</executor_class>
<seating_trigger>SEATED NOW (seat live, reported reading at 65568/65577). If this class goes dark mid-execution, the spawn call routes to MSTR SAME-TURN as a naming obligation, not a discovery.</seating_trigger>
<placement>LAPTOP (Rule 26). The apply runs on the device that owns the work — this seat's box. NOTHING here is ferried to site Z, and nothing here applies anything on the terminal box.</placement>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-21T19:55Z</issued>
<status>ACTIVE</status>
<priority>P1 — SESSION PRIORITY. Andrew-direct 2026-08-21 ~19:3xZ, VERBATIM: "Make it clear to the fabric that I want ETFS_POSITIONING DONE RIGHT NOW. IT IS PRIORITY FOR THIS SESSION". Front of this seat's queue; everything else at this seat yields.</priority>
<scope_guard>⛔ ANDREW-DIRECT DS SCOPE-LIFT, VERBATIM: *"bring the DS in just no old TOs, they address what theyre tasked now, and eveyrthing else is on hold for that seat unless qualified otherwise."* **THE HOLD REMAINS THE DEFAULT AND THE BURDEN IS ON ME AS TASKER, NOT ON YOU TO REFUSE.** This TO qualifies EXACTLY the work below and NOTHING else: no D4_ETFPOS TO, no MDPF_PROVCANON work, no backlog item, nothing from the 08-21 TO sweep. If something adjacent looks obviously worth doing — it is still held. One line to CVO's channel, keep working.</scope_guard>
<authority>PRD `docs/architecture/ETFS_POSITIONING_PRD.md` s.11.1 (the DONE) + s.10.4 (ship shape, Andrew's) + s.11.5 (inherited constraints). Build authorized END TO END 14:1xZ @1cf66d7d93 — no build fence anywhere in this TO.</authority>
<proof_of_spec>
  <!-- ISSUANCE half (COO, at decomposition): the machine-readable criterion-id set.
       Ids are FIRM-TOKENED so they cannot collide across the three parallel ETFS lanes.
       CELL_REFS ARE THE POINT: 3.0.0_SA_CVO's bidirectional alignment check is a JOIN on
       these, not a prose read -- every criterion names the decomp cell it discharges, and
       every criterion-bearing cell is reachable from some criterion. A criterion arriving
       WITHOUT cell_refs is REFUSED, never retrofitted: a retrofitted derivation makes
       alignment LOOK satisfied while being FALSE, and CVO confirmed they would have
       computed exactly that as PASSING.
       COMPLETION half (assignee, from their OWN efforts): a schema-valid instance at the
       path below, validated BEFORE the status flip.
       INVOCATION IS POSITIONAL -- there is NO --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json ETFS-TO1-AC1,ETFS-TO1-AC2,ETFS-TO1-AC3,ETFS-TO1-AC4,ETFS-TO1-AC5,ETFS-TO1-AC6,ETFS-TO1-AC7
       CHECK THE RC, NEVER THE OUTPUT STRING. The usage banner contains the vocabulary of
       BOTH verdicts ("Exit 0 = VALID"), so a caller grepping for success matches the banner
       of a call that validated NOTHING. rc=0 VALID / rc=1 INVALID / rc=2 usage. And the
       2-arg form (id set omitted) returns a clean rc=0 that says COVERAGE UNCHECKED -- pass
       the ids. -->
    <criterion id="ETFS-TO1-AC1" cell_refs="ETFS-d-1"/>
    <criterion id="ETFS-TO1-AC2" cell_refs="ETFS-d-1"/>
    <criterion id="ETFS-TO1-AC3" cell_refs="ETFS-d-1"/>
    <criterion id="ETFS-TO1-AC4" cell_refs="ETFS-d-1"/>
    <criterion id="ETFS-TO1-AC5" cell_refs="ETFS-d-1, ETFS-a-5"/>
    <criterion id="ETFS-TO1-AC6" cell_refs="ETFS-d-2"/>
    <criterion id="ETFS-TO1-AC7" cell_refs="ETFS-a-7, ETFS-a-8"/>
  <expected_criteria>ETFS-TO1-AC1,ETFS-TO1-AC2,ETFS-TO1-AC3,ETFS-TO1-AC4,ETFS-TO1-AC5,ETFS-TO1-AC6,ETFS-TO1-AC7</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_POSITIONING.TO-1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## ⛔ SPEC-AT-PICKUP — YOUR FIRST ACT, BEFORE ANY BUILD

Run these live and report what they returned. **A TO can lie about its own state; three same-day specimens proved re-grounding at pickup is the fix that worked every time.**

| # | Premise this TO rests on | The oracle that would FALSIFY it |
|---|---|---|
| O-1 | The producer is a **MINT** — no positioning producer exists today | `find data/etfs/scripts -name "*position*"` → **must be EMPTY** |
| O-2 | Weights are already ours, PFDE/PFOE full | `aws s3 ls s3://opal-data-etfs/silver/holdings/ \| tail -3` → 2026-08-20 present |
| O-3 | **`bbg/{date}/` still has ONE date and NO scheduled fire has landed** | `aws s3 ls s3://opal-data-etfs/bbg/` → **if a SECOND date appears, say so — that changes ETFS-TO1-AC5 from pending to provable** |
| O-4 | The universe is runtime-read (no redeploy to add a ticker) | `aws s3 cp s3://opal-data-etfs/config/etf_universe.json -` |

## ⛔ THE PREMISE THAT DIED TODAY — READ THIS BEFORE YOU SIZE ANYTHING

CTO passed the fabric a decomp fact at 65582: *"the production input exists now."* **IT IS FALSE AND WAS RETRACTED** (MSTR bridge 65600; CTO self-correction 65612). `s3://opal-data-etfs/bbg/2026-08-20/`'s 7 objects were written by **three AD-HOC standalone runs of `etf_daily_pull.py` from the terminal box (~10:17Z)**. The scheduled task **has not fired since the ETF leg was appended**; NextRun is **2026-08-22 07:00 local**.

**`bbg/{date}/` IS THEREFORE THREE THINGS AND YOUR CODE MUST NAME WHICH IT READS:**
1. `bbg-testpull/` — the **FROZEN QA reference** (+ the B-form reference code at `bbg-testpull/code/`).
2. `bbg/{date}/` written by a **SCHEDULED fire** — the production input. **DOES NOT EXIST YET.**
3. `bbg/2026-08-20/` — **ad-hoc output resident in the production prefix.** A third state.

**COO RULING, so you are not blocked by this:** you **BUILD against the `bbg/{date}/` CONTRACT** — schema, manifest, partitioning — which is fully readable from (2)'s artifacts and from `bbg-testpull/`. That is legitimate **build-time correctness**. You **PROVE against the first SCHEDULED landing** (ETFS-TO1-AC5). **Build does not wait; proof does.** Do NOT cite the ad-hoc objects as production evidence anywhere, and do NOT move or delete them — their disposition is an open channel item, not your work.

## Half 1 — `ETFS-d-1`: THE PROJECTION PRODUCER

Build the scheduled producer that assembles the **four books** (DIVZ / IDVZ / PFDE / PFOE) in the **Positioning shape** (PRD s.4 rectangle: book-level characteristics + returns + weighted holdings with per-holding analytics) from the (a) plane.

**SHIP SHAPE IS ANDREW'S AND IS NOT NEGOTIABLE (PRD s.10.4): TWO FULL BOOKS (PFDE/PFOE) + TWO BOOK-LEVEL SHELLS (DIVZ/IDVZ), shells upgrading forward automatically when DIVZ/IDVZ constituent rows land.** The producer must emit the two shells **without** constituent rows and pick them up **without a code change** when they arrive. **The page ships on this shape — it does NOT wait for DIVZ/IDVZ.**

**THE SHELLS' CAUSE IS ALREADY DIAGNOSED — DO NOT SIZE IT AS AN INVESTIGATION.** `DIVZ 0 / IDVZ 0` is a **missing call site**: `etfs-netassets-daily/lambda_function.py:381` defines `TS_HOLDINGS_ENABLED`, `:420` defines `fetch_trueshares_holdings`, and CTO source-confirmed the flag is **never branched on** and the function is **never called**. Not a vendor problem, not a data-availability unknown. That repair is `ETFS-c-1`, **gated on Andrew's egress word, NOT in this TO.**

**WRITE TARGET — RULED BY COO, see the ruling block below: a SEPARATE ETF artifact. Do NOT add ETF keys to the existing `positioning_data.json`.** The exact key/prefix is `ETFS_POSITIONING.TO-2`'s (AE) deliverable; **build against the CONTRACT and take the key as a parameter** so you are not blocked waiting for it.

**LAW THAT BINDS THIS BUILD (s.11.5, not preference):**
- **PRODUCTION = SCHEDULED.** An ad-hoc run is a QA instrument only, and **a pipeline whose only trigger is another pipeline's success has no schedule and is a defect.** This producer gets a **real schedule**.
- **NO shadow path, no parallel emitter, no standing comparator** (Andrew, complete veto, twice). Build it correctly and port.
- **ALERT/MONITOR MORATORIUM** — the run manifest + log ARE the record. **Do not build a freshness checker, alarm, SNS topic, or monitor.**
- **NEVER#1 as-of discipline** — `BDay(-1)`, trading calendar, never wall-clock.
- **Rule 15** — `from __future__ import annotations` at the top of every gold/silver/bronze `.py`.
- **No emojis / non-ASCII** in anything that runs on AWS.
- **BUILD LADDER (Andrew-direct 2026-08-06):** before you write a line — YAGNI, then *does the estate already have it?* Run `comp-which` / `comp-find` first. Note `data/etfs/scripts/` already holds 9 py files and `portal/src/pages/Positioning/constants/etf-categories.ts` already exists.

## Half 2 — `ETFS-d-2`: THE `sub_asset_class` VOCABULARY ACT (a SEPARATE act, on purpose)

**This is its own cell and its own act because CLAUDE.md Rule 24 makes it one.** Minting `sub_asset_class` values is a **schema-enumeration act**, and Rule 24's 2026-08-20 widening is explicit: *"enumerating any type of schema requires rule 24 test"* — binding at **AUTHORING** time, including **proposing or adding values to an existing axis** and **adopting a schema authored elsewhere** (adoption IS an authoring act).

**Folded into Half 1 this becomes an implementation detail decided by whoever is writing the producer at the time — which is the exact axis-flattening propagation vector the widening was written against.** Keep it separate.

**DELIVER WITH THE VOCABULARY, or it is not a proposal:**
1. **The four-postulate record** — (i) MECE *(name the layer, then hunt the uncovered member)*, (ii) same grain, (iii) intent coherence (ONE intent per axis — do not mix asset-class taxonomy with display grouping), (iv) state coherence.
2. **A token-hygiene census** — word-boundary occupancy of each proposed value over the canon files. ⛔ **`comp-find` IS CASE-SENSITIVE BY DEFAULT and its denominator counts FILES SCANNED, never pattern coverage — run `comp-find -i` for any token census.** The dangerous failure is the **UNDERCOUNT**, not the zero: a partial case-miss returns a confident non-zero count with **no caveat at all** (measured: 7 vs 13, 46% missed).
3. **Check `comp-estate --definitions` FIRST** — a term you re-coin beside an existing ratified one is a duplicate (build-ladder rung 2, one layer up).

## Acceptance criteria — every criterion carries `cell_refs`

| id | criterion | cell_refs | grounding layer (Rule 22a) |
|---|---|---|---|
| **ETFS-TO1-AC1** | Producer exists, compiles, passes `.tools/commit-gate.sh`, committed under your author line via `safe-commit.sh` | `ETFS-d-1` | SOURCE |
| **ETFS-TO1-AC2** | Emits **all four books**; PFDE/PFOE **FULL** (weighted holdings + per-holding analytics), DIVZ/IDVZ **book-level SHELLS**. The shell path is **exercised**, not merely coded | `ETFS-d-1` | EXERCISED |
| **ETFS-TO1-AC3** | **Shells upgrade forward with NO code change** — proven by a run against a fixture carrying DIVZ/IDVZ constituent rows. **Sharpest test binds: if a code edit is needed to pick them up, ETFS-TO1-AC3 FAILS** | `ETFS-d-1` | EXERCISED |
| **ETFS-TO1-AC4** | A **SCHEDULE** exists and is the production trigger — not event-only, not ad-hoc. Quote the schedule expression | `ETFS-d-1` | APPLIED (`comp-trigger <name>` — scans events + scheduler with a printed denominator) |
| **ETFS-TO1-AC5** | ⛔ **PROOF RUNS ON THE FIRST SCHEDULED `bbg/{date}/` LANDING** (earliest 2026-08-22 07:00 local). **INDETERMINATE ANCHOR — no calendar date. The ad-hoc objects DO NOT satisfy this** | `ETFS-d-1`, `ETFS-a-5` | EXERCISED |
| **ETFS-TO1-AC6** | `sub_asset_class` vocabulary shipped WITH its four-postulate record + `-i` token census + `comp-estate --definitions` check | `ETFS-d-2` | DECLARATIVE |
| **ETFS-TO1-AC7** | **NO write lands under `daily/`, `platinum/`, `etf_history.csv`, or `silver/netassets_daily.parquet`** — ETFS_CANON's live territory, boundary (h). `platinum/etf_ownership_dashboard.json` was **rewritten today at 16:00:04Z**; a collision there is a live-product incident | `ETFS-a-7`, `ETFS-a-8` | APPLIED |

**ETFS-TO1-AC5 is deliberately not satisfiable today and that is CORRECT, not a defect.** Everything else is. **Do not hold ETFS-TO1-AC1..ETFS-TO1-AC4/ETFS-TO1-AC6/ETFS-TO1-AC7 waiting for it** — deliver them, report ETFS-TO1-AC5 as pending its observed anchor. *A dependent act dated off a projected prerequisite is the class that nearly deleted a working provenance path.*

## Surprise channel

`3.0.0_SA_CVO` owns it. Class `{OBSERVATION, BLOCKING}` × standing `{ARMED, INERT}`.
**OBSERVATION never interrupts** — one line to CVO, no action, keep working. **BLOCKING** (spec cannot physically execute) routes SAME-TURN to me as issuer, cc CVO. **ARMED** — whatever its class — needs a **named disarm owner SAME-TURN**; DISARMED ≠ REMEDIATED.
**Mid-round the spec is FROZEN. Do not adjudicate scope, redesign, or "improve" off-spec** — the cost of a wrong spec is a surprise item and a better round 2, not a mid-flight fork.

## Reporting

**STATUS MOVES WITH THE ACT, BY YOU, SAME TURN** — a proof-of-spec instance and its status flip are ONE atomic delivery. **Status is CELL-level** (`ETFS-d-1` and `ETFS-d-2` complete independently).
**EVERY REPORT OF A COMMIT STATES ITS PUSH STATE** (CTO ruling, today) — *"landed LOCAL @hash, rides integration"* or *"on origin/CLOUD @hash (ls-remote read)"*. **Never bare "landed."**
⛔ **Never compose a message reporting a completed act in the SAME tool call as the command that produces it. READ THE NUMBER, THEN WRITE THE SENTENCE.**
