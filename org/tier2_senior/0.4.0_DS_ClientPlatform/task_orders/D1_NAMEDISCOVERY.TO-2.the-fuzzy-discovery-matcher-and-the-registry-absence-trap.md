# TO D1_NAMEDISCOVERY.TO-2 — the FUZZY DISCOVERY MATCHER, and the registry-absence trap that inverts a ruling

**Project:** `D1_NAMEDISCOVERY` · **Directive:** D1 (SITEZ) · **Round:** 1
**Issued by:** `1.0.0_SA_CTO~Z` · 2026-08-27 ~17:3xZ
**Issued to:** DS-class (`0.4.0_DS_ClientPlatform`). ⛔ **SEAT NOT YET ASSIGNED — see TO-1 §6.**
**Status:** ACTIVE · **GATED ON TO-1** (the matcher reads TO-1's declared artifacts; it must not
carry its own copy of the token set — that duplication is `ND-a-1`'s named defect)
**Cells discharged:** `ND-c-1` `ND-c-2` `ND-c-3`
**Carries CVO finding:** **F2 (P1)** — see §2. This is the finding most likely to be satisfied on
paper and violated in the build (`2.0.0_SA_COO~Z`'s assessment, and I agree).

---

## 1. WHAT TO BUILD

### 1.1 `ND-c-1` — WORD-BOUNDARY MATCHING, and it is a CORRECTNESS requirement

`Tax` and `Muni` are **native estate vocabulary**. A substring sweep returns the estate.

⛔ **THIS IS NOT A TUNING CHOICE.** 2 of the 6 tokens are common nouns; substring matching on them
does not produce a noisy answer, it produces a wrong one.

**ORACLE — a CONTROL WITH BOTH ARMS, and the failing arm is the load-bearing one:**
```
the SAME corpus, two matchers:
  substring matcher      -> MUST FAIL (returns estate vocabulary as candidates)
  word-boundary matcher  -> MUST PASS
```
A control that only exercises the passing arm proves the matcher runs, not that it discriminates.
**Print the count each arm returns.** *(Banked estate lesson: a control that cannot fail is not a
control.)*

### 1.2 `ND-c-2` — THE MATCHER IS FUZZY AT DISCOVERY, BY RULING

Andrew: *"on the lookout on a fuzzy basis."* **Recall over precision at this stage.** It catches
candidates it cannot confirm — that is the design, not a defect.

**ORACLE:** a known variant that is **NOT** among the 24 named strings is still caught. If only the
24 named strings match, the matcher is an equality test wearing the word "fuzzy" — **the fuzziness
is decoration and the cell fails.**

⚠ **AND THIS CELL IS WHY `ND-d-1` REPORTS A SET** (TO-3): under a fuzzy matcher one name satisfies
several named forms at once. Do not "resolve" that here.

---

## 2. ⛔ `ND-c-3` — A REGISTRY MISS IS NOT "NOT OPAL", AND CVO's F2 WIDENS THE TRAP

### 2.1 The cell

`idvz` and `pfde` are **un-noded BY RULING — explicitly "not missing data."** A design that resolves
a match against the `strategy_id` registry and reads absence as a negative **INVERTS THE RULING FOR
2 OF THE 6 TOKENS.**

**ORACLE:** exercised on `idvz` and `pfde` specifically — a match **SURFACES DESPITE** having no
registry entry. Both tokens named in the fixture, not one.

### 2.2 ⛔ CVO F2 (P1) — THE CELL NAMES **ONE** REGISTRY; THE ESTATE HOLDS AT LEAST **THREE**
### RESOLUTION SURFACES OVER THIS NAME SPACE, WITH **OPPOSITE** ABSENCE POLICIES

`3.0.0_SA_CVO~Z`, certification finding F2:

```
  data/mdpf/scripts/gold/mdpf_revamp_model_crosswalk.py   RAISES on an unrecognized name
  portal/src/lib/modelPortfolioColors.ts:189              a LABEL-KEYED ALIAS MAP (absence = no entry)
  the strategy_id registry                                the one surface ND-c-3 actually names
```

>> **A DESIGN THAT RESOLVES AGAINST EITHER OF THE FIRST TWO AND READS ABSENCE AS A NEGATIVE
   VIOLATES THIS CELL'S PRINCIPLE WHILE PASSING ITS LETTER.** The letter says "the strategy_id
   registry"; the principle says "a miss is not a negative." Satisfying the letter against a
   different surface is the failure mode. <<

**REQUIRED, and this is the discharge:**
1. **NAME THE RESOLUTION SURFACE YOU ACTUALLY USE**, with `file:line @ <commit-ish>`. A citation
   without a vintage is not a citation (Rule 22).
2. **STATE ITS ABSENCE POLICY EXPLICITLY** — raises / returns null / returns a default — and state
   that your code does **not** convert that absence into a `NO-MATCH`.
3. **If you resolve against more than one surface, state the precedence AND what each one's absence
   means.** Two surfaces with opposite absence policies and no declared precedence is the defect.

**ORACLE:** the `idvz`/`pfde` fixture is run against **every** resolution surface the build touches,
not only the one the cell names.

---

## 3. INVARIANTS — BINDING

`ND-inv-1` fuzzy at discovery / exact at the served key · `ND-inv-2` **discovery surfaces, it never
silently classifies** · `ND-inv-3` a value carries its claim, **and the consumer refuses an unmarked
one**.

## 4. DECLARED OUT

`ND-g-1` security grain · `ND-g-2` the `canonical_key('DIVZ SMA')` raise (forward hazard, not owned
here) · `ND-g-3` the classification act · `ND-g-4` partners beyond cottonwood.

---

## 5. `<compiler_tools_mandate>`

- **Phase 1:** `comp-blast` on whatever resolution function you intend to call — **Auto-Rule 6
  (multi-call-site predicate coverage) binds:** surface every call site of the resolver before you
  write against it, and either cover them all or list each exclusion with its reason. `comp-which`
  first per Rule 21.
- **Phase 2:** `.tools/commit-gate.sh`; both control arms exercised with counts printed.
- **Phase 3:** re-run `comp-blast` to confirm the blast radius did not widen.

## 6. `<data_reprocess_scope>`

**`<no_reprocess_needed>`** — a discovery matcher that writes no silver/bronze partition and
reclassifies no historical data. It surfaces candidates; it serves nothing (`ND-inv-1`).

<decomp_ref>workflows/atom_decomposition/runs/d1-namediscovery/20260826T214534Z/DECOMP.md @669e04f27b — cells `ND-c-1` `ND-c-2` `ND-c-3`. ⚠ **VINTAGE:** CVO certified at `@bcca23915b`; the F1/F4 repairs landed after at `@669e04f27b`. **Build against `@669e04f27b`.**</decomp_ref>
<certification>**CERTIFIED WITH FINDINGS** — `3.0.0_SA_CVO~Z`, `cvoZ_D1_NAMEDISCOVERY_DECOMP_CERTIFICATION_20260827.md`. **NO TO-mint block.** ⛔ **THIS TO CARRIES CVO's F2 (P1)** — the finding `2.0.0_SA_COO~Z` independently assessed as *"the one most likely to be satisfied on paper and violated in the build"*, and I agree. It is §2.2, not a footnote.</certification>
<issued_to>0.4.0_DS_ClientPlatform~Q</issued_to>
> ⛔ **SEATED 2026-08-27 ~18:0xZ by the COO office.** The lane was assigned by MSTR (msg 9354)
> and lived ONLY in that message until now: `to-check.py` rendered this TO **`(unassigned)`**
> or resolved a serial out of prose, while the seat was LIVE AND BUILDING against it.
> ⚠ **A SEATING THAT EXISTS ONLY IN A MESSAGE IS NOT A SEATING** — the record is what every
> instrument reads, and an unresolvable assignee reads as unowned work no matter who is at the
> keyboard. Same class as this round's other three (a re-scoped serial, a class with no
> instance, 11 stale disarm_owner rows).

<executor_class>DS-class</executor_class>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued>2026-08-27T17:3xZ</issued>
<status>COMPLETE — ROUND 1 ACCEPTED + CERTIFIED. Built by `0.4.0_DS_ClientPlatform~Q` 2026-08-27 ~17:37-18:10Z; `1.0.0_SA_CTO~Z` ACCEPTED round 1 **15/15** at 18:29Z; `3.0.0_SA_CVO~Z` CERTIFIED at 18:29Z and re-confirmed the TO-3 evidence counts at 20:45Z. Build @`fd15cd5cf3`, proofs @`b0ea4d8ff7`, evidence retraction @`20dda51bd3` — **all three verified ON ORIGIN by `2.0.0_SA_COO~Z` 2026-08-28 ~01:1xZ** (`merge-base --is-ancestor` vs `origin/SITEZ`, with a positive AND a negative control both passing). ⛔ **CLOSED BY THE ISSUING OFFICE BECAUSE THIS FACE READING `ACTIVE` MANUFACTURED A FALSE RE-DISPATCH:** it caused `2.0.0_SA_COO~Z` to rank a re-seat of world-done work at 01:0xZ, caught only because the re-seated lane refused to execute it and measured the world instead. **A TO face and the world are two carriers of one obligation; the ranking followed the one that said ACTIVE.** The decomp names no round 2. Surfaced by `0.4.0_DS_ClientPlatform~Q` (msg 11408).</status>

<proof_of_spec>
  <!-- ISSUANCE half (1.0.0_SA_CTO~Z). POSITIONAL:
         python .tools/proof-of-spec-check.py <instance>.json ND-TO2-AC1,ND-TO2-AC2,ND-TO2-AC3,ND-TO2-AC4
       CHECK THE RC, NEVER THE OUTPUT STRING; WITHOUT A PIPE. Coverage diff is BIDIRECTIONAL. -->
  <criterion id="ND-TO2-AC1" cell_refs="ND-c-1"/>
  <criterion id="ND-TO2-AC2" cell_refs="ND-c-2"/>
  <criterion id="ND-TO2-AC3" cell_refs="ND-c-3"/>
  <criterion id="ND-TO2-AC4" cell_refs="ND-c-3"/>
  <expected_criteria>ND-TO2-AC1,ND-TO2-AC2,ND-TO2-AC3,ND-TO2-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D1_NAMEDISCOVERY.TO-2_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Acceptance criteria

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`ND-TO2-AC1`** | ⛔ **A CONTROL WITH BOTH ARMS ON THE SAME CORPUS.** substring matcher **MUST FAIL** (returns estate vocabulary); word-boundary matcher **MUST PASS**. **Print the count each arm returns.** A control exercising only the passing arm proves the matcher runs, not that it discriminates — *a control that cannot fail is not a control* | `ND-c-1` | **EXERCISED, two arms** |
| **`ND-TO2-AC2`** | A known variant **NOT** among the 24 named strings is still caught. If only the 24 match, the matcher is an equality test wearing the word "fuzzy" and **the cell FAILS** | `ND-c-2` | **EXERCISED** |
| **`ND-TO2-AC3`** | Exercised on **BOTH** `idvz` **and** `pfde`: a match **SURFACES DESPITE** having no registry entry. Both tokens in the fixture, not one — they are un-noded BY RULING, *"not missing data"* | `ND-c-3` | **EXERCISED** |
| **`ND-TO2-AC4`** | ⛔ **CVO F2 — NAME THE RESOLUTION SURFACE YOU ACTUALLY USE**, with `file:line @ <commit-ish>`, **state its absence policy explicitly** (raises / null / default), and state that your code does **NOT** convert that absence into a `NO-MATCH`. If you resolve against more than one surface, **declare the precedence AND what each absence means.** ⛔ Two surfaces with opposite absence policies and no declared precedence IS the defect. Run the `idvz`/`pfde` fixture against **every** surface the build touches, not only the one `ND-c-3` names | `ND-c-3` | **SOURCE + EXERCISED** |

-- `1.0.0_SA_CTO~Z`, issuer
