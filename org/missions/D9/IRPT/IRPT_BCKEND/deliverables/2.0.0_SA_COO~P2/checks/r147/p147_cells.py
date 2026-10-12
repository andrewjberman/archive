"""IRPT_BCKEND round 147 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY owner read by an applier:
  IB147-1  IB-pr-451  one owner read of a SERVED vendor report's sections, key names only: is there a title or label member, and
                      which unit tokens does it carry (CTO msg 5665, row DSGN_IRPTV1-D2-S21).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no record).
  IB147-1-AC1  how the vendor request was found is recorded (history reads, counts by provider and state) and exactly one outcome:
               READ (one request's sections read, http 200) or NO_VENDOR_REPORT_FOUND or REFUSED (with the code).
  IB147-1-AC2  on READ: the key sets of the answer, of a dated section and of an undated section; whether any section carries a
               title or label member; the distinct section_type and units tokens with counts summing to the sections counted.
  IB147-1-AC3  the bounds: GET only after the login, at most four GETs, nothing submitted, no value, no figure, no name of a
               person or account in the record.
"""
import json
import re
import sys
from pathlib import Path

OUT = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~IB2/IB147-1_vendor_sections_owner_read.json"
OUTCOMES = ("READ", "NO_VENDOR_REPORT_FOUND", "REFUSED")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB147"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    text = f.read_text(encoding="utf-8")
    a = json.loads(text)
    o = a.get("outcome")
    if o not in OUTCOMES:
        fail("outcome must be one of %s" % (OUTCOMES,))
    if cid == "IB147-1-AC1":
        h = a.get("history_reads")
        if not isinstance(h, list) or not h or any(not isinstance(x.get("http"), int) or not isinstance(x.get("requests_listed"), int)
                                                  or not isinstance(x.get("by_provider_and_state"), dict) for x in h):
            fail("history_reads must list each history GET with its http, requests_listed and by_provider_and_state")
        if not a.get("how_the_vendor_request_was_chosen"):
            fail("how_the_vendor_request_was_chosen is not stated")
        if o == "READ" and (a.get("sections_http") != 200 or not re.match(r"^REQ-[0-9a-f]{6,}", str(a.get("request") or ""))):
            fail("READ needs sections_http 200 and the request id")
        if o == "REFUSED" and not a.get("public_reason_code"):
            fail("REFUSED needs the public_reason_code")
        print("OK: %d history read(s); outcome %s" % (len(h), o))
    elif cid == "IB147-1-AC2":
        if o != "READ":
            print("OK: outcome %s; nothing to grade on the sections" % o)
        else:
            for k in ("answer_data_keys", "dated_section_keys", "undated_section_keys"):
                if not isinstance(a.get(k), list):
                    fail("%s is not a list of key names" % k)
            if not isinstance(a.get("any_section_has_a_title_or_label_member"), bool) or not isinstance(a.get("section_keys_union"), list):
                fail("any_section_has_a_title_or_label_member and section_keys_union must be stated")
            has = any(k in ("title", "label", "name", "display_name") for k in a["section_keys_union"])
            if a["any_section_has_a_title_or_label_member"] is not has:
                fail("any_section_has_a_title_or_label_member disagrees with section_keys_union")
            n = a.get("sections_counted")
            if not isinstance(n, int) or n != a.get("dated_sections", -1) + a.get("undated_sections", -1):
                fail("sections_counted must equal dated_sections + undated_sections")
            for k in ("section_type_tokens", "units_tokens"):
                d = a.get(k)
                if not isinstance(d, dict) or sum(d.values()) != n:
                    fail("%s must map each distinct token to its count, summing to sections_counted" % k)
            if not a.get("provider"):
                fail("provider is not stated")
            print("OK: %d section(s), provider %s; title or label member: %s; %d section_type token(s), %d units token(s)" % (
                n, a["provider"], a["any_section_has_a_title_or_label_member"], len(a["section_type_tokens"]), len(a["units_tokens"])))
    elif cid == "IB147-1-AC3":
        calls = a.get("calls")
        if not isinstance(calls, list) or not calls:
            fail("calls is empty")
        gets = [c for c in calls if c.get("method") == "GET"]
        other = [c for c in calls if c.get("method") != "GET" and c.get("path") != "/auth/login"]
        if other or len(gets) > 4:
            fail("only the login and at most four GETs are allowed; read %d GET(s), %d other call(s)" % (len(gets), len(other)))
        if a.get("submitted") != 0 or a.get("values_written") != 0:
            fail("submitted and values_written must be 0")
        if re.search(r"(?<![0-9A-Za-z])[0-9]{8}(?![0-9A-Za-z])", text) or re.search(r"\"value\"\s*:\s*-?[0-9]", text):
            fail("the record carries an eight-digit token or a numeric value member")
        if re.search(r"accessToken\"\s*:\s*\"(?!<redacted>)", text) or "Bearer ey" in text:
            fail("the record carries a token")
        print("OK: %d GET(s), 0 other calls after the login; nothing submitted; no value, token or account-id token in the record" % len(gets))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
