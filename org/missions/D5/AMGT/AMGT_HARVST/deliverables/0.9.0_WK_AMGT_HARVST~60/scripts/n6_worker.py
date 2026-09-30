"""HVST-n-6 fresh-process worker: python n6_worker.py <old|new> <security_key> <YYYY-MM-DD> <reps>
Prints one line `N6JSON {...}` with the per-rep records and the served body text."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import n6_common  # noqa: E402

if __name__ == "__main__":
    path_name, key, day, reps = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    recs, text = n6_common.run_worker(path_name, key, day, reps)
    print("N6JSON " + json.dumps({"reps": recs, "body": text}))
