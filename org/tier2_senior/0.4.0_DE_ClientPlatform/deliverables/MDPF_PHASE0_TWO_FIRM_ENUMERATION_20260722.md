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

**⚠ AND POPULATION C'S INSTRUMENT HAS ITS OWN FAILURE MODE — recorded 1620Z, and it nearly fired today.**
A set-difference is only sound **if the list and the population are in the SAME KEY-SPACE.** Diff two sets
that look comparable but are keyed differently and you manufacture false absences *and* conceal true ones.

**The live near-miss (CTO, caught by CTO before sending, relayed by COO):** a first pass reported `smartx`
missing **eight** July days. **That was the instrument, not a gap.** `fact_model_aum_daily` is
**RUN_DATE-partitioned with full history inside each partition** — today's single partition holds **1,225
distinct data days.** Counting run-date folders and calling them data dates produces a confident,
specific, wrong absence.

> **ESTABLISH DATA-DATE vs RUN-DATE PARTITIONING BEFORE QUOTING ANY PARTITION-COVERAGE NUMBER.**
> **A partition that EXISTS but holds a DIFFERENT DATE-SPACE is an absence a set-difference cannot see.**

**This does not weaken Population C — it bounds it.** For firm-keyed lists (IAM `Resource` sets, `argparse
choices`, `FIRM_CONFIG`) both sides are firms and the diff is sound. For **date- or partition-keyed** lists
the key-space must be established first. **Verify the key-space, then difference.**

**POPULATION D — THE ALIAS AXIS (added 1625Z; from CVO's A11 FAILURE, relayed by COO).** Sites encoding
two-firmness in an **ALIAS namespace** rather than the canonical one. The estate carries at least two
parallel firm namespaces:

| canonical | alias | appears as |
|---|---|---|
| `49financial` | **`bd`** | `opal-data-bd`, `bd-pipeline`, `blackdiamond/49f/`, `BD_BUCKET`, `bd_bucket` |
| `inflection` | `inf` | `opal-data-inf`, `inf-pipeline`, `inf_bucket` |
| `cottonwood` | `cot` | `opal-data-cot`, `cot-pipeline`, `ROUTER_FIRM_SUFFIX` |

**⚠ THIS IS A MEASURED HOLE IN MY OWN CENSUS, NOT A HYPOTHETICAL.** I briefed my limbs on
`49financial|inflection|49f|inf|cottonwood`. **Three of the four did NOT include `bd`.** *(Only the FE limb
searched short-form ids `'bd'|'inf'|'cot'`.)* A spot-check over the MDPF gold + dispatch + publisher surface
returns a substantial `bd`-aliased population my limbs could not have seen — `validate_schwab_native_custody.py`
and `build_mdpf_wse_49f_non_model_aua.py` are densely bd-aliased throughout.
**Therefore my Population-A fraction is OVERSTATED and I am marking it so rather than restating it.**

**⚠ AND THE ALIAS AXIS IS NOISY IN BOTH DIRECTIONS — a naive sweep over-reports.** In this very tree `bd`
does **double duty**: it is the firm alias for 49financial **and** a custody-source enum value
(`DEFAULT_CUSTODY_SOURCE = "bd"`, `CUSTODY_SOURCE = bd|schwab`, `build_mdpf_wse_49f_non_model_aua.py:151`).
**`bd`-as-custody-basis is not a firm-axis site at all.** So the alias sweep must disambiguate by role, or
it trades my false-negatives for a pile of false-positives.

---

**Therefore: FOUR populations, FOUR stated fractions, never blended — for C, the key-space stated before
the difference is quoted; for D, the alias disambiguated by role.**

> **AND THE AXIS LIST IS OPEN, WHICH IS THE REAL FINDING.** It has grown **three times after someone
> declared its shape** — A (mine) → B (`0.7.0`, arity) → C (`0.7.0`, absence) → D (CVO's A11, alias). Each
> was invisible to its predecessor's method, and **each was discovered by a FAILURE, not by a review.**
> **Every fraction on this work is therefore PROVISIONAL, including all four of mine.** *(COO's framing,
> and it is the correct one: treat the axis list as open rather than as a taxonomy that has settled.)*
> **A census cannot state its own completeness — it can only state which kinds of encoding its instruments
> can return, and how many kinds it has been surprised by so far. That number is four, today.**

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
| `dim_mdpf_aggregate_aua_timeseries.py` | **1453 / 1453 — ✅ CLOSED 1645Z** *(was ~150)* | **the census's worst hole, now shut.** Andrew-direct: *"keep closing the read fraction."* Results in §4a. |
| `mdpf_aggregate_aua.py` | **~460 / 1385** | sentinel + reconcile logic largely unread — **now the largest remaining hole** |
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

### 2a. ⚠ I RAN S-13's TEST AGAINST MY OWN FOUR FRACTIONS. THREE OF THE FOUR FAIL IT.

Doctrine §7f (`@f9f6a4c72`): **a coverage fraction is only evidence if its denominator comes from OUTSIDE
the instrument's own configuration.** COO put that to me directly as a test of this census before I close
it. Running it honestly:

| fraction | its denominator | comes from? | verdict |
|---|---|---|---|
| **A · firm-token** | files containing a token **from a list I chose** | **MY CONFIGURATION** | ❌ **FAILS** — and this is *exactly* how `bd` was missed. Marking it overstated was treating the symptom; this is the disease. |
| **B · unnamed-arity** | **lines read / total lines in the file** | **THE WORLD** (a file's length is a fact, not a choice) | ✅ **SOUND** |
| **C · absence** | the enumerated lists **I decided to diff** | **MY CONFIGURATION** | ❌ **FAILS** — a list I never thought to check is not in the denominator, and its omission is invisible |
| **D · alias** | the alias set **I define** (`bd`/`inf`/`cot`) | **MY CONFIGURATION** | ❌ **FAILS** — same shape as A, one namespace over |

> **THE ONLY DENOMINATOR IN THIS CENSUS THAT IS EVIDENCE IS THE READ FRACTION.** Everything else is
> **directional**, not probative — each measures how thoroughly I applied my own chosen list, which is a
> statement about my method, not about the estate.

**AND THIS EXPLAINS THE SESSION'S OWN RESULTS RATHER THAN JUST LABELLING THEM.** The read fraction is what
overturned the crosswalk's CHECKED-CLEAN, and what produced amend 2 — the discovery that a *searched*
finding was confidently wrong in the expensive direction. **Reading was the only instrument here whose
denominator I could not accidentally define.** That is why it kept winning.

**PRACTICAL CONSEQUENCE FOR THE DECOMPOSITION (COO is downstream of this census):** quote the **read
fraction** as coverage. Treat A, C and D as **leads, not clearance** — a TO written against any of them
assumes work is done that only my own token/list choices ever looked for.

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
6a. **🔴 A FIFTH INSTRUMENT DEFECT — MINE, AND IT FAILS THE *OPPOSITE* WAY (1745Z).**
Measuring Cottonwood's `fact_holdings` I reported *"`Cash Equivalent`: object dtype, **0 / 16,762
non-null** — so CASH CANNOT BE IDENTIFIED IN THIS TABLE"*, and I sent it to DS as the **settle-before-derive
blocker** on Andrew's total-AUA directive.
**DS inverted it; I verified the inversion myself rather than inheriting it:**
`Cash Equivalent` is **16,762 / 16,762 NON-NULL**, dtype object, distinct values `['true','false']` — **a
BOOLEAN FLAG, not a money column.** I had run `pd.to_numeric()` over it; `'true'`/`'false'` coerce to `NaN`,
and the non-null count returns **0**.
**Cash was never missing — it is flagged on EVERY row, and already inside the $458.1M base:**
`true` = 1,428 rows / **$15,232,656.26 (3.33%)** · `false` = 15,334 rows / $442,881,346.84.
**So the Cottonwood base is ALREADY full-envelope, semantically matching 49F's `net_mv_plus_cash`.**

> **A FLAG MEASURED ON A NUMERIC AXIS RETURNS THE EXACT OPPOSITE OF THE TRUTH** — not *"cash is absent"*
> but *"cash is labelled everywhere."*
>
> **AND NOTE THE DIRECTION, BECAUSE IT IS NEW.** Every other instrument defect in this census fails toward
> **FALSE CLEAN** (Glob, `comp-grep -l` truncation, run-date counting, `comp-platinum`'s 2-of-5 fetches).
> **This one failed toward FALSE ALARM: it manufactured a blocker that did not exist.** Same root cause —
> wrong axis — opposite sign. **I spent the session cataloguing instruments that answer "nothing found"
> and then produced one that answers "something is broken," from the identical error.**
> *An overstated hazard spends the same credibility as a false one, and this one would have spent DS's
> hours hunting a cash leg that was never lost.*

**AND DS CORRECTED MY FRAMING, NOT JUST MY NUMBER — the more useful half.** I relayed *"propose a solution
in similar SHAPE."* DS measured that the 0824 base's `.fillna(0.0)` (`:327`) hits **0.00% of rows on live
49F data and has NEVER FIRED.** **A null policy that has never been exercised is not a design decision, it
is an untested assertion** — and copying it onto Cottonwood's 26%-null profile is how it fires for the
first time in production. **Mirror the IDENTITY (custodian total is base, model subtracted, remainder is
non-model); RE-DECIDE the nulls.**

7. **A live instrument defect found mid-census:** `Glob`/`comp-glob` is **CASE-SENSITIVE**. Globbing
   `portal/src/**/*portfolios.tsx` returns *"No files found"* while `ModelPortfolios.tsx` exists. **Any
   earlier agent who globbed the lowercase form got a FALSE CLEAN.** Prior negative results on the portal
   tree taken via Glob should be considered void until re-run.

---

## 4a. ✅ READ FRACTION CLOSED — `dim_mdpf_aggregate_aua_timeseries.py`, 1453/1453 (1645Z)

*Andrew-direct: "keep closing the read fraction." This was the number CTO carried to him as the one that
gates the date. It is now closed on this file. Three results.*

### (1) THE FILE HAS THREE LAYERS, AND ONLY ONE OF THEM IS TWO-FIRM

| layer | firm-arity | verdict |
|---|---|---|
| **helpers + gates** | **already N-firm generic** | `canonical_trading_axis(frontier)` · `_assert_cross_axis_coherence(firm_id, …, same_source, exempt_dates)` · `_honest_none_marker(model_prefix, custody_prefix, …)` · `_cohort_provenance(…)` · `load_account_dist_frontier_counts(firm_id)` · `load_served_account_count(firm_id)` · `build_source_vintage_revamp(by_feeder)` — **`by_feeder` is a firm-KEYED map.** All parameterised. **CLEAN.** |
| **per-firm builders** | one per firm, **per-VENDOR** | `build_49f_artifact` (SmartX + Schwab) · `build_inflection_artifact` (Eclipse + Orion). A `build_cottonwood_artifact` (Black Diamond) must be **written**, not generalised — each firm has different vendors. **REAL work, but EXPECTED work.** |
| **orchestration + composition** | **FIXED AT 2 — the actual blocker** | `:1387-1388` argparse choices · `:1395` `want` set · `:1398-1406` three if-blocks + the 2-arg compose · `:1408` report loop over a 3-literal · `:1207` `_sum2` · **`:1262` AND `:1286` — TWO hardcoded 2-tuple folds** (model_value *and* account_count) · `:1316-1320` the vintage merge as two literal `.update()` calls. |

**`SOURCE_PROVENANCE` at `:77-80` ALREADY CONTAINS `"blackdiamond": "Black Diamond"`** — Cottonwood's
provenance resolves with no change. A rare pre-built absence, and evidence the file was written with a
third firm in mind.

### (2) ⚠ S-6 DOWNGRADED — the "49F is the axis master" topology does not exist

**BOTH** firms call `canonical_trading_axis(frontier)` (`:583`, `:781`). The `:1403`
`shared_axis = arts.get(FIRM_49F…)` is main() passing 49F's **frontier** so the two axes match exactly —
and `:1348-1349` says so: *"expect IDENTICAL axes (both the shared canonical trading-day axis); any diff
is a NAMED structural delta, never a silent firm-sum on a mismatch."* `canonical_trading_axis`'s own
docstring (`:361-366`) reads **"All three firms share this axis so global is a trivial date-join."**

> **So there is no union-vs-intersection ruling to make. R2 ("Cottonwood JOINS the existing axis") is
> implementable by passing the same `shared_axis` — one argument.** *Second structural item that reading
> downgraded, after D3.*

### (3) 🔴 NEW — A CLOSED MODEL-KEY LIST IN THE PRODUCER, EXACTLY MIRRORING THE FE DEFECT

`:111` — `GLOBAL_MODEL_KEYS = SERVED_MODEL_KEYS + ("opal_blend_5050_int_ltc", "opal_blend_5050_st_int")`
— a hardcoded **union of the two firms' model sets**. `:1245` `for mkey in GLOBAL_MODEL_KEYS:` is the
global `by_model` loop.

**Cottonwood's models are absent from that list by OMISSION. So even a PERFECT Cottonwood artifact,
correctly folded, contributes NOTHING to global `by_model` — silently.** *(And `entry_for_key(mkey)` at
`:1246` raises on an unknown key, so adding them without a crosswalk entry fails closed — correct
direction.)*

> **THIS IS THE SAME DEFECT SHAPE AT BOTH ENDS OF THE PIPELINE.** A closed model-key list in the
> **producer** (`GLOBAL_MODEL_KEYS`), and a closed series list in the **frontend** (`STACK_SERIES`,
> S-9 — confirmed by render). **Neither errors. Both silently omit a third firm's models.** A fix at one
> end without the other still yields a Cottonwood that is invisible — and **no single limb could see
> this**: it took the producer read *plus* the FE render. **Population C, appearing independently in two
> components that no one instrument covers.**

---

## 3a. 🔴 VINTAGE CORRECTION (1710Z) — TWO OF MY STRUCTURAL FINDINGS CITE CODE THAT EXISTS AT NO COMMIT

*Prompted by COO's own downward severity correction on the same file. Verified myself against HEAD with a
positive control (`revamp_stage` ×2, 532 lines at HEAD — the read works).*

**`infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh` IS DIRTY (`+44/−3` vs HEAD) AND HAS BEEN ALL
SESSION.** Measured:

| my citation | at HEAD | in working tree | verdict |
|---|---|---|---|
| **S-3** `_audit()` `:508-539` | **ABSENT** (`_audit(` count = 0) | `:508`, `:537`, `:538` | **🔴 NO COMMIT ANCHOR EXISTS** |
| **S-4** governance lock `:484-485` (*"CTO-APPROVED AS WRITTEN (134926Z)"*) | **ABSENT** (`134926Z` count = 0) | `:484` | **🔴 NO COMMIT ANCHOR EXISTS** |
| `count_axis_source_audit` | **0** | **1** | HEAD=0 / TREE=1 |
| `keys_staged: 7` | `:493` | `:526` | ⚠ **both numbers appear in this census** (different limbs) |
| `"segments"` block | `:494` | `:527` | ⚠ same split |
| staging loops `for firm in …` | `:459`, `:472` | `:459`, `:472` | ✅ **identical — these citations stand** |

### WHAT THIS CHANGES

**S-3 and S-4 remain TRUE ABOUT THE PROPOSED CODE, and they are NOT findings about the record or the
runtime.** Their severity drops the same way COO just dropped its own: from *"a defect on the MDPF nightly
path"* to *"a defect in an unlanded, uncommitted change."*

**S-4 IS THE ONE THAT EMBARRASSES ME, BECAUSE IT IS A GOVERNANCE CLAIM.** I reported to CTO and COO that a
**CTO-approved prohibition (134926Z)** protects the per-firm failure policy, and treated it as binding law
constraining the third-firm design. **That text exists in nobody's commit.** It is in a dirty working file
that any `git checkout` or `git stash` would erase without trace. *I amplified unlanded text into a
governance finding and routed it to two Tier-1 lanes.*

### AND THERE ARE THREE VINTAGES HERE, NOT TWO — I CONFLATED THE SECOND AND THIRD

`EC2_MANIFEST.json` / `mdpf-daily-dispatch.sh:7-9`: the runner **fetches the script from
`s3://opal-data-mdpf/code/` at run time.** So:

> **DEPLOYED ARTIFACT (what runs) ≠ HEAD (the record) ≠ WORKING TREE (someone's uncommitted edit).**
> **A git commit is not a deploy here, and a working-tree read is not even the record.** My census cited
> tree as though it were record, in a document whose own §1 demands `file:line @ commit-ish`.

**THE GENERALISATION, and it is the sharpest self-correction in this census:** I have spent the session
insisting that *a line citation without a vintage is not a citation* — and the failure mode I did not
anticipate is **a citation for which NO VINTAGE CAN EXIST.** A dirty working tree is not a vintage; it is a
state no one else can reproduce and nothing can anchor. **The rule needs a second clause: verify the
citation RESOLVES at the vintage you name — because `grep` on a dirty tree answers confidently and
`git show HEAD:` is the only thing that would have caught it.**

*(All four census limbs read the working tree. `0.7.0` cited the TREE line numbers, the publisher limb
cited HEAD line numbers, and I folded both without reconciling them — a two-vintage census presented as
one.)*

---

## 4. THE STRUCTURAL FINDINGS — the expensive ones

**S-1 · The global composition gate — ⚠ DOWNGRADED 1615Z BY DIRECT READ. I OVERSTATED THIS, AND THE
CORRECTION IS THE MOST DECISION-RELEVANT THING IN THE CENSUS.**

**What I originally reported** (relayed from the producers limb, which grepped rather than read): the
two-leg conservation identity is *"arithmetically false with a third firm"*, requiring the identity itself
to be re-derived; **the single most expensive item.**

**What the source actually says**, having now read `build_global_artifact` and `_assert_global_composition`
in full (`:1094-1274 @32b35a589`):

- `:1220-1223` — **`non_model_aua` is the 49F-ONLY basis** by Andrew-direct 2026-07-22 (basis B, *"EXCLUDE
  consistently"*). Inflection's non-model is carried in a SEPARATE 2b audit field and **never enters the
  headline**.
- `:1226-1227` — `opal_aggregate = m49 + nm49 + minf`.
- The asserted identity is `opal_aggregate == model_aua + non_model_aua`.

**Add Cottonwood and the identity BALANCES BY CONSTRUCTION:**
`model_aua = m49 + minf + mcot` · `opal_aggregate = m49 + nm49 + minf + mcot` · `non_model = nm49`
→ `(m49 + minf + mcot) + nm49 == m49 + nm49 + minf + mcot` ✓

**And the LEG PINS are pins on NON-MODEL** (`:1126-1136`) — but **Cottonwood carries no non-model at all**:
`build_cottonwood_mdpf_slice.py:243` emits `"non_model_aua": [None] * len(dates)`, because Black Diamond
Rebalancer carries model assignment only and cannot support a custody-total claim. **A firm with no
non-model leg cannot falsify a non-model pin.**

> **THEREFORE: THE IDENTITY GENERALISES RATHER THAN BREAKING. D3 IS NOT A RE-DERIVATION — IT IS AN ARITY
> CHANGE.** Andrew's basis-B ruling, made for an unrelated P0 this morning, **happens to have already
> solved the three-firm case.** *This removes what the census called its single most expensive item.*

**⚠ AND THE CONDITION THAT MUST BE CARRIED WITH IT — this is a DEFERRAL, not an elimination:** the result
holds **only while Cottonwood's `non_model_aua` is null**. The day Cottonwood gains a custody total, the
third non-model leg is real and D3 returns in full. **That condition must be written into the gate as an
assertion, not left as a comment** — otherwise the next firm inherits a silently-wrong-shaped identity.

**WHY THIS CORRECTION EXISTS AT ALL, and it is the census's own lesson turned on itself:** the overstatement
came from a limb that **grepped** this file (~10% read) and reasoned from the docstring. The correction came
from **reading the arithmetic**. Population B is not merely under-covered by search — *a search can produce
a confident finding that is wrong in the expensive direction.* **This is the strongest single argument for
closing the read fraction before pricing anything.**

**S-2 · The serve path enumerates the same per-firm key list THREE times, in three languages, with no shared
source of truth.** Publisher `PUBLISH_MAP` (Python, 9 keys, explicitly *"no derive -> no mis-route"*) ·
`monolith.tf:262-266` exact-key bucket-policy ARNs · `cloudfront-distribution.tf:77-86` exact-9 behavior
paths. **Update two of three and you get a partial serve that NO single instrument sees**: publisher reports
`all_present=True` off its own unextended map length, or the key publishes and 403s at CloudFront, or the
behavior exists and the policy denies.

**S-3 · A guard that enumerates its subjects cannot protect a subject it does not enumerate.**
> **⚠ VINTAGE (see §3a): `WORKING TREE ONLY — NO COMMIT ANCHOR EXISTS.** `_audit(` is absent at HEAD. This
> is a finding about an **unlanded change**, not about the record or the deployed artifact. The
> generalisation below stands on its own; the citation does not anchor.*
`mdpf-daily-dispatch.sh:508-539` *(tree)* — `_audit()` exists *specifically* so a missing audit cannot read as clean
(*"ABSENT IS NOT CLEAN"*), **but its dict has hardcoded firm keys.** For Cottonwood the field is not
`audit_did_not_run` — Cottonwood is **absent from the dict entirely**. The guard produces exactly the
failure it was written to prevent, for any firm it does not name. *(0.7.0's finding; the generalisation is
theirs and it deserves to outlive this document: **absence-is-not-clean holds per NAMED firm, never per
firm.**)*

**S-4 · A governance lock forbids the obvious refactor, and Cottonwood has no declared policy.**
> **🔴 VINTAGE (see §3a): `WORKING TREE ONLY — NO COMMIT ANCHOR EXISTS.** `134926Z` is absent at HEAD.
> **I reported this to CTO and COO as binding governance; the text is in a dirty file a `checkout` would
> erase.** The per-firm-policy QUESTION for a third firm is real and still needs a ruling — but there is
> **no landed prohibition** to point at, and nobody should cite one.*
`mdpf-daily-dispatch.sh:484-485` *(tree)* carries an explicit CTO-approved prohibition (134926Z) protecting a
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

**S-6a · SOURCE REALITY, added 1620Z (COO, from the July completeness matrix — input to this census, not
my measurement):** **Cottonwood `fact_model_assignment` carries only 2026-07-21 and 2026-07-22** —
Rebalancer **live-state, no history**. Raised to CTO as possibly binding the flip SHAPE.
**Two consequences I can state from my own work:**
1. It **corroborates R2** (Cottonwood joins the existing axis carrying nulls before 07-21) and the plan's
   *"1–2 points at the right edge, zero overlap"* — but it makes the *"every pre-07-21 Global value is
   byte-identical with Cottonwood absent"* claim **true by construction AND nearly vacuous**: a two-day
   firm cannot move a 427-date series anywhere but its right edge.
2. **My render fixture was MORE GENEROUS than reality** (I gave Cottonwood 60 populated dates). That does
   **not** weaken the S-9 finding — the defect is keyed on the model KEY, not the date count, and the
   control proves it — but a real Cottonwood artifact would render those charts blank *and* nearly
   empty-by-data. **Stating it so nobody reads my PNG as a claim about data depth.**

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

**S-13 · A COMPLETENESS SIGNAL WHOSE DENOMINATOR IS ITS OWN CONFIGURATION — three instances, three
components, one class. AND IT QUALIFIES R10.** *(`0.7.0_AE_CloudOps` @`3a7e29f47`; limb stated: publisher
IAM face + `PUBLISH_MAP`, **NOT** producer logic.)*

| signal | its denominator | what it reports on a 3-firm cycle |
|---|---|---|
| `count_axis_source_audit` | hardcoded firm keys | GREEN — Cottonwood absent from the dict entirely |
| `keys_staged: 7` | a literal | GREEN — 7 claimed while 9 landed |
| `all_present` | `len(PUBLISH_MAP)` | **`9/9, all_present=True` — WITH COTTONWOOD UNSERVED** |

`opal-assets-mdpf-portal-publisher/lambda_function.py:37-47` — `PUBLISH_MAP` is a hardcoded 9-entry dict
with **no Cottonwood entry**; `:100` iterates the map, `:102` derives `all_present` from that iteration,
`:106` reports `len(PUBLISH_MAP)` as the total. **A firm absent from the map never enters the loop, so it
cannot lower the score.** *(Publisher IAM is genuinely CLEAN on the firm axis — wildcard prefixes, no firm
named, no IAM change needed for a third firm. The map is the defect, not the grants.)*

> **A SIGNAL THAT MEASURES ITS OWN CONFIGURATION CANNOT FAIL.** And the sting: the `_audit()` helper was
> written *specifically* to stop silent omission (*"absence of a verdict is not a passing verdict"*) — **and
> it omits silently, because its subject list is hardcoded.** Care did not save it. Only comparing the list
> to the world would.

**⚠ THIS QUALIFIES R10, WHICH IS A BINDING RULING.** R10 requires every evidence limb to state a coverage
fraction against the defect-capable population. **All three signals above would SATISFY R10 while
misleading** — each reports a fraction against *its own denominator*. **So R10 needs one more clause:**

> **RECORD WHAT THE DENOMINATOR IS DERIVED *FROM*.**
> `9/9 where 9 = len(PUBLISH_MAP)` and `9/9 where 9 = keys actually staged this cycle` **render
> identically — and only the second is evidence.**

**And it upgrades Population C beyond how it was pitched to me:** the absence axis is not only *"the one
axis that can see a missing member"* — **it is the only axis that can see a LYING GREEN SIGNAL**, because
these three are invisible to A, B and D and each passes its own check.

**S-12 · WHAT THE READ FOUND THAT NO SEARCH COULD: the composition's SEMANTICS are already N-firm-correct;
only its ARITY is fixed at 2.** *(Population B, all `@32b35a589`, none containing a firm name — invisible to
the token axis.)*

| site | code | why a search misses it |
|---|---|---|
| `:1207-1208` | `def _sum2(a, b): return None if (a is None or b is None) else round(a+b, 2)` | **the fold primitive itself, fixed at two arguments.** Named `_sum2`. Used for `model_aua` and `partner_custody`. |
| `:1262` | `for art_bm, idxmap in ((bm49, d49), (bminf, dinf)):` | **the actual per-model cross-firm fold is a hardcoded 2-element tuple-of-pairs.** This is the single most load-bearing arity site in the file. |
| `:1226-1227` | `None if None in (m49, nm49, minf) else round(m49 + nm49 + minf, 2)` | a three-term literal sum over two firms' components. |
| `:1111` | `ident, pin49, pininf, partial = [], [], [], []` | two per-firm violation accumulators, one per leg. |
| `:1094-1096` | `_assert_global_composition(..., a49, ainf, d49, dinf, ...)` | 2-firm-shaped signature + a firm-named parameter `inf_non_model`. |
| `:111` | `GLOBAL_MODEL_KEYS = SERVED_MODEL_KEYS + ("opal_blend_5050_int_ltc", "opal_blend_5050_st_int")` | global's model universe expressed as *firm A's models + firm B's models* — a two-term concat. |

**BUT — AND THIS IS THE GOOD NEWS THE CENSUS DID NOT HAVE:** the *hard* part is already right.
`:1257-1270` explicitly distinguishes **"this firm does not carry this model"** (skip, not a gap) from
**"a contributing firm's value is missing on this date"** (poison the sum to `None`) — the ABSENT-IS-NOT-ZERO
logic that closed this morning's false-dip P0. **That logic is written generically over the loop.** Make the
loop N-ary and it generalises unchanged. Likewise the gate's band/total check (`:1141-1158`) already iterates
`by_model.values()` — N-firm today.

> **So the re-home is a MECHANICAL GENERALISATION — `_sum2` → an N-ary fold, and the `((bm49,d49),(bminf,dinf))`
> literal → a list built from a firm registry — NOT a redesign of the composition's semantics.** Combined with
> the S-1 downgrade, **Phase 1a is substantially cheaper than the census priced it, and it is blocked on IAM
> (S-11) and a ruling (D5), not on difficulty.**

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
*(**FIVE** live, not six: D3 was downgraded out of this table at 1615Z. Left in place struck-through rather
than deleted, so the record shows the correction instead of hiding it.)*

| # | Decision | Why it cannot be defaulted |
|---|---|---|
| D1 | **Is Cottonwood a DRIVER, a SKIPPABLE PARTNER, or a third category?** | S-2 of the reframe. `spine_fresh` is a scalar; no code path expresses two drivers. Everything in the trigger depends on the answer. |
| D2 | **Cottonwood's count-source-audit failure policy: fail-hard or report-only?** | S-4. A CTO governance lock protects the existing asymmetry; there is no default for an unlisted firm. |
| D3 | ~~Does the two-leg conservation identity become a fold, or does Global re-derive?~~ **DOWNGRADED 1615Z — see S-1. The identity GENERALISES; basis-B already solved N=3. What remains is not a decision but a REQUIRED CONTROL: assert Cottonwood's null non-model in the gate, so the deferral cannot expire silently.** | No longer a ruling. The bad incentive I flagged (*"make it pass by dropping Cottonwood"*) **does not arise, because the gate does not fail.** |
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
`runners_49f/**`, `cot-pipeline/`, and the applied plane. **FIVE decisions (§6) gate code and none is an
engineering call** *(six, less D3, which reading the arithmetic removed — S-1)*. The forced ordering in §5 is measured, not assumed. **Phase 1a is IAM-blocked (S-11),
contradicting the plan's "parallel, all unblocked."** And the honest reframe is §7: **this is FIRMSEP.11, a
phase deferred by ruling in May and never given a task order** — which is why it keeps costing more than a
fold.

**THE ONE-LINE VERSION OF WHAT THIS CENSUS LEARNED ABOUT ITSELF:** I started with one axis, `0.7.0` showed
me a second, and the second proved there had to be a third — **and only the third can see a missing member
of a list.** Each axis was invisible to its predecessor's method. **The lesson is not "grep harder"; it is
that a census must state WHICH KIND of encoding its instrument can return, because an instrument that
enumerates only what is present will report an absence as a clean result.**
