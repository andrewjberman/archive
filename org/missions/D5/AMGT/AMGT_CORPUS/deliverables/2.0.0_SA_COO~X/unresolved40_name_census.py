"""AMGT_CORPUS -- the 40 identity-unresolved folders: what do their OWN documents say, and this seat's CALL per folder.

Andrew-direct 2026-09-24 ~16:5xZ ("2 just go look right now and make a call, if unsure look at some of the docs and try
to find a ticker"; record ANDREW_DIRECT_20260924_165xZ_LOOK_AT_THE_40_AND_MAKE_A_CALL.md). CTO R-77 named the measurement:
does any of the 40 carry a usable company name / ticker in a readable artifact? Bounded at 40 folders, NO vendor call, NO
build, NO store write.

READ-ONLY over the library (C-CORPUS-READ-ONLY): files opened "rb" only through the project's own readers
(library.census for the listing, extract.extract for docx/pdf/xlsx text). Registers nothing; the CALL column is a MEASURED
table the round-3 cut consumes, never an identity written anywhere.

  PYTHONPATH="$(pwd)" python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/unresolved40_name_census.py
"""
import collections
import datetime
import json
import os
import re
import sys

from lib.research.corpus import backlog, extract, induction_run, library

OUT_DIR = os.path.join("org", "missions", "D5", "AMGT", "AMGT_CORPUS", "deliverables", "2.0.0_SA_COO~X")
READ_EXTS = (".docx", ".pdf", ".xlsx")
MAX_FILES_PER_FOLDER = 10

CC = ("US|LN|FP|GY|GR|SW|IM|SM|NA|JP|HK|MM|BZ|CN|AU|FH|PM|IN|TT|SP|NL|TB|KS|CH|PL|DC|SS|NO|SJ|MK|ID|CT|CI|ES|BB|IT|LI|VX"
      "|SE|AV|PW|PA|ME|GA|BE|IJ|KQ|TW|SQ|AR|IR|NZ|PE|UH")
RE_EQUITY = re.compile(r"\b([A-Z][A-Z0-9]{0,7}(?:/[A-Z])?\*?)\s+(%s)\s+Equity\b" % CC)
RE_ROOT_CC = re.compile(r"\b([A-Z][A-Z0-9]{1,7}\*?)\s+(%s)\b(?!\s*[a-z])" % CC)
RE_TICKER_LABEL = re.compile(r"\(Ticker:\s*([^)\n]{1,40})\)")
RE_TICKER_WORD = re.compile(r"\bTicker\s*[:\-]\s*([A-Z0-9./\-]{1,10}(?:\s+[A-Z]{2})?)")
RE_EXCH = re.compile(r"\b(NYSE|NASDAQ|Nasdaq|LSE|TSX|ASX|HKEX|SIX|BMV|B3|Euronext|XETRA|Xetra)\s*[:\-]\s*([A-Z0-9.]{1,8})\b")
EXCH_CC = {"NYSE": "US", "NASDAQ": "US", "Nasdaq": "US", "LSE": "LN", "TSX": "CN", "ASX": "AU", "HKEX": "HK", "SIX": "SW",
           "BMV": "MM", "B3": "BZ", "Euronext": None, "XETRA": "GR", "Xetra": "GR"}
NOISE_ROOTS = {"THE", "AND", "FOR", "USD", "EUR", "GBP", "CHF", "JPY", "HKD", "MXN", "BRL", "CAD", "AUD", "EPS", "FCF", "EV",
               "PE", "PB", "ROE", "ROIC", "DPS", "CAGR", "YTD", "LTM", "NTM", "FY", "Q", "H", "MM", "BN", "K", "M", "B", "T"}


def _snippet(text, start, end, pad=70):
    a = max(0, start - pad)
    b = min(len(text), end + pad)
    return re.sub(r"\s+", " ", text[a:b]).strip()


def _blocks(document):
    if "paragraphs" in document:
        return [("docx paragraph %d" % i, p.get("text") or "") for i, p in enumerate(document["paragraphs"])]
    if "pages" in document:
        return [("pdf page %d" % i, t or "") for i, t in enumerate(document["pages"])]
    if "sheet_data" in document:
        out = []
        for sd in document["sheet_data"]:
            labels = sd.get("labels") or []
            out.append(("xlsx sheet %r labels" % sd.get("name"), "\n".join(str(x) for x in labels)))
        return out
    return []


def _company_name_guess(document, ext):
    heads = document.get("headings") or []
    for h in heads:
        t = (h.get("text") or "").strip()
        if 3 <= len(t) <= 80 and not t.isupper():
            return t
    if "paragraphs" in document:
        for p in document["paragraphs"]:
            t = (p.get("text") or "").strip()
            if 3 <= len(t) <= 80:
                return t
    if "pages" in document and document["pages"]:
        first = re.sub(r"\s+", " ", (document["pages"][0] or "")).strip()
        return first[:80] if first else None
    return None


def scan_folder(root, folder, files):
    evidence = []
    names = []
    read = 0
    unreadable = 0
    for e in sorted(files, key=lambda x: (x["ext"] not in (".docx", ".pdf"), -x["size"]))[:MAX_FILES_PER_FOLDER]:
        if e["ext"] not in READ_EXTS:
            continue
        full = os.path.join(root, e["path"].replace("/", os.sep))
        try:
            with open(full, "rb") as fh:
                body = fh.read()
        except OSError as exc:
            unreadable += 1
            evidence.append({"file": e["path"], "kind": "open-error", "value": "%s: %s" % (exc.__class__.__name__, exc)})
            continue
        doc = extract.extract("local://%s/%s" % (folder, e["path"]), body, e["ext"].lstrip("."))
        if not doc.get("extractable"):
            unreadable += 1
            evidence.append({"file": e["path"], "kind": "not-extractable", "value": doc.get("reason") or doc.get("error")})
            continue
        read += 1
        nm = _company_name_guess(doc, e["ext"])
        if nm:
            names.append({"file": e["path"], "name": nm})
        for locator, text in _blocks(doc):
            for m in RE_TICKER_LABEL.finditer(text):
                evidence.append({"file": e["path"], "locator": locator, "kind": "ticker-label", "value": m.group(1).strip(),
                                 "snippet": _snippet(text, m.start(), m.end())})
            for m in RE_EQUITY.finditer(text):
                if m.group(1) in NOISE_ROOTS:
                    continue
                evidence.append({"file": e["path"], "locator": locator, "kind": "root-cc-equity",
                                 "value": "%s %s" % (m.group(1), m.group(2)), "snippet": _snippet(text, m.start(), m.end())})
            for m in RE_TICKER_WORD.finditer(text):
                evidence.append({"file": e["path"], "locator": locator, "kind": "ticker-word", "value": m.group(1).strip(),
                                 "snippet": _snippet(text, m.start(), m.end())})
            for m in RE_EXCH.finditer(text):
                cc = EXCH_CC.get(m.group(1))
                evidence.append({"file": e["path"], "locator": locator, "kind": "exchange-prefix",
                                 "value": "%s %s" % (m.group(2), cc) if cc else "%s (%s)" % (m.group(2), m.group(1)),
                                 "snippet": _snippet(text, m.start(), m.end())})
    return evidence, names, read, unreadable


def make_call(folder, record, evidence, names, files):
    """(call, confidence, basis) -- this seat's call from the folder's own documents plus the folder's own name."""
    pair = induction_run.parse_folder_token(folder)
    folder_call = "%s %s" % pair if pair else None
    counts = collections.Counter()
    for ev in evidence:
        if ev.get("kind") in ("root-cc-equity", "ticker-label", "exchange-prefix"):
            v = ev["value"].replace(" Equity", "").strip()
            counts[v] += 1
    doc_calls = [v for v, _ in counts.most_common() if len(v.split()) == 2 and v.split()[0] not in NOISE_ROOTS]

    if record.get("state") == "AMBIGUOUS":
        cands = record.get("candidates") or []
        return ("SAME SECURITY AS EXISTING %s" % (", ".join(cands) if cands else "(see reason)"),
                "HIGH", "the resolver's own candidate already resolves to an existing key; the folder is that security -- an "
                "ENRICH (folder association), never a second record")
    if doc_calls and folder_call and doc_calls[0] == folder_call:
        return doc_calls[0], "HIGH", "folder token and %d document mention(s) agree" % counts[doc_calls[0]]
    if doc_calls and folder_call and doc_calls[0].split()[1] == folder_call.split()[1] and doc_calls[0] != folder_call:
        return doc_calls[0], "DOC-OVER-FOLDER", ("the documents state %s (%d mention(s)) while the folder name reads %s; the "
                                                 "document is the team's evidence" % (doc_calls[0], counts[doc_calls[0]], folder_call))
    if doc_calls and not folder_call:
        return doc_calls[0], "MEDIUM", "document evidence only (%d mention(s)); the folder name carries no token pair" % counts[doc_calls[0]]
    if doc_calls and folder_call:
        return doc_calls[0], "MEDIUM", ("document evidence %s (%d) does not match the folder token %s; the document wins, "
                                        "flagged" % (doc_calls[0], counts[doc_calls[0]], folder_call))
    if folder_call:
        return folder_call, "LOW", "folder name only -- no document states a ticker (%d readable file(s))" % len(files)
    if names:
        return "NONE (name only: %s)" % names[0]["name"], "NONE", "a company name reads but no ticker anywhere"
    return "NONE", "NONE", "no readable artifact carries a name or ticker (%d file(s))" % len(files)


def main():
    root = library.library_root()
    entries = library.census(root)
    by_folder = collections.defaultdict(list)
    for e in entries:
        if e["folder"]:
            by_folder[e["folder"]].append(e)
    latest = backlog.read_latest()
    unresolved = [r for r in latest["records"] if r["state"] != backlog.STATE_RESOLVED]
    rows = []
    for r in sorted(unresolved, key=lambda x: x["folder"]):
        folder = r["folder"]
        files = by_folder.get(folder, [])
        ext_counts = collections.Counter(e["ext"] for e in files)
        evidence, names, read, unreadable = scan_folder(root, folder, files)
        call, conf, basis = make_call(folder, r, evidence, names, files)
        rows.append({
            "folder": folder, "state_before": r["state"], "reason_before": (r.get("reason") or "")[:160],
            "files": len(files), "files_by_ext": dict(ext_counts), "files_read": read, "files_unreadable": unreadable,
            "company_name_guess": names[0]["name"] if names else None,
            "evidence": evidence[:12], "evidence_total": len(evidence),
            "call": call, "confidence": conf, "basis": basis,
        })
    conf_counts = collections.Counter(x["confidence"] for x in rows)
    totals = {
        "folders": len(rows),
        "called_high": conf_counts.get("HIGH", 0),
        "called_doc_over_folder": conf_counts.get("DOC-OVER-FOLDER", 0),
        "called_medium": conf_counts.get("MEDIUM", 0),
        "called_low_folder_only": conf_counts.get("LOW", 0),
        "none": conf_counts.get("NONE", 0),
    }
    totals["sum"] = sum(v for k, v in totals.items() if k not in ("folders",))
    stamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    doc = {"as_of": stamp, "library_root": root, "backlog_vintage_records": len(latest["records"]), "totals": totals, "rows": rows}
    jpath = os.path.join(OUT_DIR, "UNRESOLVED40_NAME_CENSUS_%s.json" % stamp)
    with open(jpath, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    line = ("folders %d called_high %d called_doc_over_folder %d called_medium %d called_low_folder_only %d none %d sum %d"
            % (totals["folders"], totals["called_high"], totals["called_doc_over_folder"], totals["called_medium"],
               totals["called_low_folder_only"], totals["none"], totals["sum"]))
    print(line)
    for x in rows:
        print("%-45s | %-11s | %-14s | %-32s | files %d read %d | %s" % (x["folder"][:45], x["state_before"], x["confidence"],
                                                                        x["call"][:32], x["files"], x["files_read"], x["basis"][:90]))
    print(line)
    print("written", jpath)
    return 0


if __name__ == "__main__":
    sys.exit(main())
