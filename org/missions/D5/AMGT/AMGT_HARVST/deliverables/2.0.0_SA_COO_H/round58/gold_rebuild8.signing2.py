"""HARVST served gold rebuild #8 -- signing dry run 2, after the list repair HVST-be-1 (issuer, NO WRITE).

Rules of 1.0.0_SA_CTO~Z msg 31008 that this run prints against:
- rule 2: pairs gained per NEW exact-case ticker form (a form the served file does not carry for that security);
- rule 3: 0 served pairs lost, AND every gained pair assigned to exactly ONE cause -- a new security, silver growth, or a new
  alias -- summing to the total.

Three mention builds over the CURRENT silver, each through the capturing client (PUTS SENT 0):
  B = the SERVED list (`round33/securities.universe.r33.json`): what a rebuild with no list change would serve;
  P = the PROPOSED list (`universe_securities.build()` as merged);
  T = the proposed list with every NEW ticker form removed.
A gained pair (in P, not in the served snapshot) is `new security` when its security is not in the served list; else
`silver growth` when it is also in B; else `new alias`. A pair `rests on a new ticker form` when it is in P and not in T.
Daily is built once, from P. It also draws the grader's sample: 30 pairs, 3 from each of the 10 largest gainers by
(new security + new alias), `random.Random(58)`, rows sorted before sampling.

Writes `gold_rebuild8.signing2.json` and `GOLD_REBUILD8_GAIN_SAMPLE.json` / `.md` beside itself. It states the bar and prints
BAR HOLDS or BAR BROKEN; it writes nothing to S3 either way.
"""
import collections
import datetime
import importlib.util
import io
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
R32C = os.path.join(PARENT, "round32", "checks")
sys.path.insert(0, R32C)
import ae1_common as c  # noqa: E402,F401  (puts the repo root on sys.path, as the round-32 dry run does)

_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(R32C, "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.harvest import universe_securities as us  # noqa: E402

R33 = os.path.join(PARENT, "round33", "securities.universe.r33.json")
OUT = os.path.join(HERE, "gold_rebuild8.signing2.json")


def mk(row):
    return (row.get("article_key"), row.get("security_key"))


def build_mention_rows(securities, as_of, real):
    client = sg.CapturingClient(real)
    pg.build_mention(securities, as_of, client=client)
    (key, body), = client.puts.items()
    return pq.read_table(io.BytesIO(body)).to_pylist(), client.sent, key


def main():
    served_list = json.load(open(R33, encoding="utf-8"))
    proposed, summary = us.build()
    json.dump(proposed, open(os.path.join(HERE, "securities.universe.signing2.json"), "w", encoding="utf-8"), indent=1)
    old = {s["security_key"]: s for s in served_list}
    new = {s["security_key"]: s for s in proposed}
    new_forms = {}
    for key, sec in new.items():
        fresh = [f for f in (sec.get("ticker_aliases") or []) if f not in ((old.get(key) or {}).get("ticker_aliases") or [])]
        if fresh:
            new_forms[key] = fresh
    without_new_forms = []
    for sec in proposed:
        copy = dict(sec)
        copy["ticker_aliases"] = [f for f in (sec.get("ticker_aliases") or []) if f not in new_forms.get(sec["security_key"], [])]
        without_new_forms.append(copy)
    print("LIST: served %d, proposed %d (source %s); new %d, absent %d; NEW exact-case ticker forms on %d securities"
          % (len(old), len(new), (summary.get("universe") or {}).get("source"), len(set(new) - set(old)),
             len(set(old) - set(new)), len(new_forms)))
    sys.stdout.flush()

    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    real = store._default_client()
    served_m = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    served_d = pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE)
    rows_b, sent_b, _key_b = build_mention_rows(served_list, as_of, real)
    print("BUILD B (served list, current silver): %d rows" % len(rows_b))
    sys.stdout.flush()
    rows_t, sent_t, _key_t = build_mention_rows(without_new_forms, as_of, real)
    print("BUILD T (proposed list, new ticker forms removed): %d rows" % len(rows_t))
    sys.stdout.flush()
    rows_p, sent_p, key_p = build_mention_rows(proposed, as_of, real)
    print("BUILD P (proposed list): %d rows" % len(rows_p))
    sys.stdout.flush()

    orig = pg._latest_gold_snapshot_rows
    pg._latest_gold_snapshot_rows = lambda table, client=None: rows_p if table == pg.GOLD_TABLE else orig(table, client=client)
    cd = sg.CapturingClient(real)
    pg.build_daily(proposed, as_of, client=cd)
    (dkey, dbody), = cd.puts.items()
    daily = pq.read_table(io.BytesIO(dbody)).to_pylist()
    pg._latest_gold_snapshot_rows = orig

    s_keys = {mk(r) for r in served_m}
    b_keys = {mk(r) for r in rows_b}
    t_keys = {mk(r) for r in rows_t}
    p_rows = {mk(r): r for r in rows_p}
    p_keys = set(p_rows)

    lost = sorted(s_keys - p_keys)
    lost_by_sec = collections.Counter(k[1] for k in lost)
    lost_also_in_b = [k for k in lost if k not in b_keys]
    print("MENTION: served %d -> built %d; LOST %d over %d securities (of them %d are also gone under the SERVED list on"
          " current silver, so not the list's doing)" % (len(s_keys), len(p_keys), len(lost), len(lost_by_sec), len(lost_also_in_b)))
    for key, n in lost_by_sec.most_common():
        print("  LOST %s: %d; aliases served %s -> proposed %s" % (
            key, n, json.dumps((old.get(key) or {}).get("aliases")), json.dumps((new.get(key) or {}).get("aliases"))))

    gained = sorted(p_keys - s_keys)
    cause = {}
    for k in gained:
        if k[1] not in old:
            cause[k] = "new security"
        elif k in b_keys:
            cause[k] = "silver growth"
        else:
            cause[k] = "new alias"
    totals = collections.Counter(cause.values())
    print("MENTION GAINED: %d = new security %d + silver growth %d + new alias %d (sum %d)" % (
        len(gained), totals["new security"], totals["silver growth"], totals["new alias"], sum(totals.values())))
    by_sec = collections.defaultdict(collections.Counter)
    for k, why in cause.items():
        by_sec[k[1]][why] += 1
    list_gain = {key: cnt["new security"] + cnt["new alias"] for key, cnt in by_sec.items()}
    for key, n in sorted(list_gain.items(), key=lambda kv: -kv[1]):
        if n:
            cnt = by_sec[key]
            print("  GAINED %s [%s]: new security %d, new alias %d, silver growth %d; aliases %s exact %s" % (
                key, (new[key].get("company") or ""), cnt["new security"], cnt["new alias"], cnt["silver growth"],
                json.dumps(new[key].get("aliases")), json.dumps(new[key].get("ticker_aliases"))))

    on_form = [k for k in gained if k not in t_keys]
    form_by_sec = collections.Counter(k[1] for k in on_form)
    print("NEW TICKER FORMS: %d securities carry one; %d gained pairs rest on one, over %d securities" % (
        len(new_forms), len(on_form), len(form_by_sec)))
    for key in sorted(new_forms, key=lambda x: -form_by_sec.get(x, 0)):
        print("  FORM %s %s [%s]: pairs resting on the form %d of %d gained" % (
            key, json.dumps(new_forms[key]), new[key].get("company"), form_by_sec.get(key, 0),
            sum(by_sec[key].values()) if key in by_sec else 0))

    def dk(row):
        return (row.get("security_key"), str(row.get("day"))[:10])

    od = {dk(r): r for r in served_d}
    nd = {dk(r): r for r in daily}
    d_gone = [k for k in od if k not in nd]
    print("DAILY: served %d -> built %d; gone %d, added %d" % (len(od), len(nd), len(d_gone), len([k for k in nd if k not in od])))

    top = [key for key, n in sorted(list_gain.items(), key=lambda kv: -kv[1]) if n][:10]
    sample = []
    rng = random.Random(58)
    for key in top:
        rows = sorted(k for k in gained if k[1] == key and cause[k] != "silver growth")
        for k in rng.sample(rows, min(3, len(rows))):
            r = p_rows[k]
            sample.append({"n": len(sample) + 1, "security_key": key, "company": new[key].get("company"),
                           "cause": cause[k], "rests_on_new_ticker_form": k not in t_keys, "article_key": k[0],
                           "publisher": r.get("publisher"), "title": r.get("title"), "url": r.get("url"),
                           "match_forms": r.get("match_forms"), "mention_count": r.get("mention_count"),
                           "mention_in_title": r.get("mention_in_title"), "verdict": None})
    json.dump({"about": "30 gained pairs, 3 from each of the 10 largest gainers by (new security + new alias); the question per"
                        " row: is this article's mention a mention of that company. JUDGMENT, graded by 3.0.0_SA_CVO~Z;"
                        " bar 29 of 30 (1.0.0_SA_CTO~Z msg 31008).", "seed": 58, "top": top, "sample": sample},
              open(os.path.join(HERE, "GOLD_REBUILD8_GAIN_SAMPLE.json"), "w", encoding="utf-8"), indent=1, default=str)
    lines = ["# Gold rebuild #8 -- the gain sample for `3.0.0_SA_CVO~Z` (bar 29 of 30)", "",
             "| n | security | cause | on a new ticker form | publisher | title | matched forms | names the company? |",
             "|---|---|---|---|---|---|---|---|"]
    for s in sample:
        lines.append("| %d | %s (%s) | %s | %s | %s | %s | %s | |" % (
            s["n"], s["security_key"], s["company"], s["cause"], "yes" if s["rests_on_new_ticker_form"] else "no",
            s["publisher"], str(s["title"]).replace("|", "/"), json.dumps(s["match_forms"])))
    io.open(os.path.join(HERE, "GOLD_REBUILD8_GAIN_SAMPLE.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("SAMPLE: %d pairs over %d securities" % (len(sample), len(top)))

    puts = sent_b + sent_t + sent_p + cd.sent
    out = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "as_of": str(as_of),
           "mention": {"served": len(s_keys), "built": len(p_keys), "lost": len(lost), "lost_by_security": dict(lost_by_sec),
                       "lost_keys": [list(k) for k in lost], "lost_not_the_lists_doing": len(lost_also_in_b),
                       "gained": len(gained), "gained_by_cause": dict(totals),
                       "gained_by_security": {k: dict(v) for k, v in by_sec.items()}, "key": key_p},
           "new_ticker_forms": new_forms, "pairs_on_new_ticker_form": dict(form_by_sec),
           "daily": {"served": len(od), "built": len(nd), "gone": len(d_gone), "key": dkey}, "puts_sent": puts}
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    holds = (len(lost) == 0 and sum(totals.values()) == len(gained) and not d_gone and puts == 0)
    print("BAR (0 pairs lost; every gained pair has one cause; daily gone 0; PUTS 0): %s" % ("HOLDS" if holds else "BROKEN"))
    print("PUTS SENT: %d" % puts)
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
