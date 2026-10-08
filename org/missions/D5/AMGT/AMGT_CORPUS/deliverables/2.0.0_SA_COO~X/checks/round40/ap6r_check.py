"""AMGT_CORPUS round 40, CRPS-ap-6 AMENDMENT 5 -- a served section value drops ONLY a trailing fragment of one or two words
after a sentence end (1.0.0_SA_CTO~Z ruling msg 31382, which WITHDRAWS msg 31352's "end at the last sentence end": read on all
950 stored fields that rule dropped about 14 complete bullet points and left the Nike value unfixed; evidence
r40_ap10d2_trim_tails_20261007.txt). Issuer's file. Read-only, offline: it calls the REAL `dossier._resolve_section_field` on
hand-built documents shaped like the stored values. NO S3 call.

  python ap6r_check.py        (from the repository root, PYTHONPATH=.)

Prints `ap6r build <b>/3 control <c>/6`.
  build    r1  the REAL Nike shape: the prose is the lead line's own inline text ("Special items: ... the US Tax Cuts and Jobs
               Act.") and the only item after it is "4_7_2026": the value ends "Jobs Act." and carries no "4_7_2026";
           r2  the SAP shape: "...the software is too mission-critical. sec": the value ends "mission-critical.";
           r3  a stray word after the last sentence ("...is expected to come from. Asdsa"): the value ends "come from."
  control  c1  a value that already ends at a sentence end is unchanged, to the character;
           c2  a value with decimal points and no sentence end is unchanged: a decimal point is not a sentence end;
           c3  a section of bullet lines with no full stop anywhere is unchanged;
           c4  an unfinished last sentence of THREE OR MORE words after a sentence end STAYS ("... First point stands.
               Sell-side estimates kept"): known-truncated values are served as stored (ruled);
           c5  the Shopify shape: one bullet ending in a full stop, then complete bullets with no full stop: every bullet stays;
           c6  the Imperial Brands shape: "... Geography: Europe (~42% of rev), U.S. (~35% of rev), Africa and Asia (~23% of
               rev)" is unchanged: an abbreviation's full stop followed by more than two words drops nothing.
"""
import sys

from lib.research.corpus import dossier

ROW = {"bronze_key": "bronze/research/Acme/Acme research pack 4_7_2026.docx", "report_id": "r-1"}
NAMES = dossier.SECTION_FIELD_NAMES
NEXT = "OWNERSHIP: Insiders hold five percent of the shares outstanding."


def docx(lead_name, paragraphs, inline=""):
    paras = [{"text": t, "bold": False} for t in paragraphs] + [{"text": NEXT, "bold": False}]
    return {"type": "docx", "paragraphs": paras,
            "section_leads": [{"name": lead_name, "paragraph_index": 0, "inline_remainder": inline},
                              {"name": "OWNERSHIP", "paragraph_index": len(paragraphs),
                               "inline_remainder": "Insiders hold five percent of the shares outstanding."}]}


def value(label, field, document):
    try:
        got = dossier._resolve_section_field(label, NAMES[field], (ROW, document), None, "Acme research pack", "none")
    except Exception as exc:  # a fixture the resolver cannot read is printed, never a silent zero
        return "ERROR %s: %s" % (type(exc).__name__, exc)
    return got.get("value") if got.get("value") is not None else "ABSENT: %s" % got.get("absent")


NIKE = "The dramatic decline in earnings per share in 2018 was due to a non-recurring charge from the US Tax Cuts and Jobs Act."
SAP = "Customers rarely leave because the migration cost is high and the software is too mission-critical."
FROM = "Management has said that much of the future value creation is expected to come from."
CUT = "Adjusted earnings fell even as adjusted net income rose on the higher share count. First point stands."
WHOLE = "Management guided to mid-teens growth for the full year and reiterated the margin target at the investor day."
DECIMAL = "Fourth quarter sales of $4.35bn (+14% YoY) and EPS of $4.03 against a guide of $3.90 and consensus near $3.95"
BULLETS = ["Founder and chief executive since inception", "Engineer by training with a long product record",
           "Owns a controlling founder share of the votes", "The board is majority independent of management"]
SHOP = ["Tobi Lutke, co-founder and chief executive since inception.",
        "German-Canadian, born 1980, a programmer who emigrated from Germany and tried to sell snowboards online in 2004",
        "Joined the Rails core team and created open-source libraries like Liquid and Active Merchant for commerce"]
IMB = "Imperial Brands has a market cap near 21bn. Geography: Europe (~42% of rev), U.S. (~35% of rev), Africa and Asia (~23% of rev)"

got = {
    "r1": value("SPECIAL ITEMS", "special_items", docx("SPECIAL ITEMS", ["Special items: " + NIKE, "4_7_2026"], inline=NIKE)),
    "r2": value("POSITIVES", "positives", docx("POSITIVES", ["OTHER POSITIVES:", SAP + " sec"])),
    "r3": value("MANAGEMENT", "management", docx("MANAGEMENT", ["MANAGEMENT", FROM + " Asdsa"])),
    "c1": value("NEGATIVES", "negatives", docx("NEGATIVES", ["Negatives", WHOLE])),
    "c2": value("POSITIVES", "positives", docx("POSITIVES", ["Positives", DECIMAL])),
    "c3": value("MANAGEMENT", "management", docx("MANAGEMENT", ["MANAGEMENT"] + BULLETS)),
    "c4": value("NEGATIVES", "negatives", docx("NEGATIVES", ["Negatives", CUT + " Sell-side estimates kept"])),
    "c5": value("MANAGEMENT", "management", docx("MANAGEMENT", ["MANAGEMENT"] + SHOP)),
    "c6": value("COMPANY DESCRIPTION", "company_description", docx("COMPANY DESCRIPTION", ["COMPANY DESCRIPTION:", IMB])),
}
for key in sorted(got):
    print("%s -> %r" % (key, str(got[key])[-90:]))
r1 = 1 if str(got["r1"]).endswith("Jobs Act.") and "4_7_2026" not in str(got["r1"]) else 0
r2 = 1 if str(got["r2"]).endswith("mission-critical.") else 0
r3 = 1 if str(got["r3"]).endswith("come from.") else 0
c1 = 1 if str(got["c1"]).endswith(WHOLE) else 0
c2 = 1 if str(got["c2"]).endswith(DECIMAL) else 0
c3 = 1 if str(got["c3"]).endswith(BULLETS[-1]) and BULLETS[0] in str(got["c3"]) else 0
c4 = 1 if str(got["c4"]).endswith("Sell-side estimates kept") else 0
c5 = 1 if str(got["c5"]).endswith(SHOP[-1]) and SHOP[1] in str(got["c5"]) else 0
c6 = 1 if str(got["c6"]).endswith(IMB) else 0
print("ap6r build %d/3 control %d/6" % (r1 + r2 + r3, c1 + c2 + c3 + c4 + c5 + c6))
sys.exit(0)
