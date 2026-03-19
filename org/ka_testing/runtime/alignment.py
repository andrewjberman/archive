"""
Pre-Task Alignment Protocol -- Runtime Implementation.

Implements ONT.CORE.ALIGNMENT v2: a vertical gather-then-synthesize protocol
where Workers report state to the Coordinator, and the Coordinator synthesizes
alignment from structured reports. Workers never see each other's context.

Phases:
  1: State Request (mechanical loop -- no LLM call)
  2: State Report (Workers read their own files, report naturally)
  3: Coordinator Synthesis (cross-reference all reports, produce assessment)
  4: Task Orders (enriched with resolved interface contracts)
  5: Schism Resolution (independent re-compilation under constraint, 3 LLM calls)

Integration: called from coordinator.py as alignment_pass() before task
order production. Internal to the Coordinator node -- no new graph nodes.

ONT.CORE.CONTEXT_COMPILATION v5 contract (three principles):
  1. Compilation is a chain (Workers compile upward, Coordinator synthesizes)
  2. Truth-state at every boundary (known/suspected/unknown/blocked)
  3. Quality = downstream action (consumer can act without gaps)

Ontology source: ONT.CORE.ALIGNMENT v2, ONT.CORE.CONTEXT_COMPILATION v5
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any


def _get_llm_module():
    """Return the LLM provider module based on HIERARCHY_LLM_PROVIDER env var.

    Returns either system.os.runtime.llm (Anthropic) or
    system.os.runtime.llm_openai (OpenAI). Both have identical public APIs:
    invoke_llm(), get_last_trace().
    """
    provider = os.environ.get("HIERARCHY_LLM_PROVIDER", "anthropic")
    if provider == "openai":
        from . import llm_openai
        return llm_openai
    else:
        from . import llm
        return llm


# ---------------------------------------------------------------------------
# Data Contracts
# ---------------------------------------------------------------------------

@dataclass
class StateRequest:
    """Coordinator -> Worker: scoped question about current state.

    Produced mechanically from the Worker roster -- no LLM call needed.
    Each Worker gets the full PRD section and the same question.
    """
    worker_id: str               # target worker identity (from AGENTS.json)
    worker_serial: str           # human-readable serial (e.g., ING.PORT.1)
    prd_section: str             # verbatim PRD section
    scoped_question: str         # what the Coordinator needs to know


@dataclass
class Claim:
    """A single claim with an epistemic truth-state label.

    ONT.CORE.CONTEXT_COMPILATION v5, Principle 2: every claim that crosses
    a handoff carries an explicit epistemic label. Suspected-as-known is
    the one hard invariant.
    """
    statement: str
    confidence: str = "known"  # "known" | "suspected" | "unknown" | "blocked"
    source: str = ""           # optional provenance: "file.py:42" or ""


@dataclass
class StateReport:
    """Worker -> Coordinator: report of current state.

    Workers report naturally -- structured JSON or prose. Claims carry
    truth-state labels when structured; unstructured responses are
    preserved as raw_response for the Coordinator to interpret.

    ONT.CORE.ALIGNMENT Phase 2.
    """
    worker_id: str
    worker_serial: str
    what_i_produce: list[Claim] = field(default_factory=list)
    what_exists: list[Claim] = field(default_factory=list)
    what_is_missing: list[Claim] = field(default_factory=list)
    requires_from_others: list[str] = field(default_factory=list)  # explicit dependency declarations
    constraints: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    raw_response: str = ""


@dataclass
class InterfaceMatch:
    """Field-level match analysis between a producer and consumer Worker.

    producer_confidence / consumer_confidence: the Coordinator extracts
    these from Worker prose. Workers may use [KNOWN], [SUSPECTED], etc.
    inline in free-form text. The Coordinator is responsible for reading
    those labels and reporting them here. enforce_truth_state() validates.
    """
    producer: str
    consumer: str
    producer_shape: str
    consumer_shape: str
    status: str                # "match" | "naming_conflict" | "shape_conflict" | "missing"
    resolution: str | None = None
    producer_confidence: str = "known"   # CRD-extracted: known|suspected|unknown|blocked
    consumer_confidence: str = "known"   # CRD-extracted: known|suspected|unknown|blocked


@dataclass
class Conflict:
    """Classified conflict between Workers."""
    type: str                  # "naming" | "shape" | "missing" | "schism"
    workers: list[str] = field(default_factory=list)
    description: str = ""
    resolution: str | None = None


@dataclass
class Dependency:
    """Producer-consumer dependency between Workers."""
    producer: str
    consumer: str
    artifact: str
    required_before: str = "implementation"


@dataclass
class AlignmentAssessment:
    """Coordinator's synthesis of all StateReports.

    The high-value output of Phase 3.
    """
    interfaces: list[InterfaceMatch] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    conflicts: list[Conflict] = field(default_factory=list)
    dependency_graph: list[Dependency] = field(default_factory=list)
    schisms: list[str] = field(default_factory=list)
    raw_response: str = ""
    token_usage: dict[str, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Gate: should alignment run?
# ---------------------------------------------------------------------------

def should_align(
    spec: dict[str, Any],
    task_roster: list[dict[str, Any]],
) -> bool:
    """If there are 2+ Workers, run alignment.

    The cost of a false negative (skipping alignment that was needed,
    leading to interface mismatch during execution) far exceeds the cost
    of a false positive (running alignment that finds no conflicts).
    ~25K tokens is cheap insurance.
    """
    return len(task_roster) >= 2


# ---------------------------------------------------------------------------
# Phase 1: Mechanical StateRequest generation (no LLM call)
# ---------------------------------------------------------------------------

def _produce_state_requests(
    prd_section: str,
    worker_roster: list[dict[str, Any]],
) -> list[StateRequest]:
    """Produce one StateRequest per Worker. Mechanical loop, no LLM."""
    return [
        StateRequest(
            worker_id=w["identity"],
            worker_serial=w.get("serial", ""),
            prd_section=prd_section,
            scoped_question=(
                "What do you currently produce, what exists, and "
                "what is missing relative to this design?"
            ),
        )
        for w in worker_roster
    ]


# ---------------------------------------------------------------------------
# Phase 2: Worker state invocation (single-turn, read-only, no KF gating)
# ---------------------------------------------------------------------------

def get_read_only_tools(working_directory: str) -> list[dict[str, Any]]:
    """Return the read-only subset of worker tools for state collection."""
    from .tools import get_worker_tools

    all_tools = get_worker_tools(working_directory)
    read_only_names = {"read_file", "list_dir", "grep_files"}
    return [t for t in all_tools if t.get("name") in read_only_names]


def _build_state_request_prompt(
    state_request: StateRequest,
    worker_prompt: str,
) -> tuple[str, str]:
    """Build system + user prompts for a Phase 2 Worker state invocation.

    Context compiler seam: when a structured compiler materializes,
    this function is the swap point.

    Returns:
        (system_prompt, user_prompt)
    """
    system = worker_prompt

    user = (
        "## State Report Request\n\n"
        "Report your current state relative to the design below.\n"
        "This is NOT a task order. You are reporting what exists, not building.\n\n"
        "Read whatever files you need to answer accurately.\n\n"
        f"## Design\n\n{state_request.prd_section}\n\n"
        f"## Question\n\n{state_request.scoped_question}\n\n"
        "## How to respond\n\n"
        "Structure your response however is clearest. Include:\n"
        "- What you currently produce (field names, paths, shapes)\n"
        "- What exists that's relevant to this design\n"
        "- What's missing or would need to change\n"
        "- What you require from other Workers to produce your output\n"
        "  (if none, state 'none' -- unstated dependencies are invisible)\n"
        "- Any constraints or blockers\n\n"
        "For each factual claim, note your confidence:\n"
        "- [KNOWN] if you verified it by reading the actual file\n"
        "- [SUSPECTED] if you inferred it but did not verify\n"
        "- [UNKNOWN] if you cannot determine\n"
        "- [BLOCKED] if it depends on something outside your scope\n\n"
        "Do NOT label something [KNOWN] unless you read the file that proves it.\n"
        "Ground claims in files you actually read.\n"
    )

    return system, user


def invoke_worker_for_state(
    worker_identity: str,
    state_request: StateRequest,
    working_directory: str,
) -> StateReport:
    """Invoke a Worker in single-turn mode to collect a state report.

    Separate invocation path from worker_node(). No KF stage gating,
    no deliverables. Read-only tools, max 5 iterations for file reads.

    Args:
        worker_identity: Provenance-encoded identity from AGENTS.json.
        state_request: The scoped question from the Coordinator.
        working_directory: Filesystem root for the Worker.

    Returns:
        Parsed StateReport (falls back to raw_response if parsing fails).
    """
    _llm = _get_llm_module()
    from .config import resolve_agent, load_agent_prompt, ARCHETYPE_MODELS

    agent = resolve_agent(worker_identity)
    worker_prompt = load_agent_prompt(agent)
    model = ARCHETYPE_MODELS.get(agent.get("archetype", "supplier"), ARCHETYPE_MODELS["supplier"])

    system_prompt, user_prompt = _build_state_request_prompt(state_request, worker_prompt)
    tools = get_read_only_tools(working_directory)

    response = _llm.invoke_llm(
        system=system_prompt,
        user=user_prompt,
        model=model,
        tools=tools,
        max_tokens=4096,
        max_iterations=5,
    )

    report = _parse_state_report(response, state_request)

    # Enrich evidence_refs from tool call trace
    trace = _llm.get_last_trace()
    if trace:
        report.evidence_refs = list(set(
            report.evidence_refs
            + [tc.inputs.get("file_path", "") for tc in trace.tool_calls if tc.name == "read_file"]
        ))

    return report


def invoke_worker_for_state_direct(
    system_prompt: str,
    state_request: StateRequest,
    working_directory: str,
    max_iterations: int = 5,
    max_read_chars: int = 0,
) -> StateReport:
    """Test-mode variant: takes system prompt directly, no registry lookup.

    Same logic as invoke_worker_for_state() but bypasses resolve_agent().
    Used by the test harness for Phase 5 where we need generic Worker
    prompts without polluting AGENTS.json.

    Args:
        system_prompt: Worker persona prompt (passed directly).
        state_request: The scoped question.
        working_directory: Filesystem root for read-only tools.
        max_iterations: Tool loop iteration cap (default 5, test uses 3).
        max_read_chars: Cap on file read output (0=unlimited, test uses 8000).
    """
    _llm = _get_llm_module()
    from .config import ARCHETYPE_MODELS
    from .tools import get_worker_tools

    # Build read-only tools with optional char cap
    all_tools = get_worker_tools(working_directory, max_read_chars=max_read_chars)
    read_only_names = {"read_file", "list_dir", "grep_files"}
    tools = [t for t in all_tools if t.get("name") in read_only_names]

    _, user_prompt = _build_state_request_prompt(state_request, system_prompt)

    response = _llm.invoke_llm(
        system=system_prompt,
        user=user_prompt,
        model=ARCHETYPE_MODELS.get("supplier", ARCHETYPE_MODELS.get("coordinator")),
        tools=tools,
        max_tokens=4096,
        max_iterations=max_iterations,
    )

    report = _parse_state_report(response, state_request)

    trace = _llm.get_last_trace()
    if trace:
        report.evidence_refs = list(set(
            report.evidence_refs
            + [tc.inputs.get("file_path", "") for tc in trace.tool_calls if tc.name == "read_file"]
        ))

    return report


def _parse_claims(raw: list) -> list[Claim]:
    """Parse claims from Worker response.

    Handles structured ({"statement": ..., "confidence": ...}) and
    plain strings. Unlabeled claims default to "suspected" -- the
    safe direction per ONT.CORE.CONTEXT_COMPILATION v5 Principle 2.
    """
    claims = []
    for item in raw:
        if isinstance(item, dict):
            claims.append(Claim(
                statement=item.get("statement", str(item)),
                confidence=item.get("confidence", "suspected"),
            ))
        elif isinstance(item, str):
            claims.append(Claim(statement=item, confidence="suspected"))
    return claims


def _parse_state_report(response: str, request: StateRequest) -> StateReport:
    """Parse a StateReport from a Worker's response.

    Tries JSON first, falls back to raw_response. The Coordinator's
    Phase 3 synthesis handles both structured and unstructured input.
    """
    report = StateReport(
        worker_id=request.worker_id,
        worker_serial=request.worker_serial,
        raw_response=response,
    )

    # Try JSON from fenced block
    match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
    if not match:
        match = re.search(r"\{[^{}]*\}", response, re.DOTALL)

    if match:
        try:
            data = json.loads(match.group(1) if "```" in match.group(0) else match.group(0))
            if isinstance(data, dict):
                report.what_i_produce = _parse_claims(data.get("what_i_produce", []))
                report.what_exists = _parse_claims(data.get("what_exists", []))
                report.what_is_missing = _parse_claims(data.get("what_is_missing", []))
                report.requires_from_others = data.get("requires_from_others", [])
                report.constraints = data.get("constraints", [])
                report.blockers = data.get("blockers", [])
                report.evidence_refs = data.get("evidence_refs", [])
        except (json.JSONDecodeError, IndexError):
            pass

    return report


# ---------------------------------------------------------------------------
# Phase 3: Coordinator Synthesis
# ---------------------------------------------------------------------------

def _format_report_for_synthesis(report: StateReport) -> str:
    """Format a single StateReport for the synthesis prompt.

    Preserves truth-state labels so the Coordinator sees them.
    """
    header = f"### Worker: {report.worker_serial} ({report.worker_id})\n\n"

    if report.what_i_produce or report.what_exists or report.what_is_missing:
        def _fmt(claims: list[Claim]) -> str:
            if not claims:
                return "(none)\n"
            return "\n".join(
                f"  [{c.confidence.upper()}] {c.statement}" for c in claims
            ) + "\n"

        requires = ""
        if report.requires_from_others:
            requires = f"**Requires from others:** {json.dumps(report.requires_from_others)}\n"

        return (
            header
            + f"**Produces:**\n{_fmt(report.what_i_produce)}\n"
            + f"**Exists:**\n{_fmt(report.what_exists)}\n"
            + f"**Missing:**\n{_fmt(report.what_is_missing)}\n"
            + requires
            + f"**Constraints:** {json.dumps(report.constraints)}\n"
            + f"**Blockers:** {json.dumps(report.blockers)}\n"
            + f"**Evidence:** {json.dumps(report.evidence_refs)}\n\n"
        )
    else:
        return header + f"{report.raw_response[:3000]}\n\n"


def _build_synthesis_prompt(
    state_reports: list[StateReport],
    prd_section: str,
) -> str:
    """Build the Coordinator's synthesis prompt for Phase 3.

    Context compiler seam: swap point for structured compilation.
    """
    reports_text = "".join(
        _format_report_for_synthesis(r) for r in state_reports
    )

    return (
        "## Alignment Synthesis\n\n"
        f"## Design\n\n{prd_section}\n\n"
        f"## Worker State Reports\n\n{reports_text}\n"
        "## Task\n\n"
        "Cross-reference these state reports against the design. For each interface\n"
        "between Workers, check whether the producer's output matches the consumer's\n"
        "input -- field by field. Identify conflicts, gaps, and dependencies.\n\n"
        "CRITICAL DISTINCTION -- Current vs Target state:\n"
        "Each interface must be assessed on CURRENT state (what exists on disk right\n"
        "now, as reported by Workers from file reads), not target state (what the\n"
        "design says should exist after execution). Report both:\n"
        "- producer_shape / consumer_shape: what CURRENTLY exists\n"
        "- Use status 'match' ONLY if the interface works right now\n"
        "- If both sides acknowledge a pending change, status is 'missing' (the\n"
        "  target interface does not exist yet), not 'match'\n\n"
        "TRUTH-STATE EXTRACTION -- Workers mark claims in prose with labels like\n"
        "[KNOWN], [SUSPECTED], [UNKNOWN], [BLOCKED]. Extract these labels for each\n"
        "side of every interface and report them as producer_confidence and\n"
        "consumer_confidence. If a Worker didn't label a claim, default to\n"
        "'suspected'. Do not upgrade a Worker's label.\n\n"
        "## Required Output\n\n"
        "Produce an AlignmentAssessment as JSON in ```json``` fences:\n\n"
        "```json\n"
        "{\n"
        '  "interfaces": [\n'
        '    {\n'
        '      "producer": "worker_id",\n'
        '      "consumer": "worker_id",\n'
        '      "producer_shape": "what producer CURRENTLY outputs",\n'
        '      "consumer_shape": "what consumer CURRENTLY expects",\n'
        '      "status": "match|naming_conflict|shape_conflict|missing",\n'
        '      "resolution": "your decision or null",\n'
        '      "producer_confidence": "known|suspected|unknown|blocked",\n'
        '      "consumer_confidence": "known|suspected|unknown|blocked"\n'
        '    }\n'
        '  ],\n'
        '  "gaps": ["what the design needs that nobody currently produces"],\n'
        '  "conflicts": [\n'
        '    {\n'
        '      "type": "naming|shape|missing|schism|unknown_dependency",\n'
        '      "workers": ["worker_ids"],\n'
        '      "description": "what the conflict is",\n'
        '      "resolution": "your decision or null if schism"\n'
        '    }\n'
        '  ],\n'
        '  "dependency_graph": [\n'
        '    {\n'
        '      "producer": "worker_id",\n'
        '      "consumer": "worker_id",\n'
        '      "artifact": "what is produced",\n'
        '      "required_before": "implementation|integration|verification"\n'
        '    }\n'
        '  ],\n'
        '  "schisms": ["conflicts requiring Phase 5 resolution"]\n'
        "}\n"
        "```\n"
    )


def synthesize_alignment(
    state_reports: list[StateReport],
    prd_section: str,
    coordinator_identity: str,
    coordinator_prompt: str,
) -> AlignmentAssessment:
    """Phase 3: Coordinator synthesizes all state reports."""
    _llm = _get_llm_module()
    from .config import ARCHETYPE_MODELS

    user_prompt = _build_synthesis_prompt(state_reports, prd_section)

    response = _llm.invoke_llm(
        system=coordinator_prompt,
        user=user_prompt,
        model=ARCHETYPE_MODELS["coordinator"],
        tools=[],
        max_tokens=4096,
    )

    assessment = _parse_alignment_assessment(response)
    assessment = enforce_truth_state(assessment, state_reports)

    trace = _llm.get_last_trace()
    if trace:
        assessment.token_usage = {
            "synthesis_input": trace.input_tokens,
            "synthesis_output": trace.output_tokens,
        }

    return assessment


def _parse_alignment_assessment(response: str) -> AlignmentAssessment:
    """Parse an AlignmentAssessment from the Coordinator's response."""
    assessment = AlignmentAssessment(raw_response=response)

    match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
    if not match:
        return assessment

    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return assessment

    if not isinstance(data, dict):
        return assessment

    for iface in data.get("interfaces", []):
        if isinstance(iface, dict):
            assessment.interfaces.append(InterfaceMatch(
                producer=iface.get("producer", ""),
                consumer=iface.get("consumer", ""),
                producer_shape=iface.get("producer_shape", ""),
                consumer_shape=iface.get("consumer_shape", ""),
                status=iface.get("status", "missing"),
                resolution=iface.get("resolution"),
                producer_confidence=iface.get("producer_confidence", "suspected"),
                consumer_confidence=iface.get("consumer_confidence", "suspected"),
            ))

    assessment.gaps = data.get("gaps", [])

    for conflict in data.get("conflicts", []):
        if isinstance(conflict, dict):
            assessment.conflicts.append(Conflict(
                type=conflict.get("type", "missing"),
                workers=conflict.get("workers", []),
                description=conflict.get("description", ""),
                resolution=conflict.get("resolution"),
            ))

    for dep in data.get("dependency_graph", []):
        if isinstance(dep, dict):
            assessment.dependency_graph.append(Dependency(
                producer=dep.get("producer", ""),
                consumer=dep.get("consumer", ""),
                artifact=dep.get("artifact", ""),
                required_before=dep.get("required_before", "implementation"),
            ))

    assessment.schisms = data.get("schisms", [])

    return assessment


# ---------------------------------------------------------------------------
# Truth-state deterministic enforcement (ONT.CORE.CONTEXT_COMPILATION v5.1)
# ---------------------------------------------------------------------------

def enforce_truth_state(
    assessment: AlignmentAssessment,
    state_reports: list[StateReport],
) -> AlignmentAssessment:
    """Deterministic post-check: enforce truth-state labels.

    Scans source StateReports for [UNKNOWN], [BLOCKED], and [SUSPECTED]
    claims. Cross-references against assessment interfaces and dependency
    graph. Downgrades interface status from "match" to "unknown_dependency"
    where the model missed the uncertainty.

    This exists because LLMs treat truth-state labels as informational
    metadata, not as constraints on evaluation. When the model sees
    [UNKNOWN] next to a claim and [KNOWN] next to a matching claim from
    another Worker, it resolves in favor of the concrete content over the
    abstract label. Empirically confirmed by Tests 4 and 6.

    ONT.CORE.CONTEXT_COMPILATION v5.1, Principle 2 enforcement clause:
    "Truth-state enforcement at synthesis boundaries MUST be implemented
    as a deterministic post-processing step, not as a prompt instruction."
    """
    # Collect all uncertain claims keyed by BOTH worker_id and worker_serial.
    # The LLM may reference workers by either identifier in the assessment.
    uncertain: dict[str, set[str]] = {}
    for report in state_reports:
        worker_uncertain: set[str] = set()
        for claim_list in [report.what_i_produce, report.what_exists,
                           report.what_is_missing]:
            for claim in claim_list:
                if claim.confidence in ("unknown", "blocked", "suspected"):
                    worker_uncertain.add(claim.statement.lower())
        if worker_uncertain:
            uncertain[report.worker_id] = worker_uncertain
            if report.worker_serial:
                uncertain[report.worker_serial] = worker_uncertain

    # Check each interface marked "match"
    for iface in assessment.interfaces:
        if iface.status != "match":
            continue

        # Does the producer have uncertain claims that overlap with the interface?
        producer_uncertain = uncertain.get(iface.producer, set())
        if producer_uncertain:
            shape_text = iface.producer_shape if isinstance(iface.producer_shape, str) else str(iface.producer_shape)
            for claim_text in producer_uncertain:
                if _claims_overlap(claim_text, shape_text):
                    iface.status = "unknown_dependency"
                    iface.resolution = (
                        f"DOWNGRADED: producer claim is uncertain. "
                        f"Original LLM assessment was 'match'. "
                        f"Uncertain claim: '{claim_text[:100]}'"
                    )
                    break

        # Same check for consumer
        consumer_uncertain = uncertain.get(iface.consumer, set())
        if consumer_uncertain and iface.status == "match":
            shape_text = iface.consumer_shape if isinstance(iface.consumer_shape, str) else str(iface.consumer_shape)
            for claim_text in consumer_uncertain:
                if _claims_overlap(claim_text, shape_text):
                    iface.status = "unknown_dependency"
                    iface.resolution = (
                        f"DOWNGRADED: consumer claim is uncertain. "
                        f"Uncertain claim: '{claim_text[:100]}'"
                    )
                    break

    # Layer 2: CRD-assigned confidence.
    # When Workers produce prose instead of structured JSON, the Claim lists
    # are empty and Layer 1 is a no-op. The Coordinator extracts confidence
    # from Worker prose and reports it as producer_confidence / consumer_confidence.
    # This layer enforces those CRD-assigned labels.
    for iface in assessment.interfaces:
        if iface.status != "match":
            continue

        if iface.producer_confidence in ("unknown", "blocked"):
            iface.status = "unknown_dependency"
            iface.resolution = (
                f"DOWNGRADED: Coordinator assessed producer confidence as "
                f"'{iface.producer_confidence}'. Original status was 'match'."
            )
        elif iface.consumer_confidence in ("unknown", "blocked"):
            iface.status = "unknown_dependency"
            iface.resolution = (
                f"DOWNGRADED: Coordinator assessed consumer confidence as "
                f"'{iface.consumer_confidence}'. Original status was 'match'."
            )

    # Check dependency graph for uncertain artifacts
    for dep in assessment.dependency_graph:
        producer_uncertain = uncertain.get(dep.producer, set())
        if producer_uncertain:
            for claim_text in producer_uncertain:
                if _claims_overlap(claim_text, dep.artifact):
                    already_flagged = any(
                        c.type == "unknown_dependency"
                        and dep.producer in c.workers
                        for c in assessment.conflicts
                    )
                    if not already_flagged:
                        assessment.conflicts.append(Conflict(
                            type="unknown_dependency",
                            workers=[dep.producer, dep.consumer],
                            description=(
                                f"Dependency on '{dep.artifact}' relies "
                                f"on uncertain claim from {dep.producer}"
                            ),
                        ))

    return assessment


def _claims_overlap(claim_text: str, shape_text: str) -> bool:
    """Check if an uncertain claim is relevant to an interface shape.

    Simple keyword overlap -- not semantic matching. Checks whether any
    significant term (3+ chars, not stopwords) from the uncertain claim
    appears in the shape description.
    """
    stopwords = {"the", "and", "for", "that", "with", "from", "this",
                 "are", "was", "has", "have", "been", "not", "but"}
    claim_terms = {
        w for w in claim_text.lower().split()
        if len(w) >= 3 and w not in stopwords
    }
    shape_lower = shape_text.lower() if isinstance(shape_text, str) else str(shape_text).lower()
    return any(term in shape_lower for term in claim_terms)


# ---------------------------------------------------------------------------
# Phase 5: Worker execution (full tools, KF-gated, scope-enforced)
# ---------------------------------------------------------------------------

@dataclass
class PreFlightCheck:
    """A deterministic precondition that must hold before Worker execution.

    Failure stops THIS Worker (success=False, pre_flight_failures populated)
    but does NOT halt the pipeline -- other Workers continue.
    """
    name: str
    command: str
    failure_message: str


@dataclass
class ExecutionResult:
    """Result of a Worker execution against a task order."""
    worker_id: str
    worker_serial: str
    task_order_id: str
    files_written: list[str] = field(default_factory=list)
    files_read: list[str] = field(default_factory=list)
    commit_sha: str = ""
    raw_response: str = ""
    token_usage: dict[str, int] = field(default_factory=dict)
    tool_calls: int = 0
    iterations: int = 0
    success: bool = True
    error: str = ""
    pre_flight_failures: list[str] = field(default_factory=list)


def invoke_worker_for_execution(
    system_prompt: str,
    task_order_text: str,
    worker_id: str,
    worker_serial: str,
    task_order_id: str,
    working_directory: str,
    allowed_paths: list[str] | None = None,
    max_iterations: int = 25,
    branch: str = "",
    pre_flight_checks: list[PreFlightCheck] | None = None,
) -> ExecutionResult:
    """Invoke a Worker with full tool access to execute a task order.

    This is the execution path -- Workers read, write, edit, run commands,
    and commit. KF stage gating controls the tool set per phase:
      Pe: discover (list_dir, grep_files, read_file, run_command)
      In: targeted reads (read_file, grep_files)
      Ac: write only (write_file, edit_file, apply_patch) -- READ REMOVED
      Ad: self-check + commit (read, write, run_command, git_commit)

    allowed_paths scopes write operations to the task order's declared
    deliverables. Workers cannot write outside their scope.

    Args:
        system_prompt: Worker persona prompt.
        task_order_text: The full task order (objective, requirements,
            acceptance criteria, deliverables, dependencies).
        worker_id: Worker identity.
        worker_serial: Worker serial for commit attribution.
        task_order_id: Task order ID for traceability.
        working_directory: Filesystem root.
        allowed_paths: Deliverable paths the Worker may write to.
            If None, no scope enforcement (not recommended).
        max_iterations: Total iteration budget across all KF stages.
        branch: If set, checkout this branch before execution.
    """
    _llm = _get_llm_module()
    from .config import ARCHETYPE_MODELS
    from .tools import get_worker_tools, scope_tools_for_stage, resolve_read_ratio

    import subprocess as _sp
    import sys

    result = ExecutionResult(
        worker_id=worker_id,
        worker_serial=worker_serial,
        task_order_id=task_order_id,
    )

    # Checkout branch if specified.
    # Check current branch first -- skip checkout if already correct.
    if branch:
        try:
            current = _sp.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=working_directory, capture_output=True, text=True, timeout=10,
            )
            current_branch = current.stdout.strip()
            if current_branch == branch:
                print(f"  [EXEC] Already on branch: {branch}", file=sys.stderr)
            else:
                switch = _sp.run(
                    ["git", "checkout", branch],
                    cwd=working_directory, capture_output=True, text=True, timeout=30,
                )
                if switch.returncode != 0:
                    create = _sp.run(
                        ["git", "checkout", "-b", branch],
                        cwd=working_directory, capture_output=True, text=True, timeout=30,
                    )
                    if create.returncode != 0:
                        result.success = False
                        result.error = f"Branch checkout failed: {create.stderr.strip()}"
                        return result
                print(f"  [EXEC] Checked out branch: {branch}", file=sys.stderr)
        except Exception as e:
            result.success = False
            result.error = f"Branch checkout failed: {e}"
            return result

    # Run pre-flight checks (deterministic, before any LLM calls)
    if pre_flight_checks:
        import subprocess as _sp_check
        for check in pre_flight_checks:
            try:
                check_result = _sp_check.run(
                    check.command, shell=True, cwd=working_directory,
                    capture_output=True, text=True, timeout=60,
                )
                if check_result.returncode != 0:
                    result.success = False
                    result.pre_flight_failures.append(
                        f"[{check.name}] {check.failure_message} "
                        f"(exit code {check_result.returncode}: "
                        f"{check_result.stderr.strip()[:200]})"
                    )
                    print(f"  [PRE-FLIGHT FAIL] {check.name}: {check.failure_message}", file=sys.stderr)
            except _sp_check.TimeoutExpired:
                result.success = False
                result.pre_flight_failures.append(f"[{check.name}] Timed out after 60s")
            except Exception as e:
                result.success = False
                result.pre_flight_failures.append(f"[{check.name}] Check error: {e}")

        if not result.success:
            result.error = (
                f"Pre-flight checks failed: {len(result.pre_flight_failures)} failure(s). "
                f"This Worker is stopped but the pipeline continues."
            )
            return result

    # Get full tool set with scope enforcement
    all_tools = get_worker_tools(
        working_directory,
        allowed_paths=allowed_paths,
    )

    # Build KF-staged execution
    read_ceiling, write_budget = resolve_read_ratio(0.5, max_iterations)

    stages = [
        {
            "name": "Pe",
            "tools": scope_tools_for_stage("Pe", all_tools),
            "budget": max(2, read_ceiling // 2),
            "transition_msg": (
                "IMPORTANT: Before writing ANY code, you MUST read existing source "
                "files in this codebase to understand the patterns, conventions, "
                "imports, and dependencies that are already in use. Use grep_files "
                "to find relevant files, then read_file to study them. You will NOT "
                "be allowed to proceed to writing until you have read at least one "
                "source file. Do NOT invent implementations from imagination."
            ),
            "deliverables": allowed_paths or [],
            "working_dir": working_directory,
        },
        {
            "name": "In",
            "tools": scope_tools_for_stage("In", all_tools),
            "budget": max(1, read_ceiling // 2),
            "transition_msg": (
                "STAGE TRANSITION: Pe -> In. "
                "You have discovered the codebase structure. Now read the specific "
                "files that contain patterns you need to follow. Use read_file on "
                "the most relevant source files. Your code MUST follow the patterns "
                "you find -- do not invent alternative approaches."
            ),
            "deliverables": allowed_paths or [],
            "working_dir": working_directory,
        },
        {
            "name": "Ac",
            "tools": scope_tools_for_stage("Ac", all_tools),
            "budget": max(3, write_budget * 2 // 3),
            "transition_msg": (
                "STAGE TRANSITION: In -> Ac. "
                "READ TOOLS HAVE BEEN REMOVED. "
                "Write all deliverables now.\n\n"
                "CRITICAL TOOL SELECTION:\n"
                "- NEW files (that do not exist yet): use write_file\n"
                "- EXISTING files (that already have content): use edit_file "
                "to replace specific sections, or apply_patch for multi-line "
                "changes. NEVER use write_file on an existing file -- it will "
                "destroy the existing content. write_file is BLOCKED on files "
                "that already exist."
            ),
            "deliverables": allowed_paths or [],
            "working_dir": working_directory,
        },
        {
            "name": "Ad",
            "tools": scope_tools_for_stage("Ad", all_tools),
            "budget": max(2, write_budget // 3),
            "transition_msg": (
                "STAGE TRANSITION: Ac -> Ad. "
                "Read tools are restored. Verify your deliverables exist and "
                "are correct. Run any validation commands. When satisfied, "
                f"use git_commit with author_serial='{worker_serial}' to "
                "commit your work."
            ),
            "deliverables": allowed_paths or [],
            "working_dir": working_directory,
        },
    ]

    user_prompt = (
        f"## Task Order: {task_order_id}\n\n"
        f"{task_order_text}\n\n"
        f"## Instructions\n\n"
        f"Execute this task order. You have tool access to read, write, edit, "
        f"and run commands in the working directory.\n\n"
        f"Working directory: {working_directory}\n\n"
        f"## CRITICAL RULES\n\n"
        f"1. READ BEFORE WRITING. Before creating or modifying any file, you "
        f"MUST read existing source files in this codebase that are relevant to "
        f"your task. Find similar code, study the patterns (imports, class "
        f"structure, error handling, API usage), and base your implementation "
        f"on what you find. You will NOT be allowed to proceed to writing "
        f"until you have read at least one source file.\n\n"
        f"2. NO MOCK DATA. Never hardcode stub data, placeholder values, or "
        f"mock implementations. If the task requires reading from a database, "
        f"API, or file -- write the real code that reads from the real source. "
        f"Find an existing file in the codebase that does similar I/O and "
        f"follow that pattern exactly.\n\n"
        f"3. NO INVENTED PATTERNS. Do not invent import paths, class names, "
        f"API signatures, or data structures. Every import, every API call, "
        f"every data structure must be grounded in code you have read from "
        f"this codebase during the read phase.\n\n"
    )
    if allowed_paths:
        user_prompt += (
            f"Deliverable scope (you may ONLY write to these paths):\n"
            + "\n".join(f"  - {p}" for p in allowed_paths)
            + "\n\n"
        )
    user_prompt += (
        f"After writing all deliverables, use git_commit with "
        f"author_serial='{worker_serial}' to commit your work.\n"
    )

    try:
        response = _llm.invoke_llm_staged(
            system=system_prompt,
            user=user_prompt,
            stages=stages,
            model=ARCHETYPE_MODELS.get("supplier"),
            max_tokens=8192,
        )

        result.raw_response = response

        # Extract metrics from trace
        trace = _llm.get_last_trace()
        if trace:
            result.token_usage = {
                "input": trace.input_tokens,
                "output": trace.output_tokens,
                "total": trace.total_tokens,
            }
            result.tool_calls = trace.tool_call_count
            result.iterations = trace.iterations
            result.files_written = [
                tc.inputs.get("file_path", "")
                for tc in trace.tool_calls
                if tc.name in ("write_file", "edit_file") and tc.success
            ]
            result.files_read = [
                tc.inputs.get("file_path", "")
                for tc in trace.tool_calls
                if tc.name == "read_file"
            ]
            # Check for commit SHA in tool output
            for tc in trace.tool_calls:
                if tc.name == "git_commit" and tc.success and "Committed" in tc.output:
                    sha_match = re.search(r"Committed (\w+)", tc.output)
                    if sha_match:
                        result.commit_sha = sha_match.group(1)

    except Exception as e:
        result.success = False
        result.error = str(e)

    return result


# ---------------------------------------------------------------------------
# Orchestrator: alignment_pass() (called from coordinator.py)
# ---------------------------------------------------------------------------

def alignment_pass(
    spec: dict[str, Any],
    prd_section: str,
    worker_roster: list[dict[str, Any]],
    coordinator_identity: str,
    coordinator_prompt: str,
    working_directory: str,
) -> AlignmentAssessment | None:
    """Execute the full alignment protocol (Phases 1-3).

    Called from coordinator_node() before task order production.
    Returns AlignmentAssessment if alignment ran, None if skipped.
    """
    if not should_align(spec, worker_roster):
        return None

    # Phase 1: Mechanical StateRequest generation (no LLM call)
    state_requests = _produce_state_requests(prd_section, worker_roster)

    # Phase 2: Collect StateReports (sequential)
    state_reports = []
    total_tokens = {"phase2_input": 0, "phase2_output": 0}
    for request in state_requests:
        report = invoke_worker_for_state(
            worker_identity=request.worker_id,
            state_request=request,
            working_directory=working_directory,
        )
        state_reports.append(report)

        _llm = _get_llm_module()
        trace = _llm.get_last_trace()
        if trace:
            total_tokens["phase2_input"] += trace.input_tokens
            total_tokens["phase2_output"] += trace.output_tokens

    if not state_reports:
        return None

    # Phase 3: Coordinator synthesis
    assessment = synthesize_alignment(
        state_reports=state_reports,
        prd_section=prd_section,
        coordinator_identity=coordinator_identity,
        coordinator_prompt=coordinator_prompt,
    )

    assessment.token_usage.update(total_tokens)

    return assessment


# ---------------------------------------------------------------------------
# Phase 5: Schism Resolution (conversational 2-Worker mini-thread)
# ---------------------------------------------------------------------------

def resolve_schism(
    conflict: Conflict,
    report_a: StateReport,
    report_b: StateReport,
    coordinator_identity: str,
    coordinator_prompt: str,
    working_directory: str,
) -> str:
    """Phase 5: Resolve a schism through independent re-compilation.

    ONT.CORE.ALIGNMENT v2: Workers never see each other's responses.
    The Coordinator presents each Worker with a system constraint
    extracted from the other's report, without naming the source.

    Structure:
      1. Re-query Worker A under B's constraint (independent)
      2. Re-query Worker B under A's constraint (independent)
      3. Coordinator reads both adaptations and makes binding decision

    3 LLM calls (vs 5 in the v1 conversational loop). Workers don't
    know they're in a conflict -- they're compiling state under a
    tighter constraint set.
    """
    _llm = _get_llm_module()
    from .config import ARCHETYPE_MODELS

    if len(conflict.workers) < 2:
        return f"ERROR: Schism requires 2 workers, got {len(conflict.workers)}"

    worker_a_id = conflict.workers[0]
    worker_b_id = conflict.workers[1]

    # Extract constraint from each report (presented anonymously to the other)
    constraint_from_a = _extract_constraint(report_a, conflict)
    constraint_from_b = _extract_constraint(report_b, conflict)

    # Re-query Worker A under B's constraint (independent, single-turn)
    adaptation_a = invoke_worker_for_state(
        worker_identity=worker_a_id,
        state_request=StateRequest(
            worker_id=worker_a_id,
            worker_serial=report_a.worker_serial,
            prd_section=(
                f"## System Constraint\n\n"
                f"The system has identified this constraint that affects your interface:\n\n"
                f"{constraint_from_b}\n\n"
                f"## Original Conflict\n\n{conflict.description}"
            ),
            scoped_question=(
                "Given this system constraint, what are your valid adaptations? "
                "What can you change in your output shape/format and what cannot change?"
            ),
        ),
        working_directory=working_directory,
    )

    # Re-query Worker B under A's constraint (independent, single-turn)
    adaptation_b = invoke_worker_for_state(
        worker_identity=worker_b_id,
        state_request=StateRequest(
            worker_id=worker_b_id,
            worker_serial=report_b.worker_serial,
            prd_section=(
                f"## System Constraint\n\n"
                f"The system has identified this constraint that affects your interface:\n\n"
                f"{constraint_from_a}\n\n"
                f"## Original Conflict\n\n{conflict.description}"
            ),
            scoped_question=(
                "Given this system constraint, what are your valid adaptations? "
                "What can you change in your input expectations and what cannot change?"
            ),
        ),
        working_directory=working_directory,
    )

    # Coordinator decides from both independent adaptations
    return _llm.invoke_llm(
        system=coordinator_prompt,
        user=(
            f"## Schism Resolution\n\n"
            f"**Conflict:** {conflict.description}\n\n"
            f"## Worker A ({report_a.worker_serial}) adaptations:\n\n"
            f"{adaptation_a.raw_response[:2000]}\n\n"
            f"## Worker B ({report_b.worker_serial}) adaptations:\n\n"
            f"{adaptation_b.raw_response[:2000]}\n\n"
            "Make the binding decision. Which interface design wins? "
            "Who adapts? What specific changes? If neither can adapt, "
            "escalate to Architect with a clear description of why "
            "the design needs revision."
        ),
        model=ARCHETYPE_MODELS["coordinator"],
        tools=[], max_tokens=2048,
    )


def _extract_constraint(report: StateReport, conflict: Conflict) -> str:
    """Extract a constraint from a StateReport to present anonymously.

    Frames the Worker's position as a system constraint without naming
    the source Worker. The receiving Worker sees it as a requirement
    they must adapt to, not as another Worker's opinion.
    """
    parts = []

    for c in report.what_i_produce[:3]:
        if isinstance(c, Claim):
            parts.append(f"- Output requires: {c.statement} [{c.confidence.upper()}]")

    for c in report.constraints[:3]:
        parts.append(f"- Constraint: {c}")

    if report.requires_from_others:
        for r in report.requires_from_others[:3]:
            parts.append(f"- Dependency: {r}")

    if not parts:
        parts.append(f"- {conflict.description}")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

def assessment_to_dict(assessment: AlignmentAssessment) -> dict[str, Any]:
    """Serialize AlignmentAssessment to dict for ProjectState storage."""
    return {
        "interfaces": [
            {
                "producer": i.producer, "consumer": i.consumer,
                "producer_shape": i.producer_shape, "consumer_shape": i.consumer_shape,
                "status": i.status, "resolution": i.resolution,
                "producer_confidence": i.producer_confidence,
                "consumer_confidence": i.consumer_confidence,
            }
            for i in assessment.interfaces
        ],
        "gaps": assessment.gaps,
        "conflicts": [
            {
                "type": c.type, "workers": c.workers,
                "description": c.description, "resolution": c.resolution,
            }
            for c in assessment.conflicts
        ],
        "dependency_graph": [
            {
                "producer": d.producer, "consumer": d.consumer,
                "artifact": d.artifact, "required_before": d.required_before,
            }
            for d in assessment.dependency_graph
        ],
        "schisms": assessment.schisms,
        "token_usage": assessment.token_usage,
    }
