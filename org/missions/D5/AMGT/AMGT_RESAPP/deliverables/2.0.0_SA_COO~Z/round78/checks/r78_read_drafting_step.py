"""AMGT_RESAPP round 78 -- READ: the drafting step (CTO round-78 ruling, "The draft (producer): one read first").

  python r78_read_drafting_step.py [--write <folder>]

A READ. No build, no store write, no model or vendor call, no deployed invoke. It reads from opal-data-harvest every
stored drafted document (drafting/v1/<name>.json) and the filing analysis each was built from
(filings/v1/<name>/<accession>.analysis.json), and it imports two modules to print what the code asks for:
lib.research.filings.analyze (the two prompts) and lib.research.filings.drafting_build (the section mapping).

What it prints:
  THE ASK     the six headings the model is asked for, the instruction line for GUIDANCE, the recommendation section's
              source classes (drafting_build.SECTION_SOURCES), and how many recommendation words the two prompts hold;
  THE INPUTS  per stored analysis: the filing items the excerpt was cut from (source.excerpt_items) and the prompt
              version;
  THE FACE    per stored draft: the recommendation section's sentences, each one's item class, and whether the first
              one (the card's face, ThesisCards.tsx CardLead: sentences[0]) is the first GUIDANCE finding of the
              analysis that carries a quoted span;
  THE CENSUS  the recommendation-word rule of r78_bb6.py (the same word list) over four populations, each with its
              denominator: the recommendation section's served sentences, the recommendation sentences held for
              having no quoted span, every finding of every class in the stored analyses, and the model's own first-pass
              text. Every hit is printed with its sentence so it can be read by eye.
Verdict: R78 READ DRAFTING STEP: DONE (exit 0) when every stored draft was read with its analysis.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys

BUCKET = "opal-data-harvest"
SECTION = "recommendation"
# The same list r78_bb6.py uses (RECOMMENDATION_WORDS); copied so this read stands alone.
RECOMMENDATION_WORDS = re.compile(
    r"\b(?:buy|sell|hold|overweight|underweight|outperform|underperform|accumulate|recommend\w*|rating|rated|"
    r"price\s+target|target\s+price|upside|downside|attractive|unattractive|valuation|undervalued|overvalued|"
    r"own\s+the\s+shares|add\s+to|trim|conviction)\b", re.IGNORECASE)


def _list(s3, prefix):
    out = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        out += page.get("Contents", []) or []
    return out


def _get_json(s3, key):
    return json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8"))


def _has_span(sentence):
    return any(str(span).strip() for span in (sentence.get("quoted_spans") or []))


def _hits(text):
    return sorted({m.group(0).lower() for m in RECOMMENDATION_WORDS.finditer(text or "")})


def the_ask():
    from lib.research.filings import analyze, drafting_build

    prompt_1, prompt_2 = analyze.PASS_1_PROMPT, analyze.PASS_2_PROMPT
    guidance_rule = [line.strip() for line in prompt_1.splitlines() if line.strip().startswith("- GUIDANCE findings")]
    headings = [line.strip() for line in prompt_1.splitlines()
                if line.strip() in ("GUIDANCE", "SEGMENTS", "RISKS", "COMMENTARY", "BIG BETS", "BIG CHALLENGES",
                                    "THESIS DRIVER")]
    return {
        "prompt_version_in_code": analyze.PROMPT_VERSION, "analyzer_version_in_code": analyze.ANALYZER_VERSION,
        "headings_asked": headings, "item_classes": list(analyze.ITEM_CLASSES),
        "guidance_instruction": guidance_rule,
        "pass_1_recommendation_words": _hits(prompt_1), "pass_2_recommendation_words": _hits(prompt_2),
        "section_sources": {k: list(v) for k, v in drafting_build.SECTION_SOURCES.items()},
        "section_limit": drafting_build.SECTION_LIMIT,
        "excerpt_items_by_form": {k: list(v) for k, v in __import__(
            "lib.research.filings.fetch", fromlist=["EXCERPT_ITEMS"]).EXCERPT_ITEMS.items()},
    }


def read_drafts():
    import boto3

    s3 = boto3.client("s3", region_name="us-east-1")
    rows = []
    for obj in sorted(_list(s3, "drafting/v1/"), key=lambda o: o["Key"]):
        if not obj["Key"].endswith(".json"):
            continue
        draft = _get_json(s3, obj["Key"])
        name = draft.get("security_key")
        prefix = obj["Key"].replace("drafting/v1/", "filings/v1/")[:-len(".json")] + "/"
        analysis_key = "%s%s.analysis.json" % (prefix, draft.get("accession"))
        stored = [o["Key"] for o in _list(s3, prefix)]
        analysis = _get_json(s3, analysis_key) if analysis_key in stored else None
        section = next((s for s in draft.get("sections") or [] if s.get("section") == SECTION), {})
        sentences = section.get("sentences") or []
        served = [s for s in sentences if _has_span(s)]
        held = [h for h in draft.get("held_no_span") or [] if h.get("section") == SECTION]
        row = {
            "name": name, "draft_key": obj["Key"], "draft_stored": obj["LastModified"].strftime("%Y-%m-%dT%H:%MZ"),
            "accession": draft.get("accession"), "form": draft.get("form"), "filing_date": draft.get("filing_date"),
            "draft_model": draft.get("model"), "draft_analyzer_version": draft.get("analyzer_version"),
            "analysis_key": analysis_key if analysis else None,
            "section_sentences_stored": len(sentences), "section_sentences_with_span": len(served),
            "section_item_classes": dict(collections.Counter(str(s.get("item_class")) for s in sentences)),
            "section_quote_methods": dict(collections.Counter(str(s.get("quote_method")) for s in served)),
            "held_no_span": len(held),
            "face": served[0]["text"] if served else None,
            "face_hits": _hits(served[0]["text"]) if served else [],
            "served_hits": [{"text": s["text"], "words": _hits(s["text"])} for s in served if _hits(s["text"])],
            "held_hits": [{"text": h.get("text"), "words": _hits(h.get("text"))} for h in held if _hits(h.get("text"))],
            "all_sections_sentences": sum(len(s.get("sentences") or []) for s in draft.get("sections") or []),
            "all_sections_hits": [{"section": s.get("section"), "text": x.get("text"), "words": _hits(x.get("text"))}
                                  for s in draft.get("sections") or [] for x in s.get("sentences") or []
                                  if _hits(x.get("text"))],
        }
        if analysis:
            items = analysis.get("items") or {}
            guidance = [str(i.get("text") or "") for i in items.get("guidance") or []]
            source = analysis.get("source") or {}
            all_items = [(cls, str(i.get("text") or "")) for cls, found in items.items() for i in found or []]
            first_pass = str(analysis.get("pass_1_text") or "")
            section_texts = [s.get("text") for s in sentences]
            held_texts = [h.get("text") for h in held]
            dropped = [g for g in guidance[:10] if g not in section_texts and g not in held_texts]
            row.update({
                "prompt_version": analysis.get("prompt_version"), "analyzer_version": analysis.get("analyzer_version"),
                "model": analysis.get("model"), "excerpt_items": source.get("excerpt_items"),
                "excerpt_chars": source.get("excerpt_chars"),
                "items_by_class": {cls: len(found or []) for cls, found in items.items()},
                "guidance_findings": len(guidance),
                "face_guidance_position": (guidance.index(row["face"]) + 1) if row["face"] in guidance else None,
                "face_is_first_guidance_with_span": bool(served) and all(
                    g not in [s["text"] for s in served] for g in guidance[:guidance.index(row["face"])]
                ) if row["face"] in guidance else None,
                "section_all_from_guidance": all(t in guidance for t in section_texts),
                "guidance_first_ten_split": {"in section": sum(1 for g in guidance[:10] if g in section_texts),
                                             "held no span": sum(1 for g in guidance[:10] if g in held_texts),
                                             "neither (refused or changed)": len(dropped)},
                "items_total": len(all_items),
                "item_hits": [{"class": cls, "text": text, "words": _hits(text)} for cls, text in all_items
                              if _hits(text)],
                "first_pass_chars": len(first_pass), "first_pass_hits": _hits(first_pass),
                "analysis_top_level_keys": sorted(analysis.keys()),
            })
        rows.append(row)
    return rows


def build_table():
    rows = read_drafts()
    with_analysis = [r for r in rows if r.get("analysis_key")]
    return {
        "ask": the_ask(), "drafts": len(rows), "with_analysis": len(with_analysis),
        "served_sentences": sum(r["section_sentences_with_span"] for r in rows),
        "stored_sentences": sum(r["section_sentences_stored"] for r in rows),
        "held_sentences": sum(r["held_no_span"] for r in rows),
        "faces": sum(1 for r in rows if r["face"]),
        "faces_with_word": sum(1 for r in rows if r["face_hits"]),
        "served_with_word": sum(len(r["served_hits"]) for r in rows),
        "held_with_word": sum(len(r["held_hits"]) for r in rows),
        "all_sections_sentences": sum(r["all_sections_sentences"] for r in rows),
        "all_sections_with_word": sum(len(r["all_sections_hits"]) for r in rows),
        "items_total": sum(r.get("items_total", 0) for r in with_analysis),
        "items_with_word": sum(len(r.get("item_hits") or []) for r in with_analysis),
        "items_with_word_by_class": dict(collections.Counter(
            h["class"] for r in with_analysis for h in r.get("item_hits") or [])),
        "items_with_word_by_word": dict(collections.Counter(
            w for r in with_analysis for h in r.get("item_hits") or [] for w in h["words"])),
        "guidance_findings": sum(r.get("guidance_findings", 0) for r in with_analysis),
        "section_all_from_guidance": sum(1 for r in with_analysis if r.get("section_all_from_guidance")),
        "face_is_first_guidance_with_span": sum(1 for r in with_analysis if r.get("face_is_first_guidance_with_span")),
        "prompt_versions": dict(collections.Counter(str(r.get("prompt_version")) for r in with_analysis)),
        "excerpt_items": dict(collections.Counter(json.dumps(r.get("excerpt_items")) for r in with_analysis)),
        "first_pass_stored": sum(1 for r in with_analysis if r.get("first_pass_chars")),
        "first_pass_with_word": sum(1 for r in with_analysis if r.get("first_pass_hits")),
        "rows": rows,
    }


def print_table(t):
    ask = t["ask"]
    print("THE ASK (code at HEAD: prompt %s, analyzer %s)" % (ask["prompt_version_in_code"],
                                                              ask["analyzer_version_in_code"]))
    print("   headings the model is asked for: %s" % ask["headings_asked"])
    print("   the GUIDANCE instruction: %s" % ask["guidance_instruction"])
    print("   recommendation words in the first prompt: %s; in the second: %s"
          % (ask["pass_1_recommendation_words"], ask["pass_2_recommendation_words"]))
    print("   section sources: %s; at most %d sentences a section" % (json.dumps(ask["section_sources"]),
                                                                     ask["section_limit"]))
    print("   filing items the excerpt is cut from, by form: %s" % json.dumps(ask["excerpt_items_by_form"]))
    print("THE INPUTS (%d stored drafts; %d with their analysis read)" % (t["drafts"], t["with_analysis"]))
    print("   prompt versions of the stored analyses: %s" % t["prompt_versions"])
    print("   excerpt items of the stored analyses: %s" % t["excerpt_items"])
    print("THE FACE")
    print("   recommendation sections whose every sentence is a GUIDANCE finding of the analysis: %d of %d"
          % (t["section_all_from_guidance"], t["with_analysis"]))
    print("   faces that are the first GUIDANCE finding carrying a quoted span: %d of %d"
          % (t["face_is_first_guidance_with_span"], t["with_analysis"]))
    for r in t["rows"]:
        print("   %-16s stored %2d with-span %2d held %2d | classes %s | face is GUIDANCE finding #%s of %s | first ten "
              "GUIDANCE: %s" % (r["name"], r["section_sentences_stored"], r["section_sentences_with_span"],
                                r["held_no_span"], r["section_item_classes"], r.get("face_guidance_position"),
                                r.get("guidance_findings"), r.get("guidance_first_ten_split")))
        print("      face: %s" % (r["face"] or "")[:200])
    print("THE CENSUS (the word rule of r78_bb6.py)")
    print("   faces with a recommendation word: %d of %d" % (t["faces_with_word"], t["faces"]))
    print("   recommendation sentences carrying a span (what the page serves) with a word: %d of %d"
          % (t["served_with_word"], t["served_sentences"]))
    print("   recommendation sentences held for no quoted span with a word: %d of %d"
          % (t["held_with_word"], t["held_sentences"]))
    print("   sentences of ALL five sections with a word: %d of %d" % (t["all_sections_with_word"],
                                                                      t["all_sections_sentences"]))
    print("   findings of ALL six classes in the stored analyses with a word: %d of %d; by class %s; by word %s"
          % (t["items_with_word"], t["items_total"], t["items_with_word_by_class"], t["items_with_word_by_word"]))
    print("   GUIDANCE findings in the stored analyses: %d" % t["guidance_findings"])
    print("   analyses storing the model's first-pass text: %d of %d; of those with a word anywhere in it: %d"
          % (t["first_pass_stored"], t["with_analysis"], t["first_pass_with_word"]))
    for r in t["rows"]:
        for hit in (r.get("item_hits") or []):
            print("   HIT %-16s %-14s %s | %s" % (r["name"], hit["class"], hit["words"], hit["text"][:230]))
        for hit in r["held_hits"]:
            print("   HIT %-16s held-no-span   %s | %s" % (r["name"], hit["words"], str(hit["text"])[:230]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", default=None, help="folder to write DRAFTING_STEP_READ.json to")
    a = ap.parse_args()
    table = build_table()
    print_table(table)
    if a.write:
        os.makedirs(a.write, exist_ok=True)
        with open(os.path.join(a.write, "DRAFTING_STEP_READ.json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(table, fh, indent=1, sort_keys=True)
            fh.write("\n")
        print("   wrote DRAFTING_STEP_READ.json to %s" % a.write)
    ok = table["drafts"] > 0 and table["with_analysis"] == table["drafts"]
    print("R78 READ DRAFTING STEP: %s" % ("DONE" if ok else "NOT DONE"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
