# WSE_COTMDL — FRONTEND WORKSTREAM SPEC (Cottonwood firm-specific MDPF page)

**Authority:** Andrew-direct 2026-07-22 ~1700Z — *"yes, land it as the FE workstream spec."*
**Author:** `0.4.0_DE_ClientPlatform` · **Purpose:** a decomposable spec COO can cut TOs from when the
resumption gate clears (Andrew ~1552Z: CVO verify → COO decomposition → dispatch).

> ## ⛔ STATUS: SPEC ONLY. NOTHING IN THIS DOCUMENT IS STARTED.
> The MDPF planning hold stands (CTO ruling, Andrew ~1621Z: *a priority statement is not a hold lift*).
> My WS-4 re-home remains HELD. **This is a plan, not work in progress, and landing it is not a request
> to begin it.**

**Companion documents (read these first, do not duplicate them here):**
`MDPF_FE_FORK_PATTERN_INFLECTION_TO_COTTONWOOD_20260722.md` @`108f8156c` (the fork map + instrument
limits) · `mdpf_cottonwood_render_20260722/` @`c95210ec3` (render evidence + discriminating control) ·
`MDPF_PHASE0_TWO_FIRM_ENUMERATION_20260722.md` @`b6d9b299d` (the census).

---

## 0a. 🔔 ANDREW RULINGS ~1720Z — RECORDED VERBATIM WITH SCOPE

**RULING 1 (D6 — PARTIAL), VERBATIM:**
> *"Opal Conservative Growth is Long Term Conservative, also known as Opal Long Term, also known as LTC.
> That is how that needs to be mapped."*

**RULING 2 (day-one naming), VERBATIM:**
> *"Regarding Day 1, no we are using canonical names, we are not doing this 'Satellite' bullshit unless
> explicitly asked."*

**RULING 3 (D6 — THE REMAINING HALF), VERBATIM ~1725Z:**
> *"We are not tracking Opal - Income at this time. That is not relevant to the work here, it would be a
> 'non-model' asset at this time."*

## ✅ D6 IS NOW FULLY RESOLVED — AND SET B IS RELEASED (OFF)

**I framed D6 as merge-vs-add. The answer was neither.** `Opal - Income` is **not a model at all** — it is a
non-model asset, and not tracked at this time.

| Cottonwood model | ruling | consequence |
|---|---|---|
| `Opal Conservative Growth` ($30.99M / 96 accts) | **MERGE → `opal_long_term_conservative`** | already in `STACK_SERIES` → **renders with no FE change** |
| `Opal - Income` | **NOT A MODEL — non-model, not tracked at this time** | never enters `by_model` → **no unknown key ever reaches the FE** |

> ### ⇒ **NO NON-CANONICAL MODEL KEY WILL EXIST. SET B (B1 `STACK_SERIES` + B2 `getModelColor`) IS NOT
> ### REQUIRED, AND NEITHER IS THE `GLOBAL_MODEL_KEYS` PRODUCER TWIN.**
> The render-confirmed blank-charts defect **cannot fire** on this configuration. It remains a real latent
> defect for **firm four** — which is precisely what **C1** is for.

**THE FE WORKSTREAM IS NOW: SET A (three small items) + C1 (preventive).** Set B is struck, not deferred.

### ⚠ TWO THINGS TO CARRY, NEITHER AN OBJECTION

**(1) IMPLEMENT THE EXCLUSION AS AN *ENUMERATED* ONE, NOT A SILENT DROP.** The estate already has the right
pattern: `mdpf_revamp_model_crosswalk.py:167-170` `KNOWN_EXCLUDED_ECLIPSE_IDS` — a **named register of
reviewed, deliberately-excluded models with a reason string**, so an exclusion is visible and reviewable
rather than an absence. `Opal - Income` should land in a Cottonwood analog of that register, carrying this
ruling as its reason.
**Why it matters:** the crosswalk currently **RAISES** on both Cottonwood keys (correct fail-closed).
Mapping Conservative Growth retires one raise. The Income raise must be retired **by an enumerated
exclusion**, *not* by loosening the raise — otherwise the next unknown Cottonwood model is silently
dropped instead of caught. **Same shape as CTO's 20-date rule: enumerated list, never a predicate.**

**(2) DECLARE WHERE INCOME'S DOLLARS GO — do not let it be discovered at co-sign.** For 49F and Inflection,
`non_model_aua` is a **residual**: `custody_total − model_aua`. **Cottonwood has no custody total** —
`build_cottonwood_mdpf_slice.py:243` emits `partner_custody_total = [None] * n` because the BD Rebalancer
carries model assignment only. **So a "non-model" bucket cannot be computed as a residual for Cottonwood.**
Consequence: with Income excluded from `by_model` **and** no residual to fall into, **its dollars may appear
nowhere in the artifact at all.**
**That may be exactly right** — *"not tracking at this time"* reads as *don't build for it*. **But it should
be a declared term, not a discovery.** *(I do not have Income's magnitude and am not going to quote one —
the $99.72M in my render fixture was **invented test data**, not measured.)*

### SCOPE OF RULING 1 — it covered ONE model; RULING 3 closes the other.

**RULED:** `Opal Conservative Growth` → **MERGE** onto the canonical **`opal_long_term_conservative`**
(LTC / "Opal Long Term"). $30.99M / 96 accounts.
**NOT RULED — STILL OPEN AT ANDREW:** **`Opal - Income`.** It was the model with *no counterpart at all*,
and the ruling does not name it. **Do not extend the merge to it by analogy.** *A verbatim quote without
its scope is a future contradiction with a citation.*

### CONSEQUENCES

**(a) ~~SET B IS NOT RELEASED~~ — SUPERSEDED BY RULING 3 (see above): SET B IS RELEASED / STRUCK.**
Both Cottonwood keys are resolved without a distinct new model key ever existing, so B1/B2 and the
`GLOBAL_MODEL_KEYS` twin are **not required**. *(Struck in place rather than deleted so the record shows
the ruling arriving, not a spec that was always this way.)*

**(b) RULING 2 REMOVES A WORK ITEM AND OVERRULES MY RECOMMENDATION.** I recommended advisor-facing
("Satellite") names for day one. **Overruled: canonical names.** No FE naming work; no display-name
override layer; the existing canonical `display_name` path is correct as-is. **Scope note:** *"unless
explicitly asked"* — this is **not-by-default**, not a permanent prohibition.
**The two rulings are coherent:** if Conservative Growth *is* LTC, rendering it as the canonical
"Long Term Conservative" is the same answer from both directions.

**(c) ⚠ A DATA CONSEQUENCE THAT MUST BE NAMED BEFORE THE CO-SIGN, NOT AFTER.** Merging is not a labelling
change — **it moves money into an existing series.** Global `opal_long_term_conservative` will now include
Cottonwood's **$30.99M**, so the canonical LTC line **steps** on the day Cottonwood folds in. Anyone
verifying global LTC against a pre-Cottonwood baseline will see a real discontinuity. **It must be
declared as a named delta up front** — otherwise it reads as exactly the kind of unexplained jump the
count-axis P0 taught us to treat as a defect.

**(d) OWNER OF THE MERGE:** the crosswalk mapping (Cottonwood's Rebalancer model name →
`opal_long_term_conservative`) is a **producer/DS** change in `mdpf_revamp_model_crosswalk.py`, **not FE**.
FE inherits it for free.

**Nothing in this section is started.** The hold stands.

---

## 1. THE GATING DECISION — D6 FORKS THIS ENTIRE WORKSTREAM
*(⚠ AMENDED by Ruling 1 above — the fork is now HALF-resolved; read §0a first.)*

**D6 (merge-vs-add canonical model keys) is RESERVED TO ANDREW and is untouched.** It decides the size of
this workstream, not merely its details:

| D6 outcome | FE consequence |
|---|---|
| **MERGE** — Cottonwood's models map onto canonical keys | **B-items vanish.** `STACK_SERIES` already contains those keys; charts populate. Only A-items remain. |
| **ADD** — `cottonwood_opal_conservative_growth` / `cottonwood_opal_income` stay distinct | **B-items are MANDATORY.** Without B1, *every Cottonwood model renders blank* — render-confirmed with a discriminating control. |

**Do not decompose B-items before D6.** Doing so bakes in an assumption the ruling exists to settle.

---

## 2. WORK ITEMS

### SET A — correct regardless of D6

**A1 · Condition the donut methodology caption**
`portal/src/pages/ModelPortfolios.tsx:1422`
Asserts *"Non-Model AUM = Total AUM (Opal-managed) − Black Diamond Model AUM"* while the donut centre on
the **same screen** reads **"Not yet tracked"** for that Total. Gated only on the **global**
`nonModelData` query (`:548`), so it renders under a firm selection regardless.
**Fix:** apply the conditional treatment `:2246-2258` already received in `08c6d8b2`.
**Acceptance:** Cottonwood render shows no methodology claim whose terms the page reports as untracked.
**Effort:** XS. **Risk:** low — string/conditional only.
**Note:** this is the *un-migrated twin* of an already-fixed defect. A verifier grepping `'rolled forward'`
finds only the fixed one.

**A2 · Migrate the two remaining `lastNonNull` call sites**
`ModelPortfolios.tsx:617` (per-model `currentAUM`) and `:968` (Non-Model slice) still call `lastNonNull`,
whose `return 0` sits at `:295`. `lastNonNullOrNull` exists at `:316-322`; `08c6d8b2` migrated only the
**firm-total** sites (`:883`, `:1206`, `:1377`, `:2256`).
For a firm whose `non_model_aua` is null by construction (`build_cottonwood_mdpf_slice.py:243` emits
`[None]*len(dates)`), `return 0` renders a **measured-looking $0**.
**⚠ THIS IS A DECISION, NOT A CLEANUP.** CTO's *"narrow sibling, migrate only what must"* ruling was
applied deliberately. Widening it must be **acknowledged by CTO**, not assumed by the implementer.
**Acceptance:** a Cottonwood fixture with all-null `non_model_aua` renders an honest absence, never `$0`.
**Effort:** S. **Risk:** medium — touches per-model display for all firms; needs the §4 render matrix.

**A3 · `AUMGrowthMetrics.tsx:87` — hardcoded "Total AUA" on a firm-scoped tile**
The component takes no label prop, so it reads **AUA** while the tab label (`:1575`), donut caption
(`:1422`) and footer (`:2246`) all say **AUM** under a firm selection — contradicting the
`assetsLabel(effectiveFirmId !== 'global')` rule the codebase states.
**Pre-existing; affects 49F and Inflection today, not only Cottonwood.**
**Fix:** accept a label prop; route through `assetsLabel`.
**Acceptance:** one asset-noun per view across tile, tab, donut and footer, at all four selections.
**Effort:** S. **Risk:** low.

### SET B — required ONLY if D6 = ADD

**B1 · Derive `STACK_SERIES` from the data — THE BLOCKING DEFECT**
`ModelPortfolios.tsx:142-151` is a **closed 7-entry literal**; `:1891` / `:2060` mount a `<Bar>` / `<Area>`
only for its members. The legend (`:939` → `trendModelOrder`, `:806-809`) and donut (`:613`) are
**data-driven**. The page even computes and stores the value (`:1789-1794`, `keyForModel` minting
`m_<slug>`) and then drops it because no series was ever mounted.
**RENDER-CONFIRMED with a discriminating control** (@`c95210ec3`): byte-identical fixtures, only the model
keys differing — non-canonical keys → **both trend charts BLANK** while the legend names the models and the
donut draws them; canonical keys → 4 stacked bars + full area chart.
**Fix:** derive the series list from the same source the legend uses, so legend / donut / stack share one
source of truth.
**Acceptance:** a Cottonwood fixture with non-canonical model keys renders **bars and areas**, and the
trend total reconciles to the donut total.
**Effort:** M. **⚠ RISK — AND THIS IS THE REAL COST DRIVER:** it changes rendering for **all four**
selections, so the cost is the §4 re-verification matrix, **not the diff**. Size the item on that.

**B2 · `getModelColor` — deterministic colour for unknown model keys**
`portal/src/lib/modelPortfolioColors.ts:113-118` falls back to a **two-way substring `includes`** across the
7 Opal names. Render-confirmed: **both Cottonwood models render the same blue**, in donut and legend —
two products, visually indistinguishable (control renders them orange/green).
**Worse than the blandness:** a Cottonwood model whose name contains (or is contained by) e.g. "Short Term"
would **silently inherit that model's brand colour**, which reads as correct.
**Fix:** replace the fuzzy fallback with a deterministic hash→palette assignment for unrecognised keys, or
register explicit Cottonwood entries.
**Acceptance:** two distinct Cottonwood models render two distinct colours, stable across reloads, and no
unknown key adopts a canonical model's brand colour.
**Effort:** S. **Risk:** low-medium — verify the 7 canonical models keep their exact existing colours.

### SET C — preventive, and the highest-leverage item here

**C1 · Make the per-firm presentation contracts EXHAUSTIVE BY TYPE**
`MDPF_SOURCE_ATTRIBUTION` (`:258-282`) is `Record<MdpfFirmId, …>` — its own comment states this *"is what
makes a new firm a compile error instead of a silent 'SmartX' mislabel."* **It is the only contract on the
page that is safe by construction.** `STACK_SERIES`, `MODEL_KEY`/`BLEND_AFTER` (`:97-131`) and
`getModelColor` are plain literals, so a missing firm is **silent**.
**Fix:** give the other three the same exhaustive-by-type shape.
**Acceptance:** adding a hypothetical 5th firm id to `ALL_MDPF_PARTNER_FIRMS` **fails `tsc`** until every
per-firm contract is populated. *(Exercise it — add a throwaway id, confirm the build breaks, remove it.)*
**Effort:** M. **Value:** converts every future firm onboarding from a render-discovered defect into a
build failure. **This is the only item that pays forward to firm four.**

---

## 3. PRECONDITIONS NOT OWNED BY THIS WORKSTREAM

FE work cannot be accepted end-to-end until the artifact exists at the path the page already requests.
**Not FE items — listed so decomposition does not strand this workstream:**
1. `json/mdpf/cottonwood/aggregate-aua-timeseries.json` (producer fold — HELD).
2. `json/mdpf/cottonwood/account-distribution.json` (donut / bell-curve panel).
3. **Three separate enumerations, none of which name Cottonwood** — publisher `PUBLISH_MAP`
   (`opal-assets-mdpf-portal-publisher/lambda_function.py:37-47`), the exact-key bucket policy
   (`monolith.tf:262-266`), and the exact-9 CloudFront behaviours (`cloudfront-distribution.tf:77-86`).
   **Update two of three and you get a partial serve no single instrument sees.**

**⚠ `ModelPortfolios.tsx:238-243` says the failure mode out loud:** the firm id **is** the artifact path, and
a mismatch *"404s into the queryFn's catch and renders an **EMPTY partner rather than an error** — silent,
and indistinguishable from 'no data yet'."*

---

## 4. VERIFICATION PROTOCOL — RENDER, NOT DIFF

**Every defect in this spec was found by rendering and reading a PNG. None was visible to `tsc`, and four
census limbs missed them.** The portal's own law: *"A grep cannot see contrast."*

**Required for any A/B item:**
1. `portal/scripts/ui-smoke.mjs <route> <out.png> --fixtures <f.json>` at **all four selections** —
   global · 49financial · inflection · cottonwood. **A change to a shared series/colour/label path is not
   accepted on the Cottonwood cell alone.**
2. **A discriminating control**, per B1's method: the fixture that *should* fail must actually fail.
   A render that cannot fail is not evidence.
3. `tsc -b --noEmit` clean + Surface-Check Gate.
4. **CLOSE LEG: Andrew visual smoke** — `MDPF_SCOPED` required exactly this (S5) and reopened on 2026-05-29
   without it: *"data layer passed but the portal did NOT work for firm-scoped views."* **Cottonwood
   carries the same leg.**

**Recommended, and cheap:** add a **Cottonwood fixture cell to the smoke harness** so firm four does not
rediscover this class by hand.

**Fixture pinning note (no source edit needed):** `ui-smoke.mjs:79-81` checks fixtures **before** the auth
stub, so an external-partner session can be pinned entirely through the fixtures file by overriding
`auth/refresh`. That is also the honest view — what a real Cottonwood advisor sees.

---

## 5. EXPLICITLY OUT OF SCOPE

- **Benchmark and Peers tabs.** Firm-blind **by Andrew's standing ruling 2026-05-07**
  (`ADVI_FIRMSEP.md:133`): `json/portfolios/`, `json/peers/`, `json/latest/` are **permanent intentional
  house view**; only `json/model_portfolios/` is transitional (the FIRMSEP.11 placeholder).
  Corroborated by `comp-cluster`: the one panel cluster on this page draws entirely on those prefixes.
  **⚠ Genuinely open and NOT proposed here:** the **attribution seam** — house-view numbers render under a
  Cottonwood header with *"Black Diamond Rebalancer"* beneath, and the explaining disclaimer was removed
  **Andrew-direct 2026-06-01** (`:1075-1077`). **A product call, Andrew's.**
- **`demo`'s missing MDPF registry entry.** Real and live today (blank firm name at `:1078`, SmartX
  attribution) while `firmAccess.ts:81-90` grants `/portfolios`. **Same class, different tenant — fix
  separately, do not smuggle it into Cottonwood.**
- **COUNT-mode parity**, and the producer-side `GLOBAL_MODEL_KEYS` omission (census §4a-3) — the latter is
  the producer twin of B1 and lives in the gold lane, but **fixing one end without the other still yields a
  Cottonwood that is invisible.** Sequence them together.

---

## 6. SEQUENCING FOR DECOMPOSITION

```
   D6 RULING (Andrew)  ─────────────────┐
                                        ▼
   A1 · A2* · A3   ──────────────►  [ MERGE ]  → A-items only
   (D6-independent)                 [ ADD   ]  → A-items + B1 + B2
                                        │
   C1 (preventive, any time)  ──────────┤
                                        ▼
   §3 preconditions (artifact + 3 enumerations, NOT FE)
                                        ▼
   §4 render matrix (4 selections + control) → Andrew visual smoke = CLOSE
```
`*` A2 additionally needs CTO's acknowledgement that widening the `lastNonNull` migration is intended.

**Total FE effort, honest:** small on the MERGE branch (three XS/S items); moderate on ADD, and **dominated
by the four-selection re-verification, not by the edits.**

---

**RECORDING NOTE.** Landed durably rather than left in a message, per the lesson CTO landed at 1520Z: *a
decision whose only record is a message is a clock with no keeper* — and Andrew is resetting fabric workers
with clean handoffs, so a spec that exists only in a terminal dies at the reset.
