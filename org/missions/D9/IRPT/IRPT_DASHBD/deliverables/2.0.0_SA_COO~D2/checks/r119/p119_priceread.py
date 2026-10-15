"""IRPT_DASHBD round 119, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-236, the 2026-04-21 PRICE READ (CTO analysis @d856067e84 ruling 4).

  DB-b-236 (~190) which holdings price moved, or failed to, on 2026-04-21: for the 49 Financial account rows the flow-guard read classed VALUE or
                  FLOW_AND_VALUE (the account value moved, the holdings price return did not), the account-level profile of the neighbour
                  (IRPT_BCKEND's holdings_performance_daily: status, excluded securities, excluded weight) and, where the holdings gold
                  carries security grain, the securities whose price return is flat or absent with their price source; counts only, nothing
                  written.                                                                                      DB119-4-AC1

The checker RECOMPUTES the account-level profile from the gold (read-only GET of the two 2026-04-21 partitions): the number of GRADED_DISAGREED
rows, how many hold a row in holdings_performance_daily, their status counts, how many have excluded_count above zero and the excluded_weight bands.
The security-level part is graded for form and internal consistency only (it reads a source the checker does not re-derive): state READ or ABSENT.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the record clauses on synthetic arms
"""
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~190/RD_PRICE_READ_0421_R119.json"
FG_REL = D + "0.9.0_WK_IRPT_DASHBD~186/RD_FLOW_GUARD_READ_R118.json"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~190/price_read_0421_r119.py"
DAY = "2026-04-21"
FIRM = "49financial"
CLAIMS = ("measured", "inferred", "held", "absent")
BANDS = ("zero", "le_1pct", "1_to_10pct", "gt_10pct")
FOREIGN = ("inflection", "cottonwood", "orion/", "eclipse/", "opal-data-inflection", "opal-data-cottonwood")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item",
                "delete_item", "update_item", "write_table", "write_to_dataset", ".to_parquet(", "s3 cp", "s3 sync", "s3 rm", "s3 mv")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def is_tracked(root, rel):
    return subprocess.run(["git", "-C", str(root), "ls-files", "--error-unmatch", rel], capture_output=True, text=True).returncode == 0


# ------------------------------------------------------------------------------------------------ the account-level profile (pure)
def band_of(w):
    if w is None or w == 0:
        return "zero"
    if w <= 0.01:
        return "le_1pct"
    if w <= 0.10:
        return "1_to_10pct"
    return "gt_10pct"


def profile(disagreed_accounts, holdings_rows):
    """disagreed_accounts: set of account ids; holdings_rows: dict account -> dict(status, excluded_count, excluded_weight)."""
    by_status = {}
    ex_zero = ex_pos = no_row = 0
    bands = {b: 0 for b in BANDS}
    for a in sorted(disagreed_accounts):
        h = holdings_rows.get(a)
        if h is None:
            no_row += 1
            continue
        by_status[str(h.get("status"))] = by_status.get(str(h.get("status")), 0) + 1
        if (h.get("excluded_count") or 0) > 0:
            ex_pos += 1
        else:
            ex_zero += 1
        bands[band_of(h.get("excluded_weight"))] += 1
    return {"accounts": len(disagreed_accounts), "no_holdings_row": no_row, "by_status": dict(sorted(by_status.items())),
            "excluded_count_zero": ex_zero, "excluded_count_positive": ex_pos, "excluded_weight_bands": bands}


def recount(root):
    sys.path.insert(0, str(root))
    import boto3
    import pyarrow.parquet as pq
    from lib import opal_naming
    s3 = boto3.client("s3")

    def table(name, cols):
        addr = opal_naming.address("irpt", FIRM, "gold", name, "date=%s" % DAY)
        bucket, key = addr[len("s3://"):].split("/", 1)
        body = s3.get_object(Bucket=bucket, Key=key.rstrip("/") + "/data.parquet")["Body"].read()
        return pq.read_table(io.BytesIO(body), columns=cols).to_pydict()
    ar = table("account_return_daily", ["account_id", "guard_state"])
    dis = {a for a, g in zip(ar["account_id"], ar["guard_state"]) if g == "GRADED_DISAGREED"}
    hp = table("holdings_performance_daily", ["account_id", "status", "excluded_count", "excluded_weight"])
    rows = {a: {"status": s, "excluded_count": c, "excluded_weight": w} for a, s, c, w in
            zip(hp["account_id"], hp["status"], hp["excluded_count"], hp["excluded_weight"])}
    return profile(dis, rows)


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, truth, fg, analysis_text, tracked, analysis_sha):
    exp = {"date", "value_rows", "account_profile", "security_level", "positive_control", "method_words", "analysis", "reads", "claim",
           "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["date"] == DAY and nes(rec["method_words"]) and rec["claim"] in CLAIMS, "date, method_words or claim")
    d0 = fg["dates"][0]
    need(d0["date"] == DAY, "the flow-guard record's first date is not 2026-04-21")
    vr = d0["by_cause"]["VALUE"] + d0["by_cause"]["FLOW_AND_VALUE"]
    need(rec["value_rows"] == vr and is_int(rec["value_rows"]), "value_rows %s differs from the flow-guard record's VALUE + FLOW_AND_VALUE %s" % (rec["value_rows"], vr))
    ap = rec["account_profile"]
    need(isinstance(ap, dict) and set(ap) == {"accounts", "no_holdings_row", "by_status", "excluded_count_zero", "excluded_count_positive",
                                              "excluded_weight_bands", "claim"} and ap["claim"] in CLAIMS, "account_profile keys")
    core = {k: ap[k] for k in ap if k != "claim"}
    need(core == truth, "account_profile differs from the recount: record %s, recount %s" % (core, truth))
    need(set(ap["excluded_weight_bands"]) == set(BANDS) and sum(ap["excluded_weight_bands"].values()) == ap["accounts"] - ap["no_holdings_row"],
         "excluded_weight_bands do not sum to the accounts that hold a holdings row")
    need(ap["excluded_count_zero"] + ap["excluded_count_positive"] == ap["accounts"] - ap["no_holdings_row"], "excluded counts do not sum")
    need(sum(ap["by_status"].values()) == ap["accounts"] - ap["no_holdings_row"], "by_status does not sum")
    sl = rec["security_level"]
    need(isinstance(sl, dict) and sl.get("state") in ("READ", "ABSENT") and nes(sl.get("words")), "security_level state and words")
    if sl["state"] == "ABSENT":
        need(set(sl) == {"state", "words", "claim"} and sl["claim"] in CLAIMS, "an ABSENT security_level carries state, words, claim only")
    else:
        need(set(sl) == {"state", "words", "source", "securities", "by_price_source", "by_security_class", "claim"} and sl["claim"] in CLAIMS,
             "a READ security_level keys")
        need(isinstance(sl["source"], dict) and set(sl["source"]) == {"file", "table", "words"} and all(nes(sl["source"][k]) for k in sl["source"]), "source form")
        secs = sl["securities"]
        need(isinstance(secs, list) and 1 <= len(secs) <= 25, "securities must list 1 to 25 entries")
        for s in secs:
            need(set(s) == {"security", "security_class", "price_source", "price_state", "accounts_affected", "claim"}
                 and nes(s["security"]) and nes(s["security_class"]) and nes(s["price_source"]) and s["price_state"] in ("flat", "absent")
                 and is_int(s["accounts_affected"]) and 1 <= s["accounts_affected"] <= ap["accounts"] and s["claim"] in CLAIMS, "a security entry")
        for k in ("by_price_source", "by_security_class"):
            need(isinstance(sl[k], dict) and sl[k] and all(nes(a) and is_int(b) and b >= 0 for a, b in sl[k].items()), "%s form" % k)
        need(sum(sl["by_price_source"].values()) == sum(sl["by_security_class"].values()), "by_price_source and by_security_class count the same pairs")
    pc = rec["positive_control"]
    need(isinstance(pc, dict) and set(pc) == {"description", "expected", "observed", "passed"} and pc["passed"] is True, "positive_control must pass")
    an = rec["analysis"]
    need(isinstance(an, dict) and an.get("file") == ANALYSIS_REL and an.get("tracked") is True and an.get("sha256") == analysis_sha and tracked,
         "analysis block")
    rd = rec["reads"]
    need(isinstance(rd, dict) and is_int(rd.get("s3_reads")) and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0
         and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads block")
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    low = analysis_text.lower()
    need(not [t for t in FOREIGN if t in low], "the analysis script names another firm's place")
    need(not [t for t in WRITE_TOKENS if t in low], "the analysis script holds a write call")
    return True


def run(root, cid):
    need(cid == "DB119-4-AC1", "unknown criterion %s" % cid)
    rec = load(root, REC_REL)
    fg = load(root, FG_REL)
    ap = Path(root) / ANALYSIS_REL
    need(ap.is_file(), "no analysis script")
    truth = recount(root)
    check_record(rec, truth, fg, ap.read_text(encoding="utf-8"), is_tracked(root, ANALYSIS_REL), hashlib.sha256(ap.read_bytes()).hexdigest())
    print("OK: price read: %d value rows on 2026-04-21 (equal to the flow-guard record); account profile recounted from the gold: %d accounts, "
          "%d without a holdings row, excluded-weight bands %s; security level %s" %
          (rec["value_rows"], truth["accounts"], truth["no_holdings_row"], truth["excluded_weight_bands"], rec["security_level"]["state"]))
    return True


def selftest(root):
    need(band_of(0) == "zero" and band_of(None) == "zero" and band_of(0.005) == "le_1pct" and band_of(0.05) == "1_to_10pct" and band_of(0.5) == "gt_10pct", "bands")
    hp = {"a": dict(status="OK", excluded_count=0, excluded_weight=0.0), "b": dict(status="OK", excluded_count=2, excluded_weight=0.05),
          "c": dict(status="NOT_OK", excluded_count=1, excluded_weight=0.5)}
    pr = profile({"a", "b", "c", "d"}, hp)
    need(pr["accounts"] == 4 and pr["no_holdings_row"] == 1 and pr["by_status"] == {"NOT_OK": 1, "OK": 2} and pr["excluded_count_zero"] == 1
         and pr["excluded_count_positive"] == 2 and pr["excluded_weight_bands"] == {"zero": 1, "le_1pct": 0, "1_to_10pct": 1, "gt_10pct": 1}, "profile")
    truth = profile({"a", "b", "c", "d"}, hp)
    fg = {"dates": [{"date": DAY, "by_cause": {"VALUE": 3, "FLOW_AND_VALUE": 1, "FLOW": 0, "NEITHER": 0, "NO_PRIOR": 0}}]}

    def good():
        return {"date": DAY, "value_rows": 4, "account_profile": dict(truth, claim="measured"),
                "security_level": {"state": "ABSENT", "words": "the holdings gold carries account grain only", "claim": "absent"},
                "positive_control": {"description": "d", "expected": "e", "observed": "o", "passed": True}, "method_words": "words",
                "analysis": {"file": ANALYSIS_REL, "sha256": "ab" * 32, "tracked": True},
                "reads": {"s3_reads": 4, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}, "claim": "measured",
                "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}

    def grade(rec, text="x = 1", tracked=True, h="ab" * 32, tr=truth):
        try:
            return check_record(rec, tr, fg, text, tracked, h)
        except Fail:
            return False
    need(grade(good()) is True, "GREEN arm failed")
    r = good()
    r["value_rows"] = 5
    need(grade(r) is False, "RED: value_rows differing from the flow-guard record must fail")
    r = good()
    r["account_profile"]["no_holdings_row"] = 0
    need(grade(r) is False, "RED: a profile that differs from the recount must fail")
    r = good()
    r["security_level"] = {"state": "READ", "words": "w", "source": {"file": "f", "table": "t", "words": "w"}, "securities": [], "by_price_source": {"x": 1},
                           "by_security_class": {"y": 1}, "claim": "measured"}
    need(grade(r) is False, "RED: a READ security level with no securities must fail")
    r = good()
    r["security_level"] = {"state": "READ", "words": "w", "source": {"file": "f", "table": "t", "words": "w"},
                           "securities": [{"security": "S1", "security_class": "equity", "price_source": "vendor", "price_state": "flat", "accounts_affected": 2, "claim": "measured"}],
                           "by_price_source": {"vendor": 2}, "by_security_class": {"equity": 3}, "claim": "measured"}
    need(grade(r) is False, "RED: by_price_source and by_security_class that count different pairs must fail")
    r = good()
    r["positive_control"]["passed"] = False
    need(grade(r) is False, "RED: a failed positive control must fail")
    r = good()
    r["method_words"] = "ids 1234567890"
    need(grade(r) is False, "RED: a long digit run must fail")
    need(grade(good(), tracked=False) is False, "RED: an untracked script must fail")
    need(grade(good(), text="s3.put_object(Bucket=b)") is False, "RED: a write call must fail")
    need(grade(good(), text="b = 'opal-data-cottonwood'") is False, "RED: another firm's place must fail")
    need(grade(good(), h="cd" * 32) is False, "RED: a hash mismatch must fail")
    print("selftest OK: band and profile arms, 1 green and 10 red record arms")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
            sys.exit(0)
        if len(sys.argv) != 3:
            print("usage: p119_priceread.py <repo_root> <criterion_id>")
            sys.exit(2)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
    except Exception as e:
        print("FAIL: %s: %s" % (type(e).__name__, str(e)[:200]))
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
