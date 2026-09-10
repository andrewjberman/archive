#!/usr/bin/env python3
"""NFRA_OPSEC202609 TO-OP4-S-1 (OP4-s-1, FWD-4): ONE staged burst, round 2's exact shape.

Fires ~240 POSTs at https://opalinvest.dev/auth/login, 8 concurrent threads, 10s per-request
timeout, fixture identity opsec-s6-probe-fixture2@opal.invalid / "not-a-credential" (invalid by
construction -- there is no real credential anywhere in this script or its output). Counts status
codes into a histogram and prints T0 (immediately before the first request is dispatched) and T1
(immediately after the last response, or the last per-request timeout, is collected).

stdlib only (urllib.request + threading + queue). Never prints or stores any credential; the fixture
body is echoed above in this docstring because it IS the fixture, not a secret.
"""
import json
import queue
import threading
import time
import urllib.error
import urllib.request

URL = "https://opalinvest.dev/auth/login"
HEADERS = {"Content-Type": "application/json", "User-Agent": "opal-s6-probe"}
BODY = json.dumps(
    {"email": "opsec-s6-probe-fixture2@opal.invalid", "password": "not-a-credential"}
).encode("utf-8")
N_REQUESTS = 240
N_THREADS = 8
TIMEOUT_S = 10

results = queue.Queue()


def _one_request(i):
    req = urllib.request.Request(URL, data=BODY, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            results.put(("code", resp.status))
    except urllib.error.HTTPError as e:
        # HTTPError IS the response for a non-2xx status; the code is what we want to count.
        results.put(("code", e.code))
    except urllib.error.URLError as e:
        results.put(("error", f"URLError: {e.reason}"))
    except Exception as e:  # noqa: BLE001 -- this is a status-code counting harness, not app code
        results.put(("error", f"{type(e).__name__}: {e}"))


def _worker(q):
    while True:
        try:
            i = q.get_nowait()
        except queue.Empty:
            return
        _one_request(i)
        q.task_done()


def main():
    work_q = queue.Queue()
    for i in range(N_REQUESTS):
        work_q.put(i)

    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print(f"T0={t0}")

    threads = [threading.Thread(target=_worker, args=(work_q,), daemon=True) for _ in range(N_THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    t1 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print(f"T1={t1}")

    histogram = {}
    errors = []
    total = 0
    while not results.empty():
        kind, val = results.get()
        total += 1
        if kind == "code":
            histogram[val] = histogram.get(val, 0) + 1
        else:
            errors.append(val)

    print(f"TOTAL_RESPONSES_COUNTED={total} (of {N_REQUESTS} dispatched)")
    print("STATUS_CODE_HISTOGRAM:")
    for code in sorted(histogram):
        print(f"  {code}: {histogram[code]}")
    if errors:
        print(f"NON-HTTP ERRORS ({len(errors)}):")
        for e in errors[:20]:
            print(f"  {e}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")


if __name__ == "__main__":
    main()
