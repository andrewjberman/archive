"""AMGT_CORPUS round 40, CRPS-ap-6 -- a section value that is only its own heading is not a passage (round-39 analysis
ruling 9, row Z-S89). Issuer's file. Read-only, offline: it calls the REAL `dossier._resolve_section_field` on hand-built
documents. NO S3 call.

  python ap6_check.py        (from the repository root, PYTHONPATH=.)

Prints `ap6 build <b>/4 control <c>/2`.
  build    b1  docx: the MANAGEMENT/BOARD lead paragraph is "Management/Board 80" and the next paragraph is a bold heading,
               so the block is the lead line alone: the field reads value None with an `absent` reason;
           b2  docx again, the lead line followed directly by the next section's lead: value None with an `absent` reason.
           AMENDMENT 2 (CTO ruling msg 31134: the item directly after a section's lead never ends the block):
           b3  docx: the heading, then a short BOLD line ("Sir Pascal Soriot CEO"), then prose: the value carries the prose;
           b4  pdf: the heading, then a "-" line, then prose lines (the shape of TSM's "Positives"): the value carries the
               prose.
  control  c1  a lead with an inline passage ("MANAGEMENT: The CEO has run ...") still serves that passage, cited;
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
    "lines": [{"text": t, "page": 0, "size": 9.96} for t in (
        "Management", "-", PROSE, "Gross margin reached a record on high utilization and pricing across advanced nodes.",
        "Ownership", "Insiders hold five percent of the shares outstanding today per the latest filing.")],
    "section_leads": [{"name": "MANAGEMENT", "line_index": 0, "page": 0, "inline_remainder": ""},
                      {"name": "OWNERSHIP", "line_index": 4, "page": 0, "inline_remainder": ""}],
}

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
b3 = 1 if BODY in str(results["heading_bold_then_body"].get("value") or "") else 0
b4 = 1 if PROSE in str(results["pdf_dash_then_body"].get("value") or "") else 0
print("ap6 build %d/4 control %d/2" % (b1 + b2 + b3 + b4, c1 + c2))
sys.exit(0)
