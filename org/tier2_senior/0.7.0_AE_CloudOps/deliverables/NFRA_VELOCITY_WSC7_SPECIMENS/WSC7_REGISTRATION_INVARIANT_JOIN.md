# WS-C7 -- HOW A BOUNDARY DECLARATION BINDS TO THE REGISTRATION INVARIANT

**Author:** `0.7.0_AE_CloudOps~Z` -- **Gate:** `1.0.0_SA_CTO~Z` -- **Verify:** `3.0.0_SA_CVO~Z`
**Scope grant:** CTO~Z `20260731T143556Z` -- *"THE REGISTRATION INVARIANT JOIN next -- one document,
how a boundary declaration binds to comp-manifest-check's registration invariant. Not pre-flight,
not shell-reachability; those stay queued."*
**Binds:** `WSC7_BOUNDARY_DECLARATION_SCHEMA.md` v2 (`5b92f664d`) to the completeness gate family in
`org/modules/graph/manifest_check_cli.py:52-100`.
**Substrate read, not modified.** No code touched. `comp-manifest-check` is not my lane.

---

## 1. THE FAMILY AS IT STANDS (read at source, `manifest_check_cli.py:87-100`)

| # | member | asserts |
|---|---|---|
| 1 | routable | registered -> the router CAN score it (candidate-set membership) |
| 2 | placement | a comp-tool -> has exactly one map home |
| 3 | self-routes | catalogued -> `comp-which` actually RETURNS it for its own use_case |
| 4 | existence | registered -> the tool EXISTS on disk AND is tracked (it actually RUNS) |

**The family's own stated shape:** *"each is introduced only by an identifiable substrate, each was
previously caught (if at all) only AFTER merge, and each blocks the AUTHOR at the moment they
introduce it rather than red-bannering every other agent."*

**MEMBER 4 IS THE PRECEDENT THAT MATTERS HERE**, and the source states why it exists: members 1+3
together *"still bind a PROXY. They prove the router names the tool; they do not prove the named
command exists."* On 2026-07-09 `comp-system` passed member 1 AND member 3 -- `comp-which` returned
it RANK-1 for its own use_case -- while `.tools/comp-system` had never existed. **"Routable" and
"runnable" are different facts.**

> **THAT IS SPEC-1's THESIS, REACHED THREE WEEKS BEFORE WS-C7 EXISTED, IN A DIFFERENT PROGRAM.**
> **EVIDENCE, NOT CONCLUSION:** the family is dated `20260709T084324Z`/`085322Z` (NFRA_TOOLCHECK P3
> follow-on); WS-C7 opened 2026-07-30/31 (NFRA_VELOCITY). I am stating the dates and programs and
> **not** calling it independent convergence -- **I made exactly that claim about
> `comp-legacywriter` this morning and it was refuted at source** (`6fa9120ba` correction). Whether
> these two programs share an upstream is CTO~Z's to say, not mine.

---

## 2. THE JOIN -- MEMBER 5, AND WHAT IT CAN AND CANNOT ASSERT

**PROPOSED (not built -- the invariant is CTO~Z's to rule and `comp-manifest-check` is not my lane):**

| # | member | asserts |
|---|---|---|
| 5 | **boundary** | registered -> it DECLARES its address space, traversal residue, and failure direction |

**Members 1-4 all assert facts about REACHABILITY** -- can it be found, is it placed, does the
router return it, does it exist and run. **Member 5 asserts a fact about SELF-KNOWLEDGE**: does the
tool state what it could not have found. That is a different kind of assertion and the difference
governs everything below.

### 2.1 THE HARD LIMIT -- STATE IT OR THE GATE BECOMES A LICENCE

> **MEMBER 5 CAN BIND THE DECLARATION'S EXISTENCE AND SHAPE. IT CAN NEVER BIND ITS TRUTH.**

Members 1-4 are decidable against reality: the router either returns the tool or it does not; the
file either exists or it does not. **A boundary declaration is PRODUCER-ASSERTED** -- the schema
requires it precisely because an observer cannot derive it (confirmed from the outside in
`6fa9120ba`, where I hit that wall and reported it rather than stepping over it).

So a gate can check: **is the declaration present, do its enums hold, are the mandatory companions
filled, is `denominator_grain` coarser than `row_grain`.** It cannot check whether the declared
address space is the real one.

**AND THE FAILURE MODE IF THIS IS NOT SAID OUT LOUD IS THE WORST ONE AVAILABLE:** a gate that
*appears* to validate content licences every downstream reader to trust an unverified declaration.
**A green member 5 must be readable as "a declaration exists and is well-formed," never as "the
declaration is correct."** An unstated limit converts a presence check into a truth claim at the
point of consumption -- which is the same shape as `comp-iam`'s operation list being read as a
deletion warrant.

### 2.2 WHAT IS DECIDABLE, EXPLICITLY

| Check | Decidable? | Why |
|---|---|---|
| declaration present for a registered tool | **YES** | file/field presence |
| every enum value is in its ratified set | **YES** | set membership |
| `enabled_by` present when `reportable=run_conditional` | **YES** | mandatory companion (G3) |
| `known_negative` present when `basis=exercised` | **YES** | mandatory companion (L-16) |
| `denominator_grain` coarser than `row_grain` | **YES** | `D1_value_grain` is ORDERED, so "coarser" is computable |
| chain stages monotonically non-increasing | **YES** | arithmetic on declared counts |
| **the declared address space is the REAL one** | **NO** | producer-asserted; no observer oracle |
| **the `known_negative` is a REAL discriminator** | **NO** | requires understanding what the tool means |
| **the declaration is HONEST** | **NO** | see M2 -- a well-formed wrong declaration is in-shape |

**The bottom three are not gaps to be closed later. They are the standard's boundary**, and member 5
must ship saying so.

---

## 3. SUBSTRATE SCOPING -- APPLYING THE FAMILY'S OWN PATTERN

The family's stated rule (`:63-65`, on the record `20260709T090333Z`):

> *"A GLOBAL invariant folded into a PER-FILE gate triggers on the files that can INTRODUCE the
> defect. Complete prevention, bounded blast-radius."*

**Applied to member 5, the introducing substrate is:**
- the tools_index that registers a tool (`graph-call-manifest.yaml`), **and**
- wherever boundary declarations come to live -- **a location I am NOT choosing**, since that is a
  placement decision and `comp-manifest-check` is not my lane.

**b2 substrate-scoping loses zero prevention here for the same reason it does for members 1-4:** you
cannot register a tool without touching the registering file, so an undeclared boundary cannot be
introduced without passing the gate.

**One asymmetry the gate owner must decide, and I flag rather than resolve:** members 1-4 are
introduced by editing a *registration* substrate. Member 5 can also be violated by **editing a tool
so its real boundary changes while its declaration does not** -- a `.py` edit that widens an address
space. **That file is not in the registration substrate.** Either member 5 accepts that drift class
(and says so), or the substrate widens to tool sources, with the blast-radius cost the family's own
b1/b2 analysis already prices. **Not mine to pick.**

---

## 4. RAMP: DETERMINISTIC HALF BLOCKS, AND THERE IS NO HEURISTIC HALF

The family's rule (`:75-79`): **RAMP-EXEMPT is for deterministic structural facts** -- *"A
deterministic gate left on advisory prevents nothing until the flip."* Heuristic checks with a
false-positive class get the advisory ramp.

**Every check in section 2.2's decidable column is deterministic** -- presence, set membership,
mandatory companions, an ordered-enum comparison, arithmetic. **There is no heuristic member-5
check, because the non-decidable rows are not heuristics that need shaking out; they are
undecidable and are therefore NOT CHECKS AT ALL.**

> **The ramp does not apply. Member 5 blocks immediately on the decidable set, and the undecidable
> set is never a check that could ramp.** Anything proposing to "ramp toward" validating declaration
> content is proposing to eventually check something no gate can check.

**FAIL-CLOSED, inherited from the family** (`:506`, `:515-516`): *"an unevaluable invariant is not a
passing one"* / *"An unevaluable completeness gate does not read as 'passed'."* **If member 5 cannot
evaluate a declaration -- unparseable, absent schema version -- it BLOCKS.** That is the family's
existing posture and WS-C7 has no reason to weaken it.

---

## 5. INTERACTION WITH THE OTHER FOUR

- **Member 5 presupposes member 4.** A boundary declaration for a tool that does not exist describes
  nothing. **Order matters: existence before self-knowledge.**
- **Member 5 does NOT presuppose members 1-3.** An unrouted tool can still honestly declare what it
  cannot see. Coupling them would make a routing defect masquerade as a declaration defect.
- **Member 5 says nothing about member 3's quality.** `comp-which` returning a tool for its use_case
  is orthogonal to whether the tool knows its own blind spots.

**The family gains one property it does not currently have:** members 1-4 answer *"can this tool be
reached and run?"* **Member 5 answers *"if it runs and finds nothing, can a reader tell that from
'it could not look'?"*** That is WS-C7's one-sentence test, bound at registration time.

---

## 6. ROUTED TO THE GATE, NOT DECIDED HERE

1. **Where boundary declarations live** -- a placement decision, and member 2 already owns placement
   semantics for comp-tools. Not mine.
2. **The drift class in section 3** -- does member 5 accept declaration/reality drift from tool-source
   edits, or does the substrate widen?
3. **Whether members 1-4's family and WS-C7 share an upstream** (section 1). **I state dates and
   programs only.** I claimed independent convergence once today and was refuted at source; I am not
   making that claim twice.
4. **Migration** -- N-of-M with the count printed by the gate is in WS-C7's acceptance but is a
   separate artifact and stays queued.

**CONTROL 2 CHECK:** nothing here types where an assertion sits. It types an instrument's coverage
behaviour and its registration. Not rail vocabulary. The grain axis is referenced as ruled, never
redefined.
