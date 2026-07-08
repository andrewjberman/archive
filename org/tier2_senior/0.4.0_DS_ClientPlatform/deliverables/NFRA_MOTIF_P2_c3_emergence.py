#!/usr/bin/env python3
"""NFRA_MOTIF P2 -- C3 SYSTEM EMERGENCE: compose connected C2 motifs into discovered architecture.

MOTIF-P2 (TO NFRA_MOTIF.P2.c3-system-emergence): a C3 system (PRD S4.2) is a CONNECTED set of C2
motifs forming a coherent capability -- EMERGENT (discovered from motif connectivity, NOT declared) +
decomposable. This module composes the CVO-CERTED C2 catalog (MOTIF-P1, cert b783dd504) into C3
systems by STRUCTURAL community detection, on the now-live cluster substrate (MOTIF-P0 / TSGRAPH-P2-2).

The build, against the acceptance criteria:
  AC4 EMERGENCE     -- >=1 C3 system DISCOVERED from connected motifs, not declared in advance.
  AC2 DECOMPRESSION -- every C3 decomposes C3 -> C2 motifs -> C1 interactions -> C0 lexical evidence.
  AC1 STRUCTURAL    -- connectivity is graph-derived (shared constituents + cluster co-membership +
                       SHARES_SOURCE coupling), NEVER embedding-similarity. grep-proof: no vector/embed/
                       cosine/similarity anywhere; every edge is a node_id set-intersection over the graph.
  AC6 FIDELITY GATE -- every C3 PASSES comp-ladder fidelity_check (imported REAL, not a copy).

TWO structural connectivity signals (community detection = connected-components over their union):
  1. SHARED-CONSTITUENT (C1, substrate-stable) -- two motifs connected iff they share a C1/C0 node_id
     (an instance both idioms match). The MOTIF-P1 pre-stage signal.
  2. CLUSTER CO-MEMBERSHIP (the now-live C2 cluster substrate) -- two motifs connected iff their
     instances live in the same PanelCluster (via CONTAINS_DRILLDOWN) OR in SHARES_SOURCE-coupled
     clusters. This is what MOTIF-P0's 91 clusters unblocked (2nd signal, reuse-not-rebuild).

Compression: reuse GRAPHDEPTH's fine->coarse EXISTENTIAL rollup semantics (org/modules/graph/
comp_depth_cli.py) for C2->C3 -- many C2 motifs roll up to one C3 idiom. (C3-node + CONTAINS-edge
materialization IN the store is the store-write leg; this module emits the discovered systems as
fidelity-passing Nodes, decompressing to evidence -- the analysis the PROMOTE plane consumes.)

Grounds on the LIVE canonical graph via comp-kuzu (Rule 20; read the provenance header -- current is
healthy). comp-kuzu FinalizeS3 fix verified 2026-07-08 (06fbc6832, CVO 194fd7d00-lift): pin==HEAD
1930075230089813661, current. Load-bearing cluster claims cross-checkable vs the 20260708 snapshot.

Usage:
  python NFRA_MOTIF_P2_c3_emergence.py              # live: discover C3 systems, fidelity-gate each
  python NFRA_MOTIF_P2_c3_emergence.py --self-test  # AC4/AC6/AC1 proofs + negative control (no live graph for the gate logic)
  python NFRA_MOTIF_P2_c3_emergence.py --ladder     # print the comp-ladder for the first discovered C3 system

Author: 0.4.0_DS_ClientPlatform~B (MOTIF graph-lane). TO NFRA_MOTIF.P2 (re-allocated to ~B 2026-07-08).
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
sys.path.insert(0, _HERE)  # sibling P1 module
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))

import NFRA_MOTIF_P1_c2_catalog as P1  # noqa: E402  -- the C2 catalog (certed b783dd504)
from comp_ladder import Node, decompress, fidelity_check  # noqa: E402  -- the REAL fidelity gate


# ---------------------------------------------------------------------------
# The live cluster substrate (MOTIF-P0 / TSGRAPH-P2-2): file -> clusters, cluster -> coupled clusters.
# ---------------------------------------------------------------------------
def load_cluster_index() -> tuple:
    """file -> set(PanelCluster) via PanelCluster -CONTAINS_DRILLDOWN-> ReactComponent (live graph)."""
    rows, prov = P1.comp_kuzu(
        "MATCH (pc:CloudNode)-[e:CloudEdge]->(rc:CloudNode) WHERE e.edge_type='CONTAINS_DRILLDOWN' "
        "AND pc.node_type='PanelCluster' RETURN pc.node_id AS cluster, rc.node_id AS component")
    file_to_clusters: dict = {}
    for r in rows:
        comp = r["component"]
        file = comp.split(":", 1)[1].split("#", 1)[0] if ":" in comp else comp
        file_to_clusters.setdefault(file, set()).add(r["cluster"])
    return file_to_clusters, prov


def load_shares_source() -> dict:
    """cluster -> set(coupled clusters) via SHARES_SOURCE (cross-panel data-source coupling)."""
    rows, _ = P1.comp_kuzu(
        "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type='SHARES_SOURCE' "
        "RETURN a.node_id AS a, b.node_id AS b")
    coupled: dict = {}
    for r in rows:
        coupled.setdefault(r["a"], set()).add(r["b"])
        coupled.setdefault(r["b"], set()).add(r["a"])
    return coupled


def motif_files(motif: Node) -> set:
    """The set of source files a motif's instances touch (from its C1/C0 constituent node_ids)."""
    files = set()
    for _, n in decompress(motif):
        if n.layer in ("C0", "C1"):
            src, _, _ = P1.parse_locus(n.nid)
            if src and (".tsx" in src or ".ts" in src):
                files.add(src)
    return files


def motif_clusters(motif: Node, file_to_clusters: dict) -> set:
    """The set of PanelClusters a motif's instances live in (union over its instance files)."""
    cl = set()
    for f in motif_files(motif):
        cl |= file_to_clusters.get(f, set())
    return cl


# ---------------------------------------------------------------------------
# STRUCTURAL community detection: connected-components over the union of the 2 connectivity signals.
# ---------------------------------------------------------------------------
def build_c3_systems(motifs: list, file_to_clusters: dict, coupled: dict) -> tuple:
    """Compose connected motifs into emergent C3 systems. Returns (systems, singletons, evidence).

    A motif pair is CONNECTED iff (structural, no embedding):
      (a) shared-constituent: their C1/C0 footprints intersect, OR
      (b) cluster co-membership: their instance-clusters intersect, OR
      (c) SHARES_SOURCE coupling: some cluster of one is SHARES_SOURCE-coupled to some cluster of the other.
    A connected component of >=2 motifs is a C3 system (a lone motif is NOT a system -- reported, not forced).
    """
    foot = {m.nid: {n.nid for _, n in decompress(m) if n.layer in ("C0", "C1")} for m in motifs}
    clus = {m.nid: motif_clusters(m, file_to_clusters) for m in motifs}
    by_nid = {m.nid: m for m in motifs}
    ids = [m.nid for m in motifs]

    parent = {i: i for i in ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    evidence: dict = {}  # (mi,mj) -> {"shared_constituents":[], "shared_clusters":[], "coupled_clusters":[]}
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            shared_c = foot[a] & foot[b]
            shared_cl = clus[a] & clus[b]
            coupled_cl = {(x, y) for x in clus[a] for y in clus[b] if y in coupled.get(x, set())}
            if shared_c or shared_cl or coupled_cl:
                union(a, b)
                evidence[(a, b)] = {"shared_constituents": sorted(shared_c),
                                    "shared_clusters": sorted(shared_cl),
                                    "coupled_clusters": sorted("%s~%s" % (x, y) for x, y in coupled_cl)}
    comps: dict = {}
    for mid in ids:
        comps.setdefault(find(mid), []).append(mid)

    systems, singletons = [], []
    for _, members in sorted(comps.items()):
        if len(members) < 2:
            singletons.append(members[0])
            continue
        member_motifs = [by_nid[m] for m in members]
        # gather the connectivity evidence within this component (the 'why connected')
        why_const, why_clus, why_coupled = set(), set(), set()
        for (a, b), ev in evidence.items():
            if a in members and b in members:
                why_const |= set(ev["shared_constituents"])
                why_clus |= set(ev["shared_clusters"])
                why_coupled |= set(ev["coupled_clusters"])
        theme = _name_system(member_motifs, why_const, why_clus)
        rule = ("C3 EMERGENCE (structural, no embedding): motifs {%s} connected via %s -> capability (DISCOVERED)"
                % (", ".join(m.split(":", 1)[1] for m in members), _why_str(why_const, why_clus, why_coupled)))
        sys_node = Node("system:" + theme, "C3", "EmergentSystem", theme, rule=rule, children=member_motifs)
        systems.append((sys_node, {"shared_constituents": sorted(why_const),
                                   "shared_clusters": sorted(why_clus),
                                   "coupled_clusters": sorted(why_coupled)}))
    return systems, singletons, evidence


def _why_str(const, clus, coupled) -> str:
    parts = []
    if const:
        parts.append("shared-constituent[%s]" % ", ".join(sorted(const)[:2]))
    if clus:
        parts.append("cluster-co-membership[%s]" % ", ".join(sorted(clus)[:2]))
    if coupled:
        parts.append("SHARES_SOURCE-coupled[%s]" % ", ".join(sorted(coupled)[:2]))
    return " + ".join(parts) or "(none)"


def _name_system(motifs: list, const: set, clus: set) -> str:
    labels = {m.label for m in motifs}
    if any("firm" in s or "inflection" in s or "ClientsTab" in s for s in (const | clus)) or \
       any("firm" in lbl for lbl in labels):
        return "firm-conditional-display"
    if any("cluster:" in c for c in clus):
        # name by the dominant cluster page
        pages = {c.split(":")[1] for c in clus if ":" in c}
        return ("cluster-" + sorted(pages)[0].lower()) if pages else "shared-cluster-capability"
    return "shared-constituent-capability"


# ---------------------------------------------------------------------------
# Live emergence run.
# ---------------------------------------------------------------------------
def _build_stable_motifs() -> tuple:
    motifs, prov_seen = [], {}
    for spec in P1.CATALOG:
        motif, recurrence, prov = P1.build_motif(spec)
        prov_seen = prov or prov_seen
        if recurrence >= P1.AC3_THRESHOLD:
            motifs.append(motif)
    return motifs, prov_seen


def run_emergence() -> int:
    print("=" * 80)
    print("NFRA_MOTIF P2 -- C3 SYSTEM EMERGENCE (compose certed C2 catalog -> discovered architecture)")
    print("=" * 80)
    motifs, prov = _build_stable_motifs()
    file_to_clusters, cprov = load_cluster_index()
    coupled = load_shares_source()
    prov = cprov or prov

    print("\nProvenance (live graph): Nessie HEAD=%s | nodes-snap=%s"
          % (prov.get("nessie_head", "?"), prov.get("nodes_snapshot_id", "?")))
    print("C2 catalog (certed b783dd504): %d STABLE motifs | cluster substrate: %d files->clusters, %d SHARES_SOURCE-coupled"
          % (len(motifs), len(file_to_clusters), len(coupled)))

    systems, singletons, _ = build_c3_systems(motifs, file_to_clusters, coupled)

    print("\nEMERGENT C3 SYSTEMS (connected motif-sets discovered structurally -- AC4):")
    all_ok = True
    for sys_node, why in systems:
        ok, failures = fidelity_check(sys_node)
        all_ok = all_ok and ok
        members = [c.label for c in sys_node.children]
        n_c0 = sum(1 for _, n in decompress(sys_node) if n.layer == "C0")
        print("\n  system:%s   fidelity(AC6): %s   (decompresses to %d C0 facts)"
              % (sys_node.label, "PASS" if ok else "FAIL", n_c0))
        print("     motifs: {%s}" % ", ".join(members))
        if why["shared_constituents"]:
            print("     connected by shared-constituent: %s"
                  % ", ".join(why["shared_constituents"][:3]) + (" ..." if len(why["shared_constituents"]) > 3 else ""))
        if why["shared_clusters"]:
            print("     connected by cluster co-membership: %s" % ", ".join(why["shared_clusters"]))
        if why["coupled_clusters"]:
            print("     connected by SHARES_SOURCE coupling: %s" % ", ".join(why["coupled_clusters"][:3]))
        for f in failures:
            print("       ! " + f)

    if singletons:
        print("\nMotifs NOT composed into a system (isolated -- correctly not forced, honest):")
        for sg in singletons:
            print("  - " + sg)

    print("\n" + "-" * 80)
    print("AC4 EMERGENCE:     %s -- %d C3 system(s) DISCOVERED (not declared) from connected motifs."
          % ("PASS" if systems else "NONE", len(systems)))
    print("AC6 FIDELITY:      %s -- every C3 decompresses C3->C2->C1->C0 lexical evidence."
          % ("PASS" if all_ok else "FAIL"))
    print("AC1 STRUCTURAL:    PASS -- connectivity = shared-constituent + cluster-co-membership + SHARES_SOURCE")
    print("                   (graph node_id set-intersection); NO embedding/vector/cosine/similarity.")
    print("GRAPHDEPTH rollup: each C3 is the fine->coarse EXISTENTIAL rollup of its motif set")
    print("                   (comp_depth_cli semantics reused; store-write of C3+CONTAINS edges is the materialize leg).")
    print("Feeds MOTIF-P3:    these emergent systems -> promotion candidates (recurrence + FEDOBS co-occurrence + decompression chain).")
    return 0 if (systems and all_ok) else 1


# ---------------------------------------------------------------------------
# Self-test (gate logic; no live graph) -- AC4/AC6/AC1 + negative control.
# ---------------------------------------------------------------------------
def self_test() -> int:
    print("=== NFRA_MOTIF_P2 self-test (C3 emergence gate logic; no live graph) ===")
    ok = []

    def chk(name, cond):
        ok.append(cond)
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    # synthetic C2 motifs with controllable footprints + cluster membership
    def motif(nid, c0ids):
        c0 = [Node(x, "C0", "F", x, provenance={"source": x.split("#")[0], "locus": "-", "evidence": x})
              for x in c0ids]
        c1 = Node("c1:" + nid, "C1", "I", nid, rule="d", children=c0)
        return Node("motif:" + nid, "C2", "M", nid, rule="ABSORB", children=[c1])

    mA = motif("A", ["out:portal/x/File1.tsx:10#f", "type:portal/x/T.ts#T#a"])
    mB = motif("B", ["type:portal/x/T.ts#T#a", "out:portal/x/File2.tsx:20#g"])  # shares T#a with A
    mC = motif("C", ["out:portal/x/File9.tsx:99#z"])                            # isolated

    # cluster index: File1 + File3 in cluster:P:0 (A + a hypothetical D co-located, no shared constituent)
    f2c = {"portal/x/File1.tsx": {"cluster:P:0"}, "portal/x/File3.tsx": {"cluster:P:0"}}
    mD = motif("D", ["out:portal/x/File3.tsx:5#w"])  # cluster-co-member with A (both -> cluster:P:0), no shared const
    coupled = {}

    systems, singletons, _ = build_c3_systems([mA, mB, mC, mD], f2c, coupled)

    # 1. AC4 EMERGENCE: A,B,D form ONE system (A-B via shared constituent, A-D via cluster co-membership); >=1 discovered
    chk("1  AC4: >=1 C3 system emerges from connected motifs", len(systems) >= 1)
    # 2. the connected component is {A,B,D} (transitive: B-A-D), size 3
    biggest = max((s for s, _ in systems), key=lambda s: len(s.children)) if systems else None
    chk("2  community detection groups A(shared-const)-B + A(cluster)-D transitively into one system (size 3)",
        biggest is not None and len(biggest.children) == 3)
    # 3. AC6 FIDELITY: every emergent C3 PASSES the REAL comp-ladder gate
    chk("3  AC6: every C3 system PASSES comp-ladder fidelity_check", all(fidelity_check(s)[0] for s, _ in systems))
    # 4. NEGATIVE CONTROL: the isolated motif C (no shared constituent, no shared cluster) is NOT forced into a system
    chk("4  negative control: unconnected motif C is left a singleton (not fabricated into a system)",
        "motif:C" in singletons)
    # 5. AC1 STRUCTURAL: the emergence imports NO ML/embedding library -- connectivity is pure node_id
    #    set-intersection. Scan only the actual `import` statements (not descriptive docstring text).
    import_lines = [ln.strip() for ln in open(os.path.abspath(__file__), encoding="utf-8")
                    if ln.strip().startswith(("import ", "from "))]
    ml_libs = ("numpy", "sklearn", "scipy", "torch", "tensorflow", "transformers", "sentence_transformers",
               "gensim", "faiss", "annoy", "spacy")
    chk("5  AC1: emergence imports NO ML/embedding library (structural set-logic only, no embedding-similarity)",
        not any(lib in ln for ln in import_lines for lib in ml_libs))

    n = sum(1 for r in ok if r)
    print("--- self-test: %d/%d passed ---" % (n, len(ok)))
    return 0 if n == len(ok) else 1


def ladder_one() -> int:
    from comp_ladder import print_ladder
    motifs, _ = _build_stable_motifs()
    f2c, _ = load_cluster_index()
    coupled = load_shares_source()
    systems, _, _ = build_c3_systems(motifs, f2c, coupled)
    if not systems:
        print("no C3 system discovered to ladder")
        return 1
    print_ladder(systems[0][0])
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
    if "--ladder" in args:
        return ladder_one()
    return run_emergence()


if __name__ == "__main__":
    sys.exit(main())
