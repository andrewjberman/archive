"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): counts how many of the thirteen CloudOps orders' proof instances the complete-flip gate's own
validator reads VALID. READ ONLY. Run from the repository root with a python that has jsonschema and referencing (not `-I`).

    python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/ar_proofs_valid.py

For each order it takes the instance named in the order's own text ("Instance at `<path>`") and the criterion ids of its `<criterion id=...>`
elements, runs `.tools/proof-of-spec-check.py <instance> <ids> --governing-order <order>` exactly as `to-pipeline-gate.py check_complete_flip` does,
and counts rc 0. Prints `AR-PROOFS-VALID <n> of <total>` and, for each order that is not VALID, one line `NOT-VALID <order id> <first violation>`.
ASCII only.
"""
import glob
import os
import re
import subprocess
import sys

ORDERS = ("APPLY-MODELGRANT", "APPLY-R34G", "APPLY-R34K", "APPLY-R34P", "APPLY-R34Q", "APPLY-R34S", "APPLY-R34T", "DELETE-7H-DLQ-MESSAGE",
          "DELETE-7I-DLQ-MESSAGE", "READ-RETENTION-CENSUS-R34Q", "READ-RETENTION-CENSUS", "RUN-FWD10-MULTICOMP-7J", "RUN-FWD10-MULTICOMP-7K",
          "RUN-FWD10-MULTICOMP-7M")
FOLDER = "org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/"


def main():
    valid, lines = 0, []
    for name in ORDERS:
        found = glob.glob(FOLDER + "IRPT_ANLREQ.TO-%s.*.md" % name)
        if not found:
            lines.append("NOT-VALID %s order file absent" % name)
            continue
        order = found[0].replace("\\", "/")
        text = open(order, encoding="utf-8").read()
        m = re.search(r"[Ii]nstance at `([^`]+)`", text)
        ids = ",".join(sorted(set(re.findall(r'<criterion id="([^"]+)"', text))))
        if not m or not os.path.isfile(m.group(1)):
            lines.append("NOT-VALID %s instance absent (%s)" % (name, m.group(1)[-70:] if m else "not named"))
            continue
        r = subprocess.run([sys.executable, ".tools/proof-of-spec-check.py", m.group(1), ids, "--governing-order", order], capture_output=True, text=True)
        if r.returncode == 0:
            valid += 1
        else:
            first = next((ln.strip()[:150] for ln in r.stdout.splitlines() if ln.strip().startswith("VIOLATION")), "rc=%d" % r.returncode)
            lines.append("NOT-VALID %s %s" % (name, first))
    print("AR-PROOFS-VALID %d of %d" % (valid, len(ORDERS)))
    for ln in lines:
        print(ln)
    sys.exit(0 if valid == len(ORDERS) else 1)


if __name__ == "__main__":
    main()
