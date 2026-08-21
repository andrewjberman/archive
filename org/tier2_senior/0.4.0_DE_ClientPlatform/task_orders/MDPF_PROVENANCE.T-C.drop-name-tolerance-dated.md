# TO MDPF_PROVENANCE.T-C — drop the reader's name tolerance on a STATED date (the port's last step)

<task_order id="MDPF_PROVENANCE.T-C" project="MDPF_CANPLAT">
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T13:35Z</issued>
<dated>2026-08-20 — DATED + OWNED, explicitly BEHIND T-A (08-19) and T-B's first clean scheduled run. If T-B's rename has not had one clean unattended 13:30Z run by 08-20, T-C re-dates to the day after that run — stated on this TO the same day, never silently.</dated>
<status>SUPERSEDED BY SOVEREIGN DECREE 2026-08-21 -- ANDREW-DIRECT at the DS terminal, VERBATIM, relayed by 0.4.0_DS_ClientPlatform (msg 64982): "no, none of this work matters" / "mark any of these associated TOs superseded by sovereign decree" / "i do not want this thrash and irrelevant effort". **THE TOLERANCE STAYS. DO NOT DROP IT.** T-C's whole job was to remove the `partner_provenance ?? cohort_provenance` tolerance at pairedProvenanceRead.ts:312/:719, gated on T-B's R-2 rename landing. T-B is STOPPED and marked superseded @d6d53be6fb; R-2 was never landed in source, so the new keys will not exist. MEASURED TODAY across all four live served scopes (written 2026-08-21T13:50:49Z..13:50:51Z): partner_provenance ABSENT 4/4, cohort_source ABSENT 4/4, per-firm cohort_provenance still carrying SOURCE NAMES. THEREFORE THAT TOLERANCE IS THE ONLY REASON THE GLOBAL PROVENANCE READ RESOLVES ON ALL FOUR SCOPES, and executing this TO would break the live read. It is superseded and it was also never safe to run; both are true and either alone is sufficient to leave it alone. The re-dated INDETERMINATE anchor @eb64d27e97 is now VOID, not pending -- there is no T-B run coming. No code was changed for this TO, at any point.</status>
<priority>P3 — closes the port; removes the temporary adapter so it does not become permanent</priority>
<authority>CTO RULING @fc74f8f6b4 §2 port sequence: "DE lands R-1 with name-tolerant reads -> DS lands R-2 on the scheduled path -> DE drops the tolerance on a stated date." COO decomposition per §4. Andrew 08-04: build correctly and PORT OVER — no standing dual-read.</authority>
</task_order>

## The job
Remove the `partner_provenance ?? cohort_provenance` tolerance at Global and any per-firm
`cohort_provenance` slot read that predates T-B's §1a-shape emit; the reader reads exactly the
post-R-2 keys: `point_class[]` first everywhere, `cohort_provenance[]` (§1a class shape) as refinement
per-firm, `partner_provenance[]` at Global, `cohort_source[]` ignored by the class read (it is
source-identity, not class). Update the schema SoT comment (`:12-14`) to the ruled form and cite
@fc74f8f6b4.

## Acceptance criteria
- PC-1: tolerance removed; the LIVE served artifacts (all four scopes) read clean — warn count 0 per
  scope, before/after printed.
- PC-2: T-A's inverse mutant (PA-4) and the unknown-string mutant (PA-5) still fire.
- PC-3: a fixture in the PRE-R-2 shape (legacy `cohort_provenance` = source names, no `partner_provenance`)
  now degrades LOUD by design — shown, so the drop is proven to bite (a tolerance drop nobody can see is
  a no-op).
- PC-4: zero served/rendered numbers move; screenshot control pixel-identical.

<proof_of_spec>
  <expected_criteria>PC-1,PC-2,PC-3,PC-4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/MDPF_PROVENANCE.T-C_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
Positional-id validation, check the rc.

## Discipline + reporting
Portal main tree DEV; schema-check + ternary-audit; extend the FE-2 exercise script; unpushed (MSTR
integrates). Report COO (cc CTO, MSTR) at completion; immediately if any scope still emits the old key
on the date (that is a T-B finding, not a T-C one — surface, do not tolerate).
