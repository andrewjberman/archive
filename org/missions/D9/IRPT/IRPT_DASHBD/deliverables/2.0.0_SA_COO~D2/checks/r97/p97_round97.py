"""IRPT_DASHBD round 97 (issuer 2.0.0_SA_COO~D2) -- reconcile the filled-report shape (row IRPT_DASHBD-D2-W146-S1).

Cell DB-b-182 (~148, LOCAL; S3 GET/LIST only, zero vendor calls, no served byte moves): the contract's `document` layout did not say how a filled report keys its accounts and its per-account
values, so the sample builder (~141) and the components (~142) each read it their own way and the real sample could not be rendered. The components' input type (`FilledReport` in
portal/src/pages/InvestorReporting/dashboard/report/reportModel.ts) is the tested reading; the contract now states it, and the builder emits it.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB97-1-AC1  contract 0.3.0 with `document.filled_report` stating the shape and the lineage of 0.1.0 and 0.2.0; the private sample conforms (top-level keys, household keys, account entries,
              window statuses, by_row wrappers, no unwrapped per-row map, no zero for a contract-ABSENT member); ~148/SAMPLE_ALIGN.json binds the sample, the builder and the regenerated build
              record; and round 94's DB94-2-AC1 still passes on the regenerated build record.
"""
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
D = PROJ + "deliverables/"
CONTRACT = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
SAMPLE = os.environ.get("IRPT_P97_SAMPLE", "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~141/HOUSEHOLD_SAMPLE.json")
V010 = "53fce40546882c90b634decb91ec5176a54ddf3c3b4622270bfc5cc35f66991b"
V020 = "1c5cf7ba7abff38d0ce887cc83200873f3edd9778171355621d830e515c54cd7"  # the 0.2.0 contract bytes (round 95, @853eeebbb2)
WINDOWS = ("qtd", "ytd", "last_12_months", "since_inception")
STATUSES = ("MEASURED", "NOT_SPANNED", "BREAK")
RUN = re.compile(r"\d{8,}")
HEX64 = re.compile(r"[0-9a-f]{64}")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256") and str(k) not in ("commit", "path"):
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def is_absent(v):
    return isinstance(v, dict) and set(v.keys()) == {"absent"} and isinstance(v["absent"], str) and v["absent"].strip() != ""


def is_figure(v):
    return is_absent(v) or (isinstance(v, (int, float)) and not isinstance(v, bool)) or isinstance(v, str)


def check_sample_shape(sample, contract):
    need(isinstance(sample, dict) and set(sample.keys()) == {"household", "values"}, "the sample's top-level keys must be exactly household and values, got %s" % (sorted(sample.keys()) if isinstance(sample, dict) else type(sample).__name__))
    h = sample["household"]
    need(isinstance(h, dict) and set(h.keys()) == {"household_ref", "as_of", "first_data_date", "accounts"}, "household keys %r" % (sorted(h.keys()) if isinstance(h, dict) else h))
    need(ISO.fullmatch(str(h["as_of"])) and ISO.fullmatch(str(h["first_data_date"])), "household as_of and first_data_date must be ISO dates")
    accs = h["accounts"]
    need(isinstance(accs, list) and len(accs) >= 2, "household.accounts must list 2 or more accounts")
    ids = []
    for a in accs:
        need(isinstance(a, dict) and set(a.keys()) == {"account_id", "last4", "first_data_date", "window_status"}, "an account entry's keys must be account_id, last4, first_data_date, window_status, got %r" % (sorted(a.keys()) if isinstance(a, dict) else a))
        need(re.fullmatch(r"\d{10}", str(a["account_id"])) and re.fullmatch(r"[0-9A-Za-z]{4}", str(a["last4"])) and ISO.fullmatch(str(a["first_data_date"])), "account entry %r has a malformed id, last4 or date" % a["last4"])
        ws = a["window_status"]
        need(isinstance(ws, dict) and set(ws.keys()) == set(WINDOWS) and all(v in STATUSES for v in ws.values()), "window_status must carry the four windows with a status from %r" % (STATUSES,))
        ids.append(a["account_id"])
    need(ids == sorted(ids) and len(set(ids)) == len(ids), "accounts must be in account_id order, no duplicates")
    need(h["first_data_date"] == min(a["first_data_date"] for a in accs), "household.first_data_date must be the earliest first_data_date among its accounts")
    members = {m["id"]: m for m in contract["members"]}
    vals = sample["values"]
    need(isinstance(vals, dict) and set(vals.keys()) == set(members.keys()), "values must hold exactly the contract's %d members (missing %s)" % (len(members), sorted(set(members) - set(vals))[:3]))
    classes = {"cash", "fixed_income", "equity", "structured", "alternatives", "commodities", "unclassified"}
    n_by_row = 0
    for k, v in vals.items():
        if isinstance(v, dict) and not is_absent(v):
            need(set(v.keys()) == {"by_row"} and isinstance(v["by_row"], dict) and v["by_row"], "member %s holds an unwrapped per-row map: a per-row value must be {\"by_row\": {...}}" % k)
            keys = set(v["by_row"].keys())
            need(keys <= (set(ids) | classes), "member %s: by_row keys must be account ids of the household or asset classes" % k)
            need(all(is_figure(x) for x in v["by_row"].values()), "member %s: every by_row entry must be a figure or an absent form" % k)
            n_by_row += 1
        elif isinstance(v, list):
            need(all(isinstance(s, dict) and set(s.keys()) == {"name", "points"} for s in v), "member %s: a series is a list of {name, points}" % k)
        else:
            need(is_figure(v), "member %s holds a value that is not a figure, a text, an absent form, a by_row map or a series" % k)
        if members[k]["source"] == "ABSENT":
            need(is_absent(v), "member %s is ABSENT in the contract and must hold the absent form, never a number" % k)
    need(n_by_row >= 10, "only %d per-row members: the per-account grain members (avs, act, trgl, glr) must use by_row" % n_by_row)
    return len(accs), n_by_row


def check(root):
    c = json.loads((root / CONTRACT).read_bytes().decode("utf-8"))
    ver = tuple(int(x) for x in str(c.get("contract_version") or "0.0.0").split("."))
    need(ver > (0, 2, 0), "contract_version %r must be above 0.2.0" % c.get("contract_version"))
    shas = {x.get("sha256") for x in (c.get("lineage") or [])}
    need(V010 in shas and V020 in shas, "lineage must list the 0.1.0 bytes and the 0.2.0 bytes")
    fr = (c.get("document") or {}).get("filled_report")
    need(isinstance(fr, dict) and fr.get("top_level_keys") == ["household", "values"] and fr.get("household_fields") == ["household_ref", "as_of", "first_data_date", "accounts"]
         and fr.get("account_entry_fields") == ["account_id", "last4", "first_data_date", "window_status"] and fr.get("window_status_values") == list(STATUSES)
         and str(fr.get("per_row_member_form") or "").strip() != "" and str(fr.get("window_status_rule") or "").strip() != "" and str(fr.get("first_data_date_rule") or "").strip() != "",
         "document.filled_report must state the shape: top_level_keys, household_fields, account_entry_fields, window_status_values, per_row_member_form, window_status_rule and first_data_date_rule")
    need(Path(SAMPLE).is_file(), "the private sample %s is missing" % SAMPLE)
    sample = json.loads(Path(SAMPLE).read_text(encoding="utf-8"))
    n_acc, n_rows = check_sample_shape(sample, c)
    r = json.loads((root / (D + "0.9.0_WK_IRPT_DASHBD~148/SAMPLE_ALIGN.json")).read_bytes().decode("utf-8")) if (root / (D + "0.9.0_WK_IRPT_DASHBD~148/SAMPLE_ALIGN.json")).is_file() else None
    need(r is not None, "no ~148/SAMPLE_ALIGN.json")
    need(r.get("sample_sha256") == sha(SAMPLE), "the record is not bound to the private sample's bytes")
    csha = sha(root / CONTRACT)
    need(r.get("contract_sha256") == csha, "the record is not bound to the current contract bytes")
    code = r.get("code") or {}
    f = str(code.get("file") or "")
    need(f.startswith(PROJ) and code.get("tracked") is True and HEX64.fullmatch(str(code.get("sha256") or "")) and (root / f).is_file() and sha(root / f) == code["sha256"], "code %r" % code)
    br = root / (D + "0.9.0_WK_IRPT_DASHBD~141/HOUSEHOLD_SAMPLE_BUILD.json")
    need(br.is_file() and r.get("build_record_sha256") == sha(br), "build_record_sha256 must equal the regenerated HOUSEHOLD_SAMPLE_BUILD.json")
    b = json.loads(br.read_bytes().decode("utf-8"))
    need(b.get("contract_sha256") == csha, "the regenerated build record must be bound to the current contract bytes")
    # round 94's criterion on the regenerated record
    spec = importlib.util.spec_from_file_location("p94", str(Path(__file__).resolve().parents[1] / "r94" / "p94_round94.py"))
    p94 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p94)
    try:
        p94.check_sample(root)
    except p94.Fail as e:
        raise Fail("DB94-2-AC1 no longer passes on the regenerated build record: %s" % e)
    need(r.get("accounts") == n_acc and r.get("per_row_members") == n_rows, "accounts and per_row_members must equal what the sample holds (%d and %d)" % (n_acc, n_rows))
    rd = r.get("reads") or {}
    need(rd.get("vendor_calls") == 0 and rd.get("s3_writes") == 0 and rd.get("secret_reads") == 0 and r.get("pushed") is False and r.get("served_values_changed") is False and r.get("sample_kept_private") is True, "reads/pushed/private %r" % rd)
    hits = long_digit_runs(r)
    need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: contract %s states the filled-report shape; the private sample conforms (%d accounts, %d per-row members); DB94-2-AC1 still passes on the regenerated build record" % (c["contract_version"], n_acc, n_rows))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    try:
        need(cid == "DB97-1-AC1", "unknown criterion %r" % cid)
        check(root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB97"))
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
