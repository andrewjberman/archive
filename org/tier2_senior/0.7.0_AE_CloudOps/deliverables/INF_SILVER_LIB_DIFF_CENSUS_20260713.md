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
