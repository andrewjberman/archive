"""IRPT_ANLREQ TO-READ-RETENTION-CENSUS-R34Q (applier 0.7.0_AE_CloudOps~IB2): READ ONLY. Counts only; no row body, key or id is printed.

  python census_r34q.py   one paginated scan of the PROD request index (irpt-requests) to the end.
"""
from __future__ import annotations

import datetime
from pathlib import Path

import boto3
from boto3.dynamodb.types import TypeDeserializer

HERE = Path(__file__).resolve().parent
TABLE = "irpt-requests"
COMBOS = [("irpt-dashbd-x10-v1", "301c58e24ff0feda"), ("irpt-dashbd-x10-v1", "244a20425ba40cde"), ("irpt-anlreq-audit-x10-v1", "2b4f91d3feda649b"), ("irpt-anlreq-x10-v1", "8edbe84b05765c36")]
EXACT = {"irpt-dashbd-x10-v1", "irpt-anlreq-audit-x10-v1"}
KNOWN3 = {"301c58e24ff0feda", "244a20425ba40cde", "2b4f91d3feda649b"}
OUT = []


def say(x):
    OUT.append(x)
    print(x)


def main():
    des = TypeDeserializer()
    ddb = boto3.client("dynamodb", region_name="us-east-1")
    say("R0 date=%s table=%s denominator=paginated scan to the end, counted client-side" % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), TABLE))
    scanned, ret = 0, 0
    c1 = {k: 0 for k in COMBOS}
    other_hash = other_spelling = 0
    for pg in ddb.get_paginator("scan").paginate(TableName=TABLE):
        scanned += pg["ScannedCount"]
        for it in pg["Items"]:
            r = {k: des.deserialize(v) for k, v in it.items()}
            if "policy_sha256" not in r or not str(r.get("request_revision", "")).startswith("RETENTION#"):
                continue
            ret += 1
            rev = (r.get("ref") or {}).get("policy_revision")
            revs = {x for x in (rev, r.get("policy_revision")) if isinstance(x, str)}
            h = str(r.get("policy_sha256"))[:16]
            for x in revs:
                if (x, h) in c1:
                    c1[(x, h)] += 1
                if x in EXACT and h not in KNOWN3:
                    other_hash += 1
                if x not in EXACT and ("audit" in x.lower() or "dashbd" in x.lower()) and x != "irpt-anlreq-x10-v1":
                    other_spelling += 1
    for (rev, h), n in c1.items():
        say("C1 %s %s rows=%d" % (rev, h, n))
    say("C2 other_hash=%d other_spelling=%d" % (other_hash, other_spelling))
    say("NOTE retention rows (with a policy_sha256 under a RETENTION# key): %d of %d scanned; revision matched exactly on ref.policy_revision (and a top-level policy_revision when present); other_spelling counts a revision text containing audit or dashbd that is neither of the two exact names" % (ret, scanned))
    say("CENSUS-DONE items_scanned=%d" % scanned)
    (HERE / "A_CENSUS_R34Q.txt").write_text("\n".join(OUT) + "\n", encoding="ascii", errors="replace", newline="\n")


if __name__ == "__main__":
    main()
