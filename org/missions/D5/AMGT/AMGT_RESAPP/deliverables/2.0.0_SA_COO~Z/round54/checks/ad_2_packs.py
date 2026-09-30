"""AMGT_RESAPP round 54, AMGT-ad-2 AC3 (AMENDMENT 1, CTO msg 27301) -- the one reader that takes the stored D-1 text WITHOUT the at-read
hold: the posture evidence pack (`lib/research/posture/packs.py` build_pack, read by `posture/judge.py`; every `sections[].sentences`
entry becomes a `drafted_sentence` element). Per stored D-1 document, the pack is built in process from the PRE-act bytes
(`<dir>/store/<key>.json`, saved by `ad_2_hold.py --what save`) and from the LIVE object, every other source stubbed identically, and:
  - the post pack's drafted-sentence texts, per section, equal the pre pack's minus EXACTLY the no-span sentences (the adapter's gate);
  - thesis_driver and every evidence_record element are byte-equal;
  - the total removed across the documents equals the pre-act no-span count.
The pack's S:<section>:<n> ids renumber within a section by construction (enumerate); texts are compared, never ids.
usage: python <this> --dir D   (from the repo root; S3 read-only)"""
import argparse
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.getcwd())
import boto3  # noqa: E402
from lib.research.filings import drafting_build as db  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402
from lib.research.posture import packs  # noqa: E402

STUB = (None, "stub (not read by this check)")


def pack_of(key, doc):
    src = {"D-1": (doc, "drafting/v1/%s.json" % key), "M-1": STUB, "M-1-pool": STUB, "R-1": STUB, "model_block": STUB}
    return packs.build_pack(key, "2026-09-30", "subject", None, None, sources=src)


def by_section(pack):
    out = {}
    for eid, el in pack["elements"].items():
        if el["kind"] == "drafted_sentence":
            out.setdefault(eid.split(":")[1], Counter())[el["value"]["text"]] += 1
    return out


def others(pack):
    return json.dumps({k: v for k, v in pack["elements"].items() if v["kind"] in ("thesis_driver", "evidence_record")}, sort_keys=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    a = ap.parse_args()
    s3 = boto3.client("s3", region_name="us-east-1")
    pages = s3.get_paginator("list_objects_v2").paginate(Bucket=crosswalk.POOL_BUCKET, Prefix="drafting/v1/")
    keys = [o["Key"] for p in pages for o in p.get("Contents", []) if o["Key"].endswith(".json")]
    bad, removed_total, want_total = [], 0, 0
    for k in keys:
        name = k.rsplit("/", 1)[1][:-5]
        try:
            pre = json.load(open(os.path.join(a.dir, "store", name + ".json"), encoding="utf-8"))
        except FileNotFoundError:
            bad.append("%s: no pre-act capture" % name)
            continue
        post = db._get_json_object(s3, k)
        want = {}
        for sec in pre.get("sections") or []:
            for s in sec.get("sentences") or []:
                if not any(str(x).strip() for x in s.get("quoted_spans") or []):
                    want.setdefault(sec.get("section"), Counter())[s.get("text")] += 1
        p0, p1 = pack_of(name, pre), pack_of(name, post)
        s0, s1 = by_section(p0), by_section(p1)
        removed = {sec: s0.get(sec, Counter()) - s1.get(sec, Counter()) for sec in s0}
        added = {sec: s1.get(sec, Counter()) - s0.get(sec, Counter()) for sec in s1}
        n_removed = sum(sum(c.values()) for c in removed.values())
        n_want = sum(sum(c.values()) for c in want.values())
        removed_total += n_removed
        want_total += n_want
        why = []
        if any(sum(c.values()) for c in added.values()):
            why.append("sentences ADDED to the pack")
        if {s: c for s, c in removed.items() if c} != {s: c for s, c in want.items() if c}:
            why.append("removed %d, want exactly the %d no-span sentences" % (n_removed, n_want))
        if others(p0) != others(p1):
            why.append("thesis_driver or evidence_record elements moved")
        print("%s: pack drafted sentences %d -> %d, removed %d (want %d)%s"
              % (name, sum(sum(c.values()) for c in s0.values()), sum(sum(c.values()) for c in s1.values()), n_removed, n_want,
                 "" if not why else " BAD %s" % why))
        bad += ["%s: %s" % (name, w) for w in why]
    print("documents %d; pack sentences removed %d; no-span sentences pre-act %d" % (len(keys), removed_total, want_total))
    for b in bad[:20]:
        print("  BAD", b)
    ok = bool(keys) and not bad and removed_total == want_total and want_total > 0
    print("THE POSTURE PACK LOSES EXACTLY THE NO-SPAN SENTENCES: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
