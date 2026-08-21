<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-21-inf-d04-aua-rename-fe</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform (portal lane)</issued_to>
    <date>2026-08-21</date>
    <status>pending -- STARTS at the lane's next working block. A ONE-LINER, deliberately cut as its own TO because it is a DIFFERENT REPO, a DIFFERENT LANE and a DIFFERENT MECHANISM from the DS-side rename (INF_D04.AUARENAME at 0.4.0_DS_ClientPlatform). ANDREW-DIRECT authorization, verbatim "rec approved" at the 4.0.0_SA_CRO terminal ~0052Z 2026-08-21 (record: org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20260821_D04_RENAME_AUA_IDENTITY_RESIDUAL.md; routing relayed 63977).</status>
    <project_code>ADVI_INFDRF</project_code>
  </metadata>

  <objective>
    Rename the TYPED-BUT-UNRENDERED field on the portal's HeaderTotal type to follow INF's D_04
    served-field rename: `unreconciled_aua` -> `aua_identity_residual`. The type declares a field
    the UI does not render today (3.0.0_SA_CVO's renderer census: portal/src carries ZERO
    references to the field under either name -- the type declaration is the only site).
  </objective>

  <context>
    WHY THIS IS A SEPARATE TO AND NOT A LINE IN THE DS ONE: portal is its own repo (a submodule),
    its own lane, and its own promote mechanism -- folding it into the data-side act would put two
    mechanisms behind one close, which is how half of a two-mechanism act silently does not happen.
    NEITHER SIDE BLOCKS THE OTHER: the field is UNRENDERED, so there is no ordering hazard in
    either direction -- a type naming a key the API has not renamed yet renders nothing, and a
    renamed served key with a stale type renders nothing either. Land it whenever convenient.
    ⚠ PORTAL LAW (Rule 19): the portal main worktree stays on DEV, always. Found it on PROD?
    `cd portal && git checkout DEV` before any portal work -- never work around via .runtmp copies.
    Promotes run in an ephemeral worktree via the /prod-deploy skill; this TO does NOT promote.
    ⚠ FIND THE TYPE AT SOURCE, do not trust this TO's path guess: locate the HeaderTotal
    declaration yourself (it is a type/interface field, not a rendering site) and state the file
    and line you changed in the close. If the field does not exist under either name, say so in
    one line and close NO-OP -- that is a true and useful answer, not a failure.
  </context>

  <compiler_tools_mandate>
    Before commit: `comp-transform schema-check HeaderTotal` (MISSING = runtime undefined) and
    the dependency-graph check Rule 20(b) requires ahead of ANY frontend change; a repo-scoped
    search for BOTH names to prove the type declaration is the only site (denominator printed).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - 0.4.0_DS_ClientPlatform: owns the served-side rename (INF_D04.AUARENAME); they state their
      landed key name when it deploys at the next scheduled INF run. You do not wait for it.
    - 3.0.0_SA_CVO: their renderer census is the basis for "typed, unrendered" -- cite it, do not
      re-run it.
    - No NEVER#3 leg here: this changes no served output. (The served-side act carries it.)
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is the portal TYPE rename as cut -- F1 the edit, F2 the
    denominator, F3 no-render-change, F4 close; exhaustive; the served key, the promote, and any
    rendering work are OUTSIDE.)
    F1  The HeaderTotal field renamed `unreconciled_aua` -> `aua_identity_residual`, with the
        actual file:line stated in the close (found at source, not from this TO).
    F2  DENOMINATOR PRINTED: a repo-scoped search for both names across portal/src shows the type
        declaration as the ONLY site (expected 1 before / 1 after, 0 renderers) -- if any renderer
        appears, STOP and surface: the "typed, unrendered" premise would be false and this becomes
        a display change, which is a different act.
    F3  No render change: build/typecheck clean on DEV; nothing shipped to PROD by this TO.
    F4  Proof instance VALID rc=0 positional F1-F4 (rc UNPIPED), carrying F2's counts as its
        evidence; close to 2.0.0_SA_COO cc 0.4.0_DS_ClientPlatform + 3.0.0_SA_CVO.
        (I first cut this TO saying "no proof instance required -- a one-line type edit does not
        warrant one." The commit-gate REFUSED it: a new task order carries a proof_of_spec, no
        size exemption. The gate is right and the exemption was mine to not invent -- a one-line
        edit is exactly where a skipped control is cheapest to skip and least noticed.)
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>F1,F2,F3,F4</expected_criteria>
    <instance_path>org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/INF_D04.AUARENAME-FE_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">DEV only; no promote. If F2's search finds a renderer, stop and surface rather than proceeding -- the premise, not the edit, would be what changed. Surprise channel: one line to COO.</requirement>
  </requirements>
</task_order>
