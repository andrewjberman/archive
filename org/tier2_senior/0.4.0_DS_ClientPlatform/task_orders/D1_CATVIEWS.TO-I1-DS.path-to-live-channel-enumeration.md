<task_order>
<id>D1_CATVIEWS.TO-I1-DS.path-to-live-channel-enumeration</id>
<project>D1_CATVIEWS</project>
<directive>D1</directive>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform~T</issued_to>
<issued_at>2026-08-26T21:1xZ</issued_at>
<status>complete -- ⭐ **CERTIFIED. THE CERTIFICATE EXISTS AND IS ON ORIGIN.** `cvoZ_D1_CATVIEWS_TO_I1_DS_CERTIFICATION_20260828.md` @`82a54e1775`, verdict **CERTIFIED ON THE MERITS -- 3 PASS + 1 APPLIED-GATED**. Located 15:1xZ by `3.0.0_SA_CVO~Z`; VERIFIED at this seat by containment against `origin/SITEZ` with a SOUND negative control (`origin/CLOUD` tip NOT contained, so the test demonstrably returns NO). ⛔ **THIS FACE PREVIOUSLY READ 'awaiting certification' AND WAS STALE -- the certificate POSTDATES it and nobody updated the face.** ROOT: the face and the certificate are TWO DURABLE RECORDS OF ONE FACT WITH NO NAMED PRIMARY -- the certifier writes one and cannot write the other, the issuer owns the face and has no trigger to return, so they diverge from minute one in the direction of 'outstanding'. Corrected by `2.0.0_SA_COO~Z` as ISSUER. ⚠ **BOUND, STATED BY ITS MEASURER AND NOT PAPERED OVER: this establishes A CERTIFICATE EXISTS for the criteria as they read AT CERTIFICATION TIME. It does NOT establish that no criterion was ADDED to this face afterwards -- that needs a per-face criterion-set diff, NOT RUN.**

⚠ **THE ORIGINAL `<status>` CONTENT FOLLOWS, RESTORED VERBATIM.** `2.0.0_SA_COO~Z` replaced it wholesale at @4253643625 instead of appending, destroying evidence on seven faces (142 lines on one of them). Recovered from `4253643625^` and re-attached. **NOTHING BELOW THIS LINE IS NEW; NOTHING ABOVE IT WAS IN THE ORIGINAL.**

queued -- for `3.0.0_SA_CVO~Z` CERTIFICATION. **THE WORK IS DONE AND NO EXECUTOR ACT IS PENDING.**

**RE-FACED 2026-08-28 ~04:3xZ by `2.0.0_SA_COO~Z` (issuer), on `0.4.0_DS_ClientPlatform~T`'s report (12676).**
The re-seated lane ASSESSED the deliverable that nobody had read. **ALL FOUR CRITERION VERDICTS STAND:**
`AC1` PASS (strengthened) - `AC2` PASS - `AC3` PASS - `AC4` **APPLIED-GATED**. Three defects found, all
in SUPPORTING material, **none overturning a criterion**. Assessment:
`0.4.0_DS_ClientPlatform~T/deliverables/D1_CATVIEWS.TO-I1-DS_ASSESSMENT_OF_THE_ENUMERATION_DELIVERABLE.md`
@`123441797b`.

*** IT IS CORROBORATION, NOT REPETITION, AND THAT IS WHY IT COUNTS:*** the predecessor's instrument was
the DOWNLOADED ZIP; this seat assessed from the **BUILD-INPUT** side (`git show <ref>:build_package.py`
-> AST `literal_eval` of `PACKAGE`), which **can and did disagree**. Positive AND negative controls on
every read. **The predecessor's deliverable was NOT edited** -- the assessment is a separate artifact.

**WHAT REMAINS IS A CERTIFICATION, WHICH BELONGS TO `3.0.0_SA_CVO~Z` AND TO NO EXECUTOR.**
**Per `1.0.0_SA_CTO~Z`'s standing interim control: certify ON THE MERITS WITH THE DEFECT CITED.**
A certification must read **"3 PASS + 1 APPLIED-GATED, instance INVALID on vocabulary grounds"**, never
a bare 4/4 and never a FAIL.

**EVERYTHING BELOW STILL BINDS -- the instance is CORRECTLY invalid and must NOT be edited into validity.**

---

**ORIGINAL STATUS, PRESERVED VERBATIM:** ACTIVE — and ⛔ **THIS TO'S FILED PROOF INSTANCE DOES NOT VALIDATE. DO NOT CLOSE ON IT.**

**DISARM RECORDED 2026-08-27 ~19:1xZ by `2.0.0_SA_COO~Z`** (issuer, and the `disarm_owner` named on
`D1_CATVIEWS-S11`). Surfaced by `0.4.0_DS_ClientPlatform~Z` at close-out; **I re-ran the checker at
my own seat rather than accepting the report.**

```
proof-of-spec-check.py <instance> I1DS-AC1..AC4   ->  rc=1, 19 VIOLATIONS, INVALID
  acceptance/3/status : 'APPLIED-GATED' is not a member of the status enum
  spec_ref/group      : 'I1' is not a permitted group
  acceptance/0/method : 'artifact_enumeration_plus_head_object' is not a permitted method
  acceptance/0        : 'denominator' — REQUIRED PROPERTY, MISSING
instance: .../0.4.0_DS_ClientPlatform~T/deliverables/D1_CATVIEWS.TO-I1-DS_PROOF_OF_SPEC.json
          committed @a6c2bac919, 2026-08-26T18:27:15, by 0.4.0_DS_ClientPlatform~T
```

⛔⛔ **RETRACTED 19:2xZ — THIS PARAGRAPH BLAMED THE EXECUTOR AND THE DEFECT IS MINE, IN THIS TO.**

I originally wrote that the schema predates the filing by two days, that `APPLIED-GATED` was never in
the enum, and therefore *"the value was minted at the keyboard."* **The dating is true. The conclusion
is false, and it is an accusation against a seat that complied exactly.**

>> **THIS TO MANDATES `APPLIED-GATED`.** `:146` — *"`D1-i-2` is reported **APPLIED-GATED**"*;
   `:178` — *"**AC4's expected terminal status is APPLIED-GATED, NOT PASS.**"*
   `<issued_by>2.0.0_SA_COO</issued_by>`. **`0.4.0_DS_ClientPlatform~T` DID WHAT THIS OFFICE TOLD
   THEM TO DO.** The instance is invalid because **the TO required a status value that is not in the
   schema's enum.** The defect is in the SPEC, not the EVIDENCE. <<

⛔ **AND THE MECHANISM IS THE SHARPEST INSTANCE OF THIS SESSION'S OWN CLASS.** I ran a real
discriminator — *did the tool move under the executor?* — got a TRUE answer, and it was **an answer to
the wrong question.** The question that decided it was ***did the TO mandate it?*** — and I never
asked it, **about my own artifact.** Authorship is exactly why: I reasoned about a TO I wrote from
memory of what it said instead of reading it. Retracted by `0.4.0_DS_ClientPlatform~Z`, who checked
the thing I skipped.

⚠ **AND THE REAL FINDING IS A SCHEMA GAP WITH TWO INDEPENDENT INSTANCES TODAY.** The status enum
`[PASS, FAIL, UNCOMPUTABLE-BY-CONSTRUCTION, UNVERIFIABLE-BY-INSTRUMENT, N/A-BY-CONSTRUCTION,
UNCOMPUTABLE]` **has no value for "correctly blocked."** `0.4.0_DS_ClientPlatform~P` hit the identical
wall on TO-6 AC3 — *"authorization withheld"* — and chose `FAIL` as *"the only literally-true option."*
**Two seats, two TOs, one uncovered domain member, in the gate that ENFORCES Rule 24.** `APPLIED-GATED`
was this office's attempt to name that member; it was the right concept minted in the wrong place —
**a TO cannot extend a schema's enum by asserting a value into it.**

⛔ **THE LATENT TRIGGER, which is why this is recorded on the FACE and not only in the channel:**
this TO reads `ACTIVE`, has a filed proof instance, and its lane `~T` is **DEAD** (absent from
`liveness.json`). **The next coordinator sees "evidence filed, just needs closing" — and closing on
this instance would be closing on evidence that REFUSES.** Nothing appears to have run the checker,
because `rc=1` would have surfaced it immediately.

⚠ **`ACTIVE` IS CORRECT HERE AND THIS IS *NOT* ANOTHER UN-FLIPPED-STATUS INSTANCE.** `AC4` is
genuinely not PASS. `0.4.0_DS_ClientPlatform~Z` explicitly declined to file it as one, and they were
right — the defect is the EVIDENCE ARTIFACT, not the status.

⭐ **AND `D1-i-1`'s ORPHAN DISCHARGE STANDS — I checked before writing this, because if it had rested
on the instance an invalid instance would have taken it down too.** It does not: this TO carries
`D1-i-1` in its own `<decomp_ref>` (`:12`) and at `<criterion id="I1DS-AC1"/"AC2" cell_refs="D1-i-1">`
(`:123-124`). **The TO's FACE is the load-bearing limb; the instance was corroboration, not the
basis.** The CVO Layer-5 finding stays closed.

**NOT CLAIMED:** that `~T`'s underlying enumeration WORK is wrong. The deliverable is ~12KB and
neither `0.4.0_DS_ClientPlatform~Z` nor I assessed it. ⛔ **The evidence ARTIFACT failing validation
is a DIFFERENT OBJECT from the FINDING it carries**, and conflating them would be the error this note
exists to prevent.

**REMEDY IS NOT TAKEN AND IS NOT THIS NOTE.** The hazard is disarmed — a reader can no longer close
this on refusing evidence — and DISARMED != REMEDIATED.

⛔ **UPDATED 2026-08-28 ~03:5xZ by `2.0.0_SA_COO~Z` (issuer): THE REMEDY IS NOW HELD BY A NAMED
RULING, NOT BY AN OPEN QUESTION.** This clause previously said the decision *"follows the D4/residue
question already open at `1.0.0_SA_CTO~Z`"* — **that question has been answered and a reader chasing
it would be chasing a closed one.**

`1.0.0_SA_CTO~Z`, msg 12529: **NOBODY EDITS THE SCHEMA TONIGHT.** The vocabulary work — declaring
each vocabulary's domain and RE-DERIVING its members — happens **after D1+D4**, per Andrew's pace
instruction. ⭐ **The reasoning is that patching enum values chosen to unblock tonight's filings is
exactly how the current holes were made**, and it never depended on who owned the file (`org/standards/**`
is `ANY_EXEC`, measured with both controls — there is no ownership blocker, and its absence lifts
an OWNERSHIP gate, not the SEQUENCING one).

>> **SO THE INTERIM CONTROL IS THE END STATE FOR TONIGHT, AND IT IS DELIBERATE:** FILE THE TRUE
   VALUES, ACCEPT THE `INVALID`, and **never alter evidence to satisfy the grammar.** `AC4`'s true
   terminal status IS `APPLIED-GATED`; the schema cannot express it; **the instance is therefore
   CORRECTLY invalid and must not be edited into validity.**

⚠ **WHAT THIS DOES NOT SAY:** it does not close this TO, and it does not assess `~T`'s ~12KB
enumeration deliverable, which **remains unassessed by anyone**. Lane `~T` is DEAD — confirmed
2026-08-28 03:5xZ against `liveness.json` (`~F`, `~L`, `~Q` present; `~T` absent; last `~T` commit
`2dd3c9d7ff`, 2026-08-26). `D1-i-1`'s discharge rests on this TO's FACE, not on the
instance, and that was checked before this note was written.

⛔⛔ **CORRECTED 2026-08-28 ~03:5xZ, SIX MINUTES AFTER I COMMITTED THE OPPOSITE.** The clause here
read: *"Re-seating to assess it is an issuing decision DEFERRED with the vocabulary work, and it is
NOT on D1's critical path."* **That is wrong on the part that matters, and `1.0.0_SA_CTO~Z` (12572)
measured why.**

>> **THE SCHEMA IS NOT THIS TO'S BLOCKER. THE SEAT IS, AND IT IS THE WHOLE BLOCKER.** The interim
   control already covers the filing — FILE THE TRUE VALUES, ACCEPT THE `INVALID`, and
   `3.0.0_SA_CVO~Z` certifies **on the merits with the defect cited**, the same disposition run for
   `TO-6`/`TO-8`'s `cell_refs`. **So the vocabulary hold never touched this item and deferring the
   re-seat behind it was my error, not a ruling.**

⭐ **AND IT IS THE ONLY ITEM IN D1+D4 IN THIS CONDITION.** Every other open face is executing in a
live lane, waiting on a clock, or waiting on a disposition. **This one was waiting on a person who
does not exist.**

⭐ **SEATED 2026-08-28 ~03:53Z by `0.0.0_AB_MSTR~Z`: `0.4.0_DS_ClientPlatform~T` IS LIVE (pid 30236),
AND `<issued_to>` IS UNCHANGED AND CORRECT.** Rule 27 holds — `~L`, `~Q`, `~F` are live on other
projects and this is a fourth.

⛔ **MY SEAT ASK WAS FOR A FRESH LETTER `~Y` (msg 12577) AND `0.0.0_AB_MSTR~Z`'s CHOICE IS BETTER.**
That seat had already re-seated `~T` four minutes before my ask landed. **Re-seating a dead lane on
ITS OWN TO is CONTINUITY and needs no issuer act; seating `~Y` would have forced a re-address —
a write that only exists because I picked a new name.** The `~Y` census was sound (0/0/0/absent,
`~L` positive control) and it answered a question that did not need asking.
⭐ **It is also this office's OWN prior ruling applied back to it** — *"the letter is cosmetic and a
measured-clean pre-clearance beats a fresh name"* — and the same pattern that worked for `~L` on
`ETFS_SATELLITES.TO-5-DS` and `~Q` on `D1_NAMEDISCOVERY`, neither of which needed a re-address.
**NO `~Y` SPAWN. This TO is not re-addressed and does not need to be.**</status>

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
