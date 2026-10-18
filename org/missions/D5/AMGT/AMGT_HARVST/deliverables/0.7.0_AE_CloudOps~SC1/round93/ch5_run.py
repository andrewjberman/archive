"""HVST-ch-5 driver, run from the pinned worktree (C:/tmp/ch5-build at 2e0dc6af2e). ASCII only.

Usage (one foreground command, always `python -u`, output appended to ch5_run.log by the caller):
  python -u ch5_run.py --plan                         read only: build the DIVZ document, print the manifest line it would write
  python -u ch5_run.py --go-utc 2026-10-18T04:30:00Z  the write of the ONE DIVZ object, then the read-back (Branch A)
There is NO loop, NO retry and NO background mode (COO half C-5). It never calls fund_form.write (all three funds), never runs
--write, and writes no dossier or continuation (C-6). The write window is from the issuer's GO (--go-utc, the time of the GO
message) to 90 minutes later; outside it the driver refuses.

Guards: tree is 2e0dc6af2e with an empty lib/research diff; the DIVZ build equals the measurement (object a181f84957dbb8b7.json,
reports 0, content_sha256 starting 34524f75, inputs [], method_version "2", the absent reason); the stored count is 11; the DIVZ
object is not already stored or in the manifest; gold_put must report put_performed True and existed False.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys

WT = r"C:\tmp\ch5-build"
sys.path.insert(0, WT)
os.chdir(WT)

from lib.research.corpus import fund_form, gold  # noqa: E402
from lib.research.harvest import store  # noqa: E402

PIN = "2e0dc6af2e"
OUT = r"C:\dev\ajb_workspace\org\missions\D5\AMGT\AMGT_HARVST\deliverables\0.7.0_AE_CloudOps~SC1\round93"
MANIFEST = os.path.join(OUT, "ch5_written.out")
WANT_NAME = "a181f84957dbb8b7.json"
WANT_SHA_PREFIX = "34524f75"
WANT_ABSENT = "no report whose silver row states fund_relation == holding names DIVZ"
STORED_EXPECTED = 11


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def stamp():
    return now().strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args):
    return subprocess.run(["git", "-C", WT] + list(args), capture_output=True, text=True, check=True).stdout.strip()


def in_manifest():
    return os.path.exists(MANIFEST) and " WROTE form fund=DIVZ " in open(MANIFEST, encoding="ascii").read()


def readback(client, uri, doc):
    body = gold.gold_get(uri, client=client)
    got = json.loads(body.decode("utf-8"))
    problems = []
    if got.get("subject", {}).get("fund") != "DIVZ":
        problems.append("subject.fund %r" % (got.get("subject"),))
    if got.get("method_version") != "2":
        problems.append("method_version %r" % (got.get("method_version"),))
    if got.get("fields", {}).get("reports") != 0:
        problems.append("fields.reports %r" % (got.get("fields", {}).get("reports"),))
    if got.get("fields", {}).get("absent") != WANT_ABSENT:
        problems.append("fields.absent %r" % (got.get("fields", {}).get("absent"),))
    if got.get("fields", {}).get("skeleton") != [] or got.get("fields", {}).get("by_class") != {}:
        problems.append("skeleton or by_class not empty")
    if got.get("inputs") != []:
        problems.append("inputs %r" % (got.get("inputs"),))
    rec = dict(got)
    stored_sha = rec.pop("content_sha256", None)
    if hashlib.sha256(fund_form._canonical_bytes(rec)).hexdigest() != stored_sha:
        problems.append("recomputed content_sha256 != stored")
    if stored_sha != doc["content_sha256"]:
        problems.append("stored content_sha256 != the build's")
    if "%s.json" % fund_form._inputs_sha16(got.get("inputs", [])) != WANT_NAME:
        problems.append("object name != _inputs_sha16(inputs)")
    for p in problems:
        print("READBACK-PROBLEM %s" % p)
    ok = not problems
    print("READBACK fund=DIVZ reports=%s equal=%s" % (got.get("fields", {}).get("reports"), "PASS" if ok else "FAIL"))
    return ok


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--go-utc")
    args = ap.parse_args(argv[1:])
    head = git("rev-parse", "HEAD")
    if not head.startswith(PIN) or git("diff", PIN, "HEAD", "--", "lib/research"):
        print("STOP: tree is not %s with an empty lib/research diff (HEAD %s)" % (PIN, head))
        return 2
    client = store._default_client()
    print("=== ch5_run.py plan_only=%s start %s HEAD=%s ===" % (args.plan, stamp(), head[:10]))
    items, extract_bytes = fund_form.gather_items(client=client)
    plain = fund_form._drop_extract_key(items)
    inputs = fund_form._inputs_for_fund("DIVZ", items, extract_bytes)
    doc = fund_form.build_document("DIVZ", plain, inputs)
    name = "%s.json" % fund_form._inputs_sha16(inputs)
    payload = fund_form._canonical_bytes(doc)
    print("FORM DIVZ reports=%d object=%s content_sha256=%s inputs=%d bytes=%d" % (
        doc["fields"]["reports"], name, doc["content_sha256"], len(inputs), len(payload)))
    if (name != WANT_NAME or doc["fields"]["reports"] != 0 or not doc["content_sha256"].startswith(WANT_SHA_PREFIX)
            or inputs != [] or doc["method_version"] != "2" or doc["fields"].get("absent") != WANT_ABSENT):
        print("STOP: the DIVZ build differs from the measurement; nothing written")
        return 4
    keys = gold.gold_list(fund_form.TABLE, client=client)
    divz_key = "%sfund=divz/%s" % (gold.table_prefix(fund_form.TABLE), name)
    print("STORED-COUNT %d (expected %d); DIVZ target key present: %s" % (len(keys), STORED_EXPECTED, divz_key in keys))
    if len(keys) != STORED_EXPECTED or divz_key in keys:
        print("STOP: the stored count is not %d or the DIVZ object already exists; nothing written" % STORED_EXPECTED)
        return 4
    if args.plan:
        print("PLAN-ONLY; nothing put")
        return 0
    if not args.go_utc:
        print("STOP: a write needs --go-utc (the time of the issuer's GO)")
        return 2
    go = datetime.datetime.strptime(args.go_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    if not (go <= now() < go + datetime.timedelta(minutes=90)):
        print("STOP: now %s is outside the window %s to +90 minutes" % (stamp(), args.go_utc))
        return 3
    if in_manifest():
        print("STOP: DIVZ is already in the manifest")
        return 2
    try:
        result = gold.gold_put(fund_form.TABLE, "fund=divz", name, payload, client=client)
    except Exception as exc:  # noqa: BLE001
        print("STOP (gold_put): %s: %s -- the bucket state is UNKNOWN until read" % (type(exc).__name__, exc))
        return 5
    head_obj = client.head_object(Bucket=result["bucket"], Key=result["key"])
    line = "%s WROTE form fund=DIVZ reports=0 key=%s VersionId=%s bytes=%d sha256=%s put_performed=%s existed=%s" % (
        stamp(), result["key"], head_obj.get("VersionId"), result["content_length"], result["sha256"],
        result["put_performed"], result["existed"])
    with open(MANIFEST, "a", encoding="ascii") as fh:
        fh.write(line + "\n")
    print(line)
    if not result["put_performed"] or result["existed"]:
        print("STOP: put_performed %s existed %s" % (result["put_performed"], result["existed"]))
        return 5
    ok = readback(client, result["uri"], doc)
    tail = "%s WRITTEN forms=1 reports=0" % stamp()
    with open(MANIFEST, "a", encoding="ascii") as fh:
        fh.write(tail + "\n")
    print(tail)
    print("=== fund=DIVZ done %s readback=%s ===" % (stamp(), "PASS" if ok else "FAIL"))
    return 0 if ok else 6


if __name__ == "__main__":
    sys.exit(main(sys.argv))
