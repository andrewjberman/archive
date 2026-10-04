"""HARVST round 42 HVST-ao-1 -- the serializing dry run the `chatter_window` never-widen pair signs (issuer, NO WRITE).

FWD-17: `window_tone.build_window` (the builder's own code) runs through the issuer's capturing client (PUTS SENT 0). Every
built row is then RECOMPUTED here, independently of `build_window_rows`, from the newest served mention snapshot and the
score store, using FWD-17's words: per security and window (30/90/365, ending at the last trading day before the as-of
date), the DISTINCT articles published in [window_start_served, window_end]; scored = those with a score; voters = scored
and not neutral; tone = mean signed score over the voters, null at 0 voters.

THE RULE (window build):
- before: `chatter_window` holds 0 parts (a first mint; nothing served is replaced);
- 3 rows per security of the mention snapshot that is in the universe, each window_days in {30, 90, 365};
- window_end == the last trading day before the as-of date, on every row;
- every row equals the independent recompute on articles_total, scored, voters and tone (MISMATCH 0; tone within 1e-12);
- tone is null exactly when voters == 0 (never 0.0 at 0 voters).
Reports the real rows with scored > 0 and voters 0 (all-neutral windows) beside the plant.

Writes `round42/gold_window_signing.json` (or GOLD_WINDOW_SIGNING_OUT). Prints `RULE (window build): HOLDS` only when all
of it holds.
"""
import datetime
import hashlib
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(HERE)
os.environ.setdefault("HVST_GOLD_UNIVERSE", os.path.join(DELIV, "round33", "securities.universe.r33.json"))
R32C = os.path.join(DELIV, "round32", "checks")
sys.path.insert(0, R32C)
import ae1_common as c  # noqa: E402,F401  (puts the repo root on sys.path)

_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(R32C, "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)

import pyarrow.parquet as pq  # noqa: E402

from lib import trading_calendar  # noqa: E402
from lib.research.harvest import finbert_sentiment as fs  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.harvest import window_tone as wt  # noqa: E402

OUT = os.environ.get("GOLD_WINDOW_SIGNING_OUT") or os.path.join(HERE, "gold_window_signing.json")


def window_parts(client):
    prefix = store.table_prefix("amgt", "gold", wt.TABLE)
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        keys += [o["Key"] for o in page.get("Contents", []) or [] if o["Key"].endswith(".parquet")]
    return sorted(keys)


def utc_day(v):
    if isinstance(v, datetime.datetime):
        return (v.astimezone(datetime.timezone.utc) if v.tzinfo else v).date()
    if isinstance(v, datetime.date):
        return v
    s = str(v)
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(datetime.timezone.utc).date() if "T" in s or " " in s else datetime.date.fromisoformat(s[:10])


def recompute(mention, scores, window_end):
    """FWD-17 from its words, without build_window_rows."""
    out = {}
    for sec in sorted({r["security_key"] for r in mention if r.get("security_key")}):
        days = {}
        keys = {}
        for r in mention:
            if r.get("security_key") != sec or r.get("published_utc") is None:
                continue
            ak = r.get("article_key")
            days[ak] = utc_day(r["published_utc"])
            if scores.get(r.get("sentiment_content_key")) is not None:
                keys[ak] = scores[r["sentiment_content_key"]]
            else:
                keys.setdefault(ak, None)
        for n in (30, 90, 365):
            start = max(window_end - datetime.timedelta(days=n - 1), wt.STORE_START)
            arts = [ak for ak, d in days.items() if start <= d <= window_end]
            scored = [keys[ak] for ak in arts if keys.get(ak) is not None]
            voters = [s for s in scored if s.get("label") != "neutral"]
            tone = sum(float(s["score"]) for s in voters) / len(voters) if voters else None
            out[(sec, n)] = {"articles_total": len(arts), "scored": len(scored), "voters": len(voters), "tone": tone}
    return out


def digest(rows):
    return hashlib.sha256(json.dumps(sorted(json.dumps(r, sort_keys=True, default=str) for r in rows)).encode()).hexdigest()


def main():
    universe = os.environ["HVST_GOLD_UNIVERSE"]
    securities = json.load(open(universe, encoding="utf-8"))
    wanted = {s["security_key"] for s in securities}
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    window_end = trading_calendar.prev_trading_day(as_of)
    real = store._default_client()
    parts_before = window_parts(real)
    mention = [r for r in pg._latest_gold_snapshot_rows(pg.GOLD_TABLE) if r.get("security_key") in wanted]
    scores = fs.latest_scores(real)
    cw = sg.CapturingClient(real)
    wt.build_window(securities, as_of, client=cw, sentiment_by_key=scores)
    (wkey, wbody), = cw.puts.items()
    rows = pq.read_table(io.BytesIO(wbody)).to_pylist()
    expect = recompute(mention, scores, window_end)

    mismatch = []
    for r in rows:
        e = expect.get((r["security_key"], r["window_days"]))
        same = e is not None and all(r[k] == e[k] for k in ("articles_total", "scored", "voters")) and (
            (r["tone"] is None and e["tone"] is None)
            or (r["tone"] is not None and e["tone"] is not None and abs(r["tone"] - e["tone"]) < 1e-12))
        if not same:
            mismatch.append({"row": {k: r[k] for k in ("security_key", "window_days", "articles_total", "scored", "voters", "tone")},
                             "expect": e})
    end_bad = sum(1 for r in rows if str(r["window_end"]) != str(window_end))
    null_bad = sum(1 for r in rows if (r["tone"] is None) != (r["voters"] == 0))
    per_sec = {}
    for r in rows:
        per_sec.setdefault(r["security_key"], set()).add(r["window_days"])
    shape_bad = sum(1 for v in per_sec.values() if v != {30, 90, 365}) + (len(per_sec) != len(expect) // 3)
    all_neutral = [[r["security_key"], r["window_days"], r["scored"]] for r in rows if r["scored"] > 0 and r["voters"] == 0]
    out = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "as_of": str(as_of),
           "window_end": str(window_end), "universe_file": universe, "parts_before": parts_before,
           "mention_rows_read": len(mention), "scores_read": len(scores), "rows": len(rows), "securities": len(per_sec),
           "mismatch": len(mismatch), "mismatch_sample": mismatch[:10], "window_end_wrong": end_bad,
           "tone_null_not_iff_zero_voters": null_bad, "shape_bad": shape_bad,
           "rows_with_tone": sum(1 for r in rows if r["tone"] is not None),
           "all_neutral_windows": len(all_neutral), "all_neutral_sample": all_neutral[:10],
           "key": wkey, "bytes": len(wbody), "built_digest": digest(rows), "puts_sent": cw.sent}
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    print("PARTS BEFORE: %d" % len(parts_before))
    print("MENTION ROWS READ: %d; SCORES READ: %d; WINDOW END: %s" % (len(mention), len(scores), window_end))
    print("BUILT: %d rows on %d securities; with tone %d; all-neutral windows (scored > 0, voters 0) %d"
          % (len(rows), len(per_sec), out["rows_with_tone"], len(all_neutral)))
    print("CHECKS: mismatch vs independent recompute %d; window_end wrong %d; tone-null not iff 0 voters %d; shape bad %d"
          % (len(mismatch), end_bad, null_bad, shape_bad))
    holds = (not parts_before and rows and not mismatch and not end_bad and not null_bad and not shape_bad
             and out["puts_sent"] == 0)
    print("RULE (window build): %s" % ("HOLDS" if holds else "BROKEN"))
    print("PUTS SENT: %d" % out["puts_sent"])
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
