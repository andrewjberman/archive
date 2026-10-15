"""IRPT_ANLREQ workstream ~G read-cell checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g_read_checks.py shape53 <record.json>   the C-SWITCH design record has every key, enum and evidence list
    python ar_g_read_checks.py shape54 <record.json>   the engine compose record has every key, enum and evidence list
    python ar_g_read_checks.py cite <record.json>      every {file, line, text} of the record re-opens and matches

shape prints SHAPE-OK <n keys> / SHAPE-BAD <why>; cite prints CITES-OK <n> of <n> / CITES-BAD <file>:<line> (the denominator
is every cite in the record). rc 0 only on OK. ASCII only.
"""
import json
import os
import sys

YNU = ("yes", "no", "unknown")


def repo_root():
    d = os.getcwd()
    while True:
        if os.path.isdir(os.path.join(d, "org")) and os.path.isdir(os.path.join(d, ".tools")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def is_cite(c):
    return isinstance(c, dict) and isinstance(c.get("file"), str) and isinstance(c.get("line"), int) and isinstance(c.get("text"), str) and c["text"].strip() != ""


def cites_of(node, out=None):
    """Every dict that has file+line+text keys, wherever it sits in the record."""
    out = [] if out is None else out
    if isinstance(node, dict):
        if {"file", "line", "text"} <= set(node):
            out.append(node)
        for v in node.values():
            cites_of(v, out)
    elif isinstance(node, list):
        for v in node:
            cites_of(v, out)
    return out


def need(cond, why, bad):
    if not cond:
        bad.append(why)


def cite_list(v, why, bad, minimum=1):
    ok = isinstance(v, list) and len(v) >= minimum and all(is_cite(c) for c in v)
    need(ok, "%s needs >= %d cite(s) of {file, line, text}" % (why, minimum), bad)


def nonempty_str(v):
    return isinstance(v, str) and v.strip() != ""


def shape53(doc):
    bad = []
    for k in ("base", "cell", "q1", "q2", "q3", "q4", "recommendation", "not_read"):
        need(k in doc, "missing key " + k, bad)
    if bad:
        return bad
    need(nonempty_str(doc["base"]) and nonempty_str(doc["cell"]), "base and cell must be strings", bad)
    for qn in ("q1", "q2"):
        q = doc[qn]
        need(isinstance(q, dict), qn + " must be an object", bad)
        if not isinstance(q, dict):
            continue
        need(q.get("can_read_today") in YNU, qn + ".can_read_today must be one of yes|no|unknown", bad)
        for f in ("table", "key_shape", "type_marker", "owner_marker"):
            need(nonempty_str(q.get(f)), "%s.%s must be a non-empty string (say 'not found' plainly if it is)" % (qn, f), bad)
        cite_list(q.get("role_evidence"), qn + ".role_evidence", bad)
        cite_list(q.get("evidence"), qn + ".evidence", bad)
    q3 = doc["q3"]
    need(isinstance(q3, dict) and nonempty_str(q3.get("field")), "q3.field must be a non-empty string", bad)
    if isinstance(q3, dict):
        cite_list(q3.get("client_forbidden_evidence"), "q3.client_forbidden_evidence", bad)
        cite_list(q3.get("schema_evidence"), "q3.schema_evidence", bad)
        cite_list(q3.get("readers"), "q3.readers", bad)
    q4 = doc["q4"]
    need(isinstance(q4, dict), "q4 must be an object", bad)
    if isinstance(q4, dict):
        for shape in ("A", "B"):
            s = q4.get(shape)
            need(isinstance(s, dict), "q4.%s must be an object" % shape, bad)
            if not isinstance(s, dict):
                continue
            cite_list(s.get("files"), "q4.%s.files" % shape, bad)
            need(nonempty_str(s.get("iam_diff")), "q4.%s.iam_diff must be a non-empty string (NONE if none)" % shape, bad)
            need(isinstance(s.get("owner_seats"), list) and s["owner_seats"] and all(nonempty_str(x) for x in s["owner_seats"]),
                 "q4.%s.owner_seats must be a non-empty list of strings" % shape, bad)
            cite_list(s.get("pinning_tests"), "q4.%s.pinning_tests" % shape, bad, minimum=0)
        need(nonempty_str(q4.get("forgeability")), "q4.forgeability must be a non-empty string", bad)
    rec = doc["recommendation"]
    need(isinstance(rec, dict) and rec.get("shape") in ("A", "B", "NEITHER") and nonempty_str(rec.get("deciding_fact")),
         "recommendation needs shape A|B|NEITHER and a deciding_fact", bad)
    if isinstance(rec, dict):
        cite_list(rec.get("evidence"), "recommendation.evidence", bad)
    need(isinstance(doc["not_read"], list) and all(nonempty_str(x) for x in doc["not_read"]), "not_read must be a list of strings", bad)
    return bad


def shape54(doc):
    bad = []
    for k in ("base", "cell", "q1", "q2", "q3", "q4", "not_read"):
        need(k in doc, "missing key " + k, bad)
    if bad:
        return bad
    q1 = doc["q1"]
    need(isinstance(q1, dict), "q1 must be an object", bad)
    if isinstance(q1, dict):
        els = q1.get("elements")
        need(isinstance(els, list) and len(els) >= 3, "q1.elements needs >= 3 rows", bad)
        for i, e in enumerate(els if isinstance(els, list) else []):
            ok = isinstance(e, dict) and nonempty_str(e.get("family")) and nonempty_str(e.get("function")) and nonempty_str(e.get("input_shape"))
            need(ok, "q1.elements[%d] needs family, function, input_shape" % i, bad)
            if isinstance(e, dict):
                cite_list(e.get("evidence"), "q1.elements[%d].evidence" % i, bad)
        need(isinstance(q1.get("benchmark_symbols"), list), "q1.benchmark_symbols must be a list", bad)
        need("risk_free" in q1, "q1.risk_free must be present (null if none)", bad)
        need(nonempty_str(q1.get("series_contract")), "q1.series_contract must be a non-empty string", bad)
    q2 = doc["q2"]
    need(isinstance(q2, dict) and isinstance(q2.get("stores"), list), "q2.stores must be a list", bad)
    if isinstance(q2, dict) and isinstance(q2.get("stores"), list):
        names = {s.get("name") for s in q2["stores"] if isinstance(s, dict)}
        need({"demque_price_store", "opal_etf_bbg_history"} <= names, "q2.stores must name demque_price_store and opal_etf_bbg_history", bad)
        for i, s in enumerate(q2["stores"]):
            if not isinstance(s, dict):
                bad.append("q2.stores[%d] must be an object" % i)
                continue
            for f in ("address_builder_call", "key_form", "format", "symbol_key", "basis", "cross_firm_note"):
                need(nonempty_str(s.get(f)), "q2.stores[%d].%s must be a non-empty string (say 'not found' plainly)" % (i, f), bad)
            need(isinstance(s.get("columns"), list), "q2.stores[%d].columns must be a list" % i, bad)
            need(s.get("resident_can_read_today") in YNU, "q2.stores[%d].resident_can_read_today must be yes|no|unknown" % i, bad)
            cite_list(s.get("evidence"), "q2.stores[%d].evidence" % i, bad)
    q3 = doc["q3"]
    need(isinstance(q3, dict), "q3 must be an object", bad)
    if isinstance(q3, dict):
        maps = q3.get("maps")
        need(isinstance(maps, list) and len(maps) >= 2, "q3.maps needs >= 2 rows (the Overview and one more)", bad)
        for i, m in enumerate(maps if isinstance(maps, list) else []):
            ok = isinstance(m, dict) and nonempty_str(m.get("variant")) and nonempty_str(m.get("path")) and isinstance(m.get("needs_prices"), bool)
            need(ok, "q3.maps[%d] needs variant, path, needs_prices (bool)" % i, bad)
        sel = q3.get("selection")
        need(isinstance(sel, dict), "q3.selection must be an object", bad)
        if isinstance(sel, dict):
            cite_list(sel.get("evidence"), "q3.selection.evidence", bad)
        for f in ("today_for_variants_2_3", "smallest_change"):
            need(nonempty_str(q3.get(f)), "q3.%s must be a non-empty string" % f, bad)
    q4 = doc["q4"]
    need(isinstance(q4, dict), "q4 must be an object", bad)
    if isinstance(q4, dict):
        for seam in ("price_seam", "swap_seam", "pricing_flag_seam"):
            s = q4.get(seam)
            need(isinstance(s, dict), "q4.%s must be an object" % seam, bad)
            if isinstance(s, dict):
                cite_list(s.get("evidence"), "q4.%s.evidence" % seam, bad)
        cells = q4.get("round8_cells")
        need(isinstance(cells, list) and len(cells) >= 2, "q4.round8_cells needs >= 2 rows", bad)
        for i, c in enumerate(cells if isinstance(cells, list) else []):
            ok = (isinstance(c, dict) and nonempty_str(c.get("id")) and nonempty_str(c.get("summary"))
                  and isinstance(c.get("files"), list) and c["files"] and isinstance(c.get("edges"), list))
            need(ok, "q4.round8_cells[%d] needs id, summary, files (non-empty), edges (list)" % i, bad)
    need(isinstance(doc["not_read"], list) and all(nonempty_str(x) for x in doc["not_read"]), "not_read must be a list of strings", bad)
    return bad


def cite_check(doc, root):
    cases = cites_of(doc)
    n = len(cases)
    bad, cache = [], {}
    for c in cases:
        if not is_cite(c):
            bad.append("malformed:%s" % json.dumps(c)[:80])
            continue
        path = os.path.join(root, *c["file"].split("/"))
        if path not in cache:
            if os.path.isfile(path):
                with open(path, encoding="utf-8", errors="replace") as fh:
                    cache[path] = fh.read().split("\n")
            else:
                cache[path] = None
        lines = cache[path]
        if lines is None or not (1 <= c["line"] <= len(lines)):
            bad.append("%s:%s" % (c["file"], c["line"]))
            continue
        if c["text"].strip() not in lines[c["line"] - 1].strip():
            bad.append("%s:%s" % (c["file"], c["line"]))
    return n, bad


def main(argv):
    if len(argv) != 3 or argv[1] == "":
        print("usage: ar_g_read_checks.py shape53|shape54|cite <record.json>")
        return 2
    mode, path = argv[1], argv[2]
    try:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        print(("SHAPE-BAD " if mode.startswith("shape") else "CITES-BAD ") + "cannot read %s: %s" % (path, type(exc).__name__))
        return 1
    if mode in ("shape53", "shape54"):
        bad = shape53(doc) if mode == "shape53" else shape54(doc)
        if bad:
            print("SHAPE-BAD " + "; ".join(bad[:6]) + ("" if len(bad) <= 6 else " (+%d more)" % (len(bad) - 6)))
            return 1
        print("SHAPE-OK %s" % ",".join(sorted(doc)))
        return 0
    if mode == "cite":
        root = repo_root()
        if root is None:
            print("CITES-BAD no worktree root above %s" % os.getcwd())
            return 1
        n, bad = cite_check(doc, root)
        if n == 0:
            print("CITES-BAD the record carries no cites")
            return 1
        if bad:
            for b in bad:
                print("CITES-BAD " + b)
            print("CITES-BAD %d of %d cites missed" % (len(bad), n))
            return 1
        print("CITES-OK %d of %d" % (n, n))
        return 0
    print("usage: ar_g_read_checks.py shape53|shape54|cite <record.json>")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
