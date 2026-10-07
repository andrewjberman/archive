#!/usr/bin/env python3
"""E-Y4 / cell IB-yr-624: irpt-ycharts-generate's package drops fixtures/har, and nothing at runtime reads it.

Modes (one per criterion; each prints one summary line):
  --trace          every packaged member (files[] at source_dir + staged_from repo_path, read from the working tree),
                   except fixtures/har/* themselves, is read as text and searched for a path-shaped fixtures
                   reference (see TOKEN). This is any reader -- an open(), a Path, a glob, a string constant --
                   not only an import.
  --package        files[] carries no fixtures/har member, and no test or fixture file under source_dir differs
                   from --base (the repo tests read fixtures from the repo, so they are untouched by construction).
  --trace --plant  the trace with one planted runtime member that opens a fixture; the trace must catch it.
ASCII only.
"""
import json
import re
import subprocess
import sys

MAP = "infra/aws/lambda/ci/lambda-source-map.json"
FN = "irpt-ycharts-generate"
# A path-shaped reference to fixtures/har: a "fixtures/har" or "fixtures\har" path, a quoted "har" path segment (as in
# os.path.join(..., "fixtures", "har")), or the manifest's name. Prose is not a reader; fixtures/holdings is another
# folder (row S358) and out of this cell.
TOKEN = re.compile(r"""fixtures[/\\]har|["']har["']|FIXTURE_MANIFEST""")
PLANT = ("planted_runtime_reader.py", 'open("fixtures/har/status_ok.json").read()\n')


def row():
    d = json.load(open(MAP, encoding="utf-8"))
    return d.get("functions", d)[FN]


def members(r):
    src = r["source_dir"].rstrip("/") + "/"
    out = [(m, src + m) for m in r["files"]]
    out += [(s["packaged_as"], s["repo_path"]) for s in r.get("staged_from", [])]
    return out


def trace(plant):
    r = row()
    hits, n = [], 0
    for name, path in members(r):
        if name.startswith("fixtures/har/") or not name.endswith((".py", ".json", ".sh", ".txt")):
            continue
        n += 1
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if TOKEN.search(text):
            hits.append(name)
    if plant:
        n += 1
        if TOKEN.search(PLANT[1]):
            hits.append(PLANT[0])
    for h in hits:
        print("FAIL: runtime reader of fixtures: " + h)
    if hits:
        print("FAIL: %d runtime reader(s) of fixtures across %d packaged text members" % (len(hits), n))
        return 1
    print("PASS: 0 runtime readers of fixtures across %d packaged text members" % n)
    return 0


def package(base):
    r = row()
    left = [m for m in r["files"] if m.startswith("fixtures/har/")]
    src = r["source_dir"].rstrip("/") + "/"
    diff = subprocess.run(["git", "diff", "--name-only", base, "--", src + "fixtures", src + "tests"],
                          capture_output=True, text=True)
    if diff.returncode != 0:
        print("FAIL: git diff against %s failed" % base)
        return 1
    changed = [x for x in diff.stdout.split("\n") if x]
    for m in left:
        print("FAIL: still packaged: " + m)
    for c in changed:
        print("FAIL: test or fixture file changed: " + c)
    if left or changed:
        print("FAIL: %d fixtures/har member(s) packaged, %d test or fixture file(s) changed" % (len(left), len(changed)))
        return 1
    print("PASS: files[] carries 0 fixtures/har members (%d members); 0 test or fixture files changed" % len(r["files"]))
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--package" in a:
        sys.exit(package(a[a.index("--base") + 1] if "--base" in a else "HEAD"))
    sys.exit(trace("--plant" in a))
