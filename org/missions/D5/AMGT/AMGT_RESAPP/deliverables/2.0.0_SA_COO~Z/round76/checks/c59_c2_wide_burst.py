"""AMGT_RESAPP round 76 -- the issuer's real run of r75 c59 C2 with a burst wide enough to exceed the warm pool.

Row AMGT_RESAPP-Z-S361: a burst of 6 cannot force a cold container once the route answers in 200-800 ms. This fires
--width concurrent /freshness invokes at the deployed function and reads each REPORT line: a cold invoke carries
Init Duration. Read-only on the product (GET-shaped direct invokes).

  python c59_c2_wide_burst.py [--width 40] [--bar 2000]
Prints: invokes, distinct outcomes, the cold list (status, init + duration ms), and C2 YES / NO / UNMEASURED.
"""
import argparse
import base64
import concurrent.futures
import importlib.util
import json
import os
import re
import sys

import boto3
from botocore.config import Config

HERE = os.path.dirname(os.path.abspath(__file__))
R75 = os.path.join(HERE, "..", "..", "round75", "checks", "r75_served.py")
spec = importlib.util.spec_from_file_location("r75_served", R75)
r75 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r75)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, default=40)
    ap.add_argument("--bar", type=float, default=2000.0)
    a = ap.parse_args()
    lam = boto3.client("lambda", region_name=os.environ.get("AWS_REGION", "us-east-1"),
                       config=Config(max_pool_connections=a.width + 4, read_timeout=120))

    def one(_):
        r = lam.invoke(FunctionName=r75.FN, Payload=json.dumps(r75._event(f"{r75.PREFIX}/freshness")).encode(),
                       LogType="Tail")
        body = json.loads(r["Payload"].read() or b"{}")
        log = base64.b64decode(r.get("LogResult") or b"").decode("utf-8", "replace")
        rep = next((ln for ln in log.split("\n") if ln.startswith("REPORT")), "")
        init = re.search(r"Init Duration: ([\d.]+) ms", rep)
        dur = re.search(r"\tDuration: ([\d.]+) ms", rep)
        return body.get("statusCode"), float(init.group(1)) if init else None, float(dur.group(1)) if dur else None

    with concurrent.futures.ThreadPoolExecutor(a.width) as ex:
        res = list(ex.map(one, range(a.width)))
    codes = sorted({str(c) for c, _, _ in res})
    cold = [(c, round(i + d)) for c, i, d in res if i is not None and d is not None]
    warm = sorted(round(d) for c, i, d in res if i is None and d is not None)
    print(f"burst of {a.width}: invokes {len(res)}; status codes {codes}; cold invokes {len(cold)}; warm {len(warm)}")
    print(f"cold (status, init + duration ms): {sorted(cold, key=lambda x: x[1])}")
    if warm:
        print(f"warm duration ms: min {warm[0]} max {warm[-1]}")
    if not cold:
        print("R76 C59-C2 WIDE: UNMEASURED (no cold invoke observed)")
        return 2
    ok = all(c == 200 and t <= a.bar for c, t in cold)
    over = [x for x in cold if x[1] > a.bar or x[0] != 200]
    print(f"bar {a.bar:.0f} ms: {len(cold) - len(over)} of {len(cold)} cold invokes within the bar; over {over}")
    print("R76 C59-C2 WIDE: " + ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
