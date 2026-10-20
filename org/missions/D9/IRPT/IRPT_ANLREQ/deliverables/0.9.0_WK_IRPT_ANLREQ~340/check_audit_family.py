"""AR-y-466: the platinum family ANALYSIS_AUDIT in reporting policy irpt-anlreq-x10-v1 (PRD v0.27 C-AUDIT-RECORD).

Stdlib only, offline, no AWS. Loads lib/opal_naming.py BY PATH and:
  1. runs the module's own registry validation, validate(), on the edited registry;
  2. reads the one policy whose policy_revision is irpt-anlreq-x10-v1 and checks its ANALYSIS_AUDIT row
     is exactly the row the order names;
  3. for each enabled client firm in data/firm_registry.json, resolves the firm's LONG scope through the
     module's lookup() and calls the builder address() with source irpt, that scope, tier platinum, table
     analysis_audit, a sample partition and a sample object.

Partition grammar, read from org/standards/NAMING_SCHEMA.json key.partition: "date=YYYY-MM-DD", "a named
leaf", or "{entity}={id}". The sample is date=2026-10-20, the first form. address() checks the partition
only as a non-empty ASCII segment with no slash, and the sample passes that test.

--selftest runs the same policy validation on in-memory copies of the registry. Variant A carries the new row
with unreferenced_days 30. Variant B carries tier state with unreferenced_days null. CONTROL-FIRES prints only
when BOTH read BAD. Otherwise it prints CONTROL-DOES-NOT-FIRE and exits 1.
"""

import copy
import importlib.util
import json
import os
import sys

POLICY_REVISION = "irpt-anlreq-x10-v1"
FAMILY = "ANALYSIS_AUDIT"
TABLE = "analysis_audit"
SAMPLE_PARTITION = "date=2026-10-20"
SAMPLE_OBJECT = "REQ-SAMPLE.json"
EXPECTED_ROW = {"tier": "platinum", "table": "analysis_audit", "extension": "json",
                "unreferenced_days": None, "accepted_ceiling_days": 2555}
LIB_REL = os.path.join("lib", "opal_naming.py")


def find_root(start):
    cur = start
    for _ in range(12):
        if os.path.isfile(os.path.join(cur, LIB_REL)):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return None


def load_module(root):
    spec = importlib.util.spec_from_file_location("opal_naming_by_path", os.path.join(root, LIB_REL))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def policy_row(reg):
    rows = [p for p in reg["reporting_policies"]["policies"] if p["policy_revision"] == POLICY_REVISION]
    if len(rows) != 1:
        raise ValueError("policy_revision %s appears %d times" % (POLICY_REVISION, len(rows)))
    return rows[0]


def policy_check(mod, reg, spec):
    """None when the policy validation accepts the family row, else the refusal text."""
    variant = copy.deepcopy(reg)
    policy_row(variant)["families"][FAMILY] = spec
    try:
        mod._validate_reporting_policies(variant)
    except (ValueError, KeyError, TypeError) as exc:
        return str(exc)
    return None


def selftest(root, mod):
    base = mod.load_registry()
    variant_a = dict(EXPECTED_ROW, unreferenced_days=30)
    variant_b = dict(EXPECTED_ROW, tier="state")
    verdicts = {}
    for label, desc, spec in (("A", "platinum with unreferenced_days 30", variant_a),
                              ("B", "tier state with unreferenced_days null", variant_b)):
        refusal = policy_check(mod, base, spec)
        verdicts[label] = refusal is not None
        if refusal is None:
            print("CONTROL-VARIANT-%s %s -> OK (validator accepts)" % (label, desc))
        else:
            print("CONTROL-VARIANT-%s %s -> BAD: %s" % (label, desc, refusal))
    if verdicts["A"] and verdicts["B"]:
        print("CONTROL-FIRES")
        return 0
    print("CONTROL-DOES-NOT-FIRE: the control fires only when both variants read BAD "
          "(variant A read BAD=%s, variant B read BAD=%s)" % (verdicts["A"], verdicts["B"]))
    return 1


def main(argv):
    root = find_root(os.path.dirname(os.path.abspath(__file__)))
    if root is None:
        print("AUDIT-FAMILY-BAD lib/opal_naming.py not found above this file")
        return 1
    mod = load_module(root)
    if "--selftest" in argv:
        return selftest(root, mod)

    refusals, _warnings = mod.validate()
    if refusals:
        print("AUDIT-FAMILY-BAD validator refused %d item(s): %s" % (
            len(refusals), "; ".join("%s %s: %s" % r for r in refusals[:5])))
        return 1

    reg = mod.load_registry()
    try:
        policy = policy_row(reg)
    except ValueError as exc:
        print("AUDIT-FAMILY-BAD %s" % exc)
        return 1
    spec = policy["families"].get(FAMILY)
    if spec != EXPECTED_ROW:
        print("AUDIT-FAMILY-BAD %s row is %r, expected %r" % (FAMILY, spec, EXPECTED_ROW))
        return 1

    with open(os.path.join(root, "data", "firm_registry.json"), encoding="utf-8") as fh:
        firms = json.load(fh)["firms"]
    clients = [f for f in firms if f.get("kind") == "client" and f.get("enabled") is True]
    if not clients:
        print("AUDIT-FAMILY-BAD no enabled client firm in data/firm_registry.json")
        return 1

    addresses = 0
    for firm in clients:
        try:
            row = mod.lookup(firm["firm_id"], reg)
        except KeyError:
            print("AUDIT-FAMILY-BAD firm %s resolves to no scopes.json row" % firm["firm_id"])
            return 1
        if row.get("class") != "FIRM":
            print("AUDIT-FAMILY-BAD firm %s is a %s scope" % (firm["firm_id"], row.get("class")))
            return 1
        scope = row["long"]
        try:
            addr = mod.address("irpt", scope, "platinum", TABLE, SAMPLE_PARTITION, SAMPLE_OBJECT)
        except (ValueError, KeyError) as exc:
            print("AUDIT-FAMILY-BAD builder refused %s: %s" % (scope, exc))
            return 1
        want = "s3://%s/irpt/%s/platinum/%s/%s/%s" % (row["bucket"], scope, TABLE, SAMPLE_PARTITION, SAMPLE_OBJECT)
        if addr != want:
            print("AUDIT-FAMILY-BAD %s address %s does not match the grammar %s" % (scope, addr, want))
            return 1
        print("ADDRESS firm=%s bucket=%s key=%s" % (
            scope, row["bucket"], addr[len("s3://%s/" % row["bucket"]):]))
        addresses += 1

    print("AUDIT-FAMILY-OK firms=%d addresses=%d validator=pass" % (len(clients), addresses))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
