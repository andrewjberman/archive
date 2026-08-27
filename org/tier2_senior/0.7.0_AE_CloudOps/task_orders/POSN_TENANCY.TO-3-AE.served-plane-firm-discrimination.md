<task_order>
<id>POSN_TENANCY.TO-3-AE.served-plane-firm-discrimination</id>
<title>THE SERVED PLANE: firm discrimination at the serving layer, X-Firm-Id JWT-injected, and a firm-keyed CDN cache — the access boundary itself</title>
<project>POSN_TENANCY</project>
<directive>POSN</directive>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps~Y</issued_to>
<issued_at>2026-08-27T21:2xZ</issued_at>
<status>ACTIVE</status>

<decomp_ref>
workflows/atom_decomposition/runs/posn-tenancy/20260827T200734Z/DECOMP.md — stage-3 atom decomp
v1.4, authored by 2.0.0_SA_COO~Z. **Cells this TO discharges: PT-a-1, PT-a-2, PT-a-3.**

**Certified PARTIAL by `3.0.0_SA_CVO~Z`** — 18 of 19 cells + 6 invariants CERTIFIED WITH FINDINGS at
pin `@07de844b12`. **All three cells above are in the CERTIFIED set.** Cells bind in their v1.3/v1.4
corrected wording: *a certification with findings certifies the object AS AMENDED BY ITS FINDINGS.*
</decomp_ref>

<basis>
**Andrew-direct ~21:1xZ, verbatim:** *"Bring 0.7.0_AE_CloudOps~Y online for the POSN_TENANCY"*.
Seat spawned by `0.0.0_AB_MSTR~Z` on that word.
**Andrew-direct ~19:4xZ, *"recs approved"*** (`@5f60dd944a`) settling the visibility-vs-access fork as
**(b) ACCESS** — which is why this TO exists at all: the shipped `modesFor(firm)` client gate is
**NECESSARY AND NOT SUFFICIENT**, and the missing control is **FIRM-DISCRIMINATION, NOT
AUTHENTICATION.**

⭐ **THIS TO IS THE PROJECT'S SUBSTANCE.** `1.0.0_SA_CTO~Z` ruled that round 1 staffed the
**periphery** of a multi-tenancy boundary while its **core** had no seat. These three cells are that
core.
</basis>

<inherited_do_not_reopen>
⛔ **"nobody else" IS AN ACCESS BOUNDARY.** Ruled. Do not re-ask it.
⛔ **The shipped `modesFor(firm)` gate STAYS** — it becomes one of two layers. Do not propose removing it.
⛔ **The endpoint ALREADY AUTHENTICATES** — bare → 401, invalid → a *distinct* 401, and a validated
JWT reaches the origin (`0.0.0_AB_MSTR~Z` measured **200/RS256**, two distinct 401 controls).
**Do not re-measure whether auth exists.** The gap is discrimination.
</inherited_do_not_reopen>

<cells>

| cell | statement · oracle |
|---|---|
| `PT-a-1` | **Positioning's artifact is served through `/api/scoped/`, firm-discriminated AT THE SERVING LAYER** — not filtered in the browser. **Oracle: a fetch as firm A cannot obtain firm B's bytes, EXERCISED WITH BOTH ARMS.** ⚠ **THIS CELL IS SPLIT DE+AE AND ONLY THE API/INFRA LIMB IS YOURS.** The portal limb belongs to a DE lane and is not yet seated (`TO-1-DE` is BLOCKED on a fresh DE lane). **Do not build the portal half; name the seam you leave.** |
| `PT-a-2` | ⛔ **`X-Firm-Id` IS JWT-INJECTED, NEVER CLIENT-ASSERTED.** **Oracle: a request with a FORGED/EDITED `X-Firm-Id` header is refused or ignored.** ⭐ **This is the arm that makes the whole structure non-decorative, and it is the limb R4 initially MISSED.** A client-assertable firm header means every other control here is theatre. |
| `PT-a-3` | **The CDN cache key includes firm** — a firm-A response can never be served to firm B from cache. **Oracle: two firms, same path, DISTINCT cache entries, measured AT THE EDGE.** |

</cells>

<acceptance_criteria>

| id | criterion | cell_refs | status |
|---|---|---|---|
| `T3AE-AC1` | Firm discrimination is exercised with **BOTH ARMS**: firm A obtains its own bytes (200), and **firm A attempting firm B's artifact is REFUSED** — status and body recorded for each. ⛔ **A single-arm result is not a PASS**: "A got its data" is consistent with no discrimination existing at all. | `PT-a-1` | |
| `T3AE-AC2` | ⛔ **`X-Firm-Id` FORGERY IS EXERCISED, NOT DESCRIBED.** A request carrying a client-supplied/edited `X-Firm-Id` that disagrees with the JWT is shown **refused or ignored**, with the deciding code or policy cited `file:line @ <commit-ish>`. **A configuration that merely *reads* the header from the token is not evidence — the test is what happens when a caller sends their own.** | `PT-a-2` | |
| `T3AE-AC3` | Two firms requesting the **same path** produce **DISTINCT cache entries, measured AT THE EDGE** (cache key / `Vary` / behaviour config, plus an observed response), not inferred from a distribution setting. ⚠ **`comp-routes` declares its own plane as DESIRED** — an edge claim needs an APPLIED or EXERCISED reading. | `PT-a-3` | |
| `T3AE-AC4` | ⛔ **THE BYTES, NOT THE PIXELS (`PT-inv-1`).** No criterion is discharged by a render, a screenshot, or a hidden UI element. **The shipped client gate ALREADY hides the pill while the bytes reach everyone — that is the exact defect this TO exists to close**, so a green render is affirmative evidence of nothing. | `PT-inv-1` | |
| `T3AE-AC5` | **`PT-inv-3` — `null` FIRM FAILS CLOSED**, exercised not assumed: an identity resolution failure must not widen access. **Already correct today; this TO must show it SURVIVED.** | `PT-inv-3` | |
| `T3AE-AC6` | **`PT-inv-4` — OTHER FIRMS BYTE-IDENTICAL** where they are not the subject of a change, with the denominator printed. | `PT-inv-4` | |
| `T3AE-AC7` | ⛔ **DESIRED ≠ APPLIED ≠ EXERCISED, and every claim in the deliverable names which it is.** Terraform is **DESIRED**; a live policy read is **APPLIED**; a request that got a response is **EXERCISED**. ⚠ **`PT-inv-6` was overstated in v1 for exactly this reason** — an IAM Deny was read from `.tf` and called live. **A `.tf` file is never evidence that a policy is in force.** | `PT-a-1` `PT-a-2` `PT-a-3` | |

</acceptance_criteria>

<reporting>
Deliverable in this lane's own `deliverables/`, committed via
`.tools/safe-commit.sh --author "0.7.0_AE_CloudOps~Y <0.7.0_AE_CloudOps~Y@opal.agent>" -F <msgfile>`.
Message file written by a **non-shell writer** (Write tool / python), never a heredoc.
**Push state MEASURED** with a control, **or the words "push state UNMEASURED"**.
**`cell_status` per cell from observed states ONLY** — do not synthesize cell states from criterion
verdicts.

⛔ **NEVER bare `terraform apply` — use `safe-apply`.** No `aws lambda update-function-code`
(Terraform only).
</reporting>

<standing>
⛔⛔ **ANDREW-DIRECT ~21:3xZ — A STANDING ARCHITECTURAL RULE, ADDED TO THIS TO AFTER ISSUE. VERBATIM:**
> *"this is something that agents need to be better about which is making sure that when there are
> forked routes like this, that they are structured following the same pattern, versus 2 of the 3
> doing one thing and the other one having a unique pattern, **that kind of architecture is not
> acceptable**."*

>> **THIS TO IS A ROUTE FORK, SO THE RULE BINDS IT DIRECTLY AND HARDER THAN ANY OTHER OPEN TO.**
   Whatever shape `/api/scoped/` takes for one firm, **every firm's route takes the SAME shape.**
   ⛔ **A design where two firms are served one way and the third has a bespoke path is REFUSED BY
   THE SOVEREIGN, not merely inelegant** — and it is the natural outcome of building
   firm-by-firm, which is exactly what a per-firm rollout invites. <<
⚠ **He addressed this to the TO-writing office by name.** It is recorded here rather than paraphrased
so the executing seat reads HIS words, not mine.

⛔ **ANDREW-DIRECT ~21:3xZ, SECOND RULE — DATA-DRIVEN VISIBILITY. VERBATIM:**
> *"all of these should be based on if there is data to populate and theyre invisible otherwise."*

**INVISIBLE — not `$0`, not a placeholder, not an empty state.** Where this TO's work reaches anything
that renders, presence is decided by **whether there is data to populate**, and absence renders
**nothing at all**.

· **Surprise channel:** anything odd that is not this task -> one line to `3.0.0_SA_CVO`, cc the
  issuer (`2.0.0_SA_COO~Z`), **and KEEP WORKING.**
· **`PT-inv-5` / standing moratorium: NO new alert, alarm, SNS, SES-send, notification, freshness
  checker or monitor.** Findings land as gates or owned blocking items.
· ⛔ **NO SHADOW OR BUILD-ALONGSIDE PIPELINE, no duplicate output path, no standing parity
  comparator** — Andrew complete veto. Build correctly, port directly, same-window rollback.
· ⚠ **`PT-b-2` IS UNCERTIFIED AND YOU WILL WANT IT: NO SUBSTRATE SHAPE HAS BEEN SELECTED.** Both
  shapes are live at once, and the shared limb is **unbuildable for at least one firm** —
  `smartx/` partitions by FUNCTION with **no firm boundary**, while 49 Financial's Models AND SMAs
  come from SmartX. **The scheme is PER-SOURCE-SYSTEM, not uniform.** `eclipse/` and `blackdiamond/`
  DO partition by firm. **If the served-plane design forces a substrate answer, that is a FINDING to
  surface — not a shape for this TO to pick.**
· ⚠ **`PT-b-4`, UNCERTIFIED, and it will bite an IAM condition:** ONE firm has **two live prefixes** —
  `blackdiamond/49f/` (285 objects, **holds the only `gold/` tier**) and `blackdiamond/49financial/`
  (8,862, newest today). **A firm-scoped policy naming one silently leaves the other open.** Measured
  at four seats; report what you see, do not act on it.
· **No gate gets loosened, waived or expected-green'd.** A criterion that fires is right.
</standing>

<deferred>
⚠ **`PT-e-1` (migration order, each step independently revertible) IS DELIBERATELY NOT ON THIS TO.**
It is CTO+AE and its steps cannot be stated until this TO's design exists — **an order over unknown
steps is a sequence of placeholders.** It is round 2, held by `1.0.0_SA_CTO~Z` with this lane.
⚠ **`PT-b-1` (ONE named substrate indirection) is BLOCKED BY `PT-b-2`** — the resolver's location is
a consequence of the shape, and no shape is selected.
</deferred>

<proof_of_spec>
  <criterion id="T3AE-AC1" cell_refs="PT-a-1"/>
  <criterion id="T3AE-AC2" cell_refs="PT-a-2"/>
  <criterion id="T3AE-AC3" cell_refs="PT-a-3"/>
  <criterion id="T3AE-AC4" cell_refs="PT-inv-1"/>
  <criterion id="T3AE-AC5" cell_refs="PT-inv-3"/>
  <criterion id="T3AE-AC6" cell_refs="PT-inv-4"/>
  <criterion id="T3AE-AC7" cell_refs="PT-a-1,PT-a-2,PT-a-3"/>
  <expected_criteria>T3AE-AC1,T3AE-AC2,T3AE-AC3,T3AE-AC4,T3AE-AC5,T3AE-AC6,T3AE-AC7</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~Y/deliverables/POSN_TENANCY.TO-3-AE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells declared: 6 (PT-a-1, PT-a-2, PT-a-3, PT-inv-1, PT-inv-3, PT-inv-4); criteria: 7. FORWARD — 7 of 7 criteria carry >=1 cell_ref. BACKWARD — 6 of 6 declared cells reachable from >=1 criterion (PT-a-1 from AC1+AC7, PT-a-2 from AC2+AC7, PT-a-3 from AC3+AC7, PT-inv-1 from AC4, PT-inv-3 from AC5, PT-inv-4 from AC6). Unmapped 0; untraceable 0. *(Of the decomp's 21 cells, 15 are NOT this TO's: PT-b-3/PT-c-2 discharged by TO-2-DS (ACCEPTED 4/4); PT-d-2/PT-d-3 on TO-1-DE (BLOCKED, fresh DE lane pending); PT-d-1 withheld pending per-firm bearers; PT-c-1 blocked by PT-b-2; PT-e-1 and PT-b-1 deferred per the clause above; PT-b-2, PT-b-4, R-pt1 and PT-inv-7 UNCERTIFIED — no TO may be cut against them; PT-inv-2 and PT-inv-5 bind as standing clauses.)*</alignment_denominators>
  <criterion_status_note>⛔ AC1 and AC2 are the two that can be falsely passed. AC1 fails silently on a SINGLE ARM — "firm A got its data" is equally true in a world with no discrimination at all, so the refusal arm carries the entire content of the criterion. AC2 fails silently on a CONFIGURATION READ — showing that the header is populated from the JWT does not show what happens when a caller supplies their own, and a client-assertable X-Firm-Id makes every other control on this TO decorative.</criterion_status_note>
</proof_of_spec>
</task_order>
