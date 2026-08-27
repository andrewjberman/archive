<task_order>
<id>D1_CATVIEWS.TO-L2-DS.sma-l1l2-restructure-and-scopeb-emit-one-act</id>
<title>SMA L1/L2 restructure + scope-B emit contract as ONE act, with the Rule 24 record for the emitted value-set</title>
<project>D1_CATVIEWS</project>
<directive>D1</directive>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform~Z</issued_to>
<issued_at>2026-08-27T21:0xZ</issued_at>
<status>ACTIVE</status>

<decomp_ref>
`workflows/atom_decomposition/runs/d1-catviews/20260824T195537Z/DECOMP.md` — stage-3 decomp for
`D1_CATVIEWS`, round 1 CERTIFIED. **Cells this TO discharges: `D1-h-r3`, `D1-inv-1`, `D1-inv-2`,
`D1-inv-4`.**

⛔ **ADDED AFTER `to-decomp-ref-lint` REFUSED THE FIRST COMMIT (`@9ed1182ffb`) FOR CARRYING NO
`<decomp_ref>`.** The gate runs in **ANNOUNCE** mode, so the commit landed and nothing forced this
edit. **Complying only where a gate blocks is the exact habit this office was corrected on today** —
the refusal is the instruction, not the enforcement.

⚠ **`D1-h-r3` IS CARRIED HERE AS A FALSIFIED CELL, NOT A DISCHARGED ONE.** Andrew's ~20:5xZ word
moved the tree its measurement described. This TO restates it; **`3.0.0_SA_CVO~Z` owns whether the
restatement needs re-certification.**
</decomp_ref>

<basis>
**Andrew-direct ~19:5xZ, verbatim** (quoted at `mdpf_gold_consolidator.py:573-574 @3665049808`):
*"I do not like that SMAs have a different path with no dollars, that is not right we need to
synchronize these things."*

**Andrew-direct ~20:5xZ, verbatim:** *"DE is the correct one"* — resolving the two-terminal collision.
Governing shape, relayed by `1.0.0_SA_CTO~Z`:
```
L1 SMAs = { ETF Strategies , ALT Strategies }      <- CHANGED
  ETF Strategies -> PFOE, DIVZ, etf-based SMAs     <- the four move to L2
  ALT Strategies -> Tax, Muni
Tax = ONE strategy, NOTHING BENEATH IT             <- unchanged
"the shapes should all be the same in layout"
```
**`1.0.0_SA_CTO~Z` ruling 9902:** scope B — SMA adopts the children map; the producer half is
INVARIANT ACROSS THE FORK and is **already built** (`sma_member_aum`, `:580`, measured at source).
**The EMITTED shape is a schema act owing a Rule 24 record and was explicitly NOT changed there.**
</basis>

<one_act_fence>
⛔⛔ **THIS IS ONE ACT, NOT TWO, AND THAT IS THE WHOLE REASON THIS TO EXISTS.**

`0.4.0_DS_ClientPlatform~Z` established it and it is adopted here as the issuing rationale: with
ETF/ALT at L1 and members at L2, **SMAs become structurally identical to Models and Client** —
```
Models  L0 -> {Primary, Custom}                    -> members
SMAs    L0 -> {ETF Strategies, ALT Strategies}     -> members   <- NEW
Client  L0 -> {Opal Supervised, Opal Unsupervised} -> members
```
**That IS *"the shapes should all be the same in layout"*, and it is exactly what scope-B's
children-map already describes.** >> **A seat cutting the restructure and the emit contract as two
TOs would BUILD THE SAME SURFACE TWICE**, and the second build would land on a shape the first had
already moved. <<

⚠ **BOUNDED, and the bound is theirs, kept rather than dropped:** `build_category_views()` has **NOT**
been re-read against the new shape, and **the merge is NOT asserted to be free.** The claim is that
the two rulings describe one surface — not that implementing it is trivial. **If the merge turns out
to be two acts, that is a finding to report, not a reason to cut a second TO silently.**
</one_act_fence>

<cells>

| cell | state |
|---|---|
| `D1-h-r3` | ⛔⛔ **TWO CLAIMS WELDED INTO ONE SENTENCE, NEEDING OPPOSITE REMEDIES — `1.0.0_SA_CTO~Z` RULING, and it supersedes the looser "restate it" this TO carried at `@9ed1182ffb`.** <br>**CLAIM A (a MEASUREMENT): the L1 set on 2026-08-24 was {divz, pfoe, muni, tax}.** → **SUPERSEDED, NOT WRONG.** True at its pin. ⛔ **STAMP THE VINTAGE AND RECORD THE SUPERSESSION; PRESERVE THE ORIGINAL TEXT. Do NOT silently edit a certified measurement** — that destroys the record of what was true when the decomp was built on it. <br>⛔ **CLAIM B (a DERIVATION RULE): "L1 membership = carrying a `strategy_id`."** → **STRIKE IT. A DATE STAMP IS NOT ENOUGH.** It was never a rule — it was a **coincidence of the old tree**, holding only because `idvz`/`pfde` (`strategy_id` None) were not L1 nodes. The implication is **ONE-DIRECTIONAL**: *no-`strategy_id` ⇒ ETF* holds; *ETF ⇒ no-`strategy_id`* **FAILS on `divz` and `pfoe`** (`0.4.0_DS_ClientPlatform~Z` cross-tab, `3.0.0_SA_CVO~Z` set computation). <br>>> **THIS CELL IS THE ARTIFACT THAT WOULD WALK THIS TO'S OWN IMPLEMENTER INTO THE CROSSING-CUTS TRAP** — it states a field-derivation **as a measured fact, in a certified decomp**, and the restructure is being cut **right now**. << |
| `D1-inv-4` | **VIEW-PLANE SUM — the invariant that must SURVIVE the restructure:** rendered L0 values == `total_aua − Insurance` per firm, **AND every L1 set sums to its L0 parent.** ⛔ **The L1 set has just CHANGED MEMBERS, so this invariant is being re-pointed at new nodes — it is the single most likely thing to break silently.** |
| `D1-inv-1` | **DECLARATION == CONSUMPTION** — the registry stays the only source of membership. The restructure is a registry change, not a hardcoded tree. |
| `D1-inv-2` | **GOLD-plane five-peer sum to `total_aua`** — must be BYTE-UNCHANGED. `:578-579` is explicit that `sma_member_aum` is carried *beside* `sma_aum`, never instead of it, **"so this cannot move a served total."** That property is now a criterion. |

</cells>

<acceptance_criteria>

| id | criterion | cell_refs | status |
|---|---|---|---|
| `TL2DS-AC1` | ⛔ **The Rule 24 four-postulate record for the EMITTED value-set lands WITH the change, or there is no change** — MECE over a declared domain, same grain, intent coherence, state coherence, plus a **word-boundary token census** for any new value. Per Rule 24 a value-enum proposal without its record **is not a proposal**. | `D1-h-r3` | |
| `TL2DS-AC6` | ⛔ **`D1-h-r3` IS DISCHARGED BY TWO DIFFERENT ACTS, AND DOING EITHER ONE TWICE IS A FAILURE.** (a) **Claim A PRESERVED verbatim** with a vintage stamp and a supersession note — **the original text still readable**; (b) **Claim B STRUCK**, with the one-directional implication stated in its place. **A commit that edits Claim A's text, or that date-stamps Claim B and leaves it standing, fails this criterion** — the first destroys a certified measurement, the second leaves the crossing-cuts trap armed inside the artifact this TO's implementer reads. | `D1-h-r3` | |
| `TL2DS-AC2` | The restructure and the scope-B emit contract are delivered as **ONE** change to **ONE** surface. **If they prove separable, report that as a finding** — do not silently split. | `D1-h-r3` | |
| `TL2DS-AC3` | ⛔ **`D1-inv-2` BYTE-UNCHANGED at the gold plane** — the five-peer sum to `total_aua` must not move. Exercised with the denominator printed, **not** argued from the "carried beside, never instead" comment. **A comment is the author's claim; the sum is the measurement.** | `D1-inv-2` | |
| `TL2DS-AC4` | **`D1-inv-4` re-verified against the NEW L1 set** — every L1 bucket sums to its L0 parent with the two new buckets in place, denominator printed. ⚠ **An L1 set that sums correctly because it is EMPTY is not a pass**; exhibit the member counts. | `D1-inv-4` | |
| `TL2DS-AC5` | Membership comes from the **registry** (`D1-inv-1`), not a literal tree at a call site. ⛔ **No criterion is discharged by a RENDER or a screenshot, and none by "the commit gate passed"** — the gate reads `.py`/`.sh`/`.tf` only and is structurally silent on the portal half. | `D1-inv-1` | |

</acceptance_criteria>

<reporting>
Deliverable in this lane's own `deliverables/`, committed via
`.tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform~Z <0.4.0_DS_ClientPlatform~Z@opal.agent>" -F <msgfile>`,
message file written by a **non-shell writer**, never a heredoc.
**Push state MEASURED** with a control, **or the words "push state UNMEASURED"**.
**`cell_status` per cell from observed states only** — do not synthesize cell states from criterion
verdicts.

⚠ **`D1-h-r3`'s restatement is an AMENDMENT TO A CERTIFIED DECOMP.** Land the restatement, and
**flag it to `3.0.0_SA_CVO~Z` as a cell whose certified text the sovereign moved** — the amendment is
in scope here; **re-certification is the certifier's call, not this lane's and not this office's.**
</reporting>

<standing>
· **Surprise channel:** anything odd that is not this task -> one line to `3.0.0_SA_CVO`, cc the
  issuer (`2.0.0_SA_COO~Z`), **and KEEP WORKING.**
· ⛔ **THE `D1_CATVIEWS` NO-SHIP STANDS** (`build_package.py:266`; COO ruling `@0d08954d4c`). **This TO
  does NOT lift it and must not be read as lifting it.** No re-pin, no `safe-apply`, no pin advance.
· **No new alert/alarm/monitor** — standing moratorium.
· **No gate gets loosened, waived or expected-green'd.** A criterion that fires is right.
</standing>

<proof_of_spec>
  <criterion id="TL2DS-AC1" cell_refs="D1-h-r3"/>
  <criterion id="TL2DS-AC2" cell_refs="D1-h-r3"/>
  <criterion id="TL2DS-AC3" cell_refs="D1-inv-2"/>
  <criterion id="TL2DS-AC4" cell_refs="D1-inv-4"/>
  <criterion id="TL2DS-AC5" cell_refs="D1-inv-1"/>
  <criterion id="TL2DS-AC6" cell_refs="D1-h-r3"/>
  <expected_criteria>TL2DS-AC1,TL2DS-AC2,TL2DS-AC3,TL2DS-AC4,TL2DS-AC5,TL2DS-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~Z/deliverables/D1_CATVIEWS.TO-L2-DS_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells declared: 4 (`D1-h-r3`, `D1-inv-1`, `D1-inv-2`, `D1-inv-4`); criteria: 6 (**was 5 — `TL2DS-AC6` added with `1.0.0_SA_CTO~Z`'s two-defect ruling, and this denominator moved IN THE SAME EDIT rather than being inherited**). FORWARD — 6 of 6 criteria carry >=1 cell_ref. BACKWARD — 4 of 4 declared cells reachable from >=1 criterion (`D1-h-r3` from AC1+AC2, `D1-inv-2` from AC3, `D1-inv-4` from AC4, `D1-inv-1` from AC5). Unmapped 0; untraceable 0. *(The D1 decomp's remaining cells are NOT this TO's: the Client-L1 family (`D1-k-*`), the channel-enumeration family (`D1-i-*`) and the render/consumer cells (`D1-c-*`) are untouched by the SMA-tree restructure and are deliberately out of scope.)*</alignment_denominators>
  <criterion_status_note>⛔ AC3 exists because the producer comment ALREADY asserts the property it tests (*"this cannot move a served total"*). **An author's assertion and a measurement are different objects, and the whole point of scope B being "invariant across the fork" is a claim that must be exercised rather than quoted.** A PASS on AC3 citing the comment is not a PASS.</criterion_status_note>
</proof_of_spec>
</task_order>
