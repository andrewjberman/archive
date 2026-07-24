# CI-R5R6R11R12 — ROW VERDICTS (5, 6, 11, 12)

**TO:** `MDPF_CHANNEL_INDEPENDENCE.CI-R5R6R11R12` @`53efddff35` · **Agent:** `0.4.0_DS_ClientPlatform~A` · 2026-07-24
**archetype:** IMPLEMENT · **Commits:** row 11 @`38b4569f0` (pushed) · rows 5+6 @`adfd8c327`
**Authorization:** Andrew-direct ~1720Z *"Go now, this is P0."*

---

## 0. VERDICT TABLE — and every one carries the LIVENESS column

The TO's sharpest constraint was aimed at me: *"your commits establish the DEFECTS. They CANNOT establish the
FIXES."* So each verdict below rests on an **exercise**, never on a citation of my own prior measurement.

| row | verdict | the EXERCISE that produced it | LIVE? |
|---|---|---|---|
| **5** — firm-axis poison gone | **TRUE-BUT-NOT-LIVE** | mutant on a **PRESENT, healthy** firm (49F, 92.9% of base) — cell composes instead of nulling | ❌ |
| **6** — carry-forward labelled basis+as-of | **TRUE-BUT-NOT-LIVE** *(W-7 half ROUTED, see §4)* | same mutant + 3 controls; real series 40 holes → 40 labelled held | ❌ |
| **11** — frontier stamp cannot silently overwrite | **TRUE-BUT-NOT-LIVE** | 7 constructed cases + live-S3 end-to-end + fired in a full build run | ❌ |
| **12** — `exempt_absorbed` not rendered as a reason | **NOT-YET-TRUE** | read the DEV code (satisfied) **and** the PROD code (actively contradicts) | ❌ |

> **THE LIVENESS COLUMN IS NOT A FOOTNOTE.** Rows 5, 6 and 11 are built, exercised and committed — **and
> running nowhere.** The mdpf tree's repo→runtime path is the EC2 runner, whose deployed copy of this producer
> is **51,999 bytes @2026-07-21T17:42:40Z against a 119,499-byte HEAD — 43% of HEAD, 20 commits behind** — and
> carries **zero occurrences** of every mechanism these rows touch. A closure report that counted these as
> "true" would be **true about a FILE and false about a RUNTIME.** Escalated as a P0 thirteenth item (§5).

---

## 1. ROW 5 — the `:1732` firm-axis poison

**Defect (measured previously, GC-W1 @`b078877020` — cited, not re-derived):** `acct.append(None if (cgap or
not cparts) ...)` — ANY contributing firm's `None` nulls the entire Global cell. Exercised live on 2026-05-21,
where 49F served 6,788 real accounts and Global published `None`.

**The repair:** carry-forward per PRD §2.4 (§2 below). The cell stops nulling.

**THE MUTANT — on the trap the TO named.** The forbidden shortcut was mutating a firm *already absent*, which
proves nothing. I mutated one **present and healthy**:

| | |
|---|---|
| target date | **2026-07-17** (class `band_2firm`, Global 7,686) |
| firm mutated | **49financial** — present, total 7,140, **92.9% of the Global base** |
| BEFORE (raw composed) | `Global[2026-07-17] = None` ← the defect |
| **AFTER** | **`7,671`, basis `held`, as_of `2026-07-16`** |

**Controls, each capable of failing:**
1. an unmutated healthy date stays `measured` — it does **not** silently become held ✓
2. the `absent` branch is **UNEXERCISED BY REAL DATA** (the series' first date is populated), so it was tested
   **synthetically and said so**: a leading gap stays honest-`None` and is **not** fabricated ✓
3. the mutation does not leak to neighbours ✓

## 2. ROW 6 — carry-forward with declared basis + as-of

`carry_forward_with_basis(dates, values) -> (values, basis, as_of)`, PRD §2.4 / Andrew ~1703Z.

```
value present             -> serve it,       basis "measured", as_of = that date
value absent, prior known -> serve the LAST, basis "held",     as_of = the date it came from
no prior value ever       -> honest-None,    basis "absent",   as_of = None
```

**Rows 5 and 6 are ONE mechanism, which is why this is one function.**

**WHY CARRY-FORWARD AND NOT SUM-WHAT-IS-PRESENT** — the tempting fix and the wrong one, and the PRD cites my
own measurement for it: carrying keeps the **basis** constant and lets only the **vintage** go stale; summing
whichever partners are present **changes what the number is** while looking current. GC-W2a measured that a
partner-sum fallback publishes `0` on 26 of 40 dates and reproduces `0 / 94 / 255` — the exact values this
file's own comment names as the historical defect.

**Two design points that would be easy to get backwards:**
- The **no-partial-total assertion runs on the RAW series, BEFORE the carry-forward.** It proves the producer
  never *fabricated* a partial. Moving it after would make it **pass vacuously forever**, since every
  honest-`None` becomes a held value.
- **`account_count_total_raw` is retained in the artifact.** A carry-forward that erases its own input cannot
  be audited.
- `count_provenance` is **unchanged**: provenance says *why the producer had no fresh number*, basis says
  *what is served in its place*. Collapsing them loses one.

**Result on the real series:** `{measured: 407, held: 40, absent: 0}` — **447/447 carry a value and every
carried one declares it.** Full `--firm all` dry-run: `ROWS5/6 carry-forward: 408 measured, 40 held, 0 absent
(of 448)`. This closes Andrew's original *choppiness* complaint without moving the defect.

## 3. ROW 11 — the frontier stamp cannot silently overwrite

Defect measured in GC-W2b @`4d0831382`: `load_account_dist_frontier_counts` **discarded** the source's
`period`, so the stamp site could not know its own staleness; `_latest_date()` resolves roster and valuation
partitions **independently**, so the as-of is *"whenever `account_distribution` last ran"*, not the axis date.

**Repair:** the as-of rides back under a `__as_of__` sentinel (the existing `__declared_cce__` idiom), popped
at all three call sites before model iteration; `frontier_stamp_staleness()` compares in **trading days**
(NEVER#1) and publishes the verdict in-band on `meta.frontier_count.staleness`. It **does not refuse** the
stamp — refusing would re-open the hole §2.4 exists to close. It makes the overwrite **declared**, which is
the row's actual requirement.

**EXERCISED** (the named trap was adding the check and never invoking it):
- 7 constructed cases fire correctly, including a **weekend-dated stamp** (Sunday 07-19 → 3 trading days —
  which is why `_trading_days_after` derives the exclusive count explicitly rather than subtracting 1 from the
  shim's *inclusive* helper) and an **absent as-of returning `UNKNOWN`, explicitly not `FRESH`** — an
  instrument that cannot fail is not an instrument.
- **Live S3 end-to-end**, surfacing three real states: 49F **STALE 1**, INF **STALE 2**, global
  **`AHEAD_OF_AXIS`** (a stamp dated *after* the cell it would land on — the foreign-day-roster class). That
  last one only surfaced because a negative is reported as its own verdict rather than clamped to zero.
- **Fired in a full build run**, not only in isolation.
- Sentinel-leak checked on all three legs: `__as_of__` never reaches the model-key space.
- The **Rule 14 gate caught a real defect mid-build** — an unused variable on the inflection leg meaning that
  leg's stamp would have stayed silent. Fixed, not silenced.

## 4. ROW 12 — NOT-YET-TRUE, and the reason is worse than "not done"

COO's steer was that this may already be true via the not-render branch, and not to build past it. **The code
half IS satisfied** — verified by reading `portal/src/lib/pairedProvenanceRead.ts` @`d1ba89b9` (DEV):
non-assertive label `'Exempt / absorbed elsewhere'` (`:109`), **excluded** from `VALUE_BEARING_NON_MEASURED`
(`:185-186`) so it drives no band, one tooltip call site (`ModelPortfolios.tsx:1234`), and an explicit
in-source prohibition at `:166`.

> **But PROD (`17256834`) predates it and does something worse than rendering the label as a reason.** PROD's
> `VALID` set is `{measured, interpolated_estimate, absent}` (`:96`) and `readCountTotalSeries` (`:272-282`)
> **coerces** anything outside it: *"invalid count_provenance … treating as interpolated_estimate"*.
> **So all 38 `exempt_absorbed` dates render as `interpolated_estimate` — a claim that the value was
> ESTIMATED BY INTERPOLATION, when it is an honest absence.** A *wrong and more assertive* statement.

Controls run on both retrievals (PROD file 332 lines, `ModelPortfolios` 2,707), so the zero-matches are a real
absence, not a broken `git show`. **Gate case:** it closes on a portal DEV→PROD promote, which is genuinely
blocked (Actions billing). **I stopped there and did not build the producer-side split.**

### 4a. W-7, folded into row 6 — ROUTED, NOT DECIDED

18 non-trading rows sit on a declared trading-day axis. **The obvious fix is the shortcut COO himself named**
— *"deleting the 16 weekend rows and rewriting the docstring to match would turn both criteria green, having
destroyed data to satisfy a docstring nobody verified."* The options are (a) delete rows — destroys served
data and changes a served contract, or (b) make the declaration honest: the spine is 447 with **429** trading
days, and cottonwood's axis **is** the full spine by design while 49F/INF are the trading-day set (I verified
those two 429s are the **same set**, symmetric difference 0 both ways). **(b) is clearly right to me, but it
changes what the artifact declares about itself — a contract call at CTO's gate, not one to make at speed
inside another row.**

## 5. THE THIRTEENTH ITEM (escalated P0)

The mdpf repo→runtime path is unowned and uninstrumented:
- deploy is the **EC2 runner** (`mdpf-daily-dispatch.sh:125` `s3 sync s3://opal-data-mdpf/code/scripts/`,
  `:438`, `:457`/`:513`) — **a push cannot deploy mdpf** (`file_to_s3_target(...)` → `None`; mdpf is not a
  `PIPELINE_MAP` key, `safe_deploy_core.py:22-26`).
- the deployed copy is **51,999 B @2026-07-21T17:42:40Z** vs **119,499 B** at HEAD, with **0 occurrences** of
  `frontier_stamp_staleness` / `ad_frontier` / `load_served_account_count` /
  `GLOBAL_CROSS_AXIS_EXEMPT_DATES` / `SMA_COUNT_PRESERVE_KEYS`.
- runner telemetry stops at **2026-07-18T15:02:06Z**. **NEVER#1 resolved:** 07-18 was a Saturday; 07-20→today
  are five trading days. **Not a weekend artifact.**
- yet the served artifacts are **fresh (07-23T21:47Z)** and carry classes the deployed code cannot emit.

**LOGICALLY FORCED:** whatever produced the served artifacts was **not** the deployed code.
**INFERRED AND NOT CLAIMED:** that they came from ad-hoc runs. I did not observe a run, and I did **not**
determine whether the trigger fires-and-fails-before-telemetry versus does not fire at all — **two different
defects, and I refused to guess between them.**
*(COO independently re-measured and added depth: 20 commits / +67,500 bytes behind, plus a **fail-open** at
`:525`/`:568` where a missing Stage 6 is a non-fatal WARN while a missing feeder at `:126` is FATAL.)*

## 6. GROUNDING LEDGER

| claim | grade | grounding |
|---|---|---|
| row 5 repair works on a present firm | **EXERCISED (mutant + 3 controls)** | 49F @2026-07-17, served bytes ETag `55a8b379…` |
| `absent` branch behaviour | **EXERCISED SYNTHETICALLY, said so** | unexercised by real data; constructed leading-gap case |
| row 6 labels on the real series | **MEASURED** | `{measured 407, held 40, absent 0}` of 447 |
| row 11 guard fires | **EXERCISED — constructed + live + in-build** | 7 cases, live S3 on 3 legs, full dry-run |
| row 12 PROD coerces to `interpolated_estimate` | **SOURCE-CONFIRMED** | `pairedProvenanceRead.ts:96`, `:272-282` @`origin/PROD` |
| deployed mdpf copy is ancient | **MEASURED** | live S3 listing + symbol census, 5 symbols × 0 occurrences |
| what produced the served artifacts | **INFERRED — NOT CLAIMED** | not observed; two candidate defects not discriminated |
| rows 5/6/11 are LIVE | **EXPLICITLY FALSE** | the deployed copy lacks every mechanism |

**Explicit-Z throughout. Denominators printed. Ad-hoc runs used only to EXERCISE, never cited as production
evidence (amended NEVER#4 @`7d2b8cf6f`). No EC2 deploy touched — Rule 7/12, not my lane.**
