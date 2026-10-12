"""AMGT_RESAPP round-98 PREP -- capture the /thesis payload of every resolved name from the CHECKOUT'S OWN handler (the code the redeploy would carry), in the shape of
AMGT_CORPUS's `aw4_capture.py`, so `aw4_compare.py <live pre> <this capture>` is the PREDICTION of the served effect before the act.

  PYTHONPATH=<the pin's worktree> python r98_thesis_local_capture.py <out.json>

READ-ONLY (S3 GETs through the handler's own readers; no AWS write, no invoke). The output holds client research content: it stays local and uncommitted.
Prints `capture names N ok K failed F` and the response-bytes line `aw4_capture.py` prints.
"""
import concurrent.futures
import json
import sys

from lib.research.api import scoped_amgt
from lib.research.corpus import dossier
from lib.research.harvest import store

KEEP_MODEL = ("line_names", "forecast_figures", "fiscal_unresolved", "team_sheet", "forecast_reason", "forecast_periods",
              "forecast_source_counts", "fiscal_row_count", "model_status")


def _one(key):
    event = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
    raw = scoped_amgt.handler(event)
    body = raw.get("body")
    payload = json.loads(body) if isinstance(body, str) else (body or {})
    size = len(body.encode("utf-8")) if isinstance(body, str) else len(json.dumps(body or {}).encode("utf-8"))
    ts = (payload.get("model") or {}).get("team_sheet")
    ts_bytes = None
    if isinstance(body, str):
        for sep, ea in (((", ", ": "), True), ((",", ":"), True), ((", ", ": "), False), ((",", ":"), False)):
            if len(json.dumps(payload, separators=sep, ensure_ascii=ea).encode("utf-8")) == size:
                ts_bytes = len(json.dumps(ts, separators=sep, ensure_ascii=ea).encode("utf-8"))
                break
    if ts_bytes is None:
        ts_bytes = len(json.dumps(ts).encode("utf-8"))
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
    keys = sorted(dossier._resolved_security_keys(client=store._default_client()))
    got, failed = {}, []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for fut in concurrent.futures.as_completed([pool.submit(_one, k) for k in keys]):
            try:
                key, rec = fut.result()
                got[key] = rec
            except Exception as exc:  # a failed read is counted and named, never dropped
                failed.append("%s: %s" % (type(exc).__name__, str(exc)[:100]))
    ok = sum(1 for r in got.values() if r["status"] == 200)
    json.dump({"function": {"LastModified": "LOCAL", "CodeSha256": "LOCAL " + dossier.METHOD_VERSION}, "keys": got},
              open(out_path, "w", encoding="utf-8"), sort_keys=True, ensure_ascii=True)
    sizes = sorted(r.get("response_bytes", 0) for r in got.values())
    print("capture names %d ok %d failed %d (dossier METHOD %s)" % (len(keys), ok, len(failed) + (len(got) - ok), dossier.METHOD_VERSION))
    if sizes:
        print("response_bytes min %d median %d max %d over_1MB %d" % (sizes[0], sizes[len(sizes) // 2], sizes[-1], sum(1 for x in sizes if x > 1048576)))
    for f in failed[:5]:
        print("failed %s" % f)
    return 0 if len(got) == len(keys) and ok == len(keys) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
