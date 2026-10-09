"""AMGT_CORPUS round 42, CRPS-ar-2 leg v (issuer's file): read the WRITTEN /9 objects back (CTO half term: "leg v reads the /9
objects as written") and grade them. READ-ONLY S3 reads; nothing written.

For every resolved name: the stored /9 object (`read_dossier` with METHOD_VERSION at /9) and the served /7 object (the same read
with METHOD_VERSION set to /7 for the read only). Over the section fields AND risks of the /9 object:
  ellipsis   values ending in "..." -- the pre-write --live run measured ell_true 0, so ANY "..." here is a false cut marker
  prefix     values opening with a scorecard label and score
  cut        no sentence-end mark, no "...", and not one of the pre-write run's line-end values (checked against the
             recomposed value instead: the stored value must EQUAL what the current code composes -- fields_differ)
  changes    (name, field) whose /9 value differs from the served /7 value; must equal the 12 of the pre-write table
             (evidence/r42_ar2_changes_whole_20261009.txt), value for value
Prints `ar2 legv names <n> method9 <m> ellipsis <e> prefix <p> fields_differ <d> changes <c> match_pre <k>/12` and
`ar2 legv build <b>/1`: method9 = names, ellipsis 0, prefix 0, fields_differ 0, changes 12, match_pre 12/12.

  PYTHONPATH=. python ar2_legv_stored.py
"""
import os
import re
import sys
import types

sys.modules.setdefault("fitz", types.ModuleType("fitz"))

from lib.research.corpus import dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PRE = os.path.join(os.path.dirname(os.path.dirname(HERE)), "evidence", "r42_ar2_changes_whole_20261009.txt")
RE_PREFIX = re.compile(r"^[A-Z][A-Za-z/&\- ]{2,40} \d{1,3} (?=[A-Z])")


def _read(key, client, method):
    current = dossier.METHOD_VERSION
    dossier.METHOD_VERSION = method
    try:
        return dossier.read_dossier(key, client=client)["document"]
    finally:
        dossier.METHOD_VERSION = current


def _val(doc, name):
    f = (doc.get("fields") or {}).get(name)
    if not isinstance(f, dict):
        return None
    return f.get("value") if f.get("value") is not None else "ABSENT: %s" % f.get("absent")


def _pre_table():
    t = open(PRE, encoding="utf-8").read()
    out = {}
    for blk in t.split("=== ")[1:]:
        head, rest = blk.split("\n", 1)
        _n, key, name = head.split()
        m = re.search(r"NEW:    (.*?)(?:\n=== |\nar2 |\Z)", rest + "\n", re.S)
        out[(key, name)] = m.group(1).rstrip("\n")
    return out


def main():
    client = store._default_client()
    keys = dossier._resolved_security_keys(client=client)
    names = dossier._section_field_names_resolved_as_blocks()
    pre = _pre_table()
    n = m9 = ell = pref = differ = 0
    changes = {}
    for key in keys:
        try:
            d9 = _read(key, client, dossier.METHOD_VERSION)
            d7 = _read(key, client, "amgt-corpus-dossier/7")
        except LookupError:
            continue
        n += 1
        if d9.get("method_version") == dossier.METHOD_VERSION:
            m9 += 1
        _items, pick_a, pick_b = dossier._picked_reports(key, client)
        now = dossier._recompose_section_fields(pick_a, pick_b)
        for name in names:
            v9, v7 = _val(d9, name), _val(d7, name)
            if v9 is None:
                continue
            if isinstance(v9, str) and not v9.startswith("ABSENT: "):
                if v9.rstrip().endswith(dossier._ELLIPSIS) or v9.rstrip().endswith("…"):
                    ell += 1
                    print("ELLIPSIS %s %s ...%r" % (key, name, v9[-60:]))
                if RE_PREFIX.match(v9):
                    pref += 1
                    print("PREFIX %s %s %r" % (key, name, v9[:50]))
            c = now.get(name) or {}
            composed = c.get("value") if c.get("value") is not None else "ABSENT: %s" % c.get("absent")
            if composed != v9:
                differ += 1
                print("DIFFERS %s %s" % (key, name))
            if v7 != v9:
                changes[(key, name)] = v9
    match = sum(1 for k, v in pre.items() if changes.get(k) == v)
    extra = sorted(set(changes) - set(pre))
    for k in extra:
        print("CHANGE-NOT-IN-PRE %s %s" % k)
    for k in sorted(set(pre) - set(changes)):
        print("PRE-NOT-CHANGED %s %s" % k)
    print("ar2 legv names %d method9 %d ellipsis %d prefix %d fields_differ %d changes %d match_pre %d/%d"
          % (n, m9, ell, pref, differ, len(changes), match, len(pre)))
    build = int(m9 == n and ell == 0 and pref == 0 and differ == 0 and len(changes) == len(pre) and match == len(pre))
    print("ar2 legv build %d/1" % build)
    return 0 if build else 1


if __name__ == "__main__":
    sys.exit(main())
