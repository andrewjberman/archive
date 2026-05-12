<task_order>
  <metadata>
    <id>0.6.0_AE_PartnerETL-2026-04-15-gold-dispatcher-hygiene</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. --><!-- HARD GATE: live 18:07 UTC partial chain MUST close before any edit. gold_dispatch.sh is pinned in-memory at fire time but the partial-chain helper re-reads it per iteration; editing during flight = chain corruption. -->
    <project_code>ad-hoc</project_code>
    <priority>P2 (post-chain hygiene; no runtime behavior change)</priority>
  </metadata>

  <references>
    <ref type="trigger">Andrew audit 2026-04-15 (post gold_dispatch.sh review during 18:07 UTC partial-chain hold)</ref>
    <ref type="subject_file">data/black_diamond/scripts/runner/gold_dispatch.sh (live on bd-gold-qa-runner AND bd-gold-layer-runner code paths)</ref>
    <ref type="related_incident">2026-04-15 17:27 UTC chain failed at B_01 NameError — orthogonal (script bug not dispatcher bug) but surfaced a dispatcher chain-sequence question (`--chain full` after A_* completed needed a one-off `/tmp/_partial_chain_b01.sh` wrapper)</ref>
  </references>

  <objective>
    Andrew's audit found 8 real bugs/dead-weight items + 6 logic traps in `gold_dispatch.sh`. Fix
    the 10-item cleanup list below in one commit (post live-chain close only). No runtime behavior
    change for current-healthy paths — just removes dead weight, fixes misleading names, dedupes
    log paths, tightens arg validation, and makes flag docs single-sourced.

    **Scope (10-item cleanup per Andrew's recommendation, verbatim):**

    1. **Delete CHAIN_REBUILD** — line 145 alias of `full`, dead code with misleading "rebuild" semantic implication. Remove constant + case arm + help line.
    2. **Dedupe CHAIN_FULL B_01b** — CHAIN_FOUNDATION ends `... B_01 B_01b` and CHAIN_CANONICAL starts `B_00 B_01b ...`. Concatenation runs B_01b.classify_new_securities.py twice per nightly. Decide: (a) drop second B_01b from CHAIN_CANONICAL, OR (b) move B_01 + B_01b out of CHAIN_FOUNDATION into a new CHAIN_HOLDINGS_SEED. Andrew's suggestion: option (b), rename CHAIN_FOUNDATION → CHAIN_DIMENSIONS (A_* only) + CHAIN_HOLDINGS_SEED (B_01 B_01b) — see item 10.
    3. **--incremental restriction** — line 226-231 strips `--incremental` for all scripts except A_00 and C_06. Either (a) restrict `--incremental` to `--single A_00|C_06` only (error with clear message otherwise), OR (b) wire through the scripts that actually need it. Andrew's worst-of-both framing — pick one path and commit to it in one cycle. Recommendation: start with (a) (tight + clear), open (b) as follow-up TO.
    4. **Dedupe --bg logs** — `--bg` re-invokes itself; wrapper + foreground each compute their own `$log_file` with different timestamps. Wrapper log stays on disk; only foreground uploads via `upload_log`. Orphan at `/tmp/gold_logs/` (evidence: 17:27 fire produced both `chain_full_20260415_172741.log` AND `full_20260415_172741.log`). Fix: either skip wrapper log OR upload both.
    5. **Fix canonical help text** — help at line 343 shows `B_00 B_02 B_03 C_00 C_01 C_02 C_04`. Actual CHAIN_CANONICAL is `B_00 B_01b B_02 B_03 C_00 C_01 C_02 C_04`. Drifted; sync.
    6. **Fix "E Diagnostics (run directly, not through dispatch)" line** — line 389 says diagnostics are run directly. Not true: S_00 IS run through dispatch (`--chain silver-prep` / `--single S_00`). Rewrite accurately.
    7. **Document --force** — top-of-file FLAGS block (line 47-50) omits it entirely. Add. Freshness-gate override with zero discoverability is a foot-gun.
    8. **Sync --no-shutdown docs** — appears in `--help` but missing from top-of-file FLAGS. Two sources of flag truth out of sync. Delete one (Andrew preference: collapse to `show_help` single source; remove top-of-file block).
    9. **Arg-parser validation** — currently `--single --bg` silently sets `TARGET="--bg"` and eats next arg. Add explicit check: if `--chain/--group/--single` is followed by a flag or EOF, reject with clear error.
    10. **Rename CHAIN_FOUNDATION** — misleading ("foundation" reads dimension/account only, actually includes B_01 B_01b holdings work). Split: `CHAIN_DIMENSIONS` (A_* only) + `CHAIN_HOLDINGS_SEED` (B_01 B_01b). Rewrite CHAIN_FULL to concatenate `CHAIN_DIMENSIONS + CHAIN_HOLDINGS_SEED + CHAIN_CANONICAL + CHAIN_DOWNSTREAM` (closes item 2 structurally).

    **Also surfaced but NOT in this TO's scope (flagged for follow-up):**
    - Logic trap 9: CHAIN_CANONICAL needs B_01 outputs despite not including B_01. Order dependency unenforced. → resolves naturally if item 10 renames land + CHAIN_FULL is sequenced correctly.
    - Logic trap 11: Auto-shutdown only fires for `MODE=chain`. `--group D` and `--single X` never shut down. Leaves 64-vCPU instance warm. Andrew flagged as "consider." → open as optional follow-up.
    - Logic trap 12: Freshness gate only guards `full/downstream/rebuild`. `--chain downstream` alone doesn't validate silver gap dates filled. → open as optional follow-up.
    - Logic trap 14: `--dry-run` only rewrites `--upload → --dry-run`. Scripts with empty default flags (S_00, C_04) run as read-only regardless. → documented-as-is, not a bug.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/runner/gold_dispatch.sh</file>
    </files>
  </scope>

  <wire_contract>
    No runtime behavior change for current healthy paths. `--chain full` still produces identical
    script sequence post-cleanup (dedup removes duplicate B_01b execution, which was a noop — B_01b
    caches no state between invocations; verify via run-sanity check pre-ship). `--incremental`
    behavior narrows from silent-passthrough to explicit rejection for unsupported scripts —
    documented deviation, visible-in-error-output.
  </wire_contract>

  <acceptance_criteria>
    1. All 10 cleanup items applied in one commit.
    2. `bash -n data/black_diamond/scripts/runner/gold_dispatch.sh` exits 0 (shell syntax check).
    3. `gold_dispatch.sh --help` output matches the FLAGS and chain definitions actually implemented (no drift between help + code).
    4. `gold_dispatch.sh --chain full --dry-run` script-sequence output contains no duplicate script IDs (dedup verified).
    5. `gold_dispatch.sh --single --bg` now produces an explicit error message about missing script-id argument (arg validation verified).
    6. `gold_dispatch.sh --incremental --chain full` either runs only A_00 + C_06 with incremental, OR explicitly errors (path chosen in item 3 is documented in commit body).
    7. Single log file per `--bg` invocation (wrapper log either skipped or uploaded; no orphans in `/tmp/gold_logs/`).
    8. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO Rule 7 locked 2026-04-15).
    9. MCP COMPLETE to COO with commit hash + diff summary + smoke-test evidence (help output, dry-run sequence, arg-validation error path).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>bash -n data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>Exit 0 (current state is syntactically valid; this baselines the pre-edit.)</expect>
        <if_mismatch>Pre-existing syntax error — STOP and surface to COO; not in scope for this TO.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --chain full --dry-run 2>&amp;1 | grep -oE '[A-Z]_[0-9a-z]+' | sort | uniq -c | sort -rn | head -5</run>
        <expect>Duplicate B_01b detected (count=2 for `B_01b`). Baselines the dedup target for acceptance #4.</expect>
        <if_mismatch>If B_01b already count=1, item 2 is stale — reconcile against current file state before writing.</if_mismatch>
      </step>
      <step>
        <run>grep -n 'CHAIN_REBUILD\|CHAIN_FOUNDATION\|CHAIN_CANONICAL\|--incremental\|--force\|--no-shutdown' data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>All 6 patterns present at stated line ranges (145, foundation line, canonical line, 47-50 FLAGS, 226-231 incremental, 343 help text). Confirms scope.</expect>
        <if_mismatch>If any line moved or pattern absent, re-baseline against current file; update the `<objective>` line-number references in the commit body to match.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>bash -n data/black_diamond/scripts/runner/gold_dispatch.sh</run>
        <expect>Exit 0 post-edit.</expect>
        <if_mismatch>Fix syntax before commit.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --help</run>
        <expect>Output shows all flags (`--chain`, `--group`, `--single`, `--bg`, `--dry-run`, `--incremental`, `--force`, `--no-shutdown`) at a single source (no dual top-of-file FLAGS block). Canonical chain list shows `B_00 B_01b B_02 B_03 C_00 C_01 C_02 C_04`.</expect>
        <if_mismatch>Documentation drift persists — re-reconcile against implementation.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --chain full --dry-run 2>&amp;1 | grep -oE '[A-Z]_[0-9a-z]+' | sort | uniq -c | awk '$1 &gt; 1'</run>
        <expect>Empty output (no script appears more than once in the full chain).</expect>
        <if_mismatch>Dedup incomplete. STOP; fix and re-run.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --single --bg 2>&amp;1</run>
        <expect>Explicit error: `--single requires a script id argument (got flag '--bg')` or similar.</expect>
        <if_mismatch>Arg validation missing; add per item 9.</if_mismatch>
      </step>
      <step>
        <run>gold_dispatch.sh --chain full --incremental --dry-run 2>&amp;1 | head -30</run>
        <expect>Per item 3 chosen path: either only A_00 + C_06 show `--incremental`, OR an explicit error rejects the combo. Commit body documents the chosen path.</expect>
        <if_mismatch>Inconsistent --incremental handling — pick one; cannot ship the "worst-of-both" state.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit + S3 upload">
      <step>
        <run>aws s3 cp data/black_diamond/scripts/runner/gold_dispatch.sh s3://opal-data-bd/code/runner/gold_dispatch.sh &amp;&amp; aws s3api head-object --bucket opal-data-bd --key code/runner/gold_dispatch.sh --query ETag</run>
        <expect>Upload success; ETag matches local md5 (deploy parity).</expect>
        <if_mismatch>Retry; if persists, surface to COO.</if_mismatch>
      </step>
      <step>
        <run>On next natural EventBridge fire (PROD runner) OR manual `--single A_00 --dry-run` on QA: observe log output goes to single file, no orphan in /tmp/gold_logs/</run>
        <expect>One log per run, uploaded to S3 diagnostics, wrapper log removed OR uploaded per item 4 choice.</expect>
        <if_mismatch>Item 4 regression; patch forward.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency description="Live 18:07 UTC partial chain MUST close before any edit to gold_dispatch.sh (HARD GATE)" status="pending"/>
  </dependencies>

  <next>
    On commit: next PROD EventBridge fire (22:00 UTC tonight for W7 verification) is the first real regression test. Post-run MCP COMPLETE with W7 log excerpt + observation that cleanup didn't regress nightly behavior.

    Optional follow-up TOs (not this TO):
    - Auto-shutdown for `--group D` + `--single X` modes (Andrew flagged, not committed)
    - Freshness-gate extension to `--chain downstream` (logic trap 12)
    - Wire `--incremental` into more scripts if item 3 chose restrict-path (re-open as expansion TO)
  </next>
</task_order>
