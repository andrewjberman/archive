#!/usr/bin/env python3
"""MDPF_CANON round 11, CN-s-7 -- the issuer's D4 grader (read-only): D4-new against D4-ref and the pair's section 2.

  python r11_cn_s_7_d4.py --ref <d4_ref_response.json> --new <d4_new_response.json> [--stored <dir of global__<type>.json>]

Gates (pair NEVER_WIDEN_PAIR_R11_CN_S_7.md section 2; CTO half @2fe324e11e: D4-new is the whole gate):
  G1  new: status green, errors empty, a4_objects_built 16, 16 bodies.
  G2  new Global aggregate: as_of_last is 2026-10-16, equal to the 49financial and inflection as_of_last of the SAME response,
      with 499 dates and the dated key 2026-10-16.
  G3  new Global headline non-None: last-row model_aua, opal_aggregate_aua, non_model_aua; aum-metrics total.aum.
  G4  new Global: no None model_value for the five core models on any date from 2026-07-21 to as_of_last.
  G5  the 12 non-Global bodies of new equal ref's, parsed, volatile paths removed (denominator printed).
LISTED, never graded (CTO): per Global artifact, the business-diff path counts of new against ref (same function before and
after, same legs) and, with --stored, against the stored 2026-10-15 objects; paths printed (first 10 non-timestamp), no value.
Exit 0 only when G1-G5 pass. ASCII only.
"""
import argparse
import json
import os
import sys

CORE = ("opal_ultra_short_term", "opal_short_term", "opal_intermediate", "opal_long_term_conservative", "opal_long_term_aggressive")
VOL = ("_provenance.process_time", "_provenance.trigger", "_provenance.source_vintage_age_hours", "generated_at",
       "last_updated", "meta.generated_at", "_provenance.written_at")
TYPES = ("aggregate-aua-timeseries", "aum-metrics", "category-views", "account-distribution")
res = []


def arm(name, ok, note=""):
    res.append(bool(ok))
    print("  %-3s %s %s" % (name, "PASS" if ok else "FAIL", note))


def body(r, key):
    b = r["bodies"][key]
    return json.loads(b["body"]) if isinstance(b, dict) and "body" in b else (json.loads(b) if isinstance(b, str) else b)


def paths(x, y, p=""):
    """business-diff paths of two parsed bodies (volatile and *.generated_at paths removed)"""
    out = []
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y)):
            q = (p + "." + k) if p else k
            if q in VOL or k == "generated_at":
                continue
            if k not in x or k not in y:
                out.append(q)
            else:
                out += paths(x[k], y[k], q)
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            out.append(p + "[len %d->%d]" % (len(x), len(y)))
        for i, (u, v) in enumerate(zip(x, y)):
            out += paths(u, v, "%s[%d]" % (p, i))
    elif x != y:
        out.append(p)
    return out


def key_of(r, scope, atype):
    return next(k for k in r["bodies"] if k.startswith("portal/gold/mdpf/%s/%s/" % (scope, atype)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--stored")
    a = ap.parse_args()
    R = json.load(open(a.ref))
    N = json.load(open(a.new))
    print("ROUND 11 CN-S-7 D4: ref status=%s errors=%s a4=%s bodies=%d | new status=%s errors=%s a4=%s bodies=%d" % (
        R.get("status"), R.get("errors"), R.get("a4_objects_built"), len(R["bodies"]),
        N.get("status"), N.get("errors"), N.get("a4_objects_built"), len(N["bodies"])))
    arm("G1", N.get("status") == "green" and N.get("errors") == [] and N.get("a4_objects_built") == 16 and len(N["bodies"]) == 16)

    gkey = key_of(N, "global", "aggregate-aua-timeseries")
    g = body(N, gkey)
    a49 = body(N, key_of(N, "49financial", "aggregate-aua-timeseries"))
    ainf = body(N, key_of(N, "inflection", "aggregate-aua-timeseries"))
    D = g["dates"]
    arm("G2", g["as_of_last"] == "2026-10-16" == a49["as_of_last"] == ainf["as_of_last"] and len(D) == 499 and gkey.endswith("/2026-10-16.json"),
        "global key=%s as_of_last=%s 49f=%s inf=%s dates=%d" % (gkey.rsplit("/", 1)[-1], g["as_of_last"], a49["as_of_last"], ainf["as_of_last"], len(D)))
    i = len(D) - 1
    am = body(N, key_of(N, "global", "aum-metrics"))
    tot = (am.get("total") or {}).get("aum")
    head = {k: g[k][i] is not None for k in ("model_aua", "opal_aggregate_aua", "non_model_aua")}
    arm("G3", all(head.values()) and tot is not None, "last-row present %s aum-metrics total.aum present=%s" % (head, tot is not None))
    bad = [(k, D[j]) for k in CORE if k in g["by_model"] for j in range(len(D)) if D[j] >= "2026-07-21" and g["by_model"][k]["model_value"][j] is None]
    arm("G4", not bad and all(k in g["by_model"] for k in CORE), "core None cells since 2026-07-21=%d keys present=%d of 5" % (len(bad), sum(k in g["by_model"] for k in CORE)))

    nonglobal = [k for k in R["bodies"] if "/global/" not in k]
    diff = [k for k in nonglobal if k not in N["bodies"] or paths(body(R, k), body(N, k))]
    arm("G5", len(nonglobal) == 12 and not diff, "non-global bodies compared=%d differing=%d %s" % (len(nonglobal), len(diff), [k.split("mdpf/")[1] for k in diff][:4]))

    print("  LISTED (not graded): Global business diffs, counts and paths only")
    for t in TYPES:
        try:
            kn = key_of(N, "global", t)
            kr = key_of(R, "global", t)
        except StopIteration:
            print("    %-26s missing in a response" % t)
            continue
        d = paths(body(R, kr), body(N, kn))
        print("    %-26s new key %s vs ref key %s: %d diff path(s) %s" % (t, kn.rsplit("/", 1)[-1], kr.rsplit("/", 1)[-1], len(d), d[:10]))
        if a.stored:
            f = os.path.join(a.stored, "global__%s.json" % t)
            if os.path.exists(f):
                s = json.load(open(f))
                s = json.loads(s["body"]) if isinstance(s, dict) and "body" in s and len(s) < 4 else s
                ds = paths(s, body(N, kn))
                print("    %-26s vs stored: %d diff path(s) %s" % ("", len(ds), ds[:10]))
    k = sum(res)
    print("ROUND 11 CN-S-7 D4: %d of %d gates" % (k, len(res)))
    return 0 if k == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
