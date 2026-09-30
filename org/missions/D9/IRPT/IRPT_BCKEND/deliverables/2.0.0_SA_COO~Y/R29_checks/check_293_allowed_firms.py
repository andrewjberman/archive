#!/usr/bin/env python3
"""IB-yr-293 AC1 -- decide() refuses a data_firm outside the row's allowedFirmIds by a NAMED code.

Five cases against `current_authority.decide`, all offline (a dict row, no SDK):
  1. opal-capital / admin / allowedFirmIds "cottonwood", data_firm inflection  -> ACTOR_FIRM_NOT_ALLOWED
  2. same row, data_firm cottonwood                                             -> ALLOWED, scope OPAL_GLOBAL,
                                                                                  evidence.allowed_firm_ids == ["cottonwood"]
  3. allowedFirmIds "ALL", data_firm inflection                                 -> ALLOWED (ALL is unrestricted)
  4. NO allowedFirmIds attribute, data_firm inflection                          -> ALLOWED, evidence.allowed_firm_ids_absent True
                                                                                  (every existing principal keeps its behaviour)
  5. list form ["cottonwood", "49financial"], data_firm 49financial             -> ALLOWED
PASS iff all five. Base run (CLOUD HEAD before the cut): FAIL on case 1 (ALLOWED, the row is not read).
Issuer 2.0.0_SA_COO~Y, round 29. ASCII only.
"""
import os
import sys

ROOT = str(__import__("pathlib").Path(__file__).resolve().parents[8])  # parents[0] is R29_checks itself; the repo root is parents[8]
sys.path.insert(0, os.path.join(ROOT, "infra", "aws", "lambda", "investor-reporting", "ycharts", "generate"))

from current_authority import CurrentAuthorityRefused, decide  # noqa: E402

RECORD = {"owner": {"principal_id": "svc-irpt-analysis@opalinvest.com", "home_firm_id": "opal-capital",
                    "firm_id": "cottonwood"}, "accepted_at": 1790121600}
NOW = 1790121601


def row(**extra):
    base = {"email": "svc-irpt-analysis@opalinvest.com", "firmId": "opal-capital", "status": "active",
            "role": "admin", "userType": "service", "createdAt": "2026-09-20T00:00:00Z"}  # born BEFORE accepted_at
    base.update(extra)
    return base


def outcome(user, data_firm):
    try:
        ev = decide(user, RECORD, data_firm=data_firm, now=NOW, phase="start")
        return "ALLOWED", ev
    except CurrentAuthorityRefused as exc:
        return str(exc), exc.evidence


def main():
    results = []
    d, ev = outcome(row(allowedFirmIds="cottonwood"), "inflection")
    results.append(("1 restricted row, foreign firm", d == "ACTOR_FIRM_NOT_ALLOWED", d))
    d, ev = outcome(row(allowedFirmIds="cottonwood"), "cottonwood")
    results.append(("2 restricted row, allowed firm", d == "ALLOWED" and ev.get("scope") == "OPAL_GLOBAL"
                    and ev.get("allowed_firm_ids") == ["cottonwood"], d))
    d, ev = outcome(row(allowedFirmIds="ALL"), "inflection")
    results.append(("3 ALL is unrestricted", d == "ALLOWED", d))
    d, ev = outcome(row(), "inflection")
    results.append(("4 absent attribute keeps today's behaviour", d == "ALLOWED"
                    and ev.get("allowed_firm_ids_absent") is True, d))
    d, ev = outcome(row(allowedFirmIds=["cottonwood", "49financial"]), "49financial")
    results.append(("5 list form", d == "ALLOWED", d))
    for name, ok, got in results:
        print(("PASS " if ok else "FAIL ") + name + " -> " + got)
    n = sum(1 for _, ok, _ in results if ok)
    print("%d of %d cases hold" % (n, len(results)))
    if n == len(results):
        print("PASS: all five allowed-firm cases hold")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
