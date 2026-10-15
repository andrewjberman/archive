"""ct_check.py -- grades one slice of the curated tags (NFRA_MCPINDEX round 18, RESEARCH, Z-C-S61). Run from the repo root.

  python ct_check.py slice <h1|h2|h3|p1>   the slice's group-map file (slices.json, key `file`) is a JSON object {"rows": {"<entity>": {"nl_tags": [...]}}} (an
                                           optional "_about" string is allowed) with exactly the slice's entities, each carrying ONLY the key nl_tags, in the form the
                                           ASSETS emitter's --group-map accepts (MX-c-21): 4 to 6 distinct tags; each tag 2 to 5 words of lowercase ASCII letters and
                                           digits joined by single spaces; at least 3 of the tags are NOT among the derived tags that derive_nl_tags.derive_tags gives
                                           the same row (so the tags are written, not copied); at least 1 tag shares a word of 4 or more letters with the row's own
                                           entity, meaning or example questions (the tags stay grounded in the row)

C30_CATALOG overrides the catalog read for the row text and CT_DIR the folder the slice file is read from (planted arms). Exit 0 PASS, 1 FAIL, 9 no run.
"""
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.environ.get("C30_CATALOG") or "infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml"
SECTIONS = ("silver_datasets", "portal_datasets", "harvest_datasets")
TAG = re.compile(r"^[a-z0-9]+( [a-z0-9]+){1,4}$")


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def rows():
    cat = yaml.safe_load(open(CATALOG, encoding="utf-8", errors="replace").read())
    return {r["entity"]: r for s in SECTIONS for r in cat.get(s, [])}


def grade(slice_id):
    spec = json.load(open(os.path.join(HERE, "slices.json"), encoding="utf-8"))
    if slice_id not in spec:
        print("ERROR: unknown slice %s" % slice_id)
        return 9
    path, want = spec[slice_id]["file"], spec[slice_id]["entities"]
    if os.environ.get("CT_DIR"):
        path = os.path.join(os.environ["CT_DIR"], os.path.basename(path))
    print("DENOMINATOR slice %s: %d entities assigned; file %s" % (slice_id, len(want), path))
    if not os.path.isfile(path):
        return report([("the curated-tags file exists", False)])
    try:
        got = json.load(open(path, encoding="utf-8"))
    except ValueError as e:
        return report([("the file is a JSON object (%s)" % str(e)[:60], False)])
    if not isinstance(got, dict) or not isinstance(got.get("rows"), dict):
        return report([("the file is a JSON object with a rows object", False)])
    shape = [e for e, v in got["rows"].items() if not (isinstance(v, dict) and sorted(v) == ["nl_tags"])]
    got = {e: (v.get("nl_tags") if isinstance(v, dict) else None) for e, v in got["rows"].items()}
    sys.path.insert(0, os.path.join("workflows", "atom_decomposition"))
    import derive_nl_tags
    allrows = rows()
    bad_shape, bad_count, bad_tag, dup, copied, ungrounded = [], [], [], [], [], []
    for e in want:
        tags = got.get(e)
        if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
            bad_shape.append(e)
            continue
        if not 4 <= len(tags) <= 6:
            bad_count.append(e)
        if [t for t in tags if not TAG.match(t)]:
            bad_tag.append(e)
        if len(set(tags)) != len(tags):
            dup.append(e)
        r = allrows.get(e)
        if r is None:
            bad_shape.append(e)
            continue
        derived = set(derive_nl_tags.derive_tags(e, r.get("business_meaning") or "", r.get("example_questions") or []))
        if sum(1 for t in tags if t not in derived) < 3:
            copied.append(e)
        text = " ".join([e, str(r.get("business_meaning") or "")] + [str(q) for q in (r.get("example_questions") or [])]).lower()
        grounded = set(w for w in re.findall(r"[a-z0-9]{4,}", text))
        if not any(w in grounded for t in tags for w in re.findall(r"[a-z0-9]{4,}", t.lower())):
            ungrounded.append(e)
    extra = sorted(set(got) - set(want))
    missing = sorted(set(want) - set(got))
    res = [("the rows object holds exactly the %d assigned entities (missing %d, extra %d)" % (len(want), len(missing), len(extra)), not missing and not extra),
           ("every entry is {\"nl_tags\": [strings]} for a row of the catalog (%d are not)" % (len(bad_shape) + len(shape)), not bad_shape and not shape),
           ("every row has 4 to 6 tags (%d do not)" % len(bad_count), not bad_count),
           ("every tag is 2 to 5 words of lowercase ASCII letters and digits (%d rows have a bad tag)" % len(bad_tag), not bad_tag),
           ("no row repeats a tag (%d do)" % len(dup), not dup),
           ("every row has at least 3 tags the derivation does not give (%d do not)" % len(copied), not copied),
           ("every row has a tag that shares a 4-letter word with the row's own text (%d do not)" % len(ungrounded), not ungrounded)]
    return report(res)


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "slice":
        print(__doc__)
        return 9
    return grade(sys.argv[2])


if __name__ == "__main__":
    sys.exit(main())
