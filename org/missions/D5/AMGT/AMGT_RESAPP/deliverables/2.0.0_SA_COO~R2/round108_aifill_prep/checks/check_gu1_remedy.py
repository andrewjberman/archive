"""check_gu1_remedy.py -- acceptance arms for AMGT-gu-1 (the FWD-41 five-new-name remedy: clause-level support, the cross-block recency rule, the run-together word).

  PYTHONPATH=<repo root> python check_gu1_remedy.py
Offline, stdlib only; the model and the fetcher are stubs. CVO row AMGT_RESAPP-D1-C-S158 (ADJUDICATION_v135): QXO team_view kept a sentence whose
$3 billion, Apollo and Temasek clause its cited source does not carry; HSBA team_view kept a buyback pause that the interim results cited by another
block of the same page contradict; NG/ printed 'Pettigrewafter'. Each arm names the behaviour it pins. A control arm passes at the base.
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

NOW = datetime.datetime(2026, 10, 16, 8, 0, 0, tzinfo=datetime.timezone.utc)
URL_A = "https://example.com/annual-results-2025"
URL_B = "https://example.com/interim-results-2026"
PAGE_A = ("The board paused further buybacks until CET1 is restored to its target range. "
          "Georges Elhedery replaced Noel Quinn as chief executive in September 2024.")
PAGE_B = ("Interim Results 2026. HSBC reported profit before tax of 21 billion. "
          "We also intend to initiate a share buy-back of up to $1bn.")
TEAM_1 = "The board paused further buybacks until CET1 is restored to its target range."
TEAM_2 = "Georges Elhedery replaced Noel Quinn as chief executive in September 2024."
PILLAR = "HSBC announced a share buy-back of up to $1bn in 2026."
Q_A1 = "paused further buybacks until CET1 is restored to its target range"
Q_A2 = "Georges Elhedery replaced Noel Quinn as chief executive in September 2024"
Q_B = "initiate a share buy-back of up to $1bn"
CALL = {"model": "claude-opus-5", "web_search_requests": 2, "input_tokens": 100, "output_tokens": 50}


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
    """Grounding calls only. rules: list of (substring, label_one_source, verdict_one, label_two_source, verdict_two) ... see rows()."""

    def __init__(self, rows, fail_second=False):
        self.rows, self.calls, self.fail_second = rows, [], fail_second

    def __call__(self, prompt, *, system=None, web_search_max_uses=0, max_tokens=1500):
        self.calls.append(prompt)
        two = "[S2]" in prompt
        if two and self.fail_second:
            raise RuntimeError("stub model down")
        out = []
        for n, text in numbered(prompt):
            hit = next((r for key, r in self.rows if key in text), None)
            row = (hit or {}).get("two" if two else "one") or {"verdict": "UNSUPPORTED", "source": None, "quote": None}
            out.append(dict(row, n=n))
        return types.SimpleNamespace(text=json.dumps({"verdicts": out}), model="stub-ground", input_tokens=10, output_tokens=5)


def sup(label, quote):
    return {"verdict": "SUPPORTED", "source": label, "quote": quote}


def con(label, quote):
    return {"verdict": "CONTRADICTED", "source": label, "quote": quote}


def main():
    from lib.research.aifill import contract, grounding, orchestrate

    arms = L.Arms("GU-1")

    # ---- the folding of invisible and hyphen characters -----------------------------------------------------------
    arms.run("fold: a zero-width space between words leaves a space", lambda: (contract.fold_text("Pettigrew​after a board") == "Pettigrew after a board", contract.fold_text("Pettigrew​after a board")))
    arms.run("fold: a non-breaking hyphen folds to a hyphen", lambda: (contract.fold_text("co‑founder") == "co-founder", contract.fold_text("co‑founder")))
    arms.run("fold: soft hyphen and zero-width joiner join silently", lambda: (contract.fold_text("inter­mediate and re‍enter") == "intermediate and reenter", contract.fold_text("inter­mediate and re‍enter")))
    arms.run("fold: control -- a symbol among spaces drops as before", lambda: (contract.fold_text("Price ☃ up") == "Price  up", contract.fold_text("Price ☃ up")))

    # ---- the clause-level check: every number and name a sentence states must be in the source -----------------------
    qxo_text = ("Since launching QXO in 2023, Jacobs firm has spent around $30 billion buying Beacon, Kodiak, and TopBuild. "
                "Closings were April 2025.")
    qxo = "The deals were partly funded by equity financing raised to $3 billion with investors including Apollo and Temasek."
    q_first = "Jacobs firm has spent around $30 billion buying Beacon, Kodiak, and TopBuild"

    def ground_one(sentence, page_text, quote, reference=None, label="S1", verdict="SUPPORTED"):
        model = Model([(sentence[:20], {"one": {"verdict": verdict, "source": label, "quote": quote}, "two": {"verdict": verdict, "source": label, "quote": quote}})])
        kwargs = {} if reference is None else {"reference": reference}
        return grounding.ground_block(sentence, [src(URL_A, page_text)], model, NOW, **kwargs)

    def clause_unsupported():
        res = ground_one(qxo, qxo_text, q_first)
        rec = res.record["sentences"][0]
        return rec["verdict"] == "UNSUPPORTED" and res.kept == [] and res.text == "", rec["verdict"]
    arms.run("clause: a SUPPORTED verdict on a first-clause quote is refused (Apollo, Temasek, $3 billion)", clause_unsupported)

    def carried_sentence():
        sent = "Jacobs firm has spent around $30 billion buying Beacon in 2023."
        res = ground_one(sent, qxo_text, "Jacobs firm has spent around $30 billion buying Beacon")
        return res.record["sentences"][0]["verdict"] == "SUPPORTED" and res.text == sent, res.record["sentences"][0]["verdict"]
    arms.run("clause: control -- a sentence whose numbers and names are all carried stays SUPPORTED", carried_sentence)

    def number_mismatch():
        sent = "Jacobs firm has spent around $3 billion buying Beacon."
        res = ground_one(sent, qxo_text, "Jacobs firm has spent around $30 billion buying Beacon")
        return res.record["sentences"][0]["verdict"] == "UNSUPPORTED", res.record["sentences"][0]["verdict"]
    arms.run("clause: $3 billion is not carried by a source that says $30 billion", number_mismatch)

    def digits_inside_a_word():
        sent = "The board paused further buybacks until CET1 is restored to its target range."
        res = ground_one(sent, PAGE_A, Q_A1)
        return res.record["sentences"][0]["verdict"] == "SUPPORTED", res.record["sentences"][0]["verdict"]
    arms.run("clause: control -- the digit inside CET1 is not a number to carry", digits_inside_a_word)

    # ---- reference sources: they can contradict a sentence, never support one ------------------------------------------
    def ref_contradicts():
        res = ground_one(TEAM_1, PAGE_A, Q_B, reference=[src(URL_B, PAGE_B)], label="S2", verdict="CONTRADICTED")
        rec = res.record["sentences"][0]
        return rec["verdict"] == "CONTRADICTED" and rec["source"] == 1 and rec["quote"] == Q_B and res.text == "", rec
    arms.run("reference: a CONTRADICTED verdict on the reference source records its index and quote", ref_contradicts)

    def ref_never_supports():
        res = ground_one(PILLAR, PAGE_A, Q_B, reference=[src(URL_B, PAGE_B)], label="S2", verdict="SUPPORTED")
        return res.record["sentences"][0]["verdict"] == "UNSUPPORTED" and res.kept == [], res.record["sentences"][0]["verdict"]
    arms.run("reference: a SUPPORTED verdict on the reference source is UNSUPPORTED", ref_never_supports)

    def ref_order():
        res = ground_one(TEAM_1, PAGE_A, Q_A1, reference=[src(URL_B, PAGE_B)], label="S1", verdict="SUPPORTED")
        urls = [s["url"] for s in res.record["sources"]]
        return urls == [URL_A, URL_B] and res.used_urls == [URL_A], urls
    arms.run("reference: the record lists the own source first and the reference after; only the own is used", ref_order)

    def ref_control():
        res = ground_one(TEAM_1, PAGE_A, Q_A1)
        return res.record["sentences"][0]["verdict"] == "SUPPORTED" and len(res.record["sources"]) == 1, len(res.record["sources"])
    arms.run("reference: control -- no reference leaves the call as before", ref_control)

    # ---- the document: the recency pass over the web management blocks ----------------------------------------------------
    def web_draft(block_id, text, urls):
        cites = [{"source_kind": "web", "url": u, "title": "T " + u[-6:], "quote": "q", "ref": None} for u in urls]
        return lambda ctx: contract.make_block(block_id, "WEB_SEARCH", text, cites, [], CALL, require_grounding=False)

    def none_b(block_id):
        return lambda ctx: contract.none_block(block_id, "Nothing here.")

    def fetch(url):
        return src(url, {URL_A: PAGE_A, URL_B: PAGE_B}.get(url, ""))

    def build(model, team_text=TEAM_1 + " " + TEAM_2, **kw):
        builders = {bid: none_b(bid) for bid in contract.BLOCK_IDS}
        builders["mgmt_team_view"] = web_draft("mgmt_team_view", team_text, [URL_A])
        builders["thesis_pillars"] = web_draft("thesis_pillars", PILLAR, [URL_B])
        return orchestrate.build_document("HSBA_LN_Equity", {"overlay": None, "thesis": None, "errors": {}}, model, now=NOW, builders=builders, fetch=fetch, ground=True, **kw)

    rows = [(TEAM_1[:20], {"one": sup("S1", Q_A1), "two": con("S2", Q_B)}), (TEAM_2[:20], {"one": sup("S1", Q_A2), "two": sup("S1", Q_A2)}),
            (PILLAR[:20], {"one": sup("S1", Q_B), "two": sup("S1", Q_B)})]

    def stale_dropped():
        model = Model(rows)
        doc = build(model)
        blk = doc["blocks"]["mgmt_team_view"]
        sents = {s["text"]: s for s in blk["grounding"]["sentences"]}
        bad = sents.get(TEAM_1, {})
        ok = (blk["text"] == TEAM_2 and bad.get("verdict") == "CONTRADICTED" and bad.get("source") == 1 and bad.get("quote") == Q_B
              and [s["url"] for s in blk["grounding"]["sources"]] == [URL_A, URL_B] and len(model.calls) == 3
              and contract.validate_document(doc, require_grounding=True) == [])
        return ok, "text=%r calls=%d" % (blk["text"][:40], len(model.calls))
    arms.run("recency: a sentence the other block's newer page contradicts is dropped, with source and quote", stale_dropped)

    def citations_follow():
        blk = build(Model(rows))["blocks"]["mgmt_team_view"]
        return [c["url"] for c in blk["citations"]] == [URL_A], [c["url"] for c in blk["citations"]]
    arms.run("recency: the kept block cites only the pages its kept sentences rest on", citations_follow)

    def tokens_summed():
        mc = build(Model(rows))["blocks"]["mgmt_team_view"]["grounding"]["model_call"]
        return mc["input_tokens"] == 20 and mc["output_tokens"] == 10, mc
    arms.run("recency: the record's model_call carries both grounding calls' tokens", tokens_summed)

    def all_contradicted():
        rows_all = [(TEAM_1[:20], {"one": sup("S1", Q_A1), "two": con("S2", Q_B)}), (PILLAR[:20], {"one": sup("S1", Q_B), "two": sup("S1", Q_B)})]
        doc = build(Model(rows_all), team_text=TEAM_1)
        blk = doc["blocks"]["mgmt_team_view"]
        reason = getattr(orchestrate, "RECENCY_REASON", None)
        return blk["source_class"] == "NONE" and blk["text"] is None and reason is not None and blk["reason"] == reason, blk.get("reason")
    arms.run("recency: every sentence contradicted gives a NONE block with the recency reason", all_contradicted)

    def switch_off():
        model = Model(rows)
        blk = build(model, recency=False)["blocks"]["mgmt_team_view"]
        return blk["text"] == TEAM_1 + " " + TEAM_2 and len(model.calls) == 2, len(model.calls)
    arms.run("recency: recency=False leaves the block as grounded and makes no extra call", switch_off)

    def no_other_web_block():
        model = Model(rows)
        builders = {bid: none_b(bid) for bid in contract.BLOCK_IDS}
        builders["mgmt_team_view"] = web_draft("mgmt_team_view", TEAM_1 + " " + TEAM_2, [URL_A])
        doc = orchestrate.build_document("HSBA_LN_Equity", {"overlay": None, "thesis": None, "errors": {}}, model, now=NOW, builders=builders, fetch=fetch, ground=True)
        return doc["blocks"]["mgmt_team_view"]["text"] == TEAM_1 + " " + TEAM_2 and len(model.calls) == 1, len(model.calls)
    arms.run("recency: control -- no other web block means no extra call", no_other_web_block)

    def check_fails_closed():
        doc = build(Model(rows, fail_second=True))
        blk = doc["blocks"]["mgmt_team_view"]
        reason = getattr(orchestrate, "RECENCY_UNCHECKED", None)
        return blk["source_class"] == "NONE" and reason is not None and blk["reason"] == reason, blk.get("reason")
    arms.run("recency: a recency call that fails withholds the text", check_fails_closed)

    def thesis_untouched():
        doc = build(Model(rows))
        return doc["blocks"]["thesis_pillars"]["text"] == PILLAR, doc["blocks"]["thesis_pillars"]["text"]
    arms.run("recency: control -- only the management blocks are re-checked", thesis_untouched)

    return arms.finish()


if __name__ == "__main__":
    sys.exit(main())
