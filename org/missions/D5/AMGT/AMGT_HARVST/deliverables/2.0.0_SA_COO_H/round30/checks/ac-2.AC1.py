"""HVST-ac-2 AC1 (issuer, read-only): the sa probe stayed inside its pair.

PASS requires, reading `~85/ac2_probe.json` and S3:
- the account read ran, and it ran BEFORE any listing request;
- a listing ran only after an authorized 200;
- 0 sign-in and 0 refresh calls;
- every host touched is Seeking Alpha's (or the collector's own proxy);
- the harvest bucket's sa root and run-record root are unchanged against `~85/ac2_before.json`.
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
from lib.research.harvest import store  # noqa: E402

WK = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~85")


def listing(prefix):
    cl = store._default_client()
    out = {}
    for page in cl.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for o in page.get("Contents", []) or []:
            out[o["Key"]] = o["ETag"].strip('"')
    return out


def roots():
    from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER
    sa = store.table_prefix(SOURCE_FOR_PUBLISHER["sa"], "bronze", "x").split("/harvest/", 1)[0] + "/harvest/"
    return {"sa": sa, "run_record": store.table_prefix("amgt", "bronze", "run_record")}


def snapshot():
    return {k: listing(p) for k, p in roots().items()}


def main():
    if "--before" in sys.argv:
        snap = snapshot()
        os.makedirs(WK, exist_ok=True)
        with open(os.path.join(WK, "ac2_before.json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(snap, fh, indent=1, sort_keys=True)
        print("before: %s" % {k: len(v) for k, v in snap.items()})
        print("ACT-START GATE: OK")
        return 0
    failures = []
    with open(os.path.join(WK, "ac2_probe.json"), encoding="utf-8") as fh:
        probe = json.load(fh)
    with open(os.path.join(WK, "ac2_before.json"), encoding="utf-8") as fh:
        before = json.load(fh)
    acct, lst = probe.get("account") or {}, probe.get("listing")
    print("security %s; token_source %s" % ((probe.get("security") or {}).get("sa_symbol"), probe.get("token_source")))
    print("account: status %s class %s authorized %s body_kept %s"
          % (acct.get("status"), acct.get("class"), acct.get("authorized"), acct.get("body_kept")))
    print("listing: %s" % (json.dumps(lst)[:300] if lst else None))
    if acct.get("status") is None:
        failures.append("no account read recorded")
    if lst and not (acct.get("status") == 200 and acct.get("authorized")):
        failures.append("a listing ran without an authorized 200 account read")
    if lst and (lst.get("seq") or 1) <= (acct.get("seq") or 0):
        failures.append("the listing did not follow the account read")
    if probe.get("sign_in_calls") or probe.get("refresh_calls"):
        failures.append("sign-in %s / refresh %s calls" % (probe.get("sign_in_calls"), probe.get("refresh_calls")))
    hosts = probe.get("hosts") or []
    foreign = [h for h in hosts if "seekingalpha.com" not in h and "proxy" not in h.lower()]
    print("hosts: %s" % hosts)
    if foreign:
        failures.append("hosts outside Seeking Alpha: %s" % foreign)
    after = snapshot()
    for k in before:
        if before[k] != after.get(k):
            failures.append("%s root changed (%d -> %d objects)" % (k, len(before[k]), len(after.get(k, {}))))
    print("S3 roots unchanged: %s" % all(before[k] == after.get(k) for k in before))
    print("AC1 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
