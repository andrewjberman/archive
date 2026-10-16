"""check_gv1_round110.py -- acceptance arms for AMGT-gv-1 (AIFILL round 110: the CVO's inert quality rows C-S160 and the CTO's generic rule).

  PYTHONPATH=<repo root> python check_gv1_round110.py
Offline, stdlib only; the model and the fetcher are stubs. Four mechanisms, each with a control that passes at the base:
  (a) the specifics check must not withhold a name that carries a diacritic (SAN's naming sentence: Belen Garijo Lopez), nor read the pack text
      with its non-ASCII characters escaped;
  (b) a sentence that only describes its source ("the headline says nothing about ...") is not kept (CTO 6620 item (2)(1));
  (c) an OPAL_SOURCE management bio that only restates the pack passage the page already shows is withheld with a reason (round-106 rule (e));
  (d) a management bio that opens on an unnamed pronoun is withheld with a reason.
"""
from __future__ import annotations

import datetime
import json
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "round106_aifill_prep", "checks"))
import aifill_check_lib as L  # noqa: E402

NOW = datetime.datetime(2026, 10, 16, 10, 0, 0, tzinfo=datetime.timezone.utc)
URL = "https://example.com/leadership"
CALL = {"model": "claude-opus-5", "web_search_requests": 2, "input_tokens": 100, "output_tokens": 50}
INPUTS = {"overlay": None, "thesis": {"dossier_fields": {"management": None}}, "errors": {}}


def src(url, text):
    return {"kind": "web", "url": url, "label": None, "status": "OK", "http_status": 200, "title": "Page", "text": text, "chars": len(text)}


def numbered(prompt):
    out, seen = [], False
    for line in prompt.splitlines():
        if line.strip() == "SENTENCES":
            seen = True
            continue
        if seen and ". " in line:
            head, _, rest = line.partition(". ")
            if head.isdigit():
                out.append((int(head), rest))
    return out


class Model(object):
    """Grounding calls only: every sentence whose text starts with a key gets SUPPORTED on S1 with the quote given for that key."""

    def __init__(self, quotes):
        self.quotes, self.calls = quotes, []

    def __call__(self, prompt, *, system=None, web_search_max_uses=0, max_tokens=1500):
        self.calls.append(prompt)
        rows = []
        for n, text in numbered(prompt):
            quote = next((q for key, q in self.quotes.items() if text.startswith(key)), None)
            rows.append({"n": n, "verdict": "SUPPORTED" if quote else "UNSUPPORTED", "source": "S1" if quote else None, "quote": quote})
        return types.SimpleNamespace(text=json.dumps({"verdicts": rows}), model="stub-ground", input_tokens=10, output_tokens=5)


def main():
    from lib.research.aifill import contract, grounding, orchestrate

    arms = L.Arms("GV-1")

    def ground(sentence, page, quote):
        return grounding.ground_block(sentence, [src(URL, page)], Model({sentence[:18]: quote}), NOW)

    # ---- (a) the diacritic false drop --------------------------------------------------------------------------------
    garijo = "Belen Garijo Lopez was appointed chief executive of Sanofi in February 2026."
    page_accents = "Belén Garijo López was appointed chief executive of Sanofi in February 2026, after the ouster of Paul Hudson."
    q_garijo = "Belén Garijo López was appointed chief executive of Sanofi in February 2026"

    def accent_kept():
        res = ground(garijo, page_accents, q_garijo)
        return res.record["sentences"][0]["verdict"] == "SUPPORTED" and res.text == garijo, res.record["sentences"][0]["verdict"]
    arms.run("diacritic: a name with accents in the page matches its ASCII-folded sentence", accent_kept)

    def pack_text_not_escaped():
        draft = {"opal_inputs": ["thesis.dossier_fields.management"], "citations": [{"source_kind": "opal", "ref": "Research team pack"}]}
        served = {"thesis": {"dossier_fields": {"management": "Belén Garijo López leads Sanofi."}}}
        text = orchestrate._opal_sources(draft, served)[0]["text"]
        return "Belén" in text and "\\u00e9" not in text, text[:60]
    arms.run("diacritic: the pack text built for an OPAL source keeps its characters, not \\uXXXX escapes", pack_text_not_escaped)

    def absent_name_still_drops():
        sent = "The deals were funded by investors including Apollo and Temasek."
        res = ground(sent, "Jacobs firm has spent around $30 billion buying Beacon and Kodiak.", "Jacobs firm has spent around $30 billion buying Beacon and Kodiak")
        return res.record["sentences"][0]["verdict"] == "UNSUPPORTED", res.record["sentences"][0]["verdict"]
    arms.run("diacritic: control -- a name absent from the source still drops the sentence", absent_name_still_drops)

    # ---- (b) a sentence about the source ----------------------------------------------------------------------------------
    headline_page = "A Bloomberg headline reports that Bavarian Nordic named a former Sanofi executive as its chief executive."
    talk = "The headline says nothing about Sanofi's current management team."

    def source_talk_dropped():
        res = ground(talk, headline_page + " " + talk, "The headline says nothing about Sanofi's current management team")
        return res.record["sentences"][0]["verdict"] == "UNSUPPORTED" and res.kept == [], res.record["sentences"][0]["verdict"]
    arms.run("source talk: a sentence that only describes its source is not kept", source_talk_dropped)

    def fact_sentence_kept():
        sent = "Sanofi named a new chief executive in February 2026."
        res = ground(sent, "Sanofi named a new chief executive in February 2026 after a board review.", "Sanofi named a new chief executive in February 2026")
        return res.record["sentences"][0]["verdict"] == "SUPPORTED", res.record["sentences"][0]["verdict"]
    arms.run("source talk: control -- a sentence stating a fact about the company stays SUPPORTED", fact_sentence_kept)

    arms.run("source talk: the grounding prompt names the rule", lambda: ("only describes what a source says" in grounding.SYSTEM, ""))

    # ---- (c) an OPAL bio that only restates the pack -------------------------------------------------------------------------
    pack = ("Kristin Peck has served as chief executive of Zoetis since 2020 and brings more than 20 years of experience in life sciences "
            "and animal health. She sits on the boards of Blackrock and the Mayo Clinic.")
    pack_sents = ["Kristin Peck has served as chief executive of Zoetis since 2020 and brings more than 20 years of experience in life sciences and animal health.",
                  "She sits on the boards of Blackrock and the Mayo Clinic."]

    def opal_draft(text):
        cite = {"source_kind": "opal", "ref": "Research team pack", "url": None, "title": None, "quote": None}
        return lambda ctx: contract.make_block("mgmt_bio", "OPAL_SOURCE", text, [cite], ["thesis.dossier_fields.management"], None, require_grounding=False)

    def none_b(block_id):
        return lambda ctx: contract.none_block(block_id, "Nothing here.")

    def build_one(block_id, draft, model, inputs=None, **kw):
        builders = {b: none_b(b) for b in contract.BLOCK_IDS}
        builders[block_id] = draft
        return orchestrate.build_document("ZTS_US_Equity", inputs or INPUTS, model, now=NOW, builders=builders, fetch=lambda u: src(u, ""), ground=True, **kw)

    pack_inputs = {"overlay": None, "thesis": {"dossier_fields": {"management": pack}}, "errors": {}}

    def restated_withheld():
        quotes = {pack_sents[0][:18]: pack_sents[0][:150], pack_sents[1][:18]: pack_sents[1]}
        doc = build_one("mgmt_bio", opal_draft(" ".join(pack_sents)), Model(quotes), pack_inputs)
        blk = doc["blocks"]["mgmt_bio"]
        reason = getattr(orchestrate, "RESTATES_REASON", None)
        return blk["source_class"] == "NONE" and reason is not None and blk["reason"] == reason, blk.get("reason")
    arms.run("restatement: an OPAL bio that repeats the pack passage is withheld with the restatement reason", restated_withheld)

    def paraphrase_kept():
        text = "Peck leads Zoetis, the animal health company, and has held the post for six years."
        doc = build_one("mgmt_bio", opal_draft(text), Model({"Peck leads Zoetis": "has served as chief executive of Zoetis since 2020"}), pack_inputs)
        blk = doc["blocks"]["mgmt_bio"]
        return blk["source_class"] == "OPAL_SOURCE" and blk["text"] == text, blk.get("reason")
    arms.run("restatement: control -- a bio that says it in its own words is kept", paraphrase_kept)

    def web_bio_not_checked_for_restatement():
        cite = {"source_kind": "web", "url": URL, "title": "T", "quote": "q", "ref": None}
        text = pack_sents[0]
        draft = lambda ctx: contract.make_block("mgmt_bio", "WEB_SEARCH", text, [cite], [], CALL, require_grounding=False)  # noqa: E731
        doc = build_one("mgmt_bio", draft, Model({text[:18]: text[:150]}), pack_inputs, recency=False)
        return doc["blocks"]["mgmt_bio"]["source_class"] in ("WEB_SEARCH", "NONE"), doc["blocks"]["mgmt_bio"]["source_class"]
    arms.run("restatement: control -- the rule is for OPAL_SOURCE bios only (a web bio is not tested against the pack)", web_bio_not_checked_for_restatement)

    # ---- (d) a bio that opens on a pronoun ---------------------------------------------------------------------------------------
    leadership = "He joined the company in 2001 as an auditor. Jane Roe became chief executive in 2020."

    def web_draft(block_id, text):
        cite = {"source_kind": "web", "url": URL, "title": "T", "quote": "q", "ref": None}
        return lambda ctx: contract.make_block(block_id, "WEB_SEARCH", text, [cite], [], CALL, require_grounding=False)

    def build_web(block_id, text, quotes):
        builders = {b: none_b(b) for b in contract.BLOCK_IDS}
        builders[block_id] = web_draft(block_id, text)
        return orchestrate.build_document("ZTS_US_Equity", INPUTS, Model(quotes), now=NOW, builders=builders,
                                          fetch=lambda u: src(u, leadership), ground=True, recency=False)

    def pronoun_withheld():
        doc = build_web("mgmt_bio", "He joined the company in 2001 as an auditor.", {"He joined": "He joined the company in 2001 as an auditor"})
        blk = doc["blocks"]["mgmt_bio"]
        reason = getattr(orchestrate, "UNNAMED_REASON", None)
        return blk["source_class"] == "NONE" and reason is not None and blk["reason"] == reason, blk.get("reason")
    arms.run("pronoun: a bio whose kept text opens on He or She is withheld with the unnamed reason", pronoun_withheld)

    def named_opening_kept():
        text = "Jane Roe became chief executive in 2020."
        blk = build_web("mgmt_bio", text, {"Jane Roe": "Jane Roe became chief executive in 2020"})["blocks"]["mgmt_bio"]
        return blk["source_class"] == "WEB_SEARCH" and blk["text"] == text, blk.get("reason")
    arms.run("pronoun: control -- a bio that opens on a name is kept", named_opening_kept)

    def recent_not_affected():
        text = "He joined the company in 2001 as an auditor."
        blk = build_web("mgmt_recent", text, {"He joined": "He joined the company in 2001 as an auditor"})["blocks"]["mgmt_recent"]
        return blk["source_class"] == "WEB_SEARCH" and blk["text"] == text, blk.get("reason")
    arms.run("pronoun: control -- the rule is for management bios only", recent_not_affected)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
