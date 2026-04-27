<task_order>
  <metadata>
    <id>ADHC_COMPIL.003.cto-prd-compiler-mandate</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>1.0.0_SA_CTO</issued_to>
    <date>2026-04-27</date>
    <status>pending</status>
    <project_code>ADHC_COMPIL</project_code>
    <theme>C</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL.md §6 (commit 172470a8)</prd_ref>
    <effort>1–2 weeks</effort>
    <gates_on>None — parallelizable with ADHC_COMPIL.001 and .002</gates_on>
    <gates_for>ADHC_COMPIL.004 (prd-evidence-check.sh, stretch) | ADHC_COMPIL.006 (Theme E validate protocol)</gates_for>
    <self_assigned>CTO confirmed self-authoring this TO (message 20260427T150539Z)</self_assigned>
  </metadata>

  <objective>
    Codify the required compiler runs at PRD-authoring time so every PRD's
    Compiler Evidence section is populated before TO decomposition begins.
    The discipline exists in CTO/COO institutional knowledge but is not
    enforced by any template, prompt, or gate. Closes the class of error
    where PRDs claim artifacts that no producer writes
    (e.g., ADVI_49EXEC platinum/advisors/{id}/positions.json incident).
  </objective>

  <scope>
    1. org/templates/prd_template.md
       Sections: §1 Scope, §2 Existing State, §3 Architecture, §4 Component Specs,
       §5 Compiler Evidence (NEW MANDATORY SECTION), §6 TO Candidates, §7 Open Questions.
       §5 must include inline guidance listing required runs by PRD type
       (with reference to PRD_AUTHORING_PROTOCOL.md).

    2. docs/architecture/PRD_AUTHORING_PROTOCOL.md
       Full operator doc with required-runs matrix:

       | PRD touches…         | Required compiler runs |
       |----------------------|------------------------|
       | Gold script          | comp-pipescript io, comp-blast, comp-platinum reverse |
       | Portal component     | comp-routes trace, comp-cache collisions, comp-transform schema-check |
       | Lambda               | comp-iam service, comp-routes trace |
       | EC2 service          | comp-iam service, EC2_MANIFEST.json check |
       | New artifact claim   | comp-platinum reverse (must show producer exists) |
       | Cross-firm portal    | comp-routes trace for both firm scopes |

       Include worked examples using ADVI_INFLEC_BRONZERUN_V2.md and ADVI_RDVSDS
       as positive references (both have good compiler-evidence sections).

    3. CTO + COO prompt.md updates
       Add one-line rule to each: "Every new PRD must include §5 Compiler Evidence
       — required runs per docs/architecture/PRD_AUTHORING_PROTOCOL.md."

    4. (Stretch — can split to ADHC_COMPIL.004 if preferred)
       .tools/prd-evidence-check.sh: scan docs/architecture/ for PRDs missing
       §5 header or compiler-tool citation. Warn only, never block. One-time
       baseline coverage report to org/compiler-tools-log.md.
       Note: CTO spec allows splitting this to ADHC_COMPIL.004 (AE 0.7.0 owner).
       Recommend split — keeps CTO scope authoring-only, AE handles tooling.
  </scope>

  <acceptance_criteria>
    1. org/templates/prd_template.md exists with §5 Compiler Evidence as a
       required section. Template includes inline guidance referencing
       PRD_AUTHORING_PROTOCOL.md.
    2. docs/architecture/PRD_AUTHORING_PROTOCOL.md exists with full required-runs
       matrix + ≥2 worked examples (positive references from existing PRDs).
    3. CTO + COO prompt.md both reference the protocol explicitly (one line each).
    4. (Stretch) .tools/prd-evidence-check.sh lints existing PRDs and reports
       coverage to org/compiler-tools-log.md as a one-time baseline.
       (Or: split to ADHC_COMPIL.004 — AE 0.7.0 executes stretch criterion.)
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT require backfill of existing PRDs in v1 — forward-only mandate.</rule>
    <rule>Do NOT block commits on missing §5 in v1 — warn only.</rule>
  </do_not>

  <deliverables>
    <deliverable type="document">org/templates/prd_template.md</deliverable>
    <deliverable type="document">docs/architecture/PRD_AUTHORING_PROTOCOL.md</deliverable>
    <deliverable type="code">CTO + COO prompt.md updates</deliverable>
    <deliverable type="code">(Stretch or delegate to .004) .tools/prd-evidence-check.sh</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO when all non-stretch ACs complete</deliverable>
  </deliverables>
</task_order>
