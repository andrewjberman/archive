"""AMGT_HARVST round 12, cell HVST-a-1, AC1 -- issuer-written, dry-run at the base before the cut.

THE DECLARED MOUNT AND THE HANDLED ROUTE SET AGREE AT 18, BOTH TIMELINE ROUTES INCLUDED, and the terraform's own
count precondition moved with them. Read from source TEXT and from the adapter's own table; no AWS, no network.
Exit 0 only if every line reads PASS.
"""
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 9))
sys.path.insert(0, REPO)

from lib.research.api import scoped_amgt  # noqa: E402

TF = os.path.join(REPO, "infra", "aws", "terraform", "harvest", "scoped-amgt-api.tf")
WANT = [
    "GET /api/scoped/amgt/security/{security_key}/timeline",
    "GET /api/scoped/amgt/security/{security_key}/timeline/day/{date}",
]
failures = []


def check(label, ok, detail=""):
    print("%s: %s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        failures.append(label)


def norm(route):
    return re.sub(r"\s+", " ", route).strip()


text = open(TF, encoding="utf-8").read()
block = re.search(r"scoped_amgt_routes\s*=\s*\[(.*?)\]", text, re.S)
# Only quoted strings that START with an HTTP verb are route keys: the list also carries comments whose prose
# contains quoted phrases ("Adam can see", "api/scoped/amgt"), and counting those read 18 at a base of 16.
tf_routes = sorted(norm(r) for r in re.findall(r'"((?:GET|POST|PUT|PATCH|DELETE) [^"]+)"', block.group(1))) \
    if block else []
table = sorted(norm(r) for r in scoped_amgt.scoped_amgt_route_table())
pre = re.search(r"length\(local\.scoped_amgt_routes\)\s*==\s*(\d+)", text)

print("terraform scoped_amgt_routes: %d; scoped_amgt_route_table(): %d; precondition: == %s"
      % (len(tf_routes), len(table), pre.group(1) if pre else "ABSENT"))
for want in WANT:
    check("terraform mounts", want in tf_routes, want)
    check("adapter table serves", want in table, want)
check("terraform count is 18", len(tf_routes) == 18, str(len(tf_routes)))
check("adapter table count is 18", len(table) == 18, str(len(table)))
check("terraform precondition reads == 18", bool(pre) and pre.group(1) == "18", pre.group(0) if pre else "ABSENT")
only_tf = sorted(set(tf_routes) - set(table))
only_table = sorted(set(table) - set(tf_routes))
check("mount == table, both directions", not only_tf and not only_table,
      "tf-only=%s table-only=%s" % (only_tf, only_table))

print("AC1 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
sys.exit(0 if not failures else 1)
