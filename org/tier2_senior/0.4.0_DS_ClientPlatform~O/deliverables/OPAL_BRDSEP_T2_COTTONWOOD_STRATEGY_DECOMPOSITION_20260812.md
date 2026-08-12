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

**The clean closer, if wanted — a decision I did not take unilaterally:** invoking the deployed
`cot-rebalancer-runner` with `MODEL_DETAIL_SCOPE=all` pulls all 63 compositions from AWS, where the
scheduled path already works. **That widens what lands in production bronze (63 details vs 29), which
is a production footprint change for a measurement, so it is CTO's call and not mine.**

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
