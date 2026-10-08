"""AMGT_CORPUS round 40, CRPS-ap-6 -- a section value that is only its own heading is not a passage (round-39 analysis
ruling 9, row Z-S89). Issuer's file. Read-only, offline: it calls the REAL `dossier._resolve_section_field` on hand-built
documents. NO S3 call.

  python ap6_check.py        (from the repository root, PYTHONPATH=.)

Prints `ap6 build <b>/6 control <c>/3`.
  build    b1  docx: the MANAGEMENT/BOARD lead paragraph is "Management/Board 80" and the next paragraph is a bold heading,
               so the block is the lead line alone: the field reads value None with an `absent` reason;
           b2  docx again, the lead line followed directly by the next section's lead: value None with an `absent` reason.
           AMENDMENT 2 (CTO ruling msg 31134: the item directly after a section's lead never ends the block):
           b3  docx: the heading, then a short BOLD line ("Sir Pascal Soriot CEO"), then prose: the value carries the prose;
           b4  pdf: the heading, then a "-" line, then prose lines (the shape of TSM's "Positives"): the value carries the
               prose.
           AMENDMENT 3 (the after-census, evidence/r40_ap10_section_recompose_census_20261007.txt: 17 of the 41 "gains"
           were page furniture or a table header served as a passage):
           b5  pdf: "Special items:", then a page header ("4_30_2026"), a page number ("5") and the next unnamed headings
               ("Supporting documentation:", "Business model"): no item is prose, so the field reads absent;
           b6  docx: "COMMON STOCK COMPARISON", then "6/23/2026": absent.
  control  c3  a section of short bullet lines (none over the heading word cap, 25 or more words in all) is still served;
           c1  a lead with an inline passage ("MANAGEMENT: The CEO has run ...") still serves that passage, cited;
           c2  a heading-only lead followed by a body paragraph serves the body (the value contains the body sentence).
"""
import sys

from lib.research.corpus import dossier

NAMES = dossier.SECTION_FIELD_NAMES["management"]
ROW = {"bronze_key": "bronze/research/Acme/Acme Initiation.docx", "report_id": "r-1"}
BODY = "The chief executive has run the company for ten years and owns four percent of the shares."


def docx(paragraphs, leads):
    return {"type": "docx", "paragraphs": [{"text": t, "bold": b} for t, b in paragraphs], "section_leads": leads}


def resolve(document):
    return dossier._resolve_section_field("MANAGEMENT", NAMES, (ROW, document), None, "Acme Initiation.docx", "none")


def is_refused(field):
    return field.get("value") is None and bool(field.get("absent"))


heading_only = docx(
    [("Management/Board 80", True), ("OWNERSHIP", True), ("Insiders hold five percent of the shares outstanding.", False)],
    [{"name": "MANAGEMENT/BOARD", "paragraph_index": 0, "inline_remainder": "80"},
     {"name": "OWNERSHIP", "paragraph_index": 1, "inline_remainder": ""}],
)
heading_then_lead = docx(
    [("Management/Board 80", False), ("OWNERSHIP: Insiders hold five percent of the shares outstanding.", False)],
    [{"name": "MANAGEMENT/BOARD", "paragraph_index": 0, "inline_remainder": "80"},
     {"name": "OWNERSHIP", "paragraph_index": 1, "inline_remainder": "Insiders hold five percent of the shares outstanding."}],
)
inline = docx(
    [("MANAGEMENT: " + BODY, False), ("OWNERSHIP: Insiders hold five percent of the shares outstanding.", False)],
    [{"name": "MANAGEMENT", "paragraph_index": 0, "inline_remainder": BODY},
     {"name": "OWNERSHIP", "paragraph_index": 1, "inline_remainder": "Insiders hold five percent of the shares outstanding."}],
)
heading_then_body = docx(
    [("Management/Board", True), (BODY, False), ("OWNERSHIP: Insiders hold five percent of the shares outstanding.", False)],
    [{"name": "MANAGEMENT/BOARD", "paragraph_index": 0, "inline_remainder": ""},
     {"name": "OWNERSHIP", "paragraph_index": 2, "inline_remainder": "Insiders hold five percent of the shares outstanding."}],
)

PROSE = "Revenue and net income both set all-time quarterly records on operating leverage and a favorable mix shift."
heading_bold_then_body = docx(
    [("MANAGEMENT:", True), ("Sir Pascal Soriot CEO", True), (BODY, False),
     ("OWNERSHIP: Insiders hold five percent of the shares outstanding.", False)],
    [{"name": "MANAGEMENT", "paragraph_index": 0, "inline_remainder": ""},
     {"name": "OWNERSHIP", "paragraph_index": 3, "inline_remainder": "Insiders hold five percent of the shares outstanding."}],
)
pdf_dash_then_body = {
    "type": "pdf",
    # row AMGT_CORPUS-Z-W2-S22: the dash is BOLD, as in TSM's pack, so the reader flags it as a standalone heading and this
    # arm fails when the first-item rule is absent (with plain lines it passed with or without the rule).
    "lines": [{"text": t, "page": 0, "size": 9.96, "bold_all": t == "-"} for t in (
        "Management", "-", PROSE, "Gross margin reached a record on high utilization and pricing across advanced nodes.",
        "Ownership", "Insiders hold five percent of the shares outstanding today per the latest filing.")],
    "section_leads": [{"name": "MANAGEMENT", "line_index": 0, "page": 0, "inline_remainder": ""},
                      {"name": "OWNERSHIP", "line_index": 4, "page": 0, "inline_remainder": ""}],
}

pdf_furniture = {
    "type": "pdf",
    "lines": [{"text": t, "page": p, "size": s} for t, p, s in (
        ("Special items:", 2, 9.8), ("4_30_2026", 3, 12.0), ("5", 3, 12.0), ("Supporting documentation:", 3, 9.8),
        ("Business model", 3, 9.8), ("Ownership", 3, 9.8),
        ("Insiders hold five percent of the shares outstanding today per the latest filing.", 3, 9.8))],
    "section_leads": [{"name": "SPECIAL ITEMS", "line_index": 0, "page": 2, "inline_remainder": ""},
                      {"name": "OWNERSHIP", "line_index": 5, "page": 3, "inline_remainder": ""}],
}
docx_date_only = docx(
    [("COMMON STOCK COMPARISON", True), ("6/23/2026", False), ("OWNERSHIP: Insiders hold five percent of the shares.", False)],
    [{"name": "COMMON STOCK COMPARISON", "paragraph_index": 0, "inline_remainder": ""},
     {"name": "OWNERSHIP", "paragraph_index": 2, "inline_remainder": "Insiders hold five percent of the shares."}],
)
BULLETS = ["Tobi Lutke, founder and chief executive since inception.", "German-Canadian engineer by training.",
           "Owns a controlling founder share.", "Harley Finkelstein is president.", "Jeff Hoffmeister is finance chief.",
           "The board is majority independent."]
docx_bullets = docx(
    [("MANAGEMENT", True)] + [(b, False) for b in BULLETS] + [("OWNERSHIP: Insiders hold five percent of the shares.", False)],
    [{"name": "MANAGEMENT", "paragraph_index": 0, "inline_remainder": ""},
     {"name": "OWNERSHIP", "paragraph_index": 7, "inline_remainder": "Insiders hold five percent of the shares."}],
)
SPECIAL = dossier.SECTION_FIELD_NAMES["special_items"]
COMPARE = dossier.SECTION_FIELD_NAMES["comparison_set"]


def resolve_as(label, names, document):
    return dossier._resolve_section_field(label, names, (ROW, document), None, "Acme Initiation.docx", "none")


results = {}
for label, document in (("heading_only", heading_only), ("heading_then_lead", heading_then_lead), ("inline", inline),
                        ("heading_then_body", heading_then_body), ("heading_bold_then_body", heading_bold_then_body),
                        ("pdf_dash_then_body", pdf_dash_then_body)):
    try:
        results[label] = resolve(document)
    except Exception as exc:  # a fixture the resolver cannot read is printed, never a silent zero
        results[label] = {"error": "%s: %s" % (type(exc).__name__, exc)}
    print("%s -> %r" % (label, {k: results[label].get(k) for k in ("value", "absent", "error") if k in results[label]}))

b1 = 1 if is_refused(results["heading_only"]) else 0
b2 = 1 if is_refused(results["heading_then_lead"]) else 0
c1 = 1 if BODY in str(results["inline"].get("value") or "") and results["inline"].get("citation") else 0
c2 = 1 if BODY in str(results["heading_then_body"].get("value") or "") else 0
for label, call in (("pdf_furniture", lambda: resolve_as("SPECIAL ITEMS", SPECIAL, pdf_furniture)),
                    ("docx_date_only", lambda: resolve_as("COMPARISON SET", COMPARE, docx_date_only)),
                    ("docx_bullets", lambda: resolve(docx_bullets))):
    try:
        results[label] = call()
    except Exception as exc:
        results[label] = {"error": "%s: %s" % (type(exc).__name__, exc)}
    print("%s -> %r" % (label, {k: str(results[label].get(k))[:90] for k in ("value", "absent", "error") if k in results[label]}))
b5 = 1 if is_refused(results["pdf_furniture"]) else 0
b6 = 1 if is_refused(results["docx_date_only"]) else 0
c3 = 1 if BULLETS[3] in str(results["docx_bullets"].get("value") or "") else 0
b3 = 1 if BODY in str(results["heading_bold_then_body"].get("value") or "") else 0
b4 = 1 if PROSE in str(results["pdf_dash_then_body"].get("value") or "") else 0
print("ap6 build %d/6 control %d/3" % (b1 + b2 + b3 + b4 + b5 + b6, c1 + c2 + c3))
sys.exit(0)
