"""All-accounts census of the BUILT irpt-performance-adapter's 49F answer, run as the adapter's own code (CRO 102752 (c):
the runners directory absent from the harness path; CTO 102736: the served rule, not a re-derivation).

Usage: python adapter_cold_census.py <built zip> [<end date>]
Same harness as adapter_cold_periods.py: a fresh interpreter whose import path is ONLY the extracted zip, the service
composed by `installed.build_runtime` over the real S3 client. For speed, and without changing any answer:
- the composed HoldingsGoldSource is wrapped so each partition object is read ONCE and handed back per account,
  and its partition listing is taken once and reused;
- `ids.opaque_account` (a pure hash) is memoized.
`holdings_gold.calculate` itself runs unchanged for every account with a row on the end date, for YTD, QTD, 1Y and
Since inception, and each exception is classified by the built Entry's own reasons table.
Prints per period: figures / named refusals by code / UNEXPECTED, and the accounts at or above +100% or at or below
-100%. Read-only (S3 list/get).
"""
import os
import subprocess
import sys
import tempfile
import zipfile

import boto3

zpath = sys.argv[1]
end_arg = sys.argv[2] if len(sys.argv) > 2 else ""
repo = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 9)).replace("\\", "/").lower()
d = tempfile.mkdtemp(prefix="adapter_census_")
zipfile.ZipFile(zpath).extractall(d)
cfg = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName="irpt-performance-adapter")
env = dict(os.environ)
for k, v in (cfg.get("Environment") or {}).get("Variables", {}).items():
    env[k] = v.replace("/var/task", d.replace("\\", "/"))
env.setdefault("AWS_DEFAULT_REGION", "us-east-1")

PROBE = r'''
import sys, os, collections, datetime, functools, time, logging
REPO = %(repo)r
sys.path[:] = [p for p in sys.path if p and not p.replace(chr(92), "/").lower().startswith(REPO)]
sys.path.insert(0, ".")
assert not any("runners_49f" in p for p in sys.path), "runners_49f on the harness path before composition"
import boto3
class RefuseTable:
    def __getattr__(self, name):
        raise AssertionError("table not expected on the 49F holdings path: " + name)
import entry
captured = {}
_orig = entry.build_entry
def _capture(service):
    captured["service"] = service
    captured["boundary"] = _orig(service)
    return captured["boundary"]
entry.build_entry = _capture
import installed
installed.build_runtime(table=RefuseTable(), s3=boto3.client("s3"), mapping_as_of=os.environ["IRPT_PERFORMANCE_MAPPING_AS_OF"],
                        transport_factory=lambda *a, **k: None)
svc, boundary = captured["service"], captured["boundary"]
reasons = getattr(boundary, "reasons", None) or {}
import holdings_gold, tenants, ids, parity_period_returns as ppr
logging.disable(logging.CRITICAL)
ids.opaque_account = functools.lru_cache(maxsize=None)(ids.opaque_account)
src = svc.holdings_source
_read = src._read
cache = {}
COLUMNS = ["account_id", "business_date", "daily_return", "account_value", "excluded_count", "excluded_weight", "status"]
def cached_read(day, account_key):
    # One compact copy per partition: the columns calculate() reads, sorted by account, sliced on demand.
    if day not in cache:
        receipt, frame = _read(day, None)
        frame = frame[[c for c in COLUMNS if c in frame.columns]].copy()
        frame["account_id"] = frame["account_id"].astype(str)
        frame = frame.sort_values("account_id", kind="stable").reset_index(drop=True)
        ids_ = frame["account_id"].to_numpy()
        bounds, start = {}, 0
        for i in range(1, len(ids_) + 1):
            if i == len(ids_) or ids_[i] != ids_[start]:
                bounds[ids_[start]] = (start, i)
                start = i
        cache[day] = (receipt, frame, bounds)
    receipt, frame, bounds = cache[day]
    if account_key is None:
        return receipt, frame
    a, b = bounds.get(account_key, (0, 0))
    return receipt, frame.iloc[a:b]
src._read = cached_read
src.max_workers = 1
days = src.partition_dates()
_days = list(days)
src.partition_dates = lambda: list(_days)  # one S3 listing, reused: the adapter lists once per answer
end = %(end)r or days[-1]
t0 = time.perf_counter()
for day in days:
    if day <= end:
        cached_read(day, None)
print("partitions cached", len(cache), "in %%.0fs" %% (time.perf_counter() - t0))
keys = src.account_keys(end)
windows = [(p, ppr.period_window(p, datetime.date.fromisoformat(end))[0].isoformat()) for p in ("YTD", "QTD", "1Y")]
windows.append(("SI", "1970-01-01"))
print("end", end, "| accounts with a row on the end date", len(keys), "| windows", windows)
def classify(exc):
    for cls in type(exc).__mro__:
        if cls.__name__ in reasons:
            return reasons[cls.__name__]
    return "UNEXPECTED"
total_unexpected = 0
for period, start in windows:
    t0 = time.perf_counter()
    counts, high, low, examples = collections.Counter(), [], [], {}
    for raw in keys:
        canon = ids.opaque_account(tenants._CANONICAL_49F, raw)
        scope = {"verified_request_firm_id": tenants._LEGACY_SHORT_ID["49F"], "permitted_account_set": [canon],
                 "resolved_scope": {"scope_ids": [canon]}}
        try:
            v = holdings_gold.calculate(scope, start, end, src)["report"]["returns"]["account_detail"][0]["value"]
            counts["FIGURE"] += 1
            if v >= 1.0:
                high.append((v, raw[-4:]))
            if v <= -1.0:
                low.append((v, raw[-4:]))
        except Exception as exc:
            code = classify(exc)
            counts[code] += 1
            examples.setdefault(code, "%%s: %%s" %% (type(exc).__name__, str(exc)[:80]))
    total_unexpected += counts["UNEXPECTED"]
    print("%%-3s %%s..%%s accounts %%d | %%s | >= +100%%%%: %%d | <= -100%%%%: %%d | %%.0fs" %% (period, start, end, len(keys),
          dict(counts), len(high), len(low), time.perf_counter() - t0))
    for v, s in sorted(high, reverse=True):
        print("    ..%%s %%+.2f%%%%" %% (s, v * 100))
    for v, s in sorted(low):
        print("    ..%%s %%+.2f%%%% (AT OR BELOW -100%%%%)" %% (s, v * 100))
    for code, ex in examples.items():
        print("    example %%s -- %%s" %% (code, ex))
print("UNEXPECTED answers:", total_unexpected)
'''
r = subprocess.run([sys.executable, "-c", PROBE % {"repo": repo, "end": end_arg}], capture_output=True, text=True, cwd=d, env=env)
print((r.stdout or "").strip())
if r.returncode:
    print((r.stderr or "")[-1500:])
ok = r.returncode == 0 and "UNEXPECTED answers: 0" in (r.stdout or "")
print("ADAPTER COLD CENSUS PASS" if ok else "ADAPTER COLD CENSUS FAIL")
sys.exit(0 if ok else 1)
