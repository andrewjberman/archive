"""MDPF_CANON round 4, cell CN-d-4 AMENDMENT 2, criterion AC4 -- the reader census's row for the count-source audit names the gold
tier and cites lines that resolve in the repointed audit (CVO's grade of AC3, NOT MET on the declarative arm).

One command, four arms; prints `ROUND 4 CENSUS: k of 4 arms` and exits 0 only on all four.
Root = $R4_ROOT, else `git rev-parse --show-toplevel`.

  C1 no census row that names mdpf_revamp_count_source_audit.py also carries the staging-tree text `gold/mdpf_revamp/` (with the slash: the audit's own path `gold/mdpf_revamp_count_source_audit.py` is not the tree)
  C2 every `data/mdpf/scripts/gold/mdpf_revamp_count_source_audit.py:<n>` citation in the census resolves to a line of the audit that
     contains `partition_uri(` or `latest_gold_artifact(` or `def unaudited_firms`
  C3 the audit is cited at least twice (a read and a caller), and at least one citation line contains `latest_gold_artifact(`
  C4 (control) a census row still names verify_mdpf_revamp_conditions.py together with `gold/mdpf_revamp/`: that reader was not
     examined by this round and must stay listed as it was
"""
import os
import re
import subprocess
import sys

CENSUS = "org/missions/D8/MDPF/MDPF_CANON/deliverables/0.9.0_WK_MDPF_CANON~4/READER_CENSUS.md"
AUDIT = "data/mdpf/scripts/gold/mdpf_revamp_count_source_audit.py"
TOKENS = ("partition_uri(", "latest_gold_artifact(", "def unaudited_firms")


def _root() -> str:
    r = os.environ.get("R4_ROOT")
    if r:
        return r
    return subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()


def main() -> int:
    root = _root()
    cp = os.path.join(root, *CENSUS.split("/"))
    ap = os.path.join(root, *AUDIT.split("/"))
    if not os.path.isfile(cp) or not os.path.isfile(ap):
        print("  census or audit file absent")
        print("ROUND 4 CENSUS: 0 of 4 arms")
        return 1
    rows = [ln for ln in open(cp, encoding="utf-8").read().splitlines() if ln.startswith("|")]
    audit_lines = open(ap, encoding="utf-8").read().splitlines()
    named = [r for r in rows if "mdpf_revamp_count_source_audit.py" in r]
    arms = []

    bad = [r[:90] for r in named if "gold/mdpf_revamp/" in r]
    ok = bool(named) and not bad
    print("  C1 %s: %d row(s) name the audit; %d of them still carry gold/mdpf_revamp/" % ("PASS" if ok else "FAIL", len(named), len(bad)))
    arms.append(ok)

    cites = []
    for r in named:
        cites += [int(n) for n in re.findall(re.escape(AUDIT) + r":(\d+)", r)]
    unresolved = []
    for n in cites:
        txt = audit_lines[n - 1] if 1 <= n <= len(audit_lines) else ""
        if not any(t in txt for t in TOKENS):
            unresolved.append(n)
    ok = bool(cites) and not unresolved
    print("  C2 %s: %d citation(s) of the audit; unresolved %s" % ("PASS" if ok else "FAIL", len(cites), unresolved if unresolved else "none"))
    arms.append(ok)

    has_read = any(1 <= n <= len(audit_lines) and "latest_gold_artifact(" in audit_lines[n - 1] for n in cites)
    ok = len(cites) >= 2 and has_read
    print("  C3 %s: citations %d, one on latest_gold_artifact( %s" % ("PASS" if ok else "FAIL", len(cites), "yes" if has_read else "no"))
    arms.append(ok)

    ok = any("verify_mdpf_revamp_conditions.py" in r and "gold/mdpf_revamp/" in r for r in rows)
    print("  C4 %s: verify_mdpf_revamp_conditions.py row %s" % ("PASS" if ok else "FAIL", "still listed with the staging tree" if ok else "missing or altered"))
    arms.append(ok)

    k = sum(1 for a in arms if a)
    print(f"ROUND 4 CENSUS: {k} of {len(arms)} arms")
    return 0 if k == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
