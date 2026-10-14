"""c11_depth.py -- MX-c-9 AC3 / MX-r-12 instrument (FWD-20 depth, PRD v0.10 item 2): depth is read from the served
artifact, and one MEASURED depth is compared with its artifact by a SECOND instrument.

Usage: python c11_depth.py <gateway dir> <catalog yaml> <aws exe>

PART 1 -- the catalog's (a) entries. Each `history_depth` is a valid claim: measured and inferred carry `value` and
`basis`; absent carries `reason`. A MEASURED entry names its served object through `row` (plus `scope` when the row key
holds `{scope}`) and the body field it read (`field`, a dotted path). For EACH measured entry, this instrument fetches
the object with the aws CLI (never the emitter's boto3) and reads that one field: a date (or a list whose first element
is a date). It must equal `value`. `mdpf_get_aggregate_aua` is required to be measured: its object carries `as_of_first`
(CTO round-10 analysis, row Z-W33-S1).
PART 2 -- answer time. In-process discover, as the Opal-internal principal, on "What is the AUA trend over time for a
firm?" (the row's own example question). Its first portal_mdpf_aggregate_aua match carries a history depth read at answer
time from the served artifact, claim measured, equal to the PART 1 value read for that row. The match is the row whose
`property.entity` is the AUA entry's `row` (at issuance the channel row mp.03.aggregate-aua-timeseries, the first
answer to that question), or the portal_datasets entity.
Only a date is printed; no other value of any object is read out.
"""
import json
import os
import subprocess
import sys
import tempfile

gw, cat_path, aws = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3]
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
CLAIMS = {"measured", "inferred", "absent"}


def dig(obj, path):
    for part in str(path).split("."):
        if isinstance(obj, dict):
            obj = obj.get(part)
        else:
            return None
    if isinstance(obj, list) and obj:
        obj = obj[0]
    return str(obj)[:10] if obj is not None else None


a = [e for e in (doc.get("tool_index") or []) if isinstance(e, dict) and e.get("member") == "a"]
valid = measured = verified = inferred = absent = 0
aua_value = None
aua_row = None
for e in a:
    hd = e.get("history_depth") or {}
    c = hd.get("claim")
    ok = c in CLAIMS and (bool(str(hd.get("reason") or "").strip()) if c == "absent"
                          else bool(str(hd.get("value") or "").strip()) and bool(str(hd.get("basis") or "").strip()))
    valid += ok
    absent += c == "absent"
    inferred += c == "inferred"
    if c != "measured":
        continue
    measured += 1
    basis = str(hd.get("basis") or "")
    bucket = basis[5:].split("/", 1)[0] if basis.startswith("s3://") else ""
    key = keys.get(str(hd.get("row") or ""), "").replace("{scope}", str(hd.get("scope") or ""))
    got = None
    if bucket and key and hd.get("field"):
        fd, tmp = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        p = subprocess.run([aws, "s3", "cp", "s3://%s/%s" % (bucket, key), tmp, "--only-show-errors"],
                           capture_output=True, text=True, timeout=120)
        if p.returncode == 0:
            try:
                got = dig(json.load(open(tmp, encoding="utf-8")), hd["field"])
            except ValueError:
                got = None
        os.remove(tmp)
    agree = got is not None and got == str(hd.get("value"))[:10]
    verified += agree
    if e.get("tool") == "mdpf_get_aggregate_aua" and agree:
        aua_value, aua_row = got, str(hd.get("row") or "")
    print("DEPTH %s row=%s key=%s field=%s catalog=%s second_instrument=%s %s"
          % (e.get("tool"), hd.get("row"), key or "-", hd.get("field"), hd.get("value"), got, "AGREE" if agree else "DISAGREE"))
print("PART1 (a) entries %d; depth claims valid %d of %d; measured %d (verified by the second instrument %d of %d); "
      "inferred %d; absent %d; mdpf_get_aggregate_aua measured=%s" % (len(a), valid, len(a), measured, verified, measured,
                                                                     inferred, absent, aua_value or "NO"))

sys.path.insert(0, gw)
os.chdir(gw)
from app.graphql_plumbing import catalog_gate as g  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402

r = od.discover("What is the AUA trend over time for a firm?", g.OPAL_INTERNAL)
AUA_IDS = {"mp.03.aggregate-aua-timeseries", "portal_mdpf_aggregate_aua"} | ({aua_row} if aua_row else set())
m = [x for x in (r.get("matches") or []) if (x.get("property") or {}).get("entity") in AUA_IDS
     or x.get("dataset") in AUA_IDS]
hd = {}
if m:
    f = m[0].get("freshness") or {}
    hd = m[0].get("history_depth") or f.get("history_depth") or {}
ans_ok = bool(m) and hd.get("claim") == "measured" and aua_value is not None and str(hd.get("value"))[:10] == aua_value
print("PART2 discover AUA match=%s answer-time depth claim=%s value=%s (part 1: %s) %s"
      % (bool(m), hd.get("claim"), hd.get("value"), aua_value, "OK" if ans_ok else "BAD"))
ok = a and valid == len(a) and measured >= 1 and verified == measured and aua_value is not None and ans_ok
sys.exit(0 if ok else 1)
