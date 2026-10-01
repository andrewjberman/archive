"""Where did Cottonwood's key-path shape grow, and does it grow between old-code days too? Read-only."""
import json

import boto3

B = "opal-data-assets"
s3 = boto3.client("s3")


def shape(o, path="", out=None):
    out = set() if out is None else out
    if isinstance(o, dict):
        for k, v in o.items():
            shape(v, path + "/" + str(k), out)
    elif isinstance(o, list):
        for v in o:
            shape(v, path + "[]", out)
    else:
        out.add(path)
    return out


def load(date):
    return json.loads(s3.get_object(Bucket=B, Key="portal/gold/mdpf/cottonwood/aggregate-aua-timeseries/%s.json" % date)["Body"].read())


dates = ["2026-09-22", "2026-09-25", "2026-09-28", "2026-09-29", "2026-09-30"]
shapes = {d: shape(load(d)) for d in dates}
for a, b in zip(dates, dates[1:]):
    added, removed = shapes[b] - shapes[a], shapes[a] - shapes[b]
    roots = sorted({"/".join(p.split("/")[:4]) for p in added})
    outside = [p for p in added if not p.startswith("/meta/custom_residual_detail/by_date/")]
    print("%s -> %s: paths %d -> %d | added %d removed %d | added outside /meta/custom_residual_detail/by_date/: %d %s | added roots %s"
          % (a, b, len(shapes[a]), len(shapes[b]), len(added), len(removed), len(outside), outside[:4], roots[:3]))
last = shapes[dates[-1]]
taxy = sorted(p for p in last if "tax" in p.lower())
print("newest doc: paths naming tax: %d; of them outside custom_residual_detail: %d %s" % (
    len(taxy), len([p for p in taxy if "custom_residual_detail" not in p]), [p for p in taxy if "custom_residual_detail" not in p][:4]))
print("  sample:", taxy[:2])
