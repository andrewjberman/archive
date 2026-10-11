import collections
import json
import boto3
from lib.research.api import scoped_amgt
from lib.research.peers import numeric_tickers as nt

s3 = boto3.client("s3", region_name="us-east-1")
rows = {}
for u in ["sp500", "r1000", "r1000v", "acwx", "eafe", "eafev"]:
    d = json.loads(s3.get_object(Bucket="opal-data-portal-v2",
                                 Key="json/security_scanner/latest/universes/%s/universe_data.json" % u)["Body"].read())
    for s in d["securities"]:
        rows.setdefault(str(s["ticker"]), s)
non = [s for t, s in rows.items() if not (t.isascii() and t.isalpha() and s.get("country") == "United States")]
index = scoped_amgt._held_name_index()
print("held name index: tokens", len(index), "keys", len({k for v in index.values() for k in v}))
numeric = [s for s in non if nt.is_numeric_ticker({"ticker": str(s["ticker"])})]
other = [s for s in non if s not in numeric]
print("non-US rows", len(non), "| all-digit tickers", len(numeric), "| other forms", len(other))
res = collections.Counter()
served = []
for s in numeric:
    out = nt.numeric_fields({"ticker": str(s["ticker"]), "name": s.get("name")}, scoped_amgt._resolve_held_form,
                            index, scoped_amgt._clean_display_name)
    if "security_key" in out:
        res[out["identity"]["matched_as"]] += 1
        served.append((s["ticker"], s.get("name"), out["security_key"], out["identity"]["matched_as"]))
    else:
        res["reason"] += 1
print("numeric rows by outcome:", dict(res))
print("sample served:", served[:6])
# the OTHER non-US rows: would a unique name token match? (potential only: no code path serves it)
pot = 0
ex = []
for s in other:
    tok = nt.name_token(scoped_amgt._clean_display_name(s.get("name")))
    keys = sorted(set(index.get(tok) or [])) if tok else []
    if len(keys) == 1:
        pot += 1
        ex.append((s["ticker"], s.get("name"), keys[0]))
print("OTHER non-US rows whose name token matches exactly one held company (not served today):", pot, "of", len(other))
print("examples:", ex[:8])
