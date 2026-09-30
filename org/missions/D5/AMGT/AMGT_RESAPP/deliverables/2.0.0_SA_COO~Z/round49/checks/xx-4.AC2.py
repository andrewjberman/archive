"""AMGT_RESAPP round 49, AMGT-xx-4 AC2 -- ON THE SERVED PLANE: the DEPLOYED function's rank-history series carry the served name.

Read-only invokes of `opal-amgt-scoped-api`: GET /lead-panel/rankings/trending/chatter (the first five tickers), then
GET /lead-panel/timeseries/trending/chatter?tickers=<those five>,ZZZNOTHELD US. Every series carries `name`, `classification`,
`name_state`; at least one reads name_state SERVED; the unheld ticker reads ABSENT with a null name; no series is named by its ticker.
usage: python <this>   (from the repo root)"""
import importlib.util
import sys

import boto3

CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"


def main():
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    client = boto3.client("lambda", region_name=cl.REGION)
    print("deployed CodeSha256 %s" % client.get_function_configuration(FunctionName=cl.FUNCTION)["CodeSha256"])
    obj, meta = cl._invoke(client, "%s/lead-panel/rankings/trending/chatter" % cl.ROUTE_PREFIX)
    tickers = [str(r.get("ticker")) for r in ((obj or {}).get("rows") or [])[:5] if r.get("ticker")] + ["ZZZNOTHELD US"]
    obj, meta = cl._invoke(client, "%s/lead-panel/timeseries/trending/chatter" % cl.ROUTE_PREFIX, {"tickers": ",".join(tickers)})
    series = (obj or {}).get("series") or []
    bad = []
    served = 0
    for s in series:
        if not all(k in s for k in ("name", "classification", "name_state")):
            bad.append("series %s lacks name/classification/name_state" % s.get("ticker"))
            continue
        served += s.get("name_state") == "SERVED"
        if s.get("name") and s.get("name") == str(s.get("ticker") or "").split(" ")[0]:
            bad.append("series %s named by its ticker" % s.get("ticker"))
        if s.get("ticker") == "ZZZNOTHELD US" and (s.get("name_state") != "ABSENT" or s.get("name") is not None):
            bad.append("unheld ticker reads %r / %r" % (s.get("name_state"), s.get("name")))
    if not series or not served:
        bad.append("series %d, name SERVED %d (%s)" % (len(series), served, str(meta)[:160]))
    for b in bad:
        print("  BAD", b)
    print("tickers asked %d, series %d, name SERVED %d" % (len(tickers), len(series), served))
    ok = not bad
    print("THE DEPLOYED RANK-HISTORY SERIES CARRY THE SERVED NAME: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
