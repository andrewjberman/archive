"""AMGT_CORPUS round 41, CRPS-aq-5 prep (issuer's file): every section value the dossier re-write at METHOD /8 would change,
printed WHOLE -- served (/7, the pick the portal serves) and new (re-composed in memory with the current code). READ-ONLY: the
same reads as `dossier --section-recompose-census`, nothing written, no put. For the never-widen pair: each changed value is read
whole before the served act (round 40's ap-10(d) CTO half C1).

  PYTHONPATH=. python aq5_changes_whole.py
"""
import sys
import types

sys.modules.setdefault("fitz", types.ModuleType("fitz"))

from lib.research.corpus import dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402


def main():
    client = store._default_client()
    keys = dossier._resolved_security_keys(client=client)
    entries = []
    for key in keys:
        try:
            served = dossier.read_dossier(key, client=client)["document"]
        except LookupError:
            continue
        _items, pick_a, pick_b = dossier._picked_reports(key, client)
        entries.append((key, served, dossier._recompose_section_fields(pick_a, pick_b)))
    scan = dossier._section_recompose_scan(entries)
    n = 0
    for key, name, served, now in scan["changes"]:
        n += 1
        new = now.get("value") if now.get("value") is not None else "ABSENT: %s" % now.get("absent")
        print("=== %d %s %s" % (n, key, name))
        print("SERVED: %s" % served)
        print("NEW:    %s" % new)
    print("aq5 changes %d of %d fields in %d names" % (len(scan["changes"]), scan["compared"], scan["names"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
