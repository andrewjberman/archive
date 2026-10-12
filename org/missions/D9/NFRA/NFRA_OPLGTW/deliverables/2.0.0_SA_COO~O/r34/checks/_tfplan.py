"""Shared reader for a saved targeted Terraform plan plus its exit-code file (round-34 apply checks).

usage: python _tfplan.py <plan.txt> <plan.rc> <want_add> <want_change> <want_destroy> [address ...]
Prints one line and exits 0 only when: rc == 0; the summary reads exactly the wanted counts ("No changes." == 0/0/0);
and, when addresses are given, the set of '# <addr> will be ...' lines equals them. A summary at rc != 0 is not a verdict.
"""
import re
import sys


def main(argv):
    plan_p, rc_p = argv[1], argv[2]
    want = tuple(int(x) for x in argv[3:6])
    addrs_want = sorted(argv[6:])
    try:
        text = open(plan_p, encoding="utf-8", errors="replace").read().replace("\r", "")
        rc = open(rc_p, encoding="utf-8").read().strip()
    except OSError as exc:
        print("plan or rc file unreadable: %s" % exc)
        return 1
    m = re.findall(r"^Plan: (\d+) to add, (\d+) to change, (\d+) to destroy\.", text, re.M)
    got = tuple(int(x) for x in m[-1]) if m else ((0, 0, 0) if "No changes." in text else None)
    addrs = sorted(set(re.findall(r"^\s*# (\S+) will be ", text, re.M)))
    ok = rc == "0" and got == want and (not addrs_want or addrs == addrs_want)
    print("%s: rc=%s summary=%s (want %s) addresses %d %s" % (plan_p.replace("\\", "/").rsplit("/", 1)[-1], rc, got, want,
                                                                 len(addrs), addrs))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
