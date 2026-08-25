# SPEC — COTTONWOOD "CLIENT - OPAL SUPERVISED": WHAT HAS TO HAPPEN

**Author:** `0.4.0_DS_ClientPlatform~F` · **Requested by:** Andrew, 2026-08-25 ~05:3xZ, at this terminal.
**Status:** SPEC / PROPOSAL. Not a registration, not a self-assignment. Input to Rule 27
stage 1–2 for whoever registers it.
**Every figure below is measured; vintages stated. Nothing here is estimated.**

---

## 1. THE GOAL, IN HIS WORDS

> *"You just check the Accounts that come in via the Rebalancer pulls on Black Diamond. If there is
> an 'Opal-' constituent model included in any of those portfolios, the remaining balance of that
> account is 'Client - Opal Supervised'."*

Display labels, his ruling: **`Client - Opal Supervised`** / **`Client - Opal Unsupervised`** — the
perspective sits in the name, because "Supervised" alone has two referents (Cottonwood's, = the
whole 458M; Opal's, = the derived residual) and that ambiguity has already produced one $302.6M
misclassification at this lane.

**THE MECHANISM EXISTS AND IS IDENTIFIED.** `silver/fact_model_definition` carries model
constituents (`model_name`, `sleeve_name`, `component_name`, `symbol`, `absolute_allocation`,
`relative_allocation`). `sleeve_name` IS the Opal constituent — measured values include
`Opal Intermediate-Term` (200 rows), `Opal Conservative Growth` (144), `Opal Short-Term` (128),
`Opal Ultra Short-Term Income` (126), `Opal Long-Term Aggressive` (48).

**THE PREDICATE IS NOT COMPUTABLE TODAY.** Two independent upstream gaps, below.

---

## 2. GAP A — THE REBALANCER MODEL-DETAIL PULL IS PARTIAL (**this is the blocker**)

### Measured (2026-08-24 partition)
| | |
|---|---|
| models in `fact_model_roster` | **64** |
| models in `fact_model_definition` | **30** |
| **models with NO constituent data** | **42** |
| files in `bronze/rebalancer_model_detail/2026-08-24/` | **30** |
| `Anna *9237` (`1ae61190-70fb-4d6c-a259-cee9019ed125`) | **NOT PULLED** |
| `Anna *9238` (`6ae9e540-9b27-474c-8ad9-3dfc5131c530`) | **NOT PULLED** |

### Classification — **INGEST GAP, NOT A BUILD BUG**
Bronze holds one JSON per model_id and contains only 30. Silver converts all 30 faithfully. **Nothing
downstream drops anything; the detail was never fetched.** An ingest gap and a silver-build bug take
opposite remedies, so this is stated before any repair.

### Why it is the blocker, and why "fix Anna" is the wrong repair
The 42 unpulled models include both Anna strategies **and the entire `Core | Satellite`
30/40/50/60/70/80/90/98 family**, `Core / Satellite Equity`, the CA Tax-Free variants, the 529-F2
American Funds series, `CSTF40 Conservative G&I - Gillham`, `CSTF50 Moderate G&I - Harris`.
**`Core | Satellite` is exactly the shape that carries Opal sleeves** — the pulled Opal models have
that structure. Any of the **492** accounts currently classified Opal-Unsupervised may be assigned to
one of the 42. **The error is not the $46,436,739.80 of Anna; it is unbounded.** Patching the two
accounts Andrew happened to name would convert a visible systematic gap into an invisible residual
one on a client-facing fee line.

### ⛔ NOT LOCATED, AND NOT GUESSED
The **writer** of `bronze/rebalancer_model_detail` is not in `data/**` or `infra/aws/lambda/**` under
any name found (only the bronze→silver `rebalancer_conversion.py` is). Likely an EC2 collector.
**FIRST ACT: open that writer and state the selection rule before proposing a remedy.**

### HYPOTHESIS — flagged, NOT a finding, needs the writer read
Every parent carrying an Opal component in `fact_model_definition` is itself `is_opal = True`. **If
the pull selects models by Opal name or flag, it is circular** — detail is fetched only for models
already believed Opal, so an Opal sleeve inside a non-Opal-named model can never be discovered.
That is `build_dim_model_portfolio.attributes():275`'s disjunction one layer up: the code was fixed
to attribute Opal children of non-Opal-named parents, **and the data required to see them is never
pulled.** Anna is the specimen. **Source-confirm before acting.**

### Acceptance criteria
- **A1** The selection rule in the bronze writer is READ and STATED at `file:line @commit`, and the
  42 absences are classified as *deliberate* or *defect*. A count is not a classification.
- **A2** `bronze/rebalancer_model_detail/{date}/` file count == the roster's model count, **or** every
  excluded model is enumerated with its reason. **A silently partial pull is the defect.**
- **A3** `fact_model_definition` covers every roster model on the same date; the two Anna model_ids
  resolve with their constituents present.
- **A4** The pull EMITS ITS OWN DENOMINATOR (`fetched N of M roster models`) so a future partial pull
  is visible without a cross-table census. **This is what would have surfaced it in June.**

---

## 3. GAP B — THE `fact_holdings` PRODUCER STOPPED (already owned; stated for sequencing)

`PATH A` `opal-data-assets/blackdiamond/cottonwood/silver/fact_holdings/` — last partition
**2026-08-19**. `PATH B` `opal-data-cot/silver/holdings/` — **08-20 and 08-21 present**.
`build_dim_model_portfolio.py:73` reads PATH A; `:66` records the value source **moved there from
PATH B**. **The data is in the path we moved away from and absent from the one we moved to** —
migration-shaped: restart/backfill A's producer, or repoint. A decision, not a fix.
Adjacent tables in the SAME tree (`roster`, `blend`, `assignment`, `model_definition`) run to 08-24:
**one table's producer, not the tree and not the firm.**
**Silent-success:** `latest_holdings_date(s3, on_or_before=…)` at `:116` falls back to the newest
partition at-or-before the assignment date, so the artifact emits `value_date=2026-08-19` against
`assignment_date=2026-08-24` **and does not error.**
**Owned:** `ADVI_COTETL` per CTO. **Blocks:** the Models ↔ Client boundary at his canonical date only.
**Acceptance:** assert the **VALUE DATE**, not that the artifact built.

---

## 4. THE PREDICATE — buildable once GAP A closes

**Definition.** For each account in the Rebalancer pull: if its assigned portfolio contains an Opal
constituent model (via `fact_model_definition.sleeve_name` / `component_name`), then that account's
**non-Opal-model balance** is `Client - Opal Supervised`. Every other supervised account's balance is
`Client - Opal Unsupervised`. Held-away (Black Diamond `account_supervised = Unsupervised`,
**$30,322,927.42** @08-19) is excluded from **every** Cottonwood figure.

### Acceptance criteria
- **P1** All **819** Black-Diamond-supervised accounts classified, **0 undeterminable**, denominator
  printed. An account assigned to a model with no constituent data is UNDETERMINABLE, never a
  default to Unsupervised — **defaulting is the exact defect this spec exists to fix.**
- **P2** `Anna *9237` and `Anna *9238` land in `Client - Opal Supervised` — the named specimen, and
  the regression test.
- **P3** `Models + Client-Opal-Supervised + Client-Opal-Unsupervised == Cottonwood-supervised total`
  to the cent, at ONE vintage, with the vintage on the artifact.
- **P4** Every figure struck at a **single** date. The `458,053,742.19` total is 08-21; the model
  attribution is 08-19 until GAP B closes. **No cross-vintage subtraction** — that produced a
  retracted, ratified error at this lane tonight.

---

## 5. SEQUENCING

```
GAP A (pull)  ─┐
               ├─→  PREDICATE (§4)  ─→  COT EMIT at 458,053,742.19
GAP B (holdings) ─┘
```
**A and B are independent of each other and BOTH gate the predicate.** A gates *who* is supervised;
B gates *at what date* the Models boundary can be struck. Closing one alone does not unblock the
emit — **and either alone will look like progress.**

---

## 6. NOT IN SCOPE
Ruled and awaiting execution elsewhere, deliberately excluded so this spec is not read as
re-litigating them: the D1 all-scope enum flip; the Call 2 supersession (Moderate Income + 15/85 as
Custom Models); `49financial` and `inflection` Client L1 (landed `@4ebad3642a`, flat assertions with
no predicate dependency); the `COT_CANON458` artifact sweep.

## 7. WHAT IS ALREADY TRUE AND NEEDS NO WORK
Cottonwood-supervised total **458,053,742.19** @08-21 — reproduces Black Diamond's own dashboard to
**$0.19**, with three of four portfolio-group rows tying to the cent and the fourth explained by
`D_05`'s documented pair-grain double-booking. Held-away exclusion **$30,322,927.42**. The filter
basis is source-confirmed from Black Diamond's bundle: `supervisedFilterType: 2` (Supervised) ×
`billableFilterType: 1` (All Assets).

---

# 8. ANDREW 2026-08-25 ~05:4xZ — "BACKFILL OR NEW PIPELINE?" AND THE SELF-HEALING DESIGN

## VERBATIM

> Is this just a backfill issue or do we need a whole new pipeline built out/expanded for rebalancer?
>
> What should effectively happen is that the pipeline should be self-healing. When a new Opal Model
> appears in one of these portfolios, the balance of that portfolio is moved over to "Client - Opal
> Supervised"
>
> Every day when the data is pulled, there needs to be a scan if there is any new ones
>
> THat is the loose idea

## ANSWER: **EXPANSION, NOT A NEW PIPELINE. AND NOT A BACKFILL.**

**NOT a new pipeline.** Every component already exists and runs daily: the bronze feed
(`bronze/rebalancer_model_detail/{date}/{model_id}.json`), the converter
(`rebalancer_conversion.py`, `_DETAIL_RE` at `:57`), the silver table
(`fact_model_definition`, 11 columns incl. `sleeve_name` / `component_name` / allocations), and the
daily schedule that produced 30 files at 02:00:4x on 08-24. **What is wrong is COVERAGE — 30 of 64
models — not capability.** Nothing needs building that does not exist.

**NOT (only) a backfill, and this is the load-bearing half.** A backfill fixes *today* and the pull
re-breaks *tomorrow*: if the writer's selection rule is what produced 30 of 64, it will produce a
partial set again on the next run, and the next model Cottonwood creates lands outside it. **A
backfill would restore the number and leave the mechanism that lost it.** Backfill is OPTIONAL and
separate — needed only if the historical timeseries must be restated, which is its own decision.

## ⛔ HIS SELF-HEALING REQUIREMENT CHANGES THE ARCHITECTURE, AND IT IS THE BETTER ONE

> *"the pipeline should be self-healing. When a new Opal Model appears in one of these portfolios,
> the balance of that portfolio is moved over to Client - Opal Supervised"*

**READ PRECISELY: this is DERIVE-DAILY, not DETECT-AND-NOTIFY.** Membership is not a stored list
that drifts and needs reconciling — it is **recomputed from the constituent data on every run**. A
new Opal model appearing in a portfolio then requires **no detection at all**; the next day's
derivation simply places that balance in `Client - Opal Supervised` because the constituent is there.
**Correct by construction, with nothing to notice.**

This is the opposite of the hand-map pattern that has cost this project repeatedly (the
`CANONICAL_KEY` LOUD-guard failures, the `PENDING_RULING` entries, the 15/85 that needed a ruling to
enter a map). **A derived membership has no map to fall out of date.**

## WHAT ACTUALLY NEEDS A DAILY CHECK — AND IT IS NOT THE MODELS

If membership is derived daily, **the models need no scan.** The one thing that *does* need checking
is **COVERAGE OF THE PULL**, because a partial pull silently produces *confidently wrong*
membership — an account whose model was not fetched derives as Opal-Unsupervised and looks
classified. **That is exactly today's defect, and it is invisible without the check.**

⛔ **AND IT IS A PRODUCER ASSERT, NOT A MONITOR.** The standing moratorium bans building alerts,
notifiers and freshness checkers as deliverables. This is the sanctioned shape instead: the pull
**counts what it fetched against the roster and REFUSES / RAISES on a shortfall**, naming the missing
model_ids — the same shape as this lane's `Insurance == 0` emit guard and the registry's F5. It fails
the run loudly rather than notifying anyone, and there is nothing to subscribe to. **No SNS, no SES,
no `*-monitor`.**

## REVISED ACCEPTANCE — replaces §2 A2/A4 and adds S1–S3

- **A2′** The pull fetches detail for **every** roster model, or refuses the run naming each excluded
  model_id and its reason. **A silently partial pull is the defect, not the shortfall itself.**
- **A4′** The pull prints `fetched N of M roster models` on every run. **Denominator on the artifact,
  not in a dashboard.**
- **S1 — DERIVED, NOT STORED.** Opal-supervision membership is recomputed each run from
  `fact_model_definition`. **No hand map, no membership table, nothing to fall out of date.**
  EXERCISE: add a fixture model carrying an Opal sleeve → the next derivation moves that portfolio to
  `Client - Opal Supervised` **with zero code and zero registry edits.** That test IS the
  self-healing requirement; if it needs an edit, the design has failed.
- **S2 — UNDETERMINABLE IS A STATE, NOT A DEFAULT.** An account whose model has no constituent data
  derives as **UNDETERMINABLE** and is counted, never silently Unsupervised. Today that is **42
  models**; the target is **0**, and the number is printed either way. **A default here is what put
  the firm's two largest accounts on the wrong side of a fee line.**
- **S3 — NO NEW SCHEDULE.** The daily Rebalancer pull already runs (02:00:4x observed 08-24). The
  coverage assert rides **inside** it. Per the standing rule, a production pipeline has a schedule —
  this one has one, and nothing new is scheduled.

## SEQUENCE, REVISED

1. **READ THE WRITER'S SELECTION RULE** (still not located; likely an EC2 collector). Everything
   below depends on whether 30-of-64 is deliberate or a defect, and **that is one read.**
2. **EXPAND COVERAGE** to all roster models + the refuse-on-shortfall assert (**A2′/A4′**).
3. **DERIVE THE PREDICATE DAILY** from `fact_model_definition` (**S1/S2**).
4. **BACKFILL — SEPARATE DECISION**, only if the historical series must be restated. Not required for
   a current-state display taxonomy, and **it must not be done before step 2** or it re-breaks on the
   next run.
