"""AMGT_RESAPP round 46, AMGT-uu-4 AC3 -- ON THE SERVED PLANE, EVERY SERVED BASE CASE IS ON THE ADJUSTED BASIS AND CARRIES ITS BASIS.

One read-only invoke of the DEPLOYED opal-amgt-scoped-api's /thesis route per name of the LIVE research library (read fresh,
read time printed). Over the names whose served model.cases.base is SERVED: base.inputs.consensus_eps.basis is an object with a
`mnemonic`; base.inputs.trailing_median_pe.basis names both PX_LAST and IS_COMP_EPS_ADJUSTED; base.formula contains
"adjusted"; upside and downside equal the ruled ABSENT object. Denominators printed: names, reads OK, base SERVED, compliant.
A name with no identity or a failed read is COUNTED and printed, never dropped. Exit 0 only when every SERVED base complies,
at least one base is SERVED, and no read failed. usage: python <this>   (from the repo root)"""
import datetime
import importlib.util
import json
import os
import sys

import boto3

sys.path.insert(0, os.getcwd())
CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
RULED = {"status": "ABSENT", "reason": "methodology to be discussed with Andrew"}


def main():
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    from lib.research.corpus import library
    from lib.research.identity import crosswalk
    from lib.research.api import scoped_amgt as sa
    root = library.library_root()
    folders = list(library.list_folders(root))
    print("population: LIVE research library %s, %d folders, read_at %s" % (
        root, len(folders), datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")), flush=True)
    client = boto3.client("lambda", region_name=cl.REGION)
    print("deployed CodeSha256 %s" % client.get_function_configuration(FunctionName=cl.FUNCTION)["CodeSha256"])
    pilots = crosswalk.load_pilots()
    n_read = n_fail = n_served = n_ok = 0
    for folder in folders:
        key = sa.resolve_identity(crosswalk.harvester_key(folder, pilots)[0]).get("security_key")
        if not key:
            n_fail += 1
            print("NO-IDENTITY %s" % folder)
            continue
        obj, meta = cl._invoke(client, "%s/security/%s/thesis" % (cl.ROUTE_PREFIX, key))
        if obj is None:
            n_fail += 1
            print("READ-FAILED %s %s" % (key, json.dumps(meta)[:160]))
            continue
        n_read += 1
        cases = ((obj.get("model") or {}).get("cases")) or {}
        base = cases.get("base") or {}
        if base.get("status") != "SERVED":
            continue
        n_served += 1
        inp = base.get("inputs") or {}
        bad = []
        if not isinstance((inp.get("consensus_eps") or {}).get("basis"), dict) or not inp["consensus_eps"]["basis"].get("mnemonic"):
            bad.append("consensus_eps.basis")
        pb = json.dumps((inp.get("trailing_median_pe") or {}).get("basis") or "")
        if "PX_LAST" not in pb or "IS_COMP_EPS_ADJUSTED" not in pb:
            bad.append("trailing_median_pe.basis")
        if "adjusted" not in str(base.get("formula") or "").lower():
            bad.append("formula")
        if cases.get("upside") != RULED or cases.get("downside") != RULED:
            bad.append("upside/downside moved")
        if bad:
            print("NON-COMPLIANT %s: %s" % (key, ", ".join(bad)))
        else:
            n_ok += 1
    print("served: reads OK %d of %d names (failed %d); base SERVED %d; ADJUSTED AND BASIS-CARRYING %d of %d" % (
        n_read, len(folders), n_fail, n_served, n_ok, n_served))
    return 0 if n_served and n_ok == n_served and n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
