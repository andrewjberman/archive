# Cottonwood Backtest-Projection (Pre-Creation Hypothetical Series) — Design Spec

**Author:** `4.0.0_SA_CRO` (Chief Research Officer) · **Home:** `org/tier1_exec/4.0.0_SA_CRO/` · **Date:** 2026-07-23
**Chain (Andrew-ordered):** this spec → **`3.0.0_SA_CVO` tandem review** → **`2.0.0_SA_COO` decomposition.** CTO + COO CC.
**Companion:** CTO's Global-aggregation half (the third class enters the same incumbent provenance channel). CTO owns the
Global aggregator; this spec owns the METHOD + the per-firm emission.
**Egress:** NONE used in design. **One net-new dependency flagged (ETF price history) with an egress decision — §7.**
**Grades:** **[GROUNDED]** read at source · **[PROVEN]** computed prior · **[PROPOSAL]** design, CVO's to review ·
**[DECISION]** needs Andrew/CTO.

> **One line: for dates BEFORE a model existed, compute what its composition *would have been worth* from ETF price
> history — a hypothetical performance series that NEVER claims to be actuals, carried as a THIRD provenance class
> (`backtest_projection`) in the same channel as measured/interpolated, in its own visual style, with the composition
> vintage stated per date. It is the honest way past the 05-28 ceiling: not by pretending there were assets, but by
> showing how the strategy would have performed.**

---

## 1. Authority + where it sits

**Andrew-direct (via CTO 045749Z):** *"This is a good start but we need to figure out the backstest projection and
also the 'Global' view aggregation."* The Global half is CTO's; the **backtest-projection design is mine.** It completes
the three-band model on the page:

| Band | Provenance | Meaning | Where |
|---|---|---|---|
| solid | `measured` | actual model AUM | forward (~07-21+), and recovered dates |
| yellow-dashed | `interpolated_estimate` | estimated ACTUAL model AUM (real accounts, fuzzy assignment) | the migration gap (~05-28→07-21) |
| **third style (§4)** | **`backtest_projection`** | **HYPOTHETICAL composition performance — no real assets** | **pre-creation (< model createdAt)** |

**The 05-28 structural ceiling stands for the first two classes** (there were no actual Opal-model assets before the
models existed). **The backtest is the honest way past it precisely because it never claims to be actuals** — it is a
"how this strategy would have performed" line, not an assets-under-management claim.

---

## 2. What the backtest IS, and IS NOT **[the honesty spine]**

| | |
|---|---|
| **IS** | The model's composition (its ETF basket + weights) valued over historical ETF prices — a hypothetical performance/value series for dates before the model existed. Clearly labelled, its own visual style. |
| **IS NOT** | An assets-under-management claim. There were **no accounts, no book, no AUM** before the model existed. It never enters a measured channel, never blends into an interpolated-actuals point, never feeds fee-basis / identities / DDB. **A date carries exactly ONE class.** |

**This is the standard "hypothetical historical performance" disclosure every asset manager uses for a strategy that
post-dates the period shown — and it carries the same obligation: labelled hypothetical, never actual.**

---

## 3. The third provenance class — extends tonight's signed machinery, does not reinvent **[CONTRACT, per CTO envelope]**

`backtest_projection` joins the **incumbent** provenance enum in the SAME channel (CTO R-1 vocabulary):
`measured | interpolated_estimate | backtest_projection | absent` — one **additive** enum extension (frozen-additive
legal), one more derived `point_class`. Structural guarantees are **the ones already built** (no new machinery):
- **Same compute-quarantine (§3 of the interpolated spec):** every measured-only consumer filters on the provenance
  value; `backtest_projection` is filtered out exactly as `interpolated_estimate` is. One filter predicate, one channel.
- **`point_class` taint:** a Global point is `backtest_projection`-class only where ALL contributing firm/model cohorts
  are backtest (a backtest point never mixes with measured/interpolated on the same date — the one-class-per-date rule).
- **`backfill_method`** carries the method id + **the composition vintage (§5)** — the honesty-critical field here.
- **`confidence` sibling:** the backtest has NO assignment uncertainty (no accounts to assign) — so washout-confidence
  does NOT apply. Its honesty statement is the **composition-vintage label**, not a scalar (§5/§8). Emit `confidence`
  null (or a reserved `n/a`) and carry the vintage in `backfill_method` — do not manufacture a washout number where the
  uncertainty is of a different kind.

---

## 4. The MECHANISM **[PROPOSAL]**

For a model `M` with terminal composition weights `w_i` over ETFs `i` (GROUNDED: the compositions decompose to liquid
ETFs — e.g. Conservative Growth = DIVZ 14.45% + CLIP 0.74% + CASH 0.99% + …; §10), and a pre-creation date `d`:

**Step 1 — composition growth index** from ETF price history:
```
CompIndex(M, d) = Σ_i  w_i × ( price_i(d) / price_i(d_base) )
```
(total-return prices where available; price-return + a note otherwise — a labelled method choice, §5.)

**Step 2 — anchor to the real series for visual continuity (recommended):**
```
backtest_value(M, d) = first_real_value(M) × CompIndex(M, d) / CompIndex(M, createdAt(M))
```
so the backtest line **meets** the interpolated/measured line at `createdAt(M)` — one continuous curve, three styles.

> **HONESTY CAVEAT ON THE ANCHOR (state it in the product):** this scales the composition's *performance* to connect to
> the first real value. It is **"how a book of this strategy would have performed,"** NOT a claim there were assets. The
> anchored form is for visual continuity; the underlying truth is a **performance index**, not AUM. **RECOMMENDED
> ALTERNATIVE for maximum honesty:** render the backtest band on a **rebased performance basis** (growth-of-$1) visually
> distinct enough that no one reads it as dollars — Andrew/CTO to choose continuity-vs-purity. I lean anchored-with-
> strong-visual-distinction: continuous line, unmistakable style, explicit "hypothetical" legend.

**No accounts, no fuzzy match, no assignment** — the backtest is pure composition math on prices. So the fingerprint/
assignment concerns do not arise here; the ONLY honesty risks are (a) mislabelling it as actual (guarded by the class),
and (b) the composition-vintage assumption (§5).

---

## 5. COMPOSITION VINTAGE — binds hard (CTO v1.2 binding, load-bearing here) **[GROUNDED / DECISION]**

A backtest computed with TODAY's weights over June prices is a **specific labelled choice.** The spec must state which
vintage per date and carry it in `backfill_method`:
- **Dated compositions:** `fact_model_blend` / `model_detail` history is **live-state only** (no pre-07-21 partitions) —
  so dated pre-creation compositions **do not exist** (the model didn't exist, so neither did its composition).
- **Therefore the only available method is CURRENT-COMPOSITION-HELD-CONSTANT** — and it is **legal ONLY as a labelled
  method** (CTO point 3). It is **defensible** here on measured grounds: `0.6.2`'s B6 finding established the *structural*
  blend is stable (the daily model_detail movement is price REVALUATION, not composition edits). So holding the current
  structural composition constant backward is a bounded assumption, not a wild one — but it IS an assumption, and the
  `backfill_method` field states it verbatim: `backtest_current_composition_held_constant_YYYYMMDD`.
- **Consequence to disclose:** the backtest shows how *today's* composition would have performed historically — a
  legitimate and standard hypothetical, labelled as such. It does not claim the model's composition was the same then
  (it didn't exist then).

---

## 6. BOUNDARY — one class per date, keyed on the real createdAt **[GROUNDED]**

Per model `M`, the boundaries are **the real `createdAt(M)` from bronze `rebalancer_model_detail`** (my createdAt
finding — stable 22/22 across partitions, a real birth date; the interpolated spec's floor input):
```
d <  createdAt(M)                 -> backtest_projection     (hypothetical; no assets existed)
createdAt(M) <= d < first_measured -> interpolated_estimate   (real accounts, fuzzy assignment — the migration gap)
d >= first_measured               -> measured
```
**No date carries two classes.** The backtest ends exactly where actuals (interpolated or measured) begin, per model.
This is why the createdAt must be the REAL bronze birth date, not `last_update` (the revaluation stamp) — same Rule-17
sourcing note as the interpolated spec.

---

## 7. ETF PRICE SOURCE — GROUNDED: NOT in-estate as a dedicated source **[GROUNDED / DECISION for Andrew]**

Per CTO point 5, grounded before proposing egress. **What exists in-estate:** `opal-market-data-v2` + `opal-market-update`
carry **FRED macro series only** (bond/credit indices, oil, FX — read at source) — **NOT ETF close prices.** A search for
the models' actual tickers (DIVZ, CLIP, BIV, IEFA, JAAA, …) across both buckets returned **nothing.** So a dedicated ETF
price history is **not in-estate.** Three options, ranked:

1. **DERIVE from our OWN holdings history (in-estate, ZERO egress) — recommended to try first.** The daily holdings
   snapshots carry per-security **market value AND units** → `price_i(d) = MV_i(d) / units_i(d)` for any ETF we held on
   `d`. **Coverage limit:** only dates/ETFs actually held — cot holdings reach ~06-08, so this covers the ~05-28→06-08
   sliver directly and little before. **For a backtest that reaches further back (which is the point), it is insufficient
   alone** — but it is a free, in-estate cross-check for the overlap window and should anchor any external series.
2. **A public free ETF price source** (the compositions are ~15 liquid, publicly-traded ETFs; daily closes are public
   data). This is **not client data and not a competitor API** — a different egress category than the vendor prohibition.
   **Andrew/CTO decision:** whether a public market-data pull is in-policy without a per-use vendor word.
3. **`ycharts` (has full ETF history) — vendor egress, Andrew's explicit per-use word REQUIRED** every time (standing
   prohibition; availability is not authorization). Only if 1+2 are ruled out.

**RECOMMENDATION:** derive-from-holdings for the overlap cross-check (free), and route the **pre-06-08 price source as a
DECISION to Andrew/CTO** — public-source vs ycharts-egress. **The backtest cannot be built past ~06-08 without one of
them; naming that gate is part of the honest spec, not a detail to paper over.**

---

## 8. Validation the build must carry **[PROPOSAL]**

1. **Class exclusivity:** assert no date carries two provenance classes per model (backtest ends exactly at createdAt).
2. **Never-measured guard:** a `backtest_projection` point is REJECTED by every measured-only consumer and renders only
   in the backtest style (the same mutant CVO runs for interpolated, extended to the third class).
3. **Vintage stamped:** every backtest point carries the composition-vintage `backfill_method`; a backtest point with a
   null/absent vintage fails LOUD (the vintage is the honesty statement — it cannot be missing).
4. **Anchor continuity:** the backtest value at `createdAt` equals the first real value (the anchor is exact; a
   discontinuity at the seam is a method artifact to flag).
5. **Price-source provenance:** each backtest point records which price source produced it (holdings-derived vs external),
   so a mixed-source series is legible.

---

## 9. Proposed / held / decided — by whom

- **PROPOSED (CRO):** the method above — composition × ETF price history, anchored, current-composition-held-constant
  (labelled), pre-createdAt only, as the third provenance class in the incumbent channel.
- **DECISIONS (Andrew / CTO):** (a) the ETF price source — public-pull vs ycharts-egress vs holdings-derived-only-and-
  accept-the-~06-08-floor (§7); (b) anchored-AUM-continuity vs rebased-performance-purity for the visual (§4); (c) the
  backtest visual style (I propose **desaturated/grey DOTTED** — certainty rank solid > dashed > dotted, and grey reads
  "not your assets" — with a legend *"Backtested — hypothetical composition performance, not actual assets"*).
- **FOR CVO TANDEM REVIEW:** the class-exclusivity + never-measured guards (§8), and the composition-vintage-as-honesty-
  statement (§5) — is the label sufficient that a hypothetical can never be read as actual? The same pinned-delta process
  as the interpolated spec.
- **NOT this spec's to do:** build, dispatch, the Global aggregator (CTO's), or the price-source egress decision.

---

## 10. Grounding

**[GROUNDED]** model compositions decompose to liquid ETFs with weights (bronze `rebalancer_model_detail.hierarchy`,
read this session: e.g. Conservative Growth = DIVZ 14.45% + CLIP 0.74% + CASH 0.99% + …; Sat-50 = Intermediate 75% +
Short 25% → their ETFs) · createdAt stable/real per model (the interpolated-spec finding) · `opal-market-data-v2` /
`opal-market-update` carry FRED macro only, NO ETF prices (S3 read) · holdings snapshots carry MV + units → derivable
prices (prior grounding) · B6 structural-blend stability justifies current-composition-held-constant (0.6.2). **[PROVEN]**
B1/B2 terminal compositions + weights. **[PROPOSAL]** the anchored composition-index method, the visual style, the
confidence-is-a-vintage-label choice. **[DECISION]** the ETF price source (§7) + the continuity-vs-purity visual (§4).

**One-line:** a labelled hypothetical — today's composition valued over historical ETF prices, anchored to the real
series, never called actuals — as a third provenance class in the same channel; the honest content is real (composition
+ prices), the honest label is `backtest_projection`, and the one real gate is where the ETF prices come from before
~06-08.
