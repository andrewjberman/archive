"""c10_second.py -- MX-r-11 AC3 instrument (FWD-20 PROOF): one (a) tool's catalog depth and freshness against the served
artifact, read by a SECOND instrument (the aws CLI listing, never the emitter's own boto3 read).

AMENDED A1 (2.0.0_SA_COO~MI, 2026-10-13 ~21:4xZ, at the MX-c-8 drain). As MX-c-8 measured them, every (a) tool's
`history_depth` reads `absent`, because each served object is one overwritten file with no date in its key. A measured
`freshness` names its served object through the catalog `row` it was read from (basis = the bucket root; the naming
gate refuses re-typed platinum/ key literals, row Z-W33-S5). The pick and the grade follow that shape.

Usage:
  python c10_second.py pick <catalog yaml>    -> "PICK <tool> <bucket> <key> <method> <fresh> <depth_claim> <depth_value|->"
  python c10_second.py grade <pick line file> <listing file>
PICK: the FIRST tool_index entry, by tool name, with member a, `freshness.claim` measured, a method in
{last-modified, key-date}, and an `s3://<bucket>/` basis. Its object key is the `key` of the catalog mapping whose
`entity` equals `freshness.row` (or the basis path itself when it names a key).
LISTING: `Key<TAB>LastModified` lines from `list-objects-v2 --prefix <key>`.
GRADE:
  FRESHNESS -- the listed object's date (LastModified UTC, or the key's date for key-date) is on or after the catalog
               freshness value (the object can only be re-written after emission).
  DEPTH     -- claim absent: CONFIRMED when exactly one object sits at the key and the key carries no date segment (no
               history is listable). Claim measured: the earliest listed date equals the catalog value.
"""
import re
import sys

DATE = re.compile(r"(\d{4}-\d{2}-\d{2}|(?<!\d)\d{8}(?!\d))")


def norm(d: str) -> str:
    d = d.strip()
    return "%s-%s-%s" % (d[:4], d[4:6], d[6:8]) if re.fullmatch(r"\d{8}", d) else d[:10]


if sys.argv[1] == "pick":
    import yaml
    doc = yaml.safe_load(open(sys.argv[2], encoding="ascii"))
    keys: dict = {}

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
    for e in sorted((doc.get("tool_index") or []), key=lambda x: str(x.get("tool", ""))):
        fr, hd = e.get("freshness") or {}, e.get("history_depth") or {}
        if e.get("member") != "a" or fr.get("claim") != "measured" or fr.get("method") not in ("last-modified", "key-date"):
            continue
        m = re.fullmatch(r"s3://([^/]+)/(.*)", str(fr.get("basis") or ""))
        if not m:
            continue
        key = m.group(2) or keys.get(str(fr.get("row") or ""), "")
        if not key:
            continue
        print("PICK %s %s %s %s %s %s %s" % (e["tool"], m.group(1), key, fr["method"], norm(str(fr["value"])),
                                             hd.get("claim") or "none", norm(str(hd.get("value"))) if hd.get("value") else "-"))
        sys.exit(0)
    print("PICK none: no (a) tool_index entry carries a measured freshness resolvable to one served key")
    sys.exit(1)

_, tool, bucket, key, method, fresh, dclaim, dvalue = open(sys.argv[2], encoding="utf-8").read().split()
objs = []
for line in open(sys.argv[3], encoding="utf-8"):
    parts = line.rstrip("\n").split("\t")
    if len(parts) < 2 or parts[0] in ("", "None"):
        continue
    if method == "key-date":
        m = DATE.search(parts[0])
        d = norm(m.group(1)) if m else ""
    else:
        d = parts[1][:10]
    objs.append((parts[0], d))
dated = [d for _, d in objs if d]
if not dated:
    print("GRADE %s objects 0 dated under s3://%s/%s: no second reading" % (tool, bucket, key))
    sys.exit(1)
latest = max(dated)
f_ok = fresh <= latest
if dclaim == "absent":
    exact = [k for k, _ in objs if k == key]
    d_ok = len(objs) == 1 and len(exact) == 1 and not DATE.search(key)
    dline = "depth=absent objects_at_key=%d listed=%d key_has_date=%s %s" % (len(exact), len(objs), bool(DATE.search(key)),
                                                                        "CONFIRMED" if d_ok else "REFUTED")
elif dclaim == "measured":
    d_ok = min(dated) == dvalue
    dline = "depth=measured earliest=%s catalog=%s %s" % (min(dated), dvalue, "AGREE" if d_ok else "DISAGREE")
else:
    d_ok, dline = False, "depth claim %s is not gradable" % dclaim
print("GRADE %s s3://%s/%s method=%s latest=%s catalog_fresh=%s %s; %s"
      % (tool, bucket, key, method, latest, fresh, "AGREE" if f_ok else "DISAGREE", dline))
sys.exit(0 if f_ok and d_ok else 1)
