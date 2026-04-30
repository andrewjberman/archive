<task_order>
  <metadata>
    <id>ADHC_COMPIL.012.ds-comp-freshness-tool</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <lane_rationale>Reassigned from ~D → ~A per Andrew direction 2026-04-30 PM. ~A consolidates remaining DS-side INFLEC-track work (already holds staged ORNREN.003) and has deepest INFLEC chain context — W4.* gold authoring, INFGRD.003 chain rerun, ORNREN.001 author. The cadence-config authoring overlaps heavily with ~A's existing knowledge of which Orion artifacts have which freshness expectations.</lane_rationale>
    <coordination>Sequential with ~A's other staged work (ORNREN.003 STAGED awaiting INFLEC stabilization). .011 (INF script-id resolver, DS~C) is COMPLETE — `script &lt;id&gt;` form unblocked; .012 ships full subcommand surface, not partial. If ~D performed any pre-reassignment work on .012, hand off WIP files + audit notes to ~A via session log.</coordination>
    <date>2026-04-30</date>
    <status>COMPLETE</status><!-- AC10 Andrew ACK received 2026-04-30: all vendor entries WARN only. ~D did build + AC1-AC9/AC11-AC13; ~A closed AC10 + committed vendor severity fix. RAVC4 sent. -->
    <project_code>ADHC_COMPIL</project_code>
    <theme>G (v3) — tool + cadence config (paired with .013 dispatch integration)</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL_V3.md §4.6</prd_ref>
    <effort>2–3 weeks (cadence-config authoring is the long pole)</effort>
    <gates_on>None</gates_on>
    <gates_for>ADHC_COMPIL.013 (AE dispatch-script integration gates on this — tool must exist + config must be authored before AE wires it into bd-gold-dispatch.sh / orion-gold-dispatch.sh)</gates_for>
    <critical_path>YES — this is the v3 long pole. Start as early as practical.</critical_path>
  </metadata>

  <objective>
    Build `comp-freshness`: a new compiler tool that detects stale upstream
    S3 data before a script runs against it and produces wrong output
    silently. Two incidents in the past two weeks would have been caught
    pre-dispatch by this tool:

    - 2026-04-17 RPS forensics: Schwab bronze RPS feed last refresh
      `CRS20260407.RPS` (10 days stale) drove $130M overshoot in
      linear_interpolation on April 17 STAUDT diagnostic. Discovered
      manually via `aws s3 ls`; no compiler signal pre-dispatch.
    - 2026-04-29 INFGRD.003: silver/aum_snapshot/ carried only 2026-04-21
      partition when running INF_D_04 on 2026-04-29 (8 days stale).
      Combined with a separate column-name mismatch, produced wrong AUA
      ($89.6M displayed vs $182.71M correct).

    Tool answers: "is the data feeding this chain fresh enough to run?" with
    a deterministic PASS/WARN/FAIL verdict. AE then wires it into the
    dispatch scripts in .013.
  </objective>

  <scope>
    Build .tools/comp-freshness with the following surface:

    Subcommands:
    - `comp-freshness chain {bd|inf}` — check every artifact in the
      pipeline chain's read set against cadence config
    - `comp-freshness script <id>` — check just that script's input
      artifacts. Note: depends on .011 INF ID resolver for INF-script lookup;
      acceptable to ship the BD path first and add INF behind .011.
    - `comp-freshness artifact <s3-prefix>` — check just one artifact's
      most-recent partition vs cadence config
    - `comp-freshness --list` — print the cadence config in human-readable
      form
    - `comp-freshness --help` — standard

    Output format (one line per artifact checked):
      `<artifact_id> | <s3_key> | <last_modified_iso8601> | <age_h> | <fail_at_h> | <STATUS>`
    where STATUS ∈ {PASS, WARN, FAIL}.

    Exit codes:
    - 0 — all PASS (or all PASS + WARN; WARN does not block dispatch)
    - 1 — any FAIL (one or more artifacts beyond fail_at_h)
    - 2 — config error (missing entry, unparseable yaml, AWS unreachable)

    AWS access: same `AWS_EC2_METADATA_DISABLED=true` environment defaults
    as comp-pipescript deployed (memory/AWS hang fixes already documented).
    Use `aws s3api list-objects-v2 --max-items 1` ordered by partition date
    OR `aws s3 ls --recursive | sort | tail -1` — pick whichever is faster
    for the typical chain (~30+ artifacts). Document the choice.

    Cadence config files (NEW):

    1. data/black_diamond/scripts/gold/gold_freshness_config.yaml
    2. data/orion/scripts/gold/gold_freshness_config.yaml

    Config schema:
    ```
    - artifact_id: <unique_id>
      s3_key_prefix: s3://<bucket>/<prefix>/
      cadence: {daily|weekly|business-daily|vendor-daily|on-demand}
      warn_age_hours: <int>
      fail_age_hours: <int>
      severity: {ERROR|WARN}  # default ERROR; WARN downgrades fail_age_hours to warn-only
      notes: optional string for context (especially for vendor feeds)
    ```

    Cadence config authoring (the long pole):

    - Walk every chain (BD + INF) and enumerate every silver/bronze
      artifact-prefix that any gold script reads. Use comp-pipescript io <each
      gold script> to source the read set authoritatively.
    - For each prefix, declare cadence + thresholds based on:
      - Internal nightly chains: cadence=daily, warn=30h, fail=48h
      - Partner feeds (Schwab, Inflection RPS, Orion API): cadence=vendor-daily,
        warn=36h, fail=72h (more lenient because vendor cadence is not
        100% reliable)
      - Weekly artifacts (e.g. histbf weekly snapshots): cadence=weekly,
        warn=8d, fail=14d
      - On-demand/static dims (rare): cadence=on-demand, no thresholds
        (excluded from chain checks but listed in --list for visibility)
    - Andrew sign-off required on partner-feed thresholds (PRD §7 Q1
      recommendation: DS drafts, Andrew reviews vendor entries)

    Target coverage at v3 ship: ≥30 BD artifacts + ≥10 INF artifacts.
    Remaining artifacts can be backfilled in a v4 follow-up TO if scope.
  </scope>

  <acceptance_criteria>
    Tool behavior:
    1. `comp-freshness chain bd` checks all silver/bronze artifacts feeding
       the BD gold chain. Exit 0 if all within fail_age_hours; exit 1 if
       any beyond. WARN entries do not affect exit code.
    2. `comp-freshness chain inf` analogous for INF chain. (Note: `chain`
       and `artifact` forms must work independent of .011; `script <id>`
       form may be partial pending .011 INF resolver.)
    3. `comp-freshness artifact s3://opal-data-bd/bronze/schwab/rps/`
       returns one line with age + verdict. Exit 0 if PASS, 1 if FAIL.
    4. `comp-freshness --list` prints cadence config grouped by pipeline
       (BD then INF), sorted by artifact_id within each.
    5. Config error (missing yaml, malformed entry, AWS unreachable) →
       exit 2 with error message naming the specific problem.

    Retrospective-reproduction (forces real-incident coverage):
    6. Synthetic re-run of 2026-04-17 RPS state: pointing
       `comp-freshness artifact s3://opal-data-bd/bronze/schwab/rps/` at
       the version-state from April 17 (use `aws s3api list-object-versions`
       to find the timestamp of the last partition pre-incident; mock or
       verify behavior) returns FAIL with `age=240h+`. Document the test
       method in session log.
    7. Synthetic re-run of 2026-04-29 INFGRD aum_snapshot: pointing
       `comp-freshness artifact s3://opal-data-inf/silver/aum_snapshot/`
       on 2026-04-29 (using a configured 30h warn / 48h fail) would have
       returned FAIL with `age=192h`.

    Coverage:
    8. Cadence config covers ≥30 BD artifacts (every silver/bronze prefix
       read by any BD gold script).
    9. Cadence config covers ≥10 INF artifacts.
    10. Andrew sign-off on partner-feed entries documented in session log
        (Schwab + Inflection feeds at minimum). Recommendation: send a
        single MCP message to Andrew listing partner-feed entries and the
        proposed warn/fail thresholds, await ACK.

    Operability:
    11. `comp-freshness chain bd` runs in <30s against the live BD chain
        (~30 artifacts × ~1 AWS call each).
    12. AWS-unreachable error output is distinguishable from "FAIL: file
        too old" — same convention as comp-pipescript deployed AWS_UNREACHABLE
        post-ADHC_ROUTER.T2 fix.

    Logging:
    13. Append one row per AC to `org/compiler-tools-log.md`.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT integrate comp-freshness into bd-gold-dispatch.sh / orion-gold-dispatch.sh in this TO — that is .013's scope. Tool + config only here.</rule>
    <rule>Do NOT extend coverage to DynamoDB or non-S3 sources — out of scope per PRD §1 and §7 Q4 (v4 candidate).</rule>
    <rule>Do NOT hardcode S3 bucket names — read from existing config (lib.config or per-pipeline yaml) where the chain already knows them.</rule>
    <rule>Do NOT ship partner-feed thresholds without Andrew sign-off (PRD §7 Q1). If Andrew unavailable for ACK, ship internal-only entries first and follow up.</rule>
    <rule>Do NOT take on COMP_LEARNS scope — workspace-side only (per Andrew's directive 2026-04-29).</rule>
    <rule>Do NOT use emoji in tool output — CLAUDE.md "Code Quality" section. Plain ASCII PASS/WARN/FAIL/ERROR.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">.tools/comp-freshness — Python entry point with subcommand dispatch</deliverable>
    <deliverable type="code">data/black_diamond/scripts/gold/gold_freshness_config.yaml (≥30 entries)</deliverable>
    <deliverable type="code">data/orion/scripts/gold/gold_freshness_config.yaml (≥10 entries)</deliverable>
    <deliverable type="code">tests/comp_freshness/ fixture suite covering chain/script/artifact forms + retrospective reproduction (AC6+AC7)</deliverable>
    <deliverable type="document">org/modules/graph/comp-tools.yaml entry for comp-freshness (matches the existing tool-doc pattern)</deliverable>
    <deliverable type="document">Session log documenting: cadence-config audit method, AWS API call choice rationale, retrospective-reproduction test method, Andrew partner-feed ACK</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC1–AC13 verification, sample chain output for BD + INF, retrospective-reproduction evidence (AC6+AC7)</deliverable>
  </deliverables>

  <compiler_tools_mandate>
    Phase 1 (before write):
    - `comp-build` if cache older than HEAD
    - For each BD + INF gold script: `comp-pipescript io <script>` to source
      the read set authoritatively. Capture every `s3://opal-data-bd/silver/`
      and `s3://opal-data-bd/bronze/` prefix; same for opal-data-inf. This
      is the input to the cadence config audit.
    - Direct read of `.tools/comp-pipescript` `deployed` subcommand to
      borrow the AWS environment-defaults pattern (AWS_UNREACHABLE handling)
    - Direct read of `data/black_diamond/scripts/gold/gold_validate_config.yaml`
      to mirror the schema style for consistency

    Phase 2 (before commit):
    - Run AC1–AC5 against the live BD + INF chains; capture stdout
    - Run AC6 + AC7 retrospective-reproduction tests; document the test
      method in session log
    - `.tools/ds-commit-gate.sh` on every .py file in change set (Rule 14)
    - MCP message to Andrew with partner-feed thresholds for sign-off; do
      not commit until ACK or explicit "ship internal-only first" direction

    Phase 3 (after commit):
    - Append one row per AC to `org/compiler-tools-log.md`
    - Hand off to AE 0.7 for .013 integration; provide tool path + config
      paths + AC verification evidence
  </compiler_tools_mandate>
</task_order>
