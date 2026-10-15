"""IRPT_DASHBD round 118 (worker 0.9.0_WK_IRPT_DASHBD~186) -- DB-b-231, the flow-guard READ.

READ-ONLY. For the 49 Financial account_return_daily gold partition of 2026-04-21 and of the five dates by households
broken (2026-07-02, 2026-10-13, 2026-09-22, 2026-10-06, 2026-09-16): every GRADED_DISAGREED account-day is classified
from its persisted columns by which input disagrees (FLOW, VALUE, FLOW_AND_VALUE, NEITHER, NO_PRIOR); the value gap of
the VALUE and FLOW_AND_VALUE rows is profiled by sign, by size band and by the account's row on the next trading day.

Reads: GET only. data.parquet and manifest.json of each date partition; data.parquet of the previous trading day
(required) and of the next trading day (absent is recorded, never zero). Every address is lib/opal_naming.address()
output for the firm's registry row. Writes: the record RD_FLOW_GUARD_READ_R118.json in this folder, and one counts-only
private file under the worker's private evidence folder. Nothing else.

Usage: python -I <this file> <repo_root>
"""
import datetime as dt
import hashlib
import io
import json
import os
import subprocess
import sys
from pathlib import Path

FIRM_KEY = "49financial"
REGISTRY_REL = "data/firm_registry.json"
TABLE = "account_return_daily"
FOLDER = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~186/"
ANALYSIS_REL = FOLDER + "flow_guard_read_r118.py"
REC_REL = FOLDER + "RD_FLOW_GUARD_READ_R118.json"
PRIVATE_DIR = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~186"
PRIVATE_NAME = "flow_guard_read_r118_counts.json"
DATES = ["2026-04-21", "2026-07-02", "2026-10-13", "2026-09-22", "2026-10-06", "2026-09-16"]
CAUSES = ["FLOW", "VALUE", "FLOW_AND_VALUE", "NEITHER", "NO_PRIOR"]
PROFILE_KEYS = ["value_gap_rows", "gap_positive", "gap_negative", "band_le_1pct", "band_1_to_5pct", "band_gt_5pct",
                "reversal_next_day", "not_reversed", "no_next_day_row"]
GUARD_GD = "GRADED_DISAGREED"
DQ_FU = "FLOW_UNRECONCILED"
COLUMNS = ["account_id", "market_value_eod", "external_flow", "holdings_price_return", "guard_state", "day_quality"]
CLASS_WORDS = ("Each GRADED_DISAGREED account-day is classified from its persisted columns alone. With V the market value, "
               "F the external flow, p the holdings price return and V0 the same account's market value on the previous "
               "trading day: NO_PRIOR when there is no previous-day row, the previous value is null or not above zero, or "
               "V, F or p is null. Otherwise the account's return v = V/V0 - 1 and its flow share s = |F|/V0 are compared "
               "with the date's own tolerance tau: FLOW when s is above tau and |v - p| is not, VALUE when |v - p| is above "
               "tau and s is not, FLOW_AND_VALUE when both are above, NEITHER when neither is. The label says which input "
               "disagrees in persisted terms; it is inferred, not read from the producer's internal comparison.")
TOL_FILE = "gold/account_return_daily/date=<day>/manifest.json (the date's own partition manifest, 49financial)"


class Stop(Exception):
    pass


class Reader(object):
    """GET only. There is deliberately no method that changes a remote object."""

    def __init__(self):
        import boto3
        self._s3 = boto3.client("s3")
        self.gets = 0

    def get(self, bucket, key):
        self.gets += 1
        return self._s3.get_object(Bucket=bucket, Key=key)["Body"].read()


def is_absent(exc):
    from botocore.exceptions import ClientError
    if not isinstance(exc, ClientError):
        return False
    return exc.response.get("Error", {}).get("Code") in ("NoSuchKey", "404")


def locate(naming, firm, day):
    addr = naming.address("irpt", firm, "gold", TABLE, "date=%s" % day)
    rest = addr[len("s3://"):]
    bucket, _, key = rest.partition("/")
    return bucket, key.rstrip("/") + "/"


def read_partition(reader, bucket, prefix, want_manifest):
    """Returns (rows, raw_count, manifest). rows maps account_id to a tuple (V, F, p, guard_state, day_quality).
    A duplicate account-day row is a surprise and stops the read."""
    import pyarrow.parquet as pq
    body = reader.get(bucket, prefix + "data.parquet")
    t = pq.read_table(io.BytesIO(body), columns=COLUMNS).to_pydict()
    raw = len(t["account_id"])
    rows = {}
    for i in range(raw):
        a = t["account_id"][i]
        if a in rows:
            raise Stop("duplicate account-day row in a partition; a surprise row is owed")
        rows[a] = (t["market_value_eod"][i], t["external_flow"][i], t["holdings_price_return"][i],
                   t["guard_state"][i], t["day_quality"][i])
    man = None
    if want_manifest:
        man = json.loads(reader.get(bucket, prefix + "manifest.json").decode("utf-8"))
    return rows, raw, man


def tolerance_of(man, day):
    try:
        tau = man["thresholds"]["tolerance"]
    except (KeyError, TypeError):
        raise Stop("the manifest of %s lacks thresholds.tolerance; a BLOCKING row is owed" % day)
    if isinstance(tau, bool) or not isinstance(tau, (int, float)):
        raise Stop("thresholds.tolerance of %s is not a number" % day)
    return float(tau)


def cause_of(v, f, p, v0, tau):
    """The five-way cause of one GRADED_DISAGREED account-day. v0 is the previous trading day's market value or None."""
    if v0 is None or not v0 > 0 or v is None or f is None or p is None:
        return "NO_PRIOR"
    chg = v / v0 - 1.0
    flow_big = abs(f) / v0 > tau
    value_gap = abs(chg - p) > tau
    if flow_big and value_gap:
        return "FLOW_AND_VALUE"
    if flow_big:
        return "FLOW"
    if value_gap:
        return "VALUE"
    return "NEITHER"


def split(rows_t, rows_0, tau):
    by = dict((c, 0) for c in CAUSES)
    gd = fu = 0
    for a, r in rows_t.items():
        if r[4] == DQ_FU:
            fu += 1
        if r[3] == GUARD_GD:
            gd += 1
            prior = rows_0.get(a)
            v0 = prior[0] if prior is not None else None
            by[cause_of(r[0], r[1], r[2], v0, tau)] += 1
    return gd, fu, by


def gap_of(v, p, v0):
    """(V / V0 - 1) - p, or None where it is undefined."""
    if v0 is None or not v0 > 0 or v is None or p is None:
        return None
    return (v / v0 - 1.0) - p


def profile(rows_t, rows_0, rows_next, tau):
    out = dict((k, 0) for k in PROFILE_KEYS)
    for a, r in rows_t.items():
        if r[3] != GUARD_GD:
            continue
        prior = rows_0.get(a)
        v0 = prior[0] if prior is not None else None
        if cause_of(r[0], r[1], r[2], v0, tau) not in ("VALUE", "FLOW_AND_VALUE"):
            continue
        g = gap_of(r[0], r[2], v0)
        out["value_gap_rows"] += 1
        if g > 0:
            out["gap_positive"] += 1
        else:
            out["gap_negative"] += 1
        ag = abs(g)
        if ag <= 0.01:
            out["band_le_1pct"] += 1
        elif ag <= 0.05:
            out["band_1_to_5pct"] += 1
        else:
            out["band_gt_5pct"] += 1
        nxt = rows_next.get(a) if rows_next is not None else None
        if nxt is None:
            out["no_next_day_row"] += 1
            continue
        g2 = gap_of(nxt[0], nxt[2], r[0])
        if g2 is not None and abs(g2) > tau and (g2 > 0) != (g > 0):
            out["reversal_next_day"] += 1
        else:
            out["not_reversed"] += 1
    return out


def positive_control():
    """Synthetic account-days through the same split(): one per cause, plus a prior-day row that is absent and a
    prior-day row whose value is null (both NO_PRIOR)."""
    tau = 0.001244
    rows_t = {
        "c_value": (1.10, 0.0, 0.0, GUARD_GD, DQ_FU),
        "c_flow": (1.00, 0.5, 0.0, GUARD_GD, DQ_FU),
        "c_both": (1.10, 0.5, 0.0, GUARD_GD, DQ_FU),
        "c_neither": (1.0005, 0.0, 0.0, GUARD_GD, DQ_FU),
        "c_no_row": (1.0, 0.0, 0.0, GUARD_GD, DQ_FU),
        "c_null_prior": (1.0, 0.0, 0.0, GUARD_GD, DQ_FU),
    }
    rows_0 = {
        "c_value": (1.0, 0.0, 0.0, "GRADED_AGREED", "MEASURED"),
        "c_flow": (1.0, 0.0, 0.0, "GRADED_AGREED", "MEASURED"),
        "c_both": (1.0, 0.0, 0.0, "GRADED_AGREED", "MEASURED"),
        "c_neither": (1.0, 0.0, 0.0, "GRADED_AGREED", "MEASURED"),
        "c_null_prior": (None, 0.0, 0.0, "GRADED_AGREED", "MEASURED"),
    }
    expected = {"c_value": "VALUE", "c_flow": "FLOW", "c_both": "FLOW_AND_VALUE", "c_neither": "NEITHER",
                "c_no_row": "NO_PRIOR", "c_null_prior": "NO_PRIOR"}
    observed = {}
    for a, r in rows_t.items():
        prior = rows_0.get(a)
        v0 = prior[0] if prior is not None else None
        observed[a] = cause_of(r[0], r[1], r[2], v0, tau)
    gd, _fu, by = split(rows_t, rows_0, tau)
    want_by = {"FLOW": 1, "VALUE": 1, "FLOW_AND_VALUE": 1, "NEITHER": 1, "NO_PRIOR": 2}
    passed = observed == expected and by == want_by and gd == len(rows_t)
    return {"passed": bool(passed),
            "description": "six synthetic account-days through the classifier: one VALUE, one FLOW, one FLOW_AND_VALUE, "
                           "one NEITHER, one with no previous-day row and one with a null previous value (both NO_PRIOR); "
                           "tolerance 0.001244",
            "expected": "; ".join("%s=%s" % (k, expected[k]) for k in sorted(expected)),
            "observed": "; ".join("%s=%s" % (k, observed[k]) for k in sorted(observed)),
            "by_cause": by}


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def is_tracked(repo, rel):
    r = subprocess.run(["git", "-C", repo, "ls-files", "--error-unmatch", rel], capture_output=True, text=True)
    return r.returncode == 0


def main(argv):
    repo = os.path.abspath(argv[1] if len(argv) > 1 else ".")
    pc = positive_control()
    print("POSITIVE CONTROL: passed=%s" % pc["passed"])
    if not pc["passed"]:
        raise Stop("the positive control failed; the classifier is not trusted: %s" % pc["observed"])
    sys.path.insert(0, repo)
    from lib import opal_naming as naming
    from lib import trading_calendar as tc
    with open(os.path.join(repo, REGISTRY_REL), "rb") as fh:
        registry = json.loads(fh.read().decode("utf-8"))
    firms = [f for f in registry.get("firms", []) if f.get("firm_id") == FIRM_KEY]
    if len(firms) != 1:
        raise Stop("the registry does not enumerate exactly one row for the firm")
    firm = firms[0]["firm_id"]

    reader = Reader()
    results = []
    diag = []
    for day in DATES:
        d_obj = dt.date.fromisoformat(day)
        b, k = locate(naming, firm, day)
        rows_t, raw_t, man = read_partition(reader, b, k, True)
        tau = tolerance_of(man, day)
        d0 = tc.prev_trading_day(d_obj).isoformat()
        b0, k0 = locate(naming, firm, d0)
        try:
            rows_0, raw_0, _m = read_partition(reader, b0, k0, False)
        except Exception as exc:
            if is_absent(exc):
                raise Stop("the previous trading day partition of %s is absent; an unreadable source is never a zero" % day)
            raise
        x = d_obj + dt.timedelta(days=1)
        while not tc.is_trading_day(x):
            x += dt.timedelta(days=1)
        d1 = x.isoformat()
        b1, k1 = locate(naming, firm, d1)
        try:
            rows_n, raw_n, _m = read_partition(reader, b1, k1, False)
            present = True
        except Exception as exc:
            if not is_absent(exc):
                raise
            rows_n, raw_n, present = None, None, False
        gd, fu, by = split(rows_t, rows_0, tau)
        prof = profile(rows_t, rows_0, rows_n, tau)
        results.append({"date": day, "tolerance": tau, "rows": len(rows_t), "rows_graded_disagreed": gd,
                        "rows_flow_unreconciled": fu, "by_cause": by, "value_gap_profile": prof})
        diag.append({"date": day, "prev_day": d0, "prev_rows": raw_0, "next_day": d1, "next_partition_present": present,
                     "next_rows": raw_n})
        print("DATE %s: tolerance %r; rows %d; graded_disagreed %d; flow_unreconciled %d; by_cause %s"
              % (day, tau, len(rows_t), gd, fu, by))
        print("  VALUE PROFILE %s: %s" % (day, prof))
        print("  PREV %s rows %d; NEXT %s partition %s rows %s" % (d0, raw_0, d1,
                                                                 "present" if present else "ABSENT", raw_n))

    tot_gd = sum(x["rows_graded_disagreed"] for x in results)
    tot_by = dict((c, sum(x["by_cause"][c] for x in results)) for c in CAUSES)
    print("TOTALS: rows_graded_disagreed %d; by_cause %s" % (tot_gd, tot_by))

    sha = sha256_of(os.path.abspath(__file__))
    tracked = is_tracked(repo, ANALYSIS_REL)
    rec = {
        "dates": [{"date": x["date"], "tolerance": x["tolerance"], "rows": x["rows"],
                   "rows_graded_disagreed": x["rows_graded_disagreed"],
                   "rows_flow_unreconciled": x["rows_flow_unreconciled"], "by_cause": x["by_cause"],
                   "value_gap_profile": x["value_gap_profile"], "claim": "inferred"} for x in results],
        "totals": {"rows_graded_disagreed": tot_gd, "by_cause": tot_by, "claim": "inferred"},
        "classification": {"words": CLASS_WORDS, "claim": "inferred"},
        "tolerance_source": {"file": TOL_FILE, "key_path": "thresholds.tolerance",
                             "words": "the tolerance is read from each date's own partition manifest.json, the same partition "
                                      "the rows are read from; no tolerance is taken from another date or from the producer"},
        "positive_control": {"description": pc["description"], "expected": pc["expected"],
                             "observed": pc["observed"], "passed": True},
        "analysis": {"file": ANALYSIS_REL, "sha256": sha, "tracked": tracked},
        "reads": {"s3_reads": reader.gets, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
        "files_in_repo": False,
        "served_values_changed": False,
        "pushed": False,
        "deployed": False,
    }
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    private = {"scope": "counts only: partition row counts, previous and next partition presence per date",
                "diagnostics": diag, "s3_reads": reader.gets}
    with open(os.path.join(PRIVATE_DIR, PRIVATE_NAME), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(private, indent=2, sort_keys=True) + "\n")
    with open(os.path.join(repo, REC_REL), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec, indent=2) + "\n")
    print("RECORD WRITTEN: %s" % REC_REL)
    print("ANALYSIS SHA256 %s; tracked %s; s3 GET calls %d" % (sha, tracked, reader.gets))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Stop as e:
        print("STOP: %s" % e)
        sys.exit(3)
