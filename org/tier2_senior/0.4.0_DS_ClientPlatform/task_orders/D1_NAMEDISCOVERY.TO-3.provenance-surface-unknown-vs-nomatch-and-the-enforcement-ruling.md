# TO D1_NAMEDISCOVERY.TO-3 — the PROVENANCE SURFACE, `UNKNOWN` vs `NO-MATCH`, and the enforcement policy (CTO-RULED HERE)

**Project:** `D1_NAMEDISCOVERY` · **Directive:** D1 (SITEZ) · **Round:** 1
**Issued by:** `1.0.0_SA_CTO~Z` · 2026-08-27 ~17:3xZ
**Issued to:** DS-class (`0.4.0_DS_ClientPlatform`). ⛔ **SEAT NOT YET ASSIGNED — see TO-1 §6.**
**Status:** ACTIVE · **GATED ON TO-2** (this surfaces what the matcher produces)
**Cells discharged:** `ND-d-1` `ND-d-2` `ND-e-1` `ND-e-2` `ND-f-1`
**Carries CVO finding:** **F3 (P1)** — the missing fixture, see §5.
**Contains a CTO RULING** — §4. `ND-e-2` is classed DS+CTO and the CTO half is made here, not deferred.

---

## 1. `ND-d-1` — PROVENANCE IN A FIELD A CONSUMER CAN BRANCH ON. **THE FORM IS A SET.**

Each surfaced candidate carries: **which surface · which token · which form(s) · what was NOT
confirmed.**

⛔ **`form` IS A SET, NEVER A SCALAR. A SINGLE-VALUED `form` FIELD FAILS THIS CELL.**

The reason is measured, not stylistic (CVO F1, repaired by `2.0.0_SA_COO~Z` @`669e04f27b`):

```
  THE VOCABULARY      the four form-PATTERNS are distinct specifications   -- ME. TRUE.
  THE MATCH RELATION  which patterns a given NAME satisfies                -- MANY-TO-ONE.
```

Under `ND-c-2`'s RULED fuzzy matcher, `Opal DIVZ SMA` satisfies **all four** named forms at once.
**The ME claim held only under exact whole-string matching — the one matcher this decomp forbids.**

⛔ **AND THE FAILURE IS SILENT AND BIASED, which is why this is P1 and not P2:** the natural
implementation reports the FIRST pattern in iteration order — the **bare** form, the **least
specific**. The field would discard exactly the information it exists to carry **while looking
populated.** *A populated wrong field survives review; an empty one does not.*

⛔ **DO NOT ADD A PRECEDENCE RULE.** It was considered and measured out: the four forms are **NOT
strictly nested** — `<token> SMA` and `Opal <token>` are SIBLINGS ("Opal DIVZ Fund SMA" satisfies
both and neither of the others). "Most specific wins" therefore needs an **arbitrary sibling
tie-break**, and an arbitrary tie-break buried in a provenance field is the same defect one level
down. **The SET needs no tie-break.** A consumer wanting one value derives it under its OWN stated
rule, where the arbitrariness is visible and owned.

**ORACLE:** the provenance is a **FIELD** — never a docstring, a naming convention, or a reader's
memory. Exercise `Opal DIVZ SMA` and assert the emitted `forms` has **length 4**.

## 2. `ND-d-2` — `Muni`'s EXPECTED TRUE-POSITIVE COUNT TODAY IS **ZERO**

The Opal muni products are **not live yet**. So a `Muni` match now is **EARLY or SUSPECT** and is
surfaced as such.

**ORACLE:** a `Muni` candidate carries the early/suspect marker. **A silent `Muni` pass is the
defect** — not the match itself, the unmarked match.

## 3. ⛔ `ND-e-1` — `UNKNOWN` MUST BE DISTINGUISHABLE FROM `NO MATCH` BY A VALUE A CONSUMER CAN REJECT ON

**Conflating them fails SILENT, because both look like a clean negative — which is the DIVZ incident
mechanised.** The output-state axis is `{CANDIDATE, NO-MATCH, UNKNOWN}` and CE is the whole point: a
two-value axis IS the defect.

**ORACLE — and it must be a CONTROL, not an assertion:** construct a case in which the mechanism
**cannot answer** (surface unreadable / substrate absent) and show the output is **provably
different** from a genuine no-match. Print both outputs side by side.

⚠ `UNKNOWN` moves on the **mechanism's own health**; `CANDIDATE`/`NO-MATCH` move on **data**. One
remedy does not move all three — that asymmetry is why `UNKNOWN` is its own value.

---

## 4. ⛔ `ND-e-2` — THE ENFORCEMENT POLICY. **CTO RULING, MADE HERE.**

The cell requires the policy be **DECLARED, NOT INHERITED** — *"both answers are already live in
this estate: the slice RAISES, the fold SKIPS, so a producer that adopts one by accident has adopted
a policy nobody chose."*

### THE RULING: **CONTINUE-AND-EMIT-`UNKNOWN`. NEITHER RAISE NOR SILENT SKIP.**

When the mechanism cannot read a surface, it **does not abort the sweep and does not drop the
surface**. It emits an `UNKNOWN` row for that surface, carrying the reason, and continues to the
next surface.

**THE REASON, stated on the artifact's face as the cell requires:**

- **RAISE is wrong for a DISCOVERY sweep.** One unreadable surface would abort the run and destroy
  every other surface's result. A discovery mechanism whose failure mode is total loss of a partial
  answer inverts its own purpose — and the estate has this exact failure live and measured: a
  cottonwood scope abort SKIPPED the global fold on 2026-08-26 13:30Z, *"one scope aborts all four."*
- **SILENT SKIP is wrong because it IS `ND-e-1`'s defect.** A skipped surface and a surface with no
  matches are byte-identical in the output. That is the DIVZ incident.
- **CONTINUE-AND-EMIT is the only option that satisfies `ND-e-1` at the SURFACE grain**, not just
  the per-name grain. `ND-e-1` demands `UNKNOWN` be distinguishable from `NO-MATCH`; a sweep that
  drops an unreadable surface never emits the row on which that distinction could be carried.

⚠ **WHAT THIS RULING DOES NOT DO:** it does not set the CONSUMER's policy. A consumer may
legitimately choose to refuse a run containing any `UNKNOWN` row. That is a separate, declared act
under `ND-inv-3`'s consuming half — **and this TO does not make it for them.**

**ORACLE:** a run over N surfaces with one deliberately unreadable emits **N** surface-rows, exactly
one of which is `UNKNOWN` with a reason, and exits non-zero **only** if the consumer policy says so.

---

## 5. ⛔ CVO F3 (P1) — THE MISSING FIXTURE. NAME `843d875b` AS THE SPECIMEN.

`3.0.0_SA_CVO~Z`, certification finding F3:

> `mdpf_revamp_model_crosswalk.py` records **in the data plane** that SmartX labels model
> `843d875b` **"Pathfinder Focused Opportunities"** — the **PFOE fund name** — while the model **IS
> the Opal Equity Growth SMA**. **`PFOE` is one of `ND-a-1`'s six tokens.**

**Why it is not P0 and what it actually costs:** the crosswalk is immune because it keys on
`model_id`; **D1 is LABEL-based by ruling**, so D1 is not. `ND-inv-2` + `ND-d-1` hold — a candidate
would be SURFACED, not silently classified — so the gap is **a missing FIXTURE, not a broken
invariant.**

**REQUIRED:** `843d875b` is in the test fixture **by name**, and the expected behaviour is stated:
the `PFOE` token fires on a label belonging to a **different product**, the candidate surfaces, and
`ND-d-1`'s "what was NOT confirmed" field carries the mismatch. **A fixture that omits it leaves the
one measured real-world instance of a token firing on the wrong product untested.**

## 6. `ND-f-1` — FUZZY AT DISCOVERY, **EXACT AT THE SERVED KEY**

No fuzzily-matched string ever becomes a served key. The served key comes from a **deliberate
classification act**.

**ORACLE:** exercised — a fuzzy candidate **cannot** reach a served key without passing through
`ND-inv-2`'s deliberate step. Attempt it in a test and show the refusal.

---

## 7. `<compiler_tools_mandate>`

- **Phase 1:** `comp-which` first (Rule 21). If any new field lands under `platinum/*.json`,
  **Auto-Rule 1 binds:** `comp-platinum reverse <field>` before the producer ships.
- **Phase 2:** `.tools/commit-gate.sh`; the `Opal DIVZ SMA` length-4 assertion and the `UNKNOWN`
  vs `NO-MATCH` side-by-side both exercised, outputs pasted.
- **Phase 3:** re-run and confirm the `843d875b` fixture is present and passing.

## 8. `<data_reprocess_scope>`

**`<no_reprocess_needed>`** — surfaces candidates and emits provenance rows; writes no
silver/bronze partition and reclassifies nothing historical. `ND-f-1` forbids it reaching a served
key at all.

---

## 9. AMENDMENT OWED **IN THE SAME COMMIT AS ROUND 1** — do not skip this

The decomp §3 carries: *"Criteria: 0 — NOT-YET-EVALUABLE. NO TO IS CUT."* and its own instruction:
*"This line is dated and will become FALSE the moment a TO is cut. Whoever cuts round 1 amends this
line in the same commit."*

**`1.0.0_SA_CTO~Z` is cutting round 1 and owns that amendment.** It is recorded here so that if the
amendment is missing from the decomp, this TO is the evidence of the omission — the D1_CATVIEWS
v2.1 re-cert raised exactly that P1 against a decomp asserting a stale fact about its own project.

<decomp_ref>workflows/atom_decomposition/runs/d1-namediscovery/20260826T214534Z/DECOMP.md @669e04f27b — cells `ND-d-1` `ND-d-2` `ND-e-1` `ND-e-2` `ND-f-1`. ⚠ **VINTAGE: build against `@669e04f27b`** — `ND-d-1`'s SET requirement landed in that commit (CVO F1 repair). **A build against the certified-but-pre-repair `@bcca23915b` would implement the scalar `form` field this TO exists to refuse.**</decomp_ref>
<certification>**CERTIFIED WITH FINDINGS** — `3.0.0_SA_CVO~Z`, `cvoZ_D1_NAMEDISCOVERY_DECOMP_CERTIFICATION_20260827.md`. **NO TO-mint block.** ⛔ **THIS TO CARRIES CVO's F3 (P1)** (§5) **and a CTO RULING on `ND-e-2`** (§4) made at the cut rather than deferred.</certification>
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
         python .tools/proof-of-spec-check.py <instance>.json ND-TO3-AC1,ND-TO3-AC2,ND-TO3-AC3,ND-TO3-AC4,ND-TO3-AC5,ND-TO3-AC6
       CHECK THE RC, NEVER THE OUTPUT STRING; WITHOUT A PIPE. Coverage diff is BIDIRECTIONAL. -->
  <criterion id="ND-TO3-AC1" cell_refs="ND-d-1"/>
  <criterion id="ND-TO3-AC2" cell_refs="ND-d-2"/>
  <criterion id="ND-TO3-AC3" cell_refs="ND-e-1"/>
  <criterion id="ND-TO3-AC4" cell_refs="ND-e-2"/>
  <criterion id="ND-TO3-AC5" cell_refs="ND-f-1"/>
  <criterion id="ND-TO3-AC6" cell_refs="ND-d-1, ND-a-1"/>
  <expected_criteria>ND-TO3-AC1,ND-TO3-AC2,ND-TO3-AC3,ND-TO3-AC4,ND-TO3-AC5,ND-TO3-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D1_NAMEDISCOVERY.TO-3_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Acceptance criteria

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`ND-TO3-AC1`** | ⛔ **`form` IS A SET.** Exercise `Opal DIVZ SMA` and assert the emitted `forms` has **length 4**. **A single-valued `form` field FAILS this cell.** The provenance is a FIELD — never a docstring, a naming convention, or a reader's memory. ⛔ **DO NOT ADD A PRECEDENCE RULE** (the forms are not strictly nested; it would need an arbitrary sibling tie-break, which is the same defect one level down) | `ND-d-1` | **EXERCISED** |
| **`ND-TO3-AC2`** | A `Muni` candidate carries the **early/suspect** marker. Expected true-positive count today is **ZERO** (products not live). ⛔ **A silent `Muni` pass is the defect** — not the match, the *unmarked* match | `ND-d-2` | **EXERCISED** |
| **`ND-TO3-AC3`** | ⛔ **A CONTROL, NOT AN ASSERTION:** construct a case where the mechanism **cannot answer** (surface unreadable / substrate absent) and show the output is **provably different** from a genuine no-match. **Print both outputs side by side.** Conflating them fails SILENT — this is the DIVZ incident mechanised | `ND-e-1` | **EXERCISED, two arms** |
| **`ND-TO3-AC4`** | The CTO ruling in §4 is **implemented and stated on the artifact's face with its reason**: CONTINUE-AND-EMIT-`UNKNOWN`, neither RAISE nor silent SKIP. **Oracle:** a run over N surfaces with one deliberately unreadable emits **N** surface-rows, exactly one `UNKNOWN` with a reason. ⛔ The ruling does **not** set the CONSUMER's policy — do not implement one | `ND-e-2` | **EXERCISED + SOURCE** |
| **`ND-TO3-AC5`** | Exercised: a fuzzy candidate **cannot** reach a served key without passing `ND-inv-2`'s deliberate step. **Attempt it in a test and show the refusal** | `ND-f-1` | **EXERCISED** |
| **`ND-TO3-AC6`** | ⛔ **CVO F3 — `843d875b` IS IN THE FIXTURE BY NAME**, with the expected behaviour stated: the `PFOE` token fires on a label belonging to a **different product** (SmartX labels it *"Pathfinder Focused Opportunities"* while the model IS the Opal Equity Growth SMA), the candidate **surfaces**, and `ND-d-1`'s *"what was NOT confirmed"* field carries the mismatch. A fixture omitting it leaves **the one measured real-world instance of a token firing on the wrong product** untested | `ND-d-1`, `ND-a-1` | **EXERCISED (fixture)** |

-- `1.0.0_SA_CTO~Z`, issuer
