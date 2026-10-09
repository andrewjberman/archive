"""AMGT_RESAPP round 88 item 1 (CTO~DELL1 round-87 analysis) -- the FAILED-description withhold DRIVEN on a planted copy of the store.

  python r88_planted.py [--reader-ref HEAD] [--expect-withhold yes|no]

Read-only: copies the five stored drafts (`s3://opal-data-harvest/drafting/v1/<KEY>.json`, latest) into a temp directory and PLANTS one
FAILED description: NU's copy is its PRIOR stored version `ms8LxPe84kA9x8qb4L4f74vtKnlO2HRQ` (round 86, kk-3), whose one
company_description sentence (a launch metric) reads FAILED. The reader is `lib/research/api/scoped_amgt.py` AT --reader-ref, loaded
from `git show` (HEAD = the deployed bytes: its sha256 is printed beside the live package member's), pointed at the copy through
`AMGT_DRAFTING_ROOT`. NOTHING is written to the served store.
    P1 planted NU: --expect-withhold yes -> 0 description sentences, verdict FAILED, withheld_failed >= 1, description_verdict_test set;
       --expect-withhold no (the negative arm, an older reader) -> the FAILED sentence IS served (>= 1 sentence);
    P2 the /overlay description for planted NU is not SERVED and carries the failing test's detail (yes arm only);
    P3 control: ASML, BABA, PBR, SAP read from the same copy serve exactly what the live function serves for them (company_description
       sentence texts equal, verdict equal).
Verdict: R88 PLANTED: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

BUCKET = "opal-data-harvest"
KEYS = ("ASML_NA_Equity", "BABA_US_Equity", "NU_US_Equity", "PBR_US_Equity", "SAP_GY_Equity")
PLANT_KEY = "NU_US_Equity"
PLANT_VERSION = "ms8LxPe84kA9x8qb4L4f74vtKnlO2HRQ"
MEMBER = "lib/research/api/scoped_amgt.py"
FN = "opal-amgt-scoped-api"
SECTION = "company_description"


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def _desc(block):
    for s in block.get("drafted_sections") or []:
        if s.get("section_id") == SECTION:
            return s
    return {}


def _live_thesis(key):
    import boto3

    event = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
    lam = boto3.client("lambda", region_name="us-east-1")
    r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    return json.loads(r.get("body") or "{}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader-ref", default="HEAD")
    ap.add_argument("--expect-withhold", choices=("yes", "no"), default="yes")
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    sys.path.insert(0, root)
    import boto3

    s3 = boto3.client("s3", region_name="us-east-1")
    src = subprocess.run(["git", "show", "%s:%s" % (a.reader_ref, MEMBER)], capture_output=True, cwd=root).stdout
    if not src:
        print("ERROR: git show %s:%s read nothing" % (a.reader_ref, MEMBER))
        return 2
    f = boto3.client("lambda", region_name="us-east-1").get_function(FunctionName=FN)
    z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(f["Code"]["Location"], timeout=120).read()))
    dep = z.read([n for n in z.namelist() if n.endswith(MEMBER)][0])
    print("   reader %s:%s sha256 %s | live %s member sha256 %s | equal %s" % (
        a.reader_ref, MEMBER, hashlib.sha256(src).hexdigest()[:16], f["Configuration"]["CodeSha256"][:12],
        hashlib.sha256(dep).hexdigest()[:16], src == dep))
    tmp = tempfile.mkdtemp(prefix="r88_planted_")
    for key in KEYS:
        kw = {"Bucket": BUCKET, "Key": "drafting/v1/%s.json" % key}
        if key == PLANT_KEY:
            kw["VersionId"] = PLANT_VERSION
        body = s3.get_object(**kw)["Body"].read()
        open(os.path.join(tmp, "%s.json" % key), "wb").write(body)
    print("   copy: %s (5 drafts; %s planted from VersionId %s); the served store is not written" % (tmp, PLANT_KEY, PLANT_VERSION))
    # the reader locates drafting/schema.json from its own path: mirror lib/research/{api,drafting} from the SAME ref
    os.makedirs(os.path.join(tmp, "lib", "research", "api"))
    os.makedirs(os.path.join(tmp, "lib", "research", "drafting"))
    schema = subprocess.run(["git", "show", "%s:lib/research/drafting/schema.json" % a.reader_ref], capture_output=True, cwd=root).stdout
    open(os.path.join(tmp, "lib", "research", "drafting", "schema.json"), "wb").write(schema)
    modpath = os.path.join(tmp, "lib", "research", "api", "scoped_amgt_reader.py")
    open(modpath, "wb").write(src)
    spec = importlib.util.spec_from_file_location("r88_reader", modpath)
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    os.environ[reader.ENV_DRAFTING_ROOT] = tmp
    planted = reader.read_drafted_sections(PLANT_KEY)
    d = _desc(planted)
    n = len(d.get("sentences") or [])
    print("   planted %s: status %s, %s sentences %d, verdict %s, withheld_failed %s, test set %s" % (
        PLANT_KEY, planted.get("drafting_status"), SECTION, n, d.get("description_verdict_state"), d.get("withheld_failed"),
        bool(d.get("description_verdict_test"))))
    if a.expect_withhold == "yes":
        p1 = say(n == 0 and d.get("description_verdict_state") == "FAILED" and (d.get("withheld_failed") or 0) >= 1
                 and bool(d.get("description_verdict_test")),
                 "P1 the planted FAILED description is withheld (0 sentences, FAILED, withheld_failed, test kept)")
        ov = reader.read_description(PLANT_KEY, model_block={}, drafting=planted)
        detail = json.dumps(ov.get("describes_business_test") or ov.get("probes") or "")
        print("   /overlay description: status %s, reason %s" % (ov.get("status"), str(ov.get("reason"))[:120]))
        p2 = say(ov.get("status") != "SERVED" and ("failed_on" in detail or "rule" in detail),
                 "P2 the /overlay description is not served and carries the failing test's detail")
    else:
        p1 = say(n >= 1, "P1 (negative arm, reader %s) the planted FAILED sentence IS served: %d sentence(s)" % (a.reader_ref, n))
        p2 = True
    bad = []
    for key in KEYS:
        if key == PLANT_KEY:
            continue
        mine = _desc(reader.read_drafted_sections(key))
        live = _desc(_live_thesis(key))
        same = ([s.get("text") for s in mine.get("sentences") or []] == [s.get("text") for s in live.get("sentences") or []]
                and mine.get("description_verdict_state") == live.get("description_verdict_state"))
        print("   control %-15s copy %d / live %d sentences, verdict %s / %s, equal %s" % (
            key, len(mine.get("sentences") or []), len(live.get("sentences") or []), mine.get("description_verdict_state"),
            live.get("description_verdict_state"), same))
        if not same:
            bad.append(key)
    p3 = say(not bad, "P3 control: the four unplanted names serve exactly what live serves: %d of 4 (differ %s)" % (4 - len(bad), bad))
    ok = p1 and p2 and p3
    print("R88 PLANTED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
