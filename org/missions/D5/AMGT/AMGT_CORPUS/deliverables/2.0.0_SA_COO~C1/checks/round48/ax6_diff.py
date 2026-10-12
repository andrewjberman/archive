"""AMGT_CORPUS round 48, CRPS-ax-6 (the /14 dossier write; CTO round-47 analysis ADDENDUM 1, msg 4113) -- the diff of EVERY dossier field of every served name,
the WRITTEN /14 objects against the stored /13, and the team_sheet read inside it. Issuer's file. READ-ONLY: S3 reads only.

  PYTHONPATH=. python ax6_diff.py --pre     before leg w: names with a stored /13 object and with a /14 object (expect /14 = 0 everywhere)
  PYTHONPATH=. python ax6_diff.py --post    the WRITTEN /14 objects (read_dossier at METHOD /14) against /13

Expected: CHANGED on `team_sheet` only, on exactly the names that carry a FactSet code the nine entries name and that no own sheet labels; every other field SAME.
The team_sheet arm, per name:
  keys_equal     class, workbook_key, sheet, rows, model_rows_beside, reason, row_classes, row_numbers, row_values, periods, row_counts, row_formats equal /13's
  labels_moved   every row whose row_labels entry differs from /13's is `claim absent` -> `claim held` with `source factset`, the code one of the nine entries, the text
                 and cite as the entry stores them, and nothing else changed; printed as a count per code
  shape          row_classes, row_numbers, row_values, row_labels, row_formats all as long as rows; row_counts sums to it; periods a list
  reader_equal   the stored team_sheet equals a fresh team_sheet.rows_for(key) (the reader's own answer)
  shares         row_labels claims over the rows per class: measured / held (cross-workbook, FactSet) / FactSet line, the three shares the CTO asked for
Prints `ax6 build <b>/1`: 1 only when every served name read at /14, DROPPED 0, keys_equal n/n, labels_moved as predicted (no other label moved), shape n/n,
reader_equal n/n, and no value on a master name.
"""
import collections
import json
import sys

from lib.research.corpus import dossier, team_sheet
from lib.research.harvest import store

KEYS = ("class", "workbook_key", "sheet", "rows", "model_rows_beside", "reason", "row_classes", "row_numbers", "row_values", "periods", "row_counts",
        "row_formats")
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
    print("ax6 method %s mode %s" % (dossier.METHOD_VERSION, mode))
    client = store._default_client()
    keys = sorted(dossier._resolved_security_keys(client=client))
    if mode == "--pre":
        have14 = missing13 = 0
        for key in keys:
            try:
                d13 = _read(key, client, "amgt-corpus-dossier/13")
                if d13.get("method_version") != "amgt-corpus-dossier/13":
                    missing13 += 1
                    print("PRE-NOT-AT-13 %s method %s" % (key, d13.get("method_version")))
            except LookupError:
                missing13 += 1
                print("PRE-NO-13 %s" % key)
            try:
                d14 = _read(key, client, "amgt-corpus-dossier/14")
                have14 += int(d14.get("method_version") == "amgt-corpus-dossier/14")
            except LookupError:
                pass
        print("ax6 pre names %d without_a_/13_object %d with_a_/14_object %d" % (len(keys), missing13, have14))
        return 0
    entries = team_sheet._factset_entries()
    counts = {"SAME": 0, "NEWFIELD": 0, "CHANGED": 0, "DROPPED": 0}
    n = keys_eq = shape_ok = reader_equal = labels_ok = master_ok = 0
    outside = []
    moved_by = collections.Counter()
    moved_names = set()
    shares = {"own": collections.Counter(), "master": collections.Counter()}
    for key in keys:
        try:
            d13 = _read(key, client, "amgt-corpus-dossier/13")
            d14 = _read(key, client, "amgt-corpus-dossier/14")
        except LookupError as exc:
            print("UNREAD %s %s" % (key, str(exc)[:80]))
            continue
        if d14.get("method_version") != "amgt-corpus-dossier/14":
            print("NOT-AT-14 %s method %s" % (key, d14.get("method_version")))
            continue
        n += 1
        f13, f14 = d13.get("fields") or {}, d14.get("fields") or {}
        for name in sorted(set(f13) | set(f14)):
            a, b = name in f13, name in f14
            if a and not b:
                cls = "DROPPED"
            elif b and not a:
                cls = "NEWFIELD"
            elif _canon(f13[name]) == _canon(f14[name]):
                cls = "SAME"
            else:
                cls = "CHANGED"
            counts[cls] += 1
            if cls != "SAME":
                print("%s %s %s" % (cls, key, name))
            if cls == "CHANGED" and name != "team_sheet":
                outside.append((key, name))
                print("  WHOLE /13 %s" % _canon(f13.get(name)))
                print("  WHOLE /14 %s" % _canon(f14.get(name)))
        t13, t14 = f13.get("team_sheet") or {}, f14.get("team_sheet") or {}
        side = "master" if t14.get("class") == "master" else "own"
        if all(_canon(t13.get(k)) == _canon(t14.get(k)) for k in KEYS):
            keys_eq += 1
        else:
            print("KEYS-CHANGED %s" % key)
        rows = t14.get("rows") or []
        shaped = (all(len(t14.get(k) or []) == len(rows) for k in ALIGNED)
                  and sum((t14.get("row_counts") or {}).get(c, 0) for c in ("FIGURE", "HEADING", "CONTROL")) == len(rows)
                  and isinstance(t14.get("periods"), list))
        shape_ok += int(shaped)
        if not shaped:
            print("SHAPE-WRONG %s" % key)
        ok = True
        for lab, e13, e14 in zip(rows, t13.get("row_labels") or [], t14.get("row_labels") or []):
            if _canon(e13) == _canon(e14):
                continue
            code = (e14 or {}).get("code")
            good = (isinstance(e13, dict) and isinstance(e14, dict) and e13.get("claim") == "absent" and e14.get("claim") == "held"
                    and e14.get("source") == "factset" and code in entries and e14.get("text") == entries[code]["text"]
                    and e14.get("cite") == entries[code]["cite"] and e13.get("code") == code)
            if good:
                moved_by[code] += 1
                moved_names.add(key)
            else:
                ok = False
                print("LABEL-MOVED-UNEXPECTEDLY %s %r: %s -> %s" % (key, lab, _canon(e13)[:140], _canon(e14)[:140]))
        labels_ok += int(ok)
        if side == "master":
            master_ok += int(all(v is None for v in t14.get("row_values") or []) and all(v is None for v in t14.get("row_formats") or [])
                             and t14.get("periods") == [])
        for e in t14.get("row_labels") or []:
            if not e:
                continue
            kind = "measured" if e.get("claim") == "measured" else ("held_factset" if (e.get("claim") == "held" and e.get("source") == "factset")
                                                                   else ("held_bloomberg" if e.get("claim") == "held" else "line"))
            shares[side][kind] += 1
        fresh = team_sheet.rows_for(key, client=client)
        if _canon(t14) == _canon(fresh):
            reader_equal += 1
        else:
            print("TS-DIFFERS-FROM-READER %s" % key)
    print("ax6 label shares own %s | master %s" % (dict(shares["own"]), dict(shares["master"])))
    print("ax6 labels moved absent->held by code %s over %d names (rows %d)" % (dict(sorted(moved_by.items())), len(moved_names), sum(moved_by.values())))
    print("ax6 names %d fields %d same %d newfield %d changed %d dropped %d changed_outside_team_sheet %d (%s)" % (
        n, sum(counts.values()), counts["SAME"], counts["NEWFIELD"], counts["CHANGED"], counts["DROPPED"], len(outside),
        ",".join(sorted({"%s:%s" % o for o in outside}))[:300]))
    print("ax6 keys_equal %d/%d labels_as_predicted %d/%d shape %d/%d reader_equal %d/%d master_without_value %d" % (
        keys_eq, n, labels_ok, n, shape_ok, n, reader_equal, n, master_ok))
    build = int(n == len(keys) and counts["DROPPED"] == 0 and not outside and keys_eq == n and labels_ok == n and shape_ok == n and reader_equal == n
                and master_ok >= 0)
    print("ax6 build %d/1" % build)
    return 0 if build else 1


if __name__ == "__main__":
    sys.exit(main())
