"""ADVI_COTBKF TO-CB-cs-1 AC2 (issuer's check, AMENDED 1): do the use_class labels of the built account_day_value mark the Yahoo-sourced prices?

The built table's price_source column carries the store name, never the per-point source, so the check joins the build's
(cusip, date) to the regrade's security_day_price.parquet, whose `source` column is the per-point label.
  a = priced, non-cash account_day_value rows whose (cusip, date) point names yahoo_finance or linear_interpolation in the price file
  b = rows whose use_class is not NOT_YAHOO
Prints one line:
  LABELS adv_rows=<n> yahoo_point_rows=<a> labelled_rows=<b> equal=<a==b>
Counts only; no account, name or value is read into the output. A missing file raises (the criterion FAILS where the build or
the regrade does not exist). Cash rows are the rows priced by the CASH store (`cash-at-par`), which the builder never labels.
Usage: python cs1_ac2_label_check.py [build_dir] [regrade_after_dir]
"""
import sys

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

BUILD = sys.argv[1] if len(sys.argv) > 1 else "C:/Dev/ajb_workspace/.scratch/cotbkf_r97/build"
AFTER = sys.argv[2] if len(sys.argv) > 2 else "C:/Dev/ajb_workspace/.scratch/cotbkf_r97/regrade/after"
YAHOO = ("yahoo_finance", "linear_interpolation")
CASH_STORE = "cash-at-par"


def names_yahoo(src):
    hit = None
    for y in YAHOO:
        m = pc.or_(pc.or_(pc.equal(src, y), pc.starts_with(src, y + "|")),
                   pc.or_(pc.ends_with(src, "|" + y), pc.match_substring(src, "|" + y + "|")))
        m = pc.fill_null(m, False)
        hit = m if hit is None else pc.or_(hit, m)
    return hit


adv = pq.read_table(BUILD + "/account_day_value.parquet", columns=["cusip", "date", "close", "price_source", "use_class"])
px = pq.read_table(AFTER + "/security_day_price.parquet", columns=["cusip", "date", "source"])
yahoo_pts = px.filter(names_yahoo(px["source"].cast("string"))).select(["cusip", "date"]).group_by(["cusip", "date"]).aggregate([])
priced = adv.filter(pc.and_(pc.is_valid(adv["close"]), pc.not_equal(pc.fill_null(adv["price_source"].cast("string"), ""), CASH_STORE)))
j = priced.join(yahoo_pts.append_column("_y", pa.array([1] * yahoo_pts.num_rows, pa.int8())), keys=["cusip", "date"], join_type="inner")
a = j.num_rows
b = int(pc.sum(pc.fill_null(pc.not_equal(adv["use_class"].cast("string"), "NOT_YAHOO"), False).cast("int64")).as_py() or 0)
print("LABELS adv_rows=%d yahoo_point_rows=%d labelled_rows=%d equal=%s" % (adv.num_rows, a, b, a == b))
