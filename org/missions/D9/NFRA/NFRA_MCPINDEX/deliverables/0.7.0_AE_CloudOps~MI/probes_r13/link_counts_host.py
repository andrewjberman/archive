"""link_counts_host.py -- runs ON the gateway host under /opt/opal-gateway/.venv/bin/python (the only place the
gateway's deps exist). MX-r-12 PHASE A, amendment A1. READ-ONLY: reads /opt/opal-gateway and two /tmp files
shipped beside it; writes nothing, touches no served path, opens no socket.

Computes MC Portal's per-tool catalog link counts for TWO trees, by the SAME mechanism on both sides so the
numbers are comparable: it extracts each tree's OWN `_catalog_read_tool_rows` source and execs it with that
tree's OWN catalog path bound to CATALOG_YAML. Importing the module wholesale is not an option for the cut
(its tree is not on this box), so the live side carries a CONTROL: the same count taken by importing the real
installed module, which must agree with the exec'd form or the mechanism is not trustworthy.

Inputs, all absolute paths:
  argv[1] LIVE reader source   (expected: /opt/opal-gateway/app/admin_gateway_breakdown.py)
  argv[2] LIVE catalog         (expected: /opt/opal-gateway/app/refs/DATA_CATALOG.yaml)
  argv[3] CUT reader source    (shipped to /tmp)
  argv[4] CUT catalog          (shipped to /tmp)
"""

import ast
import os
import sys

FUNC = "_catalog_read_tool_rows"


def reader_counts(reader_src_path, catalog_path):
    """Exec ONLY that file's _catalog_read_tool_rows, with CATALOG_YAML bound to catalog_path."""
    src = open(reader_src_path, encoding="utf-8").read()
    tree = ast.parse(src)
    fn = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == FUNC:
            fn = node
            break
    if fn is None:
        raise SystemExit("ERROR: %s not found in %s" % (FUNC, reader_src_path))
    ns = {"CATALOG_YAML": catalog_path}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), reader_src_path, "exec"), ns)
    rows = ns[FUNC]()
    return {t: len(ids) for t, ids in rows.items()}, fn.lineno


def emit(tag, counts, lineno, reader, catalog):
    total = sum(counts.values())
    print("---%s reader=%s:%d catalog=%s" % (tag, reader, lineno, catalog))
    for t in sorted(counts):
        print("%s TOOL %s %d" % (tag, t, counts[t]))
    print("---%s TOTALS tools=%d links=%d" % (tag, len(counts), total))
    return counts


live_reader, live_cat, cut_reader, cut_cat = sys.argv[1:5]

live, live_ln = reader_counts(live_reader, live_cat)
emit("LIVE", live, live_ln, live_reader, live_cat)

cut, cut_ln = reader_counts(cut_reader, cut_cat)
emit("CUT", cut, cut_ln, cut_reader, cut_cat)

# CONTROL: the live side, taken by importing the REAL installed module. Must agree with the exec'd form.
ctl = "SKIPPED"
try:
    sys.path.insert(0, "/opt/opal-gateway")
    os.chdir("/opt/opal-gateway")
    from app import admin_gateway_breakdown as agb

    real = {t: len(ids) for t, ids in agb._catalog_read_tool_rows().items()}
    ctl = "AGREE" if real == live else "DISAGREE real=%r exec=%r" % (sorted(real.items()), sorted(live.items()))
except Exception as e:
    ctl = "EXC %s: %s" % (type(e).__name__, e)
print("---CONTROL exec-vs-real-import %s" % ctl)

# The comparison A1 asks for: per-tool EQUALITY, and the difference if any.
added = sorted(set(cut) - set(live))
removed = sorted(set(live) - set(cut))
moved = sorted(t for t in (set(cut) & set(live)) if cut[t] != live[t])
print("---DIFF tools_added=%r tools_removed=%r counts_changed=%r" % (added, removed, moved))
for t in moved:
    print("---DIFF TOOL %s live=%d cut=%d" % (t, live[t], cut[t]))
print("---VERDICT per_tool_link_counts %s" % ("EQUAL" if not (added or removed or moved) else "DIFFER"))
