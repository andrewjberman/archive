"""ADVI_FIRMBKTS round 3 check for cell FB-f-6 (the producer census: who writes 49 Financial's served platinum keys),
issuer 2.0.0_SA_COO~B1.

--census FILE grades PRODUCER_CENSUS.json (3 arms). The census is the blast radius the cutover window's step 2 (the
producers' repoint) needs. Shape:
  {"classes": [{"class": "<prefix>", "objects": N, "writers": [{"script": "<repo path>", "line": N,
                "key_expr": "<the text of the writing line's key>", "bucket_expr": "<how the bucket is chosen>",
                "runner": "<what runs it>", "schedule": "<its trigger or null>"}],
                "orphan": false, "orphan_evidence": "<only when orphan>"}],
   "bucket_seam": {"definition": "<repo path>:<line>", "scripts_reading_and_writing_through_it": N,
                   "separable_per_output": true|false, "evidence": "<one paragraph>"},
   "denominators": {"manifest_objects": N, "classes_in_table": N}}
  C1 every served class of the round-1 table (opal-data-bd, MOVE, platinum tier: 11) has exactly one entry, with
     object counts that sum to the F7 manifest's, and at least one writer or `orphan: true` with its evidence
  C2 every writer's script exists and its named line contains the text its `key_expr` quotes (re-read here, not trusted)
  C3 the seam: the definition line exists, and the count of scripts under the gold script directories that import it
     equals the census's number (re-counted here)
--root points at another tree. Never edit this file. Plain ASCII; the last line carries the arm count.
"""
import argparse
import gzip
import json
import os
import re
import subprocess
import sys

DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
MANIFEST = DELIV + "/0.9.0_WK_ADVI_FIRMBKTS~8/F7_MANIFEST.tsv.gz"
GOLD_DIRS = ("data/black_diamond/scripts/gold", "data/assets/scripts/gold")


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _classes(root):
    with open(os.path.join(root, DELIV, "mapping.json"), encoding="utf-8") as fh:
        rows = json.load(fh)["rows"]
    return sorted(r["prefix"] for r in rows if r.get("bucket") == "opal-data-bd" and r.get("disposition") == "MOVE"
                  and (r.get("dest") or {}).get("tier") == "platinum")


def census(root, path):
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    want = _classes(root)
    n_manifest = {}
    with gzip.open(os.path.join(root, MANIFEST), "rt", encoding="ascii") as fh:
        for line in fh:
            if not line.strip() or line.startswith("#"):
                continue
            src = line.split("\t")[0]
            # the longest class prefix owns the key (gold/platinum/firm/ before gold/...)
            owner = None
            for p in want:
                if src.startswith(p) and (owner is None or len(p) > len(owner)):
                    owner = p
            if owner:
                n_manifest[owner] = n_manifest.get(owner, 0) + 1
    entries = doc.get("classes") or []
    by = {}
    for e in entries:
        by.setdefault(e.get("class"), []).append(e)
    res = []
    ok1 = set(by) == set(want) and all(len(v) == 1 for v in by.values())
    tot = 0
    for p in want:
        e = (by.get(p) or [{}])[0]
        tot += e.get("objects") or 0
        if e.get("objects") != n_manifest.get(p, 0):
            print("    OBJECTS %s census=%r manifest=%d" % (p, e.get("objects"), n_manifest.get(p, 0)))
            ok1 = False
        if not e.get("writers") and not (e.get("orphan") is True and str(e.get("orphan_evidence", "")).strip()):
            print("    NO-WRITER-NO-ORPHAN %s" % p)
            ok1 = False
    print("  classes in the table=%d entries=%d objects=%d (manifest %d)" % (len(want), len(entries), tot,
                                                                         sum(n_manifest.values())))
    res.append(("C1 every served class has exactly one entry, its objects equal the F7 manifest's, and it names a "
                "writer or is an evidenced orphan", ok1 and tot == sum(n_manifest.values()) and bool(entries)))

    ok2 = True
    n_w = n_ok = 0
    for e in entries:
        for w in e.get("writers") or []:
            n_w += 1
            p = os.path.join(root, str(w.get("script", "")))
            try:
                with open(p, encoding="utf-8", errors="replace") as fh:
                    lines = fh.read().split("\n")
                text = lines[int(w["line"]) - 1]
                quote = str(w.get("key_expr", "")).strip()
                if quote and quote in text:
                    n_ok += 1
                else:
                    print("    LINE-MISMATCH %s:%s does not contain %r" % (w.get("script"), w.get("line"), quote[:60]))
                    ok2 = False
            except Exception as ex:  # noqa: BLE001
                print("    UNREADABLE %s:%s (%s)" % (w.get("script"), w.get("line"), type(ex).__name__))
                ok2 = False
            if not str(w.get("bucket_expr", "")).strip() or not str(w.get("runner", "")).strip():
                print("    WRITER-FIELDS %s:%s" % (w.get("script"), w.get("line")))
                ok2 = False
    print("  writers=%d with the named line re-read and containing the quoted key text=%d" % (n_w, n_ok))
    res.append(("C2 every writer's named line exists and contains the key text the census quotes, and names its "
                "bucket expression and runner", ok2 and n_w > 0))

    seam = doc.get("bucket_seam") or {}
    ok3 = False
    try:
        dpath, dline = str(seam.get("definition", "")).rsplit(":", 1)
        with open(os.path.join(root, dpath), encoding="utf-8", errors="replace") as fh:
            text = fh.read().split("\n")[int(dline) - 1]
        has_def = "S3_BUCKET" in text
        pat = re.compile(r"from\s+lib\.config\s+import[^\n]*\bS3_BUCKET\b")
        count = 0
        for d in GOLD_DIRS:
            top = os.path.join(root, d)
            for dp, _dn, fns in os.walk(top):
                for fn in fns:
                    if fn.endswith(".py"):
                        with open(os.path.join(dp, fn), encoding="utf-8", errors="replace") as fh:
                            if pat.search(fh.read()):
                                count += 1
        print("  seam definition line holds S3_BUCKET: %s; scripts importing it recounted=%d census=%r"
              % (has_def, count, seam.get("scripts_reading_and_writing_through_it")))
        ok3 = (has_def and count == seam.get("scripts_reading_and_writing_through_it")
               and isinstance(seam.get("separable_per_output"), bool) and bool(str(seam.get("evidence", "")).strip()))
    except Exception as ex:  # noqa: BLE001
        print("  seam unreadable (%s)" % type(ex).__name__)
    res.append(("C3 the bucket seam's definition line exists and the number of gold scripts importing it equals the "
                "recount", ok3))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--census", required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = census(root, a.census)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable census (%s: %s)" % (type(e).__name__, str(e)[:160]))
        res = [("PRODUCER_CENSUS.json is present and reads", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 3 PRODUCER CENSUS: %d of 3 arms" % n)
    sys.exit(0 if n == 3 else 1)


if __name__ == "__main__":
    main()
