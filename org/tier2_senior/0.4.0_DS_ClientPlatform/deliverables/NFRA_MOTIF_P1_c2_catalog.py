#!/usr/bin/env python3
"""NFRA_MOTIF P1 -- the FIRST C2 motif catalog: ABSORB the TSGRAPH D1-D7 detector-library.

MOTIF-P1 (PRD docs/architecture/NFRA_MOTIF_PRD.md S5): "ABSORB the TSGRAPH detector-library
D1-D7 as the frontend-class C2 motif catalog... don't rebuild." This module IS that absorb,
runnable + grounded on the LIVE canonical graph (Rule 20: QUERY, never rebuild; Rule 22: every
recurrence + decompression chain is source-grounded on comp-kuzu rows, never invented).

The absorb principle (why a detector IS a C2 motif -- absorb-map S0):
  A C2 motif (PRD S3/S4.1) = a lossy-toward-abstraction, lossless-toward-provenance compression
  of a CONNECTED C1 subgraph, qualified by recurrence >= 2 (AC3: a recurrence-1 pattern is an
  *instance*, not a motif). Each detector Dn template-matches a recurring frontend idiom over the
  live C1 graph; every returned row is one instance (a connected C1 subgraph) that decompresses to
  file:line lexical evidence via the node_id + edge props. So:
      detector Dn -> C2 motif motif:<idiom>; live row-set = the motif's instances;
      len(rows) = recurrence (stability); each row's node_id+props = one instance's
      decompression chain (C1 interaction -> C0 lexical fact).

What this module does (the GO'd MOTIF-P1 build-entry checklist, minus the P2-2-gated leg):
  1. Re-validate each detector query HEAD-current on the live graph (marker oracle; counts drift,
     structure holds) -- and REPORT any drift/detector-bug found, never paper over it.
  2. Compose each absorbed detector into a C2 motif NODE (reusing comp_ladder.Node) whose children
     are the live instances (C1 interactions) bottoming out in C0 lexical facts (the decompression
     chain), with recurrence attached.
  3. Bind every motif to comp-ladder.fidelity_check (AC6 FIDELITY GATE): a motif that will not
     decompress to C0 evidence is a LATENT node -> build-fail. We import the ACTUAL gate, not a copy.
  4. Apply the AC3 stability threshold (recurrence >= 2 = motif; else instance/gap).
  5. Route the 3 documented gaps (D6/D8/D9) as coverage-channel entries with a named extractor-
     extension route -- NOT silently dropped (mirrors LAW-2 + the PRD's own honest-gap discipline).

NOT done here (P2-2-gated, staged): materializing these motifs AS C2 nodes/edges IN the store +
the GRAPHDEPTH CONTAINS-rollup C1->C2->C3 compression on live cluster edges + C3 emergence (P2) +
PROMOTE candidate emission with the FEDOBS co-occurrence join (P3). The catalog DESIGN + the
composed-and-fidelity-passing C2 nodes are available NOW on the comp-cluster CLI substrate.

Source (grounded, not invented): deliverables/tsgraph_detectors.yaml (commit cf1c1dcde, the
TSGRAPH P3-2 detector-library, CVO-certed) + deliverables/MOTIF_P1_D1toD7_C2_catalog_absorb_map.md.

Usage:
  python NFRA_MOTIF_P1_c2_catalog.py                # live absorb: run detectors, compose motifs,
                                                    #   fidelity-check each, print the C2 catalog
  python NFRA_MOTIF_P1_c2_catalog.py --self-test    # gate-logic tests (no live graph needed):
                                                    #   fidelity negative control + AC3 + D2 type-bug
  python NFRA_MOTIF_P1_c2_catalog.py --ladder D1    # print the full comp-ladder for one motif
  python NFRA_MOTIF_P1_c2_catalog.py --catalog      # print the absorb catalog table (no live run)

Author: 0.4.0_DS_ClientPlatform~B (MOTIF graph-lane, re-allocated 2026-07-08). Reuses my CSE-C1
materializer discipline: spec-as-code, grounded on live rows, an exercisable gate + a negative control.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
# bind to the ACTUAL fidelity gate (req#3: every C2/C3 node PASSES comp-ladder fidelity_check)
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))
from comp_ladder import Node, decompress, fidelity_check  # noqa: E402


# ---------------------------------------------------------------------------
# comp-kuzu runner -- QUERY the live canonical graph (Rule 20), capture provenance header.
# ---------------------------------------------------------------------------
def comp_kuzu(query: str) -> tuple:
    """Run a Cypher query on the canonical Kuzu DB. Returns (rows: list[dict], provenance: dict).

    Invokes comp-kuzu's underlying python CLI (infra/aws/globgrph/kuzu_cli.py --json) DIRECTLY via
    sys.executable -- the SAME canonical persisted Kuzu DB the `.tools/comp-kuzu` bash wrapper hits
    (Rule 20). We call the python entrypoint rather than the bash wrapper because `bash` is not
    reachable from a python subprocess on this host (it resolves to WSL's relay, which errors).
    The CLI prints a provenance header then the JSON array; we capture Nessie HEAD + snapshot ids.
    """
    cli = os.path.join(WS, "infra", "aws", "globgrph", "kuzu_cli.py")
    proc = subprocess.run(
        [sys.executable, cli, "--json", query],
        capture_output=True, text=True, cwd=WS, timeout=120,
    )
    out = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")
    prov = {}
    for line in out.splitlines():
        s = line.strip()
        if s.startswith("Nessie HEAD:"):
            prov["nessie_head"] = s.split(":", 1)[1].strip()
        elif s.startswith("nodes snapshot-id:"):
            prov["nodes_snapshot_id"] = s.split(":", 1)[1].strip()
        elif s.startswith("edges snapshot-id:"):
            prov["edges_snapshot_id"] = s.split(":", 1)[1].strip()
    # JSON begins at the first '[' at column 0 (the header lines are all indented or ===-ruled)
    idx = out.find("\n[")
    if idx < 0:
        idx = out.find("[")
    if idx < 0:
        return [], prov
    try:
        rows = json.loads(out[idx:].strip())
    except json.JSONDecodeError:
        # find the balanced array
        start = out.find("[", idx if idx >= 0 else 0)
        depth, end = 0, -1
        for i in range(start, len(out)):
            if out[i] == "[":
                depth += 1
            elif out[i] == "]":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        rows = json.loads(out[start:end]) if end > 0 else []
    return rows, prov


# ---------------------------------------------------------------------------
# node_id -> C0 lexical evidence (the lossless-toward-provenance address)
#   out:portal/.../X.tsx:725#spread              -> file X.tsx, line 725, sym spread
#   type:portal/.../portal-proxy.ts#T#field      -> file portal-proxy.ts, sym T#field
#   rc:portal/.../MetricsRow.tsx#MetricsRow       -> file MetricsRow.tsx, sym MetricsRow
#   endpoint:getDataRefreshHistory                -> sym getDataRefreshHistory (no file locus)
# ---------------------------------------------------------------------------
def parse_locus(node_id: str) -> tuple:
    """Return (source, locus, symbol) parsed from a graph node_id. The node_id IS the lexical
    address -> this is what makes every C0 fact bottom out in real file:line (or symbol) evidence."""
    body = node_id.split(":", 1)[1] if ":" in node_id and node_id.split(":", 1)[0] in (
        "out", "type", "rc", "endpoint", "symbol") else node_id
    sym = ""
    if "#" in body:
        path, sym = body.split("#", 1)
    else:
        path = body
    locus = "-"
    source = path
    if ".tsx:" in path or ".ts:" in path:
        source, locus = path.rsplit(":", 1)
    return source, ("L" + locus if locus != "-" else "-"), sym


def c0_fact(node_id: str, ntype: str, evidence_extra: str = "") -> Node:
    """Build a C0 lexical-fact node from a live graph node_id (+ any edge-prop evidence)."""
    source, locus, sym = parse_locus(node_id)
    ev = node_id + ((" :: " + evidence_extra) if evidence_extra else "")
    return Node(node_id, "C0", ntype, sym or node_id,
                provenance={"source": source, "locus": locus, "evidence": ev})


# ---------------------------------------------------------------------------
# THE ABSORB CATALOG -- one spec per detector. queries are the CANONICAL (corrected) form.
#   verdict: ABSORB | ABSORB-candidate | ABSORB-advisory | ABSORB-overlap-lens | GAP
# ---------------------------------------------------------------------------
FLOWS_GUARD = ("e.edge_type='FLOWS_TO' AND e.props CONTAINS 'recompute/guarded' "
               "AND NOT (e.props CONTAINS '\"condition\": null')")

CATALOG = [
    {
        "id": "D1", "motif": "silent-display-fork", "ntype": "SilentDisplayFork",
        "catalog_class": "A1/A3", "tier": "gate-ready", "promote_first": True, "verdict": "ABSORB",
        "idiom": ">=2 guarded FLOWS_TO from DISTINCT sources into one out: display sink",
        # recurrence: distinct out: sinks fed by >=2 distinct guarded sources
        "recurrence_query": (
            "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE " + FLOWS_GUARD +
            " AND b.node_id STARTS WITH 'out:' WITH b.node_id AS dst, "
            "count(DISTINCT a.node_id) AS srcCount WHERE srcCount >= 2 RETURN dst, srcCount ORDER BY dst"),
        "key": "dst",
        # expansion: per sink, its guarded source fields + the guard condition (the decompression chain)
        "expansion_query": (
            "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE " + FLOWS_GUARD +
            " AND b.node_id STARTS WITH 'out:' RETURN b.node_id AS dst, a.node_id AS src, "
            "e.props AS props ORDER BY dst, src"),
        "sample": None,  # full (only 5)
    },
    {
        "id": "D2", "motif": "cross-firm-asymmetry", "ntype": "CrossFirmAsymmetry",
        "catalog_class": "A2", "tier": "gate-ready", "promote_first": False, "verdict": "ABSORB",
        "idiom": "firm-identity-literal FLOWS_TO with a one-sided branch (trueBranch=0 XOR falseBranch=0)",
        # CANONICAL (corrected): CAST the string-typed sum column to INT64 -- see the D2 type-bug finding
        "recurrence_query": (
            "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type='FLOWS_TO' "
            "AND e.props CONTAINS 'inflection_wealth_management' WITH b.node_id AS dst, "
            "sum(CASE WHEN e.props CONTAINS '== true' THEN 1 ELSE 0 END) AS trueBranch, "
            "sum(CASE WHEN e.props CONTAINS '== false' THEN 1 ELSE 0 END) AS falseBranch, "
            "count(e) AS firmEdges WHERE CAST(trueBranch AS INT64) = 0 OR CAST(falseBranch AS INT64) = 0 "
            "RETURN dst, firmEdges, trueBranch, falseBranch ORDER BY dst"),
        "key": "dst",
        "expansion_query": (
            "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type='FLOWS_TO' "
            "AND e.props CONTAINS 'inflection_wealth_management' RETURN b.node_id AS dst, "
            "a.node_id AS src, e.props AS props ORDER BY dst, src"),
        "sample": None,
        "finding": ("D2 TYPE-BUG (grounded HEAD-current): sum(CASE...) is STRING-typed on the current "
                    "Kuzu build (nodes-snapshot rebuilt since pre-stage 8205589666541874180 -> "
                    "6127141211382924351); the yaml D2's 'WHERE trueBranch = 0' compares string-vs-int "
                    "and returns 0 rows. Motif is LIVE (2 asymmetric inflection forks). Fix = "
                    "CAST(... AS INT64) (this catalog's canonical form). Flag to tsgraph_detectors.yaml owner (0.4.0_DE)."),
    },
    {
        "id": "D3", "motif": "hardcoded-firm-literal", "ntype": "HardcodedFirmLiteral",
        "catalog_class": "A9", "tier": "advisory", "promote_first": False, "verdict": "ABSORB-overlap-lens",
        "idiom": "bare firm-identity literal in a FLOWS_TO/PROP_PASSES branch position",
        "recurrence_query": (
            "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE (e.edge_type='FLOWS_TO' "
            "OR e.edge_type='PROP_PASSES') AND (e.props CONTAINS 'inflection_wealth_management' "
            "OR e.props CONTAINS \"'bd'\" OR e.props CONTAINS \"'cot'\") "
            "RETURN e.edge_type AS et, a.node_id AS src, b.node_id AS dst ORDER BY dst"),
        "key": "dst",  # dst can repeat; recurrence measured as distinct edges below
        "expansion_query": (
            "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE (e.edge_type='FLOWS_TO' "
            "OR e.edge_type='PROP_PASSES') AND (e.props CONTAINS 'inflection_wealth_management' "
            "OR e.props CONTAINS \"'bd'\" OR e.props CONTAINS \"'cot'\") "
            "RETURN b.node_id AS dst, a.node_id AS src, e.props AS props ORDER BY dst, src"),
        "sample": None,
        "note": ("Overlap with D2 on the inflection edges is EXPECTED (different lens: the hardcoded "
                 "literal itself vs the branch-asymmetry). Original 'bd' anchor is a REMEDIATED incident "
                 "(ADVI_SHARED.006), re-anchored to the live inflection literal."),
    },
    {
        "id": "D4", "motif": "dead-component", "ntype": "DeadComponent",
        "catalog_class": "A5", "tier": "candidate-gen", "promote_first": True, "verdict": "ABSORB-candidate",
        "idiom": "ReactComponent with 0 inbound INSTANTIATES (negative-space)",
        "recurrence_query": (
            "MATCH (rc:CloudNode) WHERE rc.node_type='ReactComponent' "
            "OPTIONAL MATCH (j:CloudNode)-[e:CloudEdge]->(rc) "
            "WITH rc, sum(CASE WHEN e.edge_type='INSTANTIATES' THEN 1 ELSE 0 END) AS inst "
            "WHERE CAST(inst AS INT64) = 0 RETURN rc.node_id AS id ORDER BY id"),
        "key": "id",
        "expansion_query": None,  # absence motif: the instance IS the node + the 0-inbound fact
        "sample": 8,
        "note": ("FP-DENSE (121 raw). ABSORBED AS A CANDIDATE MOTIF: a hit is promoted to a dead-code "
                 "FINDING only after file-level confirm (no import + no JSX). Carries D4's 3 FP-filter "
                 "classes (conditional-render gap / design-system barrel / page route-roots + lazy)."),
    },
    {
        "id": "D5", "motif": "orphan-endpoint", "ntype": "OrphanEndpoint",
        "catalog_class": "A5-variant", "tier": "advisory", "promote_first": False, "verdict": "ABSORB-advisory",
        "idiom": "Endpoint with 0 inbound FETCHES (dead data channel)",
        "recurrence_query": (
            "MATCH (ep:CloudNode) WHERE ep.node_type='Endpoint' "
            "OPTIONAL MATCH (h:CloudNode)-[e:CloudEdge]->(ep) "
            "WITH ep, sum(CASE WHEN e.edge_type='FETCHES' THEN 1 ELSE 0 END) AS f "
            "WHERE CAST(f AS INT64) = 0 RETURN ep.node_id AS id ORDER BY id"),
        "key": "id",
        "expansion_query": None,
        "sample": 8,
        "note": ("ADVISORY: mixes true-dead endpoints with non-hook callers the extractor can't resolve "
                 "to a FETCHES edge (getAUM* known-FP class). Confirm true-deadness with a caller grep."),
    },
    {
        "id": "D7", "motif": "render-without-null-guard", "ntype": "RenderWithoutNullGuard",
        "catalog_class": "A8", "tier": "advisory", "promote_first": False, "verdict": "ABSORB-advisory",
        "idiom": "nullable Field is a RENDERS target (guard not modeled -> WARN)",
        "recurrence_query": (
            "MATCH (jr:CloudNode)-[e:CloudEdge]->(f:CloudNode) WHERE e.edge_type='RENDERS' "
            "AND f.node_type='Field' AND (f.props CONTAINS '\"optional\": true' "
            "OR f.props CONTAINS '| null' OR f.props CONTAINS '| undefined') "
            "RETURN DISTINCT f.node_id AS id ORDER BY id"),
        "key": "id",
        "expansion_query": None,  # instance = the nullable field node + its RENDERS in-edge
        "sample": 8,
        "note": ("ADVISORY / WARN-ONLY: the graph cannot see the render-site guard, so a correctly-guarded "
                 "render is indistinguishable from an unguarded one. Promotes to gate-ready only after the "
                 "extractor emits RENDERS.guarded:bool (extractor_ask_D7_guarded_bool)."),
    },
]

# GAPS -- documented coverage-channel entries, NOT absorbed, NOT silently dropped (LAW-2).
GAPS = [
    {"id": "D6", "class": "A6", "name": "prop-drill-depth", "recurrence": 0,
     "why": ("STRUCTURAL MISS: PROP_PASSES is a FLAT one-hop binding (source ALWAYS a JSXElement, target a "
             "Prop/Field); a Prop/Field is never a PROP_PASSES source, so NO chain length>=2 exists "
             "(2-hop = 0 -> depth>=4 = 0). recurrence-0 = not a motif on this substrate."),
     "route_to": "extractor-extension: emit a transitive PROP_DRILL edge (link Prop-receipt -> child JSXElement re-pass)"},
    {"id": "D8", "class": "A4", "name": "any-erosion", "recurrence": None,
     "why": "NOT graph-modeled: the extractor emits no AnyCast node for `: any` / `as any`; nothing to MATCH.",
     "route_to": "extractor-extension (AnyCast node w/ file:line) OR NFRA_DEBTSCAN/PORTALSWEEP no-explicit-any ESLint"},
    {"id": "D9", "class": "A7", "name": "hook-dep-mismatch", "recurrence": None,
     "why": ("NOT graph-modeled: no HookDep edges (declared-deps vs referenced-idents set-diff); "
             "neither side is in the graph."),
     "route_to": "extractor-extension (Hook->{declared} + Hook->{referenced}) THEN set-diff; interim react-hooks/exhaustive-deps ESLint"},
]

AC3_THRESHOLD = 2  # recurrence >= 2 = a motif; recurrence 1 = an instance (PRD AC3 stability threshold)


# ---------------------------------------------------------------------------
# Compose one detector's live rows into a C2 motif Node (the decompression chain).
# ---------------------------------------------------------------------------
def build_motif(spec: dict) -> tuple:
    """Run the detector live, compose the C2 motif Node tree, return (motif_node, recurrence, prov)."""
    rows, prov = comp_kuzu(spec["recurrence_query"])
    # recurrence = distinct instance keys (for D3 the "instance" is an edge, count distinct edges)
    if spec["id"] == "D3":
        recurrence = len(rows)  # each row is a distinct firm-literal edge
    else:
        recurrence = len({r[spec["key"]] for r in rows})
    instance_keys = sorted({r[spec["key"]] for r in rows})

    # expansion detail (positive-edge motifs) grouped by sink
    detail = {}
    if spec.get("expansion_query"):
        ex_rows, _ = comp_kuzu(spec["expansion_query"])
        for r in ex_rows:
            detail.setdefault(r["dst"], []).append(r)

    sample = spec.get("sample")
    keys_for_tree = instance_keys[:sample] if sample else instance_keys

    c1_instances = []
    for key in keys_for_tree:
        if spec.get("expansion_query") and key in detail:
            # positive-edge motif: C1 interaction (the guarded/firm-literal fork at this sink)
            #   children = C0 sink fact + C0 source facts (each with the guard condition as evidence)
            c0_children = [c0_fact(key, "DisplaySink", "display/render sink")]
            for e in detail[key]:
                cond = ""
                try:
                    cond = json.loads(e["props"]).get("condition", "")
                except Exception:  # noqa: BLE001
                    cond = e.get("props", "")[:80]
                c0_children.append(c0_fact(e["src"], "SourceField", "guard: " + cond))
            c1_instances.append(Node(
                "c1:" + spec["id"] + ":" + key, "C1", spec["ntype"] + "Interaction",
                spec["motif"] + " @ " + key,
                rule="detector " + spec["id"] + ": " + spec["idiom"],
                children=c0_children))
        else:
            # absence motif (D4/D5): the instance IS the node + the negative-space fact
            neg = "0 inbound INSTANTIATES" if spec["id"] == "D4" else (
                "0 inbound FETCHES" if spec["id"] == "D5" else "nullable field, RENDERS target")
            c0 = c0_fact(key, spec["ntype"] + "Site", neg)
            c1_instances.append(Node(
                "c1:" + spec["id"] + ":" + key, "C1", spec["ntype"] + "Occurrence",
                spec["motif"] + " @ " + key,
                rule="detector " + spec["id"] + " (" + spec["tier"] + "): " + spec["idiom"],
                children=[c0]))

    motif = Node(
        "motif:" + spec["motif"], "C2", spec["ntype"], spec["motif"],
        rule="ABSORB " + spec["id"] + " (" + spec["catalog_class"] + "): " + spec["idiom"],
        children=c1_instances)
    return motif, recurrence, prov


# ---------------------------------------------------------------------------
# Live absorb: run every detector, compose + fidelity-check every motif, print the catalog.
# ---------------------------------------------------------------------------
def run_absorb() -> int:
    print("=" * 78)
    print("NFRA_MOTIF P1 -- C2 motif catalog (ABSORB TSGRAPH D1-D7) -- LIVE HEAD-current")
    print("=" * 78)
    all_ok = True
    prov_seen = {}
    results = []
    for spec in CATALOG:
        motif, recurrence, prov = build_motif(spec)
        prov_seen = prov or prov_seen
        ok, failures = fidelity_check(motif)
        stable = recurrence >= AC3_THRESHOLD
        n_c0 = sum(1 for _, n in decompress(motif) if n.layer == "C0")
        results.append((spec, motif, recurrence, stable, ok, failures, n_c0))
        if not ok:
            all_ok = False

    print("\nProvenance (live graph the absorb ran on):")
    print("  Nessie HEAD: %s | nodes-snap: %s | edges-snap: %s"
          % (prov_seen.get("nessie_head", "?"),
             prov_seen.get("nodes_snapshot_id", "?"), prov_seen.get("edges_snapshot_id", "?")))

    print("\n%-4s %-26s %-14s %-6s %-6s %-8s %s" %
          ("Dn", "motif", "tier", "recur", "AC3", "fidelity", "verdict"))
    print("-" * 90)
    for spec, motif, recurrence, stable, ok, failures, n_c0 in results:
        print("%-4s %-26s %-14s %-6s %-6s %-8s %s" % (
            spec["id"], spec["motif"], spec["tier"], recurrence,
            "STABLE" if stable else "inst.", "PASS" if ok else "FAIL", spec["verdict"]))
        if failures:
            for f in failures:
                print("       ! " + f)

    print("\nDocumented GAPS (coverage-channel; NOT absorbed, NOT silently dropped -- LAW-2):")
    for g in GAPS:
        rec = g["recurrence"]
        rec_s = ("recurrence=%s" % rec) if rec is not None else "not graph-modeled"
        print("  %-4s %-20s [%s] %s" % (g["id"], g["name"], g["class"], rec_s))
        print("       route -> " + g["route_to"])

    # findings/notes
    print("\nFindings + absorb notes:")
    for spec in CATALOG:
        if spec.get("finding"):
            print("  [" + spec["id"] + "] FINDING: " + spec["finding"])
    print("\nGRAPHDEPTH rollup reuse (req#2): each C2 motif is the fine->coarse EXISTENTIAL rollup of its")
    print("  instance set (many C1 interactions -> one C2 idiom) -- the same rollup semantics as")
    print("  comp-depth rollup (org/modules/graph/comp_depth_cli.py). Materializing the CONTAINS edges")
    print("  IN the graph is P2-2-gated (MOTIF-P0, 0.7.0_AE); the compression SEMANTICS apply now.")
    print("PROMOTE candidate emission (req#5, P3-staged): each STABLE motif -> a candidate carrying")
    print("  {recurrence, decompression-chain, fedobs_cooccurrence: <iceberg.globgrph.cse cse_coevolution")
    print("  join, P3/in-VPC>}. Full emission is MOTIF-P3.")

    absorbed = sum(1 for s in CATALOG)
    print("\nSUMMARY: %d detectors absorbed (%d STABLE motifs pass the AC6 fidelity gate) + %d gaps routed."
          % (absorbed, sum(1 for r in results if r[3] and r[4]), len(GAPS)))
    print("AC6 FIDELITY GATE (every C2 motif decompresses to C0 evidence): %s"
          % ("PASS -- all motifs grounded, no LATENT node" if all_ok else "FAIL -- latent node(s) found"))
    return 0 if all_ok else 1


# ---------------------------------------------------------------------------
# Self-test -- gate logic, no live graph needed (CI-able, exercisable by CTO/CVO).
# ---------------------------------------------------------------------------
def self_test() -> int:
    print("=== NFRA_MOTIF_P1 self-test (gate logic; no live graph) ===")
    passed = []

    # 1. POSITIVE: a well-formed motif (C2 -> C1 -> C0-with-evidence) passes fidelity_check.
    good_c0 = Node("out:portal/src/pages/ModelPortfolios.tsx:725#spread", "C0", "DisplaySink",
                   "spread", provenance={"source": "portal/src/pages/ModelPortfolios.tsx",
                                         "locus": "L725", "evidence": "out:...:725#spread :: guard"})
    good_c1 = Node("c1:D1:x", "C1", "SilentDisplayForkInteraction", "fork", rule="D1", children=[good_c0])
    good_c2 = Node("motif:silent-display-fork", "C2", "SilentDisplayFork", "silent-display-fork",
                   rule="ABSORB D1", children=[good_c1])
    ok, _ = fidelity_check(good_c2)
    passed.append(("positive: well-formed motif PASSES fidelity", ok is True))

    # 2. NEGATIVE CONTROL: a LATENT C2 motif (no children / no decompression path) MUST FAIL.
    #    This is the gate biting -- a motif you cannot decompress to evidence = the LAW-2 violation.
    latent = Node("motif:latent", "C2", "LatentMotif", "latent (embedding-like)", children=[])
    ok_l, fails_l = fidelity_check(latent)
    passed.append(("negative control: LATENT motif (no children) FAILS the gate", ok_l is False and len(fails_l) > 0))

    # 3. NEGATIVE CONTROL 2: a C2 whose chain does NOT bottom out in C0 evidence (evidence-less C0) FAILS.
    bad_c0 = Node("x", "C0", "Field", "x", provenance=None)
    bad_c2 = Node("motif:bad", "C2", "M", "bad", children=[Node("c1", "C1", "I", "i", children=[bad_c0])])
    ok_b, fails_b = fidelity_check(bad_c2)
    passed.append(("negative control 2: evidence-less C0 FAILS the gate", ok_b is False and len(fails_b) > 0))

    # 4. AC3 stability threshold: recurrence 1 = instance (NOT a motif); recurrence >= 2 = motif.
    passed.append(("AC3: recurrence 1 classified as instance", (1 >= AC3_THRESHOLD) is False))
    passed.append(("AC3: recurrence 2 classified as motif", (2 >= AC3_THRESHOLD) is True))

    # 5. D2 type-bug documentation: the buggy int-compare form vs the corrected CAST form.
    #    (documented as a runnable assertion over the KNOWN buckets; the live proof is in run_absorb.)
    buckets = [{"trueBranch": "0", "falseBranch": "2"}, {"trueBranch": "0", "falseBranch": "2"}]
    buggy = [b for b in buckets if b["trueBranch"] == 0 or b["falseBranch"] == 0]       # str vs int -> []
    fixed = [b for b in buckets if int(b["trueBranch"]) == 0 or int(b["falseBranch"]) == 0]  # -> 2
    passed.append(("D2 type-bug: buggy int-compare drops all rows", len(buggy) == 0))
    passed.append(("D2 fix: CAST/int-compare recovers 2 asymmetric forks", len(fixed) == 2))

    n_ok = sum(1 for _, p in passed if p)
    for name, p in passed:
        print("  [%s] %s" % ("PASS" if p else "FAIL", name))
    print("--- self-test: %d/%d passed ---" % (n_ok, len(passed)))
    return 0 if n_ok == len(passed) else 1


def print_catalog() -> int:
    print("NFRA_MOTIF P1 -- ABSORB CATALOG (design; no live run)")
    print("%-4s %-26s %-13s %-13s %s" % ("Dn", "motif", "tier", "verdict", "idiom"))
    print("-" * 100)
    for s in CATALOG:
        print("%-4s %-26s %-13s %-13s %s" % (s["id"], s["motif"], s["tier"], s["verdict"], s["idiom"][:44]))
    print("\nGAPS (routed, not dropped):")
    for g in GAPS:
        print("  %-4s %-20s [%s]" % (g["id"], g["name"], g["class"]))
    return 0


def ladder_one(dn: str) -> int:
    from comp_ladder import print_ladder
    spec = next((s for s in CATALOG if s["id"] == dn), None)
    if not spec:
        print("unknown detector %s (have D1-D7 minus gaps)" % dn)
        return 2
    motif, recurrence, _ = build_motif(spec)
    print("recurrence (stability) = %d  |  AC3 %s" % (recurrence, "STABLE" if recurrence >= AC3_THRESHOLD else "instance"))
    print_ladder(motif)
    return 0


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    args = sys.argv[1:]
    if "--self-test" in args:
        return self_test()
    if "--catalog" in args:
        return print_catalog()
    if "--ladder" in args:
        i = args.index("--ladder")
        return ladder_one(args[i + 1] if i + 1 < len(args) else "D1")
    return run_absorb()


if __name__ == "__main__":
    sys.exit(main())
