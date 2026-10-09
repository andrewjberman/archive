"""DB-6-AC1 -- the 1,498.38 USD flow residual on acct#89d0916a is named from landed responses.

Reads the worker's record
  org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/FLOW_RESIDUAL_acct#89d0916a_R2.json
and grades:
  1. account == "acct#89d0916a" and vendor_calls == 0;
  2. abs(abs(residual_usd) - 1498.38) <= 0.01;
  3. leg_named is one of the closed set below and leg_explanation is non-empty;
  4. legs is non-empty; every leg carries an s3:// key and a numeric amount_usd; the legs flagged
     "is_residual": true sum (in absolute value) to within 0.01 of abs(residual_usd);
  5. every cited s3:// key exists (head_object), denominator printed.
Usage: python <this file> <repo_root>
"""
import json
import sys
from pathlib import Path

LEG_NAMED = {"IN_KIND_VALUED_DIFFERENTLY", "INTERNAL_HERE_EXTERNAL_AT_VENDOR", "OTHER"}
TARGET = 1498.38
TOL = 0.01


def fail(msg):
    print("FAIL: " + msg)
    print("DB-6-AC1 FAIL")
    sys.exit(1)


def _REAL(token):
    """Resolve an acct# token to the real account id at run time from the private evidence dir (outside the repo)."""
    import json as _json
    import os as _os
    d = _os.environ.get("IRPT_PRIVATE_EVIDENCE_DIR")
    if not d:
        raise SystemExit("REFUSE: IRPT_PRIVATE_EVIDENCE_DIR is not set; this historical script needs the private account map")
    p = _os.path.join(d, "account_map_49financial.json")
    if not _os.path.isfile(p):
        raise SystemExit("REFUSE: account_map_49financial.json is absent from IRPT_PRIVATE_EVIDENCE_DIR")
    with open(p, encoding="utf-8") as fh:
        m = _json.load(fh)
    if token not in m:
        raise SystemExit("REFUSE: token %s is not in the account map" % token)
    return m[token]


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    rec_path = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/FLOW_RESIDUAL_acct#89d0916a_R2.json"
    if not rec_path.is_file():
        fail("no record at %s" % rec_path)
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    if rec.get("account") != _REAL("acct#89d0916a"):
        fail("account %r != acct#89d0916a" % rec.get("account"))
    if rec.get("vendor_calls") != 0:
        fail("vendor_calls %r != 0" % rec.get("vendor_calls"))
    try:
        residual = float(rec["residual_usd"])
    except (KeyError, TypeError, ValueError):
        fail("residual_usd missing or not numeric")
    if abs(abs(residual) - TARGET) > TOL:
        fail("residual_usd %.2f is not 1,498.38 within 0.01" % residual)
    if rec.get("leg_named") not in LEG_NAMED:
        fail("leg_named %r not in %s" % (rec.get("leg_named"), sorted(LEG_NAMED)))
    if not str(rec.get("leg_explanation") or "").strip():
        fail("leg_explanation is empty")
    legs = rec.get("legs")
    if not isinstance(legs, list) or not legs:
        fail("legs is empty")
    keys = []
    resid_sum = 0.0
    for i, leg in enumerate(legs):
        key = str(leg.get("key") or "")
        if not key.startswith("s3://"):
            fail("leg %d carries no s3:// key" % i)
        try:
            amount = float(leg["amount_usd"])
        except (KeyError, TypeError, ValueError):
            fail("leg %d amount_usd missing or not numeric" % i)
        if leg.get("is_residual") is True:
            resid_sum += abs(amount)
        keys.append(key)
    if abs(resid_sum - abs(residual)) > TOL:
        fail("legs flagged is_residual sum to %.2f, not %.2f" % (resid_sum, abs(residual)))
    try:
        import boto3
        s3 = boto3.client("s3")
    except Exception as exc:  # noqa: BLE001
        fail("boto3 unavailable: %s" % exc)
    found = 0
    for key in sorted(set(keys)):
        bucket, _, obj = key[len("s3://"):].partition("/")
        try:
            s3.head_object(Bucket=bucket, Key=obj)
            found += 1
        except Exception as exc:  # noqa: BLE001
            fail("cited key does not resolve: %s (%s)" % (key, exc.__class__.__name__))
    print("OK: %d of %d cited keys exist; residual %.2f; leg %s" % (found, len(set(keys)), residual, rec["leg_named"]))
    print("DB-6-AC1 PASS")


if __name__ == "__main__":
    main()
