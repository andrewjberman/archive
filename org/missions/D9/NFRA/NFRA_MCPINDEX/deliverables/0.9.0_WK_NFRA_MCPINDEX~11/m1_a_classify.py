# MX-m-1 (a): SSM Status vs the outcome the run's own uploaded log records. Log-records-failure predicate (any of):
#   a line beginning "ERROR:" containing "fail"; "Download exit code: N" or "Merge exit code: N" with N nonzero; a line "FAILED".
import json
import re
import collections
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else ".scratch/a"
PATS = [r"^ERROR:.*fail", r"(Download|Merge) exit code: [1-9]", r"^FAILED\s*$"]


def logfail(t):
    return any(
        re.search(p, t, re.M | re.I if p.startswith("^ERROR") else re.M) for p in PATS
    )


rows = json.load(open("%s/runs.json" % OUT))
tab = collections.defaultdict(collections.Counter)
span = {}
for r in rows:
    inv = json.load(open("%s/inv/%s.json" % (OUT, r["cmd"]), encoding="utf-8"))[
        "CommandInvocations"
    ]
    r["rc"] = inv[0]["CommandPlugins"][0]["ResponseCode"] if inv else None
    if r["vid"]:
        t = open(
            "%s/logs/%s.log" % (OUT, r["cmd"]), encoding="utf-8", errors="replace"
        ).read()
        r["logfail"] = logfail(t)
    else:
        r["logfail"] = None
    d = r["doc"]
    ver = ""
    if d == "opal-bd-asset-dim-download":
        ver = (
            "v1"
            if r["t"] < "2026-09-26T23:20"
            else ("v2" if r["t"] < "2026-09-27T01:31" else "v3")
        )
    tab[(d, ver)][
        (
            r["status"],
            "log=FAIL"
            if r["logfail"]
            else ("log=ok" if r["logfail"] is False else "log=NONE"),
        )
    ] += 1
    span.setdefault((d, ver), []).append(r["t"][:10])
for k in sorted(tab):
    c = tab[k]
    n = sum(c.values())
    mism = sum(v for (s, lg), v in c.items() if s == "Success" and lg == "log=FAIL")
    rev = sum(v for (s, lg), v in c.items() if s != "Success" and lg != "log=FAIL")
    print(
        "%-32s %-3s N=%2d %s..%s  SSM-Success+log-FAIL=%2d  SSM-notSuccess+log-not-FAIL=%d  %s"
        % (k[0], k[1], n, min(span[k]), max(span[k]), mism, rev, dict(c))
    )
json.dump(rows, open("%s/runs_classified.json" % OUT, "w"), indent=1)
