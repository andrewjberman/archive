"""account_id_hash_builder.py -- the served account-id hash list the client-data-check gate reads (CTO containment ruling @0e8209c33c
AMENDMENT 3 @4b7dcc5929; MSTR~DELL2 msg 3726). Owner: 2.0.0_SA_COO~P2.

Reads, for every firm, the latest partition of each source table its holdings builder reads (holdings_snapshot.py / holdings_49f.py),
takes every column named like an account id or number, and writes sha256(UPPER(id)) per line to $OPAL_ACCOUNT_ID_HASHES, else
~/.opal/account_id_hashes.txt -- OUTSIDE the repo. No id is printed or written anywhere else; the stdout carries counts only.

Forms hashed per value: the stripped string; for an all-digit id also its 10-digit zero-pad and its zero-stripped form (>= 5 digits),
so a file carrying either spelling is caught. Ids the client-data-check tokenizer cannot see (< 5 digits, outside [A-Za-z0-9-]{5,24})
are counted and skipped.

Usage: python account_id_hash_builder.py [--as-of YYYY-MM-DD] [--extra <file of ids, one 10-digit token per match>]...
Exit 1 when any firm yields 0 ids or any source fails to read: an ABSENT source is never a smaller list.
"""
import argparse
import datetime as dt
import hashlib
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/investor_reporting"))

# A column whose name ENDS in an account identity word (account_id, Account_Number, commonwealth_account, AccountNumber, ...);
# account_type / Account_Status / account_open_date are not ids and are excluded by the anchor.
ACCOUNT_COL = re.compile(r"(?i)(account|acct)[ _]?(id|number|num|no|nbr)?$")
DATE_LIKE = re.compile(r"\d{4}-\d{2}-\d{2}|\d{8}T|\d{4}/\d{2}/\d{2}")
MIN_DIGITS_ALL_NUMERIC = 8  # a shorter all-digit token is indistinguishable from an ordinary number (ports, counts)
# A zero-padded short id (0000081907) collides with PDF xref offsets and padded counters; an all-digit form needs this many
# significant digits, so "0"/empty ids padded to 0000000000 never enter the list.
MIN_SIGNIFICANT_DIGITS = 7
GATE_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{4,23}")

# (firm, bucket, table prefix, partition prefix). Latest partition <= as_of; key is <prefix><part><date>/data.parquet.
SOURCES = [
    # 49F's two Schwab reporting masters (firm registry `masters`), the SmartX overlay and the Black Diamond 49f scope.
    ("49financial", "opal-data-assets", "schwab/08335338/silver/dim_balance/", "date="),
    ("49financial", "opal-data-assets", "schwab/08335338/silver/dim_position/", "date="),
    ("49financial", "opal-data-assets", "schwab/08335338/silver/fact_acc/", "date="),
    ("49financial", "opal-data-assets", "schwab/08242234/silver/dim_balance/", "date="),
    ("49financial", "opal-data-assets", "schwab/08242234/silver/dim_position/", "date="),
    ("49financial", "opal-data-assets", "schwab/08242234/silver/fact_acc/", "date="),
    ("49financial", "opal-data-assets", "smartx/platform/silver/fact_allocation_account_map/", "date="),
    ("49financial", "opal-data-assets", "blackdiamond/49f/silver/dim_account_xref/", "date="),
    ("49financial", "opal-data-assets", "blackdiamond/49f/silver/fact_bd_allocation/", "date="),
    ("cottonwood", "opal-data-assets", "blackdiamond/cottonwood/silver/fact_holdings/", "date="),
    ("cottonwood", "opal-data-assets", "blackdiamond/cottonwood/silver/fact_allocations/", "date="),
    ("cottonwood", "opal-data-assets", "blackdiamond/cottonwood/silver/fact_model_assignment/", "date="),
    ("inflection", "opal-data-inf", "silver/api_dims/accounts_v2/", "snapshot_date="),
] + [("cottonwood", "opal-data-assets", "commonwealth/cottonwood/silver/%s/" % t, "date=")
     for t in ("account_day_value", "account_links", "coverage", "crosswalk", "performance", "positions", "transactions")]


def forms(v):
    if v is None:
        return set()
    if isinstance(v, float):
        if v != v or v != int(v):
            return set()
        v = int(v)
    s = str(v).strip()
    out = {s}
    if s.isdigit():
        if len(s) < 10:
            out.add(s.zfill(10))
        out.add(s.lstrip("0") or "0")
    return {x.upper() for x in out if GATE_TOKEN.fullmatch(x) and sum(c.isdigit() for c in x) >= 5
            and not DATE_LIKE.search(x) and not (x.isdigit() and len(x) < MIN_DIGITS_ALL_NUMERIC)
            and not (x.isdigit() and len(x.lstrip("0")) < MIN_SIGNIFICANT_DIGITS)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", default=dt.date.today().isoformat())
    ap.add_argument("--extra", action="append", default=[])
    a = ap.parse_args()
    import boto3
    import holdings_snapshot as hs

    s3 = boto3.client("s3")
    ids = {"49financial": set(), "cottonwood": set(), "inflection": set()}
    bad = 0
    srcs = [(f, b, p, d, None) for f, b, p, d in SOURCES]
    try:
        _, inf_key = hs._inf_positions_source_key(s3, a.as_of)
        srcs.append(("inflection", "opal-data-inf", inf_key, None, inf_key))
    except Exception as e:  # noqa: BLE001
        print("ERROR: inflection positions key: %s" % type(e).__name__)
        bad += 1
    for firm, bucket, prefix, part, key in srcs:
        try:
            if key is None:
                date = hs._latest_date_partition(s3, bucket, prefix, date_prefix=part, as_of=a.as_of)
                if date is None:
                    raise LookupError("no partition")
                key = "%s%s%s/" % (prefix, part, date)
            keys = [key] if key.endswith(".parquet") else sorted(
                o["Key"] for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=key)
                for o in pg.get("Contents", []) if o["Key"].endswith(".parquet"))
            if not keys:
                raise LookupError("no parquet in partition")
            import pandas as pd
            df = pd.concat([hs._read_parquet(s3, bucket, k) for k in keys], ignore_index=True)
        except Exception as e:  # noqa: BLE001
            print("ERROR: %s %s: %s" % (firm, prefix, type(e).__name__))
            bad += 1
            continue
        cols = [c for c in df.columns if ACCOUNT_COL.match(str(c).replace(" ", "_"))]
        if not cols:
            print("WARN: %s %s has no account-named column; columns %s" % (firm, key, list(df.columns)[:30]))
        before = len(ids[firm])
        skipped = 0
        for c in cols:
            for v in df[c].dropna().unique():
                f = forms(v)
                if not f:
                    skipped += 1
                ids[firm] |= f
        print("OK: %s %s rows=%d cols=%s new_forms=%d skipped=%d" % (firm, key.rsplit("/", 2)[0], len(df), cols,
                                                                      len(ids[firm]) - before, skipped))
    for x in a.extra:
        toks = set(re.findall(r"(?<!\d)\d{10}(?!\d)", Path(x).read_text(encoding="utf-8")))
        before = len(ids["49financial"])
        for t in toks:
            ids["49financial"] |= forms(t)
        print("OK: extra file -> 49financial new_forms=%d (tokens %d)" % (len(ids["49financial"]) - before, len(toks)))
    for firm, v in ids.items():
        shapes = {}
        for i in v:
            k = re.sub(r"[0-9]", "9", re.sub(r"[A-Za-z]", "A", i))
            shapes[k] = shapes.get(k, 0) + 1
        print("SHAPES: %s %s" % (firm, sorted(shapes.items(), key=lambda kv: -kv[1])[:8]))
    hashes = {hashlib.sha256(i.encode("utf-8")).hexdigest() for s in ids.values() for i in s}
    out = Path(os.environ.get("OPAL_ACCOUNT_ID_HASHES", "").strip() or (Path.home() / ".opal" / "account_id_hashes.txt"))
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.write_text("".join(h + "\n" for h in sorted(hashes)), encoding="ascii")
    os.replace(tmp, out)
    for firm, v in ids.items():  # per-firm lists beside the union, for token minting (acct#<sha8 of "firm:id">)
        pf = out.parent / ("account_id_hashes.%s.txt" % firm)
        pf.write_text("".join(h + "\n" for h in sorted(hashlib.sha256(i.encode("utf-8")).hexdigest() for i in v)),
                      encoding="ascii")
    print("WROTE: %s hashes=%d per_firm_forms=%s sources_failed=%d" % (out, len(hashes), {k: len(v) for k, v in ids.items()}, bad))
    empty = [k for k, v in ids.items() if not v]
    if empty or bad:
        print("ERROR: firms with 0 ids %s; failed sources %d -- the list is INCOMPLETE" % (empty, bad))
        sys.exit(1)


if __name__ == "__main__":
    main()
