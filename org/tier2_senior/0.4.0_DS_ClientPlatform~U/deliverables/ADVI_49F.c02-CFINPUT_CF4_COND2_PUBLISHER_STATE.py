"""CF-4 condition (2), CTO 76420: RE-VERIFY the served-delta-0 basis AT DEPLOY TIME.

"a 24-hour-old measurement of the thing that makes this safe is not the thing that makes this
safe." The basis is AE~L's @bfb74b20c2 finding that the ADVI publisher activation is NOT BUILT,
measured on three planes. Each plane is re-read here, now, and each carries a POSITIVE CONTROL
so an absence cannot be manufactured by a broken instrument or a permissions artifact.

If ANY plane has changed state, the correct outcome is STOP and the gate re-opens.
Read-only: describes and lists, changes nothing.
"""
import sys

import boto3

REGION = "us-east-1"
SCHEDULE = "advi-49f-publisher"
PUB_DOC = "advi-49f-publisher-dispatch"
CTRL_DOC = "advi-49f-chain-dispatch"

ok = True
print("CF-4 CONDITION (2) -- publisher activation state, RE-MEASURED at deploy time\n")

# ---- PLANE 1: SCHEDULE -------------------------------------------------------
print("PLANE 1 -- SCHEDULE")
try:
    sch = boto3.client("scheduler", region_name=REGION)
    try:
        g = sch.get_schedule(Name=SCHEDULE)
        state = g.get("State")
        print(f"  {SCHEDULE}: State={state}  ScheduleExpression={g.get('ScheduleExpression')}")
        print(f"    target Input names document: "
              f"{(g.get('Target', {}) or {}).get('Input', '')[:120]}")
        if state != "DISABLED":
            ok = False
            print("    *** CHANGED: schedule is no longer DISABLED -- STOP, gate re-opens ***")
    except sch.exceptions.ResourceNotFoundException:
        print(f"  {SCHEDULE}: NOT FOUND (also a not-built state)")
    # POSITIVE CONTROL: the lister must be able to see schedules at all
    n = len(sch.list_schedules(MaxResults=100).get("Schedules", []))
    print(f"    POSITIVE CONTROL: list_schedules returns {n} schedule(s) -- instrument LIVE"
          if n else "    *** CONTROL DEAD: list_schedules returned 0 -- absence is not evidence ***")
    ok = ok and bool(n)
except Exception as exc:
    ok = False
    print(f"  INSTRUMENT ERROR: {type(exc).__name__}: {exc} -- NOT a not-built verdict")

# ---- PLANE 2: SSM DOCUMENT ---------------------------------------------------
print("\nPLANE 2 -- SSM DOCUMENT")
try:
    ssm = boto3.client("ssm", region_name=REGION)

    def doc_state(name):
        try:
            d = ssm.describe_document(Name=name)["Document"]
            return d.get("Status")
        except ssm.exceptions.InvalidDocument:
            return None

    pub = doc_state(PUB_DOC)
    ctrl = doc_state(CTRL_DOC)
    print(f"  {PUB_DOC}: {'ABSENT' if pub is None else pub}")
    print(f"  POSITIVE CONTROL {CTRL_DOC}: {'ABSENT' if ctrl is None else ctrl}"
          f"  -- {'instrument LIVE' if ctrl else '*** CONTROL DEAD ***'}")
    if pub is not None:
        ok = False
        print("    *** CHANGED: the publisher document now EXISTS -- STOP, gate re-opens ***")
    ok = ok and (ctrl is not None)
except Exception as exc:
    ok = False
    print(f"  INSTRUMENT ERROR: {type(exc).__name__}: {exc} -- NOT a not-built verdict")

# ---- PLANE 3: LAMBDA ALLOWLIST ----------------------------------------------
print("\nPLANE 3 -- LAMBDA ALLOWLIST")
try:
    lam = boto3.client("lambda", region_name=REGION)
    fns = [f for p in lam.get_paginator("list_functions").paginate()
           for f in p["Functions"] if "49f" in f["FunctionName"].lower()
           or "advi" in f["FunctionName"].lower()]
    print(f"  candidate dispatcher functions: {[f['FunctionName'] for f in fns]}")
    for f in fns:
        cfg = lam.get_function_configuration(FunctionName=f["FunctionName"])
        env = (cfg.get("Environment", {}) or {}).get("Variables", {}) or {}
        allowed = env.get("ALLOWED_DOCUMENTS")
        default = env.get("SSM_DOCUMENT_NAME")
        print(f"  {f['FunctionName']}: ALLOWED_DOCUMENTS="
              f"{'UNSET' if allowed is None else allowed} | SSM_DOCUMENT_NAME={default}")
        if allowed and PUB_DOC in allowed:
            ok = False
            print("    *** CHANGED: publisher document is now ALLOWLISTED -- STOP ***")
    if not fns:
        print("  *** no candidate function matched -- instrument cannot speak to this plane ***")
        ok = False
except Exception as exc:
    ok = False
    print(f"  INSTRUMENT ERROR: {type(exc).__name__}: {exc} -- NOT a not-built verdict")

print(f"\nCF-4 CONDITION (2) VERDICT: {'UNCHANGED -- deploy may proceed' if ok else 'STOP'}")
print("Basis re-measured, not inherited from @bfb74b20c2 (2026-08-26).")
sys.exit(0 if ok else 1)
