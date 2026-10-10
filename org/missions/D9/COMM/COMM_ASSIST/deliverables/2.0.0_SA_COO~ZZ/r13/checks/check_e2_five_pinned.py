"""COMM_ASSIST round 13, criterion CAe2-AC1 (issuer's check; the worker reads it and never edits it).

firm_domains() is pinned to C-MAIL's five parties. The five are named here literally, by PARTY KEY (never a domain string):
cottonwood, inflection, 49financial, alongside, opal. A synthetic registry carries the five plus a SIXTH client firm that has
a tenant email domain; the pinned function returns the five and not the sixth. Control: the live registry's keys are a subset
of the five. Domains in the synthetic registry are fixtures under the reserved .test TLD.

    python org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~ZZ/r13/checks/check_e2_five_pinned.py

LAST line: `E2-FIVE ok=<True|False>`. At the base (before the pin) the sixth firm is returned, so it prints ok=False.
"""
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * 9)))
sys.path.insert(0, ROOT)
from data.transcripts.scripts.teams_chat import mail_requests as m  # noqa: E402

FIVE = {"cottonwood", "inflection", "49financial", "alongside", "opal"}
SIXTH = "sixthfirm"


def _firm(key):
    return {"key": key, "class": "FIRM", "tenant": {"kind": "client", "email_domain": key + ".test"}}


def _party(key):
    return {"party": key, "considered": True, "email_domains": [{"domain": key + ".test", "claim": "measured"}]}


def main():
    reg = {"scopes": {"scopes": [_firm("cottonwood"), _firm("inflection"), _firm("49financial"), _firm(SIXTH)]},
           "mail_parties": {"mail_parties": [_party("alongside"), _party("opal")]}}
    got = set(m.firm_domains(reg))
    synthetic_ok = got == FIVE
    print("ARM synthetic keys=%s sixth_present=%s ok=%s" % (sorted(got), SIXTH in got, synthetic_ok))
    live = set(m.firm_domains())
    live_ok = live <= FIVE
    print("ARM live_subset keys=%s ok=%s" % (sorted(live), live_ok))
    print("E2-FIVE ok=%s" % (synthetic_ok and live_ok))


if __name__ == "__main__":
    main()
