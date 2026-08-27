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
workflows/atom_decomposition/runs/d1-catviews/20260824T195537Z/DECOMP.md — stage-3 decomp for
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
| `TL2DS-AC6` | ⛔⛔ **`D1-h-r3` CARRIES **FOUR** CLAIMS, NOT TWO — `3.0.0_SA_CVO~Z`'s ruling, which read the cell AT SOURCE and found that both my quote and `1.0.0_SA_CTO~Z`'s stopped at *"his four, verbatim"*, i.e. **before the two that EXECUTE.** <br>`A` **MEASUREMENT** (L1 set on 08-24) → **PRESERVE verbatim + vintage stamp + supersession note.** <br>`B` **DERIVATION** (`L1 = members carrying a strategy_id`) → **STRIKE.** <br>`C` **BEHAVIOUR** (*"…carry NO L1 node UNTIL A STRATEGY IS REGISTERED"*) → **STRIKE. A postulate-(iv) trap stated as a PROMISE** — it says registering a strategy for `idvz` *gains* it an L1 node, which the new tree makes flatly wrong. <br>`D` **ORACLE** (`[m for m in members_for('SMA') if m.strategy_id] == 4 …`) → **STRIKE. It is RUNNABLE**, so it is the claim most likely to be re-executed by someone checking their work. <br>⛔ **A commit that edits `A`'s text, or that date-stamps `B`/`C`/`D` and leaves any standing, FAILS.** | `D1-h-r3` | |
| `TL2DS-AC7` | ⛔⛔ **THE STRIKE HAS *SEVEN* SITES, NOT FIVE — AMENDED 21:3xZ. TWO ARE IN THE PORTAL SUBMODULE AND ONE OF THEM CITES `D1-h-r3` BY NAME.** Each of the seven is amended or explicitly dispositioned with a reason: <br>**RECORDS** — `1` `DECOMP.md:103` (the cell) · `2` `DECOMP.md:170` **vouches for it** (*"`D1-h-r3` … UNAFFECTED and, by his word, LOAD-BEARING"*) · `3` `TO-R1-DS:107` AC2 · `4` `TO-F3-DS` `D1F3DS-AC3` — ⭐ **ALREADY DISPOSITIONED BY THE ISSUER: NO RE-POINT, NO EDIT.** It consumed the cell's **membership** half (`resolve_any('opal_div_sma') → divz`), not the struck **level/derivation** half, so it is invariant to the restructure. **Do not touch it.** <br>**CODE** — `5` `mdpf_category_registry.py:906-914` · `6` **`portal/src/api/endpoints/aum.ts:687`** — `/** SMA L1 node = a member carrying a strategy_id (D1-h-r3). */` <br>`7` **`portal/src/components/CategoryViewTree.tsx:188` and `:245`** — ⛔⛔ **CORRECTED 21:3xZ, AND THE ISSUER'S FIRST WORDING WAS WRONG: THE CODE IS DATA-DRIVEN AND CORRECT. DO NOT "FIX" IT.** I wrote that these were *"deliberate withholdings"* and that *"the render is withholding a bar."* **Read at source by `0.4.0_DS_ClientPlatform~Z`, that is false:** `:189` `const hasAmounts = rows.some(r => r.aum !== null && r.aum !== undefined)` is computed **FROM THE ROWS**, and `:243`'s ternary branches on `r.aum`. **NOTHING HARDCODES "no AUM."** <br>>> **THE COMMENTS ASSERT THE STRUCK PREMISE; THE CODE DOES NOT IMPLEMENT IT.** The behaviour is **LATENT, NOT WITHHELD** — it activates on its own the moment `sma_member_aum` (`mdpf_gold_consolidator.py:579, 596-597`) reaches the client block. **STRIKE THE COMMENTS; CHANGE NO BRANCHING.** << <br>⭐ **AND `:245` SPLITS THE SAME WAY `D1-h-r3` DID — `AC6`'s shape one layer down:** *PREMISE* (*"SMA L1 carries a strategy id and NO amount"*) → **STALE, struck**; *REASONING* (*"rendering $0 would say 'this firm holds none of it' about a firm holding millions"*) → ⛔ **SOUND, AND IT MUST SURVIVE.** A `$0` for an absent value is still a lie about a firm holding millions. **Preserve the reasoning, strike the premise it hangs on.** <br>⚠ **The issuer read the COMMENTS and asserted what the CODE does** — the `[DOC]` band's standing warning (*prose DESCRIBES the code and may be STALE*), earned. <br>⭐ **INSTRUMENT NOTE, and it is the reusable part:** `comp-find 'D1-h-r3' --files --all` returns **SURFACED=2** (23 hits / 27,290 files) — sweeping the **CITATION** answers *"what depends on this cell"* directly, where sweeping the phrase `"SMA L1"` returns a 16-file candidate set needing classification. **Sweep the citation, not the topic.** <br>⚠ **BOUND: THE CODE IS CORRECT TODAY.** Under the old tree the four *are* the L1 nodes — not a live defect, **this restructure's work.** ⚠ **Portal vintage is submodule HEAD `dd80c624` (this box), NOT verified against `origin/DEV`** — resolve the vintage before claiming anything about served bytes. <br>⛔ **`un_noded_members` (`:914`) NEEDS AN EXPLICIT DISPOSITION — dissolved, retained-as-empty, or removed.** Under ETF/ALT `idvz`/`pfde` may **get homes and the concept dissolve**, while a consumer reading it today gets `[idvz, pfde]`. **Silence ships a field whose meaning changed underneath its readers.** | `D1-h-r3` | |
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
⛔⛔ **ANDREW-DIRECT ~21:3xZ — TWO STANDING RULES, ADDED AFTER ISSUE, BOTH LANDING ON THIS TO. VERBATIM:**
> *"Yeah all of these should be based on if there is data to populate and theyre invisible otherwise.
> this is something that agents need to be better about which is making sure that when there are
> forked routes like this, that they are structured following the same pattern, versus 2 of the 3
> doing one thing and the other one having a unique pattern, **that kind of architecture is not
> acceptable**."*

**(1) DATA-DRIVEN VISIBILITY — it CONFIRMS the code and CONDEMNS the comments.**
`CategoryViewTree.tsx:243` already branches on `r.aum`. ⭐ **His rule is what that code does** — which
is the second independent confirmation that `AC7`'s "strike the comments, change no branching" is
right. **INVISIBLE — not `$0`, not a placeholder.** ⚠ **And it vindicates the `:245` REASONING** this
TO told you to preserve (*"rendering $0 would say 'this firm holds none of it'"*) while its PREMISE is
struck: **he has now stated the rule that reasoning was reaching for.**

**(2) FORKED ROUTES FOLLOW THE SAME PATTERN — this is the whole point of the restructure.**
```
Models  L0 -> {Primary, Custom}                    -> members
SMAs    L0 -> {ETF Strategies, ALT Strategies}     -> members   <- the change
Client  L0 -> {Opal Supervised, Opal Unsupervised} -> members
```
>> ⛔ **"2 OF THE 3 DOING ONE THING AND THE OTHER ONE HAVING A UNIQUE PATTERN" IS EXACTLY THE SHAPE
   THIS TO EXISTS TO REMOVE — and it is now a SOVEREIGN PROHIBITION, not a preference.** <<

⛔⛔ **SUPERSEDED 21:4xZ — `AC1` IS UNBLOCKED BY SOVEREIGN ANSWER, NOT BY THE INFERENCE BELOW.**
**ANDREW-DIRECT: *"yes approve all recs"*, over `/open-calls` CALL 1 —**
```
CALL 1   are idvz/pfde inside "ETF Strategies"?   REC (a) YES   -> APPROVED
```
>> **`idvz` AND `pfde` ARE INSIDE "ETF Strategies". THE TREE IS MECE OVER SMA MEMBERS AND THE Rule 24
   RECORD IS NOW WRITABLE. `TL2DS-AC1` IS RESUMED — this paragraph is the LIFT, issued by the office
   that placed the hold.** <<
⚠ **AND `un_noded_members` FOLLOWS FROM IT (`AC7`):** with both members homed, the concept has no
remaining occupants — **that makes DISSOLVED the indicated disposition, but `AC7` still requires the
disposition to be STATED and justified, not inherited from this line.**

⭐ **WHAT THE PRIOR TEXT SAID, PRESERVED BECAUSE IT WAS THE RIGHT CALL AT THE TIME:** I had argued
that leaving them un-noded would give SMA a structural feature Models and Client lack — a unique
pattern in 1 of 3 forked routes, against his ~21:3xZ rule — **and I explicitly refused to resume the
criterion on it, writing "DO NOT RESUME ON THIS PARAGRAPH."** The inference pointed the same way the
sovereign answer landed. ⛔ **THAT IS NOT VINDICATION AND MUST NOT BE READ AS ANY.** A correct guess
held as an argument is worth exactly what it was worth before the answer arrived: nothing, until he
spoke. **`0.4.0_DS_ClientPlatform~Z` was right to hold, and the hold cost this project nothing.**

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
  <criterion id="TL2DS-AC7" cell_refs="D1-h-r3"/>
  <expected_criteria>TL2DS-AC1,TL2DS-AC2,TL2DS-AC3,TL2DS-AC4,TL2DS-AC5,TL2DS-AC6,TL2DS-AC7</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D1_CATVIEWS.TO-L2-DS_PROOF_OF_SPEC.json</instance_path>
  <!-- ⛔ CORRECTED 22:0xZ BY THE ISSUER, BEFORE THE INSTANCE WAS FILED. The declared path was
       `.../0.4.0_DS_ClientPlatform~Z/deliverables/` — A DIRECTORY THAT DOES NOT EXIST. Measured:
       ~A ~B ~F ~G ~H ~I ~J ~K all exist; `~Z` does NOT, and `0.4.0_DS_ClientPlatform~Z` has been
       committing this TO's artifacts to the BASE dir (TL2DS-AC1_RULE24_RECORD.md @41a52a8459,
       TL2DS-AC7_SITE_LEDGER.md), which is the known site-Z owned-paths gap: flat `~Z` lane paths
       are UNDEFINED to safe-commit, so the suffixed dir is not reliably writable here.
       CONTROL: `0.7.0_AE_CloudOps~Y/deliverables/` DOES exist and holds TO-3-AE's instance — so the
       suffixed convention is sound generally and the defect is specific to `~Z`.
       THIS IS THE THIRD TIME TONIGHT A MACHINE-READABLE FIELD IN ONE OF MY TOs WOULD HAVE FAILED A
       COMPLIANT EXECUTOR (markdown backticks in <decomp_ref>; a five-site count that was seven;
       this path). Caught BEFORE filing this time rather than after a red proof-of-spec. -->
  <instance_path_note>If the executing lane CAN write `org/tier2_senior/0.4.0_DS_ClientPlatform~Z/deliverables/`, that is the preferred location and the issuer will re-point on request. The base path is declared because it is where this lane's artifacts for this TO measurably are.</instance_path_note>
  <alignment_denominators>cells declared: 4 (`D1-h-r3`, `D1-inv-1`, `D1-inv-2`, `D1-inv-4`); criteria: 7 (**5 -> 6 on `1.0.0_SA_CTO~Z`'s two-defect ruling, 6 -> 7 on `3.0.0_SA_CVO~Z`'s four-claims/five-sites ruling. The denominator moved IN THE SAME EDIT BOTH TIMES rather than being inherited** — this line was wrong twice on the sibling POSN_TENANCY decomp today and I am not trusting arithmetic on it). FORWARD — 7 of 7 criteria carry >=1 cell_ref. BACKWARD — 4 of 4 declared cells reachable from >=1 criterion (`D1-h-r3` from AC1+AC2, `D1-inv-2` from AC3, `D1-inv-4` from AC4, `D1-inv-1` from AC5). Unmapped 0; untraceable 0. *(The D1 decomp's remaining cells are NOT this TO's: the Client-L1 family (`D1-k-*`), the channel-enumeration family (`D1-i-*`) and the render/consumer cells (`D1-c-*`) are untouched by the SMA-tree restructure and are deliberately out of scope.)*</alignment_denominators>
  <criterion_status_note>⛔ AC3 exists because the producer comment ALREADY asserts the property it tests (*"this cannot move a served total"*). **An author's assertion and a measurement are different objects, and the whole point of scope B being "invariant across the fork" is a claim that must be exercised rather than quoted.** A PASS on AC3 citing the comment is not a PASS.</criterion_status_note>
</proof_of_spec>
</task_order>
