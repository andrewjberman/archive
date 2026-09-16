#!/usr/bin/env python3
"""og_i2_act.py -- the ACT side of NFRA_OPLGTW.TO-OG-i-2 (cell OG-i-2). The grader is og_i2.py; this file only
produces the evidence the grader reads, performs the ONE apply the order admits, and writes the alias-key value.

Subcommands:
  redact <show.json> <plan.txt> <out.json>
      Redact `terraform show -json` of a saved planfile into the committed plan file og_i2.plan.json. Kept: every
      resource_changes entry's address, type and actions; a create's planned `after` with every attribute the plan
      marks sensitive replaced by a marker, and its after_unknown; a non-create non-no-op's changed attribute NAMES.
      Dropped: prior_state, planned_values, configuration and variables (the root carries ExternalIds and secrets).
  bucket <out.json>
      One get-bucket-policy read of the source bucket: sha256 and length of the policy text, never the text.
  apply
      The ONE safe-apply run: `.tools/safe-apply.sh -chdir=<root> apply -no-color` with stdin a pipe. The approval
      prompt is answered `yes` ONLY when the plan terraform prints in THIS run creates exactly this cell's ten
      resources and updates, replaces or destroys nothing; otherwise `no` (terraform cancels, nothing is written).
      The source bucket policy is read immediately before and after (evidence/bucket_policy_pre.json / _post.json).
  put-alias-key
      Writes the FIRST value of opal/mcp/opal-gateway-schwab-account-ref-key: {"current_version": "v1",
      "keys": {"v1": base64(32 bytes from secrets.token_bytes)}}. Refuses if the secret already holds a value
      (never a rotation). The value is never printed or written anywhere but Secrets Manager; the record keeps the
      version id, the version stage and the shape.

Standard library + boto3. ASCII only. botocore/boto3/urllib3 loggers are held at INFO or higher (row W3-S26).
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import json
import logging
import os
import re
import secrets
import shutil
import subprocess
import sys
import threading
import time
from collections import Counter

for _n in ("botocore", "boto3", "urllib3"):
    logging.getLogger(_n).setLevel(logging.INFO)

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(HERE)
_top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, text=True)
REPO = _top.stdout.strip() or os.path.abspath(os.path.join(DELIV, *[".."] * 6))
sys.path.insert(0, os.path.join(REPO, ".tools"))

SERIAL = os.environ.get("OPAL_AGENT_SERIAL") or "0.9.0_WK_NFRA_OPLGTW~1"
REGION = "us-east-1"
BUCKET = "opal-data-assets"
EVID = os.path.join(DELIV, "evidence", "og_i2")
APPLY_REC = os.path.join(EVID, "apply.json")
APPLY_LOG = os.path.join(EVID, "apply.log")
BP_PRE = os.path.join(EVID, "bucket_policy_pre.json")
BP_POST = os.path.join(EVID, "bucket_policy_post.json")
ALIAS_REC = os.path.join(EVID, "alias_key_put.json")
ALIAS_SECRET = "opal/mcp/opal-gateway-schwab-account-ref-key"
TF_ROOT_REL = "infra/aws/terraform/opal-gateway"
SAFE_APPLY_REL = ".tools/safe-apply.sh"
EXPECTED_CREATES = {
    "aws_iam_role.schwab_data_read",
    "aws_iam_role_policy.schwab_data_read_policy",
    "aws_iam_role.schwab_catalog_read",
    "aws_iam_role_policy.schwab_catalog_read_policy",
    "aws_iam_role_policy.gw_assume_schwab_readers",
    "aws_secretsmanager_secret.schwab_account_ref_key",
    "aws_secretsmanager_secret_policy.schwab_account_ref_key_gw_read",
    "aws_secretsmanager_secret.schwab_reader_external_ids",
    "aws_secretsmanager_secret_version.schwab_reader_external_ids",
    "aws_secretsmanager_secret_policy.schwab_reader_external_ids_gw_read",
}
DISK_FLOOR = 2 * 1024 ** 3
PROMPT = "Enter a value:"
ACTIONS_HDR = "Terraform will perform the following actions:"
HDR_RE = re.compile(r"^\s*# ([A-Za-z0-9_.\[\]\"-]+) ((?:will|must) be .*)$", re.M)
PLAN_RE = re.compile(r"^Plan: (\d+) to add, (\d+) to change, (\d+) to destroy\.", re.M)
SENSITIVE = "<sensitive: redacted by og_i2_act.py>"


def now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def iso(t: datetime.datetime) -> str:
    return t.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def rel(p: str) -> str:
    return os.path.relpath(p, REPO).replace("\\", "/")


def write_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1, sort_keys=False)
        fh.write("\n")


def mask(value, sens):
    """Replace every value the plan marks sensitive with a marker."""
    if sens is True:
        return SENSITIVE
    if isinstance(value, dict) and isinstance(sens, dict):
        return {k: mask(v, sens.get(k)) for k, v in value.items()}
    if isinstance(value, list) and isinstance(sens, list):
        return [mask(v, sens[i] if i < len(sens) else None) for i, v in enumerate(value)]
    return value


# --------------------------------------------------------------------------- redact
def cmd_redact(show_path: str, txt_path: str, out_path: str) -> int:
    with open(show_path, "rb") as fh:
        raw = fh.read()
    d = json.loads(raw.decode("utf-8"))
    plan_line = ""
    with open(txt_path, encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            if ln.startswith("Plan:") or ln.startswith("No changes."):
                plan_line = ln.strip()
    out_rc = []
    for r in d.get("resource_changes", []):
        ch = r.get("change", {})
        acts = ch.get("actions", [])
        e = {"address": r["address"], "mode": r.get("mode"), "type": r.get("type"), "name": r.get("name"),
             "actions": acts}
        if acts == ["create"]:
            e["after"] = mask(ch.get("after"), ch.get("after_sensitive"))
            e["after_unknown"] = ch.get("after_unknown")
        elif acts != ["no-op"]:
            before, after = ch.get("before") or {}, ch.get("after") or {}
            e["changed_attribute_names"] = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
            e["replace_paths"] = ch.get("replace_paths") or []
        out_rc.append(e)
    counts = Counter("+".join(e["actions"]) for e in out_rc)
    out = {
        "format_version": d.get("format_version"),
        "terraform_version": d.get("terraform_version"),
        "timestamp": d.get("timestamp"),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "plan_line": plan_line,
        "counts": dict(sorted(counts.items())),
        "redaction": ("Redacted by og_i2_act.py redact from `terraform show -json` of the saved planfile: every "
                      "resource_changes entry's address, type and actions; creates keep `after` with every "
                      "plan-sensitive value masked, and after_unknown; other non-no-op entries keep changed "
                      "attribute NAMES and replace_paths. prior_state, planned_values, configuration and variables "
                      "are dropped."),
        "resource_changes": out_rc,
        "output_changes": {k: {"actions": v.get("actions")} for k, v in sorted(d.get("output_changes", {}).items())},
    }
    write_json(out_path, out)
    print("OK: redacted %s (sha256 %s) -> %s; %d resource_changes %s; %s"
          % (rel(show_path), out["source_sha256"], rel(out_path), len(out_rc), json.dumps(out["counts"]), plan_line))
    return 0


# --------------------------------------------------------------------------- bucket policy
def bucket_read() -> dict:
    import boto3
    s3 = boto3.Session(region_name=REGION).client("s3")
    t = now()
    text = s3.get_bucket_policy(Bucket=BUCKET)["Policy"]
    doc = json.loads(text)
    return {"read_utc": iso(t), "instrument": "s3api get-bucket-policy (boto3 get_bucket_policy)", "bucket": BUCKET,
            "policy_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "policy_length": len(text),
            "statement_count": len(doc.get("Statement", [])),
            "statement_sids": [s.get("Sid") for s in doc.get("Statement", [])]}


def cmd_bucket(out_path: str) -> int:
    b = bucket_read()
    write_json(out_path, b)
    print("OK: %s sha256=%s len=%d -> %s" % (b["read_utc"], b["policy_sha256"], b["policy_length"], rel(out_path)))
    return 0


# --------------------------------------------------------------------------- apply
def judge(text: str) -> dict:
    """Judge the plan terraform printed in THIS run, before its approval prompt."""
    res = {"ok": False, "reasons": [], "creates": [], "other_headers": [], "plan_line": None}
    if ACTIONS_HDR not in text:
        res["reasons"].append("no action list before the prompt")
        return res
    body = text.rsplit(ACTIONS_HDR, 1)[1].split("Do you want to perform these actions", 1)[0]
    pl = PLAN_RE.search(body)
    res["plan_line"] = pl.group(0) if pl else None
    res_body = body.split("\nPlan: ", 1)[0]
    for m in HDR_RE.finditer(res_body):
        addr, what = m.group(1), m.group(2).strip()
        if what == "will be created":
            res["creates"].append(addr)
        else:
            res["other_headers"].append("%s %s" % (addr, what))
    cr = res["creates"]
    if set(cr) != EXPECTED_CREATES or len(cr) != len(set(cr)):
        res["reasons"].append("creates != this cell's ten: extra %s missing %s"
                              % (sorted(set(cr) - EXPECTED_CREATES), sorted(EXPECTED_CREATES - set(cr))))
    if res["other_headers"]:
        res["reasons"].append("update/destroy/replace/other: %s" % res["other_headers"])
    if not pl:
        res["reasons"].append("no Plan: line")
    elif (int(pl.group(1)), int(pl.group(2)), int(pl.group(3))) != (len(EXPECTED_CREATES), 0, 0):
        res["reasons"].append("Plan: line %r is not %d to add, 0 to change, 0 to destroy"
                              % (pl.group(0), len(EXPECTED_CREATES)))
    res["ok"] = not res["reasons"]
    return res


def redact_log(text: str) -> str:
    text = text.replace("\r\n", "\n")
    if "\nOutputs:\n" in text:
        head, tail = text.rsplit("\nOutputs:\n", 1)
        tail = re.sub(r"^(\S+)\s*=.*$", r"\1 = <value redacted by og_i2_act.py>", tail, flags=re.M)
        text = head + "\nOutputs:\n" + tail
    return text


def cmd_apply() -> int:
    from git_bash_resolver import git_bash
    from msys_argv_guard import is_msys_risky
    free = shutil.disk_usage("C:\\").free
    print("DISK C: free %.2f GiB at %s (floor 2.00 GiB)" % (free / 1024 ** 3, iso(now())))
    if free < DISK_FLOOR:
        print("REFUSED: C: is under the 2 GiB floor; nothing planned, nothing written")
        return 3
    bash = git_bash()
    if not bash:
        print("REFUSED: no Git Bash resolved; nothing planned, nothing written")
        return 3
    argv_tail = [SAFE_APPLY_REL, "-chdir=" + TF_ROOT_REL, "apply", "-no-color"]
    risky = [a for a in argv_tail if is_msys_risky(a)]
    if risky:
        print("REFUSED: MSYS-risky argv %s; nothing planned, nothing written" % risky)
        return 3
    prior = None
    if os.path.isfile(APPLY_REC):
        with open(APPLY_REC, encoding="utf-8") as fh:
            prior = json.load(fh)
    pre = bucket_read()
    write_json(BP_PRE, pre)
    print("BUCKET POLICY PRE  %s sha256=%s" % (pre["read_utc"], pre["policy_sha256"]))
    env = dict(os.environ)
    env["OPAL_AGENT_SERIAL"] = SERIAL
    env["PATH"] = os.path.dirname(sys.executable) + os.pathsep + env.get("PATH", "")
    t_start = now()
    p = subprocess.Popen([bash] + argv_tail, cwd=REPO, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    buf = bytearray()
    lock = threading.Lock()
    done = threading.Event()

    def reader():
        while True:
            chunk = p.stdout.read1(65536)
            if not chunk:
                break
            with lock:
                buf.extend(chunk)
            sys.stdout.write(chunk.decode("utf-8", "replace"))
            sys.stdout.flush()
        done.set()

    th = threading.Thread(target=reader, daemon=True)
    th.start()
    answered, t_prompt, t_answer, guard = None, None, None, None
    deadline = time.time() + 1800
    while not done.is_set():
        time.sleep(0.5)
        if answered is None:
            with lock:
                text = buf.decode("utf-8", "replace")
            if PROMPT in text:
                t_prompt = now()
                guard = judge(text.replace("\r\n", "\n"))
                answered = "yes" if guard["ok"] else "no"
                p.stdin.write((answered + "\n").encode("ascii"))
                p.stdin.flush()
                p.stdin.close()
                t_answer = now()
                print("\nGUARD %s at %s: %s" % (answered, iso(t_answer), guard["reasons"] or "the admitted plan"))
            elif time.time() > deadline:
                print("\nGUARD: no prompt within 1800 s; closing stdin (terraform cancels on EOF), never a kill")
                p.stdin.close()
                answered = "eof"
    rc = p.wait()
    th.join(10)
    t_end = now()
    post = bucket_read()
    write_json(BP_POST, post)
    print("BUCKET POLICY POST %s sha256=%s" % (post["read_utc"], post["policy_sha256"]))
    text = buf.decode("utf-8", "replace").replace("\r\n", "\n")
    with open(APPLY_LOG, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(redact_log(text))
    rec = {
        "command": "bash " + " ".join(argv_tail),
        "cwd": "<worktree root>",
        "serial": SERIAL,
        "start_utc": iso(t_start),
        "prompt_utc": iso(t_prompt) if t_prompt else None,
        "answer": answered,
        "answer_utc": iso(t_answer) if t_answer else None,
        "end_utc": iso(t_end),
        "rc": rc,
        "guard": guard,
        "apply_complete": re.findall(r"^Apply complete! Resources: .*$", text, re.M),
        "saved_planfile_consumed": False,
        "log": rel(APPLY_LOG),
        "bucket_policy_pre": rel(BP_PRE),
        "bucket_policy_post": rel(BP_POST),
        "bucket_policy_identical": pre["policy_sha256"] == post["policy_sha256"],
        "prior_attempts": ([prior] + (prior.get("prior_attempts") or [])) if prior else [],
    }
    if prior:
        rec["prior_attempts"][0].pop("prior_attempts", None)
    write_json(APPLY_REC, rec)
    print("APPLY RECORD %s: rc %d answer %s start %s end %s complete %s bucket-policy identical %s"
          % (rel(APPLY_REC), rc, answered, rec["start_utc"], rec["end_utc"], rec["apply_complete"],
             rec["bucket_policy_identical"]))
    return rc


# --------------------------------------------------------------------------- alias key
def cmd_put_alias_key() -> int:
    import boto3
    sm = boto3.Session(region_name=REGION).client("secretsmanager")
    desc = sm.describe_secret(SecretId=ALIAS_SECRET)
    stages = desc.get("VersionIdsToStages") or {}
    if stages:
        print("REFUSED: %s already holds %d version(s); this command writes only the FIRST value, never a rotation"
              % (ALIAS_SECRET, len(stages)))
        return 3
    key = secrets.token_bytes(32)
    value = json.dumps({"current_version": "v1", "keys": {"v1": base64.b64encode(key).decode("ascii")}})
    t = now()
    r = sm.put_secret_value(SecretId=ALIAS_SECRET, SecretString=value)
    del value, key
    got = json.loads(sm.get_secret_value(SecretId=ALIAS_SECRET)["SecretString"])
    shape = {"top_level_keys": sorted(got), "current_version": got.get("current_version"),
             "key_versions": sorted((got.get("keys") or {})),
             "current_key_decoded_bytes": len(base64.b64decode(got["keys"][got["current_version"]], validate=True))}
    del got
    rec = {"written_utc": iso(t), "secret_name": ALIAS_SECRET, "secret_arn": desc["ARN"],
           "instrument": "secretsmanager put-secret-value, then get-secret-value read back for SHAPE only",
           "version_id": r.get("VersionId"), "version_stages": r.get("VersionStages"),
           "generator": "python secrets.token_bytes(32), base64", "value_recorded": False, "shape_read_back": shape}
    write_json(ALIAS_REC, rec)
    print("OK: %s version %s stages %s shape %s -> %s" % (ALIAS_SECRET, r.get("VersionId"), r.get("VersionStages"),
                                                         json.dumps(shape), rel(ALIAS_REC)))
    return 0


def main(argv: list) -> int:
    if len(argv) == 5 and argv[1] == "redact":
        return cmd_redact(argv[2], argv[3], argv[4])
    if len(argv) == 3 and argv[1] == "bucket":
        return cmd_bucket(argv[2])
    if len(argv) == 2 and argv[1] == "apply":
        return cmd_apply()
    if len(argv) == 2 and argv[1] == "put-alias-key":
        return cmd_put_alias_key()
    print("usage: og_i2_act.py redact <show.json> <plan.txt> <out.json> | bucket <out.json> | apply | put-alias-key")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
