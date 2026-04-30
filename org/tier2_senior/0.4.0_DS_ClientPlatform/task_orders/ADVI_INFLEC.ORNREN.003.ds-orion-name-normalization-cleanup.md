<task_order>
  <metadata>
    <id>ADVI_INFLEC.ORNREN.003.ds-orion-name-normalization-cleanup</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-30</date>
    <status>STAGED — Andrew Option B + divergence-rule confirmed 2026-04-30 PM ("yes it should be option B … the premise is that we dont add the INF_ prefix unless there is actually a change in the script from the BD version"). DS~A assigned. Andrew will activate when ready ("i'll get that up and running").</status>
    <lane_rationale>~A lane — historically owns INFLEC chain authoring (W4.* gold chain, ORNREN.001 author, INFGRD.003 chain rerun). Has deepest context on which orion scripts diverged from BD vs not.</lane_rationale>
    <project_code>ADVI_INFLEC</project_code>
    <theme>ORNREN follow-up — naming-debt cleanup surfaced post-ORNREN.001/.002</theme>
    <prd_ref>None — captured directly from 2026-04-30 ad-hoc audit during ADHC_COMPIL.011 INF script-id resolver scope review. Andrew direction: stage it.</prd_ref>
    <effort>2–4 days when activated (includes risk-shaped S3 + dispatch verification — not 1 day rename-only)</effort>
    <gates_on>
      (1) INFSHIP Phase 3 RD smoke + Andrew V2 sign-off COMPLETE.
      (2) INFGRD chain ≥7 days steady-state with no rerun; otherwise rename-during-active-investigation = self-inflicted churn.
      (3) ADHC_COMPIL.011 (INF script-id resolver) COMPLETE — the resolver currently masks the inconsistency by accepting any `INF_*` form; once it lands and ID-form lookups work, naming inconsistency becomes the user-visible problem rather than a tool-resolution problem.
    </gates_on>
    <gates_for>None — purely cleanup. v1 portal LIVE; not blocking ship.</gates_for>
  </metadata>

  <objective>
    Normalize the data/orion/scripts/gold/ corpus to a single canonical
    naming convention. Today the directory has THREE coexisting generations:

    (1) **Vendor convention (no prefix)** — ORNREN.001 result: A_00, B_00,
        C_00, D_00c, D_02, D_04, 09, build_canonical_prices. ~25 files.
    (2) **Holdover I_ prefix** — missed by ORNREN.001 rename spec:
        I_D00.portal_aggregates.py, I_D00b.portal_timeseries.py,
        I_D03.composition_artifacts.py. 3 files.
    (3) **Re-prefixed INF_** — added by post-ORNREN INFSHIP/INFGRD work:
        INF_09, INF_A_*, INF_B_*, INF_C_*, INF_D_* (incl. new
        D_05/D_06/D_07/D_08), INF_build_canonical_prices.py,
        INF_run_c_chain.py. ~30 files.
    (3a) **Double-prefix INF_I_** — worst case, mixes both prior
         conventions: INF_I_D00, INF_I_D00b, INF_I_D00c, INF_I_D02b,
         INF_I_D02d, INF_I_D03. 6 files.

    Net: ~64 files where the 25 vendor-convention names and ~30 INF_-prefixed
    names are partial duplicates. The 3 holdover I_* files plus 6 INF_I_*
    files are the most egregious — neither convention applies.

    Cleanup goals (priority order):
    1. Decide canonical convention with Andrew (vendor-no-prefix vs
       firm-prefix INF_) before any rename — this is the load-bearing
       decision, not the rename mechanics.
    2. Eliminate INF_I_* double-prefix entirely (no convention defends it).
    3. Eliminate I_D00*/I_D03 holdovers that ORNREN.001 missed.
    4. Resolve the partial duplication between vendor-convention and
       INF_-prefix copies — pick one, delete the other.
    5. Update orion-gold-dispatch.sh + S3 (s3://opal-data-inf/code/gold/) +
       any cross-references in lib/ + comp-pipescript graph.
  </objective>

  <canonical_convention>
    **Andrew ruling 2026-04-30 PM — Option B with divergence rule.**

    The convention for `data/orion/scripts/{gold,silver,bronze}/`:

    - **No prefix** (e.g. `A_00.accounts_dimension.py`) = the Orion script
      is logically equivalent to the BD version at `data/black_diamond/scripts/gold/A_00.accounts_dimension.py`.
      Same operations, same shape; only the bucket pointer / config-driven
      env differs. The directory location (`data/orion/`) does the
      firm-scoping; the prefix would be redundant.
    - **`INF_` prefix** (e.g. `INF_D_05.activity_scan.py`) = the script
      has Inflection-specific divergent logic that the BD version doesn't
      have, OR the script is novel to the Orion pipeline (e.g. new
      dimensions like activity_scan, cash_drag, concentration_risk that
      have no BD sibling).

    The prefix carries information. Its presence signals "this script
    diverges from the BD pattern; read it carefully." Its absence signals
    "this script is the same as BD's — if you change BD's, propagate
    here." This is self-documenting and matches how directory-scoped
    firm conventions work elsewhere in the repo.

    **Eliminated entirely (no convention defends them):**
    - `INF_I_*` double-prefix (6 files: INF_I_D00, INF_I_D00b, INF_I_D00c,
      INF_I_D02b, INF_I_D02d, INF_I_D03)
    - `I_*` single-prefix holdovers from ORNREN.001 (3 files: I_D00,
      I_D00b, I_D03)

    **Decision criterion per duplicate pair** (e.g. `A_00.py` AND
    `INF_A_00.py` both exist today): diff against the BD equivalent at
    `data/black_diamond/scripts/gold/A_00.*.py`. Three outcomes:

    1. **Identical or trivially different** (bucket name only, env var
       only, comment-only changes) → keep the no-prefix version, delete
       `INF_*`. Note in session log what the trivial difference was.
    2. **Meaningfully divergent** (Inflection-specific logic, additional
       columns, different transform, different schema handling) → keep
       the `INF_*` version, delete the no-prefix. Document the divergence
       in the session log so future readers know why the prefix is there.
    3. **Both diverge from BD AND from each other** (the worst case;
       partial duplication during INFSHIP rapid iteration) → escalate
       to Andrew + CTO before resolving. Do not unilaterally pick.

    Files novel to Orion (no BD sibling — e.g. INF_D_05 activity_scan,
    INF_D_06 cash_drag, INF_D_07 concentration_risk, INF_D_08
    nmec_nmnc_nna): keep `INF_` prefix uniformly. They are by definition
    divergent from BD because BD has no equivalent.
  </canonical_convention>

  <scope>
    Step 1 — Per-pair divergence audit:

    For every script in data/orion/scripts/gold/ that has both a
    no-prefix and `INF_` form (e.g. `A_00.accounts_dimension.py` AND
    `INF_A_00.accounts_dimension.py`), produce a divergence report:

    - `diff data/black_diamond/scripts/gold/<bd>.py data/orion/scripts/gold/<no-prefix>.py`
    - `diff data/black_diamond/scripts/gold/<bd>.py data/orion/scripts/gold/INF_<name>.py`
    - For each pair, classify per the canonical convention:
      - **Identical-or-trivial** → keep no-prefix, delete INF_*
      - **Meaningfully divergent** → keep INF_*, delete no-prefix
      - **Both diverge from BD AND from each other** → ESCALATE to Andrew
        + CTO before resolving. Do not unilaterally pick.

    Capture the divergence-audit table in the session log. Each row:
    `<script_id> | <pair: no-prefix exists? | INF_ exists?> | BD diff |
    INF diff | classification | resolution | rationale`.

    Step 2 — INF_I_* and I_* elimination:

    All 6 INF_I_* files (INF_I_D00, INF_I_D00b, INF_I_D00c, INF_I_D02b,
    INF_I_D02d, INF_I_D03) and all 3 I_* holdovers (I_D00, I_D00b,
    I_D03) get resolved per Step 1's logic against their BD equivalents
    if any. If no BD equivalent exists (the I_D00* / D00b case may be
    Orion-novel), keep with `INF_` prefix per the novel-to-Orion rule.

    Step 3 — File rename (git mv preserves history):

    Apply the Step 1 + Step 2 resolutions:
    - Rename surviving files to canonical name per convention
    - Delete losing-side duplicates (`git rm`)
    - Eliminate INF_I_ double-prefix entirely (rename to INF_ if
      surviving, delete if losing-side)

    Step 4 — Internal cross-reference updates:

    Grep for every renamed name across data/orion/, lib/,
    orion-gold-dispatch.sh, lib/utils/. Update every reference.
    ORNREN.001 caught most of these for the vendor-convention pass;
    expect comparable scope, plus the new INF_*/INF_I_* references that
    INFSHIP/INFGRD added.

    Step 5 — orion-gold-dispatch.sh:

    Update CHAIN definition lists. Verify every named script in the
    dispatch chain matches a real file post-rename.

    Step 6 — comp-pipescript graph + comp-validate / comp-freshness config:

    - Run `comp-build` to refresh the graph cache.
    - Walk `gold_validate_config.yaml` and (post-.012) `gold_freshness_config.yaml`
      under data/orion/scripts/gold/. Update `producer_script:` fields
      where the producer script-id changed.

    Step 7 — S3 sync:

    - Upload renamed files under s3://opal-data-inf/code/gold/ AND
      s3://opal-data-inf/code/silver/ (both layers).
    - Delete obsolete S3 keys ONLY after MATCH verification + 24h soak.
    - Use `aws s3api list-objects-v2` to confirm the post-state.

    Step 8 — Verification:

    - `comp-pipescript deployed` against every renamed script: MATCH.
    - One full Orion gold chain dispatch on QA runner; confirm zero
      missing-file errors. Tag chain run as "ORNREN.003 verification" in
      session log.
    - `comp-validate` against every artifact with config: PASS or
      NO_CONFIG (post-.015), no MISSING_ARTIFACT.

    Step 9 — Documentation:

    - Update ADVI_INFLEC PRD and any active session-log references to
      use the canonical names.
    - Add one entry to org/compiler-tools-log.md per renamed script.
    - **Document the divergence rule in `data/orion/scripts/README.md`**
      (create if absent) so future agents know the convention without
      reading this TO. One paragraph: "Files in this directory carry
      the `INF_` prefix only when they diverge from the BD equivalent;
      no-prefix files are equivalent to BD's, just bucket-pointed at
      Orion." This is the structural fix that prevents convention drift
      from re-accumulating.
  </scope>

  <acceptance_criteria>
    1. Divergence-audit table committed in the session log: every
       duplicate-pair script_id classified as identical-or-trivial,
       meaningfully-divergent, or escalated. No pair left unclassified.
    2. Zero files in data/orion/scripts/gold/ + data/orion/scripts/silver/
       carry the `INF_I_*` double-prefix.
    3. Zero files carry the `I_` single-prefix (the 3 ORNREN.001
       holdovers gone).
    4. No partial-duplicate pairs remain (e.g., `A_00.py` and
       `INF_A_00.py` cannot both exist for the same logical script).
    5. Every surviving file follows the divergence rule:
       - No-prefix files have ≤ trivial diff against the BD equivalent
         (verifiable: `diff` shows only bucket name, env var name,
         comment whitespace).
       - `INF_*` files have meaningful divergence from BD OR are novel
         to Orion (no BD equivalent). The divergence/novelty is
         documented in the file header comment AND the session log.
    6. Any "both diverge" cases were escalated to Andrew + CTO with
       resolution captured in MCP exchange + session log.
    7. orion-gold-dispatch.sh CHAIN list points to live filenames; full
       chain dispatch on QA runner completes without missing-file errors.
    8. comp-pipescript deployed MATCH for every renamed script.
    9. S3 keys synced under s3://opal-data-inf/code/{gold,silver}/;
       obsolete keys deleted post-MATCH + 24h soak.
    10. gold_validate_config.yaml + (post-.012) gold_freshness_config.yaml
        updated with new `producer_script:` values where applicable.
    11. comp-build cache refreshed; `comp-pipescript io <new-name>` works;
        old names exit 1 with closest-match suggestion (per .008 + .011
        patterns).
    12. ADVI_INFLEC PRD updated to reference canonical names.
    13. **`data/orion/scripts/README.md` documents the divergence rule**
        as the canonical convention. Future agents read it; convention
        drift cannot re-accumulate via fork-and-rename.
    14. Session log documents every file rename + each S3 key
        upload/delete + the QA dispatch verification.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT modify any script logic during rename — pure rename + delete pass. Bug discovery during the divergence audit: flag as separate TO. The exception is file-header comment additions documenting why an `INF_*` file diverges from BD (per AC5).</rule>
    <rule>Do NOT pick the no-prefix or INF_ side of a duplicate pair without running the diff against BD. The convention is divergence-driven, not name-driven.</rule>
    <rule>Do NOT silently resolve a "both diverge from BD AND from each other" case — escalate to Andrew + CTO. Picking unilaterally risks shipping the wrong logic.</rule>
    <rule>Do NOT delete S3 obsolete keys until comp-pipescript deployed MATCH on the new keys + 24h soak window passes. Allow rollback if dispatch issues surface.</rule>
    <rule>Do NOT activate until INFSHIP Phase 3 RD smoke + Andrew V2 sign-off complete AND INFGRD chain has ≥7 days steady-state. Renaming during active investigation creates self-inflicted churn.</rule>
    <rule>Do NOT split into sub-TOs by layer (gold vs silver) — atomic transition is safer than partial. Either ship the whole cleanup or none.</rule>
    <rule>Do NOT skip the README.md documentation step (AC13). The structural fix that prevents convention drift IS the README; without it, the next INFSHIP-class push will re-accumulate the same mess.</rule>
    <rule>Do NOT take on COMP_LEARNS scope — workspace-side only.</rule>
  </do_not>

  <deliverables>
    <deliverable type="decision">Andrew Option A vs Option B ruling captured in session log</deliverable>
    <deliverable type="code">All renames committed via git mv to preserve history</deliverable>
    <deliverable type="code">orion-gold-dispatch.sh CHAIN updated</deliverable>
    <deliverable type="code">lib/ helpers + cross-references updated</deliverable>
    <deliverable type="code">gold_freshness_config.yaml + gold_validate_config.yaml producer_script fields updated</deliverable>
    <deliverable type="infra">S3 keys synced under s3://opal-data-inf/code/{gold,silver}/; obsolete keys deleted</deliverable>
    <deliverable type="document">Session log: per-file rename table, diff resolutions for partial-duplicate pairs, S3 sync log, QA dispatch verification output</deliverable>
    <deliverable type="document">ADVI_INFLEC PRD update reflecting canonical names</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC1 Andrew ruling capture, AC2-AC5 directory listings (pre + post), AC6 dispatch run output, AC7 deployed MATCH summary, AC8 S3 listing, AC10 spot-checks</deliverable>
  </deliverables>

  <activation_protocol>
    Andrew has already ruled on the canonical convention (Option B with
    divergence rule, 2026-04-30 PM). Activation gate is operational, not
    decisional:

    1. Wait for gates: INFSHIP Phase 3 + Andrew V2 sign-off COMPLETE,
       INFGRD chain ≥7 days steady-state with no rerun, ADHC_COMPIL.011
       (INF script-id resolver) COMPLETE.
    2. When gates clear, Andrew flips status from STAGED to OPEN ("i'll
       get that up and running") and dispatches DS~A directly.
       Alternatively, COO can MCP Andrew when gates clear to confirm
       activation.
    3. DS~A executes per scope. The divergence audit (Step 1) is the
       front-loaded effort; expect ~half the total time on auditing,
       half on rename mechanics + S3 + verification.
    4. Effort ~2–4 days; tag the rename commit `ornren-cleanup-{YYYYMMDD}`
       for git history clarity.
    5. Any "both diverge" escalations during the audit pause execution
       until Andrew + CTO resolve.
  </activation_protocol>

  <historical_context>
    ORNREN.001 (DS, 2026-04-22, complete 2026-04-27) renamed 28 I_* files
    to vendor-convention; missed I_D00, I_D00b, I_D03 (~3 files).
    ORNREN.002 (AE, complete 2026-04-27 + re-shipped 2026-04-29
    `f6ccb392c`) handled dispatch wiring + EC2 manifest.

    INFSHIP (2026-04-28) and INFGRD (2026-04-29 to -30) added new gold
    scripts under INF_* convention (D_05 activity_scan, D_06 cash_drag,
    D_07 concentration_risk, D_08 nmec_nmnc_nna, plus INF_I_* artifacts
    that retained the I_ middle segment from earlier drafts). The INF_*
    convention was applied inconsistently — some files got renamed in
    place to INF_*, others were created fresh; the INF_I_* double-prefix
    is the historical fingerprint of that inconsistency.

    Audit surfacing: 2026-04-30 PM during ADHC_COMPIL.011 INF script-id
    resolver scope review. Andrew direction: capture as TO, defer
    activation, do not block v3.
  </historical_context>
</task_order>
