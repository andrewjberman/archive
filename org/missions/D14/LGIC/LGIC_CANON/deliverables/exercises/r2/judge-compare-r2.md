# judge-compare-r2 -- the comparison over judges C, D and E, every disagreement traced to a canon coordinate

**Cell** `CN-j-7`, round 2, decomposition v4. **Written by** `0.9.0_WK_LGIC_CANON~7` on TO
`LGIC_CANON.CN-j-7-r2`, in worktree branch `wk-lgic-canon-2-7`, base `7db18a4464`.
**This worker judged nothing.** It read three finished judge files and the canon; it did not grade a plane.

⛔ **NOTHING HERE PICKS A WINNER.** Every disagreement below is LOCATED in the canon and left open.
Adjudication is `3.0.0_SA_CVO`'s at L9 (order: *"Do not resolve a disagreement by picking a winner"*).

**Inputs read, all at base `7db18a4464` in this worktree:**

```
org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/r2/judge-c.tsv          13 plane rows
org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/r2/judge-d.tsv          13 plane rows
org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/r2/judge-e.tsv           7 plane rows
infra/logic/02_DOCTRINE.md                                                     627 lines, v1.1
org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/CN_SEVEN_RULES.json
org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/CN_SEVERITY.md
org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/CN_TREE_INFLECTION.md
```

Read additionally, because section 3 could not be answered without them (see section 0):

```
org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/CN_TREE_MDPF.md   judge E's tree
org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/judge-a.tsv                            round 1, same tree
org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/judge-b.tsv                            round 1, same tree
org/missions/D14/LGIC/LGIC_CANON/task-orders/LGIC_CANON.CN-j-6-r2.judge-e-negative-arm.md      E's brief
```

---

## 0. WHAT WAS COMPARED -- and the population the cell text assumes and the fixed inputs deny

⚠ **C AND D DID NOT JUDGE THE SAME TREE AS E, SO "E's verdicts versus C's and D's" HAS NO SHARED CELL.**

| judge | its order | its tree | planes | had the severity brief? |
|---|---|---|---|---|
| C | `CN-j-4-r2` | `fixed_inputs/r2/CN_TREE_INFLECTION.md` | 13 | YES -- order line 28 and line 37 name `CN_SEVERITY.md` |
| D | `CN-j-5-r2` | `fixed_inputs/r2/CN_TREE_INFLECTION.md` | 13 | YES -- order line 27 and line 36 name `CN_SEVERITY.md` |
| E | `CN-j-6-r2` | `fixed_inputs/r1/CN_TREE_MDPF.md` | 7 | NO -- by design, and its order names the file nowhere |

`CN_TREE_INFLECTION.md` says so itself: *"`CN-j-6` (judge E) does NOT read this file -- its tree is round 1's
MDPF tree, unchanged, as the negative arm."* `CN_SEVERITY.md` says the same from the other side: *"Judge E
judges the same tree round 1's judges did."* **The INTENDED comparator for E is round 1's judges A and B, who
judged the MDPF tree WITH the scale in their orders** -- not C and D, who judged a different tree.

So this document does what the two comparisons each admit:

- **Section 1** is C vs D, plane by plane, axis by axis -- 13 planes x 5 axes = **65 axis cells**, a real
  common denominator because both judged the identical file.
- **Section 3** answers the arm on the **MDPF tree**, E against round 1's A and B, the only population where
  a with-scale / without-scale contrast has shared planes. E vs C/D is reported there too, at the only grain
  it supports (vocabulary and decision discipline), and labelled as such.

Filed as surprise row `LGIC_CANON-W7-S4`. Nothing was worked around: both comparisons are printed.

---

## 1. C versus D -- agreement and disagreement, per plane per axis

Legend: `C`=CONFORMS `X`=DECLARED-EXCEPTION `P`=DEPARTS-RECOMMENDED `U`=UNDETERMINED `V`=VIOLATES.
Each cell is `judgeC/judgeD`; **bold** marks a disagreement.

| # | plane | A1 C/D | A2 C/D | A3 C/D | A4 C/D | A5 C/D | same |
|---|---|---|---|---|---|---|---|
| 1 | `orion/inflection/bronze/` | C/C | C/C | C/C | U/U | C/C | 5 of 5 |
| 2 | `orion/inflection/silver/` | U/U | C/C | C/C | U/U | **U/C** | 4 of 5 |
| 3 | `eclipse/inflection/bronze/` | C/C | C/C | **V/U** | U/U | C/C | 4 of 5 |
| 4 | `eclipse/inflection/silver/` | U/U | C/C | C/C | U/U | **U/C** | 4 of 5 |
| 5 | `opal-data-inf/platinum/` | C/C | **V/C** | U/U | U/U | C/C | 4 of 5 |
| 6 | `opal-data-inf/gold/` | C/C | **V/C** | U/U | U/U | V/V | 4 of 5 |
| 7 | `opal-data-inf/silver/` | **V/U** | V/V | U/U | U/U | V/V | 4 of 5 |
| 8 | `opal-data-inf/bronze/` | V/V | V/V | U/U | U/U | V/V | 5 of 5 |
| 9 | `opal-data-inf/backup/gold_canonical_PRE_REDERIVE_.../` | U/U | U/U | V/V | U/U | U/U | 5 of 5 |
| 10 | `opal-data-inf/_pre_rebuild_backup/.../silver/` | U/U | U/U | V/V | U/U | U/U | 5 of 5 |
| 11 | `opal-data-inf/_toolprobe_scratch/` | U/U | U/U | V/V | U/U | U/U | 5 of 5 |
| 12 | `opal-data-inf/backup/pre_pullheal_.../code/gold/` | U/U | U/U | V/V | U/U | U/U | 5 of 5 |
| 13 | `opal-data-inf/code/{bronze,silver,gold}` | U/U | C/C | C/C | U/U | U/U | 5 of 5 |

**AGREEMENT, with its denominator: 59 of 65 axis cells identical (90.8 percent); 6 of 65 differ.**
By axis: A1 12 of 13, A2 11 of 13, A3 12 of 13, A4 13 of 13, A5 11 of 13.
By plane: 7 planes agree 5 of 5; 6 planes differ on exactly one axis each; **no plane differs on two axes.**
No disagreement is a CONFORMS-versus-VIOLATES inversion: every one of the six is adjacent on the canon's own
severity order (`02_DOCTRINE.md:117-120`).

### 1a. The six disagreements, each traced to a canon coordinate

| marker | id | plane | axis | judge C | judge D | canon coordinate where the room is | what the canon does not say |
|---|---|---|---|---|---|---|---|
| DISAGREE | D1 | `orion/inflection/silver/` | A5 | UNDETERMINED | CONFORMS | R10 census, `infra/logic/02_DOCTRINE.md:414-419` -- it enumerates VIOLATED-LIVE JSON-under-silver instances and adds *"Completeness and trigger UNMEASURED by the census"*, and it carries NO monolith-wide clearance line; contrast R9's census at `:405-406`, *"Monolith bronze CONFORMANT"* | whether ABSENCE FROM A VIOLATION LIST is a clearance. C reads no-clearance as UNDETERMINED; D reads not-named-as-violated as CONFORMS. R9 grants the blanket tag and R10 does not, and neither rule says whether the asymmetry is deliberate |
| DISAGREE | D2 | `eclipse/inflection/bronze/` | A3 | VIOLATES | UNDETERMINED | R1, grammar at `:149-152` (the `{table}` slot, SOURCE-FIRST, superseded 2026-09-13) versus R1's OWN census at `:171`, *"53 of 53 non-SmartX monolith planes CONFORMANT"*; plus the tree's note that the 108 date-named table-level prefixes are a ledger sub-finding *"it did not re-measure (CTO msg 96116 item 6)"* | at which GRAIN R1 is tested. The census clears the PLANE; the grammar binds the KEY. C applies the grammar to the 108 sub-prefixes and reads VIOLATES; D holds that a sub-finding the ledger did not re-measure cannot be settled from this tree and reads UNDETERMINED. R1 states no grain for its own census tag |
| DISAGREE | D3 | `eclipse/inflection/silver/` | A5 | UNDETERMINED | CONFORMS | R10 census, `infra/logic/02_DOCTRINE.md:414-419` -- the same coordinate as D1, on the second monolith silver plane | the same silence as D1. The two rows are ONE canon hole reached twice, not two independent splits |
| DISAGREE | D4 | `opal-data-inf/platinum/` | A2 | VIOLATES | CONFORMS | R6 census, `:364-365`, *"firm-bucket platinum CONFORMANT (bd 24,631 - inf 8,673 - cot 1,136, all live)"* versus R5's which-bucket bullet at `:354-357`, *"Ruled so far: ... `opal-data-49financial`, `-inflection`, `-cottonwood` firm"*; R7 at `:376-380` makes the firm bucket MANDATORY without naming the bucket STRING | whether the LEGACY SHORT-FORM bucket `opal-data-inf` IS "the firm bucket" while `opal-data-inflection` is unminted (the tree: *"does not exist yet"*). R6's census counts `inf` 8,673 as CONFORMANT firm-bucket platinum -- the same 8,673 objects this plane holds -- while R5's ruled name for inflection's firm bucket is the long form. D reads the census tag, C reads the ruled name. The canon carries both and reconciles neither |
| DISAGREE | D5 | `opal-data-inf/gold/` | A2 | VIOLATES | CONFORMS | R5 at `:346-347` plus its census at `:350-352`, whose VIOLATED-LIVE list does NOT include `opal-data-inf/gold/` and whose closing line reads *"Firm/product bucket golds CONFORMANT on home (format: R11)"*; R5's which-bucket bullet at `:354-357`; R7 at `:376-380` | the same unstated identity as D4, on gold instead of platinum. Both judges cite R5/R7 and split on whether the short-form bucket satisfies them. NOTE the correlation: D4 and D5 are ONE unresolved identity reached twice -- they are not two independent disagreements, and counting them as two overstates the split |
| DISAGREE | D6 | `opal-data-inf/silver/` | A1 | VIOLATES | UNDETERMINED | R18 at `:516-523`: the rule text (*"NO SHADOW PATH, NO DUAL-WRITE"*), its only census example (*"a dual-write twin -- VIOLATED (live status 31d)"*) and its single non-application (*"a same-window rollback copy explicitly named in a never-widen sign-off"*); with R19 at `:524-531`, which makes a migration its own project and gives it no in-flight STATUS | whether a migration MID-CUTOVER -- legacy plane live, canonical destination twins already live, both dated 09-12 -- is the standing dual-write R18 forbids. R18's only worked example carries a DURATION (31d) but the rule states no duration test, and R19 names no state a plane occupies between PORT and REPOINT. C reads two live copies as the forbidden thing; D reads the missing standing evidence as undecidable |

**Every one of the six traces. Zero untraced.** Rows that could not be traced would be listed here as the
finding; there are none.

### 1b. Where the rule CITATIONS differ without the verdict differing

Not a verdict disagreement and not counted above, but it is the same canon hole one level down. On the 12
backup/scratch/probe and code rows the two judges agree on every verdict while citing different rule sets:
C cites `A1:R18` and `A5:R9/R10/R11` (the rule that WOULD govern the tier the artifact imitates); D cites
`R9` on both A1 and A5 for every backup row (the rule the AXIS TABLE names). Coordinate: the §2 axis table
at `infra/logic/02_DOCTRINE.md:88-94` names rules per axis, and R17 at `:506-515` governs non-tier material
without saying what the OTHER four axes cite when they do not apply. This is the identical shape round 1
filed as `LGIC_CANON-W7-S1` on axis A1, one round earlier and on the other tree.

---

## 2. THE SEVEN-RULE REACH (A-13), with denominators

Source of truth per judge: **that judge's own `reach` column**, read by name, plus its why-text.
⚠ The whole-row reading is NOT used and must not be: it counts a rule a judge NAMES while explaining it is
NOT reached (`LGIC_CANON-W5-S2`, repaired by the issuer at `df30196cc1`, `LGIC_CANON-S9`).
**Denominator for every partition below: 7, the rules in `CN_SEVEN_RULES.json`.**

### 2a. Union of C and D -- the INFLECTION tree

```
REACHED     (3 of 7): R14, R17, R19
NOT REACHED (4 of 7): R3, R8, R15, R21
```

C alone: reached 3 of 7 (R14, R17, R19). D alone: reached 3 of 7 (R14, R17, R19).
**C and D AGREE EXACTLY on all seven, 7 of 7 -- there is no reach disagreement to trace.** The instrument
that once printed 7 for D and 3 for C was reading D's prose, not D's determination.

Why each NOT REACHED rule is not reached, from the judges' own text and `CN_SEVEN_RULES.json`:

- `R3` -- needs two vendor MASTERS of ONE firm. Orion and Eclipse are two SOURCES for one firm, not two masters.
- `R8` -- needs a GENERAL (non-firm-attributable) plane. Every plane in this tree is inflection firm data.
- `R15` -- needs a source served RAW and separately consumed by a derived plane. No raw-serve route is named.
- `R21` -- `CN_SEVEN_RULES.json` marks it `reachable_today: false` estate-wide (`LGIC_CANON-S4`): a tree reaches
  it only by carrying the VIOLATION, and this tree's non-tier prefixes are backups and a probe, which is R17's
  territory. **A printed NOT REACHED is a result, not an omission** -- this partition is the answer, not a gap.

### 2b. Judge E, separately -- the MDPF tree

```
REACHED     (2 of 7): R14, R19
NOT REACHED (5 of 7): R3, R8, R15, R17, R21
```

E's per-plane reach column: P1 `R14`; P2 `none of the seven`; P3 `R19`; P4 `R19`; P5 `R19`; P6 `R14, R19`; P7 `R14`.

### 2c. The union across all three judges, and what the difference measures

```
UNION C + D + E   REACHED     (3 of 7): R14, R17, R19
UNION C + D + E   NOT REACHED (4 of 7): R3, R8, R15, R21
```

**The one rule the two trees differ on is R17**, reached by the INFLECTION tree (4 backup/scratch/probe
prefixes inside a tier bucket, planes 9-12) and not by the MDPF tree. That single rule is the measured
delta A-13's second-tree choice bought: the new tree adds R17 and nothing else over round 1's. It does not
move R3, R8, R15 or R21, which stay NOT REACHED across both trees and all five judgings in this project.

---

## 3. THE ARM'S ANSWER

### 3a. The comparison the arm was designed for -- E against round 1's A and B, same tree, same planes

Round 1's judges A and B emitted ONE verdict per axis for the whole tree; E emitted one per plane per axis.
To compare them at all, E's 7 planes must be rolled up per axis. **The roll-up rule is the canon's own
(`02_DOCTRINE.md:130`, "the most severe verdict"), it is THIS COMPARER's instrument, and judge E never
printed a tree-level verdict of any kind.** That disclosure is load-bearing; see 3c.

| axis | judge A (r1, had the scale) | judge B (r1, had the scale) | judge E rolled up (no scale in its brief) | match? |
|---|---|---|---|---|
| A1 | UNDETERMINED | UNDETERMINED | UNDETERMINED (6 UNDETERMINED, 1 DECLARED-EXCEPTION) | YES |
| A2 | VIOLATES | VIOLATES | VIOLATES (4 VIOLATES, 2 CONFORMS, 1 DECLARED-EXCEPTION) | YES |
| A3 | VIOLATES | VIOLATES | VIOLATES (2 VIOLATES, 5 UNDETERMINED) | YES |
| A4 | UNDETERMINED | UNDETERMINED | UNDETERMINED (7 UNDETERMINED) | YES |
| A5 | VIOLATES | VIOLATES | VIOLATES (2 VIOLATES, 4 UNDETERMINED, 1 CONFORMS) | YES |

**5 of 5. E does NOT diverge from the with-scale judges on the tree all three judged.** And the agreement is
not only in the labels -- it is in the same facts, plane by plane:

- the Orion JWT read is register X1 and reads DECLARED-EXCEPTION for A judge, B judge and E alike (E on P1);
- P1's bronze in `opal-data-mdpf` is an A2 violation of R4 for all three;
- P4 and P5 gold in `opal-data-assets` is an A2 violation of R5 and an A5 violation of R11 for all three;
- P6's cottonwood and inflection platinum slices violate R6/R7 while X7 covers only 49financial's, for all three;
- P7's `global/` is the R7 cross-firm-composite branch under register X2 for all three;
- P2's code home CONFORMS under R16 for all three;
- A4 is UNDETERMINED for all three, on R13's deferred heavy threshold.

### 3b. E against C and D, at the only grain that population supports

No shared plane exists (section 0), so no per-plane divergence can be computed and none is claimed here.
What IS comparable:

- **Vocabulary.** E used 4 distinct verdict values (`CONFORMS`, `DECLARED-EXCEPTION`, `UNDETERMINED`,
  `VIOLATES`); C used 3 and D used 3 (neither used `DECLARED-EXCEPTION`; no judge used `DEPARTS-RECOMMENDED`).
  **4 of 4 of E's values occur whole-word in the canon E read** -- `check_canon_r2.py j7-e-vocab`, denominator
  4, absent 0. E, with no severity brief, produced a value C and D did not use at all, and got it from
  `02_DOCTRINE.md:106-115`, where the closed five-value vocabulary lives.
- **Discipline.** All three refuse to guess at a closely similar rate: E 22 UNDETERMINED of 35 axis cells
  (62.9 percent), C 35 of 65 (53.8 percent), D 35 of 65 (53.8 percent). All three
  cite a rule id on every row (`j4-cites`, `j5-cites`, `j6-cites` all PASS). All three reach for the register
  (X1/X2/X7 in E; R20 in C's and D's reasoning) rather than reading a declared departure as a violation.

### 3c. WHAT THIS DOES AND DOES NOT ESTABLISH -- the answer stated with its limit

**The finding, in the cell's own terms: E's verdicts do NOT diverge in the way the severity order would
predict.** On the reading section 3a supports, round 1's five-of-five agreement was agreement on facts a
judge can reach from the canon and the tree, and the CVO's `C-S9` worry -- that the agreement came from a
shared scale the canon did not carry -- is NOT what the evidence shows, on this tree.

⛔ **AND THE NO-DIVERGENCE RESULT IS WEAKER THAN IT LOOKS. THREE MEASURED REASONS, EACH OF WHICH A READER
MUST HAVE BEFORE USING THE SENTENCE ABOVE:**

1. **The canon E read CARRIES the withheld scale, verbatim.** `infra/logic/02_DOCTRINE.md:105-130` (v1.1,
   landed by `CN-k-2` THIS ROUND) holds the five-value vocabulary, the severity order
   `CONFORMS < DECLARED-EXCEPTION < DEPARTS-RECOMMENDED < UNDETERMINED < VIOLATES`, both non-obvious
   placements, and the most-severe roll-up rule -- the same content as `CN_SEVERITY.md`, which is the file
   withheld from E. This is the DESIGN and E's order says so (RULING R-8, `LGIC_CANON-S6`: *"WHAT IS
   WITHHELD FROM YOU IS A BRIEF, NOT THE CANON"*). **So the arm tests "does the CANON supply the scale",
   and CANNOT test "would a judge with NO scale agree" -- that experiment is no longer available in this
   estate, because the scale is now in the canon.** A reader who takes 3a as the second answer reads a
   question that was not asked.
2. **Neither arm ever exercised the ORDER.** Whole-word census over the three round-2 judge files for
   `severity | most severe | more severe | less severe`: **judge C 0, judge D 0, judge E 0.** The same census
   over round 1: **judge A 1 (*"less severe than UNDETERMINED"*), judge B 2 (*"the more severe finding"*,
   *"the most severe finding"*).** Round 1's judges had to RANK because their output grain was one verdict per
   axis for a whole tree; round 2 changed the grain to one verdict per plane per axis, which never forces a
   roll-up, so **C and D, who HELD the severity brief, used it exactly as much as E, who did not: not at all.**
   The arm's own file claims it is *"the only thing that separates the two arms"*; measured on the outputs,
   it separated nothing observable. Filed as `LGIC_CANON-W7-S5`.
3. **The roll-up in 3a is insensitive, and here is by how much.** Because `max()` over 7 planes is decided by
   the single most severe cell, E's rolled-up axis verdict would survive a large number of per-plane changes:
   A3 and A5 would each need **2** plane-verdicts flipped to move; A2 needs **4**; A1 needs **6** and A4 needs
   **7** (every plane). So the 5-of-5 match tolerates up to two independent reading errors on three of the
   five axes without showing any divergence at all. **It is a weak discriminator and it is the one this cell
   has**, because E's output carries no tree-level verdict of its own.

**The honest summary for L9:** the canon decided these planes the same way for a judge holding the severity
brief and for a judge holding only the canon (5 of 5 on the shared tree, and the same rules and registers
underneath). That answers `C-S9` for the CLASSIFICATION vocabulary and it does NOT answer it for the
ORDER -- nothing in round 2's output grain ever required a judge to rank two verdicts against each other, so
the ranking was not tested by either arm. If the ORDER is to be tested, the cell that tests it must ask a
judge for a per-plane or per-tree ROLL-UP, which no round-2 cell did.

---

## 4. Provenance -- what was run, and with what result

```
timeout 120 python .../fixed_inputs/r2/check_canon_r2.py j7-blind     -> PASS-J7-JUDGES-MUTUALLY-BLIND    (6 pairs, 0 leaks)
timeout 120 python .../fixed_inputs/r2/check_canon_r2.py j7-e-vocab   -> PASS-J7-E-VOCAB-FROM-CANON       (denominator 4, absent 0)
timeout 120 python .../fixed_inputs/r2/check_canon_r2.py j4-reach     -> PASS-J4-REACH-PRINTED            (3 of 7)
timeout 120 python .../fixed_inputs/r2/check_canon_r2.py j5-reach     -> PASS-J5-REACH-PRINTED            (3 of 7, DISCLOSED line)
timeout 120 python .../fixed_inputs/r2/check_canon_r2.py k2-severity  -> PASS-K2-SEVERITY-ORDERED         (5 of 5 placed)
timeout 120 python .../fixed_inputs/r2/check_canon_r2.py k2-vocab     -> PASS-K2-VOCAB-CARRIED            (5 of 5 present)
```

The 65-cell matrix, the 6 disagreements, E's roll-up and the three reach partitions were computed from the
TSVs by a scratch script in this worktree's `.scratch/` (not committed; its inputs are the three committed
TSVs and its outputs are printed in full above, so every number here is re-derivable from the files named).

**Rows filed by this cell:** `LGIC_CANON-W7-S4` (the tree mismatch in the comparison the cell text names),
`LGIC_CANON-W7-S5` (the severity brief separated nothing observable in either arm). Both OBSERVATION, both
INERT, both `UNDER_INVESTIGATION`.
