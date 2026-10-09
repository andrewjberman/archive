"""Issuer's check for COMM_ASSIST.TO-CA-d-1 (round 11): the two saved targeted plans of module.ldo_001 show that the mail-key
wiring is inert while its variable is empty and complete when it is set. Reads the worker's two plan texts (terraform plan
-no-color output); makes no AWS call. Last line: PLANS-CA-d-1 ok=<True|False>."""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *([os.pardir] * 8)))
DELIV = os.path.join(ROOT, "org", "missions", "D9", "COMM", "COMM_ASSIST", "deliverables", "0.9.0_WK_COMM_ASSIST~5")
FAKE = "arn:aws:secretsmanager:us-east-1:000000000000:secret:comm-assist-plan-probe"
HEADER = re.compile(r"^\s*# (\S+) (will be|must be)")
SUMMARY = re.compile(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy")


def read(name):
    path = os.path.join(DELIV, name)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def facts(text):
    heads = [m.group(1) for m in (HEADER.match(line) for line in text.splitlines()) if m]
    s = SUMMARY.search(text)
    return {
        "outside": [h for h in heads if not h.startswith("module.ldo_001.")],
        "add": int(s.group(1)) if s else None, "destroy": int(s.group(3)) if s else None,
        "mail_env": len(re.findall(r"MAIL_BEARER_SECRET", text)),
        "get_secret_on_fake": FAKE in text and "secretsmanager:GetSecretValue" in text,
        "fake": text.count(FAKE),
    }


def main() -> int:
    checks = []
    empty, setv = read("PLAN_EMPTY.txt"), read("PLAN_SET.txt")
    checks.append(("PLAN_EMPTY.txt present", empty is not None))
    checks.append(("PLAN_SET.txt present", setv is not None))
    if empty is not None:
        f = facts(empty)
        checks += [("empty: nothing outside module.ldo_001", not f["outside"]),
                   ("empty: 0 to add, 0 to destroy", f["add"] == 0 and f["destroy"] == 0),
                   ("empty: no MAIL_BEARER_SECRET", f["mail_env"] == 0),
                   ("empty: the probe ARN absent", f["fake"] == 0)]
    if setv is not None:
        f = facts(setv)
        checks += [("set: nothing outside module.ldo_001", not f["outside"]),
                   ("set: 0 to destroy", f["destroy"] == 0),
                   ("set: MAIL_BEARER_SECRET in both functions' environment", f["mail_env"] >= 2),
                   ("set: a read of the probe ARN granted", f["fake"] >= 1)]
    for name, ok in checks:
        print("CHECK %s ok=%s" % (name, ok))
    ok = all(v for _, v in checks)
    print("PLANS-CA-d-1 ok=%s" % ok)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
