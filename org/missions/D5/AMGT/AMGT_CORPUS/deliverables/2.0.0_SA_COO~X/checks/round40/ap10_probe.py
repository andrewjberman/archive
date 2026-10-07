"""AMGT_CORPUS round 40, CRPS-ap-10 (m) -- the ONE-NAME probe of the six consensus-dispersion mnemonics.

Authority: 1.0.0_SA_CTO~Z msg 30490 ("Probe ONE name first (the field exists and is entitled), then let the daily fire carry
them. No one-off pull.") under ANDREW_DIRECT_20261006_201xZ (research is outside the Bloomberg no-modify order).

Read-only against the local Terminal (127.0.0.1:8194). ONE security, THREE ReferenceDataRequests (one per forecast override,
the same three requests the daily pull makes per name). It writes NO S3 object and NO served key; its only output is the
printed table and the JSON evidence file named on the command line.

  python ap10_probe.py "<security>" <evidence.json>

Per override it prints, for each field: its value, or its field error (category/subcategory/message). The two spellings of the
standard deviation are requested side by side so an invalid name reads INVALID, not absent.
"""
import json
import sys

import blpapi

SIX = ["BEST_CPS_STANDARD_DEV", "BEST_CPS_AVG", "BEST_CPS_NUMEST", "BEST_EPS_STANDARD_DEV", "BEST_EPS_AVG", "BEST_EPS_NUMEST"]
CONTROLS = ["BEST_CPS", "BEST_EPS", "BEST_PERIOD_END_DATE"]
OTHER_SPELLINGS = ["BEST_CPS_STDDEV", "BEST_EPS_STDDEV"]
FIELDS = SIX + CONTROLS + OTHER_SPELLINGS
OVERRIDES = ["1FY", "2FY", "3FY"]


def one_request(sess, svc, security, override):
    req = svc.createRequest("ReferenceDataRequest")
    req.append("securities", security)
    for f in FIELDS:
        req.append("fields", f)
    o = req.getElement("overrides").appendElement()
    o.setElement("fieldId", "BEST_FPERIOD_OVERRIDE")
    o.setElement("value", override)
    sess.sendRequest(req)
    values, errors, security_error = {}, {}, None
    for _tick in range(600):
        ev = sess.nextEvent(60000)
        for msg in ev:
            if not msg.hasElement("securityData"):
                continue
            sd = msg.getElement("securityData")
            for i in range(sd.numValues()):
                e = sd.getValueAsElement(i)
                if e.hasElement("securityError"):
                    security_error = e.getElement("securityError").getElementAsString("message")
                fd = e.getElement("fieldData")
                for j in range(fd.numElements()):
                    el = fd.getElement(j)
                    values[str(el.name())] = el.getValue()
                if e.hasElement("fieldExceptions"):
                    fx = e.getElement("fieldExceptions")
                    for j in range(fx.numValues()):
                        x = fx.getValueAsElement(j)
                        info = x.getElement("errorInfo")
                        errors[x.getElementAsString("fieldId")] = "%s/%s: %s" % (
                            info.getElementAsString("category"), info.getElementAsString("subcategory"),
                            info.getElementAsString("message"))
        if ev.eventType() in (blpapi.Event.RESPONSE, blpapi.Event.TIMEOUT):
            break
    return values, errors, security_error


def main(argv):
    security, out_path = argv[1], argv[2]
    opts = blpapi.SessionOptions()
    opts.setServerHost("127.0.0.1")
    opts.setServerPort(8194)
    sess = blpapi.Session(opts)
    if not sess.start() or not sess.openService("//blp/refdata"):
        print("ERROR: no Bloomberg session on 127.0.0.1:8194")
        return 4
    svc = sess.getService("//blp/refdata")
    record = {"security": security, "fields": FIELDS, "overrides": {}, "calls": 0}
    for override in OVERRIDES:
        values, errors, security_error = one_request(sess, svc, security, override)
        record["calls"] += 1
        record["overrides"][override] = {"values": {k: str(v) for k, v in values.items()}, "errors": errors,
                                         "security_error": security_error}
        print("override %s security_error %s" % (override, security_error))
        for f in FIELDS:
            state = "VALUE %s" % values[f] if f in values else ("ERROR %s" % errors[f] if f in errors else "NO VALUE, NO ERROR")
            print("   %-24s %s" % (f, state))
    sess.stop()
    returned = [f for f in SIX if all(f in record["overrides"][o]["values"] for o in OVERRIDES)]
    refused = [f for f in SIX if any(f in record["overrides"][o]["errors"] for o in OVERRIDES)]
    print("probe security %s calls %d six_returned_on_every_override %d of 6 six_with_a_field_error %d of 6" % (
        security, record["calls"], len(returned), len(refused)))
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(record, handle, indent=1)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
