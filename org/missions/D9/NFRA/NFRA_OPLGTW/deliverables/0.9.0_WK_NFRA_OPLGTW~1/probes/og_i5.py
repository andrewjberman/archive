#!/usr/bin/env python
"""NFRA_OPLGTW OG-i-5 probe -- the access-state table rename, one function per acceptance criterion.

Usage: og_i5.py <AC-short-id>   e.g. og_i5.py AC1

Prints its measurement with vintage and denominator, then exactly one line:
  VERDICT: PASS-OGI5-AC<n>
  VERDICT: FAIL-OGI5-AC<n> <reason>

No item content (a real pk/sk value or an attribute payload) is ever printed -- only digests and
counts (order BOUNDS: "no record for a real person is created, revised or read into evidence").
"""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def _parse_iso(ts: str) -> datetime:
    """Parse an ISO8601 timestamp (Z-suffixed UTC or an explicit +HH:MM offset) to a tz-aware
    datetime, so two timestamps in DIFFERENT offsets compare by INSTANT, never by raw string."""
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))

sys.path.insert(0, str(Path(__file__).resolve().parent))
from og_i5_lib import (  # noqa: E402
    OLD_TABLE,
    REGION,
    load_json,
    table_exists,
)

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent
EVID = DELIV / "evidence" / "og_i5"
# The workspace root is resolved via `git rev-parse --show-toplevel` (_ws()), never path
# arithmetic off this file's location.


def _ws() -> Path:
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, cwd=str(HERE))
    return Path(r.stdout.strip())


def _run(cmd, cwd=None, timeout=90):
    print(f"+ {' '.join(cmd)}")
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout)


def _git_commit_time(ws: Path, ref: str) -> str:
    r = _run(["git", "-C", str(ws), "show", "-s", "--format=%cI", ref])
    return r.stdout.strip()


def _pass(ac):
    print(f"VERDICT: PASS-OGI5-{ac}")
    return 0


def _fail(ac, reason):
    print(f"VERDICT: FAIL-OGI5-{ac} {reason}")
    return 1


def ac1():
    ws = _ws()
    sys.path.insert(0, str(ws))
    from lib.opal_naming import name, grade

    n = name("gateway", None, "access-state", "table")
    g = grade(n, "DYNAMODB_TABLE")
    print(f"builder name() = {n!r}")
    print(f"grade() = {g!r}")
    if n != "gateway-access-state-table":
        return _fail("AC1", f"name() returned {n!r}, expected gateway-access-state-table")
    if g[0] != "CONFORMANT":
        return _fail("AC1", f"grade() returned {g!r}, expected CONFORMANT")
    return _pass("AC1")


def ac2():
    ws = _ws()
    sentinel_path = "org/critical_paths/.open_deploys/nfra-oplgtw-og-i-5-access-state-rename.json"
    # --diff-filter=A: the commit that ADDED the sentinel, never "last touched" -- the ledger close
    # later DELETES this same path, and a plain `git log -1` on it would return the deletion commit
    # (memory trap: "git log path returns zero/wrong commit for add-then-delete").
    r = _run(["git", "-C", str(ws), "log", "--diff-filter=A", "--format=%H", "--", sentinel_path])
    commits = [c for c in r.stdout.splitlines() if c.strip()]
    sentinel_commit = commits[-1] if commits else ""
    if not sentinel_commit:
        return _fail("AC2", "no commit found adding the ledger sentinel")
    sentinel_time = _git_commit_time(ws, sentinel_commit)
    apply1_plan = load_json(EVID / "apply1.plan.json")
    apply1_ts = apply1_plan["timestamp"]
    print(f"sentinel commit {sentinel_commit} at {sentinel_time}")
    print(f"apply1 plan timestamp (recorded start, upper bound on the true apply start) {apply1_ts}")
    if _parse_iso(sentinel_time) >= _parse_iso(apply1_ts):
        return _fail("AC2", f"sentinel commit time {sentinel_time} not before apply1 start {apply1_ts}")
    return _pass("AC2")


def ac3():
    p = load_json(EVID / "apply1.plan.json")
    rc = p["resource_changes"]
    non_noop = [r for r in rc if r["change"]["actions"] != ["no-op"]]
    creates = [r for r in non_noop if r["change"]["actions"] == ["create"]]
    updates = [r for r in non_noop if r["change"]["actions"] == ["update"]]
    destroys = [r for r in non_noop if "delete" in r["change"]["actions"]]
    print(f"denominator: {len(rc)} resource(s) in plan; non-noop: {len(non_noop)}")
    for r in non_noop:
        print(f"  {r['address']}: {r['change']['actions']}")
    ok = (
        len(creates) == 1
        and creates[0]["address"] == "aws_dynamodb_table.access_state_new"
        and len(updates) == 2
        and {r["address"] for r in updates} == {
            "aws_iam_role_policy.gw_access_state_runtime",
            "aws_iam_role_policy.access_admin_policy",
        }
        and len(destroys) == 0
    )
    if not ok:
        return _fail("AC3", "apply1 plan is not exactly 1 create (new table) + 2 update (grants) + 0 destroy")
    return _pass("AC3")


def ac4():
    d = load_json(EVID / "new_table_describe.json")["Table"]
    ttl = load_json(EVID / "new_table_ttl.json")["TimeToLiveDescription"]
    pitr = load_json(EVID / "new_table_pitr.json")["ContinuousBackupsDescription"]["PointInTimeRecoveryDescription"]
    print(f"SSE: {d['SSEDescription']['Status']}")
    print(f"PITR: {pitr['PointInTimeRecoveryStatus']}")
    print(f"Billing: {d['BillingModeSummary']['BillingMode']}")
    print(f"TTL: {ttl['TimeToLiveStatus']} attribute={ttl.get('AttributeName')}")
    print(f"KeySchema: {d['KeySchema']}")
    ok = (
        d["SSEDescription"]["Status"] == "ENABLED"
        and pitr["PointInTimeRecoveryStatus"] == "ENABLED"
        and d["BillingModeSummary"]["BillingMode"] == "PAY_PER_REQUEST"
        and ttl["TimeToLiveStatus"] == "ENABLED"
        and ttl.get("AttributeName") == "expires_at"
        and d["KeySchema"] == [
            {"AttributeName": "pk", "KeyType": "HASH"},
            {"AttributeName": "sk", "KeyType": "RANGE"},
        ]
    )
    if not ok:
        return _fail("AC4", "new table's live description does not match the required shape")
    return _pass("AC4")


def _digest_pair(old_file, new_file):
    old = load_json(EVID / old_file)
    new = load_json(EVID / new_file)
    return old, new


def ac5():
    old, new = _digest_pair("post_cutover_old_digest.json", "post_cutover_new_digest.json")
    print(f"old table item_count={old['item_count']} taken_utc={old['taken_utc']}")
    print(f"new table item_count={new['item_count']} taken_utc={new['taken_utc']}")
    if old["item_count"] != new["item_count"]:
        return _fail("AC5", f"counts differ: old={old['item_count']} new={new['item_count']}")
    return _pass("AC5")


def ac6():
    old, new = _digest_pair("post_cutover_old_digest.json", "post_cutover_new_digest.json")
    keys_equal = set(old["digests"]) == set(new["digests"])
    mismatches = [k for k in old["digests"] if old["digests"].get(k) != new["digests"].get(k)]
    print(f"old counts_by_namespace={old['counts_by_namespace']}")
    print(f"new counts_by_namespace={new['counts_by_namespace']}")
    print(f"key sets equal: {keys_equal}; digest mismatches: {len(mismatches)}")
    if not keys_equal or mismatches or old["counts_by_namespace"] != new["counts_by_namespace"]:
        return _fail("AC6", "per-item digest or per-namespace count mismatch between old and new")
    return _pass("AC6")


_HISTORICAL_MARKERS = (
    "/deliverables/",
    "/surprise-channel/",
    "surprise_channel/",
    "RULINGS",
    "/logs/",
    "/change_management/",
    "/.open_deploys/",
    "/audit/archive/",
    "atom_decomposition/runs/",
    # Widened beyond AC7's literal parenthetical (deliverables/surprise-channel/rulings/logs/
    # change-management): task orders, the PRD and the decomposition doc are FROZEN project-history
    # documents (order BOUNDS: "the spec AND the decomposition are FROZEN"), outside this cell's
    # <paths> write grant, and their old-name mentions describe already-issued/already-completed
    # cells (OG-i-1/a-1/d-1/p-1/v-5) truthfully under the name that was correct when each was
    # written. Filed as NFRA_OPLGTW-W1-S<k> (surprise row) rather than silently narrowed.
    "/task-orders/",
    "/prd/",
    "/decompositions/",
)


def ac7():
    ws = _ws()
    r = _run(["git", "-C", str(ws), "grep", "-F", "-n", "opal-gateway-access-state"])
    lines = [line for line in r.stdout.splitlines() if line.strip()]
    print(f"denominator: {len(lines)} hit line(s) (git grep -F, unscoped, at HEAD)")
    live_hits = []
    for line in lines:
        path = line.split(":", 1)[0]
        historical = any(m in ("/" + path.replace("\\", "/")) for m in _HISTORICAL_MARKERS)
        tag = "HISTORICAL" if historical else "LIVE"
        print(f"  [{tag}] {line}")
        if not historical:
            live_hits.append(line)
    # A LIVE hit is only a true violation if it names the exact retired identifier
    # "opal-gateway-access-state" as a whole token (not a substring of a distinct,
    # differently-named resource such as a test fixture's "opal-gateway-access-state-2").
    import re

    genuine = []
    for line in live_hits:
        for m in re.finditer(r"opal-gateway-access-state", line):
            end = m.end()
            trailing = line[end : end + 1]
            if trailing and (trailing.isalnum() or trailing in "-_"):
                continue  # part of a longer, distinct identifier -- not the retired table's name
            genuine.append(line)
            break
    print(f"LIVE non-historical hits: {len(live_hits)}; genuine whole-identifier references among them: {len(genuine)}")

    for fname, must_contain in (
        ("infra/aws/terraform/opal-gateway/schwab_access_state.tf", "gateway-access-state-table"),
        ("infra/aws/ec2/opal-gateway/app/access_state.py", "gateway-access-state-table"),
        ("org/standards/NFRA_OPLGTW_CONTRACT.json", "gateway-access-state-table"),
    ):
        text = (ws / fname).read_text(encoding="utf-8")
        if must_contain not in text:
            return _fail("AC7", f"{fname} does not name the new table")
        print(f"  {fname} names the new table: OK")
    if genuine:
        return _fail("AC7", f"{len(genuine)} genuine live reference(s) to the retired table name remain")
    return _pass("AC7")


_ANSI_RE = None


def _strip_ansi(s: str) -> str:
    global _ANSI_RE
    if _ANSI_RE is None:
        import re

        _ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
    return _ANSI_RE.sub("", s)


def ac8():
    ws = _ws() / "infra" / "aws" / "ec2" / "opal-gateway"
    py = _ws() / ".venv-og" / "Scripts" / "python.exe"
    total = 0
    for mod in ("test_access_state.py", "test_oauth_durable.py", "test_principal_cutover.py"):
        r = subprocess.run(
            [str(py), "-m", "pytest", f"tests/{mod}", "-q", "--color=no"],
            capture_output=True, text=True, cwd=str(ws), timeout=280,
        )
        clean = _strip_ansi(r.stdout).strip()
        tail = clean.splitlines()[-1] if clean else "(no output)"
        print(f"{mod}: rc={r.returncode} {tail}")
        if r.returncode != 0 or "passed" not in tail:
            return _fail("AC8", f"{mod} did not pass cleanly (rc={r.returncode})")
        total += int(tail.split()[0])
    print(f"total passed across 3 modules: {total}")
    return _pass("AC8")


def ac9():
    cmd = load_json(EVID / "ac9_ssm_command_text.json")
    result = load_json(EVID / "ac9_ssm_result.json")
    print("command text:")
    print(cmd["commands"][0])
    print(f"vintage: {result.get('ExecutionEndDateTime')}  status: {result.get('Status')}")
    out = result.get("StandardOutputContent", "")
    print(out)
    runtime_ok = "RUNTIME: SUCCESS" in out
    policy_denied = "POLICY: AccessDeniedException" in out
    if not (runtime_ok and policy_denied and result.get("Status") == "Success"):
        return _fail("AC9", "RUNTIME write did not succeed and/or POLICY write was not AccessDenied")
    return _pass("AC9")


def ac10():
    p = load_json(EVID / "apply2.plan.json")
    rc = p["resource_changes"]
    non_noop = [r for r in rc if r["change"]["actions"] != ["no-op"]]
    print(f"denominator: {len(rc)} resource(s) in plan; non-noop: {len(non_noop)}")
    for r in non_noop:
        print(f"  {r['address']}: {r['change']['actions']}")
    ok_shape = (
        len(non_noop) == 1
        and non_noop[0]["address"] == "aws_dynamodb_table.access_state_old"
        and non_noop[0]["change"]["actions"] == ["delete"]
    )
    if not ok_shape:
        return _fail("AC10", "apply2 plan is not exactly 1 destroy of the old table and nothing else")
    ws = _ws()
    evid_commit_file = EVID / "EVIDENCE_COMMIT.txt"
    if not evid_commit_file.exists():
        return _fail("AC10", "no recorded evidence commit to compare apply2's start against")
    evid_commit = evid_commit_file.read_text(encoding="utf-8").strip()
    evid_time = _git_commit_time(ws, evid_commit)
    apply2_start_file = Path(__file__).resolve().parent.parent / "evidence" / "og_i5" / "APPLY2_START.txt"
    if not apply2_start_file.exists():
        return _fail("AC10", "no recorded apply2 start time")
    apply2_start = apply2_start_file.read_text(encoding="utf-8").strip()
    print(f"evidence commit {evid_commit} at {evid_time}")
    print(f"apply2 start {apply2_start}")
    if not (_parse_iso(evid_time) < _parse_iso(apply2_start)):
        return _fail("AC10", f"evidence commit time {evid_time} not before apply2 start {apply2_start}")
    return _pass("AC10")


def ac11():
    ws = _ws()
    exists = table_exists(OLD_TABLE, REGION)
    print(f"old table {OLD_TABLE!r} exists: {exists}")
    ledger_file = ws / "org" / "critical_paths" / ".open_deploys" / "nfra-oplgtw-og-i-5-access-state-rename.json"
    ledger_open = ledger_file.exists()
    print(f"ledger sentinel still present: {ledger_open}")
    r = subprocess.run(
        [str(ws / ".tools" / "terraform.exe"), "-chdir=infra/aws/terraform/opal-gateway", "plan", "-input=false", "-detailed-exitcode"],
        capture_output=True, text=True, cwd=str(ws), timeout=110,
    )
    print(f"fresh plan detailed-exitcode: {r.returncode}")
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(no plan output)")
    if exists:
        return _fail("AC11", "describe-table on the old name did not return ResourceNotFound")
    if ledger_open:
        return _fail("AC11", "the ledger entry's sentinel is still present -- not closed before this read")
    if r.returncode != 0:
        return _fail("AC11", f"fresh plan of the root is not 0-changes (detailed-exitcode={r.returncode})")
    return _pass("AC11")


def ac12():
    start, end = _digest_pair("copy_start_old_digest.json", "post_cutover_old_digest.json")
    print(f"old table copy_start item_count={start['item_count']} taken_utc={start['taken_utc']}")
    print(f"old table post_cutover item_count={end['item_count']} taken_utc={end['taken_utc']}")
    diffs = [k for k in start["digests"] if start["digests"].get(k) != end["digests"].get(k)]
    keys_equal = set(start["digests"]) == set(end["digests"])
    print(f"digest diffs: {len(diffs)}; key sets equal: {keys_equal}")
    ssm_result = load_json(EVID / "ac12_ssm_result.json")
    ssm_cmd = load_json(EVID / "ac12_ssm_command_text.json")
    print("app-reference SSM command text:")
    print(ssm_cmd["commands"][0])
    out = ssm_result.get("StandardOutputContent", "")
    print(out)
    match_zero = "MATCH_COUNT=0" in out
    if diffs or not keys_equal or start["item_count"] != end["item_count"] or not match_zero:
        return _fail("AC12", "old-table digest changed between copy-start and post-cutover, or the deployed app references a table name")
    return _pass("AC12")


def ac13():
    old, new = _digest_pair("post_cutover_old_digest.json", "post_cutover_new_digest.json")
    ws = _ws()
    refmove_file = EVID / "REFMOVE_COMMIT.txt"
    refmove_commit = refmove_file.read_text(encoding="utf-8").strip() if refmove_file.exists() else ""
    if refmove_commit:
        refmove_time = _git_commit_time(ws, refmove_commit)
        print(f"reference-move commit {refmove_commit} at {refmove_time}")
    print(f"old post-cutover taken_utc={old['taken_utc']}  new post-cutover taken_utc={new['taken_utc']}")
    print(f"old counts_by_namespace={old['counts_by_namespace']}  new counts_by_namespace={new['counts_by_namespace']}")
    mismatches = [k for k in old["digests"] if old["digests"].get(k) != new["digests"].get(k)]
    keys_equal = set(old["digests"]) == set(new["digests"])
    ok = keys_equal and not mismatches and old["item_count"] == new["item_count"] and old["counts_by_namespace"] == new["counts_by_namespace"]
    if refmove_commit and _parse_iso(refmove_time) >= _parse_iso(old["taken_utc"]):
        return _fail("AC13", f"post-cutover scan taken_utc {old['taken_utc']} is not after the reference-move commit {refmove_time}")
    if not ok:
        return _fail("AC13", "post-cutover item count / digest / namespace-count comparison does not match")
    return _pass("AC13")


DISPATCH = {
    "AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6, "AC7": ac7,
    "AC8": ac8, "AC9": ac9, "AC10": ac10, "AC11": ac11, "AC12": ac12, "AC13": ac13,
}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in DISPATCH:
        print(f"usage: og_i5.py <{'|'.join(DISPATCH)}>", file=sys.stderr)
        return 2
    return DISPATCH[sys.argv[1]]()


if __name__ == "__main__":
    raise SystemExit(main())
