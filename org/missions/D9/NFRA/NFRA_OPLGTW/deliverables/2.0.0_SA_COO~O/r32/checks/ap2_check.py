"""OPLGTW OG-ap-2 checks (OG-bf-1 leg Y, the 49F dispatcher date gate, deployed by the site Z applier).

  python ap2_check.py AC1 <repo_root>
      The LIVE advi-49f-gold-dispatch zip (aws lambda get-function -> Code.Location, downloaded) holds lambda_function.py
      and trading_calendar.py byte-equal to box/sitez HEAD's
      infra/aws/lambda/opal-assets/advi-49f-gold-dispatch/lambda_function.py and lib/trading_calendar.py; the live
      CodeSha256 is no longer the rollback hash TjIWGFWk...; the function reads State Active, LastUpdateStatus Successful.
  python ap2_check.py AC2 <record.json>
      Arm 1: the record names the RequestId of one synthetic invoke; the function's own CloudWatch log for that RequestId
      carries a 'SKIP:' line naming 'is not the production T-1' and no 'dispatched: doc=' line.
"""
import io
import json
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

FN = "advi-49f-gold-dispatch"
ROLLBACK = "TjIWGFWkbUswLkA+mUac9NS+LRZ1q7o6lR1iQLb0kI4="


def aws(args, root):
    shim = Path(root) / ".tools" / ("aws.cmd" if sys.platform == "win32" else "aws")
    p = subprocess.run([str(shim)] + args + ["--region", "us-east-1", "--output", "json"], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=100)
    if p.returncode != 0:
        raise RuntimeError("aws %s rc=%d" % (args[:2], p.returncode))
    return json.loads(p.stdout or "null")


def ac1(root):
    root = Path(root)
    fn = aws(["lambda", "get-function", "--function-name", FN], root)
    cfg = fn["Configuration"]
    data = urllib.request.urlopen(fn["Code"]["Location"], timeout=60).read()
    z = zipfile.ZipFile(io.BytesIO(data))
    want = {"lambda_function.py": root / "infra/aws/lambda/opal-assets/advi-49f-gold-dispatch/lambda_function.py",
            "trading_calendar.py": root / "lib/trading_calendar.py"}
    names = set(z.namelist())
    ok = True
    for member, src in want.items():
        same = member in names and z.read(member) == src.read_bytes()
        print("member %s: present=%s equal-to-HEAD=%s" % (member, member in names, same))
        ok = ok and same
    print("live CodeSha256=%s (rollback %s); State=%s LastUpdateStatus=%s"
          % (cfg.get("CodeSha256"), ROLLBACK, cfg.get("State"), cfg.get("LastUpdateStatus")))
    ok = ok and cfg.get("CodeSha256") != ROLLBACK and cfg.get("State") == "Active" \
        and cfg.get("LastUpdateStatus") == "Successful"
    return ok


def ac2(record, root):
    try:
        rec = json.load(open(record, encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("record unreadable: %s (%s)" % (record, type(exc).__name__))
        return False
    rid = rec.get("request_id") or ""
    if not rid:
        print("record names no request_id")
        return False
    # Only START/END/REPORT lines carry the RequestId (row NFRA_OPLGTW-Z-S71). Find them, then read EVERY line of that
    # log stream between START and END: the invocation's own output.
    group = "/aws/lambda/" + FN
    marks = aws(["logs", "filter-log-events", "--log-group-name", group, "--filter-pattern", '"%s"' % rid,
                 "--start-time", str(int(rec.get("invoked_epoch_ms", 0)) - 60000)], root).get("events", [])
    starts = [e for e in marks if e.get("message", "").startswith("START")]
    ends = [e for e in marks if e.get("message", "").startswith(("END", "REPORT"))]
    if not starts or not ends:
        print("request %s: START/END not found (%d marker events)" % (rid, len(marks)))
        return False
    stream = starts[0]["logStreamName"]
    t0, t1 = starts[0]["timestamp"], max(e["timestamp"] for e in ends)
    ev = aws(["logs", "filter-log-events", "--log-group-name", group, "--log-stream-names", stream,
              "--start-time", str(t0), "--end-time", str(t1 + 1)], root).get("events", [])
    text = "\n".join(e.get("message", "") for e in ev)
    skip = "SKIP:" in text and "is not the production T-1" in text
    disp = "dispatched: doc=" in text
    print("request %s: log events %d; SKIP with 'is not the production T-1' %s; 'dispatched: doc=' %s"
          % (rid, len(ev), skip, disp))
    return len(ev) > 0 and skip and not disp


def main(argv):
    if len(argv) < 3 or argv[1] not in ("AC1", "AC2"):
        print(__doc__)
        return 2
    try:
        ok = ac1(argv[2]) if argv[1] == "AC1" else ac2(argv[2], argv[3] if len(argv) > 3 else ".")
    except Exception as exc:  # the instrument's own failure is a FAIL, never a pass
        print("instrument failure: %s" % type(exc).__name__)
        ok = False
    print("RESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
