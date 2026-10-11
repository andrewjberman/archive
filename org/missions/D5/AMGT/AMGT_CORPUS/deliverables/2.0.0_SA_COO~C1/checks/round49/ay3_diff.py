"""AMGT_CORPUS round 49, CRPS-ay-3 (the /15 dossier write; decomposition v49.1) -- the diff of EVERY dossier field of every served name,
the WRITTEN /15 objects against the stored /14, and the team_sheet read inside it. Issuer's file. READ-ONLY: S3 reads only.

  PYTHONPATH=. python ay3_diff.py --pre     before leg w: names with a stored /14 object and with a /15 object (expect /15 = 0 everywhere)
  PYTHONPATH=. python ay3_diff.py --post    the WRITTEN /15 objects (read_dossier at METHOD /15) against /14

Expected: CHANGED on `team_sheet` only; DROPPED 0; the team_sheet arm, per name:
  outside        rows, row_numbers, row_labels, periods, class, workbook_key, sheet, model_rows_beside, reason equal /14's; every row_class equal
                 except FIGURE -> BLOCK; row_values and row_formats equal /14's at every non-BLOCK row and null at a BLOCK row
  blocks         present iff a BLOCK row exists; each BLOCK row in exactly one block with block_row true; kind in period / case / unread; an unread block
                 has columns [] and no cell; no value cell under a header-less column (headerless 0); rows by kind sum to the BLOCK rows
  separators     every FIGURE row at /14 with an alphabetic text cell in a period column is a BLOCK row at /15 (the CVO's 62)
  master         a master answer's row_values and row_formats are all null and periods []; no numeric block cell that is not a header run
  reader_equal   the stored team_sheet equals a fresh team_sheet.rows_for(key)
Prints the split BLOCK rows by kind with the denominator (own / master; rows; FIGURE rows at /14) and `ay3 build <b>/1`.
"""
import collections
import json
import sys

from lib.research.corpus import dossier, team_sheet
from lib.research.harvest import store

SAME_KEYS = ("class", "workbook_key", "sheet", "rows", "model_rows_beside", "reason", "row_numbers", "row_labels", "periods")


def _read(key, client, method):
    current = dossier.METHOD_VERSION
    dossier.METHOD_VERSION = method
    try:
        return dossier.read_dossier(key, client=client)["document"]
    finally:
        dossier.METHOD_VERSION = current


def _canon(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=True)


def _alpha(v):
    if not isinstance(v, str) or not v.strip():
        return False
    t = v.strip()
    return (any(ch.isalpha() for ch in t) and not t.startswith("#") and t.lower() not in ("na", "n/a", "nm")
            and not all(ch in "0123456789.,%x -" for ch in t))


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _headerless(blocks):
    n = 0
    for blk in blocks:
        if blk["kind"] == "unread":
            continue
        headed = set()
        for r in blk["rows"]:
            for j, cell in enumerate(r["cells"]):
                if cell is not None and _num(cell["v"]) and r["kind"] == "body" and j not in headed:
                    n += 1
            if r["kind"] in ("title", "years"):
                headed.update(j for j, cell in enumerate(r["cells"]) if cell is not None)
    return n


def _check_name(t14, t15):
    """(ok, reasons, kinds Counter, block rows, headerless, withheld)."""
    why = []
    for k in SAME_KEYS:
        if _canon(t14.get(k)) != _canon(t15.get(k)):
            why.append("key:" + k)
    c14, c15 = t14.get("row_classes") or [], t15.get("row_classes") or []
    v14, v15 = t14.get("row_values") or [], t15.get("row_values") or []
    f14, f15 = t14.get("row_formats") or [], t15.get("row_formats") or []
    if not (len(c14) == len(c15) == len(v14) == len(v15) == len(f14) == len(f15) == len(t15.get("rows") or [])):
        why.append("shape")
        return False, why, collections.Counter(), 0, 0, 0
    block_idx = [i for i, c in enumerate(c15) if c == "BLOCK"]
    for i, (a, b) in enumerate(zip(c14, c15)):
        if a != b and not (a == "FIGURE" and b == "BLOCK"):
            why.append("class@%d" % i)
        if b == "BLOCK":
            if v15[i] is not None or f15[i] is not None:
                why.append("block-value@%d" % i)
        elif _canon(v14[i]) != _canon(v15[i]) or _canon(f14[i]) != _canon(f15[i]):
            why.append("value@%d" % i)
    counts = t15.get("row_counts") or {}
    want = {c: sum(1 for x in c15 if x == c) for c in ("FIGURE", "HEADING", "CONTROL")}
    if block_idx:
        want["BLOCK"] = len(block_idx)
    if counts != want:
        why.append("row_counts")
    blocks = t15.get("blocks")
    kinds = collections.Counter()
    withheld = 0
    if block_idx:
        if not blocks:
            why.append("blocks-absent")
            blocks = []
        numbers = t15.get("row_numbers") or []
        seen = collections.Counter()
        for blk in blocks:
            if blk.get("kind") not in ("period", "case", "unread"):
                why.append("kind")
            if blk.get("kind") == "unread" and (blk.get("columns") != [] or any(r["cells"] for r in blk["rows"]) or not blk.get("why")):
                why.append("unread-shape")
            withheld += int(blk.get("withheld") or 0)
            for r in blk["rows"]:
                if r["block_row"]:
                    seen[r["row_number"]] += 1
                    kinds[blk["kind"]] += 1
        for i in block_idx:
            if seen[numbers[i]] != 1:
                why.append("block-row-count@%d" % numbers[i])
        if sum(kinds.values()) != len(block_idx):
            why.append("kinds-sum")
    elif blocks is not None or "BLOCK" in counts:
        why.append("blocks-without-block-rows")
    hv = _headerless(blocks or [])
    if hv:
        why.append("headerless:%d" % hv)
    for i, (a, b) in enumerate(zip(c14, c15)):
        if a == "FIGURE" and v14[i] and any(_alpha(x) for x in v14[i]) and b != "BLOCK":
            why.append("separator-row-not-block@%d" % i)
    if t15.get("class") == "master":
        if any(x is not None for x in v15) or any(x is not None for x in f15) or t15.get("periods") != []:
            why.append("master-value")
        for blk in blocks or []:
            for r in blk["rows"]:
                runs = set()
                row = [None if cell is None else cell["v"] for cell in r["cells"]]
                for j, v in enumerate(row):
                    if _num(v) and 1990 <= v <= 2100 and float(v).is_integer():
                        runs.add(j)
                if any(_num(v) and j not in runs for j, v in enumerate(row)):
                    why.append("master-number")
                    break
    return not why, why, kinds, len(block_idx), hv, withheld


def main():
    mode = "--post" if "--post" in sys.argv else "--pre"
    print("ay3 method %s mode %s" % (dossier.METHOD_VERSION, mode))
    client = store._default_client()
    keys = sorted(dossier._resolved_security_keys(client=client))
    if mode == "--pre":
        have15 = missing14 = 0
        for key in keys:
            try:
                d14 = _read(key, client, "amgt-corpus-dossier/14")
                if d14.get("method_version") != "amgt-corpus-dossier/14":
                    missing14 += 1
                    print("PRE-NOT-AT-14 %s method %s" % (key, d14.get("method_version")))
            except LookupError:
                missing14 += 1
                print("PRE-NO-14 %s" % key)
            try:
                d15 = _read(key, client, "amgt-corpus-dossier/15")
                have15 += int(d15.get("method_version") == "amgt-corpus-dossier/15")
            except LookupError:
                pass
        print("ay3 pre names %d without_a_/14_object %d with_a_/15_object %d" % (len(keys), missing14, have15))
        return 0
    counts = {"SAME": 0, "NEWFIELD": 0, "CHANGED": 0, "DROPPED": 0}
    n = ok_names = reader_equal = 0
    outside = []
    bad = []
    split = {"own": collections.Counter(), "master": collections.Counter()}
    totals = collections.Counter()
    for key in keys:
        try:
            d14 = _read(key, client, "amgt-corpus-dossier/14")
            d15 = _read(key, client, "amgt-corpus-dossier/15")
        except LookupError as exc:
            print("UNREAD %s %s" % (key, str(exc)[:80]))
            continue
        if d15.get("method_version") != "amgt-corpus-dossier/15":
            print("NOT-AT-15 %s method %s" % (key, d15.get("method_version")))
            continue
        n += 1
        f14, f15 = d14.get("fields") or {}, d15.get("fields") or {}
        for name in sorted(set(f14) | set(f15)):
            a, b = name in f14, name in f15
            if a and not b:
                cls = "DROPPED"
            elif b and not a:
                cls = "NEWFIELD"
            elif _canon(f14[name]) == _canon(f15[name]):
                cls = "SAME"
            else:
                cls = "CHANGED"
            counts[cls] += 1
            if cls != "SAME":
                print("%s %s %s" % (cls, key, name))
            if cls == "CHANGED" and name != "team_sheet":
                outside.append((key, name))
        t14, t15 = f14.get("team_sheet") or {}, f15.get("team_sheet") or {}
        ok, why, kinds, nblock, hv, withheld = _check_name(t14, t15)
        ok_names += int(ok)
        if not ok:
            bad.append(key)
            print("TEAM-SHEET-WRONG %s %s" % (key, ",".join(why[:8])))
        side = "master" if t15.get("class") == "master" else "own"
        for k, v in kinds.items():
            split[side][k] += v
        totals["block_rows"] += nblock
        totals["withheld"] += withheld
        totals["headerless"] += hv
        totals["rows"] += len(t15.get("rows") or [])
        totals["figure_at_14"] += sum(1 for c in (t14.get("row_classes") or []) if c == "FIGURE")
        totals["blocks"] += len(t15.get("blocks") or [])
        fresh = team_sheet.rows_for(key, client=client)
        if _canon(t15) == _canon(fresh):
            reader_equal += 1
        else:
            print("TS-DIFFERS-FROM-READER %s" % key)
    print("ay3 split block_rows %d = period %d + case %d + unread %d ; own %s ; master %s" % (
        totals["block_rows"], split["own"]["period"] + split["master"]["period"], split["own"]["case"] + split["master"]["case"],
        split["own"]["unread"] + split["master"]["unread"], dict(split["own"]), dict(split["master"])))
    print("ay3 denominators names %d rows %d figure_rows_at_14 %d blocks %d withheld_cells %d headerless_values %d" % (
        n, totals["rows"], totals["figure_at_14"], totals["blocks"], totals["withheld"], totals["headerless"]))
    print("ay3 names %d fields %d same %d newfield %d changed %d dropped %d changed_outside_team_sheet %d (%s)" % (
        n, sum(counts.values()), counts["SAME"], counts["NEWFIELD"], counts["CHANGED"], counts["DROPPED"], len(outside),
        ",".join(sorted({"%s:%s" % o for o in outside}))[:300]))
    print("ay3 team_sheet_ok %d/%d reader_equal %d/%d" % (ok_names, n, reader_equal, n))
    build = int(n == len(keys) and counts["DROPPED"] == 0 and not outside and ok_names == n and reader_equal == n)
    print("ay3 build %d/1" % build)
    return 0 if build else 1


if __name__ == "__main__":
    sys.exit(main())
