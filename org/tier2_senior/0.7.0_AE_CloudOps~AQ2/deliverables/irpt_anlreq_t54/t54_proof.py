"""IRPT_ANLREQ TO-APPLY-t54 step 6 (0.7.0_AE_CloudOps~AQ2): the driven proof of the `fail` op on ONE existing synthetic job row. No model call.

  python t54_proof.py --selftest      offline check of the comparison helpers
  python t54_proof.py --live --go     the sequence below

Row: tenant 49financial, job REQ-d47252fe74634d0c5cdd8067 (the FWD-1 run's synthetic request). Sequence: (0) read the row by get-item
(ConsistentRead): it must EXIST, its state is recorded, hop_failure must be ABSENT, else STOP with nothing written; (1) invoke
irpt-commentary-draft-store-lambda op=fail hop=COMMENTARY code=COMMENTARY_DRAFT_REFUSED twice: the first answer hop_failure_written true, the
second false; (2) read the row: hop_failure = {hop, code, at}, the state unchanged, every other attribute unchanged (a hash of the item
without hop_failure equals the hash read at (0)); (3) negative arm A: a REQ- id of 24 zeros answers hop_failure_written false and get-item
reads that key ABSENT; (4) negative arm B: tenant inflection with the 49financial request id answers REFUSED/UNAVAILABLE and the 49financial
row is unchanged; (5) RESTORE: remove ONLY hop_failure with a conditional update (condition: its code equals the recorded one) and read the
item back equal to the hash read at (0). The restore also runs in a finally if anything after the first write fails.
Prints statuses, names, hashes and the stamp's shape only; no attribute value other than state, hop and code is printed.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys

REGION = "us-east-1"
FN = "irpt-commentary-draft-store-lambda"
TABLE = "irpt-jobs"
TENANT = "49financial"
JOB = "REQ-d47252fe74634d0c5cdd8067"
ZERO = "REQ-" + "0" * 24
CODE = "COMMENTARY_DRAFT_REFUSED"


def digest(item, drop=()):
    return hashlib.sha256(json.dumps({k: v for k, v in item.items() if k not in drop}, sort_keys=True).encode()).hexdigest()


def selftest():
    a = {"tenant": {"S": "t"}, "state": {"S": "READY"}}
    b = dict(a, hop_failure={"M": {"code": {"S": "X"}}})
    assert digest(a) == digest(a) and digest(a) != digest(b)
    assert digest(b, drop=("hop_failure",)) == digest(a)
    assert digest({"x": {"S": "1"}, "y": {"S": "2"}}) == digest({"y": {"S": "2"}, "x": {"S": "1"}})
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?(Z|\+00:00)", "2026-10-16T09:00:00+00:00")
    print("SELFTEST OK helpers: digest (equal, differs on an added attribute, drop, key order), stamp shape")
    return 0


def live():
    import boto3
    ddb = boto3.client("dynamodb", region_name=REGION)
    lam = boto3.client("lambda", region_name=REGION)
    ks = {k["KeyType"]: k["AttributeName"] for k in ddb.describe_table(TableName=TABLE)["Table"]["KeySchema"]}
    print("key schema names: hash=%s range=%s" % (ks.get("HASH"), ks.get("RANGE")))

    def key(tenant, job):
        return {ks["HASH"]: {"S": tenant}, ks["RANGE"]: {"S": job}}

    def get(tenant, job):
        return ddb.get_item(TableName=TABLE, Key=key(tenant, job), ConsistentRead=True).get("Item")

    def invoke(payload):
        r = lam.invoke(FunctionName=FN, InvocationType="RequestResponse", Payload=json.dumps(payload).encode())
        body = json.loads(r["Payload"].read().decode() or "null")
        return r["StatusCode"], r.get("FunctionError"), body

    bad = []
    wrote = None
    pre = get(TENANT, JOB)
    if pre is None:
        print("STOP: the synthetic row does not exist; nothing written")
        return 2
    state0 = pre.get("state", {}).get("S")
    h0 = digest(pre)
    print("PRE row EXISTS: attribute names=%s state=%s hop_failure=%s item_sha256=%s" % (sorted(pre), state0, "PRESENT" if "hop_failure" in pre else "ABSENT", h0))
    if "hop_failure" in pre:
        print("STOP: hop_failure is not ABSENT; nothing written")
        return 2
    try:
        pay = {"op": "fail", "tenant": TENANT, "request_id": JOB, "hop": "COMMENTARY", "code": CODE}
        for n, want in ((1, True), (2, False)):
            sc, fe, body = invoke(pay)
            got = body.get("hop_failure_written") if isinstance(body, dict) else None
            ok = sc == 200 and not fe and isinstance(body, dict) and body.get("status") == "OK" and got is want
            print("INVOKE %d: StatusCode %s FunctionError %s status %s hop_failure_written %s expected %s %s" % (n, sc, fe, body.get("status") if isinstance(body, dict) else body, got, want, "PASS" if ok else "FAIL"))
            if n == 1 and got is True:
                wrote = True
            if not ok:
                bad.append("invoke %d" % n)
        post = get(TENANT, JOB)
        hf = (post or {}).get("hop_failure", {}).get("M")
        shape = bool(hf) and set(hf) == {"hop", "code", "at"}
        stamp = hf["at"].get("S", "") if shape else ""
        stamp_ok = bool(re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?(Z|\+00:00)", stamp))
        print("ROW after: hop_failure keys=%s hop=%s code=%s at=%s (UTC stamp shape %s)" % (sorted(hf) if hf else None, hf["hop"].get("S") if shape else None, hf["code"].get("S") if shape else None, stamp, "OK" if stamp_ok else "BAD"))
        row_ok = shape and hf["hop"].get("S") == "COMMENTARY" and hf["code"].get("S") == CODE and stamp_ok
        same_state = post.get("state", {}).get("S") == state0
        same_rest = digest(post, drop=("hop_failure",)) == h0
        print("ROW after: state %s (precondition %s) unchanged=%s; every other attribute unchanged (sha256 of the item without hop_failure equals PRE)=%s" % (post.get("state", {}).get("S"), state0, same_state, same_rest))
        if not (row_ok and same_state and same_rest):
            bad.append("row after the writes")
        h1 = digest(post)
        sc, fe, body = invoke(dict(pay, request_id=ZERO))
        absent = get(TENANT, ZERO) is None
        okA = sc == 200 and not fe and isinstance(body, dict) and body.get("hop_failure_written") is False and absent
        print("NEG A (no job row, 24 zeros): StatusCode %s hop_failure_written %s; get-item reads that key %s -> %s" % (sc, body.get("hop_failure_written") if isinstance(body, dict) else body, "ABSENT" if absent else "PRESENT", "PASS" if okA else "FAIL"))
        if not okA:
            bad.append("negative arm A")
        sc, fe, body = invoke(dict(pay, tenant="inflection"))
        unchanged = digest(get(TENANT, JOB) or {}) == h1
        okB = sc == 200 and isinstance(body, dict) and body.get("status") == "REFUSED" and body.get("reason") == "UNAVAILABLE" and unchanged
        print("NEG B (tenant inflection, the 49financial id): StatusCode %s answer=%s; the 49financial row unchanged=%s -> %s" % (sc, json.dumps(body, sort_keys=True), unchanged, "PASS" if okB else "FAIL"))
        if not okB:
            bad.append("negative arm B")
    finally:
        cur = get(TENANT, JOB)
        if cur is not None and "hop_failure" in cur and wrote:
            code = cur["hop_failure"]["M"]["code"]["S"]
            ddb.update_item(TableName=TABLE, Key=key(TENANT, JOB), UpdateExpression="REMOVE hop_failure",
                            ConditionExpression="hop_failure.#c = :c", ExpressionAttributeNames={"#c": "code"}, ExpressionAttributeValues={":c": {"S": code}})
            print("RESTORE: conditional REMOVE hop_failure (condition code == recorded %s) done" % code)
        fin = get(TENANT, JOB)
        eq = fin is not None and "hop_failure" not in fin and digest(fin) == h0
        print("RESTORE read: hop_failure %s; item sha256 equals PRE: %s" % ("ABSENT" if fin is not None and "hop_failure" not in fin else "PRESENT", eq))
        if not eq:
            bad.append("restore")
    print("PROOF %s %s" % ("OK" if not bad else "FAIL", bad or ""))
    return 0 if not bad else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--live" in sys.argv and "--go" in sys.argv:
        sys.exit(live())
    print(__doc__)
    sys.exit(2)
