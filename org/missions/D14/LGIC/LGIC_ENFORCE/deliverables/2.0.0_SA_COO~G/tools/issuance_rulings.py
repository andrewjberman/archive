"""Issuance rulings check: before writing a <paths> block, read the rulings that touch it.

WHY THIS EXISTS, and it is one incident. RULING R-2 (2026-09-16 ~06:0xZ) measured 12
ownerless deliverables sitting directly under `deliverables/` with no serial folder, said
the shape was the defect, and ordered them moved. I then cut FOUR more cells in exactly
that shape -- EXERCISE_FWD7_R2.md, LIMB_ROOTS_CENSUS.md, REGISTRY_TOKEN_CLASSES.md,
RESOURCE_ROWS.md -- and the population went 12 -> 17. R-12 owned half of that (R-2 named a
round already closed) and endorsed this check as the issuer's own L6 build, with the
durable rule it carries:

    A RULING ABOUT A POPULATION BINDS THE NEXT CUT ONLY IF THE CUT READS IT.

WHAT IT DOES. Parses a rulings ledger into one block per `## R-<n>`, collects every repo
path each block names, and for a proposed or existing task order reports which rulings
touch any entry in its <paths> -- by exact path, or because a ruling names a DIRECTORY
that would contain it. It prints the ruling's headline so the issuer reads the thing
itself.

WHAT IT DOES NOT DO, stated because a check that hides its limits is worse than none:
  1. It does NOT decide whether a ruling is still open. It surfaces; the issuer reads.
     There is no machine-readable open/closed field in the ledger and inventing one from
     prose would be the "parsing prose reads the TOOL, not the world" failure.
  2. It does NOT understand what a ruling ORDERS. A ruling that merely mentions a path in
     passing looks identical here to one that orders it moved.
  3. It reads ONE ledger by default. The estate carries ~70 rulings files; pass --ledger
     to add others. A zero here is a zero over the ledgers READ, never over the estate.
  4. It is ADVISORY. It refuses nothing.
  5. CONTAINS OVER-FIRES ON A CROWDED DIRECTORY, and the real run shows it: checking
     `.tools/ds-precommit-check.py` surfaces R-1 (via `.tools/safe-merge.sh`) and R-11
     (via `.tools/naming-gate.py`) purely because all three are siblings in `.tools/`.
     Neither ruling is about that file. The rule is only as sharp as the directory is
     specific, so read CONTAINS hits on a shared directory as "go look", not "you are
     in breach". It is sharp exactly where R-2 was -- a project's own deliverables
     folder, where being a sibling IS the population.

MEASURED ON THE INCIDENT IT WAS BUILT FROM: run against EN-d-1's order it prints
    TOUCHED org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/EXERCISE_FWD7_R2.md
       R-2 [CONTAINS via .../FIRM_FORMS_READERS.md]
which is precisely the cut that should not have been written without reading R-2.

USAGE
    python <this> --order <path/to/TO.md>
    python <this> --paths infra/logic/x.md org/missions/.../deliverables/Y.md
    python <this> --order <TO> --ledger <a.md> --ledger <b.md>
    python <this> --selftest
"""

import argparse
import importlib.util
import io
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *([os.pardir] * 8)))

def _load(mod_name, rel):
    spec = importlib.util.spec_from_file_location(mod_name, os.path.join(REPO, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# REUSE, NOT REIMPLEMENT. My own <paths> pattern was `<paths>(.*?)</paths>` UNANCHORED,
# and a task order says "the `<paths>` block below" in its BOUNDS prose BEFORE the real
# block -- so .search() took the PROSE mention and swallowed the whole BOUNDS section as
# paths (21 "entries", most of them whole sentences). The estate already fixed exactly
# this on the surprise-row gate in 2026-09: anchor at line start. owned-paths-validate.py
# carries the anchored pattern and the grant grammar, so this imports it rather than
# keeping a second, worse copy. Found by running the tool on a REAL order; the selftest
# passed throughout, because its fixture had no prose mention.
_OPV = _load("opv", os.path.join(".tools", "owned-paths-validate.py"))

DEFAULT_LEDGER = os.path.join(
    "org", "tier1_exec", "1.0.0_SA_CTO", "deliverables",
    "SELF_DRIVE_LGIC_RULINGS_20260916.md")

_RULING_RE = re.compile(r"^##\s+(R-\d+)\b[^\n]*", re.M)
_PATH_RE = re.compile(
    r"(?<![\w/.-])((?:org|lib|infra|data|\.tools|docs|deck_generation|integrations)"
    r"/[\w./*?\[\]~-]+)")


def _norm(p):
    return p.replace("\\", "/").lstrip("/").rstrip(".,;`)")


def parse_ledger(text):
    """[(ruling_id, headline, {paths})] -- one entry per `## R-<n>` block."""
    out = []
    marks = list(_RULING_RE.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        block = text[m.start():end]
        headline = block.splitlines()[0].lstrip("#").strip()
        paths = {_norm(x) for x in _PATH_RE.findall(block)}
        out.append((m.group(1), headline, paths))
    return out


def order_paths(text):
    """The <paths> entries a task order declares -- the ESTATE'S parser, anchored."""
    return [_norm(e) for e in _OPV._paths_block_entries(text or "")]


def touches(entry, ruling_paths):
    """Why a ruling touches this entry, or None.

    EXACT      the ruling names this very path.
    CONTAINS   the ruling names a DIRECTORY that would contain it -- the population case,
               which is the one R-2 was and the one a per-file match would have missed.
    UNDER      the entry is a directory and the ruling names something inside it.
    """
    for rp in ruling_paths:
        if rp == entry:
            return ("EXACT", rp)
    ent_dir = entry if entry.endswith("/") else entry.rsplit("/", 1)[0] + "/"
    for rp in ruling_paths:
        rp_dir = rp if rp.endswith("/") else rp.rsplit("/", 1)[0] + "/"
        if rp_dir == ent_dir and rp != entry:
            return ("CONTAINS", rp)
        if entry.endswith("/") and rp.startswith(entry):
            return ("UNDER", rp)
    return None


def run(paths, ledgers):
    rulings = []
    for lg in ledgers:
        full = lg if os.path.isabs(lg) else os.path.join(REPO, lg)
        if not os.path.exists(full):
            print("LEDGER NOT FOUND, skipped: %s" % lg)
            continue
        rulings.extend(parse_ledger(io.open(full, encoding="utf-8", errors="replace").read()))
    print("rulings parsed: %d over %d ledger(s)" % (len(rulings), len(ledgers)))
    print("paths to check : %d" % len(paths))
    print("")
    hits = 0
    for entry in paths:
        found = []
        for rid, headline, rpaths in rulings:
            why = touches(entry, rpaths)
            if why:
                found.append((rid, headline, why))
        if not found:
            print("  clear   %s" % entry)
            continue
        hits += len(found)
        print("  TOUCHED %s" % entry)
        for rid, headline, (kind, rp) in found:
            print("     %-5s [%-8s via %s]" % (rid, kind, rp))
            print("           %s" % headline[:150])
    print("")
    print("RESULT: %d ruling-touch(es) over %d path(s)" % (hits, len(paths)))
    print("ADVISORY -- it does NOT say whether a ruling is still open, nor what it orders.")
    print("READ EACH RULING NAMED ABOVE BEFORE CUTTING THESE PATHS.")
    return 0


def selftest():
    ok = True
    led = (
        "# ledger\n"
        "## R-2 (2026) -- FIRM_FORMS_READERS.md is misplaced; fix the PLACEMENT\n"
        "The file `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/FIRM_FORMS_READERS.md`\n"
        "sits directly under deliverables/ with no serial folder.\n"
        "## R-9 (2026) -- the negative arm could not discriminate\n"
        "Nothing about placement here; it names `infra/logic/02_DOCTRINE.md`.\n")
    rs = parse_ledger(led)
    a1 = (len(rs) == 2 and rs[0][0] == "R-2")
    print("PARSE     two rulings, first is R-2: %s" % a1)
    ok = ok and a1

    ff = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/FIRM_FORMS_READERS.md"
    a2 = touches(ff, rs[0][2]) is not None and touches(ff, rs[0][2])[0] == "EXACT"
    print("EXACT     the named file is matched: %s" % a2)
    ok = ok and a2

    # THE POPULATION CASE: a NEW file, never named by any ruling, in the ruled directory.
    newf = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/LIMB_ROOTS_CENSUS.md"
    t = touches(newf, rs[0][2])
    a3 = t is not None and t[0] == "CONTAINS"
    print("CONTAINS  a NEW sibling in the ruled directory is caught: %s   <- the R-2 case" % a3)
    ok = ok and a3

    a4 = touches("infra/logic/02_DOCTRINE.md", rs[0][2]) is None
    print("NEGATIVE  an unrelated path is NOT matched by R-2: %s" % a4)
    ok = ok and a4

    a5 = touches("infra/logic/02_DOCTRINE.md", rs[1][2]) is not None
    print("POSITIVE  that path IS matched by the ruling that names it: %s" % a5)
    ok = ok and a5

    a6 = order_paths("<paths>\nlib/a.py\n# comment\n`org/b.md`\n</paths>") == ["lib/a.py", "org/b.md"]
    print("PATHS     block parsed, comment dropped, backticks stripped: %s" % a6)
    ok = ok and a6

    print("SELFTEST: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--order", help="a task order; its <paths> block is checked")
    ap.add_argument("--paths", nargs="*", default=[], help="explicit paths instead of an order")
    ap.add_argument("--ledger", action="append", default=[], help="repeatable; defaults to the LGIC ledger")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    ledgers = a.ledger or [DEFAULT_LEDGER]
    paths = [_norm(p) for p in a.paths]
    if a.order:
        full = a.order if os.path.isabs(a.order) else os.path.join(REPO, a.order)
        paths += order_paths(io.open(full, encoding="utf-8", errors="replace").read())
    if not paths:
        ap.error("give --order or --paths")
    return run(paths, ledgers)


if __name__ == "__main__":
    sys.exit(main())
