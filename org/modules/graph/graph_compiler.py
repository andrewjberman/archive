"""
Corpus semantic graph compiler — three-tier entity intelligence.

Mirrors system/os/cli/compile.py architecture applied to the research corpus
(s3://corporeal-agg/json) instead of codebases.

Tier 1 (pt1): Per-entity compile — static x-ray of a single entity.
  Phase 1 (Inventory):  Load dossier JSON files for the entity
  Phase 2 (Extraction): Per-filetype extractors emit typed edges + condition nodes
  Phase 3 (Expansion):  Optionally compile neighbors to N hops
  → compile_entity_graph()

Tier 2 (pt2): Cross-entity compile — like compile_structural_graph_cross().
  Merge multiple entity inventories into a unified graph. Resolve cross-entity
  edges: shared agencies, shared contracts, shared sectors, bidirectional
  supply chains. Answers "how are these N entities connected?"
  → compile_entity_graph_cross()

Tier 3 (pt3): Temporal diff — like diff_graphs() + baselines.
  Compare entity graphs across time using snapshots + monthly data.
  Detect edge additions/removals, relationship shifts, concentration changes.
  → diff_entity_graphs(), save/load snapshots

Two rail systems:

  CONTRACT RAILS — observed relationships (entity↔entity via work):
    supply_chain        — contractor→contractor via sub/prime relationship
    award_recipient     — contractor→agency (aggregate relationship-level)
    award_binding       — contractor→agency (per-award, carries contract attrs)

  CLOUD RAILS — computed similarity (entity→cloud hub→entity):
    cloud_naics         — entity→cloud:naics:{code} (industry cluster)
    cloud_psc           — entity→cloud:psc:{code} (product/service cluster)
    cloud_geo           — entity→cloud:geo:{state} (geographic cluster)
    cloud_fingerprint   — entity→cloud:fp:{cloudId} (behavioral fingerprint cluster)
    cloud_market        — entity→cloud:naics:{code} (market position within sector)

  CROSS-ENTITY (pt2):
    shared_agency       — entity↔entity via common agency awards
    shared_contract     — entity↔entity via same parent_award_id
    shared_cloud        — entity↔entity via same cloud hub

Condition nodes:
  clearance, set_aside, small_business, defense_orientation, performance_status

Design rules:
  1. Entities are nodes, contracts are edges. (PRINCIPAL directive, 2026-03-29)
  2. Cloud hubs are keyed cluster nodes. Two entities in the same cloud share
     a hub — traverse entity→hub→entity. Cloud key determines the dimension.
"""

import hashlib
import json as _json
import gzip
import logging
import os
import time
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)

COMPILER_VERSION = "corpus-graph-v2"


# ── Edge + Node Types ───────────────────────────────────────────────

EDGE_CLASSES = {
    # Contract rails — observed relationships (entity↔entity via work)
    "supply_chain":        "contract",
    "award_recipient":     "contract",
    "award_binding":       "contract",
    # Cloud rails — computed similarity (entity→cloud hub)
    "cloud_naics":         "cloud",
    "cloud_psc":           "cloud",
    "cloud_geo":           "cloud",
    "cloud_fingerprint":   "cloud",
    "cloud_market":        "cloud",
    # pt2: cross-entity edges (resolved during cross-compilation)
    "shared_agency":       "cross_entity",
    "shared_contract":     "cross_entity",
    "shared_cloud":        "cross_entity",
}


def _edge(edge_type: str, source: str, target: str, **attrs) -> dict:
    return {
        "type": edge_type,
        "class": EDGE_CLASSES[edge_type],
        "source": source,
        "target": target,
        **attrs,
    }


def _node(node_type: str, node_id: str, label: str, **attrs) -> dict:
    return {
        "id": node_id,
        "type": node_type,
        "label": label,
        **attrs,
    }


def _cond(cond_type: str, cond_id: str, label: str, **attrs) -> dict:
    return {
        "id": cond_id,
        "type": "condition",
        "subtype": cond_type,
        "label": label,
        **attrs,
    }


# ── Phase 2: Per-Filetype Extractors ───────────────────────────────

def _extract_identity(uei: str, doc: dict) -> tuple[list, list, list]:
    """Extract entity node, cloud hub edges, and condition nodes from identity.json."""
    nodes = []
    edges = []
    conds = []

    data = doc.get("data", {})

    # Parse keyword/spectrum blobs for entity attributes
    keywords_raw = data.get("keywordsBlob")
    keywords_parsed = None
    if keywords_raw and isinstance(keywords_raw, str):
        try:
            keywords_parsed = _json.loads(keywords_raw)
        except Exception:
            pass

    spectrum_raw = data.get("spectrumBlob")
    spectrum_parsed = None
    if spectrum_raw and isinstance(spectrum_raw, str):
        try:
            spectrum_parsed = _json.loads(spectrum_raw)
        except Exception:
            pass

    # Entity node (root) — carries keyword/spectrum as attributes for pt2 similarity
    entity_attrs = dict(
        name=data.get("contractorName"),
        city=data.get("contractorCity"),
        state=data.get("contractorState"),
        state_name=data.get("contractorStateName"),
        country=data.get("contractorCountry"),
        revenue_ttm_m=data.get("revenueTtmMillions"),
        pipeline_active_m=data.get("pipelineActiveMillions"),
        obligations_ttm_m=data.get("obligationsTtmMillions"),
        awards_active=data.get("awardsActiveCount"),
        awards_lifetime=data.get("awardsLifetimeCount"),
        composite_score=data.get("compositeScore"),
        performance_tier=data.get("performanceTier"),
        classification_lifetime=data.get("entityClassificationLifetime"),
        classification_active=data.get("entityClassificationActive"),
        fingerprint=data.get("fingerprintString"),
        fingerprint_entropy=data.get("fingerprintEntropyScore"),
        cloud_id=data.get("cloudId"),
    )
    if keywords_parsed:
        top_kw = sorted(keywords_parsed.get("keywords", []),
                        key=lambda k: k.get("frequency", 0), reverse=True)[:20]
        entity_attrs["keywords_top20"] = [k["keyword"] for k in top_kw]
        entity_attrs["keywords_unique_count"] = (
            _json.loads(data.get("keywordsMetadata", "{}")).get("unique_keywords")
            if data.get("keywordsMetadata") else None)
    if spectrum_parsed:
        entity_attrs["spectrum"] = {
            s["label"]: s["coordinate"]
            for s in spectrum_parsed.get("spectrum", [])
        }

    nodes.append(_node("entity", uei,
                        label=data.get("contractorName", uei), **entity_attrs))

    # ── Cloud rails ──────────────────────────────────────────────

    # Cloud: NAICS
    naics = data.get("primaryNaicsCode")
    naics_desc = data.get("primaryNaicsDescription")
    if naics:
        hub_id = f"cloud:naics:{naics}"
        nodes.append(_node("cloud_hub", hub_id, label=naics_desc or naics,
                           cloud_key="naics", naics_code=naics,
                           naics_description=naics_desc))
        edges.append(_edge("cloud_naics", uei, hub_id,
                           naics_code=naics, naics_description=naics_desc))

    # Cloud: PSC (Product/Service Code)
    psc = data.get("primaryPscCode")
    psc_desc = data.get("primaryPscDescription")
    if psc:
        hub_id = f"cloud:psc:{psc}"
        nodes.append(_node("cloud_hub", hub_id, label=psc_desc or psc,
                           cloud_key="psc", psc_code=psc,
                           psc_description=psc_desc))
        edges.append(_edge("cloud_psc", uei, hub_id,
                           psc_code=psc, psc_description=psc_desc))

    # Cloud: Geographic
    state = data.get("contractorState")
    if state:
        hub_id = f"cloud:geo:{state}"
        nodes.append(_node("cloud_hub", hub_id,
                           label=data.get("contractorStateName", state),
                           cloud_key="geo", state_code=state))
        edges.append(_edge("cloud_geo", uei, hub_id,
                           city=data.get("contractorCity"), state=state))

    # Cloud: Fingerprint (pre-computed cluster from ETL)
    cloud_id = data.get("cloudId")
    if cloud_id:
        hub_id = f"cloud:fp:{cloud_id}"
        nodes.append(_node("cloud_hub", hub_id,
                           label=f"{cloud_id} ({data.get('cloudMemberCount', '?')} members)",
                           cloud_key="fingerprint",
                           cloud_status=data.get("cloudStatus"),
                           member_count=data.get("cloudMemberCount"),
                           similarity_estimate=data.get("cloudSimilarityEstimate")))
        edges.append(_edge("cloud_fingerprint", uei, hub_id,
                           fingerprint=data.get("fingerprintString"),
                           entropy=data.get("fingerprintEntropyScore"),
                           keyword_count=data.get("fingerprintKeywordCount"),
                           similarity=data.get("cloudSimilarityEstimate")))

    # Condition nodes — Bug 4 fix: check multiple small business indicators
    is_sb = data.get("smallBusinessIndicator")
    sb_classification = data.get("entityClassificationActive", "")
    if is_sb or (sb_classification and "small" in sb_classification.lower()):
        conds.append(_cond("small_business", f"cond:sb:{uei}",
                           f"{data.get('contractorName', uei)} is small business",
                           classification=sb_classification))

    # Set-aside eligibility (8(a), HUBZone, WOSB, SDVOSB, etc.)
    set_aside = data.get("predominantSetAsideType") or data.get("setAsideType")
    if set_aside and set_aside.upper() not in ("NONE", "NO SET ASIDE USED", ""):
        conds.append(_cond("set_aside", f"cond:sa:{uei}",
                           f"Set-aside: {set_aside}",
                           set_aside_type=set_aside))

    defense_pct = data.get("defenseActivePercent") or 0
    if defense_pct > 50:
        conds.append(_cond("defense_orientation", f"cond:def:{uei}",
                           f"{defense_pct:.0f}% defense",
                           defense_active_pct=defense_pct,
                           defense_lifetime_pct=data.get("defenseLifetimePercent")))

    # Only flag non-performing if isPerforming is False AND no active awards.
    # isPerforming can be wrong for pure subs (ETL only checks prime contracts).
    is_performing_flag = data.get("isPerforming")
    active_awards = data.get("awardsActiveCount") or 0
    if is_performing_flag is False and active_awards == 0:
        conds.append(_cond("performance_status", f"cond:perf:{uei}",
                           "not currently performing"))

    return nodes, edges, conds


def _extract_network(uei: str, doc: dict) -> tuple[list, list, list]:
    """Extract supply chain edges from network.json.

    Bug 1 fix: Only produce supply_chain for CONTRACTOR↔CONTRACTOR.
    Agency relationships are skipped — activity.json covers them better.
    Bug 3 fix: Check relationshipEntityType to set correct node type.
    """
    nodes = []
    edges = []
    conds = []

    relationships = doc.get("relationships", [])

    for rel in relationships:
        # Determine the "other" entity.
        # For perspective-flipped records, the subject is already the root entity
        # (our UEI) and the relationship entity is the "other" (the prime).
        # The flip just means the row was originally from the prime's perspective.
        other_uei = rel.get("relationshipEntityUei")
        other_name = rel.get("relationshipEntityName")

        if not other_uei or other_uei == uei:
            continue

        # Determine entity type — Bug 1 + Bug 3 fix
        entity_type = (rel.get("relationshipEntityType", "")
                       or rel.get("networkEdgeType", "")).upper()

        is_agency = "AGENCY" in entity_type

        # Skip agency relationships from network.json — activity.json
        # covers agency→contractor edges with richer award-level detail
        if is_agency:
            continue

        # Other entity node (contractor)
        city = rel.get("relationshipEntityHqCity")
        state = rel.get("relationshipEntityHqState")

        nodes.append(_node(
            "entity", other_uei,
            label=other_name or other_uei,
            name=other_name,
            city=city,
            state=state,
        ))

        direction = rel.get("flowDirection", "").upper()

        edges.append(_edge(
            "supply_chain", uei, other_uei,
            direction=direction,
            active_obligations=rel.get("activeObligationsValue"),
            active_obligations_count=rel.get("activeObligationsCount"),
            lifetime_obligations=rel.get("lifetimeObligationsValue"),
            lifetime_obligations_count=rel.get("lifetimeObligationsCount"),
            active_awards=rel.get("activeAwardsCount"),
            lifetime_awards=rel.get("lifetimeAwardsCount"),
            status=rel.get("relationshipStatus"),
            award_types=rel.get("awardTypes"),
            primary_naics=rel.get("primaryNaicsCode"),
            performance_start=rel.get("performanceStartDate"),
            performance_end=rel.get("performanceEndDate"),
        ))

    return nodes, edges, conds


def _extract_peers(uei: str, doc: dict) -> tuple[list, list, list]:
    """Extract competitive peer edges from peers.json.

    Peers are identified by shared peer group — the entity's cloud cluster.
    The peer file gives the entity's position; actual peer entities come from
    corpus.get_peer_group() if available. For now, extract the entity's peer
    metadata as condition nodes (positioning within its competitive set).
    """
    nodes = []
    edges = []
    conds = []

    data = doc.get("data", {})

    cloud_tier = data.get("cloudPerformanceTier")
    cloud_rank = data.get("cloudCompositeRank")
    cloud_size = data.get("cloudGroupSize")
    demo_tier = data.get("demographicPerformanceTier")

    if cloud_tier:
        conds.append(_cond("peer_position", f"cond:peer:{uei}",
                           f"Cloud: {cloud_tier} (#{cloud_rank}/{cloud_size}), "
                           f"Demographic: {demo_tier}",
                           cloud_tier=cloud_tier,
                           cloud_rank=cloud_rank,
                           cloud_group_size=cloud_size,
                           cloud_composite=data.get("cloudCompositeScore"),
                           demographic_tier=demo_tier,
                           demographic_rank=data.get("demographicCompositeRank"),
                           demographic_group_size=data.get("demographicGroupSize"),
                           demographic_composite=data.get("demographicCompositeScore")))

    return nodes, edges, conds


def _extract_activity(uei: str, doc: dict) -> tuple[list, list, list]:
    """Extract award/agency edges from activity.json (structured format).

    Design: contracts are edges, not nodes. Each award produces an
    award_binding edge from contractor→agency carrying all contract
    attributes. (PRINCIPAL directive, 2026-03-29)

    Bug 2 fix: Read totalPrimeObligations/contractorObligations, not totalObligations.
    """
    nodes = []
    edges = []
    conds = []

    def _process_flow_group(flow_entities: list, flow_dir: str):
        for entity in flow_entities:
            other_uei = entity.get("entityUei")
            other_name = entity.get("entityName")
            rel_type = entity.get("relationshipType", "unknown")

            if not other_uei:
                continue

            # Agency or entity node
            node_type = "agency" if rel_type == "agency" else "entity"
            nodes.append(_node(node_type, other_uei,
                               label=other_name or other_uei,
                               name=other_name))

            metrics = entity.get("metrics", {})

            # Bug 2 fix: use correct obligation fields
            prime_obligations = metrics.get("totalPrimeObligations")
            contractor_obligations = metrics.get("contractorObligations")
            total_award_value = metrics.get("totalAwardValue")

            # Top-level award_recipient edge (aggregate relationship)
            edges.append(_edge(
                "award_recipient", uei, other_uei,
                direction=flow_dir,
                relationship_type=rel_type,
                total_award_value=total_award_value,
                total_prime_obligations=prime_obligations,
                contractor_obligations=contractor_obligations,
                utilization_pct=metrics.get("utilization"),
                award_count=metrics.get("awardCount"),
                active_award_count=metrics.get("activeAwardCount"),
                has_active=entity.get("hasActiveAwards"),
                latest_action=entity.get("latestActionDate"),
                earliest_action=entity.get("earliestActionDate"),
                naics_codes=entity.get("naicsCodes"),
            ))

            # Per-award: award_binding edges (contract = edge, not node)
            for award in entity.get("awards", []):
                edges.append(_edge(
                    "award_binding", uei, other_uei,
                    direction=flow_dir,
                    parent_award_id=award.get("parentAwardId"),
                    contract_number=award.get("contractNumber"),
                    total_obligations=award.get("totalObligations"),
                    parent_award_value=award.get("parentAwardValue"),
                    cumulative_obligated=award.get("cumulativeObligated"),
                    event_count=award.get("eventCount"),
                    is_active=award.get("isActive"),
                    is_defense=award.get("isDefenseFlow"),
                    naics=award.get("naicsCode"),
                    naics_desc=award.get("naicsDescription"),
                    psc=award.get("pscCode"),
                    psc_desc=award.get("pscDescription"),
                    set_aside=award.get("setAsideType"),
                    competition=award.get("competitionType"),
                    pricing=award.get("contractPricingType"),
                    performance_start=award.get("performanceStartDate"),
                    performance_end=award.get("performanceEndDate"),
                    latest_action=award.get("latestActionDate"),
                    flow_type=award.get("flowType"),
                    flow_subtype=award.get("flowSubtype"),
                ))

    # Process inflows
    inflows = doc.get("inflows", {})
    _process_flow_group(inflows.get("agencies", []), "INFLOW")
    _process_flow_group(inflows.get("primes", []), "INFLOW")

    # Process outflows
    outflows = doc.get("outflows", {})
    _process_flow_group(outflows.get("subcontractors", []), "OUTFLOW")

    return nodes, edges, conds


def _extract_discovery(uei: str, doc: dict) -> tuple[list, list, list]:
    """Extract market position signal from discovery.json.

    Emits a cloud_market edge to the NAICS cloud hub (same hub as cloud_naics).
    This edge carries market position metrics — the entity's rank/share within
    its industry cluster.
    """
    nodes = []
    edges = []
    conds = []

    data = doc.get("data", {})

    naics = data.get("primaryNaicsCode")
    if naics:
        edges.append(_edge(
            "cloud_market", uei, f"cloud:naics:{naics}",
            revenue_ttm_m=data.get("revenueTtmMillions"),
            pipeline_active_m=data.get("pipelineActiveMillions"),
            obligations_lifetime=data.get("obligationsLifetime"),
            obligations_1yr=data.get("obligations1Year"),
            obligations_90d=data.get("obligations90Day"),
            revenue_growth_yoy=data.get("revenueGrowthYoy"),
            defense_lifetime_pct=data.get("defenseLifetimePercent"),
            classification=data.get("entityClassificationLifetime"),
        ))

    return nodes, edges, conds


# ── Phase 1: Inventory ─────────────────────────────────────────────

_FILE_KEYS = ["identity", "network", "peers", "activity", "discovery"]

_EXTRACTORS = {
    "identity":  _extract_identity,
    "network":   _extract_network,
    "peers":     _extract_peers,
    "activity":  _extract_activity,
    "discovery": _extract_discovery,
}


# ── Compile ────────────────────────────────────────────────────────

def compile_entity_graph(
    uei: str,
    fetch_fn,
    hops: int = 1,
    _visited: Optional[set] = None,
) -> dict:
    """Compile a semantic graph centered on a single entity.

    Args:
        uei:      Contractor UEI to compile.
        fetch_fn: Callable(uei, file_key) -> dict|None. Wraps corpus.json_fetch
                  or any other data source.
        hops:     Number of hops to expand. 1 = root entity only.
                  2 = root + immediate neighbors. etc.
        _visited: Internal — tracks already-compiled entities to prevent cycles.

    Returns:
        dict with keys: root, nodes, edges, condition_nodes, meta
    """
    if _visited is None:
        _visited = set()

    _visited.add(uei)

    all_nodes = []
    all_edges = []
    all_conds = []
    files_loaded = []

    # Phase 1: Load dossier files
    docs = {}
    for key in _FILE_KEYS:
        doc = fetch_fn(uei, key)
        if doc is not None:
            docs[key] = doc
            files_loaded.append(key)

    if not docs:
        return {
            "root": uei,
            "nodes": [],
            "edges": [],
            "condition_nodes": [],
            "meta": {"hops": 0, "files_loaded": [], "entities_compiled": [uei],
                     "error": "no dossier data found"},
        }

    # Phase 2: Extract edges from each file
    for key, doc in docs.items():
        extractor = _EXTRACTORS.get(key)
        if extractor:
            nodes, edges, conds = extractor(uei, doc)
            all_nodes.extend(nodes)
            all_edges.extend(edges)
            all_conds.extend(conds)

    # Deduplicate nodes by id (keep first seen — root entity's own data wins)
    seen_ids = set()
    deduped_nodes = []
    for node in all_nodes:
        if node["id"] not in seen_ids:
            seen_ids.add(node["id"])
            deduped_nodes.append(node)

    # Phase 3: Hop expansion
    entities_compiled = [uei]
    if hops > 1:
        # Find neighbor entity UEIs from edges
        neighbor_ueis = set()
        for edge in all_edges:
            for endpoint in (edge["source"], edge["target"]):
                if (endpoint not in _visited
                        and not endpoint.startswith(("cloud:", "cond:"))):
                    neighbor_ueis.add(endpoint)

        for neighbor_uei in neighbor_ueis:
            sub = compile_entity_graph(
                neighbor_uei, fetch_fn,
                hops=hops - 1,
                _visited=_visited,
            )
            # Merge sub-graph
            for node in sub["nodes"]:
                if node["id"] not in seen_ids:
                    seen_ids.add(node["id"])
                    deduped_nodes.append(node)
            all_edges.extend(sub["edges"])
            all_conds.extend(sub["condition_nodes"])
            entities_compiled.extend(sub["meta"]["entities_compiled"])

    # Summary
    edge_type_counts = {}
    for e in all_edges:
        edge_type_counts[e["type"]] = edge_type_counts.get(e["type"], 0) + 1

    node_type_counts = {}
    for n in deduped_nodes:
        node_type_counts[n["type"]] = node_type_counts.get(n["type"], 0) + 1

    return {
        "root": uei,
        "nodes": deduped_nodes,
        "edges": all_edges,
        "condition_nodes": all_conds,
        "meta": {
            "hops": hops,
            "files_loaded": files_loaded,
            "entities_compiled": entities_compiled,
            "summary": {
                "total_nodes": len(deduped_nodes),
                "total_edges": len(all_edges),
                "total_conditions": len(all_conds),
                "by_edge_type": edge_type_counts,
                "by_node_type": node_type_counts,
            },
        },
    }


# ── Temporal Edge Activity ─────────────────────────────────────────
#
# The graph stores all edges (active and inactive) with temporal data.
# Active/inactive is computed at query time via as_of, not at compile time.
# This keeps the cache valid indefinitely and leaves the time-machine
# backdoor open — pass a past date to see what was active then.

_CONTRACT_EDGE_TYPES = {"supply_chain", "award_recipient", "award_binding"}


def _is_edge_active(edge: dict, as_of: str) -> bool:
    """Determine if a contract edge is active as of a given date (YYYY-MM-DD).

    Rules:
    - award_binding: performance_end >= as_of
    - supply_chain: active_obligations > 0 (no date available)
    - award_recipient: has_active flag OR active_award_count > 0
    - cloud/cross edges: always considered active (not temporal)
    """
    etype = edge.get("type", "")

    if etype not in _CONTRACT_EDGE_TYPES:
        return True  # cloud and cross-entity edges are not temporal

    if etype == "award_binding":
        end = edge.get("performance_end")
        if end:
            return end >= as_of
        return edge.get("is_active", False)

    if etype == "supply_chain":
        return (edge.get("active_obligations") or 0) > 0

    if etype == "award_recipient":
        return (edge.get("has_active") is True
                or (edge.get("active_award_count") or 0) > 0)

    return True


def _today() -> str:
    return time.strftime("%Y-%m-%d", time.gmtime())


def active_edges(graph: dict, as_of: Optional[str] = None) -> list[dict]:
    """Return only active edges from a graph as of a date. Default: today."""
    d = as_of or _today()
    return [e for e in graph["edges"] if _is_edge_active(e, d)]


def active_subgraph(graph: dict, as_of: Optional[str] = None) -> dict:
    """Return a copy of the graph containing only active edges and their nodes.

    This is the primary view for the frontend — the "live" graph.
    """
    d = as_of or _today()
    live_edges = [e for e in graph["edges"] if _is_edge_active(e, d)]

    # Collect node IDs referenced by live edges
    live_node_ids = set()
    for e in live_edges:
        live_node_ids.add(e["source"])
        live_node_ids.add(e["target"])

    # Always include root
    root = graph.get("root")
    if root:
        live_node_ids.add(root)

    live_nodes = [n for n in graph["nodes"] if n["id"] in live_node_ids]
    live_conds = [c for c in graph.get("condition_nodes", [])
                  if any(nid in c["id"] for nid in live_node_ids)]

    edge_type_counts = {}
    for e in live_edges:
        edge_type_counts[e["type"]] = edge_type_counts.get(e["type"], 0) + 1

    node_type_counts = {}
    for n in live_nodes:
        node_type_counts[n["type"]] = node_type_counts.get(n["type"], 0) + 1

    return {
        "root": root,
        "roots": graph.get("roots"),
        "nodes": live_nodes,
        "edges": live_edges,
        "condition_nodes": live_conds,
        "meta": {
            **graph.get("meta", {}),
            "view": "active",
            "as_of": d,
            "summary": {
                "total_nodes": len(live_nodes),
                "total_edges": len(live_edges),
                "total_conditions": len(live_conds),
                "by_edge_type": edge_type_counts,
                "by_node_type": node_type_counts,
            },
        },
    }


# ── Graph Query Helpers ────────────────────────────────────────────
# All traversal functions accept active_only (default True) and as_of.
# Frontend default: active_only=True, as_of=today → live graph.
# Time machine: active_only=True, as_of="2024-06-01" → historical view.
# Full graph: active_only=False → all edges regardless of time.

def neighbors(graph: dict, node_id: str, edge_type: Optional[str] = None,
              direction: Optional[str] = None,
              active_only: bool = True, as_of: Optional[str] = None) -> list[dict]:
    """Find all neighbors of a node, optionally filtered by edge type and activity."""
    d = as_of or _today()
    results = []
    node_index = {n["id"]: n for n in graph["nodes"]}

    for edge in graph["edges"]:
        if edge_type and edge["type"] != edge_type:
            continue
        if active_only and not _is_edge_active(edge, d):
            continue

        neighbor_id = None
        edge_dir = edge.get("direction")

        if edge["source"] == node_id:
            neighbor_id = edge["target"]
        elif edge["target"] == node_id:
            neighbor_id = edge["source"]

        if neighbor_id is None:
            continue

        if direction and edge_dir and edge_dir != direction:
            continue

        neighbor_node = node_index.get(neighbor_id)
        results.append({
            "node": neighbor_node or {"id": neighbor_id, "type": "unknown", "label": neighbor_id},
            "edge": edge,
        })

    return results


def subgraph(graph: dict, node_id: str, edge_types: Optional[list] = None,
             max_depth: int = 2,
             active_only: bool = True, as_of: Optional[str] = None) -> dict:
    """Extract a subgraph reachable from node_id within max_depth hops."""
    d = as_of or _today()
    visited = set()
    frontier = {node_id}
    collected_nodes = set()
    collected_edges = []

    node_index = {n["id"]: n for n in graph["nodes"]}

    for _ in range(max_depth):
        next_frontier = set()
        for nid in frontier:
            if nid in visited:
                continue
            visited.add(nid)
            collected_nodes.add(nid)

            for edge in graph["edges"]:
                if edge_types and edge["type"] not in edge_types:
                    continue
                if active_only and not _is_edge_active(edge, d):
                    continue

                other = None
                if edge["source"] == nid:
                    other = edge["target"]
                elif edge["target"] == nid:
                    other = edge["source"]

                if other is not None:
                    collected_edges.append(edge)
                    collected_nodes.add(other)
                    if other not in visited:
                        next_frontier.add(other)

        frontier = next_frontier

    return {
        "root": node_id,
        "nodes": [node_index[nid] for nid in collected_nodes if nid in node_index],
        "edges": collected_edges,
        "condition_nodes": [c for c in graph.get("condition_nodes", [])
                           if any(nid in c["id"] for nid in collected_nodes)],
        "meta": {"view": "active" if active_only else "full", "as_of": d},
    }


def find_path(graph: dict, source_id: str, target_id: str,
              max_depth: int = 5,
              active_only: bool = True, as_of: Optional[str] = None) -> Optional[list[dict]]:
    """BFS shortest path between two nodes. Returns list of edges, or None."""
    from collections import deque
    d = as_of or _today()

    adjacency = {}
    for edge in graph["edges"]:
        if active_only and not _is_edge_active(edge, d):
            continue
        adjacency.setdefault(edge["source"], []).append(edge)
        adjacency.setdefault(edge["target"], []).append(edge)

    queue = deque([(source_id, [])])
    visited = {source_id}

    while queue:
        current, path = queue.popleft()
        if len(path) >= max_depth:
            continue

        for edge in adjacency.get(current, []):
            next_id = edge["target"] if edge["source"] == current else edge["source"]
            if next_id in visited:
                continue

            new_path = path + [edge]
            if next_id == target_id:
                return new_path

            visited.add(next_id)
            queue.append((next_id, new_path))

    return None


def blast_radius(graph: dict, node_id: str,
                 edge_types: Optional[list] = None,
                 active_only: bool = True, as_of: Optional[str] = None) -> dict:
    """Find all nodes downstream of node_id — what breaks if this node goes away.

    Follows edges where node_id is a source (outbound dependencies).
    Returns affected nodes grouped by depth.
    """
    from collections import deque
    d = as_of or _today()

    affected = {}  # depth -> list of nodes
    visited = {node_id}
    node_index = {n["id"]: n for n in graph["nodes"]}

    queue = deque([(node_id, 0)])

    while queue:
        current, depth = queue.popleft()

        for edge in graph["edges"]:
            if edge_types and edge["type"] not in edge_types:
                continue
            if active_only and not _is_edge_active(edge, d):
                continue

            # Follow source→target direction only
            if edge["source"] != current:
                continue

            target = edge["target"]
            if target in visited:
                continue

            visited.add(target)
            affected.setdefault(depth + 1, []).append({
                "node": node_index.get(target, {"id": target, "type": "unknown", "label": target}),
                "via_edge": edge,
            })
            queue.append((target, depth + 1))

    return {
        "source": node_id,
        "total_affected": sum(len(v) for v in affected.values()),
        "by_depth": affected,
    }


# ── Fingerprinting & Cache (mirrors planning/cache.py) ────────────

def _fingerprint_entity_data(docs: dict) -> str:
    """SHA256 fingerprint of an entity's raw dossier data.

    Mirrors fingerprint_structural_inventory() — content-based,
    not timestamp-based. Cache is valid until the underlying data changes
    (i.e., next ETL refresh writes new JSON to S3).
    """
    canonical = _json.dumps(docs, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()[:16]


def _scope_key_for_entity(uei: str) -> str:
    """Derive a cache scope key for an entity.

    Mirrors scope_key_for_working_directory() in planning/store.py.
    """
    digest = hashlib.sha256(uei.lower().encode()).hexdigest()[:12]
    return f"entity_{uei}--{digest}"


_DEFAULT_CACHE_DIR = Path(os.environ.get(
    "CORPUS_GRAPH_CACHE",
    os.path.expanduser("~/.corporeal/graph_cache"),
))


def _cache_path(uei: str, cache_dir: Optional[Path] = None) -> Path:
    d = cache_dir or _DEFAULT_CACHE_DIR
    return d / f"{_scope_key_for_entity(uei)}.json"


def load_cached_graph(uei: str, cache_dir: Optional[Path] = None) -> Optional[dict]:
    """Load a cached entity graph if it exists and version matches."""
    p = _cache_path(uei, cache_dir)
    if not p.exists():
        return None
    try:
        with open(p, encoding="utf-8") as f:
            cached = _json.load(f)
        if cached.get("_cache", {}).get("compiler_version") != COMPILER_VERSION:
            return None
        return cached
    except Exception:
        return None


def save_cached_graph(graph: dict, uei: str,
                      fingerprint: str, cache_dir: Optional[Path] = None) -> Path:
    """Save a compiled graph to cache with fingerprint receipt."""
    d = cache_dir or _DEFAULT_CACHE_DIR
    d.mkdir(parents=True, exist_ok=True)
    p = _cache_path(uei, d)

    graph["_cache"] = {
        "compiler_version": COMPILER_VERSION,
        "fingerprint": fingerprint,
        "scope_key": _scope_key_for_entity(uei),
        "cached_at": time.strftime("%Y-%m-%dT%H%M%SZ", time.gmtime()),
    }

    tmp = p.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        _json.dump(graph, f, indent=2, default=str)
    tmp.rename(p)
    return p


def compile_entity_graph_cached(
    uei: str,
    fetch_fn,
    hops: int = 1,
    cache_dir: Optional[Path] = None,
    force: bool = False,
) -> dict:
    """Compile with cache-hit detection mirroring architect_scan_node().

    1. Load raw docs → fingerprint
    2. Check cache → if fingerprint matches, return cached (no recompile)
    3. If miss, compile fresh → save to cache
    """
    t0 = time.monotonic()

    # Phase 1: Inventory (load raw docs for fingerprinting)
    docs = {}
    for key in _FILE_KEYS:
        doc = fetch_fn(uei, key)
        if doc is not None:
            docs[key] = doc

    fingerprint = _fingerprint_entity_data(docs)

    # Cache check
    if not force:
        cached = load_cached_graph(uei, cache_dir)
        if cached and cached.get("_cache", {}).get("fingerprint") == fingerprint:
            cached["meta"]["cache_status"] = "hit"
            cached["meta"]["timing"] = {"total_s": round(time.monotonic() - t0, 4)}
            return cached

    # Cache miss — full compile
    def _cached_fetch(u, k):
        if u == uei:
            return docs.get(k)
        return fetch_fn(u, k)

    graph = compile_entity_graph(uei, _cached_fetch, hops=hops)
    graph["meta"]["cache_status"] = "miss"
    graph["meta"]["timing"] = {"total_s": round(time.monotonic() - t0, 4)}

    save_cached_graph(graph, uei, fingerprint, cache_dir)
    return graph


# ── Tier 2: Cross-Entity Compilation ──────────────────────────────
#    Mirrors compile_structural_graph_cross() + merge_inventories()

def compile_entity_graph_cross(
    ueis: list[str],
    fetch_fn,
    cache_dir: Optional[Path] = None,
) -> dict:
    """Compile multiple entities into a unified graph with cross-entity edges.

    Mirrors compile_structural_graph_cross() — scans each entity independently,
    merges inventories, then runs cross-entity matchers to find shared agencies,
    shared contracts, shared sectors, and bidirectional supply chains.
    """
    t0 = time.monotonic()

    # Phase 1: Compile each entity (pt1 per entity, with caching)
    entity_graphs = {}
    for uei in ueis:
        entity_graphs[uei] = compile_entity_graph_cached(uei, fetch_fn, hops=1,
                                                          cache_dir=cache_dir)

    # Phase 2: Merge into unified graph
    all_nodes = []
    all_edges = []
    all_conds = []
    seen_ids = set()

    for uei, g in entity_graphs.items():
        for node in g.get("nodes", []):
            if node["id"] not in seen_ids:
                seen_ids.add(node["id"])
                all_nodes.append(node)
        all_edges.extend(g.get("edges", []))
        all_conds.extend(g.get("condition_nodes", []))

    # Phase 3: Cross-entity edge resolution
    cross_edges = _resolve_cross_entity_edges(ueis, all_nodes, all_edges)
    all_edges.extend(cross_edges)

    # Summary
    edge_type_counts = {}
    for e in all_edges:
        edge_type_counts[e["type"]] = edge_type_counts.get(e["type"], 0) + 1

    node_type_counts = {}
    for n in all_nodes:
        node_type_counts[n["type"]] = node_type_counts.get(n["type"], 0) + 1

    return {
        "roots": ueis,
        "mode": "cross_entity",
        "nodes": all_nodes,
        "edges": all_edges,
        "condition_nodes": all_conds,
        "meta": {
            "entities_compiled": ueis,
            "cross_edges_found": len(cross_edges),
            "summary": {
                "total_nodes": len(all_nodes),
                "total_edges": len(all_edges),
                "total_conditions": len(all_conds),
                "by_edge_type": edge_type_counts,
                "by_node_type": node_type_counts,
            },
            "timing": {"total_s": round(time.monotonic() - t0, 4)},
        },
    }


def _resolve_cross_entity_edges(
    root_ueis: list[str],
    nodes: list[dict],
    edges: list[dict],
) -> list[dict]:
    """Detect implicit relationships across compiled entities.

    Three cross-entity matchers:
    - shared_agency:  two+ entities receive awards from the same agency
    - shared_contract: two+ entities on the same contract vehicle (parent_award_id)
    - shared_cloud:   two+ entities connected to the same cloud hub (any key)
    """
    cross_edges = []
    root_set = set(root_ueis)

    # Index: agency_id → set of root entity UEIs that have award_recipient edges to it
    agency_to_entities: dict[str, set] = {}
    # Index: parent_award_id → set of root entity UEIs that have award_binding edges
    contract_to_entities: dict[str, set] = {}
    # Index: cloud_hub_id → set of root entity UEIs connected to that hub
    cloud_to_entities: dict[str, set] = {}

    cloud_edge_types = {"cloud_naics", "cloud_psc", "cloud_geo", "cloud_fingerprint", "cloud_market"}

    for edge in edges:
        src, tgt = edge["source"], edge["target"]

        if edge["type"] == "award_recipient" and src in root_set:
            agency_to_entities.setdefault(tgt, set()).add(src)

        elif edge["type"] == "award_binding" and src in root_set:
            parent_id = edge.get("parent_award_id")
            if parent_id:
                contract_to_entities.setdefault(parent_id, set()).add(src)

        elif edge["type"] in cloud_edge_types and src in root_set:
            cloud_to_entities.setdefault(tgt, set()).add(src)

    # Shared agency: two+ root entities receive awards from the same agency
    for agency_id, entities in agency_to_entities.items():
        if len(entities) < 2:
            continue
        entity_list = sorted(entities)
        for i in range(len(entity_list)):
            for j in range(i + 1, len(entity_list)):
                cross_edges.append(_edge(
                    "shared_agency", entity_list[i], entity_list[j],
                    via=agency_id,
                    agency_name=next((n["label"] for n in nodes if n["id"] == agency_id), agency_id),
                ))

    # Shared contract: two+ root entities on the same contract vehicle
    for parent_award_id, entities in contract_to_entities.items():
        if len(entities) < 2:
            continue
        entity_list = sorted(entities)
        for i in range(len(entity_list)):
            for j in range(i + 1, len(entity_list)):
                cross_edges.append(_edge(
                    "shared_contract", entity_list[i], entity_list[j],
                    via=parent_award_id,
                    parent_award_id=parent_award_id,
                ))

    # Shared cloud: two+ root entities connected to the same cloud hub
    node_index = {n["id"]: n for n in nodes}
    for hub_id, entities in cloud_to_entities.items():
        if len(entities) < 2:
            continue
        hub_node = node_index.get(hub_id, {})
        cloud_key = hub_node.get("cloud_key", hub_id.split(":")[1] if ":" in hub_id else "unknown")
        entity_list = sorted(entities)
        for i in range(len(entity_list)):
            for j in range(i + 1, len(entity_list)):
                cross_edges.append(_edge(
                    "shared_cloud", entity_list[i], entity_list[j],
                    via=hub_id,
                    cloud_key=cloud_key,
                    hub_label=hub_node.get("label", hub_id),
                ))

    return cross_edges


# ── Tier 3: Diff & Baseline (mirrors compile.py baselines) ────────

_DEFAULT_BASELINE_DIR = Path(os.environ.get(
    "CORPUS_GRAPH_BASELINES",
    os.path.expanduser("~/.corporeal/graph_baselines"),
))


def _edge_key(e: dict) -> str:
    """Stable identity for an edge. Mirrors compile.py _edge_key()."""
    return f"{e.get('source', '')}→{e.get('target', '')}:{e.get('type', '')}"


def _node_key(n: dict) -> str:
    return n.get("id", "")


def diff_entity_graphs(baseline: dict, current: dict) -> dict:
    """Compute structural diff between two entity graph compilations.

    Mirrors diff_graphs() in compile.py. Detects:
    - Nodes added/removed (new/lost relationships, agencies, contracts)
    - Edges added/removed (new/severed supply chains, awards)
    - Edge attribute changes (dollar value shifts, status changes)
    - Condition changes (gained/lost small business, defense orientation)
    """
    b_edges = {_edge_key(e): e for e in baseline.get("edges", [])}
    c_edges = {_edge_key(e): e for e in current.get("edges", [])}

    b_nodes = {_node_key(n): n for n in baseline.get("nodes", [])}
    c_nodes = {_node_key(n): n for n in current.get("nodes", [])}

    b_conds = {c["id"]: c for c in baseline.get("condition_nodes", [])}
    c_conds = {c["id"]: c for c in current.get("condition_nodes", [])}

    added_edges = [c_edges[k] for k in sorted(set(c_edges) - set(b_edges))]
    removed_edges = [b_edges[k] for k in sorted(set(b_edges) - set(c_edges))]

    added_nodes = [c_nodes[k] for k in sorted(set(c_nodes) - set(b_nodes))]
    removed_nodes = [b_nodes[k] for k in sorted(set(b_nodes) - set(c_nodes))]

    added_conds = [c_conds[k] for k in sorted(set(c_conds) - set(b_conds))]
    removed_conds = [b_conds[k] for k in sorted(set(b_conds) - set(c_conds))]

    # Detect value shifts on edges that exist in both
    value_shifts = []
    for key in set(b_edges) & set(c_edges):
        b_e, c_e = b_edges[key], c_edges[key]
        for attr in ("active_obligations", "total_award_value",
                     "lifetime_obligations", "active_awards",
                     "total_prime_obligations", "contractor_obligations",
                     "total_obligations", "cumulative_obligated"):
            b_val = b_e.get(attr)
            c_val = c_e.get(attr)
            if b_val is not None and c_val is not None and b_val != c_val:
                value_shifts.append({
                    "edge": key,
                    "attribute": attr,
                    "baseline": b_val,
                    "current": c_val,
                    "delta": c_val - b_val if isinstance(c_val, (int, float)) else None,
                })

    b_summary = baseline.get("meta", {}).get("summary", {})
    c_summary = current.get("meta", {}).get("summary", {})

    return {
        "nodes_added": [{"id": n["id"], "type": n["type"], "label": n.get("label", "")}
                        for n in added_nodes],
        "nodes_removed": [{"id": n["id"], "type": n["type"], "label": n.get("label", "")}
                          for n in removed_nodes],
        "edges_added": [{"source": e["source"], "target": e["target"], "type": e["type"]}
                        for e in added_edges],
        "edges_removed": [{"source": e["source"], "target": e["target"], "type": e["type"]}
                          for e in removed_edges],
        "conditions_added": added_conds,
        "conditions_removed": removed_conds,
        "value_shifts": value_shifts,
        "summary_delta": {
            k: {
                "baseline": b_summary.get(k, 0),
                "current": c_summary.get(k, 0),
                "delta": c_summary.get(k, 0) - b_summary.get(k, 0),
            }
            for k in ("total_nodes", "total_edges", "total_conditions")
            if isinstance(b_summary.get(k, 0), (int, float))
        },
    }


def save_entity_snapshot(graph: dict, uei: str,
                         description: str = "",
                         baseline_dir: Optional[Path] = None) -> Path:
    """Save a timestamped snapshot for future diffing.

    Mirrors save_baseline() in compile.py.
    """
    d = (baseline_dir or _DEFAULT_BASELINE_DIR) / uei
    d.mkdir(parents=True, exist_ok=True)

    ts = time.strftime("%Y-%m-%dT%H%M%SZ", time.gmtime())
    snapshot = {
        **graph,
        "_snapshot": {
            "timestamp": ts,
            "description": description,
            "uei": uei,
        },
    }

    snapshot_path = d / f"{ts}.json.gz"
    with gzip.open(snapshot_path, "wt", encoding="utf-8") as f:
        _json.dump(snapshot, f, indent=2, default=str)

    # Update latest pointer (uncompressed for fast reads)
    latest_path = d / "latest.json"
    with open(latest_path, "w", encoding="utf-8") as f:
        _json.dump(snapshot, f, indent=2, default=str)

    return snapshot_path


def load_entity_snapshot(uei: str,
                         snapshot_path: Optional[Path] = None,
                         baseline_dir: Optional[Path] = None) -> Optional[dict]:
    """Load the latest snapshot for an entity, or a specific one.

    Mirrors load_baseline() in compile.py.
    """
    if snapshot_path and snapshot_path.exists():
        p = snapshot_path
    else:
        d = (baseline_dir or _DEFAULT_BASELINE_DIR) / uei
        p = d / "latest.json"

    if not p.exists():
        return None

    if str(p).endswith(".gz"):
        with gzip.open(p, "rt", encoding="utf-8") as f:
            return _json.load(f)
    with open(p, encoding="utf-8") as f:
        return _json.load(f)


def list_entity_snapshots(uei: str,
                          baseline_dir: Optional[Path] = None) -> list[dict]:
    """List all snapshots for an entity, newest first.

    Mirrors list_snapshots() in compile.py.
    """
    d = (baseline_dir or _DEFAULT_BASELINE_DIR) / uei
    if not d.exists():
        return []

    snapshots = []
    files = sorted(list(d.glob("2*.json.gz")) + list(d.glob("2*.json")),
                   reverse=True)
    for f in files:
        if f.name == "latest.json":
            continue
        try:
            if str(f).endswith(".gz"):
                data = _json.loads(gzip.open(f, "rt", encoding="utf-8").read())
            else:
                data = _json.loads(f.read_text(encoding="utf-8"))
            snap = data.get("_snapshot", {})
            meta = data.get("meta", {}).get("summary", {})
            snapshots.append({
                "file": f.name,
                "timestamp": snap.get("timestamp", f.stem),
                "description": snap.get("description", ""),
                "nodes": meta.get("total_nodes", 0),
                "edges": meta.get("total_edges", 0),
                "conditions": meta.get("total_conditions", 0),
            })
        except Exception:
            continue
    return snapshots


# ── Tier 4: Global Graph (materialized parquet layer) ─────────────
#
# The global graph is the "big picture" view for the frontend product.
# It reads from pre-materialized parquet files (produced by materialize_graph.py)
# instead of compiling entities one-by-one from JSON.
#
# Hybrid model:
#   - DuckDB (parquet) for the global active-edge graph + cloud membership
#   - JSON (pt1 compile) for entity-level detail on click/zoom
#
# The materialized parquets live at s3://corporeal-agg/parquet/graph/

_GRAPH_PARQUET_PREFIX = f"s3://{os.environ.get('PARQUET_BUCKET', 'corporeal-agg')}/parquet/graph"


class GlobalGraph:
    """Query interface for the materialized global graph.

    Reads from three parquet files:
      active_edges.parquet    — contract rails
      cloud_membership.parquet — cloud rails
      node_attributes.parquet  — entity metadata

    All queries support as_of for time-machine lookback.
    """

    def __init__(self, db_conn=None, parquet_prefix: str = None, local_dir: str = None):
        """Initialize with a DuckDB connection.

        Args:
            db_conn: Existing DuckDB connection (e.g., from corpus._get_db()).
                     If None, creates a new one with httpfs.
            parquet_prefix: S3 prefix for graph parquets. Default: s3://corporeal-agg/parquet/graph
            local_dir: If set, read from local parquet files instead of S3.
        """
        if db_conn is not None:
            self._db = db_conn
        else:
            import duckdb
            self._db = duckdb.connect()
            self._db.execute("INSTALL httpfs; LOAD httpfs;")
            region = os.environ.get('AWS_REGION', 'us-east-1')
            self._db.execute(f"SET s3_region='{region}';")
            self._db.execute("SET s3_use_ssl=true;")
            try:
                import boto3
                creds = boto3.Session().get_credentials()
                if creds:
                    r = creds.get_frozen_credentials()
                    self._db.execute(f"SET s3_access_key_id='{r.access_key}';")
                    self._db.execute(f"SET s3_secret_access_key='{r.secret_key}';")
                    if r.token:
                        self._db.execute(f"SET s3_session_token='{r.token}';")
            except Exception:
                pass

        if local_dir:
            self._edges = os.path.join(local_dir, "active_edges.parquet")
            self._clouds = os.path.join(local_dir, "cloud_membership.parquet")
            self._nodes = os.path.join(local_dir, "node_attributes.parquet")
        else:
            pfx = parquet_prefix or _GRAPH_PARQUET_PREFIX
            self._edges = f"{pfx}/active_edges.parquet"
            self._clouds = f"{pfx}/cloud_membership.parquet"
            self._nodes = f"{pfx}/node_attributes.parquet"

    def _query(self, sql: str) -> list[dict]:
        return self._db.execute(sql).fetchdf().to_dict(orient="records")

    # ── Contract rail queries ─────────────────────────────────────

    def active_edge_count(self, as_of: Optional[str] = None) -> int:
        d = as_of or _today()
        return self._db.execute(
            f"SELECT COUNT(*) FROM read_parquet('{self._edges}') "
            f"WHERE performance_end >= '{d}' OR performance_end IS NULL"
        ).fetchone()[0]

    def active_edges_for_entity(self, uei: str, as_of: Optional[str] = None) -> list[dict]:
        """All active contract edges touching a specific entity."""
        d = as_of or _today()
        return self._query(
            f"SELECT * FROM read_parquet('{self._edges}') "
            f"WHERE (source_uei = '{uei}' OR target_uei = '{uei}') "
            f"AND (performance_end >= '{d}' OR performance_end IS NULL)"
        )

    def active_edges_for_entities(self, ueis: list[str], as_of: Optional[str] = None) -> list[dict]:
        """Active contract edges touching any of the given entities."""
        d = as_of or _today()
        uei_list = ",".join(f"'{u}'" for u in ueis)
        return self._query(
            f"SELECT * FROM read_parquet('{self._edges}') "
            f"WHERE (source_uei IN ({uei_list}) OR target_uei IN ({uei_list})) "
            f"AND (performance_end >= '{d}' OR performance_end IS NULL)"
        )

    def entity_counterparties(self, uei: str, as_of: Optional[str] = None) -> list[dict]:
        """Unique counterparties for an entity via active contracts."""
        d = as_of or _today()
        return self._query(f"""
            SELECT
                CASE WHEN source_uei = '{uei}' THEN target_uei ELSE source_uei END AS counterparty_uei,
                CASE WHEN source_uei = '{uei}' THEN target_name ELSE source_name END AS counterparty_name,
                CASE WHEN source_uei = '{uei}' THEN target_type ELSE 'contractor' END AS counterparty_type,
                CASE WHEN source_uei = '{uei}' THEN 'outflow' ELSE 'inflow' END AS flow_direction,
                COUNT(*) AS contract_count,
                SUM(obligations) AS total_obligations,
                MAX(latest_action) AS latest_action
            FROM read_parquet('{self._edges}')
            WHERE (source_uei = '{uei}' OR target_uei = '{uei}')
            AND (performance_end >= '{d}' OR performance_end IS NULL)
            GROUP BY 1, 2, 3, 4
            ORDER BY total_obligations DESC
        """)

    def edges_between(self, uei_a: str, uei_b: str, as_of: Optional[str] = None) -> list[dict]:
        """All active contracts between two specific entities."""
        d = as_of or _today()
        return self._query(
            f"SELECT * FROM read_parquet('{self._edges}') "
            f"WHERE ((source_uei = '{uei_a}' AND target_uei = '{uei_b}') "
            f"    OR (source_uei = '{uei_b}' AND target_uei = '{uei_a}')) "
            f"AND (performance_end >= '{d}' OR performance_end IS NULL)"
        )

    # ── Cloud rail queries ────────────────────────────────────────

    def cloud_members(self, hub_id: str) -> list[dict]:
        """All entities in a specific cloud hub."""
        return self._query(
            f"SELECT c.*, n.name, n.state, n.classification, n.revenue_ttm_m "
            f"FROM read_parquet('{self._clouds}') c "
            f"LEFT JOIN read_parquet('{self._nodes}') n ON c.uei = n.uei "
            f"WHERE c.hub_id = '{hub_id}' "
            f"ORDER BY n.revenue_ttm_m DESC NULLS LAST"
        )

    def entity_clouds(self, uei: str) -> list[dict]:
        """All cloud hubs an entity belongs to."""
        return self._query(
            f"SELECT * FROM read_parquet('{self._clouds}') WHERE uei = '{uei}'"
        )

    def shared_clouds(self, uei_a: str, uei_b: str) -> list[dict]:
        """Cloud hubs shared by two entities."""
        return self._query(
            f"SELECT a.hub_id, a.cloud_key, a.hub_label "
            f"FROM read_parquet('{self._clouds}') a "
            f"JOIN read_parquet('{self._clouds}') b ON a.hub_id = b.hub_id "
            f"WHERE a.uei = '{uei_a}' AND b.uei = '{uei_b}'"
        )

    # ── Node queries ──────────────────────────────────────────────

    def entity_attrs(self, uei: str) -> Optional[dict]:
        """Node attributes for a single entity."""
        rows = self._query(
            f"SELECT * FROM read_parquet('{self._nodes}') WHERE uei = '{uei}'"
        )
        return rows[0] if rows else None

    def entity_attrs_bulk(self, ueis: list[str]) -> list[dict]:
        """Node attributes for multiple entities."""
        uei_list = ",".join(f"'{u}'" for u in ueis)
        return self._query(
            f"SELECT * FROM read_parquet('{self._nodes}') WHERE uei IN ({uei_list})"
        )

    # ── Aggregate / stats ─────────────────────────────────────────

    def stats(self, as_of: Optional[str] = None) -> dict:
        """Global graph statistics."""
        d = as_of or _today()
        edge_count = self._db.execute(
            f"SELECT COUNT(*) FROM read_parquet('{self._edges}') "
            f"WHERE performance_end >= '{d}' OR performance_end IS NULL"
        ).fetchone()[0]
        node_count = self._db.execute(
            f"SELECT COUNT(*) FROM read_parquet('{self._nodes}')"
        ).fetchone()[0]
        cloud_count = self._db.execute(
            f"SELECT COUNT(DISTINCT hub_id) FROM read_parquet('{self._clouds}')"
        ).fetchone()[0]
        return {
            "as_of": d,
            "active_edges": edge_count,
            "entities": node_count,
            "cloud_hubs": cloud_count,
        }
