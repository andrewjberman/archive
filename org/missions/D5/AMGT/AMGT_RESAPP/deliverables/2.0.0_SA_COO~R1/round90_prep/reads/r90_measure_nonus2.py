import json
import collections
import boto3
from lib.research.identity import crosswalk
s3 = boto3.client("s3", region_name="us-east-1")
rows = {}
for u in ["sp500","r1000","r1000v","acwx","eafe","eafev"]:
    d = json.loads(s3.get_object(Bucket="opal-data-portal-v2", Key="json/security_scanner/latest/universes/%s/universe_data.json"%u)["Body"].read())
    for s in d["securities"]:
        rows.setdefault(str(s["ticker"]), s)
doc, index, amb = crosswalk.load_crosswalk()
recs = doc["records"]
def exch(r):
    b = r.get("bloomberg") or ""
    p = b.split()
    return p[-1] if len(p) > 1 else ""
c = collections.Counter(exch(r) for r in recs)
print("pool records by exchange code:", dict(c.most_common(15)))
nonus = [r for r in recs if exch(r) != "US"]
print("pool non-US records:", len(nonus), "of", len(recs))
hits = []
for r in nonus:
    b = r["bloomberg"].split()
    root = b[0]
    sec = rows.get(root)
    hits.append((r["bloomberg"], bool(sec), (sec or {}).get("country")))
print("pool non-US records whose root appears as a scanner ticker:", sum(1 for h in hits if h[1]), "of", len(nonus))
print("samples", [h for h in hits if h[1]][:10])
# upper bound for the 1,816 non-US scanner rows: scanner rows (non-US-alpha) whose ticker equals a pool non-US root
roots = {r["bloomberg"].split()[0] for r in nonus}
non_rows = [s for t, s in rows.items() if not (t.isascii() and t.isalpha() and s.get("country") == "United States")]
print("non-US scanner rows with ticker == a pool non-US root:", sum(1 for s in non_rows if str(s["ticker"]) in roots), "of", len(non_rows))
# US-listed foreign names (ADRs) alphabetic ticker but country != United States
adr = [s for t, s in rows.items() if t.isascii() and t.isalpha() and s.get("country") != "United States"]
print("alphabetic tickers with country != United States:", len(adr))
print("of which resolve under '<T> US':", sum(1 for s in adr if crosswalk.resolve(str(s['ticker'])+" US").get('security_key')))
