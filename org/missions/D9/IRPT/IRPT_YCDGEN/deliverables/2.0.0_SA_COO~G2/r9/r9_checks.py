"""IRPT_YCDGEN round 9 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python r9_checks.py d9      the rule-less elements file of cell YCD-d-9 is complete and true to held_data

Cell YCD-a-9's two checks are r8/r8_checks.py f8 and f8fold (written in round 8, failing at base).
Prints one RESULT line: R9-<MODE>-OK or R9-<MODE>-FAIL <reason>; rc 0 only on OK. ASCII only.
"""
import json
import os
import sys

MAP = "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps/overview_map.json"
OUT = "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/0.9.0_WK_IRPT_YCDGEN~12/RULE_LESS_ELEMENTS_YCD-d-9.json"
WORDS = ("YES_SEEN_IN_REPO", "PARTIAL", "NOT_SEEN_IN_REPO")


def main(mode):
    if mode != "d9":
        raise SystemExit(__doc__)
    sys.path.insert(0, "infra/aws/lambda/investor-reporting/ycharts/research")
    import held_data
    doc = json.load(open(MAP, encoding="utf-8"))
    elements = doc["elements"] if isinstance(doc, dict) else doc
    held = [e for e in elements if isinstance(e.get("source"), dict) and e["source"].get("computed") == "OPAL_HELD"]
    rule_less = {e["id"]: e for e in held if held_data.RULES.get(e["source"].get("group")) is None}
    want = {"map_elements": len(elements), "opal_held_elements": len(held), "rule_less_elements": len(rule_less)}
    print("counted:", want)
    if not os.path.isfile(OUT):
        print("R9-D9-FAIL the file is absent: " + OUT)
        return 1
    got = json.load(open(OUT, encoding="utf-8"))
    problems = []
    if got.get("denominator") != want:
        problems.append("denominator %r != counted %r" % (got.get("denominator"), want))
    rows = got.get("elements") if isinstance(got.get("elements"), list) else []
    ids = [r.get("element_id") for r in rows]
    if sorted(map(str, ids)) != sorted(map(str, rule_less)):
        problems.append("element ids differ: %d in the file, %d rule-less in the map" % (len(ids), len(rule_less)))
    families = set()
    for r in rows:
        e = rule_less.get(r.get("element_id"))
        if e is None:
            continue
        group = e["source"].get("group")
        if r.get("group") != group or r.get("why_no_rule") != held_data._not_held_reason(group):
            problems.append("%s: group or why_no_rule is not held_data's" % r.get("element_id"))
        if r.get("feedable") not in WORDS:
            problems.append("%s: feedable %r" % (r.get("element_id"), r.get("feedable")))
        families.add(r.get("input_family"))
        for ev in r.get("repo_evidence") or []:
            if not isinstance(ev, dict) or not os.path.isfile(str(ev.get("path"))):
                problems.append("%s: evidence path is not a file: %r" % (r.get("element_id"), ev.get("path") if isinstance(ev, dict) else ev))
    logged = {s.get("input_family") for s in (got.get("search_log") or []) if isinstance(s, dict)}
    if families - logged:
        problems.append("families with no search_log entry: %s" % sorted(map(str, families - logged)))
    if problems:
        for p in problems[:12]:
            print("  " + p[:240])
        print("R9-D9-FAIL %d problem(s)" % len(problems))
        return 1
    print("R9-D9-OK elements=%d families=%d" % (len(rows), len(families)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
