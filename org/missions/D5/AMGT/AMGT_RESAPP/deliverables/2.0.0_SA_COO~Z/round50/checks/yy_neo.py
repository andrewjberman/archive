"""AMGT_RESAPP round 50 -- the proxy's officers served and labelled for what they are (AMGT-yy-3, CTO round-49 ruling 3).

--plane plan:   `python -m lib.research.management.proxy_officers --persist --dry-run --security-key <K>` prints the M-1 object it
                WOULD write (JSON on stdout, one object): officers >= 3, `officer_set` == "named_executive_officers",
                `officer_set_label` == LABEL, `source_form` == "DEF 14A", a `source_accession`. Nothing is written.
--plane local:  this tree's `read_management(key)` over that PLANNED object (the pool read stubbed to it) carries the officers,
                `officer_set`, `officer_set_label`, `source_form`, `source_accession` through to the payload.
--plane served: the DEPLOYED function's management payload for the key carries the same (after the real write).
Names: INTU_US_Equity and HAL_US_Equity (the two whose annual report points elsewhere).
usage: python <this> --plane plan|local|served   (from the repo root)"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys

sys.path.insert(0, os.getcwd())
CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
NAMES = ["INTU_US_Equity", "HAL_US_Equity"]
LABEL = "Named executive officers, from the company's latest proxy statement (DEF 14A)"
FIELDS = ("officer_set", "officer_set_label", "source_form", "source_accession")


def planned(key):
    p = subprocess.run([sys.executable, "-m", "lib.research.management.proxy_officers", "--persist", "--dry-run",
                        "--security-key", key], capture_output=True, text=True, encoding="utf-8", timeout=55,
                       env=dict(os.environ, PYTHONPATH=os.getcwd()))
    if p.returncode != 0:
        return None, "rc=%s %s" % (p.returncode, (p.stderr or p.stdout)[-160:])
    try:
        return json.loads(p.stdout), None
    except ValueError:
        return None, "stdout is not one JSON object: %r" % p.stdout[:120]


def judge(key, obj, bad):
    if not isinstance(obj, dict):
        bad.append("%s: no object" % key)
        return
    officers = obj.get("officers") or []
    if len(officers) < 3:
        bad.append("%s: officers %d" % (key, len(officers)))
    if obj.get("officer_set") != "named_executive_officers" or obj.get("officer_set_label") != LABEL:
        bad.append("%s: set/label %r / %r" % (key, obj.get("officer_set"), obj.get("officer_set_label")))
    if obj.get("source_form") != "DEF 14A" or not obj.get("source_accession"):
        bad.append("%s: source %r %r" % (key, obj.get("source_form"), obj.get("source_accession")))
    print("  %s officers %d, set %r, source %r %r" % (key, len(officers), obj.get("officer_set"), obj.get("source_form"),
                                                     obj.get("source_accession")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plane", choices=("plan", "local", "served"), required=True)
    a = ap.parse_args()
    bad = []
    for key in NAMES:
        if a.plane == "served":
            spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
            cl = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cl)
            import boto3
            obj, meta = cl._invoke(boto3.client("lambda", region_name=cl.REGION), "%s/security/%s/thesis" % (cl.ROUTE_PREFIX, key))
            judge(key, (obj or {}).get("management"), bad)
            continue
        plan, err = planned(key)
        if err:
            bad.append("%s: plan %s" % (key, err))
            continue
        if a.plane == "plan":
            judge(key, plan, bad)
            # AMENDMENT 1 (row Z-W177-S2): the object yy-5 writes into the served M-1 store must validate against that store's
            # own schema -- enrich.validate over lib/research/management/management.schema.json.
            from lib.research.management import enrich
            try:
                result = enrich.validate(plan)  # returns (valid: bool, errors: list)
                problems = [] if (isinstance(result, tuple) and result[0]) else (result[1] if isinstance(result, tuple) else result)
            except Exception as exc:  # noqa: BLE001 -- a raise is a refusal
                problems = ["%s: %s" % (type(exc).__name__, str(exc)[:160])]
            if problems:
                bad.append("%s: planned object fails management.schema.json: %s" % (key, str(problems)[:200]))
            else:
                print("  %s validates against management.schema.json" % key)
            continue
        from lib.research.api import scoped_amgt as sa
        saved = sa.read_pool_object
        try:
            sa.read_pool_object = lambda prefix, k, *args, **kw: (plan, {"status": "SERVED", "key": "stub"}) if prefix == sa.MANAGEMENT_PREFIX else saved(prefix, k, *args, **kw)
            judge(key, sa.read_management(key), bad)
        finally:
            sa.read_pool_object = saved
    for b in bad:
        print("  BAD", b)
    ok = not bad
    print("THE PROXY'S OFFICERS ARE SERVED AS NAMED EXECUTIVE OFFICERS (%s): %s" % (a.plane, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
