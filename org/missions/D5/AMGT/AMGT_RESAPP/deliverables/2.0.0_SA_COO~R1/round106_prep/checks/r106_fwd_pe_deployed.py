"""AMGT_RESAPP round-106 PREP -- `AMGT-bm-3`: the DEPLOYED read of `AMGT-bm-2`'s forward P/E withhold, against a capture taken IMMEDIATELY before the apply.

  PYTHONPATH=<checkout root> python r106_fwd_pe_deployed.py capture <out.json> [--workers 4]
  PYTHONPATH=<checkout root> python r106_fwd_pe_deployed.py verify <population.json> <pre.json> [--workers 4]

`capture` reads the LIVE function's /thesis body for every resolved name and writes {key: [status, body]}; it writes nothing else (the file stays local, uncommitted).
`verify` reads the live function NOW (the candidate) and checks it against the capture (the base), with the same six arms as `r106_fwd_pe_check.py`
(F1 to F6: the deployed function serves exactly the captured BEST_PE_RATIO rows minus the different-currency rows; kept rows equal; every withheld row has a
`model.forecast_withheld` entry naming both codes; PBR US names USD and BRL; no other path moved (floats and clocks only); the withheld count equals the population)
and one more:
  F7  the AI-fill hold is intact: every name's `ai_fill` reads status ABSENT with blocks {} before AND after (the apply must not move the environment variable).
Dry run before the apply: `R106_POST_LOCAL=1` reads the checkout's own handler as the deployed side (run it from the pin's worktree; it must read YES), and without it the same call reads NO (the base function still serves the rows).
Prints the same summary line and `R106 FORWARD PE DEPLOYED: YES|NO (n of 7 arms)`. Writes nothing.
"""
import concurrent.futures
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, ".")
import r106_fwd_pe_check as c  # noqa: E402  (its helpers: live, set_aside, walk, same_number, pe_rows, CLOCK)
from lib.research.corpus import dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402


def keys():
    return sorted(dossier._resolved_security_keys(client=store._default_client()))


def workers():
    return int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4


def capture(out):
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers()) as pool:
        res = list(pool.map(lambda k: (k, c.live(k)), keys()))
    json.dump({k: [s, b] for k, (s, b) in res}, open(out, "w", encoding="utf-8"))
    print("captured %d names, status not 200: %s" % (len(res), [k for k, (s, _) in res if s != 200][:4]))
    return 0


def verify(pop_path, pre_path):
    pop = json.load(open(pop_path, encoding="utf-8"))
    pre = json.load(open(pre_path, encoding="utf-8"))
    expected = {}
    for r in pop:
        for row in r["rows"]:
            p, e = (row.get("price_currency") or ""), (row.get("eps_currency") or "")
            if p and e and p.upper() != e.upper():
                expected[(r["key"], str(row["fiscal_year"]))] = (p, e)
    ks = sorted(pre)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers()) as pool:
        post = dict(zip(ks, pool.map(c.local if os.environ.get("R106_POST_LOCAL") == "1" else c.live, ks)))
    f1 = f2 = f3 = f5 = f7 = True
    withheld = base_n = cand_n = 0
    names_w = set()
    bad = []
    for k in ks:
        (sb, b), (sa, a) = pre[k], post[k]
        if (sb, sa) != (200, 200):
            bad.append(k)
        rb, ra = c.pe_rows(b), c.pe_rows(a)
        unresolved = [u for u in ((a.get("model") or {}).get("forecast_withheld") or []) if u.get("mnemonic") == c.MN]
        base_n += len(rb)
        cand_n += len(ra)
        want = {x: v for x, v in rb.items() if (k, x[0]) in expected}
        keep = {x for x in rb if x not in want}
        if set(ra) != keep:
            f1 = False
            print("  F1 %s: deployed rows %s vs expected %s" % (k, sorted(ra)[:4], sorted(keep)[:4]))
        for x in keep:
            if ra.get(x) != rb[x]:
                f2 = False
                print("  F2 %s %s differs" % (k, x))
        for x in want:
            withheld += 1
            names_w.add(k)
            p, e = expected[(k, x[0])]
            hit = [u for u in unresolved if str(u.get("fiscal_year")) == x[0] and p in str(u.get("reason")) and e in str(u.get("reason"))]
            if not hit:
                f3 = False
                print("  F3 %s %s: no forecast_withheld entry naming %s and %s" % (k, x, p, e))
        nb, na = c.set_aside(b, {"rows": 0, "check": 0}), c.set_aside(a, {"rows": 0, "check": 0})
        other = [(p, x, y) for p, x, y in c.walk(nb, na) if not (c.CLOCK.search(p) or c.same_number(x, y))]
        if other:
            f5 = False
            print("  F5 %s %s" % (k, other[0][0][:80]))
        for side, body in (("pre", b), ("post", a)):
            fill = body.get("ai_fill") or {}
            if fill.get("status") != "ABSENT" or fill.get("blocks") not in ({}, None):
                f7 = False
                print("  F7 %s %s ai_fill status %s" % (k, side, fill.get("status")))
    pbr = post.get("PBR_US_Equity")
    pbr_a = pbr[1] if pbr else {}
    pbr_u = [u for u in ((pbr_a.get("model") or {}).get("forecast_withheld") or []) if u.get("mnemonic") == c.MN]
    f4 = bool(pbr and not c.pe_rows(pbr_a) and pbr_u and all("USD" in str(u.get("reason")) and "BRL" in str(u.get("reason")) for u in pbr_u))
    f6 = withheld == len(expected)
    print("names %d | captured forward P/E rows %d | deployed %d | withheld %d (population %d) | names with a withheld row %d | status not (200, 200): %s" % (len(ks), base_n, cand_n, withheld, len(expected), len(names_w), bad[:4]))
    arms = [("F1 deployed rows = captured rows minus the different-currency rows", f1), ("F2 kept rows equal the capture's", f2), ("F3 every withheld row has a reason naming both currencies", f3),
            ("F4 PBR US withholds with a reason naming USD and BRL", f4), ("F5 no other path differs (floats and clocks only)", f5), ("F6 withheld count equals the population", f6),
            ("F7 the AI-fill hold is intact before and after", f7)]
    for name, ok in arms:
        print("   %s %s" % ("PASS" if ok else "FAIL", name))
    ok = all(x for _, x in arms) and not bad
    print("R106 FORWARD PE DEPLOYED: %s (%d of 7 arms)" % ("YES" if ok else "NO", sum(1 for _, x in arms if x)))
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "capture":
        sys.exit(capture(sys.argv[2]))
    if len(sys.argv) >= 4 and sys.argv[1] == "verify":
        sys.exit(verify(sys.argv[2], sys.argv[3]))
    print(__doc__)
    sys.exit(2)
