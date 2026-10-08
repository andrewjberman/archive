"""bh-1 (round 61): the (article, security) pairs that rest on the bare-name fallback alone.

READ-ONLY. Reads the r60 list file and every latest silver article through the served iterator
(S3 GET, no put). Uses pg._security_mentions as it stands; does not re-implement the matcher.
Run from the repo root of the worktree:  PYTHONPATH=. python -u <this file>
"""
import copy
import json
import os
import random
import sys

from lib.research.harvest import publication_gold as pg

HERE = os.path.dirname(os.path.abspath(__file__))
LIST_FILE = os.path.join(
    HERE, "..", "2.0.0_SA_COO_H", "round60", "securities.universe.r60.json")
CONTEXT = 120
SAMPLE_N = 30
SEED = 61


def _spans(text, company, field):
    """Every span of the company string (case-insensitive, word-bounded, as the matcher's own
    pattern builds it) in one text, with 120 chars of context each side."""
    out = []
    pattern = pg._span_pattern([company])
    if pattern is None or not text:
        return out
    for m in pattern.finditer(text):
        out.append({
            "where": field,
            "text": m.group(0),
            "case": "stored case" if m.group(0) == company else "other case",
            "context": text[max(0, m.start() - CONTEXT):m.end() + CONTEXT],
        })
    return out


def main():
    with open(LIST_FILE, encoding="utf-8") as fh:
        securities = json.load(fh)
    empties = [s for s in securities if not s.get("aliases")]
    stripped = []
    for s in empties:
        t = copy.deepcopy(s)
        t["company"] = ""
        t["aliases"] = []
        stripped.append(t)

    stats = {s["security_key"]: {"served": 0, "fallback": 0, "nocase": 0} for s in empties}
    progress = []
    pairs = []  # fallback-only pairs, with spans taken at scan time
    n = 0
    for row in pg._iter_latest_articles():
        n += 1
        if n % 500 == 0:
            progress.append("progress: %d articles read" % n)
            print(progress[-1], flush=True)
        for s, t in zip(empties, stripped):
            with_fb = pg._security_mentions(row, s)
            if with_fb["mention_count"] < 1:
                continue
            st = stats[s["security_key"]]
            st["served"] += 1
            if pg._security_mentions(row, t)["mention_count"] >= 1:
                continue
            st["fallback"] += 1
            spans = _spans(row.get("title") or "", s["company"], "title")
            for i, block in enumerate(row.get("text_blocks") or []):
                spans += _spans(block, s["company"], "block %d" % i)
            if not any(sp["case"] == "stored case" for sp in spans):
                st["nocase"] += 1
            pairs.append({
                "security_key": s["security_key"],
                "company": s["company"],
                "article_key": row.get("article_key"),
                "publisher": row.get("publisher"),
                "title": row.get("title"),
                "url": pg.article_url(row),
                "spans": spans,
            })

    lines = list(progress)
    lines.append("DENOMINATOR: securities %d, with an empty alias list %d, silver articles %d"
                 % (len(securities), len(empties), n))
    printed = 0
    for s in empties:
        st = stats[s["security_key"]]
        lines.append("%s company=%s ticker_aliases=%s: pairs served %d, resting on the fallback alone %d, "
                     "of those with no span in the stored case %d"
                     % (s["security_key"], s["company"], s.get("ticker_aliases") or [],
                        st["served"], st["fallback"], st["nocase"]))
        printed += 1
    F = len(pairs)
    lines.append("FALLBACK-ONLY PAIRS: %d over %d securities" % (F, len(empties)))

    pairs.sort(key=lambda p: (p["security_key"], p["article_key"]))
    sample = pairs if F < SAMPLE_N else random.Random(SEED).sample(pairs, SAMPLE_N)
    lines.append("SAMPLE: %d of %d, seed %d" % (len(sample), F, SEED))
    rows = []
    for i, p in enumerate(sample, 1):
        r = {"row": i}
        r.update(p)
        rows.append(r)

    with open(os.path.join(HERE, "BH1_FALLBACK_SAMPLE.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rows, fh, indent=1, ensure_ascii=True)
        fh.write("\n")

    md = []
    md.append("# BH1 fallback-only sample (round 61, HVST-bh-1)\n")
    md.append(
        "The population is every (article, security) pair served by the r60 list file whose security has an "
        "empty `aliases` list, so it is matched on its `company` string, and that counts at least one mention "
        "as the security stands but none once the fallback is taken away (company set to the empty string, "
        "aliases still empty, ticker_aliases unchanged). A pair was chosen by `pg._security_mentions` run both "
        "ways over every latest silver article; the fallback-only pairs were sorted by (security_key, "
        "article_key) and sampled with `random.Random(61)` (all of them when fewer than 30). Counts: %d "
        "fallback-only pairs over %d empty-alias securities, %d silver articles read, %d pairs in this sample. "
        "The question per row is: is this article about this security. This file carries no verdict and no "
        "grade; a reviewer grades it.\n" % (F, len(empties), n, len(sample)))
    for r in rows:
        md.append("## Row %d -- %s -- %s\n" % (r["row"], r["security_key"], r["article_key"]))
        md.append("- company: %s" % r["company"])
        md.append("- publisher: %s" % r["publisher"])
        md.append("- title: %s" % r["title"])
        md.append("- url: %s" % r["url"])
        md.append("- spans of the company string: %d\n" % len(r["spans"]))
        for sp in r["spans"]:
            md.append("  - [%s] `%s` (%s): ...%s..." % (
                sp["where"], sp["text"], sp["case"], sp["context"].replace("\n", " ").replace("\r", " ")))
        md.append("")
    with open(os.path.join(HERE, "BH1_FALLBACK_SAMPLE.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(md) + "\n")

    fail = []
    if n <= 0:
        fail.append("N == 0")
    if not empties:
        fail.append("E == 0")
    if printed != len(empties):
        fail.append("not every empty-alias security printed its line")
    if len(sample) != min(SAMPLE_N, F):
        fail.append("sample size %d != min(30, F)=%d" % (len(sample), min(SAMPLE_N, F)))
    if any(not r["spans"] for r in rows):
        fail.append("a sample row has no span")
    lines.append("CENSUS OK" if not fail else "CENSUS FAIL: " + "; ".join(fail))

    out = "\n".join(lines) + "\n"
    with open(os.path.join(HERE, "bh1_fallback_census.out"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    sys.stdout.write(out)
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
