"""Round 80, cell R2 (CTO round-79 analysis R2): a citation heading is never a bare number or percentage.

--crit AC1  the built behaviour, on plants: passages.heading_has_words / passages.clean_location exist and
            build_passage_map never carries a letterless line as a heading; ids, spans and texts unchanged.
--crit AC2  the seam against the REAL store (read only): every drafting/v1 document served through
            scoped_amgt.read_drafted_sections; letterless headings counted in the stored records (before)
            and in what is served (after), denominator printed. The store itself is never written.
--crit AC3  the bound: what is served differs from the stored records ONLY in `location`, and only where
            the stored location carried a letterless heading.

A heading is "letterless" when it holds no alphabetic character (str.isalpha), e.g. '5.09%', '1', '(1)',
'2025 2024 2023', '$1.19 ($20.38)'. The first segment (the item) and the last ('paragraph N') are not headings.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile

BUCKET = "opal-data-harvest"
PREFIX = "drafting/v1/"


def letterless(segment):
    return not any(ch.isalpha() for ch in segment)


def bad_headings(location):
    parts = [p.strip() for p in str(location or "").split(" / ")]
    return [p for p in parts[1:-1] if letterless(p)]


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def ac1():
    from lib.research.filings import passages as P

    results = []
    has = hasattr(P, "heading_has_words") and hasattr(P, "clean_location")
    results.append(say(has, "P1 passages.heading_has_words and passages.clean_location exist"))
    long_a = "A" * 10 + " the first long paragraph of the risk factor section, well over sixty characters."
    long_b = "The second long paragraph, which in the stored 20-F followed a percentage line in a table."
    long_c = "The third long paragraph, after a real short heading line that names a section of the filing."
    excerpt = "\n".join([
        "ITEM 3.D. RISK FACTORS", "General Meeting.", long_a, "5.09%", "0.01%", long_b,
        "(1)", "Our customers", "2025 2024 2023", long_c,
    ])
    pm = P.build_passage_map(excerpt, ["ITEM 3.D. RISK FACTORS"])
    locs = [p["location"] for p in pm]
    print("   plant locations: %s" % locs)
    results.append(say(len(pm) == 3, "P2 three passages (short lines are never passages)"))
    results.append(say(all(not bad_headings(loc) for loc in locs), "P3 no location carries a letterless heading"))
    results.append(say(len(locs) == 3 and "General Meeting." in locs[0] and "Our customers" in locs[2],
                       "P4 a heading with words is still carried"))
    spans_ok = [(p["id"], p["start"], p["end"], p["text"]) for p in pm] == [
        ("P%04d" % i, excerpt.index(t), excerpt.index(t) + len(t), t) for i, t in enumerate([long_a, long_b, long_c])]
    results.append(say(spans_ok, "P5 ids, spans and texts are what the excerpt holds (unchanged rule)"))
    if has:
        cases = {
            "ITEM 3.D. RISK FACTORS / 5.09% / paragraph 65": "ITEM 3.D. RISK FACTORS / paragraph 65",
            "ITEM 7. MD&A / $1.19 ($20.38) ($5.81) / paragraph 17": "ITEM 7. MD&A / paragraph 17",
            "ITEM 3.D. RISK FACTORS / General Meeting. / paragraph 60": "ITEM 3.D. RISK FACTORS / General Meeting. / paragraph 60",
            "ITEM 7 / paragraph 3": "ITEM 7 / paragraph 3",
            "": "",
            None: "",
        }
        got = {k: P.clean_location(k) for k in cases}
        print("   clean_location: %s" % got)
        results.append(say(got == cases, "P6 clean_location drops only a letterless heading"))
        results.append(say(P.heading_has_words("General Meeting.") and not P.heading_has_words("0.01%")
                           and not P.heading_has_words("(1)"), "P7 heading_has_words"))
    else:
        results.append(say(False, "P6 clean_location drops only a letterless heading"))
        results.append(say(False, "P7 heading_has_words"))
    return all(results)


def _fetch_store(dest):
    import boto3

    s3 = boto3.client("s3", region_name="us-east-1")
    keys = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
        keys += [o["Key"] for o in page.get("Contents", []) if o["Key"].endswith(".json")]
    for key in keys:
        with open(os.path.join(dest, key[len(PREFIX):]), "wb") as fh:
            fh.write(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())
    return sorted(k[len(PREFIX):-len(".json")] for k in keys)


def _served(names, root):
    from lib.research.api import scoped_amgt

    os.environ["AMGT_DRAFTING_ROOT"] = root
    out = {}
    for name in names:
        stored = json.load(open(os.path.join(root, name + ".json"), encoding="utf-8"))
        block = scoped_amgt.read_drafted_sections(name)
        out[name] = (stored, block)
    return out


def _served_evidence(block):
    for section in block.get("drafted_sections") or block.get("sections") or []:
        for sentence in section.get("sentences") or []:
            for ev in sentence.get("evidence") or []:
                yield ev.get("id"), ev.get("passage"), (ev.get("source") or {})
    for pid, item in (block.get("thesis_driver_passages") or {}).items():
        yield pid, item.get("passage_text"), (item.get("passage_cite") or {})


def ac2_ac3(crit):
    with tempfile.TemporaryDirectory() as root:
        names = _fetch_store(root)
        served = _served(names, root)
    print("   names in s3://%s/%s: %d" % (BUCKET, PREFIX, len(names)))
    stored_n = stored_bad = served_n = served_bad = 0
    drift = []
    changed = changed_ok = 0
    for name, (stored, block) in served.items():
        recs = {r.get("id"): r for r in stored.get("evidence_records") or []}
        for r in recs.values():
            stored_n += 1
            stored_bad += 1 if bad_headings((r.get("source") or {}).get("location")) else 0
        status = block.get("drafting_status")
        for pid, passage, source in _served_evidence(block):
            served_n += 1
            loc = source.get("location")
            served_bad += 1 if bad_headings(loc) else 0
            rec = recs.get(pid) or {}
            rsrc = rec.get("source") or {}
            if (rec.get("passage") or "") != (passage or ""):
                drift.append((name, pid, "passage"))
            for k in source:  # a driver cite carries only accession + location
                if k != "location" and k != "accession" and rsrc.get(k) != source.get(k):
                    drift.append((name, pid, k))
            if loc != rsrc.get("location"):
                changed += 1
                if bad_headings(rsrc.get("location")) and not bad_headings(loc):
                    changed_ok += 1
                else:
                    drift.append((name, pid, "location changed without a letterless heading"))
        print("   %-18s status=%s" % (name, status))
    if crit == "AC2":
        print("   stored records: %d, with a letterless heading: %d" % (stored_n, stored_bad))
        print("   served citations: %d, with a letterless heading: %d" % (served_n, served_bad))
        r = [say(stored_n > 0 and served_n > 0, "S1 the store was read and cites were served (N of N names: %d)" % len(names)),
             say(stored_bad > 0, "S2 positive control: the store still carries letterless headings (fix is at the read)"),
             say(served_bad == 0, "S3 no served citation names a letterless heading")]
        return all(r)
    print("   served citations: %d, location changed: %d, of which a letterless heading dropped: %d" % (served_n, changed, changed_ok))
    print("   drift: %d %s" % (len(drift), drift[:5]))
    return say(served_n > 0 and not drift, "B1 only `location` moves, and only where it carried a letterless heading")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1", "AC2", "AC3"])
    ap.add_argument("--where", default="local")
    a = ap.parse_args()
    ok = ac1() if a.crit == "AC1" else ac2_ac3(a.crit)
    print("R80 R2 %s SERVED: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
