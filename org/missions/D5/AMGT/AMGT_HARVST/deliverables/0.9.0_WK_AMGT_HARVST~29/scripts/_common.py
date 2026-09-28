"""HVST-y-2 shared read helpers -- imported by ac1/ac2/ac3 (same-directory import, since each
script is invoked as `python .../<script>.py` and Python prepends the script's own directory to
sys.path). READS ONLY: no S3 write, no S3 delete, no vendor call anywhere in this module.

The four `assign_tier` inputs (mention_in_title, mention_in_lead, mention_count, share) are
recomputed straight from the STORED silver article text (title + text_blocks) by calling
`publication_gold._security_mentions`, which reads only `article_row.get("title")` and
`article_row.get("text_blocks")` plus the security's alias list -- never the gold row's own
stored `mention_in_title`/`mention_in_lead`/`mention_count` booleans/count. That is the trap
BOUNDS clause 2 of the task order names, and this module never reads those three gold-row fields
for the purpose of computing a derived tier.

The alias set per `security_key` comes from a LIVE read of the current universe
(`universe_securities.build()`) -- the same pool-universe-derived alias source
`publication_gold`'s own 2b scope item wires the gold builders to -- never from the stale
hand-written 6-security file under deliverables/~4/securities.json, which does not cover 49 of
the 55 security_keys the newest snapshot actually carries (measured this cut).
"""

import os
import sys


def _ensure_repo_root_on_path():
    """Walks up from this file's own directory to the first ancestor carrying BOTH `lib/` and
    `.tools/` (the repo root's own markers, never a fixed `../../..` count -- the task order's
    literal invocation is `python <this file>` with no `cd` and no PYTHONPATH, and this file
    lives 6 directories under the repo root)."""
    here = os.path.abspath(os.path.dirname(__file__))
    path = here
    for _ in range(15):
        if os.path.isdir(os.path.join(path, "lib")) and os.path.isdir(os.path.join(path, ".tools")):
            if path not in sys.path:
                sys.path.insert(0, path)
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    raise RuntimeError(
        "_ensure_repo_root_on_path: no ancestor of %r carries both lib/ and .tools/" % (here,)
    )


_ensure_repo_root_on_path()

import lib.research.harvest.publication_gold as pg  # noqa: E402
import lib.research.harvest.universe_securities as us  # noqa: E402


def load_context():
    """(gold_rows, articles_by_key, securities_by_key, universe_summary) -- three live S3 reads
    (Opal-owned, permitted) and one pure alias derivation. No write anywhere."""
    gold_rows = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    articles_by_key = {row.get("article_key"): row for row in pg._iter_latest_articles()}
    securities_list, universe_summary = us.build()
    securities_by_key = {s["security_key"]: s for s in securities_list}
    return gold_rows, articles_by_key, securities_by_key, universe_summary


def rederive_row(gold_row, articles_by_key, securities_by_key):
    """(status, detail). status is one of AGREE / DISAGREE / UNMEASURABLE_TEXT /
    UNMEASURABLE_SECURITY -- the third bucket is never folded into a mismatch."""
    article_key = gold_row.get("article_key")
    security_key = gold_row.get("security_key")
    article = articles_by_key.get(article_key)
    security = securities_by_key.get(security_key)

    if article is None:
        return "UNMEASURABLE_TEXT", {
            "article_key": article_key,
            "security_key": security_key,
            "reason": "no silver article row for this article_key in the newest silver_latest read",
        }
    if security is None:
        return "UNMEASURABLE_SECURITY", {
            "article_key": article_key,
            "security_key": security_key,
            "reason": "security_key absent from the live universe_securities.build() alias table",
        }

    info = pg._security_mentions(article, security)
    derived_tier, derived_weight = pg.assign_tier(
        info["mention_in_title"], info["mention_in_lead"], info["mention_count"], info["share"],
    )
    stored_tier = gold_row.get("signal_tier")
    detail = {
        "article_key": article_key,
        "security_key": security_key,
        "stored_tier": stored_tier,
        "stored_weight": gold_row.get("signal_weight"),
        "derived_tier": derived_tier,
        "derived_weight": derived_weight,
        "inputs_from_text": {
            "mention_in_title": info["mention_in_title"],
            "mention_in_lead": info["mention_in_lead"],
            "mention_count": info["mention_count"],
            "share": info["share"],
        },
    }
    status = "AGREE" if derived_tier == stored_tier else "DISAGREE"
    return status, detail


def rederive_all(gold_rows, articles_by_key, securities_by_key):
    """Runs `rederive_row` over every row; returns the four buckets plus the detail rows."""
    agree, disagree, unmeasurable_text, unmeasurable_security = [], [], [], []
    for row in gold_rows:
        status, detail = rederive_row(row, articles_by_key, securities_by_key)
        if status == "AGREE":
            agree.append(detail)
        elif status == "DISAGREE":
            disagree.append(detail)
        elif status == "UNMEASURABLE_TEXT":
            unmeasurable_text.append(detail)
        else:
            unmeasurable_security.append(detail)
    return agree, disagree, unmeasurable_text, unmeasurable_security
