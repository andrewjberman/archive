# D1_NAMEDISCOVERY — PURPOSE-LEVEL PRD v2

**Rule 27 step 2.** WHAT and WHY only. No design, no matcher, no thresholds, no schema mint, no TO.
**Author:** `0.4.0_DS_ClientPlatform~R` · **Allocated by:** `2.0.0_SA_COO` 73551 · **Date:** 2026-08-26
**Project:** `org/projects/D1_NAMEDISCOVERY.json` @`e9990032fe` (registered by `0.0.0_AB_MSTR`, LD-0460)
**Consumes (do not re-derive):** `@195cfbdbe9` · `@4b6503cdbd` · `3.0.0_SA_CVO` 73238 s.2

> ## ⛔ v2 AMENDMENT — v1's §7.1 WAS WRONG, AND THE CAUSE IS WORTH MORE THAN THE FIX
>
> **v1 reported the GRAIN as an open sovereign question. IT WAS ALREADY CLOSED.** Andrew ~18:06Z,
> **VERBATIM: "Constituent-level means the model/sleeve name space, not security grain."**
> Corrected per `1.0.0_SA_CTO` 73677. §7.1 and §7.2 now record CLOSED rulings; §7.3 carries an
> architecture default.
>
> **HOW THE ERROR HAPPENED — A VINTAGE READ MISTAKEN FOR THE RECORD.** The spine handed to this
> author pinned `@4dc2cd6087`. That commit's version of the record says, at item 4, *"Item B
> (model/sleeve name space vs SECURITY grain) remains OPEN at Andrew."* **It was superseded
> `@4b6503cdbd` — 56 SECONDS LATER — which closed Item B with the verbatim above.** This author read
> exactly the ref it was given, reported it faithfully, and was wrong about the world.
>
> ⛔ **THE LESSON, STATED SO THE NEXT READER INHERITS IT: A COMMIT-PINNED READ ANSWERS ABOUT A
> VINTAGE, NEVER ABOUT THE CURRENT STATE OF A RECORD.** `git show <ref>:<path>` is the right
> instrument for *"what did this say when it was cited"* and the wrong one for *"what does this say."*
> A record cited by hash inherits that hash's staleness **silently**, and the citation looks more
> rigorous than a bare path — which is what makes it persuasive. **Read the pinned vintage AND
> `git log` the path.** Cost: one `git log`. Does not apply when the vintage IS the question.

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

### 4.0 THE GRAIN — RULED, AND IT BOUNDS EVERYTHING BELOW

> **"Constituent-level means the model/sleeve name space, not security grain."** — Andrew ~18:06Z,
> `@4b6503cdbd` (see §7.1)

**The declared domain is the MODEL/SLEEVE NAME SPACE. Security grain is explicitly OUT.** Every
denominator in this section is counted over that space and no other.

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

## 7. THE THREE SCOPE QUESTIONS — TWO CLOSED BY SOVEREIGN WORD, ONE ON AN ARCHITECTURE DEFAULT

> **v1 carried all three as OPEN. Two were already answered.** Corrected per `1.0.0_SA_CTO` 73677.
> **CITE THESE, DO NOT RE-ASK — re-asking a settled question re-opens settled law.**

### 7.1 ✅ THE GRAIN — CLOSED BY SOVEREIGN WORD ~18:06Z

> **"Constituent-level means the model/sleeve name space, not security grain."**
> — Andrew, ~18:06Z, verbatim, recorded `@4b6503cdbd` item 4

**OPERATIVE: the declared domain is the MODEL/SLEEVE NAME SPACE. SECURITY GRAIN IS EXPLICITLY OUT
OF DOMAIN.** The decomp cuts against that grain.

*Corroborating, now that the ruling is known: every example Andrew gave (`DIVZ SMA`, `Opal Tax
SMA`, `Opal Muni SMA`) is sleeve-shaped, and the incident was a sleeve. That was **evidence**, and
v1 correctly declined to treat it as the answer — the answer existed and was elsewhere.*

### 7.2 ✅ THE ETF POPULATION — CLOSED BY HIS OWN WORDS. IT IS OPEN.

> **"same for really any opal ETF, and associated conjunctions, the etfs including PFOE PFDE IDVZ
> DIVZ."** — Andrew, ~17:56Z, `@195cfbdbe9`

**"REALLY ANY OPAL ETF" ANSWERS THE QUESTION.** *"Including"* is membership-naming, not closure.

**OPERATIVE: the ETF population is OPEN — any Opal ETF. The four tickers are NAMED SEED MEMBERS,
not the domain.** **Completeness criteria are written against the OPEN population**, which is the
mechanism's whole point: fuzzy at discovery, exact at the served key. §4.2's honest-denominator
note stands and is now the ruled position rather than a caveat.

### 7.3 ⚠ THE INPUT POPULATION — NO RECORDED WORD. ARCHITECTURE DEFAULT, OVERRIDE WINDOW OPEN.

No verbatim closes the input span. **`1.0.0_SA_CTO`'s architecture default (73677), effective
unless Andrew says otherwise:**

- **DECLARED DOMAIN = the CLASS of partner-supplied constituent-name surfaces** — any partner, any
  custodian feed delivering model/sleeve names.
- **V1 COVERAGE = cottonwood's surfaces** — the one book with the measured failure.
- **A second partner is therefore a MEMBERSHIP ADD, never a schema change.**

⛔ **THE DOMAIN IS NAMED NOW PRECISELY SO THE v1 DENOMINATOR IS HONEST** — *"cottonwood's N
surfaces of the declared class"* rather than silently universal (Rule 24(i): MECE is over a
**declared** domain). Andrew's word supersedes same-turn if he widens or narrows.

*(The separate read-only cottonwood sweep dispatched to `0.6.2_AE_PartnerETL~A` does NOT ride this
project.)*

---

## 8. EXPLICITLY OUT OF SCOPE OF THIS DOCUMENT

Refusals, not preferences: **no** matcher/algorithm design · **no** thresholds or fuzziness
parameters · **no** schema, enum or token mint · **no** registry structure · **no** TO · **no**
code · **no** file touched outside this one · **no** remediation of the `canonical_key('DIVZ SMA')`
hazard.

**Out of DOMAIN, by sovereign word (§7.1): the SECURITY grain.** Not a deferral — ruled out.

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

**§7.1 and §7.2 are CLOSED BY SOVEREIGN WORD and are cited, not inferred.** §7.3 carries a named
architecture default from `1.0.0_SA_CTO` with the sovereign override window open, and is labelled
as a default rather than a ruling.

### ⛔ ONE INSTRUMENT NEAR-MISS FROM THE v2 CORRECTION, RECORDED BECAUSE IT NEARLY WENT THE OTHER WAY

Checking whether the claimed verbatim existed, this author ran a content census for the phrase
`not security grain` across the estate. **It returned a clean, well-formed, denominator-printed
ZERO over 26,902 files — for a string that IS PRESENT in the file.** The record line-wraps
mid-phrase (`not` ends a line, `security grain` begins the next), and a line-based matcher cannot
see across the break.

>> **A MULTI-WORD PATTERN SPANNING A LINE BREAK IS INVISIBLE TO A LINE-BASED SEARCH, AND THE ZERO
>> IT RETURNS IS INDISTINGUISHABLE FROM A GENUINE ABSENCE.** Had that zero been led with instead of
>> the file read, it would have "confirmed" that a Tier-1 seat fabricated a sovereign quotation —
>> a false accusation carrying a printed denominator. **The denominator was honest and the answer
>> was wrong.** Read the artifact; a phrase census is a NOTICING instrument, never a deciding one.

