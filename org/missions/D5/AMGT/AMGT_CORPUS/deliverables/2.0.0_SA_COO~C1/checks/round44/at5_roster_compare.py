"""AMGT_CORPUS round 44, CRPS-at-5 -- FWD-11's officer comparison, by content, name by name (round-39 ruling 5:
ledger/ROUND_ANALYSIS.round39.md:39; close read @987284b18e item 3). Issuer's file. READ-ONLY S3 reads; nothing written.

For SAP_GY_Equity and BABA_US_Equity (the two names that serve BOTH a team management passage and a FILING roster):
  served   scoped_amgt.read_management(key)["officers"]  -- the roster the page shows
  filing   roster.derive_roster(roster.load_source_object(key), as_of)  -- the producer's parse of the persisted filing, re-run now
  text     the persisted filing object's text: every served name must appear in it verbatim (whitespace-collapsed), so the
           comparison does not rest on the parser alone
Per name prints served name/role, the filing-parse match, and whether the name is in the filing text; then
`at5 <key> served <s> filing <f> same_names <n> same_roles <r> in_text <t>` and `at5 unchanged <u>/2`, where a roster is
UNCHANGED when every served officer pairs BY NAME with the filing parse's officer of that name, the roles are equal, the counts
are equal, and every served name is in the text (round-39 ruling 5: by content, name by name). Order is printed, not graded: the
served list leads with the CEO, the parse keeps the filing's table order.
  PYTHONPATH=. python at5_roster_compare.py
"""
import re
import sys
import types

sys.modules.setdefault("fitz", types.ModuleType("fitz"))

from lib.research.api import scoped_amgt  # noqa: E402
from lib.research.management import roster  # noqa: E402

KEYS = ("SAP_GY_Equity", "BABA_US_Equity")


def norm(s):
    return re.sub(r"\s+", " ", roster.asciify(str(s or ""))).strip().lower()


def _text_of(obj):
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        return " ".join(_text_of(v) for v in obj.values())
    if isinstance(obj, list):
        return " ".join(_text_of(v) for v in obj)
    return ""


def main():
    unchanged = 0
    for key in KEYS:
        served_doc = scoped_amgt.read_management(key)
        served = served_doc.get("officers") or []
        src, label = roster.load_source_object(key)
        derived = roster.derive_roster(src, served_doc.get("as_of") or "", label)
        filing = (derived.get("officers") if isinstance(derived, dict) else derived) or []
        if isinstance(derived, tuple):
            filing = derived[0].get("officers", []) if isinstance(derived[0], dict) else derived[0]
        text = norm(_text_of(src))
        print("== %s roster_source %s source_key %s" % (key, served_doc.get("roster_source"), served_doc.get("source_key")))
        same_names = same_roles = in_text = 0
        by_name = {norm(f.get("name")): f for f in filing}
        for o in served:
            f = by_name.get(norm(o.get("name"))) or {}
            nm = bool(f)
            rl = nm and norm(o.get("role")) == norm(f.get("role"))
            tx = norm(o.get("name")) in text
            same_names += int(nm)
            same_roles += int(rl)
            in_text += int(tx)
            print("  %-34s | %-48s | filing-parse name %s role %s | in filing text %s" % (
                roster.asciify(o.get("name") or "")[:34], roster.asciify(o.get("role") or "")[:48], nm, rl, tx))
        ok = len(served) > 0 and len(served) == len(filing) and same_names == same_roles == in_text == len(served)
        unchanged += int(ok)
        same_order = [norm(o.get("name")) for o in served] == [norm(f.get("name")) for f in filing]
        print("at5 %s served %d filing %d same_names %d same_roles %d in_text %d same_order %s" % (
            key, len(served), len(filing), same_names, same_roles, in_text, same_order))
    print("at5 unchanged %d/2" % unchanged)
    return 0 if unchanged == 2 else 1


if __name__ == "__main__":
    sys.exit(main())
