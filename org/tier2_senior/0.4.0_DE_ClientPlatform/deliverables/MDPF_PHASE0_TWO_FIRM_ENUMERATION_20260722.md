# MDPF PHASE 0 — THE TWO-FIRM ENUMERATION

**Owner:** `0.4.0_DE_ClientPlatform` · **Authorized:** CTO carve-out 3 (151655Z), cascaded by COO @152259Z —
*"read-only MDPF ANALYSIS continues, especially Phase 0. Enumerating is not initiating."*
**Scope discipline:** read-only throughout. Zero edits to MDPF code, zero applies, zero publishes, zero ETag
moves, no producer runs. The WS-4 re-home remains HELD and untouched.

**VINTAGES** (a line citation without a vintage is not a citation):
- Four census limbs: **`a09e14438`**
- `0.7.0_AE_CloudOps` infra limb: **`1be38817f`**
- My own direct verifications: **`8da5fbfa5`** and **`32b35a589`**

---

## 0. THE HEADLINE, BEFORE THE NUMBERS

**Three findings change the plan's shape. Everything else is inventory.**

**(1) MDPF IS THE LAGGARD, NOT THE FRONTIER.** Cottonwood is already onboarded across the estate — and
**3-firm canonical tuples already exist in sibling Lambdas**, which I verified myself rather than relaying:
- `infra/aws/lambda/etfs-pipeline/etfs-canon-fanin/lambda_function.py:47 @32b35a589`
  `CANONICAL_PARTNERS = ("49financial", "inflection", "cottonwood")`
- `infra/aws/lambda/opal-assets/opal-assets-daily-emitter/lambda_function.py:696 @32b35a589`
  `FOLD_PARTNERS = ("49financial", "inflection", "cottonwood")`

Also already 3-firm: `terraform/partner-firms/cottonwood.tf` (onboarded 2026-04-29), a full 16-file
`terraform/cot-pipeline/`, `served-guard-cot/_root.tf` (*"Uniform across all 3 firms"*), and
`lambda-edge/_shared/firm-config.mjs:51-54` (cottonwood → `opal-data-cot`).
**This raises every MDPF two-firm site from "unknown design" to "known-divergent from an existing estate
pattern."** We are not inventing three-firm-ness; we are catching one pipeline up to it.

**(2) THE MDPF TWO-FIRM ASSUMPTION IS ROLE-ASYMMETRIC, NOT A LIST OF TWO.** It is **one DRIVER
(inflection) + one SKIPPABLE PARTNER (49financial)**, and the asymmetry is load-bearing:
`mdpf-daily-trigger/lambda_function.py:520 @a09e14438` — `partners = {"49financial": bd}   # inflection is
the spine/DRIVER, not a skippable partner`; `run_date` derives from the spine (`:506`); only the spine can
halt (`:541`); and the EventBridge trigger **is** inflection's sentinel
(`terraform/mdpf-pipeline/eventbridge.tf:30-37`). **`spine_fresh` is a scalar — no code path can express
two drivers.** Onboarding Cottonwood therefore requires an **architectural ruling first**: is Cottonwood a
driver, a skippable partner, or a third category? **No list-append answers this.**

**(3) PHASE 0's EXIT CONDITION IS NOT MET, AND I AM NOT GOING TO REPORT THAT IT IS.** The plan's exit is
*"the list is closed and priced."* The list is **materially better characterized and NOT closed** — §3
states exactly why, and it is a property of the problem, not of effort. **What IS now closed is the SHAPE**,
and per PART 3 of the plan the shape is what sets the date.

---

## 1. THE DEFECT-CAPABLE POPULATION — DEFINITION

A site is **defect-capable** if onboarding a third partner firm requires it to change, **or** requires an
explicit verification that it need not. It splits into **two populations that must never be blended into one
fraction**, because one is searchable and the other is not:

**POPULATION A — THE FIRM-TOKEN AXIS.** Sites naming a firm: `49financial`, `inflection`, `49f`, `inf`,
`cottonwood`, display names, and firm-scoped bucket/prefix ARNs. **Searchable.** Coverage is measurable.

**POPULATION B — THE UNNAMED-ARITY AXIS.** Sites encoding two-ness **without naming any firm**: a hardcoded
count, a 2-element concat, a two-term sum, a fixed-arity signature, a closed series list, a pair of
positional args. **This axis is NOT reliably searchable** — I ran the sweep and it returns overwhelmingly
test-row-count noise while missing every real member. Every confirmed member of Population B in this census
was found by **READING**, not by searching. Credit to `0.7.0_AE_CloudOps`, who identified the class and
whose own words are the proof: *"I caught `keys_staged: 7` only because I read the block, not because the
search found it."*

**POPULATION C — THE ABSENCE AXIS (added 1550Z; `0.7.0_AE_CloudOps`, and it is the one that closes Phase 0).**
Sites that encode two-firmness **by OMISSION** — a firm simply missing from a list that should contain it.
**This is a subset of NEITHER sweep above, and the reason is categorical, not incidental:**

> **AN ABSENCE HAS NO TOKEN. YOU CANNOT GREP FOR WHAT IS NOT THERE.**
> Populations A and B are both *pattern searches*, and **every pattern search enumerates what IS PRESENT.**
> A missing member of a list is structurally outside what either can ever return — not rare, not deep,
> **categorically invisible.**

**The instrument for Population C is a SET-DIFFERENCE, not a pattern match:** wherever the estate enumerates
its subjects — IAM `Resource` lists, prefix `Condition`s, EventBridge patterns, `argparse choices=[...]`,
config maps, `FIRM_CONFIG`-style dicts — **take the list and diff it against the real firm population.**
Cheap, because the lists are few and short. **This is the axis that can actually close the enumeration**,
and neither of my two sweeps could have.

**Therefore: THREE populations, THREE stated fractions, never blended.**

> **THIS IS THE METHODOLOGICAL FINDING AND IT BINDS THE ADVISORY.** I fanned out four census limbs and
> briefed every one of them on firm LITERALS. So Population B was under-covered in **all four**, not just in
> infra. A fraction whose denominator is *"sites containing a firm token"*, reported as if it meant
> *"sites encoding two-firmness"*, is a rigorous instrument on the wrong axis — it survives review precisely
> because the method looks careful. **Two fractions, always. Never one blended number.**

**CORROBORATION THAT POPULATION B IS REAL AND LOAD-BEARING** — none of these contains a firm name:
`keys_staged: 7` (on the co-sign's own evidence artifact) · `pd.concat([u49, uinf])` ·
`return units, a49 + ainf` · `assert len(SERVED_MODEL_KEYS) == 7` / `== 5` / `== 2` ·
`len(art["partners"]) == 2` · `STACK_SERIES` (a closed 7-entry FE series list) ·
`SPINE_NON_MODEL_20260718 = 312170328.70` (a frozen two-firm SUM whose guard silently degrades to a no-op
when the sum changes) · `"total_steps": 11` · `name = "invoke-the-two-feeders"` (the count "two" inside a
deployed IAM resource NAME — a replace, not an in-place update).

**AND A GREP-NEGATIVE THAT MATTERS MORE THAN A GREP-POSITIVE:** an adjacent-firm-pair regex over **all 383
`.tf` files returned ZERO matches.** There is no `["49financial", "inflection"]` literal anywhere in
Terraform. The two-firm assumption in the IAM/TF plane is expressed **entirely as separate,
individually-named, single-firm statements and resources.** **A search for "the list of firms" in Terraform
comes up empty and reads as CLEAN.** That is the most dangerous shape in the estate: harder to find, and far
easier to leave half-done, than an explicit list.

---

## 2. COVERAGE — TWO FRACTIONS, PER AREA, WITH THE DENOMINATOR STATED

### Population A (firm-token axis) — file-level

| Area | Examined / total | Note |
|---|---|---|
| `data/mdpf/scripts/gold/` | **17 / 17** source files | 10 read in full, 3 partial, 4 grep-only |
| `infra/aws/terraform/mdpf-pipeline/` | **9 / 9** `.tf` | all read in full; runner role = 22 statements |
| `infra/aws/lambda/mdpf-pipeline/` | **3 / 4** `lambda_function.py` | `wsb-49f-*`, `wsd-49f-*` dirs NOT opened |
| `infra/aws/ec2/mdpf-daily-runner/` dispatch | **573 / 573** lines | read in full, HEAD + working tree |
| publisher Lambda + its TF | **108 / 108**, **143 / 143** | read in full |
| `data/assets/scripts/gold/` | **11 / 29** source files | **18 NOT examined** (17 are `runners_49f/**`) |
| `portal/src/**` | **~25 / 381** files opened | 381 = 210 `.tsx` + 171 `.ts` |
| `infra/` beyond the MDPF module | **~30 / ~7600** candidates | **the large open denominator** |

### Population B (unnamed-arity axis) — bounded by LINES READ, not files touched

| File | Lines read / total | Consequence |
|---|---|---|
| `dim_mdpf_aggregate_aua_timeseries.py` | **~150 / 1453** | **the worst hole** — highest firm-token density (140 hits) AND the home of `build_global_artifact`. ~90% unread on the arity axis. |
| `mdpf_aggregate_aua.py` | **~460 / 1385** | sentinel + reconcile logic largely unread |
| `portal/src/pages/ModelPortfolios.tsx` | **~700 / 2276** | the MDPF page itself |

**Read this honestly: the three files that matter most are 10%, 33%, and 31% read on the axis that cannot be
searched.** Any claim that the list is closed would rest on the 90% of the densest file nobody opened.

### Raw finding counts per limb (NOT deduplicated — overlaps are real and named)
producers **66** · infra **47** · publisher **27** · FE **14 graded + 7 verified-clean** · 0.7.0 **6**.
Known overlaps include the staging loops, `keys_staged: 7`, the count-source audit, and
`compute_per_firm_account_distribution.py` — each independently found by 2–3 limbs. **I am deliberately not
publishing a deduplicated integer**: a precise-looking total assembled across five differing methods would
be false precision, and R10 asks for a coverage fraction against a defect-capable population, not a
headcount.

---

## 3. WHY THE LIST CANNOT BE DECLARED CLOSED

1. **Population B is not searchable** (§1). Its coverage is a *read* fraction, and the densest file is ~10% read.
2. **`runners_49f/**` — 17 files unopened**, 10 of them grep-negative-only. `c04_recon_guard.py` is named
   *reconciliation guard* and is the highest-probability unread home of a `global == A + B` identity.
3. **`infra/` outside the MDPF module** — `cot-pipeline/` (16 `.tf`) unread, so Cottonwood's *existing*
   dispatch/IAM hooks are unassessed; plus ~12 other firm-scoped TF roots unread.
4. **`comp-grep -l "mdpf" infra/` TRUNCATED at its 200-match cap** — the 18-file list is a **lower bound**,
   not an enumeration. An instrument that truncates silently cannot close a denominator.
5. **THE APPLIED PLANE IS ENTIRELY UNTOUCHED.** Zero live AWS calls across all limbs (correct under the
   hold). Every BLOCKING verdict is a claim about the **repo**, not production — DESIRED, never APPLIED.
6. **NOTHING WAS EXERCISED.** Every "it will raise / it will silently skip" is INFERRED from source.
7. **A live instrument defect found mid-census:** `Glob`/`comp-glob` is **CASE-SENSITIVE**. Globbing
   `portal/src/**/*portfolios.tsx` returns *"No files found"* while `ModelPortfolios.tsx` exists. **Any
   earlier agent who globbed the lowercase form got a FALSE CLEAN.** Prior negative results on the portal
   tree taken via Glob should be considered void until re-run.

---

## 4. THE STRUCTURAL FINDINGS — the expensive ones

**S-1 · The global composition gate asserts a TWO-LEG conservation identity that a third firm makes
arithmetically false.** `dim_mdpf_aggregate_aua_timeseries.py:1104-1106 @a09e14438` pins BOTH legs so
inflection's non-model *"can neither be silently DROPPED nor silently FOLDED IN."* Adding Cottonwood does
not add an argument — it requires re-deriving **what the identity IS**. Failure mode is perverse: the gate
fails loudly, so **the path of least resistance under schedule pressure is to make it pass by excluding
Cottonwood.** Single most expensive item in the census.

**S-2 · The serve path enumerates the same per-firm key list THREE times, in three languages, with no shared
source of truth.** Publisher `PUBLISH_MAP` (Python, 9 keys, explicitly *"no derive -> no mis-route"*) ·
`monolith.tf:262-266` exact-key bucket-policy ARNs · `cloudfront-distribution.tf:77-86` exact-9 behavior
paths. **Update two of three and you get a partial serve that NO single instrument sees**: publisher reports
`all_present=True` off its own unextended map length, or the key publishes and 403s at CloudFront, or the
behavior exists and the policy denies.

**S-3 · A guard that enumerates its subjects cannot protect a subject it does not enumerate.**
`mdpf-daily-dispatch.sh:508-539` — `_audit()` exists *specifically* so a missing audit cannot read as clean
(*"ABSENT IS NOT CLEAN"*), **but its dict has hardcoded firm keys.** For Cottonwood the field is not
`audit_did_not_run` — Cottonwood is **absent from the dict entirely**. The guard produces exactly the
failure it was written to prevent, for any firm it does not name. *(0.7.0's finding; the generalisation is
theirs and it deserves to outlive this document: **absence-is-not-clean holds per NAMED firm, never per
firm.**)*

**S-4 · A governance lock forbids the obvious refactor, and Cottonwood has no declared policy.**
`mdpf-daily-dispatch.sh:484-485` carries an explicit CTO-approved prohibition (134926Z) protecting a
**per-firm failure policy** — inflection FAILS the stage, 49F is REPORT-ONLY (rationale: 49F has a known
unfixable defect; failing nightly would train everyone to ignore the guard). **This is correct and must not
be collapsed.** But there is **no default for an unlisted firm**. This is a **decision request, not a code
change**, and it cannot be resolved by an engineer acting unilaterally.

**S-5 · Per-firm named keys are in the SERVED ARTIFACT SCHEMAS, not just in code.**
`inflection_non_model_aua` is emitted on **every row** of `time_series`; plus `n_49f`, `n_inflection`,
`only_49f`, `only_inflection`. Making these firm-keyed maps is a **breaking artifact-shape change with
frontend consumers** — cross-track coordination, not a gold-side edit.

**S-6 · The date axis has a master/follower topology and 49F is the master.**
`dim_mdpf_aggregate_aua_timeseries.py:1403` — `shared_axis = arts.get(FIRM_49F, {}).get("dates")`.
Cottonwood's own gold has a different frontier. A third firm forces the question the two-firm design
deferred: does global's axis become a **union, an intersection, or stay 49F-mastered with a third
follower?** *Each answer changes served values.* **R2 already rules Cottonwood JOINS the existing axis —
this is the mechanism by which that ruling must be implemented, and it is not free.**

**S-7 · A conservation guard DEGRADES SILENTLY rather than failing.**
`dim_mdpf_non_model_assets.py:122-124` pins `SPINE_NON_MODEL_20260718 = 312170328.70`, a **two-firm-summed**
magic constant, and refuses any row equal to it. Add a third firm, the sum changes, **the guard matches
nothing — it does not fail, it becomes a no-op that still looks like a guard in code review.**

**S-8 · The place that most needs a Cottonwood change has NO DEPLOY PATH.** `mdpf-freshness-checker` holds
the 14-cohort taxonomy (the highest-value single edit for third-firm observability) but has **no Terraform
Lambda resource, no `lambda-source-map.json` entry, and its schedule is absent from `trigger-map.json`** —
while `EC2_MANIFEST.json:397` asserts it runs live at `cron(45 16 * * ? *)`. Related: `alarms.tf:118`
defines a 14-key threshold map **no resource consumes**, referencing an alarm `(d)` that does not exist.

**S-9 · The FE legend and the FE stack read from DIFFERENT SOURCES.**
`ModelPortfolios.tsx:142-151` `STACK_SERIES` is a **closed 7-entry literal**; the legend
(`:939 trendModelOrder.map`) and the donut (`:613 Object.values(by_model)`) are **data-driven**. A Cottonwood
model outside the canonical 7 gets a legend swatch and a donut slice and **no bar** — the page even computes
and stores the value (`:1789-1794`) before dropping it. **The trend silently totals less than the donut. No
error, no gap, no console warning.** Every guard on this page was built for the *value* being absent; none
for the *series* being absent.

**S-11 · PHASE 1a IS IAM-BLOCKED. THE PLAN LISTS IT AS "parallel, all unblocked" — IT IS NOT.**
*(`0.7.0_AE_CloudOps` ARN-axis sweep @`6440ed9d8`, run at my request; this is a Population-C finding and
neither of my sweeps could have produced it.)*
`terraform/mdpf-pipeline/iam.tf:243-252` — Sid `AssetsRevampSilverRead` grants **exactly five ARNs**, and
**`blackdiamond/cottonwood/silver/*` is not one of them.** Cottonwood silver **exists** there — 12 `fact_*`
tables from the WS-5 converter. `AssetsRevampListScoped` carries the same closed prefix list.

**GROUNDED ON ALL THREE LAYERS, per Rule 22a:**
- **desired** (Terraform) and **applied** (live `get-role-policy`) **AGREE** → this is **not drift, it was
  never built**;
- **exercised** (`simulate-principal-policy`) → **`implicitDeny`** on the Cottonwood ARN, **`allowed`** on
  inflection **from a SEPARATE invocation** — so the control discriminates rather than merely passing.

**CONSEQUENCE FOR MY OWN NEXT STEP:** Phase 1a re-homes Cottonwood as `build_cottonwood_artifact()` *inside
the shared producer*, which runs on `mdpf-daily-runner-ec2-role`. **It will `AccessDenied` on the first
Cottonwood read**, and `_latest_date` / `_read_partition` discovery fails on the List side too. Two additive
statements fix it. **Not written — an IAM change under the hold; CTO to sequence.**

**S-10 · Two silent-failure modes on a PARTIAL onboarding, both worse than a hard error.**
(a) **Trigger/dispatch desync** — open `partners` without opening `SKIP_49F` and the Lambda exports
`MDPF_STALE_PARTNERS=cottonwood`, *believes it skipped*, and the runner **runs Cottonwood's feeders anyway
on stale data**, fabricating a residual — the exact class skipping exists to prevent.
(b) **Silent taxonomy omission** — `evaluate_cohorts` iterates only `EXPECTED_COHORTS`, so an un-enrolled
Cottonwood cohort emits **no metric at all**, and `treat_missing_data` cannot distinguish *"never enrolled"*
from *"fine."*

---

## 5. A FORCED ORDERING, ESTABLISHED BY MEASUREMENT

`mdpf_revamp_count_source_audit.py:93` holds `AUDITED_FIRMS = {"inflection", "49financial"}`, and
`:102-109` + `:237-241` set **`rc = 1` on ANY unaudited prefix under `gold/mdpf_revamp/`** — before the
`--firm` branches, so it fires regardless of which firm was requested. **This is deliberate**, and the file
names Cottonwood explicitly (`:87-92`, quoting CTO 135923Z *"the population changes with a third firm"*).

**I measured the live prefix state to establish whether the tripwire is already tripped** (read-only listing,
`@32b35a589`): `gold/mdpf_revamp/` holds **10 objects** across **`49financial/`, `global/`, `inflection/`,
`portfolios/`** — **no `cottonwood/` prefix.** *(Retrieval control: my first listing returned `None`; a
`head-object` on a known key succeeded with ETag `08f9720e…`, matching the plan's documented global ETag.
The listing was broken, not the prefix empty. Re-run corrected. **A listing that contradicts a known-present
fact is a broken retrieval, not an absence.**)*

**THEREFORE — THE TRIPWIRE IS ARMED AND NOT YET TRIPPED, AND THE ORDERING IS FORCED:**
**the third audit leg (`AUDITED_FIRMS` + `audit_cottonwood()` + the argparse choices) MUST land in the SAME
change as the staging loops.** Stage Cottonwood first and the nightly returns non-zero, **no
`cycle-complete.json` marker is written, and the parity streak cannot accrue — even if every Cottonwood
artifact is perfect.** You cannot stage first and audit later.

---

## 6. DECISIONS THAT MUST BE MADE BEFORE CODE — none is an engineering call

| # | Decision | Why it cannot be defaulted |
|---|---|---|
| D1 | **Is Cottonwood a DRIVER, a SKIPPABLE PARTNER, or a third category?** | S-2 of the reframe. `spine_fresh` is a scalar; no code path expresses two drivers. Everything in the trigger depends on the answer. |
| D2 | **Cottonwood's count-source-audit failure policy: fail-hard or report-only?** | S-4. A CTO governance lock protects the existing asymmetry; there is no default for an unlisted firm. |
| D3 | **Does the two-leg conservation identity become a fold, or does Global re-derive?** | S-1. The gate is a *correctness* gate; the cheap path is to make it pass by dropping Cottonwood. |
| D4 | **Do the per-firm named artifact keys become firm-keyed maps?** | S-5. Breaking artifact-shape change with FE consumers. |
| D5 | **Which Cottonwood source is canonical for MDPF** — `opal-data-cot` or `opal-data-assets/blackdiamond/cottonwood/**`? | Two mutually-fenced source-of-truth locations exist in one directory, both CTO-conditioned. **Not resolvable from source.** |
| D6 | **The merge-vs-add canonical-key ruling** (crosswalk raises on 2 unmapped Cottonwood keys, fails closed). | **ALREADY RESERVED TO ANDREW.** Unchanged. Not worked around, not softened. |

---

## 7. STALE RECORDS FOUND WHILE ENUMERATING — surfaced, not reconciled

**A stale record says something false with authority.** Three, all source-contradicted:

1. **`org/projects/ADVI_FIRMSEP.json`** — says Phase 3 / FIRMSEP.10 is *gated on Cottonwood credentials +
   bucket creation* as of 2026-05-22. **Source says it SHIPPED:** cottonwood is live in
   `firm-config.mjs:51-54`, and the FIRMSEP.04 CI sentinel is **flipped and active** at
   `shared-advisor-router/test/firm-routing.spec.mjs:85-88`.
2. **`comp-constants.config.yaml:564-568`** — records `FIRM_CONFIG` as *"3 firms: 49financial, inflection,
   mockadv"* and asserts *"Cottonwood NOT yet present here (pre-FIRMSEP.10)."* **At HEAD the constant holds
   FIVE** (`demo` and `cottonwood` both landed since). The drift registry's record of the constant is two
   firms behind the constant. **Whether this degrades the drift GATE is UNEXERCISED — I did not run it, and
   a config read is DESIRED, not behavior.** Routed to `0.8.0_AE_CloudComp` as its owner.
3. **`ADVI_FIRMSEP_ONBOARDING_PLAYBOOK.md` — DOES NOT EXIST.** Referenced as the canonical onboarding
   sequence by `ADVI_FIRMSEP.10`'s TO and by `firm-config.mjs:20`. *(Positive control: the same `ls` finds
   its two sibling `ADVI_FIRMSEP*` docs, so the search reaches that directory.)* **The plan names FIRMSEP.10
   as "the skeleton" — the skeleton is the TO's 13 scope steps, not a playbook.**

**AND THE ONE THAT REFRAMES THE PHASE:** **FIRMSEP.11 is the real name of this work, and no task order was
ever authored.** `ADVI_FIRMSEP.md:365` carries it as a **QUEUED PLACEHOLDER** — content-layer firm-split,
*"COO authors TO file when product timeline materializes"*, gated on Andrew-direct 2026-05-07:
*"preliminary work that can be done to structure for that modeling ADVI setup is great, but cant be
implemented yet."*

> **THEREFORE: FIRMSEP.10 shipped the TENANCY/ROUTING half of Cottonwood onboarding in May. The MDPF data
> half is FIRMSEP.11 in substance — a phase that was explicitly deferred by ruling and never scoped into a
> task order. That is WHY the estate encodes "exactly two firms" throughout MDPF: the content layer was
> never firm-partitioned, BY DECISION.** The MDPF revamp is now building that partition under a new prefix
> (`json/mdpf/{firm}/`) rather than by splitting the old one. **This is not an overrun on a data fold. It is
> an unscoped phase being executed under the name of a different one** — which is the most economical
> explanation of every estimate that has failed here, and it belongs in the advisory.

---

## 8. WHAT I DID NOT DO, AND THE ONE I MOST WANT

- **The render was not run.** `portal/scripts/ui-smoke.mjs --fixtures` pinned to `firmId:cottonwood` is the
  control that found **both** known FE defects — *"by RENDERING the Cottonwood partner view and READING the
  PNG, not by a type-check."* **A grep cannot see contrast.** S-9 and four other FE findings are
  render-visible classes a single pass would confirm or kill in minutes. **It is read-only and I believe it
  sits inside carve-out 3 — but it is a step beyond static reading, so I am ASKING rather than assuming.**
- No exercise of any gate, no mutants, no producer runs, no applies — all correctly forbidden.
- I did not reconcile the stale records; surfaced to their owners.

---

**BOTTOM LINE.** The shape is closed; the list is not. The remaining unknown is concentrated and *named*:
Population B in three large files, **Population C estate-wide (barely started — one sweep, one root)**,
`runners_49f/**`, `cot-pipeline/`, and the applied plane. **Six decisions (§6) gate code and none is an
engineering call.** The forced ordering in §5 is measured, not assumed. **Phase 1a is IAM-blocked (S-11),
contradicting the plan's "parallel, all unblocked."** And the honest reframe is §7: **this is FIRMSEP.11, a
phase deferred by ruling in May and never given a task order** — which is why it keeps costing more than a
fold.

**THE ONE-LINE VERSION OF WHAT THIS CENSUS LEARNED ABOUT ITSELF:** I started with one axis, `0.7.0` showed
me a second, and the second proved there had to be a third — **and only the third can see a missing member
of a list.** Each axis was invisible to its predecessor's method. **The lesson is not "grep harder"; it is
that a census must state WHICH KIND of encoding its instrument can return, because an instrument that
enumerates only what is present will report an absence as a clean result.**
