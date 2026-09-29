"""Sweep-2 section 1 (1.0.0_SA_CTO ROUND_ANALYSIS.sweep2.md): every served period on a COLD container of the BUILT
irpt-performance-adapter artifact, before apply -- each a figure or a named refusal, never UNEXPECTED.

Usage: python adapter_cold_periods.py <built zip> <account suffix> [<account suffix> ...]
In a fresh interpreter whose import path is ONLY the extracted zip (repo paths stripped; the function's environment
with /var/task mapped to the extraction), `installed.build_runtime` composes the service over the REAL S3 client and a
table stub that refuses every call (the 49F holdings path never touches the table). For each 49F account (raw key found
by its last digits in the latest gold partition) and each period -- YTD, QTD, 1Y, 3Y by the packaged
`parity_period_returns.period_window` at the latest gold date, and Since inception (1970-01-01) -- it calls
`holdings_gold.calculate` with the composed holdings port and classifies any exception by the built Entry's own reasons
table (MRO walk, as the boundary does). Read-only: S3 list/get only.
Pass: no answer is UNEXPECTED.
"""
import os
import subprocess
import sys
import tempfile
import zipfile

import boto3

zpath, suffixes = sys.argv[1], sys.argv[2:]
repo = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 9)).replace("\\", "/").lower()
d = tempfile.mkdtemp(prefix="adapter_cold_")
zipfile.ZipFile(zpath).extractall(d)
cfg = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName="irpt-performance-adapter")
env = dict(os.environ)
for k, v in (cfg.get("Environment") or {}).get("Variables", {}).items():
    env[k] = v.replace("/var/task", d.replace("\\", "/"))
env.setdefault("AWS_DEFAULT_REGION", "us-east-1")

PROBE = r'''
import sys, os, json, time
REPO = %(repo)r
sys.path[:] = [p for p in sys.path if p and not p.replace(chr(92), "/").lower().startswith(REPO)]
sys.path.insert(0, ".")
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
src = svc.holdings_source
print("composed: holdings_source", type(src).__name__, src.describe(), "| reasons", len(reasons))
import holdings_gold, tenants, parity_period_returns as ppr, datetime
from ids import opaque_account
days = src.partition_dates()
end = days[-1]
keys = src.account_keys(end)
def classify(exc):
    for cls in type(exc).__mro__:
        if cls.__name__ in reasons:
            return reasons[cls.__name__]
    return "UNEXPECTED"
windows = []
for p in ("YTD", "QTD", "1Y"):
    w = ppr.period_window(p, datetime.date.fromisoformat(end))
    windows.append((p, w[0].isoformat() if w else None))
# 3Y is outside the packaged ruled set (QTD, YTD, 1Y, SI), so the page's 3Y window is 1Y's start moved back two years.
one_y = dict(windows)["1Y"]
windows.append(("3Y", str(int(one_y[:4]) - 2) + one_y[4:] if one_y else None))
windows.append(("SI", "1970-01-01"))
print("latest gold date", end, "| partitions", len(days), "| windows", windows)
unexpected = missing = 0
accounts = []
for want in %(suffixes)r:
    hits = [k for k in keys if k.endswith(want)]
    if not hits:
        print("account ..%%s: no raw key in %%s" %% (want, end)); missing += 1
    accounts.extend(hits)
for raw in accounts:
    suffix = raw[-6:]
    canon = opaque_account(tenants._CANONICAL_49F, raw)
    scope = {"verified_request_firm_id": tenants._LEGACY_SHORT_ID["49F"], "permitted_account_set": [canon],
             "resolved_scope": {"scope_ids": [canon]}}
    for period, start in windows:
        t0 = time.perf_counter()
        if start is None:
            print("  ..%%s %%-3s no window at %%s" %% (suffix, period, end)); continue
        try:
            out = holdings_gold.calculate(scope, start, end, src)
            v = out["report"]["returns"]["account_detail"][0]["value"]
            dates = out["report"].get("dates") or {}
            print("  ..%%s %%-3s %%s..%%s FIGURE %%+.4f%%%%  provider %%s  actual %%s..%%s  %%.1fs" %% (suffix, period, start, end, v * 100,
                  out["report"]["lineage"]["provider"], dates.get("actual_start"), dates.get("actual_end"), time.perf_counter() - t0))
        except Exception as exc:
            code = classify(exc)
            unexpected += code == "UNEXPECTED"
            print("  ..%%s %%-3s %%s..%%s REFUSED %%s (%%s: %%s)  %%.1fs" %% (suffix, period, start, end, code, type(exc).__name__, str(exc)[:90], time.perf_counter() - t0))
print("accounts probed:", len(accounts), "| suffixes not found:", missing)
print("UNEXPECTED answers:", unexpected + missing)
'''
r = subprocess.run([sys.executable, "-c", PROBE % {"repo": repo, "suffixes": suffixes}], capture_output=True, text=True, cwd=d, env=env)
out = (r.stdout or "") + (r.stderr or "")[-1500:]
print(out.strip())
ok = r.returncode == 0 and "UNEXPECTED answers: 0" in (r.stdout or "")
print("ADAPTER COLD PERIODS PASS" if ok else "ADAPTER COLD PERIODS FAIL")
sys.exit(0 if ok else 1)
