"""c16_check.py -- grades MX-c-16 (the certified-channel corrections in the emitter), run from the repo root.

  python c16_check.py ac1   the NEW catalog: (a) the json/portfolios/aum-metrics.json row is deny + ruled; (b) no artifact row has a json/mdpf/ key and
                            the mdpf_model_portfolios channel lost exactly that one row; (c) the news channel text carries 381,261, not 298K, an
                            EMPTY marker for opal-harvest-articles and a frozen marker (2026-04-13) for the Seeking Alpha output
  python c16_check.py ac2   the CVO's difference control (3.0.0_SA_CVO~Z, R16_MX-c-16_PRE-ISSUE_READ_20261014.md condition 1): for EVERY known firm
                            principal (and opal-internal and two unknown firm ids) x EVERY key of the BASE catalog, the new key set, and the
                            scope-substituted json/mdpf/<scope>/<file> keys, catalog_gate.gate() old against new; prints the pair count and the
                            deny->serve count beside it; PASS only when deny->serve is 0 over a non-empty denominator
  python c16_check.py ac3   the CVO's condition 2: on the news channel and on every sentiment_news_mood artifact row, verdict_class, allowlist, firm and
                            firm_resolution, before and after, all unchanged; the news channel keeps no artifacts

BASE is the catalog at git ref BASE_REF (the cut's base), read with `git show`. NEW is the working-tree catalog, or C16_NEW (a planted copy).
Exit 0 PASS, 1 FAIL, 9 no run.
"""
import os
import subprocess
import sys
import tempfile

import yaml

BASE_REF = "0f40810fa2"
GW = "infra/aws/ec2/opal-gateway"
CATALOG = GW + "/app/refs/DATA_CATALOG.yaml"
NEW = os.environ.get("C16_NEW") or CATALOG
MDPF_FILES = ("aum-metrics", "account-distribution", "aggregate-aua-timeseries", "category-views")

sys.path.insert(0, os.path.join(os.getcwd(), GW))
from app.graphql_plumbing import catalog_gate as cg  # noqa: E402


def base_path(tmp):
    r = subprocess.run(["git", "show", "%s:%s" % (BASE_REF, CATALOG)], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        print("ERROR: git show %s:%s failed (rc %d)" % (BASE_REF, CATALOG, r.returncode))
        sys.exit(9)
    p = os.path.join(tmp, "base_catalog.yaml")
    with open(p, "wb") as fh:
        fh.write(r.stdout)
    return p


def rows_of(cat, channel=None):
    out = []
    for name, ch in (cat.get("channels") or {}).items():
        if channel and name != channel:
            continue
        for row in ch.get("artifacts") or []:
            out.append((name, row))
    return out


def ac1():
    with open(NEW, encoding="ascii") as fh:
        cat = yaml.safe_load(fh)
    tmp = tempfile.mkdtemp(prefix="c16_")
    with open(base_path(tmp), encoding="ascii") as fh:
        base = yaml.safe_load(fh)
    res = []
    aum = [r for _c, r in rows_of(cat) if r.get("key") == "json/portfolios/aum-metrics.json"]
    res.append(("(a) the json/portfolios/aum-metrics.json row is deny + ruled", len(aum) == 1 and aum[0].get("verdict_class") == "deny"
                and aum[0].get("verdict_state") == "ruled"))
    legacy = [r for _c, r in rows_of(cat) if str(r.get("key", "")).startswith("json/mdpf/")]
    n_new, n_old = len(rows_of(cat, "mdpf_model_portfolios")), len(rows_of(base, "mdpf_model_portfolios"))
    res.append(("(b) no json/mdpf/ artifact row; the mdpf channel lost exactly that one row (%d -> %d)" % (n_old, n_new),
                not legacy and n_new == n_old - 1))
    news = (cat.get("channels") or {}).get("news") or {}
    articles = str((news.get("tables") or {}).get("articles", ""))
    hazards = " || ".join(str(h) for h in (news.get("hazards") or []))
    res.append(("(c) news.tables.articles carries 381,261 and not 298K", "381,261" in articles and "298K" not in articles))
    res.append(("(c) a news hazard marks opal-harvest-articles EMPTY", any("opal-harvest-articles" in h and "EMPTY" in h for h in hazards.split(" || "))))
    res.append(("(c) a news hazard marks the Seeking Alpha output frozen since 2026-04-13",
                any("frozen" in h and "2026-04-13" in h for h in hazards.split(" || "))))
    return report(res)


def ac2():
    tmp = tempfile.mkdtemp(prefix="c16_")
    old = cg.load_catalog(base_path(tmp))
    new = cg.load_catalog(NEW)
    keys = set(old["rows_by_key"]) | set(new["rows_by_key"])
    for scope in cg.KNOWN_FIRMS + ("global",):
        for f in MDPF_FILES:
            keys.add("json/mdpf/%s/%s.json" % (scope, f))
    principals = [(cg.OPAL_INTERNAL, "")] + [("firm", f) for f in cg.KNOWN_FIRMS] + [("firm", "nosuchfirm"), ("firm", "")]
    d2s = s2d = same = 0
    first = []
    for key in sorted(keys):
        for cls, firm in principals:
            o, n = cg.gate(old, key, cls, firm).allowed, cg.gate(new, key, cls, firm).allowed
            if (not o) and n:
                d2s += 1
                if len(first) < 5:
                    first.append((key, cls, firm))
            elif o and not n:
                s2d += 1
            else:
                same += 1
    pairs = len(keys) * len(principals)
    print("DENOMINATOR keys=%d principals=%d pairs=%d (base catalog keys %d, new catalog keys %d, plus %d scope-substituted json/mdpf keys)"
          % (len(keys), len(principals), pairs, len(old["rows_by_key"]), len(new["rows_by_key"]), len(cg.KNOWN_FIRMS + ("global",)) * len(MDPF_FILES)))
    print("deny->serve=%d serve->deny=%d unchanged=%d" % (d2s, s2d, same))
    for k in first:
        print("  WIDENED: %s principal=%s firm=%r" % k)
    return report([("deny->serve is 0 over a non-empty denominator", pairs > 0 and d2s == 0 and d2s + s2d + same == pairs)])


def ac3():
    tmp = tempfile.mkdtemp(prefix="c16_")
    with open(base_path(tmp), encoding="ascii") as fh:
        base = yaml.safe_load(fh)
    with open(NEW, encoding="ascii") as fh:
        new = yaml.safe_load(fh)
    fields = ("verdict_class", "allowlist", "firm", "firm_resolution")
    res = []

    def view(cat):
        out = {}
        for ch in ("news", "sentiment_news_mood"):
            body = (cat.get("channels") or {}).get(ch) or {}
            out[ch + " (channel fields)"] = tuple(body.get(f) for f in fields)
            for row in body.get("artifacts") or []:
                out["%s %s" % (ch, row.get("key"))] = tuple(row.get(f) for f in fields)
        return out
    b, n = view(base), view(new)
    for k in sorted(set(b) | set(n)):
        same = b.get(k) == n.get(k) and k in b and k in n
        print("%s | before %s | after %s | %s" % (k, b.get(k), n.get(k), "unchanged" if same else "CHANGED"))
        res.append((k, same))
    res.append(("the news channel keeps no artifacts rows", not ((new.get("channels") or {}).get("news") or {}).get("artifacts")))
    return report([("every gate field on %d news / sentiment_news_mood entries unchanged and the news channel keeps no artifacts" % (len(res) - 1),
                    all(ok for _n, ok in res))])


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2", "ac3"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2, "ac3": ac3}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
