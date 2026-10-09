"""TO-DB-b-78 A2, A3, A6 of the first fire: reads the five gold partitions of <day> from S3 (read only) and prints the packet's
after-read figures. Never prints an account id (an account is shown as a sha256 prefix).
Usage (worktree root): python <this file> <day> <out.json>
"""
import hashlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))


def main(day, out_json):
    import boto3
    import pandas as pd
    import opal_naming as on
    import account_activity_lots as aal
    s3 = boto3.client("s3", region_name="us-east-1")

    def addr(t, name):
        u = on.address("irpt", "49financial", "gold", t, "date=%s" % day) + "/" + name
        return u.replace("s3://", "").split("/", 1)

    def frame(t):
        b, k = addr(t, "data.parquet")
        return pd.read_parquet(io.BytesIO(s3.get_object(Bucket=b, Key=k)["Body"].read())), k

    def manifest(t):
        b, k = addr(t, "manifest.json")
        return json.loads(s3.get_object(Bucket=b, Key=k)["Body"].read().decode("utf-8")), k

    def sha(x):
        return hashlib.sha256(str(x).encode()).hexdigest()[:10]

    res = {"day": day}
    act, k_act = frame("account_activity_daily")
    man_act, _ = manifest("account_activity_daily")
    meas = act[act["coverage"] == "MEASURED"]
    res["a2"] = {"partition": k_act, "rows": int(len(act)), "coverage_census": {k: int(v) for k, v in act["coverage"].value_counts().items()},
                 "manifest_coverage": man_act.get("coverage_census", man_act.get("coverage")), "measured_rows": int(len(meas))}
    if len(meas):
        r = meas.iloc[0]
        ident = r["beginning_value"] + r["contributions"] - r["withdrawals"] + r["realized"] + r["unrealized_change"] + r["income"] - r["ending_value"]
        res["a2"].update({"account_sha": sha(r["account_id"]), "identity_expression": float(ident), "identity_gap": float(r["identity_gap"]),
                          "rounding_allowance": float(r["rounding_allowance"]),
                          "abs_gap_within_allowance": bool(abs(float(r["identity_gap"])) <= float(r["rounding_allowance"]) + 1e-12 and abs(float(ident)) <= float(r["rounding_allowance"]) + 1e-9)})
        allm = (meas["identity_gap"].abs() <= meas["rounding_allowance"] + 1e-12)
        res["a2"]["measured_rows_all_within_allowance"] = bool(allm.all())
    res["a3"] = {}
    for t, key in (("account_lot_realized", aal.PRIMARY_KEYS["account_lot_realized"]), ("account_lot_unrealized_daily", aal.PRIMARY_KEYS["account_lot_unrealized_daily"]),
                   ("account_activity_daily", aal.PRIMARY_KEYS["account_activity_daily"])):
        f, k = (act, k_act) if t == "account_activity_daily" else frame(t)
        dup = int(f.duplicated(subset=list(key)).sum())
        e = {"partition": k, "primary_key": list(key), "rows": int(len(f)), "distinct_keys": int(len(f) - dup), "equal": dup == 0}
        if "basis_source" in f.columns:
            c = {k2: int(v) for k2, v in f["basis_source"].value_counts().items()}
            e["basis_source_counts"] = c
            e["basis_source_all_in_enum"] = set(c) <= {"CUSTODIAN", "IN_KIND_TRANSFER_VALUE", "WASH_SALE_EXCLUDED_BASIS"}
        res["a3"][t] = e
    cls, k_cls = frame("account_class_daily")
    man_cls, _ = manifest("account_class_daily")
    ret, k_ret = frame("account_return_daily")
    cm = cls[cls["coverage"] == "MEASURED"]
    ident = {}
    if len(cm):
        g = cm.groupby("account_id")["class_return_daily"].sum()
        tr = ret.drop_duplicates("account_id").set_index("account_id")["total_return_daily"]
        j = pd.concat([g.rename("s"), tr.rename("t")], axis=1, join="inner").dropna()
        gap = (j["s"] - j["t"]).abs()
        first = j.index[0]
        ident = {"account_sha": sha(first), "class_rows": int((cm["account_id"] == first).sum()), "abs_gap": float(gap.iloc[0]),
                 "within_1e-9": bool(gap.iloc[0] <= 1e-9), "accounts_compared": int(len(j)), "accounts_within_1e-9": int((gap <= 1e-9).sum()),
                 "max_abs_gap": float(gap.max())}
    un = cls[cls["asset_class"] == "unclassified"]["market_value_eod"].sum()
    tot = cls["market_value_eod"].sum()
    share = float(un / tot) if tot else None
    res["a6"] = {"partition": k_cls, "class_rows": int(len(cls)), "accounts": int(cls["account_id"].nunique()), "identity": ident,
                 "unclassified_sum": float(un), "all_sum": float(tot), "unclassified_share": share,
                 "manifest_unclassified_share_of_value": man_cls.get("unclassified_share_of_value"),
                 "share_equals_manifest": (man_cls.get("unclassified_share_of_value") is not None and share is not None and abs(float(man_cls["unclassified_share_of_value"]) - share) < 1e-9)}
    res["returns_partition"] = {"partition": k_ret, "rows": int(len(ret))}
    Path(out_json).write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
