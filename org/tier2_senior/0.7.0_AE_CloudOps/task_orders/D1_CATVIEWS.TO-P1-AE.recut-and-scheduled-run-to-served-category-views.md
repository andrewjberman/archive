<task_order>
<id>D1_CATVIEWS.TO-P1-AE.recut-and-scheduled-run-to-served-category-views</id>
<title>PIPE THE ASSET CATEGORIES DATA: cited-literal re-cut at a valid pin, then a SCHEDULED run that actually emits category_views to the served plane</title>
<project>D1_CATVIEWS</project>
<directive>D1</directive>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps~Z</issued_to>
<issued_at>2026-08-27T22:4xZ</issued_at>
<status>ACTIVE</status>

<decomp_ref>
workflows/atom_decomposition/runs/d1-catviews/20260824T195537Z/DECOMP.md — stage-3 decomp for
D1_CATVIEWS, round 1 CERTIFIED. **Cells this TO discharges: D1-inv-2, D1-inv-3, D1-inv-4.**
</decomp_ref>

<basis>
**ANDREW-DIRECT ~22:4xZ:** *"we still havent gotten data flowing to the Asset Categories panel,
theyre just using mock numbers from DE, which is fine because theyre only on DEV Branch, but we need
to figure that out, what agent is tasked with piping that data?"*

⛔ **THE MEASURED ANSWER WAS: NOBODY. THIS TO IS THAT ANSWER BEING FIXED.**
```
category_views SERVED         opal-data-portal-v2  0 keys containing 'category'
                              opal-data-cot        0 keys containing 'category'
PRODUCER CODE                 EXISTS AND IS BUILT --
                              mdpf_category_registry.py:844  build_category_views(...)
                              mdpf_gold_consolidator.py:537  _shape_category_views(...)
OPEN D1_CATVIEWS TOs          ONE -- TO-I1-DS (channel enumeration, NOT production),
                              held by 0.4.0_DS_ClientPlatform~T, not a live seat
```
**The code is built. The artifact has never existed. No TO covered producing it.**

⚠ **WHY THE GAP PERSISTED, stated plainly because it is this office's miss:** the COO NO-SHIP ruling
`@0d08954d4c` (~19:3xZ) named exactly this work and said *"the path runs through an AE-class re-cut,
and **there is no AE seat**."* **That was true when written and stopped being true at ~21:0xZ when
AE seats came online. Nobody re-cut it.** This TO is ~90 minutes late.
</basis>

<the_interlock>
⛔ **THIS IS NOT A DEADLOCK AND MUST NOT BE READ AS ONE.** The build refuses at the **default pin**
because PACKAGE names `mdpf_category_registry`, which **does not exist at `bf74d031c1` (2026-08-10)** —
that pin **predates the module's birth at `be05d938af` (2026-08-19)**. **That refusal is the interlock
working, not a breakage.**
**The sanctioned shape is a CITED-LITERAL RE-CUT at a pin that CONTAINS the module** —
`build_package.py` names the **`4e0410825e` precedent**. **AE-class, which is why it is yours.**

⛔⛔ **THE `D1_CATVIEWS` NO-SHIP STANDS AND THIS TO DOES NOT LIFT IT.** `build_package.py:266` names
**"a COO/Andrew ship ruling"** as what lifts it. **This TO produces the EVIDENCE that would justify a
lift; it does not perform one, and completing it is not an argument that the pin may advance.**
**No pin advance, no promote, no PROD anything.**
</the_interlock>

<cells>

| cell | what this TO owes it |
|---|---|
| `D1-inv-2` | **GOLD-plane: the five top-level peers SUM TO `total_aua`, per firm** — **measured ON THE SERVED ARTIFACT**, not in a test harness, **denominator printed**. |
| `D1-inv-4` | **VIEW-plane: rendered L0 values sum to `total_aua − Insurance`, AND every L1 set sums to its L0 parent** — on the served output. ⛔ **`0.4.0_DS_ClientPlatform~Z` measured this invariant TRUE BUT UNENFORCED** (perturbing an L1 bucket by +5.00 raises nothing, in SMAs *and* Models). **You are verifying a value that NOTHING GUARDS — say so in the deliverable.** |
| `D1-inv-3` | **Legacy `non_model` fields BYTE-UNCHANGED** — the regression direction that announces nothing if it breaks. |

</cells>

<acceptance_criteria>

| id | criterion | cell_refs | status |
|---|---|---|---|
| `TP1AE-AC1` | **`category_views` EXISTS ON THE SERVED PLANE for at least one firm**, emitted by a **SCHEDULED** producer run. **Key, bucket, byte size and `LastModified` (UTC, `s3api`) recorded.** ⛔ **An ad-hoc run is PERMITTED FOR QA and is NEVER the acceptance** — *"ad-hoc artifacts are never production evidence"*, and *"success-of-upstream as the only trigger is a defect."* **The SCHEDULED fire is the acceptance.** | `D1-inv-2` | |
| `TP1AE-AC2` | **`D1-inv-2` holds ON THE SERVED ARTIFACT** — five gold-plane peers sum to `total_aua`, per firm, **denominator printed, measured on the fetched bytes.** | `D1-inv-2` | |
| `TP1AE-AC3` | **`D1-inv-4` holds on the served output** — L0 values sum to `total_aua − Insurance`, and **every L1 set sums to its L0 parent, with member counts exhibited.** ⚠ **An L1 set that sums because it is EMPTY is not a pass.** ⛔ **Report that the invariant is UNENFORCED** (measured by `0.4.0_DS_ClientPlatform~Z`) — **a passing value behind no guard is a different state from a guarded one.** | `D1-inv-4` | |
| `TP1AE-AC4` | **`D1-inv-3` byte-unchanged** — legacy `non_model` fields identical before/after, **by hash or ETag**, not by inspection. | `D1-inv-3` | |
| `TP1AE-AC5` | ⛔ **The `ViewPlaneError` path EXERCISED at least once AGAINST A REAL MISMATCH** and shown to refuse. **Its FIRST real exercise must not be a client-facing producer run** — that is the specific hazard the NO-SHIP ruling named: a five-peer invariant that raises on mismatch can **abort a client-facing producer**. | `D1-inv-2` | |
| `TP1AE-AC6` | ⛔ **DESIRED ≠ APPLIED ≠ EXERCISED on every claim**, and **the re-cut pin is cited by CONTENT** (`git show <pin>:<file>` + a negative control), **never by `merge-base --is-ancestor`** — a cherry-picked or ephemeral pin resolves only by content. **No `.tf` cited as evidence of force.** | `D1-inv-2` `D1-inv-3` | |

</acceptance_criteria>

<reporting>
Deliverable + proof instance in this lane's own `deliverables/`, committed via
`.tools/safe-commit.sh --author "0.7.0_AE_CloudOps~Z <0.7.0_AE_CloudOps~Z@opal.agent>" -F <msgfile>`,
message file written by a **non-shell writer**, never a heredoc.
**Push state MEASURED** with a control, **or the words "push state UNMEASURED"**.
⛔ **`cell_status` per cell from OBSERVED states only — put the block in the `.md` MEASUREMENT RECORD,
NOT the proof instance:** `PROOF_OF_SPEC.schema.json` is `additionalProperties:false` and has no slot
for it. **Do not synthesize cell states from criterion verdicts.**
⛔ **NEVER bare `terraform apply` — use `safe-apply`.** No `aws lambda update-function-code`.
⚠ **`aws s3 ls` renders LOCAL time; `s3api` renders UTC** — name which produced any timestamp.
</reporting>

<standing>
· **Surprise channel:** anything odd that is not this task -> one line to `3.0.0_SA_CVO`, cc the
  issuer (`2.0.0_SA_COO~Z`), **and KEEP WORKING.**
· **No new alert/alarm/monitor** — standing moratorium. **No shadow or build-alongside pipeline,
  no duplicate output path, no standing parity comparator** — Andrew complete veto.
· ⚠ **The panel currently renders MOCK numbers from DE on DEV.** ⛔ **Do NOT treat the mock as a
  contract or reconcile the real output to it** — if served output disagrees with the mock, **the
  mock is wrong**, and that is a finding for `0.4.0_DE_ClientPlatform~Z`, not a defect to fix here.
· ⛔⛔ **AND AGREEMENT WITH THE MOCK IS ALSO WORTHLESS — `0.4.0_DE_ClientPlatform~Z` DISCLOSED THIS
  AGAINST THEIR OWN ARTIFACT, UNPROMPTED.** The smoke fixture (portal `@20373baa`) is **NOT an
  independent description of the expected block: it was DERIVED FROM `mdpf_category_registry.py`.**
  >> **SO IF THE SERVED ARTIFACT MATCHES THE FIXTURE, THAT IS NOT TWO SOURCES AGREEING — IT IS THE
     PRODUCER AGREEING WITH A RESTATEMENT OF ITSELF.** ⛔ **Do NOT cite fixture agreement as
     corroboration in any criterion.** Same author, one rung, counted twice. <<
  ⭐ **WHAT THE FIXTURE IS LEGITIMATELY GOOD FOR — a SHAPE CHECKLIST, and use it only that way:**
  children with **both** buckets emitted for every firm · **ETF 4 members / ALT 2** · `l1_nodes` and
  `un_noded_members` **ABSENT**.
  ⚠ **TWO PLACES THE FIXTURE IS KNOWINGLY AHEAD OF THE PRODUCER — A MISMATCH THERE IS EXPECTED AND IS
  NOT A DEFECT IN THE SERVED ARTIFACT:** (1) **per-member `aum`** — `_members()` does not emit it
  (`registry:900-903`), and the fixture carries **invented** values because Andrew ~22:3xZ asked the
  drilldowns to show amounts; (2) **EVERY MAGNITUDE is invented** — *"the $4.00M is not cottonwood's
  DIVZ AUM."* ⛔ **Do not report either as a producer defect.**
  ⭐ **`0.4.0_DE_ClientPlatform~Z` re-derives the fixture against the served artifact once one exists,
  and reports disagreement as a DE finding. Nothing is owed to that lane by this TO.**
· **No gate gets loosened, waived or expected-green'd.** A criterion that fires is right.
</standing>

<proof_of_spec>
  <criterion id="TP1AE-AC1" cell_refs="D1-inv-2"/>
  <criterion id="TP1AE-AC2" cell_refs="D1-inv-2"/>
  <criterion id="TP1AE-AC3" cell_refs="D1-inv-4"/>
  <criterion id="TP1AE-AC4" cell_refs="D1-inv-3"/>
  <criterion id="TP1AE-AC5" cell_refs="D1-inv-2"/>
  <criterion id="TP1AE-AC6" cell_refs="D1-inv-2,D1-inv-3"/>
  <expected_criteria>TP1AE-AC1,TP1AE-AC2,TP1AE-AC3,TP1AE-AC4,TP1AE-AC5,TP1AE-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~Z/deliverables/D1_CATVIEWS.TO-P1-AE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells declared: 3 (D1-inv-2, D1-inv-3, D1-inv-4); criteria: 6. FORWARD — 6 of 6 criteria carry >=1 cell_ref. BACKWARD — 3 of 3 declared cells reachable from >=1 criterion (D1-inv-2 from AC1+AC2+AC5+AC6, D1-inv-4 from AC3, D1-inv-3 from AC4+AC6). Unmapped 0; untraceable 0. *(The decomp's remaining cells are NOT this TO's: the Client-L1 family (D1-k-*), channel enumeration (D1-i-*, carried by TO-I1-DS), the render/consumer cells (D1-c-*) and the SMA-tree family (D1-h-r3, discharged by TO-L2-DS) are untouched by producing the served artifact.)*</alignment_denominators>
  <criterion_status_note>⛔ AC1 is the one that can be falsely passed, and the failure is cheap and invisible: an AD-HOC run produces a real artifact at a real key, and every downstream criterion then measures TRUE against it. The artifact would be genuine and the acceptance would still be wrong, because a pipeline whose only trigger is a human is not a pipeline. AC1 passes on the SCHEDULED fire or it does not pass.</criterion_status_note>
</proof_of_spec>
</task_order>
