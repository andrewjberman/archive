"""IRPT_ANLREQ AR-g-102 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g102_checks.py g102     the release-33 SOURCE: the source map re-pins exactly six irpt-ycharts-generate rows (one new) and one
                                     irpt-status row to pins whose blobs equal HEAD's, byte-preserving; the generated package differs from the
                                     base build in exactly those members; generate.tf gains the IRPT_TICKETS_TABLE variable and ONE inline
                                     policy of ONE statement (GetItem on the one table) and nothing else
    python ar_g102_checks.py scope    the branch changed only the map, generate.tf and the cell's own files (against the merge-base with box/dell2)

Prints one RESULT line: AR-G102-OK / AR-G102-FAIL or AR-G102-SCOPE-OK / AR-G102-SCOPE-FAIL; rc 0 only on OK. ASCII only.
"""
import difflib
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

MAP = "infra/aws/lambda/ci/lambda-source-map.json"
TF = "infra/aws/terraform/investor-reporting/ycharts/generate.tf"
IR = "infra/aws/lambda/investor-reporting/"
GEN, STATUS = "irpt-ycharts-generate", "irpt-status"
EXPECT_REPIN = {GEN: {"portfolio.py": IR + "intake/portfolio.py", "uploads.py": IR + "intake/uploads.py",
                      "acceptance.py": IR + "ycharts/generate/acceptance.py", "submission_service.py": IR + "ycharts/generate/submission_service.py",
                      "generate_installed.py": IR + "reports/generate_installed.py"},
                STATUS: {"status.py": IR + "ops/status.py"}}
NEW_ROW = ("ticket_confirmation.py", IR + "ycharts/generate/ticket_confirmation.py")
ARN = "arn:aws:dynamodb:${var.aws_region}:${data.aws_caller_identity.current.account_id}:table/opal-tickets"
POLICY_NAME = "irpt-ycharts-generate-ticket-read-policy"
OWN = (MAP, TF)
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
HEX40, HEX64 = re.compile(r"[0-9a-f]{40}"), re.compile(r"[0-9a-f]{64}")


def git_text(*args):
    out = subprocess.run(["git", *args], capture_output=True)
    return out.returncode, out.stdout


def merge_base():
    rc, out = git_text("merge-base", "HEAD", "box/dell2")
    return out.decode().strip() if rc == 0 else None


def blob_bytes(ref, path):
    rc, out = git_text("show", "%s:%s" % (ref, path))
    return out if rc == 0 else None


def members(smap, function, ref):
    """The member bytes the builder would zip: staged rows from their pins, the rest from the working tree at the source dir."""
    entry = smap["functions"][function]
    src = entry["source_dir"].strip("/")
    staged = {}
    for row in entry.get("staged_from") or []:
        data = blob_bytes(row["pin"], row["repo_path"])
        if data is None:
            raise ValueError("blob missing for %s@%s" % (row["repo_path"], row["pin"][:10]))
        staged[row["packaged_as"]] = data
    out = {}
    for f in entry["files"]:
        out[f] = staged[f] if f in staged else Path(src + "/" + f).read_bytes()
    return out


def extract_block(text, start_pattern):
    m = re.search(start_pattern, text)
    if not m:
        return None
    depth, i = 0, m.end() - 1
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[m.start():i + 1]
        i += 1
    return None


def cases():
    out = []

    def case(name, ok, why=""):
        out.append((name, bool(ok), why))

    base_ref = merge_base()
    if base_ref is None:
        raise ValueError("no merge-base with box/dell2")
    base_text = blob_bytes(base_ref, MAP).decode("utf-8")
    new_bytes = Path(MAP).read_bytes()
    new_text = new_bytes.decode("utf-8")
    base_map, new_map = json.loads(base_text), json.loads(new_text)
    # M1: the only differences in the whole map
    expected_rows = {fn: dict(rows) for fn, rows in EXPECT_REPIN.items()}
    problems = []
    for fn in set(base_map["functions"]) | set(new_map["functions"]):
        b, n = base_map["functions"].get(fn), new_map["functions"].get(fn)
        if fn not in (GEN, STATUS):
            if b != n:
                problems.append("function changed: " + fn)
            continue
        bn = {k: v for k, v in b.items() if k not in ("staged_from", "files")}
        nn = {k: v for k, v in n.items() if k not in ("staged_from", "files")}
        if bn != nn:
            problems.append("fields changed in " + fn)
        brows = {r["packaged_as"]: r for r in b["staged_from"]}
        nrows = {r["packaged_as"]: r for r in n["staged_from"]}
        for name in set(brows) | set(nrows):
            if name in expected_rows.get(fn, {}):
                if brows[name]["repo_path"] != nrows[name]["repo_path"] or brows[name]["packaged_as"] != nrows[name]["packaged_as"]:
                    problems.append("row identity changed: %s %s" % (fn, name))
                if brows[name] == nrows[name]:
                    problems.append("row not re-pinned: %s %s" % (fn, name))
            elif fn == GEN and name == NEW_ROW[0]:
                if name in brows or name not in nrows or nrows[name]["repo_path"] != NEW_ROW[1]:
                    problems.append("the new row is wrong")
            elif brows.get(name) != nrows.get(name):
                problems.append("an unexpected row changed: %s %s" % (fn, name))
        if len(n["staged_from"]) != len(nrows):
            problems.append("duplicate packaged_as in " + fn)
        expect_files = list(b["files"]) + ([NEW_ROW[0]] if fn == GEN else [])
        if sorted(n["files"]) != sorted(expect_files) or len(n["files"]) != len(set(n["files"])):
            problems.append("the files list is not the base plus ticket_confirmation.py")
    for key in set(base_map) | set(new_map):
        if key != "functions" and base_map.get(key) != new_map.get(key):
            problems.append("top-level key changed: " + key)
    case("M1-only-the-expected-rows-change", not problems, "; ".join(problems)[:240])
    # M2: each re-pinned or new row binds a pin whose blob is HEAD's
    bad = []
    rows_checked = 0
    for fn, rows in list(EXPECT_REPIN.items()) + [(GEN, {NEW_ROW[0]: NEW_ROW[1]})]:
        for row in new_map["functions"][fn]["staged_from"]:
            if row["packaged_as"] not in rows:
                continue
            rows_checked += 1
            pin, path = row["pin"], row["repo_path"]
            blob = blob_bytes(pin, path) if HEX40.fullmatch(pin) else None
            head = Path(path).read_bytes() if Path(path).is_file() else None
            if blob is None or head is None:
                bad.append("%s: pin or file missing" % row["packaged_as"])
            elif not (hashlib.sha256(blob).hexdigest() == row["sha256"] == hashlib.sha256(head).hexdigest()) or not HEX64.fullmatch(row["sha256"]):
                bad.append("%s: blob, sha256 and the tree differ" % row["packaged_as"])
            elif subprocess.run(["git", "merge-base", "--is-ancestor", pin, "HEAD"]).returncode != 0:
                bad.append("%s: pin is not an ancestor of HEAD" % row["packaged_as"])
    case("M2-pins-are-full-commits-whose-blob-equals-the-tree", not bad and rows_checked == 7, "%d rows; %s" % (rows_checked, "; ".join(bad)[:200]))
    # M3: byte-preserving
    allowed = [re.compile(p) for p in (r'^\s*"pin": "[0-9a-f]{40}",$', r'^\s*"sha256": "[0-9a-f]{64}"$', r'^\s*\{$', r'^\s*\},$',
                                       r'^\s*"repo_path": "infra/aws/lambda/investor-reporting/ycharts/generate/ticket_confirmation.py",$',
                                       r'^\s*"packaged_as": "ticket_confirmation.py",$', r'^\s*"ticket_confirmation.py",$')]
    diff = [ln for ln in difflib.unified_diff(base_text.split("\n"), new_text.split("\n"), lineterm="", n=0) if ln[:1] in "+-" and ln[:3] not in ("+++", "---")]
    odd = [ln for ln in diff if not any(p.match(ln[1:]) for p in allowed)]
    case("M3-byte-preserving-edit", not odd and new_bytes.count(b"\r") == base_text.encode("utf-8").count(b"\r") and new_bytes.endswith(b"\n") == base_text.endswith("\n"),
         "%d odd lines: %s" % (len(odd), odd[:3]))
    # M4: the generated packages differ in exactly the expected members
    try:
        bgen, ngen = members(base_map, GEN, base_ref), members(new_map, GEN, "HEAD")
        bst, nst = members(base_map, STATUS, base_ref), members(new_map, STATUS, "HEAD")
        dgen = sorted(k for k in set(bgen) | set(ngen) if bgen.get(k) != ngen.get(k))
        dst = sorted(k for k in set(bst) | set(nst) if bst.get(k) != nst.get(k))
        want_gen = sorted(list(EXPECT_REPIN[GEN]) + [NEW_ROW[0]])
        case("M4-generate-package-delta-is-exactly-six-members", dgen == want_gen, str(dgen))
        case("M4-status-package-delta-is-exactly-status-py", dst == ["status.py"], str(dst))
        case("M4-ticket-confirmation-is-added-not-changed", NEW_ROW[0] not in bgen and NEW_ROW[0] in ngen)
    except Exception as exc:
        case("M4-packages-build", False, "%s: %s" % (type(exc).__name__, str(exc)[:160]))
    # T: generate.tf
    base_tf = blob_bytes(base_ref, TF).decode("utf-8")
    new_tf = Path(TF).read_text(encoding="utf-8")
    env_line = '    IRPT_TICKETS_TABLE             = "opal-tickets"\n'
    module = extract_block(new_tf, r'module "irpt_ycharts_generate" \{')
    env = extract_block(module or "", r"environment_variables = \{") or ""
    case("T1-env-variable-once-in-the-function-environment", env.count('IRPT_TICKETS_TABLE             = "opal-tickets"') == 1 and new_tf.count("IRPT_TICKETS_TABLE") == 1)
    policy = extract_block(new_tf, r'resource "aws_iam_role_policy" "generate_ticket_read" \{')
    case("T2-one-policy-resource", policy is not None and new_tf.count('"generate_ticket_read"') == 1)
    p = policy or ""
    case("T3-policy-name-role-and-effect", ('name = "%s"' % POLICY_NAME) in p and "role = aws_iam_role.generate.id" in p and p.count("Effect") == 1 and 'Effect   = "Allow"' in p, p[:80])
    actions = re.findall(r"Action\s*=\s*(\[[^\]]*\])", p)
    case("T4-one-action-getitem-only", actions == ['["dynamodb:GetItem"]'] and p.count("Action") == 1, str(actions))
    resources = re.findall(r"Resource\s*=\s*(\[[^\]]*\])", p)
    case("T5-one-resource-the-table-arn-only", resources == ['["%s"]' % ARN] and p.count("Resource") == 1, str(resources))
    case("T6-one-statement-no-index-no-wildcard", p.count("Sid") == 1 and "*" not in p and "index" not in p.lower() and "NotAction" not in p and "Condition" not in p)
    try:
        sys.path.insert(0, "lib")
        import opal_naming
        named = opal_naming.name("irpt", None, "ycharts-generate-ticket-read", "policy")
    except Exception as exc:
        named = "REFUSED %s" % type(exc).__name__
    case("T7-name-is-the-naming-builders-output", named == POLICY_NAME, named)
    stripped = new_tf.replace(env_line, "", 1)
    if policy:
        start = stripped.index(policy)
        comment_start = stripped.rfind("\n\n", 0, start) + 2
        stripped = stripped[:comment_start] + stripped[start + len(policy):].lstrip("\n")
    case("T8-the-rest-of-generate-tf-is-the-base-byte-for-byte", stripped == base_tf, "lengths %d vs %d" % (len(stripped), len(base_tf)))
    case("T9-ascii", all(ord(c) < 128 for c in new_tf) or any(ord(c) > 127 for c in base_tf))
    return out


def g102():
    try:
        out = cases()
    except Exception as exc:
        print("AR-G102-FAIL the cases could not run: %s: %s" % (type(exc).__name__, str(exc)[:200]))
        return 1
    failed = [(n, why) for n, ok, why in out if not ok]
    for name, why in failed:
        print("CASE-FAIL", name, why)
    if failed:
        print("AR-G102-FAIL %d of %d cases failed: %s" % (len(failed), len(out), str([n for n, _ in failed])[:300]))
        return 1
    print("AR-G102-OK %d cases" % len(out))
    return 0


def scope():
    base_ref = merge_base()
    rc, raw = git_text("diff", "--name-only", "box/dell2...HEAD")
    diff = raw.decode().split() if rc == 0 else []
    folder = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~"
    order = "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-102."
    stray = [p for p in diff if p not in OWN and not p.startswith(ISSUER) and not p.startswith(folder) and not p.startswith(order)]
    if base_ref is None or stray:
        print("AR-G102-SCOPE-FAIL stray=%s" % str(stray[:5]))
        return 1
    print("AR-G102-SCOPE-OK %d changed paths, all the cell's own" % len(diff))
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "g102":
        sys.exit(g102())
    if mode == "scope":
        sys.exit(scope())
    print("usage: ar_g102_checks.py g102 | scope")
    sys.exit(2)
