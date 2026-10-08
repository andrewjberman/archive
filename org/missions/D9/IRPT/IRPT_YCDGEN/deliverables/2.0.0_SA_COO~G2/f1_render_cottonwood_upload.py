"""Render ONE Cottonwood account's served platinum holdings as an upload file (Ticker,Dollars).

CTO~DELL2 ruling msg 1340 (1). The CSV holds client figures, so it is written OUTSIDE the repo (session scratchpad).
The provenance record (refs, VersionIds, counts; no figures, account named by a sha256 prefix) is printed as JSON.
"""
import csv
import hashlib
import json
import sys

sys.path.insert(0, r"C:/dev/ajb_workspace/infra/aws/lambda/investor-reporting")
sys.path.insert(0, r"C:/dev/ajb_workspace/lib")
import boto3  # noqa: E402
from holdings import publication as P  # noqa: E402

OUT = sys.argv[1]  
ACCOUNT_INDEX = 24
pub = P.HoldingsPublication(boto3.client("s3", region_name="us-east-1"), "cottonwood")
observed = pub.begin()
idx = observed["document"]
date = idx["latest_date"]
row = idx["dates"][date]
part = "date=" + date
man = json.loads(pub.read_exact(row["manifest"], expected_location=pub.location("platinum", part, row["revision"] + ".manifest.json"), max_bytes=P.MAX_JSON_BYTES))
hdr = json.loads(pub.read_exact(man["platinum_header"], expected_location=pub.location("platinum", part, row["revision"] + ".header.json"), max_bytes=P.MAX_JSON_BYTES))
acct = hdr["scope"]["account_ids"][ACCOUNT_INDEX]
doc, manifest, receipt = pub.capture(account_ids=[acct])
rows, skipped = [], []
for n in doc["nodes"]:
    if n.get("node_kind") != "SECURITY":
        continue
    sym = (n.get("display") or {}).get("symbol")
    amt = n.get("amount") or {}
    if not sym or amt.get("units") != "USD" or not isinstance(amt.get("value"), (int, float)) or amt["value"] <= 0:
        skipped.append(n.get("node_id"))
        continue
    rows.append((sym, round(float(amt["value"]), 2)))
with open(OUT, "w", newline="", encoding="ascii") as f:
    w = csv.writer(f)
    w.writerow(["Ticker", "Dollars"])
    w.writerows(rows)
print(json.dumps({
    "source_index": observed["reference"],
    "business_date": date, "revision": row["revision"], "manifest": row["manifest"],
    "header": man["platinum_header"],
    "account": {"index_in_scope": ACCOUNT_INDEX, "scope_size": len(hdr["scope"]["account_ids"]),
                "sha256_prefix": hashlib.sha256(acct.encode()).hexdigest()[:12]},
    "security_nodes": len(rows) + len(skipped), "rows_written": len(rows), "rows_skipped": len(skipped),
    "file": OUT, "file_sha256": hashlib.sha256(open(OUT, "rb").read()).hexdigest(),
}, indent=1))
