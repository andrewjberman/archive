"""AMGT_CORPUS round 44, CRPS-at-1 AMENDMENT 2 (the /11 re-write; CTO rulings msg 3213, 3317 withdrawn by 3351) -- the diff of EVERY
dossier field, all names, of the WRITTEN /11 objects against the served /10. Issuer's file. READ-ONLY: S3 reads only; nothing written.

  PYTHONPATH=. python at10_diff.py --pre     before leg w: counts of stored /10 and /11 objects per name (expect /11 = 0 everywhere)
  PYTHONPATH=. python at10_diff.py --post    the WRITTEN /11 objects (read_dossier with METHOD_VERSION at /11) against /10

Per name and field of doc["fields"] (every field the dossier carries), the /11 object is classed against the /10 object:
  SAME      equal to /10
  NEWFIELD  absent at /10, present at /11 (expected: `team_sheet` and nothing else, on every name)
  CHANGED   present at both, unequal (expected: only the changed-input class `model_rows`, fed by the daily model block; every one
            is printed WHOLE; any other field is Branch C)
  DROPPED   present at /10, absent at /11 (must be 0)
Also, per name, the stored `team_sheet` is compared to a fresh `team_sheet.rows_for(key)` (the reader's own answer): they must be equal.
Prints `at10 method <v>`, the NEWFIELD / CHANGED / DROPPED lines, the team_sheet class counts, then
`at10 names <n> fields <f> same <s> newfield <w> changed <c> dropped <d> changed_outside_inputs <o> ts_equal_reader <e>/<n>` and
`at10 build <0|1>/1` (build = names 95, newfield set == {team_sheet} on all, dropped 0, changed_outside_inputs 0, ts_equal_reader all).
"""
import json
import sys

from lib.research.corpus import dossier, team_sheet
from lib.research.harvest import store

CHANGED_INPUT_CLASS = {"model_rows"}


def _read(key, client, method):
    current = dossier.METHOD_VERSION
    dossier.METHOD_VERSION = method
    try:
        return dossier.read_dossier(key, client=client)["document"]
    finally:
        dossier.METHOD_VERSION = current


def _canon(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=True)


def _method_of(doc):
    return doc.get("method_version")


def main():
    mode = "--post" if "--post" in sys.argv else "--pre"
    print("at10 method %s mode %s" % (dossier.METHOD_VERSION, mode))
    client = store._default_client()
    keys = dossier._resolved_security_keys(client=client)
    n = 0
    if mode == "--pre":
        have11 = 0
        for key in keys:
            d10 = _read(key, client, "amgt-corpus-dossier/10")
            try:
                d11 = _read(key, client, "amgt-corpus-dossier/11")
                has = _method_of(d11) == "amgt-corpus-dossier/11"
            except LookupError:
                has = False
            have11 += int(has)
            n += 1
            if _method_of(d10) != "amgt-corpus-dossier/10":
                print("PRE-NOT-AT-10 %s method %s" % (key, _method_of(d10)))
        print("at10 pre names %d with_a_/11_object %d" % (n, have11))
        return 0
    counts = {"SAME": 0, "NEWFIELD": 0, "CHANGED": 0, "DROPPED": 0}
    newfield_names, outside, ts_equal = set(), 0, 0
    classes = {}
    for key in keys:
        try:
            d10 = _read(key, client, "amgt-corpus-dossier/10")
            d11 = _read(key, client, "amgt-corpus-dossier/11")
        except LookupError as exc:
            print("UNREAD %s %s" % (key, str(exc)[:80]))
            continue
        if _method_of(d11) != "amgt-corpus-dossier/11":
            print("NOT-AT-11 %s method %s" % (key, _method_of(d11)))
            continue
        n += 1
        f10, f11 = d10.get("fields") or {}, d11.get("fields") or {}
        for name in sorted(set(f10) | set(f11)):
            in10, in11 = name in f10, name in f11
            if in10 and not in11:
                cls = "DROPPED"
            elif in11 and not in10:
                cls = "NEWFIELD"
                if name == "team_sheet":
                    newfield_names.add(key)
            elif _canon(f10[name]) == _canon(f11[name]):
                cls = "SAME"
            else:
                cls = "CHANGED"
            counts[cls] += 1
            if cls != "SAME":
                print("%s %s %s" % (cls, key, name))
            if cls == "CHANGED":
                if name not in CHANGED_INPUT_CLASS:
                    outside += 1
                print("  WHOLE /10 %s" % _canon(f10.get(name)))
                print("  WHOLE /11 %s" % _canon(f11.get(name)))
            if cls == "NEWFIELD" and name != "team_sheet":
                outside += 1
        stored = f11.get("team_sheet")
        fresh = team_sheet.rows_for(key, client=client)
        classes[(stored or {}).get("class")] = classes.get((stored or {}).get("class"), 0) + 1
        if _canon(stored) == _canon(fresh):
            ts_equal += 1
        else:
            print("TS-DIFFERS-FROM-READER %s" % key)
    print("at10 team_sheet classes %s" % json.dumps(classes, sort_keys=True, default=str))
    print("at10 names %d fields %d same %d newfield %d changed %d dropped %d changed_outside_inputs %d ts_equal_reader %d/%d" % (
        n, sum(counts.values()), counts["SAME"], counts["NEWFIELD"], counts["CHANGED"], counts["DROPPED"], outside, ts_equal, n))
    build = int(n == 95 and len(newfield_names) == 95 and counts["DROPPED"] == 0 and outside == 0 and ts_equal == n)
    print("at10 build %d/1" % build)
    return 0 if build else 1


if __name__ == "__main__":
    sys.exit(main())
