"""ADVI_COTBKF TO-CB-cs-1 AC2 (issuer's check): do the use_class labels of the built account_day_value mark the Yahoo-sourced prices?

Reads only the three label/price columns of <build>/account_day_value.parquet and prints one line:
  LABELS adv_rows=<n> yahoo_source_rows=<a> labelled_rows=<b> equal=<a==b>
a = rows whose price_source has a '|'-split part equal to yahoo_finance or linear_interpolation (dv.YAHOO_SOURCES);
b = rows whose use_class is not NOT_YAHOO. Counts only; no account, name or value is read or printed.
A missing file raises (the criterion FAILS at a base where the build does not exist).
"""
import sys

import pyarrow.compute as pc
import pyarrow.parquet as pq

BUILD = sys.argv[1] if len(sys.argv) > 1 else "C:/Dev/ajb_workspace/.scratch/cotbkf_r97/build/account_day_value.parquet"
YAHOO = ("yahoo_finance", "linear_interpolation")

t = pq.read_table(BUILD, columns=["price_source", "use_class", "porting_verdict"])
n = t.num_rows
src = t["price_source"].cast("string")
hit = None
for y in YAHOO:
    # a '|'-joined label names a source when it equals it, starts with it + '|', ends with '|' + it, or holds '|' + it + '|'
    m = pc.or_(pc.or_(pc.equal(src, y), pc.starts_with(src, y + "|")),
               pc.or_(pc.ends_with(src, "|" + y), pc.match_substring(src, "|" + y + "|")))
    m = pc.fill_null(m, False)
    hit = m if hit is None else pc.or_(hit, m)
a = int(pc.sum(hit.cast("int64")).as_py() or 0)
b = int(pc.sum(pc.fill_null(pc.not_equal(t["use_class"].cast("string"), "NOT_YAHOO"), False).cast("int64")).as_py() or 0)
print("LABELS adv_rows=%d yahoo_source_rows=%d labelled_rows=%d equal=%s" % (n, a, b, a == b))
