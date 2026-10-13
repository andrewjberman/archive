"""c10_second.py -- MX-r-11 AC3 instrument (FWD-20 PROOF): one tool's catalog depth and freshness against the served
artifact, read by a SECOND instrument (the aws CLI listing, never the emitter's own boto3 read).

Usage:
  python c10_second.py pick <catalog yaml>            -> prints "PICK <tool> <bucket> <prefix> <method> <depth> <fresh>"
  python c10_second.py grade <pick line file> <listing file>
The pick is the FIRST tool_index entry, by tool name, whose history_depth AND freshness both read claim measured with an
`s3://<bucket>/<prefix>` basis and a method in {key-date, last-modified}. The listing is `Key<TAB>LastModified` lines.
key-date: the date is the first YYYY-MM-DD (or YYYYMMDD) in the key; last-modified: the UTC date of LastModified.
DEPTH must equal the earliest date exactly; FRESHNESS must be <= the latest date (it can only advance after emission).
"""
import re
import sys


def norm(d: str) -> str:
    d = d.strip()
    return "%s-%s-%s" % (d[:4], d[4:6], d[6:8]) if re.fullmatch(r"\d{8}", d) else d[:10]


if sys.argv[1] == "pick":
    import yaml
    doc = yaml.safe_load(open(sys.argv[2], encoding="ascii"))
    for e in sorted((doc.get("tool_index") or []), key=lambda x: str(x.get("tool", ""))):
        hd, fr = e.get("history_depth") or {}, e.get("freshness") or {}
        if hd.get("claim") != "measured" or fr.get("claim") != "measured":
            continue
        m = re.fullmatch(r"s3://([^/]+)/(.*)", str(hd.get("basis") or ""))
        if not m or hd.get("method") not in ("key-date", "last-modified") or fr.get("basis") != hd.get("basis"):
            continue
        print("PICK %s %s %s %s %s %s" % (e["tool"], m.group(1), m.group(2) or "-", hd["method"], norm(str(hd["value"])),
                                          norm(str(fr["value"]))))
        sys.exit(0)
    print("PICK none: no tool_index entry carries measured depth and freshness on one s3:// basis with a method")
    sys.exit(1)

_, tool, bucket, prefix, method, depth, fresh = open(sys.argv[2], encoding="utf-8").read().split()
dates = []
for line in open(sys.argv[3], encoding="utf-8"):
    parts = line.rstrip("\n").split("\t")
    if len(parts) < 2 or parts[0] in ("", "None"):
        continue
    if method == "key-date":
        m = re.search(r"(\d{4}-\d{2}-\d{2}|(?<!\d)\d{8}(?!\d))", parts[0])
        if m:
            dates.append(norm(m.group(1)))
    else:
        dates.append(parts[1][:10])
if not dates:
    print("GRADE %s objects dated 0 under s3://%s/%s: no second reading" % (tool, bucket, prefix))
    sys.exit(1)
lo, hi = min(dates), max(dates)
ok = lo == depth and fresh <= hi
print("GRADE %s s3://%s/%s method=%s objects_dated=%d earliest=%s catalog_depth=%s latest=%s catalog_fresh=%s %s"
      % (tool, bucket, prefix, method, len(dates), lo, depth, hi, fresh, "AGREE" if ok else "DISAGREE"))
sys.exit(0 if ok else 1)
