"""AMGT_CORPUS round 47, CRPS-aw-3 (the /13 dossier write; CTO round-46 ADDENDA 1 to 3, msgs 3972, 3994, 4001) -- the diff of EVERY dossier field of every
served name, the WRITTEN /13 objects against the served /12, and the team_sheet read inside it. Issuer's file. READ-ONLY: S3 reads only.
Round 46's aw3_diff.py moved one version; the team_sheet arm now reads the /13 keys (row_labels, row_formats), the corrected
classes, and the master arm.

  PYTHONPATH=. python aw3_diff.py --pre     before leg w: stored /11 and /12 objects per name (expect /12 = 0 everywhere)
  PYTHONPATH=. python aw3_diff.py --post    the WRITTEN /12 objects (read_dossier at METHOD /12) against /11

Per name and field of doc["fields"]: SAME / NEWFIELD / CHANGED / DROPPED, every non-SAME field printed, a CHANGED field printed WHOLE.
Expected: CHANGED on `team_sheet` (every name: keys were added) and on `model_rows` (the daily model block); anything else is an INPUT that
moved since /11 (the au-1 ingest stored 12 new bronze objects; a changed pillar, management or case set on exactly those names is read
and named, not hidden) or Branch C. The team_sheet arm, per name:
  old_keys_equal   the six round-44 keys (class, workbook_key, sheet, rows, model_rows_beside, reason) equal /11's: the /12 field is additive
  shape            row_classes, row_numbers, row_values all as long as rows; row_counts sums to len(rows); periods a list
  reader_equal     the stored team_sheet equals a fresh team_sheet.rows_for(key) (the reader's own answer)
  by source (an ESTIMATE, the page decides): of the FIGURE rows, those whose label matches a row spec of portal modelSheet.ts are
  Bloomberg candidates; the others take the team's value when a numeric cell exists, else a why in words.
Prints per name `aw3 <key> class <c> rows <n> FIGURE <f> HEADING <h> CONTROL <c> fig_with_value <v> fig_without_value <w>`, then the totals and
`aw3 build <0|1>/1` (names 95, dropped 0, old_keys_equal / shape / reader_equal on all).
"""
import json
import re
import sys

from lib.research.corpus import dossier, team_sheet
from lib.research.harvest import store

OLD_KEYS = ("class", "workbook_key", "sheet", "rows", "model_rows_beside", "reason")
EXPECTED_CHANGED = {"team_sheet", "model_rows"}
SPEC_FILE = "portal/src/pages/SecurityAnalysis/modelSheet.ts"


def _read(key, client, method):
    current = dossier.METHOD_VERSION
    dossier.METHOD_VERSION = method
    try:
        return dossier.read_dossier(key, client=client)["document"]
    finally:
        dossier.METHOD_VERSION = current


def _canon(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=True)


def _spec_labels():
    text = open(SPEC_FILE, encoding="utf-8").read()
    out = set()
    for name in ("FINANCIAL_SUMMARY_ROWS", "MARGIN_HISTORY_ROWS", "V3_LINE_ROWS"):
        a = text.index("export const %s" % name)
        body = text[a:text.index("]\n", a)]
        for m in re.finditer(r"label:\s*'([^']*)'", body):
            out.add(re.sub(r"\s+", " ", m.group(1)).strip().lower())
    return out


def _numeric(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    mode = "--post" if "--post" in sys.argv else "--pre"
    print("aw3 method %s mode %s" % (dossier.METHOD_VERSION, mode))
    client = store._default_client()
    keys = sorted(dossier._resolved_security_keys(client=client))
    if mode == "--pre":
        have13 = missing12 = 0
        for key in keys:
            try:
                d12 = _read(key, client, "amgt-corpus-dossier/12")
                if d12.get("method_version") != "amgt-corpus-dossier/12":
                    missing12 += 1
                    print("PRE-NOT-AT-11 %s method %s" % (key, d12.get("method_version")))
            except LookupError:
                missing12 += 1
                print("PRE-NO-11 %s" % key)
            try:
                d13 = _read(key, client, "amgt-corpus-dossier/13")
                have13 += int(d13.get("method_version") == "amgt-corpus-dossier/13")
            except LookupError:
                pass
        print("aw3 pre names %d without_a_/11_object %d with_a_/12_object %d" % (len(keys), missing12, have13))
        return 0
    spec = _spec_labels()
    counts = {"SAME": 0, "NEWFIELD": 0, "CHANGED": 0, "DROPPED": 0}
    n = old_equal = shape_ok = reader_equal = 0
    outside = []
    tot = {"FIGURE": 0, "HEADING": 0, "CONTROL": 0}
    fig_value = fig_novalue = bbg_candidate = team_est = why_est = 0
    classes = {}
    for key in keys:
        try:
            d12 = _read(key, client, "amgt-corpus-dossier/12")
            d13 = _read(key, client, "amgt-corpus-dossier/13")
        except LookupError as exc:
            print("UNREAD %s %s" % (key, str(exc)[:80]))
            continue
        if d13.get("method_version") != "amgt-corpus-dossier/13":
            print("NOT-AT-12 %s method %s" % (key, d13.get("method_version")))
            continue
        n += 1
        f12, f13 = d12.get("fields") or {}, d13.get("fields") or {}
        for name in sorted(set(f12) | set(f13)):
            a, b = name in f12, name in f13
            if a and not b:
                cls = "DROPPED"
            elif b and not a:
                cls = "NEWFIELD"
            elif _canon(f12[name]) == _canon(f13[name]):
                cls = "SAME"
            else:
                cls = "CHANGED"
            counts[cls] += 1
            if cls != "SAME":
                print("%s %s %s" % (cls, key, name))
            if cls == "CHANGED" and name not in EXPECTED_CHANGED:
                outside.append((key, name))
                print("  WHOLE /11 %s" % _canon(f12.get(name)))
                print("  WHOLE /12 %s" % _canon(f13.get(name)))
        t12, t13 = f12.get("team_sheet") or {}, f13.get("team_sheet") or {}
        classes[t13.get("class")] = classes.get(t13.get("class"), 0) + 1
        if all(_canon(t12.get(k)) == _canon(t13.get(k)) for k in OLD_KEYS):
            old_equal += 1
        else:
            print("OLD-KEYS-CHANGED %s" % key)
        rows = t13.get("rows") or []
        rc = t13.get("row_counts") or {}
        shaped = (len(t13.get("row_classes") or []) == len(rows) == len(t13.get("row_numbers") or []) == len(t13.get("row_values") or [])
                  and sum(rc.get(c, 0) for c in ("FIGURE", "HEADING", "CONTROL")) == len(rows)
                  and isinstance(t13.get("periods"), list))
        shape_ok += int(shaped)
        if not shaped:
            print("SHAPE-WRONG %s" % key)
        fresh = team_sheet.rows_for(key, client=client)
        if _canon(t13) == _canon(fresh):
            reader_equal += 1
        else:
            print("TS-DIFFERS-FROM-READER %s" % key)
        f = h = c = fv = fn = 0
        for label, cl, vals in zip(rows, t13.get("row_classes") or [], t13.get("row_values") or []):
            if cl == "FIGURE":
                f += 1
                has = isinstance(vals, list) and any(_numeric(v) for v in vals)
                fv += int(has)
                fn += int(not has)
                if re.sub(r"\s+", " ", label).strip().lower() in spec:
                    bbg_candidate += 1
                elif has:
                    team_est += 1
                else:
                    why_est += 1
            elif cl == "HEADING":
                h += 1
            elif cl == "CONTROL":
                c += 1
        tot["FIGURE"] += f
        tot["HEADING"] += h
        tot["CONTROL"] += c
        fig_value += fv
        fig_novalue += fn
        print("aw3 %s class %s rows %d FIGURE %d HEADING %d CONTROL %d fig_with_value %d fig_without_value %d" % (
            key, t13.get("class"), len(rows), f, h, c, fv, fn))
    print("aw3 team_sheet classes %s" % json.dumps(classes, sort_keys=True, default=str))
    print("aw3 row classes FIGURE %d HEADING %d CONTROL %d sum %d" % (tot["FIGURE"], tot["HEADING"], tot["CONTROL"], sum(tot.values())))
    print("aw3 FIGURE rows with a team value %d without %d | by source ESTIMATE bloomberg_candidate %d team %d why %d" % (
        fig_value, fig_novalue, bbg_candidate, team_est, why_est))
    print("aw3 names %d fields %d same %d newfield %d changed %d dropped %d changed_outside_expected %d (%s)" % (
        n, sum(counts.values()), counts["SAME"], counts["NEWFIELD"], counts["CHANGED"], counts["DROPPED"], len(outside),
        ",".join(sorted({"%s:%s" % o for o in outside}))[:300]))
    print("aw3 old_keys_equal %d/%d shape %d/%d reader_equal %d/%d" % (old_equal, n, shape_ok, n, reader_equal, n))
    build = int(n == len(keys) and counts["DROPPED"] == 0 and old_equal == n and shape_ok == n and reader_equal == n)
    print("aw3 build %d/1" % build)
    return 0 if build else 1


if __name__ == "__main__":
    sys.exit(main())
