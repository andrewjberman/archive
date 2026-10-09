"""ops_probe.py -- MX-o-1 / MX-o-2 AC3 instrument: the reader's seam probe against its REAL neighbour (live served S3).

Imports the reader module from the gateway tree, calls it ONCE with a real boto3 S3 client and the Opal-internal
principal on the census's probe_scope, and grades the envelope (PRD v0.8 contracts 1 and 3):
  - rows >= 1, and EVERY row's key set equals the fixture's row key set exactly (tools/ops_kit/fixtures/<reader>.json);
  - scope stated and equal to the asked scope; as_of stated with as_of_claim == "measured"; completeness stated;
  - no row carries a fixture value as data (a row equal to any fixture row is a violation).
Read-only. Prints counts, keys and dates only, never a row value.
Usage: python ops_probe.py <gateway dir> <ops_trade_rec|ops_billing> <trade_rec|billing> <probe_scope>
"""
import json
import os
import sys

gw, pkg, reader, scope = sys.argv[1:5]
sys.path.insert(0, gw)
os.chdir(gw)
import boto3  # noqa: E402
from app.graphql_plumbing import catalog_gate as g  # noqa: E402

mod = __import__("app.integrations.%s.integration" % pkg, fromlist=["read"])
root = os.path.abspath(os.path.join(gw, "..", "..", "..", ".."))
fx = json.load(open(os.path.join(root, "tools", "ops_kit", "fixtures", reader + ".json"), encoding="utf-8"))
want = set(fx["rows"][0].keys())
env = mod.read(boto3.client("s3"), (g.OPAL_INTERNAL, ""), scope)
rows = env.get("rows") or []
bad = []
if not rows:
    bad.append("0 rows")
off = [sorted(set(r.keys()) ^ want) for r in rows if set(r.keys()) != want]
if off:
    bad.append("%d of %d rows differ from the fixture keys (first diff %s)" % (len(off), len(rows), off[0]))
if env.get("scope") != scope:
    bad.append("scope %r != asked %r" % (env.get("scope"), scope))
if not env.get("as_of") or env.get("as_of_claim") != "measured":
    bad.append("as_of %r claim %r (must be stated, claim measured)" % (env.get("as_of"), env.get("as_of_claim")))
if env.get("completeness") in (None, ""):
    bad.append("completeness not stated")
fxrows = [json.dumps(r, sort_keys=True) for r in fx["rows"]]
if any(json.dumps(r, sort_keys=True) in fxrows for r in rows):
    bad.append("a served row equals a fixture row (a fixture value is never served as data)")
for b in bad:
    print("VIOLATION: " + b)
print("probe %s tool=%s scope=%s: rows %d, fixture keys %d of %d rows exact; as_of=%s claim=%s; completeness=%s; violations %d"
      % (pkg, getattr(mod, "TOOL", None), scope, len(rows), len(rows) - len(off), len(rows), env.get("as_of"),
         env.get("as_of_claim"), "stated" if env.get("completeness") not in (None, "") else "absent", len(bad)))
sys.exit(0 if not bad else 1)
