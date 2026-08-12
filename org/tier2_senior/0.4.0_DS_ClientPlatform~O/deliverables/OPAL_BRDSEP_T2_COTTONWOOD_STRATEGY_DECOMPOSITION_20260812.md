# OPAL_BRDSEP.T2 — Cottonwood: the 18 Strategies decomposed by constituent Model

**Author:** `0.4.0_DS_ClientPlatform~O` · 2026-08-12
**TO:** `OPAL_BRDSEP.T2` @`cbf5a9d63d`, **narrowed by CTO `[STOP]` 1933Z** (operative spec)
**Type:** Measurement. Changes no served artifact; `platinum/` read-only.
**Determinism:** decomposition re-run and diffed; figures reproduce.

---

## 0. Andrew-direct, VERBATIM (2026-08-12 ~1925Z, CTO terminal)

> *"It is specifically for the group of 'Strategies' i sent from the Cottonwood Rebalance endpoint.
> I want to know the full value of those 'Strategies', broken out by its constituent 'Models' of which
> i want a total from anything tagged 'Opal' and the balance of the strategy with anything non-Opal
> Model."*

**One firm. Two levels. Level 1 = the 18 strategies' value. Level 2 = the constituent models inside
them, split into an Opal-tagged subtotal and the balance.**

---

## 1. THE ANSWER

| | Value | as-of |
|---|---:|---|
| **Full value of the 18 Strategies** | **$187,928,913.13** | 2026-08-10 |
| — the 16 whose composition we hold | $141,392,564.43 | |
| — **the 2 we cannot decompose** (`Anna *9237`, `Anna *9238`) | **$46,536,348.70** | |
| **Of the decomposable $141,392,564.43:** | | |
| — **OPAL-tagged constituent subtotal** | **$134,387,049.10** | |
| — **BALANCE (non-Opal constituents)** | **$7,005,515.33** | |

**The decomposition closes: $134,387,049.10 + $7,005,515.33 = $141,392,564.43, asserted per strategy
and in total, not assumed.** Every one of the 16 with children has constituent weights summing to
1.000 (checked, column `closes` in §3).

⛔ **24.8% of the 18-strategy value is UNDECOMPOSED** and that is the headline caveat, not a footnote.

### 1b. THE COTTONWOOD CONTRIBUTION TO OPAL AUA ON ANDREW'S RULED BASIS

> **Andrew-direct ~1950Z, verbatim:** *"the only remaining subject is a factor of the model vs
> non-model breakdown of the two anna accounts. Regardless, we are including the total amount in the
> Opal AUA/account growth, but I'd like to have it decomposed if possible."*

**His ruling is about the two Anna accounts' inclusion. It is not a ruling on the internal
composition of the other sixteen.** On that basis:

```
Cottonwood contribution to Opal AUA = $183,066,671.69   as-of 2026-08-10
  = $136,530,322.99   T1 basis, unchanged
  + $46,536,348.70    the two Anna accounts at full value, RULED IN
```

⛔ **It is NOT $187,928,913.13 (the 18-strategy total).** That figure would simultaneously
**add $7,005,515.33 that this document measures as non-Opal** (the three Sleeves plus the two leaf
strategies) **and drop $2,143,273.89 of off-list Opal-named strategy value that is inside T1's
figure** — a $4,862,241.44 net overstatement moving in two directions at once.

**The addition is clean and I can assert that rather than assume it:** T1's $136,530,322.99 contains
**zero** Anna contribution — the reconciliation in §6 closes *exactly* with both Annas fully
excluded, and an exact tie could not survive any Anna value being inside it. So this is a genuine
addition, not a double-count.

⚠ **MARK IT AS A BASIS CHANGE WHEREVER IT TRAVELS.** Against T1's $136,530,322.99 this is a $46.5M
jump that is **a sovereign inclusion ruling, not growth.** Unmarked, it reads as a quarter of new
money appearing at Cottonwood.

**If the leaf strategies are also ruled Opal** (still open, §4): **$189,291,964.87.**

---

## 1c. ⭐ ANDREW-DIRECT ~1955Z — THE TICKER BASIS, WHICH SUPERSEDES THE COMPOSITION BASIS AND CLOSES THE ANNA GAP

> **VERBATIM:** *"assume that if the holding is an Opal Aggregate holding (check agg "Positioning"
> from Portal for ticker list) that it is part of an opal model. I want to assess how much value is
> in non-opal model tickers"*

**This is a better instrument than the composition tree and it does what the composition tree could
not: it decomposes the two Anna accounts.** Membership is decided by TICKER against the Portal's own
Opal Aggregate holdings, so it needs no per-strategy composition and is therefore immune to the
name-gating gap in §5.

**The universe:** `s3://opal-data-portal-v2/json/positioning/positioning_data.json` →
`current_holdings.AGG.holdings`, **29 tickers**, `data_as_of` **2026-08-11**, `generated_at`
2026-08-12T11:06:04Z. **The AGG list is the exact union of all five model sleeves (UST/ST/INT/LT/ULT)
— 29 distinct tickers across all of them — so it is the complete Opal universe, not a subset.**
*(The file is gzipped despite its `.json` extension; read accordingly.)*

### The two Anna accounts — the §5 UNCOMPUTABLE, closed on this basis

| | Total | In Opal tickers | **NOT in Opal tickers** |
|---|---:|---:|---:|
| `Anna *9237` | $20,052,465.74 | $14,767,194.32 (73.6%) | **$5,285,271.42 (26.4%)** |
| `Anna *9238` | $26,483,882.96 | $24,059,257.67 (90.8%) | **$2,424,625.29 (9.2%)** |
| **Combined** | **$46,536,348.70** | **$38,826,451.99 (83.4%)** | **$7,709,896.71 (16.6%)** |

`*9237` non-Opal is chiefly cash (FCASH $2,463,348) plus USHY $763,027 and Sprott gold PHYS $742,508.
`*9238` non-Opal is gold PHYS $1,279,878, USHY $825,703, cash $319,044.

### All 18 Strategies on the ticker basis

| | Value | Share |
|---|---:|---:|
| Total | $187,928,913.13 | 100% |
| **In Opal-model tickers** | **$160,711,950.76** | **85.5%** |
| **NOT in Opal-model tickers** | **$27,216,962.37** | **14.5%** |
| — of which cash / money-market / uncategorized | $7,692,519.05 | 28.3% of non-Opal |
| — **of which INVESTED in outside tickers (162 distinct)** | **$19,524,443.32** | **71.7% of non-Opal** |

**Largest outside positions across the 18** — the wallet-share targets:

| Ticker | Value | Accounts |
|---|---:|---:|
| GLD | $4,999,144.26 | 286 |
| FDRXX | $4,063,407.71 | 289 |
| FCASH | $3,319,823.07 | 34 |
| USHY | $2,375,535.56 | 10 |
| PHYS | $2,163,907.64 | 8 |
| AAPL | $1,260,783.40 | 4 |
| SPYI | $984,661.94 | 8 |
| JEPI | $535,706.16 | 8 |

**All of Cottonwood, not just the 18:** $482,567,772.65 total — **$164,274,408.76 (34.0%) in Opal
tickers, $318,293,363.89 (66.0%) not.**

### ⚠ Two things to carry with these figures

**1. This basis gives a HIGHER Opal number than the composition basis — $160,711,950.76 vs
$134,387,049.10 — and both are correct about different questions.** The composition basis asks *which
model is this account running*; the ticker basis asks *is this holding an Opal-model holding*. Andrew's
ruling selects the ticker basis, and it has the practical advantage of covering all 18 including the
Annas. **Do not mix the two in one total.**

**2. It settles the managed-vs-product ambiguity in §5b — in the MANAGED direction.** The 29-ticker
list is mostly third-party ETFs the Opal models hold (iShares Core MSCI EAFE, SPDR S&P 500, Vanguard,
Dimensional). So "in an Opal model" here means **inside an Opal-managed allocation**, not **an
Opal-issued product**. On the narrower product reading, the Annas hold only $9,121,075.85 (19.6%) —
our own four ETFs. Both measured; the ruling picks the first.

⚠ **The rule is an ASSUMPTION he set, and it is stated as one:** a holding whose ticker appears in the
Aggregate is *assumed* to be there because of an Opal model. It is not proof that a specific position
was placed by one — an account could hold QQQ independently of any Opal sleeve.

---

## 2. WHICH SIGNAL DEFINES "TAGGED OPAL" — it is a NAME, and I am saying so plainly

**The Rebalance endpoint carries no tag or attribute field for this.** A constituent model in
`hierarchy.children` exposes: `id, rebalanceModelType, name, depth, metadata{isFullAllocation},
absoluteAllocation, relativeAllocation, updatedBy, createdBy, updatedAt, createdAt, isInferred,
isLiquidationOnly, isPublished, firmId, toleranceBandOptions, children, components`.
**There is no `tag`, no category, no Opal flag.**

> **THEREFORE THIS CLASSIFICATION IS NAME-BASED, AT A SECOND LEVEL, AND IT IS JUDGED — NOT READ.**
> **28 constituent models** were classified by whether their `name` contains "opal".

That matters because the *same heuristic at the strategy level* was already measured to fail in both
directions: it **drops** 3 of 18 (no "opal" string) and **invents** 4 false absences (spacing and
name variants). I have no reason to think the constituent level is safer, and one measured case
below shows it is not (§4).

---

## 3. LEVEL 1 + LEVEL 2 — per strategy (as-of 2026-08-10)

| Strategy | Strategy value | Constituents | Opal-tagged | Balance | closes |
|---|---:|---:|---:|---:|:--:|
| Opal Satellite 50 | $35,059,407.13 | 2 | $35,059,407.13 | $0.00 | ✓ |
| Opal Satellite 60 | $32,522,970.13 | 1 | $32,522,970.13 | $0.00 | ✓ |
| Opal Satellite 80 | $22,303,170.34 | 1 | $22,303,170.34 | $0.00 | ✓ |
| Opal Satellite 70 | $17,894,445.56 | 2 | $17,894,445.56 | $0.00 | ✓ |
| Opal Satellite 40 | $11,975,137.78 | 2 | $11,975,137.78 | $0.00 | ✓ |
| **Opal Moderate Income Portfolio** | $4,989,575.76 | **0** | **$0.00** | **$4,989,575.76** | ✗ |
| Opal Ultra Short Term | $2,895,622.20 | 1 | $2,895,622.20 | $0.00 | ✓ |
| Opal UST/ Sat 70 | $2,374,378.79 | 3 | $2,374,378.79 | $0.00 | ✓ |
| Opal - Cash + Satellite 50 | $2,332,508.01 | 3 | $2,332,508.01 | $0.00 | ✓ |
| Opal 66% Long Term / 34% UST | $2,171,701.04 | 2 | $2,171,701.04 | $0.00 | ✓ |
| Opal Satellite 30 | $1,649,393.53 | 2 | $1,649,393.53 | $0.00 | ✓ |
| Opal Satellite 15 | $1,265,018.25 | 1 | $1,265,018.25 | $0.00 | ✓ |
| **Opal - Income** | $1,235,717.42 | **0** | **$0.00** | **$1,235,717.42** | ✗ |
| Opal Satellite 98 | $1,151,126.04 | 1 | $1,151,126.04 | $0.00 | ✓ |
| **Blended Opal / Satellite 50** | $1,040,296.21 | 5 | $260,074.05 | **$780,222.16** | ✓ |
| Opal - Beecherl Legg | $532,096.24 | 2 | $532,096.24 | $0.00 | ✓ |
| **Anna \*9237** | $20,052,465.74 | **NO COMPOSITION** | — | — | — |
| **Anna \*9238** | $26,483,882.96 | **NO COMPOSITION** | — | — | — |
| **TOTAL** | **$187,928,913.13** | 28 | **$134,387,049.10** | **$7,005,515.33** | |

**The "Opal Satellite N" family is 100% Opal by constituent** — a "Satellite 50" is a 75/25 blend of
*Opal Intermediate-Term* and *Opal Short-Term*. The satellite sleeve is itself an Opal model, so the
name reads like a blend with outside content and is not one.

**The only genuine non-Opal constituents in the whole set** sit inside `Blended Opal / Satellite 50`:
*Sleeve - Equity* (0.375), *Sleeve - Tax-Free Bond* (0.36), *Sleeve - Core Money Market* (0.015),
against *Opal Intermediate-Term* (0.1875) + *Opal Short-Term* (0.0625). **$780,222.16 of balance.**

---

## 3b. LEVEL 2 IN FULL — every constituent model, with its value and its source (T2-A2, T2-A5)

**Source column is uniform and that is itself the finding: 28 of 28 constituents come from our own
landing; 0 from a live sweep, because the live sweep failed (§5).**

| Strategy | Constituent model | rel.alloc | Value | Opal? | Source |
|---|---|---:|---:|:--:|---|
| **Anna \*9237** | *no composition available* | - | $20,052,465.74 | - | **NONE - name-gated gap** |
| **Anna \*9238** | *no composition available* | - | $26,483,882.96 | - | **NONE - name-gated gap** |
| Blended Opal / Satellite 50 | Opal Intermediate-Term | 0.1875 | $195,055.54 | YES | own landing 2026-08-12 |
| Blended Opal / Satellite 50 | Opal Short-Term | 0.0625 | $65,018.51 | YES | own landing 2026-08-12 |
| Blended Opal / Satellite 50 | Sleeve - Core Money Market | 0.0150 | $15,604.44 | no | own landing 2026-08-12 |
| Blended Opal / Satellite 50 | Sleeve - Equity | 0.3750 | $390,111.08 | no | own landing 2026-08-12 |
| Blended Opal / Satellite 50 | Sleeve - Tax-Free Bond | 0.3600 | $374,506.64 | no | own landing 2026-08-12 |
| **Opal Moderate Income Portfolio** | *LEAF - 8 direct securities, no child model* | - | $4,989,575.76 | **?** | own landing 2026-08-12 |
| Opal - Beecherl Legg | Opal Conservative Growth | 0.7900 | $420,356.03 | YES | own landing 2026-08-12 |
| Opal - Beecherl Legg | Opal Ultra Short-Term Income | 0.2100 | $111,740.21 | YES | own landing 2026-08-12 |
| Opal - Cash + Satellite 50 | Opal Intermediate-Term | 0.6845 | $1,596,601.74 | YES | own landing 2026-08-12 |
| Opal - Cash + Satellite 50 | Opal Short-Term | 0.2280 | $531,811.83 | YES | own landing 2026-08-12 |
| Opal - Cash + Satellite 50 | Opal Ultra Short-Term Income | 0.0875 | $204,094.45 | YES | own landing 2026-08-12 |
| **Opal - Income** | *LEAF - 4 direct securities, no child model* | - | $1,235,717.42 | **?** | own landing 2026-08-12 |
| Opal 66% Long Term / 34% UST | Opal Conservative Growth | 0.6600 | $1,433,322.69 | YES | own landing 2026-08-12 |
| Opal 66% Long Term / 34% UST | Opal Ultra Short-Term Income | 0.3400 | $738,378.35 | YES | own landing 2026-08-12 |
| Opal Satellite 15 | Opal Short-Term | 1.0000 | $1,265,018.25 | YES | own landing 2026-08-12 |
| Opal Satellite 30 | Opal Intermediate-Term | 0.2500 | $412,348.38 | YES | own landing 2026-08-12 |
| Opal Satellite 30 | Opal Short-Term | 0.7500 | $1,237,045.15 | YES | own landing 2026-08-12 |
| Opal Satellite 40 | Opal Intermediate-Term | 0.5000 | $5,987,568.89 | YES | own landing 2026-08-12 |
| Opal Satellite 40 | Opal Short-Term | 0.5000 | $5,987,568.89 | YES | own landing 2026-08-12 |
| Opal Satellite 50 | Opal Intermediate-Term | 0.7500 | $26,294,555.35 | YES | own landing 2026-08-12 |
| Opal Satellite 50 | Opal Short-Term | 0.2500 | $8,764,851.78 | YES | own landing 2026-08-12 |
| Opal Satellite 60 | Opal Intermediate-Term | 1.0000 | $32,522,970.13 | YES | own landing 2026-08-12 |
| Opal Satellite 70 | Opal Conservative Growth | 0.5000 | $8,947,222.78 | YES | own landing 2026-08-12 |
| Opal Satellite 70 | Opal Intermediate-Term | 0.5000 | $8,947,222.78 | YES | own landing 2026-08-12 |
| Opal Satellite 80 | Opal Conservative Growth | 1.0000 | $22,303,170.34 | YES | own landing 2026-08-12 |
| Opal Satellite 98 | Opal Long-Term Aggressive | 1.0000 | $1,151,126.04 | YES | own landing 2026-08-12 |
| Opal Ultra Short Term | Opal Ultra Short-Term Income | 1.0000 | $2,895,622.20 | YES | own landing 2026-08-12 |
| Opal UST/ Sat 70 | Opal Conservative Growth | 0.4565 | $1,083,903.92 | YES | own landing 2026-08-12 |
| Opal UST/ Sat 70 | Opal Intermediate-Term | 0.4565 | $1,083,903.92 | YES | own landing 2026-08-12 |
| Opal UST/ Sat 70 | Opal Ultra Short-Term Income | 0.0870 | $206,570.95 | YES | own landing 2026-08-12 |
| | | | **$134,387,049.10 Opal** | | |
| | | | **$7,005,515.33 balance** | | |
| | | | **$141,392,564.43 sum** | | |

**Only SIX distinct Opal constituent models appear across the whole set** — Intermediate-Term,
Short-Term, Conservative Growth, Ultra Short-Term Income, Long-Term Aggressive, and (via the leaf
strategies) none. Eighteen strategies are built from six building blocks plus three Sleeves.

---

## 4. ⛔ THE $6,225,293.18 THAT IS A CLASSIFICATION ARTIFACT, NOT A MEASUREMENT

**`Opal Moderate Income Portfolio` and `Opal - Income` have ZERO child models.** They are **leaf
strategies** holding securities *directly* — Dimensional Core Fixed Income, iShares Broad USD High
Yield, JPMorgan Equity Premium Income, NEOS S&P 500 High Income, SPDR Portfolio High Yield.

**A constituent-model test scores them 0% Opal. A name test scores them 100% Opal.** Both are
defensible and they differ by **$6,225,293.18** — 89% of the entire reported balance.

> **So the $7,005,515.33 balance is really two different things:**
> **$780,222.16** — genuinely non-Opal constituents (the sleeves above). **Measured.**
> **$6,225,293.18** — two Opal-*named* strategies with no Opal child model. **A definitional
> outcome, not a measurement.**
>
> *(Those two components sum to $7,005,515.34 against the aggregate $7,005,515.33 — a one-cent
> float-rounding difference from summing per-strategy products rather than the running total. Stated
> rather than silently rounded, because this document asserts its decompositions close.)*

**This is the definitional question the STOP told me not to answer silently, so I am not answering
it.** If Andrew rules leaf strategies count as Opal, the balance falls to **$780,222.16** and the
Opal subtotal rises to **$140,612,342.28**. Both figures are given so either ruling is one
substitution away. AE's 2026-08-07 scan independently identified these as leaf strategies and warned
that *"a composition-based scan alone would miss them"* — it did.

---

## 5. THE TWO STRATEGIES WE CANNOT DECOMPOSE, AND THE LIVE PULL I ATTEMPTED

`Anna *9237` and `Anna *9238` carry **$46,536,348.70 (24.8% of the total)** and our own landing has
**no composition for either**. This is not chance: `cot-rebalancer-runner` pulls composition under
`MODEL_DETAIL_SCOPE=opal_closure`, which **seeds only on strategies whose NAME contains "opal"** and
walks downward. Neither Anna carries the string. **Composition coverage for the 18 is 16 of 18 (89%)
and the 2 missing are missing by that exact mechanism.**

**I spent the standing cot-BD lift, and it did not succeed.** Read-only attempt, minimal scope, using
the deployed runner's own auth path (`load_bd_session` → `Puller`), requesting two model IDs and
nothing else:

```
AUTH: cookie jar loaded from secret (GetSecretValue only)     -> OK
AUTH: bearer minted in-memory via GET /auth/token             -> OK
GET /api/models/1ae61190-...  -> HTTP 401 Unauthorized
  (Puller re-minted the bearer and retried per its own 401 path -- still 401)
```

**NOTHING WAS WRITTEN — no S3, no secret write, no bronze landing.** I stopped rather than retry a
vendor endpoint further.

⚠ **I am NOT concluding the lift is broken or the session is dead.** One observation, from a laptop,
against an endpoint whose scheduled Lambda pull succeeded from AWS at 02:00Z today. `/auth/token`
succeeding while `/api/models/{id}` 401s is a *discriminating* detail worth recording — but the
mechanism (IP/tenancy binding, cookie rotation since 02:00Z, per-endpoint entitlement) is
**unestablished**. Reported as an observation, not a diagnosis.

**The partial record does not close either.** AE's 08-07 live scan documents both Anna compositions,
but the weights sum to **0.97** and **0.967** — they do not reach 1.000, so they cannot support an
exact decomposition. Using them would produce a number that looks precise and is not.

**Therefore both Anna strategies are `UNCOMPUTABLE-BY-CONSTRUCTION` from available evidence**, and
their $46,536,348.70 sits outside the split rather than being distributed into it on an assumption.

**The clean closer was authorized by CTO and then found to be UNEXECUTABLE as conditioned.** They
authorized invoking the deployed `cot-rebalancer-runner` with `MODEL_DETAIL_SCOPE=all` from AWS,
conditioned on *"existing parameter only — if closing this needs a CODE change, STOP."*
**The condition fires.** Source-grounded in `lambda_function.py`:
`lambda_handler` (`:407-417`) reads only `mode`, `date`, `force`; `MODEL_DETAIL_SCOPE` is a
module-level env read (`:70`) evaluated at cold-start; `--scope` exists **only** in the CLI `main()`
(`:424-429`), and the module docstring says so outright (`:38`). There is no event parameter that
produces `scope=all` on the deployed function.

⚠ **And the only available route is materially different from the act authorized.** Flipping the
function's env var is not per-invocation — **every scheduled nightly run would land the full roster,
permanently**, which is a standing scope change to a production producer rather than the additive
one-off that was reasoned about. **Not run. No invoke, no config touched, no code edited.** Handed
back.

### 5b. WHAT THE TWO ACCOUNTS ACTUALLY HOLD — measured without the composition endpoint

The model-attribution split is blocked; **the content is not.** Read directly from holdings:

| | `Anna *9237` | `Anna *9238` |
|---|---|---|
| Account | **Anna Thiessen - Individual** | **Harms 2020 Trust** |
| Tax status / rebalancer `isManaged` | Taxable / **False** | Taxable / **False** |
| Value | $20,052,465.74 | $26,483,882.96 |
| Distinct tickers | 71 | 34 |
| Cash equivalent | $2,463,348.13 (12.3%) | $319,044.11 (1.2%) |
| **In Opal ETFs** | **$1,986,413.55 (9.9%)** | **$7,134,662.30 (26.9%)** |
| Third-party | $18,066,052.20 (90.1%) | $19,349,220.66 (73.1%) |

**Combined: $9,121,075.85 (19.6%) sits in our own ETFs** — DIVZ, IDVZ, PFDE, PFOE — and
**$37,415,272.86 (80.4%) is third-party**: iShares Core MSCI EAFE, SPDR S&P 500, iShares Mid-Cap,
Sprott Physical Gold, high-yield, CLO and ultra-short income.

**So what remains genuinely unmeasurable is the model ATTRIBUTION, not the content.** Both accounts
present as bespoke multi-asset portfolios that *include* Opal products, and both are flagged
`isManaged=False` in the rebalancer despite sitting on Andrew's strategy list.

> ⛔ **AN AMBIGUITY THIS EXPOSES, AND IT IS LARGER THAN THESE TWO ACCOUNTS.** The
> **$134,387,049.10 "Opal-tagged" figure means money in Opal-MANAGED MODELS. It does not mean money
> in OPAL PRODUCTS.** If the Opal models hold third-party ETFs the way these two accounts do, those
> are very different quantities. **I have not measured it** — it needs the Opal models' own holdings
> — and I am not asserting they differ. But a reader shown "Opal AUA" may reasonably assume the
> second meaning, and only the first is what was measured.

---

## 6. RECONCILIATION AGAINST T1's $136,530,322.99 — it closes EXACTLY, and the mechanism is INFERRED

T1 put Cottonwood Opal model AUA at **$136,530,322.99** (platinum `model_aua`, 2026-08-10).
My Opal-tagged constituent subtotal is **$134,387,049.10**. **Delta = −$2,143,273.89.**

> **That delta equals the off-list Opal-named strategy value to the cent:**
> **$134,387,049.10 + $2,143,273.89 = $136,530,322.99** — exact.

The $2,143,273.89 is the value in `Opal Hendrickson LT/UST` and `Opal Sat 50+ 15% cash`: strategies
that **are Opal-named but are NOT on Andrew's 18-list**, so they are outside my scope and inside
platinum's.

⚠ **The arithmetic is exact; the mechanism is INFERRED.** The exact closure *suggests* platinum's
`model_aua` is computed over the full Opal-named strategy set rather than the 18-list — but **I have
not read platinum's producer to confirm it**, and an exact tie is evidence for a hypothesis, not
proof of one. **Direction, stated as CTO asked:** my figure is **lower** than T1's, and it is lower
because my scope is narrower (18 strategies, not all Opal-named). Neither figure is defective and
neither was tuned toward the other.

---

## 7. COTTONWOOD ACCOUNT + CLIENT DELTAS — the T1 gap, closed

| Basis | Accounts | Clients (`Relationship ID`) |
|---|---|---|
| **Andrew-ruled 0 start** (2026-04-01 → 2026-08-10) | 0 → 926 = **+926** | 0 → 223 = **+223** |
| **Measured coverage window** (2026-06-09 → 2026-08-10) | 680 → 926 = **+246** | 206 → 223 = **+17** |

⛔ **The measured +246 is NOT clean growth — the count-ramp check fires.**

| Date | Rows | Accounts | Relationships | Value |
|---|---:|---:|---:|---:|
| 2026-06-09 | 10,183 | 680 | 206 | $373,157,665.00 |
| 2026-06-30 | 11,453 | 813 | 218 | $436,654,607.00 |
| 2026-07-15 | 16,615 | 845 | 221 | $435,714,870.67 |
| 2026-07-20 | 16,762 | 913 | 221 | $458,114,003.10 |
| 2026-08-10 | 17,138 | 926 | 223 | $482,567,772.65 |

Accounts +36% against relationships +8%; rows +45% between 06-30 and 07-15 against a 4% account rise.
That is the feed picking up more accounts and more assets **inside existing relationships** —
onboarding, landing on the producer's declared `first_tracked_date` of 2026-07-20. **The
+$109,410,107.65 over that window must not be read as growth.**

---

## 8. CONTROLS

**Relationship-grain collapse (the double-count trap) — FIRED.** cot `fact_holdings` is
Relationship × Account × Asset. Naive sum **$482,772,843.42**; deduped to (AccountID, AssetID)
**$482,567,772.65**; **$205,070.77 phantom** from 2 of 17,138 pairs held under two relationships.
**The deduped figure ties EXACTLY to platinum `partner_custody_total` @2026-08-10** — which is the
evidence the collapse is correct rather than merely plausible.

**Per-strategy closure assertion.** Constituent weights summed per strategy and compared to 1.000:
**16 of 16 with children close**; the 2 zero-children strategies are flagged `✗` and are the leaf
case in §4, not a weight defect.

**Absent-is-not-zero.** The 2 Anna strategies are held OUT of the split rather than entered as zero.
Entering them at zero would have reported a balance of $7,005,515.33 against a total of
$187,928,913.13 and implied a 96.3% Opal share — from data covering 75.2% of the value.

---

## 9. DENOMINATORS

| Scan | Denominator |
|---|---|
| Andrew's strategy list | 18 |
| Cottonwood roster (today's landing) | 63 of 63 (`totalResultCount`=63, `pageCount`=1) |
| T1 matcher resolution | 18 of 18 resolved (17 exact, 1 normalized) |
| Composition landed for the 18 | **16 of 18 (89%)**; 29 of 63 roster-wide (46%, name-gated) |
| Constituent models classified | 28, **all by name** |
| Strategies whose weights close to 1.000 | 16 of 16 with children |
| `fact_holdings` @2026-08-10 | 17,140 raw → 17,138 deduped · 926 accounts · 223 relationships |
| Rebalancer accounts | 921 rows · 921 account numbers · 47 distinct strategies |
| Account-number join | 917 matched · 9 holdings-only · 4 accounts-only |
| Coverage-window partitions read | 7 dates, 2026-06-09 → 2026-08-10 |
| Live vendor pull attempted | 2 model IDs · 0 succeeded (HTTP 401) · 0 bytes written |

---

## 10. WHAT SURPRISED ME

1. **"Opal Satellite 50" is 100% Opal.** The name reads like a blend of Opal and something else; the
   constituents are two Opal models. The names that *sound* mixed are pure, and the one that sounds
   pure — `Opal - Income` — holds only third-party ETFs.
2. **89% of the reported "balance" is a definitional artifact, not non-Opal money.** $6.2M of
   $7.0M comes from two leaf strategies scoring 0% on a constituent test purely because they have no
   constituents.
3. **The T1 reconciliation closed to the cent on the first attempt**, and the residual was exactly a
   quantity I had measured for a different purpose in T1.
4. **The vendor lift was authorized, warranted, and still did not work** — and it failed in a
   discriminating way (`/auth/token` OK, `/api/models/{id}` 401) that is worth more as a recorded
   observation than the two compositions would have been.
5. **The name-gating gap landed exactly on the two strategies that are 25% of the value.** The
   mechanism is name-based and so is the exposure: the strategies missing composition are missing
   *because* they are not named "Opal", and they are large.

---

## 11. COMPILER TOOLS

| Tool | Call | Result |
|---|---|---|
| `comp-find` | `collapse_relationship_grain` | PASS — 53 hits, DEF=3; located the canonical collapse, one call |
| `comp-find --name` | `fact_allocation` | MEASURED ZERO over 26,100 files, with the tool's own honest "not a claim of absence" disclaimer |
| comp-rail gate | fired twice on raw `aws s3 ls` / `infra` grep | **Correctly.** Reworked to a row-count ramp and the native `Grep` tool; the ramp was the better instrument anyway |
| `commit-gate.sh` | `extract_brdsep_t2.py` | PASS |
| `proof-of-spec-check.py` | instance + criterion set | VALID |

**Reused rather than rebuilt (build-ladder rung 2):** the live-pull attempt imported the deployed
runner's own `load_bd_session` and `Puller` instead of re-implementing BD auth. That reuse is also
what produced the discriminating 401 — a hand-rolled client would have left me unsure whether the
failure was mine.

---

## 12. EVIDENCE INDEX

| Figure | Source |
|---|---|
| Strategy composition (16 of 18) | `s3://opal-data-assets/blackdiamond/cottonwood/bronze/rebalancer_model_detail/2026-08-12/{id}.json` → `hierarchy.children[].relativeAllocation` |
| Strategy roster + account→strategy | `.../bronze/rebalancer_{models,accounts}/2026-08-12/` |
| Strategy value | `s3://opal-data-assets/blackdiamond/cottonwood/silver/fact_holdings/date=2026-08-10/` |
| Name-gating mechanism | `infra/aws/lambda/cot-pipeline/cot-rebalancer-runner/lambda_function.py:275,279,298-317` |
| Leaf-strategy corroboration | `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/BD_REBALANCER_OPAL_COMPOSITION_SCAN_20260807.md` |
| T1 comparator (read-only) | `s3://opal-data-portal-v2/platinum/mdpf/cottonwood/aggregate-aua-timeseries.json` |
