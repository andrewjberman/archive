"""AMGT_CORPUS round 40, CRPS-ap-10 (d2) -- what each sentence-end TRIM drops, and the named values of the CVO's grade.

Read-only (S3 reads of the stored dossiers and extractions; writes nothing). For every (name, field) whose re-composed value on
the current code differs from the stored dossier's value it prints: characters kept, characters dropped, the last 60 characters
KEPT and the whole DROPPED tail cut to 140 characters. Then the named values of the CVO's grade (the two stray tokens and the six
mid-sentence values), each with its last 60 characters now, whether or not it changed. Research text appears only as these tails.

  python ap10d2_trim_tails.py        (PYTHONPATH=. from the repository root)
"""
import sys

from lib.research.corpus import dossier
from lib.research.harvest import store

NAMED = [("NKE_US_Equity", "special_items"), ("SAP_GY_Equity", "positives"), ("LLY_US_Equity", "negatives"),
         ("NU_US_Equity", "positives"), ("NU_US_Equity", "negatives"), ("QXO_US_Equity", "negatives"),
         ("UNH_US_Equity", "negatives"), ("SHOP_CN_Equity", "management")]


def ascii_only(text):
    return str(text).encode("ascii", "replace").decode("ascii")


def main():
    client = store._default_client()
    keys = dossier._resolved_security_keys(client=client)
    changed = dropped_total = 0
    seen = {}
    for key in keys:
        try:
            served = dossier.read_dossier(key, client=client)["document"]
        except LookupError:
            continue
        _raw, pick_a, pick_b = dossier._picked_reports(key, client)
        now = dossier._recompose_section_fields(pick_a, pick_b)
        fields = served.get("fields") or {}
        for name, new in now.items():
            old = (fields.get(name) or {}).get("value")
            new_value = new.get("value")
            seen[(key, name)] = (old, new_value, served.get("method_version"))
            if old == new_value:
                continue
            changed += 1
            if isinstance(old, str) and isinstance(new_value, str) and old.startswith(new_value):
                tail = old[len(new_value):]
                dropped_total += len(tail)
                print("TRIM %-18s %-26s kept %5d dropped %4d | kept ends %r | dropped %r" % (
                    key, name, len(new_value), len(tail), ascii_only(new_value[-60:]), ascii_only(tail[:140])))
            else:
                print("OTHER %-18s %-26s old %r new %r" % (key, name, ascii_only(str(old)[-60:]), ascii_only(str(new_value)[-60:])))
    print("changed %d fields; characters dropped in all %d" % (changed, dropped_total))
    print("")
    print("the CVO's eight named values, as stored and as re-composed now:")
    for key, name in NAMED:
        old, new_value, method = seen.get((key, name), (None, None, None))
        print("%-16s %-14s stored(%s) ends %r | now ends %r | changed %s" % (
            key, name, str(method).rsplit("/", 1)[-1], ascii_only(str(old)[-50:]), ascii_only(str(new_value)[-50:]), old != new_value))
    return 0


if __name__ == "__main__":
    sys.exit(main())
