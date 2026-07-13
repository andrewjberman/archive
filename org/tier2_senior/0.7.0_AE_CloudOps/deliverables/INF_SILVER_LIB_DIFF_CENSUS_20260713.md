# INF SILVER LIB -- DIFF CENSUS OF RECORD

**Author:** 0.7.0_AE_CloudOps~B · **Date:** 2026-07-13 · **Gate:** CTO-ratified (5 conditions)
**Status:** CENSUS COMPLETE. **NOTHING BUILT. NOTHING DEPLOYED. NO TERRAFORM TOUCHED. NO LEDGER OPENED**
(NEVER#6 binds a *deploy*; a census deploys nothing).

**Subject:** the DEPLOYED packages, pulled from Lambda via `get_function` -> presigned S3 -> unzip.
**Never the repo.** The whole finding this work rests on is that repo != runtime; a census of `data/`
would have re-committed the original sin.

---

## PRECONDITION -- both holds verified LIVE on the APPLIED plane before anything ran

| Hold | Plane | Evidence |
|---|---|---|
| `INF_GOLD_DISPATCH_HOLD` | **APPLIED** | `lambda get-function-configuration inf-gold-trigger` -> env var **SET** (full CTO+COO reason string), `INF_GOLD_DISPATCH_RELEASE` = **null**. LastMod 13:01:13Z. |
| Gold trigger rules | **APPLIED** | All 3 EventBridge rules targeting `inf-gold-trigger` = **DISABLED** (`inf-canonical-prices-daily`, `inf-gold-full-on-bronze-complete`, `inf-gold-incremental-daily`). |

Not a config read of the repo -- the live Lambda config and the live rule states. **The firebreak is real**,
which is the only reason this census was safe to run.

## DENOMINATOR (printed, per Rule 22)

```
24  inf-* lambdas enumerated (the full INF tree, not the 5 I was handed)
 5  CARRY a vendored copy of the silver lib and/or its converter
 0  UNRESOLVABLE            <-- a GAP would never have been recorded as a pass
```
**BOUNDARY, not a gap:** `bd`/`cot` copies are NOT censused -- NEVER#1 + the 49F sovereign hold. Out of
scope **by rule**, not unmeasured by accident.

---

## >> FINDING 0 -- THE MAP I WAS GIVEN WAS ALREADY WRONG. THE BUCKET PAID FOR ITSELF IMMEDIATELY. <<

| lambda | dispatch said | **MEASURED (deployed, now)** |
|---|---|---|
| `inf-accounts-v2-daily` | 397L lib | **495L** |
| `inf-silver-chain` | 397L lib | **495L** |
| `inf-api-positions` / `-reps` | 257L lib | **360L** |
| `inf-api-txn` | 257L lib | 257L (the only one that matched) |

Not an error by anyone -- those four were **redeployed today** (13:54Z / 15:26Z / 16:59Z) and the numbers
were taken before the deploys landed. **That is the entire thesis of this project, demonstrated on its own
briefing document.** A census of the map would have been wrong on 4 of 5 rows.

## FINDING 1 -- CANONICAL IS DEPLOYED NOWHERE

`data/` canonical: lib **595L** `sha=89ddfda0`, converter **1124L** `sha=e3e04af9`.
**Neither body exists in ANY of the 24 inf-* lambdas.** 3 distinct deployed lib bodies + 4 distinct deployed
converter bodies, and canonical is none of them.

**So the layer body would be code that has NEVER EXECUTED IN THIS RUNTIME.** That does not make it wrong --
but it means the canary is not a formality, it is the only thing standing between us and a simultaneous
behaviour change on four production writers.

## FINDING 2 -- THERE IS NO LIVE BEHAVIOURAL DRIFT LEFT. THE FORKS HAVE ALREADY CONVERGED.

Classifier: strip docstrings, compare **ASTs** (behaviour), cross with **reachability from `lambda_handler`**
(transitive call graph). Text/sha equality is not used for any verdict -- *it calls a docstring edit a defect
and a changed constant clean.*

| lambda | **BEHAVIOURAL + REACHABLE** | behavioural + inert | cosmetic | missing + reachable |
|---|---|---|---|---|
| `inf-api-txn` | **0** | 4 | 14 | 0 |
| `inf-api-positions` | **0** | 1 | 17 | 0 |
| `inf-api-reps` | **0** | 1 | 17 | 0 |
| `inf-accounts-v2-daily` | **0** | 0 | 21 | 0 |
| `inf-silver-chain` | **0** | 0 | 21 | 0 |

**ZERO behaviour-affecting reachable divergence anywhere.** Every reachable symbol is behaviourally identical
to canonical. `write_silver_api_dim_parquet` differs by **60L vs 52L -- eight lines of DOCSTRING**; the 0-row
guard body (`DIM_ALLOWS_EMPTY`, both `EmptyDimWriteError` raises) is **byte-identical** in canonical and in
all five deployed copies.

>> **THIS REFRAMES THE PROJECT. The layer is NOT fixing a live defect -- today's hand-fixes already closed
them. Its value is PREVENTIVE: stopping the NEXT desync. Nobody is bleeding. There is no clock, and now
there is a measured reason there is no clock.** <<

---

## >> FINDING 3 -- THE RISK REGISTER IS EXACTLY INVERTED. THIS IS THE DELIVERABLE. <<

The `inf-api-txn` exclusion rests on a causal claim (mine, in Q2; adopted as CTO's ruling):
> *"Handing it the canonical body CHANGES WHAT IS REACHABLE: a guard that has NEVER ONCE RUN starts running
> in production."*

**MEASURED, AND IT IS FALSE.** Counterfactual: substitute the canonical lib **and converter** into each
deployed package, rebuild the call graph, re-take the closure from `lambda_handler`, diff the reach sets.

```
inf-api-txn            reachable  7 -> 7    ACTIVATED: NONE
                       write_silver_api_dim_parquet  False -> False
                       apply_aua_guard               False -> False

inf-api-positions      reachable 13 -> 14   ACTIVATED: ['coerce_silver_ids']   <<<<<<
inf-api-reps           reachable 16 -> 17   ACTIVATED: ['coerce_silver_ids']   <<<<<<

inf-accounts-v2-daily  reachable 16 -> 16   ACTIVATED: NONE
inf-silver-chain       reachable  9 -> 9    ACTIVATED: NONE
```

**Reachability is driven by the HANDLER's call graph. txn's handler never enters those paths, and swapping
the body behind them changes nothing.** The hazard cited to exclude txn **does not exist on txn.**

**AND IT EXISTS ON THE TWO LAMBDAS NOBODY WAS WATCHING.** `coerce_silver_ids` is **absent from the
positions/reps forks and never runs today**. Consolidation makes the canonical converter call it and the
canonical lib define it -- so it **begins executing**, changing silver ID dtypes on two production writers.
**One of them is `positions_mv` -- the holdings book, a direct input to INF_B_00's served AUA.**

**Whether that activation is a FIX or a REGRESSION is not mine to rule** (Rule 14's `ds-precommit-check`
*mandates* `coerce_silver_ids` in silver code, so the forks lacking it may well be the drift). **But it is a
BEHAVIOUR CHANGE, and it would have shipped inside a change everyone -- me included -- believed was
behaviour-neutral.**

> **The same shape as the banked lesson, one level up: *"a census comparing CONSTANTS called the two dangerous
> Lambdas CLEAN and the inert one DIRTY -- exactly backwards."* It happened again, in the DESIGN OF THE GATE
> ITSELF, and only a measured counterfactual caught it.**

**THE DECISION MAY SURVIVE. THE REASON MUST NOT.** Excluding txn is still defensible -- it is not a writer,
it gains nothing from the layer, and you do not take risk for zero benefit. **But it must be excluded for
THAT reason.** A falsified mechanism left in the record is one somebody cites in a month -- exactly what the
INF hold record itself warns about (*"do not act on any mechanism you find quoted in an older brief"*).

---

## MY OWN INSTRUMENT FAILED FIRST. THE PROVEN-RED CASE CAUGHT IT.

**Census v1 FAILED.** It unioned call sites across every module, so a call inside the converter's dead code
counted as "called". It reported `write_silver_api_dim_parquet` **CALLED** in `inf-api-txn` -- the one Lambda
we *know* calls it zero times -- and returned **identical verdicts for txn and positions/reps**, the two it
exists to separate. **It could not discriminate, and by the pre-registered bar its verdicts on the other four
were worth nothing.**

v2+ computes a real transitive call graph from `lambda_handler` and passes: txn `reachable=False` on both
watched symbols, and it now *separates* txn from the other four.

**This is the proven-RED discipline working exactly as designed** -- and it is why `inf-api-txn` was the right
thing to demand. *A census with no known defect in it cannot be validated.*

### Honest bounds of the instrument (stated, not hidden)
- **Static only.** Dynamic dispatch (`getattr`, `globals()[...]`, `eval`) is invisible to it.
- **Name-based resolution.** Same-named functions in different modules are conflated.
- **It OVER-reports reachability** -- the SAFE direction: it can call an inert symbol live, never a live
  symbol inert. So `ACTIVATED: NONE` on txn is the *strong* direction of this instrument's error.
- **Not exercised.** Every verdict here is static analysis of a deployed artifact. **It is not a runtime
  observation, and I am not calling it one.**

---

## RECOMMENDATION (a recommendation, not a decision)

1. **Consolidate `inf-accounts-v2-daily` + `inf-silver-chain` first.** Zero reachable behavioural divergence
   AND zero counterfactual activation. **They are the measured-safe set.** Canary = `inf-silver-chain`
   (lowest blast radius; not the holdings book).
2. **`inf-api-positions` + `inf-api-reps` are NOT in the safe set.** They carry a live `coerce_silver_ids`
   activation. **They need a DS ruling on whether coercion is correct for those dims, and an exercised
   verify -- not a consolidation.**
3. **`inf-api-txn` stays excluded -- REASON CORRECTED.** Not "it would activate dead code" (false). Rather:
   **it is not a writer, it gains nothing, and consolidation is risk for zero benefit.** Document the
   exception AT THE DIVERGENCE POINT so the next person does not "fix" it.
4. Conditions 5 + 6 stand and are unaffected: **delete the vendored copy in the same deploy that attaches the
   layer** (`/var/task` shadows `/opt/python`), **assert `__file__` resolves under `/opt/python`** plus a
   layer-only build marker, and **assert the layer ARN + version pin per function, post-apply, on the LIVE
   config.**

**Nothing is built until this is read.** Per CTO: *"If the census is all you get done this window, that is a
complete and useful deliverable -- it converts '6 copies, 4 versions' from a fog into a decision."*

## Compiler Tools

| Tool | Result | Note |
|---|---|---|
| `aws lambda get-function` (x24, deployed packages) | PASS | the subject of the census; presigned-URL download + unzip. Denominator printed, 0 unresolvable. |
| `aws lambda get-function-configuration` / `events describe-rule` | PASS | APPLIED-plane hold verification (Rule 22a) -- not a repo read. |
| raw `grep` (canonical lib location, hold token) | rail-checked | no comp-tool models a vendored lib's file identity or a hold flag's live value; marked inline. |
| **census v1 (own build)** | **FAIL -> the finding** | failed its own proven-RED case. Presence-of-call-site, not reachability. Replaced. |
| census v2-v5 (own build) | PASS | handler-rooted call graph; AST behavioural equivalence; full-scope counterfactual. |

**What worked:** the proven-RED case caught my own broken instrument on the first run. **What failed:** census
v1 -- and it failed in exactly the way the dispatch warned it would. **Gap found:** the gate's own txn
exclusion rests on a mechanism that measurement falsifies, and the hazard it names is real on two *other*
lambdas.

---

## FOLLOW-ON (FILED, NOT STARTED) -- THE BETTER DISPOSITION FOR `inf-api-txn`: DELETE THE TWO FILES IT NEVER IMPORTS

**Status: FILED. Do NOT start it. Owner: unassigned. No clock.**

The census's handler finding is bigger than the exception note it produced. `inf-api-txn/lambda_function.py`
imports **neither** `_orion_api_silver_lib` **nor** `convert_orion_api_to_silver` -- and has not since
`ADVI_TXNAMG.004` (2026-05-15) removed the silver/transactions write. **Both files nevertheless still ship
inside the production deployment package.** That is not merely *consistent* with the measured reach set of
7 -> 7 -- **it is the MECHANISM of it.**

So the right long-term disposition is **not "excluded forever, with a note."** It is **delete the dead files**:

| what it removes | how |
|---|---|
| the fork | one fewer copy of the silver lib in the estate |
| the comp-constants drift | the file carrying the weakened 50M-400M band ceases to exist |
| the gate block | permanently -- **without touching a single constant** |
| the exception note | unnecessary: **you cannot consolidate a file that is not there** |
| vestigial baggage | dead weight shipped in a production package since 2026-05-15 |

> ## **STRUCTURE BEATS ASSERTION. Rather than documenting an exception forever, REMOVE THE THING THE EXCEPTION IS ABOUT.**
> *A note saying "do not consolidate this fork" is a comment -- a claim with no vintage and no test. **A deleted
> file cannot be consolidated.*** Today taught us what comments are worth; this is the structural version of the
> same fix.

**BAR BEFORE ANYONE TOUCHES IT (it is a package change to a LIVE production Lambda, and it gets the same bar as
everything else):**
1. **Download the DEPLOYED package** and prove the handler imports neither file **in the bytes that actually run**
   -- not in the repo.
2. **EXERCISE** the Lambda after removal. **A static reach set is not a runtime observation, and I said so:** this
   census's instrument **OVER-reports** reachability, so *"not reachable"* is the **strong** direction of its
   error -- which is what makes this **promising, not proven.**
3. Terraform-only, coordinate with CTO~B, ledger at the apply.

**It is promising precisely because the instrument's bias runs the safe way. It is not proven, and nothing here
authorizes the deletion.**

---
---

# >> CORRECTION -- 2026-07-13, 18:00Z. THE VERDICT ABOVE IS WRONG, AND SO IS THE PREMISE OF THE PROJECT. <<

**This correction is appended, not merged into the text above.** The original verdict was ACCEPTED by base-AE
and ratified by CTO~B. **A record that was accepted and then silently improved teaches nobody.** Read the
original, then read why it failed.

## WHAT THE CENSUS SAID
> **FINDING 2: "ZERO behaviour-affecting reachable divergence anywhere."** (all five lambdas, headline verdict)

## IT IS FALSE. AND THE CENSUS COULD NOT HAVE SEEN OTHERWISE.

```
POSITIONS_BRONZE_KEY_TPL        (a MODULE-LEVEL CONSTANT in convert_orion_api_to_silver.py)
  DEPLOYED FORKS (running now):  'bronze/positions/{snap}.parquet'      <- CORRECT
  CANONICAL   (the LAYER BODY):  'bronze/positions/{snap}.jsonl.gz'     <- *** STALE ***
```
**GROUND TRUTH, live S3, denominator printed** -- `s3://opal-data-inf/bronze/positions/`, 4,537 objects
(2,272 `.parquet` / 2,265 `.jsonl.gz`):

| date | written |
|---|---|
| 2026-07-08 | `.parquet` |
| 2026-07-09 | `.parquet` + `.jsonl.gz` |
| **2026-07-10** | `.parquet` + `.jsonl.gz` -- **THE LAST `.jsonl.gz` EVER WRITTEN** |
| 2026-07-11 | `.parquet` **only** |
| 2026-07-12 | `.parquet` **only** |
| 2026-07-13 | `.parquet` **only** (today) |

**Attaching the layer would re-point the positions bronze read at a key that has not been written for three
days.** The holdings book's source.

## >> AND IT FALSIFIES THE PREMISE OF THE ENTIRE CONSOLIDATION, NOT JUST THIS APPLY <<

> ## **CANONICAL IS THE STALE ONE. THE FORKS ARE NOT BEHIND -- THEY ARE AHEAD.**

Every argument for this project rested on *"there is ONE artifact to be in parity WITH."* **That artifact is
wrong about the holdings book's source key.** This is the *"forks may differ for a REASON"* warning landing
exactly: **the runtime moved forward and `data/` did not.**

**The consolidation is still right as a GOAL. Its METHOD -- collapse everything onto canonical -- IS DEAD.**
**Ruling (CTO~B, 2026-07-13): the consolidation proceeds ONLY on a per-divergence DISPOSITION -- every
difference adjudicated, the winning side NAMED and JUSTIFIED. CANONICAL GETS NO PRESUMPTION.**

## WHY MY INSTRUMENT WAS BLIND -- and this is the transferable part

My v4 classifier compared **function bodies** (AST, docstrings stripped) crossed with **reachability from the
handler**. **A MODULE-LEVEL CONSTANT IS NOT A FUNCTION BODY.**

> ## **THE CODE IS IDENTICAL. THE CALL GRAPH IS IDENTICAL. THE REACH SET IS IDENTICAL. IT READS A DIFFERENT FILE.**
> ## **A CONSTANT THAT NAMES A DATA SOURCE IS THE MOST CONSEQUENTIAL LINE IN THE FILE -- AND IT IS INVISIBLE TO EVERY CENSUS THAT DEFINES "BEHAVIOUR" AS *CODE THAT RUNS*.**

**My census only ever asked ONE of the three questions a change-analysis must ask:**

| question | did I ask it? |
|---|---|
| **What will newly EXECUTE?** | YES -- and it found `coerce_silver_ids`. |
| **What will STOP executing?** | **NO** (computed, never reported -- see the reporting defect below). |
| **What will now be READ FROM SOMEWHERE ELSE?** | **NO. This is the one that would have broken the holdings book.** |

**A DATA PIPELINE CAN BE DESTROYED WITHOUT A SINGLE NEW LINE RUNNING.**

## THE OTHER DIVERGENCES THE SOURCE DIFF FOUND (all four targets)

| divergence | disposition |
|---|---|
| `POSITIONS_BRONZE_KEY_TPL` `.parquet` -> `.jsonl.gz` | **FORK WINS. Canonical is stale.** `data/` needs the fix, not the Lambdas. |
| `+ _DIM_DEFER_GUARD = {'performance': ...}` | **UNDISPOSED** -- a defer guard the forks do not have. New behaviour. Needs a ruling. |
| `+ CW_NAMESPACE='Inflection/GoldChain'` `CW_SERVICE='inf-gold-layer-runner'` | **REFUSED.** The **silver** lambdas would emit CloudWatch metrics **identifying themselves as the gold-chain runner -- DURING THE GOLD-CHAIN FREEZE.** An agent checking whether the hold is working would see gold-chain telemetry flowing and conclude the chokepoint had **FAILED** -- and the remedy for a failed safety control is **DESTRUCTIVE**. *It would have corrupted the observability of the very control we built today.* |
| `- LOCAL_BRONZE_API_DIR` / `- LOCAL_SILVER_API_DIMS_DIR` (positions fork) | UNDISPOSED -- canonical re-adds them. |

## A. DEACTIVATED SET -- MEASURED, EXPLICITLY, ALL FOUR: **NONE**

**And a reporting defect of my own, recorded rather than quietly fixed:** I *had* computed this in v5
(`before - after`) but only **printed it when non-empty**. So in the original report **"I measured zero" and
"I did not look" SHARED A SIGNATURE** -- against my own stated bar, *in the same document where I stated it*.

> **Absence-of-data and failure-to-read must never share a signature.** *Print the zero. A silent field is
> indistinguishable from an unasked question.*

## WHAT ACTUALLY CAUGHT THIS -- and it was not the instrument

**Not my census. The HOLD.** Base-AE stopped the canary and forced the two mirror questions I had never asked.
At the moment it was caught I had **FOUR GREENS**: a CTO-ratified gate, an exec-cleared Terraform window, my
own accepted census, and a DS ruling. **Nobody was wrong. The instrument was.**

**STATUS: CANARY HELD. Nothing applied, no Terraform, no layer, no ledger. No clock -- there is no live drift,
nothing is bleeding, and the layer is PREVENTIVE, not remedial.**

---

# CENSUS v7 -- THE REBUILT CLASSIFIER + THE PER-DIVERGENCE DISPOSITION

**Scope added:** module-level constants · path/key literals · bucket/prefix/dim names · the two mirror
questions (**what STOPS**, **what is READ FROM ELSEWHERE**).

**PROVEN-RED CASE (asserted before any verdict is trusted): `POSITIONS_BRONZE_KEY_TPL`.** The script exits 2
if it does not fire. **It FIRED** -- the rebuilt classifier sees the line v4 was blind to, so its verdicts are
admissible. *(Same bar `inf-api-txn` was for v2 -- which v1 failed.)*

## THE DISPOSITION -- canonical gets NO presumption (CTO~B ruling)

Identical divergence set across all four targets.

| # | divergence | disposition | why |
|---|---|---|---|
| 1 | **`POSITIONS_BRONZE_KEY_TPL`** fork `.parquet` / canonical `.jsonl.gz` | **>> FORK WINS. HARD BLOCKER. <<** | The producer has written `.parquet` **only** since 2026-07-10. **Canonical reads a key dead for three days.** The fix belongs in `data/`, not in the Lambdas. **Routed to DS.** |
| 2 | **`+ CW_NAMESPACE='Inflection/GoldChain'`** · **`+ CW_SERVICE='inf-gold-layer-runner'`** (`_orion_api_silver_lib.py:499-500`, emitted at `:511`) | **>> REFUSED. <<** | The **silver** Lambdas would emit CloudWatch metrics **identifying themselves as the gold-chain runner, during the gold-chain FREEZE.** An agent auditing whether the hold is working would see gold telemetry, conclude the chokepoint **FAILED**, and reach for a **destructive** remedy. *It poisons the instrument that answers the one question the hold exists to answer.* (Alternative outcome, if the namespace is IAM-scoped to the runner role: a denied emit spraying errors. Both bad; **neither visible in a reach set.**) |
| 3 | `+ _DIM_DEFER_GUARD = {'performance': (...)}` | **UNDISPOSED** | A defer guard the forks do not have. New behaviour. Needs a ruling before it ships. |
| 4 | `+ _FIPS_TO_USPS` | **CANONICAL WINS** | A pure FIPS->state lookup table. No source implication, no behaviour risk. |
| 5 | `LOCAL_BRONZE_API_DIR` / `LOCAL_SILVER_API_DIMS_DIR` | **CANONICAL WINS** | fork hardcodes literals; canonical **resolves them dynamically** (`_resolve_local_bronze_dir()` / `_resolve_local_silver_dims_dir()`, handling EC2 / local-dev / env-override). Strictly better. **The handler's `/tmp` monkeypatch (`lambda_function.py:78`) still governs -- it assigns the module attribute AFTER import.** Not a break. |

## >> AND ROW 5 IS A THIRD HOLE IN MY OWN INSTRUMENT -- A FALSE POSITIVE, CAUGHT BEFORE IT SHIPPED <<

v7 first reported rows 5 as **"canonical would REMOVE these two constants"** -- which, given
`lambda_function.py` monkeypatches one of them and the converter reads the other **four times**, reads as a
**hard break: the layer kills positions and reps at import.** I was one message away from reporting it.

**IT IS FALSE. Canonical defines both.**
```
CANONICAL  :66  LOCAL_BRONZE_API_DIR      = _resolve_local_bronze_dir()        <- a CALL
           :105 LOCAL_SILVER_API_DIMS_DIR = _resolve_local_silver_dims_dir()   <- a CALL
FORK       :57  LOCAL_BRONZE_API_DIR      = 'data/inf/manual_api/pulls'        <- a LITERAL
           :58  LOCAL_SILVER_API_DIMS_DIR = 'data/inf/silver/api_dims'         <- a LITERAL
```
**My extractor used `ast.literal_eval` and silently `continue`d on any non-literal value. A constant COMPUTED
BY A FUNCTION CALL WAS INVISIBLE TO IT -- so it reported the name as ABSENT from canonical.**

> ## **A FALSE FAIL IS MORE DANGEROUS THAN A FALSE PASS, BECAUSE ITS REMEDY IS DESTRUCTIVE.**
> Had I shipped it: *"positions/reps cannot take the layer -- it breaks them at import."* **Wrong, and it would
> have killed a correct change.** *Caught only because I grounded the claim at source before reporting it --
> the same rule that caught everything else today.*

**Third instrument hole found in my own work today** (v1: presence-not-reachability · v4: blind to module
constants · v7: blind to computed constants). **All three self-reported. The pattern is not that the
instruments are bad -- it is that EVERY instrument is blind to something, and the only defence is to ground
the claim at source before you act on it.**

## THE VERDICT

**THE CANARY CANNOT PROCEED AS DESIGNED.** Not because of a process failure -- because **the layer body is
wrong** in two independent ways, one of which (row 1) would break the holdings book's bronze read and one of
which (row 2) would corrupt the observability of the gold-chain hold.

**REQUIRED BEFORE ANY LAYER SHIPS:**
1. **`data/` is FIXED** -- `POSITIONS_BRONZE_KEY_TPL` -> `.parquet`. **DS's call, not mine.** *(And check: if
   anything currently executes the canonical converter, IT IS READING A DEAD KEY TODAY. Possible live defect
   in `data/`. Routed, not chased.)*
2. **The CW namespace/service is resolved** -- the layer must NOT make silver Lambdas emit as the gold-chain
   runner. Parameterise per-consumer, or strip it from the shared body.
3. **`_DIM_DEFER_GUARD` is disposed.**
4. Only then: re-plan the canary.

**NOTHING APPLIED. No Terraform, no layer, no ledger. NO CLOCK -- zero live drift, nothing bleeding, the layer
is PREVENTIVE.**
