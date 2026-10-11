"""IRPT_YCDGEN served-read window 6: the read-only owner reads after the irpt-status rev 6 apply (TO-APPLY-Y1 AMENDMENT 8).

    python w6_reads.py R3 <out.json>                 # one owner GET of the history, svc on its native firm (cottonwood)
    python w6_reads.py R45 <request_id> <out.json>   # status-job + analysis-report sections + ONE GET .../original (49financial)
    python w6_reads.py R6 <request_id> <out.json>    # ONE status-job read with the portal's date opt-in header (49financial)
    python w6_reads.py CENSUS <request_id> <out.json> # ONE sections read; writes only counts by page, status, method and masked reason

Reuses f1_svc_run.py's call() and scrub(): the password is read by NAME into memory and never printed or written; the record
keeps codes, ids and section names only. Submits nothing. ASCII only.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "f1_svc_release"))

import boto3  # noqa: E402
import f1_svc_run as f1  # noqa: E402


def login():
    password = boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(SecretId=f1.SECRET)["SecretString"]
    s, resp = f1.call("POST", "/auth/login", {"email": f1.EMAIL, "password": password}, {"Content-Type": "application/json"},
                      record_body={"email": "<svc>", "password": "<redacted>"})
    del password
    token = resp.get("accessToken") if isinstance(resp, dict) else None
    f1.say("login", s, "token present", bool(token))
    if not token:
        return None
    return {"Content-Type": "application/json", "Authorization": "Bearer " + token, "X-Contract-Version": "v1"}


def codes(resp):
    st = resp.get("status") if isinstance(resp, dict) else None
    st = st if isinstance(st, dict) else {}
    op = st.get("operation") if isinstance(st.get("operation"), dict) else {}
    return {"ok": resp.get("ok") if isinstance(resp, dict) else None, "operation_id": op.get("operation_id"),
            "state": st.get("state"), "public_reason_code": st.get("public_reason_code")}


def main(argv):
    mode = argv[1]
    out = argv[-1]
    result = {"mode": mode, "started_at": f1.stamp(), "api": f1.API}
    h = login()
    summary = []
    if h:
        if mode == "R3":
            q = "?selected_tenant=cottonwood"
            s, r = f1.call("GET", f1.BASE + "/analysis/requests" + q, None, h)
            summary.append(dict(read="R3 history", http=s, **codes(r)))
        elif mode == "R45":
            rid = argv[2]
            q = "?selected_tenant=49financial"
            result["request"] = rid
            for name, path in (("R4 status-job", "/status/" + rid + q),
                               ("R4 analysis-report sections", "/analysis/" + rid + "/sections" + q),
                               ("R5 original", "/analysis/requests/" + rid + "/original" + q)):
                s, r = f1.call("GET", f1.BASE + path, None, h)
                summary.append(dict(read=name, http=s, **codes(r)))
        elif mode == "R6":
            # CTO~DELL2 msg 4152: ONE status-job re-read WITH the portal's date opt-in (portal
            # contracts/prospect-dates.ts PROSPECT_DATE_HEADER; ops/entry.py job_status reads it).
            rid = argv[2]
            hh = dict(h)
            hh["X-IRPT-Status-Dates"] = "prospect-v1"
            s, r = f1.call("GET", f1.BASE + "/status/" + rid + "?selected_tenant=49financial", None, hh)
            d = r.get("data") if isinstance(r, dict) and isinstance(r.get("data"), dict) else {}
            summary.append(dict(read="R6 status-job with X-IRPT-Status-Dates", http=s, state=d.get("state"),
                                public_reason_code=d.get("public_reason_code"),
                                source_date_keys=sorted((d.get("source_dates") or {}).keys())))
        elif mode == "CENSUS":
            # Round 8 cell YCD-c-8: ONE read of the report's sections; only an aggregate is written. The raw answer is
            # read with a plain opener so `page` and `reason` are seen before any scrub; no value is kept and every digit
            # in a reason is masked, so the record carries counts and reason shapes, never a figure.
            import collections
            import re
            import urllib.request
            rid = argv[2]
            req = urllib.request.Request(f1.API + f1.BASE + "/analysis/" + rid + "/sections?selected_tenant=49financial",
                                         headers=h, method="GET")
            with urllib.request.urlopen(req, timeout=60) as resp:
                status, raw = resp.status, json.loads(resp.read().decode("utf-8"))
            data = raw.get("data") if isinstance(raw, dict) and isinstance(raw.get("data"), dict) else {}
            rows = data.get("sections") if isinstance(data.get("sections"), list) else []
            tally = collections.Counter()
            for row in rows:
                reason = row.get("reason")
                reason = re.sub(r"[0-9]", "#", reason) if isinstance(reason, str) else None
                page = row.get("page") if isinstance(row.get("page"), int) else None
                tally[(page, row.get("status"), row.get("method") if row.get("status") != "VALUE" else "(a value)",
                       row.get("section_type"), reason)] += 1
            census = [{"page": k[0], "status": k[1], "method": k[2], "section_type": k[3], "reason": k[4], "sections": n}
                      for k, n in sorted(tally.items(), key=lambda kv: (kv[0][0] or 0, str(kv[0][1]), str(kv[0][2]),
                                                                        str(kv[0][3]), str(kv[0][4])))]
            result.update(request=rid, provider=data.get("provider"), sections_total=len(rows), census=census,
                          computation_validation_status=(data.get("computation_validation") or {}).get("status"))
            summary.append(dict(read="CENSUS sections", http=status, sections_total=len(rows), groups=len(census)))
        elif mode == "INTERSECT":
            # Round 8 cell YCD-e-8: ONE read of the request's ORIGINAL upload (Ticker,Dollars). The tickers are compared, in
            # memory, with the key set of a held-characteristics parquet given on the command line. Only COUNTS are written:
            # no ticker, no amount, no file byte. argv: INTERSECT <request_id> <characteristics.parquet> <out.json>
            import csv
            import io
            import urllib.request
            import pyarrow.parquet as pq
            rid, parquet_path = argv[2], argv[3]
            req = urllib.request.Request(f1.API + f1.BASE + "/analysis/requests/" + rid + "/original?selected_tenant=49financial",
                                         headers=h, method="GET")
            with urllib.request.urlopen(req, timeout=60) as resp:
                status, answer = resp.status, json.loads(resp.read().decode("utf-8"))
            route = ((answer.get("data") or {}).get("download_route") or {}) if isinstance(answer, dict) else {}
            url = route["url"]
            own = url.startswith("/") or url.startswith(f1.API)
            url = f1.API + url if url.startswith("/") else url
            # the bearer goes only to Opal's own origin; a pre-signed link to another host is fetched bare
            freq = urllib.request.Request(url, headers=(h if own else {}), method="GET")
            with urllib.request.urlopen(freq, timeout=60) as resp:
                file_status, body = resp.status, resp.read()
            import hashlib
            file_sha = hashlib.sha256(body).hexdigest()
            rows = [r for r in csv.reader(io.StringIO(body.decode("utf-8-sig"))) if r]
            head = [c.strip().lower() for c in rows[0]]
            col = head.index("ticker") if "ticker" in head else 0
            tickers = sorted({r[col].strip().upper() for r in rows[1:] if len(r) > col and r[col].strip()})
            table = pq.read_table(parquet_path).to_pydict()
            keys = [str(k) for k in table["security"]]
            by_plain = {k.rsplit(" US Equity", 1)[0].strip().upper(): i for i, k in enumerate(keys) if k.endswith(" US Equity")}
            exact = {k.strip().upper() for k in keys}
            per_input = {}
            for field in ("CNTRY_OF_DOMICILE", "GICS_SECTOR_NAME"):
                column = table[field]
                per_input[field] = sum(1 for t in tickers if t in by_plain and column[by_plain[t]] not in (None, ""))
            result.update(request=rid, original_sha256=file_sha, original_matches_served_sha=(file_sha == (answer.get("data") or {}).get("sha256")),
                          securities_in_request=len(tickers), store_rows=len(keys),
                          store_keys_with_us_equity_suffix=len(by_plain),
                          request_tickers_matching_a_store_key_after_suffix_strip=sum(1 for t in tickers if t in by_plain),
                          request_tickers_matching_a_store_key_exactly=sum(1 for t in tickers if t in exact),
                          request_tickers_with_a_non_null_value=per_input)
            summary.append(dict(read="INTERSECT original", http=status, file_http=file_status, securities_in_request=len(tickers),
                                matching_after_suffix_strip=result["request_tickers_matching_a_store_key_after_suffix_strip"],
                                matching_exactly=result["request_tickers_matching_a_store_key_exactly"], per_input=per_input))
        else:
            raise SystemExit("mode must be R3, R45, R6, CENSUS or INTERSECT")
    for row in summary:
        f1.say(json.dumps(row))
    result.update(ended_at=f1.stamp(), summary=summary, calls=f1.log)
    json.dump(result, open(out, "w", encoding="utf-8", newline="\n"), indent=1)
    return 0 if h else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
