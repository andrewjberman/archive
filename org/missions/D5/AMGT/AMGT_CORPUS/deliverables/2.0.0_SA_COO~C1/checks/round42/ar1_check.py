"""AMGT_CORPUS round 42 PRE-DRAFT check (issuer's file; NOT ISSUED until the round-41 analysis) for the CTO's one cell (msg 2968,
CTO half ADDENDUM 1): `risks` is re-composed like every section field, and a bullet line's end counts as a sentence end, so a "..."
marks a REAL cut only. Read-only and OFFLINE over the round-41 frozen picks (checks/round41/aq12_picks.json: 24 affected names + 5
controls, AZN LN and BP LN included). No S3, no network.

  PYTHONPATH=. python ar1_check.py

Per name and text field (the section fields AND `risks`), the value the CURRENT code composes is classed:
  END       ends at a sentence end (. ! ? ; : ) ] or a quote, straight or curly)
  ELL-TRUE  ends with "..." and the report's sentence really continues: a pdf block whose NEXT line is non-blank, the same font size
            (within the reader's tolerance), and not a section lead, bold or a bullet -- text the reader could not finish
  ELL-FALSE ends with "..." anywhere else (a docx paragraph; a pdf block followed by a blank, bullet, bold, lead or size change, or
            the end of the document): a whole line wrongly marked cut -- MEASURED by this rule, not read
  CUT       neither (no sentence end and no ellipsis)
  PREFIX    opens with a scorecard label and score
Prints `ar1 counts cut <c> ell_false <f> ell_true <t> prefix <p> of <n> values` and `ar1 build <b>/1 control <k>/1`:
  build    cut 0, ell_false 0, prefix 0
  control  every value that ended at a sentence end in round 41's base snapshot (checks/round41/aq12_base_values.json, section
           fields only) keeps its last 60 characters.
"""
import json
import os
import re
import sys
import types

sys.modules.setdefault("fitz", types.ModuleType("fitz"))

from lib.research.corpus import dossier  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R41 = os.path.join(os.path.dirname(HERE), "round41")
ENDS = tuple(".!?;:)]\"'”’")
RE_PREFIX = re.compile(r"^[A-Z][A-Za-z/&\- ]{2,40} \d{1,3} (?=[A-Z])")
EDGE = 60


def _block(names, pick_a, pick_b):
    found = dossier._resolve_section_block_from_picks(names, pick_a, pick_b)
    if found is None:
        return None, None
    pick, _locator, items, _text = found
    return pick[1], items


def _ellipsis_is_true(document, names, items):
    if not document or document.get("type") != "pdf" or not items:
        return False
    lead = dossier._find_section_lead(document, names)
    if lead is None:
        return False
    lines = document.get("lines") or []
    end = lead["line_index"] + len(items)
    last_size = None
    for idx in range(end - 1, lead["line_index"] - 1, -1):
        if (lines[idx].get("text") or "").strip():
            last_size = lines[idx].get("size")
            break
    if end >= len(lines) or last_size is None:
        return False
    nxt = lines[end]
    text = (nxt.get("text") or "").strip()
    leads = {ld["line_index"] for ld in dossier._document_section_leads(document)}
    if (not text or end in leads or nxt.get("bold_all") or nxt.get("bold_first") or text.startswith(dossier._BULLET_STARTS)
            or nxt.get("size") is None or abs(nxt["size"] - last_size) > dossier._CONTINUE_SIZE_TOLERANCE):
        return False
    return True


def main():
    fx = json.load(open(os.path.join(R41, "aq12_picks.json"), encoding="utf-8"))
    base = json.load(open(os.path.join(R41, "aq12_base_values.json"), encoding="utf-8"))
    counts = {"END": 0, "ELL-TRUE": 0, "ELL-FALSE": 0, "CUT": 0}
    prefix, n, now = 0, 0, {}
    for key, (pick_a, pick_b) in fx["picks"].items():
        fields = dossier._recompose_section_fields(pick_a, pick_b)
        risks, _pm = dossier._resolve_risks_field(pick_a, pick_b, "A", "B")
        fields = dict(fields)
        fields["risks"] = risks
        for name, field in fields.items():
            v = (field or {}).get("value") if isinstance(field, dict) else None
            if not isinstance(v, str) or name not in dossier.SECTION_FIELD_NAMES:
                continue
            v = v.strip()
            n += 1
            now["%s|%s" % (key, name)] = v
            if RE_PREFIX.match(v):
                prefix += 1
                print("PREFIX %s %s %r" % (key, name, v[:50]))
            if v.endswith(dossier._ELLIPSIS) or v.endswith("…"):
                document, items = _block(dossier.SECTION_FIELD_NAMES[name], pick_a, pick_b)
                cls = "ELL-TRUE" if _ellipsis_is_true(document, dossier.SECTION_FIELD_NAMES[name], items) else "ELL-FALSE"
            elif v.endswith(ENDS):
                cls = "END"
            else:
                cls = "CUT"
            counts[cls] += 1
            if cls != "END":
                print("%s %s %s ...%r" % (cls, key, name, v[-60:]))
    moved = [k for k, v in base.items() if v.endswith(ENDS) and not now.get(k, "").endswith(v[-EDGE:])]
    for k in moved:
        print("CONTROL-MOVED %s" % k)
    print("ar1 counts cut %d ell_false %d ell_true %d prefix %d of %d values"
          % (counts["CUT"], counts["ELL-FALSE"], counts["ELL-TRUE"], prefix, n))
    build = 1 if counts["CUT"] == 0 and counts["ELL-FALSE"] == 0 and prefix == 0 else 0
    print("ar1 build %d/1 control %d/1" % (build, 0 if moved else 1))
    return 0 if build and not moved else 1


if __name__ == "__main__":
    sys.exit(main())
