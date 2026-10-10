"""COMM_ASSIST round 13, criterion CAe1-AC2 (issuer's check; the worker reads it and never edits it).

The driven mail's exact body (DRIVEN_BODY below, the text the sender is given) passes `mail_requests.considered()` as "ok"
when it arrives from an Opal sender, in BOTH shapes Graph can serve it: plain text, and HTML as Outlook wraps a typed body.
The sender address is built from the live domain table's own Opal entry; no domain is typed. Control: the same body with
the name removed is refused as body_no_andrew.

    python org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~ZZ/r13/checks/check_e1_body_considered.py

LAST line: `E1-BODY ok=<True|False>`. This is a BOUND: it is expected to PASS at the base. If it passes and the live route
still refuses the driven mail as body_no_andrew, the defect is in what the route serves as the body, not in the predicate.
"""
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * 9)))
sys.path.insert(0, ROOT)
from data.transcripts.scripts.teams_chat import mail_requests as m  # noqa: E402

DRIVEN_BODY = ("Andrew, this is a driven test of your mail assistant (COMM_ASSIST round 13, cell CA-e-1). "
               "Please ignore any draft it offers; no reply is needed.")
NAMELESS = DRIVEN_BODY.replace("Andrew, ", "")
HTML = ('<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body>'
        '<div class="elementToProof" style="font-family:Aptos; font-size:12pt">%s</div></body></html>')


def msg(addr, content, kind):
    return {"from": {"emailAddress": {"address": addr, "name": "Opal Sender"}},
            "body": {"contentType": kind, "content": content}}


def main():
    doms = m.firm_domains().get("opal") or []
    if not doms:
        print("ERROR: the live domain table has no opal entry")
        print("E1-BODY ok=False")
        return
    addr = "sender@" + doms[0]
    domains = m.firm_domains()
    text = m.considered(msg(addr, DRIVEN_BODY, "text"), domains)
    html = m.considered(msg(addr, HTML % DRIVEN_BODY, "html"), domains)
    ctl = m.considered(msg(addr, NAMELESS, "text"), domains)
    print("ARM text=%r html=%r control_nameless=%r" % (text, html, ctl))
    ok = text == (True, "ok") and html == (True, "ok") and ctl == (False, "body_no_andrew")
    print("E1-BODY ok=%s" % ok)


if __name__ == "__main__":
    main()
