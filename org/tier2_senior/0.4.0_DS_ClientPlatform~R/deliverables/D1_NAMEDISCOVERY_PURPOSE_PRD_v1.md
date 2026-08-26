# D1_NAMEDISCOVERY — PURPOSE-LEVEL PRD v1

**Rule 27 step 2.** WHAT and WHY only. No design, no matcher, no thresholds, no schema mint, no TO.
**Author:** `0.4.0_DS_ClientPlatform~R` · **Allocated by:** `2.0.0_SA_COO` 73551 · **Date:** 2026-08-26
**Project:** `org/projects/D1_NAMEDISCOVERY.json` @`e9990032fe` (registered by `0.0.0_AB_MSTR`, LD-0460)
**Consumes (do not re-derive):** `@195cfbdbe9` · `@4dc2cd6087` · `3.0.0_SA_CVO` 73238 s.2

> **ACCEPTANCE BAR FOR THIS DOCUMENT (issuer's, verbatim):** *"I can read it and produce an
> atom-decomp without asking you a question."* Where that was not achievable, §7 names the reason
> rather than inventing an answer.

---

## 1. THE SOVEREIGN'S WORD — VERBATIM

**Andrew-direct 2026-08-26 ~17:56Z**, at the `1.0.0_SA_CTO` terminal, immediately after his
DIVZ-SMA bucketing ruling:

> Yeah this means whatever system we have for scanning for "Opal" clearly is not enough for these
> guys, who were SUPPOSED to label every opal model/sma/etc in their accounts. I think we need to
> create a comparable mechanism that scans for SMAs as well, like any constituent-level name
> including "DIVZ" "DIVZ SMA" for DIVZ SMA, maybe "Tax SMA" and "Tax" disambiguated as a
> single-word name,  "Opal Tax SMA" would be potential too, as we do not know how these fuckers
> name these things. Same for "Muni" "Muni SMA" "Opal Muni" "Opal Muni SMA". same for really any
> opal ETF, and associated conjunctions, the etfs including PFOE PFDE IDVZ DIVZ.

**~17:58Z, confirming the structured reading:**

> Yeah just saw your reponse, youre exactly correct, we need to be on the lookout on a fuzzy basis
> for these things

**~18:06Z, ruling `CA Tax-Free Bond` not Opal:**

> CA Tax-Free Bond is not us, it would literally say Muni and I dont think those are live yet

---

## 2. THE PROBLEM

**Partner labeling of Opal products is unreliable, and it is unreliable BY MEASUREMENT, not by
suspicion.** The partner was contractually supposed to label every Opal model/SMA in their
accounts and did not do so reliably.

Opal's existing discovery is a name scan for **"Opal"** operating at the **model/blend** level. A
holding that is an Opal product but is *not named* with "Opal" — and is not a blend — is invisible
to it. On 2026-08-26 the **DIVZ SMA sleeve read as non-Opal** to that scan and therefore
mis-bucketed in a client-facing figure. Andrew ruled DIVZ an Opal SMA by hand at ~17:42/17:45Z.

**The hand-ruling fixed one instance. It did not fix the class.** The next unlabeled Opal SMA or
ETF sleeve repeats the incident, and nothing in the estate is looking for it.

**WHY IT MATTERS:** a missed Opal constituent does not fail loudly. It lands in the wrong bucket
of a **client-facing** AUA/AUM figure and reads as a correct number. The error is silent,
directional (Opal dollars understated), and discovered only by someone noticing a name.

---

## 3. WHAT IS BEING BUILT — THE PURPOSE IN ONE SENTENCE

**A discovery mechanism, comparable to the existing "Opal" model scan but operating at
CONSTITUENT level, that fuzzily catches candidate Opal SMA and ETF names in partner-supplied data
and SURFACES them for deliberate classification — never classifying them itself.**

Andrew's posture, in his words: **"on the lookout on a fuzzy basis."**

---

## 4. THE DOMAIN — WITH ITS DENOMINATOR, AND WHERE THE DENOMINATOR IS OPEN

### 4.1 The token set — 6 NAMED

`DIVZ` · `PFOE` · `PFDE` · `IDVZ` · `Tax` · `Muni`

### 4.2 The variant grammar per token — 4 NAMED FORMS

| form | ruling's own examples |
|---|---|
| bare token | `DIVZ`, `Tax`, `Muni` |
| `<token> SMA` | `DIVZ SMA`, `Tax SMA`, `Muni SMA` |
| `Opal <token>` | `Opal Muni` |
| `Opal <token> SMA` | `Opal Tax SMA`, `Opal Muni SMA` |

Plus **"associated conjunctions"** for the ETF tickers — named in the ruling, not enumerated.

**PRINTED DENOMINATOR: 6 named tokens × 4 named forms = 24 named variant strings, over an ETF
population the ruling leaves OPEN.**

⛔ **THE DENOMINATOR IS HONESTLY OPEN AND MUST NOT BE PRINTED AS CLOSED.** The ruling says *"really
any opal ETF, and associated conjunctions, the etfs **including** PFOE PFDE IDVZ DIVZ."*
**"Including" is not "namely."** The four tickers are exemplary, not exhaustive, and "associated
conjunctions" is an unenumerated form class. **Any decomp cell that treats 24 as the complete
domain is measuring a set the ruling did not close.** Whether the mechanism must reach ETFs beyond
the four named is a SCOPE CALL for the issuer (§7.2).

### 4.3 Two measured properties of this domain

**(a) TWO OF THE SIX TOKENS HAVE NO REGISTRY ENTRY, BY RULING.** The existing `strategy_id`
registry anchor (`aua_taxonomy.v1.json:111`, the D1_CATVIEWS SMA member set) carries
**6 SMA members, 4 of which carry a `strategy_id`**: `divz`, `muni`, `pfoe`, `tax`. `idvz` and
`pfde` are **un-noded — the RULED Q1 state, explicitly "not missing data."**
**CONSEQUENCE FOR PURPOSE:** the mechanism must be able to surface a candidate for a token whose
registry entry **does not yet exist**. A design that resolves a match against the registry and
treats a miss as "not Opal" inverts the ruling for 2 of the 6 tokens.

**(b) ONE TOKEN'S EXPECTED TRUE-POSITIVE COUNT TODAY IS ZERO.** Andrew: the Opal muni product
*"would literally say Muni and I dont think those are live yet."* So a `Muni` match in today's
book is **EARLY or SUSPECT**, not expected. The record calls this *"worth a flag-loud."*
**This is a property of the domain, stated here as such.** The mechanism for flagging is HOW and
is out of scope.

**(c) THE OPAL-SIDE NAMING DISCRIMINATOR.** Partner tax-free descriptors (`CA Tax-Free Bond`,
`Tax-Free Bond`) are **NOT** Opal name-forms; the Opal muni would *"literally say Muni."* The
`Tax`/`Muni` tokens stay candidate-catchers, but the Muni-literal is the Opal-side convention.

---

## 5. THE TWO INVARIANTS — BOTH FROM THE RULING, BOTH BINDING

### INVARIANT 1 — FUZZY AT DISCOVERY, EXACT AT THE SERVED KEY

A **wide net** finds candidates (variant grammar, token-boundary tolerance). A **deliberate gate**
decides what becomes a served key. The two stages have **opposite error preferences**: discovery
should over-catch, the served key must not.

⛔ **AND THE COMMON-NOUN HALF IS PART OF THIS INVARIANT, NOT A DETAIL.** `Tax` and `Muni` are
**native English vocabulary in this estate.** They match at **word/name boundary only, never as
substrings.** This is not a preference: a substring census over a common-noun token has been
measured in this estate returning **422 "violations" that were native vocabulary**, and the same
class produced an `egress`←`regression` false hit. **A substring sweep on `Tax` returns the
estate.** Any decomp cell that measures `Tax`/`Muni` occupancy must print the predicate it used.

### INVARIANT 2 — DISCOVERY SURFACES, IT NEVER SILENTLY CLASSIFIES

A matched-but-unregistered name is a **surfaced candidate for review** — the existing registry F5
crosswalk-review WARN shape — **never an auto-classification into a served bucket.**

**WHY, with the standing example from the same day:** the DIVZ SMA's served key is `opal_div_sma`,
**not** `DIVZ`. A mechanism that auto-slugged a discovered name into a served key would have
minted the wrong key while looking successful. **The catch that the served key is deliberate is
the reason this invariant exists.**

---

## 6. THE REQUIRED FAILURE MODE (Rule 28 q7) — AND THE EXEMPLAR THAT SHOWS BOTH ANSWERS

**THE QUESTION THE MECHANISM MUST ANSWER BEFORE IT IS BUILT: what does it return when it CANNOT
answer, and is that DISTINGUISHABLE from a genuine negative?**

For this mechanism the two states are:

| state | meaning | what it must NOT be confused with |
|---|---|---|
| **NO MATCH** | this name is not an Opal candidate | — |
| **UNKNOWN** | this name matched, and the mechanism has no registered classification for it | **NO MATCH.** Conflating them is the DIVZ incident, mechanised. |

⛔ **THESE TWO MUST BE DIFFERENT VALUES A CONSUMER CAN BRANCH ON.** If "I do not recognise this
name" and "this name is not Opal" render identically, the mechanism reproduces the exact defect it
was built to fix — and it will do so silently, because both look like a clean negative.

### The enforcement-shape exemplar — two live producers, opposite policies

`3.0.0_SA_CVO` 73238 s.2 exercised the estate's own two answers to this question:

- **`build_cottonwood_mdpf_slice.py` RAISES** on an unknown model name, by design, with the remedy
  in the exception text. `canonical_key('DIVZ SMA')` → `ValueError`. **Fails LOUD, at build.**
- **The `GLOBAL_MODEL_KEYS` fold SKIPS** a key it does not know. **Fails SILENT.**

> **THE SLICE RAISES, THE FOLD SKIPS. That contrast IS the difference between "exact at the served
> key" being ENFORCED and being HOPED FOR.**

**This PRD does not choose the policy — that is design.** It requires that **the mechanism declare
one, and that the declared policy make UNKNOWN distinguishable from NO MATCH.**

⚠ **A LIVE FORWARD HAZARD, NAMED HERE AND NOT REMEDIATED HERE:** `canonical_key('DIVZ SMA')`
raises today, and Andrew ruled DIVZ an Opal SMA. Whatever next routes DIVZ dollars through the
slice path meets that raise. It is a **named consequence of a sovereign ruling that has not
reached every producer** — not a defect in this project, not this author's to fix, and recorded so
the decomp inherits it rather than discovering it.

---

## 7. OPEN QUESTIONS — SURFACED, NOT FILLED

> `2.0.0_SA_COO` 73551 s.3: *"If the PRD cannot be written without inventing a design decision,
> that decision is a FINDING for me, not a gap for you to fill."* These are those findings.

### 7.1 ⛔ OPEN AT ANDREW — THE GRAIN. This one is load-bearing.

`@4dc2cd6087` s.4 records **Item B still open at Andrew: "model/sleeve name space vs SECURITY
grain."** That is the grain of the very thing being discovered, and **the domain of this PRD
cannot be closed without it.**

| reading | what "constituent-level name" spans | consequence |
|---|---|---|
| **SLEEVE / position-name space** | names of sleeves and positions as the partner labels them inside accounts | the population the DIVZ incident occurred in; all of the ruling's examples are this shape |
| **SECURITY grain** | security-level identifiers/names underneath | a different and larger population, different denominators, different match surface |

**EVIDENCE, NOT A RULING:** every example Andrew gave (`DIVZ SMA`, `Opal Tax SMA`, `Opal Muni
SMA`) is sleeve-shaped, and the incident was a sleeve. **That is suggestive and it is not his
answer, and Item B is recorded as open.** *This author is not resolving it.* The decomp inherits
the fork.

### 7.2 SCOPE — is the ETF population closed at four?

The ruling's *"really any opal ETF ... including PFOE PFDE IDVZ DIVZ"* leaves it open (§4.2).
**Issuer call:** does the mechanism cover exactly the 6 named tokens, or any Opal ETF including
ones not yet named? The two produce different completeness criteria and different denominators.

### 7.3 WHAT COUNTS AS THE INPUT POPULATION

The incident was in **cottonwood** constituent names. Whether this mechanism's purpose spans one
partner's book or every partner-supplied constituent surface is not stated in the ruling.
**Issuer call.** *(A separate read-only sweep of current cottonwood constituent names was
dispatched to `0.6.2_AE_PartnerETL~A` and explicitly does NOT ride this project.)*

---

## 8. EXPLICITLY OUT OF SCOPE OF THIS DOCUMENT

Refusals, not preferences: **no** matcher/algorithm design · **no** thresholds or fuzziness
parameters · **no** schema, enum or token mint · **no** registry structure · **no** TO · **no**
code · **no** file touched outside this one · **no** remediation of the `canonical_key('DIVZ SMA')`
hazard · **no** resolution of §7.1's grain fork.

**Not in scope of the PROJECT, per the register:** the immediate read-only cottonwood sweep
(dispatched separately); tomorrow's D8 fire — **nothing serves off this and it is not on the
critical path.**

---

## 9. WHAT "DONE" WOULD MEAN FOR THE MECHANISM (purpose-level only)

The mechanism is fit for purpose when a person can answer, for any partner-supplied constituent
name in the declared population:

1. **is this a candidate Opal SMA/ETF name?** — fuzzily, across the variant grammar, with
   common-noun tokens matched at boundary;
2. **if yes, is it already registered, or is it NEW?** — and NEW is a **surfaced candidate**, never
   an automatic served key;
3. **if the mechanism cannot answer, does it say so in a way a consumer can branch on** — UNKNOWN
   distinguishable from NO MATCH (§6).

**The measure of success is that the next unlabeled Opal SMA is SURFACED rather than silently
mis-bucketed.** It is not "zero unlabeled SMAs" — that is the partner's behaviour, which this
mechanism does not control and must not assume.

---

## 10. PROVENANCE

Every claim in §1 is quoted from the verbatim records; the paraphrase risk is deliberately
avoided because **the phrasing is the ruling.** §4.3(a)'s registry counts are read from the
D1_CATVIEWS `strategy_id` census (`4 of 6 SMA members carry a strategy_id`; `idvz`/`pfde` un-noded
as the ruled Q1 state). §6's exemplar is `3.0.0_SA_CVO`'s **exercised** result, not a source read.
**§7.1 is unresolved at the sovereign and is stated as such rather than closed by inference.**
