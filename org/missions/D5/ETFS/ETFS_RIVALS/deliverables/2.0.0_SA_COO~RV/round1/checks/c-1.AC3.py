"""RIV-c-1 AC3 -- homes are builder output: every address/name homes.py exposes equals address()/name() output,
and no product file in the package types the bucket or a resource name (CLAUDE.md rule 30)."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

NAMES = {
    "etfs-rivalfunds-daily": ("etfs", None, "rivalfunds", "daily"),
    "etfs-rivalfunds-daily-lambda": ("etfs", None, "rivalfunds", "lambda", "daily"),
    "etfs-rivalfunds-fetch-holdings-lambda": ("etfs", None, "rivalfunds", "lambda", "fetch-holdings"),
    "rivalfunds-build-silver-lambda": ("rivalfunds", None, "build-silver", "lambda"),
    "rivalfunds-build-canonical-shape-lambda": ("rivalfunds", None, "build-canonical-shape", "lambda"),
    "rivalfunds-publish-page-lambda": ("rivalfunds", None, "publish-page", "lambda"),
}


def run(v):
    root = c.setup_path()
    from lib.opal_naming import name
    from rivalfunds import homes

    exposed = homes.all_addresses("2026-09-29")
    expected = {
        "issuer_bronze": c.address("issuer-site", "etfs", "bronze", "holdings", "date=2026-09-29"),
        "issuer_silver": c.address("issuer-site", "etfs", "silver", "holdings", "date=2026-09-29"),
        "canonical_shape": c.address("rivalfunds", "etfs", "gold", "canonical_shape", "date=2026-09-29"),
        "trade_schedule": c.address("rivalfunds", "etfs", "gold", "trade_schedule", "date=2026-09-29"),
        "page": c.address("rivalfunds", "etfs", "platinum", "page", "date=2026-09-29"),
    }
    for k, want in expected.items():
        v.check(exposed.get(k) == want, f"homes.all_addresses()['{k}'] == {want} (got {exposed.get(k)})")
    for stage in ("fetch-holdings", "build-silver", "build-canonical-shape", "build-trade-schedule", "publish-page"):
        want = c.address("rivalfunds", "etfs", "state", stage, "date=2026-09-29")
        got = homes.marker_prefix(stage, "2026-09-29")
        v.check(got == want, f"homes.marker_prefix('{stage}') == {want} (got {got})")
    names = homes.all_names()
    for nm, args in NAMES.items():
        v.check(name(*args) == nm and nm in names.values(), f"homes.all_names() carries {nm} == name{args}")
    pkg = root / "data" / "etfs" / "scripts" / "rivalfunds"
    offenders = []
    for p in pkg.rglob("*.py"):
        if "tests" in p.parts:
            continue
        txt = p.read_text(encoding="utf-8")
        typed_uri = p.name != "sinks.py" and "s3://" in txt  # sinks.py parses URIs; nothing else types one
        if re.search(r"opal-data-etfs", txt) or typed_uri or any(nm in txt for nm in NAMES):
            offenders.append(str(p.relative_to(root)))
    v.check(not offenders, f"no typed bucket, s3:// literal or resource name in product files ({offenders})")


failures = c.guarded("AC3", run)
if failures == 0:
    print("AC3 RESULT: PASS 0 failures")
else:
    print(f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
