"""HARVST served gold rebuild #5 -- the serializing dry run the NEW never-widen pair signs (issuer, NO WRITE).

Track C step 1 (CTO msg 28509; cells aj-7 + aj-8): `title` (VERBATIM) and `published_precision` JOIN every gold mention
row. This runs the round-32 dry run (round32/checks/gold_rebuild.signing.py: the builders' own code through a capturing
client, PUTS SENT 0) with ONE change to the comparison: rows are compared on the PRE-EXISTING field set, so the two
added fields alone never count as a change. Its rule is otherwise the round-32 rule: mention gone 0 / changed 0;
daily gone 0 / OTHER 0. Then it checks every built mention row CARRIES both new fields, with the title verbatim against
the silver article (null where silver has none).

Writes `round37/gold_rebuild5_signing.json`. Prints `RULE: HOLDS` only when all of it holds.
"""
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R32C = os.path.join(os.path.dirname(HERE), "round32", "checks")
sys.path.insert(0, R32C)
ADDED_FIELDS = ("title", "published_precision")

_spec = importlib.util.spec_from_file_location("r32_signing", os.path.join(R32C, "gold_rebuild.signing.py"))
r32 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r32)

import pyarrow.parquet as pq  # noqa: E402

from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

r32.OUT = os.path.join(HERE, "gold_rebuild5_signing.json")


def _rows_by_pre_existing(rows, key):
    return {key(r): json.dumps({k: v for k, v in r.items() if k not in ADDED_FIELDS}, sort_keys=True, default=str)
            for r in rows}


r32.rows_by = _rows_by_pre_existing

_captured = {}
_orig_capturing = r32.sg.CapturingClient


class _Spy(_orig_capturing):
    def put_object(self, Bucket, Key, Body, **kw):
        _captured[Key] = Body
        return super().put_object(Bucket=Bucket, Key=Key, Body=Body, **kw)


r32.sg.CapturingClient = _Spy


def main():
    rc = r32.main()
    mention_keys = [k for k in _captured if "/article_security_mention/" in k]
    if len(mention_keys) != 1:
        print("FIELDS: could not isolate the captured mention part (%d candidates)" % len(mention_keys))
        print("RULE: BROKEN")
        return 1
    rows = pq.read_table(io.BytesIO(_captured[mention_keys[0]])).to_pylist()
    missing = sum(1 for r in rows if any(f not in r for f in ADDED_FIELDS))
    silver = {}
    for pub in sorted({r.get("publisher") for r in rows if r.get("publisher")}):
        for (k,), s in store.silver_latest(hg.SOURCE_FOR_PUBLISHER[pub], "article", ("article_key",)).items():
            silver[k] = s
    title_bad = sum(1 for r in rows if r.get("article_key") in silver
                    and r.get("title") != (silver[r["article_key"]].get("title") or None))
    prec_bad = sum(1 for r in rows if r.get("article_key") in silver
                   and r.get("published_precision") != silver[r["article_key"]].get("published_precision"))
    titled = sum(1 for r in rows if r.get("title"))
    print("FIELDS: %d built rows; missing a new field %d; title not verbatim %d; precision mismatch %d; titled %d"
          % (len(rows), missing, title_bad, prec_bad, titled))
    out = json.load(open(r32.OUT, encoding="utf-8"))
    out["added_fields"] = {"rows": len(rows), "missing": missing, "title_not_verbatim": title_bad,
                           "precision_mismatch": prec_bad, "titled": titled, "compare": "pre-existing fields only"}
    json.dump(out, open(r32.OUT, "w", encoding="utf-8"), indent=1, default=str)
    holds = rc == 0 and not missing and not title_bad and not prec_bad
    print("RULE (rebuild #5): %s" % ("HOLDS" if holds else "BROKEN"))
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
