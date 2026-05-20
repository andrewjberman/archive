<task_order>
  <metadata>
    <id>MDLP_VOLAUD.003</id>
    <slug>ae-yang-generate-benchmark-returns-retire-or-redesign</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL~B</issued_to>
    <date>2026-05-19 (authored ~17:3XZ as base AE 0.5; LANE OVERRIDE to ~B ~17:42Z per Andrew-direct provisioning of 0.5.0_AE_OpalETL~B; re-dispatch ~17:4XZ)</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <lane_override_note>ANDREW-DIRECT LANE OVERRIDE 2026-05-19 ~17:42Z (verbatim via CTO relay): "I am provisioning 0.5.0_AE_OpalETL~B for VOLAUD, do not distract 0.5.0_AE base with this". Base AE 0.5 stays untouched on SSCN_DIVDEF.004 + their natural queue. ~B (just-provisioned, PID 7064 LIVE per COO~B observation) fully owns the MDLP_VOLAUD project arc from .003 onward. Original CTO disposition had AE 0.5 base as the lane; Andrew operational call overrides per `feedback_andrew_product_invariant_overrides_sequenced_gates` -- top-tier authority, no re-converge needed.</lane_override_note>
    <project_code>MDLP_VOLAUD</project_code>
    <supersedes>MDLP_VOLAUD.002 (closed-as-superseded-by-redirect 2026-05-19 ~17:3XZ per CTO disposition on this Phase 0 finding; the .002 target hypothesis -- `yang-model-portfolio-benchmarks` runtime divergence -- was disproved by AE 0.5.0's empirical chain (S3 versioning + fresh-invoke + dual-writer race identification). .003 carries the fix for the actual root cause: dual-writer race in SFN where `yang-generate-benchmark-returns` overwrites `yang-model-portfolio-benchmarks`'s correct emit.</supersedes>
    <priority>P1 -- TIME-PRESSURED. Structural dual-writer race in Step Functions fires on every scheduled SFN execution; tomorrow's 2026-05-20T14:00Z scheduled run will race again (50/50 outcome). Currently-served JSON is incidentally correct (AE's 17:18Z fresh-invoke was single-invocation, no race) but the page may flip to collapsed-1D/WTD/MTD on tomorrow's emit depending on race outcome. Target Phase 1 fix BEFORE 2026-05-20T14:00Z scheduled SFN run.</priority>
    <sla>~1-2h post-Phase 0.5 wall depending on Phase 1 branch:
      - Phase 0.5 probe: ~30min AE 0.5
      - Phase 1 RETIRE branch (default if Phase 0.5 verdict = pure-redundant): ~30-45min AE 0.5 (Terraform SFN-state-transition removal + Lambda removal + IAM cleanup + source-map entry removal)
      - Phase 1 REDESIGN branch (if Phase 0.5 verdict = unique-consumer): pause + re-converge to CTO; no Phase 1 work until CTO ruling on the redesign architecture
      - Phase 2 verify: tomorrow's scheduled SFN run produces single-write + correctly-differentiated 1D/WTD/MTD values
    Total: ~2h post AE 0.5 SSCN_DIVDEF.004 close to Phase 1 retire ship; comfortable margin to 2026-05-20T14:00Z (~21h remaining).</sla>
    <deadline>2026-05-20T14:00Z (next scheduled SFN execution; race fires again unless Phase 1 retires the second writer OR redesigns the dual-write).</deadline>
  </metadata>

  <references>
    <origin>1.0.0_SA_CTO MCP to 2.0.0_SA_COO 2026-05-19 ~17:3XZ ("Dispositions: (ii) spin .003 + Phase 0.5 probe before (a)/(b) ruling; AE 0.5 lane; target fix pre-2026-05-20T14:00Z SFN run"). CTO PATH (ii) + PHASE-0.5-PROBE-DEFER on (a)/(b) ruling. AE 0.5.0 Phase 0 finding via 2.0.0_SA_COO~B cross-lane FYI 2026-05-19 ~17:3XZ.</origin>
    <ae_phase_0_finding>AE 0.5.0 empirical chain (essentially completed .002's diagnostic mission + disproved its target hypothesis):
      - Byte-collapse NOT reproducible from `yang-model-portfolio-benchmarks` alone
      - Fresh `aws lambda invoke` at 17:18Z produced correctly-differentiated values matching DS~B local probe to-the-cent
      - S3 versioning shows TWO writes 2026-05-19 morning, 1 second apart:
        * v1 CORRECT, generated_at 11:25:02Z (from `yang-model-portfolio-benchmarks`)
        * v2 COLLAPSED, generated_at 11:25:03Z (OVERWROTE v1; from second Lambda)
      - Second Lambda: `yang-generate-benchmark-returns` -- writes the SAME S3 key (`OUTPUT_KEY_COMPREHENSIVE='json/benchmarks/model_portfolio_benchmarks.json'`)
      - Different runtime: py3.11 vs py3.12
      - Different Layer: pandas-pyarrow-layer:1 vs AWSSDKPandas-Python312:16
      - Both fired from same Step Functions execution -> race + last-writer-wins
      - `yang-generate-benchmark-returns` IS the collapsed writer
      - Currently-served JSON is incidentally correct (last-writer-wins, but AE's fresh invoke was single-invocation, no race occurred)
      - Structural bug fires on every scheduled SFN execution</ae_phase_0_finding>
    <cto_leans_retire>CTO lean (deferred pending Phase 0.5): "(a) retire on the legacy-Lambda hypothesis -- the name pattern `yang-generate-benchmark-returns` is more generic; `yang-model-portfolio-benchmarks` was the MDLP_RVVALT 2026-05-04 ship; same OUTPUT_KEY suggests the old Lambda was supposed to be retired when the new one shipped but the SFN was never updated. But I'm speculating; the probe is cheap insurance."</cto_leans_retire>
    <ds_b_canonical>DS~B's MDLP_VOLAUD.001 audit brief + probe + anchor-JSON inputs remain canonical verification context (the local-on-same-pickle baseline AE 0.5's fresh-invoke matched to-the-cent is the same baseline .003 Phase 2 will verify against post-fix). Brief: `docs/briefs/mdlp-etf-vs-index-volatility-audit-20260519.md`. Probe: `org/tier2_senior/0.4.0_DS_ClientPlatform/probes/mdlp_volaud_001_etf_vs_index_audit.py`.</ds_b_canonical>
    <sequencing>AE 0.5 currently on SSCN_DIVDEF.004 (~30min wall per 2.0.0_SA_COO~B route); resumes MDLP_VOLAUD work post-SSCN. SSCN_DIVDEF.004 stays AE 0.5's CURRENT priority -- THIS TO does NOT interrupt mid-flight. Sequence: SSCN_DIVDEF.004 ship -> .003 Phase 0.5 probe -> Phase 1 retire OR redesign-pause -> Phase 2 verify. Approximate AE 0.5 session window: SSCN close + ~1.5-2h for retire path OR pause-for-CTO + indeterminate for redesign path.</sequencing>
    <pipeline_rule>Rule 1 (Terraform-only for SFN state + Lambda + IAM removal). Rule 13 (AE owns yang-pipeline + SFN infrastructure).</pipeline_rule>
  </references>

  <context>
    Step Functions executes both `yang-model-portfolio-benchmarks` (newer, py3.12, AWSSDKPandas-Python312:16) AND `yang-generate-benchmark-returns` (older, py3.11, pandas-pyarrow-layer:1) in the same execution; both write to the SAME S3 key `json/benchmarks/model_portfolio_benchmarks.json`. Last-writer-wins. The older Lambda's `calculate_period_returns` / `calculate_volatility` for 1D/WTD/MTD branches produces collapsed (byte-identical) values across the three short-window periods + writes them last (1 second after the newer Lambda's correct emit). Currently-served JSON is incidentally correct because AE's fresh-invoke today happened to be single-invocation (no race). Tomorrow's scheduled SFN execution races again; the structural defect re-fires until the dual-writer-same-key pattern is eliminated. Phase 0.5 probe determines whether `yang-generate-benchmark-returns` is pure-redundant (clean retire) or has a unique downstream consumer (redesign required).
  </context>

  <scope>
    <step>Phase 0.5 -- PURPOSE + CONSUMER LANDSCAPE PROBE (~30min). Determine `yang-generate-benchmark-returns` role:
      - Read `infra/aws/lambda/ci/lambda-source-map.json` entry for the Lambda (purpose + last-deployed lineage)
      - Read the Lambda's source code (per source-map; what does its logic look like? Same as `yang-model-portfolio-benchmarks`? Subset/superset/different?)
      - Read the SFN state machine definition (`infra/aws/terraform/yang-pipeline/` per AE inspection) -- which state(s) invoke `yang-generate-benchmark-returns`? Parallel-write with `yang-model-portfolio-benchmarks` or sequential? Same input event?
      - `comp-blast yang-generate-benchmark-returns` -- enumerate ALL downstream consumers (S3-write paths + any direct callers from other Lambdas/SFN steps/EventBridge rules)
      - `comp-routes trace` for the OUTPUT_KEY_COMPREHENSIVE S3 path -- is there a portal endpoint that indirectly consumes via the shared key? (Both Lambdas write the same key, so consumer trace points to the key, not to either Lambda directly; AE judgment on whether to trace key vs Lambda separately.)
      - **Verdict:**
        * **PURE-REDUNDANT** = `yang-generate-benchmark-returns` writes the same S3 key + same shape + no unique downstream consumer + the newer `yang-model-portfolio-benchmarks` covers the same role -> safe to retire.
        * **UNIQUE-CONSUMER** = `yang-generate-benchmark-returns` has a unique downstream consumer OR different output shape OR serves a role `yang-model-portfolio-benchmarks` doesn't cover -> retire is unsafe; redesign required.
      - Document findings + verdict in a brief at `docs/briefs/mdlp-volaud-003-phase0.5-probe-{YYYYMMDD}.md` OR in the session log per AE convention. Channel-push verdict to COO + CC CTO + CC DS~B for ratification on the Phase 1 branch.</step>
    <step>Phase 1 BRANCH A -- RETIRE (default if Phase 0.5 verdict = pure-redundant). Terraform-only deploy per Rule 1:
      - Remove `yang-generate-benchmark-returns` SFN state transition from the yang-pipeline state machine (or whatever SFN it's wired into; AE verifies via Phase 0.5)
      - Remove the Lambda function + its IAM role/policies
      - Remove the source-map entry in `infra/aws/lambda/ci/lambda-source-map.json`
      - Remove any Lambda Layer reference if the layer was Lambda-specific (else leave the layer; comp-iam gaps verifies)
      - Commit via .tools/safe-commit.sh --author -> push CLOUD -> plan -> apply -> 0-diff verified -> tag `yang-v{next}` (run `git tag -l "yang-v*" | sort -V | tail -5` first; current is `yang-v2.4.2`) -> push --follow-tags -> record-terraform-deploy
      - ~30-45min wall</step>
    <step>Phase 1 BRANCH B -- REDESIGN (only if Phase 0.5 verdict = unique-consumer). PAUSE + RE-CONVERGE TO CTO. Do NOT proceed without CTO architectural ruling on the redesign shape:
      - Possible redesigns: (i) separate S3 keys for the two Lambdas (cleanest if both serve distinct consumers); (ii) merge logic into one Lambda + retire the other (similar to Branch A but requires logic merge); (iii) sequential SFN states with explicit ordering (eliminates race but keeps both writers + same key, fragile).
      - AE 0.5 channel-pushes the Phase 0.5 verdict + redesign options to COO + CC CTO; pauses Phase 1 work until CTO rules.</step>
    <step>Phase 2 -- empirical verification (BOTH branches):
      - AC1 anchor-reproduction: trigger an SFN execution with controlled payload post-fix; verify SINGLE S3 write (no v1+v2 versioning race); verify the emit values are correctly-differentiated per period across all 5 models.
      - AC2 cross-empirical: same fresh-invoke pattern AE 0.5 used today (17:18Z, single-invocation); reproduces post-fix with no collapse.
      - AC3 (post-tomorrow-scheduled-fire): verify the natural 2026-05-20T14:00Z scheduled SFN execution produces single-write + correct values. Wait for the cron OR document AE-side justification for proxy via manual SFN trigger.
      - 6-of-9 long-window cells (1M, QTD, 1Q, YTD, 1Y, SI) must STILL reproduce TO THE CENT against DS~B's probe baseline (no regression on the microstructure-validated cells from .001 audit).</step>
    <step>Phase 3 -- RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform~B (DS~B's probe baseline is the cross-validator for Phase 2 AC2; their audit verdict on the 6-of-9 cells gates the no-regression check). Record: Phase 0.5 verdict + branch taken; commit SHA + tag + apply timestamp; AC1/AC2/AC3 transcripts; 6-of-9 long-window no-regression check. On RAVC2-accept: MDLP_VOLAUD.json status -> complete; REGISTRY row moves to Completed (3-step atomic per closure discipline); MDLP_VOLAUD project closes.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Anchor-reproduction: SFN execution with controlled payload post-fix produces SINGLE S3 write (S3 versioning shows one new version, not two; or only one PutObject visible in CloudTrail for the key) + correctly-differentiated 1D/WTD/MTD values across all 5 models. Transcript captured.</ac>
    <ac id="AC2">Cross-empirical: fresh `aws lambda invoke` on `yang-model-portfolio-benchmarks` (same pattern as AE 0.5's 17:18Z today) reproduces correctly-differentiated values + matches DS~B local probe to-the-cent. Confirms no regression on the surviving Lambda.</ac>
    <ac id="AC3">Tomorrow's scheduled 2026-05-20T14:00Z SFN execution produces single-write + correct values. Verify via S3 versioning post-fire + value-spot-check on the served JSON. (OR AE-side justification + manual SFN trigger as proxy; document choice.)</ac>
    <ac id="AC4">6-of-9 long-window no-regression: 1M, QTD, 1Q, YTD, 1Y, SI cells reproduce TO THE CENT against DS~B's MDLP_VOLAUD.001 probe baseline. NO regression on microstructure-validated cells.</ac>
    <ac id="AC5">Terraform-only deploy per Rule 1: commit via safe-commit.sh -> push CLOUD -> plan -> apply -> 0-diff verified -> tagged yang-v{next} (latest-tag-checked) -> pushed --follow-tags -> record-terraform-deploy.</ac>
    <ac id="AC6">No emoji (ASCII only per CLAUDE.md). Pre-commit gate on any .py touched (likely none -- pure Terraform + source-map removal). Session log under `org/tier2_senior/0.5.0_AE_OpalETL/logs/YYYY-MM-DD/` with: Phase 0.5 probe findings + verdict + Branch A vs B decision; AC1/AC2/AC3/AC4 transcripts; comp-tools row.</ac>
    <ac id="AC7">Compiler-tools: comp-blast yang-generate-benchmark-returns (Phase 0.5 + post-retire empty-check) + comp-iam gaps (post-retire orphan IAM check) + comp-pipescript io yang-generate-benchmark-returns (Phase 0.5 baseline + post-retire empty) + comp-routes trace for the OUTPUT_KEY_COMPREHENSIVE path (Phase 0.5 consumer trace).</ac>
    <ac id="AC8">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform~B with: Phase 0.5 verdict + branch + rationale; commit SHA + tag + apply timestamp; AC1/AC2/AC3/AC4 transcripts; 6-of-9 no-regression check. On accept: MDLP_VOLAUD.json status -> complete; REGISTRY row moves to Completed (3-step atomic); MDLP_VOLAUD project closes.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      Phase 0.5 compiler-tools probe:
      - comp-pipescript io yang-generate-benchmark-returns (purpose + I/O baseline)
      - comp-blast yang-generate-benchmark-returns (downstream consumer enumeration)
      - comp-routes trace for OUTPUT_KEY_COMPREHENSIVE S3 path (portal-consumer indirect check)
      Direct file-read of source-map entry + Lambda source code + SFN state machine definition.
    </before_write>
    <before_commit>
      comp-iam service yang-generate-benchmark-returns (IAM baseline pre-removal).
    </before_commit>
    <after_commit>
      comp-blast yang-generate-benchmark-returns (expect EMPTY post-retire) + comp-iam gaps (orphan-perm check post-removal) + comp-pipescript deployed yang-pipeline MATCH post-apply.
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Sequence AFTER AE 0.5's current SSCN_DIVDEF.004 (their CURRENT priority per 2.0.0_SA_COO~B routing; do NOT interrupt mid-flight). DS~B is the cross-validator for Phase 2 AC2 + AC4 no-regression check (their probe baseline + audit verdict from .001 are the canonical verification anchors); CC on RAVC2. Lane: AE 0.5 stays throughout (same as .002). If Phase 1 retire requires Terraform-removal in a module owned by another AE (e.g., AE 0.7 if yang-pipeline's SFN was codified separately), lane-split surfaces operationally to COO for routing -- channel-push to COO if AE 0.5 discovers cross-lane ownership during Phase 0.5 probe.
  </cross_domain_coordination>

  <out_of_scope>
    Original MDLP_VOLAUD.002 target hypothesis (yang-model-portfolio-benchmarks runtime divergence under AWSSDKPandas-Python312:16 Layer) -- DISPROVED by AE 0.5's Phase 0 finding; not a real defect class on that Lambda. 6-of-9 long-window microstructure-validated cells (from DS~B's .001 audit) -- AUDIT-CLOSED; this TO must preserve them (AC4 no-regression check) but does NOT re-litigate them.
  </out_of_scope>

  <deliverables>
    - Phase 0.5 verdict (pure-redundant vs unique-consumer) + brief OR session-log Findings block.
    - Phase 1 deliverable per branch: RETIRE (Terraform SFN-state removal + Lambda removal + IAM cleanup + source-map entry removal + yang-v{next} tag) OR REDESIGN-PAUSE (CTO re-converge with options).
    - Phase 2 verification: AC1/AC2/AC3 transcripts + AC4 6-of-9 no-regression check.
    - Session log under org/tier2_senior/0.5.0_AE_OpalETL/logs/YYYY-MM-DD/ with: Phase 0.5 + Phase 1 + Phase 2 transcripts; comp-tools row.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + CC 0.4.0_DS_ClientPlatform~B.
  </deliverables>
</task_order>
