"""POSN_TENANCY TO-2-DS -- the presence probe. READ-ONLY: list-objects-v2 only.

WHY MANUAL PAGINATION AND NOT THE CLI'S AUTO-PAGINATE:
  T2DS-AC1 requires a COMPLETE listing with NextToken shown ABSENT or paginated to
  exhaustion. The CLI's auto-paginate MERGES pages and DROPS IsTruncated/NextToken
  from the merged object, so the very field the criterion asks me to show is the one
  auto-paginate removes -- and `KeyCount` reads absent for every prefix (banked).
  So each page is fetched with --no-paginate and the loop terminates ONLY on
  IsTruncated == False, which is exhaustion PROVEN rather than assumed.
  --max-items and head are BANNED by the TO and appear nowhere here.

EVERY probe records: pages fetched, keys found, and the terminal IsTruncated.
An EMPTY result and a FAILED retrieval are NOT the same thing and are not allowed to
render the same: a non-zero rc raises, so a failure can never be reported as an absence.
"""
import json
import os
import subprocess
import sys

# Native Windows python cannot exec the bash shim `.tools/aws`, and a RELATIVE
# path fails CreateProcess. Resolve the .cmd sibling to an ABSOLUTE native path.
# Forward slashes only in the literal -- a backslash here becomes a real escape
# when this file is authored through a shell (banked: '\a' ate '.tools\aws').
AWS = os.path.abspath(os.path.join(os.getcwd(), ".tools/aws.cmd"))
if not os.path.exists(AWS):
    raise SystemExit("ERROR: aws shim not found at %s -- fail closed loud rather "
                     "than reporting an absence produced by a missing tool." % AWS)


def list_all(bucket, prefix):
    """Returns (keys, pages, truncated_final, error). Exhaustion is PROVEN by the loop."""
    keys, pages, token = [], 0, None
    while True:
        cmd = [AWS, "s3api", "list-objects-v2", "--bucket", bucket,
               "--prefix", prefix, "--output", "json", "--no-paginate"]
        if token:
            cmd += ["--continuation-token", token]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode != 0:
            # A FAILED RETRIEVAL RETURNS A VALUE. It must never render as an absence.
            return (keys, pages, None, p.stderr.decode("utf-8", "replace").strip()[:200])
        body = json.loads(p.stdout or b"{}")
        pages += 1
        keys += [c["Key"] for c in body.get("Contents", [])]
        if body.get("IsTruncated"):
            token = body.get("NextContinuationToken")
            if not token:
                return (keys, pages, True, "IsTruncated=True but NO NextContinuationToken")
        else:
            return (keys, pages, False, None)


def probe(label, bucket, prefix, expect):
    keys, pages, trunc, err = list_all(bucket, prefix)
    print("-" * 74)
    print("PROBE  %s" % label)
    print("  s3://%s/%s" % (bucket, prefix))
    if err:
        print("  ERROR: retrieval FAILED -- this is NOT an absence: %s" % err)
        return {"label": label, "bucket": bucket, "prefix": prefix,
                "outcome": "RETRIEVAL-FAILED", "error": err, "expect": expect}
    print("  pages fetched      : %d" % pages)
    print("  terminal IsTruncated: %s   <- False == exhaustion PROVEN" % trunc)
    print("  KEYS FOUND         : %d      (expect: %s)" % (len(keys), expect))
    for k in keys[:40]:
        print("      %s" % k)
    if len(keys) > 40:
        print("      ... and %d more (full set counted, not truncated for the COUNT)"
              % (len(keys) - 40))
    return {"label": label, "bucket": bucket, "prefix": prefix,
            "outcome": "EMPTY" if not keys else "NON-EMPTY",
            "pages": pages, "is_truncated_final": trunc,
            "key_count": len(keys), "keys": keys, "expect": expect}


def main():
    results = []
    print("=" * 74)
    print("POSN_TENANCY TO-2-DS -- Cottonwood Positioning presence at the SERVED KEY")
    print("=" * 74)

    # --- AC1: the SERVED Positioning prefix, complete -----------------------
    results.append(probe(
        "AC1-a  SERVED Positioning prefix (whole prefix, every key)",
        "opal-data-portal-v2", "json/positioning/",
        "the unscoped artifact; ANY firm-scoped key would show here"))

    # --- AC1: is there ANY cottonwood-scoped key on the served bucket? ------
    results.append(probe(
        "AC1-b  ANY 'cotton' key anywhere on the SERVED bucket",
        "opal-data-portal-v2", "json/",
        "0 cottonwood-scoped keys (filtered below)"))

    # --- AC1: Cottonwood's data HOME ---------------------------------------
    results.append(probe(
        "AC1-c  Cottonwood's data HOME (legacy per-firm bucket)",
        "opal-data-cot", "",
        "a home that exists; NO Positioning data in it"))

    # --- AC2: POSITIVE CONTROL on the probe --------------------------------
    results.append(probe(
        "AC2-a  POSITIVE CONTROL -- same probe, same form, prefix known NON-EMPTY",
        "opal-data-portal-v2", "json/positioning/",
        "NON-EMPTY: proves the probe can find keys when they exist"))

    results.append(probe(
        "AC2-b  POSITIVE CONTROL -- a firm home known to hold data",
        "opal-data-49financial", "",
        "NON-EMPTY: proves the probe works against a FIRM bucket, not just the served one"))

    out = "posn_probe_results.json"
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(results, fh, indent=2)
    print("-" * 74)
    print("full result set written to %s (the DENOMINATOR is an artifact, not this summary)"
          % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
