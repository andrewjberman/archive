#!/usr/bin/env python3
"""MDPF_CANON round 11, CN-s-6 -- the issuer's D4 grader (read-only): D4-new against D4-ref and the pair's section 3.

  python r11_cn_s_6_d4.py --ref <d4_ref_response.json> --new <d4_new_response.json> [--served <fire served_response.json>]

Gates (pair NEVER_WIDEN_PAIR_R11_CN_S_6.md section 3, (i) to (iv) and (vi) reported as a flag where the response cannot
show it; CTO msg 7600):
  G1  new: status green, errors empty, a4_objects_built 16, 16 bodies.
  G2  new Global aggregate: as_of_last equals the 49financial and inflection as_of_last of the SAME response and is not 2026-10-16;
      its dates carry no 2026-10-16.
  G3  new Global headline non-None: last-row model_aua, opal_aggregate_aua, non_model_aua; aum-metrics total.aum.
  G4  new Global: no None model_value for the five core models on any date from 2026-07-21 to as_of_last.
  G5  the 12 non-Global bodies of new equal ref's, parsed, volatile paths removed (denominator printed).
  INFO (not a gate): with --served, the Global model_aua and non_model_aua deltas on 2026-10-15 against the fire-served object.
Prints counts, dates and flags only. Exit 0 only when G1-G5 pass. ASCII only.
"""
import argparse
import json
import sys

CORE = ("opal_ultra_short_term", "opal_short_term", "opal_intermediate", "opal_long_term_conservative", "opal_long_term_aggressive")
VOL = ("_provenance.process_time", "_provenance.trigger", "_provenance.source_vintage_age_hours", "generated_at",
       "last_updated", "meta.generated_at")
res = []


def arm(name, ok, note=""):
    res.append(bool(ok))
    print("  %-3s %s %s" % (name, "PASS" if ok else "FAIL", note))


def body(r, key):
    b = r["bodies"][key]
    return json.loads(b["body"]) if isinstance(b, dict) and "body" in b else (json.loads(b) if isinstance(b, str) else b)


def strip(o, path=""):
    if isinstance(o, dict):
        return {k: strip(v, (path + "." + k) if path else k) for k, v in o.items()
                if ((path + "." + k) if path else k) not in VOL and k != "generated_at"}
    if isinstance(o, list):
        return [strip(v, path + "[]") for v in o]
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--served")
    a = ap.parse_args()
    R = json.load(open(a.ref))
    N = json.load(open(a.new))
    print("ROUND 11 CN-S-6 D4: ref status=%s errors=%s a4=%s bodies=%d | new status=%s errors=%s a4=%s bodies=%d" % (
        R.get("status"), R.get("errors"), R.get("a4_objects_built"), len(R["bodies"]),
        N.get("status"), N.get("errors"), N.get("a4_objects_built"), len(N["bodies"])))
    arm("G1", N.get("status") == "green" and N.get("errors") == [] and N.get("a4_objects_built") == 16 and len(N["bodies"]) == 16)

    agg = "portal/gold/mdpf/%s/aggregate-aua-timeseries/"
    gkey = next(k for k in N["bodies"] if k.startswith(agg % "global"))
    g = body(N, gkey)
    a49 = body(N, next(k for k in N["bodies"] if k.startswith(agg % "49financial")))
    ainf = body(N, next(k for k in N["bodies"] if k.startswith(agg % "inflection")))
    D = g["dates"]
    arm("G2", g["as_of_last"] == a49["as_of_last"] == ainf["as_of_last"] and g["as_of_last"] != "2026-10-16" and "2026-10-16" not in D,
        "global key=%s as_of_last=%s 49f=%s inf=%s dates=%d has_1016=%s" % (gkey.rsplit("/", 1)[-1], g["as_of_last"], a49["as_of_last"], ainf["as_of_last"], len(D), "2026-10-16" in D))
    i = len(D) - 1
    am = body(N, next(k for k in N["bodies"] if k.startswith("portal/gold/mdpf/global/aum-metrics/")))
    tot = (am.get("total") or {}).get("aum")
    head = {k: g[k][i] is not None for k in ("model_aua", "opal_aggregate_aua", "non_model_aua")}
    arm("G3", all(head.values()) and tot is not None, "last-row present %s aum-metrics total.aum present=%s" % (head, tot is not None))
    bad = [(k, D[j]) for k in CORE if k in g["by_model"] for j in range(len(D)) if D[j] >= "2026-07-21" and g["by_model"][k]["model_value"][j] is None]
    arm("G4", not bad and all(k in g["by_model"] for k in CORE), "core None cells since 2026-07-21=%d keys present=%d of 5" % (len(bad), sum(k in g["by_model"] for k in CORE)))

    nonglobal = [k for k in R["bodies"] if "/global/" not in k]
    diff = [k for k in nonglobal if k not in N["bodies"] or strip(body(R, k)) != strip(body(N, k))]
    arm("G5", len(nonglobal) == 12 and not diff, "non-global bodies compared=%d differing=%d %s" % (len(nonglobal), len(diff), [k.split("mdpf/")[1] for k in diff][:4]))

    if a.served:
        try:
            S = json.load(open(a.served))["bodies"]
            sk = "portal/gold/mdpf/global/aggregate-aua-timeseries/2026-10-15.json"
            sg = json.loads(S[sk]["body"])
            SD = sg["dates"]
            for f in ("model_aua", "non_model_aua"):
                print("  INFO %s delta on 2026-10-15 vs fire-served: %.2f" % (f, g[f][D.index("2026-10-15")] - sg[f][SD.index("2026-10-15")]))
        except Exception as e:  # noqa: BLE001
            print("  INFO served compare skipped: %r" % (e,))
    k = sum(res)
    print("ROUND 11 CN-S-6 D4: %d of %d gates" % (k, len(res)))
    return 0 if k == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
