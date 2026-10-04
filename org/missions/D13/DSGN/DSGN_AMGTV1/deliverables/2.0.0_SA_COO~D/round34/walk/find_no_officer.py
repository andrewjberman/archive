"""find_no_officer.py -- DSGN_AMGTV1 round 34 (issuer 2.0.0_SA_COO~D): which covered names' served filings list NO officers (FWD-7).

Read-only: the same capture_lib as round 31 (lambda:Invoke of the deployed opal-amgt-scoped-api, GET routes only, no write call).
For every covered name in the served 30-day collected-chatter universe, GET /security/<key>/thesis and count the served management
officers. Prints one line per name with an officer count of 0 or an absent management block, and the denominator.
Usage (repo root): python <this file>
"""
import importlib.util
import json
import os

import boto3

CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
HERE = os.path.dirname(os.path.abspath(__file__))
UNIVERSE = os.path.join(HERE, "..", "..", "round31", "fixtures", "windows.chatter.30.json")


def officers(payload):
    """The served officer list, wherever the thesis bundle carries it: (count, where) or (None, reason)."""
    if not isinstance(payload, dict):
        return None, "payload not an object"
    for path in (("management", "officers"), ("management", "members"), ("exec_management", "officers"), ("officers",)):
        node = payload
        for k in path:
            node = node.get(k) if isinstance(node, dict) else None
        if isinstance(node, list):
            return len(node), "/".join(path)
    mgmt = payload.get("management")
    if isinstance(mgmt, dict):
        return None, "management keys: " + ",".join(sorted(mgmt.keys()))[:120]
    return None, "no management block (top keys: " + ",".join(sorted(payload.keys()))[:160] + ")"


def main():
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    client = boto3.client("lambda", region_name=cl.REGION)
    rows = json.load(open(UNIVERSE, encoding="utf-8"))["payload"]["rows"]
    keys = [(r["security_key"], r.get("ticker")) for r in rows]
    zero, unknown, n = [], [], 0
    for key, ticker in keys:
        obj, meta = cl._invoke(client, cl.ROUTE_PREFIX + "/security/%s/thesis" % key, {})
        n += 1
        payload = obj.get("payload", obj) if isinstance(obj, dict) else obj
        count, where = officers(payload)
        if count == 0:
            zero.append((ticker, key, where))
            print("ZERO", ticker, key, where, flush=True)
        elif count is None:
            unknown.append((ticker, key, where))
            if len(unknown) <= 3:
                print("UNKNOWN-SHAPE", ticker, key, where, flush=True)
    print("names read %d | zero officers %d | shape unknown %d" % (n, len(zero), len(unknown)))


if __name__ == "__main__":
    main()
