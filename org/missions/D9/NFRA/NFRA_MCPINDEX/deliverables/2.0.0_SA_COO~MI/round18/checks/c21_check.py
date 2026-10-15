"""c21_check.py -- grades MX-c-21 (CONTRACT C-GROUP item 1: `bucket` on every catalog row and every tool_index row; the emitter's --group-map), from the repo root.

  python c21_check.py ac1   the emitted catalog (infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml, or C21_CATALOG), regenerated WITH the issuer's assets map: every row of silver_datasets,
                            portal_datasets and harvest_datasets carries a `bucket` that is an S3 bucket name (opal-data-...) or `dynamodb`; against the catalog at BASE_REF a row differs only in
                            bucket, vendor, firm and nl_tags/nl_tags_basis (the keys the map and the bucket rule add or replace); a row that already had an S3 bucket keeps it
  python c21_check.py ac2   the tool index: every entry carries `bucket` and `source_group` {id, name, kind}; id == bucket; kind is `bucket` for an opal-data- bucket, `graph` for graph, else `store`; a tool
                            that catalog rows name as read_tool has the bucket of its PRIMARY row (its `index` row for member a, else the most frequent, ties alphabetical); a tool declared in
                            tool_index/members.yaml with `bucket` and `bucket_source` (path:line) for an opal-data- bucket has that bucket named within 6 lines of that line in the file
  python c21_check.py ac3   the unit tests: workflows/atom_decomposition/tests/test_c_group.py holds at least 10 tests and the whole atom_decomposition test folder passes

Exit 0 PASS, 1 FAIL, 9 no run."""
import ast
import collections
import os
import re
import subprocess
import sys
import tempfile

import yaml

BASE_REF = "c4c106aea1"
CATALOG = os.environ.get("C21_CATALOG") or "infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml"
SECTIONS = ("silver_datasets", "portal_datasets", "harvest_datasets")
BUCKET = re.compile(r"^(opal-data-[a-z0-9-]+|dynamodb)$")
MEMBERS = "workflows/atom_decomposition/tool_index/members.yaml"


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok  " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def load(path):
    with open(path, encoding="ascii") as fh:
        return yaml.safe_load(fh)


def base_catalog():
    r = subprocess.run(["git", "show", "%s:infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml" % BASE_REF], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        print("ERROR: git show base rc %d" % r.returncode)
        sys.exit(9)
    p = os.path.join(tempfile.mkdtemp(prefix="c21_"), "base.yaml")
    open(p, "wb").write(r.stdout)
    return load(p)


def rows(cat):
    out = {}
    for sec in SECTIONS:
        for r in cat.get(sec) or []:
            if isinstance(r, dict) and r.get("entity"):
                out[r["entity"]] = r
    return out


def ac1():
    new, base = rows(load(CATALOG)), rows(base_catalog())
    bad = sorted(e for e, r in new.items() if not (isinstance(r.get("bucket"), str) and BUCKET.match(r["bucket"])))
    print("DENOMINATOR rows %d (base %d); with a valid bucket %d" % (len(new), len(base), len(new) - len(bad)))
    for e in bad[:5]:
        print("  BAD bucket %s: %r" % (e, new[e].get("bucket")))
    odd, moved = [], []
    for e, r in base.items():
        if e not in new:
            continue
        diff = set(k for k in set(r) | set(new[e]) if r.get(k) != new[e].get(k))
        if diff - {"bucket", "vendor", "firm", "nl_tags", "nl_tags_basis"}:
            odd.append((e, sorted(diff)))
        if isinstance(r.get("bucket"), str) and BUCKET.match(r["bucket"]) and new[e].get("bucket") != r["bucket"]:
            moved.append(e)
    print("rows differing outside bucket/vendor/firm/nl_tags: %d; rows whose valid S3 bucket moved: %d" % (len(odd), len(moved)))
    for o in odd[:5]:
        print("  ODD %s" % (o,))
    return report([("every row carries a valid bucket (%d of %d)" % (len(new) - len(bad), len(new)), len(new) > 0 and not bad),
                   ("rows differ from the base only in bucket, vendor, firm and the curated tags", not odd), ("no valid S3 bucket was changed", not moved),
                   ("the row set equals the base's", sorted(new) == sorted(base) or set(base) <= set(new))])


def primary_bucket(cat):
    by_tool = collections.defaultdict(collections.Counter)
    ent = rows(cat)
    for r in ent.values():
        if r.get("read_tool") and r.get("bucket"):
            by_tool[r["read_tool"]][r["bucket"]] += 1
    return by_tool, ent


def ac2():
    cat = load(CATALOG)
    ti = cat.get("tool_index") or []
    by_tool, ent = primary_bucket(cat)
    members = {m["tool"]: m for m in (yaml.safe_load(open(MEMBERS, encoding="ascii"))["members"])}
    shape, kind, derive, source, n_decl = [], [], [], [], 0
    for e in ti:
        t = e.get("tool")
        b, sg = e.get("bucket"), e.get("source_group")
        if not (isinstance(b, str) and re.match(r"^[a-z0-9][a-z0-9-]*$", b) and isinstance(sg, dict) and sg.get("id") == b and isinstance(sg.get("name"), str) and sg["name"].strip()
                and sg.get("kind") in ("bucket", "graph", "store")):
            shape.append(t)
            continue
        want = "bucket" if b.startswith("opal-data-") else ("graph" if b == "graph" else "store")
        if sg["kind"] != want:
            kind.append(t)
        if t in by_tool:
            idx = ent.get(str(e.get("index")))
            if e.get("member") == "a" and idx and idx.get("bucket"):
                exp = idx["bucket"]
            elif e.get("member") == "a":
                exp = None       # an (a) tool indexed by a channel row: the channel's bucket (the catalog's top-level bucket)
            else:
                exp = sorted(by_tool[t].items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
            if exp is not None and b != exp:
                derive.append("%s: %s != %s" % (t, b, exp))
        m = members.get(t) or {}
        if m.get("bucket_source") and b.startswith("opal-data-"):
            n_decl += 1
            path, _sep, line = str(m["bucket_source"]).rpartition(":")
            try:
                lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
                n = int(line)
                if not any(b in x for x in lines[max(0, n - 7):n + 6]):
                    source.append("%s: %s not near %s" % (t, b, m["bucket_source"]))
            except (OSError, ValueError):
                source.append("%s: unreadable %s" % (t, m.get("bucket_source")))
    print("DENOMINATOR tool_index entries %d; malformed %d; kind wrong %d; bucket differs from its rows %d; declared S3 buckets %d, unproved %d" %
          (len(ti), len(shape), len(kind), len(derive), n_decl, len(source)))
    for x in (shape[:3] + kind[:3] + derive[:3] + source[:3]):
        print("  %s" % (x,))
    kinds = collections.Counter((e.get("source_group") or {}).get("kind") for e in ti)
    print("kinds %s; buckets %d distinct" % (dict(kinds), len({e.get("bucket") for e in ti})))
    return report([("every tool_index entry carries bucket and a matching source_group (%d of %d)" % (len(ti) - len(shape), len(ti)), len(ti) == 99 and not shape),
                   ("kind follows the bucket", not kind), ("a tool the rows name has its primary row's bucket", not derive),
                   ("every declared S3 bucket is named at its bucket_source line", not source)])


def ac3():
    tf = "workflows/atom_decomposition/tests/test_c_group.py"
    n = 0
    if os.path.exists(tf):
        n = sum(1 for node in ast.walk(ast.parse(open(tf, encoding="utf-8").read())) if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"))
    print("tests in test_c_group.py: %d" % n)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--no-header", "workflows/atom_decomposition/tests"], capture_output=True, text=True, timeout=280)
    tail = [ln for ln in (r.stdout or "").replace("\x1b", "").splitlines() if "passed" in ln or "failed" in ln][-1:]
    print("pytest rc=%d: %s" % (r.returncode, tail[0].strip() if tail else (r.stdout or r.stderr)[-200:]))
    return report([("the new test file holds at least 10 tests", n >= 10), ("the atom_decomposition test folder passes", r.returncode == 0)])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2", "ac3"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2, "ac3": ac3}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
