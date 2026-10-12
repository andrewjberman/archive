"""reads8_check.py -- the one mechanical check of IRPT_ANLREQ.TO-READS-Y8 (arm F2: the original-file route's owner check, live, read-only).

Usage:  python reads8_check.py [--root <repo root>]

Prints READS8-OK when the result file is complete, its verdict follows from its arms by the rule below, and it holds no request id,
ticket id, address or link; otherwise one FAIL line per problem and READS8-FAIL. It grades the record's FORM and the verdict's
logic; it cannot see the function or the table.

The rule (CTO msg 6541): the control (a caller the rule admits for the record's firm) gets the signed link's PRESENCE; arm (b) is
refused NOT_AUTHORIZED. Control present (the link's presence; AMENDMENT 1: not an `ok` member) and (b) NOT_AUTHORIZED = OWNER_SCOPED_REFUSAL. Control refused = UNEXERCISED_LIVE. Anything
else = ANOMALY, which is a finding, not a pass.
"""
import json
import re
import sys
from pathlib import Path

RESULT = "org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/F2_original_route_owner_check.json"
ARMS = ("control", "b", "a", "b_absent_id")
FORBIDDEN = (r"REQ-[0-9a-f]{24}", r"TCK-\d{8}-[0-9a-f]{8}", r"@", r"https?://", r"X-Amz", r"[0-9a-f]{40,}")
VERDICTS = ("OWNER_SCOPED_REFUSAL", "UNEXERCISED_LIVE", "ANOMALY")


def control_served(control):
    """AMENDMENT 1 (issuer, after the first run): the control is SERVED when the signed link is PRESENT and no refusal code came back --
    the CTO's rule (msg 6541) is the link's presence. A served envelope carries no `ok` member (the first run read `ok` as absent while
    the link, expiry, hash and length were all present), so `ok` is not the test; an explicit `ok: false` still means refused."""
    return control.get("url_present") is True and control.get("public_reason_code") is None and control.get("ok") is not False


def expected_verdict(arms):
    control, arm_b = arms["control"], arms["b"]
    if not control_served(control):
        return "UNEXERCISED_LIVE"
    if arm_b.get("ok") is False and arm_b.get("public_reason_code") == "NOT_AUTHORIZED":
        return "OWNER_SCOPED_REFUSAL"
    return "ANOMALY"


def main(argv):
    root = Path(argv[argv.index("--root") + 1]) if "--root" in argv else Path(__file__).resolve().parents[9]
    problems = []
    if not (root / ".tools").is_dir():
        problems.append("root %s is not the repository root" % root)
    path = root / RESULT
    if not path.is_file():
        problems.append("no %s" % RESULT)
    else:
        doc = json.loads(path.read_text(encoding="utf-8"))
        arms = doc.get("arms") or {}
        if doc.get("control_log_check") not in ("CLEAN", "NOT_READ", "LINK_IN_LOG"):
            problems.append("control_log_check must be CLEAN, NOT_READ or LINK_IN_LOG")
        if doc.get("control_log_check") == "LINK_IN_LOG":
            # the run ended at the control: no other arm ran, and the verdict is ANOMALY
            if doc.get("verdict") != "ANOMALY" or set(arms) - {"control"}:
                problems.append("LINK_IN_LOG ends the run at the control: verdict ANOMALY and no other arm")
            arms = {}
        for arm in ARMS if arms else ():
            if arm not in arms:
                problems.append("arms lacks %r" % arm)
        if arms and all(arm in arms for arm in ARMS):
            if arms["a"].get("public_reason_code") != "FIRM_BINDING" and doc.get("verdict") == "OWNER_SCOPED_REFUSAL":
                problems.append("arm a was not refused FIRM_BINDING; the fence arm must be explained, not passed over")
            if doc.get("verdict") not in VERDICTS:
                problems.append("verdict %r is not one of %s" % (doc.get("verdict"), VERDICTS))
            elif doc["verdict"] != expected_verdict(arms):
                problems.append("verdict %s does not follow from the arms (the rule gives %s)" % (doc["verdict"], expected_verdict(arms)))
            for arm in ("b", "a", "b_absent_id"):
                if "url_present" in arms[arm] and arms[arm]["url_present"]:
                    problems.append("arm %s was served a link; that is a finding and the verdict must be ANOMALY" % arm)
            print("verdict %s: control ok=%s url_present=%s; b=%s; a=%s; b_absent_id=%s" % (
                doc.get("verdict"), arms["control"].get("ok"), arms["control"].get("url_present"),
                arms["b"].get("public_reason_code"), arms["a"].get("public_reason_code"), arms["b_absent_id"].get("public_reason_code")))
        tie = doc.get("tie") or {}
        if not tie.get("code_sha256") or tie.get("tied_to") in (None, ""):
            problems.append("tie lacks code_sha256 or tied_to (write UNTIED if no source ties it; never leave it blank)")
        for key in ("read_at", "tenant", "identity_arn_tail", "ledger_open_entries_naming_irpt_status", "control_log_check"):
            if key not in doc:
                problems.append("the result lacks %r" % key)
        if doc.get("claim") != "measured":
            problems.append("claim is not measured")
        if doc.get("writes_made") != []:
            problems.append("writes_made must be an empty list")
        body = json.dumps({key: value for key, value in doc.items() if key != "tie"})
        for pattern in FORBIDDEN:
            if re.search(pattern, body):
                problems.append("the result holds a string matching %s (an id, an address or a link)" % pattern)
    for problem in problems:
        print("FAIL: %s" % problem)
    print("READS8-%s" % ("FAIL" if problems else "OK"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
