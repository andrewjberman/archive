#!/usr/bin/env python3
"""i2_fixture -- shared harness for TO-CG-I-2 (CG-s-43).

GRAIN: this harness does NOT transcribe the producer's dangling predicate. It loads
`infra/aws/globgrph/derive_stitch.py` AS A MODULE and calls the real
`build_stitched_graph()`, so the number graded is the producer's own
`meta["genuine_dangling"]` computed by the producer's own code. The only things
replaced are the three INPUT loaders (`load_aws_layer`, `portal.build_portal_stitch_graph`,
`T.build_graph`), which are the egress-bearing ones -- nothing in this harness reads S3,
runs a task, builds an image or publishes anything.

ENVIRONMENT: the BASELINE arm loads the producer source at a PINNED COMMIT via
`git show <pin>:<path>` (pre-remedy bytes), the CURRENT arm loads the worktree file.
Both are resolved BY CONTENT with a control, never by "is this commit an ancestor"
(the tree clause: a hash test answers "did this commit land", not "is the fix present").

TREE: every run prints the worktree it ran in and the commit it pinned.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import types
from pathlib import Path

WS = Path(__file__).resolve()
while WS.name and not (WS / ".git").exists():
    WS = WS.parent
PRODUCER_REL = "infra/aws/globgrph/derive_stitch.py"
PRODUCER_ABS = WS / "infra" / "aws" / "globgrph" / "derive_stitch.py"
GLOBGRPH_DIR = str(PRODUCER_ABS.parent)

# The commit this worker started from: the producer BEFORE this order touched it.
BASELINE_PIN = "b5bb2f16a0ad960406fea53ead0b0e1a1d24526f"
# The marker this order's remedy writes into the producer. Absent in the baseline bytes
# BY CONSTRUCTION (the pin predates the order); present in the worktree once the remedy lands.
REMEDY_MARKER = "CG-s-43"


def _git(*args: str) -> str:
    env = dict(os.environ)
    env["MSYS_NO_PATHCONV"] = "1"          # git show <ref>:<slashed path>
    p = subprocess.run(["git", "-C", str(WS), *args], capture_output=True, env=env)
    if p.returncode != 0:
        raise RuntimeError("ERROR: git %s rc=%d %s" % (args, p.returncode,
                                                       p.stderr.decode("utf-8", "replace")[:400]))
    return p.stdout.decode("utf-8", "replace")


def tree_facts() -> dict:
    return {
        "worktree": str(WS).replace("\\", "/"),
        "branch": _git("rev-parse", "--abbrev-ref", "HEAD").strip(),
        "head": _git("rev-parse", "HEAD").strip(),
        "baseline_pin": BASELINE_PIN,
    }


def baseline_source() -> str:
    src = _git("show", "%s:%s" % (BASELINE_PIN, PRODUCER_REL))
    # POSITIVE CONTROL on the retrieval: a mangled/empty git show returns clean-empty.
    if len(src) < 10000 or "def build_stitched_graph" not in src:
        raise RuntimeError("ERROR: baseline source retrieval failed (len=%d)" % len(src))
    return src


def current_source() -> str:
    return PRODUCER_ABS.read_text(encoding="utf-8")


def load_producer(src: str, name: str):
    """Exec the producer source as a module. __file__ points at the REAL path so the
    producer's own `_WS = parents[3]` resolves to the workspace root."""
    if GLOBGRPH_DIR not in sys.path:
        sys.path.insert(0, GLOBGRPH_DIR)   # the producer imports its same-dir sibling
    if str(WS) not in sys.path:
        sys.path.insert(0, str(WS))
    mod = types.ModuleType(name)
    mod.__file__ = str(PRODUCER_ABS)
    mod.__name__ = name
    sys.modules[name] = mod
    exec(compile(src, str(PRODUCER_ABS), "exec"), mod.__dict__)
    return mod


# --------------------------------------------------------------------------- fixture
ANCHOR = "arn:aws:lambda:us-east-1:313476888478:function:i2-anchor"
KEPT = "comp:i2-kept"          # emitted by THIS cycle and present in the archive
RETIRED = "comp:i2-retired"    # in the archive, NOT emitted by this cycle -> dropped on read
PHANTOM = "comp:i2-phantom"    # in NEITHER: the negative control for the dangling check


class _FakeTrace:
    edges: list = []
    nodes: dict = {}


def make_snapshot(with_phantom_edge: bool) -> dict:
    """The ARCHIVED snapshot this producer reads back: its own prior output plus AWS nodes."""
    edges = [
        # archived stitch edge onto a node THIS cycle does not re-emit. NOT STORED_IN, so
        # derive_stitch.py:158-159 does not drop it.
        {"source": RETIRED, "target": ANCHOR, "edge_type": "FETCHES", "layer": "inter"},
        # control: the same shape onto a node this cycle DOES re-emit.
        {"source": KEPT, "target": ANCHOR, "edge_type": "FETCHES", "layer": "inter"},
    ]
    if with_phantom_edge:
        edges.append({"source": PHANTOM, "target": ANCHOR,
                      "edge_type": "FETCHES", "layer": "inter"})
    return {
        "classes_data": {
            "Component": {"nodes": [
                {"id": KEPT, "type": "Component", "source": "portal-stitch", "name": "i2-kept"},
                {"id": RETIRED, "type": "Component", "source": "portal-stitch",
                 "name": "i2-retired"},
            ]},
            "Lambda": {"nodes": [
                {"id": ANCHOR, "arn": ANCHOR, "type": "LAMBDA", "name": "i2-anchor"},
            ]},
        },
        "edges": edges,
        "_snapshot_key": "FIXTURE/i2/no-s3-read",
    }


def make_portal() -> dict:
    """THIS cycle's emission: KEPT is re-emitted, RETIRED is not (a SHRINKING emission)."""
    return {
        "classes_data": {
            "Component": {"nodes": [
                {"id": KEPT, "type": "Component", "source": "portal-stitch", "name": "i2-kept"},
            ]},
        },
        "edges": [
            {"source": KEPT, "target": ANCHOR, "edge_type": "FETCHES", "layer": "intra"},
        ],
    }


def run_producer(mod, with_phantom_edge: bool = False) -> dict:
    """Run the REAL build_stitched_graph over the fixture. No S3, no egress."""
    snap = make_snapshot(with_phantom_edge)
    mod.load_aws_layer = lambda: snap

    fake_portal = types.SimpleNamespace(build_portal_stitch_graph=lambda ws: make_portal())
    mod.portal = fake_portal
    mod.T = types.SimpleNamespace(build_graph=lambda ws: _FakeTrace())

    g = mod.build_stitched_graph(WS)
    node_ids = {str(n.get("id", "")) for v in g["classes_data"].values() for n in v["nodes"]}
    snap_stitch_ids = {str(n.get("id", "")) for v in snap["classes_data"].values()
                       for n in v.get("nodes", []) if n.get("source") == "portal-stitch"}
    dropped = sorted(snap_stitch_ids - node_ids)
    node_absent_edge_present = [e for e in g["edges"]
                                if e["source"] in dropped or e["target"] in dropped]
    return {
        "genuine_dangling": g["meta"]["genuine_dangling"],
        "dangling_sample": g["_genuine_dangling"],
        "collapsed": g["meta"]["stitch_unify"]["collapsed_copies"],
        "total_nodes": g["meta"]["total_nodes"],
        "total_edges": g["meta"]["total_edges"],
        "node_ids": sorted(node_ids),
        "dropped_ids": dropped,
        "node_absent_edge_present": node_absent_edge_present,
        "edges": g["edges"],
    }


def jdump(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True)
