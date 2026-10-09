"""AMGT_CORPUS round 42, CRPS-ar-2 prep (issuer's file): every section value (risks included) the dossier re-write at METHOD /9
would change AGAINST WHAT THE PAGE SERVES (/7: the deployed scoped API reads /7; the stored /8 is never served), printed WHOLE.
READ-ONLY: S3 reads only, nothing written, no put.

The served pick is `read_dossier` with the module's METHOD_VERSION set to `amgt-corpus-dossier/7` for the read only (the reader picks
among objects of its own method, CRPS-j-4); the new value is `_recompose_section_fields` with the current code (METHOD /9).

  PYTHONPATH=. python ar2_changes_whole.py
"""
import sys
import types

sys.modules.setdefault("fitz", types.ModuleType("fitz"))

from lib.research.corpus import dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402

SERVED_METHOD = "amgt-corpus-dossier/7"


def _served(key, client):
    current = dossier.METHOD_VERSION
    dossier.METHOD_VERSION = SERVED_METHOD
    try:
        return dossier.read_dossier(key, client=client)["document"]
    finally:
        dossier.METHOD_VERSION = current


def main():
    client = store._default_client()
    keys = dossier._resolved_security_keys(client=client)
    entries, method_seen = [], {}
    for key in keys:
        try:
            served = _served(key, client)
        except LookupError:
            continue
        m = served.get("method_version")
        method_seen[m] = method_seen.get(m, 0) + 1
        _items, pick_a, pick_b = dossier._picked_reports(key, client)
        entries.append((key, served, dossier._recompose_section_fields(pick_a, pick_b)))
    scan = dossier._section_recompose_scan(entries)
    for i, (key, name, old, now) in enumerate(scan["changes"], 1):
        new = now.get("value") if now.get("value") is not None else "ABSENT: %s" % now.get("absent")
        print("=== %d %s %s" % (i, key, name))
        print("SERVED: %s" % old)
        print("NEW:    %s" % new)
    print("ar2 served methods %s" % sorted(method_seen.items(), key=lambda kv: str(kv[0])))
    print("ar2 changes %d of %d fields in %d names" % (len(scan["changes"]), scan["compared"], scan["names"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
