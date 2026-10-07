"""AMGT_RESAPP round 78 -- AMGT-bb-6: the Recommendation cards over the covered names (CTO round-77 ruling 8).

  --crit AC1 --where deployed [--write <folder>]
  --crit AC2 --where local

A READ. GET-shaped direct invokes of the deployed function's /thesis route for every covered name. Nothing is written
to any store.

THE TWO LABELS ARE PAGE TEXT, each switched by one served field (portal/src/pages/SecurityAnalysis/components/
ThesisCards.tsx, CardLead):
  "The research team's Base case leads, as written in the team's pack"
        shows when model.team_cases.base.status is "SERVED" and its `table` is a non-empty object;
  "A machine draft, not the research team's view"
        shows when drafted_sections holds the section whose section_id is "recommendation" with 1 or more sentences.
A card carries BOTH labels when both hold. Each covered name falls in ONE of four label states, summing to the covered
count: BOTH, MACHINE_DRAFT_ONLY, BASE_CASE_ONLY, NEITHER.

THE SENTENCE RULE. The card's face shows the FIRST sentence of the recommendation section. A sentence IS a
recommendation only when it carries a recommendation word (RECOMMENDATION_WORDS below: buy, sell, hold, overweight,
underweight, outperform, underperform, accumulate, recommend, rating, price target, upside, downside, attractive,
valuation, and the like). A sentence with none of them is NOT a recommendation. Of those, a sentence with no
forward-looking word either (OUTLOOK_WORDS: expects, plans, projects, guidance, will, and the like) states nothing
about the future at all; ASML's governance-code sentence is that kind.

AC1 (a read that prints its counts; PASSES at the base):
    C1 the covered list holds 95 names and every /thesis answers 200;
    C2 the four label states sum to the covered count;
    C3 the named case: ASML_NA_Equity carries BOTH labels and its face sentence is not a recommendation.
    With --write <folder> the table is also written there as RECOMMENDATION_CARDS.json and RECOMMENDATION_CARDS.md.
AC2 (the committed table; FAILS at the base, where no worker has written one):
    C1 exactly one RECOMMENDATION_CARDS.json sits under a worker's deliverables folder;
    C2 its four label states sum to its covered count and hold each covered name once;
    C3 ASML_NA_Equity sits in BOTH with a face sentence that is not a recommendation.
Verdict: R78 BB6 <CRIT> READ: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
TABLE_GLOB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~*/RECOMMENDATION_CARDS.json"
STATES = ("BOTH", "MACHINE_DRAFT_ONLY", "BASE_CASE_ONLY", "NEITHER")
NAMED = "ASML_NA_Equity"
RECOMMENDATION_WORDS = re.compile(
    r"\b(?:buy|sell|hold|overweight|underweight|outperform|underperform|accumulate|recommend\w*|rating|rated|"
    r"price\s+target|target\s+price|upside|downside|attractive|unattractive|valuation|undervalued|overvalued|"
    r"own\s+the\s+shares|add\s+to|trim|conviction)\b", re.IGNORECASE)
OUTLOOK_WORDS = re.compile(
    r"\b(?:expects?|expected|plans?|planning|projects?|projected|forecasts?|outlook|guidance|anticipates?|intends?|"
    r"will|aims?|targets?|continues?\s+to|goal)\b", re.IGNORECASE)


def _event(path):
    return {"rawPath": path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
            "queryStringParameters": None}


def read_one(key, lam):
    raw = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(
        _event("%s/security/%s/thesis" % (PREFIX, key))).encode())["Payload"].read())
    try:
        body = json.loads(raw.get("body") or "{}")
    except (ValueError, TypeError):
        body = {}
    base = ((body.get("model") or {}).get("team_cases") or {}).get("base")
    base_leads = bool(isinstance(base, dict) and base.get("status") == "SERVED" and isinstance(base.get("table"), dict)
                      and base.get("table"))
    sentences = []
    for section in body.get("drafted_sections") or []:
        if isinstance(section, dict) and section.get("section_id") == "recommendation":
            sentences = [str(s.get("text") or "") for s in (section.get("sentences") or []) if isinstance(s, dict)]
    machine_draft = len(sentences) >= 1
    state = ("BOTH" if base_leads and machine_draft else "MACHINE_DRAFT_ONLY" if machine_draft
             else "BASE_CASE_ONLY" if base_leads else "NEITHER")
    kinds = []
    for text in sentences:
        if RECOMMENDATION_WORDS.search(text):
            kinds.append("RECOMMENDATION_WORD")
        elif OUTLOOK_WORDS.search(text):
            kinds.append("OUTLOOK_ONLY")
        else:
            kinds.append("NEITHER_WORD")
    return {"name": key, "status_code": raw.get("statusCode"), "state": state, "base_case_leads": base_leads,
            "machine_draft": machine_draft, "team_cases_served": (body.get("model") or {}).get("team_cases") is not None,
            "sentences": len(sentences), "face_sentence": sentences[0] if sentences else None,
            "face_kind": kinds[0] if kinds else None, "sentence_kinds": kinds,
            "words_hit": sorted({m.group(0).lower() for t in sentences for m in RECOMMENDATION_WORDS.finditer(t)})}


def build_table():
    import boto3

    from lib.research.coverage import covered_universe

    keys = sorted(covered_universe.covered_security_keys())
    lam = boto3.client("lambda", region_name="us-east-1")
    with ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(lambda k: read_one(k, lam), keys))
    with_card = [r for r in rows if r["machine_draft"]]
    return {
        "covered": len(keys),
        "states": {s: sorted(r["name"] for r in rows if r["state"] == s) for s in STATES},
        "not_200": sorted(r["name"] for r in rows if r["status_code"] != 200),
        "cards_with_a_sentence": len(with_card),
        "face_not_a_recommendation": sorted(r["name"] for r in with_card if r["face_kind"] != "RECOMMENDATION_WORD"),
        "face_neither_word": sorted(r["name"] for r in with_card if r["face_kind"] == "NEITHER_WORD"),
        "no_sentence_is_a_recommendation": sorted(
            r["name"] for r in with_card if "RECOMMENDATION_WORD" not in r["sentence_kinds"]),
        "sentences_total": sum(r["sentences"] for r in rows),
        "sentences_with_a_recommendation_word": sum(r["sentence_kinds"].count("RECOMMENDATION_WORD") for r in rows),
        "rows": rows,
    }


def print_table(table):
    print("   covered names %d; /thesis not 200: %d" % (table["covered"], len(table["not_200"])))
    for s in STATES:
        print("   %-19s %3d  %s" % (s, len(table["states"][s]), ", ".join(table["states"][s][:30])
                                    + (" ..." if len(table["states"][s]) > 30 else "")))
    print("   sum %d of %d" % (sum(len(v) for v in table["states"].values()), table["covered"]))
    n = table["cards_with_a_sentence"]
    print("   cards with a drafted sentence %d of %d" % (n, table["covered"]))
    print("   face sentence is NOT a recommendation (no recommendation word): %d of %d" % (
        len(table["face_not_a_recommendation"]), n))
    print("      of those, no forward-looking word either: %d  %s" % (len(table["face_neither_word"]),
                                                                    ", ".join(table["face_neither_word"])))
    print("   cards where NO sentence carries a recommendation word: %d of %d" % (
        len(table["no_sentence_is_a_recommendation"]), n))
    print("   sentences with a recommendation word: %d of %d sentences" % (
        table["sentences_with_a_recommendation_word"], table["sentences_total"]))
    for r in table["rows"]:
        if r["machine_draft"]:
            print("   %-16s %-18s %-19s %2d sentence(s) words %s | %s" % (
                r["name"], r["state"], r["face_kind"], r["sentences"], r["words_hit"], (r["face_sentence"] or "")[:110]))


def named_ok(table):
    row = next((r for r in table["rows"] if r["name"] == NAMED), {})
    print("   named case %s: state %s; face kind %s" % (NAMED, row.get("state"), row.get("face_kind")))
    return row.get("state") == "BOTH" and row.get("face_kind") in ("OUTLOOK_ONLY", "NEITHER_WORD")


def write_table(table, folder):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "RECOMMENDATION_CARDS.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(table, fh, indent=1, sort_keys=True, ensure_ascii=True)
        fh.write("\n")
    n = table["cards_with_a_sentence"]
    lines = ["# The Recommendation cards over the covered names", "", "| label state | names |", "|---|---|"]
    for s in STATES:
        lines.append("| %s | %d |" % (s, len(table["states"][s])))
    lines.append("| sum | %d of %d |" % (sum(len(v) for v in table["states"].values()), table["covered"]))
    lines += ["", "BOTH: %s" % (", ".join(table["states"]["BOTH"]) or "none"), "",
              "Cards with a drafted sentence: %d." % n,
              "Face sentence is not a recommendation: %d of %d." % (len(table["face_not_a_recommendation"]), n),
              "Of those, no forward-looking word either: %d (%s)." % (
                  len(table["face_neither_word"]), ", ".join(table["face_neither_word"]) or "none"),
              "Cards where no sentence carries a recommendation word: %d of %d." % (
                  len(table["no_sentence_is_a_recommendation"]), n), "",
              "| name | label state | face sentence kind | sentences | face sentence |", "|---|---|---|---|---|"]
    for r in table["rows"]:
        if r["machine_draft"]:
            text = (r["face_sentence"] or "").replace("|", "/").encode("ascii", "replace").decode("ascii")
            lines.append("| %s | %s | %s | %d | %s |" % (r["name"], r["state"], r["face_kind"], r["sentences"], text))
    with open(os.path.join(folder, "RECOMMENDATION_CARDS.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print("   wrote RECOMMENDATION_CARDS.json and .md to %s" % folder)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    ap.add_argument("--write", default=None, help="folder to write the table to (AC1 only)")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))

    if a.crit == "AC2":
        found = sorted(glob.glob(TABLE_GLOB))
        clause("C1 exactly one committed table", len(found) == 1, "%d found %s" % (len(found), found))
        if len(found) != 1:
            return verdict(a, ok)
        with open(found[0], encoding="utf-8") as fh:
            table = json.load(fh)
    else:
        if a.where != "deployed":
            clause("C0 AC1 reads the deployed function", False, "run with --where deployed")
            return verdict(a, ok)
        table = build_table()
        clause("C1 the covered names are read and every /thesis answers 200",
               table["covered"] == 95 and not table["not_200"], "%d covered" % table["covered"])
    print_table(table)
    listed = [n for s in STATES for n in table["states"][s]]
    clause("C2 the four label states sum to the covered count",
           len(listed) == len(set(listed)) == table["covered"], "%d of %d" % (len(listed), table["covered"]))
    clause("C3 the named case carries both labels over a sentence that is not a recommendation", named_ok(table))
    if a.crit == "AC1" and a.write:
        write_table(table, a.write)
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print("R78 BB6 %s READ: %s" % (a.crit, "YES" if yes else "NO"))
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
