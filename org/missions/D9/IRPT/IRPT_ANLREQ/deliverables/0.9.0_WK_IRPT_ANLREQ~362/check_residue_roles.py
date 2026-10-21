#!/usr/bin/env python3
"""Offline checks for the residue delete roles (TO AR-y-489). Stdlib only, no AWS, no network.

python -I check_residue_roles.py            -> one line: RESIDUE-ROLES-OK ... (rc 0) or RESIDUE-ROLES-BAD <why> (rc 1)
python -I check_residue_roles.py --selftest -> CONTROL-FIRES (rc 0) only when all five in-memory mutants read BAD

The manifest and the .tf are read as bytes/text from this worktree. The order's fenced block is the spec for the .tf.
"""

import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[7]
MANIFEST_REL = (
    "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/"
    "synthetic_residue_delete_list_supplement_runs7e_7j_20261021.json"
)
TF_REL = "infra/aws/terraform/investor-reporting/ycharts/irpt_residue_delete_r35.tf"
ORDER_REL = (
    "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/"
    "IRPT_ANLREQ.TO-AR-y-489.residue-delete-roles-terraform-source-for-the-29-version-manifest.md"
)
PINNED_BLOB = "7963026db44e4760e34bb28f2b21dc141c7c3fac"
BUCKET = "opal-data-irpt"
KEY_PREFIX = "irpt/49financial/"
PRINCIPAL = "arn:aws:iam::313476888478:user/cloudops-dell2-agent-user"
CHUNK_SIZE = 12
EXPECT_ENTRIES = 29
EXPECT_SIZES = [12, 12, 5]
POLICY_CAP = 4000
DELETE_ACTION = '"s3:DeleteObjectVersion"'
TRUST_ACTION = '"sts:AssumeRole"'
POLICY_RE = re.compile(r'resource "aws_iam_role_policy" "irpt_residue_delete_(\d)" \{\n(.*?)\n\}', re.S)
RESOURCE_RE = re.compile(
    r'Resource\s*=\s*\[for o in local\.chunks\[(\d+)\] : '
    r'"arn:aws:s3:::\$\{o\.bucket\}/\$\{o\.key\}"\]'
)
VERSION_RE = re.compile(r'"s3:VersionId"\s*=\s*\[for o in local\.chunks\[(\d+)\] : o\.version_id\]')


def blob_of(raw):
    """The git blob id of raw bytes (hashlib form, for in-memory mutants)."""
    return hashlib.sha1(b"blob %d\x00" % len(raw) + raw).hexdigest()


def order_block(order_text):
    """The text between the first pair of ``` fences after the 'The change' paragraph."""
    lines = order_text.replace("\r\n", "\n").split("\n")
    start = next(i for i, line in enumerate(lines) if line.startswith("*The change.*"))
    opening = next(i for i in range(start, len(lines)) if lines[i] == "```")
    closing = next(i for i in range(opening + 1, len(lines)) if lines[i] == "```")
    return "\n".join(lines[opening + 1:closing]) + "\n"


def git_blob(rel):
    proc = subprocess.run(
        ["git", "hash-object", "--", rel],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise subprocess.SubprocessError("git hash-object %s rc=%d" % (rel, proc.returncode))
    return proc.stdout.strip()


def load_inputs():
    if not (REPO_ROOT / "org").is_dir() or not (REPO_ROOT / ".tools").is_dir():
        raise OSError("repo root %s carries no org/ and .tools/" % REPO_ROOT)
    manifest_raw = (REPO_ROOT / MANIFEST_REL).read_bytes()
    tf_raw = (REPO_ROOT / TF_REL).read_bytes()
    tf_text = tf_raw.decode("utf-8")
    order_text = (REPO_ROOT / ORDER_REL).read_bytes().decode("utf-8")
    block = order_block(order_text)
    blob = git_blob(MANIFEST_REL)
    if blob != blob_of(manifest_raw):
        raise ValueError("git hash-object disagrees with the manifest bytes")
    tf_blob = git_blob(TF_REL)
    if tf_blob != blob_of(tf_raw):
        raise ValueError("git hash-object disagrees with the .tf bytes")
    return manifest_raw, tf_text, block, blob, tf_blob


def check_manifest(entries, fails):
    """Every entry is a well-formed delete target. Returns False when an entry is not an object."""
    if len(entries) != EXPECT_ENTRIES:
        fails.append("manifest has %d entries, expected %d" % (len(entries), EXPECT_ENTRIES))
    pairs = []
    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fails.append("entry %d is not an object" % idx)
            return False
        bucket = entry.get("bucket")
        key = entry.get("key")
        version = entry.get("version_id")
        if bucket != BUCKET:
            fails.append("entry %d bucket %r is not %s" % (idx, bucket, BUCKET))
        if not isinstance(key, str) or not key.startswith(KEY_PREFIX):
            fails.append("entry %d key does not start with %s" % (idx, KEY_PREFIX))
        for label, value in (("key", key), ("version_id", version)):
            if not isinstance(value, str):
                fails.append("entry %d %s is null or not a string" % (idx, label))
            elif set(value) & set("*?[]") or value.endswith("/"):
                fails.append("entry %d %s carries a wildcard character or ends with /" % (idx, label))
        pairs.append((key, version))
    if len(set(pairs)) != len(pairs):
        fails.append("a (key, version_id) pair repeats in the manifest")
    return True


def check_tf(tf_text, block, fails):
    if tf_text != block:
        fails.append(".tf text differs from the order's fenced block")
    if tf_text.count('resource "aws_iam_role" "') != 3:
        fails.append(".tf does not carry exactly 3 aws_iam_role resources")
    if tf_text.count('resource "aws_iam_role_policy" "') != 3:
        fails.append(".tf does not carry exactly 3 aws_iam_role_policy resources")
    brackets = re.findall(r'\bAction\s*=\s*\[([^\]]*)\]', tf_text)
    quoted = re.findall(r'\bAction\s*=\s*("[^"\n]*")', tf_text)
    if len(brackets) + len(quoted) != len(re.findall(r'\bAction\b', tf_text)):
        fails.append("an Action is neither a string literal nor a one-element list")
    if brackets != [DELETE_ACTION] * 3:
        fails.append("policy Action is not exactly s3:DeleteObjectVersion x3: %s" % brackets)
    if quoted != [TRUST_ACTION] * 3:
        fails.append("trust Action is not exactly sts:AssumeRole x3: %s" % quoted)
    principals = re.findall(r'\bPrincipal\s*=\s*\{\s*AWS\s*=\s*"([^"]*)"\s*\}', tf_text)
    if len(re.findall(r'\bPrincipal\b', tf_text)) != 3 or principals != [PRINCIPAL] * 3:
        fails.append("principal is not the one user ARN x3: %s" % principals)
    literals = re.findall(r'"([^"\n]*)"', tf_text)
    if any("*" in literal for literal in literals):
        fails.append("a wildcard * appears in a string literal")


def check_policies(tf_text, chunks, entries, fails):
    indexes = []
    all_pairs = []
    for match in POLICY_RE.finditer(tf_text):
        idx, body = match.group(1), match.group(2)
        indexes.append(idx)
        if 'name = "irpt-residue-delete-%s-policy"' % idx not in body:
            fails.append("policy %s is not named irpt-residue-delete-%s-policy" % (idx, idx))
        if "role = aws_iam_role.irpt_residue_delete_%s.id" % idx not in body:
            fails.append("policy %s is not attached to its own role" % idx)
        res_match = RESOURCE_RE.search(body)
        ver_match = VERSION_RE.search(body)
        if res_match is None or ver_match is None:
            fails.append("policy %s Resource or s3:VersionId is not the chunk expression" % idx)
            continue
        if res_match.group(1) != idx or ver_match.group(1) != idx:
            fails.append("policy %s reads a chunk other than its own" % idx)
            continue
        chunk = chunks[int(idx)] if int(idx) < len(chunks) else []
        resources = ["arn:aws:s3:::%s/%s" % (o.get("bucket"), o.get("key")) for o in chunk]
        versions = [o.get("version_id") for o in chunk]
        all_pairs.extend(zip(resources, versions))
        doc = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": ["s3:DeleteObjectVersion"],
                "Resource": resources,
                "Condition": {"StringEquals": {"s3:VersionId": versions}},
            }],
        }
        rendered = json.dumps(doc, separators=(",", ":"))
        if len(rendered) >= POLICY_CAP:
            fails.append("policy %s rendered document is %d characters, cap is %d" % (idx, len(rendered), POLICY_CAP))
    if sorted(indexes) != ["0", "1", "2"]:
        fails.append("policy blocks are not indexes 0, 1, 2 once each: %s" % sorted(indexes))
    expected = [
        ("arn:aws:s3:::%s/%s" % (e.get("bucket"), e.get("key")), e.get("version_id")) for e in entries
    ]
    if sorted(all_pairs, key=repr) != sorted(expected, key=repr):
        fails.append("chunk (Resource, s3:VersionId) pairs are not the manifest's entries exactly once each")


def validate(manifest_raw, tf_text, block, blob):
    """Return (failures, summary). An empty failure list is the OK reading."""
    fails = []
    if blob != PINNED_BLOB:
        fails.append("manifest blob %s is not the pinned %s" % (blob, PINNED_BLOB))
    try:
        entries = json.loads(manifest_raw.decode("utf-8"))["objects"]
    except (KeyError, TypeError, ValueError) as exc:
        return fails + ["manifest is unreadable: %s" % exc], None
    if not isinstance(entries, list) or not check_manifest(entries, fails):
        return fails, None
    chunks = [entries[i:i + CHUNK_SIZE] for i in range(0, len(entries), CHUNK_SIZE)]
    sizes = [len(chunk) for chunk in chunks]
    if sizes != EXPECT_SIZES:
        fails.append("chunklist sizes are %s, expected %s" % (sizes, EXPECT_SIZES))
    check_tf(tf_text, block, fails)
    check_policies(tf_text, chunks, entries, fails)
    return fails, {"entries": len(entries), "sizes": sizes}


def dump(obj):
    return json.dumps(obj, indent=2).encode("utf-8")


def selftest(manifest_raw, tf_text, block, blob):
    base_fails, _ = validate(manifest_raw, tf_text, block, blob)
    if base_fails:
        print("CONTROL-VOID baseline is not clean: %s" % "; ".join(base_fails))
        return 1
    manifest = json.loads(manifest_raw.decode("utf-8"))
    mutants = []
    # 1. a fourth Action, s3:GetObject, added to the first policy statement
    tf_action = tf_text.replace(
        'Action    = ["s3:DeleteObjectVersion"]',
        'Action    = ["s3:DeleteObjectVersion", "s3:GetObject"]',
        1,
    )
    mutants.append(("extra-action-getobject", manifest_raw, tf_action))
    # 2. a wildcard * at the end of one manifest key
    wild = copy.deepcopy(manifest)
    wild["objects"][0]["key"] += "*"
    mutants.append(("wildcard-key", dump(wild), tf_text))
    # 3. the principal changed to the account root
    tf_root = tf_text.replace(PRINCIPAL, "arn:aws:iam::313476888478:root", 1)
    mutants.append(("principal-root", manifest_raw, tf_root))
    # 4. one manifest entry dropped
    dropped = copy.deepcopy(manifest)
    del dropped["objects"][0]
    mutants.append(("dropped-entry", dump(dropped), tf_text))
    # 5. one entry duplicated into another chunk (entry 0 written over the first entry of chunk 1)
    dup = copy.deepcopy(manifest)
    dup["objects"][12] = copy.deepcopy(dup["objects"][0])
    mutants.append(("duplicate-into-chunk-1", dump(dup), tf_text))
    fired = 0
    for name, raw, text in mutants:
        fails, _ = validate(raw, text, block, blob_of(raw))
        if fails:
            fired += 1
            print("MUTANT %s BAD: %s" % (name, "; ".join(fails)), file=sys.stderr)
        else:
            print("MUTANT %s PASSED (control did not fire)" % name, file=sys.stderr)
    if fired == len(mutants):
        print("CONTROL-FIRES")
        return 0
    print("CONTROL-DID-NOT-FIRE %d of %d mutants read BAD" % (fired, len(mutants)))
    return 1


def main(argv):
    try:
        manifest_raw, tf_text, block, blob, tf_blob = load_inputs()
    except (OSError, ValueError, StopIteration, subprocess.SubprocessError) as exc:
        print("RESIDUE-ROLES-BAD inputs unreadable: %s" % exc)
        return 1
    if "--selftest" in argv:
        return selftest(manifest_raw, tf_text, block, blob)
    fails, summary = validate(manifest_raw, tf_text, block, blob)
    if fails or summary is None:
        print("RESIDUE-ROLES-BAD " + "; ".join(fails))
        return 1
    print(
        "RESIDUE-ROLES-OK entries=%d chunks=%d sizes=%s action=s3:DeleteObjectVersion only "
        "principal=cloudops-dell2-agent-user only no_wildcard=yes manifest_blob=%s"
        % (
            summary["entries"],
            len(summary["sizes"]),
            ",".join(str(size) for size in summary["sizes"]),
            blob[:10],
        )
    )
    print("INFO tf_blob=%s" % tf_blob, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
