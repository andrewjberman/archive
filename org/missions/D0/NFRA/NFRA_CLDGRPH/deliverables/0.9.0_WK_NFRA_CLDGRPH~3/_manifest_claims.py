#!/usr/bin/env python3
"""E3-AC4 instrument -- the S53 claim, on the BUILDER and on the STAYING stores.

BUILDER half: ast-parse the builder, find the function that calls the shared
manifest writer (`write_manifest`), and inside THAT function find a call whose
KEYWORD ARGUMENTS carry both `edge_count_claim` and `artifact_claim`. Scoping
the search to the manifest-writing function is the point: a claim stamped in
some unrelated helper would not travel with a build.

STORE half: for every artifact in the disposition record that is one of the two
STORES and whose disposition is not a RETIRE, read `<store>._build_manifest.json`
and require both claim fields. A RETIRE store is excluded from the denominator
and PRINTED as excluded -- an empty denominator would pass vacuously and is
reported as such rather than as a pass.

usage: _manifest_claims.py --builder <py> --record <md> [--store-root <dir>]
                           [--label L]
exit 0 always; the caller grades the printed lines.
"""
from __future__ import annotations

import ast
import json
import os
import re
import sys

CLAIM_KEYS = ("edge_count_claim", "artifact_claim")
WRITER_NAME = "write_manifest"
# The two STORES of cell CG-s-19, by basename. kuzu_load.py is a builder and the
# lock is not a store; neither can carry a manifest field, and both are named in
# the record with `manifest: n/a`.
STORE_BASENAMES = ("kuzu_db", "kuzu_ac7.db")
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


def builder_half(path: str) -> bool:
    print("--- BUILDER: %s ---" % path)
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except (OSError, SyntaxError) as ex:
        print("  UNREADABLE: %s" % ex)
        print("BUILDER_STAMPS_CLAIM=false")
        return False
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
        for c in calls:
            kws = _kwnames(c)
            if all(k in kws for k in CLAIM_KEYS):
                print("  CLAIM CALL: %s(...) at line %d -- keywords: %s"
                      % (_callee(c), c.lineno, ", ".join(kws)))
                found = True
        if not found:
            print("  NO call in %s() carries both %s"
                  % (fn.name, " and ".join(CLAIM_KEYS)))
    print("BUILDER_STAMPS_CLAIM=%s" % ("true" if found else "false"))
    return found


def _record_stores(record: str):
    txt = open(record, encoding="utf-8").read()
    for b in re.findall(r"```json\n(.*?)\n```", txt, re.S):
        try:
            d = json.loads(b)
        except Exception:
            continue
        if isinstance(d, dict) and "artifacts" in d:
            out = []
            for e in d["artifacts"]:
                a = str(e.get("artifact", ""))
                base = a.rstrip("/").split("/")[-1].split(" ")[0]
                if base in STORE_BASENAMES:
                    out.append((a, base, str(e.get("disposition", ""))))
            return out
    return []


def store_half(record: str, store_root: str) -> None:
    print("--- STAYING STORES, from the disposition record %s ---" % record)
    stores = _record_stores(record)
    if not stores:
        print("  NO store artifacts found in the record")
    staying, ok = [], 0
    for a, base, disp in stores:
        if disp.startswith("RETIRE"):
            print("  EXCLUDED FROM THE DENOMINATOR (disposition %s, a retired"
                  " store carries no claim): %s" % (disp, a))
            continue
        staying.append((a, base, disp))
    for a, base, disp in staying:
        mpath = os.path.join(store_root, base + MANIFEST_SUFFIX)
        if not os.path.exists(mpath):
            print("  MISSING MANIFEST  %s  (disposition %s)" % (mpath, disp))
            continue
        try:
            data = json.load(open(mpath, encoding="utf-8"))
        except Exception as ex:
            print("  UNPARSEABLE MANIFEST %s: %s" % (mpath, ex))
            continue
        missing = [k for k in CLAIM_KEYS if k not in data]
        if missing:
            print("  CLAIM MISSING     %s  lacks %s" % (mpath, ", ".join(missing)))
            continue
        ok += 1
        print("  CLAIM PRESENT     %s  edge_count_claim=%r  artifact_claim=%r"
              " (disposition %s)"
              % (mpath, data["edge_count_claim"], data["artifact_claim"], disp))
    if not staying:
        print("  DENOMINATOR IS ZERO -- every store retired. A 0-of-0 pass is"
              " VACUOUS and is reported here as such, not as a pass.")
    print("MANIFEST_CLAIM_FIELDS=%d of %d staying store(s)" % (ok, len(staying)))


def main() -> int:
    args = sys.argv[1:]
    opts = {"--builder": None, "--record": None, "--label": "REAL",
            "--store-root": r"C:\Users\AndrewBerman\Desktop\ajb_workspace\infra\aws\globgrph"}
    i = 0
    while i < len(args):
        if args[i] in opts:
            opts[args[i]] = args[i + 1]
            i += 2
        else:
            i += 1
    print("=== MANIFEST CLAIMS [%s] ===" % opts["--label"])
    builder_half(opts["--builder"])
    print()
    store_half(opts["--record"], opts["--store-root"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
