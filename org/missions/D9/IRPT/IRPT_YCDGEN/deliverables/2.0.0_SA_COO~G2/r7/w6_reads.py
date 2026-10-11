"""IRPT_YCDGEN served-read window 6: the read-only owner reads after the irpt-status rev 6 apply (TO-APPLY-Y1 AMENDMENT 8).

    python w6_reads.py R3 <out.json>                 # one owner GET of the history, svc on its native firm (cottonwood)
    python w6_reads.py R45 <request_id> <out.json>   # status-job + analysis-report sections + ONE GET .../original (49financial)
    python w6_reads.py R6 <request_id> <out.json>    # ONE status-job read with the portal's date opt-in header (49financial)

Reuses f1_svc_run.py's call() and scrub(): the password is read by NAME into memory and never printed or written; the record
keeps codes, ids and section names only. Submits nothing. ASCII only.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "f1_svc_release"))

import boto3  # noqa: E402
import f1_svc_run as f1  # noqa: E402


def login():
    password = boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(SecretId=f1.SECRET)["SecretString"]
    s, resp = f1.call("POST", "/auth/login", {"email": f1.EMAIL, "password": password}, {"Content-Type": "application/json"},
                      record_body={"email": "<svc>", "password": "<redacted>"})
    del password
    token = resp.get("accessToken") if isinstance(resp, dict) else None
    f1.say("login", s, "token present", bool(token))
    if not token:
        return None
    return {"Content-Type": "application/json", "Authorization": "Bearer " + token, "X-Contract-Version": "v1"}


def codes(resp):
    st = resp.get("status") if isinstance(resp, dict) else None
    st = st if isinstance(st, dict) else {}
    op = st.get("operation") if isinstance(st.get("operation"), dict) else {}
    return {"ok": resp.get("ok") if isinstance(resp, dict) else None, "operation_id": op.get("operation_id"),
            "state": st.get("state"), "public_reason_code": st.get("public_reason_code")}


def main(argv):
    mode = argv[1]
    out = argv[-1]
    result = {"mode": mode, "started_at": f1.stamp(), "api": f1.API}
    h = login()
    summary = []
    if h:
        if mode == "R3":
            q = "?selected_tenant=cottonwood"
            s, r = f1.call("GET", f1.BASE + "/analysis/requests" + q, None, h)
            summary.append(dict(read="R3 history", http=s, **codes(r)))
        elif mode == "R45":
            rid = argv[2]
            q = "?selected_tenant=49financial"
            result["request"] = rid
            for name, path in (("R4 status-job", "/status/" + rid + q),
                               ("R4 analysis-report sections", "/analysis/" + rid + "/sections" + q),
                               ("R5 original", "/analysis/requests/" + rid + "/original" + q)):
                s, r = f1.call("GET", f1.BASE + path, None, h)
                summary.append(dict(read=name, http=s, **codes(r)))
        elif mode == "R6":
            # CTO~DELL2 msg 4152: ONE status-job re-read WITH the portal's date opt-in (portal
            # contracts/prospect-dates.ts PROSPECT_DATE_HEADER; ops/entry.py job_status reads it).
            rid = argv[2]
            hh = dict(h)
            hh["X-IRPT-Status-Dates"] = "prospect-v1"
            s, r = f1.call("GET", f1.BASE + "/status/" + rid + "?selected_tenant=49financial", None, hh)
            d = r.get("data") if isinstance(r, dict) and isinstance(r.get("data"), dict) else {}
            summary.append(dict(read="R6 status-job with X-IRPT-Status-Dates", http=s, state=d.get("state"),
                                public_reason_code=d.get("public_reason_code"),
                                source_date_keys=sorted((d.get("source_dates") or {}).keys())))
        else:
            raise SystemExit("mode must be R3, R45 or R6")
    for row in summary:
        f1.say(json.dumps(row))
    result.update(ended_at=f1.stamp(), summary=summary, calls=f1.log)
    json.dump(result, open(out, "w", encoding="utf-8", newline="\n"), indent=1)
    return 0 if h else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
