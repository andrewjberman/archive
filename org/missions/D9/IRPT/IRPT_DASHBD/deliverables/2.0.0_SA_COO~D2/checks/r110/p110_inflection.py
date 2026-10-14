"""IRPT_DASHBD round 110, the Inflection chain (issuer 2.0.0_SA_COO~D2) -- the CVO's four-line remedy of the first Inflection render (ADJUDICATION_v69, DB109-2-J1 FAIL)
and the CTO's round-110 analysis (@e0c72e187d): one chain, three orders, one worker slot (~175).

  DB-b-217  the CONTRACT 0.5.0: an equivalence map (members that name the same quantity for the same entity) and the household return sourced from Orion's client grain
            for Inflection only (the CTO's ruling, round 110 row 3).                                                                               DB110-1-AC1
  DB-b-222  the Inflection SAMPLE v3: each account's own first-data date and window statuses, a per-account since-inception benchmark, the gain/loss Ending Value filled,
            the household return from Orion's client grain with its source, the custodian number's real last four as the label.                      DB110-2-AC1
  DB-b-223  the RENDER of that sample: not-spanned words, one reason per cell, the gain/loss Ending Value printed, the real last four after "ending"; every page read.
                                                                                                                                                   DB110-3-AC1 (+ J1, the CVO's)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers on synthetic arms and on round 109's render (the known defects must be found)
"""
import hashlib
import importlib.util
import inspect
import json
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P9 = load_mod("p109", "r109/p109_round109.py")
P7, P6, P5, P3, P = P9.P7, P9.P6, P9.P5, P9.P3, P9.P
need, nes, is_int, sha = P.need, P.nes, P.is_int, P.sha
D, PRIV, Fail = P.D, P.PRIV, P.Fail
accounts_of, whole_document_scan = P6.accounts_of, P6.whole_document_scan
WINDOWS = ("qtd", "ytd", "last_12_months", "since_inception")
CONTRACT_REL = P5.CONTRACT_REL
SAMPLE_DIR10 = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~175/"
OUT_R10 = PRIV + "fwd21_sample_r110/"
CACHE = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~174/work/positions_daily_cache.parquet"
W175 = D + "0.9.0_WK_IRPT_DASHBD~175/"
REQ_HH = ("pvs.qtd.ending_value", "pvs.ytd.ending_value", "pvs.last_12_months.ending_value", "pvs.since_inception.ending_value", "hold.ending_value", "act.ending_value.household")
REQ_ACC = ("avs.qtd.ending_value", "avs.ytd.ending_value", "avs.last_12_months.ending_value", "avs.since_inception.ending_value", "glr.ending_value", "act.ending_value.account")
EQ_KEYS = {"id", "meaning", "entity", "members"}
SRC_KEYS = {"input", "grain", "table", "field", "fold", "claim"}
# DB104-2-AC1 and DB104-3-AC1 pin the contract at 0.4.1 and have read FAIL since the 0.4.2 bump (superseded, not a regression)
OLDER = ("DB104-1-AC1", "DB104-4-AC1", "DB104-5-AC1", "DB105-1-AC1", "DB105-2-AC1", "DB105-3-AC1", "DB106-1-AC1", "DB106-2-AC1",
         "DB107-1-AC1", "DB108-1-AC1", "DB108-2-AC1", "DB109-1-AC1", "DB109-2-AC1", "DB109-3-AC1")
NEEDS_MORE = "needs more history"


# ---------------------------------------------------------------- pure helpers
def state_of(x):
    """absent | num | other, for one figure."""
    if P5.has_absent_key(x):
        return "absent"
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return "num"
    return "other"


def member_state(values, mid, entity):
    """the state and value of member mid for an entity: a household grain member holds its figure directly, an account grain member holds it in by_row[entity]."""
    v = values[mid]
    if isinstance(v, dict) and "by_row" in v:
        x = v["by_row"].get(entity)
        return state_of(x), x
    return state_of(v), v


def equivalence_conflicts(values, contract, account_ids):
    """THE EQUIVALENCE RULE: members of one class, for one entity, are all filled or all absent, and two filled values agree to within 0.01."""
    out = []
    for cl in contract.get("equivalences") or []:
        ents = ["household"] if cl["entity"] == "household" else list(account_ids)
        for e in ents:
            seen = [(m,) + member_state(values, m, e) for m in cl["members"]]
            states = {s for _m, s, _x in seen}
            if len(states) > 1:
                out.append("%s %s: %s" % (cl["id"], e if e == "household" else "an account", ", ".join("%s is %s" % (m, s) for m, s, _x in seen)))
                continue
            nums = [x for _m, s, x in seen if s == "num"]
            if nums and max(nums) - min(nums) > 0.01:
                out.append("%s %s: the members are filled and differ" % (cl["id"], e if e == "household" else "an account"))
    return out


def plant_equivalence_conflict(values, contract, account_ids):
    """a copy with ONE member of the first account class absent while its equivalents hold figures."""
    v = json.loads(json.dumps(values))
    cl = next(c for c in contract["equivalences"] if c["entity"] == "account")
    mid = cl["members"][0]
    x = v[mid]
    key = account_ids[0]
    if isinstance(x, dict) and "by_row" in x:
        x["by_row"][key] = {"absent": "planted by the checker", "kind": "NO_SOURCE_YET"}
    else:
        v[mid] = {"absent": "planted by the checker", "kind": "NO_SOURCE_YET"}
    return v


def synthetic_values(contract, account_ids):
    """every member of every class filled with 1.0 (account grain members as by_row maps), for the contract-level control."""
    v = {}
    for cl in contract.get("equivalences") or []:
        for m in cl["members"]:
            v[m] = {"by_row": {a: 1.0 for a in account_ids}} if cl["entity"] == "account" else 1.0
    return v


def months_back(d, n):
    y, m = d.year, d.month - n
    while m <= 0:
        y, m = y - 1, m + 12
    return date(y, m, min(d.day, 28))


def window_start(asof, w):
    """the calendar start day of a window other than since_inception (the contract's start_rule)."""
    if w == "qtd":
        return date(asof.year, 3 * ((asof.month - 1) // 3) + 1, 1)
    if w == "ytd":
        return date(asof.year, 1, 1)
    return months_back(asof, 12)


def first_dates():
    """account id -> the first date the account has a positions row, from the round-109 positions cache (counts the checker needs, never printed)."""
    import pyarrow.parquet as pq
    t = pq.read_table(CACHE, columns=["acc", "date", "n_rows"]).to_pylist()
    out = {}
    for r in t:
        if r["n_rows"] and r["n_rows"] > 0:
            a, d = str(r["acc"]), str(r["date"])
            if a not in out or d < out[a]:
                out[a] = d
    return out


def iso(s):
    return date.fromisoformat(str(s))


# ---------------------------------------------------------------- DB110-1-AC1 (the contract 0.5.0)
def check_contract(root):
    c = P.contract(root)
    ver = tuple(int(x) for x in str(c.get("contract_version") or "0.0.0").split("."))
    need(ver >= (0, 5, 0), "the contract must be version 0.5.0 or later (it reads %s)" % ".".join(str(x) for x in ver))
    members = {m["id"]: m for m in c["members"]}
    eq = c.get("equivalences")
    need(isinstance(eq, list) and len(eq) >= 2, "the contract must carry an `equivalences` list of at least 2 classes")
    seen = {}
    for cl in eq:
        need(isinstance(cl, dict) and set(cl.keys()) == EQ_KEYS, "an equivalence class has exactly the keys %s" % sorted(EQ_KEYS))
        need(cl["entity"] in ("household", "account") and nes(cl["id"]) and nes(cl["meaning"]), "a class names its id, its meaning and an entity of household or account")
        need(isinstance(cl["members"], list) and len(cl["members"]) >= 2 and all(m in members for m in cl["members"]), "class %s: at least 2 members, each a contract member" % cl["id"])
        need(len({members[m]["unit"] for m in cl["members"]}) == 1, "class %s: the members share one unit (same grain)" % cl["id"])
        for m in cl["members"]:
            need(m not in seen, "member %s is in two classes (%s and %s): the classes must not overlap" % (m, seen.get(m), cl["id"]))
            seen[m] = cl["id"]
    hh = [cl for cl in eq if cl["entity"] == "household" and set(REQ_HH) <= set(cl["members"])]
    ac = [cl for cl in eq if cl["entity"] == "account" and set(REQ_ACC) <= set(cl["members"])]
    need(len(hh) == 1 and len(ac) == 1, "one household class must hold the six household ending-value members and one account class the six account ending-value members (%d and %d found)" % (len(hh), len(ac)))
    # the household return: sourced from Orion's client grain for Inflection only; every other firm stays ABSENT
    sourced, absent = [], []
    for w in WINDOWS:
        m = members["pvs.%s.return_cumulative" % w]
        need(m["source"] == "ABSENT", "pvs.%s.return_cumulative stays ABSENT for every other firm (source ABSENT)" % w)
        fs, fa = (m.get("firm_sources") or {}), (m.get("firm_absent") or {})
        need(set(fs.keys()) <= {"inflection"} and set(fa.keys()) <= {"inflection"}, "pvs.%s.return_cumulative: firm_sources and firm_absent name inflection only" % w)
        need((("inflection" in fs) + ("inflection" in fa)) == 1, "pvs.%s.return_cumulative: Inflection is either sourced (firm_sources) or absent with a reason (firm_absent), exactly one" % w)
        if "inflection" in fs:
            s = fs["inflection"]
            need(isinstance(s, dict) and SRC_KEYS <= set(s.keys()) and all(nes(s[k]) for k in SRC_KEYS), "pvs.%s.return_cumulative firm_sources.inflection must carry %s, each in words" % (w, sorted(SRC_KEYS)))
            need(s["grain"] == "client" and "orion/inflection/silver/fact_performance" in s["table"], "the Inflection household return is Orion's CLIENT-grain fact_performance under orion/inflection/silver (grain %r, table %r)" % (s["grain"], s["table"]))
            need("opal" not in s["claim"].lower() or "reported" in s["claim"].lower(), "the claim must say the figure is reported by the platform at client grain (not Opal-computed)")
            sourced.append(w)
        else:
            need(nes(fa["inflection"]), "pvs.%s.return_cumulative firm_absent.inflection must hold the reason in words" % w)
            absent.append(w)
    need(len(sourced) >= 1, "at least one household return window must be sourced for Inflection from Orion's client grain")
    # the holdings overview repeats the household return: hold.return_<window> carries the same firm source as pvs.<window>.return_cumulative and is its equivalent
    for w in WINDOWS:
        pv, hd = members["pvs.%s.return_cumulative" % w], members["hold.return_%s" % w]
        need(hd["source"] == "ABSENT" and (hd.get("firm_sources") or {}) == (pv.get("firm_sources") or {}) and (hd.get("firm_absent") or {}) == (pv.get("firm_absent") or {}),
             "hold.return_%s must keep source ABSENT and carry exactly the firm_sources and firm_absent of pvs.%s.return_cumulative (the holdings table prints the same household return)" % (w, w))
        need(any(cl["entity"] == "household" and {"pvs.%s.return_cumulative" % w, "hold.return_%s" % w} <= set(cl["members"]) for cl in eq), "an equivalence class of entity household must hold pvs.%s.return_cumulative and hold.return_%s" % (w, w))
    # the control: the equivalence rule reports a planted conflict and is quiet on a consistent set
    accs = ["a1", "a2"]
    sv = synthetic_values(c, accs)
    need(equivalence_conflicts(sv, c, accs) == [], "the equivalence rule reports a conflict on a consistent synthetic set")
    need(len(equivalence_conflicts(plant_equivalence_conflict(sv, c, accs), c, accs)) >= 1, "CONTROL: the equivalence rule is blind to a planted pair (one member absent, its equivalents printed)")
    # the record
    r = P.load(root, W175 + "CONTRACT_R110.json")
    need(r.get("contract_version") == c["contract_version"] and r.get("contract_sha256") == sha(root / CONTRACT_REL), "the record's contract_version and contract_sha256 must equal the contract at HEAD")
    need(r.get("equivalence_classes") == len(eq) and r.get("household_windows_sourced") == sourced and r.get("household_windows_absent") == absent, "the record's counts must equal the contract's: classes %d, sourced %s, absent %s" % (len(eq), sourced, absent))
    oc = r.get("older_criteria")
    need(isinstance(oc, dict) and sorted(oc.keys()) == sorted(OLDER) and all(v == "PASS" for v in oc.values()), "older_criteria must list each of the %d earlier live criteria with PASS (a contract change must not turn an earlier PASS into a FAIL)" % len(OLDER))
    need(not P.long_digit_runs(r), "the record holds a run of 8 or more digits")
    # this checker re-runs the two earlier criteria that read the contract bytes most directly
    for cid, rel in (("DB105-1-AC1", "r105/p105_round105.py"), ("DB109-1-AC1", "r109/p109_round109.py")):
        g = subprocess.run([sys.executable, "-I", str(HERE.parent / rel), str(root), cid], capture_output=True, text=True, timeout=100)
        need(g.returncode == 0 and (cid + " PASS") in g.stdout, "the earlier criterion %s no longer passes with the new contract: %s" % (cid, (g.stdout.strip().splitlines() or ["no output"])[-1][:200]))
    print("OK: contract %s: %d equivalence classes (no overlap, one unit each), the planted pair is reported; household return sourced from Orion's client grain for Inflection in %d window(s), absent with a reason in %d; every other firm stays ABSENT; earlier criteria still PASS"
          % (c["contract_version"], len(eq), len(sourced), len(absent)))


# ---------------------------------------------------------------- DB110-2-AC1 (the Inflection sample v3)
def check_sample(root):
    r = P.load(root, W175 + "BUILD_R110.json")
    c = P.contract(root)
    ver = tuple(int(x) for x in str(c.get("contract_version") or "0.0.0").split("."))
    need(ver >= (0, 5, 0), "the contract must be 0.5.0 or later")
    s = r.get("sample") or {}
    sp = str(s.get("path") or "").replace("\\", "/")
    need(sp.startswith(SAMPLE_DIR10) and sp.endswith("HOUSEHOLD_SAMPLE.json") and Path(sp).is_file(), "sample.path must be the private HOUSEHOLD_SAMPLE.json under %s" % SAMPLE_DIR10)
    need(not sp.startswith(str(root.resolve()).replace("\\", "/").rstrip("/") + "/"), "the sample is inside the repo: client data never goes there")
    need(s.get("sha256") == sha(sp) and s.get("contract_sha256") == sha(root / CONTRACT_REL), "sample.sha256 and sample.contract_sha256 must equal the sample bytes and the contract bytes")
    sm = P.sample_json(sp)
    P5.check_sample_shape_k(sm, c, "inflection")
    prob = P5.kind_problems(sm["values"], c, "inflection")
    need(not prob, "kind carrier: %s" % "; ".join(prob[:3]))
    acc = accounts_of(sm)
    vals = sm["values"]
    conf, dis, st = whole_document_scan(vals, acc)
    need(st["unmapped"] == 0 and not conf and not dis, "whole-document rule: unmapped %d, %s" % (st["unmapped"], "; ".join((conf + dis)[:3])))
    need(r.get("whole_document") == {"cells_scanned": st["cells_scanned"], "absent_cells": st["absent_cells"], "keys": st["keys"], "unmapped": 0, "conflicts": 0}, "whole_document must equal the checker's own denominator %s with unmapped 0 and conflicts 0" % st)
    pc, _pd, _ps = whole_document_scan(P6.plant_conflict(vals, acc), acc)
    need(len(pc) >= 1, "CONTROL: the whole-document rule is blind to a planted conflict")
    ec = equivalence_conflicts(vals, c, acc)
    need(not ec, "equivalence rule: %s" % "; ".join(ec[:3]))
    need(len(equivalence_conflicts(plant_equivalence_conflict(vals, c, acc), c, acc)) >= 1, "CONTROL: the equivalence rule is blind to a planted pair in the sample")
    need(r.get("equivalence") == {"classes": len(c["equivalences"]), "conflicts": 0}, "equivalence must be {classes %d, conflicts 0}" % len(c["equivalences"]))
    # the household: the deterministic rule, as for round 109
    import pyarrow.parquet as pq
    need(Path(P9.DIM_DRY).is_file(), "the private account_dim dry run of round 108 is missing")
    h, accts = P9.pick_household(pq.read_table(P9.DIM_DRY).to_pylist())
    need(h is not None and r.get("household_ref_sha256") == hashlib.sha256(h.encode("utf-8")).hexdigest() and sorted(acc) == sorted(accts), "the sample is the hash-rule household's accounts (%d expected)" % len(accts))
    # the account's own first-data date, from the positions cache, and the window statuses it implies
    asof = iso(sm["household"]["as_of"])
    fd = first_dates()
    need(Path(CACHE).is_file(), "the round-109 positions cache is missing")
    for a in sm["household"]["accounts"]:
        need(a["account_id"] in fd and a["first_data_date"] == fd[a["account_id"]], "an account's first_data_date must be the first date it has positions rows (the checker reads the positions cache): %d of %d accounts agree" % (sum(1 for x in sm["household"]["accounts"] if fd.get(x["account_id"]) == x["first_data_date"]), len(acc)))
    need(sm["household"]["first_data_date"] == min(a["first_data_date"] for a in sm["household"]["accounts"]), "the household first_data_date is the earliest of its accounts'")
    hh0 = iso(sm["household"]["first_data_date"])
    n_ns = 0
    for a in sm["household"]["accounts"]:
        f0 = iso(a["first_data_date"])
        for w in ("qtd", "ytd", "last_12_months"):
            ws = window_start(asof, w)
            st_w = a["window_status"][w]
            if f0 > ws + timedelta(days=7):
                need(st_w == "NOT_SPANNED", "an account whose first data (after the window start) must read NOT_SPANNED for %s, got %s" % (w, st_w))
                n_ns += 1
                for mid in [m["id"] for m in c["members"] if m["id"].startswith("avs.%s.benchmark_" % w)]:
                    x = vals[mid]["by_row"][a["account_id"]]
                    need(P5.is_absent_k(x) and x["kind"] == "INSUFFICIENT_HISTORY" and NEEDS_MORE not in x["absent"].lower(), "%s: a window the account did not span carries INSUFFICIENT_HISTORY in the not-spanned words, never 'needs more history' (kind %s)" % (mid, x.get("kind") if isinstance(x, dict) else x))
            elif f0 <= ws - timedelta(days=7):
                need(st_w != "NOT_SPANNED", "an account with data before the %s window start must not read NOT_SPANNED" % w)
        # since inception: the account's own window; never the household's figures
        for mid in [m["id"] for m in c["members"] if m["id"].startswith("avs.since_inception.benchmark_")]:
            x = vals[mid]["by_row"][a["account_id"]]
            hv = vals[mid.replace("avs.", "pvs.", 1)]
            if state_of(x) == "num" and state_of(hv) == "num":
                if f0 > hh0 + timedelta(days=30):
                    need(abs(x - hv) > 0.05, "%s: an account that opened after the household's inception must not carry the household's since-inception benchmark figure" % mid)
                elif f0 == hh0:
                    need(abs(x - hv) <= 0.05, "%s: an account that opens on the household's inception date must carry the same benchmark figure" % mid)
    need(r.get("not_spanned_account_windows") == n_ns, "not_spanned_account_windows must equal the checker's count %d" % n_ns)
    # Ending Value filled from the member the overview prints
    for a in acc:
        x = vals["glr.ending_value"]["by_row"][a]
        need(state_of(x) == "num", "glr.ending_value must be filled for every account (the overview prints it)")
    # lots stay words; account returns stay words; the household return is filled where the contract sources it
    for mid in [m["id"] for m in c["members"] if m["id"].startswith(("trgl.", "glr.")) and m["id"] != "glr.ending_value"]:
        v = vals[mid]
        leaves = list(v["by_row"].values()) if isinstance(v, dict) and "by_row" in v else [v]
        need(all(P5.is_absent_k(x) and x["kind"] == "NO_SOURCE_YET" and x["absent"].startswith(P9.LOTS_WORDS) for x in leaves), "%s: a lot member reads NO_SOURCE_YET with the words %r" % (mid, P9.LOTS_WORDS))
    for w in WINDOWS:
        v = vals["avs.%s.return_cumulative" % w]
        leaves = list(v["by_row"].values()) if isinstance(v, dict) and "by_row" in v else [v]
        need(all(P5.is_absent_k(x) and x["kind"] == "NO_SOURCE_YET" and x["absent"] == P9.ACCT_WORDS for x in leaves), "avs.%s.return_cumulative: account returns stay NO_SOURCE_YET with the words %r" % (w, P9.ACCT_WORDS))
    members = {m["id"]: m for m in c["members"]}
    sourced = [w for w in WINDOWS if "inflection" in (members["pvs.%s.return_cumulative" % w].get("firm_sources") or {})]
    filled, nohist = [], []
    for w in WINDOWS:
        x = vals["pvs.%s.return_cumulative" % w]
        if w in sourced:
            if state_of(x) == "num":
                need(abs(x) < 500, "pvs.%s.return_cumulative: Orion's client-grain figure fills it as percent points" % w)
                filled.append(w)
            else:
                need(P5.is_absent_k(x) and x["kind"] == "INSUFFICIENT_HISTORY", "pvs.%s.return_cumulative: a sourced window whose opening day has no factor row is absent with kind INSUFFICIENT_HISTORY" % w)
                nohist.append(w)
        else:
            need(P5.is_absent_k(x) and x["kind"] == "NO_SOURCE_YET", "pvs.%s.return_cumulative: a window Orion does not carry stays NO_SOURCE_YET" % w)
    need(len(filled) >= 1, "at least one household return window must be filled from Orion's client grain")
    hs = r.get("household_return_source") or {}
    need(hs.get("windows") == filled and hs.get("windows_without_history") == nohist and nes(hs.get("claim")) and "client" in hs.get("claim", "").lower() and hs.get("newest_partition_only") is True and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(hs.get("partition_date") or "")),
         "household_return_source must be {windows %s, windows_without_history %s, claim (client grain), newest_partition_only true, partition_date ISO}" % (filled, nohist))
    # the label: the custodian number's real last four characters, never an ordinal
    l4 = [str(a["last4"]) for a in sm["household"]["accounts"]]
    need(all(re.fullmatch(r"[0-9A-Za-z]{4}", x) for x in l4), "each account's last4 is four letters or digits (the last four alphanumeric characters of the custodian number)")
    coll = sum(1 for x in l4 if l4.count(x) > 1)
    need(r.get("last4_collisions") == coll, "last4_collisions must equal the number of accounts that share a last4 with another account of the household (the checker counts %d)" % coll)
    need(all(x != "%04d" % (i + 1) for i, x in enumerate(l4)), "last4 must be the custodian number's real last four characters, never the ordinal 0001, 0002, ...")
    need(nes(r.get("last4_source")) and "custodian" in r["last4_source"].lower(), "last4_source must say in words that the label is the custodian number's last four characters as stored")
    need(r.get("as_of") == sm["household"]["as_of"] and iso(r["as_of"]) <= iso(r.get("benchmark_data_as_of") or "1900-01-01"), "as_of must equal the sample's and not be later than benchmark_data_as_of")
    n_f, tot_f = P6.members_filled(vals, c)
    need(r.get("benchmark_members") == {"total": 32, "filled": n_f} and tot_f == 32, "benchmark_members must equal the checker's count {total 32, filled %d}" % n_f)
    ar = json.loads((root / P9.ALIEN_REC).read_bytes().decode("utf-8"))
    need(r.get("orion_guard") == ar["result"]["guard_state_for_render_record"], "orion_guard must equal the issuer's read-gate state")
    b = r.get("builder") or {}
    bf = str(b.get("file") or "")
    need(bf == W175 + "build_sample_inflection_r110.py" and (root / bf).is_file() and b.get("sha256") == sha(root / bf) and b.get("tracked") is True, "builder: the tracked build_sample_inflection_r110.py in the worker's folder, hashed as recorded")
    src = (root / bf).read_text(encoding="utf-8")
    need("inflection_account_dim" in src and not P9.P8.foreign_hits(src) and not P9.P8.write_hits(src), "the builder uses the Inflection adapter, names no other firm's place and holds no write call")
    rd = r.get("reads") or {}
    need(rd.get("vendor_calls") == 0 and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0 and rd.get("secret_reads") == 0 and is_int(rd.get("s3_reads")), "reads: zero writes, vendor calls and secret reads; s3_reads an integer")
    need(r.get("files_in_repo") is False and r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False, "files_in_repo, served_values_changed, pushed and deployed must be false")
    need(not P.long_digit_runs({k: v for k, v in r.items() if k != "sample"}), "the record holds a run of 8 or more digits")
    print("OK: Inflection sample v3 (%d accounts): each account's own first-data date (%d not-spanned account windows, benchmark in the not-spanned words), since-inception benchmark per account, gain/loss Ending Value filled, equivalence rule 0 conflicts (planted pair caught), household return from Orion's client grain in %d window(s), labels are real last fours"
          % (len(acc), n_ns, len(filled)))


# ---------------------------------------------------------------- DB110-3-AC1 (the render)
def cell_texts(html):
    """(member, entity, text) for every data-member element that carries a data-entity: the text up to the element's close."""
    out = []
    for m in P7.CELL_RE.finditer(html):
        if "data-note=" in m.group(2):
            continue
        ent = P7.attr(m.group(2), "data-entity")
        close = html.find("</%s>" % m.group(1), m.end())
        out.append((m.group(3), ent, P3.visible_text(html[m.end():close if close > 0 else m.end() + 400]).strip()))
    return out


def render_extras(html, sm, is_export):
    """the round-110 clauses on one HTML: (1) the gain/loss Ending Value prints a figure for every account; (2) no note says 'needs more history' for an account and window that is not spanned;
    (3) one reason per cell: a key named by two absent notes with different words fails; (4) every 'ending XXXX' label is an account's real last four."""
    fails = []
    acc = {a["account_id"]: a for a in sm["household"]["accounts"]}
    gl = {e: t for m, e, t in cell_texts(html) if m == "glr.ending_value" and e}
    for a in acc:
        t = gl.get(a)
        if t is None or "not available" in t.lower() or not re.search(r"\$\s*[\d,]+", t):
            fails.append("the gain/loss Ending Value of an account does not print a figure (%s)" % ("no cell" if t is None else "reads %r" % t[:40]))
    notes = [n for n in P7.parse_notes(html) if n["kind"] == "absent"]
    by_key = {}
    for n in notes:
        for mem, ent in n["keys"]:
            by_key.setdefault((mem, ent), set()).add(re.sub(r"\s+", " ", n["text"]).strip().lower())
            m = re.match(r"avs\.(qtd|ytd|last_12_months)\.", mem)
            a = acc.get(ent)
            if m and a and a["window_status"][m.group(1)] == "NOT_SPANNED" and NEEDS_MORE in n["text"].lower():
                fails.append("a note says 'needs more history' for an account window that is not spanned (%s)" % m.group(1))
    two = sorted(k for k, v in by_key.items() if len(v) > 1)
    if two:
        fails.append("%d cell(s) carry two different reasons in two notes (first: %s|%s)" % (len(two), two[0][0], "an account" if two[0][1] in acc else two[0][1]))
    last4 = {a["last4"] for a in acc.values()}
    printed = set(re.findall(r"\bending\s+([0-9A-Za-z]{4})\b", P3.visible_text(html)))
    if not printed or not printed <= last4:
        fails.append("an 'ending XXXX' label is not an account's last four (%d printed, %d not an account's)" % (len(printed), len(printed - last4)))
    l4s = [a["last4"] for a in acc.values()]
    for dup in sorted({x for x in l4s if l4s.count(x) > 1}):
        if not re.search(r"ending\s+%s\s*\(\d+ of \d+\)" % re.escape(dup), P3.visible_text(html)):
            fails.append("two accounts of the household share a last four and the label carries no '(k of n)' to tell them apart")
    return fails


def extra_inflection10(root, r, k, vals, tab, exp):
    P9.extra_inflection(root, r, k, vals, tab, exp)
    sm = P.sample_json(str((k.get("sample") or {}).get("path") or ""))
    for name, text, ex in (("tab_html", tab, False), ("export_html", exp, True)):
        f = render_extras(text, sm, ex)
        need(not f, "%s: %s" % (name, "; ".join(f[:3])))


def build_check_render():
    src = inspect.getsource(P9.check_render)
    for a, b in (("0.9.0_WK_IRPT_DASHBD~173/RENDER_R109.json", "0.9.0_WK_IRPT_DASHBD~175/RENDER_R110.json"),
                 ("0.9.0_WK_IRPT_DASHBD~173/BUILD_R109.json", "0.9.0_WK_IRPT_DASHBD~175/BUILD_R110.json"),
                 ("wk-IRPT_DASHBD-173-portal", "wk-IRPT_DASHBD-175-portal"),
                 ("extra_inflection(root, r, k, vals, tab, exp)", "extra_inflection10(root, r, k, vals, tab, exp)"),
                 ("OUT_R9", "OUT_R10")):
        need(a in src, "check_render generation: %r not in the round-109 source" % a)
        src = src.replace(a, b)
    ns = dict(vars(P9))
    ns.update(OUT_R10=OUT_R10, extra_inflection10=extra_inflection10)
    exec(compile(src, "p110_check_render", "exec"), ns)
    return ns["check_render"]


def check_render(root):
    build_check_render()(root)


# ---------------------------------------------------------------- self-test
def selftest(root):
    c = P.contract(root)
    arms = []

    def arm(name, ok):
        arms.append(name)
        if not ok:
            raise Fail("self-test arm failed: " + name)
    accs = ["a1", "a2"]
    cc = dict(c)
    cc["equivalences"] = [{"id": "E_ACC", "meaning": "x", "entity": "account", "members": list(REQ_ACC)}, {"id": "E_HH", "meaning": "y", "entity": "household", "members": list(REQ_HH)}]
    sv = synthetic_values(cc, accs)
    arm("equivalence quiet on a consistent set", equivalence_conflicts(sv, cc, accs) == [])
    arm("equivalence reports a planted absent twin", len(equivalence_conflicts(plant_equivalence_conflict(sv, cc, accs), cc, accs)) == 1)
    sv2 = json.loads(json.dumps(sv))
    sv2["glr.ending_value"]["by_row"]["a1"] = 2.5
    arm("equivalence reports two filled values that differ", len(equivalence_conflicts(sv2, cc, accs)) == 1)
    arm("window start qtd", window_start(date(2026, 10, 13), "qtd") == date(2026, 10, 1))
    arm("window start ytd", window_start(date(2026, 10, 13), "ytd") == date(2026, 1, 1))
    arm("window start last 12 months", window_start(date(2026, 10, 13), "last_12_months") == date(2025, 10, 13))
    html_bad = ('<p data-note="absent" data-note-keys="avs.ytd.benchmark_long_term|1111">needs more history than is available yet.</p>'
                '<p data-note="absent" data-note-keys="avs.ytd.benchmark_long_term|1111">Not held for the whole period.</p>'
                '<td data-member="glr.ending_value" data-entity="1111">Not available yet</td>')
    sm = {"household": {"accounts": [{"account_id": "1111", "last4": "AB12", "first_data_date": "2026-06-15", "window_status": {"qtd": "MEASURED", "ytd": "NOT_SPANNED", "last_12_months": "NOT_SPANNED", "since_inception": "MEASURED"}}]}}
    f = render_extras(html_bad, sm, True)
    arm("render extras find the three defects (ending value, false reason, two reasons) and the missing label", len(f) == 4)
    html_ok = ('<p data-note="absent" data-note-keys="avs.ytd.benchmark_long_term|1111">Not held for the whole period.</p>'
               '<td data-member="glr.ending_value" data-entity="1111">$1,000</td><h2>Account ending AB12</h2>')
    arm("render extras are quiet on a clean render", render_extras(html_ok, sm, True) == [])
    sm2 = json.loads(json.dumps(sm))
    sm2["household"]["accounts"].append(dict(sm["household"]["accounts"][0], account_id="2222"))
    html_dup = html_ok + '<td data-member="glr.ending_value" data-entity="2222">$5</td>'
    arm("a shared last four needs a (k of n) label", len(render_extras(html_dup, sm2, True)) == 1 and render_extras(html_dup.replace("Account ending AB12", "Account ending AB12 (1 of 2)"), sm2, True) == [])
    # round 109's own render carries the CVO's counts 2 to 4: the extras must find them
    rj = root / (D + "0.9.0_WK_IRPT_DASHBD~173/RENDER_R109.json")
    if rj.is_file():
        rec = json.loads(rj.read_bytes().decode("utf-8"))
        kj = json.loads((root / (D + "0.9.0_WK_IRPT_DASHBD~173/BUILD_R109.json")).read_bytes().decode("utf-8"))
        smp = P.sample_json(kj["sample"]["path"])
        exp = Path(P.private_file(root, rec["outputs"].get("export_html"), P9.OUT_R9, ".html", "export_html")).read_text(encoding="utf-8")
        f = render_extras(exp, smp, True)
        arm("round 109's render (the CVO read it) is found defective by the extras", any("Ending Value" in x for x in f) and any("two different reasons" in x or "needs more history" in x for x in f))
    print("SELFTEST OK: %d arms: %s" % (len(arms), "; ".join(arms)))


CHECKS = {"DB110-1-AC1": check_contract, "DB110-2-AC1": check_sample, "DB110-3-AC1": check_render}


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        selftest(Path(argv[2] if len(argv) > 2 else ".").resolve())
        return 0
    if len(argv) != 3 or argv[2] not in CHECKS:
        print("usage: p110_inflection.py <repo_root> <%s>" % "|".join(CHECKS))
        return 2
    root, cid = Path(argv[1]).resolve(), argv[2]
    try:
        CHECKS[cid](root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % cid)
        return 1
    except Exception as e:
        print("FAIL: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        return 1
    print("%s PASS" % cid)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
