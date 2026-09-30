"""AMGT_RESAPP round 47, AMGT-vv-4 AC3 -- ON THE SERVED PLANE: every SERVED Base case's formula names each input's own basis, and
/thesis carries the team's cases beside it exactly as the dossier holds them.

One read-only invoke of the DEPLOYED function's /thesis route per LIVE research-library name (read time printed). Per name:
(a) when `model.cases.base` is SERVED, its `formula` == "Bloomberg consensus EPS (FY1, BEST_EPS) x adjusted trailing-median P/E
    (PX_LAST / IS_COMP_EPS_ADJUSTED)" and its `label` == "Historical-multiple reference" (the CTO anchor ruling 2);
(b) `model.team_cases` exists, and per case its `status` is SERVED exactly when `read_dossier(key)`'s case `value` is not null.
Denominators printed. Exit 0 only when (a) and (b) hold on every read name, at least one base and one team case is SERVED, and no
read failed. usage: python <this>   (from the repo root)"""
import datetime
import importlib.util
import os
import sys

import boto3

sys.path.insert(0, os.getcwd())
CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
WANT = "Bloomberg consensus EPS (FY1, BEST_EPS) x adjusted trailing-median P/E (PX_LAST / IS_COMP_EPS_ADJUSTED)"
LABEL = "Historical-multiple reference"


def main():
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    from lib.research.corpus import dossier, library
    from lib.research.identity import crosswalk
    from lib.research.api import scoped_amgt as sa
    root = library.library_root()
    folders = list(library.list_folders(root))
    print("population: LIVE research library %s, %d folders, read_at %s" % (
        root, len(folders), datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")), flush=True)
    client = boto3.client("lambda", region_name=cl.REGION)
    print("deployed CodeSha256 %s" % client.get_function_configuration(FunctionName=cl.FUNCTION)["CodeSha256"])
    pilots = crosswalk.load_pilots()
    n_read = n_fail = n_base = n_formula = n_team_served = n_team_ok = 0
    for folder in folders:
        key = sa.resolve_identity(crosswalk.harvester_key(folder, pilots)[0]).get("security_key")
        obj, meta = cl._invoke(client, "%s/security/%s/thesis" % (cl.ROUTE_PREFIX, key)) if key else (None, {"no_identity": folder})
        if obj is None:
            n_fail += 1
            print("READ-FAILED %s %s" % (key, str(meta)[:140]))
            continue
        n_read += 1
        model = obj.get("model") or {}
        base = (model.get("cases") or {}).get("base") or {}
        if base.get("status") == "SERVED":
            n_base += 1
            if base.get("formula") == WANT and base.get("label") == LABEL:
                n_formula += 1
            else:
                print("FORMULA/LABEL %s: %r / %r" % (key, base.get("formula"), base.get("label")))
        team = model.get("team_cases")
        try:
            dcases = (dossier.read_dossier(key)["document"].get("fields") or {}).get("cases") or {}
        except LookupError:
            dcases = {}
        good = isinstance(team, dict)
        for name in ("base", "upside", "downside"):
            want_served = (dcases.get(name) or {}).get("value") is not None
            got = (team or {}).get(name) or {}
            n_team_served += got.get("status") == "SERVED"
            good = good and ((got.get("status") == "SERVED") == want_served)
        n_team_ok += good
        if not good:
            print("TEAM-CASES %s: served %s" % (key, None if team is None else {k: (v or {}).get("status") for k, v in team.items()}))
    print("served: reads OK %d of %d (failed %d); base SERVED %d, formula as ruled %d of %d; team_cases as the dossier holds "
          "them %d of %d names, %d case(s) SERVED" % (n_read, len(folders), n_fail, n_base, n_formula, n_base, n_team_ok, n_read,
                                                     n_team_served))
    ok = n_fail == 0 and n_base and n_formula == n_base and n_team_ok == n_read and n_team_served > 0
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
