#!/usr/bin/env python3
"""E4-AC3 instrument -- the S53 claim on the stitch BUILDER and its MANIFEST.

BUILDER half: ast-parse the builder, find the function that calls the shared
manifest writer (`write_manifest`), and inside THAT function require a call
whose KEYWORD ARGUMENTS carry both `edge_count_claim` and `artifact_claim`.
Scoping to the manifest-writing function is the point: a claim stamped in an
unrelated helper would not travel with a build.

MANIFEST half: read `<store>._build_manifest.json` in the main workspace and
require both fields -- denominator 2, the two FIELDS. The STORE's size and
mtime are printed beside the task order's census constants, because a claim
added to a manifest must not have touched the artifact it describes.

usage: _stitch_claim.py --builder <py> --store <abs path> [--label L]
       [--expect-bytes N] [--expect-mtime 'YYYY-MM-DD HH:MM']
exit 0 always; the caller grades the printed lines.
"""
from __future__ import annotations

import ast
import datetime
import json
import os
import sys

CLAIM_KEYS = ("edge_count_claim", "artifact_claim")
WRITER_NAME = "write_manifest"
MANIFEST_SUFFIX = "._build_manifest.json"


def _kwnames(call: ast.Call):
    return [kw.arg for kw in call.keywords if kw.arg]


def _callee(call: ast.Call) -> str:
    f = call.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return "<expr>"


def builder_half(path: str) -> None:
    print("--- BUILDER: %s ---" % path)
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except (OSError, SyntaxError) as ex:
        print("  UNREADABLE: %s" % ex)
        print("BUILDER_STAMPS_CLAIM=false")
        return
    found = False
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call)]
        writers = [c for c in calls if _callee(c) == WRITER_NAME]
        if not writers:
            continue
        print("  MANIFEST-WRITING FUNCTION: %s() at line %d -- calls %s at line %d"
              % (fn.name, fn.lineno, WRITER_NAME, writers[0].lineno))
        print("     writer keywords: %s" % ", ".join(_kwnames(writers[0])))
        local = False
        for c in calls:
            kws = _kwnames(c)
            if all(k in kws for k in CLAIM_KEYS):
                print("  CLAIM CALL: %s(...) at line %d -- keywords: %s"
                      % (_callee(c), c.lineno, ", ".join(kws)))
                local = True
                found = True
        if not local:
            print("  NO call in %s() carries both %s"
                  % (fn.name, " and ".join(CLAIM_KEYS)))
    print("BUILDER_STAMPS_CLAIM=%s" % ("true" if found else "false"))


def manifest_half(store: str, expect_bytes, expect_mtime) -> None:
    print("--- STORE + MANIFEST: %s ---" % store)
    if os.path.exists(store):
        st = os.stat(store)
        mt = datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")
        same = (expect_bytes is None or st.st_size == int(expect_bytes)) and \
               (expect_mtime is None or mt == expect_mtime)
        print("  STORE bytes=%d (cut: %s)  mtime='%s' (cut: '%s')  UNCHANGED=%s"
              % (st.st_size, expect_bytes, mt, expect_mtime, same))
    else:
        print("  STORE ABSENT at %s" % store)
    mpath = store + MANIFEST_SUFFIX
    if not os.path.exists(mpath):
        print("  MANIFEST ABSENT at %s" % mpath)
        print("MANIFEST_CLAIM_FIELDS=0 of %d" % len(CLAIM_KEYS))
        return
    data = json.load(open(mpath, encoding="utf-8"))
    present = 0
    for k in CLAIM_KEYS:
        if k in data:
            present += 1
            print("  FIELD PRESENT  %s = %r" % (k, data[k]))
        else:
            print("  FIELD MISSING  %s" % k)
    print("  MANIFEST: %s" % mpath)
    print("  (the other keys, untouched: %s)"
          % ", ".join(sorted(k for k in data if k not in CLAIM_KEYS)))
    print("MANIFEST_CLAIM_FIELDS=%d of %d" % (present, len(CLAIM_KEYS)))


def main() -> int:
    args = sys.argv[1:]
    opts = {"--builder": None, "--store": None, "--label": "REAL",
            "--expect-bytes": None, "--expect-mtime": None}
    i = 0
    while i < len(args):
        if args[i] in opts:
            opts[args[i]] = args[i + 1]
            i += 2
        else:
            i += 1
    print("=== STITCH CLAIM [%s] ===" % opts["--label"])
    builder_half(opts["--builder"])
    print()
    manifest_half(opts["--store"], opts["--expect-bytes"], opts["--expect-mtime"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
