# COTTONWOOD MDPF PAIR — RELEASE NOTE, §2: FIGURES · DENOMINATORS · PLACEMENT

**Author:** `0.4.0_DS_ClientPlatform~T` · **Per:** Andrew-direct 18:10Z `@666fe25b0c` CALL 1, relayed
`1.0.0_SA_CTO` 72923 — *"the release note ships with the ruled figure splits, denominators, and the
$8.44M-explained/$36.2M-was-re-attribution history."*
**Scope of THIS file:** §2 only — the figures, their denominators, and where each lands.
**§1 (the re-attribution history + the WSE_COTMDL causal chain) is `0.6.2_AE_PartnerETL~A`'s**, which
holds that measurement; proposed at 72933, COO may route otherwise.

> ⛔ **EVERY FIGURE BELOW CARRIES ITS POPULATION ON THE SAME LINE AS THE NUMBER.** This thread moved one
> correct figure with a wrong denominator attached **four separate times** in four hours. A number
> without its population is the defect this document is shaped to prevent.

**Vintage of every figure:** assignment `2026-08-26` × value `2026-08-25`. Firm AUM
**$480,687,460.42** — *unchanged*. **Nothing here is new money. All of it is re-attribution and
re-bucketing.**

---

## 1. WHAT CHANGED, IN ONE LINE

Accounts held under a **non-Opal container that holds Opal children** were dropped before the blend
descent ever ran, so their Opal dollars never reached attribution. They are now walked. Separately,
one sleeve that is an **Opal SMA** was classified non-Opal and had landed in the residual; it now
buckets to SMAs.

---

## 2. THE MODELS LIMB — +$43,676,557.13

| model (display) | before | after | recovered | denominator |
|---|---|---|---|---|
| Long Term *(← Opal Conservative Growth)* | 34,739,871.01 | 58,077,721.46 | **+23,337,850.45** | 2 accounts |
| Ultra-Short Term | 6,700,756.16 | 18,597,065.93 | **+11,896,309.77** | 2 accounts |
| **Fixed Income** *(new key)* | — | 8,442,396.91 | **+8,442,396.91** | 2 accounts |
| **TOTAL** | 140,410,927.00 | **184,087,484.13** | **+43,676,557.13** | **2 accounts** |

**THE RECOVERED POPULATION IS 2 ACCOUNTS — NOT 129.** 129 is the *blast radius* of the removed
pre-filter; of those, **2** actually hold Opal constituents and carry the entire amount. The other
**127 hold none** and are correctly excluded. Both numbers are true; only one is the population.

`by_model` goes **5 keys → 6**, gaining `Fixed Income`. Decomposed total
**147,047,720.63 → 190,724,277.76**, tying to dim opal `190,724,277.75` (1c float, tolerance 0.02).

---

## 3. THE SMA LIMB — $1,393,065.98

| figure | value | denominator |
|---|---|---|
| SMAs (L0) → `opal_div_sma` | **$1,393,065.98** | **1 account** — `z0926705231` (`Anna *9237`) only |

`Anna *9238` carries **no DIVZ leg at all**. This limb's population is **one**, not the two that the
supervised segment spans.

**Ruling:** Andrew-direct 17:42/17:45Z `@9261c99991` — the `DIVZ SMA` sleeve *"is an OPAL SMA →
SMAs(L0)/DIVZ(L1)"*. Its prior classification as non-Opal is what put it in the residual.

**PLACEMENT (named, because placement is exactly what the sovereign corrected):**
`meta.sma_l0.by_key["opal_div_sma"]` in **both** artifacts. **NOT** in `by_model`, **NOT** in the
sidecar's `by_model_unit_values`, **NOT** in the identity-(i) sum, **NOT** in the residual.
**Key is the SERVED key `opal_div_sma`, not the taxonomy label `DIVZ`** — emitting the label would
mint a new key beside a live one.

---

## 4. THE SUPERVISED SEGMENT — AND ⚠ THE ONE FIGURE A READER WILL GET WRONG

| grain | value | denominator |
|---|---|---|
| **FULL SEGMENT — this is the field that ships** (`meta.client_opal_supervised.dollars`) | **$2,256,694.98** | **3 accounts** |
| non-Opal-parent subset (`…dollars_from_nonopal_parent_accounts`) | **$1,476,313.07** | **2 accounts** |

⚠ **THE CONDITIONAL-YES AT 18:10Z QUOTES `~$1.48M`. THAT IS THE 2-ACCOUNT SUBSET, NOT THE SERVED
FIELD.** The served field carries **$2,256,694.98**; the gap is **$780,381.91** — the sleeve dollars
on a third account, `z0926768741` (`Blended Opal / Satellite 50`, parent **is** Opal), whose
remainder is in scope under *"any account with Opal Models contained."*
**Surfaced at 72930; resolution is Andrew's or CTO's, not this lane's.** Recorded here so the number
and the sentence that authorized it cannot silently disagree on a client-facing surface.

**Itemisation — the segment is measured, not a remainder.** Parts asserted to sum per account:

```
sleeve            780,381.91   (3 sleeves on z0926768741)
unattributed-leg        0.00   <- was 1,393,065.98; going to ZERO *is* the DIVZ leg leaving
unallocated       1,476,313.07  (blend weights of 0.97 / 0.967 falling short of 1.0)
                 -------------
                  2,256,694.98   itemisation_breaks 0 · negative_residual_accounts 0
```

`supervised_basis: opal-models-residual` ships **on the artifact's face** — "Supervised" has two
referents on this firm and the bare word already cost this lane a $302,619,818.60 misclassification.

**Still in the residual by sovereign ruling, not by omission:** `Sleeve - Equity` $390,190.96,
`Sleeve - Tax-Free Bond` $374,583.32, `Sleeve - Core Money Market` $15,607.64. Andrew, 18:0xZ
`@4dc2cd6087`: *"CA Tax-Free Bond is not us, it would literally say Muni and I dont think those are
live yet."*

---

## 5. THE PARTITION HOLDS

```
supervised 2,256,694.98  +  SMAs 1,393,065.98  =  3,649,760.96
```
— **identical to the pre-DIVZ segment total.** The SMA ruling moved money **between two named
buckets**; it created and destroyed none. That invariant is a check arm, not a coincidence.

---

## 6. UNCHANGED, AND RE-MEASURED RATHER THAN ASSUMED

firm AUM **$480,687,460.42** · `model_aum` **$184,087,484.13** · `by_model` **6 keys** · bridge
**330/330, dropped 0** · identity (i) delta **0.0100** vs tolerance 0.02 · identities **PASS** ·
`json.dumps` clean on all three artifacts · `mdpf_category_registry` **absent from `sys.modules`
after a full build** (the import edge is gone by exercise, not by grep).

---

## 7. WHAT THIS DOCUMENT IS NOT

Not an acceptance and not an authorization to serve. **A9 is graded off the LAMBDA's run**, not these
in-process figures, on the protocol registered at 72813 — vintage must move on **both** `LastModified`
and `CodeSha256`, then delta `0.0100` present and `43676557.1200` absent as the PRIMARY arm. The serve
decision is **Andrew's**, conditional-YES per `@666fe25b0c`.
