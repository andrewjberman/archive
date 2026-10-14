"""AC1 (TO TCKT_VNEXT.TO-R18-TR1): re-compute the ticket-attachment address from the naming builder and check
ATTACH_ADDRESS.json against it.

Prints ADDRESS-OK <bucket_template> <key_template> (exit 0) or ADDRESS-BAD <why> (exit 1).
The record is read from the environment variable ATTACH_ADDRESS_JSON when it is set (the mutant check uses this),
otherwise from ATTACH_ADDRESS.json beside this file. Nothing is created in AWS; no network call is made.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))  # deliverables/<serial>/ up to the worktree root
FIRMS = ["49financial", "inflection", "cottonwood"]
SOURCE, TIER, TABLE, PARTITION = "portal", "state", "ticket_attachments", "trade-form"
TOKEN = "{firm}"
S3_RE = re.compile(r"^s3://([^/]+)/(.+)$")


def bad(why):
    print("ADDRESS-BAD " + why)
    sys.exit(1)


def load_record():
    path = os.environ.get("ATTACH_ADDRESS_JSON") or os.path.join(HERE, "ATTACH_ADDRESS.json")
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        bad("cannot read record %s: %s" % (path, exc))


def main():
    sys.path.insert(0, os.path.join(ROOT, "lib"))
    os.chdir(ROOT)
    try:
        import opal_naming
    except Exception as exc:  # the import itself is a check
        bad("cannot import lib/opal_naming.py from the worktree: %s" % exc)

    computed = {}
    for firm in FIRMS:
        try:
            addr = opal_naming.address(SOURCE, firm, TIER, TABLE, PARTITION)
        except Exception as exc:
            bad("builder refused %s: %s" % (firm, exc))
        m = S3_RE.match(addr)
        if not m:
            bad("builder output is not an s3:// address for %s: %r" % (firm, addr))
        computed[firm] = {"address": addr, "bucket": m.group(1), "key": m.group(2)}

    # Derive the templates from the computed addresses: the firm id replaced by {firm} must be one template.
    bucket_tmpl = set()
    key_tmpl = set()
    for firm in FIRMS:
        bucket_tmpl.add(computed[firm]["bucket"].replace(firm, TOKEN))
        key_tmpl.add(computed[firm]["key"].replace(firm, TOKEN) + "/")
    if len(bucket_tmpl) != 1:
        bad("the three firms' buckets do not fit one template: %s" % sorted(bucket_tmpl))
    if len(key_tmpl) != 1:
        bad("the three firms' keys do not fit one template: %s" % sorted(key_tmpl))
    derived_bucket_tmpl = bucket_tmpl.pop()
    derived_key_tmpl = key_tmpl.pop()

    rec = load_record()
    for label, want in (("tier", TIER), ("source", SOURCE), ("table", TABLE), ("partition", PARTITION)):
        if rec.get(label) != want:
            bad("record %s is %r, builder call uses %r" % (label, rec.get(label), want))

    bt = rec.get("bucket_template")
    kt = rec.get("key_template")
    if not isinstance(bt, str) or bt.count(TOKEN) != 1:
        bad("bucket_template must contain {firm} exactly once: %r" % (bt,))
    if not isinstance(kt, str) or kt.count(TOKEN) != 1:
        bad("key_template must contain {firm} exactly once: %r" % (kt,))
    if not kt.endswith("/"):
        bad("key_template must end with a trailing slash: %r" % (kt,))

    # Round trip: each firm's template fill reproduces the firm's printed bucket and key exactly.
    for firm in FIRMS:
        if bt.format(firm=firm) != computed[firm]["bucket"]:
            bad("bucket_template round trip fails for %s: %r != %r" % (firm, bt.format(firm=firm), computed[firm]["bucket"]))
        if kt.format(firm=firm) != computed[firm]["key"] + "/":
            bad("key_template round trip fails for %s: %r != %r" % (firm, kt.format(firm=firm), computed[firm]["key"] + "/"))

    if bt != derived_bucket_tmpl:
        bad("bucket_template %r is not the builder's template %r" % (bt, derived_bucket_tmpl))
    if kt != derived_key_tmpl:
        bad("key_template %r is not the builder's template %r" % (kt, derived_key_tmpl))

    addresses = rec.get("addresses")
    if not isinstance(addresses, dict) or set(addresses) != set(FIRMS):
        bad("addresses must be keyed by exactly the three firms")
    for firm in FIRMS:
        if addresses[firm] != computed[firm]["address"]:
            bad("addresses[%s] %r != builder %r" % (firm, addresses[firm], computed[firm]["address"]))

    buckets = rec.get("buckets")
    if not isinstance(buckets, dict) or set(buckets) != set(FIRMS):
        bad("buckets must be keyed by exactly the three firms")
    for firm in FIRMS:
        if buckets[firm] != computed[firm]["bucket"]:
            bad("buckets[%s] %r != builder %r" % (firm, buckets[firm], computed[firm]["bucket"]))

    if rec.get("validate_rc") != 0:
        bad("record validate_rc is %r, expected 0" % (rec.get("validate_rc"),))
    try:
        proc = subprocess.run([sys.executable, os.path.join("lib", "opal_naming.py"), "validate"],
                              cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=110)
    except subprocess.TimeoutExpired:
        bad("python lib/opal_naming.py validate timed out")
    if proc.returncode != 0:
        bad("python lib/opal_naming.py validate rc=%d" % proc.returncode)

    print("ADDRESS-OK %s %s" % (bt, kt))
    sys.exit(0)


if __name__ == "__main__":
    main()
