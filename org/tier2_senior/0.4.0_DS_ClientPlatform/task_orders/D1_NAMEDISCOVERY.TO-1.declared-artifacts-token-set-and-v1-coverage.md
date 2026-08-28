# TO D1_NAMEDISCOVERY.TO-1 — the DECLARED ARTIFACTS: token set, variant grammar, and the v1 coverage set

**Project:** `D1_NAMEDISCOVERY` · **Directive:** D1 (SITEZ) · **Round:** 1
**Issued by:** `1.0.0_SA_CTO~Z` · 2026-08-27 ~17:3xZ
**Issued to:** DS-class (`0.4.0_DS_ClientPlatform`). ⛔ **SEAT NOT YET ASSIGNED — see SEATING below.**
**Status:** ACTIVE
**Cells discharged:** `ND-a-1` `ND-a-2` `ND-a-3` `ND-b-1` `ND-b-2`
**Decomp:** `workflows/atom_decomposition/runs/d1-namediscovery/20260826T214534Z/DECOMP.md`
**Certification:** `org/tier1_exec/3.0.0_SA_CVO/deliverables/cvoZ_D1_NAMEDISCOVERY_DECOMP_CERTIFICATION_20260827.md`
— **CERTIFIED WITH FINDINGS, no TO-mint block** (`3.0.0_SA_CVO~Z`, msg 9321)

---

## 0. THE THREE THINGS YOU MAY NOT RE-OPEN

Closed by sovereign word `@862b6bf35c` ("recs approved", 2026-08-26 ~21:07Z). **A cell that
re-asks one of these re-opens settled law.**

- **GRAIN** — *"Constituent-level means the model/sleeve name space, not security grain"*
  (`@4b6503cdbd`). **Security grain is OUT OF DOMAIN.** Every denominator you print is counted over
  the model/sleeve name space and no other.
- **ETF POPULATION IS OPEN** — *"really any opal ETF ... the etfs INCLUDING PFOE PFDE IDVZ DIVZ."*
  **"Including" is not "namely."** The four tickers are named SEED MEMBERS, not closure.
- **INPUT SPAN** — the declared domain is the **CLASS** of partner-supplied constituent-name
  surfaces. **v1 coverage = cottonwood's surfaces.** A second partner is a MEMBERSHIP ADD.

---

## 1. WHAT TO BUILD

### 1.1 `ND-a-1` — the token set and variant grammar, AS DATA

Six named tokens × four named forms, plus the unenumerated fifth form class:

```
tokens (6):  DIVZ · PFOE · PFDE · IDVZ · Tax · Muni
forms  (4):  bare · "<token> SMA" · "Opal <token>" · "Opal <token> SMA"
forms  (5th): "associated conjunctions" -- AN UNENUMERATED, OPEN CLASS. It is a DECLARED VALUE.
```

⛔ **THE SET IS A DECLARED ARTIFACT A NON-AUTHOR CAN READ AND EXTEND — NEVER A LITERAL EMBEDDED IN
A MATCHER.** If the only place these strings exist is inside a regex, this cell is not discharged.

**ORACLE:** a reader who has never seen the code can open one file, read all six tokens and all
five form classes, and add a seventh token without touching matcher logic.

### 1.2 `ND-a-2` — THE DENOMINATOR PRINTS ITS OWN OPENNESS

⛔ **A BARE `24` ANYWHERE IS THE DEFECT.** The population is open by ruling, so every printed
denominator says so on its face:

```
GOOD:  "7 candidates over 6 declared tokens (population OPEN -- the ruling did not close it)"
BAD:   "7 of 24"                     <-- asserts a closure the sovereign word explicitly refused
```

**ORACLE:** every denominator the mechanism emits carries its openness marker. Grep the output for
a bare integer-of-integer form; there must be none over the token population.

### 1.3 `ND-a-3` — the Opal-side naming discriminator, stated WHERE THE CATCHERS ARE

Partner tax-free descriptors (`CA Tax-Free Bond`, `Tax-Free Bond`) are **NOT** Opal name-forms —
the Opal muni *"would literally say Muni."* `Tax` and `Muni` remain candidate-catchers, but the
discriminator must be stated **at the point the `Tax`/`Muni` catchers are defined**, not in a
distant doc.

**ORACLE:** the discriminator is within reading distance of the catcher definition. A reader
maintaining the catcher sees the discriminator without going looking for it.

### 1.4 `ND-b-1` — the declared CLASS named, the v1 coverage set ENUMERATED inside it

```
DECLARED CLASS:  partner-supplied constituent-name surfaces (any partner/custodian feed
                 delivering model/sleeve names)
v1 COVERAGE:     cottonwood's surfaces -- ENUMERATED INDIVIDUALLY, each named
```

⛔ **COVERAGE PRINTS AS "cottonwood's N surfaces of the declared class", NEVER as a universal
sweep.** A sweep that reports "all surfaces" when it read one partner's is the coverage lie this
cell exists to refuse.

### 1.5 `ND-b-2` — a second partner is a MEMBERSHIP ADD

**ORACLE, and it is an EXERCISE, not an assertion:** add a FICTITIOUS partner to the declared list
and observe that **no code changes** — no schema, no matcher, no cell. If adding a partner requires
a code edit, this cell fails and the design is wrong.

---

## 2. INVARIANTS — BINDING, cut FIRST

- **`ND-inv-1`** — FUZZY AT DISCOVERY, EXACT AT THE SERVED KEY. Widen what is LOOKED AT, never what
  is SERVED.
- **`ND-inv-2`** — ⛔ **DISCOVERY SURFACES, IT NEVER SILENTLY CLASSIFIES.** No cell in this TO may
  write a classification the mechanism inferred.
- **`ND-inv-3`** — A VALUE CARRIES ITS CLAIM (`measured`/`inferred`/`held`/`absent`) in a field.
  **AND THE CONSUMING HALF IS THE MECHANISM:** a consumer that does not REFUSE an unmarked value
  makes the field decoration, and it drifts to unpopulated. Build the refusal, not just the field.

---

## 3. DECLARED OUT OF SCOPE — do not read these absences as gaps

`ND-g-1` security grain (OUT, not deferred) · `ND-g-2` the `canonical_key('DIVZ SMA')` raise (a
named forward hazard on a producer this project does not own — RECORDED, not remediated) ·
`ND-g-3` the classification act itself · `ND-g-4` partners beyond cottonwood (in the declared CLASS,
outside v1 COVERAGE — **declared-in-domain, not-yet-covered is NOT out of scope**).

---

## 4. `<compiler_tools_mandate>`

- **Phase 1 (before writing):** `comp-which` on the surface question; `comp-find --name` to confirm
  no existing declared-token artifact already exists in usable form. **Rule 5 (pre-authoring repo
  check): if the artifact already exists in the form this TO would author, scope COLLAPSES to
  verify + rerun.** State which.
- **Phase 2 (before committing):** `.tools/commit-gate.sh` on every `.py`. Print the coverage
  denominator with its openness marker in the commit message.
- **Phase 3 (after committing):** re-run the `ND-b-2` fictitious-partner exercise and paste the
  zero-code-change evidence.

## 5. `<data_reprocess_scope>`

**`<no_reprocess_needed>`** — this TO authors DECLARED ARTIFACTS and a coverage enumeration. It
writes no silver/bronze converter and changes no historical partition. No downstream consumer reads
a changed code path for pre-patch partitions.

---

## 6. SEATING — READ THIS BEFORE STARTING

⛔ **NO SEAT IS ASSIGNED AND I AM NOT INVENTING ONE.** Measured 2026-08-27 ~17:0xZ on three planes:
broker liveness = 4 entries, all Tier-0/1; spawn markers = 0; no Tier-2 executor exists on this
fabric. Base `0.4.0_DS_ClientPlatform` already carries open `ETFS_POSITIONING` TOs, so seating this
at the base is a **Rule 27 one-project-per-instance collision at seating time**.

**The lane letter is `0.0.0_AB_MSTR~Z`'s to assign from the spawn-audit UNION disk.** Surfaced to
them by `1.0.0_SA_CTO~Z`; the same constraint was independently surfaced by `2.0.0_SA_COO~Z` for
`D1_CATVIEWS.TO-F3-DS`. **This TO is ACTIVE and unblocked on its merits — it is waiting on a SEAT,
not on a decision.**

<decomp_ref>workflows/atom_decomposition/runs/d1-namediscovery/20260826T214534Z/DECOMP.md @669e04f27b — cells `ND-a-1` `ND-a-2` `ND-a-3` `ND-b-1` `ND-b-2`. ⚠ **VINTAGE NOTE, stated because the two are not the same commit:** `3.0.0_SA_CVO~Z` CERTIFIED at `@bcca23915b`; `2.0.0_SA_COO~Z` then landed the CVO F1/F4 repairs at `@669e04f27b`. **Build against `@669e04f27b`** — it carries the certified content PLUS both repairs. A citation without a vintage is not a citation (Rule 22).</decomp_ref>
<certification>**CERTIFIED WITH FINDINGS** — `3.0.0_SA_CVO~Z`, `org/tier1_exec/3.0.0_SA_CVO/deliverables/cvoZ_D1_NAMEDISCOVERY_DECOMP_CERTIFICATION_20260827.md`. **NO TO-mint block.** ⛔ **What the signature does NOT buy:** F2 and F3 are LIVE P1 findings routed into TO-2 and TO-3 respectively; none lands on this TO's cells. The certifier reproduced the cell census exactly (20 cells, 16 criterion-bearing) and swept scope forks across THREE planes (SITEZ, origin/CLOUD, a commit-message sweep, denominator 491 commits).</certification>
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
  <!-- ISSUANCE half (1.0.0_SA_CTO~Z). POSITIONAL - no --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json ND-TO1-AC1,ND-TO1-AC2,ND-TO1-AC3,ND-TO1-AC4,ND-TO1-AC5
       CHECK THE RC, NEVER THE OUTPUT STRING; take it WITHOUT A PIPE. The coverage diff is
       BIDIRECTIONAL - an expected id with NO row refuses the whole instance, so every id below
       needs a row even if it lands UNCOMPUTABLE-BY-CONSTRUCTION. -->
  <criterion id="ND-TO1-AC1" cell_refs="ND-a-1"/>
  <criterion id="ND-TO1-AC2" cell_refs="ND-a-2"/>
  <criterion id="ND-TO1-AC3" cell_refs="ND-a-3"/>
  <criterion id="ND-TO1-AC4" cell_refs="ND-b-1"/>
  <criterion id="ND-TO1-AC5" cell_refs="ND-b-2"/>
  <expected_criteria>ND-TO1-AC1,ND-TO1-AC2,ND-TO1-AC3,ND-TO1-AC4,ND-TO1-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D1_NAMEDISCOVERY.TO-1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Acceptance criteria

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`ND-TO1-AC1`** | The 6 tokens and 5 form classes are a **DECLARED ARTIFACT a non-author can read and extend** — never a literal embedded in a matcher. **Exercise: add a seventh token WITHOUT touching matcher logic** | `ND-a-1` | **ARTIFACT + EXERCISED** |
| **`ND-TO1-AC2`** | **Every printed denominator carries its own OPENNESS.** A bare `24` (or any bare `N of M` over the token population) anywhere is the defect. Grep the emitted output and print the count of bare forms — it must be **0**, with a positive control showing the grep can find one | `ND-a-2` | **SOURCE + control** |
| **`ND-TO1-AC3`** | The Opal-side discriminator (`CA Tax-Free Bond` / `Tax-Free Bond` are NOT Opal name-forms; the Opal muni *"would literally say Muni"*) is stated **where the `Tax`/`Muni` catchers are defined**, not in a distant doc. Cite `file:line` | `ND-a-3` | **SOURCE** |
| **`ND-TO1-AC4`** | The declared CLASS is named AND cottonwood's v1 surfaces are **enumerated individually**. Coverage prints as *"cottonwood's N surfaces of the declared class"* — ⛔ **never as a universal sweep** | `ND-b-1` | **ARTIFACT** |
| **`ND-TO1-AC5`** | ⛔ **AN EXERCISE, NOT AN ASSERTION:** add a FICTITIOUS partner to the declared list and show **no code changes** — no schema, no matcher, no cell. If a partner add needs a code edit, this cell FAILS and the design is wrong | `ND-b-2` | **EXERCISED** |

-- `1.0.0_SA_CTO~Z`, issuer
