# MDPF legacy roster single-sourcing -- findings from a CANCELLED item

**archetype:** DIAGNOSE
**Author:** 0.7.0_AE_CloudOps (PID 18964)
**Window:** 2026-07-28T204400Z - 205900Z
**Item status:** **CANCELLED** by CTO 205446Z (reading 1, CANONICAL ONLY; Ruling 1 -- legacy stays
untouched -- stands unbroken). Cottonwood already reaches the product via the canonical lineage
(`build_global_artifact(a49, ainf, acot)`, exercised ~15:00Z).
**Why this file exists:** CTO 205547Z -- *"a cancelled item's design work is exactly the kind that
evaporates, and three of these five findings are load-bearing for whoever eventually re-points this
producer."* Also: **DS's implementation patch is PRESERVED and re-appliable**
(`org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/HELD_20260728T2046Z_roster_single_source/`),
so a latent defect recorded here is a defect that travels with a live patch.

**Grounding vintage:** all repo claims at HEAD `1b4df4b223`. Live-state claims carry their own probe.

---

## F-1. "ENROLL COTTONWOOD" IS A MISNOMER -- THE FIX IS SUBTRACTION, NOT ADDITION

Cottonwood has been a **declared partner since 07-24**. `data/mdpf/config/partner_roster.json`
declares three partners -- `49financial`, `inflection`, `cottonwood` -- with cottonwood's row fully
specified:

```
cottonwood.legs.model.quantities.value : effective_from 2026-05-28
cottonwood.legs.model.quantities.count : effective_from 2026-07-22
  bounded_historical_fact.unbackfillable_before = 2026-07-22
  "a BOUNDED HISTORICAL FACT about a closed window, NOT a permanent exemption"
```

`mdpf_aggregate_aua.py` does not fail to know about cottonwood. **It never ASKS.** It answers the
roster question itself, twice, from literals:

| site (@`1b4df4b223`) | form |
|---|---|
| `:492-500` `expected_partners_for(date)` | `base = {"49financial"}`; adds `"inflection"` if `date >= INFLECTION_PARTNER_ONBOARD_DATE` |
| `:1132` | `expected_partners = {"49financial", "inflection"}` -- a bare literal that **never calls the function above it** |

**The correct fix deletes both literals and asks the roster.** Cottonwood then appears *because it is
a roster row* -- which is `mdpf_roster.py`'s own stated acceptance, the **PARTNER-#4 TEST**:
*"onboarding a partner must be A ROSTER ROW AND NOTHING ELSE -- no code edit, no constant bump."*

### F-1a. The literal reading of the dispatch would have been WORSE than the current defect
"Enroll cottonwood at `:492-500` and `:1132`" reads naturally as *add `"cottonwood"` to those two
sets*. That is **a fourth string in a hardcoded list** -- CTO's own 171123Z ruling against, and the
same reasoning `~C` used to refuse the `assets_gold` fix the same evening. It would additionally have
**silently asserted cottonwood expected for COUNT back to 2026-05-28** -- false, and un-backfillable
from the vendor. A wrong expectation that can never be satisfied is worse than a missing one: the
missing one is silent, the wrong one fires forever and gets suppressed.

---

## F-2. THE PRESERVED PATCH IS QUANTITY-BLIND (safety catch, recorded against a live patch)

DS's reverted diff replaced the `:1132` literal with:

```python
expected_partners = expected_partners_for(date)      # date only -- NO quantity
```

**Quantity is exactly what cottonwood's row splits** (`value` from 05-28, `count` from 07-22). A
date-only call collapses the two, which `mdpf_roster`'s own docstring names as *"recreating the defect
in a different shape."*

**Binding requirement on any re-application:** the `:1132` site feeds `feeders_missing` off `partners`
blocks carrying `model_aua` / `sma_aua` / `non_model_aua` -- i.e. **`quantity="value"`** -- and it must
be **passed explicitly, never defaulted**. CTO recorded this against the preserved patch at 205547Z.

---

## F-3. RUNTIME PRESENCE IS THE REAL BLOCKER -- NOT IMPORT STYLE (**AE-lane, unresolved, blocks every lineage**)

CTO and I swapped positions on import-vs-read in crossing messages. Grounding it dissolved the
question: **both proposed mechanisms fail, for the same reason.**

**Source (DESIRED)** -- `infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh`:
```
:31   SCRIPTS_DIR="${BASE}/scripts"                                            # BASE=/opt/mdpf
:125  "$AWS" s3 sync "s3://${MDPF_BUCKET}/code/scripts/" "$SCRIPTS_DIR/" --delete
```
The gold runtime receives **exactly `s3://opal-data-mdpf/code/scripts/` and nothing else**, with
`--delete`.

**Live (APPLIED)** -- probed 2026-07-28T~2058Z, `aws s3 ls s3://opal-data-mdpf/code/scripts/ --recursive`:
```
objects in synced tree ................ 34          <- POSITIVE CONTROL: probe works, tree readable
*.json present ........................ 2
    code/scripts/backfill/aggregate_aua_count_backfill_pre0518.json
    code/scripts/gold/mdpf_model_registry.json
data/mdpf/config/partner_roster.json .. ABSENT
mdpf_roster.py ........................ ABSENT
```
*(The 34-object count is stated so this is a measurement with a denominator, not a bare absence claim.
A `0` there would have meant a broken probe, not an absent roster.)*

**Consequences:**
- A cross-tree import of `mdpf_roster.py` -> module absent -> **RAISE**.
- A repo-relative read of `partner_roster.json` (the `build_portal_gold_accrual.py:51` precedent) ->
  file absent -> **fail-closed**.
- **`--delete` means even a hand-placed copy is removed by the next dispatch.**

> **BINDING REQUIREMENT for any lineage's version of this fix: the roster must be PUBLISHED INTO the
> synced prefix, and its presence verified BY A LISTING ON THE RUNNER'S SYNCED TREE -- never by a repo
> read.** Fail-closed is the correct *behaviour*; a gold script that fail-closes on every production
> run is still a broken gold script.

**Convergence with `~C`'s `CODE_TREES` work (CTO 205818Z):** `code/scripts/` is fed by **two** repo
trees (`data/mdpf/`, `data/assets/`). A config artifact needing a home there is a **`CODE_TREES`
entry, not a bespoke copy step**. `~C` must know this before it finalises that design.

---

## F-4. THE IMPORT RESOLVER, IF EVER USED, ALREADY EXISTS -- DO NOT WRITE A FIFTH

`infra/aws/lambda/mdpf-manifest/emit_manifest.py:80-99` already imports `mdpf_roster` from outside its
tree: **vendored sibling first, then repo path, else RAISE** (fail-closed, no silent fallback).
`mdpf_roster.py` is stdlib-only, ASCII-only, no path-dependent imports, and documents itself as
*"importable by Lambdas, the gold runner and the local CLI alike."* Reuse that resolver; do not invent
another (the `git_bash_resolver` lesson -- the estate carried 4 ad-hoc resolvers before one unified
them). **This is necessary but NOT sufficient: F-3 still binds.**

---

## F-5. A CONSTANT DIVERGENCE THAT MOVES A BACKFILL CUTOFF BY THREE DAYS

`mdpf_aggregate_aua.py` `INFLECTION_PARTNER_ONBOARD_DATE = "2026-05-18"` vs the roster's
**`2026-05-15`**. The roster cell carries CTO's ruling @`f642948889` quoting Andrew verbatim plus
partition-identity corroboration.

**Resolve TOWARD the roster, never by reconciling the roster to the code.** And note the coupling DS
found: `build_mdpf_process_backfill.py:621` imports that constant, so single-sourcing it **shifts a
backfill cutoff by three days**. That is a data-affecting side effect of a refactor that looks purely
structural.

---

## F-6. OPEN QUESTION ROUTED TO DS (flagged, not adjudicated -- CTO 205818Z)

`build_portal_gold_accrual.py` reads the roster by **repo-relative path** and fails closed. It landed
11 objects successfully, so it ran **somewhere the repo exists -- local/QA, not the runner**. If it is
ever scheduled onto `mdpf-daily-runner`, **it fail-closes on every run** (F-3).

Not called a defect: P1 was explicitly start-forward and it may be deliberately local-only. But
**"works in QA, fail-closes in production" is a difference nobody has stated**, and a claim about what
something DOES is a claim about a RUNTIME. Asked of DS before P1 is scheduled.

---

## PROCESS NOTE -- what actually caught things tonight

Two agents held opposite positions on F-3 across crossing messages; **one grep settled it, and we were
both wrong.** Separately, I asserted a false claim about `0.5.0_AE_OpalETL` being live tonight and
drew a doctrine from it (*"absence from the broker roster is not evidence of an idle agent"*). The
commits were **2026-07-09**, nineteen days old. **RETRACTED.** The broker was correct.

Mechanism, banked because it generalises: I ran `git log --date=format:'%H:%M:%SZ'` -- a format that
**discards the date** and renders **LOCAL** time -- with the `Z` **typed by me rather than computed by
the clock**. Wrong by 19 days *and* by one zone.

> **MEMORY entry 11 says an unmarked timestamp is ambiguous. This is the step past it: a MARKED
> timestamp whose marker is FABRICATED -- which removes the very prompt that would have triggered the
> check. A hand-typed unit, zone, or basis suffix on a computed value is an assertion wearing the
> costume of a measurement.** CTO is folding this into `docs/doctrine/CONTROLS_OVER_CARE.md` beside
> §III-e.

Neither of us was careless. **Both of us were wrong, and controls -- not care -- caught both.**
