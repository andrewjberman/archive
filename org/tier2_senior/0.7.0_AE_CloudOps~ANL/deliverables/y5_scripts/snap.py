"""Y5 snapshot of R2/R3/R4/R5 on the live irpt-status build. READ-ONLY. usage: snap.py <out.json>
Stores only booleans, digests, counts, codes, ids and key names. No principal, link or body."""
import hashlib
import json
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from irptlib import R_HISTORY, R_JOB, R_SECTIONS, code, config, invoke, owner_headers, requests_all  # noqa: E402


def find(o, key, path=""):
    """First (path, value) for a dict key anywhere in o."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key:
                return path + "/" + k, v
            r = find(v, key, path + "/" + k)
            if r:
                return r
    elif isinstance(o, list):
        for i, v in enumerate(o[:3]):
            r = find(v, key, path + "[%d]" % i)
            if r:
                return r
    return None


def dig(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True).encode()).hexdigest()[:16]


out = {"config": config()}
recs, den = requests_all()
out["scan"] = dict(den, requests=len(recs))
R2, R4 = {}, {}
for t, rid, r in recs:
    h = owner_headers(r)
    s = invoke(R_SECTIONS, h, {"jobId": rid}, {"selected_tenant": t})
    d = s.get("data") if isinstance(s, dict) else None
    row = {"tenant": t, "ok_shape": isinstance(d, dict), "code": code(s)}
    if isinstance(d, dict):
        prov = find(s, "provider")
        row.update({"data_keys": sorted(d.keys()), "retained_ref": "retained_ref" in d,
                    "provider": prov[1] if prov else None, "provider_path": prov[0] if prov else None,
                    "sections": len(d.get("sections") or []), "request_ref_digest": dig(d.get("request_ref"))})
        body = {k: v for k, v in d.items() if k != "retained_ref"}
        row["body_digest_without_retained_ref"] = dig(body)
    else:
        row["top_keys"] = sorted(s.keys()) if isinstance(s, dict) else None
    R2[rid] = row
    j = invoke(R_JOB, dict(h, **{"x-irpt-status-dates": "prospect-v1"}), {"jobId": rid}, {"selected_tenant": t})
    jd = j.get("data") if isinstance(j, dict) else None
    sd = find(j, "source_dates")
    R4[rid] = {"tenant": t, "code": code(j), "state": (find(j, "state") or (0, None))[1],
               "source_dates_present": bool(sd and sd[1]), "source_dates_digest": dig(sd[1]) if sd and sd[1] else None,
               "date_basis": (find(j, "date_basis") or (0, None))[1] if sd else None}
out["R2"] = R2
out["R4R5"] = R4

# R3: history as each owner of at least one request, all pages
def history(tenant, headers):
    """All history pages for one owner: (rows, pages, page_keys, row_keys, last_page, error)."""
    rows, pages, page_keys, row_keys, last, cursor = [], 0, set(), set(), {}, None
    while pages <= 40:
        q = {"selected_tenant": tenant, "limit": "25"}
        if cursor:
            q["cursor"] = cursor
        b = invoke(R_HISTORY, headers, None, q)
        d = b.get("data") if isinstance(b, dict) else None
        if not isinstance(d, dict):
            return rows, pages, page_keys, row_keys, last, {"error_code": code(b), "top_keys": sorted(b.keys()) if isinstance(b, dict) else None}
        pages += 1
        last = d
        page_keys.update(d.keys())
        for x in d.get("items") or []:
            row_keys.update(x.keys())
            rows.append(x)
        cursor = d.get("next_cursor")
        if not cursor:
            break
    return rows, pages, page_keys, row_keys, last, None


R3 = {}
seen = set()
for t, rid, r in recs:
    key = (t, r["owner"]["principal_id"], r["owner"]["home_firm_id"])
    if key in seen:
        continue
    seen.add(key)
    rows, pages, page_keys, row_keys, last, err = history(t, owner_headers(r))
    if err is not None:
        R3[len(R3)] = dict(err, tenant=t)
        continue
    claims = {}
    for x in rows:
        c = str(x.get("client_claim"))
        claims[c] = claims.get(c, 0) + 1
    R3[len(R3)] = {"tenant": t, "pages": pages, "rows": len(rows), "page_keys": sorted(page_keys),
                   "row_keys": sorted(row_keys), "has_client_id": "client_id" in row_keys,
                   "has_client_claim": "client_claim" in row_keys, "claims": claims,
                   "unreadable_rows": last.get("unreadable_rows"),
                   "row_ids_digest": dig(sorted(json.dumps(x.get("identity"), sort_keys=True) for x in rows))}
out["R3"] = R3
with open(sys.argv[1], "w", encoding="ascii", newline="\n") as fh:
    fh.write(json.dumps(out, indent=1, sort_keys=True, default=str) + "\n")
print("WROTE", sys.argv[1])
print("config", out["config"], "scan", out["scan"])
print("R2 ok", sum(1 for v in R2.values() if v["ok_shape"]), "of", len(R2), "| codes", sorted({str(v["code"]) for v in R2.values()}))
print("R2 providers", sorted({str(v.get("provider")) for v in R2.values()}), "retained_ref present", sum(1 for v in R2.values() if v.get("retained_ref")))
print("R4R5 dates present", sum(1 for v in R4.values() if v["source_dates_present"]), "of", len(R4), "| codes", sorted({str(v["code"]) for v in R4.values()}), "| states", sorted({str(v["state"]) for v in R4.values()}))
for k, v in R3.items():
    print("R3", {a: v[a] for a in v if a not in ("row_ids_digest",)})
