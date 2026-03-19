"""
KA Testing: Real-world alignment protocol test against ADVI_CLSUNI PRD.

Uses the duplicated runtime at org/ka_testing/runtime/.

Runs the alignment protocol with real Workers reading real ajb_workspace files.
Workers have tool access and read actual source code.

Exercises:
  Phase 1: Mechanical StateRequest generation
  Phase 2: Real Worker state collection (read_file, list_dir, grep_files)
  Phase 3: Coordinator synthesis from real reports + enforce_truth_state()
  Phase 4: Coordinator produces task orders from assessment (vs PRD-only baseline)

Usage:
  cd ajb_workspace/
  HIERARCHY_LLM_PROVIDER=openai python -m org.ka_testing.advi_clsuni.run_alignment
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup -- import from org/ka_testing/runtime/
# ---------------------------------------------------------------------------
AJB_WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
KA_ROOT = AJB_WORKSPACE / "org" / "ka_testing"
sys.path.insert(0, str(KA_ROOT))

from runtime.alignment import (
    Claim,
    StateRequest,
    StateReport,
    AlignmentAssessment,
    invoke_worker_for_state_direct,
    synthesize_alignment,
    assessment_to_dict,
    _format_report_for_synthesis,
    invoke_worker_for_execution,
    PreFlightCheck,
    ExecutionResult,
)

RESULTS_DIR = KA_ROOT / "advi_clsuni" / "results"

# ---------------------------------------------------------------------------
# PRD section (verbatim excerpt covering the cross-agent interfaces)
# ---------------------------------------------------------------------------

PRD_SECTION = """
BD Securities Classification Unification (ADVI_CLSUNI)

ARCHITECTURE:
- New DynamoDB table 'bd-securities' with ticker PK, asset_class/sub_asset_class GSIs
- Canonical taxonomy: equity | fixed_income | alternatives (cash is computed residual)
- lib/etf_classifier.py: shared module used by EC2 gold scripts AND Lambda

DATA CONTRACT CHANGES:
- client_timeseries/{rel_id}.json mix fields: BEFORE: equity, fixed_income, structured_notes, cash, other -> AFTER: equity, fixed_income, alternatives
- MixTimeseriesPoint TypeScript: drops structured_notes, cash, other; adds alternatives
- FirmMixPeriodPoint: same change pattern
- Cash is NOT stored -- computed as 1 - equity - fixed_income - alternatives

CROSS-AGENT INTERFACES:
- DS writes lib/etf_classifier.py (used by EC2 gold scripts)
- DT copies lib/etf_classifier.py to opal-partners-data Lambda dir, builds/deploys
- DS updates 06b output JSON shape (drops structured_notes/cash/other, adds alternatives)
- RD updates TypeScript types to match new JSON shape
- DS updates opal-partners-data Lambda to use ETFClassifier instead of static dict

SEQUENCING:
- AE_CloudOps creates DynamoDB table first (WS1)
- DS writes all code (WS2-WS6) -- must be combined with GLDRST path changes
- DT deploys after WS1 Terraform + DS WS6 commit
- AE_PartnerETL seeds + classifies + runs gold after table exists + DS commits
- RD can work in parallel (portal types don't depend on backend)
"""

# ---------------------------------------------------------------------------
# Worker prompts (derived from real agent mandates)
# ---------------------------------------------------------------------------

WORKER_DS_PROMPT = """You are a data science agent for the BD pipeline (0.4.0_DS_ClientPlatform).
You own the gold layer scripts in data/black_diamond/scripts/gold/, the ETF
classification logic, and the Lambda handler code in
infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/.

You produce: gold layer JSON artifacts (client_timeseries, firm_mix_views,
advisors/), Lambda endpoints for the advisor intelligence API, and shared
Python modules used by both EC2 and Lambda.

Your key files:
- data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py
- data/black_diamond/scripts/gold/lib/ (if it exists)
- infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/
"""

WORKER_RD_PROMPT = """You are a frontend research/development agent (0.4.2_RD_AdvisorIntelligence).
You own the portal TypeScript types and React components for the Advisor
Intelligence pages.

You produce: TypeScript interfaces, React components, chart configurations,
and derived data computations in the portal frontend.

Your key files:
- portal/src/pages/AdvisorIntelligence/types.ts
- portal/src/pages/AdvisorIntelligence/ClientsTab.tsx
- portal/src/pages/AdvisorIntelligence/components/
"""

WORKER_DT_PROMPT = """You are a deployment/infrastructure agent (0.4.0_DT_ClientPlatform).
You own Lambda deployment via Terraform, the build-and-upload pipeline,
and the shared-infra Terraform module.

You produce: Terraform configurations, Lambda deployment artifacts,
API Gateway route configurations.

Your key files:
- infra/aws/terraform/partners-api/
- infra/aws/terraform/shared-infra/
- infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/
"""

WORKER_AE_CLOUDOPS_PROMPT = """You are an infrastructure/cloud operations agent (0.7.0_AE_CloudOps).
You own shared AWS infrastructure: DynamoDB tables, S3 buckets, IAM roles,
and the shared-infra Terraform module.

You produce: Terraform configurations for shared resources, IAM policy
updates, DynamoDB table definitions.

Your key files:
- infra/aws/terraform/shared-infra/
- infra/aws/ec2/EC2_MANIFEST.json
"""

WORKER_AE_PARTNERETL_PROMPT = """You are a partner ETL operations agent (0.6.0_AE_PartnerETL).
You own EC2 deployment, gold layer execution, seed/classification scripts,
and the operational pipeline that runs data transformations.

You produce: deployed code on EC2, gold layer output artifacts, classification
database entries, operational run logs.

Your key files:
- data/black_diamond/scripts/gold/run_gold_layer.sh
- data/black_diamond/scripts/classification/ (if it exists)
- infra/aws/ec2/
"""

COORDINATOR_PROMPT = """You are a Coordinator agent. Your job is to sequence
and decompose work across multiple Worker agents. You evaluate interface
compatibility, identify conflicts, and produce dependency graphs.

You are pragmatic and precise. When analyzing Worker state reports, you
check field-level compatibility: exact field names, exact types, exact
paths. Semantic similarity is not enough -- advisorId and advisor_id are
different field names that will break at integration."""

# ---------------------------------------------------------------------------
# Worker roster
# ---------------------------------------------------------------------------

WORKER_CONFIG = [
    {"identity": "AE-CLOUDOPS", "serial": "AE.CO.1", "prompt": WORKER_AE_CLOUDOPS_PROMPT},
    {"identity": "DS-WORKER", "serial": "DS.CP.1", "prompt": WORKER_DS_PROMPT},
    {"identity": "RD-WORKER", "serial": "RD.AI.1", "prompt": WORKER_RD_PROMPT},
    {"identity": "DT-WORKER", "serial": "DT.CP.1", "prompt": WORKER_DT_PROMPT},
    {"identity": "AE-PARTNERETL", "serial": "AE.PE.1", "prompt": WORKER_AE_PARTNERETL_PROMPT},
]


def run_real_alignment():
    """Run full alignment protocol Phases 1-4 against ADVI_CLSUNI PRD."""

    working_dir = str(AJB_WORKSPACE)
    provider = os.environ.get("HIERARCHY_LLM_PROVIDER", "anthropic")
    print(f"Working directory: {working_dir}", file=sys.stderr)
    print(f"Provider: {provider}", file=sys.stderr)

    results = {
        "test": "ka_advi_clsuni_real_alignment",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": provider,
        "working_directory": working_dir,
        "phases": {},
    }

    # -----------------------------------------------------------------------
    # Phase 1: Mechanical StateRequest generation
    # -----------------------------------------------------------------------
    print("\n=== Phase 1: StateRequest generation (mechanical) ===", file=sys.stderr)
    state_requests = [
        StateRequest(
            worker_id=w["identity"],
            worker_serial=w["serial"],
            prd_section=PRD_SECTION,
            scoped_question=(
                "What do you currently produce, what exists, and "
                "what is missing relative to this design?"
            ),
        )
        for w in WORKER_CONFIG
    ]
    results["phases"]["phase1"] = {
        "requests": len(state_requests),
        "workers": [w["serial"] for w in WORKER_CONFIG],
    }
    print(f"  Generated {len(state_requests)} StateRequests", file=sys.stderr)

    # -----------------------------------------------------------------------
    # Phase 2: Real Worker state collection
    # -----------------------------------------------------------------------
    print("\n=== Phase 2: Worker state collection (real LLM + real files) ===", file=sys.stderr)
    state_reports = []
    phase2_results = []

    for i, request in enumerate(state_requests):
        worker = WORKER_CONFIG[i]
        print(f"\n  --- {worker['serial']} ({worker['identity']}) ---", file=sys.stderr)
        start = time.time()

        report = invoke_worker_for_state_direct(
            system_prompt=worker["prompt"],
            state_request=request,
            working_directory=working_dir,
            max_iterations=5,
            max_read_chars=10000,
        )

        wall_time = time.time() - start
        state_reports.append(report)

        # Capture metrics
        from runtime.alignment import _get_llm_module
        _llm = _get_llm_module()
        trace = _llm.get_last_trace()

        report_metrics = {
            "worker_id": worker["identity"],
            "worker_serial": worker["serial"],
            "wall_time_s": round(wall_time, 2),
            "tokens_input": trace.input_tokens if trace else 0,
            "tokens_output": trace.output_tokens if trace else 0,
            "tool_calls": trace.tool_call_count if trace else 0,
            "iterations": trace.iterations if trace else 0,
            "files_read": [
                tc.inputs.get("file_path", "")
                for tc in (trace.tool_calls if trace else [])
                if tc.name == "read_file"
            ],
            "claims_produced": len(report.what_i_produce),
            "claims_exists": len(report.what_exists),
            "claims_missing": len(report.what_is_missing),
            "requires_from_others": report.requires_from_others,
            "confidence_distribution": _count_confidence(report),
        }
        phase2_results.append(report_metrics)

        print(f"    Time: {report_metrics['wall_time_s']}s", file=sys.stderr)
        print(f"    Tokens: {report_metrics['tokens_input']}in / {report_metrics['tokens_output']}out", file=sys.stderr)
        print(f"    Tool calls: {report_metrics['tool_calls']} ({report_metrics['iterations']} iter)", file=sys.stderr)
        print(f"    Files read: {report_metrics['files_read']}", file=sys.stderr)
        print(f"    Claims: {report_metrics['claims_produced']}prod / {report_metrics['claims_exists']}exist / {report_metrics['claims_missing']}miss", file=sys.stderr)
        print(f"    Requires from others: {report_metrics['requires_from_others']}", file=sys.stderr)
        print(f"    Confidence: {report_metrics['confidence_distribution']}", file=sys.stderr)

    results["phases"]["phase2"] = phase2_results

    # -----------------------------------------------------------------------
    # Phase 3: Coordinator synthesis
    # -----------------------------------------------------------------------
    print("\n=== Phase 3: Coordinator synthesis ===", file=sys.stderr)
    start = time.time()

    assessment = synthesize_alignment(
        state_reports=state_reports,
        prd_section=PRD_SECTION,
        coordinator_identity="KA-TEST-COORDINATOR",
        coordinator_prompt=COORDINATOR_PROMPT,
    )

    wall_time = time.time() - start

    phase3 = {
        "wall_time_s": round(wall_time, 2),
        "token_usage": assessment.token_usage,
        "interfaces": [
            {
                "producer": i.producer, "consumer": i.consumer,
                "status": i.status,
                "producer_shape": str(i.producer_shape)[:300],
                "consumer_shape": str(i.consumer_shape)[:300],
                "resolution": i.resolution[:300] if i.resolution else None,
                "producer_confidence": i.producer_confidence,
                "consumer_confidence": i.consumer_confidence,
            }
            for i in assessment.interfaces
        ],
        "gaps": assessment.gaps,
        "conflicts": [
            {"type": c.type, "workers": c.workers, "description": c.description[:300]}
            for c in assessment.conflicts
        ],
        "dependency_graph": [
            {"producer": d.producer, "consumer": d.consumer,
             "artifact": d.artifact, "required_before": d.required_before}
            for d in assessment.dependency_graph
        ],
        "schisms": assessment.schisms,
    }
    results["phases"]["phase3"] = phase3

    print(f"  Time: {phase3['wall_time_s']}s", file=sys.stderr)
    print(f"  Tokens: {assessment.token_usage}", file=sys.stderr)
    print(f"  Interfaces ({len(assessment.interfaces)}):", file=sys.stderr)
    for i in assessment.interfaces:
        print(f"    {i.producer} -> {i.consumer}: {i.status}", file=sys.stderr)
        if i.resolution:
            print(f"      Resolution: {i.resolution[:120]}", file=sys.stderr)
    print(f"  Gaps: {assessment.gaps}", file=sys.stderr)
    print(f"  Conflicts ({len(assessment.conflicts)}):", file=sys.stderr)
    for c in assessment.conflicts:
        print(f"    [{c.type}] {c.description[:120]}", file=sys.stderr)
    print(f"  Dependencies ({len(assessment.dependency_graph)}):", file=sys.stderr)
    for d in assessment.dependency_graph:
        print(f"    {d.producer} -> {d.consumer}: {d.artifact} (before: {d.required_before})", file=sys.stderr)
    if assessment.schisms:
        print(f"  SCHISMS: {assessment.schisms}", file=sys.stderr)

    # -----------------------------------------------------------------------
    # Phase 4: Task orders from assessment vs PRD-only baseline
    # -----------------------------------------------------------------------
    print("\n=== Phase 4: Task order comparison (assessment-enriched vs PRD-only) ===", file=sys.stderr)

    from runtime.alignment import _get_llm_module
    _llm = _get_llm_module()
    from runtime.config import ARCHETYPE_MODELS

    # 4a: Assessment-enriched task orders
    alignment_context = _format_alignment_for_task_orders(assessment)
    enriched_prompt = (
        f"## Design\n\n{PRD_SECTION}\n\n"
        f"{alignment_context}\n\n"
        f"## Task\n\n"
        "Produce task orders for each Worker. Each task order should specify:\n"
        "- Which Worker\n"
        "- What they must produce (specific file paths, field names, shapes)\n"
        "- Interface contracts (exact field names from the alignment assessment)\n"
        "- Dependencies (which task must complete first)\n"
        "- Acceptance criteria\n\n"
        "Return as a structured list.\n"
    )

    start = time.time()
    enriched_response = _llm.invoke_llm(
        system=COORDINATOR_PROMPT,
        user=enriched_prompt,
        model=ARCHETYPE_MODELS.get("coordinator"),
        tools=[],
        max_tokens=4096,
    )
    enriched_time = time.time() - start
    enriched_trace = _llm.get_last_trace()

    # 4b: PRD-only baseline task orders
    baseline_prompt = (
        f"## Design\n\n{PRD_SECTION}\n\n"
        f"## Task\n\n"
        "Produce task orders for each Worker. Each task order should specify:\n"
        "- Which Worker\n"
        "- What they must produce\n"
        "- Dependencies\n"
        "- Acceptance criteria\n\n"
        "Return as a structured list.\n"
    )

    start = time.time()
    baseline_response = _llm.invoke_llm(
        system=COORDINATOR_PROMPT,
        user=baseline_prompt,
        model=ARCHETYPE_MODELS.get("coordinator"),
        tools=[],
        max_tokens=4096,
    )
    baseline_time = time.time() - start
    baseline_trace = _llm.get_last_trace()

    results["phases"]["phase4"] = {
        "enriched": {
            "wall_time_s": round(enriched_time, 2),
            "tokens_input": enriched_trace.input_tokens if enriched_trace else 0,
            "tokens_output": enriched_trace.output_tokens if enriched_trace else 0,
            "response": enriched_response[:5000],
        },
        "baseline": {
            "wall_time_s": round(baseline_time, 2),
            "tokens_input": baseline_trace.input_tokens if baseline_trace else 0,
            "tokens_output": baseline_trace.output_tokens if baseline_trace else 0,
            "response": baseline_response[:5000],
        },
    }

    print(f"  Enriched: {round(enriched_time, 2)}s, "
          f"{enriched_trace.input_tokens if enriched_trace else '?'}in / "
          f"{enriched_trace.output_tokens if enriched_trace else '?'}out tokens", file=sys.stderr)
    print(f"  Baseline: {round(baseline_time, 2)}s, "
          f"{baseline_trace.input_tokens if baseline_trace else '?'}in / "
          f"{baseline_trace.output_tokens if baseline_trace else '?'}out tokens", file=sys.stderr)

    # -----------------------------------------------------------------------
    # Raw reports for human review
    # -----------------------------------------------------------------------
    results["raw_reports"] = [
        {"worker_serial": r.worker_serial, "raw_response": r.raw_response[:5000]}
        for r in state_reports
    ]
    results["raw_assessment"] = assessment.raw_response[:5000]

    # -----------------------------------------------------------------------
    # Save
    # -----------------------------------------------------------------------
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    results_file = RESULTS_DIR / f"real_alignment_{provider}_{timestamp}.json"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {results_file}", file=sys.stderr)

    # Summary
    total_tokens = sum(
        r.get("tokens_input", 0) + r.get("tokens_output", 0) for r in phase2_results
    )
    total_tokens += assessment.token_usage.get("synthesis_input", 0) + assessment.token_usage.get("synthesis_output", 0)
    if enriched_trace:
        total_tokens += enriched_trace.input_tokens + enriched_trace.output_tokens
    if baseline_trace:
        total_tokens += baseline_trace.input_tokens + baseline_trace.output_tokens

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"TOTAL: {total_tokens} tokens across {3 + 1 + 2} LLM calls", file=sys.stderr)
    print(f"  Phase 2: {len(state_reports)} Workers", file=sys.stderr)
    print(f"  Phase 3: {len(assessment.interfaces)} interfaces, "
          f"{len(assessment.conflicts)} conflicts, "
          f"{len(assessment.dependency_graph)} dependencies", file=sys.stderr)
    print(f"  Phase 4: enriched vs baseline task orders (human review needed)", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)


def _format_alignment_for_task_orders(assessment: AlignmentAssessment) -> str:
    """Format the assessment as enrichment context for task order production."""
    parts = ["## Alignment Assessment (from Worker state reports)\n"]

    if assessment.interfaces:
        parts.append("### Resolved Interfaces\n")
        for iface in assessment.interfaces:
            parts.append(
                f"- **{iface.producer}** -> **{iface.consumer}**: {iface.status.upper()}\n"
                f"  Producer: {str(iface.producer_shape)[:200]}\n"
                f"  Consumer: {str(iface.consumer_shape)[:200]}\n"
            )
            if iface.resolution:
                parts.append(f"  RESOLVED: {iface.resolution[:200]}\n")

    if assessment.gaps:
        parts.append("### Gaps\n" + "\n".join(f"- {g}" for g in assessment.gaps) + "\n")

    if assessment.conflicts:
        parts.append("### Conflicts\n")
        for c in assessment.conflicts:
            parts.append(f"- [{c.type}] {c.description[:200]}")
            if c.resolution:
                parts.append(f"  DECISION: {c.resolution[:200]}")

    if assessment.dependency_graph:
        parts.append("### Dependency Graph\n")
        for d in assessment.dependency_graph:
            parts.append(f"- {d.producer} -> {d.consumer}: {d.artifact} (before: {d.required_before})")

    parts.append(
        "\nIMPORTANT: Use the resolved interfaces above when writing task order "
        "interface contracts. Each task order should embed specific field names, "
        "types, and paths from this assessment.\n"
    )
    return "\n".join(parts)


def _count_confidence(report: StateReport) -> dict:
    counts = {"known": 0, "suspected": 0, "unknown": 0, "blocked": 0}
    for claim_list in [report.what_i_produce, report.what_exists, report.what_is_missing]:
        for claim in claim_list:
            counts[claim.confidence] = counts.get(claim.confidence, 0) + 1
    return counts


# ---------------------------------------------------------------------------
# Phase 5: Execution — concrete task orders, dependency-ordered Workers
# ---------------------------------------------------------------------------

TASK_ORDER_AE_CLOUDOPS = """
## Task Order: CLSUNI-WS1 — DynamoDB Table + IAM (AE_CloudOps)

Add the bd-securities DynamoDB table and supporting IAM to shared-infra Terraform.

### File to modify
infra/aws/terraform/shared-infra/main.tf

### What to add (append after the existing opal_partner_49financial resource)

1. DynamoDB table resource:
   resource "aws_dynamodb_table" "bd_securities" {
     name         = "bd-securities"
     billing_mode = "PAY_PER_REQUEST"
     hash_key     = "ticker"

     attribute { name = "ticker";        type = "S" }
     attribute { name = "asset_class";   type = "S" }
     attribute { name = "sub_asset_class"; type = "S" }

     global_secondary_index {
       name            = "asset-class-index"
       hash_key        = "asset_class"
       projection_type = "ALL"
     }
     global_secondary_index {
       name            = "sub-asset-class-index"
       hash_key        = "sub_asset_class"
       projection_type = "ALL"
     }
     point_in_time_recovery { enabled = true }
     tags = { pipeline = "bd", managed_by = "terraform" }
   }

2. IAM managed policy granting DynamoDB + Secrets Manager access:
   resource "aws_iam_policy" "bd_securities_access" {
     name = "bd-securities-access"
     policy = jsonencode({
       Version = "2012-10-17"
       Statement = [
         {
           Effect   = "Allow"
           Action   = ["dynamodb:Scan","dynamodb:GetItem","dynamodb:PutItem",
                       "dynamodb:UpdateItem","dynamodb:BatchWriteItem"]
           Resource = [aws_dynamodb_table.bd_securities.arn,
                       "arn:aws:dynamodb:us-east-1:313476888478:table/etf-classifications"]
         },
         {
           Effect   = "Allow"
           Action   = ["secretsmanager:GetSecretValue"]
           Resource = "arn:aws:secretsmanager:us-east-1:313476888478:secret:openai-api-key-*"
         }
       ]
     })
   }

3. Attach policy to EC2 role (bd-exporter-ec2-role) and Lambda role (partners-lambda-role):
   resource "aws_iam_role_policy_attachment" "ec2_bd_securities" {
     role       = "bd-exporter-ec2-role"
     policy_arn = aws_iam_policy.bd_securities_access.arn
   }
   resource "aws_iam_role_policy_attachment" "lambda_bd_securities" {
     role       = "partners-lambda-role"
     policy_arn = aws_iam_policy.bd_securities_access.arn
   }

### After writing the Terraform
Run: terraform plan to verify (read-only, safe). Use the .tools/terraform.exe binary.
Working dir for terraform: infra/aws/terraform/shared-infra/
Command: .tools/terraform.exe plan -no-color 2>&1 | head -50

### Acceptance criteria
- aws_dynamodb_table.bd_securities resource block present in main.tf
- aws_iam_policy.bd_securities_access resource block present
- Both aws_iam_role_policy_attachment resources present
- terraform plan shows the new resources as additions (no unexpected destroys)
"""

TASK_ORDER_DS = """
## Task Order: CLSUNI-WS2 — lib/etf_classifier.py (DS)

Write the shared ETFClassifier module. This is the canonical classification source
for both EC2 gold scripts and the opal-partners-data Lambda.

### Files to create
- data/black_diamond/scripts/gold/lib/__init__.py  (empty)
- data/black_diamond/scripts/gold/lib/etf_classifier.py

### What etf_classifier.py must contain

A class ETFClassifier with:

1. Class-level singleton:
   _instance = None
   @classmethod
   def instance(cls, table_name='bd-securities', region='us-east-1') -> 'ETFClassifier':
       if cls._instance is None:
           cls._instance = cls(table_name, region)
       return cls._instance

2. __init__: Full DynamoDB table scan into two in-memory dicts:
   self._ticker_map: dict[str, dict]   # ticker -> full item
   self._name_map: dict[str, str]      # normalized_alias -> ticker
   Load name_aliases StringSet from each item to build _name_map.
   If scan fails, log ERROR and set both dicts to {}.

3. classify(ticker, asset_name) -> str:
   Returns 'equity' | 'fixed_income' | 'alternatives' | ''
   '' means unknown -> caller treats as cash residual.
   Layer 1: ticker in _ticker_map -> return mapped asset_class
             (remap 'hedge' -> 'alternatives' here)
   Layer 2: normalize(asset_name) in _name_map -> get ticker -> Layer 1
   Layer 3: name pattern matching via compiled regex:
     _RE_ALTERNATIVES = re.compile(
       r'SHIELD|ANNUIT|BUFFER|MANAGED FLOOR|STRUCTURED NOTE|BARRIER NOTE'
       r'|PRINCIPAL PROTECTED|LINKED NOTE|FUTURES|COMMODITY FUND', re.IGNORECASE)
     _RE_CASH = re.compile(
       r'CASH|SWEEP|MONEY MARKET|MM FUND|GOVT CASH|MMKT|CASH RESV', re.IGNORECASE)
     _RE_FIXED_INCOME = re.compile(
       r'FIXED.INCOME|INFLATION.PROTECTED|TREASURY INFLATION|FNMA|BOND PORT|BOND FUND',
       re.IGNORECASE)
   Layer 4: ticker is 1-5 alpha chars (ETF heuristic) -> 'equity'
   Layer 5: return ''
   Special override: if ticker == 'CASH_USD' -> return '' always.

4. get_sub_asset_class(ticker, asset_name=None) -> str:
   Lookup sub_asset_class from _ticker_map. Return '' if not found.

5. resolve_ticker(asset_name) -> str | None:
   Look up normalized asset_name in _name_map. Return ticker or None.

6. normalize_name(asset_name) -> str (staticmethod):
   Uppercase, collapse whitespace to single space, strip punctuation
   except hyphens, truncate to 80 chars.

7. classify_series(ticker_series, name_series) -> pd.Series:
   Vectorized version. Applies self.classify() row-wise.
   Import pandas as pd inside the method (not at module level -- EC2 and Lambda
   may have it or may not; the import will fail fast if missing).

### After writing both files
Verify with: python3 -c "
from data.black_diamond.scripts.gold.lib.etf_classifier import ETFClassifier
c = ETFClassifier.__new__(ETFClassifier)
c._ticker_map = {'DIVZ': {'asset_class': 'equity'}}
c._name_map = {'OPAL DIVIDEND INCOME ETF': 'DIVZ'}
assert c.classify('DIVZ', None) == 'equity'
assert c.classify('CASH_USD', None) == ''
print('smoke test passed')
"

### Commit
git_commit with author_serial='DS.CP.1', message='[CLSUNI] DS.CP.1: lib/etf_classifier.py -- shared ETFClassifier module'
"""

TASK_ORDER_RD = """
## Task Order: CLSUNI-WS7 — Portal Taxonomy Update (RD)

Update TypeScript types to match the new 3-bucket taxonomy (equity, fixed_income,
alternatives). Cash becomes a computed residual -- NOT stored in the data.

### File to modify
portal/src/pages/AdvisorIntelligence/types.ts

### Changes required

1. MixTimeseriesPoint interface -- drop structured_notes, cash, other; add alternatives:
   BEFORE:
     export interface MixTimeseriesPoint {
       date: string
       equity: number
       fixed_income: number
       structured_notes: number
       cash: number
       other: number
     }
   AFTER:
     export interface MixTimeseriesPoint {
       date: string
       equity: number
       fixed_income: number
       alternatives: number
       // cash is computed residual: 1 - equity - fixed_income - alternatives
     }

2. FirmMixPeriodPoint interface -- same pattern. Find this interface and remove
   structured_notes, cash, other fields; add alternatives.
   Keep total_aua and all non-mix fields unchanged.

### Also update in ClientsTab.tsx
File: portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx

1. deriveQuarterlyFromTimeseries() -- replace the structured_notes/cash/other
   lines with a single alternatives line:
   REMOVE these lines:
     structured_notes: { value: total * mix.structured_notes, pct: mix.structured_notes },
     cash:             { value: total * mix.cash,             pct: mix.cash },
     other:            { value: total * mix.other,            pct: mix.other },
   ADD this line:
     alternatives:     { value: total * mix.alternatives,     pct: mix.alternatives },

2. MIX_PIE_COLORS -- add alternatives key:
   Find the MIX_PIE_COLORS object and add:
     alternatives:     '#f97316',
   (Keep all existing keys. structured_notes key can stay as fallback.)

### Acceptance criteria
- MixTimeseriesPoint has exactly: date, equity, fixed_income, alternatives
- FirmMixPeriodPoint no longer references structured_notes, cash, or other
- deriveQuarterlyFromTimeseries() references alternatives not the old fields
- MIX_PIE_COLORS has alternatives key

### Commit
git_commit with author_serial='RD.AI.1', message='[CLSUNI] RD.AI.1: portal taxonomy update -- MixTimeseriesPoint alternatives'
"""

TASK_ORDER_DT = """
## Task Order: CLSUNI-WS8-DT — Deploy ETFClassifier to Lambda (DT)

Copy the ETFClassifier module to the opal-partners-data Lambda directory.
The Lambda will use this instead of the existing static etf_classification.py.

### Step 1: Copy the module
Run: cp data/black_diamond/scripts/gold/lib/etf_classifier.py infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/etf_classifier.py

### Step 2: Verify the copy succeeded
Read infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/etf_classifier.py
and confirm it contains the ETFClassifier class.

### Step 3: Check existing import in opal-partners-data
Read infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py
and search for the import of etf_classification. Note the current import line.

### Step 4: Update the import in lambda_function.py
Find the line that imports from etf_classification (something like:
  from etf_classification import ETF_CLASSIFICATIONS, ASSET_NAME_TO_TICKER
  or similar)
Replace it with:
  from etf_classifier import ETFClassifier as _ETFClassifier
  _clf = _ETFClassifier.instance()

Then find any direct calls to ETF_CLASSIFICATIONS.get(ticker) or
classify_holding(ticker, asset_name) in the Lambda handler and replace with:
  _clf.classify(ticker, asset_name)

### Step 5: Commit both files
git_commit with author_serial='DT.CP.1',
message='[CLSUNI] DT.CP.1: wire ETFClassifier into opal-partners-data Lambda'
files=['infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/etf_classifier.py',
       'infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py']

### Acceptance criteria
- etf_classifier.py exists in the Lambda source directory
- lambda_function.py imports ETFClassifier and calls classify() not static dict
"""

TASK_ORDER_AE_ETL = """
## Task Order: CLSUNI-WS3 — Seed bd-securities from etf-classifications (AE_PartnerETL)

Write a seed script that copies the 116 items from the Yang etf-classifications table
into the new bd-securities table, remapping 'hedge' -> 'alternatives'.

### File to create
data/black_diamond/scripts/classification/seed_bd_securities.py

### What the script must do

1. Scan etf-classifications table (boto3 dynamodb resource)
2. For each item:
   - Copy all fields
   - If asset_class == 'hedge': set asset_class = 'alternatives'
   - Add: classified_by = 'seed_from_yang', confidence = Decimal('1.0'),
          needs_review = False, last_updated = datetime.utcnow().isoformat()
   - For Opal ETFs, add name_aliases StringSet:
     OPAL_ALIASES = {
       'DIVZ': {'OPAL DIVIDEND INCOME ETF', 'TRUESHARES LOW VOLATILITY EQUITY INCOME ETF'},
       'IDVZ': {'OPAL INTERNATIONAL DIVIDEND INCOME ETF', 'TRUESHARES INTERNATIONAL EQUITY INCOME ETF'},
       'PFDE': {'PATHFINDER DISCIPLINED US EQUITY ETF', 'PATHFINDER DISCIPLINED US EQUITIES ETF'},
       'PFOE': {'PATHFINDER FOCUSED OPPORTUNITIES ETF'},
       'PCHI': {'POLEN HIGH INCOME ETF', 'POLEN HIGH YIELD ETF'},
     }
3. Write each item to bd-securities using put_item (idempotent)
4. Print: "Seeded N items. N hedge->alternatives remapped. N aliases added."

### After writing the script
Run a dry-run check (do NOT run the script itself -- AE will execute it after DT deploys):
python3 -c "
import ast, sys
with open('data/black_diamond/scripts/classification/seed_bd_securities.py') as f:
    src = f.read()
ast.parse(src)
print('syntax OK')
"

### Commit
git_commit with author_serial='AE.PE.1',
message='[CLSUNI] AE.PE.1: seed_bd_securities.py -- copy Yang table, remap hedge->alternatives'
"""


def _print_result(label: str, result: ExecutionResult) -> None:
    """Print a Worker execution result summary."""
    status = "OK" if result.success else "FAIL"
    print(f"\n  [{status}] {label} ({result.worker_serial})", file=sys.stderr)
    if result.pre_flight_failures:
        for f in result.pre_flight_failures:
            print(f"    PRE-FLIGHT FAIL: {f}", file=sys.stderr)
    if result.error and not result.pre_flight_failures:
        print(f"    ERROR: {result.error[:200]}", file=sys.stderr)
    if result.files_written:
        for fp in result.files_written:
            if fp:
                print(f"    WROTE: {fp}", file=sys.stderr)
    if result.commit_sha:
        print(f"    COMMIT: {result.commit_sha}", file=sys.stderr)
    tok = result.token_usage
    if tok:
        print(f"    Tokens: {tok.get('input',0)}in / {tok.get('output',0)}out "
              f"| {result.iterations} iter, {result.tool_calls} tool calls", file=sys.stderr)


def run_phase5_execution(branch: str = "CLOUD_test") -> dict:
    """Phase 5: dependency-ordered Worker execution against real ajb_workspace.

    Level 0 (parallel): AE_CloudOps (Terraform), DS (classifier), RD (types)
    Level 1: DT (Lambda wiring -- depends on DS)
    Level 2: AE_PartnerETL (seed script -- depends on table + DS commits)

    AE_CloudOps and DS and RD all run first because:
    - AE_CloudOps has no code dependencies
    - DS/RD are code-only, test-branch-safe
    DT runs after DS (needs etf_classifier.py to copy into Lambda).
    AE_PartnerETL's gold run has a pre-flight check on table item count.
    """
    working_dir = str(AJB_WORKSPACE)
    results = {
        "phase": "phase5_execution",
        "branch": branch,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "workers": {},
    }

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Phase 5: Execution (branch={branch})", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    # ------------------------------------------------------------------
    # Level 0a: AE_CloudOps -- Terraform bd-securities + IAM
    # ------------------------------------------------------------------
    print("\n--- Level 0a: AE_CloudOps (Terraform) ---", file=sys.stderr)
    result_ae_co = invoke_worker_for_execution(
        system_prompt=WORKER_AE_CLOUDOPS_PROMPT,
        task_order_text=TASK_ORDER_AE_CLOUDOPS,
        worker_id="AE-CLOUDOPS",
        worker_serial="AE.CO.1",
        task_order_id="CLSUNI-WS1",
        working_directory=working_dir,
        allowed_paths=["infra/aws/terraform/shared-infra/main.tf"],
        max_iterations=20,
        branch=branch,
    )
    _print_result("AE_CloudOps", result_ae_co)
    results["workers"]["AE_CloudOps"] = {
        "success": result_ae_co.success,
        "files_written": result_ae_co.files_written,
        "commit_sha": result_ae_co.commit_sha,
        "token_usage": result_ae_co.token_usage,
        "error": result_ae_co.error,
        "pre_flight_failures": result_ae_co.pre_flight_failures,
    }

    # ------------------------------------------------------------------
    # Level 0b: DS -- lib/etf_classifier.py (parallel with AE_CloudOps)
    # ------------------------------------------------------------------
    print("\n--- Level 0b: DS (ETFClassifier module) ---", file=sys.stderr)
    result_ds = invoke_worker_for_execution(
        system_prompt=WORKER_DS_PROMPT,
        task_order_text=TASK_ORDER_DS,
        worker_id="DS-WORKER",
        worker_serial="DS.CP.1",
        task_order_id="CLSUNI-WS2",
        working_directory=working_dir,
        allowed_paths=[
            "data/black_diamond/scripts/gold/lib/etf_classifier.py",
            "data/black_diamond/scripts/gold/lib/__init__.py",
        ],
        max_iterations=25,
        branch=branch,
    )
    _print_result("DS", result_ds)
    results["workers"]["DS"] = {
        "success": result_ds.success,
        "files_written": result_ds.files_written,
        "commit_sha": result_ds.commit_sha,
        "token_usage": result_ds.token_usage,
        "error": result_ds.error,
    }

    # ------------------------------------------------------------------
    # Level 0c: RD -- portal taxonomy update (parallel with DS)
    # ------------------------------------------------------------------
    print("\n--- Level 0c: RD (portal types) ---", file=sys.stderr)
    result_rd = invoke_worker_for_execution(
        system_prompt=WORKER_RD_PROMPT,
        task_order_text=TASK_ORDER_RD,
        worker_id="RD-WORKER",
        worker_serial="RD.AI.1",
        task_order_id="CLSUNI-WS7",
        working_directory=working_dir,
        allowed_paths=[
            "portal/src/pages/AdvisorIntelligence/types.ts",
            "portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx",
        ],
        max_iterations=20,
        branch=branch,
    )
    _print_result("RD", result_rd)
    results["workers"]["RD"] = {
        "success": result_rd.success,
        "files_written": result_rd.files_written,
        "commit_sha": result_rd.commit_sha,
        "token_usage": result_rd.token_usage,
        "error": result_rd.error,
    }

    # ------------------------------------------------------------------
    # Level 1: DT -- wire ETFClassifier into Lambda (depends on DS)
    # ------------------------------------------------------------------
    print("\n--- Level 1: DT (Lambda wiring) ---", file=sys.stderr)
    if not result_ds.success:
        print("  SKIP: DS did not succeed. DT requires etf_classifier.py.", file=sys.stderr)
        results["workers"]["DT"] = {"success": False, "skipped": True,
                                     "reason": "DS did not succeed"}
    else:
        result_dt = invoke_worker_for_execution(
            system_prompt=WORKER_DT_PROMPT,
            task_order_text=TASK_ORDER_DT,
            worker_id="DT-WORKER",
            worker_serial="DT.CP.1",
            task_order_id="CLSUNI-WS8-DT",
            working_directory=working_dir,
            allowed_paths=[
                "infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/etf_classifier.py",
                "infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py",
            ],
            max_iterations=20,
            branch=branch,
        )
        _print_result("DT", result_dt)
        results["workers"]["DT"] = {
            "success": result_dt.success,
            "files_written": result_dt.files_written,
            "commit_sha": result_dt.commit_sha,
            "token_usage": result_dt.token_usage,
            "error": result_dt.error,
        }

    # ------------------------------------------------------------------
    # Level 2: AE_PartnerETL -- seed script (pre-flight: table must exist)
    # ------------------------------------------------------------------
    print("\n--- Level 2: AE_PartnerETL (seed script) ---", file=sys.stderr)
    result_ae_etl = invoke_worker_for_execution(
        system_prompt=WORKER_AE_PARTNERETL_PROMPT,
        task_order_text=TASK_ORDER_AE_ETL,
        worker_id="AE-PARTNERETL",
        worker_serial="AE.PE.1",
        task_order_id="CLSUNI-WS3",
        working_directory=working_dir,
        allowed_paths=["data/black_diamond/scripts/classification/seed_bd_securities.py"],
        max_iterations=20,
        branch=branch,
        pre_flight_checks=[
            PreFlightCheck(
                name="bd-securities-table-exists",
                command=(
                    "aws dynamodb describe-table --table-name bd-securities "
                    "--query Table.TableStatus --output text 2>&1 | "
                    "grep -q ACTIVE && echo OK || exit 1"
                ),
                failure_message=(
                    "bd-securities table does not exist or is not ACTIVE. "
                    "AE_CloudOps Terraform must apply before seed can run."
                ),
            ),
        ],
    )
    _print_result("AE_PartnerETL", result_ae_etl)
    results["workers"]["AE_PartnerETL"] = {
        "success": result_ae_etl.success,
        "files_written": result_ae_etl.files_written,
        "commit_sha": result_ae_etl.commit_sha,
        "token_usage": result_ae_etl.token_usage,
        "error": result_ae_etl.error,
        "pre_flight_failures": result_ae_etl.pre_flight_failures,
    }

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total_tokens = sum(
        (r.get("token_usage", {}) or {}).get("total", 0)
        for r in results["workers"].values()
        if isinstance(r, dict) and not r.get("skipped")
    )
    passed = sum(1 for r in results["workers"].values()
                 if isinstance(r, dict) and r.get("success"))
    total = len(results["workers"])

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Phase 5 complete: {passed}/{total} Workers succeeded", file=sys.stderr)
    print(f"Total tokens: {total_tokens}", file=sys.stderr)
    print(f"Branch: {branch}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase5", action="store_true",
                        help="Run Phase 5 execution (skips alignment phases 1-4)")
    parser.add_argument("--branch", default="CLOUD_test",
                        help="Git branch for Phase 5 commits (default: CLOUD_test)")
    args = parser.parse_args()

    if args.phase5:
        results = run_phase5_execution(branch=args.branch)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        results_file = RESULTS_DIR / f"phase5_execution_{args.branch}_{timestamp}.json"
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to: {results_file}", file=sys.stderr)
    else:
        run_real_alignment()
