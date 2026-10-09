"""BX1-AC2: run the `all` command once; every OWNED name of HOLES_OWNED_round8.md must read NOT-ASKED; hole must fall."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *[".."] * 7))
sys.path.insert(0, os.path.join(ROOT, "lib"))
os.chdir(ROOT)
import opal_naming_rootcheck as rc  # noqa: E402

D = "org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/"
OWNED = D + "0.9.0_WK_LGIC_BLANKFIX~4/HOLES_OWNED_round8.md"
BEFORE = D + "2.0.0_SA_COO~B1/ALL_ROOTS_round9_base.txt"
MAP = "infra/logic/registry/root_map.json"


def rd(p):
    with io.open(p, encoding="utf-8") as fh:
        return fh.read().splitlines()


def main():
    owned = []
    for ln in rd(OWNED):
        if ln.startswith("OWNED "):
            root, typ_name = [x.strip() for x in ln[6:].split("||")[:2]]
            typ, name = typ_name.split(" ", 1)
            owned.append((root, typ, name))
    before = [ln for ln in rd(BEFORE) if ln.startswith("ALL-ROOTS ")][-1]
    hole_before = int(re.search(r" hole=(\d+)", before).group(1))
    seen = {}

    def run_one(key, map_path, out=print, report_only=False, **kw):
        buf = []
        try:
            return rc.check_root(key, map_path, out=buf.append, report_only=report_only, **kw)
        finally:
            seen[key] = list(buf)
            for b in buf:
                out(b)

    final = []
    rc.all_roots(MAP, out=final.append, run_one=run_one)
    last = [x for x in final if x.startswith("ALL-ROOTS ")][-1]
    hole_after = int(re.search(r" hole=(\d+)", last).group(1))
    mapped = int(re.search(r" mapped=(\d+)", last).group(1))
    not_asked = 0
    for root, typ, name in owned:
        kinds = []
        for key, lines in seen.items():
            if key.rstrip("/").split("infra/aws/terraform/")[-1] != root:
                continue
            for b in lines:
                m = re.match(r"(\S+) (\S+) (.+?) -> ", b)
                if m and m.group(2) == typ and m.group(3) == name:
                    kinds.append(m.group(1))
        kind = kinds[0] if kinds and len(set(kinds)) == 1 else ("NOT-FOUND" if not kinds else "MIXED:" + ",".join(kinds))
        if kind == "NOT-ASKED":
            not_asked += 1
        print("%s %s %s -> %s" % (root, typ, name, kind))
    ok = bool(owned) and not_asked == len(owned) and hole_after < hole_before
    print("H8-RULE ok=%s owned=%d not_asked=%d hole_before=%d hole_after=%d mapped=%d"
          % (ok, len(owned), not_asked, hole_before, hole_after, mapped))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
