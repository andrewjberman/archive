"""AMGT_RESAPP round 53, AMGT-ac-4 AC1 -- scoped_amgt.py no longer says lib.research.harvest.store is unavailable in the deployed package
(row Z-S315; CTO round-52 analysis item 4). store.py IS packaged (zz-8's and ab-6's content diffs list it) and /thesis imports it through
corpus.dossier. PASS when, on the whitespace-normalised text of lib/research/api/scoped_amgt.py, no claim reads "unavailable in the
deployed package" (or "not in the deployed package") about harvest.store, AND importing the adapter plus the /thesis path's lazy
`lib.research.corpus.dossier` leaves 'lib.research.harvest.store' in sys.modules (the dynamic control).
usage: python <this>   (from the repo root)"""
import re
import subprocess
import sys

MOD = "lib/research/api/scoped_amgt.py"
FALSE = re.compile(r"(unavailable|not (packaged )?in) (in )?the deployed package", re.I)


def main():
    flat = re.sub(r"\s+", " ", " ".join(ln.strip().lstrip("#").strip() for ln in open(MOD, encoding="utf-8").read().splitlines()))
    hits = [flat[max(0, m.start() - 160):m.end()] for m in FALSE.finditer(flat)]
    store_hits = [h for h in hits if "harvest.store" in h or "the first" in h]
    probe = "import sys; import lib.research.api.scoped_amgt; import lib.research.corpus.dossier; print('lib.research.harvest.store' in sys.modules)"
    p = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True, timeout=90)
    dyn = (p.stdout.strip().splitlines() or [""])[-1] == "True"
    print("claims that store is unavailable in the deployed package: %d %s" % (len(store_hits), [h[-120:] for h in store_hits[:2]]))
    print("dynamic: harvest.store loaded on the /thesis path: %s" % dyn)
    ok = not store_hits and dyn
    print("THE ADAPTER'S TEXT STATES HARVEST.STORE IS PACKAGED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
