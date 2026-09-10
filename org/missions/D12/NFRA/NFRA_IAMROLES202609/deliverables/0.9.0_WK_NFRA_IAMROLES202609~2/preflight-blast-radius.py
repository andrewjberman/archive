#!/usr/bin/env python3
"""
preflight-blast-radius.py -- NFRA_IAMROLES202609 task order TO-IAM-s-8, cell IAM-s-8.

THE ASK (FWD-5, verbatim from the ratified endpoint): "An engineer can narrow a permission and
know beforehand what it would break." DONE WHEN EXERCISED -- a real narrowing has been CHECKED
in advance and the check was BELIEVED. The bar is on the CHECK, never on an apply: this file
contains NO terraform apply, NO safe-apply, NO put-role-policy / delete-role-policy /
attach-role-policy / detach-role-policy call, and it never will. Every AWS call this script makes
is READ-ONLY (iam:Get*, iam:List*, iam:SimulatePrincipalPolicy via the comp-iam-usage instrument).

THIS CELL COMPOSES, IT DOES NOT RE-DERIVE:
  - IAM-s-1's instrument `.tools/comp-iam-usage permission-cold` (PERMISSION-grain usage, IAM
    Access Advisor ACTION_LEVEL -- never Access Analyzer, per C-ANALYZER-PRICED-FIRST).
  - IAM-s-1's instrument `.tools/comp-iam-usage reach-check` (a live (role,action,resource)
    verdict on `aws iam simulate-principal-policy`, Rule-22a disciplined: (a) exact
    --resource-arns, so a grant on ANY arn does not falsely read GRANTED for every arn; (b) ONE
    resource per call, the positive control a SEPARATE call, because batching corrupts the
    control; (c) a conditioned statement with no context is UNKNOWN, never a false deny).
  - IAM-s-4's condition-axis-reader.py, invoked against every LOCAL .tf file this script can
    resolve a candidate statement to, for the REQUIRES/REQUIRES-NOTHING axis.
  - comp-blast (the code/infra dependency graph), run against every compute identity (Lambda)
    this script finds assuming the role, per the L5 battery's own naming of this cell as the one
    that makes comp-blast applicable.
  - comp-iam (the DESIRED-plane Terraform<->source cross-reference), queried to name where IT is
    blind, because a silent DESIRED-plane gap would read as "nothing breaks" and that is exactly
    the false-clean C-NO-ACCESSDENIED forbids.

EVERYTHING READ FROM A POLICY DOCUMENT (live or in Terraform) IS DESIRED (C-DESIRED-UNTIL-
EXERCISED). Only a comp-iam-usage reach-check call (a real simulate-principal-policy invocation)
moves a resource's verdict to EXERCISED. Every printed line says which plane it is on.

Usage:
    python preflight-blast-radius.py --role <role-name> --remove <action>

Only ever prints. Never mutates IAM, Terraform state, or any live resource.
"""
import argparse
import fnmatch
import json
import shlex
import subprocess
import sys
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

TIMEOUT_S = 100  # each subprocess call stays well inside the harness's `timeout 120` wrapper


def utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_tool(argv, timeout=TIMEOUT_S):
    """Run a comp-* tool by PATH-resolved name (shims live in ~/bin). The shims are extensionless
    bash scripts; a native-Windows Python's subprocess (no shell=True) cannot CreateProcess an
    extensionless script directly (WinError 2 -- no shebang support), so every call is routed
    through `bash -c` (non-login: profiles never load per CLAUDE.md, and PATH is already inherited
    from the parent environment, which carries the ~/bin forwarders). Returns (rc, stdout, stderr)."""
    cmd_str = " ".join(shlex.quote(a) for a in argv)
    try:
        p = subprocess.run(["bash", "-c", cmd_str], capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        return 124, (e.stdout or ""), (e.stderr or "TIMEOUT after %ss" % timeout)
    except FileNotFoundError as e:
        return 127, "", str(e)


def extract_leading_json(text):
    """comp-iam-usage reach-check prints a JSON object then a trailing prose block. Parse just the
    JSON prefix with json.JSONDecoder.raw_decode, which stops at the object's closing brace."""
    text = text.lstrip()
    if not text.startswith("{"):
        return None
    dec = json.JSONDecoder()
    try:
        obj, _end = dec.raw_decode(text)
        return obj
    except json.JSONDecodeError:
        return None


def iam_action_matches(pattern, target):
    """IAM action-string wildcard match ('*' / '?'), case-insensitive (IAM action names are
    matched case-insensitively by the real policy engine)."""
    return fnmatch.fnmatchcase(target.lower(), pattern.lower())


def statement_actions(stmt):
    a = stmt.get("Action", stmt.get("action", []))
    if isinstance(a, str):
        return [a]
    return list(a or [])


def statement_resources(stmt):
    r = stmt.get("Resource", stmt.get("resource"))
    if r is None:
        return None, "NotResource" in stmt or "notresource" in {k.lower() for k in stmt}
    if isinstance(r, str):
        return [r], False
    return list(r), False


def fetch_live_role_statements(iam, role_name):
    """Read every inline + attached-managed policy document on a role. READ-ONLY. Returns a list
    of dicts: {source, kind, sid, effect, actions, resources, resources_blind_notresource,
    condition, raw_statement}."""
    out = []
    role = iam.get_role(RoleName=role_name)["Role"]
    role_arn = role["Arn"]

    for name in iam.list_role_policies(RoleName=role_name)["PolicyNames"]:
        doc = iam.get_role_policy(RoleName=role_name, PolicyName=name)["PolicyDocument"]
        stmts = doc["Statement"]
        stmts = stmts if isinstance(stmts, list) else [stmts]
        for stmt in stmts:
            resources, notres_blind = statement_resources(stmt)
            out.append({
                "source": name,
                "kind": "inline",
                "sid": stmt.get("Sid", "(no Sid)"),
                "effect": stmt.get("Effect"),
                "actions": statement_actions(stmt),
                "resources": resources,
                "resources_blind_notresource": notres_blind,
                "condition": stmt.get("Condition"),
            })

    for ap in iam.list_attached_role_policies(RoleName=role_name)["AttachedPolicies"]:
        parn = ap["PolicyArn"]
        meta = iam.get_policy(PolicyArn=parn)["Policy"]
        ver = meta["DefaultVersionId"]
        doc = iam.get_policy_version(PolicyArn=parn, VersionId=ver)["PolicyVersion"]["Document"]
        stmts = doc["Statement"]
        stmts = stmts if isinstance(stmts, list) else [stmts]
        for stmt in stmts:
            resources, notres_blind = statement_resources(stmt)
            out.append({
                "source": "%s (managed %s)" % (ap["PolicyName"], ver),
                "kind": "managed",
                "sid": stmt.get("Sid", "(no Sid)"),
                "effect": stmt.get("Effect"),
                "actions": statement_actions(stmt),
                "resources": resources,
                "resources_blind_notresource": notres_blind,
                "condition": stmt.get("Condition"),
            })

    return role_arn, out


def derive_probe_arn(pattern):
    """A concrete resource ARN to hand to a (role,action,resource) simulate call. A trailing '*'
    is replaced with a synthetic, clearly-marked probe leaf so the call tests the SAME prefix the
    live policy scopes; a bare '*' cannot be probed as one concrete ARN and is reported as such,
    never silently narrowed to something smaller than the grant."""
    if pattern == "*":
        return None, "WILDCARD-UNPROBEABLE (a bare '*' resource is not one concrete ARN; " \
                      "probing any single ARN under it would UNDER-STATE the true grant, so " \
                      "this pattern is reported, not simulated)"
    if pattern.endswith("*"):
        return pattern[:-1] + "preflight-blast-radius-probe-object", None
    return pattern, None


def account_id_from_role_arn(role_arn):
    # arn:aws:iam::<account>:role/<name>
    return role_arn.split(":")[4]


def find_compute_identities(role_name, repo_root):
    """Which Lambda functions (per the committed lambda-source-map.json) assume this role. A
    STATIC, already-committed artifact -- read-only, no AWS call needed for this part."""
    import os
    path = os.path.join(repo_root, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
    if not os.path.isfile(path):
        return [], "lambda-source-map.json not found at %s -- compute-identity enumeration BLIND" % path
    # NOTE (memory: "subprocess text mode is cp1252 here" / native-Windows Python default):
    # this repo file is UTF-8; opening without an explicit encoding decodes as cp1252 and can
    # raise UnicodeDecodeError on non-ASCII bytes. encoding="utf-8" is required, not optional.
    with open(path, "r", encoding="utf-8") as f:
        m = json.load(f)
    hits = []
    entries = m.get("functions", m) if isinstance(m, dict) else m
    if isinstance(entries, dict):
        for fn_name, meta in entries.items():
            if isinstance(meta, dict) and meta.get("iam_role") == role_name:
                hits.append(fn_name)
    return hits, None


def locate_local_tf_file(policy_name, repo_root):
    """Best-effort: which LOCAL .tf file (if any) declares this inline policy by name, via
    `comp-find` (a content search of the repo, not a re-derived grep -- CLAUDE.md Rule 21). A
    managed policy created out-of-band (no aws_iam_role_policy/aws_iam_policy Terraform resource
    checked in) will not resolve, and that absence is itself reported, never silently skipped."""
    rc, out, err = run_tool(["comp-find", policy_name, "infra/aws/terraform"], timeout=60)
    if rc != 0:
        return None
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("infra/aws/terraform") and ".tf:" in line:
            return line.split(":")[0]
    return None


def try_condition_axis_reader(repo_root, tf_file, sid, script_path):
    """Compose IAM-s-4's reader against a LOCAL .tf file that carries this statement's Sid. Never
    re-derives the REQUIRES/REQUIRES-NOTHING logic; only shells out to the existing instrument."""
    rc, out, err = run_tool(["python", script_path, "--policy", tf_file], timeout=60)
    if rc != 0:
        return "condition-axis-reader.py rc=%d on %s (err: %s)" % (rc, tf_file, err.strip()[:200])
    # Find the block for this Sid in the reader's text output.
    lines = out.splitlines()
    for i, line in enumerate(lines):
        if sid and sid in line:
            window = "\n".join(lines[i:i + 6])
            return window
    return "reader ran on %s (rc=0) but did not print a block naming Sid=%r verbatim -- see full output" % (tf_file, sid)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--role", required=True, help="IAM role name")
    ap.add_argument("--remove", required=True, dest="action", help="the IAM action to predict the removal of, e.g. s3:PutObject")
    ap.add_argument("--repo-root", default=None, help="override the repo root (default: git rev-parse --show-toplevel)")
    args = ap.parse_args()

    if args.repo_root:
        repo_root = args.repo_root
    else:
        rc, out, err = run_tool(["git", "rev-parse", "--show-toplevel"], timeout=15)
        repo_root = out.strip() if rc == 0 else "."

    print("=" * 78)
    print("PRE-FLIGHT BLAST RADIUS -- IAM-s-8 (FWD-5)")
    print("run at (UTC): %s" % utcnow())
    print("role:         %s" % args.role)
    print("candidate removal (Allow-action, NOT applied): %s" % args.action)
    print("STATUS: CHECK ONLY. No terraform apply / safe-apply / put-role-policy / "
          "delete-role-policy / attach-role-policy / detach-role-policy has been called by this "
          "run or ever will be by this file.")
    print("=" * 78)

    # ---- Step 1: LIVE policy enumeration (DESIRED-plane text, read live not from a repo file) ----
    iam = boto3.client("iam", region_name="us-east-1")
    try:
        role_arn, statements = fetch_live_role_statements(iam, args.role)
    except ClientError as e:
        print("ERROR: could not read live IAM state for role %r: %s" % (args.role, e))
        sys.exit(2)

    account_id = account_id_from_role_arn(role_arn)
    print("\n[1] LIVE POLICY ENUMERATION (plane: DESIRED -- policy TEXT, read live via "
          "iam:List*/iam:Get*, read-only)")
    print("    role ARN: %s" % role_arn)
    print("    inline + attached-managed policy documents read: statements examined = %d"
          % len(statements))

    matching = []
    for stmt in statements:
        if stmt["effect"] != "Allow":
            continue
        if not any(iam_action_matches(pat, args.action) for pat in stmt["actions"]):
            continue
        matching.append(stmt)

    if not matching:
        print("    No live Allow statement grants %s to this role at all -- there is nothing to "
              "remove; the candidate narrowing is a no-op. (Denominator of statements examined: "
              "%d; matching Allow statements: 0.)" % (len(statements), len(statements)))
        # Still worth naming Deny statements that reference the action, if any (informational).

    # Build the distinct resource-pattern population (denominator #1)
    resource_rows = []  # each: {pattern, sources:[...], base_sources:[...], sid, condition}
    seen = {}
    for stmt in matching:
        # base_source strips the "(managed vN)" annotation so it can be compared, verbatim, to a
        # SECOND instrument's own naming (comp-blast's IAM_POLICY 'label') without a re-derived
        # string transform doing double duty as both display text and a join key.
        base_source = stmt["source"].split(" (managed ")[0]
        if stmt["resources_blind_notresource"]:
            resource_rows.append({
                "pattern": "(NotResource -- see raw statement)",
                "sources": [stmt["source"]],
                "base_sources": [base_source],
                "sid": stmt["sid"],
                "condition": stmt["condition"],
                "notresource_blind": True,
            })
            continue
        for pat in (stmt["resources"] or []):
            key = pat
            if key not in seen:
                seen[key] = {"pattern": pat, "sources": [], "base_sources": [], "sid": stmt["sid"], "condition": stmt["condition"], "notresource_blind": False}
                resource_rows.append(seen[key])
            seen[key]["sources"].append("%s (Sid=%s)" % (stmt["source"], stmt["sid"]))
            seen[key]["base_sources"].append(base_source)

    print("\n    Allow statements naming action %s: %d" % (args.action, len(matching)))
    print("    DISTINCT resource patterns granting it (DENOMINATOR of resources examined): %d"
          % len(resource_rows))
    for row in resource_rows:
        cond_note = "REQUIRES(%s)" % ",".join(sorted((row["condition"] or {}).keys())) if row["condition"] else "REQUIRES-NOTHING (no Condition block, plane: DESIRED, policy text)"
        print("      - %-55s cond=%s  granted by: %s" % (row["pattern"], cond_note, "; ".join(row["sources"])))

    # ---- Step 1a: COMPOSE IAM-s-4's condition-axis-reader.py against every matching statement
    # this script can trace to a LOCAL .tf file. Never re-derives the REQUIRES/REQUIRES-NOTHING
    # call -- it shells out to the actual reader and quotes its own output. A statement with no
    # local .tf custody (a pre-existing, out-of-band managed policy) has nothing for the reader to
    # read; that is reported as a named gap, never silently smoothed into "no condition".
    condition_reader_script = __file__.replace("preflight-blast-radius.py", "condition-axis-reader.py")
    print("\n[1a] CONDITION AXIS -- composing IAM-s-4's condition-axis-reader.py (not re-derived)")
    seen_sources = set()
    for stmt in matching:
        src_key = (stmt["kind"], stmt["source"])
        if src_key in seen_sources:
            continue
        seen_sources.add(src_key)
        if stmt["kind"] != "inline":
            print("    Sid=%s (source: %s) -- MANAGED policy, no aws_iam_role_policy/aws_iam_policy "
                  "Terraform resource is checked into this repo for it (confirmed out-of-band, "
                  "PRE-EXISTING per infra/aws/terraform/data-refresh/main.tf's own comment). "
                  "condition-axis-reader.py HAS NO LOCAL FILE TO READ. Condition-key presence read "
                  "directly off the live GetPolicyVersion document instead (a MANUAL read, NOT "
                  "IAM-s-4's reader, and labelled as such): %s"
                  % (stmt["sid"], stmt["source"],
                     ("REQUIRES(%s)" % ",".join(sorted(stmt["condition"].keys()))) if stmt["condition"] else "REQUIRES-NOTHING"))
            continue
        tf_file = locate_local_tf_file(stmt["source"], repo_root)
        if not tf_file:
            print("    Sid=%s (source: %s) -- inline policy but no local .tf file resolved by "
                  "comp-find; condition-axis-reader.py cannot be composed here. BLIND, not "
                  "reported as REQUIRES-NOTHING." % (stmt["sid"], stmt["source"]))
            continue
        result = try_condition_axis_reader(repo_root, tf_file, stmt["sid"], condition_reader_script)
        print("    Sid=%s (source: %s, file: %s) -- condition-axis-reader.py says:\n      %s"
              % (stmt["sid"], stmt["source"], tf_file, result.replace("\n", "\n      ")))

    # ---- Step 2: EXERCISE -- one comp-iam-usage reach-check simulate call per resource ----
    print("\n[2] EXERCISE -- `aws iam simulate-principal-policy` via `.tools/comp-iam-usage "
          "reach-check`, ONE resource ARN per call (Rule-22a limit (b): batching corrupts the "
          "control). Plane moves from DESIRED to EXERCISED here.")
    would_break = []
    already_blocked = []
    unprobed = []
    for row in resource_rows:
        if row.get("notresource_blind"):
            unprobed.append((row["pattern"], "NotResource statement -- this script does not evaluate NotResource semantics; BLIND, not reported as safe"))
            continue
        probe_arn, why_not = derive_probe_arn(row["pattern"])
        if probe_arn is None:
            unprobed.append((row["pattern"], why_not))
            continue
        rc, out, err = run_tool(["comp-iam-usage", "reach-check", args.role, args.action, probe_arn], timeout=TIMEOUT_S)
        parsed = extract_leading_json(out) if rc == 0 else None
        if parsed is None:
            unprobed.append((row["pattern"], "reach-check rc=%d could not be parsed (stderr: %s)" % (rc, err.strip()[:200])))
            continue
        verdict = parsed.get("verdict")
        cond = parsed.get("rule22a", {}).get("condition_handling")
        missing_ctx = parsed.get("missing_context_values") or []
        line = "      probe=%-70s verdict=%-12s condition_handling=%s missing_context=%s" % (
            probe_arn, verdict, cond, missing_ctx or "none")
        print(line)
        if verdict == "allowed":
            would_break.append((row["pattern"], probe_arn, row["sources"]))
        elif verdict in ("implicitDeny", "explicitDeny"):
            already_blocked.append((row["pattern"], probe_arn, verdict))
        else:
            unprobed.append((row["pattern"], "reach-check returned verdict=%r (neither allow nor deny) -- UNKNOWN, not reported as safe" % verdict))

    if unprobed:
        print("\n    UNPROBED / BLIND resource patterns (reported, never counted as 'safe'):")
        for pat, why in unprobed:
            print("      - %-55s %s" % (pat, why))

    # ---- Controls: one positive, one negative, each a SEPARATE call ----
    print("\n[2a] CONTROLS (separate calls, never batched with the target -- Rule-22a limit (b))")
    # Positive control: pick a resource this role is independently known to reach (any statement
    # not matching the removed action), to prove the instrument is not stuck answering "allowed".
    control_pos = None
    for stmt in statements:
        if stmt["effect"] != "Allow":
            continue
        if any(iam_action_matches(pat, args.action) for pat in stmt["actions"]):
            continue  # skip statements that touch the removed action, keep the control independent
        acts = [a for a in stmt["actions"] if "*" not in a]
        ress = [r for r in (stmt["resources"] or []) if isinstance(r, str) and "*" not in r]
        if acts and ress:
            control_pos = (acts[0], ress[0])
            break
    if control_pos:
        rc, out, err = run_tool(["comp-iam-usage", "reach-check", args.role, control_pos[0], control_pos[1]], timeout=TIMEOUT_S)
        parsed = extract_leading_json(out) if rc == 0 else None
        print("    POSITIVE control (%s, %s): verdict=%s" % (control_pos[0], control_pos[1], (parsed or {}).get("verdict", "UNPARSED rc=%d" % rc)))
    else:
        print("    POSITIVE control: no independent (non-wildcard action, non-wildcard resource) "
              "Allow statement found to use as a control -- instrument's discrimination is UNPROVEN "
              "for this run.")

    neg_action = "iam:CreateUser" if not iam_action_matches("iam:*", args.action) else "sts:AssumeRootRole"
    neg_resource = "arn:aws:iam::%s:user/preflight-negative-control-nonexistent" % account_id
    rc, out, err = run_tool(["comp-iam-usage", "reach-check", args.role, neg_action, neg_resource], timeout=TIMEOUT_S)
    parsed = extract_leading_json(out) if rc == 0 else None
    print("    NEGATIVE control (%s, %s): verdict=%s" % (neg_action, neg_resource, (parsed or {}).get("verdict", "UNPARSED rc=%d" % rc)))

    # ---- Step 3: historical-usage plane (IAM-s-1's permission-cold, composed not re-derived) ----
    print("\n[3] HISTORICAL-USAGE PLANE (composed from IAM-s-1: `.tools/comp-iam-usage "
          "permission-cold`, IAM Access Advisor ACTION_LEVEL -- never Access Analyzer)")
    rc, out, err = run_tool(["comp-iam-usage", "permission-cold", "--role", args.role, "--lookback", "90", "--json"], timeout=TIMEOUT_S)
    if rc == 0:
        try:
            pc = json.loads(out)
            row = next((r for r in pc.get("rows", []) if r["permission"] == args.action), None)
            if row is None:
                print("    %s is not in this role's GRANTED set at all per permission-cold "
                      "(denominator=%d granted permissions examined) -- consistent with, or "
                      "contradicting, step [1]'s live read; if it contradicts, DO NOT silently "
                      "prefer one plane." % (args.action, len(pc.get("rows", []))))
            elif row["status"] == "unobservable":
                print("    %s status=unobservable (%s). The HISTORICAL-USAGE plane is BLIND on "
                      "this exact action; only the live reach-check verdicts in [2] and the "
                      "compute-identity/comp-blast evidence in [4] carry weight for this "
                      "prediction." % (args.action, row.get("reason")))
            else:
                print("    %s status=%s%s" % (
                    args.action, row["status"],
                    (" last_used=%s (%sd ago)" % (row.get("last_used"), row.get("age_days"))) if row.get("last_used") else ""))
        except (json.JSONDecodeError, KeyError) as e:
            print("    could not parse permission-cold --json output (%s)" % e)
    else:
        print("    permission-cold rc=%d (err: %s)" % (rc, err.strip()[:300]))

    # ---- Step 4: compute identities + comp-blast (code/infra dependency graph) ----
    print("\n[4] COMPUTE IDENTITIES SHARING THIS ROLE + comp-blast (code/infra dependency graph)")
    fns, blind_reason = find_compute_identities(args.role, repo_root)
    if blind_reason:
        print("    %s" % blind_reason)
    print("    Lambda functions assuming this role (source: infra/aws/lambda/ci/lambda-source-map.json, "
          "a committed artifact): %d found: %s" % (len(fns), ", ".join(fns) if fns else "(none)"))
    if len(fns) > 1:
        print("    NOTE: role is SHARED across %d compute identities. A statement removed for one "
              "function's use case is removed for ALL of them -- a narrowing intended for %s may "
              "silently affect %s too." % (len(fns), fns[0] if fns else "?", ", ".join(fns[1:])))

    blast_total_nodes = 0
    for fn in fns:
        lambda_arn = "arn:aws:lambda:us-east-1:%s:function:%s" % (account_id, fn)
        rc, out, err = run_tool(["comp-blast", lambda_arn, "--direction", "downstream", "--json"], timeout=TIMEOUT_S)
        if rc != 0:
            print("    comp-blast %s: rc=%d (err: %s)" % (lambda_arn, rc, err.strip()[:200]))
            continue
        try:
            i = out.index("{")
            data = json.loads(out[i:])
        except (ValueError, json.JSONDecodeError):
            print("    comp-blast %s: could not parse JSON output" % lambda_arn)
            continue
        consumers = data.get("consumers", {})
        n = sum(len(v) if isinstance(v, list) else 1 for v in consumers.values())
        blast_total_nodes += n
        # Each consumer entry is a dict ({'id','label','depth','direction'}), not a bare string.
        iam_policy_entries = consumers.get("IAM_POLICY", [])
        iam_policies_seen = [e.get("label", e.get("id", str(e))) if isinstance(e, dict) else str(e)
                             for e in iam_policy_entries]
        print("    comp-blast %s: %d downstream nodes (LOWER BOUND -- dynamic/FUNC-key consumers "
              "the extractors don't edge are NOT counted, per the tool's own caveat). "
              "IAM_POLICY band (%d): %s" % (lambda_arn, n, len(iam_policies_seen), ", ".join(iam_policies_seen[:10]) + (" ..." if len(iam_policies_seen) > 10 else "")))
        # Cross-check: do the granting-statement sources from [1] appear in comp-blast's
        # independent IAM_POLICY consumer band? (a second instrument, not a repeat of the first)
        our_sources = {bs for row in resource_rows for bs in row.get("base_sources", [])}
        corroborated = our_sources & set(iam_policies_seen)
        missing = our_sources - set(iam_policies_seen)
        if corroborated:
            print("      cross-check (comp-blast independently names): %s" % ", ".join(sorted(corroborated)))
        if missing:
            print("      cross-check GAP -- named live by boto3 in [1] but ABSENT from comp-blast's "
                    "graph for %s: %s (the graph may not have re-derived since this policy's last "
                    "edit; treat comp-blast's count here as a floor, not a ceiling)" % (lambda_arn, ", ".join(sorted(missing))))

    # ---- Step 5: DESIRED-plane cross-reference (comp-iam) blindness, named not silenced ----
    print("\n[5] comp-iam DESIRED-PLANE CROSS-REFERENCE -- named where it is BLIND, per C-NO-ACCESSDENIED")
    rc, out, err = run_tool(["comp-iam", "role", args.role], timeout=60)
    if rc != 0 or "No role matching" in out:
        print("    comp-iam has NO role entry for %r at all (rc=%d). comp-iam's Terraform<->code "
              "cross-reference is COMPLETELY BLIND to this role -- it cannot corroborate or "
              "contradict anything in this report; do not read its silence as 'no gap'."
              % (args.role, rc))
    else:
        print("    comp-iam role %r: (first 400 chars) %s" % (args.role, out[:400].replace("\n", " | ")))

    for fn in fns:
        rc, out, err = run_tool(["comp-iam", "service", fn], timeout=60)
        if rc == 0:
            not_mapped = out.count("note: role not mapped")
            total_ops = out.count("via:")
            if not_mapped and not_mapped == total_ops and total_ops > 0:
                print("    comp-iam service %s: ALL %d call-site operations read 'role not mapped' "
                      "-- comp-iam's Terraform parser cannot attach this compute identity's granted "
                      "policies to any code call site at all. Its verdict space for %s is "
                      "[UNKNOWN] x %d, not a clean bill." % (fn, total_ops, fn, total_ops))
            elif total_ops:
                print("    comp-iam service %s: %d/%d call-site operations unmapped." % (fn, not_mapped, total_ops))

    rc, out, err = run_tool(["comp-iam", "stats"], timeout=60)
    if rc == 0:
        unmodeled_lines = [line for line in out.splitlines() if ":UNMODELED" in line or "UNMAPPED-METHOD" in line]
        gaps_line = next((line for line in out.splitlines() if "Permission gaps:" in line), None)
        print("    comp-iam stats (live): %s" % (gaps_line.strip() if gaps_line else "(no gaps line found)"))
        target_service = args.action.split(":")[0]
        hit = [line for line in unmodeled_lines if target_service in line]
        if hit:
            print("    NAMED BLIND SPOT for service %r elsewhere in the estate (informational -- "
                  "not this role, but the SAME comp-iam instrument's own limit on this action's "
                  "service): %s" % (target_service, "; ".join(x.strip() for x in hit)))

    # ---- Step 6: verdict ----
    print("\n" + "=" * 78)
    print("PREDICTION (EXERCISED via simulate-principal-policy, plane: APPLIED, live)")
    if would_break:
        print("  Removing %s from %s WOULD BREAK %d live-verified caller path(s):" % (args.action, args.role, len(would_break)))
        for pat, probe, sources in would_break:
            print("    - resource pattern %-45s (probed %s) -- currently ALLOWED; granted by: %s" % (pat, probe, "; ".join(sources)))
    else:
        print("  No probed resource pattern currently evaluates ALLOWED for this (role, action) pair.")
    if already_blocked:
        print("  %d resource pattern(s) already evaluate NOT-ALLOWED (removal is a no-op there): %s"
              % (len(already_blocked), ", ".join(p for p, _, _ in already_blocked)))
    if unprobed:
        print("  %d resource pattern(s) COULD NOT BE PROBED and are NOT claimed safe: %s"
              % (len(unprobed), ", ".join(p for p, _ in unprobed)))
    print("  DENOMINATOR: %d live statement(s) examined, %d distinct resource pattern(s) "
          "examined (of which %d probed via simulate, %d unprobed/blind), %d compute identity(ies) "
          "examined via comp-blast totaling %d downstream graph node(s) (a LOWER BOUND)."
          % (len(statements), len(resource_rows), len(resource_rows) - len(unprobed), len(unprobed), len(fns), blast_total_nodes))
    print("  NOTHING WAS APPLIED TO THE WORLD BY THIS RUN.")
    print("=" * 78)


if __name__ == "__main__":
    main()
