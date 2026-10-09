"""AMGT_CORPUS round 41, CRPS-aq-3 close read: PICK THE NAME BY THE READ (analysis item 3). Issuer's file. Read-only
(S3 reads through the same library calls the scoped API serves; nothing is written; no Bloomberg or vendor call).

For every resolved name: the served thesis pillars (read_thesis_bundle -> dossier_fields.thesis_pillars), their REAL terms
(each pillar's terms[1:], distinct, as HeaderBrief.realPillarTerms), the served feed (read_security_overlay -> feed.items),
and the headlines naming a real term as a WHOLE WORD, case-insensitively (FeedList's match). A name qualifies for the walk
when it has >= 1 real term AND >= 1 such headline. Also lists the names whose pillars carry no real term (the no-term arm).

  PYTHONPATH=. python aq3_close_pick.py [--limit N]
"""
import re
import sys
import types

sys.modules.setdefault("fitz", types.ModuleType("fitz"))

from lib.research.api import scoped_amgt  # noqa: E402
from lib.research.corpus import dossier  # noqa: E402


def real_terms(pillars):
    if not pillars:
        return None
    out = []
    for p in pillars:
        for t in (p.get("terms") or [])[1:]:
            t = (t or "").strip()
            if t and t not in out:
                out.append(t)
    return out


def matches(term, title):
    pat = r"(?<![A-Za-z0-9])" + re.escape(term.lower()) + r"(?![A-Za-z0-9])"
    return re.search(pat, (title or "").lower()) is not None


def main(argv):
    limit = None
    if "--limit" in argv:
        limit = int(argv[argv.index("--limit") + 1])
    keys = sorted(dossier._resolved_security_keys())
    if limit:
        keys = keys[:limit]
    qualify, no_term, no_dossier, errors = [], [], [], []
    for k in keys:
        try:
            th = scoped_amgt.read_thesis_bundle(k)
            pillars = ((th or {}).get("dossier_fields") or {}).get("thesis_pillars")
            terms = real_terms(pillars)
            if terms is None:
                no_dossier.append(k)
                continue
            if not terms:
                no_term.append(k)
                continue
            ov = scoped_amgt.read_security_overlay(k)
            items = ((ov or {}).get("feed") or {}).get("items") or []
            hits = [(t, it.get("title")) for t in terms for it in items if matches(t, it.get("title"))]
            if hits:
                qualify.append((k, len(terms), len(items), hits))
        except Exception as exc:  # a failed read is listed, never counted as a negative
            errors.append((k, type(exc).__name__, str(exc)[:120]))
    for k, nt, ni, hits in qualify:
        print("QUALIFY %s real_terms %d feed_items %d hits %d first %r -> %r" % (k, nt, ni, len(hits), hits[0][0], hits[0][1]))
    for k in no_term:
        print("NO-TERM %s" % k)
    for k, e, m in errors:
        print("ERROR %s %s %s" % (k, e, m))
    print("aq3 pick names %d qualify %d no_term %d no_dossier %d errors %d"
          % (len(keys), len(qualify), len(no_term), len(no_dossier), len(errors)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
