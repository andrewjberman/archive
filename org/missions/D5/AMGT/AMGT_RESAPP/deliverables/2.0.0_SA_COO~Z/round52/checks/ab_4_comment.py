"""AMGT_RESAPP round 52, AMGT-ab-4 -- scoped_amgt.py's comments no longer claim `lib.opal_naming` is never imported at runtime
(CTO round-51 ruling 6; row Z-S307's class): the adapter imports it transitively (scoped_amgt -> corpus.dossier -> harvest.store ->
lib.opal_naming at module scope), at REQUEST time on the /thesis path (`scoped_amgt.py:3218`'s lazy `from lib.research.corpus import
dossier`), not at the adapter's own import. PASS when (a) no line -- nor any claim wrapped across lines, read on the whitespace-normalised text (AMENDMENT 1) -- of
lib/research/api/scoped_amgt.py still says "never a runtime
`lib.opal_naming` import" or "sits outside the adapter's vendored closure", (b) some comment line names both `opal_naming` and the
`dossier` path, and (c) a DYNAMIC read agrees: in a clean process, importing the adapter and then the /thesis path's own lazy import
(`lib.research.corpus.dossier`) leaves 'lib.opal_naming' in sys.modules (the bare adapter import is printed beside it).
usage: python <this>   (from the repo root)"""
import re
import subprocess
import sys

MOD = "lib/research/api/scoped_amgt.py"
FALSE = re.compile(r"never a runtime `?lib\.opal_naming`? import|outside (this|the) adapter's vendored closure", re.I)


def main():
    lines = open(MOD, encoding="utf-8").read().splitlines()
    stale = [(i + 1, ln.strip()[:100]) for i, ln in enumerate(lines) if FALSE.search(ln)]
    # AMENDMENT 1: a claim wrapped across lines (a docstring) is read on the whitespace-normalised text too
    flat = re.sub(r"\s+", " ", " ".join(ln.strip().lstrip("#").strip() for ln in lines))
    wrapped = [m.group(0)[:100] for m in FALSE.finditer(flat)]
    if len(wrapped) > len(stale):
        stale += [("wrapped", w) for w in wrapped[len(stale):]]
    named = [(i + 1) for i, ln in enumerate(lines) if ln.lstrip().startswith("#") and "opal_naming" in ln and "dossier" in ln]
    probe = ("import sys; import lib.research.api.scoped_amgt; a = 'lib.opal_naming' in sys.modules; "
             "import lib.research.corpus.dossier; print(a, 'lib.opal_naming' in sys.modules)")
    p = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True, timeout=90)
    last = (p.stdout.strip().splitlines() or ["? ?"])[-1].split()
    print("    bare adapter import loads it: %s" % last[0])
    dyn = last[-1] == "True"
    print("(a) stale claims: %d %s" % (len(stale), stale[:3]))
    print("(b) comment lines naming opal_naming and the dossier path: %s" % named[:3])
    print("(c) lib.opal_naming in sys.modules after the /thesis path's dossier import: %s" % dyn)
    ok = not stale and bool(named) and dyn
    print("THE ADAPTER'S COMMENTS STATE ITS REAL lib.opal_naming IMPORT: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
