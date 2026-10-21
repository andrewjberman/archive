"""IRPT_ANLREQ TO-READ-RETENTION-CENSUS (applier 0.7.0_AE_CloudOps~IB2): READ ONLY.

  python census.py     scans the PROD request index (table irpt-requests) once, paginated to the end, and prints COUNTS only.

Nothing is written. No row body, key, id or policy document is printed. A retention row is `synthetic yes` only when its serialized form holds an id that a run
receipt of runs 7, 7b, 7c, 7d or 7e recorded (a request id, an artifact id, a portfolio id, an upload id) or a synthetic address of those runs; every other row is
`synthetic no` (so `no` means "not linkable to a run receipt", which is how the order defines it). Andrew's ticket rows are found by the ticket id inside the
request index rows themselves; his ticket row is not read.
"""
from __future__ import annotations

import datetime
import json
import re
import collections
from pathlib import Path

import boto3
from boto3.dynamodb.types import TypeDeserializer

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent
TABLE = "irpt-requests"
EPOCH = int(datetime.datetime(2026, 10, 20, 23, 12, 44, tzinfo=datetime.timezone.utc).timestamp())
REVS = {"irpt-anlreq-x10-v1": {"8edbe84b05765c36": "OLD", "cfed04bb8c2f1982": "NEW"},
        "irpt-dashbd-x10-v1": {"301c58e24ff0feda": "OLD", "244a20425ba40cde": "NEW"}}
ANDREW_TICKET = "TCK-20261020-b1d61f80"
ID_RE = re.compile(r"(REQ-[0-9a-f]{24}|ART-[0-9a-f]{64}|UP-[0-9a-f]{64}|portfolio_[0-9a-f]{64}|fwd1-[a-z0-9-]+@opal\.invalid)")
OUT = []


def say(line):
    OUT.append(line)
    print(line)


def synthetic_tokens():
    toks = set()
    for d in sorted(DELIV.glob("irpt_anlreq_commentary_e2e7*")):
        for f in d.iterdir():
            if f.is_file() and f.suffix in (".txt", ".json", ".log"):
                toks.update(ID_RE.findall(f.read_text(encoding="utf-8", errors="replace")))
    return toks


def main():
    des = TypeDeserializer()
    ddb = boto3.client("dynamodb", region_name="us-east-1")
    say("R0 date=%s table=%s r34o_epoch=%d (%s)" % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), TABLE, EPOCH, "2026-10-20T23:12:44Z"))
    syn = synthetic_tokens()
    scanned, rows, ret = 0, [], 0
    for pg in ddb.get_paginator("scan").paginate(TableName=TABLE):
        scanned += pg["ScannedCount"]
        for it in pg["Items"]:
            row = {k: des.deserialize(v) for k, v in it.items()}
            rows.append(row)
    # Andrew's request: the ids that sit in index rows naming his ticket
    andrew = set()
    for r in rows:
        s = json.dumps(r, default=str)
        if ANDREW_TICKET in s:
            andrew.update(ID_RE.findall(s))
    andrew = {a for a in andrew if not a.startswith("fwd1-")}
    c1 = collections.Counter()
    c2 = collections.Counter()
    c3 = collections.Counter()
    other_since = 0
    old_since = collections.Counter()
    andrew_rows = False
    for r in rows:
        if not isinstance(r, dict) or "policy_sha256" not in r or not str(r.get("request_revision", "")).startswith("RETENTION#"):
            continue
        ret += 1
        rev = (r.get("ref") or {}).get("policy_revision")
        h = str(r.get("policy_sha256"))[:16]
        created = int(r.get("created_at", 0))
        since = created >= EPOCH
        if rev in REVS and h in REVS[rev]:
            c1[(rev, h, "since" if since else "before")] += 1
        elif rev in REVS and since:
            other_since += 1
        firm = (r.get("owner") or {}).get("firm_id", "?")
        s = json.dumps(r, default=str)
        ids = set(ID_RE.findall(s))
        if rev in REVS and since and REVS[rev].get(h) == "OLD":
            old_since[(rev, firm, "yes" if ids & syn else "no")] += 1
        if rev in REVS and since and REVS[rev].get(h) == "NEW":
            c2[(firm, "yes" if ids & syn else "no")] += 1
        if rev in REVS and not since and REVS[rev].get(h) == "OLD":
            c3[firm] += 1
            if andrew and (ids & andrew):
                andrew_rows = True
    for rev, hs in REVS.items():
        for h in hs:
            say("C1 %s %s before=%d since=%d" % (rev, h, c1[(rev, h, "before")], c1[(rev, h, "since")]))
    for (firm, synth), n in sorted(c2.items()):
        say("C2 %s synthetic=%s new_hash=%d" % (firm, synth, n))
    say("C2 other_hash=%d" % other_since)
    for firm, n in sorted(c3.items()):
        say("C3 %s old_hash_before=%d" % (firm, n))
    say("C3 andrew_ticket_rows=%s" % ("yes" if andrew_rows else "no"))
    for (rev, firm, synth), n in sorted(old_since.items()):
        say("NOTE since_epoch_old_hash %s %s synthetic=%s n=%d" % (rev, firm, synth, n))
    if not c2:
        say("NOTE C2 no row at or after the epoch carries a NEW hash (zero groups)")
    say("CENSUS-DONE items_scanned=%d" % scanned)
    say("NOTE retention rows with a policy_sha256: %d of %d scanned; synthetic tokens read from run receipts: %d; ids found in index rows naming Andrew's ticket: %d" % (ret, scanned, len(syn), len(andrew)))
    (HERE / "A_CENSUS.txt").write_text("\n".join(OUT) + "\n", encoding="ascii", errors="replace", newline="\n")


if __name__ == "__main__":
    main()
