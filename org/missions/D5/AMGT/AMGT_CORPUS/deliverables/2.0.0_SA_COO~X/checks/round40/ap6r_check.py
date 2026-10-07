"""AMGT_CORPUS round 40, CRPS-ap-6 AMENDMENT 4 -- a served section value ends at a sentence end (1.0.0_SA_CTO~Z ruling msg
31352, on 3.0.0_SA_CVO~Z's read of the 25 gained passages). Issuer's file. Read-only, offline: it calls the REAL
`dossier._resolve_section_field` on hand-built documents. NO S3 call.

  python ap6r_check.py        (from the repository root, PYTHONPATH=.)

Prints `ap6r build <b>/3 control <c>/3`.
  build    r1  the Nike shape: prose ending "...the US Tax Cuts and Jobs Act." followed by the item "4_7_2026" (the source
               file's date): the value ends "Jobs Act." and carries no "4_7_2026";
           r2  the SAP shape: "...the software is too mission-critical. sec": the value ends "mission-critical.";
           r3  a value whose last sentence is unfinished ("... First point stands. Sell-side estimates kept"): the value ends
               "First point stands."
  control  c1  a value that already ends at a sentence end is unchanged, to the character;
           c2  NEGATIVE CONTROL: a value with decimal points and no sentence end ("... sales of $4.35bn (+14% YoY) and EPS of
               $4.03 against a guide of $3.90") is unchanged: a decimal point is not a sentence end;
           c3  a section of bullet lines with no full stop anywhere is unchanged.
"""
import sys

from lib.research.corpus import dossier

ROW = {"bronze_key": "bronze/research/Acme/Acme research pack 4_7_2026.docx", "report_id": "r-1"}
SPECIAL = dossier.SECTION_FIELD_NAMES["special_items"]
POSITIVES = dossier.SECTION_FIELD_NAMES["positives"]
NEGATIVES = dossier.SECTION_FIELD_NAMES["negatives"]
MANAGEMENT = dossier.SECTION_FIELD_NAMES["management"]
NEXT = ("OWNERSHIP: Insiders hold five percent of the shares outstanding.", False)


def docx(lead_name, paragraphs):
    paras = [{"text": t, "bold": b} for t, b in paragraphs] + [{"text": NEXT[0], "bold": NEXT[1]}]
    return {"type": "docx", "paragraphs": paras,
            "section_leads": [{"name": lead_name, "paragraph_index": 0, "inline_remainder": ""},
                              {"name": "OWNERSHIP", "paragraph_index": len(paragraphs),
                               "inline_remainder": "Insiders hold five percent of the shares outstanding."}]}


def value(label, names, document):
    try:
        field = dossier._resolve_section_field(label, names, (ROW, document), None, "Acme research pack", "none")
    except Exception as exc:  # a fixture the resolver cannot read is printed, never a silent zero
        return "ERROR %s: %s" % (type(exc).__name__, exc)
    return field.get("value") if field.get("value") is not None else "ABSENT: %s" % field.get("absent")


NIKE = "The dramatic decline in earnings per share in 2018 was due to a non-recurring charge from the US Tax Cuts and Jobs Act."
SAP = "Customers rarely leave because the migration cost is high and the software is too mission-critical."
CUT = "Adjusted earnings fell even as adjusted net income rose on the higher share count. First point stands."
WHOLE = "Management guided to mid-teens growth for the full year and reiterated the margin target at the investor day."
DECIMAL = "Fourth quarter sales of $4.35bn (+14% YoY) and EPS of $4.03 against a guide of $3.90 and consensus near $3.95"
BULLETS = ["Founder and chief executive since inception", "Engineer by training with a long product record",
           "Owns a controlling founder share of the votes", "The board is majority independent of management"]

got = {
    "r1": value("SPECIAL ITEMS", SPECIAL, docx("SPECIAL ITEMS", [("Special items:", False), (NIKE, False), ("4_7_2026", False)])),
    "r2": value("POSITIVES", POSITIVES, docx("POSITIVES", [("OTHER POSITIVES:", False), (SAP + " sec", False)])),
    "r3": value("NEGATIVES", NEGATIVES, docx("NEGATIVES", [("Negatives", False), (CUT + " Sell-side estimates kept", False)])),
    "c1": value("NEGATIVES", NEGATIVES, docx("NEGATIVES", [("Negatives", False), (WHOLE, False)])),
    "c2": value("POSITIVES", POSITIVES, docx("POSITIVES", [("Positives", False), (DECIMAL, False)])),
    "c3": value("MANAGEMENT", MANAGEMENT, docx("MANAGEMENT", [("MANAGEMENT", False)] + [(b, False) for b in BULLETS])),
}
for key in sorted(got):
    print("%s -> %r" % (key, str(got[key])[-90:]))
r1 = 1 if str(got["r1"]).endswith("Jobs Act.") and "4_7_2026" not in str(got["r1"]) else 0
r2 = 1 if str(got["r2"]).endswith("mission-critical.") else 0
r3 = 1 if str(got["r3"]).endswith("First point stands.") else 0
c1 = 1 if str(got["c1"]).endswith(WHOLE) else 0
c2 = 1 if str(got["c2"]).endswith(DECIMAL) else 0
c3 = 1 if str(got["c3"]).endswith(BULLETS[-1]) and BULLETS[0] in str(got["c3"]) else 0
print("ap6r build %d/3 control %d/3" % (r1 + r2 + r3, c1 + c2 + c3))
sys.exit(0)
