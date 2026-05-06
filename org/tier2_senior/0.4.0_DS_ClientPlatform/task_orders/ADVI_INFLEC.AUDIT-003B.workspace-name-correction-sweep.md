<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.AUDIT-003B</id>
    <project>ADVI_INFLEC</project>
    <title>Workspace categorical name correction — joe_brandenburg (replace contaminated surface tokens across 22 files)</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-06</issued_date>
    <status>complete</status><!-- CLOSED 20260506T~1355Z by 1.0.0_SA_CTO RAVC4 ACCEPT. Commits a4e505460 + 23925b518 pushed 873951a32..23925b518. All ACs PASS per CTO adjudication. AC1/AC3 quasi-pass ruled PASS: meta-documentation not contamination. --><!-- Direct CTO TO authoring per Andrew authorization 2026-05-06; recovery from prior session context-poisoning incident. COO will not communicate to ~A in the interim. -->
    <priority>high</priority>
    <estimated_effort>~30-45 minutes mechanical (no design work — purely categorical replacement)</estimated_effort>
  </metadata>

  <context>
    The advisor's correct name is **joe_brandenburg**. A prior agent session generated a corrupted surface token (the wrong name) and propagated it across 22 files in this workspace before the contamination was caught. The S3 production prefix `platinum/advisors/` is clean and uses the correct key. The QA prefix `qa/advisors/` has a stray contaminated key path which AE 0.6.1 will clean up under separate dispatch — that is OUT OF SCOPE for this TO.

    This is a categorical text-replacement task. There is no design judgment involved. There is no investigation required. You will run mechanical commands and verify counts.
  </context>

  <anti_poisoning_protocol>
    Read this section twice before starting any work.

    **Rule 1 — Do not type the names from memory.** Use only the literal commands and patterns provided in this TO. When you need to invoke either name, copy-paste from this document. Do not generate the spelling autoregressively.

    **Rule 2 — Do not read your own prior session logs in this workspace as part of "verifying your work" or "remembering context."** They contain the contaminated token and will reanchor your context. The TO body and the file inventory below are sufficient — you do not need to consult older logs to do this task.

    **Rule 3 — Do not narrate the contaminated token in chat or in commit messages beyond what's strictly necessary.** When describing what you replaced, prefer phrasing like "the contaminated surname token" or "the wrong name." When describing what's correct, name `joe_brandenburg` explicitly and as often as needed.

    **Rule 4 — Mechanical replacement only.** Use `Edit` with `replace_all: true` per file. Do not retype file contents. Do not freehand any string that contains either name.

    **Rule 5 — Verification is grep-count, not eyeballing.** Final acceptance is a grep that returns the expected post-state count. Do not visually scan files looking for misspellings — you will hallucinate matches.

    **Rule 6 — One critical exclusion.** The file `data/black_diamond/scripts/gold/lib/ticker_overrides.py` line 154 contains the string `'BRUNSWICK CORP COM': 'BC'` — this is the legitimate public company **Brunswick Corporation** (NYSE: BC), entirely unrelated to the advisor. **Do NOT modify this line.** It is a true positive. Your replacement scope does not touch it.
  </anti_poisoning_protocol>

  <correct_name_reference>
    The correct advisor identifier is `joe_brandenburg`.

    All occurrences of the wrong-token form `joe_brunswick` must be replaced with `joe_brandenburg`. All standalone occurrences of the wrong-surname form `brunswick` (case-insensitive) that refer to the advisor must be replaced with `brandenburg` (preserving original case where applicable).

    The single exception is the Brunswick Corporation ticker entry described in Rule 6 above.
  </correct_name_reference>

  <phase id="0" when="before any edit">
    <step id="0.1">
      <objective>Establish ground-truth count of contaminated occurrences before any change.</objective>
      <run>From repo root: grep -ri "brunswick" --include="*.md" --include="*.py" --include="*.json" --include="*.xml" -l | sort > /tmp/audit003b_contaminated_files_before.txt</run>
      <run>grep -ri "brunswick" --include="*.md" --include="*.py" --include="*.json" --include="*.xml" -c | sort > /tmp/audit003b_counts_before.txt</run>
      <expect>~22 files matching the inventory in §file_inventory below, plus the one preserved file `data/black_diamond/scripts/gold/lib/ticker_overrides.py` with count 1.</expect>
      <if_mismatch>If the file count differs materially from the inventory: STOP. MCP CTO with the diff before proceeding. Do not improvise.</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="filename rename first">
    <step id="1.1">
      <objective>Rename the contaminated session log filename via git mv (preserves history).</objective>
      <run>git mv "org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-05/ADVI_INFLEC_AUDIT003_joe_brunswick_top_holdings.md" "org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-05/ADVI_INFLEC_AUDIT003_joe_brandenburg_top_holdings.md"</run>
      <expect>git mv reports the rename; `git status` shows the rename pair.</expect>
    </step>
  </phase>

  <phase id="2" when="content edits per file">
    <step id="2.1">
      <objective>For each file in the inventory below, use Edit with `replace_all: true` to replace the contaminated token with the correct name. Do this file-by-file. Do not batch across files in a single Edit call — replace_all is per-file.</objective>
      <pattern>
        For each file: invoke Edit with old_string = `joe_brunswick`, new_string = `joe_brandenburg`, replace_all = true.
        For files that contain the bare-surname form (e.g., capitalized at sentence start): also invoke Edit with old_string = `Brunswick`, new_string = `Brandenburg`, replace_all = true — BUT verify the file is not the ticker_overrides.py exclusion before doing so.
        Lower-case bare form (`brunswick`): invoke Edit with old_string = `brunswick`, new_string = `brandenburg`, replace_all = true — same exclusion check.
      </pattern>
      <protocol>
        After each file's Edit, do not immediately move to the next file. First: re-read the just-edited file and confirm the contaminated token is gone via Grep (post-edit count = 0). Then move on. This catches Edit failures (e.g., file not in context) before they compound.
      </protocol>
    </step>
  </phase>

  <file_inventory note="22 files to modify. The ticker_overrides.py file is listed last as a sanity anchor and is NOT in the modification set.">
    <ds_lane_files note="DS lane — your own authorship; no override needed">
      <file count="11">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_INFLEC.AUDIT-003.joe-brandenburg-top-holdings.md</file>
      <file count="4">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-05/ADVI_RPBKTPI_001_session_2026-05-05.md</file>
      <file count="4">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-05/ADVI_INFLEC_pipeline_audit_session.md</file>
      <file count="3">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-05/ADVI_INFLEC_DS_B_session_closeout.md</file>
      <file count="5">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-05/ADVI_INFLEC_context_cont_closeout.md</file>
      <file count="15">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-05/ADVI_INFLEC_chain_verify_joe_rep_id.md</file>
      <file count="2">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-05/ADVI_INFLEC_AUDIT008_009_DS_D_session.md</file>
      <file count="20" rename_first="true">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-05/ADVI_INFLEC_AUDIT003_joe_brandenburg_top_holdings.md (post-rename — see Phase 1)</file>
      <file count="2">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-04/ADVI_INFLEC_portal_gap_triage.md</file>
      <file count="1">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-04/advi_bfix4_session_summary_postcompaction.md</file>
      <file count="1">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-06/DS_C_startup_2026-05-06.md</file>
    </ds_lane_files>
    <production_code_files note="DS lane (data/orion is DS-owned per orion-pipeline ownership)">
      <file count="1" line="17" detail="Comment only — INFLECTION_REP_IDS set is correct; just the parenthetical comment is wrong">data/orion/scripts/gold/INF_D_08.nmec_nmnc_nna.py</file>
    </production_code_files>
    <cross_lane_files note="REQUIRES GIT_COMMIT_AUTHOR_OVERRIDE per Andrew authorization 2026-05-06">
      <file count="1" lane="CTO">org/tier1_exec/1.0.0_SA_CTO/prompt.md</file>
      <file count="1" lane="CTO">org/tier1_exec/1.0.0_SA_CTO/logs/2026-05-05/session7_inflec_audit_push_close.md</file>
      <file count="1" lane="CTO">docs/architecture/ADVI_INFINGE.md</file>
      <file count="1" lane="COO">org/tier1_exec/2.0.0_SA_COO/logs/2026-05-05/advi_inflec_inflfe_session_2026-05-05.md</file>
      <file count="1" lane="AE_0.6.1">org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-05-05/audit006_inf_i_d00c_geo_drill_prod_dispatch.md</file>
      <file count="2" lane="AE_0.6.1">org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-05-05/advi_infship_a2_close_and_d02b_catalog.md</file>
      <file count="3" lane="DE_0.4.0">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/inflec_fe_state_of_affairs.md</file>
      <file count="1" lane="DE_0.4.0">org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-05-05/SESSION_2026-05-05.md</file>
      <file count="4" lane="DE_0.4.0">org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-05-05/advi_inflfe_003_defensive_render_sweep.md</file>
    </cross_lane_files>
    <preserved_file note="DO NOT MODIFY — legitimate Brunswick Corporation public company ticker entry">
      <file count="1" line="154" reason="NYSE: BC ticker — unrelated to advisor; true positive">data/black_diamond/scripts/gold/lib/ticker_overrides.py</file>
    </preserved_file>
  </file_inventory>

  <phase id="3" when="commit assembly">
    <step id="3.1">
      <objective>Assemble ALL changes into a single atomic commit using safe-commit.sh. Single commit avoids the half-state where some files are corrected and others are not — which would re-contaminate any agent who pulls mid-sweep.</objective>
      <run>From repo root, list every file you modified plus the rename pair: prepare a pathspec list.</run>
      <run>Use `.tools/safe-commit.sh` with explicit author override authorization for cross-lane edits. Per ADHC_OWNPTH protocol, cross-lane authorized edits use `GIT_COMMIT_AUTHOR_OVERRIDE` env var. For this TO, the override value should be `MULTI_LANE` (or `CTO_AUTHORIZED` if MULTI_LANE is not in the allowlist — check the hook script for valid values; if neither works, use `--force` flag which logs a FORCE-BYPASS audit entry to org/git-author-override-audit.log).</run>
      <commit_message_template>
fix(ADVI_INFLEC.AUDIT-003B): workspace categorical name correction sweep — replace contaminated advisor surname token across 22 files

Recovery from prior agent context-poisoning incident. The advisor's correct
identifier is joe_brandenburg; a prior session propagated a wrong surface
token across 22 workspace files. This sweep is mechanical replacement only
— no design judgment, no investigation.

Scope:
- 11 DS-lane session logs (~50 occurrences) corrected
- 1 DS-lane TO body corrected (residual stragglers)
- 1 DS log filename renamed via git mv (history preserved)
- 1 production code comment corrected (data/orion/...INF_D_08.nmec_nmnc_nna.py:17)
  — INFLECTION_REP_IDS frozenset itself was always correct; only the comment
- 1 CTO prompt.md dashboard line corrected
- 1 CTO session log corrected
- 1 CTO PRD (ADVI_INFINGE.md) corrected
- 1 COO session log corrected
- 2 AE 0.6.1 session logs corrected
- 1 DE deliverable (inflec_fe_state_of_affairs.md) + 2 DE session logs corrected

Preserved (true positive, NOT modified):
- data/black_diamond/scripts/gold/lib/ticker_overrides.py:154 — BRUNSWICK
  CORP COM is Brunswick Corporation (NYSE: BC), unrelated to advisor.

Cross-lane override: Andrew direct authorization 2026-05-06 (CTO TO
ADVI_INFLEC.AUDIT-003B). Single atomic commit prevents re-contamination
during partial state.

S3 qa/advisors/{contaminated-key}/ prefix cleanup: out of scope for this
TO; AE 0.6.1 dispatch separate.
      </commit_message_template>
    </step>
    <step id="3.2">
      <objective>Push to origin/CLOUD per standard DS push permission.</objective>
      <run>git push origin CLOUD</run>
    </step>
  </phase>

  <acceptance_criteria>
    <criterion id="AC1" type="machine_checkable">Post-commit, post-push, run from repo root: `grep -ri "brunswick" --include="*.md" --include="*.py" --include="*.json" --include="*.xml" -c | grep -v ":0$" | wc -l` returns **exactly 1** — the only remaining file with hits is `data/black_diamond/scripts/gold/lib/ticker_overrides.py` (1 hit, line 154 BRUNSWICK CORP).</criterion>
    <criterion id="AC2" type="machine_checkable">`grep -ri "brunswick" data/black_diamond/scripts/gold/lib/ticker_overrides.py` shows the BRUNSWICK CORP COM line unchanged at line 154.</criterion>
    <criterion id="AC3" type="machine_checkable">`grep -r "joe_brunswick" .` (case-sensitive) returns zero matches.</criterion>
    <criterion id="AC4" type="machine_checkable">`ls org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-05/ | grep brunswick` returns empty (filename rename succeeded).</criterion>
    <criterion id="AC5" type="machine_checkable">`git log -1 --name-only` shows the rename pair (delete of old filename + add of new) and all modified files in single commit.</criterion>
    <criterion id="AC6" type="machine_checkable">`git diff HEAD~1 -- data/orion/scripts/gold/INF_D_08.nmec_nmnc_nna.py` shows ONLY a comment-line change at line 17; the `INFLECTION_REP_IDS: frozenset[int] = frozenset({3, 6, 11, 12})` value itself is unchanged.</criterion>
    <criterion id="AC7" type="machine_checkable">`git diff HEAD~1 -- data/black_diamond/scripts/gold/lib/ticker_overrides.py` shows zero changes (file untouched).</criterion>
    <criterion id="AC8" type="evidence">Session log under `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-06/` documents: (a) before-count vs after-count grep results from Phase 0 step, (b) confirmation of Phase 1 git mv, (c) commit hash, (d) push receipt, (e) AC1-7 results pasted as evidence. Session log filename: `audit003b_name_correction_sweep.md` — note: filename does NOT contain the contaminated token.</criterion>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before writing any fix">
      None applicable — this is a text-replacement hygiene sweep, not a code or schema change. No comp-tools surface affected.
    </phase>
    <phase id="2" when="before committing">
      None applicable — same reason.
    </phase>
    <phase id="3" when="after committing">
      None applicable — same reason. AC1-7 grep verifications take the place of a compiler check.
    </phase>
    <justification>This TO modifies neither code logic nor data shapes. The single .py file edit is to a comment string only; it changes no AST node, no field name, no API contract. comp-pipescript / comp-blast / comp-iam etc. would surface zero relevant signal. Documenting the absence here so the gate is explicitly waived rather than silently skipped.</justification>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    <note>This TO touches files across multiple agent lanes (CTO/COO/AE/DE/DS) but the modification is non-semantic (text replacement of a name only). No other agent has overlapping work scope on this token. COO has been instructed by Andrew to not communicate with DS~A during this TO's execution to avoid context pollution from cross-traffic. Other agents may continue their independent work; their files will be cleanly updated by this single commit when they next pull from origin/CLOUD.</note>
  </cross_domain_coordination>

  <out_of_scope>
    <item>S3 cleanup: `s3://opal-data-inf/qa/advisors/{contaminated-key}/` prefix exists from a prior QA run. AE 0.6.1 will be dispatched separately to delete the contaminated prefix and confirm the canonical `qa/advisors/joe_brandenburg/` is the only one remaining. DS~A does not need to touch S3.</item>
    <item>The `silver/api_dims/assets/` rep_id=6 silver-gap referenced in the original AUDIT-003 TO body is unrelated to this hygiene sweep — that's pipeline data scope handled by INFINGE Phase 1.</item>
    <item>Process / policy update for "agents must not freehand entity names during renames" — separate CTO follow-on, not this TO.</item>
  </out_of_scope>

  <session_log_required>true</session_log_required>

  <ravc_protocol>
    On AC8 evidence package complete, RAVC4 to CTO (1.0.0_SA_CTO) with: commit hash, push receipt, all AC outputs pasted. CTO will accept and close. No COO involvement on this TO per Andrew direction.
  </ravc_protocol>
</task_order>
