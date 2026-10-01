"""HVST-ae-5 AC2 (issuer, read-only): the unattended challenge run's record (FWD-11 DONE WHEN, the challenge half).

Reads `~91/ae5_unattended_run.json`, the record the worker's WORLD phase writes:
{"started_at", "host", "publishers": {"<pub>": {"challenge_met": <signature or "none">, "path": <solver or "none">,
 "passed": bool, "session_source": <profile path>, "operator_input_detected": bool, "articles_collected": int,
 "validation_security": <key>}}}

PASS requires, for EACH of bbg, wsj and barrons:
- `session_source` is the publisher's persistent profile (contains `/<pub>` or `\\<pub>`);
- `operator_input_detected` is false (no human hand: verification.last_operator_input unchanged);
- `passed` is true and `articles_collected` >= 1;
- where `challenge_met` is not "none", `path` names the solver that passed it.
A publisher that met no challenge and collected passes this criterion; the record says so.
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
RECORD = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~91/ae5_unattended_run.json")
PUBS = ("bbg", "wsj", "barrons")


def main():
    failures = []
    if not os.path.exists(RECORD):
        print("RECORD: absent (%s)" % RECORD)
        print("AC2 RESULT: FAIL (1 failure(s))")
        print("  FAIL: no unattended run record")
        return 1
    rec = json.load(open(RECORD, encoding="utf-8"))
    print("RUN: started_at %s host %s" % (rec.get("started_at"), rec.get("host")))
    for pub in PUBS:
        p = (rec.get("publishers") or {}).get(pub)
        if not p:
            failures.append("%s: no entry" % pub)
            continue
        print("  %-8s challenge=%s path=%s passed=%s source=%s operator_input=%s articles=%s"
              % (pub, p.get("challenge_met"), p.get("path"), p.get("passed"), p.get("session_source"),
                 p.get("operator_input_detected"), p.get("articles_collected")))
        src = str(p.get("session_source") or "").replace("\\", "/")
        if "/" + pub not in src:
            failures.append("%s: session source is not its persistent profile" % pub)
        if p.get("operator_input_detected") is not False:
            failures.append("%s: operator input detected or unrecorded" % pub)
        if p.get("passed") is not True or int(p.get("articles_collected") or 0) < 1:
            failures.append("%s: did not pass and collect" % pub)
        if str(p.get("challenge_met")) not in ("none", "None") and str(p.get("path")) in ("", "none", "None"):
            failures.append("%s: a challenge was met but no solver path is named" % pub)
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
