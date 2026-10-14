"""c12_depth.py -- MX-c-10 AC1 / AC3, MX-r-13 instrument (FWD-20 depth, PRD v0.10 item 2, ROUND_ANALYSIS.round11.md
ruling 1): EVERY member-(a) tool's history depth, graded PER TOOL with the denominator printed. Never a sample (the
standing lesson: a check that samples one member of a set never grades a claim about the whole set).

Usage:
  python c12_depth.py catalog <gateway dir> <catalog yaml> <aws exe>   -> AC1: the catalog claims, per tool
  python c12_depth.py answer  <gateway dir> <catalog yaml>             -> AC3: the answer-time depth, per measured row

A depth CLAIM (on a tool entry's `history_depth`, or on each element of `history_depth.links` when its claim is
`per-link`, the multi-index query tools' form) is one of:
  measured  value YYYY-MM-DD, basis s3://<bucket>/, row (+ scope when the row key holds {scope}), field (a dotted path;
            a list's first element is taken), method in {body-field, series-first, snapshot-asof}. GRADED: the aws CLI
            fetches the object and reads `field`; it must equal `value`.
  inferred  value, basis (where the window was read from) and source. Valid for a live-queried row's served window.
  absent    reason. VALID ONLY when the claim names a `row` whose served object resolves AND the object carries NO date
            anywhere this instrument scans (top-level values, the first element of top-level lists, and one level of
            nested mappings). An absent with no resolvable artifact is invalid: a live-queried row is `inferred`.
AC1 PASS: every (a) tool valid, with the denominator printed (N of N).
AC3 PASS: for EVERY measured claim, discover(row, exact=True) answers that row with history_depth claim measured and
the same value, read at answer time; AND the two rows the CVO read as carrying dates (round-11 analysis section 1),
mp.01.aum-metrics and etfs.01.positioning-data, are among the measured rows (issuer anchors, so AC3 cannot pass on the
one row that was already measured at base).
Only dates are printed.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

mode, gw, cat_path = sys.argv[1], os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3])
aws = sys.argv[4] if len(sys.argv) > 4 else ""
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}")
import yaml  # noqa: E402

doc = yaml.safe_load(open(cat_path, encoding="ascii"))
keys = {}


def walk(node):
    if isinstance(node, dict):
        if node.get("entity") and isinstance(node.get("key"), str):
            keys.setdefault(str(node["entity"]), node["key"])
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)


walk({k: v for k, v in doc.items() if k != "tool_index"})
tools = [e for e in (doc.get("tool_index") or []) if isinstance(e, dict) and e.get("member") == "a"]


def claims_of(e):
    hd = e.get("history_depth") or {}
    if hd.get("claim") == "per-link":
        return [x for x in (hd.get("links") or []) if isinstance(x, dict)]
    return [hd]


def fetch(c):
    basis = str(c.get("basis") or "")
    bucket = basis[5:].split("/", 1)[0] if basis.startswith("s3://") else "opal-data-portal-v2"
    key = keys.get(str(c.get("row") or ""), "").replace("{scope}", str(c.get("scope") or ""))
    if not key or "{" in key or "*" in key:
        return None, key
    fd, tmp = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    p = subprocess.run([aws, "s3", "cp", "s3://%s/%s" % (bucket, key), tmp, "--only-show-errors"],
                       capture_output=True, text=True, timeout=180)
    obj = None
    if p.returncode == 0:
        try:
            obj = json.load(open(tmp, encoding="utf-8"))
        except ValueError:
            obj = None
    os.remove(tmp)
    return obj, key


def dig(obj, path):
    for part in str(path).split("."):
        obj = obj.get(part) if isinstance(obj, dict) else None
    if isinstance(obj, list) and obj:
        obj = obj[0]
    if isinstance(obj, dict):
        return None
    return str(obj)[:10] if obj is not None else None


def any_date(obj):
    def scal(v):
        return isinstance(v, str) and bool(DATE.match(v))
    if isinstance(obj, dict):
        for v in obj.values():
            if scal(v) or (isinstance(v, list) and v and scal(v[0])):
                return True
            if isinstance(v, dict) and any(scal(w) or (isinstance(w, list) and w and scal(w[0])) for w in v.values()):
                return True
            if isinstance(v, list) and v and isinstance(v[0], dict) and any(scal(w) for w in v[0].values()):
                return True
    return False


if mode == "catalog":
    ok_tools = 0
    for e in tools:
        cs = claims_of(e)
        res = []
        for c in cs:
            k = c.get("claim")
            if k == "measured":
                obj, key = fetch(c)
                got = dig(obj, c.get("field")) if obj is not None else None
                good = (c.get("method") in ("body-field", "series-first", "snapshot-asof") and got is not None
                        and got == str(c.get("value"))[:10])
                res.append((good, "measured %s field=%s catalog=%s aws=%s" % (c.get("row"), c.get("field"),
                                                                              c.get("value"), got)))
            elif k == "inferred":
                good = all(str(c.get(f) or "").strip() for f in ("value", "basis", "source"))
                res.append((good, "inferred %s value=%s basis=%s" % (c.get("row") or "-", c.get("value"),
                                                                    str(c.get("basis"))[:50])))
            elif k == "absent":
                obj, key = fetch(c) if c.get("row") else (None, "")
                good = obj is not None and not any_date(obj) and bool(str(c.get("reason") or "").strip())
                why = ("no resolvable artifact (a live-queried row is inferred)" if obj is None
                       else "artifact carries a date" if any_date(obj) else "no date in the artifact")
                res.append((good, "absent %s: %s" % (c.get("row") or "-", why)))
            else:
                res.append((False, "claim %r is not one of measured/inferred/absent/per-link" % k))
        tool_ok = bool(res) and all(g for g, _ in res)
        ok_tools += tool_ok
        print("TOOL %-30s %s %s" % (e.get("tool"), "OK " if tool_ok else "BAD", " | ".join(t for _, t in res)))
    print("DEPTH (a) tools graded %d of %d; valid %d of %d" % (len(tools), len(tools), ok_tools, len(tools)))
    sys.exit(0 if tools and ok_tools == len(tools) else 1)

sys.path.insert(0, gw)
os.chdir(gw)
from app.graphql_plumbing import catalog_gate as g  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402

measured = [(e.get("tool"), c) for e in tools for c in claims_of(e) if c.get("claim") == "measured"]
seen, ok = set(), 0
for tool, c in measured:
    row = str(c.get("row") or "")
    if row in seen:
        continue
    seen.add(row)
    r = od.discover(row, g.OPAL_INTERNAL, exact=True)
    ms = [m for m in (r.get("matches") or []) if (m.get("property") or {}).get("entity") == row or m.get("dataset") == row]
    hd = (ms[0].get("history_depth") or {}) if ms else {}
    good = hd.get("claim") == "measured" and str(hd.get("value"))[:10] == str(c.get("value"))[:10]
    ok += good
    print("ANSWER %-38s claim=%s value=%s catalog=%s %s" % (row, hd.get("claim"), hd.get("value"), c.get("value"),
                                                            "OK" if good else "BAD"))
ANCHORS = ("mp.01.aum-metrics", "etfs.01.positioning-data")
anc = sum(1 for a in ANCHORS if a in seen)
print("ANSWER-TIME measured rows %d; answered measured and equal %d of %d; anchors measured %d of %d"
      % (len(seen), ok, len(seen), anc, len(ANCHORS)))
sys.exit(0 if seen and ok == len(seen) and anc == len(ANCHORS) else 1)
