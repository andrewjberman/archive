# ADVI_PERFRP — ROUND-2 SCOPE READ (input to `2.0.0_SA_COO`'s cut)

**Seat:** `0.4.0_DS_ClientPlatform~U` · **Stamped:** 2026-08-26T2145Z · **Commissioned:** `2.0.0_SA_COO` 73736 s.2
**Mandate:** SCOPE ONLY — no TOs authored, no criterion ids minted, nothing built. A cell round 2 needs that the decomp lacks is a FINDING for the issuer.
**Grounded on:** (a) the delivered round-1 artifacts · (b) the layer-5 partition (73689, discharged `@c8eafa5975`) · (c) the O-1..O-6 spec-at-pickup verdicts (73683)
**Decomp:** `workflows/atom_decomposition/runs/advi-perfrp/20260824T201222Z/DECOMP.md` @1ce9b2d6bc

---

## 1. ⛔ FINDING FIRST — THE DECOMP DOES NOT NAME A "ROUND 2". `DS~PRF / DE~PRF / AE~PRF` **IS ROUND 1**, AND IT IS CUT AND DELIVERED.

73736 s.2 reads: *"The decomp names round 2 as the next step (`DS~PRF / DE~PRF / AE~PRF`, one project per lane)."*

**Measured at the decomp's own face — `DECOMP.md:212-219`, s.5 STATUS + HAND-OFF:** that three-lane split is the **round-1 TO cut**, and it is the cut that already happened:
> *"**TOs after cert, ONE PROJECT PER Tier-2 LANE INSTANCE** ... **`DS~<PRF>`** {`a-1..a-6`, `b-1..b-7`, `c-1` emitter half, `inv-2/3/5/6`} · **`DE~<PRF>`** {`d-1..d-8`, `inv-1`, `inv-3` render half} · **`AE~<PRF>`** {`c-1` publisher/IAM half, `c-2`, `c-3`, `inv-4`, `inv-5` IAM half}"*

That is **exactly** the 18 / 10 / 5 partition layer 5 measured from the TO faces. The document's own title is `— ROUND 1`.

**THE DECOMP'S NEXT NAMED STEP IS WAVE 3, NOT A ROUND 2** (`DECOMP.md:219`):
> *"**Wave 3 (order s.3):** the attribution cells (`fact_performance_attribution_daily`, P-7) open only when INSURE 49F is live; COT binding after COTKEY."*

⛔ **CONSEQUENCE FOR THE CUT: there is no undelivered decomp-declared cell set waiting to become round-2 TOs.** A round 2 cut against this decomp would either (i) re-issue round-1 cells — the failure mode this seat was seated on and that 73653 already owns — or (ii) require **NEW cells the decomp does not contain**, which is the FINDING 73736 asked to be told rather than discover.

---

## 2. THE DENOMINATOR — of the 36

**The decomp's own arithmetic (`DECOMP.md:205-206`) INDEPENDENTLY CORROBORATES the layer-5 partition:**
> *"**Cells: 36** = inv:6 · a:6 · b:7 · c:3 · d:8 · e:1 · f:1 · g:4. **Criterion-bearing: 32** (the four `g` boundary cells carry none by declaration)."*

Layer 5 derived **30 (three TOs) + 2 (CVO) + 4 (boundaries)** from the **TO faces**. The decomp asserts **32 criterion-bearing + 4 boundaries** from **its own side**. **30 + 2 = 32.** Two different instruments, same partition — and I did not have this line when I ran layer 5.

| bucket | n | state | instrument |
|---|---|---|---|
| **DS `TO-R1-DS`** | 18 | **DISCHARGED** — TO `<status>complete</status>` | proof-of-spec **VALID rc=0**, 14 rows, 18/18 fwd + 18/18 back; **corroborated independently** by a landed feature commit per AC and push state vs a fetched ref |
| **AE `TO-R1-AE`** | 5 | **OPEN LIMBS** — TO `<status>ACTIVE</status>` | proof-of-spec **VALID rc=0**, 6 rows, 5/5 fwd + 5/5 back. `0.7.0_AE_CloudOps~L` is **LIVE on it now** (AC4 closed 73691; AC1 data half moving) |
| **DE `TO-R1-DE`** | 10 | **PROOF-VALID, LANE UNSEATED** | proof-of-spec **VALID rc=0**, 13 rows, 10/10 fwd + 10/10 back. `0.4.0_DE_ClientPlatform~E` reads **NOT REGISTERED**, no pending TOs |
| **CVO** | 2 | `e-1` **TRIGGERABLE** (fires on `b-1`'s first emission, which occurred @495564c875) · `f-1` standing control | CVO-owned; not this lane's to call |
| **BOUNDARIES** | 4 | **DECLARED OUT**, carry no criterion by declaration | `g-1` deferred/GAP by ruling · `g-2` method reused + wrapper trio routed to COO · `g-3` INF+COT at their gates · `g-4` insurance = `ADVI_INSURE`'s cells |
| | **36** | | |

⛔ **A BOUNDARY I DECLINE TO CROSS:** I ran the proof instrument on all three, but I corroborated **only DS** against landed commits and push state. **AE's 5 and DE's 10 read VALID on the proof instance alone from my vantage** — and a valid proof instance is not the same claim as delivered work. **Their discharge is their lanes' and CVO's to assert, not mine.** Stated because the table above would otherwise read as three equal verdicts and they are not.

---

## 3. WAVE-3 GATE STATE — MEASURED, because it decides whether there is anything to cut at all

| gate | decomp condition | measured state | verdict |
|---|---|---|---|
| INSURE 49F live | attribution cells "open only when INSURE 49F is live" | `gold/advi/insurance/` holds **exactly one prefix: `insurance_nav_current/`** | **PARTIAL** — one table live. Whether that satisfies "INSURE 49F is live" is the issuer's call, not a measurement |
| the wave-3 cell itself | `fact_performance_attribution_daily` | **ABSENT** from `gold/advi/canonical/` (denominator: the 8 prefixes in O-1) | not built |
| COT binding | "COT binding after COTKEY" | `org/projects/ADVI_COTKEY.json` → `status: active`, **STAGE 1 REGISTERED**, in the Rule-27 pipeline | **CLOSED** — not ruled |

**So wave 3 is gated at two of three, and the one that is not gated is a partial the issuer must adjudicate.**

---

## 4. WHAT ROUND 2 WOULD ACTUALLY COVER — candidates, not cells

**Ordered by whether they are unblocked today.**

**(A) UNBLOCKED — open limbs inside round-1 TOs.** Not new cells; the existing ones finishing. `AE~L` is executing this now; the DE lane is unseated with `TO-R1-DE` proof-valid but its `<status>` still `ACTIVE`. **A cut here would collide with a live seat — sequencing, not scope.**

**(B) UNBLOCKED — the O-2 input-dependence question. THIS IS THE FINDING, and the decomp has no cell for it.** See s.5.

**(C) GATED — wave 3.** Attribution cells + COT binding. Blocked per s.3 above; not round-2 material until the gates lift.

**(D) RULED OUT — `g-1` deferred cards** (benchmarks, MWR, asset-level contribution, Capital Markets, target allocation, projected income, fixed income, wallet share, statements/PDF). **"DEFERRED or GAP by ruling — no cell, no tile"** (`DECOMP.md:136`). Un-deferring is Andrew's or CTO's word, never a lane's.

**(E) NAMED, NOT COMMISSIONED — the content-level lane-assignment pass** (does `c-1`'s "emitter half" truly belong to DS rather than AE). `3.0.0_SA_CVO` 73731 explicitly declined to commission it tonight and named it as its own item *"because an item that keeps absorbing adjacent questions never closes."* **Recorded here so the round-2 cut does not silently absorb it.**

---

## 5. ⛔ THE FINDING — O-2's MOVEMENT HAS NO CELL, AND THE ARTIFACT CANNOT SAY WHICH ARM IT TOOK

**MEASURED (O-2, my 73683).** `twr_daily`'s four TWR operands — `bmv`, `emv`, `cf_net`, `cf_gross` — were ABSENT and **returned at `date=2026-08-24`**. Full census, **DENOMINATOR 531 partitions** (2024-07-09..2026-08-25), every one read: **13 cols on 525, 9 cols on 6** (`2025-01-09`, `2026-08-10`, `2026-08-18`..`2026-08-21`). 525 + 6 = 531.

**THE DELIVERED CODE IS CORRECT AND WAS NEVER AT RISK.** `perfrp_emit_core.py:120` declares `TWR_OPERANDS`; `:156` computes `missing_operands` **at runtime**; `perfrp_contract.py:363` sources `bmv`/`emv` from `canonical_valuation`, **not** from `twr_daily`'s own columns. The producer branches; it never baked the 9.

**INDEPENDENTLY CORROBORATED FROM THE OTHER SIDE, THIS SESSION:** `0.7.0_AE_CloudOps~L` measured performance now **COMPUTED 6415/7348 acct + 3931/4398 rel, `INPUTS_ABSENT`=0 both grains** — the downstream signature of the same upstream event, on a different instrument, without either seat knowing the other's half (linked in my 73749).

>> **THE ROUND-2 QUESTION, and it is a QUESTION not a claim: the projection's output is INPUT-DEPENDENT across a boundary nothing declares. A served figure computed on a 9-col partition and one computed on a 13-col partition are DIFFERENT COMPUTATIONS, and nothing on the artifact's face says which arm produced it.** That is the CLAUDE.md §4 shape — *a value must carry its claim, in a field a consumer can reject on* — and the consuming half is what makes it real. **Whether that warrants a provenance field is a DECOMP question and therefore the issuer's.** I have not minted a cell, named an id, or proposed a schema. <<

⛔ **CORRECTED 2026-08-26T2150Z BY `0.7.0_AE_CloudOps~L` (73789). MY CAUSE CLAUSE WAS WRONG AND THE CORRECTION IS ACCEPTED IN FULL.**
This section originally read: *"the band can recur. It is upstream data, so neither lane's code change caused it and neither can prevent it."*
**IT IS A CODE FIX, IT IS DATED, AND IT IS ATTRIBUTABLE.** `_pull_prev_valuation_into_mirror` landed in **`b9a665364f`** (2026-08-25T02:57:56Z, `0.4.0_DS_ClientPlatform~H`, OPAL_GLDRNS twr D-1 mirror), an ancestor of the bytes measured DEPLOYED on 08-25 — **with a negative control (`b9915d8271` is NOT an ancestor), so the test discriminates.**
**The decisive instrument is the two adjacent SCHEDULED chain fires, which I never looked at:**
`chain_20260824T124542Z` → `date=2026-08-21`, **no prev-valuation-pull line at all** (pre-mirror code) → the **9-col** partition.
`chain_20260825T124542Z` → `date=2026-08-24`, *"prev valuation pull: 2 object(s) for date=2026-08-21 (D-1 of 2026-08-24) -> mirror"* → the **13-col** partition.
**The transition boundary in my census sits EXACTLY at the first chain fire after the fix reached `_code/`.** And the 08-22/08-23 hole is Saturday and Sunday — the D-1 pull took Friday 08-21 for chain date Monday 08-24, the prior TRADING day. Correct calendar behaviour, not a gap.

**WHY MY VERSION WAS WRONG, and it is the transferable half:** I measured the **STORAGE** side (schema width across 531 partitions) and inferred a cause from it. **A schema census can establish WHEN a column set changed and is structurally blind to WHY** — the producer-side chain log and the commit ancestry are the instruments that discriminate cause, and I ran neither. ⚠ **`b9a665364f` was visible in my own first `git log` read of this session and I did not connect it.**
⚠ **And the direction matters:** *"fragile upstream data"* is the **SAFE-SOUNDING** claim, so nobody would have pushed back on it. `0.7.0_AE_CloudOps~L` spent a message on one clause precisely because *"upstream data that can move back"* and *"a durable code fix"* carry **OPPOSITE RISK POSTURES** for the 49F serve, and Andrew's DATA half is being adjudicated against exactly this.

**WHAT SURVIVES, per that seat's own boundary — it does not overshoot:** the band **can** still recur, for a **DIFFERENT reason than the one I named.** The mirror pull reads D-1's already-uploaded `canonical_valuation` from S3 and carries an explicit `ABSENT-IN-S3 ... holds 0` branch, so **a MISSING D-1 refuses again** — which is the shape of the 2026-08-11..08-17 hole filed below. **Durable against the recurrence I named; still exposed to a missing D-1. Two failure modes, two owners, not merged.**
**AND THE ROUND-2 QUESTION GETS SHARPER, NOT WEAKER:** the arm boundary is now a **KNOWN, DATED, ATTRIBUTABLE** event, so a provenance field would have something concrete to record. Still a decomp candidate for the issuer; still not a cell either lane minted.

**OBSERVATION x INERT, already filed (73683), restated only for completeness:** `twr_daily` has **no partitions for 2026-08-11..2026-08-17** — five trading days — immediately adjacent to the 9-col band. Not investigated: not my task, embargo respected, and the live frontier is a healthy T-1 (`date=2026-08-25` on Wed 2026-08-26; 08-22/08-23 were the weekend).

---

## 5b. ⛔ ADDED 2026-08-26T2205Z — THE OUTLIER COHORT. A ROUND-2 INPUT, AND THE REMEDY SHAPE IS NOT WHAT THE PACKET ASSUMES.

`2.0.0_SA_COO` 73812 rules that Andrew's DATA half and `0.7.0_AE_CloudOps~L`'s outlier finding go to him in **one packet**, because the outlier **arms at the instant of a YES**. That message states the cause as **OPEN** — *"a near-zero BMV denominator and an unneutralised external cash flow both produce this shape, and the separating control was not run."* **I ran it** (emitter content is `TO-R1-DS`, this lane; read-only). Reported as 73823 and 73844.

**BOTH NAMED CAUSES FAIL.**
· **Cash flow — FALSIFIED on 2 of 4** at `date=2026-08-25`: `cf_net` is **exactly 0.00** for `0057178995` (+1054.3%) and `0012906417` (-88.1%). And `0013289888`'s flow is **NEGATIVE 10,000** while value rises **27.24x** — the wrong sign for the cash-flow story.
· **Near-zero BMV — neither necessary nor sufficient.** `bmv<2,000`: **n=370, 3 extreme (0.81%)** — 367 of 370 are fine. `bmv>=2,000`: n=6,042, 1 extreme — and that one is the **+2722.3%**, at bmv **10,135**.

**AND THE POPULATION IS NOT FOUR ACCOUNTS — IT IS A DAILY COHORT THAT CHURNS COMPLETELY.**

| date | non-null `r_net` | \|r_net\|>20% | max | bimodal gap |
|---|---|---|---|---|
| 2026-08-24 | 6,412 | **9** | **+69,056.0%** (`0032486794`, bmv 57.00) | #9 -89.4% → #10 -12.6% = **7.1x** |
| 2026-08-25 | 6,415 | **4** | +2,722.3% | #4 -50.0% → #5 +7.2% = **7.0x** |

**INTERSECTION: EMPTY.** No account persists across the two days.
⛔ **THE PACKET'S HEADLINE `+2722.3%` IS DATE-SCOPED AND IS NOT THE WORST OBSERVED — 08-24 printed `+69,056.0%`, 25x higher.** State the DATE as well as the GRAIN.
⛔ **A SUPPRESSION LIST IS OBSOLETE THE DAY AFTER IT IS WRITTEN.** 73812 s.3's *"suppressing four keys of 6415 is small"* is true of a fixed set; **this set is not fixed.** The remedy must be a per-day RULE, not an enumeration.
⛔ **AND A DENOMINATOR FLOOR MISSES MORE THAN HALF:** across both days, of **13** outliers a `bmv<2,000` floor catches **6** and misses **7** — including `-100.0%` at bmv **263,880.75** and `+108.6%` at bmv **241,834.54**. **BMV is not the discriminator at either date.**

**THE THRESHOLD IS NOT MANUFACTURING THIS.** A chosen cutoff is exactly where an artifact would hide, so it was tested: **both days break independently at the same place** (7.1x and 7.0x gaps). Any line from ~15% to ~45% selects the identical sets.

**BASE RATE: 2 of 2.** The five 9-col partitions (`2026-08-10`, `08-18`..`08-21`) carry **ZERO non-null `r_net`** — returns did not exist in that band, which corroborates the `INPUTS_ABSENT` story from the storage side. **Returns have EVER been computed on exactly two dates and BOTH produced a bimodal implausible-return cohort.** *Stated as 2 of 2, not as a rate — two dates is a small denominator for the word "every day."*

**SECOND READ — `canonical_positions` + `canonical_valuation`, both dates:** all four 08-25 accounts carry `mkt_value_long` = `mkt_value_short` = **0.0** with the whole value in `fair_value`; **two hold ZERO positions on both dates** while their valuation moves; one gained a position (6→7) as value went 11.5x. **The valuation is not backed by a coherent position set.**

**WHAT IS NOT CLAIMED:** no root cause — the upstream loader was not read. The **return math is not what is wrong**: `0.7.0_AE_CloudOps~L` measured the deployed emitter modules **8/8 MATCH with 4 of 5 vintage controls firing**. **Whether these accounts should produce a return at all is ARCHITECTURAL and no measurement answers it** — a zero-position account with a moving fair value may be a genuine cash or alternative holding rather than a defect.

**AS A ROUND-2 INPUT:** this is the second candidate (with the O-2 provenance question in s.5) that **the decomp has no cell for.** Both are the issuer's to rule. **No cell minted, no id coined, no emitter changed.**

---

## 6. WHAT THIS READ DID **NOT** DO

No TO authored. No criterion id minted. No cell proposed. Nothing built, nothing deployed, no gate touched or expected-green'd. **`build_package.py:266`'s stale-pin interlock and `D1_CATVIEWS` were not approached** — flagged in 73736 s.4 and deliberately given a wide berth.
**Read-only throughout**, except this file and the layer-5 record in this same lane folder.

---

## Provenance
`0.4.0_DS_ClientPlatform~U`, 2026-08-26T2145Z. Chain: seated 73604 → measured `TO-R1-DS` DISCHARGED 73631 → issuer ruled **(b)** 73653 → layer 5 answered 73689 → **discharged** by `3.0.0_SA_CVO` 73731 `@c8eafa5975` → **ratified + re-pointed** by `2.0.0_SA_COO` 73736 → this read.
`c8eafa5975` push state: **landed LOCAL, rides integration** — in `origin/CLOUD..HEAD`, `branch -r --contains` empty, positive control `4424c948f7` returns `origin/CLOUD`.
