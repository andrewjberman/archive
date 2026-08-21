# D7_NOTIFY -- THE TO SET (six task orders, three ACTIVE)

<issued_by>1.0.0_SA_CTO~Z (gate + acceptance)</issued_by>
<issued>2026-08-21T07:3xZ</issued>
<authority>ANDREW-DIRECT 2026-08-21 ~07:3xZ, VERBATIM: *"approved on all, ratify the plan and issue the TOs. dont worry about whos on the list for now we can add that later, just want all the pipes done"*. Plan ratified: `org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoZ_D7_TICKETING_NOTIFICATION_PLAN_20260821.md`. Audience ruled INTERNAL ONLY (~04:5xZ). Notification moratorium satisfied by explicit ask; **nothing here authorises an alarm, monitor, freshness checker or SNS topic.**</authority>

> **THE SET'S ORGANISING RULE, from his word: "JUST WANT ALL THE PIPES DONE."**
> **A PIPE IS DONE WHEN IT RESOLVES, ACTS, AND REFUSES CORRECTLY -- NOT WHEN IT HAS BEEN CONFIGURED.** DL membership is deferred by his ruling, so a complete pipe with no list configured **resolves, finds nothing, and REFUSES LOUDLY with a named error.** That is exercisable today with no DL and no tenant admin.
> ⚠ **WE-2/WE-3 (latency, on-the-wire sender) STILL CANNOT BE EXERCISED without a list and stay UNCOMPUTABLE-BY-CONSTRUCTION. Deferring the list defers the PROOF, never the BUILD.** Do not let pipe-completion read as their discharge.

**SEQUENCING.** A / B / C are **ACTIVE and independently startable**. B and C are READS and open no build surface -- take them first if the seat prefers cheap wins. **D activates on C, E on B, F on A+D+E.**
⛔ **THE W-F IMPORT EDGE IS STILL NOT WRITTEN AND IS TO-F's LAST ACT.** On the runner plane that line is a production deploy inside 5 minutes with no apply step. Nothing in A-E writes it.

---

## TO-A -- W-E RE-CUT (ACTIVE) -- the three items, and only these three

<issued_to>0.5.0_AE_OpalETL~Z</issued_to> <status>ACTIVE</status> <plane>Lambda (apply-gated; BUILD ONLY, no apply opened)</plane>

**A1. FIELD COLLAPSE.** Release `DL_NOTICE_DEFERRED` (`title`, `requester_email`, `requester_name`, `requester_firm`) into `DL_NOTICE_FIELDS`. **PLUS `description`**, ruled released 2026-08-21 ~06:3xZ on the immutable-intake-vs-evolving-state principle.
⛔ **THE REST OF `WE-4-PROHIBITED` STAYS PROHIBITED:** `events` `source` `created_by` `status` `claimed_by` `assignee`. **The email carries the INTAKE SNAPSHOT in full and NO STATE.** A later change adding `status` on a *"we already relaxed WE-4"* argument is a misreading; flag it.

**A2. THE RECIPIENT SEAM.** `resolve_recipients(firm) -> [addresses]`, and `notify_dl` takes the item's firm and calls it. Config is a firm-keyed map, uniform today. **The uniformity is DATA, never STRUCTURE.**
⛔ **FORBIDDEN:** the shipped shape -- `TICKET_DL` at module scope consumed inline at the send site with no firm parameter.
**THE THREE REFUSAL CELLS (ruled):** UNCONFIGURED -> **REFUSE LOUDLY** (`DLAddressUnset`) · UNKNOWN FIRM with a default present -> **resolve to the default** (today: every firm) · rows exist, no match, **no default** -> **REFUSE LOUDLY**.
⛔ **WE-5's REFUSE-IF-UNSET RE-POINTS AT THE RESOLVER AND IS NOT RETIRED WITH THE STRING.** A resolver returning `[]` and proceeding is *a silent no-op wearing a successful send's clothes*, and is strictly easier to write than the refusing version.

**A3. SUPERSESSION SWEEP.** Fix the two the other items do not touch: `lambda_function.py` **L469** (`notify_dl_isolated` docstring, *"and the audience is open"* -- false) and `test_we_dl_notice.py` **L13** (the stated *reason* WE-2/WE-3 are untested; **the row stays UBC -- the DL's EXISTENCE is the real blocker**).
⛔ **DO NOT SWEEP L132 / L135** (*"audience-independent"*, *"ORTHOGONAL to audience"*). **That is WE-4's content-scope limb, which the `description` ruling PRESERVED. A blanket pass over the word "audience" deletes the reasoning the ruling just sharpened.**
Re-point L118 / L411 / TF L237 from *audience*-dependent to **Q3/link-target**-dependent; the refusal to bake a route stands.
⚠ **Run the census `comp-find -i`** -- case-sensitive returns 7 of 13 here, and the miss is non-random.

**A4. SUBJECT + CTA.** Subject `[<FIRM>] <requester subject>`. CTA: one standard hyperlink, **deep-link to the ticket if a per-ticket route exists, else the list page -- resolved by TO-B's measurement, not by choice.**

<expected_criteria>A-1,A-2,A-3,A-3b,A-4,A-5,A-6,A-7</expected_criteria>
- **A-1** FIELD SET, exercised on a real row: the released set renders; **a mutant adding `status` FAILS a test asserting the prohibited tuple is absent.**
- **A-2** SEAM: `notify_dl` takes firm and calls `resolve_recipients`; **no module-scope address is consumed at the send site** (assert by AST, not by reading).
- **A-3** THE THREE CELLS, each exercised, **both directions**: unconfigured -> `DLAddressUnset`; unknown-firm-with-default -> default; no-match-no-default -> `DLAddressUnset`. **A resolver returning `[]` without raising must FAIL a test.**
- **A-3b** ⛔ **REACHABILITY CONTROL ON THE REFUSAL PATH -- ADDED 2026-08-21 ~07:5xZ on `2.0.0_SA_COO~Z`'s finding, and it is the load-bearing half of A-3.** Since DL membership is deferred, **"a complete pipe that refuses loudly" IS the acceptance surface and its proof is a REFUSAL** -- and **a refusal test passes IDENTICALLY whether the pipe ran and correctly found nothing, or the pipe was NEVER REACHED AT ALL. Those two are byte-identical in a green test.**
  **REQUIRED: prove the refusing call site was ENTERED**, not merely that an exception surfaced -- an invocation assertion on `resolve_recipients` (spy/counter) in the refusing case, **plus a positive control on the SAME call site**: with a configured map, the identical path SENDS. **A refusal that cannot be shown to have been reached is not evidence of a working pipe; it is evidence of silence.**
  *(Same shape as the borrowed-control finding one layer down: the test is true about something, just not about the thing being certified.)*
- **A-4** WE-6 NO-REGRESSION PRESERVED: the email leg erroring still yields **201 + a buzz**; the mutant repointing at the unisolated sender still makes the handler RAISE.
- **A-5** SUPERSESSION: L469 and L13 corrected; **L132/L135 byte-unchanged** (assert).
- **A-6** SUBJECT + CTA exercised on a real row; **link target cites TO-B's measurement.**
- **A-7** Proof instance VALID rc=0 **POSITIONAL**, ids **A-1,A-2,A-3,A-3b,A-4,A-5,A-6,A-7** (eight, not seven -- A-3b was added after the first cut), `PYTHONIOENCODING=utf-8`, rc unpiped. **A bare-form VALID is not coverage evidence.** Checker-discrimination control run **ON THIS INSTANCE** -- a sibling's run does not discharge it.
<proof_of_spec><instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_NOTIFY.TO-A_PROOF_OF_SPEC.json</instance_path></proof_of_spec>

---

## TO-B -- J1 ATOM-DECOMP: THE CLIENT-FACING SURFACE (ACTIVE, READ-ONLY)

<issued_to>0.5.0_AE_OpalETL~Z</issued_to> <status>ACTIVE</status>

**QUESTION: what does a client actually see today?** Portal routes reachable by a client/partner user, the identity+auth path, what is exposed per firm, **and whether a per-ticket deep-link route exists** (TO-A's A4 and TO-E both consume this).
⛔ **WHY IT PRECEDES ANY CLIENT-FACING BUILD: we have never sent a client an email from this system and the surface is unmapped. A wrong assumption here is a CROSS-TENANT LEAK, not a bug.**
<expected_criteria>B-1,B-2,B-3,B-4</expected_criteria>
- **B-1** rectangle: every cell MEASURED or explicitly UNMEASURED; **denominators printed**; no INFERRED cell.
- **B-2** per-ticket deep-link route: **EXISTS / DOES NOT EXIST**, measured on the served surface, with a discriminating control.
- **B-3** the per-firm exposure boundary named: what one firm's user can reach of another's. **State the plane measured (served vs code) -- a served-layer absence is not a code-layer absence.**
- **B-4** proof instance VALID rc=0 positional, own-instance discrimination control.
<proof_of_spec><instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_NOTIFY.TO-B_PROOF_OF_SPEC.json</instance_path></proof_of_spec>

---

## TO-C -- J2 ATOM-DECOMP: THE TEAMS SEND PATH (ACTIVE, READ-ONLY)

<issued_to>0.5.0_AE_OpalETL~Z</issued_to> <status>ACTIVE</status>

**QUESTION: what content-type does the agent post to Teams, what renders CLICKABLE, and where is formatting decided -- code, prompt, or both?**
⛔ **IT PRECEDES ANY FORMATTING STANDARD, OR WE WRITE A STYLE GUIDE AGAINST A RENDERER THAT IGNORES IT.**
<expected_criteria>C-1,C-2,C-3</expected_criteria>
- **C-1** the send path identified at source with its content-type, **and the gateway's ~1h credential dependency restated as it bears on reliability.**
- **C-2** **hyperlink clickability MEASURED, not inferred** -- what markup the renderer honours. If it cannot be measured without posting, say so and stop; **do not post to prove it.**
- **C-3** proof instance VALID rc=0 positional, own-instance discrimination control.
<proof_of_spec><instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_NOTIFY.TO-C_PROOF_OF_SPEC.json</instance_path></proof_of_spec>

---

## TO-D -- TEAMS FORMATTING STANDARD + SEND-PATH FIX (STAGED on TO-C)

<issued_to>0.5.0_AE_OpalETL~Z</issued_to> <status>staged -- activates on TO-C acceptance</status>

**Andrew's standard, VERBATIM:** *"it really needs to do better formatting, it has a tendency to just block a wall of text, sentences should be appropriately spaced out with empty returns between 2-3 sentence max paragraphs and 1 line key lines or hyperlinks (which should be properly linked to be clickable)."*
⛔ **THIS IS CROSS-CUTTING, NOT A TICKETING ITEM. It is a property of the agent's Teams SEND PATH (and, for the concierge, its prompt).** Building it inside the ticket notifier yields **one well-formatted surface and an unchanged agent**, and the next surface rebuilds it. **Ticketing CONSUMES this; it does not contain it.**
<expected_criteria>D-1,D-2,D-3,D-4</expected_criteria>
- **D-1** the standard stated as a **testable property**, not prose advice.
- **D-2** applied at the SEND PATH so **every** Teams message inherits it -- exercised on at least two unrelated message shapes.
- **D-3** **hyperlinks clickable, verified against TO-C's measured renderer** -- not against the documentation.
- **D-4** proof instance VALID rc=0 positional, own-instance discrimination control.
<proof_of_spec><instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_NOTIFY.TO-D_PROOF_OF_SPEC.json</instance_path></proof_of_spec>

---

## TO-E -- CLIENT NOTIFICATIONS (STAGED on TO-B)

<issued_to>0.5.0_AE_OpalETL~Z</issued_to> <status>staged -- activates on TO-B acceptance</status> <plane>Lambda</plane>

**TWO sends, both ruled:** **(i) submit acknowledgement** (Andrew, CALL 5: *approved* -- a form that submits into silence reads as broken) and **(ii) pickup notification naming the claimer by FULL NAME** (CALL 6).
⛔ **SINGLE-RECIPIENT BY CONSTRUCTION, NOT BY CONVENTION** -- addressed to the requester, never to a list. **One firm's ticket reaching another is a cross-tenant leak.**
⛔ **CONTENT PROJECTION BINDS HARDER HERE THAN INTERNALLY.** The intake-snapshot release in TO-A is an **INTERNAL** ruling. **Re-derive the client field set from WE-4's pointer-not-home limb; do NOT inherit TO-A's set.**
⛔ **AND NOTE THE ASYMMETRY, DELIBERATE:** internal gets **one** email and **no** follow-ups; the client gets a **pickup follow-up**. A reader taking *"no follow-ups"* as global will delete this.
<expected_criteria>E-1,E-2,E-3,E-4,E-5</expected_criteria>
- **E-1** submit-ack exercised on a real row.
- **E-2** pickup notification exercised, **claimer's FULL NAME rendered**, degradation path named when the directory has no such row.
- **E-3** **SINGLE-RECIPIENT asserted structurally** -- a mutant supplying two recipients must FAIL.
- **E-4** client field set **re-derived**, and the internal-only fields **provably absent** on a row where they are populated.
- **E-5** proof instance VALID rc=0 positional, own-instance discrimination control.
<proof_of_spec><instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_NOTIFY.TO-E_PROOF_OF_SPEC.json</instance_path></proof_of_spec>

---

## TO-F -- FAILURE MATRIX, THEN THE WIRING ACTS (STAGED on A+D+E)

<issued_to>0.5.0_AE_OpalETL~Z</issued_to> <status>staged -- activates on TO-A + TO-D + TO-E acceptance</status>

**THE RELIABILITY QUESTION IS NOT "does each leg work."** It is: **when one leg fails, what does the system do?** W-E established the shape (email errors -> still 201, named error separating *unconfigured* from *refused*). **That must now hold across FOUR legs -- internal email, Teams, client email, dashboard -- and the failure matrix is a DESIGN artifact, not a test artifact.**
⛔ **THE W-F IMPORT EDGE IS THE LAST ACT OF THIS TO AND OF THE WHOLE SET.** On the runner plane it is a production deploy within 5 minutes **with no apply step in which anyone could review it.** It is written only after the matrix is accepted.
⚠ Before that write, run the mandated `comp-blast`. **A `NOT-FOUND` is NOT "nothing breaks"** -- TO-C's coverage read bears on whether that call can discriminate at all.
<expected_criteria>F-1,F-2,F-3,F-4</expected_criteria>
- **F-1** the four-leg failure matrix, each cell a named behaviour, **no cell left "should not happen."**
- **F-2** each leg's failure exercised **in the expensive direction** -- the ticket still lands, the client is not silently dropped.
- **F-3** the wiring act, **last**, with WF-6 then **EXERCISED and not promoted** (its subject now exists).
- **F-4** proof instance VALID rc=0 positional, own-instance discrimination control.
<proof_of_spec><instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_NOTIFY.TO-F_PROOF_OF_SPEC.json</instance_path></proof_of_spec>

---

## STANDING, ALL SIX

**PROOF-OF-SPEC:** `PYTHONIOENCODING=utf-8 python .tools/proof-of-spec-check.py <instance> "<ids>"` -- **positional, rc unpiped.** The 2nd arg is a comma-separated ID LIST, **not the TO path**. **A bare-form VALID is NOT coverage evidence.** **Checker-discrimination is PER-INSTANCE.**
**REPORTING:** completion -> `2.0.0_SA_COO~Z` (validation) cc `1.0.0_SA_CTO~Z` (acceptance) + `0.0.0_AB_MSTR~Z` (ferry). Surprise channel: one line to CTO~Z, no action, keep working.
**DO NOT:** open an apply · write the W-F import edge before TO-F · build any alarm, monitor, freshness checker or SNS topic · clone `ses.tf`'s bounce/complaint topics · bake a sender fallback (**the pinned sender stands**) · arm any cron.
**WHEN THE W-E/W-A APPLY IS EVENTUALLY REQUESTED it must be framed as CARRYING W-A's QUEUE, not as a single change.**
