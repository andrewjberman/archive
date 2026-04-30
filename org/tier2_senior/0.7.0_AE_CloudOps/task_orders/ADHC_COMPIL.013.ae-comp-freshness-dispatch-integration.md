<task_order>
  <metadata>
    <id>ADHC_COMPIL.013.ae-comp-freshness-dispatch-integration</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-30</date>
    <status>COMPLETE</status>
    <project_code>ADHC_COMPIL</project_code>
    <theme>G integration (v3) — paired with .012 tool authoring</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL_V3.md §4.6 (mandates section)</prd_ref>
    <effort>2–3 days</effort>
    <gates_on>ADHC_COMPIL.012 COMPLETE — comp-freshness tool must exist + cadence config must be authored before AE wires it into dispatch.</gates_on>
    <gates_for>v3 ship — final TO before all-green; closes the runtime-data-freshness gap end-to-end.</gates_for>
  </metadata>

  <objective>
    Wire `comp-freshness` (shipped under .012) into `bd-gold-dispatch.sh` and
    `orion-gold-dispatch.sh` as a pre-flight gate. Pattern follows the v1
    Theme B cascade gate (.002): run the check before chain dispatch, abort
    on FAIL, allow `--no-freshness-check` bypass with audit logging.

    The tool exists pointlessly without integration; this TO is what makes
    the freshness-detection actually fire automatically before every
    nightly + on-demand chain run.
  </objective>

  <scope>
    Modify bd-gold-dispatch.sh and orion-gold-dispatch.sh:

    Gate behavior (default):
    1. Before chain dispatch (after `comp-pipescript deployed` checks
       already in place), run:
         comp-freshness chain {bd|inf}
    2. If exit 0: proceed with dispatch.
    3. If exit 1 (any FAIL): abort dispatch with non-zero exit. Print:
       - The failing artifacts + ages (relay comp-freshness stdout)
       - Suggested next steps (typically: re-run upstream silver/bronze
         backfill, or check vendor-feed status)
       - Suggested bypass command if operator is intentionally proceeding
    4. If exit 2 (config error / AWS unreachable): abort with non-zero exit
       and a distinct error message — this is a tooling failure, not a
       data-freshness FAIL. Operators may bypass via --no-freshness-check
       in this case while infra is repaired.

    Override flag: --no-freshness-check
    - Bypasses the gate (for emergency debug, isolated re-emission, or
      AWS-unreachable scenarios).
    - Appends a bypass entry to org/compiler-tools-log.md, format:
      [ADHC_COMPIL.013] FRESHNESS-BYPASS: <timestamp> | <dispatcher> | <chain> | <operator> | <reason-from-flag-arg-or-empty>
    - The bypass log entry is the accountability trail; do NOT suppress.

    Optional flag accompanying bypass: --bypass-reason "<short text>"
    - Stored in the log entry for audit context. If absent, log "(no reason
      given)".

    --chain full vs --chain partial: gate runs on both. The freshness check
    is independent of the cascade-gate (.002); both run in sequence.

    Sequence in dispatcher (after .002's cascade gate):
      1. comp-pipescript deployed check (already present, pre-existing)
      2. comp-pipescript postdeps cascade gate (.002)
      3. comp-freshness chain check (THIS TO)
      4. Proceed with dispatch

    All three gates must PASS (or have a documented bypass) before dispatch
    fires.

    Both dispatchers get identical gate behavior:
    - bd-gold-dispatch.sh: `comp-freshness chain bd`
    - orion-gold-dispatch.sh: `comp-freshness chain inf`

    Documentation:
    - Update CLAUDE.md "Critical Deployment Rules" section if appropriate
      (deferred; coordinate with CTO before adding rules)
    - Update inline `--help` of both dispatcher scripts to document the
      gate + bypass flag
  </scope>

  <acceptance_criteria>
    1. bd-gold-dispatch.sh --chain full (with all freshness PASS) → proceeds
       normally. Same as today + freshness-check stdout shown.
    2. bd-gold-dispatch.sh --chain full (with at least one freshness FAIL,
       e.g. by synthetically setting fail_age_hours=1 on a known-old
       artifact) → exits non-zero, prints failing artifacts, prints
       suggested bypass command.
    3. bd-gold-dispatch.sh --chain full --no-freshness-check (with FAIL
       state) → proceeds AND appends bypass entry to
       org/compiler-tools-log.md with [ADHC_COMPIL.013] FRESHNESS-BYPASS prefix.
    4. bd-gold-dispatch.sh --chain full --no-freshness-check --bypass-reason
       "vendor RPS feed scheduled outage 2026-04-30" → proceeds AND log
       entry contains the reason text.
    5. orion-gold-dispatch.sh equivalents (AC1–AC4 mirrored for INF).
    6. Config-error (exit 2) handling: simulate by temporarily renaming the
       cadence yaml; dispatcher aborts with distinct error message AND
       documents that --no-freshness-check is the unblock path during
       infra repair.
    7. Sequence verified: comp-pipescript deployed → cascade gate (.002) →
       comp-freshness gate (.013) → dispatch. Order matters because
       freshness-check is the most expensive (AWS calls); skipping when
       earlier gates fail saves cycles.
    8. Bypass log entries formatted correctly; readable as a single-line
       audit record.
    9. Append one row per AC to org/compiler-tools-log.md.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT start before .012 is COMPLETE — comp-freshness must exist + cadence config must be live + Andrew partner-feed ACK must be in.</rule>
    <rule>Do NOT modify the cadence config yamls — those are .012's deliverable. AE-side change is dispatcher-only.</rule>
    <rule>Do NOT allow --no-freshness-check to suppress the bypass log entry — it's the accountability trail for ops review.</rule>
    <rule>Do NOT change the order of existing gates — append the freshness gate AFTER deployed-check + cascade-gate, not before. The earlier gates are cheaper; running them first short-circuits failures faster.</rule>
    <rule>Do NOT treat AWS-unreachable as a freshness FAIL — distinct error class, distinct exit (2 vs 1). Operators must be able to bypass freshness during AWS infra outages without misreading them as stale data.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">bd-gold-dispatch.sh with comp-freshness gate + --no-freshness-check + --bypass-reason flags</deliverable>
    <deliverable type="code">orion-gold-dispatch.sh with same</deliverable>
    <deliverable type="code">Test fixture: synthetic FAIL state reproduction (set fail_age_hours=1 on a non-stale artifact, confirm gate fires)</deliverable>
    <deliverable type="document">Updated --help output for both dispatchers</deliverable>
    <deliverable type="document">Session log with AC1–AC9 verification + bypass-log-entry sample</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO with: AC exit codes, bypass log excerpt, sequence verification (AC7), one nightly-chain-run-with-gate-active confirmation post-deploy</deliverable>
  </deliverables>

  <compiler_tools_mandate>
    Phase 1 (before write):
    - Confirm .012 is COMPLETE; pull tool path + config paths from .012's RAVC4
    - `comp-blast bd-gold-dispatch.sh` and `comp-blast orion-gold-dispatch.sh`
      to confirm no other tool/script depends on dispatcher exit-code semantics
    - Direct read of bd-gold-dispatch.sh + orion-gold-dispatch.sh to locate
      the .002 cascade-gate insertion point — append after that

    Phase 2 (before commit):
    - Run AC1–AC8 fixture cases on the QA runner first (do NOT exercise on
      PROD until QA-PASS)
    - Confirm bypass log entries are correctly formatted by tail -1 of
      org/compiler-tools-log.md after each --no-freshness-check run
    - One full QA-runner chain dispatch with the gate active to confirm no
      regressions in dispatch behavior

    Phase 3 (after commit):
    - Wait for one nightly chain run to fire with the gate active; capture
      the comp-freshness output from the dispatcher log
    - Append one row per AC to org/compiler-tools-log.md
    - If any FAIL fires unexpectedly on a real nightly run, escalate to DS
      0.4 immediately — likely indicates a cadence-config threshold needs
      tuning (this is expected during the first 1–2 weeks of operation)
  </compiler_tools_mandate>
</task_order>
