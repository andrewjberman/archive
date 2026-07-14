#!/usr/bin/env python3
"""NFRA_MOTIF P2 -- the P2-2 CLUSTER CO-MEMBERSHIP connectivity signal (the GO'd build's delta).

BUILDS ON the pre-staged C3-emergence core @ cd022f539 (imports NFRA_MOTIF_P1_c2_catalog; nothing
re-derived): DS~B's prestage proved AC4 emergence with connectivity signal 1 (shared constituents,
substrate-independent) and its own NOTE named the remaining delta -- "the GO'd MOTIF-P2 build ADDS
P2-2's cluster co-membership as a 2nd connectivity signal (enrich, not replace)". P2-2 is now
VERIFIED-LIVE (MOTIF.P0 fold 2026-07-14: 91 PanelCluster nodes + 91 CLUSTERS / 241
CONTAINS_DRILLDOWN / 55 SHARES_SOURCE edges on the canonical graph at HEAD-current vintage), so the
signal is buildable. THIS is that signal:

  two motifs are SIGNAL-2 CONNECTED iff some PanelCluster's member-file set intersects BOTH
  motifs' constituent-file footprints -- the panels the UI actually groups together become an
  independent, structural (never embedding) connectivity witness for motif composition.

The run REPORTS signal-2 components, compares them against signal-1 (the prestage's
shared-constituent systems): CORROBORATED (same membership), NEW (signal-2-only -- fidelity-gated
before it may be called a system), LOST (signal-1-only -- kept; signal 2 enriches, never replaces).
Any NEW system is a candidate for the governed materialize-spec path (motif_c2c3_materialize.json
update -> derive fold), NOT written to the graph here -- req#3-structural + the P1 lifecycle's
zero-auto-mutation posture both hold.

Producer input: s3://opal-313476888478-globgrph/producers/ts-semantic/portal_clusters.json (the
AUTHORITATIVE copy the derive consumed) with the repo extraction copy as a DISCLOSED fallback;
when both are readable their sha256 parity is reported (a silent divergence is how a stale-fixture
verdict happens). Denominators printed for every mapping stage; unmappable motifs are DISCLOSED,
never dropped.

Usage:
  python NFRA_MOTIF_P2_cluster_cosignal.py               # the signal-2 run + comparison verdict
  python NFRA_MOTIF_P2_cluster_cosignal.py --self-test    # hermetic fixture (positive + negative)

Author: 0.8.0_AE_CloudComp~Z (NFRA_MOTIF.P2 per the 2026-07-14 sovereign redirect @14c2aeeba;
builds ON cd022f539). 2026-07-14.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
_GRAPH_DIR = os.path.join(WS, "org", "modules", "graph")
_DS_DELIV = os.path.join(WS, "org", "tier2_senior", "0.4.0_DS_ClientPlatform", "deliverables")
for p in (_GRAPH_DIR, _DS_DELIV):
    if p not in sys.path:
        sys.path.insert(0, p)

_spec = importlib.util.spec_from_file_location(
    "nfra_motif_p1_c2_catalog", os.path.join(_DS_DELIV, "NFRA_MOTIF_P1_c2_catalog.py"))
cat = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cat)   # DS~B's core -- the single source of the catalog + signal 1

from comp_ladder import fidelity_check  # noqa: E402  (the shared AC6 gate -- reference, not rebuilt)

BUCKET = "opal-313476888478-globgrph"
PRODUCER_KEY = "producers/ts-semantic/portal_clusters.json"
REPO_COPY = os.path.join(WS, "org", "modules", "graph", "tsgraph_spike", "out",
                         "portal_clusters.producer.json")

_FILE_RE = re.compile(r"portal/[^\s#:]+?\.(?:tsx|ts)")


def _files_of(ref: str) -> set:
    """Extract portal source-file paths from a constituent / drilldown node id (out:/type:/rc: forms)."""
    return set(_FILE_RE.findall(ref or ""))


def load_producer() -> tuple:
    """(doc, source_label). S3 authoritative; repo copy is the DISCLOSED fallback; parity reported."""
    s3_body = None
    try:
        import boto3
        s3_body = boto3.client("s3", region_name="us-east-1").get_object(
            Bucket=BUCKET, Key=PRODUCER_KEY)["Body"].read()
    except Exception as e:  # noqa: BLE001 -- creds/offline: fall back, DISCLOSED below
        print(f"WARN: S3 producer unreadable ({e.__class__.__name__}) -- falling back to repo copy")
    repo_body = None
    if os.path.exists(REPO_COPY):
        with open(REPO_COPY, "rb") as fh:
            repo_body = fh.read()
    if s3_body is not None and repo_body is not None:
        pa, pb = hashlib.sha256(s3_body).hexdigest()[:12], hashlib.sha256(repo_body).hexdigest()[:12]
        print(f"INFO: producer parity S3={pa} repo={pb} -> {'IDENTICAL' if pa == pb else 'DIVERGED (S3 wins; repo copy is a stale extraction)'}")
    body, src = (s3_body, f"s3://{BUCKET}/{PRODUCER_KEY}") if s3_body is not None else \
                (repo_body, REPO_COPY + " (FALLBACK -- S3 unread this run)")
    if body is None:
        raise RuntimeError("no cluster producer readable (S3 + repo copy both absent) -- "
                           "signal 2 CANNOT run; do not report an empty result as a negative")
    return json.loads(body), src


def cluster_files(doc: dict) -> tuple:
    """PanelCluster id -> member source-file set (from CONTAINS_DRILLDOWN targets).
    THE SIGNAL IS DEFINED ON PanelClusters ONLY ('cluster:' sources -- P2-2's clusters). Nested
    'rc:' drilldown containers also appear as CONTAINS_DRILLDOWN sources (depth>=2 nesting); they
    are EXCLUDED from the signal definition and returned separately for the denominator disclosure
    -- counting them as clusters is the count-of-WHAT error (verification law 6)."""
    out: dict = {}
    nested_excluded = 0
    for e in doc.get("edges", []):
        if e.get("edge_type") == "CONTAINS_DRILLDOWN":
            src = e.get("source", "")
            if src.startswith("cluster:"):
                out.setdefault(src, set()).update(_files_of(e.get("target", "")))
            else:
                nested_excluded += 1
    return out, nested_excluded


def build_motif_footprints() -> tuple:
    """(motif_nid -> constituent-file set, motifs list) via DS~B's core -- catalog + AC3 gate mirrored."""
    motifs = []
    for spec in cat.CATALOG:
        motif, recurrence, _ = cat.build_motif(spec)
        if recurrence >= cat.AC3_THRESHOLD:
            motifs.append(motif)
    foot = {}
    for m in motifs:
        files = set()
        for ref in cat.motif_constituents(m):
            files |= _files_of(ref)
        foot[m.nid] = files
    return foot, motifs


def signal2_components(foot: dict, clusters: dict) -> tuple:
    """Union-find motifs by cluster co-membership. Returns (components >=2, singletons, witnesses)
    where witnesses[(a,b)] = the cluster ids connecting the pair (the inspectable 'why')."""
    ids = sorted(foot)
    parent = {i: i for i in ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    witnesses: dict = {}
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            shared = [cid for cid, files in clusters.items()
                      if (files & foot[a]) and (files & foot[b])]
            if shared:
                witnesses[(a, b)] = sorted(shared)
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[ra] = rb
    comps: dict = {}
    for i in ids:
        comps.setdefault(find(i), []).append(i)
    systems = sorted([sorted(v) for v in comps.values() if len(v) >= 2])
    singletons = sorted(v[0] for v in comps.values() if len(v) == 1)
    return systems, singletons, witnesses


def run() -> int:
    print("=" * 78)
    print("NFRA_MOTIF P2 -- cluster co-membership (signal 2; builds ON cd022f539, enrich-not-replace)")
    print("=" * 78)
    doc, src = load_producer()
    clusters, nested_excluded = cluster_files(doc)
    foot, motifs = build_motif_footprints()
    n_files = len(set().union(*clusters.values())) if clusters else 0
    print(f"producer: {src}")
    print(f"denominators: {len(clusters)} PanelClusters ('cluster:' sources ONLY; {nested_excluded} "
          f"nested 'rc:' drilldown-container edges EXCLUDED from the signal definition) -> "
          f"{n_files} distinct member files; {len(foot)} stable motifs (AC3-gated)")
    unmapped = sorted(m for m, files in foot.items() if not files)
    if unmapped:
        print(f"DISCLOSED: {len(unmapped)} motif(s) with NO file-mappable constituents "
              f"(cannot participate in signal 2, NOT dropped from the record): {unmapped}")

    s2, singles, wit = signal2_components(foot, clusters)
    print(f"\nSIGNAL-2 components (cluster co-membership): {len(s2)}")
    for members in s2:
        print("  {%s}" % ", ".join(m.split(":", 1)[1] for m in members))
        for (a, b), cids in sorted(wit.items()):
            if a in members and b in members:
                print("     witness %s <-> %s via cluster(s): %s"
                      % (a.split(':', 1)[1], b.split(':', 1)[1], ", ".join(cids[:4])))

    # signal 1 (the prestage's shared-constituent systems) via DS~B's core, for the comparison.
    s1_nodes, s1_singletons = cat.build_c3_systems(motifs)
    s1 = sorted([sorted(c.nid for c in s.children) for s in s1_nodes])
    print(f"\nSIGNAL-1 components (shared constituents, the prestage): {len(s1)}")

    corroborated = [m for m in s2 if m in s1]
    new = [m for m in s2 if m not in s1]
    only_s1 = [m for m in s1 if m not in s2]
    print("\nVERDICT (enrich-not-replace):")
    print(f"  CORROBORATED (both signals agree): {len(corroborated)} -> {corroborated}")
    print(f"  NEW under signal 2 only:           {len(new)} -> {new}")
    print(f"  signal-1-only (KEPT -- signal 2 never removes a system): {len(only_s1)} -> {only_s1}")

    all_fid = True
    if new:
        print("\nNEW candidate systems are FIDELITY-GATED before the word 'system' applies (AC6):")
        by_nid = {m.nid: m for m in motifs}
        for members in new:
            node = cat.Node(
                cat.system_node_id("cluster-co-membership", members), "C3", "EmergentSystem",
                "cluster-co-membership",
                rule="C3 EMERGENCE (signal 2): motifs {%s} co-member in cluster(s) %s -> capability"
                     % (", ".join(m.split(":", 1)[1] for m in members),
                        ", ".join(sorted({c for (a, b), cs in wit.items()
                                          for c in cs if a in members and b in members})[:3])),
                children=[by_nid[m] for m in members])
            ok, failures = fidelity_check(node)
            all_fid = all_fid and ok
            print("  %s fidelity(AC6): %s" % (node.nid, "PASS" if ok else "FAIL"))
            for f in failures:
                print("    ! " + f)
        print("  route: a PASSING new system goes to the GOVERNED materialize-spec path "
              "(motif_c2c3_materialize.json update -> derive fold) -- NOT written here.")
    out = {
        "producer_source": src, "denominators": {"clusters": len(clusters),
                                                 "cluster_files": n_files, "stable_motifs": len(foot)},
        "signal2_components": s2, "signal2_singletons": singles,
        "signal1_components": s1,
        "verdict": {"corroborated": corroborated, "new_signal2_only": new,
                    "signal1_only_kept": only_s1},
        "unmapped_motifs_disclosed": unmapped,
    }
    out_path = os.path.join(_HERE, "motif_p2_cluster_cosignal.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(f"\nOK: wrote {os.path.relpath(out_path, WS)}")
    return 0 if all_fid else 1


# ---------------------------------------------------------------------------
# Self-test -- hermetic fixture; the signal must FIRE on a wired fixture and STAY SILENT on a
# disjoint one (a connectivity signal that cannot distinguish the two measures nothing).
# ---------------------------------------------------------------------------
def self_test() -> int:
    print("=== NFRA_MOTIF_P2_cluster_cosignal self-test (hermetic) ===")
    ok = []

    def chk(name, cond):
        ok.append(bool(cond))
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))

    foot = {"motif:a": {"portal/src/pages/X.tsx"}, "motif:b": {"portal/src/pages/Y.tsx"},
            "motif:c": {"portal/src/pages/Z.tsx"}}
    # positive: one cluster spans X+Y -> {a,b} composes; c stays single.
    clusters = {"cluster:P:0": {"portal/src/pages/X.tsx", "portal/src/pages/Y.tsx"}}
    s2, singles, wit = signal2_components(foot, clusters)
    chk("positive: a cluster spanning two motifs' files composes exactly {a,b}",
        s2 == [["motif:a", "motif:b"]] and singles == ["motif:c"])
    chk("witness carried: the connecting cluster id is on the record",
        wit.get(("motif:a", "motif:b")) == ["cluster:P:0"])
    # negative control: disjoint clusters -> NO systems (the signal can stay silent).
    s2n, singlesn, witn = signal2_components(foot, {"cluster:P:1": {"portal/src/pages/W.tsx"}})
    chk("negative control: disjoint clusters compose NOTHING (3 singletons, 0 witnesses)",
        s2n == [] and len(singlesn) == 3 and witn == {})
    # the signal definition excludes nested rc: containers (count-of-WHAT discipline).
    cf, nx = cluster_files({"edges": [
        {"edge_type": "CONTAINS_DRILLDOWN", "source": "cluster:P:0",
         "target": "rc:portal/src/pages/X.tsx#A"},
        {"edge_type": "CONTAINS_DRILLDOWN", "source": "rc:portal/src/pages/X.tsx#A",
         "target": "rc:portal/src/pages/Y.tsx#B"}]})
    chk("definition: 'cluster:' sources only; nested 'rc:' container edges excluded + counted",
        list(cf) == ["cluster:P:0"] and nx == 1)
    # file extraction handles all three ref forms.
    chk("ref parsing: out:/type:/rc: forms all yield the file",
        _files_of("out:portal/src/pages/X.tsx:291#name") == {"portal/src/pages/X.tsx"}
        and _files_of("type:portal/src/pages/t.ts#T#f") == {"portal/src/pages/t.ts"}
        and _files_of("rc:portal/src/pages/X.tsx#Comp") == {"portal/src/pages/X.tsx"})
    n = sum(1 for x in ok if x)
    print("--- self-test: %d/%d passed ---" % (n, len(ok)))
    return 0 if n == len(ok) else 1


def main() -> int:
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass
    if "--self-test" in sys.argv[1:]:
        return self_test()
    return run()


if __name__ == "__main__":
    sys.exit(main())
