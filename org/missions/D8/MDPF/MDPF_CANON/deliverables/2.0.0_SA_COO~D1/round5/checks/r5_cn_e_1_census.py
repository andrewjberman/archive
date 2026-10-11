"""MDPF_CANON round 5, cell CN-e-1, criterion AC3 -- the reader census's row for the aum-timeseries instrument names the gold tier
and cites lines that resolve in the repointed script (the declarative arm the CVO graded NOT MET on CN-d-4, closed here by construction).

One command, four arms; prints `ROUND 5 CENSUS: k of 4 arms` and exits 0 only on all four.
Root = $R4_ROOT, else `git rev-parse --show-toplevel`.

  C1 no census row that names dim_mdpf_aum_timeseries.py also carries the staging-tree text `gold/mdpf_revamp/` (with the slash)
  C2 every `data/mdpf/scripts/gold/dim_mdpf_aum_timeseries.py:<n>` citation in the census resolves to a line of the script that
     contains `partition_uri(`, `def latest_gold_aggregate` or `SERVED_KEY` (the second row that names the
     script is the served-key verify instrument, whose cite must follow its line)
  C3 the script is cited at least twice (the loader and its read), and at least one citation line is `def latest_gold_aggregate`
  C4 (control) the row for dim_mdpf_aum_metrics.py still carries `gold/mdpf_revamp/`: that writer is not this cell's and must stay listed
"""
import os
import re
import subprocess
import sys

CENSUS = "org/missions/D8/MDPF/MDPF_CANON/deliverables/0.9.0_WK_MDPF_CANON~4/READER_CENSUS.md"
AUDIT = "data/mdpf/scripts/gold/dim_mdpf_aum_timeseries.py"
TOKENS = ("partition_uri(", "def latest_gold_aggregate", "SERVED_KEY")


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
        print("ROUND 5 CENSUS: 0 of 4 arms")
        return 1
    rows = [ln for ln in open(cp, encoding="utf-8").read().splitlines() if ln.startswith("|")]
    audit_lines = open(ap, encoding="utf-8").read().splitlines()
    named = [r for r in rows if "dim_mdpf_aum_timeseries.py" in r]
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

    has_read = any(1 <= n <= len(audit_lines) and "def latest_gold_aggregate" in audit_lines[n - 1] for n in cites)
    ok = len(cites) >= 2 and has_read
    print("  C3 %s: citations %d, one on def latest_gold_aggregate %s" % ("PASS" if ok else "FAIL", len(cites), "yes" if has_read else "no"))
    arms.append(ok)

    ok = any("dim_mdpf_aum_metrics.py" in r and "gold/mdpf_revamp/" in r for r in rows)
    print("  C4 %s: dim_mdpf_aum_metrics.py row %s" % ("PASS" if ok else "FAIL", "still listed with the staging tree" if ok else "missing or altered"))
    arms.append(ok)

    k = sum(1 for a in arms if a)
    print(f"ROUND 5 CENSUS: {k} of {len(arms)} arms")
    return 0 if k == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
