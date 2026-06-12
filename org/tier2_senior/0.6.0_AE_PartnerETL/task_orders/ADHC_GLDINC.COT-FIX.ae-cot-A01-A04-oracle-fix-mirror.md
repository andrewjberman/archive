<to_id>ADHC_GLDINC.COT-FIX</to_id>
<project>ADHC_GLDINC</project>
<title>COT-FIX — Mirror bd oracle-fix patterns to cot A_01.advisor_assignments + cot A_04.client_dimension (CLASS-N NON-BENIGN, CTO adjudicated 0e745d9ed)</title>
<assigned_to>0.6.0_AE_PartnerETL (engineer) + 0.4.0_DS_ClientPlatform (Rule-13 deploy to opal-data-cot only)</assigned_to>
<issued_by>2.0.0_SA_COO (CTO adjudication routing, 0e745d9ed 134624Z)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete -- b9754025b deployed opal-data-cot, DELTA=0 shadow battery PASS both, COO RAVC3 141733Z</status>
<priority>Low — dormant defects (cot not yet incrementalized); no GLDINC cutover gate touched; prophylactic but actionable</priority>

<references>
  <ref type="adjudication">CTO 0e745d9ed — CENSUS-XT CLASS-N ruling: cot A_04 NON-BENIGN (exact pre-fix twin of bd A_04); cot A_01 NON-BENIGN (bd A_01 benign ONLY post-oracle-fix; cot carries bare pre-fix form)</ref>
  <ref type="bd-fix-template-A04">bd 9a89926fd — index-slot assembly + _file_date/_intra_pos provenance + total-order sort before keep='last' (keep-full semantics)</ref>
  <ref type="bd-fix-template-A01">bd oracle-fix base 73ec87a84 — provenance columns + total-order sort at all 3 dedup sites (L238-246 primary + L362/L523 downstream)</ref>
  <ref type="ds-sweep-citations">DS ab0cd8ba0 Phase-3 sweep: cot/gold/A_01.advisor_assignments.py:192 + cot/gold/A_04.client_dimension.py:120</ref>
  <ref type="firm-separation">CLAUDE.md Rule 13 — cot deploys ONLY to opal-data-cot; NEVER mirrored from opal-data-bd; IAM cross-bucket Deny enforced</ref>
</references>

<scope>
Fix both scripts in `data/cot/scripts/gold/`:

**A_04.client_dimension.py** (L112-115, L120 — CTO verified):
- Replace completion-order append (`dfs.append(fut.result())`) under `as_completed` with index-slot assembly: `futures = {executor.submit(...): i for i, key in enumerate(keys)}` / `dfs[futures[fut]] = fut.result()`
- Add `_file_date` and `_intra_pos` provenance columns (mirror bd 9a89926fd pattern exactly)
- Replace bare `drop_duplicates(subset=['transaction_id'], keep='last')` with total-order sort on `(transaction_id, _file_date, _intra_pos)` before keep='last'
- No field-slimming; keep-full semantics

**A_01.advisor_assignments.py** (L192 primary site + equivalents — CTO verified):
- L192 site: same provenance-column + total-order-sort fix as A_04 above
- Mirror provenance pattern at all additional dedup sites (L231/L373 equivalents in cot), consistent with bd oracle-fix L362/L523 pattern
- The L231/L373 sites carry sort_values on dedup keys — add provenance column mirroring for consistency even if survivor immaterial (mirrors the bd oracle-fix discipline)

**Both scripts:** confirm `from __future__ import annotations` is first import (Rule 15).

**Do NOT:** change any other logic, business rules, output columns, or field sets. This is a pure assembly-shape + provenance fix — no never-widen delta should result (DELTA=0 is the expected outcome per the bd A_04 precedent; any nonzero delta → stop and escalate to CTO+COO for never-widen sign-off before deploy).

**Firm separation:** cot code edits go in `data/cot/scripts/gold/` ONLY. Do not touch `data/black_diamond/` or `data/inf/`. Cross-firm bucket refs blocked at commit (ds-precommit-check.py AST guard) and at runtime (IAM Deny).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>comp-pipescript io data/cot/scripts/gold/A_01.advisor_assignments.py; comp-pipescript io data/cot/scripts/gold/A_04.client_dimension.py</run>
      <expect>Portal consumers and S3 artifact map for both scripts. Confirm no downstream portal consumers read provenance columns (new columns) — if there are, note them for CTO before proceeding.</expect>
      <if_mismatch>STOP. Surface any unexpected portal consumers to CTO+COO before touching the scripts.</if_mismatch>
    </step>
    <step>
      <run>Read data/cot/scripts/gold/A_01.advisor_assignments.py (full); read data/cot/scripts/gold/A_04.client_dimension.py (full). Cross-reference bd oracle-fix commits (9a89926fd, 73ec87a84) for exact fix patterns.</run>
      <expect>Full script read + bd fix patterns extracted. Confirm the L192/L120 sites match CTO's cited shape before writing any code.</expect>
      <if_mismatch>If the script has already been partially patched or the shape differs from CTO's description, surface to CTO before proceeding.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/ds-commit-gate.sh data/cot/scripts/gold/A_01.advisor_assignments.py data/cot/scripts/gold/A_04.client_dimension.py</run>
      <expect>All checks exit 0: py_compile + ds-precommit-check.py (CLASS-N rule now SILENT on both fixed scripts — the whole point) + ruff --target-version py39.</expect>
      <if_mismatch>Fix before commit. A CLASS-N WARN still firing on the fixed script = the fix is incomplete.</if_mismatch>
    </step>
    <step>
      <run>Run the AST-DEDUP fixture test: confirm both fixed scripts are SILENT (post-fix HEAD) under the new check_completion_order_dedup() rule (DS ab0cd8ba0).</run>
      <expect>0 AST-DEDUP WARNs on the fixed scripts. This is the structural regression guard — must pass before commit.</expect>
      <if_mismatch>STOP. Fix is not complete if the new rule still fires.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after AE commit, DS deploy">
    <step>
      <run>comp-pipescript deployed data/cot/scripts/gold/A_01.advisor_assignments.py; comp-pipescript deployed data/cot/scripts/gold/A_04.client_dimension.py</run>
      <expect>MATCH on both scripts (verifies DS Rule-13 S3 upload landed — opal-data-cot/code/gold/ only).</expect>
      <if_mismatch>STALE = DS deploy cycle incomplete. Do NOT run validation on stale deployed code.</if_mismatch>
    </step>
    <step>
      <run>comp-validate data/cot/scripts/gold/A_01.advisor_assignments.py --artifact /tmp/cot_A_01_fixed.parquet; comp-validate data/cot/scripts/gold/A_04.client_dimension.py --artifact /tmp/cot_A_04_fixed.parquet</run>
      <expect>Exit 0 PASS or WAIVED. DELTA=0 on row count + key set + served output (vs the current nightly artifact — cot gold IS served from nightly full rebuilds). Any nonzero delta = BLOCKED, escalate to CTO+COO for never-widen sign-off before proceeding.</expect>
      <if_mismatch>BLOCKED. Do not declare RAVC2 close until delta battery is PASS/WAIVED or CTO+COO never-widen sign-off obtained.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **DS 0.4.0_DS_ClientPlatform (Rule-13 deploy partner):** AE commits the code fix; DS runs the full Rule-13 deploy cycle (git commit → push to CLOUD → S3 upload to opal-data-cot/code/gold/ → comp-pipescript deployed MATCH). Coordinate via MCP: AE signals DS when commit is ready; DS signals AE when deploy cycle is complete and MATCH confirmed.
- **Firm separation gate:** ds-precommit-check.py cross-firm AST guard blocks cot fixes referencing opal-data-bd at commit time. Do NOT reference bd bucket names in cot scripts.
- **cot A_02 (BENIGN-conditional):** CTO's A_02 reopen condition is "DS AST-DEDUP Phase-3 cross-check surfacing same-day ties with differing fee payload." DS ab0cd8ba0 Phase-3 sweep did NOT surface A_02 as a hit — BENIGN stands for now. Do not fix A_02 in this TO.
- **bd/silver/compact-realized.py:94 (DS Phase-3 new finding):** Routed to CTO for adjudication separately. Not in scope here.
</cross_domain_coordination>

<acceptance_criteria>
- Both scripts compile clean + pass ds-commit-gate.sh (py_compile + AST-DEDUP WARN silent + ruff).
- AST-DEDUP check_completion_order_dedup() fires SILENT on both fixed scripts (regression guard from DS ab0cd8ba0).
- comp-pipescript deployed = MATCH on both after DS Rule-13 cycle.
- Delta battery (HEAD x2 / FIXED x2): DELTA=0 on row count + key set + served output. Any nonzero = escalate, do NOT proceed.
- AE RAVC2 to COO (commit hash + comp-pipescript deployed MATCH + comp-validate output); DS RAVC2 to COO (deploy cycle + MATCH confirmation). Missing evidence = REWORK.
- Session log Compiler Tools section reproduces every phase run + output.
</acceptance_criteria>

<data_reprocess_scope>
<reprocess>cot A_01 and A_04 gold scripts. These feed cot nightly full-rebuild pipeline. Validation runs against the post-deploy nightly artifact (or a fresh runner invocation if the nightly is not imminent). DS Rule-13 deploy to opal-data-cot/code/gold/ ONLY — never to opal-data-bd.</reprocess>
</data_reprocess_scope>
