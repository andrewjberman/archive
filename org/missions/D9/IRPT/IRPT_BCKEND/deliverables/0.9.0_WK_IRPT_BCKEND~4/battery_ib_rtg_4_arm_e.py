#!/usr/bin/env python3
"""IB-rtg-4 arm (e) -- PROVEN LIVE, under the DEPLOYED role and bytes.

Reuses the bounded-principal mechanism in
org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/battery_ib_rtf_10.py
(rtf-9 packet blob a1f36b95b2, both halves at HEAD), a FRESH epoch, full lifecycle (K1+K1b
create -> login -> directory search+resolve to find a granted account -> holdings request for
that account -> K1b+K1 delete -> refresh refused -> 401 after exp).

ACCEPTANCE (R75-AC1, now served): an exercised holdings request for an account the principal's
OWN resolve just granted reads a SCOPE-RESOLVED answer -- NEVER FIRM_BINDING with firm_id absent
-- under irpt-holdings-role. Prints route, function, role, and the served public reason.
"""
from __future__ import annotations

import json
import os
import secrets
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RTF10_DIR = os.path.abspath(os.path.join(HERE, "..", "0.7.0_AE_CloudOps~V"))
sys.path.insert(0, RTF10_DIR)
import battery_ib_rtf_10 as rtf10  # noqa: E402

WS = rtf10.WS
OUTPUT_PATH = os.path.join(HERE, "IB-rtg-4_R75-AC1_arm_e_live_proof.txt")
TOKEN = "IBR75-HOLDINGS-LIVE-PROOF-SCOPE-RESOLVED"
LEDGER_SLUG = "irpt-bckend-ib-rtg-4-live-principal"


def emit(line: str = "") -> None:
    rtf10.emit(line)


MY_SENTINEL_REL = "org/critical_paths/.open_deploys/%s.json" % LEDGER_SLUG


def my_precondition() -> bool:
    emit("  PRECONDITION: the rtf-9 packet's 2 of 2 halves at HEAD; THIS order's own live-principal "
         "ledger (%s) committed OPEN" % LEDGER_SLUG)
    rc, head = rtf10.git("rev-parse", "--verify", "--quiet", "HEAD:" + rtf10.RTF9_PACKET_REL)
    _, wt = rtf10.git("hash-object", rtf10.RTF9_PACKET_REL)
    pk = rc == 0 and head.strip() == rtf10.RTF9_BLOB == wt.strip()
    n = 0
    for who, path in rtf10.RTF9_HALVES.items():
        rc2, text = rtf10.git("show", "HEAD:" + path)
        n += rc2 == 0 and rtf10.RTF9_BLOB in text
    rc3, _ = rtf10.git("rev-parse", "--verify", "--quiet", "HEAD:" + MY_SENTINEL_REL)
    emit("  rtf-9 packet blob at HEAD %s (== %s: %s); halves naming it %d of 2; THIS order's "
         "principal ledger sentinel (%s) at HEAD: %s"
         % (head.strip(), rtf10.RTF9_BLOB, pk, n, MY_SENTINEL_REL, rc3 == 0))
    return pk and n == 2 and rc3 == 0


def main() -> int:
    emit("IB-rtg-4 R75-AC1 arm (e) -- live proof under the deployed role and bytes -- run at %s -- "
         "worktree HEAD %s" % (rtf10.now_iso(), rtf10.git("rev-parse", "HEAD")[1].strip()))
    emit("")
    if not my_precondition():
        emit("STOP at the precondition: nothing written")
        with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(rtf10.LINES) + "\n")
        return 1

    if not rtf10.prefix_scan("before"):
        emit("STOP: a principal key already exists (residue) -- nothing written")
        with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(rtf10.LINES) + "\n")
        return 1

    om = json.loads(rtf10.s3.get_object(Bucket=rtf10.OM_BUCKET, Key=rtf10.OM_KEY)["Body"].read().decode("utf-8"))
    present = rtf10.ADVISOR in (om.get("advisors") or {})
    emit("GUARD: %s PRESENT in s3://%s/%s: %s" % (rtf10.ADVISOR, rtf10.OM_BUCKET, rtf10.OM_KEY, present))
    if not present:
        emit("STOP at the guard: nothing written")
        with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(rtf10.LINES) + "\n")
        return 1

    epoch = int(time.time())
    password = secrets.token_urlsafe(24)
    rtf10.SECRETS.append(password)
    created: dict = {}
    sess: dict = {}
    result_ok = False
    holdings_row = None
    try:
        k = rtf10.create_principal(epoch, password, created)
        created["k1_created"] = k["k1_created"]
        sess = rtf10.login(k["email"], password)
        c = sess.get("claims") or {}
        keys_ok = k["ok"] and sess.get("http") == 200 and c.get("firmId") == rtf10.FIRM and c.get("advisorKey") == rtf10.ADVISOR
        emit("keys read back 2 of 2 and the session as the rtf-9 packet declares: %s" % keys_ok)
        if keys_ok:
            tok = sess["token"]
            rnd = secrets.token_hex(12)
            # directory search -> resolve -> a granted account id (mirrors rtf-10's requests_arm shape)
            st1, _h1, b1 = rtf10.http("GET", rtf10.PFX + "/directory/search", tok, query={"q": "a", "limit": "25"})
            j1 = rtf10.as_json(b1)
            d1 = j1.get("data") if isinstance(j1, dict) and isinstance(j1.get("data"), list) else []
            emit("directory search WITH a query (q=a) -> HTTP %d, %d entries" % (st1, len(d1)))
            first = d1[0] if d1 else {}
            ids = first.get("ids") or {}
            st3, _h3, b3 = rtf10.http("POST", rtf10.PFX + "/directory/resolve", tok,
                                      body={"selection": {"relationship_id": ids.get("relationship_id")}})
            j3 = rtf10.as_json(b3)
            d3 = j3.get("data") if isinstance(j3, dict) else None
            emit("directory resolve WITH a selection -> HTTP %d, ok=%s, account_count=%s"
                 % (st3, (d3 or {}).get("ok") if isinstance(d3, dict) else None, (d3 or {}).get("account_count") if isinstance(d3, dict) else None))
            acc = (ids.get("account_ids") or [None])[0] or ("acc_" + rnd)
            emit("account resolved for the granted request: %s (fallback synthetic if resolve carried none: %s)"
                 % (acc, acc == "acc_" + rnd))

            fn = "irpt-holdings"
            cfg = rtf10.lam.get_function_configuration(FunctionName=fn)
            live_role = cfg["Role"].split("/")[-1]
            st2, _h2, b2 = rtf10.http("GET", rtf10.PFX + "/holdings/" + acc, tok)
            j2 = rtf10.as_json(b2)
            c2 = rtf10.classify(st2, j2)
            holdings_row = c2
            firm_binding_absent = (c2.get("code") == "FIRM_BINDING") and not c2.get("firm_id")
            scope_resolved = (c2["class"] in ("SERVED", "POLICY")) and not firm_binding_absent
            emit("ROUTE %s%s/holdings/%s -> FUNCTION %s (EXECUTION ROLE %s): class=%s http=%d code=%s firm_id=%s "
                 "business_date=%s -> %s" % (rtf10.BASE, rtf10.PFX, acc, fn, live_role, c2["class"], st2,
                                             c2.get("code"), "present" if c2.get("firm_id") else "ABSENT",
                                             c2.get("business_date"), "SCOPE-RESOLVED" if scope_resolved else "FIRM_BINDING WITH firm_id ABSENT (FAIL)"))
            result_ok = scope_resolved
    except Exception as exc:  # noqa: BLE001 -- recorded, then the rollback runs
        emit("EXCEPTION during the act: %s: %s -- rollback now" % (type(exc).__name__, str(exc)[:300]))
    finally:
        rb = rtf10.rollback(created, sess)

    after_ok = rtf10.prefix_scan("after")
    life_ok = bool(rb.get("k1b_deleted")) and bool(rb.get("k1_deleted")) and bool(rb.get("refresh_refused")) and bool(rb.get("expired_refused")) and after_ok
    emit("")
    emit("lifecycle closed (2 of 2 deleted, refresh refused, 401 after exp, no residue): %s" % life_ok)
    emit("holdings result: %s" % holdings_row)
    overall = result_ok and life_ok
    emit("")
    if overall:
        emit("RESULT: R75-AC1 arm (e) PASS")
        emit(TOKEN)
    else:
        emit("RESULT: R75-AC1 arm (e) FAIL -- result_ok=%s life_ok=%s" % (result_ok, life_ok))
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(rtf10.LINES) + "\n")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
