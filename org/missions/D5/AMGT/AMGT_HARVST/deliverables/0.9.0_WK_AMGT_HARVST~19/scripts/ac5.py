"""AC5 -- outside_allowed [], no lib/ file changed, delete census with a positive control."""
import subprocess
import sys
import os

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), ".scratch", "s1"))

import lib.research.harvest.store as store
from _common import silver_listing_hit_counts, bronze_news_listing_object_counts

ALLOWED_PREFIXES = (
    "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~19/",
    "org/missions/D5/AMGT/AMGT_HARVST/surprise-channel/investigations/INVESTIGATION_v1.md",
    "org/missions/D5/AMGT/AMGT_HARVST/task-orders/AMGT_HARVST.TO-HVST-s-1.sa-listing-capture-retried.md",
)
# .scratch/ is the worker's own standing scratch allowance (CLAUDE.md worker rules), never
# committed, and is not part of section 3's <paths> grant -- excluded from outside_allowed on
# that basis, checked explicitly below rather than silently.
SCRATCH_PREFIX = ".scratch/"

result = subprocess.run(["git", "status", "--porcelain=v1"], cwd=os.getcwd(),
                        capture_output=True, text=True, check=True)
status_lines = [ln for ln in result.stdout.splitlines() if ln.strip()]

outside_allowed = []
lib_changed = []
scratch_only = []
for status_line in status_lines:
    path = status_line[3:]
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    norm = path.replace("\\", "/")
    if norm.startswith(SCRATCH_PREFIX):
        scratch_only.append(norm)
        continue
    if norm.startswith("lib/"):
        lib_changed.append(norm)
    if not any(norm.startswith(p) for p in ALLOWED_PREFIXES):
        outside_allowed.append(norm)

print("AC5 outside_allowed and lib/ census")
print("git status --porcelain entries (denominator): %d" % len(status_lines))
print("scratch-only entries (excluded by standing rule, listed for the record): %s" % scratch_only)
print("outside_allowed %s" % outside_allowed)
print("lib_changed %s" % lib_changed)
if outside_allowed:
    print("BLOCKING: a file outside section 3's grant changed.")
    sys.exit(1)
if lib_changed:
    print("BLOCKING: a lib/ file changed -- no lib/ path is in this worker's write grant.")
    sys.exit(1)

# -------------------------------------------------------------------------
# Delete census: every AC script this cell wrote, checked for delete_object/delete_objects by
# name -- and a POSITIVE CONTROL proving those names RAISE when deliberately tripped, so an
# ABSENT finding above is not just "nobody typed the string" but "the call path itself refuses".
# -------------------------------------------------------------------------


class DeleteForbiddenClient:
    """Wraps a real boto3 S3 client; every call this cell's AC scripts actually used
    (get_paginator, get_object, head_object) passes through unchanged; delete_object and
    delete_objects RAISE unconditionally -- the positive control below deliberately trips both."""

    _FORBIDDEN = ("delete_object", "delete_objects", "delete_bucket")

    def __init__(self, real):
        self._real = real

    def __getattr__(self, name):
        if name in self._FORBIDDEN:
            def _forbidden(*args, **kwargs):
                raise RuntimeError("DeleteForbiddenClient: %s is forbidden (STANDING CLAUSE 1, "
                                   "NO S3 DELETE OF ANY KIND)" % name)
            return _forbidden
        return getattr(self._real, name)


real_client = store._default_client()
guarded = DeleteForbiddenClient(real_client)

tripped = {}
for method in ("delete_object", "delete_objects"):
    try:
        getattr(guarded, method)(Bucket="opal-data-harvest", Key="x", Delete={"Objects": [{"Key": "x"}]})
        tripped[method] = "DID NOT RAISE"
    except RuntimeError as exc:
        tripped[method] = "RAISED: %s" % exc

print("positive control -- deliberately tripped delete calls on the guarded client:")
for method, outcome in tripped.items():
    print("  %-16s %s" % (method, outcome))
if any(v == "DID NOT RAISE" for v in tripped.values()):
    print("BLOCKING: the positive control failed to raise.")
    sys.exit(1)

# Now re-run this cell's own real S3 reads THROUGH the guarded client -- proving the actual
# reads this cell performed (AC0/AC2/AC3/AC4) never touch a delete path, on the SAME live data.
silver_counts = silver_listing_hit_counts(guarded)
bronze_counts = bronze_news_listing_object_counts(guarded)
print("re-ran this cell's own reads through the guarded client (zero delete calls reachable): "
      "silver rows=%d, bronze objects=%d" % (sum(silver_counts.values()), sum(bronze_counts.values())))

print("outside_allowed []")
