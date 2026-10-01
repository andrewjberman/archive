"""Exposure read for row IRPT_BCKEND-W100-S2 (1.0.0_SA_CTO msg 103403).

Scans every CloudFront access-log object of the portal distribution for requests of a
perfrp leaf under /platinum/advi/<firm>/ and prints them by firm, leaf and status.
Read-only. The client address is hashed and never printed.

Usage: python perfrp_exposure_scan.py <dir of *.gz synced from
       s3://opal-data-security/waf-logs/cloudfront-access/> <out.json>
"""
import collections
import glob
import gzip
import hashlib
import json
import os
import sys

LEAF = "perfrp_performance_account.json"
FIRM = "49financial"


def ua_family(ua):
    if "Macintosh" in ua:
        return "Mac"
    if "Windows" in ua:
        return "Windows"
    return "other"


def referer_path(ref):
    if ref.count("/") >= 3:
        return "/" + ref.split("/", 3)[3]
    return ref


def main(log_dir, out_path):
    files = sorted(glob.glob(os.path.join(log_dir, "*.gz")))
    fields = None
    total = 0
    by = collections.Counter()
    rows = []
    for path in files:
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if line.startswith("date time "):
                    fields = line.split()
                    continue
                if not line.strip():
                    continue
                total += 1
                rec = dict(zip(fields, line.rstrip("\n").split("\t")))
                uri = rec.get("cs-uri-stem", "")
                if "/platinum/advi/" not in uri or "perfrp" not in uri:
                    continue
                firm = uri.split("/platinum/advi/")[1].split("/")[0]
                leaf = uri.rsplit("/", 1)[-1]
                by[(firm, leaf, rec["sc-status"])] += 1
                if firm == FIRM and leaf == LEAF:
                    rows.append({
                        "ts_utc": rec["date"] + "T" + rec["time"] + "Z",
                        "status": rec["sc-status"],
                        "sc_bytes": int(rec["sc-bytes"]),
                        "content_type": rec.get("sc-content-type"),
                        "edge_result": rec.get("x-edge-result-type"),
                        "host": rec.get("x-host-header"),
                        "referer_path": referer_path(rec.get("cs(Referer)", "-")),
                        "client": hashlib.sha256(rec["c-ip"].encode()).hexdigest()[:8],
                        "ua_family": ua_family(rec.get("cs(User-Agent)", "")),
                    })
    print("DENOMINATOR: files", len(files), "| request lines", total)
    for key, count in sorted(by.items()):
        print("  ", count, key)
    clients = {row["client"] for row in rows}
    print("49F", LEAF, "rows:", len(rows), "| distinct clients (hashed):", len(clients))
    for row in rows:
        print("  ", json.dumps(row))
    result = {
        "files": len(files),
        "request_lines": total,
        "by_firm_leaf_status": [[*key, count] for key, count in sorted(by.items())],
        "rows_49f_performance_account": rows,
    }
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(result, out, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
