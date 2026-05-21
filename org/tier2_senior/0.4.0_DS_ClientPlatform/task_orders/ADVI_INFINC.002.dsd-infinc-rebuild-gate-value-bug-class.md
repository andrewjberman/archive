<task_order>
  <metadata>
    <id>ADVI_INFINC.002</id>
    <slug>dsd-infinc-rebuild-gate-value-bug-class</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <!-- COMPLETE + CTO RAVC-accepted 2026-05-21: commit 43e13faf6 — DS 0.4.0 took the PREFERRED path; added lib/skip_gate.rebuild_requested() shared helper, converged all 5 Pattern-B gates (INF_C_02/C_03/D_05/D_06/D_09) onto it, retired the re-inline-drift root cause; ds-commit-gate + comp-pipescript io clean; S3-deployed + verified. AC1-AC4 met. NOTE: this TO is mis-numbered .002 (collides with the COMPLETE Pattern-A migration ADVI_INFINC.002) — flagged to COO for renumber to the next free serial. -->
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO — CTO-ruled (the ADVI_INFINC follow-on home for the systemic INFINC_REBUILD gate-value bug). DS~D lane. NOTE: if the ~D lane has no live agent when this is read (the broker has shown no live `0.4.0_DS_ClientPlatform~D`), it re-routes to the base `0.4.0_DS_ClientPlatform` lane — same phantom-lane handling as ADVI_INFGRO.009 (~C). The 4 in-scope scripts are INF_C/INF_D Client-Platform gold scripts; base DS 0.4.0 just fixed the sibling INF_C_02, so base is a valid fallback owner. COO re-routes on a loop tick if ~D stays unpicked.</dispatch_unblock_condition>
    <project_code>ADVI_INFINC</project_code>
    <priority>P2 — NOT urgent (no active rebuild depends on the 4 scripts right now) but MUST land before the next rebuild chain run, else that run silently no-ops those 4 dims.</priority>
    <sla>~30-60 min — 4 one-line-class fixes (or a small helper-consumption refactor); the work is small, the verification is the substance.</sla>
  </metadata>

  <references>
    <origin>Surfaced by ADVI_INFGRO.009 (2026-05-20): the .009 rebuild trigger was defective two ways; the second — INF_C_02's inline `_force_rebuild` gate checked INFINC_REBUILD == 'true' while the dispatch + `lib/skip_gate.py` emit the canonical `'1'` — was fixed for INF_C_02 in commit 4ccbce567. DS 0.4.0 then found the SAME mismatch in 4 more inline gates. CTO ruled (2026-05-20) this is an ADVI_INFINC mechanism-consistency defect (the INFINC_REBUILD canonical-value contract is ADVI_INFINC's) and the home is an ADVI_INFINC follow-on TO, DS~D lane.</origin>
    <canonical>`lib/skip_gate.py` defines the canonical INFINC_REBUILD value as `'1'`; the orion-gold-dispatch.sh dispatch exports `INFINC_REBUILD="1"`. Any gate checking `== 'true'` is dead against the canonical value.</canonical>
  </references>

  <context>
    The INFINC_REBUILD rebuild-gate has its canonical value `'1'` (lib/skip_gate.py + the dispatch emit). FIVE inline Pattern-B `_force_rebuild` gates re-implement the check inline instead of consuming the shared helper; 4 of the 5 check `== 'true'` — so a chain-driven rebuild silently no-ops those 4 dimensions (they stay append-only even when a full rebuild is requested). INF_C_02 (the 5th) was fixed under ADVI_INFGRO.009 (4ccbce567). This TO fixes the remaining 4. It is a latent-defect-class fix — there is no live incident, but the next rebuild chain run would silently mis-process those 4 dims without it.
  </context>

  <scope>
    <in_scope>
      The 4 still-bugged inline `_force_rebuild` gates:
      - INF_C_03.account_performance.py:150
      - INF_D_05.client_top_holdings.py:379
      - INF_D_06.client_timeseries.py:571
      - INF_D_09.account_timeseries.py:316

      FIX SHAPE (CTO-specified — structural-over-cultural; the TO author picks at execution based on the `lib/skip_gate.py` helper's call signature):
      - PREFERRED: make the 4 gates CONSUME the canonical `lib/skip_gate.py` gate helper rather than re-inline the value comparison — this is the durable fix (a value-align alone leaves the next re-inline free to reintroduce the bug). IF helper-consumption is a low-delta change (the helper's signature drops in cleanly), do that — AND ideally retrofit INF_C_02's 4ccbce567 inline fix to consume the helper too, so all 5 gates are uniform.
      - FALLBACK: IF helper-consumption is materially bigger than a small refactor, ship the 4 one-line `'true'` -> canonical-`'1'` value-aligns now (accept the canonical `'1'` + truthy synonyms, matching the 4ccbce567 INF_C_02 fix) + add a tracked `<follow_up>` note in the session log to converge all 5 gates onto the helper later.
      Flag in the session log which path was taken + why (the helper signature inspection).
    </in_scope>
    <out_of_scope>
      - INF_C_02 — already fixed (4ccbce567); only RETROFIT it to the helper IF the preferred path is taken (and even then it is optional polish, not required).
      - orion-gold-dispatch.sh / the dispatch-side INFINC_REBUILD production — already correct (it emits `'1'`); do not touch it.
      - Any rebuild-chain re-run — this TO is the code fix only; it lands before the next scheduled rebuild, it does not trigger one.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the edits">
      <step>
        <run>comp-pipescript io  on each of the 4 gold scripts (INF_C_03, INF_D_05, INF_D_06, INF_D_09)</run>
        <expect>The load list + COLUMN GAPS + portal consumers for each — confirm the `_force_rebuild` gate edit does not sit near a column-gap or a consumer surprise; scope the change precisely.</expect>
        <if_mismatch>If a script is not a comp-pipescript node, fall back to a direct source read at the cited line + document.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh  on each of the 4 .py files</run>
        <expect>All three checks exit 0 (py_compile + ds-precommit-check + ruff py39) — CLAUDE.md Rule 14.</expect>
        <if_mismatch>Fix the surfaced issue before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>grep the 4 scripts' gate lines + (if a rebuild dry-run is cheap) a dry-run confirming the gate now fires on INFINC_REBUILD='1'</run>
        <expect>All 4 gates now accept the canonical `'1'` (via the helper or the value-align); a `INFINC_REBUILD='1'` rebuild would now genuinely re-materialize those 4 dims.</expect>
        <if_mismatch>If a gate still reads `== 'true'`, the fix did not land on that script — re-apply before signalling done.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>The fix changes only the rebuild-gate's value comparison — it affects which dims a FUTURE rebuild chain re-materializes. Historical partitions are unaffected (they were correctly append-only-maintained); no backfill. The next scheduled rebuild chain run picks up the corrected gates automatically. No silver/bronze touched.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    Origin is ADVI_INFGRO.009 (INF_C_02 sibling fix 4ccbce567) — read it for the canonical pattern. `lib/skip_gate.py` is the shared-helper source. No shared S3 artifact written. No other active TO touches these 4 gate lines.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">All 4 inline `_force_rebuild` gates (INF_C_03:150, INF_D_05:379, INF_D_06:571, INF_D_09:316) no longer dead against the canonical INFINC_REBUILD='1' — either consuming the `lib/skip_gate.py` helper (preferred) or value-aligned to accept `'1'` (fallback). The path taken + the helper-signature reasoning recorded in the session log.</ac>
    <ac id="AC2">If the fallback path was taken: a tracked `<follow_up>` note to converge all 5 gates onto the shared helper later. If the preferred path: optionally INF_C_02 retrofitted to the helper for uniformity.</ac>
    <ac id="AC3">Phase-1 comp-pipescript io + Phase-2 ds-commit-gate (exit 0) + Phase-3 verification reproduced in the session log Compiler Tools section. Committed + pushed + push-confirmed on origin/CLOUD.</ac>
    <ac id="AC4">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The 4 gate fixes (helper-consumption or value-align), committed + push-confirmed.
    - Session log with Compiler Tools section + the path-taken rationale + (if fallback) the follow-up note.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT touch orion-gold-dispatch.sh / the dispatch-side INFINC_REBUILD production — it is already correct.</rule>
    <rule>Do NOT trigger a rebuild chain — this TO is the code fix only.</rule>
    <rule>Every gold-script edit: `from __future__ import annotations` first import stays intact (CLAUDE.md Rule 15); ds-commit-gate before commit (Rule 14).</rule>
    <rule>No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
