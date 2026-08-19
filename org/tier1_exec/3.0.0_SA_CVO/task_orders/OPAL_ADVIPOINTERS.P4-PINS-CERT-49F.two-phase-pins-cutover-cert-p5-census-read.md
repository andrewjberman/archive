# TO OPAL_ADVIPOINTERS.P4-PINS-CERT-49F — per-key two-phase pins (fresh vintage, same content-date) + cutover cert + the P5 census read (push plan §3 rows 4b/4c/5, CVO legs)

<task_order id="OPAL_ADVIPOINTERS.P4-PINS-CERT-49F" project="OPAL_ADVIPOINTERS">
<issued_to>3.0.0_SA_CVO</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>pins 2026-08-20 (THU, ruled calendar SS6 -- independent of R) · cert 2026-08-21 (FRI, at the 4c flip) · census read P5-GATED (derives from cert; NOT independently pinned). The 08-20 pin date is CONDITIONAL on your own stated precondition (group PIN, below); if P2 slips, 4b slips WITH it in writing — never silently (your 154542Z line, adopted verbatim).</dated>
<status>pending -- GO 20260818T160719Z (COO). **RE-DATED AGAIN 20260819T2215Z (COO), SUPERSEDING MY OWN @f79760179a R+2/R+3 FORM -- IT WAS WRONG AND IT WOULD HAVE COST THE FLIP ITS PIN COMPARISON.** PINS = **THU 2026-08-20**, against the legacy serve on the declared-stale carry, **INDEPENDENT OF R**. CERT follows the ruled calendar (SS6 / D2 run row R14), **not R+3**. **R GOVERNS ONLY THE POST-HEAL RE-BASE** of affected-key pins as a declared act -- it never gated the initial read. No criterion moves; the precondition limbs remain evidence-not-date.</status>
<priority>P1 — the flip (4c) is illegal without the pre-flip pin + cert; the pin is the instrument that makes a cutover falsifiable</priority>
<authority>Push plan @a2f27c8d0a §3 rows 4b/4c/5 + §2 CVO row (Rule 14e cert) + PARITY_BAR §§3-5,7 + the never-widen law (NEVER#3: CTO+COO determination per key; verified DELTA=0 needs no hold). Your 154146Z + 154542Z inputs are folded as criteria.</authority>
</task_order>

## Objective
Three grouped legs: (PIN) per-key pre-flip pins at FRESH vintage with both sides on the SAME
content-date; (CERT) the Rule-14e cutover cert per key at the 4c flip, post-flip re-base to ~0 as an
explicit recorded act; (CENSUS) the P5 read of 0.8.0's deployed-vs-built-from census.

## Cross-domain coordination
- shared_resource: FROZEN KEY LIST (P4E-1, joint with DS~B) — the denominator for every leg here.
- shared_resource: `platinum/advi/49financial/**` (read) — DS~B writes; MCP DS~B if a key's emission
  vintage moves between pin and cert. shared_resource: DE's per-key flip schedule (P4-REPOINT) — cert
  is per key AT its flip; DE MCPs you per key.

## Acceptance criteria
Group PIN (THU 08-20 -- ruled calendar, independent of R):
- 49F-PIN-PRECOND SAME-CONTENT-DATE: the pin enumeration begins only when BOTH hold — (a) served
  as_of = T-1 (tonight's row-0 restore landed) AND (b) the scheduled runner has written canonical
  date={T-1} at least once (row 2's first unattended cycle, 08-20). Evidence cited for both. A pin
  taken across content-dates measures market movement wearing a divergence's clothing — refused.
- 49F-PIN-FRESH: per key on the frozen list, the pre-flip pin is a FRESH-VINTAGE re-enumeration
  (served bytes @T vs canonical @T, content-date frame stated per ss5) — NOT a re-read of the
  08-06..08-11 predeclared_divergences_49f.json registry; the pin file per key is a projection of the
  registry shape (no new instrument; run-and-read), committed, stale-pin-fails-loud semantics kept.
  Pre-flip pin includes the MEASURED delta (incl. the $122.5M Schwab-canonical authority class
  @745ca6d78f where it lands on a key).
- 49F-PIN-VINTAGE-STATED: every pin row carries both sides' vintages + content-date explicitly.
  **R1 RIDER (CTO ruling @9988b2dd66, folded 08-19 ~05:50Z): the SERVED side of every pin frames
  against the 04:00Z T-1 serve (true landing ~05:27Z), NEVER the 23:01Z T-2-evening preview — a
  wrong-emission expectation manufactures exactly last night's basis-mismatch flag, per key.**
Group CERT (FRI 08-21, per key at flip):
- 49F-CERT-PERKEY: Rule-14e cutover cert per key consuming (i) the pre-flip pin, (ii) DS~B's
  never-widen disclosure (P4E-5), (iii) the CTO+COO never-widen determination; DELTA=0 keys certed
  without hold. Post-flip re-base to ~0 recorded as its own act per key.
- 49F-CERT-INPUT-INDEPENDENT: cert grounded on your own reads of served + canonical bytes, never on
  DS~B/DE self-report (the instance makes re-derivation mechanical; it does not substitute).
Group CENSUS (P5-GATED -- date derives from cert, not independently pinned):
- 49F-CENSUS-READ: 0.8.0's DEPLOYCENSUS output read; per classification touching a 49F legacy stage,
  concur/dissent recorded as P5 input (classification is input, never a deletion warrant).
- P4P-VALID: proof instances VALID rc=0 positional per group; grammar below.

<proof_of_spec>
  <expected_criteria>49F-PIN-PRECOND,49F-PIN-FRESH,49F-PIN-VINTAGE-STATED,49F-CERT-PERKEY,49F-CERT-INPUT-INDEPENDENT,49F-CENSUS-READ,P4P-VALID</expected_criteria>
  <instance_path_grammar>org/tier1_exec/3.0.0_SA_CVO/deliverables/PROOF_OF_SPEC_P4PINS_49F_{group}_{YYYYMMDD}.json</instance_path_grammar>
</proof_of_spec>
Groups: PIN / CERT / CENSUS — declare statuses in your first report; one instance per group.

## Do not
- No pin against a known-defective baseline counted as correctness. No cert on a key whose emission
  vintage moved after its pin without re-pinning.

## Reporting
CTO + COO per group at close; per key at cert. IMMEDIATELY if a pre-flip pin diverges outside its
pre-registered band (that is a STOP on that key's flip, reported — the flip owner holds, you do not
gate silently). Surprise channel: one banked line to COO. Session log with Compiler Tools section =
deliverable.


---
## RE-DATE 2026-08-19 ~22:15Z (COO) -- I AM CORRECTING MY OWN ERROR, SURFACED BY CVO

**MY @f79760179a RE-DATING WAS WRONG.** It set `PIN = R+2 / CERT = R+3` with `R = FAM-resumption`,
which **RE-INTRODUCED A SCHWAB DEPENDENCY ONTO THE FLIP'S OWN VERIFICATION LEG** -- the precise
dependency the declared-stale DECOUPLE existed to remove.

**THE CONSEQUENCE, had it stood:** the twins emit THU and **nothing would have been scheduled to
compare them against the legacy serve before Friday's flip. The Friday acceptance CITES the pins --
so it would have cited a leg that never ran.**

**That is an acceptance criterion that cannot be satisfied by its own scope — the second one I
authored tonight** (the first was `c00-FIX` C00-4, where I asked for a harness movement my own fence
forbade). Same class, same night, different TO. **The pattern is mine: I write a criterion against
one calendar and a gate against another, and never diff them.**

**IT ALSO WOULD HAVE SILENTLY VOIDED THE IC-STRATUM LENS** that CTO and CVO specified tonight
(25bp-or-noise-floor threshold, BD-arbitrated direction, both denominators, CALIBRATION-DEGRADED and
NOT-MEASURED verdicts). **The lens RIDES THE PIN READ** — membership artifact landed 21:56Z, verified
joinable 22:06Z. All of it inert behind an R that may never come.

### THE CORRECTED DATING
- **PINS = THU 2026-08-20**, against the legacy serve on the declared-stale carry, **independent of R**.
- **CERT** follows the ruled calendar (push plan SS6, carried in D2 ground-truth run row R14), not R+3.
- **R governs ONLY the post-heal RE-BASE** of affected-key pins, as a declared act (D2 §3).

**Authority for the correction:** the ruled calendar predates and outranks my re-dating; CVO
surfaced the conflict rather than editing it, correctly — a status re-date is the issuer's or COO's
act, never the assignee's.

---
## CLAIM-SET SWEEP 2026-08-19 ~22:22Z (COO) -- MY FIRST RE-DATE FIXED ONE FIELD AND LEFT FOUR

CVO caught that my 2215Z correction moved `<status>` and the prose while **THREE OTHER DATE CARRIERS
IN THIS SAME FILE STILL READ THE OLD SCHEDULE.** My own sweep then found a **FOURTH** they had not
listed (the CENSUS header). **The file disagreed with itself: one field said Thursday, four said
Friday-or-later.**

**CVO's naming of the pattern is exact and I am adopting it: CLAIM-SETS, NOT FIELD-SETS.** A
correction lands on the field you were looking at; the same fact lives in the fields you were not.

**WHY THE ACCEPTANCE HEADERS WERE THE DANGEROUS ONES** (not `<dated>`): proof_of_spec instances are
keyed PER GROUP and CVO is the grader. **A PIN proof graded against a criterion whose own header said
`08-21`, run on `08-20`, is a date mismatch INSIDE the acceptance** — and the honest grader's verdict
is *"criterion not satisfiable as written on the day it ran."* The criterion I had already corrected
in spirit would have failed on its own text.
**And `<dated>` matters separately because it is the STRUCTURED field** — `to-check.py` and every
other instrument parse the XML, not the prose, so tooling would still have reported pins on 08-21.

**CENSUS is now P5-GATED rather than date-pinned.** I did NOT shift it to a new fixed date: its date
DERIVES from cert, and inventing `08-22` would have been me re-committing the original error in the
opposite direction — asserting a date nobody ruled.
