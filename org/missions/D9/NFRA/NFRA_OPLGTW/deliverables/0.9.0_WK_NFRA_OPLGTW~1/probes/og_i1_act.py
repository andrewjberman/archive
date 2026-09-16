#!/usr/bin/env python3
"""og_i1_act.py -- the ACT side of NFRA_OPLGTW.TO-OG-i-1 (cell OG-i-1). The grader is og_i1.py; this file only
produces the evidence the grader reads, and performs the ONE apply the order admits.

Subcommands:
  redact <show.json> <plan.txt> <out.json>
      Redact `terraform show -json` of a saved planfile into the committed plan file. Kept: every resource_changes
      entry's address and actions; a create's planned after/after_unknown; an update's changed attribute NAMES (list
      counts, and scalar before/after for `description` only), its unknown-after names and replace_paths, and for the
      WAF sets the addresses COUNT before/after. Dropped: prior_state, planned_values, configuration and every
      address list -- the root carries Secrets Manager and WAF state.
  waf <out.json>
      One get-ip-set read of both regional blocked-IP sets: count, sha256 of the sorted and of the as-returned list,
      a sha256 prefix of the lock token, description presence. Never the addresses.
  apply
      The ONE safe-apply run (ruling 97237: plan and apply in one run, never a saved plan). In order: the disk floor
      (refuse under 2 GiB, before any AWS write), the WAF pre-read, `.tools/safe-apply.sh -chdir=<root> apply
      -no-color` with stdin a pipe -- the approval prompt is answered `yes` ONLY when the plan terraform prints in
      THIS run creates a subset of this cell's four resources, updates a subset of the two admitted WAF sets with
      `description` as the only changed attribute, and destroys or replaces nothing; otherwise `no` (terraform
      cancels, nothing is written). Then the WAF post-read, evidence/apply.json and evidence/apply.log (root output
      VALUES redacted). A WAFOptimisticLockException is recorded and the run ends; a re-run is a new invocation with
      a fresh pre-read, never a forced retry.

Spawning: safe-apply.sh runs under the resolved Git Bash (git_bash_resolver). msys_safe_run wraps subprocess.run and
cannot carry an interactive stdin, so every argv element is checked with msys_argv_guard.is_msys_risky and the run
refuses if any is risky. Standard library + boto3. ASCII only.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(HERE)
_top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, text=True)
REPO = _top.stdout.strip() or os.path.abspath(os.path.join(DELIV, *[".."] * 6))
sys.path.insert(0, os.path.join(REPO, ".tools"))

SERIAL = os.environ.get("OPAL_AGENT_SERIAL") or "0.9.0_WK_NFRA_OPLGTW~1"
REGION = "us-east-1"
EVID = os.path.join(DELIV, "evidence")
APPLY_REC = os.path.join(EVID, "apply.json")
APPLY_LOG = os.path.join(EVID, "apply.log")
WAF_PRE = os.path.join(EVID, "waf_pre.json")
WAF_POST = os.path.join(EVID, "waf_post.json")
TF_ROOT_REL = "infra/aws/terraform/opal-gateway"
SAFE_APPLY_REL = ".tools/safe-apply.sh"
EXPECTED_CREATES = {
    "aws_dynamodb_table.access_state",
    "aws_iam_role_policy.gw_access_state_runtime",
    "aws_iam_role.access_admin",
    "aws_iam_role_policy.access_admin_policy",
}
ADMITTED_UPDATES = {
    "aws_wafv2_ip_set.opal_blocked_ips_regional_v4",
    "aws_wafv2_ip_set.opal_blocked_ips_regional_v6",
}
WAF_SETS = {"v4": "opal-blocked-ips-regional", "v6": "opal-blocked-ips-regional-ipv6"}
DISK_FLOOR = 2 * 1024 ** 3
PROMPT = "Enter a value:"
ACTIONS_HDR = "Terraform will perform the following actions:"
HDR_RE = re.compile(r"^\s*# ([A-Za-z0-9_.\[\]\"-]+) ((?:will|must) be .*)$", re.M)
ATTR_RE = re.compile(r"^\s*(-/\+|\+/-|[~+-]) ([A-Za-z0-9_]+)\b")
PLAN_RE = re.compile(r"^Plan: (\d+) to add, (\d+) to change, (\d+) to destroy\.", re.M)


def now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def iso(t: datetime.datetime) -> str:
    return t.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def rel(p: str) -> str:
    return os.path.relpath(p, REPO).replace("\\", "/")


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def write_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1, sort_keys=False)
        fh.write("\n")


def any_true(x) -> bool:
    if isinstance(x, bool):
        return x
    if isinstance(x, dict):
        return any(any_true(v) for v in x.values())
    if isinstance(x, list):
        return any(any_true(v) for v in x)
    return False


def count(v):
    return len(v) if isinstance(v, (list, dict)) else None


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
            e["after"] = ch.get("after")
            e["after_unknown"] = ch.get("after_unknown")
        elif acts != ["no-op"]:
            before, after, unk = ch.get("before") or {}, ch.get("after") or {}, ch.get("after_unknown") or {}
            changed = {}
            for k in sorted(set(before) | set(after)):
                if before.get(k) != after.get(k):
                    row = {"before_count": count(before.get(k)), "after_count": count(after.get(k))}
                    if k == "description":
                        row["before"], row["after"] = before.get(k), after.get(k)
                    changed[k] = row
            e["changed_attributes"] = changed
            e["unknown_after"] = sorted(k for k, v in unk.items() if any_true(v))
            e["replace_paths"] = ch.get("replace_paths") or []
            if r.get("type") == "aws_wafv2_ip_set":
                e["addresses_count_before"] = count(before.get("addresses"))
                e["addresses_count_after"] = count(after.get("addresses"))
        out_rc.append(e)
    counts = Counter("+".join(e["actions"]) for e in out_rc)
    out = {
        "format_version": d.get("format_version"),
        "terraform_version": d.get("terraform_version"),
        "timestamp": d.get("timestamp"),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "plan_line": plan_line,
        "counts": dict(sorted(counts.items())),
        "redaction": ("Redacted by og_i1_act.py redact from `terraform show -json` of the saved planfile: every "
                      "resource_changes entry's address and actions; creates keep after/after_unknown; updates keep "
                      "changed attribute NAMES with list counts (description before/after in full), unknown_after, "
                      "replace_paths and the WAF addresses COUNT. prior_state, planned_values, configuration and "
                      "every address list are dropped."),
        "resource_changes": out_rc,
        "output_changes": {k: {"actions": v.get("actions")} for k, v in sorted(d.get("output_changes", {}).items())},
    }
    write_json(out_path, out)
    print("OK: redacted %s (sha256 %s) -> %s; %d resource_changes %s; %s"
          % (rel(show_path), out["source_sha256"], rel(out_path), len(out_rc), json.dumps(out["counts"]), plan_line))
    return 0


# --------------------------------------------------------------------------- waf
def waf_read() -> dict:
    import boto3
    c = boto3.Session(region_name=REGION).client("wafv2")
    ids, listed, marker = {}, 0, None
    while True:
        kw = {"Scope": "REGIONAL", "Limit": 100}
        if marker:
            kw["NextMarker"] = marker
        r = c.list_ip_sets(**kw)
        for s in r.get("IPSets", []):
            listed += 1
            ids[s["Name"]] = s["Id"]
        marker = r.get("NextMarker")
        if not marker or not r.get("IPSets"):
            break
    t = now()
    sets = {}
    for k, name in WAF_SETS.items():
        g = c.get_ip_set(Name=name, Scope="REGIONAL", Id=ids[name])
        addrs = g["IPSet"].get("Addresses", [])
        sets[k] = {"name": name, "id": ids[name], "count": len(addrs),
                   "sha256_sorted": sha("\n".join(sorted(addrs))),
                   "sha256_as_returned": sha("\n".join(addrs)),
                   "lock_token_sha256_12": sha(g["LockToken"])[:12],
                   "description_present": bool(g["IPSet"].get("Description"))}
    return {"read_utc": iso(t), "instrument": "wafv2 list-ip-sets (REGIONAL, paginated) + get-ip-set x2",
            "listed_regional_ip_sets": listed, "sets": sets}


def waf_line(w: dict) -> str:
    return " ".join("%s count=%d sha256=%s" % (k, w["sets"][k]["count"], w["sets"][k]["sha256_sorted"][:16])
                    for k in ("v4", "v6"))


def cmd_waf(out_path: str) -> int:
    w = waf_read()
    write_json(out_path, w)
    print("OK: %s %s -> %s" % (w["read_utc"], waf_line(w), rel(out_path)))
    return 0


# --------------------------------------------------------------------------- apply
def judge(text: str) -> dict:
    """Judge the plan terraform printed in THIS run, before its approval prompt."""
    res = {"ok": False, "reasons": [], "creates": [], "updates": [], "other_headers": [], "update_attr_lines": {},
           "plan_line": None}
    if ACTIONS_HDR not in text:
        res["reasons"].append("no action list before the prompt")
        return res
    body = text.rsplit(ACTIONS_HDR, 1)[1].split("Do you want to perform these actions", 1)[0]
    pl = PLAN_RE.search(body)
    res["plan_line"] = pl.group(0) if pl else None
    res_body = body.split("\nPlan: ", 1)[0]
    ms = list(HDR_RE.finditer(res_body))
    for i, m in enumerate(ms):
        addr, what = m.group(1), m.group(2).strip()
        blk = res_body[m.end(): ms[i + 1].start() if i + 1 < len(ms) else len(res_body)]
        if what == "will be created":
            res["creates"].append(addr)
        elif what == "will be updated in-place":
            res["updates"].append(addr)
            names = []
            for ln in blk.splitlines():
                mm = ATTR_RE.match(ln)
                if mm and mm.group(2) != "resource":
                    names.append("%s %s" % (mm.group(1), mm.group(2)))
            res["update_attr_lines"][addr] = names
        else:
            res["other_headers"].append("%s %s" % (addr, what))
    cr, up = res["creates"], res["updates"]
    if not (cr or up):
        res["reasons"].append("no create or update header parsed")
    if not set(cr) <= EXPECTED_CREATES or len(cr) != len(set(cr)):
        res["reasons"].append("create outside this cell: %s" % sorted(set(cr) - EXPECTED_CREATES))
    if not set(up) <= ADMITTED_UPDATES:
        res["reasons"].append("update outside the admitted WAF pair: %s" % sorted(set(up) - ADMITTED_UPDATES))
    for addr, names in res["update_attr_lines"].items():
        if not names or any(n.split(" ", 1)[1] != "description" for n in names):
            res["reasons"].append("%s changes %s, not description only" % (addr, names))
    if res["other_headers"]:
        res["reasons"].append("destroy/replace/other: %s" % res["other_headers"])
    if not pl:
        res["reasons"].append("no Plan: line")
    elif (int(pl.group(3)) != 0 or int(pl.group(1)) != len(cr) or int(pl.group(2)) != len(up)):
        res["reasons"].append("Plan: line %r disagrees with %d creates / %d updates / 0 destroy"
                              % (pl.group(0), len(cr), len(up)))
    res["ok"] = not res["reasons"]
    return res


def redact_log(text: str) -> str:
    text = text.replace("\r\n", "\n")
    if "\nOutputs:\n" in text:
        head, tail = text.rsplit("\nOutputs:\n", 1)
        tail = re.sub(r"^(\S+)\s*=.*$", r"\1 = <value redacted by og_i1_act.py>", tail, flags=re.M)
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
    pre = waf_read()
    write_json(WAF_PRE, pre)
    print("WAF PRE  %s %s" % (pre["read_utc"], waf_line(pre)))
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
    post = waf_read()
    write_json(WAF_POST, post)
    print("WAF POST %s %s" % (post["read_utc"], waf_line(post)))
    text = buf.decode("utf-8", "replace").replace("\r\n", "\n")
    with open(APPLY_LOG, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(redact_log(text))
    identical = all(pre["sets"][k]["count"] == post["sets"][k]["count"]
                    and pre["sets"][k]["sha256_sorted"] == post["sets"][k]["sha256_sorted"] for k in ("v4", "v6"))
    proof = "PRE %s %s | POST %s %s | %s" % (pre["read_utc"], waf_line(pre), post["read_utc"], waf_line(post),
                                              "IDENTICAL both sets" if identical else "DIFFERENT")
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
        "waf_optimistic_lock_exception": "WAFOptimisticLockException" in text,
        "saved_planfile_consumed": False,
        "log": rel(APPLY_LOG),
        "waf_pre": rel(WAF_PRE),
        "waf_post": rel(WAF_POST),
        "waf_proof_line": proof,
        "prior_attempts": ([prior] + (prior.get("prior_attempts") or [])) if prior else [],
    }
    if prior:
        rec["prior_attempts"][0].pop("prior_attempts", None)
    write_json(APPLY_REC, rec)
    print("APPLY RECORD %s: rc %d answer %s start %s end %s complete %s lockexc %s"
          % (rel(APPLY_REC), rc, answered, rec["start_utc"], rec["end_utc"], rec["apply_complete"],
             rec["waf_optimistic_lock_exception"]))
    print("LEDGER-PROOF COND-2: %s" % proof)
    return rc


def main(argv: list) -> int:
    if len(argv) >= 2 and argv[1] == "redact" and len(argv) == 5:
        return cmd_redact(argv[2], argv[3], argv[4])
    if len(argv) == 3 and argv[1] == "waf":
        return cmd_waf(argv[2])
    if len(argv) == 2 and argv[1] == "apply":
        return cmd_apply()
    print("usage: og_i1_act.py redact <show.json> <plan.txt> <out.json> | waf <out.json> | apply")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
