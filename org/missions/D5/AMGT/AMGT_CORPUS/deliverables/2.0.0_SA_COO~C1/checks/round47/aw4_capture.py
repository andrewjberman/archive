"""AMGT_CORPUS round 47, CRPS-aw-4 / aw-6 -- capture the LIVE /thesis payload of every resolved name (round 46's av_capture.py with the response
SIZE in bytes added: the CTO's ceiling of 1 MB per response, msg 4086 point 3). READ-ONLY. Issuer's file.

  PYTHONPATH=. python aw4_capture.py <out.json>

For every resolved security (`dossier._resolved_security_keys`), a GET-shaped direct invoke of the live `opal-amgt-scoped-api`
(`/api/scoped/amgt/security/<key>/thesis`, firm header `opal`), keeping only what the Model tab reads: `fiscal_year_figures`,
`fiscal_years`, `header_figures`, `check_face`, `model_status` and the `model` block's `line_names`, `forecast_figures`,
`fiscal_unresolved`, `team_sheet`. Prints the function's LastModified and CodeSha256 and one line `capture names N ok K failed F`.
The output file holds client research content: it stays local (the scratchpad), and only the derived census is committed.
"""
import concurrent.futures
import json
import sys

import boto3

from lib.research.corpus import dossier
from lib.research.harvest import store

FN = "opal-amgt-scoped-api"
KEEP_MODEL = ("line_names", "forecast_figures", "fiscal_unresolved", "team_sheet", "forecast_reason", "forecast_periods",
              "forecast_source_counts", "fiscal_row_count", "model_status")


def _one(lam, key):
    event = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
    raw = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    body = raw.get("body")
    # team_sheet bytes AS SERIALISED in this response: the separator style that reproduces the body's own length (default first, then compact)
    ts_bytes = None
    try:
        _p = json.loads(body) if isinstance(body, str) else (body or {})
        _ts = (_p.get("model") or {}).get("team_sheet")
        _n = len(body.encode("utf-8")) if isinstance(body, str) else None
        for _sep, _ea in (((", ", ": "), True), ((",", ":"), True), ((", ", ": "), False), ((",", ":"), False)):
            if _n is not None and len(json.dumps(_p, separators=_sep, ensure_ascii=_ea).encode("utf-8")) == _n:
                ts_bytes = len(json.dumps(_ts, separators=_sep, ensure_ascii=_ea).encode("utf-8"))
                break
        if ts_bytes is None:
            ts_bytes = len(json.dumps(_ts).encode("utf-8"))
    except Exception:  # a capture never fails on the size estimate
        ts_bytes = None
    size = len(body.encode("utf-8")) if isinstance(body, str) else len(json.dumps(body or {}).encode("utf-8"))
    payload = json.loads(body) if isinstance(body, str) else (body or {})
    model = payload.get("model") or {}
    return key, {
        "status": raw.get("statusCode"),
        "response_bytes": size,
        "team_sheet_bytes": ts_bytes,
        "model_status": payload.get("model_status"),
        "fiscal_year_figures": payload.get("fiscal_year_figures"),
        "fiscal_years": payload.get("fiscal_years"),
        "header_figures": payload.get("header_figures"),
        "posture": payload.get("posture"),
        "dossier_fields": payload.get("dossier_fields"),
        "check_face": payload.get("check_face"),
        "model": {k: model.get(k, "<KEY ABSENT>") for k in KEEP_MODEL},
    }


def main(argv):
    out_path = argv[0]
    lam = boto3.client("lambda", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FN)
    print("function %s LastModified %s CodeSha256 %s" % (FN, cfg.get("LastModified"), cfg.get("CodeSha256")))
    keys = sorted(dossier._resolved_security_keys(client=store._default_client()))
    got = {}
    failed = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for fut in concurrent.futures.as_completed([pool.submit(_one, lam, k) for k in keys]):
            try:
                key, rec = fut.result()
                got[key] = rec
            except Exception as exc:  # a failed invoke is counted and named, never dropped
                failed.append(str(exc)[:120])
    ok = sum(1 for r in got.values() if r["status"] == 200)
    json.dump({"function": {"LastModified": cfg.get("LastModified"), "CodeSha256": cfg.get("CodeSha256")}, "keys": got},
              open(out_path, "w", encoding="utf-8"), sort_keys=True, ensure_ascii=True)
    sizes = sorted(r.get("response_bytes", 0) for r in got.values())
    print("capture names %d ok %d failed %d" % (len(keys), ok, len(failed) + (len(got) - ok)))
    if sizes:
        print("response_bytes min %d median %d max %d over_1MB %d" % (sizes[0], sizes[len(sizes) // 2], sizes[-1], sum(1 for x in sizes if x > 1048576)))
    for f in failed[:5]:
        print("failed %s" % f)
    return 0 if len(got) == len(keys) and ok == len(keys) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
