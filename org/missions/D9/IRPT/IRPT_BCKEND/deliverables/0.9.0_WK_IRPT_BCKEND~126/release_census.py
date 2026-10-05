"""Release census (IRPT_BCKEND IB-pr-323; CTO half condition 2 for release r54).

  census <built.zip> <live.zip> [--rules <json>] [--out <json>]
      Lists every member of the two zips as added / removed / changed (sha256 differs) / unchanged. Each added, removed or
      changed member is attributed to an order id by the rules file (path pattern -> order id), or else marked RIDER.
      Writes JSON {"members": [...], "counts": {...}, "riders": [...]} to --out (or stdout); exits 1 when any RIDER exists.
  fetch-live <function> --out <path> [--region us-east-1]
      Downloads the live bundle with boto3 lambda.get_function(...)['Code']['Location'] (a read only) to <path>.
      The presigned URL is never printed: any error text is scrubbed of it.

Rules file: either {"rules": [{"pattern": "<fnmatch>", "order": "<order id>"}, ...]}, a bare list of those objects, or a
mapping {"<fnmatch>": "<order id>"}. The first matching pattern wins. Patterns are matched against the member name.
"""
import argparse
import fnmatch
import hashlib
import json
import re
import sys
import zipfile

STATUSES = ("added", "removed", "changed", "unchanged")
_URL_RE = re.compile(r"https?://\S+")


def _digests(path):
    """member name -> sha256 hex of its bytes (directory entries skipped)."""
    out = {}
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            out[info.filename] = hashlib.sha256(zf.read(info.filename)).hexdigest()
    return out


def load_rules(path):
    """Returns an ordered list of (pattern, order id)."""
    if not path:
        return []
    with open(path, "rb") as fh:
        data = json.loads(fh.read().decode("utf-8"))
    if isinstance(data, dict) and "rules" in data:
        data = data["rules"]
    if isinstance(data, dict):
        return [(str(k), str(v)) for k, v in data.items()]
    return [(str(r["pattern"]), str(r["order"])) for r in data]


def attribute(name, rules):
    for pattern, order in rules:
        if fnmatch.fnmatchcase(name, pattern):
            return order
    return None


def census(built_zip, live_zip, rules=None):
    built, live = _digests(built_zip), _digests(live_zip)
    rules = rules or []
    members = []
    for name in sorted(set(built) | set(live)):
        if name not in live:
            status = "added"
        elif name not in built:
            status = "removed"
        elif built[name] != live[name]:
            status = "changed"
        else:
            status = "unchanged"
        row = {"member": name, "status": status, "built_sha256": built.get(name), "live_sha256": live.get(name)}
        if status == "unchanged":
            row["attribution"] = None
        else:
            order = attribute(name, rules)
            row["attribution"] = order if order else "RIDER"
        members.append(row)
    counts = {s: sum(1 for m in members if m["status"] == s) for s in STATUSES}
    counts["members"] = len(members)
    riders = [m["member"] for m in members if m["attribution"] == "RIDER"]
    counts["riders"] = len(riders)
    return {"built": str(built_zip), "live": str(live_zip), "members": members, "counts": counts, "riders": riders}


def _scrub(text):
    return _URL_RE.sub("<url-redacted>", str(text))


def fetch_live(function, out_path, region="us-east-1"):
    """get_function read -> download the code bundle. Never prints or returns the signed URL."""
    import urllib.request

    import boto3

    client = boto3.client("lambda", region_name=region)
    resp = client.get_function(FunctionName=function)
    url = resp["Code"]["Location"]
    try:
        with urllib.request.urlopen(url, timeout=120) as r, open(out_path, "wb") as fh:  # noqa: S310 - presigned https
            data = r.read()
            fh.write(data)
    except Exception as exc:  # the exception text can carry the signed URL
        raise RuntimeError("download failed: %s: %s" % (type(exc).__name__, _scrub(exc))) from None
    return {
        "function": function,
        "out": out_path,
        "bytes": len(data),
        "sha256_hex": hashlib.sha256(data).hexdigest(),
        "code_sha256_b64": resp["Configuration"].get("CodeSha256"),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("census")
    c.add_argument("built")
    c.add_argument("live")
    c.add_argument("--rules")
    c.add_argument("--out")
    f = sub.add_parser("fetch-live")
    f.add_argument("function")
    f.add_argument("--out", required=True)
    f.add_argument("--region", default="us-east-1")
    args = ap.parse_args(argv)

    if args.cmd == "census":
        result = census(args.built, args.live, load_rules(args.rules))
        text = json.dumps(result, indent=2) + "\n"
        if args.out:
            with open(args.out, "wb") as fh:
                fh.write(text.encode("utf-8"))
        else:
            sys.stdout.write(text)
        cn = result["counts"]
        sys.stderr.write("census: %d members, added=%d removed=%d changed=%d unchanged=%d RIDER=%d\n"
                         % (cn["members"], cn["added"], cn["removed"], cn["changed"], cn["unchanged"], cn["riders"]))
        return 1 if result["riders"] else 0
    try:
        res = fetch_live(args.function, args.out, args.region)
    except Exception as exc:
        sys.stderr.write("ERROR: fetch-live %s: %s\n" % (args.function, _scrub(exc)))
        return 2
    sys.stdout.write(json.dumps(res) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
