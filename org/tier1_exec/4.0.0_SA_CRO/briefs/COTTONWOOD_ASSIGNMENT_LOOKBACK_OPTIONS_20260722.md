# Cottonwood Historical Model-Assignment — Option Set

**Author / owning agent:** `4.0.0_SA_CRO` — Chief Research Officer · **Date:** 2026-07-22
**Commissioned:** Andrew-direct ~1740Z (*"we surely can figure out how to get lookback for this"*), routed via
`1.0.0_SA_CTO`; **Andrew confirmed the ask directly to me before I acted** — the relay was an assertion and
`send_message` has no sender auth, so it was verified out-of-band rather than assumed.
**Egress used: NONE.** Every finding below comes from templates, captures, and S3 data we already hold.
**Route:** `1.0.0_SA_CTO` → Andrew.

> **THE TWO CONSTRAINTS, held throughout:**
> **1. Nothing that fabricates.** Every option below is graded on whether it can **distinguish *what it was*
> from *what it is***. The option that cannot is named and ruled out (§5.1).
> **2. No new wire.** Nothing here was probed live. Where an option needs a call, it says so and stops.

---

## AMENDMENT — 2026-07-22, Andrew-direct, AFTER this brief was written. Read this before §1.

**Andrew, verbatim:** *"Cottonwood does not have full lookback yet because they are in the process of
migrating their data to Black Diamond, so I would not get too indebted to what they have or don't have yet.
Our goal is just to get whatever we have access to cleanly and explainably."*

**This reframes the problem and I am recording it rather than silently rewriting the brief.**

**WHAT CHANGES — the premise.** I wrote this as *"the history exists somewhere; find the path to it."* The
actual situation is that **Cottonwood is mid-migration INTO Black Diamond.** The absent history is therefore
**neither a BD platform limitation nor a Cottonwood data defect — it is a migration in progress.** Much of
what is missing today is expected to arrive on its own.

**WHAT THAT INVALIDATES:**
- **§7's ceiling was right for the wrong reason.** I attributed it to our ingest horizons plus BD retention.
  The actual binding constraint is **how far Cottonwood's migration has progressed** — which is a moving
  target, not a fixed wall, and **not ours to measure from the outside.**
- **Option 4.5 (vendor conversation) drops from "hold" to actively counterproductive for now.** Asking Black
  Diamond to supply historical assignment for a tenant *currently migrating into* Black Diamond is asking for
  something that does not exist there yet. It would spend a vendor conversation on a question the migration is
  already answering.
- **Options 4.3 / 4.4 (capture walks for a BD historical-assignment surface) drop in priority.** A surface
  that returns history BD does not yet hold returns nothing useful.

**WHAT SURVIVES, and why it survives INTACT:**
- **4.1 + 4.2 (re-select the account-level dimension; run the never-run template dump) stand unchanged** —
  because they were never "reconstruction." They are *"select the field we should have been selecting and
  read what is actually there."* That is exactly **"get whatever we have access to, cleanly."**
- **§3's temporal-vs-current probe becomes MORE important, not less.** If BD stamps *current* assignment onto
  historical rows, and we backfill from it **while real history is still migrating in**, we would be
  manufacturing a series that the migration later contradicts — **creating a reconciliation problem of our own
  making, against ground truth that is still arriving.** The probe is the gate that prevents that.

**A THIRD CONSTRAINT, now binding, which the original brief did not carry:**

> **3. WHATEVER WE BUILD MUST BE ADDITIVE AND NON-CONFLICTING WITH DATA THAT ARRIVES LATER.**
> No synthesized rows, no frozen backfill, no hardcoded series start. The series must simply **extend
> backwards on its own as the migration lands more history.** Anything that writes a value where real data
> will later appear is a future contradiction we authored ourselves.

**THE OBJECTIVE, RESTATED in Andrew's terms:** not *"obtain lookback."* It is **"represent exactly what we
have, honestly labelled, in a way that grows by itself."** A short, true, self-extending series is the
deliverable. **Do not get indebted to what Cottonwood has or does not have today.**

**PRACTICAL CONSEQUENCE FOR THE PRODUCT:** rendering Cottonwood from its true first date with the start
honestly labelled is **already a correct answer** — not a placeholder for a better one. The work worth doing
is the cheap, non-committal part (4.2 then 4.1) that makes "whatever we have" as complete and as explainable
as it can be, and then **letting it grow.**

---

## 1. Headline — the most promising path is one we already own, aimed one level off

**Black Diamond's DataMining templates already carry model-assignment dimensions, and one of them is already
selected and already flowing into our silver — but at the WRONG LEVEL.**

| Table | Assignment dimensions in the template | Selected? |
|---|---|---|
| **transactions** (qt2) | `Portfolio Strategy ID/Name` → `portfolioRebalStrategyID/Name` | **YES — selected, 63/63 dims** |
| **realized** (qt3) | **Account** Strategy ID/Name, **`Account Rebal Assignment ID`**, Account Program ID/Name, Manager Strategy, Investment Strategy Name — *plus* the Portfolio-level set | **NO** — available, `isEnabled: True`, 9/209 selected |
| **unrealized** (qt4) | same 13 dimensions as realized | **NO** — available, `isEnabled: True`, 8/208 selected |
| allocations (qt5) | Account/Investment/Manager Strategy | thin envelope locally |
| holdings (qt1) | — | thin envelope locally (server-side; §5.4) |

**Measured in our own silver:** `silver/transactions/*.parquet` carries `portfolio_strategy_id` and
`portfolio_strategy_name` (71 columns), back to **2026-03-09**. On 2026-07-20 (13,303 rows):
**`portfolio_strategy_id` is 100% null; `portfolio_strategy_name` has exactly one distinct value —
`"No Strategy"`.**

> **SHAPE vs DATA — the distinction that makes this actionable.** That emptiness is **not** BD failing to
> retain history. Cottonwood's rebalancer assignments are held at **ACCOUNT** level
> (`accountRebalStrategyID` — the field `0.6.2_AE_PartnerETL~A` identified as live-state), while our template
> selected the **PORTFOLIO**-level dimension. **We have been ingesting an empty column for four months
> because it is the wrong level, not because the data is absent.** The account-level dimensions sit in the
> same templates, `isEnabled: True`, unselected.

---

## 2. Why this matters more than it looks

D2 establishes that **the dimension/fact selection lives server-side under the templateId**, and that the
sanctioned way to change a query is to **re-persist the template — not to change code**. So selecting the
account-level assignment dimensions is a **configuration change to a query we already run**, not a new
endpoint, not a new product, and not a vendor conversation.

**And DataMining is date-windowed.** Unlike the Rebalancer live-state API, a DataMining query takes an
explicit window. *If* BD stamps the assignment that was in force on each row's date, then a past-window query
returns **what it was** — the fabrication-safe property Constraint 1 demands, obtained by reading a stored
dimension rather than inferring from present state.

**That "if" is the whole question, and it is NOT yet established.** See §3.

---

## 3. The decisive unknown — and the controlled test that settles it

**UNKNOWN: are BD's rebal-assignment dimensions TEMPORAL (the assignment in force on that row's date) or
CURRENT (today's assignment stamped onto historical rows)?**

If temporal → we have a genuine lookback source. **If current → it is exactly the trap CTO named**: the
`--date`-is-a-filename defect with better manners, and it must be ruled out rather than shipped.

**I could not settle it from stored data, because the one selected column is empty.** I am not inferring it
either way.

**THE TEST (one probe, no new endpoint, no new wire beyond a query we already run):**
1. Re-persist the transactions (or unrealized) template with the **Account**-level assignment dimensions
   selected — `accountRebalStrategyID`, `accountRebalStrategyName`, `AccountRebalAssignmentID`,
   `AccountRebalProgramID/Name`.
2. Run it for **two windows**: a recent one, and one from **before a known assignment change**.
3. **Read the discriminator:** does the account-level strategy value **differ between the two windows for the
   same account**?
   - **Differs → TEMPORAL.** BD holds real assignment history and we can query it back as far as the table
     reaches.
   - **Identical at today's value → CURRENT-STATE STAMPED.** Ruled out under Constraint 1, permanently, and
     documented so nobody re-proposes it.
4. **Positive control (required):** include an account whose assignment we *know* changed between the two
   windows — otherwise "identical" is indistinguishable from "nothing changed," and the test cannot fail.
   *(The 2-day assignment series we do have — 07-21 and 07-22 — is the seed for identifying a changed
   account, if any changed across those two days.)*

**Cost:** one template re-persist + two queries on an existing, already-authorized ingest path. **This is the
cheapest thing on this list by a wide margin and it is also the most informative — it either opens the whole
option or closes it.**

---

## 4. The option set

Ranked by **expected depth × fidelity ÷ cost**. Grades: **[GROUNDED]** verified at source ·
**[INFERRED]** reasoned, labelled · **[UNPROBED]** requires a call I did not make.

### 4.1 — Re-persist the DataMining template to select Account-level assignment **[GROUNDED / then UNPROBED]**
- **Depth:** potentially to each table's horizon — transactions **2026-03-09**, unrealized/allocations
  **2026-04-22**, holdings **2026-06-08**. *(Cottonwood's own ingest horizons, not BD's retention.)*
- **Grain:** account × date, with `AccountRebalAssignmentID` + program + strategy name.
- **Fidelity:** **conditional on §3.** Temporal → high. Current-stamped → zero, and ruled out.
- **Cost:** one template re-persist, two probe queries. No new endpoint. No vendor contact.
- **Verdict: TEST FIRST. This is the recommendation.**

### 4.2 — Run the enriched-template dump we already wrote and have never run **[GROUNDED]**
`data/cot/scripts/bronze/dump_enriched_templates.py` exists, is gate-clean, and per D2 §7 has **never been
run** — `s3://opal-data-cot/code/bronze/templates_enriched/` is **empty (confirmed today)**.
- **What it gives:** the full server-side dimension catalog for all five tables, **including holdings (qt1),
  whose selection we have never seen** — it is a 537-byte thin envelope locally.
- **Why it matters here:** it would reveal whether qt1 (the daily snapshot, the table with the cleanest daily
  grain) also carries an account-assignment dimension. **If it does, that is a materially better source than
  transactions** — a daily snapshot with assignment on it is precisely the series MDPF needs.
- **Cost:** run an existing read-only script on-box (GET template + one put per table). **Zero new surface.**
- **Verdict: DO THIS FIRST OR ALONGSIDE 4.1** — it is free information and it may change which table we target.
- *Bonus: it also closes D2's one outstanding PENDING item, which has been open since 2026-06-26.*

### 4.3 — BD's historical-assignment surface **[GROUNDED that it exists for benchmarks; UNPROBED for models]**
The RCN-0001 capture contains, verbatim:
```
GET /request/api/benchmark/1286/account/assigned?includeHistoricalBenchmarkAssignments=true
GET /request/api/benchmark/1286/portfolio/assigned?includeHistoricalBenchmarkAssignments=true
```
**BD treats historical ASSIGNMENT as a first-class, queryable concept — proven at the parameter level.**
Also observed: `datamanagement/api/v1/dashboard/audit/*`, `.../transactionbackdates/*` (restatement
tracking), and `userExperience/portfolio_view/levelDateOptions?asOfDate=&asOfDateType=LatestBusinessDate`
(as-of semantics in the product).
- **Honest limit:** this is **benchmark** assignment, not **model/strategy** assignment, and **the response
  bodies were not retained** (68 bytes, likely an empty set). **I am not asserting a model equivalent
  exists.**
- **What would settle it:** a targeted capture of the Rebalancer's *model-assignment* screen while changing
  the date, or a look for an `includeHistorical*` sibling on the model/strategy endpoints.
- **Cost:** one capture walk (no egress — an operator-driven session, like the ones that produced RCN-0001/2).
- **Verdict: HIGH VALUE, LOW COST. Worth a capture request.**

### 4.4 — The Rebalancer's own history surfaces **[UNPROBED]**
Observed but never consumed: `rebalancer.bdreporting.com/api/sessions/top` (**rebalance sessions** — a
session is an inherently timestamped event), `POST /request/api/trademanagement/blotter/search` (a trade
blotter filterable by timeframe), `POST /api/models/strategies/search`, `GET /api/accounts/{z-id}`.
- **Why plausible:** a rebalance *session* records what was rebalanced, when, and against which model. SmartX's
  analogue (`changerequesthistory`) is explicitly an **event log** and is the pattern that works.
- **Honest limit:** both returned tiny bodies in our capture (69 B / 88 B — empty result sets for that
  session) and **no body was retained**. Whether they carry per-account model assignment over time is
  **unknown**.
- **Verdict: worth including in the same capture walk as 4.3.**

### 4.5 — Ask Cottonwood / Black Diamond **[UNPROBED — and it is a vendor conversation]**
Cottonwood may hold their own exports/archives; BD may offer a reporting or audit product that exposes
assignment history.
- **Verdict: hold.** It is the highest-cost, slowest option and **it should not be spent before 4.1/4.2/4.3
  are exhausted** — walking into a vendor conversation asking for something their API may already give us is
  the wrong opening. **Vendor contact is Andrew's call, and this brief does not initiate one.**

---

## 5. Ruled out — and why, which CTO rightly said is as valuable as the shortlist

### 5.1 — ❌ Reconstructing assignment from holdings similarity
Inferring "this account held the Long-Term model's basket in April, therefore it was assigned to Long-Term"
is **exactly the defect Constraint 1 forbids.** It infers a past assignment from present model composition
and produces a confident answer with no way to distinguish *was* from *is*. It would also fail silently
whenever two models overlap in holdings — which, for model families like Opal's ladder, is most of the time.
**Never propose this.**

### 5.2 — ❌ Re-running the existing puller with a past date
**Already proven defective today by `0.6.2`:** the eclipse puller's `--date` is **a filename, not a query** —
it fetches *today's* state and files it under the past date, **exit 0, silently.** Any variant of "run the
live-state API for a past date" inherits this. **The Rebalancer has no as-of parameter; this cannot be fixed
by calling it differently.**

### 5.3 — ❌ Back-filling from the 2-day series
Carrying 2026-07-21's assignment backwards across 427 dates is 5.1 without even the pretence of evidence.

### 5.4 — ⚠️ NOT ruled out, but explicitly UNKNOWN: holdings (qt1)
qt1's dimension selection is **server-side and has never been dumped** (D2 §7, still pending). I cannot say
whether it carries an assignment dimension. **Absence of the dimension from our 537-byte local envelope is
not evidence of absence from the template** — that envelope carries no dimensions at all, by construction.
Option 4.2 resolves this.

---

## 6. What I would do, in order

1. **Run `dump_enriched_templates.py`** (4.2) — free, on-box, read-only, and it closes a 4-week-old PENDING
   item while telling us whether qt1 is the better target.
2. **Run the temporal-vs-current probe** (§3) on whichever table the dump favours — **with the positive
   control**, because without it the test cannot fail.
3. **If temporal:** re-persist the template, backfill to the table's horizon, and Cottonwood's series extends
   from 2 points to (potentially) **March**. *That does not reach 2024-11-01 — see §7.*
4. **If current-stamped:** close 4.1 permanently in the record, and go to 4.3/4.4 with a capture request.
5. **Only then**, if all internal paths are exhausted, consider the vendor conversation (4.5) — with a precise
   ask rather than an open question.

## 7. The honest ceiling

**None of these reaches 2024-11-01.** Our Cottonwood ingest horizons are **March–June 2026**; BD's own
retention beyond that is **unmeasured**. The realistic best case is Cottonwood joining the MDPF series from
roughly **2026-03-09**, not from the series start — a **~4-month** history against a **21-month** chart.

**That is still a step change from 2 days**, and it is worth saying plainly to Andrew rather than letting
"we got lookback" imply the full series. **If full-series parity is the requirement, only 4.5 could deliver
it, and possibly not even then** — BD may simply not retain assignment history that far back for a tenant
that onboarded later.

## 8. Grounding

**[GROUNDED]** template dimension inventory + `isSelected` flags (`data/cot/scripts/bronze/templates/*.json`,
read directly) · our silver column presence and emptiness (`s3://opal-data-cot/silver/{transactions,unrealized}/`,
read directly) · ingest horizons (S3 listings) · `templates_enriched/` empty (S3 listing) ·
`includeHistoricalBenchmarkAssignments` parameter + the rebalancer endpoint inventory (RCN-0001 capture) ·
`dump_enriched_templates.py` exists and is unrun (filesystem + D2 §7).
**[INFERRED, labelled]** that account-level selection would populate where portfolio-level is empty — reasoned
from Cottonwood's assignments being account-level (`0.6.2`'s source finding) plus the dimension's presence and
`isEnabled: True`. **Not verified; §3 is the verification.**
**[UNPROBED]** everything requiring a call: 4.3, 4.4, 4.5, and the §3 probe itself.

---

# ADDENDUM — 2026-07-22: the "rebal" endpoint, measured. **How far back DO we have Opal Model allocations?**

**Andrew-direct follow-up.** Zero egress — read from `s3://opal-data-assets/blackdiamond/cottonwood/bronze/`.

## A1. The direct answer

**As ALLOCATION SNAPSHOTS: exactly two days — 2026-07-21 and 2026-07-22. And the endpoint structurally cannot
give more.**

`rebalancer_accounts` returns **911 accounts** over 5 pages, **22 fields per record**:
`accountId · accountNumber · accountType · allowSMA · canRebalance · custodianId · discretionary · exclude ·
externalId · isClosed · isInRebalanceGroup · isManaged · isRebalancerUma · isSMA · isSystemSleeve ·
isUmaSleeveAccount · name · programName · rowNumber · strategyName · taxStatus · userCanViewRestrictedPlanTeam`

> **NOT ONE OF THE 22 IS A DATE.** No `assignedDate`, no `effectiveDate`, no `createdAt`, no `since`.
> **The hypothesis that a live-state roster might still carry a per-assignment effective date — which would
> have given retroactive depth with no historical snapshot — is FALSIFIED at source for this endpoint.**

**Current state (identical on both days):** 911 rebalancer accounts · 446 with any strategy · **296 on Opal
models** across 14 named Opal strategies (Satellite 50 = 82, Satellite 60 = 79, Satellite 80 = 54,
Satellite 70 = 39, Satellite 40 = 16, Satellite 98 = 12, Satellite 30 = 4, Ultra Short Term = 3, Income = 2,
plus 5 singletons).

## A2. **But the MODELS are dated — and that is a real, measured lower bound**

`rebalancer_model_detail` **does** carry timestamps: `hierarchy.createdAt` / `updatedAt`. **An account cannot
be allocated to a model that did not exist**, so model creation dates bound allocation depth from below —
with no assignment history at all.

**25 model definitions. Every Opal model at Cottonwood was created between 2026-05-28 and 2026-07-17.**

**Cumulative earliest-possible allocation depth** (accounts whose model existed by that date):

| Date | Allocatable | Model created |
|---|---|---|
| 2026-05-29 | **54 / 296** | Opal Satellite 80 (+54) |
| 2026-06-10 | **136 / 296** | Opal Satellite 50 (+82) |
| 2026-06-23 | **215 / 296** | Opal Satellite 60 (+79) |
| 2026-06-26 → 06-29 | 219 / 296 | Blended Sat-50, Beecherl Legg, Income (+4) |
| **2026-07-06** | **290 / 296** | Satellite 30 / 40 / 70 / 98 (**+71 in one day**) |
| 2026-07-10 → 07-17 | 296 / 296 | 4 singletons (+6) |

**Cross-check: the 14 models' `accountCount` sums to exactly 296 — matching the roster count derived
independently from `rebalancer_accounts`. Two sources, same number.**

## A3. What this means — it corroborates the migration framing with numbers

- **No Opal-model allocation at Cottonwood can predate 2026-05-28.** Nothing existed to allocate to.
- **Only 54 of 296 accounts (18%) were even *allocatable* before June.**
- **71 accounts — a quarter of the book — sit on four models created on a single day, 2026-07-06.**
- **The last Opal model was created 2026-07-17 — five days before the snapshot.**
- **Eight Opal models exist with ZERO accounts**, five of them created 2026-05-28. Scaffolding stood up first
  and populated later — **the signature of a migration in progress**, not a mature book.

> **THE HONEST ANSWER TO "HOW FAR BACK": the deepest possible Opal-allocation history at Cottonwood is
> ~8 weeks, and only ~18% of the book reaches that depth. The book as it stands today is ~2 weeks old.**
> **Chasing assignment history further back is chasing something that did not exist.** The 2-day snapshot
> series is not far off the true information content of the underlying reality — which is exactly why
> *"don't get too indebted to what they have or don't have yet"* is the right posture.

## A4. Corrections this addendum makes to §1 of the main brief

**§1 said the account-level assignment dimensions are "available but not selected" everywhere.** Measured:
**on `allocations` (qt5) they ARE selected and ARE flowing into our silver** — `account_strategy_id`,
`account_strategy_name`, `manager_strategy`, `investment_strategy_name` are columns in
`silver/allocations/2026-04-22.parquet`, populated with **explicit sentinels** — `"No Strategy"`,
`"No Manager Strategy Define"`, `"No Investment Strategy Def"` — not nulls.

**That is BD affirmatively reporting "no assignment," not BD withholding data** — and the whole 2026-04-22
Cottonwood allocations partition is **3 rows**. Consistent with A2: in April there were no Opal models to be
assigned to, and almost no Cottonwood data in BD at all.

**So the §1 recommendation narrows usefully:** re-selecting account-level dimensions on realized/unrealized is
still worth doing, **but the evidence now says it would correctly return "No Strategy" for the pre-June
window** — because that is the truth, not a gap. **Do it for the June-onward window and for future-proofing,
not as a lookback play.**

## A5. Residual unknowns — stated, not papered over

- **Whether `strategyName` is temporal is now moot for lookback** — there is no date field to make it
  temporal. It is a pure live-state snapshot.
- **The two snapshot days are identical** in counts, distribution and byte size. As COO established, a stable
  roster and a frozen feed are indistinguishable from S3 alone. **Nothing here resolves that** — though
  identical content over ~6.5h between a manual test pull and the first scheduled fire is unsurprising.
- **`updatedAt` on models DOES move** (five 05-28 models show `updatedAt` 2026-07-22T05:01), so the model
  layer is being touched. Whether that is composition edits or a system touch is **not determined**.
- **I did not probe BD live** for a historical-assignment surface. §4.3/§4.4 remain unprobed and, per the
  Amendment, are now low priority.
