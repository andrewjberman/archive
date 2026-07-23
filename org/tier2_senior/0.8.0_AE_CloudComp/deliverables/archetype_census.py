#!/usr/bin/env python3
"""NFRA_TOOLARCH.P1 archetype census -- dogfood the C0-C3 ladder on the live estate.
INTENT sourced from the ratified rule bank (governing artifact, above the graph).
DENOMINATOR enumerated from the live comp-kuzu graph at run time.
GAP = INTENT \\ DENOMINATOR and DENOMINATOR \\ INTENT, printed per plane.
Author: 0.8.0_AE_CloudComp~D. Read-only; queries comp-kuzu, parses the rule bank.
"""

from __future__ import annotations
import argparse
import json
import subprocess
import collections
import yaml
import sys
import os

WS = r"C:\Users\AndrewBerman\Desktop\ajb_workspace"
RULEBANK_PATH = "org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml"  # repo-relative (for git show)
RULEBANK = os.path.join(WS, *RULEBANK_PATH.split("/"))
KUZU = os.path.join(WS, ".tools", "comp-kuzu")
# Build vintage: the rule bank (INTENT) this census parsed. VINTAGE-FRAGILE by design --
# as ONTOLOGY2 adds binds_up entries the unmapped count shrinks toward 0, so a working-tree
# re-run reproduces a SMALLER boundary, not a wrong one. --rule-bank-ref pins the INTENT surface
# so the 11-type boundary is reproducible at the vintage it was measured (CVO~Z verify rec, @374db63d6).
BUILD_RULEBANK_REF = "f38a386a6"
sys.path.insert(0, os.path.join(WS, ".tools"))
from git_bash_resolver import git_bash  # noqa: E402  canonical Git-Bash path (NEVER bare bash -> WSL stub)

BASH = git_bash()

_ap = argparse.ArgumentParser(description="NFRA_TOOLARCH.P1 archetype census")
_ap.add_argument(
    "--rule-bank-ref",
    default=BUILD_RULEBANK_REF,
    help="git ref to read the rule bank (INTENT) from; '' or 'worktree' reads the working tree "
    "(live number, tracks ONTOLOGY2 closure). Default pins the build vintage %s so the "
    "measured boundary is reproducible." % BUILD_RULEBANK_REF,
)
ARGS, _ = _ap.parse_known_args()


def load_rulebank():
    """INTENT surface. Pinned to a git ref by default (reproducible); worktree on request (live)."""
    ref = (ARGS.rule_bank_ref or "").strip()
    if ref in ("", "worktree", "working-tree", "HEAD-worktree"):
        sys.stderr.write("[rule-bank] INTENT = WORKING TREE (live; unmapped count tracks ONTOLOGY2 closure)\n")
        return yaml.safe_load(open(RULEBANK, encoding="utf-8"))
    # read via git show <ref>:<path> -- bare-sha ref + no dot-leading path component => no MSYS mangle
    out = subprocess.run(
        [BASH, "-c", "git show %s:%s" % (ref, RULEBANK_PATH)],
        capture_output=True, text=True, cwd=WS,
    )
    if out.returncode != 0 or not out.stdout.strip():
        # positive-control note: a slashed/dot ref can mangle to a clean-empty stdout (CLAUDE.md git rule)
        sys.stderr.write("[rule-bank] git show %s:%s FAILED (rc=%d): %s\n" % (ref, RULEBANK_PATH, out.returncode, out.stderr[:200]))
        sys.exit(2)
    sys.stderr.write("[rule-bank] INTENT pinned @ %s (reproducible build vintage)\n" % ref)
    return yaml.safe_load(out.stdout)


def kq(cypher):
    """Run a comp-kuzu query, return list-of-dicts (JSON mode). Strips provenance header."""
    out = subprocess.run(
        [BASH, KUZU, "--json", cypher], capture_output=True, text=True, cwd=WS
    )
    txt = out.stdout
    # JSON array starts at first '['
    i = txt.find("[")
    if i < 0:
        sys.stderr.write("QUERY FAILED:\n" + out.stdout[:500] + out.stderr[:500])
        return []
    return json.loads(txt[i:])


# ---------------------------------------------------------------- INTENT: rule bank
rb = load_rulebank()
ROLES = list(rb["roles"].keys())  # 14
RELATIONS = rb["relations"]  # 10 abstract
COMPOSITES = rb["relation_composites"]  # 3
NONREL = rb["non_relation_edges"]  # 8
NODE_BIND = rb["node_bindings"]  # node_type -> role (fixed)
CONTEXTUAL = set(rb["contextual_types"])
SCOPE_OUT = set(rb["scope_outs"].keys()) | set(NODE_BIND.get("scope_out", []))

# mapped edge set (INTENT for C1): every concrete edge_type the ontology claims to cover
mapped_edges = {}  # edge_type -> how it is mapped
for rel, spec in RELATIONS.items():
    for et in spec.get("binds_up", []):
        mapped_edges[et] = f"relation:{rel}"
for comp, spec in COMPOSITES.items():
    if spec.get("concrete"):
        mapped_edges[spec["concrete"]] = f"composite:{comp}"
    for et in spec.get("also", []):
        mapped_edges[et] = f"composite:{comp}.also"
for et, spec in NONREL.items():
    mapped_edges[et] = f"non_relation:{spec.get('axis') or spec.get('binds_up') or '?'}"

# node_type -> role (fixed bindings only; contextual/scope_out handled separately)
nt_role = {}
for role, nts in NODE_BIND.items():
    if role in ("contextual", "scope_out"):
        continue
    for nt in nts:
        nt_role[nt] = role

# ---------------------------------------------------------------- PLANE MAP (grounded in motif catalog)
PLANE = {}


def setp(names, p):
    for n in names:
        PLANE[n] = p


setp(
    [
        "S3_BUCKET",
        "S3Key",
        "LAMBDA",
        "EC2_INSTANCE",
        "DYNAMODB_TABLE",
        "KMS_KEY",
        "IAM_ROLE",
        "IAM_POLICY",
        "IAM_USER",
        "IAM_STATEMENT",
        "S3_BUCKET_POLICY",
        "SECURITY_GROUP",
        "EVENT_RULE",
        "EVENT_SOURCE",
        "SCHEDULE",
        "CW_ALARM",
        "STATE_MACHINE",
        "API_GW",
        "API_ROUTE",
        "Endpoint",
        "ServedURL",
        "CLOUDFRONT_DISTRIBUTION",
        "SNS_TOPIC",
        "SQS_QUEUE",
        "SECRET",
        "SECRETREF",
        "LOG_GROUP",
        "LAMBDA_LAYER",
        "INSTANCE_PROFILE",
        "SERVICE_PRINCIPAL",
        "SSM_DOCUMENT",
        "ECS_TASK_DEFINITION",
        "ECS_CLUSTER",
        "ROUTE53_RECORD",
        "VPC_ENDPOINT",
        "CODEBUILD_PROJECT",
        "LOAD_BALANCER",
    ],
    "AWS",
)
setp(["Pipeline", "PipelineScript", "PipelineFunction"], "pipeline")
setp(
    [
        "JSXElement",
        "JSXRender",
        "ReactComponent",
        "Component",
        "Prop",
        "TypeDecl",
        "Hook",
        "DataFetch",
        "PanelCluster",
        "Page",
        "ReactQueryKey",
    ],
    "frontend",
)
setp(["MS_FILE", "MS_FOLDER", "MS_USER", "MS_SITE", "MS_LIBRARY"], "M365")
setp(["C2Motif", "C3System"], "records")
# CROSS-PLANE (resolved by edges below): Field, Module

# ---------------------------------------------------------------- DENOMINATOR: live graph
nodes = kq("MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS n ORDER BY n DESC")
edges = kq(
    "MATCH ()-[e:CloudEdge]->() RETURN e.edge_type AS t, count(*) AS n ORDER BY n DESC"
)
nt_count = {r["t"]: r["n"] for r in nodes}
et_count = {r["t"]: r["n"] for r in edges}
TOTAL_N = sum(nt_count.values())
TOTAL_E = sum(et_count.values())


# resolve Field/Module plane by dominant incident-neighbour plane
def resolve_cross(nt):
    rows = kq(
        f"MATCH (a:CloudNode)-[e:CloudEdge]-(b:CloudNode) WHERE a.node_type='{nt}' "
        f"RETURN b.node_type AS nb, count(*) AS n"
    )
    tally = collections.Counter()
    for r in rows:
        p = PLANE.get(r["nb"])
        if p and p != "records":
            tally[p] += r["n"]
    return tally


for nt in ["Field", "Module"]:
    if nt in nt_count:
        t = resolve_cross(nt)
        PLANE[nt] = t.most_common(1)[0][0] if t else "frontend"
        PLANE[nt + "__crosstally"] = dict(t)

# ============================================================ C0: ROLE CENSUS per plane
print("=" * 78)
print(
    "C0 -- ROLE CENSUS  (denominator: %d nodes / %d node_types, vintage pinned in header)"
    % (TOTAL_N, len(nt_count))
)
print("=" * 78)
role_by_plane = collections.defaultdict(lambda: collections.Counter())
unbound = collections.Counter()
contextual_n = collections.Counter()
scopeout_n = collections.Counter()
planes_order = ["AWS", "pipeline", "frontend", "M365", "records"]
for nt, c in nt_count.items():
    p = PLANE.get(nt, "UNPLANED")
    if nt in SCOPE_OUT:
        scopeout_n[p] += c
        continue
    if nt in CONTEXTUAL:
        contextual_n[p] += c
        continue
    r = nt_role.get(nt)
    if r:
        role_by_plane[p][r] += c
    else:
        unbound[p] += c
# roles present:
allroles = collections.Counter()
for p, cc in role_by_plane.items():
    for r, c in cc.items():
        allroles[r] += c
print("\nROLES OCCURRING (of 14 closed):", len(allroles), "of 14")
for r in ROLES:
    print(
        f"  {allroles.get(r, 0):>7}  {r}"
        + ("" if r in allroles else "   <-- ZERO fixed-bound instances")
    )
print("\nPER-PLANE role totals (fixed-bound nodes only):")
for p in planes_order:
    tot = sum(role_by_plane[p].values())
    print(
        f"  [{p}] {tot} role-bound nodes: "
        + ", ".join(f"{r}={c}" for r, c in role_by_plane[p].most_common())
    )
print("\nC0 COVERAGE DENOMINATOR (every node accounted):")
sb = sum(sum(cc.values()) for cc in role_by_plane.values())
print(f"  fixed-role-bound : {sb}")
print(
    f"  contextual (per-instance, NOT statically bound): {sum(contextual_n.values())}  "
    + ", ".join(f"{p}={c}" for p, c in contextual_n.items())
)
print(
    f"  scope-out (no role BY DESIGN -- D8 type axis): {sum(scopeout_n.values())}  "
    + ", ".join(f"{p}={c}" for p, c in scopeout_n.items())
)
print(
    f"  unbound tail (node_type with NO adapter binding -- C0 GAP): {sum(unbound.values())}  "
    + ", ".join(f"{p}={c}" for p, c in unbound.items() if c)
)
unbound_types = [
    nt
    for nt in nt_count
    if nt not in SCOPE_OUT and nt not in CONTEXTUAL and nt not in nt_role
]
print(f"  unbound node_types: {sorted(unbound_types)}")
print(
    f"  CHECK sum = {sb + sum(contextual_n.values()) + sum(scopeout_n.values()) + sum(unbound.values())} vs TOTAL {TOTAL_N}"
)

# ============================================================ C1: RELATION CENSUS + coverage boundary
print("\n" + "=" * 78)
print(
    "C1 -- RELATION CENSUS  (denominator: %d edges / %d edge_types)"
    % (TOTAL_E, len(et_count))
)
print("=" * 78)
# map each live edge to its relation
rel_total = collections.Counter()
live_unmapped = {}  # edge_type -> count  (DIRECTION 1)
for et, c in et_count.items():
    m = mapped_edges.get(et)
    if m is None:
        live_unmapped[et] = c
    else:
        rel_total[m] += c
print("\nABSTRACT RELATIONS carrying live edges (of 10) + composites/non-relation:")
for m, c in rel_total.most_common():
    print(f"  {c:>7}  {m}")
print(
    "\n>> DIRECTION 1 -- LIVE BUT UNMAPPED (the C1 coverage boundary; reconciles tick-29):"
)
tot_un = sum(live_unmapped.values())
for et, c in sorted(live_unmapped.items(), key=lambda x: -x[1]):
    print(f"  {c:>7}  {et}")
print(
    f"  UNMAPPED: {len(live_unmapped)} edge_types / {tot_un} edges = {100 * tot_un / TOTAL_E:.1f}% of live edge mass"
)
# DIRECTION 2 -- declared but zero-live
declared = set(mapped_edges.keys())
live = set(et_count.keys())
zero_live = sorted(declared - live)
print("\n>> DIRECTION 2 -- DECLARED BUT ZERO-LIVE-IN-PLANE (kuzu canonical surface):")
for et in zero_live:
    print(f"        0  {et}   ({mapped_edges[et]})")
print(f"  ZERO-LIVE: {len(zero_live)} declared edge_types absent from the kuzu plane")
# per-plane unmapped: attribute unmapped edges to plane by endpoints
print(
    "\n>> DIRECTION 1 per-plane (attribute each unmapped edge by its dominant endpoint plane):"
)
for et in live_unmapped:
    rows = kq(
        f"MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type='{et}' "
        f"RETURN a.node_type AS at, b.node_type AS bt LIMIT 1"
    )
    if rows:
        at, bt = rows[0]["at"], rows[0]["bt"]
        pa, pb = PLANE.get(at, "?"), PLANE.get(bt, "?")
        print(f"  {live_unmapped[et]:>7}  {et:<16} {at}({pa}) -> {bt}({pb})")

# ============================================================ C2: MOTIF CENSUS + boundary
print("\n" + "=" * 78)
print("C2 -- MOTIF CENSUS  (materialized C2Motif nodes vs ~20 canonical family target)")
print("=" * 78)
c2 = kq(
    "MATCH (n:CloudNode) WHERE n.node_type='C2Motif' RETURN n.name AS name, n.props AS props"
)
fam = []
for r in c2:
    p = json.loads(r["props"])
    fam.append(
        (
            r["name"],
            p.get("recurrence", 0),
            p.get("tier", "?"),
            p.get("catalog_class", "?"),
        )
    )
canon = [f for f in fam if f[2] == "canonical"]
debt = [f for f in fam if f[2] != "canonical"]
print(
    f"\nMATERIALIZED: {len(fam)} C2Motif nodes = {len(canon)} canonical + {len(debt)} debt/gate"
)
print("CANONICAL (tier=canonical), by recurrence:")
for n, rec, t, cl in sorted(canon, key=lambda x: -x[1]):
    print(f"  {rec:>6}  {n}")
print("DEBT / gate motifs:")
for n, rec, t, cl in sorted(debt, key=lambda x: -x[1]):
    print(f"  {rec:>6}  {n:<24} tier={t} class={cl}")
# which planes are materialized: A/B built, C/D not
print(
    "\n>> C2 COVERAGE BOUNDARY: canonical catalog = ~21 families (9 A + 4 B + 7 C + 1 D)."
)
print(
    "   Materialized A+B motif nodes present; C (frontend) + D (M365) canonical families NOT materialized as C2Motif nodes."
)

# ============================================================ C3: SYSTEM CENSUS
print("\n" + "=" * 78)
print("C3 -- SYSTEM CENSUS  (union-find over connected motifs)")
print("=" * 78)
c3 = kq(
    "MATCH (s:CloudNode)-[e:CloudEdge]->(m:CloudNode) WHERE s.node_type='C3System' AND m.node_type='C2Motif' RETURN s.name AS sys, m.name AS motif"
)
g = collections.defaultdict(list)
for r in c3:
    g[r["sys"]].append(r["motif"])
systematized = set()
for s, ms in g.items():
    print(f"  {s} ({len(ms)}): {', '.join(ms)}")
    systematized |= set(ms)
all_motifs = {f[0] for f in fam}
unsys = sorted(all_motifs - systematized)
print(
    f"\n>> C3 COVERAGE BOUNDARY: {len(systematized)} of {len(all_motifs)} motifs systematized; UNSYSTEMATIZED ({len(unsys)}): {unsys}"
)
print(
    "   (note: highest-recurrence canonical motifs among the unsystematized are the sharpest C3 gap.)"
)
