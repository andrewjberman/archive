"""r10_host.py -- runs ON the gateway host (shipped via SSM by r10.AC2.sh) under /opt/opal-gateway/.venv/bin/python.
Loads /opt/opal-gateway/.env the way systemd's EnvironmentFile does (split at the first '='), NEVER through a shell.
Prints only counts, keys-equal flags, dates, claims and need ids; never a row value and never an env value.

argv: one token per reader, "<reader>=<SERVED|GAP>:<probe_scope>", e.g. "trade_rec=SERVED:49financial".
READ lines (FWD-19 live): for each SERVED reader, the DEPLOYED module's read() once under the Opal-internal principal:
  row count, rows whose keys equal the fixture's (keys from tools/ops_kit/fixtures @cc539738c6), scope, as_of, claim.
ROUTE lines: the deployed discover's first match for "trade reconciliation" and "billing".
"""
import os
import sys

ROOT = "/opt/opal-gateway"
with open(os.path.join(ROOT, ".env"), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v)
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import boto3  # noqa: E402
from app.graphql_plumbing import catalog_gate as g  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402

KEYS = {
    "trade_rec": {"account", "custodian", "trade_date", "symbol", "side", "quantity", "opal_status",
                  "custodian_status", "matched"},
    "billing": {"account", "household", "billing_period", "aum", "fee_rate_bps", "fee_amount", "status"},
}
PKG = {"trade_rec": "ops_trade_rec", "billing": "ops_billing"}
s3 = boto3.client("s3")
for tok in sys.argv[1:]:
    reader, rest = tok.split("=", 1)
    verdict, scope = rest.split(":", 1)
    if verdict != "SERVED":
        print("READ %s verdict=GAP skipped" % reader)
        continue
    try:
        mod = __import__("app.integrations.%s.integration" % PKG[reader], fromlist=["read"])
        env = mod.read(s3, (g.OPAL_INTERNAL, ""), scope)
        rows = env.get("rows") or []
        exact = sum(1 for r in rows if set(r.keys()) == KEYS[reader])
        print("READ %s verdict=SERVED rows=%d exact=%d scope_ok=%s as_of=%s claim=%s completeness=%s"
              % (reader, len(rows), exact, env.get("scope") == scope, env.get("as_of"), env.get("as_of_claim"),
                 "stated" if env.get("completeness") not in (None, "") else "absent"))
    except Exception as exc:  # noqa: BLE001
        print("READ %s verdict=SERVED Error %s" % (reader, type(exc).__name__))
for ask, want in (("trade reconciliation", "E-30"), ("billing", "E-31")):
    ms = od.discover(ask, g.OPAL_INTERNAL).get("matches", [])
    first = ms[0] if ms else {}
    got = (first.get("need") or {}).get("id") or first.get("dataset") or "NOT_CATALOGUED"
    print("ROUTE %s first=%s want=%s" % (ask.replace(" ", "_"), got, want))
