"""check_fc3_prompts.py -- acceptance arms for AMGT-fc-3 (the five builders: prompts that forbid narration and non-English scripts, and truthful refusal reasons).

  PYTHONPATH=<repo root> python check_fc3_prompts.py
Offline, model stubbed. Needs the merged package with the NEW contract (cell fc-2): a narrated or dropped-letter reply must come back as a NONE block whose reason says what
happened (not "too long"), and the Opal path then falls through to the web path as before. The earlier checks (fa-3, fa-4, fa-5) must keep passing.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aifill_check_lib as L  # noqa: E402

DIRECT = "Answer directly: do not describe what you are going to do or what you searched, and do not address the reader."
LETTERS = "Write every name in English letters (transliterate accents and other scripts); never use another script."


def main():
    from lib.research.aifill import block_identity_description as D
    from lib.research.aifill import block_mgmt_bio as B
    from lib.research.aifill import block_mgmt_recent as R
    from lib.research.aifill import block_mgmt_team_view as T
    from lib.research.aifill import block_thesis_pillars as P

    arms = L.Arms("FC-3")
    web = lambda t="Plain text.": L.StubModel(L.result(t, citations=[L.web_cite()], web_search_requests=1))  # noqa: E731

    def sparse():
        inputs = L.served_inputs()
        inputs["thesis"]["dossier_fields"]["management"] = {"status": "ABSENT", "reason": "none"}
        inputs["thesis"]["dossier_fields"]["thesis_pillars"] = []
        inputs["overlay"]["top_band"]["description_line"] = None
        inputs["overlay"]["description"] = {"status": "ABSENT", "text": None}
        for s in inputs["thesis"]["drafted_sections"]:
            s["sentences"] = []
        inputs["overlay"]["feed"]["items"] = []
        return inputs

    mods = [("mgmt_bio", B), ("mgmt_recent", R), ("mgmt_team_view", T), ("thesis_pillars", P), ("identity_description", D)]
    for name, mod in mods:
        def web_prompt(mod=mod):
            m = web()
            mod.build_block(L.ctx(sparse(), m))
            c = m.calls[0]
            blob = (c["system"] or "") + " " + c["prompt"]
            return DIRECT in blob and LETTERS in blob and "NO_INFORMATION" in blob and c["web_search_max_uses"] >= 1, blob[-160:]
        arms.run("%s: the WEB prompt carries both rules" % name, web_prompt)

    def opal_prompts():
        out = []
        inputs = L.served_inputs()
        m = L.StubModel(L.result("Christophe Fouquet joined ASML in 2008."))
        B.build_block(L.ctx(inputs, m))
        out.append(("mgmt_bio", m.calls[0]))
        inputs = L.served_inputs()
        inputs["overlay"]["feed"]["items"] = [{"publisher": "bbg", "publisher_name": "Bloomberg", "published_date": "2026-10-01", "article_key": "bbg:1", "url": "https://x.example/a", "title": "ASML names new chief financial officer"}]
        m = L.StubModel(L.result("ASML named a new chief financial officer."))
        R.build_block(L.ctx(inputs, m))
        out.append(("mgmt_recent", m.calls[0]))
        inputs = L.served_inputs()
        inputs["thesis"]["dossier_fields"]["thesis_pillars"] = []
        m = L.StubModel(L.result("EUV demand drives growth. The light source reached a new power level."))
        P.build_block(L.ctx(inputs, m))
        out.append(("thesis_pillars", m.calls[0]))
        inputs = sparse()
        inputs["thesis"]["drafted_sections"][0]["sentences"] = [{"text": "ASML develops and sells lithography systems for chipmakers.", "evidence": [{"id": "P0001", "location": None, "accession": None}]}]
        m = L.StubModel(L.result("ASML develops and sells lithography systems for chipmakers."))
        D.build_block(L.ctx(inputs, m))
        out.append(("identity_description", m.calls[0]))
        bad = [n for n, c in out if not (DIRECT in (c["system"] or "") + c["prompt"] and LETTERS in (c["system"] or "") + c["prompt"] and c["web_search_max_uses"] == 0)]
        return not bad, bad
    arms.run("the four OPAL prompts carry both rules (and use no web search)", opal_prompts)

    narrated = "I'll research this now. The company named a new chief executive."
    for name, mod in mods:
        def web_narrated(mod=mod):
            block = mod.build_block(L.ctx(sparse(), web(narrated)))
            r = block["reason"] or ""
            return block["source_class"] == "NONE" and "described its work" in r and "too long" not in r and "_" not in r, (block["source_class"], r)
        arms.run("%s: a narrated web reply is NONE saying the model 'described its work' (not 'too long')" % name, web_narrated)

    def web_dropped():
        block = B.build_block(L.ctx(sparse(), web("Toyota (トヨタ) named a new chief executive.")))
        r = block["reason"] or ""
        return block["source_class"] == "NONE" and "outside English" in r and "too long" not in r, (block["source_class"], r)
    arms.run("a reply in another script is NONE saying 'outside English letters' (mgmt_bio)", web_dropped)

    def web_accent_kept():
        block = B.build_block(L.ctx(sparse(), web("Mark Schneider led Nestlé until 2025, when the board named a successor.")))
        return block["source_class"] == "WEB_SEARCH" and "Nestle" in block["text"] and "Nestl " not in block["text"], block.get("text") or block.get("reason")
    arms.run("an accented name is transliterated, not refused (Nestle)", web_accent_kept)

    def opal_narration_falls_to_web():
        inputs = L.served_inputs()
        m = L.StubModel(L.result("I'll summarise the officer facts for you. He joined in 2008."),
                        L.result("Christophe Fouquet became CEO of ASML in 2024.", citations=[L.web_cite("https://example.com/c", "Profile")], web_search_requests=1))
        block = B.build_block(L.ctx(inputs, m))
        return block["source_class"] == "WEB_SEARCH" and len(m.calls) == 2 and m.calls[0]["web_search_max_uses"] == 0, (block["source_class"], len(m.calls), block.get("reason"))
    arms.run("a narrated OPAL reply falls through to the web path (mgmt_bio)", opal_narration_falls_to_web)

    def both_decline_keeps_reason():
        inputs = L.served_inputs()
        m = L.StubModel(L.result("I'll summarise the officer facts for you. He joined in 2008."), L.result("NO_INFORMATION", citations=[L.web_cite()], web_search_requests=1))
        block = B.build_block(L.ctx(inputs, m))
        return block["source_class"] == "NONE" and "described its work" in block["reason"], block.get("reason")
    arms.run("narrated OPAL then a declining web path: NONE keeps 'described its work' in the joined reason", both_decline_keeps_reason)

    def too_long_still_works():
        block = B.build_block(L.ctx(sparse(), web("word " * 400)))
        return block["source_class"] == "NONE" and "too long" in block["reason"], block.get("reason")
    arms.run("a genuinely overlong reply still says 'too long'", too_long_still_works)

    def modules_ascii_no_io():
        bad = []
        for _, mod in mods:
            src = open(mod.__file__, "r", encoding="utf-8").read()
            if not open(mod.__file__, "rb").read().isascii():
                bad.append((mod.__name__, "non-ASCII"))
            bad += [(mod.__name__, w) for w in ("import boto3", "import urllib", "import requests", "import anthropic", "import socket") if w in src]
        return not bad, bad
    arms.run("the five modules are ASCII and do no I/O", modules_ascii_no_io)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
