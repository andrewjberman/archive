# TO OPAL_ADVIPOINTERS.P4-PINS-CERT-49F — per-key two-phase pins (fresh vintage, same content-date) + cutover cert + the P5 census read (push plan §3 rows 4b/4c/5, CVO legs)

<task_order id="OPAL_ADVIPOINTERS.P4-PINS-CERT-49F" project="OPAL_ADVIPOINTERS">
<issued_to>3.0.0_SA_CVO</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>pins 2026-08-21 · cert 2026-08-22 (at the 4c flip) · census read 2026-08-23 (P5-gated). The 08-21 pin date is CONDITIONAL on your own stated precondition (group PIN, below); if P2 slips, 4b slips WITH it in writing — never silently (your 154542Z line, adopted verbatim).</dated>
<status>pending -- GO 20260818T160719Z (COO); group PIN begins when its precondition reads true</status>
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
Group PIN (08-21):
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
Group CERT (08-22, per key at flip):
- 49F-CERT-PERKEY: Rule-14e cutover cert per key consuming (i) the pre-flip pin, (ii) DS~B's
  never-widen disclosure (P4E-5), (iii) the CTO+COO never-widen determination; DELTA=0 keys certed
  without hold. Post-flip re-base to ~0 recorded as its own act per key.
- 49F-CERT-INPUT-INDEPENDENT: cert grounded on your own reads of served + canonical bytes, never on
  DS~B/DE self-report (the instance makes re-derivation mechanical; it does not substitute).
Group CENSUS (08-23, P5-gated):
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
