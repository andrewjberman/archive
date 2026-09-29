"""AMGT_RESAPP round 48, AMGT-ww-3 AC1 -- THE TABLE'S OWN WRITER PLANS THE RESEARCH LIBRARY'S MISSING ROWS, AND ONLY THOSE.

`etf-classifications` has one writer for security rows: `seed-etf-constituents.py` (CTO analysis round 47 section 4 row 2: "POSN's
writer moves the AMGT rows"). Built here: a second UNIVERSE on that writer, `--universe amgt-library`, read from the research
library's stored model blocks (the 95 names in fixtures/library95.json at the cut). Its dry-run must plan:
 - CREATE exactly the library bare tickers the table does not hold (measured live now), each row asset_class `equity` and
   sub_asset_class = the block's own GICS_SECTOR_NAME (non-empty), and a name that is NEVER all-caps (Andrew-direct 2026-08-25:
   "properly capitalized (no all caps)") and never the ticker -- a name with no clean source is withheld (absent);
 - PRESERVE every library ticker the table already holds (no update without --force-names).
usage: python <this>   (from the repo root; reads S3 and DynamoDB read-only; writes nothing)"""
import json
import os
import re
import subprocess
import sys

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
WRITER = "infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-constituents.py"


def main():
    lib = json.load(open(os.path.join(HERE, "fixtures", "library95.json"), encoding="utf-8"))["names"]
    bares = sorted({n["bare"] for n in lib})
    t = boto3.resource("dynamodb", region_name="us-east-1").Table("etf-classifications")
    held = {b for b in bares if t.get_item(Key={"ticker": b}).get("Item")}
    want_create = set(bares) - held
    print("library %d, held now %d, absent now %d" % (len(bares), len(held), len(want_create)))
    env = dict(os.environ, PYTHONPATH=os.getcwd(), PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, WRITER, "--universe", "amgt-library", "--dry-run"], capture_output=True, text=True,
                       encoding="utf-8", env=env, timeout=110)
    out = p.stdout
    bad = []
    if p.returncode != 0 or "[DRY RUN] nothing written." not in out:
        bad.append("writer dry-run rc=%s: %s" % (p.returncode, (p.stderr or out).strip().splitlines()[-1:] or ""))
    plan = re.search(r"PLAN: (\d+) create / (\d+) update / (\d+) preserve-existing", out)
    creates = {}
    for m in re.finditer(r"^\s+CREATE (\S+)\s+(.*?)\s+(\S+) / (.*)$", out, re.M):
        creates[m.group(1)] = (m.group(2), m.group(3), m.group(4).strip())
    if not plan:
        bad.append("no PLAN line")
    else:
        c, u, k = map(int, plan.groups())
        if (c, u, k) != (len(want_create), 0, len(held)):
            bad.append("PLAN %d/%d/%d, want %d/0/%d" % (c, u, k, len(want_create), len(held)))
    if set(creates) != want_create:
        bad.append("CREATE set differs: extra %s missing %s" % (sorted(set(creates) - want_create)[:5], sorted(want_create - set(creates))[:5]))
    for tk, (name, ac, sac) in sorted(creates.items()):
        nm = name.strip("'\"")
        if ac != "equity" or not sac:
            bad.append("%s classification %r / %r" % (tk, ac, sac))
        if name != "None" and (nm == tk or (re.search(r"[A-Z]{2}", nm) and nm == nm.upper())):
            bad.append("%s name %r is all-caps or the ticker" % (tk, nm))
    for b in bad[:12]:
        print("  BAD", b)
    named = sum(1 for v in creates.values() if v[0] != "None")
    print("planned creates %d (named %d, name withheld %d)" % (len(creates), named, len(creates) - named))
    ok = not bad
    print("THE TABLE'S WRITER PLANS EXACTLY THE LIBRARY'S MISSING ROWS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
