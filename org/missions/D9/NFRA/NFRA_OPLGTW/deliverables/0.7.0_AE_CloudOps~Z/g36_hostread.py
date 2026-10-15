#!/usr/bin/env python
"""OG-ap-19 Phase A step 1: the live-ref md5 read of the host. READ-ONLY.

Runs ON i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python, pulled from S3 (Rule 12). It
walks the FOUR roots step 1 names -- app/, deploy/, dashboard/ and lib/ -- in ONE walk, and writes
nothing.

lib/ is in the list for the first time because OG-ap-18 put it there: before that release the directory
did not exist, so a parity read that assumed it would have failed closed on an absent path rather than
on a mismatch. Its absence is reported as a distinguishable state, not as zero files.

__pycache__ and .pyc are excluded: they are build products of the host's own interpreter and were never
in the artifact, so including them would manufacture host-only paths in every comparison.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import traceback

ROOT = "/opt/opal-gateway"
ROOTS = ("app", "deploy", "dashboard", "lib")


def md5_path(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()


def main() -> int:
    out = {"root": ROOT, "roots_requested": list(ROOTS), "tree_md5": {}, "per_root": {}, "absent_roots": []}
    for rel in ROOTS:
        base = os.path.join(ROOT, rel)
        if not os.path.isdir(base):
            out["absent_roots"].append(rel)
            out["per_root"][rel] = None          # None, never 0: absent is not empty
            continue
        n = 0
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in filenames:
                if fn.endswith(".pyc"):
                    continue
                full = os.path.join(dirpath, fn)
                key = os.path.relpath(full, ROOT).replace(os.sep, "/")
                try:
                    out["tree_md5"][key] = md5_path(full)
                except OSError as exc:
                    out["tree_md5"][key] = "UNREADABLE:%s" % type(exc).__name__
                n += 1
        out["per_root"][rel] = n
    out["files_total"] = len(out["tree_md5"])
    # the three NEWS_* .env key NAMES this release adds -- names only, never a value
    env = os.path.join(ROOT, ".env")
    if os.path.isfile(env):
        names = []
        with open(env, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    names.append(line.split("=", 1)[0])
        out["env_key_names"] = sorted(set(names))
        out["env_key_count"] = len(out["env_key_names"])
        out["news_keys_present"] = sorted(k for k in out["env_key_names"] if k.startswith("NEWS_"))
    else:
        out["env_key_names"] = None
    print("HOSTREAD_JSON")
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("HOSTREAD_JSON")
        print(json.dumps({"fatal": traceback.format_exc()[-1500:]}, indent=1))
        sys.exit(1)
