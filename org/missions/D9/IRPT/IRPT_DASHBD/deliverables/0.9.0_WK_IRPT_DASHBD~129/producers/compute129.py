import json
import numpy as np
import pandas as pd

Q = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~129/"
m = pd.read_parquet(Q + "work.parquet")
gold = pd.read_parquet(Q + "gold_rows.parquet")[
    ["account_id", "business_date", "income_received"]
]
m = m.merge(gold, on=["account_id", "business_date"], how="left")
N = len(m)
TOL = 0.001244
LARGE = 0.002535
LO, HI = -0.5, 0.5
dqmap = {
    "FLOW_UNRECONCILED": "FU",
    "LARGE_FLOW": "LF",
    "MEASURED": "MEAS",
    "NOT_MEASURABLE": "NM",
}
served = m.day_quality.map(dqmap)
f = m.flow
v1 = m.market_value_eod
v0 = m.v0
incomplete = (served == "FU") & (m.guard_state == "GUARD_NOT_REACHED")
evaluable = (
    m.base_ok
    & ~incomplete
    & (m.guard_state != "GUARD_NOT_REACHED")
    & m.pr.notna().where(
        m.guard_state.isin(["GRADED_AGREED", "GRADED_DISAGREED"]), True
    )
)
graded = m.guard_state.isin(["GRADED_AGREED", "GRADED_DISAGREED"])


def classify(r, share, ir, ev):
    with np.errstate(invalid="ignore"):
        diff = (r - (m.pr + ir)).abs()
        c = np.where(
            graded,
            np.where(diff > TOL, "FU", np.where(share > LARGE, "LF", "MEAS")),
            np.where(share <= TOL, "MEAS", "FU"),
        )
        c = pd.Series(c, index=m.index)
        oob = c.isin(["LF", "MEAS"]) & ~((r > LO) & (r < HI))
        c[oob] = "NM"
    ok = ev & np.isfinite(r)
    return c.where(ok, other=np.nan), ok


share0 = f.abs() / v0
r_end = m.r_end_raw
r_s = m.r_start_raw
r_m = m.r_mid_raw
cE, okE = classify(r_end, share0, m.ir, evaluable)
# control
ctrl = pd.Series(np.where(okE, cE, served), index=m.index)
differ_any = ctrl != served
rest_FU = ctrl == "FU"
rest_LF = ctrl == "LF"
ctl = {}
for nm, k in (("FLOW_UNRECONCILED", "FU"), ("LARGE_FLOW", "LF")):
    sv = served == k
    rs = ctrl == k
    ctl[nm] = {
        "flagged_served": int(sv.sum()),
        "flagged_restated": int(rs.sum()),
        "differ": int((sv != rs).sum()),
        "served_not_restated": int((sv & ~rs).sum()),
        "restated_not_served": int((rs & ~sv).sum()),
    }
# which differ days: chain explained?
dif = m[(ctrl != served)]
ctl["all_class_differ_days"] = int(differ_any.sum())
ctl["differ_days_carried_days_gt1"] = int((dif.carried_days > 1).sum())
ctl["differ_days_carried_days_1"] = int((dif.carried_days == 1).sum())
ctl["differ_days_with_flow_nonzero"] = int((dif.flow != 0).sum())
ctl["evaluated_days"] = int(okE.sum())
print(json.dumps(ctl, indent=1))
# D: days left as served
notrep = m.restate_status.isin(
    ["END_NOT_EQUAL_LEFT_AS_SERVED", "NO_PRIOR_LEFT_AS_SERVED"]
)
D = (ctrl != served) | notrep


def conv(r, share, ir, ev, extra_left=None):
    c, ok = classify(r, share, ir, ev)
    left = D | ~ok
    if extra_left is not None:
        left = left | extra_left
    return pd.Series(np.where(left, served, c), index=m.index), left


def moves(cs, ce=served):
    out = {}
    for nm, k in (("FLOW_UNRECONCILED", "FU"), ("LARGE_FLOW", "LF")):
        e = ce == k
        s = cs == k
        out[nm] = (int(e.sum()), int(s.sum()), int((e & ~s).sum()), int((~e & s).sum()))
    return out


def fallback(cs):
    nullE = served.isin(["FU", "NM"])
    nullS = cs.isin(["FU", "NM"])
    return {
        "null_to_value": int((nullE & ~nullS).sum()),
        "value_to_null": int((~nullE & nullS).sum()),
        "class_changed_any": int((cs != served).sum()),
        "flag_only_moves_no_change_to_return": int(
            ((cs != served) & (nullE == nullS)).sum()
        ),
    }


res = {}
for label, rr, den_adj in (("start", r_s, "s"), ("mid", r_m, "m")):
    cs, left = conv(rr, share0, m.ir, evaluable)
    res[label] = {
        "moves": moves(cs),
        "fallback": fallback(cs),
        "left_as_served_days": int(left.sum()),
    }
    # sensitivity: exclude carried_days>1 (intervening valuation not observable)
    cs2, _ = conv(rr, share0, m.ir, evaluable, extra_left=(m.carried_days > 1))
    res[label]["sens_exclude_carried_gt1"] = moves(cs2)
    # sensitivity: base follows the convention (flow share and income return on v0+f or v0+f/2)
    b = (v0 + f) if label == "start" else (v0 + f / 2)
    with np.errstate(invalid="ignore", divide="ignore"):
        shareB = f.abs() / b
        irB = m.income_received / b
    evB = evaluable & (b > 0)
    csB, _ = conv(rr, shareB, irB, evB)
    res[label]["sens_base_follows_convention"] = moves(csB)
    # days whose END base is invalid but the convention base would be positive and flow != 0
    inv = (~m.base_ok) & (served == "NM") & (m.guard_state == "GUARD_NOT_REACHED")
    res[label]["base_invalid_days_with_positive_convention_base"] = int(
        (inv & (b > 0) & (f != 0)).sum()
    )
# decomposition of END flagged FU by path
fu = served == "FU"
path = {
    "incomplete_unknown_flow_convention_independent": int((fu & incomplete).sum()),
    "ungraded_flow_share_over_tolerance": int(
        (fu & (m.guard_state == "NOT_GRADED_OUTSIDE_DOMAIN")).sum()
    ),
    "graded_disagreed": int((fu & (m.guard_state == "GRADED_DISAGREED")).sum()),
}
print(json.dumps(path, indent=1))
print(json.dumps(res, indent=1))
# NM bands
nm_band = (
    (served == "NM")
    & m.guard_state.isin(["GRADED_AGREED", "NOT_GRADED_OUTSIDE_DOMAIN"])
).sum()
out = {
    "control": ctl,
    "paths": path,
    "result": res,
    "nm_band_rejected_days_served": int(nm_band),
    "n": N,
    "D": int(D.sum()),
    "graded_disagreed_flow_zero": int(
        ((m.guard_state == "GRADED_DISAGREED") & (f == 0)).sum()
    ),
    "served_lf_flow_zero": int(((served == "LF") & (f == 0)).sum()),
}
json.dump(out, open(Q + "results.json", "w"), indent=1)
