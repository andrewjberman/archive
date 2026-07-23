#!/usr/bin/env python3
"""NFRA_TOOLARCH.CANON -- audit every comp-tool's DATA SOURCE: comp-kuzu canonical vs a floating json.
Mechanical pass: resolve each wrapper's backing python, scan for kuzu-graph signals and every .json it
READS (not writes). Judgment (projection-vs-config-vs-fixture) applied in the report. Denominator printed.
Author: 0.8.0_AE_CloudComp~D. Read-only.
"""

from __future__ import annotations
import os
import re
import glob

WS = r"C:\Users\AndrewBerman\Desktop\ajb_workspace"
TOOLS = os.path.join(WS, ".tools")

# ACTUAL kuzu data-source use (not a docstring mention of comp-kuzu). Any ONE of these = reads canonical.
KUZU_ACTUAL_RE = re.compile(
    r"import kuzu|kuzu\.Database|kuzu\.Connection|kuzu_nessie_db|KUZU_DB|"
    r"kuzu_cli|kuzu_load|\bconn\.execute\(|_run_cypher|run_cypher|from kuzu",
    re.I,
)
# subprocess shelling to comp-kuzu (canonical via the wrapper)
KUZU_SHELL_RE = re.compile(
    r"""["']comp-kuzu["']|comp-kuzu[^"']*["']\s*,|subprocess.*comp-kuzu"""
)
# every .json filename referenced ANYWHERE (path assignment, open, load) -- captured regardless of line
JSON_NAME_RE = re.compile(r"""([A-Za-z0-9_.-]+\.json)""")
# live-aws signal
AWS_RE = re.compile(
    r"boto3|check_output.*aws|['\"]aws['\"]|aws s3|aws iam|aws lambda", re.I
)


def backing_of(wrapper):
    """Extract the primary backing python invoked by a wrapper script (skip comp_log_auto)."""
    try:
        txt = open(wrapper, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    bks = []
    for m in re.finditer(r'python[0-9.]*\s+"?([^"\n]*?\.py)"?', txt):
        p = m.group(1)
        if "comp_log_auto" in p:
            continue
        p = p.replace("${WORKSPACE}", WS).replace("$WORKSPACE", WS).replace('"', "")
        p = p.replace("{WORKSPACE}", WS)
        if not os.path.isabs(p):
            # try relative to WS
            cand = os.path.join(WS, p)
            if os.path.exists(cand):
                p = cand
        bks.append(p)
    return bks


def scan(pyfile):
    """Return (reads_kuzu, [json_files_referenced], reads_aws) for a backing python."""
    if not os.path.exists(pyfile):
        return (None, [], None)  # unresolved
    txt = open(pyfile, encoding="utf-8", errors="replace").read()
    reads_kuzu = bool(KUZU_ACTUAL_RE.search(txt) or KUZU_SHELL_RE.search(txt))
    reads_aws = bool(AWS_RE.search(txt))
    jsons = set()
    # every .json filename referenced anywhere EXCEPT pure S3-key/output-write contexts.
    # We capture references; classification (source vs write vs config) is applied in the report.
    for line in txt.splitlines():
        s = line.strip()
        if s.startswith("#"):
            continue
        if ".json" not in line:
            continue
        # skip lines that only WRITE a json (open(...,'w'), json.dump, f-string s3 keys we emit)
        if re.search(r"json\.dump|open\([^)]*['\"]w['\"]|\.write_text\(", line):
            continue
        for jm in JSON_NAME_RE.finditer(line):
            fn = jm.group(1)
            # ignore obvious per-record/templated keys ({...}.json, f-string keys)
            if "{" in line[max(0, line.find(fn) - 3) : line.find(fn)]:
                continue
            jsons.add(fn)
    return (reads_kuzu, sorted(jsons), reads_aws)


wrappers = []
for w in sorted(glob.glob(os.path.join(TOOLS, "comp-*"))) + [
    os.path.join(TOOLS, "pipescript")
]:
    b = os.path.basename(w)
    if b.endswith((".py", ".sh")):
        continue
    wrappers.append(w)

rows = []
for w in wrappers:
    name = os.path.basename(w)
    bks = backing_of(w)
    if not bks:
        rows.append((name, "INLINE/NO-PY", False, [], False))
        continue
    agg_kuzu = False
    agg_aws = False
    agg_json = set()
    unresolved = False
    for bk in bks:
        k, js, a = scan(bk)
        if k is None:
            unresolved = True
            continue
        agg_kuzu = agg_kuzu or k
        agg_aws = agg_aws or a
        agg_json |= set(js)
    label = os.path.relpath(bks[0], WS) if bks else "?"
    rows.append(
        (
            name,
            label if not unresolved else label + " (UNRESOLVED)",
            agg_kuzu,
            sorted(agg_json),
            agg_aws,
        )
    )

# GRAPH/ESTATE PROJECTION jsons (a snapshot substituting for the canonical graph) -- ground-verified
PROJECTION = {
    "estate-coverage-resolver.json",  # pipescript/pipeline_cli -- frozen manifest, silently stale (EXHIBIT)
    "graph.json",  # cli.py trace-graph cache -- source-scan, kuzu re-point DEFERRED (cli.py:56)
    "stitch_graph.json",  # cross-layer stitch (upstream producer of kuzu; also read by comp-graph)
    "portal_full.graph.json",
    "portal_full.producer.json",
}
# LOUD-VINTAGE derived artifacts -- the ACCEPTED exception (read but discloses age on every number)
LOUD_VINTAGE = {"nerves-risk-edges.json", "nerves-edges.json"}
CONFIG_SOR = {  # source-of-record configs -- legitimate non-graph authorities
    "EC2_MANIFEST.json",
    "lambda-source-map.json",
    "firm_registry.json",
    "comp-tools.json",
    "package.json",
    "tsconfig.json",
    "settings.json",
}
# arg/test/output json names (argparse namespace, diff baselines, scratch) -- NOT data sources
ARGLIKE = {
    "args.json",
    "baseline.json",
    "a.json",
    "s.json",
    "foo.json",
    "dropme.json",
    "key.json",
    "missing.json",
    "fresh.json",
    "cols.json",
}


def classify_jsons(js):
    proj = [j for j in js if j in PROJECTION]
    loud = [j for j in js if j in LOUD_VINTAGE]
    cfg = [j for j in js if j in CONFIG_SOR]
    other = [
        j
        for j in js
        if j not in PROJECTION
        and j not in CONFIG_SOR
        and j not in ARGLIKE
        and j not in LOUD_VINTAGE
    ]
    return proj, loud, cfg, other


print("=" * 100)
print(
    "TOOL DATA-SOURCE AUDIT -- denominator = %d wrapped comp-tools (+pipescript)"
    % len(rows)
)
print("=" * 100)
n_kuzu = n_proj = n_loud = n_inline = 0
proj_tools = []
for name, backing, kuzu, jsons, aws in rows:
    proj, loud, cfg, other = classify_jsons(jsons)
    tags = []
    if proj:
        tags.append("FLOATING-JSON-PROJECTION:" + ",".join(proj))
        n_proj += 1
        proj_tools.append((name, proj, kuzu))
    elif kuzu:
        tags.append("KUZU-CANONICAL")
        n_kuzu += 1
    if loud:
        tags.append("LOUD-VINTAGE:" + ",".join(loud))
        n_loud += 1
    if aws and not kuzu and not proj:
        tags.append("LIVE-AWS")
    if backing == "INLINE/NO-PY":
        tags.append("INLINE")
        n_inline += 1
    tagstr = (
        " ".join(tags) if tags else "(no graph/json data-source signal -- util/config)"
    )
    print(f"  {name:<24} {tagstr}")

print("\n" + "=" * 100)
print("ROLLUP (denominator %d wrapped tools):" % len(rows))
print(f"  FLOATING-JSON PROJECTION (audit target) : {n_proj}")
print(f"  LOUD-VINTAGE derived (ACCEPTED exception): {n_loud}")
print(f"  KUZU-CANONICAL (only)                    : {n_kuzu}")
print(f"  inline/util/config/live-aws              : {len(rows) - n_proj - n_kuzu}")
print("\nFLOATING-JSON-PROJECTION TOOLS (derived set, ground-verified projections):")
for name, proj, kuzu in proj_tools:
    print(
        f"  {name:<24} <- {','.join(proj)}   {'(+kuzu too)' if kuzu else '(NOT kuzu)'}"
    )
