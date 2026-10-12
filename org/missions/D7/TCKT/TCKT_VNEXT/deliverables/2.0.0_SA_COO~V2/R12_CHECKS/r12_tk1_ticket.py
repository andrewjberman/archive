"""TCKT_VNEXT round 12 -- R12-tk-1: ONE test ticket in tenant cottonwood exists in the live store, titled as a test, open,
created by svc-commentary, and the result file lists exactly that one ticket in its write set.

The ticket is re-read here with one live get-item, independent of the result file's own claims.
Prints TK1-OK <detail> or TK1-FAIL <reason>; exit 0/1.
"""
import json
import os
import re
import subprocess
import sys

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r12_tk1/R12_TEST_TICKET_20261012.json"
KEYS = {"ticket_id", "http_status", "write_set", "deleted", "token_printed", "claim"}
TID = re.compile(r"^TCK-\d{8}-[0-9a-f]{8}$")
PRIOR = {"TCK-20261009-a1052909", "TCK-20261009-67ab7f27"}
AWS = os.path.abspath(".tools/aws.cmd")


def main():
    try:
        raw = open(RES, encoding="utf-8").read()
        doc = json.loads(raw)
    except (OSError, ValueError) as e:
        print("TK1-FAIL cannot read the result file: %s" % e)
        return 1
    if "@" in raw:
        print("TK1-FAIL the file holds an address")
        return 1
    missing = sorted(KEYS - set(doc))
    if missing:
        print("TK1-FAIL missing key(s): %s" % missing)
        return 1
    tid = doc["ticket_id"]
    if not TID.match(str(tid)) or tid in PRIOR:
        print("TK1-FAIL ticket_id is not a new ticket id: %r" % (tid,))
        return 1
    if doc["http_status"] != 201 or doc["deleted"] is not False or doc["token_printed"] is not False:
        print("TK1-FAIL status/deleted/token_printed not 201/False/False")
        return 1
    ws = doc["write_set"]
    if not isinstance(ws, list) or sum(1 for w in ws if str(w).startswith("ticket:")) != 1 or "ticket:" + tid not in ws:
        print("TK1-FAIL write_set must name exactly the one ticket: %r" % (ws,))
        return 1
    key = json.dumps({"ticket_id": {"S": tid}})
    try:
        out = subprocess.run([AWS, "dynamodb", "get-item", "--table-name", "opal-tickets", "--key", key,
                              "--region", "us-east-1", "--output", "json"],
                             capture_output=True, text=True, timeout=120)
        item = json.loads(out.stdout)["Item"]
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as e:
        print("TK1-FAIL live get-item found no ticket %s: %s" % (tid, e))
        return 1
    def s(k):
        return item.get(k, {}).get("S")

    firm = item.get("requester", {}).get("M", {}).get("firm", {}).get("S")
    bad = []
    if s("ticket_type") != "analysis_request":
        bad.append("ticket_type")
    if s("status") != "open":
        bad.append("status")
    if s("created_by") != "svc-commentary":
        bad.append("created_by")
    if firm != "cottonwood":
        bad.append("firm")
    if not (s("title") or "").startswith("[TEST TCKT_VNEXT R12]"):
        bad.append("title")
    if bad:
        print("TK1-FAIL live ticket %s differs on: %s" % (tid, bad))
        return 1
    print("TK1-OK %s firm=cottonwood status=open created_by=svc-commentary" % tid)
    return 0


if __name__ == "__main__":
    sys.exit(main())
