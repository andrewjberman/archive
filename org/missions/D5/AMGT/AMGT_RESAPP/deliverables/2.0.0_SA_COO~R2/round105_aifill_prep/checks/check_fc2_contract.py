"""check_fc2_contract.py -- acceptance arms for AMGT-fc-2 (the contract transliterates, refuses a dropped letter and refuses process narration).

  PYTHONPATH=<repo root> python check_fc2_contract.py
Offline. Imports lib.research.aifill.contract. The defects (CVO C-S133): 11 stored blocks opened with the model's narration ("I'll research this now."), and
"Nestle" was stored as "Nestl" (fold_text dropped the accented letter). The old check_fa1_contract.py must keep passing.
"""
from __future__ import annotations

import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402

OPAL = {"source_kind": "opal", "url": None, "title": None, "quote": None, "ref": "Company officer list"}


def main():
    from lib.research.aifill import contract

    arms = L.Arms("FC-2")
    fold = contract.fold_text

    cases = [("Nestlé", "Nestle"), ("Zürich", "Zurich"), ("São Paulo", "Sao Paulo"), ("François", "Francois"), ("Ørsted", "Orsted"),
             ("Straße", "Strasse"), ("Łódź", "Lodz"), ("Æther", "AEther"), ("Crème", "Creme"), ("İstanbul", "Istanbul"),
             ("Björk", "Bjork"), ("Nestlé SA", "Nestle SA"), ("café’s", "cafe's"), ("ﬁnance", "finance")]
    for raw, want in cases:
        arms.run("fold_text transliterates %r -> %r" % (raw.encode("ascii", "backslashreplace").decode(), want), lambda raw=raw, want=want: (fold(raw) == want, fold(raw)))

    arms.run("fold_text keeps the old punctuation mapping (quotes, dashes, euro)", lambda: (fold("“hi” – €5") == '"hi" - EUR 5' or fold("“hi” – €5") == '"hi" - EUR5', fold("“hi” – €5")))
    arms.run("fold_text output is always ASCII", lambda: (fold("aé中文жуαb").isascii(), fold("aé中文жуαb")))

    def dropped_api():
        folded, dropped = contract.fold_report("Toyota (トヨタ) and Nestlé")
        return folded.isascii() and "Nestle" in folded and len(dropped) == 3 and "ト" in dropped, (folded, dropped)
    arms.run("fold_report returns the folded text and the letters it could NOT transliterate", dropped_api)

    arms.run("fold_report: an accented Latin text drops nothing", lambda: (contract.fold_report("Nestlé Zürich")[1] == [], contract.fold_report("Nestlé Zürich")))

    def make(text):
        return contract.make_block("mgmt_bio", "OPAL_SOURCE", text, [OPAL])

    def translit_in_block():
        b = make("Nestlé appointed a new chief executive.")
        return b["text"] == "Nestle appointed a new chief executive." and contract.validate_block(b) == [], b["text"]
    arms.run("make_block stores the transliterated text (Nestle, not Nestl)", translit_in_block)

    def dropped_refused():
        try:
            make("Toyota (トヨタ) named a new chief executive.")
        except contract.ContractError as err:
            return "dropped" in str(err).lower(), str(err)[:100]
        return False, "accepted"
    arms.run("make_block REFUSES a text whose letters could not be transliterated, naming 'dropped'", dropped_refused)

    def punctuation_not_refused():
        return make("He said “yes” – and left…") is not None, "refused"
    arms.run("make_block does not refuse mapped punctuation (quotes, dash, ellipsis)", punctuation_not_refused)

    arms.run("NARRATION_OPENERS is a tuple of at least 14 lowercase strings", lambda: (isinstance(contract.NARRATION_OPENERS, tuple) and len(contract.NARRATION_OPENERS) >= 14 and all(s == s.lower() for s in contract.NARRATION_OPENERS), len(contract.NARRATION_OPENERS)))
    arms.run("NARRATION_OPENERS names the observed and the obvious openers", lambda: (all(o in contract.NARRATION_OPENERS for o in ("i'll", "i will", "let me", "i'm going to", "i need to")), contract.NARRATION_OPENERS))

    narrated = ["I'll research this now.MUFG announced a new president.", "I'll search for information on this. Zhang Yi is the chief executive.", "I will look into the company's strategy. It grew.",
                "Let me check the latest news. The company grew.", "I'm going to look this up. It grew.", "I need to find the CEO first. It grew.", "  \"I'll research this.\" It grew.",
                "i'll research this. It grew.", "I'LL RESEARCH THIS. It grew.", "Let's look at the company. It grew.", "I found several sources. It grew.", "First, I will search. It grew.",
                "Based on my search, the company grew."]
    for t in narrated:
        def refused(t=t):
            b = contract.none_block("mgmt_bio", "Reason.")
            b.update({"source_class": "OPAL_SOURCE", "text": t, "reason": None, "citations": [dict(OPAL)]})
            problems = contract.validate_block(b)
            return any("narration" in p.lower() for p in problems), problems[:1]
        arms.run("validate_block refuses narration: %s" % t[:44], refused)

    def later_line():
        b = contract.none_block("thesis_pillars", "Reason.")
        b.update({"source_class": "OPAL_SOURCE", "text": "Demand keeps growing.\nI'll check one more source.\nMargins rose.", "reason": None, "citations": [dict(OPAL)]})
        problems = contract.validate_block(b)
        return any("narration" in p.lower() for p in problems), problems[:1]
    arms.run("validate_block refuses narration at the start of a LATER line (pillars)", later_line)

    def legit():
        bad = []
        for t in ("Intel's chief executive took the role in 2025.", "IBM named a new CFO.", "Illumina reported higher revenue.", "Iberdrola grew its network.", "Looking ahead, the company guides higher.",
                  "Lets Holding is a small-cap.", "Searching for growth, the firm bought a rival."):
            b = contract.none_block("mgmt_bio", "Reason.")
            b.update({"source_class": "OPAL_SOURCE", "text": t, "reason": None, "citations": [dict(OPAL)]})
            if contract.validate_block(b):
                bad.append(t)
        return not bad, bad
    arms.run("validate_block does NOT refuse legitimate openers (Intel, IBM, Iberdrola, 'Looking ahead')", legit)

    def make_refuses_narration():
        try:
            make("I'll research this now. The company grew.")
        except contract.ContractError as err:
            return "narration" in str(err).lower(), str(err)[:100]
        return False, "accepted"
    arms.run("make_block REFUSES narration, naming 'narration'", make_refuses_narration)

    def none_reason_unaffected():
        b = contract.none_block("mgmt_bio", "I could not find a source for this block.")
        return contract.validate_block(b) == [], contract.validate_block(b)
    arms.run("a NONE block's reason is not subject to the narration rule", none_reason_unaffected)

    def document_refuses():
        blocks = {i: contract.none_block(i, "Reason.") for i in contract.BLOCK_IDS}
        doc = {"schema": contract.SCHEMA, "security_key": "K", "as_of": "2026-10-14", "generated_at": "2026-10-14T00:00:00Z",
               "producer": {"version": contract.PRODUCER_VERSION, "model": contract.PRODUCER_MODEL}, "blocks": blocks}
        good = contract.validate_document(copy.deepcopy(doc)) == []
        bad = copy.deepcopy(doc)
        bad["blocks"]["mgmt_recent"].update({"source_class": "OPAL_SOURCE", "text": "I'll research this now. MUFG grew.", "reason": None, "citations": [dict(OPAL)]})
        problems = contract.validate_document(bad)
        return good and any("mgmt_recent" in p and "narration" in p.lower() for p in problems), problems[:2]
    arms.run("validate_document refuses a narrated block and names it", document_refuses)

    def mangled_names():
        f = contract.name_mangling_problems
        a = f("Nestl SA named a new chairman.", ["Nestlé SA"])
        b = f("Nestle SA named a new chairman.", ["Nestlé SA"])
        c = f("Zrich Insurance grew.", ["Zürich Insurance"])
        d = f("Zurich Insurance grew.", ["Zürich Insurance"])
        e = f("Apple grew.", ["Apple Inc"])
        return bool(a) and not b and bool(c) and not d and not e, (a, b, c, d, e)
    arms.run("name_mangling_problems finds 'Nestl' for 'Nestl\\u00e9' and passes the transliterated name", mangled_names)

    def mangled_names_ascii_input():
        return contract.name_mangling_problems("The firm grew.", ["Plain Name"]) == [], "ascii names never problems"
    arms.run("name_mangling_problems: ASCII input names are never problems", mangled_names_ascii_input)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
