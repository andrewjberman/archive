# FINDING — comp-which TO-1: a catalog-derived probe set measures the CATALOG, not the instrument

**Author:** `2.0.0_SA_COO~Z` · **2026-07-13** · **archetype:** VALIDATE
**Against:** `docs/architecture/NFRA_COMPASSURANCE_COMPWHICH_TOPK.md` (PRD v0.1 `ea41572cb` → v0.2 `98a3ad2b4`), §6 TO-1
**Vintage of every citation below:** `.tools/comp-which` @ `52d008f4c`. *A line citation without a vintage is not a citation.*
**Disposition:** TO-1's probe-generation method is **anti-correlated with the defect it exists to measure.** Amended cohort design proposed. **The PRD's architecture, its abstain-before-ranking order, and F-1 all SURVIVE.**

---

## 0 — My own instrument lied first. The control caught it, not my care.

The first run of this measurement reported catalog zero-rate `0.0%`, **gibberish zero-rate `0.0%`**, mean scores 33–42.
**Gibberish cannot legitimately score 33, and that impossibility is the only reason this finding is not itself garbage.**

`RULES` entries are tuples `(keywords_list, description, ...)`. I passed `r[1]` — the description **string** — as the keyword
list. `_score_rule` then iterated its **characters**, hit the space character, matched `if " " in kw` as a "phrase," and
awarded **+3 per space in the description.** Every number in that first table was a **space count** formatted as a score.

> **I did not catch this by being careful. I caught it by running a generated gibberish control and looking at what came back.**
> *Care is not a control. Care is what you have instead of one.*

Corrected instrument, **both controls run in isolation** (Rule 22a: a control batched with the target is corrupted by its
own presence):

| Control | Result | Required |
|---|---|---|
| POSITIVE — `"what breaks if I change this function"` | score **5** | `> 0` ✓ |
| GIBBERISH — 40 generated nonsense strings | **40/40 ZERO**, mean 0.00 | ~100% zero ✓ |

Scorer = comp-which's **own** `_score_rule` over its **own** `RULES` (n=46), loaded from the binary. Not a reimplementation.

---

## 1 — The finding

TO-1 generates one probe per catalog entry **from that entry's own `use_case` text**. I verified the precondition:
**66 entries, 66/66 carry `use_case`, 38 distinct tools.** The precondition is TRUE and **the method is still wrong.**

**A probe drawn from a catalog entry's own description, scored against a catalog built from that same text, measures
STRING SELF-IDENTITY — not routing quality.** It cannot reproduce the live defect, because the live defect *is* that
**agent vocabulary ≠ catalog vocabulary**. A catalog-derived probe is, by construction, phrased the way the catalog is.

The PRD is right that *"a hand-chosen probe set measures the AUTHOR, not the instrument."* The successor inherits the
same structure: **a catalog-derived probe set measures the CATALOG'S SELF-CONSISTENCY.** It scores best exactly where the
catalog is most self-referential — which is where real agents are least likely to match it.

> **It does not merely fail to see the hole. It is brightest where the hole is deepest.**

### Measured (RULES layer, n=46; zero-score rate = the label-free coverage metric)

| Cohort | Source | n | ZERO-score | Rate | mean |
|---|---|---|---|---|---|
| **C** | catalog `use_case` — **TO-1's proposed probe source** | 66 | 12 | **18.2%** | 5.65 |
| **R** | **ORGANIC TAIL — real agent questions** (rail log, deduped) | 347 | 154 | **44.4%** | 2.17 |
| **G** | generated gibberish (control) | 40 | 40 | **100.0%** | 0.00 |

**TO-1 as specified would report an ~18% coverage hole. The real hole on actual agent traffic is ~44%.**
**It understates the defect it exists to measure by 2.4×** — while printing an honest-looking denominator, which is worse
than not measuring at all, because **TO-2 and TO-3 would then be graded against the flattering number.**

The PRD's 12 hand-written probes said **25%**. Catalog-derived says **18.2%**. Reality says **44.4%**.
**Both candidate methods understate it, in the same direction, for the same structural reason.**

### Real agent questions scoring ZERO across all 46 rules — none of these are edge cases

```
what lambdas read the inflection gold bucket
what serves inf ADVI AUA for the 49F firm?
what state machine invokes which lambdas
tools for the git committed surface
trino federation query tool
```

Each is a legitimate estate question. Today each receives **an arbitrary tie-break on list order, formatted as a
confident answer.**

---

## 2 — The denominator. The 98.8% headline SURVIVES; "6,308 routing decisions" does not mean what it reads like.

*Rule 22: print the denominator of every scan you reason from.* Decomposing the PRD's:

```
  6,308  ROUTE events              <- the PRD's stated denominator
    475  DISTINCT questions        <- same traffic, deduplicated (~13x duplication)
    347  ORGANIC-TAIL singletons   <- distinct, seen once, catalog text removed
```

The bulk is a **synthetic self-probe**: single questions repeated **85–133×**, in **60–71/minute** bursts (machine pacing,
not agent pacing), **64% of all routes on one day** — and the repeated strings are **verbatim catalog `use_case` text**
(`"Gold script I/O, chain membership, deployed-match, overlap"`).

> **Therefore the catalog-`use_case`-probe experiment TO-1 proposes HAS ALREADY BEEN RUN.** It is ~6,000 of the 6,308 rows
> **in the very log TO-1 would be measuring.**

**And the headline holds — tested against the finding, not for it:**

| | |
|---|---|
| `ROUTE-POSTERIOR` / all events | 6230/6308 = **98.8%** (PRD) |
| distinct questions taking POSTERIOR | 462/475 = **97.3%** (deduped) |

**97.3% vs 98.8% — robust to deduplication. The unfloored path IS the live path.** F-1 independently source-confirmed by
me at HEAD: `:1073-1074` prints the subjunctive, `:1075` `return 0` unconditionally, `STRONG = 4` sits at `:1221`,
downstream and unreachable. **The mechanism claim is sound; only the evidence-base framing was inflated. Fix the framing, keep the finding.**

---

## 3 — Amended TO-1: three NAMED cohorts. The headline metric needs NO labels.

**"What fraction of real agent questions score zero against the catalog" requires no ground-truth labels at all.** No hand-
labeling, no author judgment, nothing to argue about. It is the coverage number, and it is free.

| Cohort | Role |
|---|---|
| **R — REAL / HEADLINE** | de-duplicated organic tail from `comp-which-rail.log` (~347, growing). Metric: **zero-score rate. LABEL-FREE. THE number.** A denominator nobody on this project authored — **because agents wrote it, not us.** |
| **C — CATALOG / FLOOR** | generated from `use_case`. Labeled by construction. A **self-consistency check, explicitly NOT the headline.** If C is not near-ceiling, that is its own finding: *the catalog cannot retrieve itself.* |
| **G — GIBBERISH / CONTROL** | generated. **The harness FAILS if any gibberish probe returns a route.** |

**MANDATORY de-contamination of Cohort R (must be an acceptance criterion).** The organic tail contains **agents' own
gibberish probes** (`xyzzy_unlikely_token_12345`, `asdkfjhaskdjfh`) — agents were already hand-probing this tool. Those
legitimately score zero and *should*. **So 44.4% slightly OVERSTATES the genuine hole and that exact digit is not
defended.** Strip known probe tokens and re-report. **The 2.4× direction is not in doubt; the third significant figure is.**

**LAYER PRECISION — no TO may restate this wrongly.** This measured the **RULES layer (n=46)**, where the gibberish control
**passes** (100% zero), independently confirming PRD §2.3. **The live gibberish MIS-ROUTE happens further down, in the
POSTERIOR / manifest-fuzzy-backstop layer** (`_manifest_matches`, `overlap >= 2`).

> **So the harness MUST measure the LIVE BINARY'S ROUTE, not only the RULES score** — or it grades a layer that is not the
> one failing. **This is F-1 (the guard exists; the live path never reaches it) applied to the harness itself.**

**FALSIFIABLE PREDICTION (so this finding can be killed cheaply):** if Cohort C's zero-rate is close to Cohort R's, the
finding is wrong and TO-1 stands as written. **Measured: 18.2% vs 44.4%. Not close.** Show the cohort split is contaminated
in a way that closes that gap and I withdraw.

---

## Appendix — reproduction (exact, as run)

```python
import re, collections, types, random, yaml, os
src = open('.tools/comp-which', encoding='utf-8').read()
mod = types.ModuleType("cw"); mod.__name__ = "cw_not_main"
mod.__file__ = os.path.abspath('.tools/comp-which')
exec(compile(src, '.tools/comp-which', 'exec'), mod.__dict__)
RULES, score, _tokens = mod.RULES, mod._score_rule, mod._tokens   # keywords are r[0], NOT r[1]

def best(q):
    qt = _tokens(q)
    return max([score(q.lower(), qt, r[0]) for r in RULES] or [0])

# COHORT C — catalog use_case
d = yaml.safe_load(open('org/modules/graph/graph-call-manifest.yaml'))
uc = [e['use_case'] for e in (d.get('entries') or []) if e.get('use_case')]

# COHORT R — organic tail: rail-log questions seen exactly once, catalog text removed
qs = collections.Counter()
for line in open('org/mcp/comp-which-rail.log', encoding='utf-8', errors='replace'):
    if 'ROUTE-' not in line:
        continue
    m = re.search(r'q="([^"]*)"', line)
    if m:
        qs[m.group(1)] += 1
catalog_pref = {u.strip()[:60] for u in uc}
cohortR = [q for q, c in qs.items() if c == 1 and q.strip()[:60] not in catalog_pref]

# COHORT G — generated gibberish control (MUST be ~100% zero, else the instrument is lying)
random.seed(7)
cohortG = [' '.join(''.join(random.choice('abcdefghijklmnopqrstuvwxyz')
           for _ in range(random.randint(4, 9))) for _ in range(random.randint(3, 6)))
           for _ in range(40)]

for name, co in [("C catalog", uc), ("R organic", cohortR), ("G gibberish", cohortG)]:
    sc = [best(q) for q in co]
    z = sum(1 for s in sc if s == 0)
    print("%-12s n=%-4d ZERO %3d = %5.1f%%  mean=%.2f" % (name, len(co), z, 100*z/len(co), sum(sc)/len(sc)))
```

**The `r[0]` comment is the whole lesson: `r[1]` is the description string, and passing it silently counts spaces as
phrase matches. A passing assertion that was never mutated has never been tested.**
