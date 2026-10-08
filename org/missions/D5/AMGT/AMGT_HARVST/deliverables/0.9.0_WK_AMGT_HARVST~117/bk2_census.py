"""HVST-bk-2 (round 66): what the capitalised-headline rule removes. In a title capitalised throughout, an exact-case form
alone does not pair; it needs a second anchor.

READ-ONLY (S3 GET through the served iterator, no put, no gold build). Reads the r64 list file and every latest silver article.

AFTER  = `pg._security_mentions` as it stands in this worktree (the rule on).
BEFORE = the same function with the rule switched off: `pg._CAPITALISED_HEADLINE_RULE = False` for the one call. With the
         switch False the code path is the pre-bk-2 path (`title_exact` is `exact`, so every title count is the old one).
Where the rule can act: only when `pg._capitalised_throughout(title)` is true (the rule's first condition). For an article
whose title is not capitalised throughout, BEFORE == AFTER by the code, so BEFORE is computed only for capitalised titles
and AFTER for every pair; a pair's BEFORE count elsewhere equals its AFTER count. PAIRS ADDED is measured on the
capitalised titles (the only place a difference can arise).

STRICT is reported beside R: the removed pairs whose title is capitalised throughout with NO minor-word allowance (every
alphabetic word begins upper-case), the reading of the order's text taken literally (row AMGT_HARVST-Z-W117-S1).

Run from the repo root of the worktree:  PYTHONPATH=. python -u <this file>
"""
import json
import os
import re
import sys

from lib.research.harvest import publication_gold as pg

HERE = os.path.dirname(os.path.abspath(__file__))
LIST_FILE = os.path.join(HERE, "..", "2.0.0_SA_COO_H", "round64", "securities.universe.r64.json")
REPORTED_TITLE = "Bond Traders Bet on Fed Delivering 25 BP Rate Increase"
REPORTED_DATE = "2026-09-16"
REPORTED_SECURITY = "BP_US_Equity"


def _asc(t):
    return str(t).encode("ascii", "backslashreplace").decode("ascii")


def _strict_capitalised(title):
    """Every alphabetic word begins upper-case, no minor-word allowance, at least three alphabetic words."""
    words = 0
    for token in (title or "").split():
        letter = re.search(r"[^\W\d_]", token)
        if letter is None:
            continue
        words += 1
        if not letter.group(0).isupper():
            return False
    return words >= 3


def _before(row, security):
    pg._CAPITALISED_HEADLINE_RULE = False
    try:
        return pg._security_mentions(row, security)
    finally:
        pg._CAPITALISED_HEADLINE_RULE = True


def _published(row):
    value = row.get("published_utc")
    return (value.isoformat() if hasattr(value, "isoformat") else str(value))[:10] if value is not None else None


def main():
    assert pg._CAPITALISED_HEADLINE_RULE is True, "the rule is off at start"
    with open(LIST_FILE, encoding="utf-8") as fh:
        securities = json.load(fh)
    S = len(securities)
    stats = {s["security_key"]: {"before": 0, "after": 0, "removed": 0, "strict": 0} for s in securities}
    removed = []
    lower_kept = 0
    added = 0
    n = 0
    t = 0
    reported = []
    for row in pg._iter_latest_articles():
        n += 1
        if n % 500 == 0:
            print("progress: %d articles read" % n, flush=True)
        title = row.get("title") or ""
        capped = pg._capitalised_throughout(title)
        if capped:
            t += 1
        if title == REPORTED_TITLE and row.get("publisher") == "bbg" and _published(row) == REPORTED_DATE:
            reported.append(row.get("article_key"))
        for s in securities:
            key = s["security_key"]
            after_out = pg._security_mentions(row, s)
            after = after_out["mention_count"]
            st = stats[key]
            if not capped:
                if after >= 1:
                    st["before"] += 1
                    st["after"] += 1
                continue
            before_out = _before(row, s)
            before = before_out["mention_count"]
            st["before"] += 1 if before >= 1 else 0
            st["after"] += 1 if after >= 1 else 0
            if after >= 1 and before < 1:
                added += 1
            if before >= 1 and after >= 1 and after < before:
                lower_kept += 1
            if before >= 1 and after < 1:
                st["removed"] += 1
                strict = _strict_capitalised(title)
                st["strict"] += 1 if strict else 0
                published = row.get("published_utc")
                removed.append({
                    "security_key": key, "company": s["company"], "article_key": row.get("article_key"),
                    "publisher": row.get("publisher"),
                    "published": published.isoformat() if hasattr(published, "isoformat") else published,
                    "title": title, "matched_forms": before_out["match_forms"],
                    "strict_capitalised": strict})

    removed.sort(key=lambda p: (p["security_key"], p["article_key"] or ""))
    r = len(removed)
    per = sorted(((k, v) for k, v in stats.items() if v["removed"] > 0), key=lambda kv: (-kv[1]["removed"], kv[0]))
    gone = {(p["security_key"], p["article_key"]) for p in removed}

    lines = []
    lines.append("DENOMINATOR: securities %d, silver articles %d, titles capitalised throughout %d" % (S, n, t))
    lines.append("PAIRS REMOVED: %d over %d securities" % (r, len(per)))
    for k, v in per:
        lines.append("%s: pairs before %d after %d removed %d" % (k, v["before"], v["after"], v["removed"]))
    lines.append("PAIRS REMOVED UNDER THE STRICT READING (no minor-word allowance): %d over %d securities"
                 % (sum(v["strict"] for _k, v in per), sum(1 for _k, v in per if v["strict"] > 0)))
    lines.append("PAIRS WITH A LOWER COUNT BUT KEPT: %d" % lower_kept)
    state = []
    for ak in reported:
        state.append("%s %s %s" % (ak, REPORTED_SECURITY, "removed" if (REPORTED_SECURITY, ak) in gone else "still present"))
    if not reported:
        state.append("(no bbg article titled %r published %s in silver) %s still present" % (
            REPORTED_TITLE, REPORTED_DATE, REPORTED_SECURITY))
    lines.append("THE REPORTED PAIR: " + "; ".join(state))
    lines.append("PAIRS ADDED: %d" % added)

    fail = []
    if n <= 0:
        fail.append("N == 0")
    if t <= 0:
        fail.append("T == 0")
    if not reported or any((REPORTED_SECURITY, ak) not in gone for ak in reported):
        fail.append("the reported pair does not read removed")
    if added != 0:
        fail.append("PAIRS ADDED is %d" % added)
    lines.append("CENSUS OK" if not fail else "CENSUS FAIL: " + "; ".join(fail))

    with open(os.path.join(HERE, "BK2_REMOVED_PAIRS.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(removed, fh, indent=1, ensure_ascii=True, default=str)
        fh.write("\n")
    md = ["# BK2 removed pairs (%d) -- for a reviewer; no verdict by the worker" % r, "",
          "| security_key | company | article_key | publisher | published | title | form that matched | strict |",
          "|---|---|---|---|---|---|---|---|"]
    for p in removed:
        md.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            p["security_key"], _asc(p["company"]).replace("|", "/"), p["article_key"], p["publisher"],
            str(p["published"])[:10], _asc(p["title"]).replace("|", "/"),
            ", ".join(_asc(f) for f in p["matched_forms"]), "yes" if p["strict_capitalised"] else "no"))
    with open(os.path.join(HERE, "BK2_REMOVED_PAIRS.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(md) + "\n")

    out = "\n".join(lines) + "\n"
    with open(os.path.join(HERE, "bk2_census.out"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    sys.stdout.write(out)
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
