<task_order>
  <metadata>
    <id>MDLP_VOLAUD.002</id>
    <slug>ae-lambda-runtime-1d-wtd-mtd-anomaly-investigation</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-05-19</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>MDLP_VOLAUD</project_code>
    <priority>P2 -- audit-surfaced Lambda-output anomaly. NOT a partner-facing P0 (the long-window cells reproduce correctly to the cent + the audit's microstructure verdict holds for 6 of 9 periods; 1D/WTD/MTD collapse affects a short-window-only display and DS~B's audit already documented downstream-consumer guidance). Investigation cadence; AE 0.5.0 picks up after current commitments.</priority>
    <sla>~1d wall -- diagnostic invoke + local-vs-Lambda diff + root-cause identification (most likely Lambda Layer / runtime pandas-numpy divergence; possibly a Linux-container date-arithmetic non-determinism, possibly a Lambda-runtime-specific Series.tail() / index-slicing behavior under AWSSDKPandas-Python312:16). Fix wall depends on root cause (Layer pin bump / runtime version pin / code adjustment).</sla>
  </metadata>

  <references>
    <origin>1.0.0_SA_CTO MCP to 2.0.0_SA_COO 2026-05-19 ~15:10Z (ACK 4-item roll-up + routing MDLP_VOLAUD.002 to COO per standing "extension TO if audit surfaces anomaly" offer). DS~B MDLP_VOLAUD.001 RAVC2 brief at `docs/briefs/mdlp-etf-vs-index-volatility-audit-20260519.md` -- "Lambda-output anomaly -- collapsed 1D / WTD / MTD" section is the canonical investigation starting kit.</origin>
    <pre_authorization>MDLP_VOLAUD.json phase clause: "If audit surfaces anomaly -> may extend with Yang-pipeline fix TO (AE 0.5.0 lane)". DS~B audit's two-part verdict cleanly partitioned the microstructure-explainable cells (6 of 9, audit-closed) from the Lambda-output anomaly cells (3 of 9, this TO).</pre_authorization>
    <brief>docs/briefs/mdlp-etf-vs-index-volatility-audit-20260519.md (DS~B authored 2026-05-19, RAVC2 to CTO; see particularly the "Lambda-output anomaly -- collapsed 1D / WTD / MTD" section and the AC5 anomaly inventory row "Lambda-output collapsed period values".)</brief>
    <probe>org/tier2_senior/0.4.0_DS_ClientPlatform/probes/mdlp_volaud_001_etf_vs_index_audit.py (DS~B's reproducible Phase-0 baseline -- AE can compare against `aws lambda invoke` output on the same pickle).</probe>
    <anchor_state>The currently-served `model_portfolio_benchmarks.json` (`s3://opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json`, data_as_of=2026-05-18, generated_at=2026-05-19T11:25:03Z) shows the 1D / WTD / MTD byte-identical collapse for every model. AE .002 produces a bit-for-bit diff against this anchor.</anchor_state>
    <lambda>yang-model-portfolio-benchmarks (Yang pipeline, AE 0.5.0 lane per source-map). Deployed LastModified 2026-05-04T18:54:55Z. Deployed code md5 `81cdb6063971c32eec6aa1a20bdd914d` matches `infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py` byte-for-byte (587 lines). Code is NOT the source of drift.</lambda>
    <layer>arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python312:16 (only environmental delta separating local from deployed). Layer 16 ships pandas 2.2.x / numpy 1.26.x.</layer>
    <pickle>s3://opal-data-portal-v2/benchmarks/data_20260519_v1.pkl (resolved via benchmarks/LATEST.json -> data_pkl). DS~B's local probe consumed exactly this artifact and produced correctly-differentiated 1D / WTD / MTD values across all 5 models.</pickle>
    <ds_hypothesis>DS~B's brief §"Lambda-output anomaly" closing: "hypothesis: a Lambda-runtime (vs local) divergence in pandas Series.tail() / index-slicing under the AWSSDKPandas layer, OR a non-determinism in INCEPTION_DATE / end_date arithmetic on the Lambda's Linux container." Algorithmic (collapse cross-cuts 3 vol axes + 3 return axes for all 5 models), not numerical (would be a per-cell precision drift, not a 3-key collapse). First investigation step (per DS~B): `aws lambda invoke` with controlled event payload + compare actual JSON output to a local `python lambda_function.py` run on the same pickle.</ds_hypothesis>
    <pipeline_rule>Rule 1 (Terraform-only Lambda deploy) for any code fix; Rule 13 doesn't directly apply (this is a Yang Lambda not a DS-owned gold script). AE 0.5.0 lane per yang-pipeline ownership.</pipeline_rule>
  </references>

  <context>
    For all 5 models in the published `model_portfolio_benchmarks.json`, the 1D / WTD / MTD entries are byte-identical: returns, volatilities (INDEX + ETF + model), and spreads all carry the same scalar across the three period keys. Local execution of `lambda_function.py` against the same source pickle on the same date produces correctly differentiated values per period. Deployed binary md5 == repo md5 -- the code path is not the variable. The only environmental delta is the Lambda runtime + AWSSDKPandas Layer. This is an algorithmic divergence (cross-cuts all 3 axes for all 5 models in a coherent way), not a precision drift. Most-likely root causes (rank-ordered, AE refines on inspection): (i) pandas/numpy version delta between Layer 16 and local that affects `.tail()` / boolean-index / period-slicing semantics in `calculate_period_returns`; (ii) date arithmetic divergence on the Lambda Linux container vs local (Windows-Bash / macOS) for `end_date - timedelta(days=...)` when interacting with `INCEPTION_DATE` constants; (iii) a Lambda-runtime-only path branch (e.g. an environment-variable-conditional code path the local run doesn't trigger). The audit's microstructure verdict for the 6 long-window periods stands independently; this TO closes the 1D / WTD / MTD residual.
  </context>

  <scope>
    <step>Phase 0 -- empirical anchor reproduction. `aws lambda invoke` against `yang-model-portfolio-benchmarks` with the exact StepFunctions event that wrote the current published JSON (RequestId `fe5f8952-6553-4eaf-bb17-e37947c7008a` per DS~B's brief; event payload reconstructed from `data_pkl_key=benchmarks/data_20260519_v1.pkl` + `data_as_of_date=2026-05-18`). Compare the Lambda's actual JSON output (post-invoke, NOT the S3-served file) against DS~B's local probe output on the same pickle. Confirm the byte-collapse reproduces on a fresh Lambda invoke (not just on the S3-cached emit). Capture both transcripts.</step>
    <step>Phase 1 -- root-cause isolation. Given the deployed binary matches repo byte-for-byte, instrument `calculate_period_returns` (lines :370-458) and `calculate_volatility` (lines :470-477) with temporary diagnostic logging (CloudWatch INFO-level prints showing: (a) the n-row count entering the 1D / WTD / MTD branches; (b) the actual date boundary computed; (c) the input series sample). Deploy the instrumented version as a separate Lambda alias (`debug` or `investigation`) per Lambda Deployment Protocol -- do NOT touch the live `$LATEST` alias. Re-invoke with the same event; capture the divergence point. Most-likely outcomes:
      (a) **Layer divergence:** the diagnostic shows the same date arithmetic but different series-slicing output -> pandas/numpy version delta between Layer 16 and local. Fix path: bump to a newer AWSSDKPandas Layer (Layer 17/18 if available) AND/OR add an explicit `requirements.txt`-pinned pandas to a Lambda Layer the function owns directly.
      (b) **Date arithmetic divergence:** the diagnostic shows different date boundaries on the Lambda vs local -> `INCEPTION_DATE` / `end_date` / `timedelta` interaction differs on Linux container. Fix path: explicit UTC-anchored date computation; remove any implicit timezone handling.
      (c) **Lambda-runtime branch:** the diagnostic shows a code path the local run doesn't reach -> environment-conditional logic. Fix path: remove the environment dependency or make it explicit + tested.</step>
    <step>Phase 2 -- fix + Terraform-only deploy per CLAUDE.md Rule 1: implement the fix in `infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py` (or in iam.tf / yang-pipeline Terraform if the fix is Layer-bump). Commit via `.tools/safe-commit.sh --author` per ADHC_OWNPTH.007 (Rule 14: `.tools/ds-commit-gate.sh` on the .py edit). Push CLOUD -> build/upload Lambda zip per yang-pipeline build-and-upload pattern -> plan -> apply -> verify 0-diff -> tag `yang-v{next}` (run `git tag -l "yang-v*" | sort -V | tail -5` first; current is `yang-v2.4.2`) -> push --follow-tags -> record-terraform-deploy.sh. Remove the diagnostic instrumentation BEFORE final apply (or keep it conditional on a `DIAGNOSTIC=1` env var per AE judgment).</step>
    <step>Phase 3 -- empirical verification. Trigger a fresh StepFunctions execution (or `aws lambda invoke` directly with the same event payload) on the post-fix Lambda; pull the resulting JSON; verify the 1D / WTD / MTD entries are now differentiated per period across all 5 models AND that the AC3 6-of-9 long-window cells (1M, QTD, 1Q, YTD, 1Y, SI) still reproduce TO THE CENT against DS~B's probe baseline (no regression on the microstructure-validated cells). Cross-validate the 3 newly-fixed cells against DS~B's local probe: same Lambda input + same pickle = same output, byte-for-byte, no divergence remaining.</step>
    <step>Phase 4 -- RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + DS~B (DS~B authored the brief + carries the local probe as the cross-validator). Record: the diagnostic transcripts; the identified root cause + which hypothesis (a/b/c) held + supporting evidence; the chosen fix; the Lambda tag + commit SHA + deploy timestamp; the post-fix `aws lambda invoke` output diff vs anchor (proving the collapse cleared); the 6-of-9 long-window cells re-verified to-the-cent. On RAVC2-accept, MDLP_VOLAUD project closes (audit verdict + Lambda fix both landed).</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Phase 0 anchor reproduction confirmed: fresh `aws lambda invoke` against the live Lambda with the same event that wrote the published JSON produces the same byte-identical 1D/WTD/MTD collapse across all 5 models. Both Lambda-invoke output and DS~B's local probe output captured for diff.</ac>
    <ac id="AC2">Root cause identified with empirical evidence (CloudWatch diagnostic log capture from a `debug`-alias instrumented invoke). Which of hypotheses (a) Layer/runtime divergence, (b) date arithmetic divergence, (c) Lambda-runtime-only branch was the actual cause + supporting transcript.</ac>
    <ac id="AC3">Fix implemented + Terraform-only deployed per Rule 1: plan -> apply -> 0-diff verified -> tagged `yang-v{next}` (latest-tag-checked) -> pushed --follow-tags -> record-terraform-deploy. Diagnostic instrumentation either removed or made env-var-conditional per AE judgment + documented.</ac>
    <ac id="AC4">Post-fix verification: fresh Lambda invoke -> 1D / WTD / MTD differentiated per period across all 5 models (no byte-collapse) AND the 6 of 9 microstructure-validated long-window cells (1M, QTD, 1Q, YTD, 1Y, SI) still reproduce TO THE CENT against DS~B's probe (no regression).</ac>
    <ac id="AC5">No emoji in code or logs (ASCII only per CLAUDE.md). Pre-commit gate (.tools/ds-commit-gate.sh) exit 0 on any .py touched (Rule 14 -- if ADHC_DSFLOW.007 MSYS fix has not landed yet, run the 3 checks by hand same as AE 0.7 did for MDPF). Session log with the Compiler Tools section.</ac>
    <ac id="AC6">Compiler-tools: `comp-pipescript io yang-model-portfolio-benchmarks` (expect empty per DS~B's finding -- Lambda not in graph; document the gap as separate ADHC follow-up, not blocking this TO) + `comp-iam service yang-model-portfolio-benchmarks` if any new boto3 surface added (likely none -- diagnostic logging uses existing CW perms) + `comp-pipescript deployed yang-pipeline` MATCH post-deploy + direct iam.tf read confirming no new permissions required.</ac>
    <ac id="AC7">RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + DS~B (cross-validator) with: diagnostic transcripts; root cause + hypothesis verdict; deployed commit SHA + tag + apply timestamp; AC1/AC2/AC3/AC4 transcripts; post-fix diff vs anchor; 6-of-9 cells regression check transcript. On accept, MDLP_VOLAUD.json status -> complete + REGISTRY row moves to Completed (3-step atomic per ADHC_HALTGT / closure-discipline standard).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      `comp-pipescript io yang-model-portfolio-benchmarks` (expect empty per DS~B Phase-0 finding -- Lambda not indexed in comp graph; document the gap as separate ADHC follow-up, not blocking this TO).
      Direct file-read of `infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py` lines 333-477 for the methodology reference (`get_term_returns` + `calculate_period_returns` + `calculate_volatility`).
    </before_write>
    <before_commit>
      `.tools/ds-commit-gate.sh lambda_function.py` exit 0 (Rule 14 -- applies to all Python edits; run-by-hand the 3 checks if ADHC_DSFLOW.007 MSYS fix has not landed yet).
      `comp-iam service yang-model-portfolio-benchmarks` if any new boto3 surface added (likely none).
    </before_commit>
    <after_commit>
      `comp-pipescript deployed yang-pipeline` MATCH post-apply (rules out Lambda stale-deployed-vs-tag state).
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    None blocking -- yang-pipeline Lambda is AE 0.5.0-owned per source-map; no shared S3 artifacts touched (the source pickle + the published JSON are read/written by this same Lambda; downstream portal consumers read the JSON via CloudFront). DS~B owns the local probe (cross-validator role, RAVC2 CC); CTO endorsed; COO routes. No concurrent-agent pressure (no other MDLP work in-flight).
  </cross_domain_coordination>

  <out_of_scope>
    The 6 long-window microstructure-validated cells (1M, QTD, 1Q, YTD, 1Y, SI) are AUDIT-CLOSED per DS~B; this TO does NOT re-litigate them. The "indicative-only pending Lambda fix" downstream-consumer guidance (DS~B brief §"Recommendation #3") is a separate FE-side note for the portal Model Portfolios Benchmarks tab, not in this TO's scope. Lambda-comp-graph registration (the "not indexed in graph" finding) is a separate ADHC follow-up, not a fix-it-here scope.
  </out_of_scope>

  <deliverables>
    - Root-cause diagnostic transcripts (CloudWatch + local probe) + identified hypothesis.
    - Lambda fix in `infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py` (or Layer bump in yang-pipeline Terraform if Layer-side).
    - yang-v{next} tag + Terraform 0-diff apply + record-terraform-deploy.
    - Session log under `org/tier2_senior/0.5.0_AE_OpalETL/logs/YYYY-MM-DD/` with: Phase 0 reproduction transcript, Phase 1 root-cause transcript, fix implementation rationale, AC4 post-fix verification transcript (including 6-of-9 no-regression check), comp-tools row.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO + 0.4.0_DS_ClientPlatform~B (cross-validator). MDLP_VOLAUD.json status -> complete on RAVC2-accept (3-step atomic closure: JSON + REGISTRY row move to Completed + this TO status flip).
  </deliverables>
</task_order>
