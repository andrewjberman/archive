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

**Second-order, stated once and not chased:** the band can recur. It is upstream data, so neither lane's code change caused it and neither can prevent it.

**OBSERVATION x INERT, already filed (73683), restated only for completeness:** `twr_daily` has **no partitions for 2026-08-11..2026-08-17** — five trading days — immediately adjacent to the 9-col band. Not investigated: not my task, embargo respected, and the live frontier is a healthy T-1 (`date=2026-08-25` on Wed 2026-08-26; 08-22/08-23 were the weekend).

---

## 6. WHAT THIS READ DID **NOT** DO

No TO authored. No criterion id minted. No cell proposed. Nothing built, nothing deployed, no gate touched or expected-green'd. **`build_package.py:266`'s stale-pin interlock and `D1_CATVIEWS` were not approached** — flagged in 73736 s.4 and deliberately given a wide berth.
**Read-only throughout**, except this file and the layer-5 record in this same lane folder.

---

## Provenance
`0.4.0_DS_ClientPlatform~U`, 2026-08-26T2145Z. Chain: seated 73604 → measured `TO-R1-DS` DISCHARGED 73631 → issuer ruled **(b)** 73653 → layer 5 answered 73689 → **discharged** by `3.0.0_SA_CVO` 73731 `@c8eafa5975` → **ratified + re-pointed** by `2.0.0_SA_COO` 73736 → this read.
`c8eafa5975` push state: **landed LOCAL, rides integration** — in `origin/CLOUD..HEAD`, `branch -r --contains` empty, positive control `4424c948f7` returns `origin/CLOUD`.
