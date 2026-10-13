"""AR-y-223 (IRPT_ANLREQ round 21, workstream Y) -- the offline prediction of the driven status-rule exercise.

Runs the PACKAGED directory entry (infra/aws/lambda/investor-reporting/directory/entry.py) and the _authz/served.py it
imports, both from the worktree tree at --root, with three synthetic principals. The users table is a FAKE DynamoDB
client that answers the two calls the rule's real reader makes (CanonicalProfileReaders.get_user in
_scope/canonical_profile_reads.py: an email-index query, then a ConsistentRead GetItem), so the row shape the rule
reads is exercised, not assumed. `deps` is stubbed to stop after admission (the harness's own pattern), so the
directory and ownership artifacts are never read.

No AWS call, no key, no token is minted or verified, no identity is read; the only output is this script's stdout.
Usage: python offline_run_ar223.py --root <worktree root>
Exit 0 when the three outcomes and classes equal the design's expectations; 1 otherwise.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import sys
from pathlib import Path
from types import SimpleNamespace

ROUTE = "GET /api/scoped/investor-reporting/directory/search"
SELECTED = "cottonwood"
HOME = "opal-capital"
IR = "infra/aws/lambda/investor-reporting"
CLASS_LINE = "INTERNAL-CALLER-CLASS"
SERVED_PIN_SHA256 = "30c0eb88ec38a7ddfc410e4ae1c06ee7a9e77661812ba666a45ffcf5552c2475"
ADDR = {
    "disabled": "irpt-r21-status-disabled@opal.invalid",
    "norow": "irpt-r21-status-norow@opal.invalid",
    "active": "irpt-r21-status-active@opal.invalid",
}
CONTROL_ADDR = "irpt-r21-status-noemail@opal.invalid"
EXPECTED = {
    "disabled": ("refused", "row_non_active"),
    "norow": ("refused", "row_absent"),
    "active": ("admitted", "row_present"),
}


class StopAfterAdmission(RuntimeError):
    pass


class Spy(dict):
    """A returned PROFILE that records every read of `allowedFirmIds` (the status test must come first)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reads = []

    def __contains__(self, key):
        if key == "allowedFirmIds":
            self.reads.append(key)
        return dict.__contains__(self, key)

    def __getitem__(self, key):
        if key == "allowedFirmIds":
            self.reads.append(key)
        return dict.__getitem__(self, key)

    def get(self, key, default=None):
        if key == "allowedFirmIds":
            self.reads.append(key)
        return dict.get(self, key, default)


def typed(item):
    """A plain item in the DynamoDB JSON form the SDK returns."""
    out = {}
    for key, value in item.items():
        out[key] = {"L": [{"S": x} for x in value]} if isinstance(value, list) else {"S": value}
    return out


def profile(addr, status, with_email=True):
    item = {"PK": "USER#" + addr, "SK": "PROFILE", "firmId": HOME, "status": status, "userType": "test-filer",
            "name": "IRPT_ANLREQ R21 status-rule probe", "allowedFirmIds": [SELECTED]}
    if with_email:
        item["email"] = addr
    return typed(item)


class FakeUsersTable(object):
    """A fake DynamoDB client: the two calls CanonicalProfileReaders.get_user makes. Nothing leaves the process."""

    meta = SimpleNamespace(service_model=SimpleNamespace(service_name="dynamodb"))

    def __init__(self, items):
        self.rows = {(i["PK"]["S"], i["SK"]["S"]): i for i in items}

    def query(self, **kw):
        assert kw["IndexName"] == "email-index"
        email = kw["ExpressionAttributeValues"][":email"]["S"]
        hits = [{k: v for k, v in row.items() if k in ("PK", "SK", "email")}
                for row in self.rows.values() if "email" in row and row["email"]["S"] == email]
        return {"Items": hits}

    def get_item(self, **kw):
        assert kw.get("ConsistentRead") is True
        item = self.rows.get((kw["Key"]["PK"]["S"], kw["Key"]["SK"]["S"]))
        return {"Item": item} if item is not None else {}


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def client_bucket_map(root):
    # The live map is Terraform's local.client_firms: kind == client and enabled (iam.tf:31-34, 48). Names only.
    reg = json.loads((root / "data" / "firm_registry.json").read_text(encoding="utf-8"))
    return {f["firm_id"]: f["bucket"] for f in reg["firms"] if f.get("kind") == "client" and f.get("enabled")}


def main(argv):
    if "--root" not in argv:
        print("usage: offline_run_ar223.py --root <worktree root>")
        return 2
    root = Path(argv[argv.index("--root") + 1]).resolve()
    bmap = client_bucket_map(root)
    os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps(bmap, sort_keys=True)

    entry_path = root / IR / "directory" / "entry.py"
    spec = importlib.util.spec_from_file_location("irpt_dir_entry_r21", str(entry_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ENTRY = module.ENTRY
    import served
    import loaders
    from canonical_profile_reads import CanonicalProfileReaders

    # The fake table: the disabled and active rows carry `email`; norow has no item; the control row has no `email`.
    table = FakeUsersTable([profile(ADDR["disabled"], "disabled"), profile(ADDR["active"], "active"),
                            profile(CONTROL_ADDR, "disabled", with_email=False)])
    reader = CanonicalProfileReaders(table)
    seen = []
    state = {"row": None}

    def stub_deps(tenant, *args, **kwargs):
        seen.append(tenant)
        raise StopAfterAdmission("stop after admission")

    def real_reader_profile(email):
        user = reader.get_user(email)
        state["row"] = Spy(user) if user is not None else None
        return state["row"]

    ENTRY.deps = stub_deps
    ENTRY.opaque_firm_for = lambda *args, **kwargs: None
    ENTRY.load_service_profile = real_reader_profile

    def call(email):
        del seen[:]
        state["row"] = None
        headers = {"X-Contract-Version": served.CONTRACT_VERSION, "X-Firm-Id": HOME, "x-origin-verify": "cloudfront",
                   "x-user-email": email, "x-user-role": "user", "x-user-type": "test-filer", "x-user-tier": "internal"}
        event = {"headers": headers, "routeKey": ROUTE, "queryStringParameters": {"selected_tenant": SELECTED}}
        out_buf, err_buf = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
            answer = ENTRY.handle(event)
        lines = (out_buf.getvalue() + err_buf.getvalue()).splitlines()
        class_lines = [line for line in lines if line.startswith(CLASS_LINE)]
        blob = json.dumps(answer, default=str)
        reason = re.search(r'"public_reason_code":\s*"([A-Z_]+)"', blob)
        return {
            "outcome": "refused" if "FIRM_BINDING" in blob else "admitted",
            "class_lines": class_lines,
            "refusal_code": reason.group(1) if reason else None,
            "deps_reached": SELECTED in seen,
            "row": state["row"],
        }

    results = []
    for name in ("disabled", "norow", "active"):
        got = call(ADDR[name])
        klass = None
        if len(got["class_lines"]) == 1:
            klass = got["class_lines"][0].split(" ")[1].split("=", 1)[1]
        leak = [s for s in (ADDR[name], "irpt-r21", SELECTED, HOME)
                for line in got["class_lines"] if s in line]
        want_outcome, want_class = EXPECTED[name]
        results.append({
            "name": name,
            "home_firm": HOME,
            "selected_firm": SELECTED,
            "outcome": got["outcome"],
            "class": klass,
            "line": got["class_lines"][0] if len(got["class_lines"]) == 1 else None,
            "class_lines_found": len(got["class_lines"]),
            "refusal_code": got["refusal_code"],
            "deps_reached_for_selected_firm": got["deps_reached"],
            "allowed_firms_attribute_read": bool(got["row"] is not None and got["row"].reads),
            "line_carries_identity": bool(leak),
            "matches_expected": (got["outcome"], klass) == (want_outcome, want_class)
                                and len(got["class_lines"]) == 1,
        })

    # Control, not a design identity: a row with the same status but NO email attribute is invisible to the
    # email-index lookup, so the rule reads it as absent. The design's row shape must therefore carry `email`.
    control = call(CONTROL_ADDR)
    control_row = {"name": "control_disabled_row_without_email_attribute", "outcome": control["outcome"],
                   "class": control["class_lines"][0].split(" ")[1].split("=", 1)[1]
                   if len(control["class_lines"]) == 1 else None}

    report = {
        "served_py": {"path": served.__file__, "sha256": sha256_of(served.__file__),
                      "equals_source_map_pin": sha256_of(served.__file__) == SERVED_PIN_SHA256},
        "entry_py": {"path": str(entry_path), "sha256": sha256_of(entry_path)},
        "loaders_py": {"path": loaders.__file__, "sha256": sha256_of(loaders.__file__)},
        "reader": "_scope/canonical_profile_reads.py CanonicalProfileReaders.get_user over the fake users table",
        "bucket_map_firms_used": sorted(bmap),
        "results": results,
        "control": control_row,
        "all_match_expected": all(r["matches_expected"] for r in results),
    }
    print(json.dumps(report, indent=1, sort_keys=True))
    return 0 if report["all_match_expected"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
