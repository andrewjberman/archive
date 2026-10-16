#!/usr/bin/env python
"""OG-ev-1: a second, LOCAL scrub of W/ANSWER_BODIES.json after the host's own. Any UUID-shaped string (a model allocation id attached to a
client position, for example) is an identifier tied to a client account and is replaced by "[masked-id]"; the count is recorded in the file
under post_scrub. usage: python ev1_post_scrub.py   (from the repository root)"""
from __future__ import annotations

import json
import re

P = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ANSWER_BODIES.json"
UUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
doc = json.load(open(P, encoding="utf-8"))
count = 0


def walk(o):
    global count
    if isinstance(o, dict):
        return {k: walk(v) for k, v in o.items()}
    if isinstance(o, list):
        return [walk(v) for v in o]
    if isinstance(o, str):
        new, n = UUID.subn("[masked-id]", o)
        count += n
        return new
    return o


doc["releases"] = walk(doc["releases"])
doc["post_scrub"] = {"rule": "UUID-shaped strings replaced by [masked-id]", "replaced": count}
with open(P, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(doc, indent=1) + "\n")
print("replaced", count, "UUID-shaped strings")
