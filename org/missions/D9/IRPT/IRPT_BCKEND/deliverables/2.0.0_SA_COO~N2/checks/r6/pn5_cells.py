"""IRPT_BCKEND workstream ~PN round 6 (issuer 2.0.0_SA_COO~N2) -- the checks of cell IB-pn-5: the Scope feed writes the raw Orion
replies ONCE per run (CTO ruling @2f780e14a6, option B) instead of embedding them in every day's bronze envelope.

Usage: python <this file> <repo_root> <criterion_id> | python <this file> <repo_root> GOLDEN
Prints "<id> PASS" or "<id> FAIL: <reason>" last, exit 0 or 1. GOLDEN prints the silver sha256 of the fixtures (run at the BASE).

  IBN5-AC1  on a 3-day fixture the run writes exactly ONE raw object (not under a date= partition) and 3 day envelopes; each
            envelope has schema orion-scope-account-returns-bronze-v2, no "responses" member, keeps its metadata, and carries
            raw_object {"key", "sha256"} naming that one object, whose stored bytes hash to the sha256; the raw object holds
            every household's reply UNCHANGED (equal to the fixture reply, not sliced)
  IBN5-AC2  difference control: the silver bytes of a 1-day run and of each day of the 3-day run hash to the values the
            pre-change writer produced (GOLDEN_*), and the peak memory (tracemalloc) of the 3-day run is printed
  IBN5-AC3  the run object's address is lib/opal_naming address() output via run_object_address(pull_date, window_start, digest);
            the script holds no "s3://" and no "orion/inflection" literal; the new test file has at least 3 tests; the
            tests of data/inf/manual_api pass
"""
import gzip
import hashlib
import json
import re
import subprocess
import sys
import tracemalloc
from pathlib import Path

RAW_SCHEMA = "orion-scope-account-returns-bronze-v2"
ENVELOPE_KEYS = ("schema", "source", "scope", "table", "day", "pull_date", "window", "fee_basis", "calc_gross_of_fees",
                 "calls", "households_failed", "universe_rows", "households_without_id")
GOLDEN_ONE = "36ee30749b05326ec2d5813d4c1557696c8b1728b6687c7bc1b8dd559ecbc0c9"
GOLDEN_THREE = {"2026-10-12": "ee4080b14d86b9ac5ef438d51bb0bce6b2753e69fdd9a60a02a2c20a644265a5", "2026-10-13": "7bbf5e2f83d3569bc82f3ae14c2d76e529cfcda0fe5dfdcafb7337541b833569", "2026-10-14": "ca2e19f0e57b389adcddefec6880ea5b01c51f1ffed58d1280a1d3b6de5a781b"}
MANUAL = "data/inf/manual_api"
NEW_TEST = MANUAL + "/test_scope_feed_run_object.py"
SCRIPT = MANUAL + "/pull_inflection_scope_account_returns.py"
THREE_DAYS = ("2026-10-12", "2026-10-13", "2026-10-14")


def fail(cid, why):
    print("%s FAIL: %s" % (cid, why))
    sys.exit(1)


def need(cid, cond, why):
    if not cond:
        fail(cid, why)


def modules(root):
    for p in (root / MANUAL, root / "lib"):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    import pull_inflection_scope_account_returns as M
    import test_scope_feed_day_complete as T
    return M, T


def responses_for(T, days):
    pts = lambda f: [T._point(d, f + i * 0.001) for i, d in enumerate(days)]  # noqa: E731
    h1 = T._response([T._group(7001, series=pts(1.10)), T._group(7003, series=None)])
    h2 = T._response([T._group(7004, series=pts(1.04))])
    return {5001: h1, 5002: h2}


def run_days(root, days, from_date):
    M, T = modules(root)
    s3 = T._fixture_s3()
    s3.before = set(s3.objects)
    responses = responses_for(T, days)
    code, transport, _ = T._run(s3, responses, from_date=from_date)
    return M, T, s3, responses, code


def silver_sha(M, s3, day):
    bucket, key = M._split(M.feed_addresses(day)[1])
    return hashlib.sha256(s3.objects[(bucket, key)]).hexdigest()


def envelope(M, s3, day):
    bucket, key = M._split(M.feed_addresses(day)[0])
    return json.loads(gzip.decompress(s3.objects[(bucket, key)]).decode("ascii"))


def ac1(root):
    cid = "IBN5-AC1"
    M, T, s3, responses, code = run_days(root, THREE_DAYS, "2026-10-12")
    need(cid, code == 0, "the 3-day fixture run did not exit 0")
    day_keys = {M._split(a) for d in THREE_DAYS for a in M.feed_addresses(d)}
    new_keys = set(s3.objects) - s3.before
    need(cid, day_keys <= new_keys, "the 3 days' bronze and silver keys were not all written")
    extra = sorted(k[1] for k in new_keys if k not in day_keys)
    need(cid, len(extra) == 1, "expected exactly ONE raw object besides the 3 days' bronze and silver keys, found %d" % len(extra))
    raw_key = extra[0]
    need(cid, "date=" not in raw_key, "the raw object must not sit under a date= partition: " + raw_key)
    raw_bytes = [v for (b, k), v in s3.objects.items() if k == raw_key][0]
    digest = hashlib.sha256(raw_bytes).hexdigest()
    try:
        raw = json.loads(gzip.decompress(raw_bytes).decode("ascii"))
    except (OSError, ValueError):
        fail(cid, "the raw object is not gzip JSON")
    replies = {r["household_token"]: r["body"] for r in raw.get("responses", [])}
    expect = {M.token_of(h): body for h, body in responses.items()}
    need(cid, replies == expect, "the raw object must hold every household's reply unchanged")
    for day in THREE_DAYS:
        env = envelope(M, s3, day)
        need(cid, env.get("schema") == RAW_SCHEMA, "%s: schema must be %s" % (day, RAW_SCHEMA))
        need(cid, "responses" not in env, "%s: the envelope must carry no responses member" % day)
        need(cid, all(k in env for k in ENVELOPE_KEYS), "%s: the envelope lost a metadata member" % day)
        need(cid, len(env["calls"]) == 2 and env["window"] == {"start": "2026-10-12", "end": "2026-10-14"},
             "%s: calls or window changed" % day)
        ro = env.get("raw_object", {})
        need(cid, ro.get("sha256") == digest, "%s: raw_object.sha256 does not hash the stored raw object" % day)
        need(cid, isinstance(ro.get("key"), str) and ro["key"].endswith(raw_key), "%s: raw_object.key does not name the one raw object" % day)


def ac2(root):
    cid = "IBN5-AC2"
    M, T, s3, _responses, code = run_days(root, ("2026-10-14",), "2026-10-14")
    need(cid, code == 0, "the 1-day fixture run did not exit 0")
    need(cid, silver_sha(M, s3, "2026-10-14") == GOLDEN_ONE, "1-day silver bytes differ from the pre-change writer's")
    tracemalloc.start()
    M, T, s3, _responses, code = run_days(root, THREE_DAYS, "2026-10-12")
    _cur, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    need(cid, code == 0, "the 3-day fixture run did not exit 0")
    for day in THREE_DAYS:
        need(cid, silver_sha(M, s3, day) == GOLDEN_THREE[day], "%s: silver bytes differ from the pre-change writer's" % day)
    print("PEAK_MEMORY_BYTES=%d (3-day fixture, tracemalloc)" % peak)
    need(cid, peak > 0, "peak memory not measured")


def ac3(root):
    cid = "IBN5-AC3"
    M, _T = modules(root)
    need(cid, hasattr(M, "run_object_address"), "run_object_address(pull_date, window_start, digest) is absent")
    digest = "a" * 64
    addr = M.run_object_address("2026-10-14", "2026-10-12", digest)
    need(cid, isinstance(addr, str) and addr.startswith("s3://") and digest[:12] in addr, "the run object address does not carry the digest")
    builder = M._builder()
    need(cid, builder is not None, "lib/opal_naming does not import in this tree")
    base = builder.address(M.SOURCE, M.SCOPE, "bronze", M.TABLE, "run=x")
    need(cid, addr.startswith(base.rsplit("/run=x", 1)[0] + "/"), "the address is not under the builder's bronze table home")
    text = (root / SCRIPT).read_text(encoding="utf-8")
    need(cid, "s3://" not in text and "orion/inflection" not in text, "the script types an address literal (CLAUDE.md rule 30)")
    nt = root / NEW_TEST
    need(cid, nt.is_file() and len(re.findall(r"^def test_", nt.read_text(encoding="utf-8"), re.M)) >= 3, "the new test file is absent or holds fewer than 3 tests")
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(root / MANUAL)],
                         capture_output=True, text=True, timeout=110, cwd=str(root))
    need(cid, out.returncode == 0, "the tests of %s fail: %s" % (MANUAL, (out.stdout.strip().splitlines() or ["-"])[-1]))


CHECKS = {"IBN5-AC1": ac1, "IBN5-AC2": ac2, "IBN5-AC3": ac3}


def golden(root):
    M, T, s3, _r, code = run_days(root, ("2026-10-14",), "2026-10-14")
    print("GOLDEN_ONE =", silver_sha(M, s3, "2026-10-14"), "exit", code)
    M, T, s3, _r, code = run_days(root, THREE_DAYS, "2026-10-12")
    for day in THREE_DAYS:
        print("GOLDEN_THREE[%s] = %s" % (day, silver_sha(M, s3, day)), "exit", code)


if __name__ == "__main__":
    if len(sys.argv) != 3 or (sys.argv[2] not in CHECKS and sys.argv[2] != "GOLDEN"):
        print("usage: pn5_cells.py <repo_root> <%s|GOLDEN>" % "|".join(CHECKS))
        sys.exit(2)
    root_ = Path(sys.argv[1]).resolve()
    if sys.argv[2] == "GOLDEN":
        golden(root_)
    else:
        CHECKS[sys.argv[2]](root_)
        print("%s PASS" % sys.argv[2])
