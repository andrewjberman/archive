"""AMGT_CORPUS round 44, CRPS-at-10 LEG P -- the issuer's served read on the LIVE `opal-amgt-scoped-api` (pair
NEVER_WIDEN_ROUND44_AT10_LEGP_SERVED_EFFECT.md, section "THE ISSUER'S POST-ACT READ"). Issuer's file. READ-ONLY.

  PYTHONPATH=. python at10_legp_read.py --pre  <snapshot.json>     record the three names' blocks on the function as it is NOW
  PYTHONPATH=. python at10_legp_read.py --post <snapshot.json>     read again and compare to the snapshot

Per name (TSM_US_Equity master_absent, SAN_FP_Equity own_new, ROG_SW_Equity own_model), GET-shaped direct invoke of
/api/scoped/amgt/security/<key>/thesis. Blocks compared whole: model.team_cases, dossier_fields, dossier_sections, and every key of `model` other
than team_sheet. Prints the function's LastModified and CodeSha256, then per name: model.team_sheet class / row count / reason, and
EQUAL|DIFFERENT for each compared block. `leg p read <m>/3` counts names where team_sheet matches the stored /11 dossier field and every
other compared block is EQUAL to the snapshot.
"""
import json
import sys

import boto3

from lib.research.corpus import dossier
from lib.research.harvest import store

FN = "opal-amgt-scoped-api"
NAMES = ("TSM_US_Equity", "SAN_FP_Equity", "ROG_SW_Equity")


def _canon(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=True)


def _served(lam, key):
    event = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
    raw = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    body = raw.get("body")
    payload = json.loads(body) if isinstance(body, str) else (body or {})
    model = payload.get("model") or {}
    blocks = {
        "status": raw.get("statusCode"),
        "team_cases": model.get("team_cases"),
        "dossier_fields": payload.get("dossier_fields"),
        "dossier_sections": payload.get("dossier_sections"),
        "model_other_keys": {k: v for k, v in model.items() if k != "team_sheet"},
    }
    return blocks, model.get("team_sheet", "<KEY ABSENT>")


def _stored_11(key):
    current = dossier.METHOD_VERSION
    dossier.METHOD_VERSION = "amgt-corpus-dossier/11"
    try:
        doc = dossier.read_dossier(key, client=store._default_client())["document"]
    finally:
        dossier.METHOD_VERSION = current
    return (doc.get("fields") or {}).get("team_sheet")


def main():
    mode = "--post" if "--post" in sys.argv else "--pre"
    path = sys.argv[-1]
    lam = boto3.client("lambda", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FN)
    print("function %s LastModified %s CodeSha256 %s" % (FN, cfg.get("LastModified"), cfg.get("CodeSha256")))
    if mode == "--pre":
        snap = {"function": {"LastModified": cfg.get("LastModified"), "CodeSha256": cfg.get("CodeSha256")}, "names": {}}
        for key in NAMES:
            blocks, ts = _served(lam, key)
            snap["names"][key] = {"blocks": blocks, "team_sheet": ts}
            print("PRE %s status %s team_sheet %s" % (key, blocks["status"], "KEY ABSENT" if ts == "<KEY ABSENT>" else "present"))
        json.dump(snap, open(path, "w", encoding="utf-8"), sort_keys=True, ensure_ascii=True)
        print("snapshot written %s" % path)
        return 0
    snap = json.load(open(path, encoding="utf-8"))
    ok = 0
    for key in NAMES:
        blocks, ts = _served(lam, key)
        stored = _stored_11(key)
        pre = snap["names"][key]["blocks"]
        ts_ok = _canon(ts) == _canon(stored)
        eq = {b: (_canon(blocks[b]) == _canon(pre[b])) for b in blocks}
        rows = ts.get("rows") if isinstance(ts, dict) else None
        print("POST %s status %s team_sheet class %s rows %s reason %s equals_stored_/11 %s" % (
            key, blocks["status"], (ts or {}).get("class") if isinstance(ts, dict) else ts,
            len(rows) if isinstance(rows, list) else None, ((ts or {}).get("reason") or "")[:90] if isinstance(ts, dict) else "", ts_ok))
        for b, same in sorted(eq.items()):
            print("  %s %s" % (b, "EQUAL" if same else "DIFFERENT"))
        if ts_ok and all(eq.values()):
            ok += 1
    print("leg p read %d/3" % ok)
    return 0 if ok == 3 else 1


if __name__ == "__main__":
    sys.exit(main())
