# BD Rebalancer — Strategies comprised of Opal-named models (live scan)

**Author:** `0.7.0_AE_CloudOps~Z` · 2026-08-07 ~04:3xZ
**Authorization:** Andrew-direct per-use vendor egress, this terminal, READ-ONLY.
**Scope actually exercised:** `rebalancer.bdreporting.com` — `GET /auth/token`,
`POST /api/models/strategies/search`, `GET /api/models/{id}` ×62. **Tenancy:
`blackdiamond/cot/session` (COTTONWOOD).** Cookie read via GetSecretValue only, bearer minted
in-memory and dropped; **nothing written** — no S3, no secret write, no bronze landing.
**Denominator: 62 strategies (declared totalResultCount 62), 62/62 details pulled, 0 failures.**
**Independent cross-check:** landed bronze `blackdiamond/cottonwood/bronze/rebalancer_models/2026-08-06/`
— same 62, same 20 Opal-named, zero drift. The live scan is corroborated, not self-attested.

---

## 1. Headline

| Set | Strategies | Accounts |
|---|---|---|
| Opal-COMPOSED (≥1 Opal-named child model) | **19** | **300** |
| Opal-NAMED but leaf (own securities, no Opal children) | 3 | 8 |
| **Total Opal-touching** | **22** | **308** |
| — of which SATELLITE family | 13 | 293 |
| — of which **OUTSIDE Satellite** | **9** | **15** |
| No Opal anywhere | 40 | — |

**Andrew's read is confirmed by the scan: 9 Opal strategies / 15 accounts sit OUTSIDE the
Satellite family.** They are a small share of accounts (~5%) and a large share of *shapes*
(9 of 22 distinct strategies) — which is why a Satellite-shaped tracking model misses them.

## 2. The untracked set, named

**Opal-composed, non-Satellite (6 strategies, 7 accounts):**

| Strategy | Accts | Built from |
|---|---|---|
| Opal Ultra Short Term | 3 | Opal Ultra Short-Term Income |
| Opal - Beecherl Legg | 1 | Opal Conservative Growth (0.79), Opal Ultra Short-Term Income (0.21) |
| **Anna \*9237** | 1 | Opal Conservative Growth (0.36), **Opal Fixed Income (0.21)**, Opal Ultra Short-Term Income (0.33), + DIVZ SMA (0.07) |
| **Anna \*9238** | 1 | Opal Conservative Growth (0.607), **Opal Fixed Income (0.16)**, Opal Ultra Short-Term Income (0.2) |
| Opal 66% Long Term / 34% UST | 1 | Opal Conservative Growth (0.66), Opal Ultra Short-Term Income (0.34) |
| Opal Long Term Conservatiove *(sic)* | 0 | Opal Conservative Growth |

**Opal-named leaf strategies (3 strategies, 8 accounts)** — hold securities directly, no Opal
child models, so a composition-based scan alone would miss them: `Opal Moderate Income
Portfolio` (6), `Opal - Income` (2), `Opal Long Term Aggressive` (0).

⚠ **Neither Anna strategy carries "Opal" in its own name** — they are findable ONLY by
composition. Any tracking keyed on the strategy NAME is structurally blind to them.

## 3. The mechanism finding — why the Anna portfolios would mis-count even if tracked

The Opal building blocks used across the whole book, with usage counts:

| Child model | Used by | In `mdpf_revamp_model_crosswalk.py`? |
|---|---|---|
| Opal Intermediate-Term | 9 | tracked (`opal_intermediate`) |
| Opal Conservative Growth | 8 | tracked (`opal_long_term_conservative`) |
| Opal Ultra Short-Term Income | 8 | tracked (`opal_ultra_short_term`) |
| Opal Short-Term | 7 | tracked (`opal_short_term`) |
| Opal Long-Term Aggressive | 2 | tracked (`opal_long_term_aggressive`) |
| **Opal Fixed Income** | **2 (both Anna portfolios)** | **ABSENT — 0 hits** |

Grep denominators: `"Opal Conservative Growth"` = 2 hits (POSITIVE CONTROL, so the search
discriminates); `"Fixed Income"` = **0 hits** in the crosswalk.

**Why it matters, grounded in observed live behavior:** tonight's gold runs logged
`WARN candidate-NEW-Opal model excluded (not in crosswalk): eclipse_id=31 name='90/10 Opal
Intermediate/Ultra Short Term' -- review for crosswalk add (F5). Folded into non_model this
run.` An Opal model the crosswalk does not know is **folded into NON-MODEL** — i.e. Opal
exposure counted as non-Opal AUM.

⚠ **CLAIM SCOPE, deliberately narrow:** what is established is that the *name* "Opal Fixed
Income" is absent from the crosswalk. The crosswalk is **model_id-keyed** and its display
names are SmartX-side, and it documents at least one alias of exactly this kind
(`opal_long_term_conservative` = SmartX display "Opal Conservative Growth", NOT "Long-Term
Conservative"). So **"Opal Fixed Income" may be a BD-side alias of a tracked model rather
than a genuinely untracked one — resolving that needs the model_id tie, which is the
crosswalk owner's call (DS~Z), not mine to assert.** Reported as a candidate, not a defect.

## 4. Also observed (recorded, not chased — §0 discipline)

- Two MIXED strategies blend Opal with non-Opal sleeves: `Anna *9237` carries DIVZ SMA (0.07);
  `Blended Opal / Satellite 50` is only ~25% Opal (Intermediate 0.1875 + Short-Term 0.0625)
  against Equity/Tax-Free Bond/Money-Market sleeves (0.75).
- **All six Opal building-block models are child-only — none appears in the 62-strategy
  roster as a top-level Strategy.** A roster-level scan alone never sees them.
- Data hygiene, BD-side: `" Anna *9238"` has a **leading space** in its name;
  `"Opal Long Term Conservatiove"` is misspelled. Both are exact-name-match hazards for any
  tracking keyed on strings.
- The runner docstring records discovery ground truth as *"296 Opal across 14 models"*; the
  live plane today reads **300 accounts across 19 composed strategies** (308/22 incl. leaves).
  Drift datapoint for whoever owns that baseline — the deployed gate reconciles per-strategy
  counts, not this number, so nothing is failing on it.

## 5. What was NOT done

No writes of any kind. No schedule/infra touched. No crosswalk edit. The 49F tenancy
(`blackdiamond/49f/session`) was **not** queried — this scan is Cottonwood-only, and a
49F-side equivalent would be a separate authorized run.
