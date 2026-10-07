"""AMGT_CORPUS round 40 -- the served dossier citations by report type (1.0.0_SA_CTO~Z msg 31179, for the locator helper).

Read-only (S3 reads of the newest served dossier of every registered name, the pick the portal serves; writes nothing). It walks
each dossier for every `citation` object and counts them by the report key's file extension and by the SHAPE of the locator (a
whole number, or a string such as `<sheet>!label[<n>]`). No passage and no value is printed: counts, extensions and locator
shapes only, plus up to three example locators per non-numeric shape.

  python ap3_citation_types.py        (PYTHONPATH=. from the repository root)
"""
import collections
import re
import sys

from lib.research.corpus import dossier
from lib.research.harvest import store


def walk(node, path, out):
    if isinstance(node, dict):
        cite = node.get("citation")
        if isinstance(cite, dict):
            out.append((path, cite))
        for key, value in node.items():
            walk(value, path + [str(key)], out)
    elif isinstance(node, list):
        for value in node:
            walk(value, path, out)


def locator_shape(locator):
    if isinstance(locator, bool) or locator is None:
        return "none"
    if isinstance(locator, int):
        return "whole number"
    text = str(locator)
    if re.fullmatch(r"\d+", text):
        return "whole number (as text)"
    if re.fullmatch(r".+!label\[\d+\]", text):
        return "<sheet>!label[<n>]"
    return "other text"


def main():
    client = store._default_client()
    keys = dossier._resolved_security_keys(client=client)
    by_ext = collections.Counter()
    by_shape = collections.Counter()
    cross = collections.Counter()
    by_field = collections.Counter()
    examples = collections.defaultdict(list)
    read = unread = cites = 0
    for key in keys:
        try:
            document = dossier.read_dossier(key, client=client)["document"]
        except LookupError:
            unread += 1
            continue
        read += 1
        found = []
        walk(document, [], found)
        for path, cite in found:
            cites += 1
            report = str(cite.get("report_key") or "")
            ext = report.rsplit(".", 1)[-1].lower() if "." in report.rsplit("/", 1)[-1] else "(no extension)"
            shape = locator_shape(cite.get("locator"))
            by_ext[ext] += 1
            by_shape[shape] += 1
            cross[(ext, shape)] += 1
            field = path[-1] if path else "(root)"
            if ext not in ("docx", "pdf"):
                by_field[(ext, field)] += 1
            if shape not in ("whole number", "whole number (as text)") and len(examples[shape]) < 3:
                examples[shape].append(str(cite.get("locator"))[:60])
    print("names %d dossiers_read %d unread %d citations %d" % (len(keys), read, unread, cites))
    print("by report type: %s" % "; ".join("%s %d" % kv for kv in sorted(by_ext.items(), key=lambda kv: -kv[1])))
    print("by locator shape: %s" % "; ".join("%s %d" % kv for kv in sorted(by_shape.items(), key=lambda kv: -kv[1])))
    for (ext, shape), n in sorted(cross.items(), key=lambda kv: -kv[1]):
        print("  %-16s %-28s %d" % (ext, shape, n))
    if by_field:
        print("citations to a report that is neither docx nor pdf, by field:")
        for (ext, field), n in sorted(by_field.items(), key=lambda kv: -kv[1]):
            print("  %-10s %-34s %d" % (ext, field, n))
    for shape, items in examples.items():
        print("example locators, shape %s: %s" % (shape, " | ".join(items)))
    not_docx_pdf = sum(n for ext, n in by_ext.items() if ext not in ("docx", "pdf"))
    print("citations the helper words as `Location <n> in the report` (neither docx nor pdf): %d of %d" % (not_docx_pdf, cites))
    return 0


if __name__ == "__main__":
    sys.exit(main())
