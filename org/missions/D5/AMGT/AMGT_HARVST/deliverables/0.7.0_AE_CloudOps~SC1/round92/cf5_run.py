"""HVST-cf-5 driver, run from the pinned worktree (C:/tmp/cf5-build at 04be089e13). ASCII only.

Usage (each fund is a SEPARATE foreground command, always `python -u`, output appended to cf5_run.log by the caller):
  python -u cf5_run.py --fund PFOE --plan     read only: build that one fund in memory, print the manifest line it would write
  python -u cf5_run.py --fund PFOE             the canary write, then the read-back (Branch A)
  python -u cf5_run.py --fund IDVZ             the second write, then the read-back
There is NO loop, NO retry and NO background mode (COO half C-5). It never calls fund_form.write (which writes both funds in
one call), never runs --compare, and writes no dossier or continuation (C-6).

Guards: tree is 04be089e13 with an empty lib/research diff; UTC now inside 2026-10-18 02:45Z to 04:30Z; the funds the build
finds are exactly IDVZ and PFOE with 82 and 33 reports (else STOP); PFOE (the canary) goes first; a fund already in the manifest is
refused; gold_put must report put_performed True and existed False.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys

WT = r"C:\tmp\cf5-build"
sys.path.insert(0, WT)
os.chdir(WT)

from lib.research.corpus import fund_form, gold  # noqa: E402
from lib.research.harvest import store  # noqa: E402

PIN = "04be089e13"
OUT = r"C:\dev\ajb_workspace\org\missions\D5\AMGT\AMGT_HARVST\deliverables\0.7.0_AE_CloudOps~SC1\round92"
MANIFEST = os.path.join(OUT, "cf5_written.out")
WIN_START = datetime.datetime(2026, 10, 18, 2, 45, tzinfo=datetime.timezone.utc)
WIN_END = datetime.datetime(2026, 10, 18, 4, 30, tzinfo=datetime.timezone.utc)
EXPECT = {"PFOE": 33, "IDVZ": 82}
CANARY = "PFOE"


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def stamp():
    return now().strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args):
    return subprocess.run(["git", "-C", WT] + list(args), capture_output=True, text=True, check=True).stdout.strip()


def written():
    out = {}
    if os.path.exists(MANIFEST):
        for ln in open(MANIFEST, encoding="ascii").read().splitlines():
            parts = ln.split()
            if " WROTE form " in ln:
                out[parts[3].replace("fund=", "")] = int(parts[4].replace("reports=", ""))
    return out


def build_one(client, fund):
    items, extract_bytes = fund_form.gather_items(client=client)
    plain = fund_form._drop_extract_key(items)
    funds = fund_form.distinct_funds(plain)
    counts = {}
    for f in funds:
        counts[f] = len(fund_form._inputs_for_fund(f, items, extract_bytes))
    print("BUILD funds=%s counts=%s absent_fund_reports=%d" % (list(funds), counts, fund_form.absent_fund_reports(plain)))
    if counts != EXPECT:
        return None
    inputs = fund_form._inputs_for_fund(fund, items, extract_bytes)
    doc = fund_form.build_document(fund, plain, inputs)
    name = "%s.json" % fund_form._inputs_sha16(inputs)
    return doc, inputs, name, fund_form._canonical_bytes(doc)


def readback(client, fund, uri, name, doc, inputs, nexp):
    body = gold.gold_get(uri, client=client)
    got = json.loads(body.decode("utf-8"))
    problems = []
    if got.get("subject", {}).get("fund") != fund:
        problems.append("subject.fund %r" % (got.get("subject"),))
    if got.get("method_version") != "2":
        problems.append("method_version %r" % (got.get("method_version"),))
    if got.get("fields", {}).get("reports") != nexp:
        problems.append("fields.reports %r != %d" % (got.get("fields", {}).get("reports"), nexp))
    if len(got.get("inputs", [])) != nexp:
        problems.append("inputs %d != %d" % (len(got.get("inputs", [])), nexp))
    recomputed = dict(got)
    stored_sha = recomputed.pop("content_sha256", None)
    if hashlib.sha256(fund_form._canonical_bytes(recomputed)).hexdigest() != stored_sha:
        problems.append("recomputed content_sha256 != stored")
    if stored_sha != doc["content_sha256"]:
        problems.append("stored content_sha256 != the build's")
    if got.get("inputs") != inputs:
        problems.append("inputs differ from the build")
    if "%s.json" % fund_form._inputs_sha16(got.get("inputs", [])) != name:
        problems.append("object name != _inputs_sha16(inputs)")
    for p in problems:
        print("READBACK-PROBLEM %s" % p)
    ok = not problems
    print("READBACK fund=%s reports=%d equal=%s" % (fund, got.get("fields", {}).get("reports", -1), "PASS" if ok else "FAIL"))
    return ok


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fund", required=True)
    ap.add_argument("--plan", action="store_true")
    args = ap.parse_args(argv[1:])
    fund = args.fund
    if fund not in EXPECT:
        print("STOP: %s is not one of the two funds" % fund)
        return 2
    head = git("rev-parse", "HEAD")
    if not head.startswith(PIN) or git("diff", PIN, "HEAD", "--", "lib/research"):
        print("STOP: tree is not %s with an empty lib/research diff (HEAD %s)" % (PIN, head))
        return 2
    client = store._default_client()
    print("=== cf5_run.py fund=%s plan_only=%s start %s HEAD=%s ===" % (fund, args.plan, stamp(), head[:10]))
    built = build_one(client, fund)
    if built is None:
        print("STOP: the build differs from the measurement %s; nothing written" % EXPECT)
        return 4
    doc, inputs, name, payload = built
    n = doc["fields"]["reports"]
    print("FUND %s reports=%d sections=%d object=%s content_sha256=%s bytes=%d" % (
        fund, n, len(doc["fields"]["skeleton"]), name, doc["content_sha256"], len(payload)))
    if args.plan:
        print("PLAN-ONLY; nothing put")
        return 0
    if not (WIN_START <= now() < WIN_END):
        print("STOP: now %s is outside the window 02:45Z to 04:30Z" % stamp())
        return 3
    done = written()
    if fund in done:
        print("STOP: fund %s is already in the manifest" % fund)
        return 2
    if fund != CANARY and CANARY not in done:
        print("STOP: the canary %s must be written and read back first" % CANARY)
        return 2
    try:
        result = gold.gold_put(fund_form.TABLE, "fund=%s" % fund_form._slug(fund), name, payload, client=client)
    except Exception as exc:  # noqa: BLE001
        print("STOP (gold_put): %s: %s -- the bucket state of this fund is UNKNOWN until read" % (type(exc).__name__, exc))
        return 5
    bucket, key = result["bucket"], result["key"]
    head_obj = client.head_object(Bucket=bucket, Key=key)
    line = "%s WROTE form fund=%s reports=%d key=%s VersionId=%s bytes=%d sha256=%s put_performed=%s existed=%s" % (
        stamp(), fund, n, key, head_obj.get("VersionId"), result["content_length"], result["sha256"],
        result["put_performed"], result["existed"])
    with open(MANIFEST, "a", encoding="ascii") as fh:
        fh.write(line + "\n")
    print(line)
    if not result["put_performed"] or result["existed"]:
        print("STOP: put_performed %s existed %s" % (result["put_performed"], result["existed"]))
        return 5
    ok = readback(client, fund, result["uri"], name, doc, inputs, n)
    done = written()
    tail = "%s WRITTEN forms=%d reports=%d" % (stamp(), len(done), sum(done.values()))
    with open(MANIFEST, "a", encoding="ascii") as fh:
        fh.write(tail + "\n")
    print(tail)
    print("=== fund=%s done %s readback=%s ===" % (fund, stamp(), "PASS" if ok else "FAIL"))
    return 0 if ok else 6


if __name__ == "__main__":
    sys.exit(main(sys.argv))
