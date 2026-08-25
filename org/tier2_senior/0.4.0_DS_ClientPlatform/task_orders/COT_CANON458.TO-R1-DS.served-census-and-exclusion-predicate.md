<task_order>
<id>COT_CANON458.TO-R1-DS.served-census-and-exclusion-predicate</id>
<project>COT_CANON458</project>
<issued_to>0.4.0_DS_ClientPlatform~I</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project COT_CANON458, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending</status>
<priority>P1 -- measurement-only, fully unblocked. Produces the denominator the canonical-458M reconciliation needs and which nothing else in flight produces.</priority>
<date>2026-08-25</date>
<references>
  <ref type="decomp">workflows/atom_decomposition/runs/cot-458m-canonical/20260825T032500Z/DECOMP.md (CVO-CERTIFIED 23/23)</ref>
  <ref type="prd">docs/architecture/COT_CANON458_PRD.md</ref>
</references>
<objective>
Surfaces (a) and (b) ONLY: census the cot served set and classify every leaf on TWO
fields (does it carry a firm total, and on WHICH of the three bases), name each
total-bearing leaf's producer by BUILD INPUT, identify derived figures; then measure
the exclusion predicate and state its retroactivity honestly. MEASUREMENT ONLY --
THE EMIT REMAINS STOPPED AND NOTHING IN THIS TO PUBLISHES OR MOVES A SERVED BYTE.
</objective>
</task_order>

# TASK ORDER — COT_CANON458.TO-R1-DS · THE SERVED CENSUS + THE EXCLUSION PREDICATE

**to:** `0.4.0_DS_ClientPlatform~I` · **issuer:** `2.0.0_SA_COO` · **cut:** 2026-08-25 ~10:0xZ
**project:** `COT_CANON458` · **ONE PROJECT, ONE INSTANCE**

<decomp_ref>
workflows/atom_decomposition/runs/cot-458m-canonical/20260825T032500Z/DECOMP.md — cells
COT-a-1, COT-a-2, COT-a-3, COT-a-4, COT-b-1, COT-b-2, COT-b-3, COT-inv-3, COT-inv-4, COT-inv-5
</decomp_ref>

<decomp_context>
⛔ **THIRTEEN OF THE DECOMP'S 23 CELLS ARE EXCLUDED FROM THIS TO, AND FOR THREE DIFFERENT REASONS. NAMED SO THE
10-vs-23 DIFFERENCE IS VISIBLE RATHER THAN LOST:**
- **`COT-c-1..4` (4) — NOT THIS PROJECT'S.** The currency condition is **owned by `ADVI_COTETL`** and is enumerated in
  the decomp as a DECLARED cross-project dependency of `COT-e-1`. **No lane seated on `COT_CANON458` executes them.**
- **`COT-d-1..2`, `COT-e-1..3`, `COT-f-1..2` (7) — BLOCKED, NOT DEFERRED.** The model-attribution layer, acceptance
  and change control all sit behind the emit, which is **STOPPED**, and behind the Cottonwood ingest gap now under
  `WSE_COTMDL.TO-R1-AE` at `0.7.0_AE_CloudOps~H`.
- **`COT-inv-1`, `COT-inv-2` (2) — NOT REACHED BY MEASUREMENT.** `inv-2` is the **NEVER#3 never-widen sign-off** on
  moving a served total ($488,460,108.95 -> $458,053,742.19). **Nothing in this TO moves a served byte, so it does not
  attach — and it is named here precisely so nobody concludes from its absence that the guard was dropped.**
</decomp_context>

<proof_of_spec>
  <!-- Positional: python .tools/proof-of-spec-check.py <instance>.json CANR1DS-AC1,CANR1DS-AC2,CANR1DS-AC3,CANR1DS-AC4,CANR1DS-AC5 ; check the rc. -->
  <criterion id="CANR1DS-AC1" cell_refs="COT-a-1"/>
  <criterion id="CANR1DS-AC2" cell_refs="COT-a-2"/>
  <criterion id="CANR1DS-AC3" cell_refs="COT-a-3, COT-a-4"/>
  <criterion id="CANR1DS-AC4" cell_refs="COT-b-1, COT-b-2, COT-b-3"/>
  <criterion id="CANR1DS-AC5" cell_refs="COT-inv-3, COT-inv-4, COT-inv-5"/>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~I/deliverables/COT_CANON458.TO-R1-DS_PROOF_OF_SPEC.json</instance_path>
  <expected_criteria>CANR1DS-AC1,CANR1DS-AC2,CANR1DS-AC3,CANR1DS-AC4,CANR1DS-AC5</expected_criteria>
  <alignment_denominators>cells in this TO: 10 (a 4 · b 3 · inv 3); criteria: 5; every criterion carries >=1 cell_ref;
every one of the 10 cells is reachable from >=1 criterion. Unmapped cells 0; untraceable criteria 0. Decomp total 23;
13 excluded for three declared reasons, all named in decomp_context.</alignment_denominators>
</proof_of_spec>

---

## ⛔ THE ONE THING TO READ BEFORE ANYTHING ELSE

**THE EMIT IS STOPPED AND STAYS STOPPED.** `0.4.0_DS_ClientPlatform~F` refused it and their reason is the strongest
thing said on this project: **if the Opal-exposure predicate missed the two largest accounts at the firm, there is no
basis to claim it caught the other 490.** Patching the two accounts Andrew happened to name **would convert a VISIBLE
systematic gap into an INVISIBLE residual one — strictly worse, because it would look reconciled.**
**NOTHING IN THIS TO PUBLISHES, EMITS, OR MOVES A SERVED BYTE.** If your work starts to require one, that is a
BLOCKING surprise, not a judgment call.

---

## ACCEPTANCE CRITERIA

| id | criterion | cells | grounding |
|---|---|---|---|
| **CANR1DS-AC1** | **CENSUS the cot served set with its DENOMINATOR PRINTED.** Authoring-time reading was `s3://opal-data-cot/platinum/` = **1,125 objects, 20 distinct leaf names** — **that is a VINTAGE, not a fact: RE-MEASURE IT and state your own count with its timestamp.** ⛔ **`aws s3 ls` renders LOCAL time with no marker while `s3api`/boto3 render UTC — pin the plane, and prove the offset on ONE object if you mix tools.** | `COT-a-1` | MEASURED |
| **CANR1DS-AC2** | ⛔ **CLASSIFY EACH LEAF ON TWO FIELDS, NEVER ONE: (i) does it carry a firm total? (ii) on WHICH BASIS?** ⛔ **THERE ARE THREE BASES AND NAMING TWO IS THE DEFECT THIS CELL EXISTS TO STOP: ALL-ASSETS · COTTONWOOD-SUPERVISED · OPAL-SUPERVISED.** `total_aua` sums peers INCLUDING `Client > Unsupervised`, so **the FIRM TOTAL — the number every other number is measured against — has itself carried an undeclared basis.** A leaf whose basis you cannot determine is reported as **UNDETERMINED**, never assigned to the likeliest one. | `COT-a-2` | MEASURED + Rule 24 |
| **CANR1DS-AC3** | For every total-bearing leaf, **name the producer that computes it — RESOLVED BY BUILD INPUT (source map / package manifest), NEVER BY FILENAME.** ⛔ *Two copies of one logical producer in two trees read CLEAN under a filename-resolved check while having silently diverged.* Then **the DERIVED-FIGURE question: which leaves carry figures derived from the total** (percentages, concentration shares, per-advisor splits, chart series) — **a derived figure moves when the total moves and is the half a census of "totals" misses.** | `COT-a-3`, `COT-a-4` | SOURCE |
| **CANR1DS-AC4** | The exclusion predicate is **BD's supervision flag applied at the same plane as the view figures** (`D_05.supervised_split.py`, live). ⛔ **STATE THE RETROACTIVITY PLAINLY: `D_05` applies TODAY'S flags across ALL history by deliberate design (CTO 63310).** That is correct for dashboard AUM and **is a property a reader must be told, not one you resolve.** `aum_unflagged` measured **$0.00** on the current vintage — **re-measure it; a zero you inherited is not a zero you observed**, and KEEP the third bucket even at zero. | `COT-b-1/2/3` | MEASURED + SOURCE |
| **CANR1DS-AC5** | ⛔ **NO new schedule, trigger, alarm, SNS, monitor, freshness-checker, shadow prefix or comparator** (standing moratorium + complete veto). ⛔ **A PREFIX IS PART OF A MEASUREMENT, NOT PART OF ITS CONTEXT — every partition/vintage claim NAMES ITS FULL PATH.** ⛔ **CLAIMS STAY AT THE GRAIN THEY WERE MEASURED AT:** a statement about one table's producer is not a statement about the tree or the firm. | `COT-inv-3/4/5` | SOURCE |

---

## WHAT WOULD MAKE THIS TO WORTHLESS EVEN IF EVERY CRITERION PASSED

**A census whose denominator you did not print, or a basis you assigned by likelihood.** The entire value of this work
is that the next person can tell **which** number they are looking at and **what population it covers.** A leaf
confidently mis-assigned to the wrong basis is worse than one marked UNDETERMINED — **it reconciles, and nobody looks
again.**

## SURPRISE CHANNEL (Rule 27)

Mid-round the spec is FROZEN. One line by MCP to `3.0.0_SA_CVO`, cc me. **You do not write `org/surprise_channel/**` —
CVO files it.** OBSERVATION never interrupts; **BLOCKING routes to me same-turn**; any **ARMED** item disarms
same-turn via a NAMED owner, and **DISARMED IS NOT REMEDIATED.**

⛔ **A NOTE ON YOUR TO LIST, MEASURED THIS HOUR:** `list_task_orders` **never validates the lane suffix** — a
fabricated lane returns the base serial's entire backlog, while a fabricated *base* correctly returns "not found".
**There is no query that returns only your lane.** THIS TO IS YOUR ASSIGNMENT IN FULL; anything else the list shows
you is not yours.
