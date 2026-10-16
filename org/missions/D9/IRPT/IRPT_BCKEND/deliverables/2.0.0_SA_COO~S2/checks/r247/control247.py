"""Control for p247_cells.py: a synthetic GOOD record passes all three arms, and each planted defect fails its own arm.

Usage: python control247.py <repo_root>; prints "control247 OK (<n> positives, <m> negatives, 0 unexpected)" last, exit 0, else exit 1.
It builds a temp tree that holds copies of the signed documents (the check hashes them) and the synthetic record; the real repo is never written.
"""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(".").resolve()
sys.path.insert(0, str(HERE))
import p247_cells as P  # noqa: E402

GOOD = {
    "gates": {
        "packet_sha256_prefix": P.PACKET_SHA256_PREFIX, "addendum_1_blob": P.A1_DRAFT_BLOB, "addendum_2_blob": P.A2_COO_BLOB,
        "all_halves_signed": True, "hop2_ledger_closed": True, "one_change_at_a_time": True, "open_deploys_worktrees_read": 80,
        "before": {"read_function_sha256": P.READ_BEFORE, "export_function_sha256": P.EXPORT_BEFORE, "report_route_absent": True},
    },
    "h3": {"function": P.READ_FN, "built_sha256": "AAAA", "after_sha256": "AAAA", "route": P.REPORT_ROUTE, "route_present_after": True,
           "existing_routes_changed": 0, "plan": {"add": 1, "change": 1, "destroy": 0, "resources": ["aws_apigatewayv2_route.report", "module.read.aws_lambda_function.this"]}},
    "h4a": {"function": P.EXPORT_FN, "built_sha256": "BBBB", "after_sha256": "BBBB", "sha256_before": P.EXPORT_BEFORE, "pass_switch_unchanged": True},
    "h4b": {"fence_row": {"second_row_present": True, "regenerated_and_read_back": True}, "role_statement_before": "absent",
            "plan": {"add": 0, "change": 1, "destroy": 0}, "statements_added": 1, "statements_removed": 0,
            "statement": {"effect": "Allow", "actions": list(P.STATEMENT_ACTIONS), "resource": P.STATEMENT_RESOURCE}, "replan_changes": 0},
    "counters": {"rollback_performed": False, "console_edits": 0, "put_role_policy_calls": 0, "switch_changes": 0, "other_roles_changed": 0, "second_firm_prefixes": 0},
}


def run(tree, cid):
    p = subprocess.run([sys.executable, "-I", str(HERE / "p247_cells.py"), str(tree), cid], capture_output=True, text=True, timeout=120)
    return p.returncode, (p.stdout.strip().splitlines() or [""])[-1]


def build(rec):
    tree = Path(tempfile.mkdtemp(prefix="c247_"))
    for rel in (P.PAIR_COO, P.PAIR_CTO, P.A1_DRAFT, P.A1_COO, P.A2_COO):
        dst = tree / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, dst)
    if rec is not None:
        out = tree / P.REC
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rec), encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tree, capture_output=True, timeout=60)
    return tree


def mutate(path, value):
    r = copy.deepcopy(GOOD)
    cur = r
    for k in path[:-1]:
        cur = cur[k]
    cur[path[-1]] = value
    return r


NEG = [
    ("IB247-1-AC1", mutate(("gates", "hop2_ledger_closed"), False)),
    ("IB247-1-AC1", mutate(("gates", "before", "read_function_sha256"), "OTHER=")),
    ("IB247-1-AC1", mutate(("gates", "addendum_2_blob"), "0" * 40)),
    ("IB247-1-AC2", mutate(("h3", "route_present_after"), False)),
    ("IB247-1-AC2", mutate(("h3", "existing_routes_changed"), 1)),
    ("IB247-1-AC2", mutate(("h4a", "after_sha256"), "ZZZZ")),
    ("IB247-1-AC2", mutate(("h4a", "pass_switch_unchanged"), False)),
    ("IB247-1-AC3", mutate(("h4b", "fence_row", "regenerated_and_read_back"), False)),
    ("IB247-1-AC3", mutate(("h4b", "statements_added"), 2)),
    ("IB247-1-AC3", mutate(("h4b", "statement", "resource"), "arn:aws:s3:::opal-data-49financial/irpt/49financial/platinum/reporting/*")),
    ("IB247-1-AC3", mutate(("counters", "rollback_performed"), True)),
    ("IB247-1-AC3", mutate(("counters", "console_edits"), 1)),
]


def main():
    bad, pos, neg = [], 0, 0
    good_tree = build(GOOD)
    for cid in ("IB247-1-AC1", "IB247-1-AC2", "IB247-1-AC3"):
        rc, last = run(good_tree, cid)
        pos += 1
        if rc != 0 or not last.endswith("PASS"):
            bad.append("positive %s: %s" % (cid, last))
    shutil.rmtree(good_tree, ignore_errors=True)
    rc, last = run(build(None), "IB247-1-AC1")
    neg += 1
    if rc == 0:
        bad.append("no-record case passed")
    for cid, rec in NEG:
        tree = build(rec)
        rc, last = run(tree, cid)
        neg += 1
        if rc == 0:
            bad.append("negative did not fail: %s %s" % (cid, last))
        shutil.rmtree(tree, ignore_errors=True)
    if bad:
        print("\n".join(bad))
        print("control247 FAIL (%d unexpected)" % len(bad))
        sys.exit(1)
    print("control247 OK (%d positives, %d negatives, 0 unexpected)" % (pos, neg))


main()
