"""runys1_check.py -- the one mechanical check of IRPT_ANLREQ.TO-RUN-YS1 (the ONE synthetic cottonwood analysis request naming a ticket).

Usage:  python runys1_check.py [--root <repo root>]

Prints RUNYS1-OK when the result file is complete and consistent, and holds no address or link; otherwise one FAIL line per problem and
RUNYS1-FAIL. It grades the record's FORM and its internal consistency; it cannot see the store.

A result is ACCEPTED (the request id is REQ- plus 24 hex characters, the input id is portfolio_ plus 64 hex) or STOPPED (a named reason, no
request id). Either is a valid record; only ACCEPTED lets the draft proceed.
"""
import json
import re
import sys
from pathlib import Path

RESULT = "org/tier2_senior/0.7.0_AE_CloudOps~AR2/deliverables/SUBMIT_RUN_RESULT.json"
TICKET = "TCK-20261012-13cd3a1d"
MEMBERS = ("ran_at", "tenant", "ticket_id", "passes", "final", "filer_row_admits_cottonwood", "advisor_domain_class",
           "identity_arn_tail", "literal_keys_created", "writes_made", "claim", "not_read")
FORBIDDEN = (r"@", r"https?://", r"X-Amz")


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
        for member in MEMBERS:
            if member not in doc:
                problems.append("the result lacks %r" % member)
        if doc.get("tenant") != "cottonwood":
            problems.append("tenant is not cottonwood")
        if doc.get("ticket_id") != TICKET:
            problems.append("ticket_id is not the one V2 filed")
        if doc.get("claim") != "measured":
            problems.append("claim is not measured")
        # AMENDMENT 1 (issuer, after the first stop): a STOPPED run may report none_found or not_reached; only an ACCEPTED run proves 'reserved'.
        if doc.get("advisor_domain_class") not in ("reserved", "none_found", "not_reached"):
            problems.append("advisor_domain_class must be reserved, none_found or not_reached")
        if str(doc.get("final", "")) == "ACCEPTED" and doc.get("advisor_domain_class") != "reserved":
            problems.append("an ACCEPTED run must have advisor_domain_class 'reserved'")
        passes = doc.get("passes") or []
        if len(passes) > 8 or (not passes and str(doc.get("final", "")) == "ACCEPTED"):
            problems.append("passes must hold 1 to 8 entries when ACCEPTED (a STOPPED run before any invoke holds 0)")
        final = str(doc.get("final", ""))
        ids = doc.get("ids") or {}
        if final == "ACCEPTED":
            if not re.fullmatch(r"REQ-[0-9a-f]{24}", str(ids.get("request_id", ""))):
                problems.append("ACCEPTED needs ids.request_id of the form REQ-<24 hex>")
            if not re.fullmatch(r"portfolio_[0-9a-f]{64}", str(ids.get("input_id", ""))):
                problems.append("ACCEPTED needs ids.input_id of the form portfolio_<64 hex>")
            if not ids.get("upload_id"):
                problems.append("ACCEPTED needs ids.upload_id")
            if not doc.get("literal_keys_created"):
                problems.append("ACCEPTED needs literal_keys_created, the kinds and ids the door wrote")
        elif final.startswith("STOPPED:") and len(final) > len("STOPPED:"):
            if ids.get("request_id"):
                problems.append("a STOPPED result must not carry a request id")
        else:
            problems.append("final must be ACCEPTED or 'STOPPED: <reason>'")
        body = json.dumps(doc)
        for pattern in FORBIDDEN:
            if re.search(pattern, body):
                problems.append("the result holds a string matching %s (an address or a link)" % pattern)
        print("final %s; passes %d; filer row admits cottonwood: %s" % (final, len(passes), doc.get("filer_row_admits_cottonwood")))
    for problem in problems:
        print("FAIL: %s" % problem)
    print("RUNYS1-%s" % ("FAIL" if problems else "OK"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
