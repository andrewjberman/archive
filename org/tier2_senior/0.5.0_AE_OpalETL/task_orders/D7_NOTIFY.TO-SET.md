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
⛔ **DO NOT DELETE THE PROTECTED PAIR -- cite them BY STRING, never by line: *"audience-independent"* and *"ORTHOGONAL to audience"*.** ⚠ **COORDINATE CORRECTED 2026-08-21 ~09:5xZ (`2.0.0_SA_COO~Z`): they were at L132/L135 when this TO was written and are at **:148 / :151** after TO-A's legitimate rewrite. The protection held; the CITATION went stale.** **AND THAT IS WHY THE CRITERION ASSERTS ON THE STRINGS: a line-number assertion would have FAILED on a legitimate edit, or -- worse -- PASSED while pointing at whatever now occupies 132.** CLAUDE.md's own form: *a line citation without a vintage is not a citation.* **That is WE-4's content-scope limb, which the `description` ruling PRESERVED. A blanket pass over the word "audience" deletes the reasoning the ruling just sharpened.**
Re-point L118 / L411 / TF L237 from *audience*-dependent to **Q3/link-target**-dependent; the refusal to bake a route stands.
⚠ **Run the census `comp-find -i`** -- case-sensitive returns 7 of 13 here, and the miss is non-random.

**A4. SUBJECT + CTA.** Subject `[<FIRM>] <requester subject>`. ✅ **CTA TARGET RESOLVED 2026-08-21 ~08:5xZ BY TO-B MEASUREMENT: THE LIST PAGE.** No per-ticket deep-link route exists -- 25 routes in `App.tsx`, only 2 carry a param/wildcard and neither is per-ticket; **no query-param path either** (zero `useSearchParams`/`location.search` in the TicketCenter page; its 6 `ticket_id` hits are React keys and list button targets). **Discriminating control run:** the same regex against a synthetic `/ticket-center/:ticketId` fixture DOES detect a param, **so the absence is measured, not a broken search.** The conditional ruling resolves to its second branch by fact, not by choice.
⛔ **CTA FORM RULED 2026-08-21 ~08:2xZ, on TO-C's surprise-channel finding: THE SES LEG IS `MIMEText(body, 'plain')`, so "one standard hyperlink" on that body is A BARE URL RELYING ON CLIENT AUTOLINKING, not a labelled link.**
**RULED: plain text, CTA URL ON ITS OWN LINE, bare.** It autolinks in every major mail client, it cannot render broken, and a URL alone on a line is also what Andrew's own formatting instinct asks for (*"1 line key lines or hyperlinks"*).
⛔ **DO NOT ADD A `multipart/alternative` HTML PART IN v1.** A labelled link would need a second body -- **and two bodies for one message is the SECOND-HOME defect one surface over: they can diverge, and nothing makes them stay in step.** If a labelled link is later wanted, that is a deliberate act with its own sync obligation, not a formatting tweak. **Carded to Andrew, not built.**
⚠ **THE EMAIL AND TEAMS SURFACES DIFFER HERE AND MUST NOT BE HARMONISED:** a bare URL AUTOLINKS in mail and does NOT necessarily in Teams (TO-C left Teams autolink UNMEASURED). **Andrew's "properly linked to be clickable" was said about TEAMS; it does not import onto the email leg.**

<expected_criteria>A-1,A-2,A-3,A-3b,A-4,A-5,A-6,A-7</expected_criteria>
- **A-1** FIELD SET, exercised on a real row: the released set renders; **a mutant adding `status` FAILS a test asserting the prohibited tuple is absent.**
- **A-2** SEAM: `notify_dl` takes firm and calls `resolve_recipients`; **no module-scope address is consumed at the send site** (assert by AST, not by reading).
- **A-3** THE THREE CELLS, each exercised, **both directions**: unconfigured -> `DLAddressUnset`; unknown-firm-with-default -> default; no-match-no-default -> `DLAddressUnset`. **A resolver returning `[]` without raising must FAIL a test.**
- **A-3b** ⛔ **REACHABILITY CONTROL ON THE REFUSAL PATH -- ADDED 2026-08-21 ~07:5xZ on `2.0.0_SA_COO~Z`'s finding, and it is the load-bearing half of A-3.** Since DL membership is deferred, **"a complete pipe that refuses loudly" IS the acceptance surface and its proof is a REFUSAL** -- and **a refusal test passes IDENTICALLY whether the pipe ran and correctly found nothing, or the pipe was NEVER REACHED AT ALL. Those two are byte-identical in a green test.**
  **REQUIRED: prove the refusing call site was ENTERED**, not merely that an exception surfaced -- an invocation assertion on `resolve_recipients` (spy/counter) in the refusing case, **plus a positive control on the SAME call site**: with a configured map, the identical path SENDS. **A refusal that cannot be shown to have been reached is not evidence of a working pipe; it is evidence of silence.**
  *(Same shape as the borrowed-control finding one layer down: the test is true about something, just not about the thing being certified.)*
- **A-4** WE-6 NO-REGRESSION PRESERVED: the email leg erroring still yields **201 + a buzz**; the mutant repointing at the unisolated sender still makes the handler RAISE.
- **A-5** SUPERSESSION: the two false-reason lines corrected; **the PROTECTED PAIR byte-unchanged, asserted BY STRING** (*"audience-independent"* / *"ORTHOGONAL to audience"*) -- **never by line number.** *(They sat at L132/L135 at issue and at :148/:151 after TO-A's rewrite; the strings are the stable handle, the coordinates are not.)*
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

<issued_to>0.5.0_AE_OpalETL~Z</issued_to> <status>staged -- activates on TO-C acceptance. **RE-CUT 2026-08-21 ~08:2xZ on TO-C's finding -- SPLIT IN TWO, see D-SPLIT.**</status>

> ### ⛔ D-SPLIT -- TO-C CHANGED WHAT THIS TO IS, AND J2 IS WHY WE KNOW BEFORE BUILDING
> **`tools.py:617` and `:658` HARDCODE `contentType: "text"` at both Teams send sites** -- no branch, no parameter, no caller override. Census: **8 `contentType` hits / 71 files**, and **the two EMAIL sends at `:220`/`:238` are `"Text"` too. EVERY outbound message path in the gateway is plain text.**
> **D-PROSE (buildable now, NO deploy):** paragraph spacing, 2-3 sentence maximum, key lines and links on their own line. **All of this is expressible in plain text and needs no content-type change.**
> **D-HTML (A CODE CHANGE TO A LIVE EC2 SERVICE = A DEPLOY):** *"hyperlinks properly linked to be clickable"* requires `contentType: "html"`. **That is not a formatting standard, it is a gateway code change**, and it rides `safe-ec2-deploy` per Deployment Rule 7 -- **a different plane from everything else in this set.**
> **DO D-PROSE FIRST AND DO NOT LET IT BLOCK ON D-HTML.** **A standard written today that specifies link MARKUP would specify something the renderer discards** -- which is precisely the failure J2 existed to prevent, and it was prevented.
> ⚠ **AND THE AUTOLINK QUESTION IS OPEN, NOT ANSWERED:** TO-C established that **markup** is not honoured under `text`; whether the Teams client auto-linkifies a **bare URL** is **UNMEASURED**. **Do not read C-2 as "a bare URL is unclickable."**

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

> ### ⛔ E-0 (NEW, TO-B's B-3 FINDING) -- **A CLIENT-FACING LINK IS NOT UNIFORMLY SAFE, AND THE FIRM KEY GOVERNS IT**
> Measured at portal DEV, re-derived at the gate: **`FIRM_ALLOWED_PATHS` carries 4 firms** -- `/ticket-center` is in **0 of 4** *and* sits behind `<ProtectedRoute requireInternal>` (`ProtectedRoute.tsx:44`, `firmId !== 'opal-capital'` -> bounce), **so a client cannot reach the board by TWO INDEPENDENT GATES** (correct -- the board is internal).
> **BUT `/submit-request` IS IN ONLY 3 OF 4 -- NOT `inflection`, deliberately (`firmAccess.ts:66`, the 05-28 Tools-section ruling).**
> **THEREFORE A PICKUP EMAIL TO AN INFLECTION USER POINTING AT `/submit-request` BOUNCES THEM** -- a notification whose call-to-action lands on an access denial is worse than no link.
> **RULED: the client email's link target is FIRM-AWARE, resolved through the SAME firm key as the recipient seam, and OMITTED (not defaulted) for a firm with no reachable target.** A firm-blind client link is forbidden.
> >> **THE ARCHITECTURAL POINT, and it generalises past this TO: THE FIRM KEY RESOLVES BOTH *WHO RECEIVES* AND *WHAT THEY CAN BE SENT TO*.** Andrew declared the seam for recipients; the same seam is load-bearing for link targets, and building it for one and not the other leaves the second to be retrofitted.
> ⚠ **PLANE: CODE, at portal DEV.** Branch agreement is **not** proof the deployed bundle was built from that HEAD -- that is CI's plane and is not claimed.
⛔ **CONTENT PROJECTION BINDS HARDER HERE THAN INTERNALLY.** The intake-snapshot release in TO-A is an **INTERNAL** ruling. **Re-derive the client field set from WE-4's pointer-not-home limb; do NOT inherit TO-A's set.**
⛔ **AND NOTE THE ASYMMETRY, DELIBERATE:** internal gets **one** email and **no** follow-ups; the client gets a **pickup follow-up**. A reader taking *"no follow-ups"* as global will delete this.
<expected_criteria>E-0,E-1,E-2,E-3,E-4,E-5</expected_criteria>
- **E-0** FIRM-AWARE LINK TARGET, exercised **both directions**: a firm WITH a reachable target gets the link; **`inflection` gets NO link, not a default one.** A firm-blind link must FAIL a test. ⚠ **STATE THE DENOMINATOR AS *FIRMS*, NAMED -- `3 of 4 firms (49financial, cottonwood, demo; NOT inflection)` -- NEVER as a path count** (`2.0.0_SA_COO~Z`, validation half). **A path-framed count is the one frame a later reader cannot check against the allowlist**, which is the denominator-choice principle applied before the fact instead of after.
- **E-1** submit-ack exercised on a real row.
- **E-2** pickup notification exercised, **claimer's FULL NAME rendered**, degradation path named when the directory has no such row.
- **E-3** **SINGLE-RECIPIENT asserted structurally** -- a mutant supplying two recipients must FAIL.
- **E-4** client field set **re-derived**, and the internal-only fields **provably absent** on a row where they are populated.
- **E-5** proof instance VALID rc=0 positional, own-instance discrimination control.
<proof_of_spec><instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_NOTIFY.TO-E_PROOF_OF_SPEC.json</instance_path></proof_of_spec>

---

## TO-F -- FAILURE MATRIX, THEN THE WIRING ACTS (STAGED on A+D+E)

<issued_to>0.5.0_AE_OpalETL~Z</issued_to> <status>✅ **ACTIVE 2026-08-21 (Andrew: "proceed with D E F"). Inputs exist: A/B/C/D/E all accepted + validated.**</status>

> ### ⛔ F-0 -- THE WIRING ACT IS **HELD**, AND F IS ISSUED WITHOUT IT
> **His *"proceed with D E F"* predates the clarified fact that on the runner plane THE IMPORT EDGE IS A PRODUCTION DEPLOY** -- live within 5 minutes, **no apply step in which anyone could review it.** The TO-SET's standing DO-NOT already forbids opening an apply; **the wiring IS one, in effect if not in form.**
> **SO F DELIVERS THE MATRIX AND THE EXERCISES. THE WIRING WAITS FOR HIS EXPLICIT WORD.** Same standard as D-HTML and as `0.7.0_AE_CloudOps` stopping at the commit on the gateway TF: **an approval covers what the approver was shown.**
> **F-3 is therefore UNCOMPUTABLE-BY-CONSTRUCTION at issue, and that is not a gap** -- its subject does not exist until the edge is written. **Do not treat completing F-1/F-2/F-4 as licence to write it.**

**THE FOUR LEGS, NAMED AT ISSUE so the matrix cannot drift:** (1) **internal DL email** (SES, Lambda plane) · (2) **Teams buzz** (5-min scheduled runner, gateway-mediated, carries the ~1h credential dependency) · (3) **client email** -- submit-ack + pickup (SES, Lambda plane, single-recipient) · (4) **the escalation sweep** (`sweep.py`, runner plane, currently unwired).
**DENOMINATOR FRAMED AT ISSUE: state cell counts as LEGS x FAILURE-MODES, both named -- never as a raw test count.**

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
