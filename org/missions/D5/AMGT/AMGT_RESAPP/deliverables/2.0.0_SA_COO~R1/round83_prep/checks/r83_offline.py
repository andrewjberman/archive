"""AMGT_RESAPP round-83 PREP (DRAFT, not issued) -- an OFFLINE ASML NA re-analysis reaches Item 4.B (row AMGT_RESAPP-D1-W324-S1).

  python r83_offline.py --crit AC1 --analysis <analysis.json> --draft <drafting.json> [--excerpt <silver part | source json | text>]

Grades a re-analysis a worker produced WITHOUT any store write (analyze.py without --write-pool, objects written with --out-dir;
round83_prep/GROUP_PASSAGE_NOTES.md "The offline run"). Reads two local files and, optionally, the excerpt. No model call, no write.

AC1:
  O1  at least one SERVED sentence (draft `sections[].sentences[]`) cites a passage inside Item 4.B: the evidence id's passage
      (analysis `passage_map`) starts inside the Item 4.B band of the excerpt, by offset (--excerpt), else by the passage's
      `location` prefix.
  O2  every served sentence passes the drafting pipeline's own verbatim gate, re-run in-process
      (lib.research.drafting.verbatim.check_against_sources over pipeline.passage_texts_for the draft's evidence records).
  O3  served, held and refused counts printed over sentences drafted, and refused < served.
Verdict: R83 OFFLINE AC1: YES|NO (exit 0|1). Base (the rolled-back round-82 objects, analysis X5YQ7V, draft MZN0U0Q6): NO.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys

KEY = "ASML_NA_Equity"
BUSINESS = re.compile(r"item\s*4\s*\.?\s*b\b", re.I)


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _excerpt(path):
    """(text, labels) from a silver part (.parquet), a source object (.json) or a plain text file (labels None)."""
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq

        rows = pq.read_table(io.BytesIO(open(path, "rb").read())).to_pylist()
        row = [r for r in rows if r.get("security_key") == KEY][0]
        ex = json.loads(row["object_json"])["excerpt"]
        return ex["text"], ex.get("items")
    if path.endswith(".json"):
        ex = _load(path)["excerpt"]
        return ex["text"], ex.get("items")
    return open(path, encoding="utf-8").read(), None


def _business_band(text, labels):
    """(start, end) of Item 4.B: from its heading line to the next item heading line."""
    heads = []
    offset = 0
    wanted = [x.strip().upper() for x in (labels or [])]
    for line in text.split("\n"):
        s = line.strip().upper()
        if (wanted and s in wanted) or (not wanted and re.match(r"ITEM\s+\d+\.", s)):
            heads.append((s, offset))
        offset += len(line) + 1
    for i, (head, start) in enumerate(heads):
        if BUSINESS.match(head):
            return start, heads[i + 1][1] if i + 1 < len(heads) else len(text)
    return None


def crit_ac1(analysis_path, draft_path, excerpt_path):
    root = _root()
    if root and root not in sys.path:
        sys.path.insert(0, root)
    from lib.research.drafting import pipeline, verbatim

    analysis, draft = _load(analysis_path), _load(draft_path)
    passages = {p["id"]: p for p in analysis.get("passage_map") or []}
    band = None
    if excerpt_path:
        text, labels = _excerpt(excerpt_path)
        band = _business_band(text, labels)
        print("excerpt chars %d, Item 4.B band %s" % (len(text), band))

    def in_business(pid):
        p = passages.get(pid)
        if p is None:
            return False
        if band is not None:
            return band[0] <= p["start"] < band[1]
        return bool(BUSINESS.match(p.get("location") or ""))

    indexed = {r["id"]: r for r in draft.get("evidence_records") or []}
    served = [(sec.get("section"), s) for sec in draft.get("sections") or [] for s in sec.get("sentences") or []]
    print("passages %d (Item 4.B %d), evidence records %d, served sentences %d" % (
        len(passages), sum(1 for pid in passages if in_business(pid)), len(indexed), len(served)))

    cites_business = 0
    gate_pass = 0
    for section, s in served:
        ev = list(s.get("evidence") or [])
        missing = [e for e in ev if e not in indexed]
        verdict = "REFUSE" if missing else verbatim.check_against_sources(
            s.get("quoted_spans") or [], pipeline.passage_texts_for(ev, indexed))
        biz = [e for e in ev if in_business(e)]
        cites_business += bool(biz)
        gate_pass += verdict == "PASS"
        print("   %-20s gate %-6s Item 4.B ids %-24s %s" % (section, verdict, ",".join(biz) or "-", (s.get("text") or "")[:70]))

    o1 = cites_business >= 1
    print("%s O1 served sentences citing Item 4.B: %d of %d" % ("PASS" if o1 else "FAIL", cites_business, len(served)))
    o2 = bool(served) and gate_pass == len(served)
    print("%s O2 served sentences passing the verbatim gate re-run in-process: %d of %d" % (
        "PASS" if o2 else "FAIL", gate_pass, len(served)))
    d = draft.get("denominators") or {}
    n_served, n_held, n_refused = d.get("served", len(served)), d.get("held_no_span"), d.get("refused")
    o3 = n_refused is not None and n_served is not None and n_refused < n_served
    print("%s O3 served %s held %s refused %s of %s drafted (refused < served)" % (
        "PASS" if o3 else "FAIL", n_served, n_held, n_refused, d.get("sentences_drafted")))
    ok = o1 and o2 and o3
    print("R83 OFFLINE AC1: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--analysis", required=True)
    ap.add_argument("--draft", required=True)
    ap.add_argument("--excerpt", default=None)
    a = ap.parse_args()
    sys.exit(crit_ac1(a.analysis, a.draft, a.excerpt))


if __name__ == "__main__":
    main()
