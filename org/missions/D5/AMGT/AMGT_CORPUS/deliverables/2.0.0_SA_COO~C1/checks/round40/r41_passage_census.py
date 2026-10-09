"""AMGT_CORPUS round 40 -> 41 evidence (UB-20261009T034754Z-ea48 Part C): a census of the STORED method-7 dossiers' passage
fields for two round-41 candidates, so the round-40 analysis cuts them with each criterion already measured.

Read-only: it lists and reads the gold research_dossier objects (newest per security); nothing is written.

  python r41_passage_census.py          (PYTHONPATH=. from the repository root)

  PREFIX   a passage that opens with a scorecard label and score, "<Label> <1-3 digits> " (e.g. "Management/Board 80 Eddie
           Wu ..."): the word-boundary START item.
  CUT      a text field value that ends without a sentence end (. ! ? ; : ) " ' or a closing bracket) -- the page-break /
           word-boundary END item. Printed by field and name.
DANGLING  the subset of CUT whose last token is a trailing comma or a word that cannot end a sentence (the real cut);
           NO-STOP is a complete phrase without a full stop.
Last line: `r41 census names <n> fields <f> prefix <p> cut <c> dangling <d>`. A fix for each item would read 0 on its count.
"""
import json
import re
import sys

import boto3

BUCKET = "opal-data-harvest"
PREFIX = "amgt/harvest/gold/research_dossier/"
TEXT_FIELDS = [
    "company_description", "growth_algorithm", "investment_thesis_summary", "management", "negatives", "positives",
    "risks", "special_items", "thesis_summary", "why_we_own",
]
RE_PREFIX = re.compile(r"^[A-Z][A-Za-z/&\- ]{2,40} \d{1,3} (?=[A-Z])")
ENDS = tuple(".!?;:)]\"'”’")
# A value whose LAST token cannot end an English sentence: a trailing comma, or a closed set of function words and modals.
DANGLING_WORDS = {
    "a", "an", "the", "and", "or", "but", "of", "to", "in", "on", "for", "with", "by", "at", "from", "as", "like", "is",
    "are", "was", "were", "be", "been", "should", "would", "could", "will", "can", "may", "might", "must", "that", "which",
    "who", "whose", "all", "its", "their", "his", "her",
}


def newest_per_key(s3):
    best, token = {}, None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": PREFIX}
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        for o in r.get("Contents", []):
            k = o["Key"]
            m = re.search(r"security_key=([^/]+)/as_of=([^/]+)\.json$", k)
            if m and m.group(2) > best.get(m.group(1), ("", ""))[0]:
                best[m.group(1)] = (m.group(2), k)
        if not r.get("IsTruncated"):
            break
        token = r["NextContinuationToken"]
    return {sk: v[1] for sk, v in best.items()}


def text_of(v):
    if isinstance(v, dict):
        return v.get("value") if isinstance(v.get("value"), str) else None
    return v if isinstance(v, str) else None


def main():
    s3 = boto3.client("s3")
    keys = newest_per_key(s3)
    fields = prefixed = cut = dang = 0
    for sk in sorted(keys):
        doc = json.loads(s3.get_object(Bucket=BUCKET, Key=keys[sk])["Body"].read())
        f = doc.get("fields") or (doc.get("document") or {}).get("fields") or {}
        for name in TEXT_FIELDS:
            t = text_of(f.get(name))
            if not t:
                continue
            fields += 1
            t = t.strip()
            if RE_PREFIX.match(t):
                prefixed += 1
                print(f"PREFIX {sk:22} {name:26} {t[:70]!r}")
            if not t.endswith(ENDS):
                cut += 1
                last = t.split()[-1] if t.split() else ""
                dangling = last.endswith(",") or last.lower().strip(",") in DANGLING_WORDS
                dang += dangling
                tag = "DANGLING" if dangling else "NO-STOP "
                print(f"CUT {tag} {sk:22} {name:26} ...{t[-60:]!r}")
    print(f"r41 census names {len(keys)} fields {fields} prefix {prefixed} cut {cut} dangling {dang}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
