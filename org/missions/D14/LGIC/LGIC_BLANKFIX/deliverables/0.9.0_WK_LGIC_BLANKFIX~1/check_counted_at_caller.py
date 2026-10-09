"""BX5-AC2: run the `all` command once; module-input residuals read COUNTED-AT-CALLER; uncounted keeps only the rest."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *[".."] * 7))
sys.path.insert(0, os.path.join(ROOT, "lib"))
os.chdir(ROOT)
import opal_naming_rootcheck as rc  # noqa: E402

BEFORE = ("org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/2.0.0_SA_COO~B1/ALL_ROOTS_round9_base.txt")
MAP = "infra/logic/registry/root_map.json"


def field(line, name):
    m = re.search(r" %s=(\d+)" % name, line)
    return int(m.group(1)) if m else None


def main():
    with io.open(BEFORE, encoding="utf-8") as fh:
        base = fh.read().splitlines()
    bl = [x for x in base if x.startswith("ALL-ROOTS ")][-1]
    before = field(bl, "uncounted")
    base_unc = [x for x in base if x.startswith("UNCOUNTED ")]
    buf = []
    rc.all_roots(MAP, out=buf.append)
    al = [x for x in buf if x.startswith("ALL-ROOTS ")][-1]
    after, caller = field(al, "uncounted"), field(al, "counted_at_caller")
    printed_unc = [x for x in buf if x.startswith("UNCOUNTED ")]
    printed_cac = [x for x in buf if x.startswith("COUNTED-AT-CALLER ")]
    other = len(printed_unc)
    ok = after is not None and caller is not None and after == other and caller == len(printed_cac)
    if before is None or caller is None:
        ok = False
    elif caller + after != before:
        # names moved: list the sites that differ from the base, still require uncounted_after == other_reasons
        def sites(ls):
            return set(re.search(r"\[(.*)\]$", x).group(1) for x in ls if x.endswith("]"))

        moved = sorted(sites(printed_cac + printed_unc) ^ sites(base_unc))
        print("MOVED sites (base vs now): %s" % (moved,))
    for x in printed_cac:
        print(x)
    for x in printed_unc:
        print(x)
    print("CALLER-COUNT ok=%s uncounted_before=%s uncounted_after=%s counted_at_caller=%s other_reasons=%d"
          % (ok, before, after, caller, other))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
