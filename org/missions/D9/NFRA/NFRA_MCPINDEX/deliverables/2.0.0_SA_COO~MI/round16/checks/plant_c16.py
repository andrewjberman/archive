"""plant_c16.py -- the ISSUER's cut-time planted arms for c16.AC1-AC3 (standing battery clause 1). NOT given to the worker, NOT a criterion.

Builds a GOOD catalog from the base (the three corrections applied by hand to the loaded data) and four BAD ones, writes each to a temp file and runs
c16_check.py with C16_NEW set, comparing every exit code with the wanted one. Run from the repo root.
"""
import copy
import os
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16_check as cc  # noqa: E402


def dump(cat, name, tmp):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="ascii", newline="\n") as fh:
        yaml.safe_dump(cat, fh, sort_keys=False, allow_unicode=False)
    return p


def find(cat, key):
    for ch in cat["channels"].values():
        for r in ch.get("artifacts") or []:
            if r.get("key") == key:
                return r
    raise SystemExit("planted source row %s absent from the base" % key)


def main():
    tmp = tempfile.mkdtemp(prefix="plant16_")
    with open(cc.base_path(tmp), encoding="ascii") as fh:
        base = yaml.safe_load(fh)

    good = copy.deepcopy(base)
    r = find(good, "json/portfolios/aum-metrics.json")
    r["verdict_class"], r["verdict_state"] = "deny", "ruled"
    ch = good["channels"]["mdpf_model_portfolios"]
    ch["artifacts"] = [a for a in ch["artifacts"] if not str(a.get("key", "")).startswith("json/mdpf/")]
    news = good["channels"]["news"]
    news["tables"]["articles"] = "opal-news-articles -- QUERY by article_date ONLY (381,261 items; about 1,000 a weekday)"
    news["hazards"] = list(news.get("hazards") or []) + ["opal-harvest-articles EMPTY: 0 items -- do not serve",
                                                         "the Seeking Alpha output is frozen since 2026-04-13 -- serve only with that vintage"]

    widen_mdpf = copy.deepcopy(good)   # the dropped legacy row comes back SERVING: deny -> serve on its key
    back = copy.deepcopy(find(base, "json/mdpf/**"))
    back["verdict_class"] = "serve-with-caveat"
    widen_mdpf["channels"]["mdpf_model_portfolios"]["artifacts"].append(back)

    widen_other = copy.deepcopy(good)  # an unrelated deny row flipped to serve
    find(widen_other, "json/market/all_returns.json")["verdict_class"] = "serve"

    gate_field = copy.deepcopy(good)   # (c) must change no gate field: a sentiment row's firm changes
    find(gate_field, "json/sentiment/fear-greed-index.json + json/sentiment/keyword-sentiments.json")["firm"] = "49financial"

    news_rows = copy.deepcopy(good)    # the news channel gains an artifacts list
    news_rows["channels"]["news"]["artifacts"] = [{"key": "x", "verdict_class": "serve", "allowlist": "ALLOWLISTED", "firm": "opal-internal"}]

    arms = [("good catalog, ac1", "good", "ac1", 0), ("good catalog, ac2", "good", "ac2", 0), ("good catalog, ac3", "good", "ac3", 0),
            ("base catalog, ac1 (nothing corrected)", "base", "ac1", 1),
            ("legacy mdpf row back serving, ac2", "widen_mdpf", "ac2", 1), ("legacy mdpf row back serving, ac1", "widen_mdpf", "ac1", 1),
            ("an unrelated deny row served, ac2", "widen_other", "ac2", 1),
            ("a sentiment row's firm changed, ac3", "gate_field", "ac3", 1), ("the news channel gains artifacts, ac3", "news_rows", "ac3", 1)]
    cats = {"good": good, "base": base, "widen_mdpf": widen_mdpf, "widen_other": widen_other, "gate_field": gate_field, "news_rows": news_rows}
    paths = {k: dump(v, k + ".yaml", tmp) for k, v in cats.items()}
    ok = wrong = 0
    for label, cat, ac, want in arms:
        env = dict(os.environ, C16_NEW=paths[cat])
        r = subprocess.run([sys.executable, os.path.join(HERE, "c16_check.py"), ac], env=env, capture_output=True, text=True)
        if r.returncode == want:
            ok += 1
            print("ARM ok:    %s -> rc=%d" % (label, r.returncode))
        else:
            wrong += 1
            print("ARM WRONG: %s -> rc=%d want %d" % (label, r.returncode, want))
            print("\n".join(r.stdout.splitlines()[-6:]))
    print("PLANTED ARMS: ok %d, wrong %d" % (ok, wrong))
    return 0 if wrong == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
