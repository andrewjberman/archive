<task_order>
<id>D1_CATVIEWS.TO-I1-DS.path-to-live-channel-enumeration</id>
<project>D1_CATVIEWS</project>
<directive>D1</directive>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform~T</issued_to>
<issued_at>2026-08-26T21:1xZ</issued_at>
<status>complete -- ⭐ **CERTIFIED. THE CERTIFICATE EXISTS AND IS ON ORIGIN.** `cvoZ_D1_CATVIEWS_TO_I1_DS_CERTIFICATION_20260828.md` @`82a54e1775`, verdict **CERTIFIED ON THE MERITS -- 3 PASS + 1 APPLIED-GATED**. Located 15:1xZ by `3.0.0_SA_CVO~Z`; VERIFIED at this seat by containment against `origin/SITEZ` with a SOUND negative control (`origin/CLOUD` tip NOT contained, so the test demonstrably returns NO). ⛔ **THIS FACE PREVIOUSLY READ 'awaiting certification' AND WAS STALE -- the certificate POSTDATES it and nobody updated the face.** ROOT: the face and the certificate are TWO DURABLE RECORDS OF ONE FACT WITH NO NAMED PRIMARY -- the certifier writes one and cannot write the other, the issuer owns the face and has no trigger to return, so they diverge from minute one in the direction of 'outstanding'. Corrected by `2.0.0_SA_COO~Z` as ISSUER. ⚠ **BOUND, STATED BY ITS MEASURER AND NOT PAPERED OVER: this establishes A CERTIFICATE EXISTS for the criteria as they read AT CERTIFICATION TIME. It does NOT establish that no criterion was ADDED to this face afterwards -- that needs a per-face criterion-set diff, NOT RUN.**</status>

<decomp_ref>
workflows/atom_decomposition/runs/d1-catviews/20260824T195537Z/DECOMP.md — surface (i), cells
`D1-i-1`, `D1-i-2`, `D1-inv-5`. 3 cells of 31.

⛔ **CERT BASIS — READ THIS BEFORE THE CELLS.** The whole-artifact v2 cert `@60d4e2f1b4` is
**SUPERSEDED BY INVALIDATION**, and `1.0.0_SA_CTO~Y`'s re-cert (73700) returns a **REFUSAL on
postulate (i)** for the artifact as it stands: five derived members are absent (A1–A5) and nine
existing cells carry superseded content (B1–B9), because the decomp predates Andrew's
Opal-definition word (PRD s.8.6a, 08-25 ~04:2xZ), the `ALL_SCOPE` flip and `CLIENT_L1_RULE`.

**THIS TO CUTS ANYWAY, ON A NARROW AND INDEPENDENTLY VERIFIED BASIS, AND THE BASIS IS THE ONLY
REASON IT IS LEGAL:** `1.0.0_SA_CTO~Y` read the (i) mechanism **at source** — `build_package.py`
assembles from an immutable pin via `git show` (`pin_bytes :230-232`) and refuses a symbolic ref;
the two channels are confirmed distinct artifacts — and certified that **`i-1` / `i-2` / `inv-5` +
`R-i1` are correctly enumerated and their oracles are the right instruments.** It further recorded
that **every A/B finding lives on the (h)/Client-L1 family, orthogonal to this surface.**
**COO ruling 73710(a): this TO cuts on that certified delta. NOTHING ELSE ON `D1_CATVIEWS` CUTS
until the absorbing amendment lands and is re-certified.**
</decomp_ref>

<no_ship_fence>
⛔ **VERBATIM, AND IT BINDS EVERY CELL BELOW.**

> **`build_package.py:266` carries a stale-pin interlock whose STATED disarm condition is that
> `mdpf_category_registry.py`'s recon line adopt `RECON_TOLERANCE`. It has NOW ADOPTED IT
> (`@4e791e1e82`, 15:16Z) — so a reader will find a build refusal whose written reason no longer
> applies and conclude the pin may advance. IT MAY NOT. `D1_CATVIEWS` IS NO-SHIP FOR MORE THAN THIS
> FINDING: this was the last blocker to the package being LOADABLE, never to it being CORRECT.
> A DISARM CONDITION BEING MET IS NOT A SHIP DECISION.** (ruled 72364 s.3)

**AND `1.0.0_SA_CTO~Y`'s addition, which is the better statement of why:** the bundled registry copy
is **pre-defect AND unreferenced**, and **a pin advance destroys both properties.**

**THE NO-SHIP LIFT IS ANDREW'S BY-NAME WORD AND NOBODY ELSE'S.** Not the issuer's, not the CTO's,
not a disarm condition's, not this TO's.
</no_ship_fence>

<cells>

### `D1-i-1` — THE TWO CODE CHANNELS, ENUMERATED — **EXECUTES NOW**
Which channel each D1-touched module reaches, and which one the scheduled floor actually executes.
**Until this is stated per module, "deployed" is ambiguous by construction.**
**Scope:** 2 channels; **19 pinned modules** in the package. **DS-class, READ ONLY.**
**Output:** per module — channel(s) reached + whether the executing path is the ZIP or the S3
channel, **printed**, with the denominator beside it.
⚠ **The decomp's own axis note says the third-route question is TESTED, NOT ASSUMED, and that this
cell is where it gets tested: if a THIRD route exists for any D1-touched module, `i-1` finds it and
the axis gains a value.** A clean two-value result is a finding only if the sweep could have
returned three.

### `D1-i-2` — THE LAMBDA RE-PIN + TF APPLY — ⛔ **APPLIED-GATED, DOES NOT EXECUTE**
`D1-b-1`'s path to live: a re-pin of the package to the commit carrying the consolidator change,
then Terraform. **AE-CLASS, NOT THIS LANE'S** (Deployment Rules 1/2/4/18: Terraform-only,
commit-before-apply, source-map entry, `safe-apply`; NEVER#6 ledger opens at start, closes at
completion).
⛔ **A RE-PIN IS A PIN ADVANCE. THE NO-SHIP FENCE FORBIDS IT TONIGHT.** This cell is cut, named and
scoped **so it cannot be lost**, and it is **APPLIED-GATED on Andrew's by-name NO-SHIP lift.**
**CONTINUATION, RECORDED SO IT SURVIVES THIS TO:** at the lift, `D1-i-2` re-seats to an **AE lane**
as its own TO. **`0.6.2_AE_PartnerETL~A` is the natural seat** — it executed the identical class
tonight (minimal-pin FILE-grain rebuild, `safe-apply`, NEVER#6 opened and closed in-session,
post-apply proof on re-downloaded running bytes) — and `0.5.0_AE_OpalETL~B` holds a prepared plan
(`D1_CATVIEWS_D1-i-2_PATH_TO_LIVE_PLAN_20260825.md`). **Seat selection is the issuer's at the lift,
not this TO's.**
**Oracle when it does run:** the deployed package's **BYTES** contain the change — Rule 22a CODE
layer, resolved through the BUILD INPUT. ⛔ **NOT `plan 0-diff`, which is true and silent about code
currency. NOT commit ancestry** — Rule 22a's ephemeral-pin clause `@4424c948f7`: a minimal pin takes
file CONTENT, so `merge-base --is-ancestor` returns a controlled, persuasive NOT-DEPLOYED while the
bytes are running. **Read content at the packaged vintage, with a negative control at the pre-fix pin.**

### `D1-inv-5` — ⛔ COMMITTING IS NOT EXECUTING — **BINDS, DOES NOT EXECUTE**
**And `safe-deploy` to the code channel is not either.** No D1 cell may report a served-output
property from a commit hash or an S3 code-channel upload; the claim is grounded on the **EXECUTING
artifact**.
**Why it is an invariant and not a caution — the decomp's own postulate (iv) record:** `safe-deploy`
advances `s3-code-channel` and leaves `lambda-zip` **exactly where it was**, because the package is
assembled from a pinned commit and refuses a symbolic ref. **A plan that says "deploy the change"
delivers one value and STRUCTURALLY CANNOT deliver the other.** That is how `D1-b-1` came to have no
path to execution.

</cells>

<acceptance_criteria>

| id | criterion | cell_refs | status |
|---|---|---|---|
| `I1DS-AC1` | Every one of the 19 pinned modules is classified by channel(s) reached, with the executing path named ZIP or S3 per module, and **the denominator printed beside the count** | `D1-i-1` | |
| `I1DS-AC2` | The **third-route question is answered by a sweep that could have returned a third value** — the method is stated, and a two-value result is reported as a measured absence, not an assumption | `D1-i-1` | |
| `I1DS-AC3` | No claim in the deliverable reports a served-output or "live" property from a commit hash or an S3 code-channel upload | `D1-inv-5` | |
| `I1DS-AC4` | `D1-i-2` is reported **APPLIED-GATED** with the NO-SHIP fence cited verbatim; **no re-pin, no `safe-apply`, no pin advance is performed or proposed as ready** | `D1-i-2` | |

</acceptance_criteria>

<reporting>
Deliverable in the executing lane's own `deliverables/`, committed via
`.tools/safe-commit.sh -F <msgfile>`. **Push state MEASURED** (`ls-remote`/ancestry against a
FETCHED ref, with a control) **or the words "push state UNMEASURED"** — LOCAL is a measured value,
never a default.
**`cell_status` per cell on this face at close-out, written ONLY from states actually observed.**
⛔ **Do NOT synthesize cell states from criterion verdicts** — 4 criteria and 3 cells are different
objects, and deriving one from the other is inference wearing the authority of a measurement. Two
seats refused exactly that tonight and both were right; if a cell was not observed, leave it empty
and say so.
</reporting>

<standing>
· **Surprise channel:** anything odd that is not this task → one line to `3.0.0_SA_CVO`, cc the
  issuer, **and KEEP WORKING.**
· **Refactoring/migration embargo (Andrew ~20:32Z):** structural defects found this week are
  **RECORDED, not chased**, unless one blocks a product from shipping correct data.
· **No gate gets loosened, waived or expected-green'd.** A criterion that fires is right.
</standing>

<proof_of_spec>
  <criterion id="I1DS-AC1" cell_refs="D1-i-1"/>
  <criterion id="I1DS-AC2" cell_refs="D1-i-1"/>
  <criterion id="I1DS-AC3" cell_refs="D1-inv-5"/>
  <criterion id="I1DS-AC4" cell_refs="D1-i-2"/>
  <expected_criteria>I1DS-AC1,I1DS-AC2,I1DS-AC3,I1DS-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~T/deliverables/D1_CATVIEWS.TO-I1-DS_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells declared: 3; criteria: 4. FORWARD — 4 of 4 criteria carry ≥1 cell_ref. BACKWARD — 3 of 3 declared cells reachable from ≥1 criterion (`D1-i-1` from AC1+AC2, `D1-i-2` from AC4, `D1-inv-5` from AC3). Unmapped 0; untraceable 0. *(The remaining 28 of the decomp's 31 are NOT this TO's and are deliberately out: they are the carried + (h) + Client-L1 family, which `1.0.0_SA_CTO~Y`'s re-cert REFUSES on postulate (i) pending the issuer's absorbing amendment. This TO's 3 cells are the surface that re-cert verified SOUND at source and declared orthogonal to every A/B finding.)*</alignment_denominators>
  <criterion_status_note>⛔ AC4's expected terminal status is APPLIED-GATED, NOT PASS. `D1-i-2` cannot execute under the NO-SHIP fence, and a PASS on AC4 would assert an apply that must not have happened. A criterion whose honest verdict is "correctly did not run" is not a failure of this TO.</criterion_status_note>
</proof_of_spec>
</task_order>
