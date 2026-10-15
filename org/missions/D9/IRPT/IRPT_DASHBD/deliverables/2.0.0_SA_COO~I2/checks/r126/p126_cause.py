"""IRPT_DASHBD round 126, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the series-ended cause read (cell DB-i-13).

CTO round-122 analysis item 3 and ADDENDUM 1 (msg 8678): some Orion Scope series end months before the pull date (round 122
saw two of nine). For each early-ending series, is the account still held in Opal's own positions silver after the series
ended (Orion's series is STALE_AT_SOURCE) or not (CLOSED_OR_TRANSFERRED)? NO vendor call: the saved round-122 response bodies
(private) are read against fact_positions partitions (a GET-only read of Opal's own silver). Raw bodies and ids stay private;
the repo gets counts and words only.

  DBI126-1-AC1  the record is complete and carries no identifier; the script is a tracked file hashed as recorded with no AWS
                write call and no vendor call; every early-ending account's days-before-window-end, partitions after,
                held days, held-on-newest flag and verdict equal the checker's recompute from the saved bodies and the saved
                positions extract; the verdict counts and the series counts equal the recount; no write, no push, no deploy.

The checker RECOMPUTES from the private bodies and the worker's private positions extract (sha256 in the record). It cannot
re-read S3; the issuer spot-reads the newest partition at the drain.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest
"""
import datetime as dt
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

PRIV = Path("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~309")
BODY_FILES = ("hist_A.json", "hist_B.json")
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~313/SERIES_ENDED_CAUSE_R126.json"
END = "2026-10-13"
MAX_S3_READS = 200
VERDICTS = ("STALE_AT_SOURCE", "CLOSED_OR_TRANSFERRED", "NOT_DETERMINED")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "delete_object", "delete_objects", "copy_object", "put_item", "update_item",
                "create_multipart_upload", "put_parameter", "lambda_client", "invoke(", "start_execution")
VENDOR_TOKENS = ("requests.", "urllib.request", "http.client", "orionadvisor", "Authorization", "orion_session_jwt")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sha_str(s):
    return sha(str(s).encode("utf-8"))


def walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def _day(s):
    s = str(s)
    if "/" in s:
        return dt.datetime.strptime(s[:10], "%m/%d/%Y").date()
    return dt.date.fromisoformat(s[:10])


def key_of(raw):
    """An account key as the dimension carries it: a string, no '.0'."""
    try:
        return str(int(float(raw)))
    except (TypeError, ValueError):
        return None


def last_ends(body):
    """{account key: last end date} for the Account groups of one body that carry a series."""
    out = {}
    for g in walk(body):
        if g.get("$type") != "calculated-group" or g.get("grouping") != "Account":
            continue
        ends = [n.get("endDate") for n in walk(g) if n is not g and n.get("factor") is not None and n.get("endDate")]
        if ends:
            out[key_of(g.get("groupEntityId"))] = max(_day(e) for e in ends)
    return out


def verdict_of(n_after, held_on_newest):
    if n_after == 0:
        return "NOT_DETERMINED"
    return "STALE_AT_SOURCE" if held_on_newest else "CLOSED_OR_TRANSFERRED"


def measure(last_end, extract_values, partitions):
    """(n_after, held_days, held_on_newest) of one account from the extract: partitions strictly after its last series day
    up to the window end; held means a positive total value."""
    end = dt.date.fromisoformat(END)
    after = sorted(p for p in partitions if last_end < dt.date.fromisoformat(p[len("date="):]) <= end)
    vals = [extract_values.get(p) for p in after]
    held = [isinstance(v, (int, float)) and v > 0 for v in vals]
    return len(after), sum(held), bool(held and held[-1])


def recompute(bodies, extract):
    ends = {}
    for b in bodies:
        ends.update(last_ends(b))
    end = dt.date.fromisoformat(END)
    parts = extract.get("partitions") or []
    vals = extract.get("values") or {}
    accounts = []
    for key, last in ends.items():
        if last >= end:
            continue
        n_after, held_days, on_newest = measure(last, vals.get(key, {}), parts)
        accounts.append({"account_sha256": sha_str(key), "series_ended_days_before_window_end": (end - last).days, "partitions_after": n_after,
                         "held_days_after": held_days, "held_on_newest": on_newest, "verdict": verdict_of(n_after, on_newest)})
    accounts.sort(key=lambda a: a["account_sha256"])
    return len(ends), accounts


def no_identifiers(rec):
    """No run of 8 or more digits, except in a sha256 value or in a path or file field (the order names both as exempt)."""
    rec = json.loads(json.dumps(rec))
    for outer, inner in (("extract", "path"), ("script", "file")):
        if isinstance(rec.get(outer), dict) and inner in rec[outer]:
            rec[outer][inner] = ""
    text = re.sub(r"[0-9a-f]{64}", "", json.dumps(rec))
    for m in re.finditer(r"\d{8,}", text):
        need(False, "a run of 8 or more digits in the record: %s" % m.group(0)[:3])
    need("date=" not in text, "a partition name (a date) is in the record")


def script_clean(root, rel, want_sha):
    p = Path(root) / rel
    need(p.is_file(), "script %s is not a tracked file" % rel)
    b = p.read_bytes()
    need(sha(b) == want_sha, "script hash differs from the record")
    src = b.decode("ascii")
    for t in WRITE_TOKENS:
        need(t not in src, "script holds a write or invoke token: %s" % t)
    for t in VENDOR_TOKENS:
        need(t not in src, "script holds a vendor-call token: %s" % t)
    need("InflectionSilverReader" in src, "script must read through InflectionSilverReader (GET-only, granted prefixes)")


def check(root, priv=PRIV, rec_rel=REC_REL):
    rec = json.loads((Path(root) / rec_rel).read_bytes().decode("ascii"))
    no_identifiers(rec)
    for k in ("served_values_changed", "pushed", "deployed", "files_in_repo_private"):
        need(rec.get(k) is False, "%s must be false" % k)
    r = rec.get("reads", {})
    for k in ("s3_writes", "dynamodb_writes", "vendor_calls", "secret_reads"):
        need(r.get(k) == 0, "reads.%s must be 0" % k)
    need(isinstance(r.get("s3_reads"), int) and 0 < r["s3_reads"] <= MAX_S3_READS, "reads.s3_reads must be 1..%d" % MAX_S3_READS)
    need(isinstance(rec.get("basis_words"), str) and len(rec["basis_words"]) >= 200, "basis_words (>= 200 characters) missing")
    script_clean(root, rec["script"]["file"], rec["script"]["sha256"])
    bodies, body_shas = [], []
    for name in BODY_FILES:
        b = (Path(priv) / name).read_bytes()
        body_shas.append(sha(b))
        bodies.append(json.loads(b.decode("utf-8")))
    need(rec.get("bodies_sha256") == body_shas, "bodies_sha256 differs from the saved round-122 bodies")
    ex = rec.get("extract", {})
    ep = Path(ex.get("path", ""))
    need(ep.is_file() and sha(ep.read_bytes()) == ex.get("sha256"), "the private positions extract is missing or its hash differs")
    extract = json.loads(ep.read_bytes().decode("utf-8"))
    n_series, accounts = recompute(bodies, extract)
    need(rec.get("series_total") == n_series, "series_total: record %r recount %r" % (rec.get("series_total"), n_series))
    need(rec.get("cause_claim") == "inferred", "cause_claim must read inferred (absent from a complete partition; the account status is not read)")
    need(rec.get("early_end_count") == len(accounts), "early_end_count: record %r recount %r" % (rec.get("early_end_count"), len(accounts)))
    need(rec.get("accounts") == accounts, "per-account rows differ from the recompute")
    counts = {v: sum(1 for a in accounts if a["verdict"] == v) for v in VERDICTS}
    need(rec.get("verdict_counts") == counts, "verdict_counts differ from the recount")


def selftest():
    end = dt.date.fromisoformat(END)

    def body(acct, last):
        days = [(last - dt.timedelta(days=i)).strftime("%m/%d/%Y") for i in range(3)]
        return {"calculations": [{"$type": "calculated-group", "grouping": "Account", "groupEntityId": acct,
                                  "calculations": [{"series": [{"factor": 1.0, "endDate": d} for d in days]}]}]}
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        a_last, b_last, c_last = end - dt.timedelta(days=120), end - dt.timedelta(days=95), end
        bodies = [{"calculations": [body(11, a_last)["calculations"][0], body(33, c_last)["calculations"][0]]}, body(22, b_last)]
        parts = ["date=%s" % (end - dt.timedelta(days=i)).isoformat() for i in range(130)]
        vals = {"11": {p: 5.0 for p in parts}, "22": {p: (None if p > "date=2026-07-20" else 0.0) for p in parts}}
        n_series, accts = recompute(bodies, {"partitions": parts, "values": vals})
        need(n_series == 3 and len(accts) == 2, "selftest: counts")
        by = {a["account_sha256"]: a for a in accts}
        a = by[sha_str("11")]
        need(a["series_ended_days_before_window_end"] == 120 and a["partitions_after"] == 120 and a["held_days_after"] == 120 and a["verdict"] == "STALE_AT_SOURCE", "selftest: stale arm %r" % a)
        b = by[sha_str("22")]
        need(b["verdict"] == "CLOSED_OR_TRANSFERRED" and b["held_days_after"] == 0, "selftest: closed arm %r" % b)
        need(verdict_of(0, False) == "NOT_DETERMINED", "selftest: not determined arm")
        script = td / "s.py"
        script.write_bytes(b"from x import InflectionSilverReader\n")
        script_clean(td, "s.py", sha(script.read_bytes()))
        script.write_bytes(b"import requests.get\nInflectionSilverReader\n")
        try:
            script_clean(td, "s.py", sha(script.read_bytes()))
        except Fail:
            pass
        else:
            raise Fail("selftest: a vendor-call script passed")
        try:
            no_identifiers({"x": "12345678"})
        except Fail:
            pass
        else:
            raise Fail("selftest: an identifier-length run passed")
        no_identifiers({"extract": {"path": "C:/dev/_x_20261009/IRPT/y.json"}, "script": {"file": "org/a_20261009/b.py"}})
        try:
            no_identifiers({"extract": {"path": "ok"}, "note": "acct 20261009"})
        except Fail:
            pass
        else:
            raise Fail("selftest: a note outside the exempt fields passed")
    print("selftest PASS")


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        try:
            selftest()
        except Fail as exc:
            print("REASON: %s" % exc)
            print("selftest FAIL")
            return 1
        return 0
    root, cid = Path(argv[1]).resolve(), argv[2]
    try:
        need(cid == "DBI126-1-AC1", "unknown criterion %s" % cid)
        check(root)
    except FileNotFoundError as exc:
        print("REASON: no such file: %s" % Path(str(exc.filename)).name)
        print("%s FAIL" % cid)
        return 1
    except Fail as exc:
        print("REASON: %s" % exc)
        print("%s FAIL" % cid)
        return 1
    except Exception as exc:  # a crash is a FAIL with its type named, never a pass
        print("REASON: %s: %s" % (type(exc).__name__, str(exc)[:300]))
        print("%s FAIL" % cid)
        return 1
    print("%s PASS" % cid)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
