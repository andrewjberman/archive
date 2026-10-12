"""AMGT_RESAPP round-100 PREP -- the structural check of the cold request: one S3 client per container, not one per call.

  PYTHONPATH=<repo root> python r100_cold_check.py [--subject ASML_NA_Equity]

Runs `r100_cold_request.py` once in a FRESH process (the checkout's own handler on the live pool, GET-shaped, read-only) and grades the JSON it prints:
    C1 the cold and the warm request both served status 200.
    C2 the cold request built at most 12 S3 clients (the base builds 146: one per `_s3_client()` call).
    C3 the cold request made between 150 and 400 S3 requests (the base makes about 242: the same work is done, none skipped).
    C4 the warm request took no longer than the cold one.
Prints the numbers and `R100 COLD REQUEST: YES|NO` (exit 0|1). At the base: C2 FAIL (146 clients), C1, C3, C4 PASS. Timing is printed, never graded (it varies with the network).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def main(argv):
    subject = argv[argv.index("--subject") + 1] if "--subject" in argv else "ASML_NA_Equity"
    r = subprocess.run([sys.executable, os.path.join(HERE, "r100_cold_request.py"), "--subject", subject], capture_output=True, text=True, timeout=600)
    line = [ln for ln in r.stdout.splitlines() if ln.startswith("{")]
    if r.returncode != 0 or not line:
        say(False, "C0 the instrument ran", "rc %s, stderr %s" % (r.returncode, r.stderr[-200:].replace("\n", " ")))
        print("R100 COLD REQUEST: NO")
        return 1
    d = json.loads(line[-1])
    cold, warm = d["cold"], d["warm"]
    print("   %s %s: cold %.2f s, %d clients, %d requests, peak %d on one client; warm %.2f s, %d clients"
          % (d["route"], d["subject"], cold["elapsed_s"], cold["clients"], cold["requests"], cold["peak_one_client"], warm["elapsed_s"], warm["clients"]))
    res = [say(cold["status"] == 200 and warm["status"] == 200, "C1 cold and warm both served 200", "%s, %s" % (cold["status"], warm["status"])),
           say(cold["clients"] <= 12, "C2 the cold request built at most 12 S3 clients", "%d" % cold["clients"]),
           say(150 <= cold["requests"] <= 400, "C3 the same work: 150 to 400 S3 requests", "%d" % cold["requests"]),
           say(warm["elapsed_s"] <= cold["elapsed_s"], "C4 warm no slower than cold", "%.2f vs %.2f s" % (warm["elapsed_s"], cold["elapsed_s"]))]
    print("   arms passed %d of %d" % (sum(1 for x in res if x), len(res)))
    ok = all(res)
    print("R100 COLD REQUEST: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
