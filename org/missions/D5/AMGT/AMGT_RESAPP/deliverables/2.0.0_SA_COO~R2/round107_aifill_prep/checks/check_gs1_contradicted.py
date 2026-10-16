"""check_gs1_contradicted.py -- acceptance arms for AMGT-gs-1 (a CONTRADICTED sentence records the source that contradicted it and a verified quote).

  PYTHONPATH=<repo root> python check_gs1_contradicted.py
Offline: the model is a stub, the sources are hand-made dicts. Imports lib.research.aifill.grounding and contract (both merged). The row (AMGT_RESAPP-D1-W452-S1,
REMEDIATION_v44): a CONTRADICTED sentence is recorded with source null and quote null, so the record does not name the source that contradicted it. The remedy: the record
carries the contradicting source index and quote. A quote is checked mechanically (a run of at least 12 characters in the normalised full text of a SHOWN source), never trusted;
a contradicted sentence is dropped from the block text whatever its source or quote says.
"""
from __future__ import annotations

import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "round106_aifill_prep", "checks"))
import aifill_check_lib as L  # noqa: E402

NOW = datetime.datetime(2026, 10, 16, 6, 0, 0, tzinfo=datetime.timezone.utc)
S1 = ("Nestle announced that Philipp Navratil became Chief Executive Officer of Nestle S.A. in September 2025. He joined Nestle in 2001 as an international auditor.\n"
      "The Board of Directors elected Pablo Isla as Chairman in October 2025, earlier than anticipated, after Paul Bulcke stepped down.")
S2 = "Organic growth was 4.3 percent in 2025. The company targets savings of CHF 1 billion by the end of 2027, across four core business units."
TEXT = ("Philipp Navratil became chief executive in September 2025. He joined Nestle in 2001. Pablo Isla proposed to succeed as chairman in 2026. "
        "Organic growth was 4.3 percent in 2025. Momentum is largely organic.")
DEAD = "https://example.com/gone"
NESTLE = "https://www.nestle.com/leadership"
RESULTS = "https://example.com/results"
QUOTE = "elected Pablo Isla as Chairman in October 2025"


def src(url, text, status="OK", title="Page", kind="web", label=None, http=200):
    return {"kind": kind, "url": url, "label": label, "status": status, "http_status": http, "title": title, "text": text if status == "OK" else "",
            "chars": len(text) if status == "OK" else 0, "note": ""}


def verdicts(*rows):
    return json.dumps({"verdicts": [{"n": n, "verdict": v, "source": s, "quote": q} for n, v, s, q in rows]})


def main():
    from lib.research.aifill import contract, grounding

    arms = L.Arms("GS-1")
    # the first source did not answer, so it is not shown to the model: label S1 is list index 1, label S2 is list index 2
    srcs = lambda: [src(DEAD, "", status="NOT_FOUND", http=404), src(NESTLE, S1), src(RESULTS, S2)]  # noqa: E731

    def run(rows, text=TEXT):
        m = L.StubModel(L.result(verdicts(*rows)))
        return grounding.ground_block(text, srcs(), m, NOW), m

    def rows_with(contra):
        return [(1, "UNSUPPORTED", None, None), (2, "UNSUPPORTED", None, None), contra, (4, "SUPPORTED", "S2", "Organic growth was 4.3 percent in 2025"),
                (5, "UNSUPPORTED", None, None)]

    def third(r):
        return r.record["sentences"][2]

    def records_source_and_quote():
        r, _ = run(rows_with((3, "CONTRADICTED", "S1", QUOTE)))
        s = third(r)
        return s["verdict"] == "CONTRADICTED" and s["source"] == 1 and s["quote"] == QUOTE and "Pablo Isla" not in r.text, s
    arms.run("a CONTRADICTED sentence records the list index of the shown source and its quote; the sentence is dropped", records_source_and_quote)

    def spacing_and_case():
        q = "ELECTED  pablo isla as chairman, in October 2025"
        r, _ = run(rows_with((3, "CONTRADICTED", "S1", q)))
        s = third(r)
        return s["source"] == 1 and s["quote"] == q, s
    arms.run("the quote is checked with case, spacing and punctuation ignored, and recorded as the model gave it", spacing_and_case)

    def quote_not_in_source():
        r, _ = run(rows_with((3, "CONTRADICTED", "S1", "elected Paul Bulcke as Chairman in October 2026")))
        s = third(r)
        return s["verdict"] == "CONTRADICTED" and s["source"] is None and s["quote"] is None, s
    arms.run("a quote the source does not hold: still CONTRADICTED and dropped, source null and quote null", quote_not_in_source)

    def label_not_shown():
        r, _ = run(rows_with((3, "CONTRADICTED", "S9", QUOTE)))
        s = third(r)
        return s["verdict"] == "CONTRADICTED" and s["source"] is None and s["quote"] is None, s
    arms.run("a source label that was not shown: CONTRADICTED with source null and quote null", label_not_shown)

    def short_quote():
        r, _ = run(rows_with((3, "CONTRADICTED", "S1", "Pablo Isla")))
        s = third(r)
        return s["verdict"] == "CONTRADICTED" and s["source"] is None and s["quote"] is None, s
    arms.run("a quote shorter than 12 characters is not recorded", short_quote)

    def no_source_given():
        r, _ = run(rows_with((3, "CONTRADICTED", None, None)))
        s = third(r)
        return s["verdict"] == "CONTRADICTED" and s["source"] is None and s["quote"] is None, s
    arms.run("a CONTRADICTED row with no source and no quote keeps today's record", no_source_given)

    def not_a_supporter():
        r, _ = run(rows_with((3, "CONTRADICTED", "S1", QUOTE)))
        return r.used_urls == [RESULTS] and [k["source"] for k in r.kept] == [2], (r.used_urls, [k["source"] for k in r.kept])
    arms.run("a contradicting source is not a supporting source: not in used_urls, not in kept", not_a_supporter)

    def unsupported_leaks_nothing():
        rows = rows_with((3, "UNSUPPORTED", "S1", QUOTE))
        r, _ = run(rows)
        s = third(r)
        return s["verdict"] == "UNSUPPORTED" and s["source"] is None and s["quote"] is None, s
    arms.run("an UNSUPPORTED row that carries a source and a quote still records null and null", unsupported_leaks_nothing)

    def system_asks_for_it():
        _, m = run(rows_with((3, "CONTRADICTED", "S1", QUOTE)))
        system = m.calls[0]["system"]
        return system.startswith("You check sentences against sources.") and "For each CONTRADICTED verdict give the source label" in system, system[-160:]
    arms.run("the system prompt still begins with its words and asks for the source label and quote of a CONTRADICTED verdict", system_asks_for_it)

    def contract_accepts():
        r, _ = run(rows_with((3, "CONTRADICTED", "S1", QUOTE)))
        return contract._record_shape_problems(r.record) == [], contract._record_shape_problems(r.record)
    arms.run("the contract accepts a record whose CONTRADICTED sentence carries a source and a quote", contract_accepts)

    def ascii_only():
        b = open(grounding.__file__, "rb").read()
        return b.isascii() and b"import anthropic" not in b and b"import boto3" not in b, "non-ASCII or a forbidden import"
    arms.run("grounding.py stays ASCII with no network import", ascii_only)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
