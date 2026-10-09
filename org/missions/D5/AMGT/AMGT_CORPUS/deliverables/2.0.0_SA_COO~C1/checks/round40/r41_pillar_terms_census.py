"""AMGT_CORPUS round 40 -> 41 evidence (UB-20261009T034754Z-ea48 Part C, item "a thesis term is a term, not a whole pillar
title"): over the STORED dossiers, how many pillar terms are the pillar's whole title, and how many pillars carry no other term.

Read-only: reads the gold research_dossier objects through `dossier.read_dossier`; nothing is written.

  python r41_pillar_terms_census.py          (PYTHONPATH=. from the repository root)

Prints per name: pillars, terms, whole-title terms, pillars whose ONLY term is the whole title. Last line:
`r41 terms names <n> pillars <p> terms <t> whole_title <w> title_only_pillars <o> unstructured_entries <u>`
(an unstructured entry is a thesis_pillars value that is not a pillar object, e.g. an ABSENT reason). A fix would read 0 on whole_title.
"""
import sys

from lib.research.corpus import dossier as D
from lib.research.identity import crosswalk


def main():
    import boto3
    import re

    s3 = boto3.client("s3")
    keys, token = set(), None
    while True:
        kw = {"Bucket": "opal-data-harvest", "Prefix": "amgt/harvest/gold/research_dossier/"}
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        for o in r.get("Contents", []):
            m = re.search(r"security_key=([^/]+)/", o["Key"])
            if m:
                keys.add(crosswalk.security_key_from_slash_safe(m.group(1)))
        if not r.get("IsTruncated"):
            break
        token = r["NextContinuationToken"]
    tot = {"pillars": 0, "terms": 0, "whole": 0, "only": 0, "unstructured": 0}
    for key in sorted(keys):
        d = D.read_dossier(key)
        raw = ((d or {}).get("document") or {}).get("fields", {}).get("thesis_pillars") or []
        if not isinstance(raw, list):
            raw = [raw]
        pillars = [p for p in raw if isinstance(p, dict) and "pillar" in p]
        tot["unstructured"] += len(raw) - len(pillars)
        n_terms = n_whole = n_only = 0
        for p in pillars:
            title = (p.get("pillar") or "").strip()
            terms = [str(t).strip() for t in (p.get("terms") or [])]
            n_terms += len(terms)
            whole = sum(1 for t in terms if t and t == title)
            n_whole += whole
            n_only += bool(terms) and whole == len(terms)
        tot["pillars"] += len(pillars)
        tot["terms"] += n_terms
        tot["whole"] += n_whole
        tot["only"] += n_only
        if pillars:
            print(f"{key:24} pillars {len(pillars):2} terms {n_terms:3} whole_title {n_whole:2} title_only_pillars {n_only:2}")
    print(f"r41 terms names {len(keys)} pillars {tot['pillars']} terms {tot['terms']} whole_title {tot['whole']} "
          f"title_only_pillars {tot['only']} unstructured_entries {tot['unstructured']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
