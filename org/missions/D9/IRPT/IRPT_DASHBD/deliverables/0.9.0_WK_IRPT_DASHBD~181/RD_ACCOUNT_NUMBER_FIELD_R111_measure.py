import importlib.util
import json
import re
import time
import datetime as dt
from collections import Counter, defaultdict
import pandas as pd

ROOT = "C:/dev/wk-irpt-dashbd-181"
PRIV = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~181"
spec = importlib.util.spec_from_file_location("inflection_account_dim", ROOT + "/data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_dim.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
rd = mod.InflectionSilverReader()
THR = 0.95
ALIEN = {"date=2026-08-06", "date=2026-09-29"}
DRY = pd.read_parquet("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~171/ACCOUNT_DIM_DRY_RUN.parquet")
DRY_SCOPE = set(str(x).strip() for x in DRY["account_id"].tolist() if str(x).strip())
print("dry-run accounts in scope:", len(DRY_SCOPE))

TABLES = [("orion", "fact_assets", "accountId"), ("orion", "fact_positions", "accountId"),
          ("orion", "fact_transactions", "accountId"), ("orion", "fact_performance", None),
          ("eclipse", "fact_model_composition", None), ("eclipse", "fact_models", None),
          ("eclipse", "fact_portfolios_full", None), ("eclipse", "fact_portfolios_simple", "accountId")]

def uri(firm, t): return "s3://opal-data-assets/%s/inflection/silver/%s" % (firm, t)
def is_null(v):
    if v is None:
        return True
    if isinstance(v, float) and v != v:
        return True
    return v is pd.NA
def value_of(v):
    if is_null(v):
        return None
    s = str(v).strip()
    return s or None
def key_int(v):
    if is_null(v):
        return None
    return str(int(v))
def maxrun(s):
    return max((len(x) for x in re.findall(r"[0-9]+", s)), default=0)
def frac(n, d): return round(n / d, 6) if d else 0.0
def string_cols(df):
    out = []
    for c in df.columns:
        if str(df[c].dtype) in ("str", "object", "string"):
            if all(is_null(v) or isinstance(v, str) for v in df[c].tolist()):
                out.append(c)
    return out

def measure(shape_rows, scope, has_key, extra):
    vals = [v for _, v in shape_rows if v is not None]
    nn = len(vals)
    runs = [maxrun(v) for v in vals]
    out = dict(distinct_values=len(set(vals)), non_null_values=nn,
               share_values_digit_run_ge4=frac(sum(r >= 4 for r in runs), nn),
               share_values_digit_run_ge8=frac(sum(r >= 8 for r in runs), nn),
               share_values_all_digit=frac(sum(1 for v in vals if re.fullmatch(r"[0-9]+", v)), nn),
               share_values_alpha_only=frac(sum(1 for v in vals if re.fullmatch(r"[A-Za-z]+", v)), nn))
    acc = defaultdict(set)
    if has_key:
        for a, v in shape_rows:
            if a is not None and v is not None:
                acc[a].add(v)
    keyed = bool(has_key and nn > 0 and all(len(s) <= 1 for s in acc.values()))
    owners = Counter(v for s in acc.values() for v in s)
    with_val = [a for a in scope if a in acc]
    dr_ok = sum(1 for a in scope if a in acc and all(maxrun(v) >= 4 for v in acc[a]))
    uniq_ok = sum(1 for a in with_val if all(owners[v] == 1 for v in acc[a]))
    stable_share = 0.0
    if extra:
        union = {a: set(acc[a]) for a in with_val}
        for part in extra:
            for a, v in part:
                if a in union and v is not None:
                    union[a].add(v)
        stable_ok = sum(1 for a in with_val if len(union[a]) == 1)
        stable_share = frac(stable_ok, len(with_val))
    out.update(keyed_to_account=keyed, accounts_with_value=len(with_val),
               share_accounts_digit_run_ge4=frac(dr_ok, len(scope)),
               share_accounts_stable=stable_share,
               share_accounts_unique=frac(uniq_ok, len(with_val)),
               partitions_sampled=1 + len(extra))
    return out

def qualifies(c):
    return bool(c["keyed_to_account"] and c["partitions_sampled"] >= 2 and c["share_accounts_digit_run_ge4"] >= THR
                and c["share_accounts_stable"] >= THR and c["share_accounts_unique"] >= THR)

def pick_sample(parts, shape):
    sd = dt.date.fromisoformat(shape.split("=")[1])
    cands = []
    for p in parts:
        if p in ALIEN or p == shape:
            continue
        d = dt.date.fromisoformat(p.split("=")[1])
        if 1 <= (sd - d).days <= 120:
            cands.append(p)
    chosen = []
    for k in (30, 60, 90, 120):
        avail = [p for p in cands if p not in chosen]
        if not avail:
            break
        target = sd - dt.timedelta(days=k)
        chosen.append(min(avail, key=lambda p: abs((dt.date.fromisoformat(p.split("=")[1]) - target).days)))
    return chosen

partitions_read = set()
cands_all = []
per_table = {}
for firm, t, ak in TABLES:
    t0 = time.time()
    u = uri(firm, t)
    parts = rd.list_partitions(u)
    shape = parts[-1]
    df = rd.read_parquet(u + "/" + shape + "/data.parquet")
    partitions_read.add((firm, t, shape))
    if ak is None:
        key_fn, has_key, scope = (lambda v: None), False, (DRY_SCOPE if firm == "orion" else set())
        keys = [None] * len(df)
    else:
        has_key = True
        key_fn = key_int if firm == "orion" else value_of
        keys = [key_fn(v) for v in df[ak].tolist()]
        scope = DRY_SCOPE if firm == "orion" else set(k for k in keys if k)
    cols = string_cols(df)
    rows = {c: list(zip(keys, [value_of(v) for v in df[c].tolist()])) for c in cols}
    base = {c: measure(rows[c], scope, has_key, []) for c in cols}
    trig = [c for c in cols if has_key and (t in ("fact_positions", "fact_portfolios_simple")
            or (base[c]["share_accounts_digit_run_ge4"] >= THR and base[c]["share_accounts_unique"] >= THR))]
    extra_by_col = {c: [] for c in trig}
    sample = []
    if trig:
        sample = pick_sample(parts, shape)
        for p in sample:
            dfp = rd.read_parquet(u + "/" + p + "/data.parquet")
            partitions_read.add((firm, t, p))
            if ak in dfp.columns:
                kp = [key_fn(v) for v in dfp[ak].tolist()]
                for c in trig:
                    if c in dfp.columns:
                        extra_by_col[c].append(list(zip(kp, [value_of(v) for v in dfp[c].tolist()])))
            del dfp
    per_table[(firm, t)] = dict(shape=shape, n_parts=len(parts), n_str=len(cols),
                                n_dr4_alone=sum(1 for c in cols if base[c]["share_accounts_digit_run_ge4"] >= THR),
                                n_trig=len(trig), sample=sample, scope_n=len(scope), has_key=has_key)
    for c in cols:
        m = measure(rows[c], scope, has_key, extra_by_col.get(c, []))
        m.update(firm=firm, table=t, column=c)
        cands_all.append(m)
    print(firm, t, "shape", shape, "rows", len(df), "string cols", len(cols),
          "keyed", sum(1 for c in cols if base[c]["keyed_to_account"]),
          "dr4>=.95 (acct, shape)", sum(1 for c in cols if base[c]["share_accounts_digit_run_ge4"] >= THR),
          "stability-sampled cols", len(trig), "extra partitions", len(sample), "scope", len(scope),
          "secs", round(time.time() - t0, 1))
    del df, rows

# positive control on synthetic columns, same measure and same rule
acct = list(range(100))
num_rows = [[(a, "%08d" % ((a * 7919) % 100000000)) for a in acct] for _ in range(3)]
frag_words = ["ending", "tion", "of", "Acct", "x"]
frag_rows = [[(a, frag_words[a % 5]) for a in acct] for _ in range(3)]
pc_num = measure(num_rows[0], set(acct), True, num_rows[1:])
pc_frag = measure(frag_rows[0], set(acct), True, frag_rows[1:])
pc = dict(number=pc_num, fragment=pc_frag, number_q=qualifies(pc_num), fragment_q=qualifies(pc_frag))
print("positive control: number qualifies", pc["number_q"], "fragment qualifies", pc["fragment_q"])

for c in cands_all:
    c["qualifies"] = qualifies(c)
out = dict(candidates=cands_all, per_table={"%s.%s" % k: v for k, v in per_table.items()}, positive_control=pc,
           partitions_read=sorted("%s.%s.%s" % x for x in partitions_read), accounts_in_dry_run=len(DRY_SCOPE),
           reads_this_run=rd.reads)
with open(PRIV + "/measure_r111.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("candidates", len(cands_all), "qualifying", sum(1 for c in cands_all if c["qualifies"]),
      "partitions_read", len(partitions_read), "reads this run", rd.reads)
for c in cands_all:
    if c["qualifies"] or c["share_accounts_digit_run_ge4"] >= THR or c["keyed_to_account"]:
        print("  flag", c["firm"], c["table"], c["column"], "keyed", c["keyed_to_account"],
              "dr4", c["share_accounts_digit_run_ge4"], "stable", c["share_accounts_stable"],
              "uniq", c["share_accounts_unique"], "parts", c["partitions_sampled"], "Q", c["qualifies"])
