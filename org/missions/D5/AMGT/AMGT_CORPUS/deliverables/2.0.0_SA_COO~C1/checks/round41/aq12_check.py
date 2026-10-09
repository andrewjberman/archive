"""AMGT_CORPUS round 41, CRPS-aq-1 and CRPS-aq-2 -- a served section passage ENDS at a sentence end (or carries an explicit
ellipsis) and STARTS at a word, not at a scorecard label. Issuer's file. Read-only and OFFLINE: it re-composes the section fields
with the CURRENT code (`dossier._recompose_section_fields`) from the picked reports frozen in `aq12_picks.json` (built by the
issuer from S3 on 2026-10-09: the 24 names the round-40 census flagged CUT or PREFIX, plus 5 control names). No S3, no network.

  python aq12_check.py aq1|aq2        (PYTHONPATH=. from the repository root)

aq1  -> `aq1 build <b>/1 control <c>/1`
     build    over every affected name and text field, the re-composed value either ends at a sentence end (one of . ! ? ; : ) ]
              " ' and their curly forms) or ends with an explicit ellipsis ("..." or the single ellipsis character): CUT 0.
     control  every value that ALREADY ended at a sentence end in the base re-compose (frozen beside the picks) is unchanged,
              character for character -- the repair touches only cut values.
aq2  -> `aq2 build <b>/1 control <c>/1`
     build    no re-composed value opens with a scorecard label and score ("<Label> <1-3 digits> <Capital>", e.g.
              "Management/Board 80 Eddie Wu ..."): PREFIX 0 (BABA US and ST SP management at the base).
     control  every management value with no such prefix at the base is unchanged, character for character.
Each arm also prints its counts and the offending (name, field, edge) so a failure names what to look at.
"""
import json
import os
import re
import sys
import types

sys.modules.setdefault("fitz", types.ModuleType("fitz"))  # extract.py imports fitz; no PDF is parsed here

from lib.research.corpus import dossier  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE = os.path.join(HERE, "aq12_picks.json")
BASE = os.path.join(HERE, "aq12_base_values.json")
TEXT_FIELDS = [
    "company_description", "growth_algorithm", "investment_thesis_summary", "management", "negatives", "positives",
    "risks", "special_items", "thesis_summary", "why_we_own",
]
ENDS = tuple(".!?;:)]\"'”’")
ELLIPSIS = ("...", "…")
RE_PREFIX = re.compile(r"^[A-Z][A-Za-z/&\- ]{2,40} \d{1,3} (?=[A-Z])")


def _recompose_all():
    fx = json.load(open(FIXTURE, encoding="utf-8"))
    values = {}
    for key, (pick_a, pick_b) in fx["picks"].items():
        fields = dossier._recompose_section_fields(pick_a, pick_b)
        for name in TEXT_FIELDS:
            v = (fields.get(name) or {}).get("value")
            if isinstance(v, str):
                values["%s|%s" % (key, name)] = v.strip()
    return fx, values


def _snapshot(values):
    with open(BASE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(values, ensure_ascii=True, sort_keys=True, indent=0) + "\n")
    print("SNAPSHOT written aq12_base_values.json (%d values)" % len(values))


def aq1(fx, now, base):
    cut = [(k, v[-50:]) for k, v in now.items() if k.split("|")[0] in fx["affected"] and not v.endswith(ENDS + ELLIPSIS)]
    for k, edge in cut:
        print("CUT %s ...%r" % (k, edge))
    ended = {k: v for k, v in base.items() if v.endswith(ENDS)}
    moved = [k for k, v in ended.items() if now.get(k) != v]
    for k in moved:
        print("CONTROL-MOVED %s" % k)
    print("aq1 counts cut %d of %d values; control %d values ended at a sentence end at the base, %d moved"
          % (len(cut), len(now), len(ended), len(moved)))
    print("aq1 build %d/1 control %d/1" % (1 if not cut else 0, 1 if not moved else 0))
    return 0 if not cut and not moved else 1


def aq2(fx, now, base):
    pref = [(k, v[:50]) for k, v in now.items() if RE_PREFIX.match(v)]
    for k, edge in pref:
        print("PREFIX %s %r..." % (k, edge))
    plain = {k: v for k, v in base.items() if k.endswith("|management") and not RE_PREFIX.match(v)}
    moved = [k for k, v in plain.items() if now.get(k) != v]
    for k in moved:
        print("CONTROL-MOVED %s" % k)
    print("aq2 counts prefix %d; control %d management values without a prefix at the base, %d moved"
          % (len(pref), len(plain), len(moved)))
    print("aq2 build %d/1 control %d/1" % (1 if not pref else 0, 1 if not moved else 0))
    return 0 if not pref and not moved else 1


def main(argv):
    if len(argv) < 2 or argv[1] not in ("aq1", "aq2", "--snapshot"):
        print(__doc__)
        return 2
    fx, now = _recompose_all()
    if argv[1] == "--snapshot":
        _snapshot(now)
        return 0
    base = json.load(open(BASE, encoding="utf-8"))
    return aq1(fx, now, base) if argv[1] == "aq1" else aq2(fx, now, base)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
