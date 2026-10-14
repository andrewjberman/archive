"""One firm's REAL read-only build from a BUILT bundle tree, traced with an open audit hook and sys.modules.

Usage: python -I -B trace_build.py <tree_root> <firm> <as_of>
Prints one JSON line: the repo-relative files (forward slashes) that were opened or sit in sys.modules under the tree,
excluding __pycache__ and SHA256SUMS, plus the S3 read/refusal counters. The only S3 client is wrapped read-only
(get_, list_, head_ pass; anything else is refused and recorded). No write call is made by this script.
"""
import json
import os
import sys

tree = os.path.abspath(sys.argv[1])
firm, as_of = sys.argv[2], sys.argv[3]
producer = os.path.join(tree, "data", "assets", "scripts", "gold", "investor_reporting")
sys.path[:0] = [producer, os.path.join(tree, "lib")]
# prefix tests are case-insensitive (Windows); the recorded paths keep their on-disk case
prefix = os.path.normcase(tree) + os.sep
opened = set()


def _under(ap):
    return os.path.normcase(ap).startswith(prefix)


def _hook(event, args):
    if event == "open" and args:
        p = args[0]
        if isinstance(p, (bytes, bytearray)):
            p = os.fsdecode(p)
        if isinstance(p, str):
            ap = os.path.abspath(p)
            if _under(ap):
                opened.add(ap)


sys.addaudithook(_hook)

import boto3  # noqa: E402

READ_OPS = ("get_", "list_", "head_")


class ReadOnly:
    def __init__(self, client):
        self._c = client
        self.reads = []
        self.refused = []

    def get_object(self, **kw):
        self.reads.append((kw.get("Bucket"), kw.get("Key")))
        return self._c.get_object(**kw)

    def __getattr__(self, name):
        if name.startswith(READ_OPS):
            return getattr(self._c, name)
        self.refused.append(name)
        raise PermissionError("read-only trace refuses the %s operation" % name)


import holdings_snapshot as hs  # noqa: E402

mod_file = os.path.abspath(hs.__file__)
if not _under(mod_file):
    raise SystemExit("REFUSED: producer imported from outside the tree: %s" % mod_file)

client = ReadOnly(boto3.client("s3", region_name="us-east-1"))
inputs = hs.VersionedInputs(client)
snap = hs.build_snapshot(firm, inputs, as_of)
nodes = snap.get("nodes", [])

mods = set()
for m in list(sys.modules.values()):
    f = getattr(m, "__file__", None)
    if f:
        af = os.path.abspath(f)
        if _under(af):
            mods.add(af)


def rel(p):
    return os.path.relpath(p, tree).replace("\\", "/")


traced = set()
for p in opened | mods:
    r = rel(p)
    if "__pycache__" in r.split("/") or r == "SHA256SUMS" or r.endswith(".pyc"):
        continue
    traced.add(r)

print(json.dumps({
    "firm": firm,
    "as_of": as_of,
    "node_count": len(nodes),
    "s3_get_calls": len(client.reads),
    "s3_refused_ops": client.refused,
    "traced": sorted(traced),
    "traced_count": len(traced),
    "opened_count": len(opened),
    "module_count_under_tree": len(mods),
}, sort_keys=True))
