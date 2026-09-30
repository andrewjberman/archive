"""HVST-g-1 AC4 (JUDGMENT, presented and not graded): for every FORM with added hits under the new rule, up to 10
added hits (all if 10 or fewer, else drawn with the printed seed), each with headline, block, offset and the words
around the match. The question for the reader, per form: how many are the company? This script records NO verdict.
S3 GET/LIST only: no put, no delete, no vendor call."""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

SAMPLE_N = 10


def main():
    old_sec = C.load_json(C.OLD_PATH)
    new_sec = C.load_json(C.NEW_PATH)
    old_by, new_by = C.sec_map(old_sec), C.sec_map(new_sec)
    brands = C.brand_forms_by_security()
    articles, _hits, _served = C.fetch()
    print("== HVST-g-1 AC4 (JUDGMENT -- presented, NOT graded): added hits per form, sampled ==")
    print("seed=%d  sample=up to %d hits per form (all when %d or fewer), drawn per (class, form, security) with random.Random('<seed>|<class>|<form>|<security>')" % (
        C.SEED, SAMPLE_N, SAMPLE_N))
    print("securities=%d  silver articles=%d  matcher=publication_gold._span_pattern with the new ticker_aliases (exact case) + whole-brand aliases" % (
        len(new_sec), len(articles)))
    blocks = {}
    for art in articles:
        for key, nsec in new_by.items():
            osec = old_by.get(key)
            if osec is None:
                continue
            add, _lost = C.added_spans(art, osec, nsec, brands)
            for sp in add:
                sp = dict(sp)
                sp["article_key"] = art["article_key"]
                sp["headline"] = C.a(art.get("title"))
                sp["security_key"] = key
                blocks.setdefault((sp["class"], sp["form"], key), []).append(sp)
    total = sum(len(v) for v in blocks.values())
    by_class = {}
    for (cls, _f, _k), v in blocks.items():
        by_class[cls] = by_class.get(cls, 0) + len(v)
    print("forms with added hits (class, form, security): %d blocks; added hits=%d (%s)" % (
        len(blocks), total, ", ".join("%s=%d" % kv for kv in sorted(by_class.items()))))
    print("QUESTION FOR THE READER (3.0.0_SA_CVO~Z at L9), per form block: how many of the sampled hits ARE THE COMPANY? "
          "No verdict is recorded here.")
    sampled = 0
    for (cls, form, key), hits in sorted(blocks.items(), key=lambda kv: (kv[0][0], -len(kv[1]), kv[0][1], kv[0][2])):
        hits = sorted(hits, key=lambda h: (h["article_key"], h["where"], h["offset"]))
        if len(hits) <= SAMPLE_N:
            pick, how = hits, "ALL %d" % len(hits)
        else:
            rng = random.Random("%s|%s|%s|%s" % (C.SEED, cls, form, key))
            pick = sorted(rng.sample(hits, SAMPLE_N), key=lambda h: (h["article_key"], h["where"], h["offset"]))
            how = "%d of %d (seed %d)" % (SAMPLE_N, len(hits), C.SEED)
        sampled += len(pick)
        print("\n#### FORM %s '%s'  security=%s  added hits=%d  sampled=%s" % (cls, C.a(form), key, len(hits), how))
        for i, h in enumerate(pick, 1):
            print("  %2d. [%s] headline: %s" % (i, h["article_key"], h["headline"][:120]))
            print("      %s, offset %d, matched '%s': %s" % (h["where"], h["offset"], C.a(h["matched"]),
                                                         C.context(h["text"], h["offset"], h["end"])))
    print("\nFORM BLOCKS presented: %d; hits presented: %d of %d added hits" % (len(blocks), sampled, total))
    print("AC4 RESULT: PRESENTED (judgment; no verdict recorded)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
