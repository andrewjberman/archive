"""AMGT-au-6 PROFILE -- per route, in a FRESH process: one cold call and one warm call, wall ms and boto calls by
operation. `profile_table.py one <idx>` runs one route; `profile_table.py all <label>` runs the nine as subprocesses and
prints a markdown table. PYTHONPATH selects the tree measured (this worktree = AFTER; a `git archive` of the issuance
commit = BEFORE)."""

import collections
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def one(idx):
    import botocore.client

    calls = collections.Counter()
    orig = botocore.client.BaseClient._make_api_call

    def wrap(self, op, params):
        calls[op] += 1
        return orig(self, op, params)

    botocore.client.BaseClient._make_api_call = wrap
    sys.path.insert(0, HERE)
    import capture9
    from lib.research.api import scoped_amgt

    out = {
        "tree": os.path.dirname(os.path.dirname(os.path.dirname(scoped_amgt.__file__)))
    }
    for phase in ("cold", "warm"):
        calls.clear()
        t = time.time()
        status, body = capture9.get(*capture9.READS[idx])
        out[phase] = {
            "ms": round((time.time() - t) * 1000),
            "status": status,
            "calls": dict(calls),
        }
    print(json.dumps(out))


def allroutes(label):
    sys.path.insert(0, HERE)
    import capture9

    print(
        "| route | cold ms | cold calls (Get/List/GetObj/Query) | warm ms | warm calls |"
    )
    print("|---|---|---|---|---|")
    for i, (path, q) in enumerate(capture9.READS):
        r = subprocess.run(
            [sys.executable, __file__, "one", str(i)],
            capture_output=True,
            text=True,
            env=os.environ,
        )
        try:
            d = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            print(
                "| %s | ERROR %s |"
                % (capture9.name(path, q), (r.stderr or "")[-200:].replace("\n", " "))
            )
            continue

        def fmt(c):
            return "%d/%d/%d/%d" % (
                c.get("GetItem", 0),
                c.get("ListObjectsV2", 0),
                c.get("GetObject", 0),
                c.get("Query", 0),
            )

        print(
            "| %s | %d | %s | %d | %s |"
            % (
                capture9.name(path, q).replace(".json", "")
                + " [%s]" % d["cold"]["status"],
                d["cold"]["ms"],
                fmt(d["cold"]["calls"]),
                d["warm"]["ms"],
                fmt(d["warm"]["calls"]),
            )
        )


if __name__ == "__main__":
    if sys.argv[1] == "one":
        one(int(sys.argv[2]))
    else:
        allroutes(sys.argv[2])
