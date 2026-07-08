#!/usr/bin/env python3
"""NFRA_CSE.P3 -- the per-producer CSE EMISSION-CONTRACT spec (DS-side).

Defines, for each of the >=4 AC5 producers (git, graph_head, agent, deploy), the schema-valid CSE
shape + MANDATORY provenance it emits into the P2 C0 log (globgrph.cse). The producer-WIRING
(0.5.0_AE_OpalETL, sequenced after FEDOBS-P3) implements the live emit AGAINST this contract; this
module OWNS the contract (DS owns the CSE definition). Every contract is grounded in the producer's
REAL signal shape and proven schema-valid by round-trip through cse_schema.validate (Rule 22 -- a
contract that does not validate is not a contract).

THE EMISSION PIPELINE (PRD 4.3 / charter S3a): Producer -> [front-end parse -> semantic enrichment ->
domain recognizers] -> CSE(s) -> event log. This module specifies the RECOGNIZER OUTPUT (the CSE
shape) per producer. The front-end/enrichment is the producer's own existing signal:
  - git        : the code compiler (comp-tools / ts-morph-extract_api) over a commit -- the REFERENCE
                 (the 6 live WRITES_S3 CSEs in globgrph.cse already prove this pattern end-to-end).
  - graph_head : the CloudNode/CloudEdge delta on a Nessie HEAD-advance (my NFRA_CSE_P2_ac4_fullgraph_
                 parity.py recognizers -- the graph itself as producer; ProducerKind.GRAPH_HEAD).
  - agent      : the OPLMCP .05 audit-lake mcp_audit record (Glue: ts/user/tool/args/outcome/detail,
                 REDACTED-only -- who/tool/when/outcome/redacted-args, NEVER M365 body/content).
  - deploy     : the deploy-completion ledger (org/critical_paths/change_management/*_deploy_completion
                 .md -- legs{kind,target,proof,state}).

CONFIDENCE SPANS THE HONEST RANGE ACROSS PRODUCERS (LAW 1, deliberately):
  git / graph_head / deploy -> HIGH (1.0): the source lexically NAMES the subject (a put_object Key, a
    node_type, a ledger-named resource) -- lexically certain, a certain type.
  agent -> LOW (<=0.34) for a REDACTED M365 target: the audit-lake is redaction-proven, so the agent
    producer GENUINELY cannot type what it is forbidden to read -> Concept(untyped)+low, the honest-
    degrade target used EXACTLY as LAW 1 intends (not a workaround -- the correct honest representation
    of a target we cannot lexically resolve). An agent action on a KNOWN typed entity (e.g. a git
    commit via a tool) is HIGH; the redacted-M365 case is the honest-low case.

AC5 = >=4 producers emit VALID CSEs through the pipeline into the log. This module proves the CONTRACT
(shape + provenance + round-trip) for 4; AE wires the live emit; the graph_head persistent stream (at
0.3) becomes the log's substantive content (superseding the 6-row genesis seed -- migration option (c),
append-only-preserving).

Author: 0.4.0_DS_ClientPlatform~B   TO: NFRA_CSE.P3   Date: 2026-07-08
Status: DRAFT spec (runnable, 4/4 producers validate + round-trip). For CTO arch-gate (contract-
conformance vs his algebra) + CVO exercise-cert -> RAVC COO -> COO GOes the AE producer-wiring.
"""
from __future__ import annotations

import os
import sys

# UNIFY-NOT-BUILD: the canonical algebra + validator (P1, CVO-certed, @0.3). Path-robust for the DS
# deliverables lane; a plain sibling import at the canonical home.
_GRAPH_MOD = os.path.join(os.path.dirname(__file__), "..", "..", "..", "modules", "graph")
if os.path.isdir(_GRAPH_MOD):
    sys.path.insert(0, os.path.abspath(_GRAPH_MOD))
import cse_schema as CSE  # noqa: E402
from cse_schema import CSE as CSEvent, EntityRef, Provenance, RelationshipDelta  # noqa: E402


# ===========================================================================
# THE PER-PRODUCER EMISSION CONTRACT (the spec, as structured data -- AE implements against this).
#   Each contract fixes: the ProducerKind, the ref semantics, the compiler/artifact_class, the
#   recognizer name, the subject-typing rule + confidence band, and the provenance mapping (which
#   REAL source field lands in source/locus/evidence). The `example()` proves it validates.
# ===========================================================================
def contract_git() -> dict:
    """git commit -> code-compiler recognizer -> code CSE. The REFERENCE producer (6 live proofs)."""
    return {
        "producer_kind": CSE.ProducerKind.GIT.value,
        "ref": "the commit SHA",
        "compiler": {"id": "code-infra-compiler#1", "artifact_class": "python|ts|tf|yaml", "version": CSE.SCHEMA_VERSION},
        "recognizer": "lambda_s3_write_recognizer (+ the code-compiler recognizer family)",
        "subject_rule": "the lexically-named code/infra entity (Lambda/Function/S3Bucket/...); HIGH confidence (a put_object Key is lexically certain)",
        "provenance_map": {"source": "the source file path", "locus": "L<line>",
                           "evidence": "the literal call text (e.g. s3.put_object(Bucket=B, Key=K))"},
        "example": example_git,
    }


def contract_graph_head() -> dict:
    """Nessie HEAD-advance -> CloudNode/CloudEdge delta recognizer -> graph_head CSE."""
    return {
        "producer_kind": CSE.ProducerKind.GRAPH_HEAD.value,
        "ref": "the Nessie marker / snapshot-id at emission (== head.marker_head; one-marker-commit)",
        "compiler": {"id": "graph-head-delta-compiler", "artifact_class": "cloudnode|cloudedge", "version": CSE.SCHEMA_VERSION},
        "recognizer": "cloudnode_graph_recognizer / cloudedge_graph_recognizer (NFRA_CSE_P2_ac4_fullgraph_parity)",
        "subject_rule": "the CloudNode/CloudEdge mapped via map_cloudnode/CLOUDEDGE_TO_RELATIONSHIP; HIGH confidence (deterministic node_type->Entity); verb = create|delete|modify per the HEAD-advance delta",
        "provenance_map": {"source": "kuzu_nessie_db@<marker>", "locus": "the node_id / src->dst",
                           "evidence": "node_type=<T> / edge_type=<T>"},
        "example": example_graph_head,
    }


def contract_agent() -> dict:
    """OPLMCP .05 audit-lake mcp_audit record -> mcp-audit recognizer -> agent CSE (near-free, CVO #6)."""
    return {
        "producer_kind": CSE.ProducerKind.AGENT.value,
        "ref": "the audit `user` (agent serial / MCP principal)",
        "compiler": {"id": "mcp-audit-compiler", "artifact_class": "mcp_audit", "version": CSE.SCHEMA_VERSION},
        "recognizer": "mcp_audit_recognizer (over opal_mcp.mcp_audit: ts/user/tool/args/outcome/detail)",
        "subject_rule": "the tool's target. TYPED+HIGH when the target is a known fabric entity; "
                        "Concept(untyped)+LOW(<=0.34) for a REDACTED M365 target -- the audit-lake is "
                        "redaction-proven, so we GENUINELY cannot type it: the honest-degrade target used "
                        "exactly as LAW 1 intends (never a smuggled guess). verb from the tool's action class.",
        "provenance_map": {"source": "opal-mcp-audit/audit/dt=<dt>/<ts>.jsonl", "locus": "the ts",
                           "evidence": "tool=<tool> outcome=<outcome> args=<redacted-args>"},
        "example": example_agent,
    }


def contract_deploy() -> dict:
    """deploy-completion ledger record -> deploy-ledger recognizer -> deploy CSE."""
    return {
        "producer_kind": CSE.ProducerKind.DEPLOY.value,
        "ref": "the deploy-completion ledger id (the record filename)",
        "compiler": {"id": "deploy-ledger-compiler", "artifact_class": "deploy_completion", "version": CSE.SCHEMA_VERSION},
        "recognizer": "deploy_ledger_recognizer (over org/critical_paths/change_management/*_deploy_completion.md legs)",
        "subject_rule": "the deployed resource named in the leg target/proof (S3Bucket/Service/Lambda/IAMRole/...); "
                        "HIGH confidence (the ledger lexically NAMES the resource + carries the proof); "
                        "verb = create|modify per the leg kind (a first apply CREATEs, a re-deploy MODIFYs)",
        "provenance_map": {"source": "org/critical_paths/change_management/<id>_deploy_completion.md",
                           "locus": "leg <A|B|C>", "evidence": "the leg's proof line (the apply result / SSM proof)"},
        "example": example_deploy,
    }


PRODUCER_CONTRACTS = {
    "git": contract_git, "graph_head": contract_graph_head,
    "agent": contract_agent, "deploy": contract_deploy,
}


# ===========================================================================
# GROUNDED EXAMPLES -- one representative, REAL-sourced CSE per producer (Rule 22: grounded, not
# invented). Each is built to VALIDATE through cse_schema.validate @0.3 (the AC5 proof).
# ===========================================================================
def _cse(*, producer, ref, compiler, verb, subject, edges, prov, conf, marker, scope=None) -> CSEvent:
    quals = {CSE.Qualifier.CONFIDENCE.value: conf}
    if scope:
        quals[CSE.Qualifier.SCOPE.value] = scope
    return CSEvent(
        event_id=f"{producer}:{ref}",
        schema_version=CSE.SCHEMA_VERSION,
        producer={"kind": producer, "ref": ref},
        compiler=compiler,
        transformation={"verb": verb, "subject": subject, "edges": edges},
        provenance=prov,
        execution_meta={"timestamp": "2026-07-08T01:00Z", "actor": "harness", "run_id": ref},
        head={"marker_head": marker},
        qualifiers=quals,
    )


def example_git() -> CSEvent:
    """git: the bd-price-update WRITES_S3 code CSE (== one of the 6 live genesis rows in globgrph.cse)."""
    return _cse(
        producer=CSE.ProducerKind.GIT.value, ref="6311852d9",
        compiler={"id": "code-infra-compiler#1", "artifact_class": "python", "version": CSE.SCHEMA_VERSION},
        verb=CSE.Transformation.CREATE.value,
        subject=EntityRef(CSE.Entity.LAMBDA.value, "arn:aws:lambda:us-east-1:313476888478:function:bd-price-update"),
        edges=[RelationshipDelta(CSE.Relationship.WRITES.value,
                                 EntityRef(CSE.Entity.S3BUCKET.value, "opal-data-bd/silver/prices/canonical_prices.parquet"))],
        prov=Provenance("infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py", "L441",
                        "lambda_s3_write_recognizer",
                        "s3.put_object(Bucket=opal-data-bd, Key=silver/prices/canonical_prices.parquet)"),
        conf=1.0, marker="6127141211382924351")


def example_graph_head() -> CSEvent:
    """graph_head: a CloudNode materialized on a HEAD-advance (the graph-as-producer, my P2 recognizer)."""
    return _cse(
        producer=CSE.ProducerKind.GRAPH_HEAD.value, ref="6127141211382924351",
        compiler={"id": "graph-head-delta-compiler", "artifact_class": "cloudnode", "version": CSE.SCHEMA_VERSION},
        verb=CSE.Transformation.CREATE.value,
        subject=EntityRef(CSE.Entity.LAMBDA.value, "arn:aws:lambda:us-east-1:313476888478:function:bd-price-update"),
        edges=[],
        prov=Provenance("kuzu_nessie_db@6127141211382924351",
                        "arn:aws:lambda:us-east-1:313476888478:function:bd-price-update",
                        "cloudnode_graph_recognizer", "node_type=LAMBDA"),
        conf=1.0, marker="6127141211382924351")


def example_agent() -> CSEvent:
    """agent: an OPLMCP audit-lake tool call on a REDACTED M365 target -> Concept(untyped)+low (honest-degrade)."""
    return _cse(
        producer=CSE.ProducerKind.AGENT.value, ref="2.0.0_SA_COO~B",
        compiler={"id": "mcp-audit-compiler", "artifact_class": "mcp_audit", "version": CSE.SCHEMA_VERSION},
        verb=CSE.Transformation.CREATE.value,
        # the redacted M365 target is genuinely untypable (redaction-proven) -> Concept(untyped)+LOW.
        subject=EntityRef(CSE.Entity.CONCEPT.value, "mcp:send_channel_message:<redacted-target>"),
        edges=[],
        prov=Provenance("opal-mcp-audit/audit/dt=2026-06-24/2026-06-24T13:55:30.jsonl",
                        "2026-06-24T13:55:30Z", "mcp_audit_recognizer",
                        "tool=send_channel_message outcome=ok args={body:'<redacted 352 chars>'}"),
        conf=0.2, marker="6127141211382924351", scope="opal-m365")


def example_deploy() -> CSEvent:
    """deploy: the OPLMCP.05 R8 audit-lake apply -> a deploy CSE on the created S3 bucket (ledger-named)."""
    return _cse(
        producer=CSE.ProducerKind.DEPLOY.value, ref="20260624T1340Z_oplmcp05-r8-audit-lake",
        compiler={"id": "deploy-ledger-compiler", "artifact_class": "deploy_completion", "version": CSE.SCHEMA_VERSION},
        verb=CSE.Transformation.CREATE.value,
        subject=EntityRef(CSE.Entity.S3BUCKET.value, "s3:opal-mcp-audit"),
        edges=[RelationshipDelta(CSE.Relationship.GOVERNS.value,
                                 EntityRef(CSE.Entity.POLICY.value, "stmt:AuditLakePutOnly"))],
        prov=Provenance("org/critical_paths/change_management/20260624T1340Z_oplmcp05-r8-audit-lake_deploy_completion.md",
                        "leg A", "deploy_ledger_recognizer",
                        "safe-apply tfplan.r8 = 'Apply complete! 12 added, 0 changed, 0 destroyed'; opal-mcp-audit bucket exists (object-lock Enabled)"),
        conf=1.0, marker="6127141211382924351")


# ===========================================================================
# RUNNABLE SELF-TEST -- AC5: every producer emits a VALID CSE + round-trips (fidelity decompress).
# ===========================================================================
def self_test() -> bool:
    checks = []

    def chk(name, cond, detail=""):
        checks.append(cond)
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  -> {detail}" if (detail and not cond) else ""))

    print(f"=== NFRA_CSE.P3 emission-contract self-test (schema {CSE.SCHEMA_VERSION}) ===")
    validated = 0
    for name, contract_fn in PRODUCER_CONTRACTS.items():
        contract = contract_fn()
        cse = contract["example"]()
        ok, errs = CSE.validate(cse)
        chk(f"producer '{name}': emits a schema-valid CSE (kind={contract['producer_kind']})", ok, str(errs))
        # each must also decompress through the fidelity gate (mandatory-provenance -> lexical evidence)
        fok, ff = CSE.cse_fidelity_ok(cse)
        chk(f"producer '{name}': CSE decompresses to C0 evidence (fidelity, LAW 2)", fok, str(ff))
        if ok and fok:
            validated += 1

    # AC5: >=4 producers emit valid CSEs
    chk(f"AC5: >=4 producers emit valid CSEs (got {validated}/4)", validated >= 4)

    # the honest-range property: agent(redacted) is LOW-band Concept; the other 3 are HIGH typed
    agent_cse = example_agent()
    chk("agent redacted-target is Concept(untyped)+low (honest-degrade, LAW 1 -- not a smuggled guess)",
        agent_cse.transformation["subject"].etype == CSE.Entity.CONCEPT.value
        and CSE.confidence_band(agent_cse.qualifiers[CSE.Qualifier.CONFIDENCE.value]) == "low")
    for nm in ("git", "graph_head", "deploy"):
        c = PRODUCER_CONTRACTS[nm]()["example"]()
        et = c.transformation["subject"].etype
        band = CSE.confidence_band(c.qualifiers[CSE.Qualifier.CONFIDENCE.value])
        chk(f"'{nm}' subject is TYPED+high (lexically certain)",
            et != CSE.Entity.CONCEPT.value and band == "high")

    # a NEGATIVE control: a would-be agent CSE that smuggles a HIGH-confidence type on a redacted
    # (untypable) target MUST be REJECTED (the contract cannot let a producer invent a type).
    bad = example_agent()
    bad.qualifiers[CSE.Qualifier.CONFIDENCE.value] = 0.95   # claim high confidence on the untyped target
    ok_bad, _ = CSE.validate(bad)
    chk("NEGATIVE: agent smuggling high-confidence on a Concept(untyped) target is REJECTED (fail-closed)",
        not ok_bad)

    passed = sum(1 for c in checks if c)
    print(f"=== {passed}/{len(checks)} PASS ===")
    return passed == len(checks)


def print_spec() -> None:
    """Human-readable emission-contract spec (what AE wires against)."""
    print(f"# NFRA_CSE.P3 per-producer emission contracts (schema {CSE.SCHEMA_VERSION})\n")
    for name, fn in PRODUCER_CONTRACTS.items():
        c = fn()
        print(f"## producer: {name}  (ProducerKind.{c['producer_kind']})")
        print(f"   ref         : {c['ref']}")
        print(f"   compiler    : {c['compiler']['id']}  (artifact_class={c['compiler']['artifact_class']})")
        print(f"   recognizer  : {c['recognizer']}")
        print(f"   subject rule: {c['subject_rule']}")
        print(f"   provenance  : source={c['provenance_map']['source']}")
        print(f"                 locus={c['provenance_map']['locus']}  evidence={c['provenance_map']['evidence']}")
        print()


if __name__ == "__main__":
    if "--spec" in sys.argv:
        print_spec()
        sys.exit(0)
    sys.exit(0 if self_test() else 1)
