<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-canplat-p3-1</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-08-06</date>
    <status>staged</status>
    <go_condition>GO fires from 2.0.0_SA_COO~Z when BOTH hold: (1) MDPF_CANPLAT.P2-1's config objects are landed, (2) MDPF_CANPLAT.P1-1's gold is emitting the A4 canonical keys. Build/design work may begin on this TO's reading list now; NO DEPLOY before the GO.</go_condition>
    <project_code>MDPF_CANPLAT</project_code>
    <supersedes>MDPF_CANRTE.P3-1 (body ADOPTED @a6ae64326 — L-2-checked CLEAN by COO~Z 2026-08-06; deltas below)</supersedes>
    <governing>PRD @24d3eb2f8 · CONTRACT @a3106d585 §D (D1–D9) — this TO IS §D</governing>
  </metadata>

  <standing_instruction>
    ⛔ PRD §0, VERBATIM — THE OPERATING INSTRUCTION FOR THIS ENTIRE PROGRAM:

    > **ANDREW-DIRECT, 2026-08-06, VERBATIM:**
    > *"This is exactly correct. I need you to persist this exactly as laid out here as a PRD and issue that
    > to COO for decomposition. I just terminated every fabric agent's session on this device aside from you
    > and mstr~z because I want them respawned with this being fresh context and instruction. **I do not want
    > them to go off the rails on hunting down errors, just do what is described here.**"*

    **BUILD WHAT §2 DESCRIBES. DO NOT HUNT ERRORS.**

    - **A number that surprises you is NOT a finding.** The business logic is **correct and live**. This is
      a **SHAPE** project.
    - **The only defects in scope are SHAPE divergences.** Everything else is out of scope, however
      interesting.
    - **If you find something that looks wrong: REPORT IT, DO NOT CHANGE IT.** One line to COO~Z. Then
      continue the work. Do not open an investigation. Do not widen a task order.
    - **Prior context is deliberately not being restored. Do not go looking for the previous session's
      threads.**

    > **TREATING A CORRECT NUMBER AS A FINDING IS HOW A WORKING PIPELINE GETS "FIXED."**

    SURPRISE CHANNEL: ONE LINE to 2.0.0_SA_COO~Z, subject beginning `SURPRISE:`, then continue.
  </standing_instruction>

  <objective>
    Make `opal-assets-mdpf-portal-publisher` the CONTRACT §D projector: 09:50 ET scheduled, complete
    before 10:00 ET (D1); reads the exact A4 canonical gold keys (D2); writes the 12
    `platinum/mdpf/{scope}/{type}.json` (D3); **NEVER PATCHES SHAPE** (D4); unchanged source → no rewrite
    (D5); per-key isolation (D6); immutable publish manifest (D7); completeness against the expected 12,
    bidirectional (D8); `json/mdpf/*` and the hyphenated legacy bell untouched (D9).
  </objective>

  <adoption>
    **The body of `MDPF_CANRTE.P3-1.publisher-correction.md` AS COMMITTED @a6ae64326 IS ADOPTED AS THIS
    TO's CONTENT** — context (measured defect, roster symmetry ruling, H8 per-field source-map read),
    compiler_tools_mandate, cross_domain_coordination, acceptance criteria 1–9 (incl. 2a's ordering, 3a's
    bidirectional enumeration, 6's five-limb form), scope, requirements, do_not — subject to these
    DELTAS, which win on conflict:

    - **Δ1 · D4 IS THE ROW MOST LIKELY TO BE VIOLATED — CTO-flagged. VERBATIM: "NEVER PATCHES SHAPE.
      Projects an already-canonical gold. Zero reshaping, renaming, or field synthesis."** If the folded
      fields are absent or scope-specific when they reach you, that is a P1-1 defect to report via the
      SURPRISE channel — **do not compensate in the publisher** (already in the adopted body; restated
      because it is the program's most-likely failure).
    - **Δ2 · THE EXEMPTION DENOMINATOR IS CONTRACT §B.** Everywhere the adopted body's criterion 6 says
      the exemption list / "spec §3," read **CONTRACT §B @a3106d585** — the closed field-path list. The
      comparator is CVO~Z's (MDPF_CANPLAT.G2); your per-key served-contract comparison consumes ITS
      pinned baseline, not a fresh one.
    - **Δ3 · EXPECTED SET UNDER R12:** the 12 canonical + the 2 standalone extras remain EXPECTED until
      their fold passes R2+R7 (adopted 2a says exactly this; R12 is its rubric row). The 3 stale
      underscore twins on the served surface are ENUMERATED as unexpected-but-present (adopted 3a),
      REPORTED, never deleted (NEVER#3).
    - **Δ4 · PROGRAM CODE:** references to MDPF_CANRTE resolve to MDPF_CANPLAT (P2-1/P1-1 = this
      generation's).
  </adoption>

  <acceptance_criteria>
    Adopted criteria 1–9 @a6ae64326 stand under the deltas. Rubric rows this TO must make PASS:
    - **R1** "12 objects exist at the 12 canonical platinum paths for the day — EXISTENCE ONLY, never
      reported as freshness" (adopted 3b binds: evaluated together with the source-hash and body reads).
    - **D5/R9** second run leaves ETags untouched; `unchanged` recorded. **"14/14 written" (or "12/12
      written") IS THE DEFECT, NOT THE PASS** (adopted criterion 1, verbatim force).
    - **D8** fixture: remove one scope → completeness non-green; a missing scope cannot discover itself.
    - **R12** both standalone extras still present until their fold passes R2+R7.
    - **R14** no served key moved, no semantic changed, nothing deleted — D9 oracle: key listing unchanged
      for `json/mdpf/*` + the hyphenated bell.
  </acceptance_criteria>

  <do_not>
    <rule>Everything in the adopted &lt;do_not&gt; @a6ae64326 — verbatim force (no deploy before config
    objects exist; no roster S3 leg; no served-output moves; LastModified/ETag never freshness evidence;
    no alarms/SNS/SES/monitors; no non-ASCII in the source map).</rule>
    <rule>⛔ NO DEPLOY BEFORE THE GO CONDITION READS TRUE — staged means staged.</rule>
    <rule>NO error-hunting (§0). SURPRISE: line to COO~Z, then continue.</rule>
    <rule>Commit to your lane on SITEZ; push is MSTR~Z's (:55–:00); never rebase.</rule>
  </do_not>

  <deliverables>
    <deliverable type="commit">Corrected publisher + tests + source-map role fix + TF, committed to your lane</deliverable>
    <deliverable type="document">Per-key served-contract comparison consuming G2's pinned baseline</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>
</task_order>
