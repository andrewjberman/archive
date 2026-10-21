"""Round-47 person_access narrowing check (OG-pa-1: Menachem's tool narrowing, written by the grant writer on Andrew's owner confirm).

usage: python3 -I pacheck.py <phaseA|phaseB> <W-directory>
Prints labelled lines and a last line OK or NO. Counts and hashes only; no tool-name list, e-mail address or identifier is printed.

PHASE A reads W/PA1_CANDIDATE.json and W/PA1_PREFLIGHT_DECIDE.json.
PHASE B re-reads the LIVE person_access record (a strong read through the policy partition) and W/PA1_READBACK.json.
"""
import hashlib
import json
import os
import sys

phase, W = sys.argv[1], sys.argv[2]
WANT = {"client": 5, "schwab": 5, "etfs": 18, "portal_v2": 18}
TOTAL = sum(WANT.values())


def Y(x):
    return "yes" if x else "no"


def load(name):
    try:
        return json.load(open(os.path.join(W, name), encoding="utf-8"))
    except Exception:
        return None


def phase_a():
    c, p = load("PA1_CANDIDATE.json"), load("PA1_PREFLIGHT_DECIDE.json")
    pr = (c or {}).get("principal") or {}
    ch = (c or {}).get("change") or {}
    ok_pr = bool(c) and pr.get("role") == "menachem" and pr.get("present") is True and bool(pr.get("pk_hash")) and bool((c.get("denominator") or {}).get("registry_tools"))
    ok_ch = (ch.get("counts") == WANT and ch.get("tools_allow_total") == TOTAL and isinstance(ch.get("names_sha256"), str) and len(ch["names_sha256"]) == 64
             and ch.get("within_limits") is True and ch.get("source") == "registry of the deployed release" and ch.get("narrows_only") is True)
    dec = (p or {}).get("menachem") or {}
    ok_d = (bool(p) and dec.get("admit_all_non_client_candidate") is True and dec.get("client_admitted_without_per_firm_grant") is False
            and isinstance(dec.get("refused_outside_count"), int) and dec["refused_outside_count"] >= 1 and dec.get("outside_sample_refused") is True)
    print("candidate: menachem present with pk_hash and a printed registry denominator: %s" % Y(ok_pr))
    print("change: tools_allow counts client 5, schwab 5, etfs 18, portal_v2 18 (total %d), names hash, within the 64-item and 128-character limits, taken from the deployed registry, narrows only: %s" % (TOTAL, Y(ok_ch)))
    print("decide() pre-flight with the candidate applied: admits every non-client candidate tool, admits no client_* tool without a per-firm grant, refuses the outside sample: %s" % Y(ok_d))
    print("OK" if (ok_pr and ok_ch and ok_d) else "NO")


def phase_b():
    try:
        import boto3
        from boto3.dynamodb.types import TypeDeserializer
        td = TypeDeserializer()
        c = boto3.client("dynamodb", region_name="us-east-1")
        kw = {"TableName": "gateway-access-state-table", "ConsistentRead": True,
              "FilterExpression": "begins_with(pk,:p)", "ExpressionAttributeValues": {":p": {"S": "POLICY#"}}}
        items = []
        while True:
            r = c.scan(**kw)
            items += r["Items"]
            if "LastEvaluatedKey" not in r:
                break
            kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
    except Exception as e:
        print("live read FAILED %s" % type(e).__name__)
        print("NO")
        return

    def val(i, k):
        return list(i[k].values())[0] if k in i else None

    pk = None
    for i in items:
        if val(i, "record_type") == "principal_profile" and (val(i, "email") or "").lower().startswith("menachem"):
            pk = val(i, "pk")
    rec = None
    for i in items:
        if pk and val(i, "pk") == pk and val(i, "record_type") == "person_access":
            rec = i
    names = []
    if rec is not None and "tools_allow" in rec:
        names = sorted(str(x) for x in td.deserialize(rec["tools_allow"]))
    cand = (load("PA1_CANDIDATE.json") or {}).get("change") or {}
    sha = hashlib.sha256("\n".join(names).encode()).hexdigest() if names else ""
    status = val(rec, "status") if rec is not None else None
    rb = load("PA1_READBACK.json") or {}
    mk = (load("rl18_release.json") or {}).get("release_sha", "")
    oc = rb.get("owner_confirm") or {}
    dec = rb.get("decide") or {}
    ok_live = rec is not None and status == "active" and len(names) == TOTAL and sha == cand.get("names_sha256")
    ok_oc = oc.get("route") == "POST /api/admin/people/{tid}/{oid}/access" and oc.get("verdict") == "written" and oc.get("by") == "owner"
    ok_d = (dec.get("tree") == "deployed" and bool(mk) and dec.get("code_sha") == mk and dec.get("admit_all_non_client_candidate") is True
            and dec.get("client_admitted_without_per_firm_grant") is False and dec.get("outside_sample_refused") is True)
    print("live person_access record for menachem: active %s; tools_allow total %d (want %d); names hash equals the candidate's: %s" % (Y(status == "active"), len(names), TOTAL, Y(ok_live)))
    print("written by the grant writer on the owner's confirm through the People route (verdict written, by owner): %s" % Y(ok_oc))
    print("decide() on the LIVE record against the DEPLOYED tree at the batch17 release: admits every non-client candidate tool, no client_* tool without a per-firm grant, refuses the outside sample: %s" % Y(ok_d))
    print("OK" if (ok_live and ok_oc and ok_d) else "NO")


phase_a() if phase == "phaseA" else phase_b()
