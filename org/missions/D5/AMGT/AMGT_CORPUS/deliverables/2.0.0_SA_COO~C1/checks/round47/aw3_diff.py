"""AMGT_CORPUS round 47, CRPS-aw-3 (the /13 dossier write; CTO round-46 ADDENDA 1 to 3, msgs 3972, 3994, 4001) -- the diff of EVERY dossier field of
every served name, the WRITTEN /13 objects against the served /12, and the team_sheet read inside it. Issuer's file. READ-ONLY: S3 reads only.

  PYTHONPATH=. python aw3_diff.py --pre     before leg w: names with a stored /12 object and names with a /13 object (expect /13 = 0 everywhere)
  PYTHONPATH=. python aw3_diff.py --post    the WRITTEN /13 objects (read_dossier at METHOD /13) against /12

Expected: CHANGED on `team_sheet` (every name) and on `model_rows` (the daily model block); anything else is an INPUT that moved since /12 and is
printed WHOLE, named and read, or Branch C. The team_sheet arm, per class of the written /13 answer:
  own (own_new / own_model, 32 names)
    old_keys_equal   class, workbook_key, sheet, rows, model_rows_beside, reason equal /12's (the choice of workbook and the counted rows did not move)
    classes_moved    the names whose row_classes differ from /12's, printed with each transition (the by-name CONTROL rule moves EQY_FUND_YEAR and
                     *_OVERRIDE rows; the year-row header moves ~190 rows of CLX, ML FP and BABA from HEADING to FIGURE: row D1-S7)
  master (63 names): /12 class master_absent, /13 class master, 135 rows each, row_values and row_formats ALL None, periods [] (AMENDMENT 3)
  shape            row_classes, row_numbers, row_values, row_labels, row_formats all as long as rows; row_counts sums to it; periods a list
  reader_equal     the stored team_sheet equals a fresh team_sheet.rows_for(key) (the reader's own answer)
  labels           row_labels claims over the rows (held / measured / absent / none) per class
Prints `aw3 build <b>/1`: 1 only when every served name read at /13, DROPPED 0, own old_keys_equal 32/32, master 63/63 carrying no value, shape and
reader_equal n/n.
"""
import collections
import json
import sys

from lib.research.corpus import dossier, team_sheet
from lib.research.harvest import store

OLD_KEYS = ("class", "workbook_key", "sheet", "rows", "model_rows_beside", "reason")
EXPECTED_CHANGED = {"team_sheet", "model_rows"}
ALIGNED = ("row_classes", "row_numbers", "row_values", "row_labels", "row_formats")


def _read(key, client, method):
    current = dossier.METHOD_VERSION
    dossier.METHOD_VERSION = method
    try:
        return dossier.read_dossier(key, client=client)["document"]
    finally:
        dossier.METHOD_VERSION = current


def _canon(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=True)


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
                    print("PRE-NOT-AT-12 %s method %s" % (key, d12.get("method_version")))
            except LookupError:
                missing12 += 1
                print("PRE-NO-12 %s" % key)
            try:
                d13 = _read(key, client, "amgt-corpus-dossier/13")
                have13 += int(d13.get("method_version") == "amgt-corpus-dossier/13")
            except LookupError:
                pass
        print("aw3 pre names %d without_a_/12_object %d with_a_/13_object %d" % (len(keys), missing12, have13))
        return 0
    counts = {"SAME": 0, "NEWFIELD": 0, "CHANGED": 0, "DROPPED": 0}
    n = 0
    outside = []
    own = own_old_equal = master_ok = shape_ok = reader_equal = 0
    transitions = collections.Counter()
    moved_names = set()
    tot = {"own": collections.Counter(), "master": collections.Counter()}
    withval = {"own": 0, "master": 0}
    claims = {"own": collections.Counter(), "master": collections.Counter()}
    nmaster = 0
    for key in keys:
        try:
            d12 = _read(key, client, "amgt-corpus-dossier/12")
            d13 = _read(key, client, "amgt-corpus-dossier/13")
        except LookupError as exc:
            print("UNREAD %s %s" % (key, str(exc)[:80]))
            continue
        if d13.get("method_version") != "amgt-corpus-dossier/13":
            print("NOT-AT-13 %s method %s" % (key, d13.get("method_version")))
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
                print("  WHOLE /12 %s" % _canon(f12.get(name)))
                print("  WHOLE /13 %s" % _canon(f13.get(name)))
        t12, t13 = f12.get("team_sheet") or {}, f13.get("team_sheet") or {}
        klass = t13.get("class")
        side = "master" if klass == "master" else "own"
        rows = t13.get("rows") or []
        rc = t13.get("row_counts") or {}
        shaped = (all(len(t13.get(k) or []) == len(rows) for k in ALIGNED)
                  and sum(rc.get(c, 0) for c in ("FIGURE", "HEADING", "CONTROL")) == len(rows)
                  and isinstance(t13.get("periods"), list))
        shape_ok += int(shaped)
        if not shaped:
            print("SHAPE-WRONG %s" % key)
        if side == "own":
            own += 1
            if all(_canon(t12.get(k)) == _canon(t13.get(k)) for k in OLD_KEYS):
                own_old_equal += 1
            else:
                print("OWN-OLD-KEYS-CHANGED %s" % key)
            for lab, a, b in zip(rows, t12.get("row_classes") or [], t13.get("row_classes") or []):
                if a != b:
                    transitions[(a, b)] += 1
                    moved_names.add(key)
            for lab, a, b in zip(rows, t12.get("row_classes") or [], t13.get("row_classes") or []):
                pass
        else:
            nmaster += 1
            ok = (t12.get("class") == "master_absent" and len(rows) == 135
                  and all(v is None for v in t13.get("row_values") or [])
                  and all(v is None for v in t13.get("row_formats") or [])
                  and t13.get("periods") == [])
            master_ok += int(ok)
            if not ok:
                print("MASTER-NOT-AS-PREDICTED %s class12 %s rows %d" % (key, t12.get("class"), len(rows)))
        for c in ("FIGURE", "HEADING", "CONTROL"):
            tot[side][c] += rc.get(c, 0)
        withval[side] += sum(1 for v in t13.get("row_values") or [] if v is not None)
        for e in t13.get("row_labels") or []:
            claims[side][(e or {}).get("claim", "none")] += 1
        fresh = team_sheet.rows_for(key, client=client)
        if _canon(t13) == _canon(fresh):
            reader_equal += 1
        else:
            print("TS-DIFFERS-FROM-READER %s" % key)
        print("aw3 %s class %s rows %d %s" % (key, klass, len(rows), json.dumps(rc, sort_keys=True)))
    print("aw3 own names %d master names %d" % (own, nmaster))
    print("aw3 own row classes %s | master row classes %s" % (dict(tot["own"]), dict(tot["master"])))
    print("aw3 rows with a team value: own %d master %d" % (withval["own"], withval["master"]))
    print("aw3 label claims: own %s | master %s" % (dict(claims["own"]), dict(claims["master"])))
    print("aw3 own class transitions /12 -> /13 %s over %d names" % (
        {"%s>%s" % t: c for t, c in sorted(transitions.items())}, len(moved_names)))
    print("aw3 names %d fields %d same %d newfield %d changed %d dropped %d changed_outside_expected %d (%s)" % (
        n, sum(counts.values()), counts["SAME"], counts["NEWFIELD"], counts["CHANGED"], counts["DROPPED"], len(outside),
        ",".join(sorted({"%s:%s" % o for o in outside}))[:300]))
    print("aw3 own_old_keys_equal %d/%d master_as_predicted %d/%d shape %d/%d reader_equal %d/%d" % (
        own_old_equal, own, master_ok, nmaster, shape_ok, n, reader_equal, n))
    build = int(n == len(keys) and counts["DROPPED"] == 0 and own_old_equal == own and master_ok == nmaster
                and shape_ok == n and reader_equal == n and withval["master"] == 0)
    print("aw3 build %d/1" % build)
    return 0 if build else 1


if __name__ == "__main__":
    sys.exit(main())
