"""check_gw1_round111.py -- acceptance arms for AMGT-gw-1 (AIFILL round 111: the CTO's two items of msg 6644).

  PYTHONPATH=<repo root> python check_gw1_round111.py
Offline, stdlib only; the model and the fetcher are stubs. Four mechanisms, each with a control that passes at the base:
  (a) every web-search draft call carries the larger output limit (the round-110 set lost 9 blocks to answers truncated at 1500 tokens);
  (b) a failed block ("This block could not be produced") can be built again ALONE: every other block comes back as it was;
  (c) the unnamed-opening rule tests the opening sentence's SUBJECT, with the CEO's name from the served officer list when there is one
      ("Earlier she was ..." no longer ships);
  (d) a stored document can be re-checked by that rule, and by the restatement rule, with no model call (refinish_document);
  (e) an OPAL_SOURCE bio that PARAPHRASES the pack passage (the CVO's AZN and ISRG case) is withheld, not only a word-for-word copy.
"""
from __future__ import annotations

import copy
import datetime
import json
import os
import re
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "round106_aifill_prep", "checks"))
import aifill_check_lib as L  # noqa: E402

NOW = datetime.datetime(2026, 10, 16, 11, 0, 0, tzinfo=datetime.timezone.utc)
URL = "https://example.com/leadership"
PAGE = "Kristin Peck has led Zoetis since 2020. Earlier she was executive vice president at Pfizer. Jane Roe said she will retire in 2027."
CALL = {"model": "claude-opus-5", "web_search_requests": 2, "input_tokens": 100, "output_tokens": 50}
ROSTER = {"overlay": None, "thesis": {"management": {"officers": [
    {"name": "Kristin C. Peck", "role": "Chief Executive Officer"}, {"name": "Wetteny Joseph", "role": "Chief Financial Officer"}]}}, "errors": {}}
NO_ROSTER = {"overlay": None, "thesis": None, "errors": {}}


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
    """Grounding calls only: a sentence that is a sentence of PAGE is SUPPORTED on S1 with that sentence as its quote."""

    def __init__(self):
        self.calls = []

    def __call__(self, prompt, *, system=None, web_search_max_uses=0, max_tokens=1500):
        self.calls.append(prompt)
        rows = []
        for n, text in numbered(prompt):
            ok = text.rstrip(".") in PAGE
            rows.append({"n": n, "verdict": "SUPPORTED" if ok else "UNSUPPORTED", "source": "S1" if ok else None, "quote": text.rstrip(".") if ok else None})
        return types.SimpleNamespace(text=json.dumps({"verdicts": rows}), model="stub-ground", input_tokens=10, output_tokens=5)


def main():
    from lib.research.aifill import contract, model as seam, orchestrate

    arms = L.Arms("GW-1")

    # ---- (a) the larger output limit on every web-search draft call -------------------------------------------------------
    here = os.path.join(os.path.dirname(contract.__file__))
    names = ("block_mgmt_bio", "block_mgmt_recent", "block_mgmt_team_view", "block_identity_description", "block_thesis_pillars")

    def every_web_call_carries_the_limit():
        bad = []
        for name in names:
            text = open(os.path.join(here, name + ".py"), "r", encoding="utf-8").read()
            web = len(re.findall(r"web_search_max_uses=(?!0)\w+", text))
            lim = text.count("max_tokens=contract.WEB_DRAFT_MAX_TOKENS")
            if web != lim:
                bad.append("%s %d web calls, %d with the limit" % (name, web, lim))
        return not bad, "; ".join(bad)
    arms.run("limit: every web-search draft call in the five block modules passes max_tokens=contract.WEB_DRAFT_MAX_TOKENS", every_web_call_carries_the_limit)

    arms.run("limit: the shared limit is 4000, above the seam default of 1500",
             lambda: (getattr(contract, "WEB_DRAFT_MAX_TOKENS", 0) == 4000, getattr(contract, "WEB_DRAFT_MAX_TOKENS", None)))
    arms.run("limit: control -- the seam's own default stays 1500",
             lambda: (seam.call_model.__kwdefaults__["max_tokens"] == 1500, seam.call_model.__kwdefaults__["max_tokens"]))

    # ---- builders and a document with ONE failed block -----------------------------------------------------------------------
    def web_draft(block_id, text):
        cite = {"source_kind": "web", "url": URL, "title": "T", "quote": "q", "ref": None}
        return lambda ctx: contract.make_block(block_id, "WEB_SEARCH", text, [cite], [], CALL, require_grounding=False)

    def none_b(block_id):
        return lambda ctx: contract.none_block(block_id, "Nothing here.")

    def failing(ctx):
        raise seam.ModelError("model answer was truncated at max_tokens")

    def fetch(url):
        return src(url, PAGE)

    def build(builders_over, inputs=None, model=None, **kw):
        builders = {b: none_b(b) for b in contract.BLOCK_IDS}
        builders.update(builders_over)
        return orchestrate.build_document("ZTS_US_Equity", inputs or ROSTER, model or Model(), now=NOW, builders=builders, fetch=fetch, ground=True, recency=False, **kw)

    PILLAR = "Kristin Peck has led Zoetis since 2020."

    def doc_with_failure():
        return build({"mgmt_recent": failing, "thesis_pillars": web_draft("thesis_pillars", PILLAR)})

    # ---- (b) the retry rebuilds ONLY the failed block ---------------------------------------------------------------------------
    def retry_only_failed():
        first = doc_with_failure()
        was_failed = str(first["blocks"]["mgmt_recent"]["reason"]).startswith("This block could not be produced")
        model = Model()
        builders = {b: none_b(b) for b in contract.BLOCK_IDS}
        builders["mgmt_recent"] = web_draft("mgmt_recent", "Jane Roe said she will retire in 2027.")
        builders["thesis_pillars"] = web_draft("thesis_pillars", "A different sentence that is not in the page.")
        fixed = orchestrate.retry_failed_blocks(first, "ZTS_US_Equity", ROSTER, model, now=NOW, builders=builders, fetch=fetch)
        same = all(fixed["blocks"][b] == first["blocks"][b] for b in contract.BLOCK_IDS if b != "mgmt_recent")
        rebuilt = fixed["blocks"]["mgmt_recent"]["source_class"] == "WEB_SEARCH" and fixed["blocks"]["mgmt_recent"]["text"] == "Jane Roe said she will retire in 2027."
        return was_failed and same and rebuilt and len(model.calls) == 1 and contract.validate_document(fixed, require_grounding=True) == [], "same=%s rebuilt=%s calls=%d" % (same, rebuilt, len(model.calls))
    arms.run("retry: only the failed block is built again; every other block is returned as it was; one grounding call", retry_only_failed)

    def retry_input_untouched():
        first = doc_with_failure()
        before = copy.deepcopy(first)
        builders = {b: none_b(b) for b in contract.BLOCK_IDS}
        builders["mgmt_recent"] = web_draft("mgmt_recent", "Jane Roe said she will retire in 2027.")
        orchestrate.retry_failed_blocks(first, "ZTS_US_Equity", ROSTER, Model(), now=NOW, builders=builders, fetch=fetch)
        return first == before, "the input document changed"
    arms.run("retry: the input document is not changed", retry_input_untouched)

    def retry_nothing_failed():
        doc = build({"thesis_pillars": web_draft("thesis_pillars", PILLAR)})
        model = Model()
        out = orchestrate.retry_failed_blocks(doc, "ZTS_US_Equity", ROSTER, model, now=NOW, builders={}, fetch=fetch)
        return out == doc and not model.calls, "calls=%d" % len(model.calls)
    arms.run("retry: control -- a document with no failed block comes back equal with no call", retry_nothing_failed)

    def retry_keeps_stamps():
        from lib.research.aifill import validation
        stamped = validation.stamp_validation(doc_with_failure(), NOW, state="HELD")
        builders = {b: none_b(b) for b in contract.BLOCK_IDS}
        builders["mgmt_recent"] = web_draft("mgmt_recent", "Jane Roe said she will retire in 2027.")
        fixed = orchestrate.retry_failed_blocks(stamped, "ZTS_US_Equity", ROSTER, Model(), now=NOW, builders=builders, fetch=fetch)
        kept = all(fixed["blocks"][b].get("validation") == stamped["blocks"][b].get("validation") for b in contract.BLOCK_IDS if b != "mgmt_recent")
        return kept and "validation" not in fixed["blocks"]["mgmt_recent"], "the retried block must come back unstamped"
    arms.run("retry: untouched blocks keep their validation stamp; the rebuilt block carries none", retry_keeps_stamps)

    # ---- (c) the unnamed-opening rule tests the subject --------------------------------------------------------------------------
    def bio_doc(text, inputs):
        return build({"mgmt_bio": web_draft("mgmt_bio", text)}, inputs)["blocks"]["mgmt_bio"]

    def earlier_she_withheld():
        blk = bio_doc("Earlier she was executive vice president at Pfizer.", ROSTER)
        reason = getattr(orchestrate, "UNNAMED_REASON", None)
        return blk["source_class"] == "NONE" and reason is not None and blk["reason"] == reason, blk.get("reason")
    arms.run("subject: with the CEO's name known, 'Earlier she was ...' is withheld (no token of Kristin Peck in it)", earlier_she_withheld)

    def named_bio_kept():
        blk = bio_doc("Kristin Peck has led Zoetis since 2020.", ROSTER)
        return blk["source_class"] == "WEB_SEARCH" and blk["text"] == "Kristin Peck has led Zoetis since 2020.", blk.get("reason")
    arms.run("subject: control -- a bio that carries a token of the CEO's name is kept", named_bio_kept)

    def no_roster_earlier_she():
        blk = bio_doc("Earlier she was executive vice president at Pfizer.", NO_ROSTER)
        return blk["source_class"] == "NONE", blk.get("reason")
    arms.run("subject: with no officer list, a pronoun among the first words with no name before it is withheld", no_roster_earlier_she)

    def no_roster_named_first():
        blk = bio_doc("Jane Roe said she will retire in 2027.", NO_ROSTER)
        return blk["source_class"] == "WEB_SEARCH", blk.get("reason")
    arms.run("subject: control -- with no officer list, a name before the pronoun keeps the bio", no_roster_named_first)

    def recent_not_affected():
        blk = build({"mgmt_recent": web_draft("mgmt_recent", "Earlier she was executive vice president at Pfizer.")})["blocks"]["mgmt_recent"]
        return blk["source_class"] == "WEB_SEARCH", blk.get("reason")
    arms.run("subject: control -- the rule is for management bios only", recent_not_affected)

    # ---- (d) the pure re-check of a stored document -------------------------------------------------------------------------------
    def refinish_withholds():
        # a stored document built before the rule: a kept bio whose text opens on "Earlier she"
        kept_doc = build({"mgmt_bio": web_draft("mgmt_bio", "Kristin Peck has led Zoetis since 2020.")}, ROSTER)
        kept_doc["blocks"]["mgmt_bio"]["text"] = "Earlier she was executive vice president at Pfizer."
        before = copy.deepcopy(kept_doc)
        out = orchestrate.refinish_document(kept_doc, ROSTER)
        same_rest = all(out["blocks"][b] == kept_doc["blocks"][b] for b in contract.BLOCK_IDS if b != "mgmt_bio")
        return (out["blocks"]["mgmt_bio"]["source_class"] == "NONE" and same_rest and kept_doc == before
                and contract.validate_document(out, require_grounding=True) == []), "bio=%s" % out["blocks"]["mgmt_bio"]["source_class"]
    arms.run("refinish: a stored bio that opens on 'Earlier she ...' is withheld; the other blocks and the input are unchanged", refinish_withholds)

    def refinish_control():
        doc = build({"mgmt_bio": web_draft("mgmt_bio", "Kristin Peck has led Zoetis since 2020.")}, ROSTER)
        return orchestrate.refinish_document(doc, ROSTER) == doc, "a named bio must come back equal"
    arms.run("refinish: control -- a stored bio that names its subject comes back equal", refinish_control)

    # ---- (e) a paraphrase of the pack passage restates it --------------------------------------------------------------------------
    pack = ("Kristin Peck has served as chief executive of Zoetis since 2020 and brings more than 20 years of experience in life sciences "
            "and animal health. She sits on the boards of Blackrock and the Mayo Clinic.")
    pack_inputs = {"overlay": None, "thesis": {"dossier_fields": {"management": pack}, "management": ROSTER["thesis"]["management"]}, "errors": {}}

    class PackModel(Model):
        def __call__(self, prompt, *, system=None, web_search_max_uses=0, max_tokens=1500):
            self.calls.append(prompt)
            rows = [{"n": n, "verdict": "SUPPORTED", "source": "S1", "quote": "has served as chief executive of Zoetis since 2020"}
                    for n, _ in numbered(prompt)]
            return types.SimpleNamespace(text=json.dumps({"verdicts": rows}), model="stub-ground", input_tokens=10, output_tokens=5)

    def opal_bio(text):
        cite = {"source_kind": "opal", "ref": "Research team pack", "url": None, "title": None, "quote": None}
        draft = lambda ctx: contract.make_block("mgmt_bio", "OPAL_SOURCE", text, [cite], ["thesis.dossier_fields.management"], None, require_grounding=False)  # noqa: E731
        builders = {b: none_b(b) for b in contract.BLOCK_IDS}
        builders["mgmt_bio"] = draft
        return orchestrate.build_document("ZTS_US_Equity", pack_inputs, PackModel(), now=NOW, builders=builders, fetch=fetch, ground=True, recency=False)["blocks"]["mgmt_bio"]

    def paraphrase_withheld():
        blk = opal_bio("Kristin Peck, chief executive of Zoetis since 2020, brings over twenty years of life sciences and animal health experience.")
        reason = getattr(orchestrate, "RESTATES_REASON", None)
        return blk["source_class"] == "NONE" and reason is not None and blk["reason"] == reason, blk.get("reason")
    arms.run("paraphrase: an OPAL bio that says the pack passage again in other words is withheld with the restatement reason", paraphrase_withheld)

    def novel_bio_kept():
        text = "Peck oversees Zoetis, a veterinary business serving livestock producers worldwide."
        blk = opal_bio(text)
        return blk["source_class"] == "OPAL_SOURCE" and blk["text"] == text, blk.get("reason")
    arms.run("paraphrase: control -- an OPAL bio with content the pack passage does not carry is kept", novel_bio_kept)

    def refinish_withholds_paraphrase():
        doc = build({"mgmt_bio": web_draft("mgmt_bio", "Kristin Peck has led Zoetis since 2020.")}, ROSTER)
        bio = doc["blocks"]["mgmt_bio"]
        bio["source_class"] = "OPAL_SOURCE"
        bio["opal_inputs"] = ["thesis.dossier_fields.management"]
        bio["text"] = "Kristin Peck, chief executive of Zoetis since 2020, brings over twenty years of life sciences and animal health experience."
        before = copy.deepcopy(doc)
        out = orchestrate.refinish_document(doc, pack_inputs)
        reason = getattr(orchestrate, "RESTATES_REASON", None)
        return (out["blocks"]["mgmt_bio"]["source_class"] == "NONE" and reason is not None and out["blocks"]["mgmt_bio"]["reason"] == reason
                and doc == before), out["blocks"]["mgmt_bio"].get("reason")
    arms.run("refinish: a stored OPAL bio that paraphrases the pack passage is withheld with the restatement reason", refinish_withholds_paraphrase)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
