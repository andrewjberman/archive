<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-canplat-g2</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>3.0.0_SA_CVO~Z</issued_to>
    <date>2026-08-06</date>
    <status>pending</status>
    <project_code>MDPF_CANPLAT</project_code>
    <supersedes>none (new instrument). MDPF_CANRTE.P0-1's frozen evidence (incl. per-key schema baseline @db5f37b11) and P0-6's closed record (@49e236bff) are ADOPTED as inputs.</supersedes>
    <governing>PRD @24d3eb2f8 §5.5 (Guard 2) · CONTRACT @a3106d585 (§B = the closed field-path list; §E rows R1/R2/R7/R12)</governing>
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
    (For this TO specifically: a comparator DIFF outside §B is a REGRESSION REPORT to COO~Z — that is the
    channel working, not error-hunting. You report; DS~Z/AE~Z fix under their TOs; you never fix.)
  </standing_instruction>

  <objective>
    Build and exercise the program's verification instruments, as the seat CTO~Z named to hold Guard 2's
    line: (1) the **R7 regression comparator with all five limbs**, consuming **CONTRACT §B as Guard 2's
    CLOSED FIELD-PATH LIST**; (2) the **R1 existence** and **R2 key-set-identity** instruments; (3) the
    **R12 nothing-retires-early** verification. These instruments adjudicate the program's completion on
    one unattended scheduled cycle — build them FIRST, so they exist before any gold diff lands.
  </objective>

  <guard_2_verbatim>
    ⛔ **GUARD 2 IS FIVE REQUIREMENTS, NOT ONE SENTENCE (PRD §5.5). CARRY ALL FIVE OR CARRY NONE:**
    - **VALUE-IDENTICAL PER JSON PATH**, not byte-identical, under a **declared canonicalisation** (sorted
      keys, normalised number formatting, explicit unicode handling). *"Byte" is a FILE property; §4
      changes the shape, so a byte criterion fires on everything, reads as noisy, and gets weakened.*
    - **EXERCISED AGAINST A DELIBERATE MUTATION**, shown to **FAIL and LOCALISE**, before any PASS is
      citable. *A comparator that passes everything is indistinguishable from a broken one.*
    - **BASELINE PINNED TO EXPLICIT S3 VersionIds AT A STAMPED INSTANT.** "Today's served artifacts" is a
      moving target — 444 objects archived at 21:42Z on 08-06, and a baseline frozen at 21:01Z moved 41
      minutes later. Versioning is on; this is free.
    - **ABSENT vs NULL vs ZERO are THREE STATES.** *Absent is never zero.*
    - **THE EXEMPTION SET IS A CLOSED FIELD-PATH LIST THE COMPARATOR CONSUMES AS DATA** — and per CTO~Z's
      handoff @a3106d585, **that list IS CONTRACT §B**: *"Every field named in §B is either a canonical
      field or an explicit exemption. A field not in §B must be value-identical to the pinned baseline — a
      diff outside §B is a REGRESSION."* Prose is arguable exactly when someone wants a diff excused; the
      list is machine-consumed or the criterion is decorative.
  </guard_2_verbatim>

  <acceptance_criteria>
    1. **R7, QUOTED AS THE ROW:** "REGRESSION TEST — all five limbs. PASS iff value-identical per JSON
       path · declared canonicalisation · mutation shown to FAIL and LOCALISE · baseline pinned to
       VersionIds at a stamped instant · absent≠null≠zero." **No PASS from this comparator is citable by
       anyone until its mutation exercise is on the record** (F: "a regression test that never failed" is
       one of the six things done is NOT).
    2. **THE §B FIELD-PATH LIST EXISTS AS A COMMITTED MACHINE-CONSUMED ARTIFACT** (data file, not prose),
       extracted from CONTRACT §B @a3106d585, consumed by the comparator at run time. Its derivation
       commit is cited in every comparator report.
    3. **THE BASELINE MANIFEST EXISTS**: every compared served key with its explicit S3 VersionId, ETag,
       and the stamped pin instant. Re-pins are new manifests, never edits.
    4. **THREE-STATE HANDLING IS EXERCISED, NOT ASSERTED**: fixtures where a field is absent, null, and
       zero produce three DISTINCT verdicts, on the record, before first real use.
    5. **R1 IS REPORTED AS EXISTENCE AND NEVER AS FRESHNESS** — 12 files at 12 known paths is identical
       whether fresh or frozen; the wording of every R1 report says "existence."
    6. **R2 INSTRUMENT**: per artifact type, key-set set-diff across all four scopes = ∅ is the PASS;
       any non-empty diff is reported with the exact paths.
    7. **R12 VERIFICATION**: both standalone extras (`cottonwood/account-units.json`,
       `global/non-model-assets.json`) verified still present until their fold passes R2+R7; their
       eventual retirement is Andrew's act, never this program's.
    8. **DENOMINATORS PRINTED on every scan** (keys enumerated, fields compared, dates covered) — a
       filtered result over a truncated listing is indistinguishable from a real absence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-which "how do I enumerate served platinum keys with versions"</run>
      <expect>Routes to the canonical tool; if none fits, rail-checked s3api list-object-versions with
      denominator printed (auto-paginate, never --no-paginate, never --query length()).</expect>
    Phase 2 — during build:
      <run>comp-validate (if a config exists for comparator artifacts) / positive+negative controls in
      isolated invocations</run>
      <expect>The mutation limb IS the negative control; run it isolated from the PASS run.</expect>
    Phase 3 — reporting:
      <run>Second oracle before any result that would OPEN a big finding or CLOSE an open question
      (PRD-adopted 9f discipline)</run>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>Served platinum surface `opal-data-portal-v2/platinum/mdpf/*` (read-only to you)</shared_resource>
    <also_in_to>MDPF_CANPLAT.P3-1 (its per-key comparison consumes YOUR pinned baseline)</also_in_to>
    <required_action>You are READ-ONLY on served surfaces. Pin the baseline BEFORE tomorrow's 09:50 ET
    publisher cycle if practicable; either way the pin instant is stamped and explicit.</required_action>
    <shared_resource>Declared canonicalisation + mutation fixture</shared_resource>
    <also_in_to>MDPF_CANPLAT.P1-1 (DS~Z supplies jointly on request)</also_in_to>
    <required_action>MCP 0.4.0_DS_ClientPlatform~Z; the canonicalisation is DECLARED once, in your
    committed artifact, and both TOs cite it.</required_action>
  </cross_domain_coordination>

  <do_not>
    <rule>DO NOT write, move, or delete ANY served key. Read-only. NEVER#3 binds absolutely.</rule>
    <rule>DO NOT report a comparator diff as a defect-to-fix — it is a REGRESSION REPORT to COO~Z;
    DS~Z/AE~Z own fixes under their TOs.</rule>
    <rule>DO NOT collapse Guard 2 to "byte-compare against served artifacts" in any report, summary, or
    downstream citation — that is the version that self-destructs.</rule>
    <rule>NO standing comparator SERVICE — this is a run-and-read QA instrument executed per verification
    event, not a scheduled monitor (alarm moratorium + no-shadow rule both bind).</rule>
    <rule>NO error-hunting (§0). SURPRISE: line to COO~Z, then continue.</rule>
    <rule>Commit to your lane on SITEZ; push is MSTR~Z's (:55–:00); never rebase; scratchpad for working
    files.</rule>
  </do_not>

  <deliverables>
    <deliverable type="commit">Comparator + §B field-path list artifact + baseline manifest, committed to your lane</deliverable>
    <deliverable type="document">Mutation exercise record (FAIL + LOCALISE shown) + three-state fixture record</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>
</task_order>
