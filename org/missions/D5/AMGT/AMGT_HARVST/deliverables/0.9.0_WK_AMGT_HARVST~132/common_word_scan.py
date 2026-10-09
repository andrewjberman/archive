"""AMGT_HARVST round 76, HVST-bt-1 AMENDMENT 1/2 (`1.0.0_SA_CTO~DELL1` ADDENDUM 4 msg 2353, ADDENDUM 5 msg 2380) -- the COMMON-WORD SET, MEASURED FROM SILVER.
Worker 0.9.0_WK_AMGT_HARVST~132.

For every alias of every security in `0.9.0_WK_AMGT_HARVST~129/securities.universe.r75.json`, over every silver article (title and
every text block; the SAME read the census uses, `publication_gold._iter_latest_articles`, S3 GETs only), count:
  LOWER   whole-word uses written all lower-case (`visa`, `orange`);
  CAP_MID whole-word uses whose first letter is a capital and that are NOT the first word of a title or of a sentence.
A sentence opens at the start of a block (the title is a block), after `. `, `? `, `! `, or after a line break (the character
before the use is `\\n` or `\\r`). The word bounds are the matcher's own: `(?<!\\w)alias(?!\\w)`, case-insensitive. A use that is
neither (lower-case first letter with a later capital, `eBay`) is counted in neither column. AMENDMENT 2: an alias is a COMMON WORD
when LOWER / CAP_MID >= `publication_gold._COMMON_WORD_RATIO` (0.2; CAP_MID = 0 with LOWER > 0 is flagged); the matcher applies that
test when it loads the file, and the file holds every alias with LOWER, CAP_MID, ratio and the flag.
`CW_REUSE=1` re-writes the file from the LOWER / CAP_MID counts already in it (no silver read, the counts do not change with the
threshold), adding the ratio and the flag.

Writes `common_word_aliases.json` beside this script. Nothing is written to S3. Run from the worktree root:
`PYTHONPATH=. python <this file>`. `CW_LIMIT=<n>` stops after n articles and writes to `.scratch/` (smoke runs only).
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *[".."] * 7))
sys.path.insert(0, ROOT)

from lib.research.harvest import publication_gold as pg  # noqa: E402

LIST = os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables", "0.9.0_WK_AMGT_HARVST~129",
                    "securities.universe.r75.json")
OUT = os.path.join(HERE, "common_word_aliases.json")
LIMIT = int(os.environ.get("CW_LIMIT", "0"))
if LIMIT:
    OUT = os.path.join(ROOT, ".scratch", "common_word_aliases.smoke.json")

SENTENCE_OPENERS = (". ", "? ", "! ")


def sentence_start(text, start):
    """True when the use at `start` is the first word of its block or of a sentence (see the module docstring)."""
    if start == 0:
        return True
    if text[start - 1] in "\n\r":
        return True
    return start >= 2 and text[start - 2:start] in SENTENCE_OPENERS


def classify(text, match):
    """'lower', 'cap_mid' or None for one regex match."""
    span = match.group(0)
    letter = re.search(r"[^\W\d_]", span)
    if letter is None:
        return None
    if span == span.lower():
        return "lower"
    if letter.group(0).isupper() and not sentence_start(text, match.start()):
        return "cap_mid"
    return None


def _finish(rows, scanned):
    """Add ratio and flag to each row, sort, write `OUT`."""
    for r in rows:
        r["ratio"] = (round(float(r["lower"]) / r["cap_mid"], 6) if r["cap_mid"] > 0 else None)
        r["flagged"] = bool(pg._is_common_word(r["lower"], r["cap_mid"]))
    rows.sort(key=lambda r: (r["security_key"], r["alias"]))
    flagged = [r for r in rows if r["flagged"]]
    doc = {"definition": "COMMON when LOWER / CAP_MID >= %s (CAP_MID = 0 with LOWER > 0 counts as flagged); LOWER = whole-word "
                         "all-lower-case uses; CAP_MID = whole-word capital-first uses that are not the first word of a title/block "
                         "or of a sentence (after '. ', '? ', '! ' or a line break); counted over every silver article title and "
                         "text block" % pg._COMMON_WORD_RATIO,
           "ratio_threshold": pg._COMMON_WORD_RATIO,
           "source_list": "0.9.0_WK_AMGT_HARVST~129/securities.universe.r75.json",
           "articles_scanned": scanned, "aliases_counted": len(rows), "aliases_flagged": len(flagged), "aliases": rows}
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(doc, handle, indent=1, ensure_ascii=True)
        handle.write("\n")
    print("DONE: articles scanned %d; (security, alias) rows %d; flagged %d; wrote %s" % (scanned, len(rows), len(flagged), OUT))
    return 0


def main():
    if os.environ.get("CW_REUSE") == "1":
        old = json.load(open(OUT, encoding="utf-8"))
        return _finish([{k: r[k] for k in ("security_key", "alias", "lower", "cap_mid", "articles_scanned")} for r in old["aliases"]],
                       old["articles_scanned"])
    securities = json.load(open(LIST, encoding="utf-8"))
    by_text = {}          # alias lower-cased text -> [compiled regex, lower, cap_mid]
    for sec in securities:
        for alias in sec.get("aliases") or []:
            low = alias.strip().lower()
            if low and low not in by_text:
                by_text[low] = [re.compile(r"(?<!\w)" + re.escape(alias.strip()) + r"(?!\w)", re.I), 0, 0]
    print("aliases to count: %d distinct (lower-cased) over %d securities" % (len(by_text), len(securities)))
    scanned = 0
    for article in pg._iter_latest_articles():
        scanned += 1
        if LIMIT and scanned > LIMIT:
            scanned -= 1
            break
        texts = [article.get("title") or ""] + [b or "" for b in (article.get("text_blocks") or [])]
        for text in texts:
            if not text:
                continue
            lowered = text.lower()
            for low, entry in by_text.items():
                if low not in lowered:
                    continue
                for match in entry[0].finditer(text):
                    kind = classify(text, match)
                    if kind == "lower":
                        entry[1] += 1
                    elif kind == "cap_mid":
                        entry[2] += 1
        if scanned % 5000 == 0:
            print("scanned %d articles" % scanned)
            sys.stdout.flush()
    rows = []
    for sec in securities:
        for alias in sec.get("aliases") or []:
            low = alias.strip().lower()
            if not low:
                continue
            _rx, lower, cap_mid = by_text[low]
            rows.append({"security_key": sec["security_key"], "alias": alias, "lower": lower, "cap_mid": cap_mid,
                         "articles_scanned": scanned})
    return _finish(rows, scanned)


if __name__ == "__main__":
    sys.exit(main())
