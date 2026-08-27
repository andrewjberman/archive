# `TL2DS-AC1` — RULE 24 FOUR-POSTULATE RECORD: the SMA L1 value-set

**Lane:** `0.4.0_DS_ClientPlatform~Z` · **TO:** `D1_CATVIEWS.TO-L2-DS` · **Certifier:** `3.0.0_SA_CVO~Z`
**Authoring act:** minting the L1 value-set `{ETF Strategies, ALT Strategies}` for the SMAs node.

## PROVENANCE OF THE UNBLOCK — stated first, because I resumed a BLOCKED-SOVEREIGN criterion

This criterion was `BLOCKED-SOVEREIGN` on *"do `idvz`/`pfde` belong inside ETF Strategies?"*
**Resumed on `1.0.0_SA_CTO~Z`'s relay (10294) of Andrew's *"yes approve all recs"*, which covered
their `/open-calls` CALL 1** (*"idvz/pfde inside ETF Strategies? REC (a) YES"*).

⚠ **This is a relayed blanket approval over another seat's card, not a direct answer to this lane** —
I put the same question to his terminal and it was answered at `1.0.0_SA_CTO~Z`'s. Recorded plainly
so the basis is auditable. Per `org/XXX.md` a relayed sovereign ruling is not suspect for being
unseen by the receiver, and the relayer carried the grounding (card, rec, verbatim).
⛔ **I did NOT resume on the tempting inference** — that a uniqueness-of-shape argument from his
~21:3xZ *"2 of 3 … not acceptable"* rule implied the answer. `2.0.0_SA_COO~Z` wrote *"DO NOT RESUME ON
THIS PARAGRAPH"* beside this criterion for exactly that reason, and I did not.

---

## THE DECLARED DOMAIN

> **The SMA-view member set** — every `CategoryMember` with `view_path == "SMA"`.
> **Measured denominator: 6** — `divz, idvz, muni, pfde, pfoe, tax`.

**Declaring the domain is load-bearing here:** the postulates are scored against *this* set and
nothing else. The domain is **closed** and registry-sourced (`SMA_MEMBERS`), not open-ended.

## (i) MECE OVER THE DECLARED DOMAIN — measured, uncovered-member hunt run

```
ETF Strategies : divz, idvz, pfde, pfoe          -> 4
ALT Strategies : muni, tax                        -> 2
COVERAGE    union == domain : True    UNCOVERED : []      <- the hunt, run and empty
EXCLUSIVITY overlap         : []      DISJOINT  : True
                              4 + 2 = 6 == |domain|
```

⛔ **THE HUNT WAS NOT VACUOUS AND ITS HISTORY MATTERS.** For ~90 minutes this record could not be
written, because under the rival reading (*"etf based smas"* merely describing `pfoe`/`divz` rather
than denoting `idvz`/`pfde`) coverage was **4 of 6 with `idvz` and `pfde` uncovered** — postulate (i)
FAILING. **The sovereign answer closed the branch; the arithmetic did not.**

## (ii) SAME GRAIN

```
L1  ETF Strategies / ALT Strategies   BUCKETS over the member set
L2  divz idvz pfde pfoe / muni tax    MEMBERS
```

**One grain per level.** ⚠ **The prior tree violated this**: its L1 values *were members*
(`{divz, pfoe, muni, tax}`) while `idvz`/`pfde` sat at the same conceptual level with **no node at
all** — members and non-nodes on one axis. **The restructure is what fixes the grain, not a
side-effect of it.**

⭐ **And this is what makes SMAs match its siblings** — Models `{Primary, Custom}` and Client
`{Opal Supervised, Opal Unsupervised}` are already buckets-over-members. All three become
**L0 → two L1 buckets → L2 members**, which is Andrew's *"the shapes should all be the same in
layout"* and his ~21:3xZ *"structured following the same pattern."*

## (iii) INTENT COHERENCE — one axis, one intent

> **The axis is: IS THIS SMA ETF-BASED?** Not *does it have a registered strategy*, not *is it
> served*, not *does it carry dollars*.

⛔⛔ **THE CRITICAL CLAUSE, AND IT IS WHY THIS RECORD EXISTS: THE NEW L1 AXIS AND THE SHIPPED
`strategy_id` FIELD ARE DIFFERENT CUTS OF THE SAME SET.**

```
strategy_id SET  : divz muni pfoe tax     |   ETF-based : divz idvz pfde pfoe
strategy_id None : idvz pfde              |   non-ETF   : muni tax
CROSSING CELL    : divz, pfoe             |   cuts coincide : FALSE
```

**The implication is ONE-DIRECTIONAL:** *no `strategy_id` ⇒ ETF-based* **HOLDS**; *ETF-based ⇒ no
`strategy_id`* **FAILS on `divz` and `pfoe`.**

>> ⛔ **DO NOT DERIVE THE BUCKET FROM `strategy_id`.** An implementer meets the TRUE direction first
   — *"where do the un-noded members go?"* returns a clean, total, correct answer — and concludes the
   level is derivable. **It is not.** The result would be a structurally plausible, silently wrong
   tree **that reads as reuse rather than invention**, which is the shape that passes review. <<

*(This is the derivation struck from `D1-h-r3` Claim B `@2ce1e1b8d5`. The struck cell's own oracle
encoded it as a runnable test and was struck with it.)*

## (iv) STATE COHERENCE — what one remedy does NOT move

**State axis: `{ETF Strategies, ALT Strategies}`. One remedy moves a value: a registry edit to the
bucket assignment.**

⛔ **THE PROBE THAT CATCHES A WRONG IMPLEMENTATION, stated as a future input rather than a current
state** (`3.0.0_SA_CVO~Z`'s form):

> **When `idvz` or `pfde` later gains a `strategy_id`, does its bucket change?**
> **IT MUST NOT.** ETF-ness is intrinsic to the product; strategy registration is a lifecycle fact
> about Opal's own records. **If the bucket moves, the implementation derived the level from the
> field** and postulate (iii) is violated.

**Values this remedy does NOT move:** `asset_category` (`strategy`), `served`, `display_name`,
`strategy_id` itself, and membership of the SMA view. **The restructure is a LEVEL change only.**

⭐ **DERIVED CONSEQUENCE — `un_noded_members` DISSOLVES.** `mdpf_category_registry.py:913` builds it
as the **exact complement** of the struck predicate. With every member now bucketed, that complement
is **empty by construction**. **This is derived from the value-set, not chosen** — and it is
independently what Andrew's ~21:3xZ rule requires: *"invisible otherwise"* forbids an
always-empty-by-construction emitted key.

---

## WORD-BOUNDARY TOKEN CENSUS

```
TOKEN                 TOTAL   BANDS                              CODE TREES
"ETF Strategies"      32/27,294  HEAD=6 SURFACED=1 CONFIG=5 DOC=20      1 file
"ALT Strategies"      26/27,294  HEAD=8 SURFACED=1 CONFIG=4 DOC=13      1 file
etf_strategies                                                          0
alt_strategies                                                          0
ETF_STRATEGIES / ALT_STRATEGIES                                         0
POSITIVE CONTROL  SMA_MEMBERS -> 6 files (the sweep discriminates)
1 UNREADABLE + 1,822 BINARY NOT searched in every figure above.
```

⚠ **THE DOC/HEAD MASS IS TONIGHT'S OWN DISCUSSION, NOT PRIOR ART.** A pre-change baseline taken at
~21:0xZ over `data/ portal/src/ infra/` read **0 / 0 / 0 / 0**. The corpus now records its own
deliberation — **a census run later will re-measure this conversation.** The **CODE** figure is the
one that answers the collision question.

**The single SURFACED hit is `portal/src/api/endpoints/aum.ts` — `0.4.0_DE_ClientPlatform~Z`'s
already-landed documentation of this very change.** ⛔ **NOT a collision: it is the remedy in
flight.** Counting it as prior art would be the corpus-records-its-own-tests error.

⛔ **A REAL HOMONYM, AND THE CENSUS MUST BE CASE-SENSITIVE BECAUSE OF IT:**

```
portal/src/App.tsx:272   alt="Opal Capital"
portal/src/App.tsx:282   alt="Opal Capital"
```

**Bare `ALT` collides with the HTML `alt` attribute in the portal tree.** The two-word form
**`ALT Strategies` is unambiguous**; a bare or case-folded `alt` sweep is not. **Any future census of
this value must be case-sensitive and use the two-word token** — and no snake/upper identifier form
should be minted as bare `ALT`.

---

## WHAT THIS RECORD DOES NOT AUTHORIZE

- **No implementation.** This is the authoring record; the emit change is `AC2`/`AC4`/`AC5`.
- ⛔ **`D1_CATVIEWS` remains NO-SHIP.** No re-pin, no `safe-apply`, no pin advance. The projection has
  never produced served output, so nothing client-facing carries either tree.
- **The `MdpfCategorySmaL1Node` rename rides scope-B** (one source file, 0 `.runtmp` copies) — named
  here so it is not cut as a second act against the same interface.
- **Certification is `3.0.0_SA_CVO~Z`'s.** This record is the proposal Rule 24 requires, not its
  acceptance.
