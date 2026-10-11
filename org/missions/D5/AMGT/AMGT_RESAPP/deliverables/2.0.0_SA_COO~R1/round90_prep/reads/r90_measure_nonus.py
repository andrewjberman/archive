"""Round-90 measurement: how many non-US scanner rows does the identity pool resolve, by what form. Read-only."""
import json
import collections
import sys
import boto3
from lib.research.identity import crosswalk

BUCKET = "opal-data-portal-v2"
UNIS = ["sp500", "r1000", "r1000v", "acwx", "eafe", "eafev"]
s3 = boto3.client("s3", region_name="us-east-1")
rows = {}
asof = {}
for u in UNIS:
    key = "json/security_scanner/latest/universes/%s/universe_data.json" % u
    doc = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())
    asof[u] = doc.get("asOf")
    for sec in doc["securities"]:
        t = sec.get("ticker")
        rows.setdefault(t, sec)
print("asOf", asof)
print("distinct tickers", len(rows))

def is_us_alpha(sec):
    t = sec.get("ticker")
    return isinstance(t, str) and t.isascii() and t.isalpha() and sec.get("country") == "United States"

us = [s for s in rows.values() if is_us_alpha(s)]
non = [s for s in rows.values() if not is_us_alpha(s)]
print("US alphabetic", len(us), "| non-US-or-other", len(non))

doc, index, amb = crosswalk.load_crosswalk()
print("crosswalk records", len(doc["records"]), "index forms", len(index), "ambiguous", len(amb))
meas = [r for r in doc["records"] if r["resolution"] == crosswalk.RESOLUTION_MEASURED]
print("records MEASURED", len(meas))
print("sample record keys", sorted(meas[0].keys()))
print("sample", {k: meas[0][k] for k in ("security_key", "bloomberg", "display_ticker", "model_key") if k in meas[0]})

def hit(form):
    h = crosswalk.resolve(form)
    return h if h.get("resolution") == crosswalk.RESOLUTION_MEASURED and h.get("security_key") else None

by_form = collections.Counter()
resolved = {}
for s in non:
    t = str(s["ticker"])
    h = hit(t)
    how = "raw_ticker"
    if not h:
        # the country's own exchange suffix is a FORM; counted separately, never used to resolve
        h = None
        how = None
    if h:
        resolved[t] = (how, h["security_key"])
        by_form[how] += 1
print("non-US rows resolved by the RAW scanner ticker:", len(resolved), "of", len(non))
print("sample resolved", list(resolved.items())[:8])
cc = collections.Counter(str(s.get("country")) for s in non)
print("non-US by country (top 12)", cc.most_common(12))
# how many US-alpha rows resolve under '<T> US'
us_ok = sum(1 for s in us if hit(s["ticker"] + " US"))
print("US alphabetic resolving under '<T> US':", us_ok, "of", len(us))
# does any resolved non-US key have a model block / CRNCY? count pool keys
json.dump({"asof": asof, "n_rows": len(rows), "n_us": len(us), "n_non": len(non), "resolved_raw": resolved,
           "us_ok": us_ok}, open(sys.argv[1], "w"))
