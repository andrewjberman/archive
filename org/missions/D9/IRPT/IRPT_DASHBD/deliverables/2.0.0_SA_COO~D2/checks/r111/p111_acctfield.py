"""IRPT_DASHBD round 111 (issuer 2.0.0_SA_COO~D2) -- the account-number field read of the CTO's ROUND-111 ANALYSIS (section 2 cell 3).

  DB111-3-AC1 (~181)  READ: which Orion or Eclipse silver field holds Inflection's custodian account number (counts only, no value copied).
                      Record: deliverables/0.9.0_WK_IRPT_DASHBD~181/RD_ACCOUNT_NUMBER_FIELD_R111.json

The checker grades FORM and INTERNAL CONSISTENCY only (a read's truth is the reader's and the CTO's), plus ONE independent offline re-measure:
each candidate's `qualifies` flag is recomputed from its recorded shares by the rule below, and the answer must agree with the candidates.

  THE QUALIFYING RULE (the CTO's ruling, round 111): a STRING column holds the custodian account number only if it is keyed to the account, at least
  95 percent of accounts carry a non-null value with a digit run of 4 or more, at least 95 percent of accounts carry the same value in every sampled
  partition (at least 2 partitions sampled, else stability is not measured and the column cannot qualify), and at least 95 percent of accounts carry a
  value no other account carries.

Offline, stdlib only, terminates in seconds.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]          the pure rule and the refusal arms on synthetic records
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC = D + "0.9.0_WK_IRPT_DASHBD~181/RD_ACCOUNT_NUMBER_FIELD_R111.json"
CLAIMS = ("measured", "inferred", "held", "absent")
FIRMS = ("orion", "eclipse")
NAME = re.compile(r"[A-Za-z0-9_]{1,80}")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "scope_words")
THRESHOLD = 0.95
CAND_KEYS = {"firm", "table", "column", "distinct_values", "non_null_values", "share_values_digit_run_ge4", "share_values_digit_run_ge8", "share_values_all_digit",
             "share_values_alpha_only", "keyed_to_account", "accounts_with_value", "share_accounts_digit_run_ge4", "share_accounts_stable", "share_accounts_unique",
             "partitions_sampled", "qualifies", "claim", "words"}
SHARES = ("share_values_digit_run_ge4", "share_values_digit_run_ge8", "share_values_all_digit", "share_values_alpha_only", "share_accounts_digit_run_ge4",
          "share_accounts_stable", "share_accounts_unique")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def is_share(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and 0.0 <= x <= 1.0


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "the record %s does not exist" % rel)
    try:
        return json.loads(p.read_bytes().decode("utf-8"))
    except Exception as e:
        raise Fail("the record %s is not UTF-8 JSON (%s)" % (rel, type(e).__name__))


def claim_ok(obj, where):
    need(isinstance(obj, dict) and obj.get("claim") in CLAIMS, "%s must carry a claim field of %s" % (where, "/".join(CLAIMS)))


def digit_runs(x, key=""):
    """keys of every string holding a run of 8 or more digits outside the allowed key fields."""
    out = []
    if isinstance(x, dict):
        for k, v in x.items():
            out += digit_runs(v, k)
    elif isinstance(x, list):
        for v in x:
            out += digit_runs(v, key)
    elif isinstance(x, str) and key not in DIGIT_OK_KEYS and LONG_DIGITS.search(x):
        out.append(key)
    return out


def qualifies(c):
    """THE RULE, recomputed from one candidate's recorded numbers."""
    return bool(c["keyed_to_account"] and c["partitions_sampled"] >= 2 and c["share_accounts_digit_run_ge4"] >= THRESHOLD
                and c["share_accounts_stable"] >= THRESHOLD and c["share_accounts_unique"] >= THRESHOLD)


def check_candidate(c, i):
    w = "candidates[%d]" % i
    need(isinstance(c, dict) and set(c.keys()) == CAND_KEYS, "%s must hold exactly the keys %s" % (w, sorted(CAND_KEYS)))
    need(c["firm"] in FIRMS and isinstance(c["table"], str) and NAME.fullmatch(c["table"]) and isinstance(c["column"], str) and NAME.fullmatch(c["column"]),
         "%s: firm is orion or eclipse; table and column are names only (letters, digits, underscore)" % w)
    for k in ("distinct_values", "non_null_values", "accounts_with_value", "partitions_sampled"):
        need(is_int(c[k]) and c[k] >= 0, "%s.%s must be a non-negative integer" % (w, k))
    need(c["distinct_values"] <= c["non_null_values"], "%s: more distinct values than non-null values" % w)
    for k in SHARES:
        need(is_share(c[k]), "%s.%s must be a share from 0 to 1" % (w, k))
    need(c["share_values_digit_run_ge8"] <= c["share_values_digit_run_ge4"] + 1e-9, "%s: the share with a digit run of 8 or more exceeds the share with 4 or more" % w)
    need(c["share_values_all_digit"] + c["share_values_alpha_only"] <= 1.0 + 1e-9, "%s: the all-digit and alphabetic-only shares sum to more than 1" % w)
    need(isinstance(c["keyed_to_account"], bool) and isinstance(c["qualifies"], bool), "%s: keyed_to_account and qualifies must be true or false" % w)
    need(nes(c["words"]) and len(c["words"]) <= 600, "%s.words must be words of at most 600 characters (no value copied)" % w)
    claim_ok(c, w)
    need(c["qualifies"] == qualifies(c), "%s: qualifies is %s but the rule (keyed, 2 or more partitions, 95 percent digit-run-of-4, stable and unique) gives %s on the recorded shares"
         % (w, c["qualifies"], qualifies(c)))


def check_record(r):
    need(isinstance(r, dict), "the record is not an object")
    a = r.get("answer")
    need(isinstance(a, dict) and isinstance(a.get("field_found"), bool) and nes(a.get("words")), "answer must hold field_found (true or false) and words")
    claim_ok(a, "answer")
    cs = r.get("candidates")
    need(isinstance(cs, list) and len(cs) >= 1, "candidates must list every STRING column examined (at least 1)")
    for i, c in enumerate(cs):
        check_candidate(c, i)
    keys = [(c["firm"], c["table"], c["column"]) for c in cs]
    need(len(set(keys)) == len(keys), "a column appears twice in candidates")
    qual = [c for c in cs if c["qualifies"]]
    if a["field_found"]:
        need(NAME.fullmatch(str(a.get("table"))) and NAME.fullmatch(str(a.get("column"))), "a found field names its table and column (names only)")
        need(any(c["table"] == a["table"] and c["column"] == a["column"] and c["qualifies"] for c in cs), "answer names %s.%s but no qualifying candidate has that table and column" % (a.get("table"), a.get("column")))
        need(a["claim"] in ("measured", "inferred"), "a found field carries the claim measured or inferred")
    else:
        need(a.get("table") is None and a.get("column") is None, "when no field is found, table and column are null")
        need(not qual, "answer says no field is found but %d candidate(s) qualify under the rule" % len(qual))
        need(a["claim"] in ("measured", "held", "absent"), "a not-found answer carries the claim measured, held or absent")
    den = r.get("denominator")
    need(isinstance(den, dict) and is_int(den.get("tables_read")) and den["tables_read"] >= 1 and is_int(den.get("partitions_read")) and den["partitions_read"] >= den["tables_read"]
         and is_int(den.get("accounts_in_scope")) and den["accounts_in_scope"] >= 1 and nes(den.get("scope_words")),
         "denominator must hold tables_read (>= 1), partitions_read (>= tables_read), accounts_in_scope (>= 1) and scope_words")
    need(len({(c["firm"], c["table"]) for c in cs}) <= den["tables_read"], "candidates name more tables than denominator.tables_read")
    need(max(c["partitions_sampled"] for c in cs) <= den["partitions_read"], "a candidate samples more partitions than denominator.partitions_read")
    need(all(c["accounts_with_value"] <= den["accounts_in_scope"] for c in cs), "a candidate counts more accounts than denominator.accounts_in_scope")
    pc = r.get("positive_control")
    need(isinstance(pc, dict) and nes(pc.get("description")) and nes(pc.get("expected")) and nes(pc.get("observed")) and pc.get("passed") is True
         and pc.get("synthetic_number_qualifies") is True and pc.get("synthetic_fragment_qualifies") is False,
         "positive_control must hold description, expected, observed, passed true, synthetic_number_qualifies true and synthetic_fragment_qualifies false")
    rd = r.get("reads")
    need(isinstance(rd, dict) and all(rd.get(k) == 0 for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads")), "reads must hold vendor_calls, s3_writes, dynamodb_writes and secret_reads all 0")
    need(is_int(rd.get("s3_reads")) and rd["s3_reads"] >= 0, "reads.s3_reads must be an integer")
    need(r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False and r.get("files_in_repo") is False, "served_values_changed, pushed, deployed and files_in_repo must be false")
    need(not digit_runs(r), "the record holds a run of 8 or more digits outside a sha256, path, file, key, where or vintage field: %s" % digit_runs(r))


def run(root):
    r = load(root, REC)
    check_record(r)
    cs = r["candidates"]
    a = r["answer"]
    print("OK: %d string column(s) examined over %d table(s) and %d partition(s); %d qualify under the rule; the answer is %s; the positive control passed; no value copied"
          % (len(cs), r["denominator"]["tables_read"], r["denominator"]["partitions_read"], sum(1 for c in cs if c["qualifies"]),
             ("%s.%s" % (a["table"], a["column"])) if a["field_found"] else "no field found"))


# ------------------------------------------------------------------ self-test
def synth_cand(**kw):
    c = {"firm": "orion", "table": "fact_positions", "column": "acct_text", "distinct_values": 90, "non_null_values": 100, "share_values_digit_run_ge4": 0.2,
         "share_values_digit_run_ge8": 0.0, "share_values_all_digit": 0.0, "share_values_alpha_only": 0.8, "keyed_to_account": True, "accounts_with_value": 100,
         "share_accounts_digit_run_ge4": 0.2, "share_accounts_stable": 1.0, "share_accounts_unique": 0.5, "partitions_sampled": 5, "qualifies": False,
         "claim": "measured", "words": "a text column that carries fragments"}
    c.update(kw)
    return c


def synth_record(found):
    good = synth_cand(column="acct_no", share_values_digit_run_ge4=1.0, share_values_digit_run_ge8=1.0, share_values_all_digit=1.0, share_values_alpha_only=0.0,
                      share_accounts_digit_run_ge4=1.0, share_accounts_unique=1.0, qualifies=True, words="a digit column, stable and unique per account")
    cs = [synth_cand()] + ([good] if found else [])
    return {"answer": {"field_found": found, "table": "fact_positions" if found else None, "column": "acct_no" if found else None, "words": "words", "claim": "measured"},
            "candidates": cs, "denominator": {"tables_read": 2, "partitions_read": 6, "accounts_in_scope": 100, "scope_words": "the newest partitions of the two granted prefixes"},
            "positive_control": {"description": "the rule on two synthetic columns", "expected": "number passes, fragment fails", "observed": "number passes, fragment fails", "passed": True,
                                 "synthetic_number_qualifies": True, "synthetic_fragment_qualifies": False},
            "reads": {"s3_reads": 12, "s3_writes": 0, "vendor_calls": 0, "secret_reads": 0, "dynamodb_writes": 0},
            "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}


REFUSED = []


def must_fail(rec, why):
    try:
        check_record(rec)
    except Fail:
        REFUSED.append(why)
        return
    raise Fail("self-test arm did not refuse: " + why)


def selftest(_root):
    arms = []
    check_record(synth_record(True))
    arms.append("passing: a found field")
    check_record(synth_record(False))
    arms.append("passing: no field found")
    r = synth_record(True)
    r["answer"]["field_found"] = False
    r["answer"]["table"] = r["answer"]["column"] = None
    must_fail(r, "no field found while a candidate qualifies")
    r = synth_record(False)
    r["answer"].update(field_found=True, table="fact_positions", column="acct_text")
    must_fail(r, "a found field that does not qualify")
    r = synth_record(True)
    r["candidates"][1]["share_accounts_stable"] = 0.5
    must_fail(r, "qualifies true on a share below the threshold")
    r = synth_record(True)
    r["candidates"][1]["partitions_sampled"] = 1
    must_fail(r, "qualifies true with stability not measured")
    r = synth_record(True)
    r["candidates"][1]["sample_value"] = "x"
    must_fail(r, "an extra key in a candidate")
    r = synth_record(False)
    r["candidates"][0]["words"] = "see 12345678901 here"
    must_fail(r, "a run of 8 or more digits in words")
    r = synth_record(False)
    del r["candidates"][0]["claim"]
    must_fail(r, "a candidate with no claim")
    r = synth_record(False)
    r["positive_control"]["synthetic_fragment_qualifies"] = True
    must_fail(r, "a positive control that passes a fragment")
    r = synth_record(False)
    r["reads"]["s3_writes"] = 1
    must_fail(r, "a write")
    r = synth_record(False)
    r["candidates"][0]["column"] = "a value 7"
    must_fail(r, "a column that is not a name")
    print("OK: selftest %d refusal arms and %d passing arms" % (len(REFUSED), len(arms)))


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        selftest(argv[2] if len(argv) > 2 else ".")
        return 0
    if len(argv) != 3:
        print("usage: p111_acctfield.py <repo_root> <criterion_id> | --selftest [<repo_root>]")
        return 2
    root, cid = argv[1], argv[2]
    if cid != "DB111-3-AC1":
        print("unknown criterion %s" % cid)
        return 2
    try:
        run(root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % cid)
        return 1
    print("%s PASS" % cid)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
