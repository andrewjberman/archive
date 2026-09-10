#!/usr/bin/env python3
"""F1-AC4 / F1-AC2 instrument -- parse a TOMBSTONE's fenced json block.

Prints, for the file given:
  PARSED=true|false
  FIELD_<name>=present|MISSING     for each of the eight named fields
  MISSING_FIELDS=<comma list or NONE>
  FIELDS_PRESENT=<n> of 8
and, with --emit <dotted.path>, prints the value at that path (used by
f1_archives_verified.sh to read the recorded pre-upload sha256 back OUT of the
tombstone rather than out of the uploading script's own memory).

Exit code is 0 whatever it finds; the caller grades the printed lines.
"""
from __future__ import annotations

import json
import re
import sys

REQUIRED = ["tarball_key", "tarball_size", "tarball_etag", "manifest",
            "archive_keys", "archive_sha256", "builder_last_hash", "authority"]

FENCE = re.compile(r"```json\s*\n(.*?)\n```", re.S)


def load(path):
    src = open(path, encoding="utf-8").read()
    m = FENCE.search(src)
    if not m:
        return None, "no fenced json block"
    try:
        return json.loads(m.group(1)), None
    except ValueError as ex:
        return None, "json: %s" % ex


def main() -> int:
    args = sys.argv[1:]
    emit = None
    if "--emit" in args:
        i = args.index("--emit")
        emit = args[i + 1]
        args = args[:i] + args[i + 2:]
    path = args[0]
    doc, err = load(path)
    if emit is not None:
        if doc is None:
            print("")
            return 0
        cur = doc
        for seg in emit.split("|"):
            if isinstance(cur, dict) and seg in cur:
                cur = cur[seg]
            else:
                print("")
                return 0
        print(cur if not isinstance(cur, (dict, list)) else json.dumps(cur))
        return 0
    print("TOMBSTONE_FILE=%s" % path)
    if doc is None:
        print("PARSED=false (%s)" % err)
        print("MISSING_FIELDS=%s" % ",".join(REQUIRED))
        print("FIELDS_PRESENT=0 of 8")
        return 0
    print("PARSED=true")
    missing = []
    for f in REQUIRED:
        v = doc.get(f, None)
        ok = v is not None and v != "" and v != [] and v != {}
        print("FIELD_%s=%s" % (f, "present" if ok else "MISSING"))
        if not ok:
            missing.append(f)
    print("MISSING_FIELDS=%s" % (",".join(missing) if missing else "NONE"))
    print("FIELDS_PRESENT=%d of 8" % (8 - len(missing)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
