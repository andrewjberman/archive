"""IRPT_ANLREQ TO-READ-COMPOSITION-REFUSAL (applier 0.7.0_AE_CloudOps~IB2): R1 to R4, READ ONLY.

  python composition_refusal.py     prints the lines and writes A_COMPOSITION_REFUSAL.txt beside this file

R1 counts and quotes the closed COMPOSITION-REFUSED journal lines in the window (one read-only SSM script). R2 and R3/R4 read the two retained synthetic
state objects of run 5B (read only, in memory, nothing written to disk or S3) and run the repository's own CompositionAdmission offline. Only closed words,
UPPER_SNAKE codes, row numbers, the synthetic tickers, booleans, counts and times are printed: never an amount, weight, price, URL, signature, token or email.
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True, cwd=str(HERE)).strip())
STATE = HERE.parent / "irpt_anlreq_commentary_e2e5b" / "state_e2e5b.json"
REGION = "us-east-1"
BUCKET = "opal-data-irpt"
SYNTH = ("SPY", "AGG", "TIMXX", "ZQXWVK")
lines, answered = [], 0


def keys_by_kind():
    ks = sorted(set(json.loads(STATE.read_text(encoding="ascii"))["leftover_blob_keys"]))
    return {"normalized": next(k for k in ks if "/normalized_portfolios/" in k), "composition": next(k for k in ks if "/request_compositions/" in k)}


def load_obj(key):
    s3 = boto3.client("s3", region_name=REGION)
    return json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8"))


def r1():
    ec2, ssm = boto3.client("ec2", region_name=REGION), boto3.client("ssm", region_name=REGION)
    r = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": ["irpt-ycharts-runner"]}, {"Name": "instance-state-name", "Values": ["running"]}])
    ids = [i["InstanceId"] for x in r["Reservations"] for i in x["Instances"]]
    script = "\n".join([
        "set -u", "UNIT=irpt-analysis-resident.service", "J=$(mktemp)",
        "journalctl -u \"$UNIT\" --since '2026-10-20 02:33:30' --until '2026-10-20 02:50:30' --no-pager -o short-iso -q > \"$J\" 2>/dev/null",
        "echo \"RAW N first=$(head -1 \"$J\" | cut -d' ' -f1) last=$(tail -1 \"$J\" | cut -d' ' -f1) scanned=$(wc -l < \"$J\") refused=$(grep -c COMPOSITION-REFUSED \"$J\" || true) retained=$(grep -c retained_for_retry \"$J\" || true) submissionrefused=$(grep -c SubmissionRefused \"$J\" || true)\"",
        "grep -o 'COMPOSITION-REFUSED step=[0-9]* error_class=[A-Za-z_]*' \"$J\" | sed 's/^/RAW C /'",
        "rm -f \"$J\""]) + "\n"
    (HERE / "host_r1.sh").write_text(script, encoding="ascii", newline="\n")
    cid = ssm.send_command(InstanceIds=ids[:1], DocumentName="AWS-RunShellScript", Comment="COMPOSITION-REFUSAL R1 journal read-only", Parameters={"commands": [script], "executionTimeout": ["180"]}, TimeoutSeconds=300)["Command"]["CommandId"]
    out = ""
    for _ in range(80):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=ids[0])
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            out = inv.get("StandardOutputContent", "")
            break
    m = re.search(r"RAW N first=(\S*) last=(\S*) scanned=(\d+) refused=(\d+) retained=(\d+) submissionrefused=(\d+)", out)
    if not m:
        lines.append("R1 DENIED-OR-ERROR unparsed")
        return False
    cs = re.findall(r"RAW C COMPOSITION-REFUSED step=(\d+) error_class=(\w+)", out)
    body = "; ".join("step=%s class=%s" % c for c in cs) or "none"
    lines.append("R1 window=%s..%s scanned=%s refused=%s lines=%s retained=%s" % (m.group(1), m.group(2), m.group(3), m.group(4), body, m.group(5)))
    lines.append("NOTE-R1 SubmissionRefused lines %s" % m.group(6))
    return True


def find_rows(o, out=None):
    """Lists of dicts that look like portfolio rows (a dict with a symbol-like member)."""
    out = [] if out is None else out
    if isinstance(o, list) and o and all(isinstance(x, dict) for x in o) and any(any(k in x for k in ("ticker", "symbol", "typed_symbol", "input_symbol", "typed")) for x in o):
        out.append(o)
    if isinstance(o, dict):
        for v in o.values():
            find_rows(v, out)
    elif isinstance(o, list):
        for v in o:
            find_rows(v, out)
    return out


def sym_of(row):
    for k in ("ticker", "symbol", "typed_symbol", "input_symbol", "typed"):
        v = row.get(k)
        if isinstance(v, str):
            return v if v in SYNTH else "-"
    for v in row.values():
        if isinstance(v, str) and v in SYNTH:
            return v
    return "-"


def present(row, frag):
    for k, v in row.items():
        if frag in k.lower() and v not in (None, "", [], {}):
            return "yes"
    return "no"


def r2(norm):
    rows = find_rows(norm)
    if not rows:
        lines.append("R2 NOT-FOUND no row list in the retained normalized portfolio (top-level members: %s)" % ",".join(sorted(norm.keys()) if isinstance(norm, dict) else ["list"]))
        return False
    best = max(rows, key=len)
    for k, row in enumerate(best, 1):
        meth = row.get("method") if isinstance(row.get("method"), str) and re.fullmatch(r"[A-Z][A-Z0-9_]+", row.get("method")) else "-"
        res = row.get("resolution") if isinstance(row.get("resolution"), str) and re.fullmatch(r"[A-Z][A-Z0-9_]+", row.get("resolution")) else "-"
        lines.append("R2 row%d %s method=%s resolution=%s price=%s receipt=%s dollars=%s" % (k, sym_of(row), meth, res, present(row, "price"), present(row, "receipt"), present(row, "dollars")))
    lines.append("NOTE-R2 row member names (names only): %s" % ",".join(sorted(best[0].keys())))
    return True


def admission():
    sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting/ycharts/generate"))
    sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting"))
    sys.path.insert(0, str(ROOT / "lib"))
    import composition_admission as ca  # noqa: E402
    return ca, ca.CompositionAdmission(str(ROOT / "docs/contracts/investor-reporting/v1"))


def verdict(ca, adm, doc):
    buf = io.StringIO()
    detail = "-"
    try:
        with contextlib.redirect_stdout(buf):
            adm.validate(doc)
        return "ADMITTED", detail
    except Exception as e:  # noqa: BLE001
        m = re.search(r"COMPOSITION-REFUSED step=(\d+) error_class=(\w+)", buf.getvalue())
        res = "step=%s class=%s" % (m.group(1), m.group(2)) if m else "OTHER class=%s" % type(e).__name__
        if m and m.group(1) == "2":
            try:
                err = next(iter(adm.validator.iter_errors(json.loads(ca.canonical_bytes(doc)))), None)
                if err is not None:
                    detail = "%s@%s" % (err.validator, "/".join(str(p) for p in err.absolute_path))
            except Exception:  # noqa: BLE001
                detail = "unavailable"
        return res, detail


def drop_symbol(doc, sym):
    d = copy.deepcopy(doc)

    def walk(o):
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
                    o[k] = [x for x in v if sym not in [y for y in x.values() if isinstance(y, str)]]
                walk(o[k])
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk((d.get("resolved") or {}).get("document", d))
    return d


def r3_r4(comp):
    ca, adm = admission()
    v, det = verdict(ca, adm, comp)
    lines.append("R3 validate=%s detail=%s" % (v, det))
    v4, det4 = verdict(ca, adm, drop_symbol(comp, "ZQXWVK"))
    lines.append("R4 without_ZQXWVK validate=%s detail=%s" % (v4, det4))
    return True


if __name__ == "__main__":
    n = 0
    try:
        n += 1 if r1() else 0
    except Exception as e:  # noqa: BLE001
        lines.append("R1 DENIED-OR-ERROR %s" % type(e).__name__)
    try:
        k = keys_by_kind()
        norm, comp = load_obj(k["normalized"]), load_obj(k["composition"])
    except Exception as e:  # noqa: BLE001
        lines.append("R2 DENIED-OR-ERROR %s" % type(e).__name__)
        lines.append("R3 NOT-RUN the retained objects could not be read")
        lines.append("R4 NOT-RUN the retained objects could not be read")
        norm = comp = None
    if norm is not None:
        try:
            n += 1 if r2(norm) else 0
        except Exception as e:  # noqa: BLE001
            lines.append("R2 DENIED-OR-ERROR %s" % type(e).__name__)
        try:
            ok = r3_r4(comp)
            n += 2 if ok else 0
        except Exception as e:  # noqa: BLE001
            lines.append("R3 DENIED-OR-ERROR %s" % type(e).__name__)
            lines.append("R4 NOT-RUN the validator could not run (%s)" % type(e).__name__)
    lines.append("READS-DONE %d of 4 answered" % n)
    text = "\n".join(lines) + "\n"
    (HERE / "A_COMPOSITION_REFUSAL.txt").write_text(text, encoding="ascii", newline="\n")
    print(text)
