# MX-m-1 (a): pin, for each command, the S3 log VERSION its run uploaded last (LastModified in [start-2m, start+3h]).
import json
import datetime as dt
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else ".scratch/a"
docs = {
    "opal-bd-allocation-download": "allocation",
    "opal-bd-asset-dim-download": "asset-dim",
    "opal-bd-fees-download": "fees",
    "opal-bd-realized-download": "realized",
    "opal-bd-transaction-download": "transaction",
    "opal-bd-unrealized-download": "unrealized",
}
P = dt.datetime.fromisoformat
rows = []
for d, p in docs.items():
    vers = json.load(open("%s/ver_%s.json" % (OUT, p), encoding="utf-8")).get(
        "Versions", []
    )
    for x in vers:
        x["lm"] = P(x["LastModified"])
    for c in json.load(open("%s/cmds_%s.json" % (OUT, d), encoding="utf-8"))[
        "Commands"
    ]:
        t = P(c["RequestedDateTime"])
        c2 = sorted(
            [
                x
                for x in vers
                if t - dt.timedelta(minutes=2) <= x["lm"] <= t + dt.timedelta(hours=3)
            ],
            key=lambda x: x["lm"],
        )
        pin = c2[-1] if c2 else None
        rows.append(
            dict(
                doc=d,
                cmd=c["CommandId"],
                t=t.astimezone(dt.timezone.utc).isoformat(),
                status=c["Status"],
                nver=len(c2),
                key=pin["Key"] if pin else None,
                vid=pin["VersionId"] if pin else None,
            )
        )
json.dump(rows, open("%s/runs.json" % OUT, "w"), indent=1)
for r in rows:
    if r["vid"]:
        print(r["cmd"], r["key"], r["vid"])
