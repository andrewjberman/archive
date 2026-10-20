#!/usr/bin/env python
"""OG-rl-17 Phase B load proof: the PUBLIC /health sampler, once a second until the stop file exists. READ ONLY: one unauthenticated GET per second. One JSON line per sample: UTC time to the millisecond, the HTTP status (or the error class)
and the round trip in milliseconds. No address is written.
usage: python rl17_health.py <out.jsonl> <stopfile>"""
from __future__ import annotations

import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.request

OUT, STOP = sys.argv[1:3]
URL = "https://mcp.opalinvest.dev/health"


def probe():
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(URL, timeout=10) as resp:
            code = resp.status
    except urllib.error.HTTPError as exc:
        code = exc.code
    except Exception as exc:  # noqa: BLE001
        code = type(exc).__name__
    return code, round((time.monotonic() - t0) * 1000)


def main():
    n = 0
    with open(OUT, "a", encoding="utf-8", newline="\n") as fh:
        while not os.path.exists(STOP):
            t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            code, ms = probe()
            fh.write(json.dumps({"t": t, "code": code, "ms": ms}) + "\n")
            fh.flush()
            n += 1
            time.sleep(max(0.0, 1.0 - ms / 1000.0))
    print("health sampler stopped after %d samples" % n)


if __name__ == "__main__":
    main()
