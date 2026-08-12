"""OPAL_BRDSEP.T2 -- the NON-Opal-model cohort (wallet share), value + counts.

Per firm, under BOTH denominators:
  A = accounts holding at least one Opal model
  B = all in-scope accounts at the firm

Every figure is a COMPLEMENT, therefore a subtraction, so all three T1 hazards are live:
absent-is-not-zero, coverage-onset-presents-as-growth, and a subtraction starting at its
weakest input. Reads local mirrors of landed artifacts only; run twice and diff (T2-A9).

THE FIGURE IS AN OPPORTUNITY DENOMINATOR, NEVER AN ASSET CLAIM. It must not be added to
the T1 asset base nor presented as Opal AUA.
"""
from __future__ import annotations

import glob
import json

import pandas as pd

ANDREW18 = [
    "Anna *9237", "Anna *9238", "Blended Opal / Satellite 50",
    "Moderate Income Portfolio", "Opal - Beecherl Legg",
    "Opal - Cash + Satellite 50", "Opal - Income",
    "Opal 66% Long Term / 34% UST", "Opal Satellite 15", "Opal Satellite 30",
    "Opal Satellite 40", "Opal Satellite 50", "Opal Satellite 60",
    "Opal Satellite 70", "Opal Satellite 80", "Opal Satellite 98",
    "Opal Ultra Short Term", "Opal UST/ Sat 70",
]
OFFLIST = ["opal hendrickson lt/ust", "opal sat 50+ 15% cash",
           "opal long term aggressive", "opal long term conservative",
           "opal satellite 90"]


def norm(s) -> str:
    return " ".join(str(s).split()).strip().lower()


def rd(pat: str) -> pd.DataFrame:
    return pd.concat([pd.read_parquet(f) for f in glob.glob(pat)], ignore_index=True)


out: dict = {
    "as_of": {"49financial": "2026-08-11", "inflection": "2026-08-11", "cottonwood": "2026-08-10"},
    "warning": "OPPORTUNITY DENOMINATOR, NOT AN ASSET CLAIM -- never add to the T1 base",
}

# --------------------------------------------------------------- 49 Financial
m = rd("sx/fact_allocation_account_map/*.parquet")
r = rd("sx/fact_model_allocation_roster/*.parquet")
m = m.merge(r[["model_id", "model_name"]].drop_duplicates(), on="model_id", how="left")
m["aum_value"] = pd.to_numeric(m.aum_value, errors="coerce")
m["acct_norm"] = m.account_number.astype(str).str.strip().str.lstrip("0")
opal_m = m[m.model_name.str.startswith("Opal", na=False)]
opal_accts = set(opal_m.acct_norm)

bal = rd("cnt/bal0811/*.parquet")
bal["acct_norm"] = bal["account_id"].astype(str).str.strip().str.lstrip("0")
bal["nmpc"] = pd.to_numeric(bal["net_mv_plus_cash"], errors="coerce")
acc = rd("cnt/acc0811/*.parquet")
acc["acct_norm"] = acc["account_id"].astype(str).str.strip().str.lstrip("0")
acc["tin"] = acc["ssn_tin_number"].astype(str).str.strip()
acc = acc[(acc.tin != "") & (acc.tin.str.lower() != "nan") & (acc.tin != "0")]

inA = bal[bal.acct_norm.isin(opal_accts)]
accA = acc[acc.acct_norm.isin(opal_accts)]
accNon = acc[~acc.acct_norm.isin(opal_accts)]
both = set(accA.tin) & set(accNon.tin)
tinmap = acc.drop_duplicates("acct_norm").set_index("acct_norm")["tin"]
bal["tin"] = bal.acct_norm.map(tinmap)
bothbal = bal[bal.tin.isin(both)]
nonopal_both = bothbal[~bothbal.acct_norm.isin(opal_accts)]

opal_val = float(opal_m.aum_value.sum())
out["49financial"] = {
    "account": "08242234",
    "opal_definition": "SmartX fact_allocation_account_map, model_name starting 'Opal' (6 models with accounts)",
    "opal_model_value_smartx": opal_val,
    "platinum_model_aua": 1451519328.79,
    "smartx_minus_platinum": opal_val - 1451519328.79,
    "denominator_A": {
        "what": "accounts holding >=1 Opal model",
        "accounts": int(inA.acct_norm.nunique()), "clients": int(accA.tin.nunique()),
        "total_value": float(inA.nmpc.sum()), "opal_value": opal_val,
        "non_opal_value": float(inA.nmpc.sum()) - opal_val,
    },
    "denominator_B": {
        "what": "all accounts in 08242234",
        "accounts": int(bal.acct_norm.nunique()), "clients": int(acc.tin.nunique()),
        "total_value": float(bal.nmpc.sum()), "opal_value": opal_val,
        "non_opal_value": float(bal.nmpc.sum()) - opal_val,
    },
    "client_grain": {
        "clients_holding_both": len(both),
        "their_total_value": float(bothbal.nmpc.sum()),
        "their_non_opal_value": float(nonopal_both.nmpc.sum()),
        "their_non_opal_accounts": int(nonopal_both.acct_norm.nunique()),
    },
    "cto_cross_check": {
        "cto_subtraction": 285429409.86,
        "my_denominator_B": float(bal.nmpc.sum()) - opal_val,
        "difference": (float(bal.nmpc.sum()) - opal_val) - 285429409.86,
        "attribution": "entirely the Opal-model base: SmartX account-level vs platinum model_aua",
    },
    "denominators": {"account_map_rows": len(m), "dim_balance_rows": len(bal),
                     "fact_acc_rows_with_tin": len(acc)},
}

# ----------------------------------------------------------------- Inflection
inf = rd("cnt/inf_0811/*.parquet")
inf["cv"] = pd.to_numeric(inf["currentValue"], errors="coerce")
inf["is_opal"] = inf["modelName"].astype(str).str.lower().str.contains("opal", na=False)
grain = inf.groupby("accountId")["modelName"].nunique()
opal_clients = set(inf[inf.is_opal].clientId)
inC = inf[inf.clientId.isin(opal_clients)]
nonC = inC[~inC.is_opal]
noc = inf[~inf.clientId.isin(opal_clients)]
out["inflection"] = {
    "basis": "ORION-INCLUSIVE (silver fact_positions modelName contains 'opal'). The platinum "
             "Eclipse-crosswalked base is a DIFFERENT base; complements of the two differ.",
    "model_grain_finding": {
        "accounts": int(len(grain)),
        "accounts_with_more_than_one_model": int((grain > 1).sum()),
        "null_modelName_rows": int(inf["modelName"].isna().sum()),
        "consequence": "modelName is strictly ACCOUNT-LEVEL, so account-grain denominator A is "
                       "degenerate -- non-Opal within Opal-holding accounts is $0 BY CONSTRUCTION, "
                       "not by measurement.",
    },
    "denominator_A_account_grain": {
        "accounts": int(inf[inf.is_opal].accountId.nunique()),
        "clients": int(inf[inf.is_opal].clientId.nunique()),
        "total_value": float(inf[inf.is_opal].cv.sum()),
        "non_opal_value": 0.0,
        "note": "degenerate by construction -- see model_grain_finding",
    },
    "denominator_A_client_grain": {
        "what": "clients holding >=1 Opal ACCOUNT (the meaningful wallet-share cut here)",
        "clients": len(opal_clients),
        "their_total_value": float(inC.cv.sum()),
        "their_opal_value": float(inC[inC.is_opal].cv.sum()),
        "their_non_opal_value": float(nonC.cv.sum()),
        "their_non_opal_accounts": int(nonC.accountId.nunique()),
        "their_non_opal_clients": int(nonC.clientId.nunique()),
        "opal_share_of_their_wallet_pct": 100 * float(inC[inC.is_opal].cv.sum()) / float(inC.cv.sum()),
    },
    "denominator_B": {
        "accounts": int(inf.accountId.nunique()), "clients": int(inf.clientId.nunique()),
        "total_value": float(inf.cv.sum()),
        "opal_value": float(inf[inf.is_opal].cv.sum()),
        "non_opal_value": float(inf[~inf.is_opal].cv.sum()),
        "non_opal_accounts": int(inf[~inf.is_opal].accountId.nunique()),
        "non_opal_clients": int(inf[~inf.is_opal].clientId.nunique()),
    },
    "clients_with_no_opal_account": {"clients": int(noc.clientId.nunique()),
                                     "accounts": int(noc.accountId.nunique()),
                                     "value": float(noc.cv.sum())},
    "basis_alternative": {
        "platinum_model_aua_2026_08_10": 144978896.75,
        "complement_of_platinum_base_firmwide": float(inf.cv.sum()) - 144978896.75,
        "complement_of_orion_base_firmwide": float(inf[~inf.is_opal].cv.sum()),
    },
    "denominators": {"fact_positions_rows": len(inf)},
}

# ----------------------------------------------------------------- Cottonwood
h = rd("cot/h0810/*.parquet")
h["mv"] = pd.to_numeric(h["Market Value"], errors="coerce")
naive = float(h.mv.sum())
h = h.drop_duplicates(subset=["AccountID", "AssetID"])
acc_rows: list = []
for f in sorted(glob.glob("bd/accounts/*.json")):
    acc_rows.extend(json.load(open(f))["pagedResults"])
a = pd.DataFrame(acc_rows)
roster = json.load(open("bd/models/page_000.json"))["pagedResults"]
by = {norm(x["name"]): x["name"] for x in roster}
resolved = set()
for n in ANDREW18:
    k = norm(n)
    if k in by:
        resolved.add(norm(by[k]))
    else:
        c = [x["name"] for x in roster if k in norm(x["name"]) or norm(x["name"]) in k]
        if len(c) == 1:
            resolved.add(norm(c[0]))
a["sn"] = a.strategyName.map(norm)
a["acctn"] = a.accountNumber.astype(str).str.strip()
a["is_opal18"] = a.sn.isin(resolved)
h["acctn"] = h["Account Number"].astype(str).str.strip()
cm = h.merge(a[["acctn", "strategyName", "sn", "is_opal18"]].drop_duplicates("acctn"),
             on="acctn", how="left")
onl = cm[cm.is_opal18 == True]  # noqa: E712
off = cm[cm.sn.isin(OFFLIST)]
PLAT_MODEL = 136530322.99
out["cottonwood"] = {
    "opal_definition": "Andrew's 18-strategy list, resolved with the T1 normalized matcher",
    "matcher": {"list_size": len(ANDREW18), "resolved": len(resolved),
                "roster_size": len(roster)},
    "relationship_grain_control": {
        "naive_sum": naive, "deduped_sum": float(cm.mv.sum()),
        "phantom": naive - float(cm.mv.sum()),
        "ties_platinum_partner_custody_total": abs(float(cm.mv.sum()) - 482567772.65) < 0.01,
    },
    "denominator_A": {
        "what": "accounts whose strategy is on the 18-list",
        "accounts": int(onl.acctn.nunique()),
        "relationships": int(onl["Relationship ID"].nunique()),
        "total_value": float(onl.mv.sum()),
        "opal_MODEL_component": PLAT_MODEL,
        "non_opal_value": float(onl.mv.sum()) - PLAT_MODEL,
        "note": "an Opal STRATEGY account is not wholly Opal MODEL -- a satellite blend holds "
                "non-Opal sleeves. The difference IS the in-account wallet share.",
    },
    "denominator_B": {
        "what": "all Cottonwood accounts",
        "accounts": int(cm.acctn.nunique()),
        "relationships": int(cm["Relationship ID"].nunique()),
        "total_value": float(cm.mv.sum()),
        "opal_MODEL_component": PLAT_MODEL,
        "non_opal_value": float(cm.mv.sum()) - PLAT_MODEL,
        "ties_platinum_non_model_aua": abs((float(cm.mv.sum()) - PLAT_MODEL) - 346037449.66) < 0.01,
    },
    "off_list_opal_named": {
        "value": float(off.mv.sum()), "accounts": int(off.acctn.nunique()),
        "note": "CLASSIFICATION question -- reported as its own line, neither included nor excluded",
    },
    "denominators": {"holdings_rows_deduped": len(cm), "rebalancer_account_rows": len(a)},
}

print(json.dumps(out, indent=2, default=str))
