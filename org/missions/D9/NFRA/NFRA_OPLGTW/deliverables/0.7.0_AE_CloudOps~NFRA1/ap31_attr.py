#!/usr/bin/env python
"""OG-ap-31 Phase A step 2: attribute every live->trunk hunk of each candidate take file to a NAMED order, or call it unattributable.

usage: python ap28_attr.py <live_ref> <trunk_sha> <out.json>   (run from the repository root; read-only)

A hunk is attributed when every line it adds or removes also appears among the lines added or removed by the commits of the named orders that touched the file
(OG-en-4, 5, 6, 8, 9, 10, 12 and their amendments; found by commit subject). A hunk with a line no named commit wrote is UNATTRIBUTABLE: the file is then taken BY HUNK
(or the take stops), never whole. The comparison is by line CONTENT, not by commit ancestry, because trunk and the live release branch are not ancestors of one another
(the live ref is a release cut from a base, so `live..trunk` also lists commits the live release already carries by content)."""
from __future__ import annotations

import json
import re
import subprocess
import sys

LIVE, TRUNK, OUT = sys.argv[1:4]
G = "infra/aws/ec2/opal-gateway/"
NAMED = re.compile(r"OG-en-(13|14|15|16)\b|MX-c-24\b")
FILES = [G + "app/" + f for f in ("client_adapter_bd49f.py", "data_entitlement.py", "server.py", "integrations/opal_discover/integration.py")]


def git(*a, check=True):
    r = subprocess.run(["git"] + list(a), capture_output=True)
    if check and r.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(a[:3]), r.stderr.decode("utf-8", "replace")[:200]))
    return r.stdout.decode("utf-8", "replace")


def changed_lines(patch: str) -> set:
    out = set()
    for ln in patch.split("\n"):
        if (ln.startswith("+") or ln.startswith("-")) and not ln.startswith("+++") and not ln.startswith("---"):
            out.add(ln.rstrip("\r"))
    return out


def hunks(patch: str) -> list:
    hs, cur = [], None
    for ln in patch.split("\n"):
        if ln.startswith("@@"):
            cur = {"head": ln.split("@@")[1].strip(), "lines": set()}
            hs.append(cur)
        elif cur is not None and (ln.startswith("+") or ln.startswith("-")) and not ln.startswith("+++") and not ln.startswith("---"):
            cur["lines"].add(ln.rstrip("\r"))
    return hs


rows = []
for f in FILES:
    live_has = subprocess.run(["git", "cat-file", "-e", "%s:%s" % (LIVE, f)], capture_output=True).returncode == 0
    patch = git("diff", "-U0", LIVE, TRUNK, "--", f)
    hs = hunks(patch)
    named = []
    for ln in git("log", "--no-merges", "--format=%H\t%s", "%s..%s" % (LIVE, TRUNK), "--", f).splitlines():
        h, _, subj = ln.partition("\t")
        if NAMED.search(subj):
            named.append((h, subj))
    covered = set()
    for h, _s in named:
        covered |= changed_lines(git("show", "-U0", "--format=", h, "--", f))
    un = [x for x in hs if not x["lines"] <= covered]
    rows.append({"file": f.replace(G, ""), "live_has": live_has, "hunks": len(hs), "named_commits": [(h[:10], s[:60]) for h, s in named],
                 "attributed": len(hs) - len(un), "unattributable": len(un), "unattributable_heads": [x["head"] for x in un]})
    print("%-46s hunks %2d  attributed %2d  UNATTRIBUTABLE %2d  named commits %d" % (f.replace(G, ""), len(hs), len(hs) - len(un), len(un), len(named)))
json.dump({"live": LIVE, "trunk": TRUNK, "rows": rows}, open(OUT, "w"), indent=1)
