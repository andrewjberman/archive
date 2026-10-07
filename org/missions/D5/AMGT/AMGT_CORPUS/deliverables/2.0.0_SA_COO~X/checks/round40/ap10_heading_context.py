"""AMGT_CORPUS round 40, CRPS-ap-10 (d) -- what follows a bare section heading in the source document.

Read-only (S3 reads of the stored extractions; writes nothing). For each `<security_key>:<field>` on the command line it prints
the picked report (class A first), the section's lead line and the next items of the document, each with its bold flag (docx)
or page (pdf), and where the block reader stops. It answers one question for the short-passage census: does the report carry
text under a heading the dossier serves alone?

  python ap10_heading_context.py TSM_US_Equity:positives 8306_JP_Equity:management ...     (PYTHONPATH=. from the root)
"""
import sys

import boto3

from lib.research.corpus import dossier

AFTER = 6


def show(security_key, field, client):
    names = dossier.SECTION_FIELD_NAMES[field]
    _items_raw, pick_a, pick_b = dossier._picked_reports(security_key, client)
    for label, pick in (("A", pick_a), ("B", pick_b)):
        if pick is None:
            print("%s %s class %s: no report" % (security_key, field, label))
            continue
        row, document = pick
        lead = dossier._find_section_lead(document, names)
        report = str(row.get("bronze_key", "")).rsplit("/", 1)[-1]
        if lead is None:
            print("%s %s class %s (%s): no lead in %s" % (security_key, field, label, report, list(names)[:2]))
            continue
        _locator, items = dossier._section_block_items(document, lead)
        doc_type = document.get("type")
        print("%s %s class %s (%s, %s): lead %r inline_remainder %r block_items %d" % (
            security_key, field, label, report, doc_type, lead.get("name"), lead.get("inline_remainder"), len(items)))
        if doc_type == "docx":
            paragraphs = document.get("paragraphs") or []
            start = lead["paragraph_index"]
            for i in range(start, min(len(paragraphs), start + 1 + AFTER)):
                p = paragraphs[i]
                text = (p.get("text") or "").strip()
                mark = "LEAD " if i == start else ("in   " if i < start + len(items) else "OUT  ")
                print("   %s[%d] bold=%s words=%d %r" % (mark, i, bool(p.get("bold")), len(text.split()), text[:110]))
        else:
            lines = document.get("lines") or []
            start = lead["line_index"]
            for i in range(start, min(len(lines), start + 1 + AFTER)):
                ln = lines[i]
                text = (ln.get("text") or "").strip()
                mark = "LEAD " if i == start else ("in   " if i < start + len(items) else "OUT  ")
                print("   %s[%d] page=%s size=%s bold=%s %r" % (mark, i, ln.get("page"), ln.get("size"), ln.get("bold"), text[:110]))


def main(argv):
    client = boto3.client("s3", region_name="us-east-1")
    for arg in argv[1:]:
        security_key, field = arg.split(":", 1)
        try:
            show(security_key, field, client)
        except Exception as exc:  # a name the reader cannot open is printed, never skipped
            print("%s %s ERROR %s: %s" % (security_key, field, type(exc).__name__, exc))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
