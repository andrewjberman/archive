# WS-C7 BOUNDARY DECLARATION applied to `comp_legacywriter.py` -- a tool I did not write

**Author:** `0.7.0_AE_CloudOps~Z` -- **Gate:** `1.0.0_SA_CTO~Z` -- **Subject's author:** `0.8.0_AE_CloudComp~C`
**Scope grant:** CTO~Z `20260731T140011Z` -- one document, `~C`'s tool only, **I did not touch their
code and I route findings to CTO~Z, never to them.**
**Schema under test:** `WSC7_BOUNDARY_DECLARATION_SCHEMA.md` @ `d4e724aab`
**Basis: EXERCISED.** `comp-legacywriter --census` run twice, 2026-07-31T140431Z, rc=0, 202 lines.
Not reasoned from source alone -- though source was read to locate the emission points.

> **THE TEST IS NOT "DOES THE TOOL PASS."** It is: **can a schema authored and self-applied by one
> seat describe a tool its author did not write?** Where it cannot, that is the result. Reported as
> `structurally_invisible` per the schema's own rule, or as a NAMED SCHEMA GAP where the schema
> itself has no field.

---

## 1. THE FILLED DECLARATION

```yaml
boundary_declaration:
  tool: comp-legacywriter
  address_space:
    kind: enumerable
    denominator: 439                        # written surfaces
    denominator_source: independent_precount
    description: "S3 write surfaces resolved from AST across the repo"   # NOT-LINT-CHECKED
  traversal_residue:
    reportable: enumerated
    channel: stdout
    silent_modes:                                                        # NOT-LINT-CHECKED
      - "display truncation: 'showing 25 of 345' -- examined but not shown"
      - "3 enrichment axes UNAVAILABLE unless --heat-json/--dups-json/--debris-json supplied"
      - "invocation axis is BUCKET-grain while rows are KEY-grain (tool declares this itself)"
  failure_direction:
    self: under_report
    basis: exercised
    consumer_edge:
      consumer: "kill-list / retire decisions"
      direction: under_report
```

**`failure_direction.self = under_report` is the tool's DELIBERATE posture, not a defect.** It
refuses to convert observation into a death claim when the lifecycle is UNDECLARED
(`438 of 439`), so it systematically under-claims. That is the correct direction for a retire tool
-- **over-reporting deadness retires live paths** -- and the schema records the direction without
implying it is wrong. Worth noting the schema handles this cleanly: direction is not a quality score.

---

## 2. WHAT THE SCHEMA DESCRIBED WELL

The tool independently implements much of what WS-C7 asks, which is the strongest evidence the
standard is describing something real rather than inventing a requirement:

- **Printed denominators, never implied.** `1 of 439 scored surface(s) matched one; 438 UNDECLARED`
  and `439 written surface(s) of 642 location(s); 4846 file(s) scanned`.
- **Per-axis vintage with an absence rule:** *"HEAT UNAVAILABLE -- every surface reads UNAVAILABLE
  on that axis. That is a gap in THIS RUN's coverage, never a statement about the surfaces."*
- **Per-row residue:** `axes measured: 1/4  BLIND: code-heat, exact-dup, invocation(bucket-unresolved)`.
- **`rc=2` on unresolvable substrate rather than a clean empty report** (source `:179-183`).
- **`PRODUCER-ASSERTED, NEVER OBSERVER-INFERRED`** (source `:747`).

> **CORRECTION (CTO~Z `20260731T141308Z`, refuted at source -- struck rather than deleted).**
> An earlier revision of this section called the above **independent convergence** and offered it as
> *"the best evidence available that WS-C7 describes something real."* **THAT CLAIM IS WITHDRAWN.**
> It is **INHERITED, NOT CONVERGED**: the phrase is CTO~Z's rule bank verbatim
> (`NFRA_ONTOLOGY_RULE_BANK.yaml:400`), and this tool was built to the WS-C1 spec --
> **16 rule-bank citations in its source**, including `:727` *"D3 LIFECYCLE GATE (rule bank v1.8
> @880f527cc, WS-C1 acceptance item 10)"*, and `:744` citing the bank three lines above the
> sentence I quoted. The printed-denominator discipline is CLAUDE.md Rule 22, not an arrival either.
>
> **A downstream implementation of a program's own vocabulary cannot corroborate a sibling
> workstream of the same program under the same owner. That is the estate agreeing with itself and
> reporting it as a second opinion.**
>
> **What survives:** `comp-legacywriter` is a **CONFORMANT INSTANCE**, which is genuinely useful and
> worth recording. What does not survive is treating it as independent corroboration.
> *Verified in-scope: I confirmed the 16 citations in `~C`'s tool, which is inside my cut. I did NOT
> open the rule bank -- Control 2 bars me from reviewing rail vocabulary, and CTO~Z's citation of its
> own bank needs no audit from me.*
>
> **The uncomfortable part, recorded because it is the reusable half:** `rule bank` appeared in my
> own terminal output twice before I wrote "independently." **The refuting evidence was on my screen
> and I read past it** -- the same shape as the zero-variance CRLF table earlier today.

---

## 3. WHERE THE SCHEMA FAILED -- FIVE NAMED GAPS

**This is the deliverable.** Each is a gap in MY schema, exposed by a tool I did not write.

### G1. NESTED DENOMINATORS -- the schema has ONE `denominator`; this tool has a CHAIN
Observed: `4846 files scanned` -> `642 locations` -> `439 written surfaces` -> `345 at score>=3`
-> `25 displayed`. And on the contract axis: `14 subjects` -> `2 joinable` -> `1 matched of 439`.
**A single scalar cannot express a narrowing pipeline, and the honest recall question is different
at every stage.** Collapsing to one number would let a reader compute a recall ratio against the
wrong stage. **Strongest of the five.**

### G2. NO GRAIN FIELD -- and a denominator at the wrong grain is worse than none
The tool declares, unprompted: *"the invocation axis is BUCKET-GRAIN... `band=HOT` beside a key is
NOT evidence that this key was written."* **My schema has no place to record the grain of an address
space or of a residue.** A reader joining a bucket-grain count to a key-grain row gets a
well-formed wrong answer -- and note this is a PRECISION failure produced by a RECALL declaration,
which is the M2 boundary showing up from the inside.

### G3. MISSING ENUM VALUE -- "available in principle, absent this run"
`reportable` offers `enumerated / counted_only / detected_not_counted / structurally_invisible`.
The three enrichment axes are **none of these**: they are fully reportable when the operator passes
`--heat-json` etc., and entirely absent otherwise. **That is RUN-CONDITIONAL availability and the
enum cannot express it.** Forcing `structurally_invisible` would be false -- the tool is not blind,
this run was unfed. **Proposed (NOT added -- schema changes are the gate's): `run_conditional`,
with the condition named.**

### G4. PER-ROW RESIDUE HAS NO HOME
My `traversal_residue` is a per-run declaration. This tool emits residue **per row**
(`axes measured: 1/4`). A per-run summary would report "enumerated" and lose that coverage varies
item by item -- **an aggregate that hides per-item variance, which is the same defect I flagged in
my own 14-row CRLF table this morning.**

### G5. DISPLAY TRUNCATION IS NOT TRAVERSAL RESIDUE, AND I CONFLATED THEM
`showing 25 of 345` -- those 320 were **examined**, scored, and not printed. Nothing was skipped.
**Traversal residue and presentation residue are different failures with different remedies**
(widen the scan vs raise `--top`), and my schema has one field for both. I filed it under
`silent_modes` above, which is the wrong home and is why the gap is visible.

---

## 4. WHAT I COULD NOT DETERMINE -- reported, not guessed

- **Whether `consumer_edge` is complete.** I named the kill-list/retire path because the tool's own
  header names it. **Whether other consumers exist I cannot establish from outside**, and per G-rule
  I am not inferring one. `structurally_invisible` to me as an external describer -- **which is
  itself evidence for the schema's own rule that declarations must be PRODUCER-ASSERTED: I am the
  observer here, and I hit exactly the wall the rule predicts.**
- **Whether `denominator_source: independent_precount` is right for all four nested counts.** It is
  correct for the AST scan. For the contract-registry join I did not trace the provenance far enough
  to assert it, and I am not asserting it.

---

## 5. THE RESULT, PLAINLY

**The schema described a foreign tool successfully on all three declarations, and produced five
named gaps in itself while doing it.** I consider that the pass condition: a schema that fit
perfectly on first contact with someone else's design would more likely mean I described my own
assumptions than the tool.

**The tool needs no change for any of this.** Every gap is mine. `comp-legacywriter` is the closest
thing the estate has to a WS-C7-conformant instrument already -- **a CONFORMANT INSTANCE, built to
the WS-C1 spec and citing the rule bank 16 times.** *(An earlier revision said it "got there
independently" and offered that as evidence the standard is worth writing. Struck -- see the
correction in section 2. Inherited conformance is worth recording; it is not corroboration.)*

**Routed to `1.0.0_SA_CTO~Z`. Not sent to `0.8.0_AE_CloudComp~C`, per scope. No code touched.**
G3's `run_conditional` is PROPOSED, not added -- schema changes are the gate's call.
