#!/usr/bin/env python3
"""IB-pr-503 -- offline replay of the PACKAGED irpt-holdings serve path (round 173, workstream ~P).

Worker 0.9.0_WK_IRPT_BCKEND~354. The code replayed is the code the live function runs: each
member of infra/aws/lambda/ci/lambda-source-map.json functions["irpt-holdings"]["staged_from"] is
read with `git show <pin>:<repo_path>`, hash-checked against the source map, and written flat into
a temp folder OUTSIDE the repository; the one non-staged file is taken from the worktree.

Three SYNTHETIC one-account snapshots differ only by one member on the ACCOUNT node: account_id,
none, and unknown_member. Each is loaded through the packaged snapshot.load_snapshot over an
in-memory S3 reader and served through the packaged snapshot.project.

OFFLINE: no AWS client is created, no function is invoked, no sign-in, no vendor request, no write.
Run from the repository root:  python -I <this file>
Prints the record object (JSON) to stdout, writes the same bytes to IB173-1_holdings_passthrough_replay.json,
and exits 0. Takes no argument.
"""
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import warnings
from pathlib import Path

sys.dont_write_bytecode = True
warnings.simplefilter("ignore")

REPO = Path.cwd().resolve()
SRCMAP = REPO / "infra" / "aws" / "lambda" / "ci" / "lambda-source-map.json"
FN = "irpt-holdings"
REC_DIR = REPO / "org" / "missions" / "D9" / "IRPT" / "IRPT_BCKEND" / "deliverables" / "0.9.0_WK_IRPT_BCKEND~354"
REC_FILE = REC_DIR / "IB173-1_holdings_passthrough_replay.json"

ACCT = "ACCT-SYN-1"
BDATE = "2026-10-09"
CUSTODY = "2026-10-09"
OVERLAY = "2026-10-09"
ACCOUNT_ID_VALUE = "ACCT-SYN-1"
UNKNOWN_VALUE = "SYN-UNKNOWN-1"


def refuse(msg):
    sys.exit("REFUSED: " + msg)


def git_show(pin, repo_path):
    p = subprocess.run(["git", "-C", str(REPO), "show", "%s:%s" % (pin, repo_path)],
                       capture_output=True, timeout=60)
    if p.returncode != 0:
        refuse("git show %s:%s rc=%d" % (pin, repo_path, p.returncode))
    return p.stdout


def sha(body):
    return hashlib.sha256(body).hexdigest()


def assemble(scratch):
    """Write the packaged tree flat into `scratch`; return the members imported."""
    fn = json.loads(SRCMAP.read_bytes().decode("utf-8"))["functions"][FN]
    members, packaged = [], set()
    for e in fn["staged_from"]:
        body = git_show(e["pin"], e["repo_path"])
        digest = sha(body)
        if digest != e["sha256"]:
            refuse("%s at %s hashes %s, the source map records %s" % (e["repo_path"], e["pin"], digest, e["sha256"]))
        dst = Path(scratch, e["packaged_as"])
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(body)
        packaged.add(e["packaged_as"])
        members.append({"repo_path": e["repo_path"], "pin": e["pin"], "sha256": digest})
    for name in fn["files"]:
        if name in packaged:
            continue
        body = Path(REPO, fn["source_dir"], name).read_bytes()
        dst = Path(scratch, name)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(body)
        packaged.add(name)
        members.append({"repo_path": fn["source_dir"] + "/" + name, "pin": "WORKTREE", "sha256": sha(body)})
    return members


class StubS3:
    """In-memory S3 reader. It holds only the objects this replay put in it and refuses every write."""

    def __init__(self):
        self.objects = {}
        self.reads = 0

    def put(self, loc, body):
        bucket, key = loc
        version = "VER-" + sha(("%s/%s" % (bucket, key)).encode("utf-8") + body)[:16]
        self.objects[(bucket, key)] = (body, version)
        return {"bucket": bucket, "key": key, "version_id": version,
                "sha256": sha(body), "byte_length": len(body)}

    def get_object(self, Bucket, Key, VersionId=None, **_):
        self.reads += 1
        if (Bucket, Key) not in self.objects:
            raise LookupError("NoSuchKey (stub)")
        body, version = self.objects[(Bucket, Key)]
        if VersionId is not None and VersionId != version:
            raise LookupError("version not held (stub)")
        return {"Body": io.BytesIO(body), "VersionId": version, "ETag": '"%s"' % sha(body)}

    def put_object(self, **_):
        raise RuntimeError("the replay performs no S3 writes")


def account_node(extra):
    node = {"node_id": ACCT, "node_kind": "ACCOUNT", "parent_node_id": None, "basis": "OBSERVED",
            "amount": {"value": 1000.0, "units": "USD"},
            "clocks": {"custody_as_of": CUSTODY, "overlay_as_of": OVERLAY},
            "display": {"label": "Synthetic account 1"}}
    node.update(extra)
    return node


def security_node():
    return {"node_id": ACCT + ":security:SYN-SEC-1", "node_kind": "SECURITY", "parent_node_id": ACCT,
            "basis": "OBSERVED", "amount": {"value": 1000.0, "units": "USD"},
            "security_id": {"namespace": "SYN", "value": "SYN-SEC-1"},
            "clocks": {"custody_as_of": CUSTODY, "overlay_as_of": OVERLAY},
            "display": {"label": "Synthetic security 1"}}


def document(firm, account_node_value):
    return {"scope": {"firm_id": firm, "account_ids": [ACCT]},
            "source_set_revision": [{"source": "synthetic-source", "revision": "0" * 64,
                                     "completion_date": BDATE}],
            "clocks": {"business_date": BDATE, "custody_as_of": CUSTODY, "overlay_as_of": OVERLAY},
            "attribution_holdouts": {
                "unassigned": {"account_count": 0, "account_ids": [],
                               "value": {"value": 0.0, "currency": "USD"}, "basis": "OBSERVED",
                               "observable": "MEASURED", "denominator": "0 of 1 permitted account(s)",
                               "source": "synthetic-overlay"},
                "reconcile": {"total_before": 1000.0, "total_after": 1000.0, "difference": 0.0,
                              "tolerance": 0.01, "reconciled": True}},
            "nodes": [account_node_value, security_node()],
            "contract_version": "v1"}


def stage(P, firm, account_node_value):
    """Write one synthetic publication (index, manifest, Platinum body, Gold stub) with the packaged
    HoldingsPublication's own address builder, and return the stub reader."""
    stub = StubS3()
    pub = P.HoldingsPublication(stub, firm)
    doc = document(firm, account_node_value)
    body = P.canonical_bytes(doc)
    rev = P.digest(body)
    part = "date=" + BDATE
    plat_ref = stub.put(pub.location("platinum", part, rev + ".json"), body)
    gold_ref = stub.put(pub.location("gold", part, rev + ".parquet"), b"SYNTHETIC-GOLD-NOT-READ-AT-SERVE")
    manifest = {"schema_version": "irpt-holdings-manifest-v1", "firm_id": firm, "business_date": BDATE,
                "revision": rev, "gold": gold_ref, "source_set_revision": doc["source_set_revision"],
                "clocks": doc["clocks"], "platinum": plat_ref}
    man_ref = stub.put(pub.location("platinum", part, rev + ".manifest.json"), P.canonical_bytes(manifest))
    index = {"schema_version": "irpt-holdings-index-v1", "firm_id": firm, "latest_date": BDATE,
             "dates": {BDATE: {"revision": rev, "manifest": man_ref}}}
    stub.put(pub.location("platinum", "current", "manifest.json"), P.canonical_bytes(index))
    return stub


def verdict(member, inp, served_node):
    """passed_through / dropped for a member; unchanged for the node without the member."""
    if served_node is None:
        return "refused"
    if member is None:
        cmp_node = {k: v for k, v in served_node.items() if k != "percentages"}
        return "unchanged" if cmp_node == inp else "differs"
    if member not in served_node:
        return "dropped"
    return "passed_through" if served_node[member] == inp[member] else "altered"


def run_arm(S, P, firm, scope, arm, member, extra):
    inp = account_node(extra)
    obs = {"arm": arm}
    try:
        stub = stage(P, firm, json.loads(json.dumps(inp)))
        loaded = S.load_snapshot(firm, S.DEFAULT_PREFIX, None, s3_client=stub)
        served = S.project(loaded, scope)
        S.require_reconciled(served)
        ok, why = S.clocks_are_distinct(served)
        if not ok:
            raise S.SnapshotUnavailable(why)
    except Exception as exc:  # the refusal is the observation, recorded below
        obs["exception"] = type(exc).__name__ + ": " + str(exc)[:160]
        if getattr(exc, "__cause__", None) is not None:
            obs["cause"] = type(exc.__cause__).__name__ + ": " + str(exc.__cause__)[:160]
        return {"arm": arm, "verdict": "refused"}, obs
    served_acct = next((n for n in served["nodes"] if n["node_id"] == ACCT
                        and n.get("node_kind") == "ACCOUNT"), None)
    v = verdict(member, inp, served_acct)
    obs["served_account_node_keys"] = sorted(served_acct.keys()) if served_acct else None
    obs["served_has_member"] = bool(member is not None and served_acct is not None and member in served_acct)
    chk = S.validate_slice(served)
    obs["validate_slice_available"] = chk.get("available")
    obs["validate_slice_valid"] = chk.get("valid")
    obs["validate_slice_errors"] = list(chk.get("errors") or [])[:5]
    return {"arm": arm, "verdict": v}, obs


def main():
    scratch = tempfile.mkdtemp(prefix="irpt_bckend_503_")
    members = assemble(scratch)
    sys.path.insert(0, scratch)
    import opal_naming as ON  # packaged
    import publication as P  # packaged
    import snapshot as S  # packaged
    firm = ON.lookup("49financial")["long"]
    scope = {"permitted_account_set": [ACCT], "selected_account_ids": [ACCT],
             "selected_account_set_fingerprint": "SYN-FP-1",
             "verified_request_firm_id": firm}
    specs = [("node_with_account_id", "account_id", {"account_id": ACCOUNT_ID_VALUE}),
             ("node_without_account_id", None, {}),
             ("node_with_unknown_member", "unknown_member", {"unknown_member": UNKNOWN_VALUE})]
    arms, observations = [], []
    for arm, member, extra in specs:
        a, o = run_arm(S, P, firm, scope, arm, member, extra)
        arms.append(a)
        observations.append(o)
    record = {
        "packaged_members": members,
        "entry_used": ("snapshot.load_snapshot (packaged snapshot.py:158) over a stub s3_client, then "
                       "snapshot.project (snapshot.py:332) with require_reconciled and clocks_are_distinct; "
                       "entry.holdings_snapshot NOT run: it needs AWS (loaders.deps S3 reads and the "
                       "selection_store DynamoDB get_item)"),
        "arms": arms,
        "reading": ("The serve path passes an unknown ACCOUNT node member through unchanged: project() copies "
                    "every kept node whole with json.loads(json.dumps(n)) at snapshot.py:356 and nothing "
                    "between load_snapshot (snapshot.py:158) and the response filters node keys, while the only "
                    "schema check, validate_slice (snapshot.py:115), has no serve caller."),
        "functions_invoked": 0,
        "sign_ins_made": 0,
        "aws_writes_made": 0,
        "accounts_written": 0,
        "figures_written": 0,
        "vendor_requests_sent": 0,
        "scratch_dir": scratch,
        "observations": observations,
    }
    text = json.dumps(record, indent=2, sort_keys=False, ensure_ascii=True) + "\n"
    REC_FILE.write_text(text, encoding="ascii")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
