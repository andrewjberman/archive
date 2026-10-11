"""ADVI_FIRMBKTS round 4 check for cell FB-g-9 (the ONE SEV1 test text, the CTO's ruling on call c290), issuer
2.0.0_SA_COO~B1.

Ruling (org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULINGS_CLUSTER_TICK12_20261011_1157Z.md @087b7ac3a1): exactly ONE
text, body "Opal test, no action", from the registered toll-free number straight to the on-call phone via the SMS send API
(NOT SNS), no retry; the message id, the status and the delivery log line are reported.

--file <record.json>  grades the actor's record (3 arms):
  M1 the record is JSON and carries message_id, origination_identity_kind, message_body, sent_count, retry_count,
     delivery_status, delivery_log_line and recorded_at, each non-empty (retry_count may be 0).
  M2 exactly one send: sent_count == 1, retry_count == 0, one message id, the body equals the ruled text, and the
     send path is the SMS send API (send_api reads 'pinpoint-sms-voice-v2' or 'sms-voice', never 'sns').
  M3 no phone number sits in the record: no run of 7 or more digits after a plus sign, nowhere in the file.
Plain ASCII output; the last line carries the arm count. Never edit this file.
"""
import argparse
import json
import re
import sys

BODY = "Opal test, no action"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    a = ap.parse_args()
    res = []
    try:
        raw = open(a.file, encoding="utf-8").read()
        d = json.loads(raw)
        need = ("message_id", "origination_identity_kind", "message_body", "send_api", "delivery_status",
                "delivery_log_line", "recorded_at")
        miss = [k for k in need if not str(d.get(k, "")).strip()]
        miss += [k for k in ("sent_count", "retry_count") if not isinstance(d.get(k), int)]
        print("  fields missing or empty: %s" % (miss or "none"))
        res.append(("M1 the record carries the id, identity kind, body, send api, status, delivery log line and time",
                    not miss))
        one = (d.get("sent_count") == 1 and d.get("retry_count") == 0 and d.get("message_body") == BODY
               and str(d.get("send_api", "")).lower() in ("pinpoint-sms-voice-v2", "sms-voice")
               and isinstance(d.get("message_id"), str) and "," not in d.get("message_id", ","))
        print("  sent_count=%r retry_count=%r body ok=%s send_api=%r" % (d.get("sent_count"), d.get("retry_count"),
                                                                        d.get("message_body") == BODY, d.get("send_api")))
        res.append(("M2 exactly one send of the ruled body through the SMS send API, no retry", one))
        digits = re.findall(r"\+\s*\d[\d\s().-]{6,}", raw)
        print("  phone-number-like strings in the record: %d" % len(digits))
        res.append(("M3 no phone number sits in the record", not digits))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s)" % (a.file, type(e).__name__))
        res = [("the record is present and JSON", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 SMS RECORD: %d of 3 arms" % n)
    sys.exit(0 if n == 3 else 1)


if __name__ == "__main__":
    main()
