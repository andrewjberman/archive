# BRIEF — `comp-constants` as a gate surface: a hand-written roster enforcing a blocking gate

**To:** `1.0.0_SA_CTO` (base) · **CC:** `2.0.0_SA_COO`, `0.0.0_AB_MSTR`
**From:** `0.4.0_DS_ClientPlatform` · **Date:** 2026-08-05
**Trigger:** ANDREW-DIRECT, this terminal, 2026-08-05 ~20:4xZ. **VERBATIM:**

> "Need a brief on this too, comp-constants is a very questionable surface as a handwritten gate
> function that is hidden in the deep locking things up, need this brief delivered to CTO base"

**Scope discipline:** I surface, I do not adjudicate. He named a concern and a recipient; he did not
rule the remedy. Nothing here is a disposition — §7 lists options, and the ruling is CTO's.
**Grounding:** HEAD `8a8daae1a`. Everything in §§2–4 was measured today in the course of landing an
Andrew-ruled P0; where I am inferring rather than measuring, the line says `INFERRED`.

---

## 1. WHY THIS BRIEF EXISTS: IT BLOCKED A SOVEREIGN RULING DURING A LIVE OUTAGE

Today `comp-constants` **refused my commit** of the fix for a five-day INF gold-chain outage —
an Andrew-direct ruling (~1958Z, record `@93c898445`) that rep 10 belongs in Inflection scope.

```
BLOCKED: comp-constants drift detected on data/inf/scripts/gold/INF_D_04.client_portal_summary.py
DRIFT: 1 site(s) diverge from canonical_value
    actual:    {'10', '11', '3', '6', '12'}
    canonical: {3, 6, 11, 12}
```

**The gate was not detecting a defect. It was detecting that I had obeyed Andrew.** The "canonical"
value is a hand-typed literal in a YAML file; the world had changed and the literal had not. The
gate cannot tell those two states apart, and it fails in the blocking direction.

That is the concern in one screen, and it is the strongest single argument in this brief.

## 2. WHAT THE SURFACE ACTUALLY IS (plainly, because its shape is the issue)

- **File:** `comp-constants.config.yaml`, repo root, **706 lines**.
- **Scale:** **34 tracked constants, all 34 carrying an enforced `canonical_value`.**
- **Mechanism:** each entry hand-declares a constant's *value* as a string literal
  (`canonical_value: '{3, 6, 11, 12}'`) plus a `sites:` list. An AST scan compares every site's
  literal against it. Divergence = DRIFT.
- **Enforcement:** it runs **in-process inside `.tools/commit-gate.sh`** — the universal, all-agent,
  every-`.py`-edit gate (CLAUDE.md Rule 14). **It is blocking, on every Python commit, for every
  agent in the fabric.**

**So it is a value-freezing gate, wired into the most-travelled path in the estate.**

## 3. "HIDDEN IN THE DEEP" — MEASURED, NOT RHETORICAL

I have been the DS seat on this pipeline for months. **I did not know this surface existed until it
blocked me**, and I found it only by reading the refusal text.

- It appears in **no role-minimum table** in CLAUDE.md or `org/XXX.md`. The DS minimums name
  `comp-pipescript`, `comp-validate` — not `comp-constants`.
- It is not in the CLAUDE.md "Compiler Tools — situation → command" trigger table.
- It runs **in-process**, so it produces no separate tool invocation an agent would recognise.
- Its config sits at **repo root**, not under `org/modules/graph/` with the other comp-tool configs.

**A blocking gate that an owning-lane agent can operate beside for months without knowing it exists
is discoverable only by violation.** That is the literal meaning of "hidden in the deep," and it is
measured, not asserted.

## 4. THE STRUCTURAL FINDINGS

### 4.1 It is the "a predicate is not a roster" defect, instantiated *as a gate*

CTO ruled 2026-08-04: **a tool's universe must be a re-derived PREDICATE over the canonical graph,
not a hand-drawn allowlist.** `comp-constants` is a hand-drawn allowlist of *values*, enforcing
blockingly. It is the exact anti-pattern, sitting in the enforcement layer.

**Contrast — the shape that works, from today's other fix:** `_cot_carry_policy` reads cottonwood's
carry window out of `partner_roster.json` **at runtime**, and CTO's 230319Z ruling on it is explicit:
*read the window from the roster; do not hardcode 2, 3, or any date — a private copy of a roster value
is the sect-III-e defect.* **`comp-constants` is a private copy of 34 roster values, and it is the gate.**

### 4.2 THE LANE DEADLOCK — the sharpest finding, and it is structural, not incidental

- `comp-constants.config.yaml` is owned-paths lane **`ANY_EXEC_OR_AE`**.
- **DS is not a permitted agent.** Measured today: the owned-paths hook refused my commit.
- **But DS owns `data/*/scripts/{gold,silver,bronze}/*.py` under Rule 13** — the very files whose
  constants it gates.

**So the agent who is REQUIRED to change a constant is STRUCTURALLY FORBIDDEN from updating the gate
that governs it.** Every DS constant change is therefore a guaranteed two-agent transaction or an
audited lane override. That is not an edge case — it is the default path for the lane that owns the
most gated files.

Today's live consequence: my fix is committed (`8a8daae1a`) and the canonical bump **is not**, so the
committed estate is internally inconsistent right now, and I have had to route the decision rather
than land it. *(I declined to self-authorize the override; that call is with COO.)*

### 4.3 One real-world fact required THREE hand edits, because the roster is aliased

The Inflection rep roster is tracked as **three separate constants**, each with its own
`canonical_value`:

| tracked name | site |
|---|---|
| `INFLECTION_REP_IDS` | many |
| `PARTNER_REP_IDS['inflection']` | `convert_orion_to_silver.py` |
| `INFLECTION_EXTENDED` | `verify/shape_check.py` |

One sovereign ruling → three manual canonical bumps → and the gate blocks until **all three** are
done. **N aliases means N hand edits per real-world change, and the gate's failure mode on an
incomplete sweep is to block, not to guide.**

*(Fairly: this aliasing is a defect in the SOURCE, not created by comp-constants. But the gate
multiplies its cost, and it is the gate that stops work.)*

### 4.4 THE TOOL DOCUMENTED THIS EXACT FAILURE TWO WEEKS AGO, ON THIS EXACT CONSTANT

`comp-constants.config.yaml` header, **BL-1**, CTO-instructed 2026-07-22 — verbatim:

> "comp-constants cannot distinguish a RATIFIED divergence from DRIFT. A deliberate, signed-off
> difference has nowhere to live but a prose `notes:` string the gate does not read, so the tool
> re-reports it forever. **>> THAT IS HOW A REAL GATE BECOMES NOISE PEOPLE SCROLL PAST. <<** The
> failure is not a false positive — every report is TRUE. It is that a gate which cannot express
> 'known, accepted' trains its readers to skim, and a skimmed gate is a dead gate that still looks
> alive. THE GATE IS NOT WRONG, IT IS INEXPRESSIVE."

And its named **LIVE INSTANCE** is:

> "the 7 inf-lane drifts surfaced 2026-07-22 … (5x `INFLECTION_REP_IDS` + `GUARD_B_AUA_LOWER/UPPER`
> …) routed to `0.4.0_DS_ClientPlatform`. Some may be ratified; the tool cannot say which, so it
> cannot stop re-reporting the ones that are."

**The instrument named `INFLECTION_REP_IDS` as its own unresolvable case two weeks ago, routed it to
my seat, and today blocked a sovereign ruling on that same constant.** The declared fix — a per-site
`exempt:` carrying who ratified it, when, and why — is marked **"(not built)"**.

**BL-2** additionally records that `check` **cannot state its own coverage denominator** on full
scans (57 out-of-surface files surface only when touched). By this estate's own doctrine — *print the
denominator of every scan you reason from* — that is a gate that cannot say what it did not look at.

### 4.5 It reports production and non-production sites at identical severity

Post-fix, remaining drift includes seven `data/inf/manual_api/` entries — ad-hoc query/probe tools,
not the chain — reported exactly like a live gold-script filter site. Two of them
(`pull_inflection_assets.py [3,11,12]`, `pull_inflection_transactions.py '3,11,12'`) have been
drifted since rep 6 landed **2026-05-07** — roughly three months of a true, un-actioned report.
Also flagged: `GUARD_B_AUA_LOWER/UPPER` at 50M/400M vs canonical 150M/300M in `inf-api-txn` — plausibly
a legitimate per-function bound, but the gate has no way to say so. **This is BL-1 in the wild:
every report true, none dismissible, so the set is skimmed.**

## 5. IN FAIRNESS — WHAT IT GOT RIGHT TODAY, AND IT IS NOT SMALL

**The gate caught a real, incomplete fix of mine.** My own search was name-keyed on
`INFLECTION_REP_IDS` and would have missed `INFLECTION_EXTENDED` and the `PARTNER_REP_IDS` dict
entirely. `comp-constants` refused, and that refusal is why all three aliases surfaced and why the
sweep is complete.

**A brief that argued for deleting this surface would be wrong, and I am not arguing that.** The
*detection* is genuinely load-bearing. The questionable part is that detection is implemented as a
hand-maintained copy of the values, in a lane the changing agent often cannot write, on the universal
blocking path, undiscoverable until violated.

**The mechanism found something true. The design makes every true finding expensive and every
legitimate change a blockage.**

## 6. THE SHAPE OF THE PROBLEM, STATED ONCE

> **A drift gate that encodes the VALUE must be hand-updated every time the world legitimately
> changes — so it converts every correct change into a gate failure plus a config edit, possibly in a
> lane the changer does not hold. A drift gate that encodes the DERIVATION does not.**

`comp-constants` freezes *what the value is*. The roster/`_cot_carry_policy` pattern declares *where
the value comes from*. Only the second survives contact with a world that changes — and reps get
reassigned, bounds get re-ruled, rosters grow.

## 7. OPTIONS FOR CTO — NOT RANKED AS A RECOMMENDATION, BECAUSE THE RULING IS YOURS

1. **Build BL-1's `exempt:`** (already designed, unbuilt): per-site ratification carrying WHO/WHEN/WHY,
   expiring loudly. Smallest change; fixes noise, **does not** fix the lane deadlock or the
   value-vs-derivation shape.
2. **Fix the lane grant** so the lane that owns the gated files can update the gate's config —
   or the inverse, move the config into a lane-neutral home. Directly addresses §4.2, which is the
   one that will recur on *every* DS constant change.
3. **Point `canonical_value` at a DERIVATION** (a declared-data file + key path, resolved at check
   time) rather than a frozen literal, for constants that have a real upstream authority. This is the
   `partner_roster.json` pattern and it would have made today a no-op.
4. **Demote from blocking to advisory** for non-production surfaces (`manual_api/`, probes), keeping
   blocking for gold/silver/lambda producers. Addresses §4.5 without weakening the real gate.
5. **Discoverability, regardless of the above:** put it in the CLAUDE.md trigger table and the DS/AE
   role minimums. Cheapest item here and it removes "hidden."

**Applicable law CTO may want to weigh:** new rules should ship WITH a gate, and *gates teach at
violation time* — this one does teach at violation time, but it teaches the wrong lesson, because the
violation was correct.

## 8. WHAT I DID NOT DETERMINE

- **Whether the 34 tracked constants are individually well-chosen.** I examined the INF rep family and
  the GUARD_B bounds. The other ~30 are unassessed.
- **How often this gate has blocked other agents.** Unmeasured. `INFERRED` from BL-1's own text that
  re-reporting is chronic, but I did not count incidents and nobody should quote a rate.
- **Whether `ANY_EXEC_OR_AE` is the right lane** for this config — only that DS's exclusion from it,
  combined with DS's Rule-13 ownership of the gated files, is a structural deadlock.
- **Whether option 3 is implementable** for all 34 constants; some may have no declared upstream
  authority to point at.
- **I did not touch the tool or its config beyond today's three canonical bumps**, which remain
  uncommitted pending COO's lane decision.

---

*Delivered per Andrew-direct instruction, 2026-08-05, to `1.0.0_SA_CTO` base. Recorded + broadcast
same turn per the record-and-broadcast law.*
