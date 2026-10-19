"""Control for pn5_cells.py (cell IB-pn-5). Builds, IN MEMORY, a patched copy of the Scope feed script that does what the CTO ruling
(@2f780e14a6, option B) asks, runs AC1 and AC2 of the check against it (both must PASS), then runs variants that each break ONE
rule (each must fail only its own arm). The patch is a control for the CHECK; it is not the fix and is never written to the tree.
AC3 needs the worker's new test file and updated tests, so its parts are exercised only at the base (it must FAIL there).
Usage: python control_pn5.py <repo_root>. Prints one line per arm and "unexpected: <n>"."""
import importlib.util
import io
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pn5_cells as P  # noqa: E402

OLD_ENV = '''        envelope = {"schema": "orion-scope-account-returns-bronze-v1", "source": SOURCE, "scope": SCOPE,
                    "table": TABLE, "day": day, "pull_date": pull_date,
                    "window": {"start": window_start.isoformat(), "end": pull.isoformat()},
                    "fee_basis": FEE_BASIS, "calc_gross_of_fees": False,
                    "calls": day_calls,
                    "households_failed": failed, "universe_rows": len(universe_by_day[day]),
                    "households_without_id": no_household_by_day[day],
                    "responses": [{"household_token": c["household_token"], "body": c["response"]}
                                  for c in calls if c.get("response") is not None]}
        bronze_bytes = gzip.compress(json.dumps(envelope, sort_keys=True).encode("ascii"))'''
NEW_ENV = '''        envelope = {"schema": "@SCHEMA@", "source": SOURCE, "scope": SCOPE,
                    "table": TABLE, "day": day, "pull_date": pull_date,
                    "window": {"start": window_start.isoformat(), "end": pull.isoformat()},
                    "fee_basis": FEE_BASIS, "calc_gross_of_fees": False,
                    "calls": day_calls,
                    "households_failed": failed, "universe_rows": len(universe_by_day[day]),
                    "households_without_id": no_household_by_day[day],
                    "raw_object": {"key": RAW_ADDR, "sha256": RAW_DIGEST}@EXTRA@}
        bronze_bytes = gzip.compress(json.dumps(envelope, sort_keys=True).encode("ascii"))'''
OLD_LOOP = "    complete = _complete_days(days, universe_by_day, ok_hh)\n    for day in complete:\n        universe = [r for r in universe_by_day[day] if r[\"household_id\"] in ok_hh]\n        rows = _day_rows(universe, groups_by_hh, pull_date, window_start, pull, observed_by_hh, last_updated)"
RAW_BLOCK = '''    complete = _complete_days(days, universe_by_day, ok_hh)
    _raw = {"schema": "orion-scope-raw-replies-v1", "pull_date": pull_date,
            "responses": [{"household_token": c["household_token"], "body": @BODY@}
                          for c in calls if c.get("response") is not None]}
    RAW_BYTES = gzip.compress(json.dumps(_raw, sort_keys=True).encode("ascii"))
    RAW_DIGEST = @DIGEST@
    RAW_ADDR = run_object_address(pull_date, window_start, RAW_DIGEST)
    _bucket, _key = _split(RAW_ADDR)
    if not s3.exists(_bucket, _key):
        s3.put_bytes(_bucket, _key, RAW_BYTES, "application/gzip")
    @SECOND@
    for day in complete:
        universe = [r for r in universe_by_day[day] if r["household_id"] in ok_hh]
        rows = _day_rows(universe, groups_by_hh, pull_date, window_start, pull, observed_by_hh, last_updated)'''
ADDR_FUNC = '''

def run_object_address(pull_date, window_start, digest):
    """The run-level raw object: lib/opal_naming address() output, content-addressed by its sha256."""
    return _builder().address(SOURCE, SCOPE, "bronze", TABLE, "run=%s" % pull_date, "%s_%s.json.gz" % (window_start, digest[:12]))
'''


def build(root, schema="orion-scope-account-returns-bronze-v2", keep_responses=False, body="c[\"response\"]",
          digest='__import__("hashlib").sha256(RAW_BYTES).hexdigest()', second_object=False, silver_change=False, no_addr_func=False):
    src = (root / P.SCRIPT).read_text(encoding="utf-8")
    assert OLD_ENV in src and OLD_LOOP in src, "the script no longer has the base shape the control patches"
    env = NEW_ENV.replace("@SCHEMA@", schema)
    env = env.replace("@EXTRA@", ',\n                    "responses": [{"household_token": c["household_token"], "body": c["response"]}'
                      ' for c in calls if c.get("response") is not None]' if keep_responses else "")
    src = src.replace(OLD_ENV, env)
    second = ('_b2, _k2 = _split(run_object_address(pull_date, window_start, "f" * 64)); s3.put_bytes(_b2, _k2, b"x", "application/gzip")'
              if second_object else "pass")
    src = src.replace(OLD_LOOP, RAW_BLOCK.replace("@BODY@", body).replace("@DIGEST@", digest).replace("@SECOND@", second))
    if silver_change:
        src = src.replace("_silver_frame(rows).to_parquet(buf, index=False)", "_silver_frame(rows).assign(extra_col=1).to_parquet(buf, index=False)")
    if not no_addr_func:
        src = src.replace('\nif __name__ == "__main__":', ADDR_FUNC + '\n\nif __name__ == "__main__":')
    return src


def install(root, src):
    path = root / P.SCRIPT
    spec = importlib.util.spec_from_loader("pull_inflection_scope_account_returns", loader=None)
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(path)
    sys.modules["pull_inflection_scope_account_returns"] = module
    exec(compile(src, str(path), "exec"), module.__dict__)  # noqa: S102 (a control for a check, in memory only)
    return module


def arm(root, cid, src):
    for name in [m for m in sys.modules if m == "pull_inflection_scope_account_returns"]:
        del sys.modules[name]
    install(root, src)
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        P.CHECKS[cid](root)
        verdict = "PASS"
    except SystemExit:
        verdict = "FAIL: " + (buf.getvalue().strip().splitlines() or ["-"])[-1]
    finally:
        sys.stdout = old
    return verdict


def main(repo):
    root = Path(repo).resolve()
    unexpected = 0
    good = build(root)
    for cid in ("IBN5-AC1", "IBN5-AC2"):
        v = arm(root, cid, good)
        print("POSITIVE %-9s %s" % (cid, v[:60]))
        unexpected += v != "PASS"
    variants = [
        ("responses still embedded", dict(keep_responses=True), "IBN5-AC1"),
        ("schema not bumped", dict(schema="orion-scope-account-returns-bronze-v1"), "IBN5-AC1"),
        ("sha256 of the wrong bytes", dict(digest='"0" * 64'), "IBN5-AC1"),
        ("raw reply altered (sliced)", dict(body='dict(c["response"], sliced=True)'), "IBN5-AC1"),
        ("a second object written", dict(second_object=True), "IBN5-AC1"),
        ("silver bytes changed", dict(silver_change=True), "IBN5-AC2"),
    ]
    for label, kw, own in variants:
        other = "IBN5-AC2" if own == "IBN5-AC1" else "IBN5-AC1"
        mine, theirs = arm(root, own, build(root, **kw)), arm(root, other, build(root, **kw))
        ok = mine.startswith("FAIL") and theirs == "PASS"
        print("%-30s fails %s only: %s   (%s | %s)" % (label, own, "OK" if ok else "UNEXPECTED", mine[:50], theirs[:20]))
        unexpected += not ok
    v = arm(root, "IBN5-AC3", build(root, no_addr_func=True))
    ok = v.startswith("FAIL") and "run_object_address" in v
    print("%-30s fails IBN5-AC3: %s (%s)" % ("run_object_address absent", "OK" if ok else "UNEXPECTED", v[:60]))
    unexpected += not ok
    print("unexpected:", unexpected)
    return 1 if unexpected else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
