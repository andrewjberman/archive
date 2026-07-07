#!/usr/bin/env python3
"""NFRA_CSE.P1 -- the Canonical Semantic Event contract + versioned semantic algebra (validator).

Built by DS against CTO's authoritative algebra-design v0.1 (docs/architecture/
NFRA_CSE_algebra_schema_v0.1.md, 63b3b9015) -- the shared IR of the Semantic Control Plane.
UNIFY-NOT-BUILD: the four families + the CSE contract + the validator RULES + the mapping approach
are CTO's design (S1-S6); this module is DS's executable form (the enums-as-code + the fail-closed
validator impl + the full CloudNode/CloudEdge mapping table + the parity check + the coverage-sweep
wire). Nothing here invents algebra -- extension is a governed version-bump in CTO's design.

Two gating laws (charter): LAW 1 lexical-certainty-before-inference (reject-not-coerce; untypable ->
Concept(untyped)+low, never a guess); LAW 2 explicit-promotion (full provenance to lexical evidence
so every conclusion decompresses via comp_ladder).

DRAFT for CTO arch-gate (schema-vs-his-design) -> CVO exercise-cert (AC5 fidelity + AC4 parity).
Canonical home on gate = org/modules/graph/cse_schema.py (alongside comp_ladder.py) -- staged here
in the DS lane (org/modules/graph is EXEC-lane); CTO/exec places it canonically on the gate.

Author: 0.4.0_DS_ClientPlatform~B   TO: NFRA_CSE.P1   Date: 2026-07-07
"""
from __future__ import annotations

import enum
import os
import sys
from dataclasses import dataclass, field

# AC5 -- bind the SHARED fidelity gate (comp_ladder.py in the graph module). Path-robust so this
# draft runs from the DS deliverables lane; on canonical placement it is a plain sibling import.
_GRAPH_MOD = os.path.join(os.path.dirname(__file__), "..", "..", "..", "modules", "graph")
if os.path.isdir(_GRAPH_MOD):
    sys.path.insert(0, os.path.abspath(_GRAPH_MOD))
from comp_ladder import Node as LadderNode, fidelity_check  # noqa: E402,F401


# ===========================================================================
# S1/S5  VERSIONED ALGEBRA -- 4 governed-extensible families (CTO design S1)
#   schema_version 0.1. Each family is a CLOSED enum at a version; extension = version-bump +
#   COMPUNIFY coverage-sweep. A recognizer needing an off-enum value emits Concept(untyped)+low +
#   a coverage-gap CSE -- it NEVER invents a value (LAW 1).
# ===========================================================================
SCHEMA_VERSION = "0.1"
MIGRATION_NOTE = (
    "Add a primitive -> version-bump + COMPUNIFY coverage-sweep (which compilers must now handle "
    "it); a gap is a tracked coverage-gap, not a silent skip. Remove/rename -> version-bump + a "
    "CSE-log materializer migration. CTO-arch-gated; a recognizer never forks its own primitive."
)


class Entity(enum.Enum):
    """Nouns (typed). Org (charter) + code/infra reference-compiler vocabulary (CTO S1)."""
    # org-level
    ARTIFACT = "Artifact"
    COMPONENT = "Component"
    CONCEPT = "Concept"                # Concept(untyped) = the LAW-1 honest-degrade target
    REQUIREMENT = "Requirement"
    CONSTRAINT = "Constraint"
    DATASET = "Dataset"
    SERVICE = "Service"
    PERSON = "Person"
    ORGANIZATION = "Organization"
    POLICY = "Policy"
    # code/infra-level (concrete, first-class per CTO S1 + the S4 mapping)
    FUNCTION = "Function"
    MODULE = "Module"
    ENDPOINT = "Endpoint"
    TABLE = "Table"
    LAMBDA = "Lambda"
    S3BUCKET = "S3Bucket"
    IAMROLE = "IAMRole"
    IAMSTATEMENT = "IAMStatement"
    SCHEDULE = "Schedule"
    SECRETREF = "SecretRef"
    FIELD = "Field"
    REACTCOMPONENT = "ReactComponent"
    JSXELEMENT = "JSXElement"
    HOOK = "Hook"
    GRAPHSCOPE = "GraphScope"
    TOOL = "Tool"
    TIER = "Tier"


class Relationship(enum.Enum):
    """Typed edges (not inferred). Org (charter) + live CloudEdge discriminators (CTO S1)."""
    CONTAINS = "contains"
    REFERENCES = "references"
    DEPENDS_ON = "depends_on"
    PRODUCES = "produces"
    CONSUMES = "consumes"
    IMPLEMENTS = "implements"
    GOVERNS = "governs"
    DERIVES_FROM = "derives_from"
    SUPERSEDES = "supersedes"
    # code/infra (CloudEdge discriminators)
    CALLS = "calls"
    IMPORTS = "imports"
    READS = "reads"
    WRITES = "writes"
    RENDERS = "renders"
    FLOWS_TO = "flows_to"
    FETCHES = "fetches"
    SERVED_FROM = "served_from"
    TRIGGERS = "triggers"
    DENIED = "denied"
    ALLOWED = "allowed"
    REQUIRES = "requires"
    AUTHENTICATES = "authenticates"
    AUTHORIZES = "authorizes"


class Transformation(enum.Enum):
    """The semantic delta a CSE records -- CTO S1, closed set."""
    CREATE = "create"
    DELETE = "delete"
    MODIFY = "modify"
    SPLIT = "split"
    MERGE = "merge"
    RENAME = "rename"
    STRENGTHEN = "strengthen"
    WEAKEN = "weaken"
    RECLASSIFY = "reclassify"
    RELOCATE = "relocate"


class Qualifier(enum.Enum):
    """Orthogonal metadata keys on the qualifiers block -- CTO S1. confidence+provenance load-bearing."""
    SCOPE = "scope"
    CONFIDENCE = "confidence"
    PROVENANCE = "provenance"
    TEMPORAL_VALIDITY = "temporal_validity"
    AUTHORITY = "authority"
    VISIBILITY = "visibility"
    STABILITY = "stability"
    OWNERSHIP = "ownership"


class ProducerKind(enum.Enum):
    GIT = "git"
    AGENT = "agent"
    DEPLOY = "deploy"
    IDE = "ide"
    TICKET = "ticket"
    DOC = "doc"
    INFRA = "infra"
    API = "api"
    APPROVAL = "approval"
    GRAPH_HEAD = "graph_head"


# confidence is a FLOAT in [0,1] (CTO contract S2: `confidence: float`). The LAW-1 untyped-honest
# rule (S3.5) requires "confidence: low" -> LOW is the band confidence <= LOW_CONFIDENCE_MAX. The
# exact threshold is a CTO reconciliation question (flagged in the RAVC); 0.34 is a documented
# default (thirds: low<=0.34 < medium <=0.67 < high).
LOW_CONFIDENCE_MAX = 0.34

_ENTITY_VALUES = frozenset(e.value for e in Entity)
_REL_VALUES = frozenset(r.value for r in Relationship)
_VERB_VALUES = frozenset(t.value for t in Transformation)
_QUAL_VALUES = frozenset(q.value for q in Qualifier)
_PRODUCER_VALUES = frozenset(p.value for p in ProducerKind)


# ===========================================================================
# S2  THE CSE CONTRACT (CTO design S2 -- incl. the head.marker_head field, AC6)
# ===========================================================================
@dataclass
class EntityRef:
    etype: str            # an Entity value
    ref: str              # a stable node id (e.g. 's3:opal-data-bd', 'stmt:DenyCrossFirmBuckets')


@dataclass
class RelationshipDelta:
    rtype: str            # a Relationship value
    target: EntityRef
    verb: str = Transformation.CREATE.value   # create|delete|modify the edge itself


@dataclass
class Provenance:
    """MANDATORY (LAW 2). CTO S2: {source, locus, parser|recognizer, evidence}. Mirrors comp_ladder
    C0 provenance so a CSE decompresses through the fidelity gate. `evidence` non-empty = required."""
    source: str
    locus: str
    recognizer: str        # parser|recognizer
    evidence: str


@dataclass
class CSE:
    """The atomic record of one recognized semantic delta. Every producer emits this exact shape."""
    event_id: str
    schema_version: str
    producer: dict          # {kind, ref}
    compiler: dict          # {id, artifact_class, version}
    transformation: dict    # {verb, subject: EntityRef, edges: [RelationshipDelta]}
    provenance: Provenance  # MANDATORY
    execution_meta: dict    # {timestamp, actor, run_id} -- harness-attached
    head: dict              # {marker_head} -- GLOBGRPH marker-HEAD at emission (AC6)
    qualifiers: dict = field(default_factory=dict)   # {scope, confidence: float, ...}


# ===========================================================================
# S4  CloudNode/CloudEdge -> algebra mapping (AC3 -- the REAL code slice, two vocabularies)
#   (a) node_type STRING discriminators (derive_runner.NODE_TYPE_LAYER, uppercase) and
#   (b) node id PREFIX scheme (CTO S4: 's3:', 'component:', 'endpoint:', 'gold:', 'field:', 'rqk:',
#       'symbol:/type:', 'stmt:', 'lambda:', 'role:'). Both reconcile INTO the same Entity set.
# ===========================================================================
# (a) node_type -> Entity (all 54 NODE_TYPE_LAYER types; concrete infra kept first-class per CTO S1)
CLOUDNODE_TYPE_TO_ENTITY: dict = {
    "LAMBDA": Entity.LAMBDA, "ECS_CLUSTER": Entity.SERVICE, "ECS_TASK_DEFINITION": Entity.SERVICE,
    "EC2_INSTANCE": Entity.SERVICE, "STATE_MACHINE": Entity.SERVICE, "API_GW": Entity.SERVICE,
    "LOAD_BALANCER": Entity.SERVICE, "CLOUDFRONT_DISTRIBUTION": Entity.SERVICE,
    "SERVICE_PRINCIPAL": Entity.SERVICE, "VPC_ENDPOINT": Entity.SERVICE, "EVENT_SOURCE": Entity.SERVICE,
    "S3_BUCKET": Entity.S3BUCKET, "DYNAMODB_TABLE": Entity.TABLE, "SQS_QUEUE": Entity.DATASET,
    "SNS_TOPIC": Entity.SERVICE, "LOG_GROUP": Entity.DATASET, "S3Key": Entity.DATASET,
    "SECRET": Entity.SECRETREF, "KMS_KEY": Entity.SECRETREF,
    "S3_BUCKET_POLICY": Entity.POLICY, "IAM_POLICY": Entity.POLICY, "IAM_ROLE": Entity.IAMROLE,
    "IAM_USER": Entity.PERSON, "INSTANCE_PROFILE": Entity.POLICY,
    "SECURITY_GROUP": Entity.CONSTRAINT, "CW_ALARM": Entity.CONSTRAINT, "EVENT_RULE": Entity.SCHEDULE,
    "API_ROUTE": Entity.ENDPOINT, "ROUTE53_RECORD": Entity.ENDPOINT,
    "Component": Entity.COMPONENT, "ReactComponent": Entity.REACTCOMPONENT, "PanelCluster": Entity.COMPONENT,
    "Module": Entity.MODULE, "Page": Entity.COMPONENT, "Hook": Entity.HOOK, "DataFetch": Entity.FUNCTION,
    "Endpoint": Entity.ENDPOINT, "ServedURL": Entity.ENDPOINT, "ReactQueryKey": Entity.DATASET,
    "Field": Entity.FIELD, "Prop": Entity.FIELD, "TypeDecl": Entity.CONCEPT,
    "JSXElement": Entity.JSXELEMENT, "JSXRender": Entity.JSXELEMENT,
    "MS_SITE": Entity.ORGANIZATION, "MS_LIBRARY": Entity.DATASET, "MS_FOLDER": Entity.DATASET,
    "MS_FILE": Entity.ARTIFACT, "MS_USER": Entity.PERSON, "MS_GROUP": Entity.ORGANIZATION,
    "MS_DRIVE_ONEDRIVE": Entity.DATASET,
    "Pipeline": Entity.SERVICE, "PipelineScript": Entity.MODULE, "PipelineFunction": Entity.FUNCTION,
}

# (b) node id PREFIX -> Entity (CTO S4 nid-prefix scheme)
CLOUDNODE_PREFIX_TO_ENTITY: dict = {
    "s3:": Entity.S3BUCKET, "component:": Entity.REACTCOMPONENT, "endpoint:": Entity.ENDPOINT,
    "gold:": Entity.DATASET, "field:": Entity.FIELD, "rqk:": Entity.DATASET, "symbol:": Entity.CONCEPT,
    "type:": Entity.COMPONENT, "stmt:": Entity.IAMSTATEMENT, "role:": Entity.IAMROLE,
    "lambda:": Entity.LAMBDA, "bucket:": Entity.S3BUCKET, "hook:": Entity.HOOK, "module:": Entity.MODULE,
    "tool:": Entity.TOOL, "tier:": Entity.TIER, "scope:": Entity.GRAPHSCOPE,
}

# CloudEdge edge_type -> Relationship (live discriminators, CTO S4 + ms + code)
CLOUDEDGE_TO_RELATIONSHIP: dict = {
    "RENDERS": Relationship.RENDERS, "FLOWS_TO": Relationship.FLOWS_TO, "FETCHES": Relationship.FETCHES,
    "SERVED_FROM": Relationship.SERVED_FROM, "CONTAINS": Relationship.CONTAINS,
    "CALLS": Relationship.CALLS, "IMPORTS": Relationship.IMPORTS, "READS": Relationship.READS,
    "WRITES": Relationship.WRITES, "TRIGGERS": Relationship.TRIGGERS, "DENIED": Relationship.DENIED,
    "ALLOWED": Relationship.ALLOWED, "REQUIRES": Relationship.REQUIRES,
    "AUTHENTICATES": Relationship.AUTHENTICATES, "AUTHORIZES": Relationship.AUTHORIZES,
    "OWNED_BY": Relationship.GOVERNS, "HAS_ACCESS": Relationship.REFERENCES,
    "SHARED_WITH": Relationship.REFERENCES, "MEMBER_OF": Relationship.CONTAINS,
    "DEPENDS_ON": Relationship.DEPENDS_ON, "REFERENCES": Relationship.REFERENCES,
    "PRODUCES": Relationship.PRODUCES, "CONSUMES": Relationship.CONSUMES,
    "IMPLEMENTS": Relationship.IMPLEMENTS,
}


def map_cloudnode(nid: str, node_type: str = "") -> Entity:
    """AC3: resolve a CloudNode to its algebra Entity -- node_type first, else the nid prefix.
    Returns None if neither resolves (a coverage gap -> caller fail-closes)."""
    if node_type and node_type in CLOUDNODE_TYPE_TO_ENTITY:
        return CLOUDNODE_TYPE_TO_ENTITY[node_type]
    for pfx, ent in CLOUDNODE_PREFIX_TO_ENTITY.items():
        if str(nid).startswith(pfx):
            return ent
    return None


# ===========================================================================
# S3  THE FAIL-CLOSED VALIDATOR (CTO S3 rules 1-6, LAW 1 enforced not documented)
# ===========================================================================
class CSEValidationError(Exception):
    """Fail-closed rejection (off-schema / provenance-less / smuggled-guess / non-decompressible)."""


def validate(cse: CSE, *, check_fidelity: bool = True) -> tuple:
    """Fail-closed CSE validator. Returns (ok, errors). Implements CTO S3 rules 1-6."""
    errors: list = []

    # S3.1 schema_version known
    if cse.schema_version != SCHEMA_VERSION:
        errors.append(f"schema_version {cse.schema_version!r} != {SCHEMA_VERSION!r} (unknown algebra version)")

    # S3.2 every verb / entity-type / relationship-type IN the enum (reject, not coerce)
    tr = cse.transformation or {}
    verb = tr.get("verb")
    if verb not in _VERB_VALUES:
        errors.append(f"transformation.verb {verb!r} off-enum (reject-not-coerce)")
    subj = tr.get("subject")
    subj_etype = subj.etype if isinstance(subj, EntityRef) else (subj or {}).get("etype")
    if subj_etype not in _ENTITY_VALUES:
        errors.append(f"transformation.subject.etype {subj_etype!r} off-enum")
    for i, edge in enumerate(tr.get("edges", []) or []):
        rtype = edge.rtype if isinstance(edge, RelationshipDelta) else (edge or {}).get("rtype")
        if rtype not in _REL_VALUES:
            errors.append(f"transformation.edges[{i}].rtype {rtype!r} off-enum")

    # producer.kind on-enum + head.marker_head present (AC6)
    if (cse.producer or {}).get("kind") not in _PRODUCER_VALUES:
        errors.append(f"producer.kind {(cse.producer or {}).get('kind')!r} off-enum")
    if not str((cse.head or {}).get("marker_head", "") or "").strip():
        errors.append("head.marker_head MISSING -- a CSE must pin the GLOBGRPH marker-HEAD at emission (AC6)")

    # S3.3 provenance present AND evidence non-empty
    p = cse.provenance
    if p is None or not str(getattr(p, "evidence", "") or "").strip():
        errors.append("provenance.evidence MISSING/blank -- provenance-less CSE INVALID (LAW 2, fail-closed)")
    if p is not None:
        for fld in ("source", "locus", "recognizer"):
            if not str(getattr(p, fld, "") or "").strip():
                errors.append(f"provenance.{fld} MISSING (full lexical chain required)")

    # S3.4 qualifiers.confidence present + a float in [0,1]
    quals = cse.qualifiers or {}
    for k in quals:
        if k not in _QUAL_VALUES:
            errors.append(f"qualifier key {k!r} off-schema")
    conf = quals.get(Qualifier.CONFIDENCE.value)
    conf_ok = isinstance(conf, (int, float)) and not isinstance(conf, bool) and 0.0 <= float(conf) <= 1.0
    if conf is None:
        errors.append("qualifiers.confidence MISSING (mandatory, CTO S3.4)")
    elif not conf_ok:
        errors.append(f"qualifiers.confidence {conf!r} not a float in [0,1]")

    # S3.5 untypable -> honest-low, never a guess: Concept subject requires confidence in the low band
    if subj_etype == Entity.CONCEPT.value:
        if not (conf_ok and float(conf) <= LOW_CONFIDENCE_MAX):
            errors.append(f"subject.etype=Concept(untyped) requires confidence<={LOW_CONFIDENCE_MAX} "
                          f"(honest-low degrade); an inferred type on a low subject is the GraphRAG "
                          f"failure this validator blocks (LAW 1)")

    # S3.6 fidelity: the CSE must decompress to C0 lexical evidence (comp_ladder), else invalid
    if check_fidelity and (p is not None and str(getattr(p, "evidence", "") or "").strip()):
        fok, ffail = fidelity_check(to_ladder_node(cse))
        if not fok:
            errors.append("fidelity FAIL (non-decompressible / latent): " + "; ".join(ffail))

    return (len(errors) == 0, errors)


def validate_or_raise(cse: CSE) -> None:
    ok, errors = validate(cse)
    if not ok:
        raise CSEValidationError("; ".join(errors))


# ===========================================================================
# AC5  FIDELITY BINDING -- a CSE -> comp_ladder C0 node (decompresses to lexical evidence)
# ===========================================================================
def to_ladder_node(cse: CSE) -> LadderNode:
    p = cse.provenance
    tr = cse.transformation or {}
    subj = tr.get("subject")
    subj_ref = subj.ref if isinstance(subj, EntityRef) else (subj or {}).get("ref", "")
    return LadderNode(
        nid=f"cse:{cse.event_id}", layer="C0", ntype=f"CSE.{tr.get('verb', '?')}",
        label=f"{tr.get('verb', '?')}({subj_ref})",
        provenance={"source": p.source, "locus": p.locus, "evidence": f"[{p.recognizer}] {p.evidence}"},
    )


def cse_fidelity_ok(cse: CSE) -> tuple:
    return fidelity_check(to_ladder_node(cse))


# ===========================================================================
# S5  COMPUNIFY COVERAGE-SWEEP WIRE (AC1) + AC4 PARITY CHECK (scaffold)
# ===========================================================================
def coverage_sweep(observed_node_types: set, observed_edge_types: set) -> tuple:
    """AC1/AC3 coverage: every observed CloudNode/CloudEdge type must reconcile into the algebra
    (fail-closed, mirrors derive_runner NODE_TYPE_LAYER_GAP + reuses COMPUNIFY's one-home coverage
    discipline). Returns (ok, unmapped_node_types, unmapped_edge_types). A gap is a tracked
    coverage-gap CSE candidate (S5), never a silent skip.

    NOTE (RAVC): the live COMPUNIFY coverage-check wire (invoke its machine-checked instrument
    rather than this local set-diff) is the AC1 antecedent -- flagged as the one external wire to
    confirm with CTO/COMPUNIFY owner; this local check is the deterministic fallback.
    """
    un_n = sorted(t for t in observed_node_types if t not in CLOUDNODE_TYPE_TO_ENTITY)
    un_e = sorted(t for t in observed_edge_types if t not in CLOUDEDGE_TO_RELATIONSHIP)
    return (not un_n and not un_e, un_n, un_e)


def parity_check(cloudnodes: list, cloudedges: list) -> tuple:
    """AC4 parity SCAFFOLD: re-materializing the mapped code CSEs must reproduce the current
    CloudNode/CloudEdge graph. Given the live graph's (nid, node_type) + (src, etype, dst) lists,
    map each into the algebra and assert every node/edge reconciles (round-trip coverage). Returns
    (ok, node_gaps, edge_gaps).

    NOTE (RAVC): full AC4 parity = re-materialize mapped CSEs and structurally diff vs the live
    Kuzu graph -- needs a graph EXPORT (consult DS~A/0.8.0 per the TO consult-path). This scaffold
    proves the MAPPING is total over a provided node/edge slice (the necessary precondition);
    the structural round-trip diff is the P2 materializer's cert (CVO AC4 exercise).
    """
    node_gaps = [(nid, nt) for (nid, nt) in cloudnodes if map_cloudnode(nid, nt) is None]
    edge_gaps = [(s, et, d) for (s, et, d) in cloudedges if et not in CLOUDEDGE_TO_RELATIONSHIP]
    return (not node_gaps and not edge_gaps, node_gaps, edge_gaps)


# ===========================================================================
# S6  STORE INTERFACE (AC2/AC6 -- folded from 0.5.0_AE consult 28cf707f9)
# ===========================================================================
CSE_TABLE = "cse"
PARTITION_COLUMNS = ("source", "event_date")   # source=producer.kind, event_date=execution ts date
ONE_MARKER_COMMIT = True     # append CSE + materialize C1 in ONE Nessie commit -> C0/C1 one-marker
FIRM_SCOPE_VIA = Qualifier.SCOPE.value          # firm-scoping is a row qualifier, never bucket-routing
CONTRACT_ID = f"nfra_cse@{SCHEMA_VERSION}"       # register into the existing graph_contracts registry
RETENTION_NOTE = "append-only C0 provenance stream -- retention DECISION open (>13mo SOC2 default?), RAVC CTO"
COMPACTION_ENROLL = "join the 02:00Z Iceberg maintenance (AE constraint #4) -- P2 writer, not write-and-forget"


def partition_key(cse: CSE) -> dict:
    ts = str((cse.execution_meta or {}).get("timestamp", ""))
    return {"source": (cse.producer or {}).get("kind", ""), "event_date": ts[:10]}
