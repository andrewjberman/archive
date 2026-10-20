"""IRPT_ANLREQ TO-RUN-COMMENTARY-E2E-7D (run 7d: run 7c after the r37 release; R reads the Overview route /pdf, R3 saves it OUTSIDE the repository, R4 reads the commentary route).

  python e2e7d_run.py --selftest   the pure helpers on synthetic data (no AWS, no network)
  python e2e7d_run.py --go         R0 (read only; a red mints NOTHING), then A, L, B1, B2, P, B3, R, R2, D; stops at the FIRST red hop; deletes only after the LAST read

The password and the access token live in memory; the access token also goes to ONE private file outside the repository (deleted at D). Nothing secret,
no URL, no signature and no non-synthetic address is written to the repository or printed. Every key is recorded in KEYS the moment it is known.
"""
from __future__ import annotations

import base64
import os
import shutil
import tempfile
from email.utils import parsedate_to_datetime
import hashlib
import importlib.util
import io
import json
import re
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
STATE_FILE = HERE / "state_e2e7d.json"
REGION = "us-east-1"
EMAIL = "fwd1-commentary-e2e7d-20261020@opal.invalid"
FILER_NAME = "E2E7D SYNTHETIC FILER"
RUN7C_EMAIL = "fwd1-commentary-e2e7c-20261020@opal.invalid"
SAMPLE_DIR = "C:/dev/andrew_samples"
RUN7B_EMAIL = "fwd1-commentary-e2e7b-20261020@opal.invalid"
BUCKET_IRPT = "opal-data-irpt"
RUN7_EMAIL = "fwd1-commentary-e2e7-20261020@opal.invalid"
LEFTOVER_NOTE = "org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e2/LEFTOVER.txt"
OLD_TOKEN_SHAS = {hashlib.sha256(b"e2e-20261017T204547").hexdigest()}  # the run-2 and run-3 token (recorded in the run-3 driver); an equal token is a STOP
OLD_HOLDINGS_SHAS = {"30d44443701df5f92dfee4def4d1a1f139818ee416601b2577c66e30fb3b96a1", "8bfd3093b8ba004b234353359d93925f4e3dd197c9a05ccab826de5e63274215", "d83e1c2cc18418d69523a659d6191f6a75d9ff3fb0f229234d8c111afe073bab", "fe099d42d99fcc5d6b20abe9fd5eb76ecefb4611a9b779bcc2b75078d4274d7c", "82e05e06c0417633a856307ee43b213157473e28154df4ff1d6f008bd899e346", "79842b4fcadc1d4ef44a9e79ab77343a211e4eafa9163a7b90d45f6cf604b7f5", "cb8119d37c52f1d23be7cb113ab0dd1873466a8d5721346cd83caf246e77f2b0", "723cdf9cd7006bcb27121ef1f3b78d27ba062605c44f973d53474a7e4a414ca1", "7d3835311fd453aa66aa8c4b7fb7ad8ce7363c6e52f8f67942abc3d01af8e889"}
ADVISOR_DATE = "20261020"
RUN4_ADVISOR = "irpt-w5-advisor-20261018@opal.invalid"
ADVISOR = "irpt-w5-advisor-%s@opal.invalid" % ADVISOR_DATE
MONDAY_ADVISOR = "irpt-w5-advisor-20261019@opal.invalid"
ADVISOR_TOOL = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~172/fwd1_advisor.py"
TENANT = "49financial"
HOLDINGS = "Ticker,Dollars,Acct Market Value\nSPY,110,26000000\nAGG,200,32000000\nTIMXX,50,5000000\n"
HOLDINGS_SHA = "18d701793151727d4e28b755f5cd3d9a61e2d05c324a76ab693fe6b3ba4af92b"
FN_WANT = {"irpt-ycharts-generate": "PlCjNms/RRLRB/c15zW8Sdzl7w3ptodi3o8sSxnWjYA=", "irpt-status": "B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE=",
           "outlook-global-commentary-draft-lambda": "I/6mirBTU5+JPCUUx6Xrmd1bn1vGAjvZTL75LhOm3HY="}
WANT_ROOT = "0485393f3a-r34n"
WAITS = [3, 3, 6, 6, 12, 12, 24, 24, 30, 30, 30, 30, 30]  # sums to 240 s (ADDENDUM 4)
POLL_STEP_S, POLL_BUDGET_S = 20, 1800
YC_QUIET_S = 390
REQ_RE = re.compile(r"REQ-[0-9a-f]{24}")
TCK_RE = re.compile(r"^TCK-\d{8}-[0-9a-f]{8}$")
HOST_R0 = HERE / "host_r0.sh"

DELIV = "org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables"
COO_HALF = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_ADDENDUM9_RUN7_FILES_THROUGH_THE_PORTAL_PAGE_COO_HALF_20261020.md"
COO_HALF_BLOB = "8e355eb83638d7a044247f00e6bd9a5853e6bdca"
CTO_HALF = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_E2E_COMMENTARY_RUN_CTO_HALF.md"
BROWSER = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~325/run7_browser_leg.mjs"
CM = "org/critical_paths/change_management/"
GUARD_SHA = "d5d2fdeab3af8fcbc1f74ef2d5f2eefd7a89c3d3"
WALK_PIN = "602ca19ef40495f3ef173877f054f5fb8b53c659"
HOUSEHOLD = "E2E7 SYNTHETIC"
FIRM_ID = "49financial"


def utc(t=None):
    return datetime.fromtimestamp(t if t is not None else time.time(), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_module(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def in_forbidden_window(now=None):
    n = now or datetime.now(timezone.utc)
    if n.weekday() < 5 and (11, 30) <= (n.hour, n.minute) <= (14, 15):
        return "weekday band 11:30Z-14:15Z"
    if (n.year, n.month, n.day) == (2026, 10, 20) and (5, 45) <= (n.hour, n.minute) < (7, 0):
        return "gateway resize 05:45Z-07:00Z"
    return None


class Run:
    def __init__(self):
        self.st = {"started_utc": utc(), "hops": {}, "keys": [], "stopped_at": None, "stop_code": None, "journal": [], "r0": {}}
        self.keys = self.st["keys"]
        self.token = None
        self.password = None
        self.base = None

    def say(self, msg):
        print("%s %s" % (utc(), msg), flush=True)

    def save(self):
        STATE_FILE.write_text(json.dumps(self.st, indent=1, sort_keys=True) + "\n", encoding="ascii")

    def record(self, kind, **key):
        self.keys.append(dict(kind=kind, **key))
        self.save()

    def hop(self, name, value):
        self.st["hops"][name] = value
        self.say("HOP %s %s" % (name, value))
        self.save()

    def stop(self, hop, code):
        self.st["stopped_at"], self.st["stop_code"] = hop, code
        self.say("STOP at %s code=%s" % (hop, code))
        self.save()

    def call(self, method, path, body=None, authed=True):
        headers = {"Content-Type": "application/json", "Accept": "application/json", "X-Contract-Version": "v1"}
        if authed and self.token:
            headers["Authorization"] = "Bearer " + self.token
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                status, raw = r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            status, raw = e.code, e.read().decode("utf-8", "replace")
        try:
            obj = json.loads(raw)
        except ValueError:
            obj = None
        return status, obj, raw


def closed_code(obj, raw=""):
    """The closed reason words of an answer (UPPER_SNAKE only); never a body."""
    found = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and re.fullmatch(r"[A-Z][A-Z0-9_]{3,}", v) and k in ("public_reason_code", "code", "state", "reason", "error_code", "finding_code"):
                    found.append(v)
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    out = []
    for c in found:
        if c not in out:
            out.append(c)
    return ",".join(out[:3]) if out else "NONE"


SYNTH = ("SPY", "AGG", "TIMXX", "APPL", "ZQXWVK")
ROW_KEYS = ("row", "row_number", "row_index", "index", "line", "line_number")


def findings_of(obj):
    """The closed facts of every finding in a NEEDS_CORRECTION answer: (finding_code, row, synthetic symbol or none, suggestion shown). No value is kept."""
    out = []

    def walk(o):
        if isinstance(o, dict):
            code = o.get("finding_code") or (o.get("code") if isinstance(o.get("code"), str) and re.fullmatch(r"[A-Z][A-Z0-9_]{3,}", o.get("code")) and any(k in o for k in ROW_KEYS) else None)
            if isinstance(code, str) and re.fullmatch(r"[A-Z][A-Z0-9_]{3,}", code):
                row = next((str(o[k]) for k in ROW_KEYS if isinstance(o.get(k), (int, str)) and re.fullmatch(r"\d{1,6}", str(o.get(k))) ), "none")
                sym = next((v for v in o.values() if isinstance(v, str) and v in SYNTH), None)
                if sym is None:
                    for v in o.values():
                        if isinstance(v, dict):
                            sym = next((x for x in v.values() if isinstance(x, str) and x in SYNTH), None)
                            if sym:
                                break
                sug = o.get("suggestion")
                shown = bool(sug)
                sugv = sug if isinstance(sug, str) and re.fullmatch(r"[A-Z]{1,6}", sug) else None
                out.append({"code": code, "row": row, "symbol": sym or "none", "suggestion": "yes" if shown else "no", "suggestion_value": sugv})
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    return out


def finding_line(fs):
    return ",".join("%s@row%s:%s:suggestion=%s" % (f["code"], f["row"], f["symbol"], f["suggestion"]) for f in fs) or "none"


def sections_summary(obj):
    """ADDENDUM 5: closed counts and names only. The response may be enveloped under data; keys, counts and ids are returned, never a value."""
    top = sorted(obj.keys()) if isinstance(obj, dict) else []
    d = obj.get("data") if isinstance(obj, dict) and isinstance(obj.get("data"), dict) else obj
    inner = sorted(d.keys()) if isinstance(d, dict) and d is not obj else None
    secs = d.get("sections") if isinstance(d, dict) else None
    secs = secs if isinstance(secs, list) else []
    by = {}
    for s in secs:
        st = s.get("status") if isinstance(s, dict) else None
        by[st] = by.get(st, 0) + 1
    n_bo = sum(1 for s in secs if isinstance(s, dict) and s.get("method") == "BUILDER_ONLY" and s.get("status") != "VALUE")
    n_niv = sum(1 for s in secs if isinstance(s, dict) and s.get("status") == "NOT_AVAILABLE" and s.get("reason") == "NOT_IN_THIS_VERSION")
    disc = d.get("disclosures") if isinstance(d, dict) else None
    ids = [x.get("disclosure_id") for x in disc if isinstance(x, dict)] if isinstance(disc, list) else None
    return {"top_keys": top, "data_keys": inner, "n_sections": len(secs), "by_status": {str(k): v for k, v in sorted(by.items(), key=lambda kv: str(kv[0]))},
            "n_value": by.get("VALUE", 0), "n_not_available": by.get("NOT_AVAILABLE", 0), "n_builder_only_without_value": n_bo, "n_not_in_this_version": n_niv,
            "disclosure_ids": ids, "last_disclosure": (("NOT_SHOWN" if ids and ids[-1] == "NOT_SHOWN" else (ids[-1] if ids else "NONE")) if ids is not None else "NOT-IN-RESPONSE")}


def selftest():
    assert closed_code({"status": {"public_reason_code": "NOT_AUTHORIZED"}}) == "NOT_AUTHORIZED"
    assert closed_code({"x": "free text"}) == "NONE"
    assert REQ_RE.search("x REQ-" + "a" * 24 + " y") and not REQ_RE.search("REQ-short")
    assert TCK_RE.match("TCK-20261019-0123abcd") and not TCK_RE.match("TCK-1")
    assert hashlib.sha256(HOLDINGS.encode("ascii")).hexdigest() == HOLDINGS_SHA and HOLDINGS_SHA not in OLD_HOLDINGS_SHAS
    assert sum(WAITS) == 240
    s = sections_summary({"data": {"sections": [{"method": "BUILDER_ONLY", "status": "VALUE"}, {"method": "BUILDER_ONLY", "status": "NOT_AVAILABLE", "reason": "NOT_IN_THIS_VERSION"}, {"status": "VALUE"}],
                                   "disclosures": [{"disclosure_id": "A"}, {"disclosure_id": "NOT_SHOWN"}]}})
    assert s["n_sections"] == 3 and s["n_value"] == 2 and s["n_builder_only_without_value"] == 1 and s["n_not_in_this_version"] == 1 and s["last_disclosure"] == "NOT_SHOWN"
    assert sections_summary({"data": {"sections": []}})["last_disclosure"] == "NOT-IN-RESPONSE"
    assert in_forbidden_window(datetime(2026, 10, 20, 6, 0, tzinfo=timezone.utc)) and not in_forbidden_window(datetime(2026, 10, 19, 22, 0, tzinfo=timezone.utc))
    print("SELFTEST OK: closed_code, id shapes, holdings bytes, backoff sum, sections summary, windows")
    return 0


def ec2_id(boto3):
    ec2 = boto3.client("ec2", region_name=REGION)
    r = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": ["irpt-ycharts-runner"]}, {"Name": "instance-state-name", "Values": ["running"]}])
    ids = [i["InstanceId"] for x in r["Reservations"] for i in x["Instances"]]
    if len(ids) != 1:
        raise RuntimeError("running irpt-ycharts-runner count %d" % len(ids))
    return ids[0]


def ssm_run(ssm, iid, script, comment, wait_polls=60):
    cid = ssm.send_command(InstanceIds=[iid], DocumentName="AWS-RunShellScript", Comment=comment[:100], Parameters={"commands": [script], "executionTimeout": ["180"]}, TimeoutSeconds=300)["Command"]["CommandId"]
    for _ in range(wait_polls):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=iid)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            return inv.get("StandardOutputContent", "")
    return ""


def journal_since(ssm, iid, since_utc):
    """The closed IRPT_RESIDENT_PACKAGE lines since the S time: (UTC to the second, outcome=CODE | retained_for_retry class= code=)."""
    script = (
        "set -u\nUNIT=irpt-analysis-resident.service\nSINCE='%s'\n"
        "journalctl -u \"$UNIT\" --since \"$SINCE\" --no-pager -o short-iso -q 2>/dev/null | grep -E 'IRPT_RESIDENT_PACKAGE (outcome=|retained_for_retry)' | awk '{ts=substr($1,1,19); l=$0; m=\"\"; if (match(l, /outcome=[A-Z_]+/)) m=substr(l,RSTART,RLENGTH); else if (match(l, /retained_for_retry class=[A-Za-z_]+ code=([A-Z][A-Z0-9_]*|-)/)) m=substr(l,RSTART,RLENGTH); if (m!=\"\") print \"RAW P4 \" ts \"Z \" m}'\n"
    ) % since_utc.replace("T", " ").replace("Z", "")
    (HERE / "host_p4.sh").write_text(script, encoding="ascii", newline="\n")
    out = ssm_run(ssm, iid, script, "E2E4 P4 journal read-only")
    return [ln[7:] for ln in out.splitlines() if ln.startswith("RAW P4 ")]


def resolve_count(ssm, iid, since_utc):
    """Journal window, total lines scanned, the count of lines containing RESOLVE and the count of 'IRPT_RESIDENT_RESOLVE state=' lines since the first post. Counts only."""
    since = since_utc.replace("T", " ").replace("Z", "")
    script = "\n".join([
        "set -u", "UNIT=irpt-analysis-resident.service", "J=$(mktemp)",
        "journalctl -u \"$UNIT\" --since '" + since + "' --no-pager -o short-iso -q > \"$J\" 2>/dev/null",
        "echo \"RAW RES first=$(head -1 \"$J\" | cut -d' ' -f1) last=$(tail -1 \"$J\" | cut -d' ' -f1) scanned=$(wc -l < \"$J\") resolve_lines=$(grep -c RESOLVE \"$J\" || true) state_lines=$(grep -c 'IRPT_RESIDENT_RESOLVE state=' \"$J\" || true)\"",
        "rm -f \"$J\""]) + "\n"
    (HERE / "host_resolve.sh").write_text(script, encoding="ascii", newline="\n")
    out = ssm_run(ssm, iid, script, "E2E4 RESOLVE count read-only")
    m = re.search(r"RAW RES first=(\S*) last=(\S*) scanned=(\d+) resolve_lines=(\d+) state_lines=(\d+)", out)
    return {"window": "%s..%s" % (m.group(1), m.group(2)), "scanned": int(m.group(3)), "resolve_lines": int(m.group(4)), "state_lines": int(m.group(5))} if m else {"error": "unparsed"}


def original_holdings_key(ddb, upload_id):
    it = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": TENANT}, "request_revision": {"S": "UPLOAD#" + upload_id}}, ConsistentRead=True).get("Item") or {}
    for aid in sorted(set(re.findall(r"ART-[0-9a-f]{16,}", json.dumps(it)))):
        a = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": TENANT}, "request_revision": {"S": "ARTIFACT#" + aid}}, ConsistentRead=True).get("Item") or {}
        k = ((a.get("blob") or {}).get("M") or {}).get("key", {}).get("S")
        if k and "/original_holdings/" in k:
            return k
    return None



def read_text(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def git_out(*a, cwd=None):
    r = subprocess.run(["git"] + list(a), capture_output=True, text=True, cwd=str(cwd or ROOT), timeout=120)
    return r.returncode, (r.stdout or "").strip()


def ledger_closed(prefix):
    """The one change_management file whose name carries the ledger id; True when its Status line reads CLOSED."""
    names = [n for n in os.listdir(str(ROOT / CM)) if prefix in n and n.endswith("_deploy_completion.md")]
    if len(names) != 1:
        return "files=%d" % len(names)
    m = re.search(r"^\*\*Status:\*\* (\S+)", read_text(CM + names[0]), re.M)
    return "CLOSED" if m and m.group(1) == "CLOSED" else "status=%s" % (m.group(1) if m else "none")


def r0_closed_gates(run):
    """ADDENDUM 9 R0: the pair's blobs, the three closed records and the PROD tip. Returns the list of red items; prints no URL."""
    red = []
    g = run.st["r0"]["gates"] = {}
    rc, h = git_out("hash-object", COO_HALF)
    g["coo_half_blob"] = h[:10]
    if h != COO_HALF_BLOB:
        red.append("gate:coo_half_blob")
    cto = read_text(CTO_HALF)
    sect = cto[cto.index("## ADDENDUM 9"):] if "## ADDENDUM 9" in cto else ""
    g["cto_half_signed_on_blob"] = COO_HALF_BLOB[:10] in sect
    if not g["cto_half_signed_on_blob"]:
        red.append("gate:cto_half_blob")
    iam = [ln for ln in read_text(DELIV + "/irpt_anlreq_iamgrant/A_AFTER_IAMGRANT.txt").splitlines() if ln.strip() and not ln.startswith("NOTE-")]
    g["iam_grant_lines"], g["iam_grant_ledger"] = len(iam), ledger_closed("irpt-resident-commentary-read-20261020")
    if len(iam) != 6 or g["iam_grant_ledger"] != "CLOSED" or "G3 replan No changes" not in iam:
        red.append("gate:iam_grant")
    cf = [ln for ln in read_text(DELIV + "/irpt_anlreq_packager_cfprobe/A_PACKAGER_CFPROBE.txt").splitlines() if ln.startswith("A2 ")]
    g["cfprobe_a2"] = bool(cf) and "ATTACH_REFUSED:404" in cf[0] and not re.search(r"(40[13]\b)", cf[0])
    if not g["cfprobe_a2"]:
        red.append("gate:cfprobe_a2")
    r34 = read_text(DELIV + "/irpt_anlreq_r34n/A_AFTER_R34N.txt")
    g["r34n_v2s_ok"], g["r34n_ledger"] = ("V2S OK SPY KEPT and ZQXWVK NOT_KEPT" in r34), ledger_closed("irpt-resident-r34n-20261020")
    if not g["r34n_v2s_ok"] or g["r34n_ledger"] != "CLOSED":
        red.append("gate:r34n")
    r37_re = re.compile(r"^(S1 irpt-status live CodeSha256 B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE=|S2 delta 1 of 49 owned_report.py|S3 refusal envelope equal|S4 (ready report read byte-identical|NOT MADE .+)|S5 (PDF routes read NOT MADE .+|PDF routes read .+)|S6 census changed_members 0)$")
    r37 = [ln for ln in read_text(DELIV + "/irpt_anlreq_r37/A_AFTER_R37.txt").splitlines() if r37_re.match(ln)]
    g["r37_receipt_lines"], g["r37_ledger"] = len(r37), ledger_closed("irpt-status-r37-20261020")
    if len(r37) != 6 or g["r37_ledger"] != "CLOSED":
        red.append("gate:r37")
    sg_re = re.compile(r"^(R0 baseline implicitDeny get and getversion|C plan 0 to add 1 to change 0 to destroy|C policy diff adds exactly three ycharts_opal_reports resources|G1 other statements byte-equal|G2 get and getversion allowed put implicitDeny on ycharts_opal_reports|G3 replan No changes)$")
    sg = [ln for ln in read_text(DELIV + "/irpt_anlreq_statusgrant/A_AFTER_STATUSGRANT.txt").splitlines() if sg_re.match(ln)]
    g["status_grant_lines"], g["status_grant_ledger"] = len(sg), ledger_closed("irpt-status-opal-report-read-20261020")
    import boto3 as _b3
    _doc = _b3.client("iam", region_name=REGION).get_role_policy(RoleName="irpt-status-role", PolicyName="irpt-status-policy")["PolicyDocument"]
    _st = [s for s in (_doc["Statement"] if isinstance(_doc["Statement"], list) else [_doc["Statement"]]) if s.get("Sid") == "ReadRetainedAnalysisFamiliesUnderThePolicyPrefixesOnly"]
    _res = _st[0]["Resource"] if _st else []
    g["status_policy_live_resources"] = len(_res)
    g["status_policy_live_ycharts_entries"] = len([x for x in _res if "/state/ycharts_opal_reports/" in x])
    if len(sg) != 6 or g["status_grant_ledger"] != "CLOSED" or g["status_policy_live_ycharts_entries"] != 3 or g["status_policy_live_resources"] != 21:
        red.append("gate:status_grant")
    pr = read_text("org/tier2_senior/0.4.0_DT_ClientPlatform~DELL2/deliverables/irpt_anlreq_walk/A_PROMOTE_WALK.txt")
    k3 = re.search(r"^K3 CI success deployed sha ([0-9a-f]{12})", pr, re.M)
    g["promote_k3"], g["promote_ledger"] = bool(k3), ledger_closed("irpt-portal-anlreq-walk-20261020")
    if not g["promote_k3"] or g["promote_ledger"] != "CLOSED":
        red.append("gate:promote_record")
    rc, ls = git_out("ls-remote", "origin", "PROD", cwd=ROOT / "portal")
    tip = ls.split()[0] if ls else ""
    g["prod_tip12"] = tip[:12]
    g["prod_tip_equals_k3"] = bool(k3) and tip[:12] == k3.group(1)
    rc1, _ = git_out("merge-base", "--is-ancestor", GUARD_SHA, tip, cwd=ROOT / "portal") if tip else (99, "")
    rc3, _ = git_out("merge-base", "--is-ancestor", WALK_PIN, tip, cwd=ROOT / "portal") if tip else (99, "")
    rc2, _ = git_out("merge-base", "--is-ancestor", tip, GUARD_SHA, cwd=ROOT / "portal") if tip else (99, "")
    g["order_sha_in_prod"], g["walk_pin_in_prod"], g["negative_control_rc"] = (rc1 == 0), (rc3 == 0), rc2
    if not g["prod_tip_equals_k3"] or rc1 != 0 or rc3 != 0 or rc2 != 1:
        red.append("gate:walk_not_in_prod")
    req = urllib.request.Request(run.origin + "/ticket-center", method="HEAD")
    with urllib.request.urlopen(req, timeout=30) as r:
        lm = parsedate_to_datetime(r.headers.get("Last-Modified")).astimezone(timezone.utc)
    live_minute = datetime(2026, 10, 20, 16, 37, tzinfo=timezone.utc)  # the DT walk record's live minute (16:37:16Z)
    g["site_last_modified"] = lm.strftime("%Y-%m-%dT%H:%M:%SZ")
    if lm < live_minute:
        red.append("gate:site_last_modified")
    run.say("R0 gates %s red=%s" % (json.dumps(g, sort_keys=True), red))
    return red


def r0_reads(run, boto3, ddb, sqs, ssm, lam):
    """R0 (a)-(g), read only. Returns True only when every read is green; a red mints NOTHING."""
    red = []
    r0 = run.st["r0"]
    # (a) clock
    why = in_forbidden_window()
    r0["clock"] = {"utc": utc(), "weekday": datetime.now(timezone.utc).strftime("%A"), "forbidden": why}
    run.say("R0a clock %s %s forbidden_window=%s" % (r0["clock"]["utc"], r0["clock"]["weekday"], why))
    if why:
        red.append("a:" + why)
    red.extend(r0_closed_gates(run))
    # (b) function hashes and the running resident root
    r0["fn"] = {}
    for fn, want in FN_WANT.items():
        got = lam.get_function(FunctionName=fn)["Configuration"]["CodeSha256"]
        r0["fn"][fn] = {"equal": got == want, "got": got if got != want else "(equal)"}
        run.say("R0b %s CodeSha256 equals the order's value: %s%s" % (fn, got == want, "" if got == want else " got " + got))
        if got != want:
            red.append("b:" + fn)
    iid = ec2_id(boto3)
    out = ssm_run(ssm, iid, HOST_R0.read_text(encoding="ascii"), "E2E4 R0 host reads")
    m = re.search(r"RAW R0 resident_root=(\S+) active=(\S+)", out)
    root, active = (m.group(1), m.group(2)) if m else (None, None)
    r0["resident"] = {"root": root, "active": active}
    run.say("R0b resident root %s active=%s (want %s)" % (root, active, WANT_ROOT))
    if root != WANT_ROOT or active != "active":
        red.append("b:resident_root")
    yc = []
    for ln in out.splitlines():
        mm = re.match(r"RAW R0 ycharts_token (\S+) count=(\d+) last=(\S+)", ln)
        if mm:
            yc.append((mm.group(3), mm.group(1), int(mm.group(2))))
    r0["ycharts_tokens"] = [{"token": tk, "count": c, "last": ts} for ts, tk, c in sorted(yc)]
    last_yc = max((ts for ts, _, _ in yc), default=None)
    r0["ycharts_last_utc"] = last_yc
    run.say("R0f last ycharts-mentioning journal line UTC %s (tokens %d)" % (last_yc, len(yc)))
    # (c) API base: the config source name only
    r0["api_source"] = "portal-vite.config.ts-proxy-auth-target"
    vite = (ROOT / "portal/vite.config.ts").read_text(encoding="utf-8")
    host = run.base.split("//", 1)[1]
    r0["api_base_in_vite_proxy"] = host in vite
    run.say("R0c API base is the portal's vite.config.ts proxy target (the API the PROD portal calls): %s; X-Api-Key required: no (runs 1-3 logged in and posted with only the bearer and the contract header)" % r0["api_base_in_vite_proxy"])
    if not r0["api_base_in_vite_proxy"]:
        red.append("c:api_base")
    # (d) TICKET_DL_MAP and notification behaviour
    env = (lam.get_function_configuration(FunctionName="opal-ticket-api").get("Environment") or {}).get("Variables") or {}
    dl = env.get("TICKET_DL_MAP", "")
    r0["ticket_dl_map_empty"] = (dl.strip() in ("", "{}"))
    src = (ROOT / "infra/aws/lambda/ticket_center/lambda_function.py").read_text(encoding="utf-8", errors="replace")
    teams = bool(re.search(r"teams|webhook|slack", src, re.I))
    r0["ticket_service"] = {"teams_or_channel_reference": teams, "email_via_ses_only": "send_raw_email" in src, "dl_refuses_on_empty_map": "refusing to send" in src}
    run.say("R0d TICKET_DL_MAP reads {}: %s; Teams/channel poster in the ticket service source: %s; ticket-created email goes through SES to the DL map only (empty map refuses to send)" % (r0["ticket_dl_map_empty"], teams))
    if not r0["ticket_dl_map_empty"] or teams:
        red.append("d:notify")
    # (e) the three synthetic identities absent
    r0["absent"] = {}
    for label, email in (("user", EMAIL), ("run7_user", RUN7_EMAIL), ("run7b_user", RUN7B_EMAIL), ("run7c_user", RUN7C_EMAIL), ("advisor_20261020", ADVISOR), ("advisor_20261018_run4", RUN4_ADVISOR), ("advisor_20261019_untouched", MONDAY_ADVISOR)):
        row = ddb.get_item(TableName="opal-users-v2", Key={"PK": {"S": "USER#" + email}, "SK": {"S": "PROFILE"}}, ConsistentRead=True).get("Item")
        gsi = ddb.query(TableName="opal-users-v2", IndexName="email-index", KeyConditionExpression="email = :e", ExpressionAttributeValues={":e": {"S": email}}, Select="COUNT")["Count"]
        r0["absent"][label] = {"row_absent": row is None, "email_index_count": gsi}
        run.say("R0e %s: users row absent=%s email-index count=%d" % (label, row is None, gsi))
        if row is not None or gsi != 0:
            red.append("e:" + label)
    # (g) dead letter depth BEFORE
    run.st["dlq_before"] = dlq_depth(sqs)
    run.say("R0g commentary-ready queue depths before %s" % run.st["dlq_before"])
    # (h) token and bytes (the token itself is never written)
    run.token_secret = secrets.token_urlsafe(24)
    th = hashlib.sha256(run.token_secret.encode("ascii")).hexdigest()
    hh = hashlib.sha256(HOLDINGS.encode("ascii")).hexdigest()
    r0["token"] = {"first6": run.token_secret[:6], "sha256": th, "length": len(run.token_secret)}
    r0["holdings_sha256"] = hh
    run.say("R0h token first6 %s sha256 %s length %d; holdings sha256 %s (order %s)" % (r0["token"]["first6"], th, len(run.token_secret), hh, HOLDINGS_SHA))
    if hh != HOLDINGS_SHA or hh in OLD_HOLDINGS_SHAS or th in OLD_TOKEN_SHAS:
        red.append("h:token_or_bytes_equal_to_an_earlier_run")
    run.st["r0"]["red"] = red
    run.save()
    return not red


def dlq_depth(sqs):
    out = {}
    for tag, name in (("dlq", "outlook-global-commentary-draft-commentary-ready-dlq"), ("main", "outlook-global-commentary-draft-commentary-ready-queue")):
        a = sqs.get_queue_attributes(QueueUrl=sqs.get_queue_url(QueueName=name)["QueueUrl"], AttributeNames=["ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible"])["Attributes"]
        out[tag] = int(a["ApproximateNumberOfMessages"]) + int(a["ApproximateNumberOfMessagesNotVisible"])
    return out


def p6_swap(ddb, s3, req_id, input_id, upload_id):
    """P6 (read only): did the kept row ZQXWVK reach C-SWAP as UNRESOLVED/KEPT_AS_TYPED, and what did the swap pass do with it. Closed values only."""
    looked, docs = [], []

    def add_item(label, it):
        looked.append(label)
        rec = (it or {}).get("record", {}).get("S")
        if rec:
            try:
                docs.append((label + ".record", json.loads(rec)))
            except ValueError:
                pass
        b = ((it or {}).get("blob") or {}).get("M") or {}
        bucket, key = b.get("bucket", {}).get("S"), b.get("key", {}).get("S")
        if bucket and key and re.search(r"\.json$|run|holdings|compos|swap", key, re.I):
            try:
                head = s3.head_object(Bucket=bucket, Key=key)
                if head["ContentLength"] <= 8 * 1024 * 1024:
                    raw = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
                    try:
                        docs.append((label + ".blob", json.loads(raw.decode("utf-8", "replace"))))
                    except ValueError:
                        docs.append((label + ".blob.text", raw.decode("utf-8", "replace")))
            except Exception:  # noqa: BLE001
                looked.append(label + " blob unreadable")
    rows = []
    for tag, rev in (("request", "analysis#%s#1" % req_id), ("input", "INPUT#%s" % (input_id or "none")), ("upload", "UPLOAD#%s" % (upload_id or "none"))):
        it = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": TENANT}, "request_revision": {"S": rev}}, ConsistentRead=True).get("Item")
        if it:
            add_item(tag + " item", it)
            rows.append(it)
    arts = ddb.query(TableName="irpt-requests", KeyConditionExpression="tenant = :t AND begins_with(request_revision, :p)", FilterExpression="contains(logical_id, :r)",
                     ExpressionAttributeValues={":t": {"S": TENANT}, ":p": {"S": "ARTIFACT#"}, ":r": {"S": req_id}}, ConsistentRead=True)["Items"]
    for a in arts:
        add_item("artifact %s" % (a.get("family", {}).get("S") or a.get("logical_id", {}).get("S", "?")[-24:]), a)
    for it in rows:
        for aid in sorted(set(re.findall(r"ART-[0-9a-f]{16,}", json.dumps(it)))):
            a = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": TENANT}, "request_revision": {"S": "ARTIFACT#" + aid}}, ConsistentRead=True).get("Item")
            if a:
                add_item("artifact by id", a)
    res, meth, swap, notan = set(), set(), None, False

    def walk(o):
        nonlocal swap, notan
        if isinstance(o, dict):
            vals = [v for v in o.values() if isinstance(v, str)]
            if "ZQXWVK" in vals:
                for k in ("resolution", "method"):
                    v = o.get(k)
                    if isinstance(v, str) and re.fullmatch(r"[A-Z][A-Z0-9_]+", v):
                        (res if k == "resolution" else meth).add(v)
                for k in ("replacement", "replaced_by", "swap", "swapped_to", "to_ticker", "replacement_ticker"):
                    v = o.get(k)
                    if isinstance(v, str) and re.fullmatch(r"[A-Z]{1,6}", v):
                        swap = v
                st = o.get("status") or o.get("disposition")
                if isinstance(st, str) and st == "REPLACED" and swap is None:
                    swap = "REPLACED-NO-TICKER"
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str) and "ZQXWVK is not analysed" in o:
            notan = True
    for _, d in docs:
        if isinstance(d, str):
            if "ZQXWVK is not analysed" in d:
                notan = True
        else:
            walk(d)
    row = "UNRESOLVED/KEPT_AS_TYPED" if ("UNRESOLVED" in res and "KEPT_AS_TYPED" in meth) else ("%s/%s" % (",".join(sorted(res)) or "none", ",".join(sorted(meth)) or "none"))
    sw = ("REPLACED:%s" % swap) if swap else ("NOT_ANALYSED" if notan else "NOT-FOUND")
    return {"row": row, "swap": sw, "looked_in": looked, "documents_read": len(docs)}


def ticket_package(ddb, table, tkeys, ticket_id):
    """P7 (read only): the ticket item's package map: member names, which of the four refs are held (booleans), and the state word computed from them."""
    it = ddb.get_item(TableName=table, Key={tkeys[0]: {"S": ticket_id}}, ConsistentRead=True).get("Item") or {}
    pkg = (it.get("package") or {}).get("M")
    if pkg is None:
        for v in it.values():
            s = v.get("S")
            if s and s.startswith("{"):
                try:
                    d = json.loads(s)
                except ValueError:
                    continue
                if isinstance(d, dict) and isinstance(d.get("package"), dict):
                    pkg = {k: ({"S": x} if isinstance(x, str) else {"M": {}} if x else {}) for k, x in d["package"].items()}
                    break
    pkg = pkg or {}
    held = {k: bool((pkg.get(k) or {}).get("S") or (pkg.get(k) or {}).get("M")) for k in ("report_ref", "original_ref", "pdf_ref", "commentary_ref")}
    n = sum(held.values())
    state = "NONE" if n == 0 else ("COMPLETE" if n == 4 else "PARTIAL")
    return {"utc": utc(), "item_members": sorted(it.keys()), "package_members": sorted(pkg.keys()), "held": held, "state": state}


def pdf_pages(blob):
    try:
        from pypdf import PdfReader
        return len(PdfReader(io.BytesIO(blob)).pages)
    except Exception as e:  # noqa: BLE001
        return "reader_error_" + type(e).__name__


def save_pdf(blob):
    """R3: save the Overview PDF UNCHANGED outside the repository; keep only its size, sha256 and page count (never its text)."""
    d = Path(SAMPLE_DIR)
    d.mkdir(parents=True, exist_ok=True)
    out = d / "Opal_Overview_sample_E2E7D.pdf"
    out.write_bytes(blob)
    return {"size": len(blob), "sha256": hashlib.sha256(blob).hexdigest(), "pages": pdf_pages(blob), "saved": "outside-repo"}


def read_pdf_route(run, name, req_id):
    """One read of a status-Lambda PDF route as the filer: the closed code, or (when it answers a link) a plain GET of the link whose first four bytes must be %PDF. The URL is never kept."""
    s, obj, raw = run.call("GET", "/api/scoped/investor-reporting/analysis/requests/%s/%s?selected_tenant=%s" % (req_id, name, TENANT))
    data = obj.get("data") if isinstance(obj, dict) and isinstance(obj.get("data"), dict) else (obj if isinstance(obj, dict) else {})
    url = ((data or {}).get("download_route") or {}).get("url") if isinstance(data, dict) else None
    out = {"status": s, "pass": False}
    if s == 200 and url:
        try:
            with urllib.request.urlopen(urllib.request.Request(url), timeout=120) as r:
                blob = r.read()
                ctype = r.headers.get("Content-Type", "?")
            out.update(size=len(blob), type=ctype.split(";")[0], pdf=blob[:4] == b"%PDF", sha12=hashlib.sha256(blob).hexdigest()[:12])
            out["pass"] = bool(out["pdf"])
            if out["pdf"]:
                out["pages"] = pdf_pages(blob)
                out["_blob"] = blob
            else:
                out["code"] = "NOT_A_PDF"
        except Exception as e:  # noqa: BLE001
            out["code"] = "PDF_FETCH_" + type(e).__name__
    else:
        out["code"] = closed_code(obj) if closed_code(obj) != "NONE" else "STATUS_%s" % s
    url = None
    return out


def write_residue(run, s3):
    """The exact key and VersionId of every object this run's principal could not delete (bucket, key, version_id, size)."""
    rows = []
    for k in sorted(set(run.st.get("leftover_blob_keys") or [])):
        for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET_IRPT, Prefix=k):
            for v in pg.get("Versions", []):
                if v["Key"] == k:
                    rows.append({"bucket": BUCKET_IRPT, "key": k, "version_id": v["VersionId"], "size": v["Size"]})
            for m in pg.get("DeleteMarkers", []):
                if m["Key"] == k:
                    rows.append({"bucket": BUCKET_IRPT, "key": k, "version_id": m["VersionId"], "size": 0, "delete_marker": True})
    (HERE / "residue_7d.json").write_text(json.dumps(rows, indent=1) + "\n", encoding="ascii", newline="\n")
    run.st["residue_rows"] = len(rows)


def b_leg(run, phase, extra=()):
    """One browser phase through the tested script. Returns (rc, closed lines). The private token file is rewritten with a fresh token first."""
    s, obj, raw = run.call("POST", "/auth/login", {"email": EMAIL, "password": run.password}, authed=False)
    run.token = obj.get("accessToken") if isinstance(obj, dict) and obj.get("mfaRequired") is not True else None
    if not run.token:
        return 98, ["B-LEG-BAD %s login refused status=%s" % (phase, s)]
    Path(run.tokfile).write_text(run.token, encoding="ascii")
    cmd = [shutil.which("node"), str(ROOT / BROWSER), "--portal", str(ROOT / "portal"), "--origin", run.origin, "--token-file", run.tokfile, "--phase", phase, "--out", run.shots] + list(extra)
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=900, cwd=str(ROOT))
    lines = [ln.strip() for ln in (p.stdout or "").splitlines() if re.match(r"(B1|B2|B3|CALLS|B-LEG-)", ln.strip())]
    bad = [ln for ln in lines if re.search(r"https?://|eyJ|Bearer |X-Amz-", ln)]
    if bad:
        run.say("LEAK CONTROL: %d browser line(s) held a forbidden shape; not stored" % len(bad))
        lines = [ln for ln in lines if ln not in bad]
        run.st.setdefault("leak_flags", []).append(phase)
    run.st.setdefault("b_lines", {})[phase] = lines
    run.save()
    for ln in lines:
        run.say("BROWSER %s" % ln)
    return p.returncode, lines


def identify_upload(ddb):
    """The page makes the upload BEFORE a ticket id exists: find the ONE UPLOAD row of the tenant that carries BOTH this run's synthetic address and its unique holdings hash."""
    items, lek = [], None
    while True:
        kw = dict(TableName="irpt-requests", KeyConditionExpression="tenant = :t AND begins_with(request_revision, :p)",
                  ExpressionAttributeValues={":t": {"S": TENANT}, ":p": {"S": "UPLOAD#"}}, ConsistentRead=True)
        if lek:
            kw["ExclusiveStartKey"] = lek
        r = ddb.query(**kw)
        items += r["Items"]
        lek = r.get("LastEvaluatedKey")
        if not lek:
            break
    mine = [it for it in items if EMAIL in json.dumps(it) and HOLDINGS_SHA[:16] in json.dumps(it)]
    out = {"rows_read": len(items), "identified": len(mine)}
    if len(mine) == 1:
        out["upload_id"] = mine[0]["request_revision"]["S"][len("UPLOAD#"):]
        inp = sorted(set(re.findall(r"portfolio_[0-9a-f]{64}", json.dumps(mine[0]))))
        if not inp:
            norm = ddb.query(TableName="irpt-requests", KeyConditionExpression="tenant = :t AND begins_with(request_revision, :p)",
                             ExpressionAttributeValues={":t": {"S": TENANT}, ":p": {"S": "NORMALIZATION#" + out["upload_id"] + "#"}}, ConsistentRead=True)["Items"]
            inp = sorted(set(re.findall(r"portfolio_[0-9a-f]{64}", json.dumps(norm))))
        out["input_id"] = inp[0] if len(inp) == 1 else None
    return out


def attachment_ids(ddb, ticket_table, tkeys, ticket_id):
    it = ddb.get_item(TableName=ticket_table, Key={tkeys[0]: {"S": ticket_id}}, ConsistentRead=True).get("Item") or {}
    blob = json.dumps(it)
    up = sorted(set(re.findall(r"UP-[0-9a-f]{64}", blob)))
    inp = sorted(set(re.findall(r"portfolio_[0-9a-f]{64}", blob)))
    return (up[0] if len(up) == 1 else None), (inp[0] if len(inp) == 1 else None), len(up), len(inp)


def main_run():
    import boto3
    run = Run()
    run.token_secret = None
    ddb = boto3.client("dynamodb", region_name=REGION)
    s3 = boto3.client("s3", region_name=REGION)
    sqs = boto3.client("sqs", region_name=REGION)
    ssm = boto3.client("ssm", region_name=REGION)
    lam = boto3.client("lambda", region_name=REGION)
    aq2 = load_module("aq2_r28", "org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/sitting_r28.py")
    run.base = aq2.BASE
    vite = (ROOT / "portal/vite.config.ts").read_text(encoding="utf-8")
    run.origin = re.search(r"https://[a-z0-9]+\.cloudfront\.net", vite).group(0)  # the PROD alias host; held in memory only
    mint = load_module("fwd1_mint_e2e", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_mint.py")
    mint.EMAIL, mint.PK = EMAIL, "USER#" + EMAIL
    _orig_item_for = mint.item_for
    mint.item_for = lambda h: dict(_orig_item_for(h), name={"S": FILER_NAME})  # the page pre-fills the Advisor from this name
    ticket_table = ((lam.get_function_configuration(FunctionName="opal-ticket-api").get("Environment") or {}).get("Variables") or {}).get("TABLE_NAME")
    jobs_keys = [k["AttributeName"] for k in ddb.describe_table(TableName="irpt-jobs")["Table"]["KeySchema"]]
    tkeys = [k["AttributeName"] for k in ddb.describe_table(TableName=ticket_table)["Table"]["KeySchema"]]
    req_id = upload_id = input_id = ticket_id = None
    run.st["last_read_utc"] = None
    run.tokdir = tempfile.mkdtemp(prefix="e2e7d_")  # outside the repository (the system temp area)
    run.tokfile = os.path.join(run.tokdir, "t.bin")
    run.shots = os.path.join(run.tokdir, "shots")
    os.makedirs(run.shots, exist_ok=True)
    try:
        # ---- R0 (a red mints NOTHING)
        if not r0_reads(run, boto3, ddb, sqs, ssm, lam):
            run.hop("R0", "RED %s" % run.st["r0"]["red"])
            return run.stop("R0", "R0_RED") or run
        run.hop("R0", "portal-vite.config.ts-proxy-auth-target notify=none xapikey=no")
        # ---- A mint
        run.password = secrets.token_urlsafe(32)
        so, sys.stdout = sys.stdout, io.StringIO()
        si, sys.stdin = sys.stdin, io.StringIO(json.dumps({"password": run.password}))
        try:
            rc = mint.cmd_mint()
        finally:
            out, sys.stdout, sys.stdin = sys.stdout.getvalue(), so, si
        run.record("users", table="opal-users-v2", PK="USER#" + EMAIL, SK="PROFILE")
        ok = rc == 0 and "MINT-OK READBACK-OK" in out
        run.hop("A", ("mint ok name=%s" % FILER_NAME) if ok else "mint REFUSED " + (out.strip().splitlines() or ["?"])[0][:60])
        if not ok:
            return run.stop("A", "MINT_REFUSED") or run
        run.st["advisor_written"] = False
        run.hop("A2", "advisor prefilled-by-page")
        # ---- L login: the one private token file
        s, obj, raw = run.call("POST", "/auth/login", {"email": EMAIL, "password": run.password}, authed=False)
        run.token = obj.get("accessToken") if isinstance(obj, dict) and obj.get("mfaRequired") is not True else None
        if run.token:
            Path(run.tokfile).write_text(run.token, encoding="ascii")
        run.hop("L", "token private-file ok" if run.token and os.path.isfile(run.tokfile) else "token private-file REFUSED %s status=%s" % (closed_code(obj), s))
        if not run.token:
            return run.stop("L", "LOGIN_%s" % s) or run
        try:
            claims = json.loads(base64.urlsafe_b64decode(run.token.split(".")[1] + "=" * (-len(run.token.split(".")[1]) % 4)).decode("utf-8"))
        except Exception:  # noqa: BLE001
            claims = {}
        run.st["token_claim_name_is_filer_name"] = claims.get("name") == FILER_NAME
        run.st["token_claim_keys"] = sorted(claims.keys())
        run.say("L token claim name equals the synthetic filer name: %s (claim keys %s)" % (run.st["token_claim_name_is_filer_name"], run.st["token_claim_keys"]))
        if not run.st["token_claim_name_is_filer_name"]:
            return run.stop("L", "NAME_CLAIM_ABSENT") or run
        # the holdings file: exact bytes, outside the repository
        hpath = os.path.join(run.tokdir, "holdings_e2e7d.csv")
        with open(hpath, "wb") as fh:
            fh.write(HOLDINGS.encode("ascii"))
        if hashlib.sha256(open(hpath, "rb").read()).hexdigest() != HOLDINGS_SHA:
            return run.stop("A", "HOLDINGS_SHA") or run
        # ---- B1 (read only)
        rc, lines = b_leg(run, "b1")
        b1 = next((ln for ln in lines if ln.startswith("B1 ")), None)
        m = re.match(r"B1 form labels=(\d+) advisor=(\S+) advisor_prefilled=(\S+) report_type=(\S+) commentary=(\S+) firms=(.*?) models=(\d+)$", b1 or "")
        if rc != 0 or not m:
            run.st["b1_line"] = "NOT-RUN b1 " + ((lines[-1] if lines else "no output")[:120])
            run.hop("B1", run.st["b1_line"])
            return run.stop("B1", "B_LEG_BAD") or run
        labels, adv, pre, rt, cm, firms, models = int(m.group(1)), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), int(m.group(7))
        run.st["b1_line"] = "form <labels=%d advisor=%s advisor_prefilled=%s report_type=%s commentary=%s firms=%s models=%d>" % (labels, adv, pre, rt, cm, firms, models)
        run.st["b1_firm_count"] = len([x for x in firms.split(",") if x.strip()])
        run.hop("B1", run.st["b1_line"])
        if adv != "required" or pre != "yes" or rt != "absent" or cm != "absent" or models != 5:
            return run.stop("B1", "B1_FACTS_RED") or run
        # ---- B2: wait the YCharts quiet time, then ONE filing through the page
        lyc = run.st["r0"].get("ycharts_last_utc")
        if lyc:
            due = datetime.fromisoformat(lyc.replace("Z", "+00:00")).timestamp() + YC_QUIET_S
            while time.time() < due:
                time.sleep(min(20, max(1, due - time.time())))
        t_b2 = time.time()
        run.st["b2_start_utc"] = utc(t_b2)
        rc, lines = b_leg(run, "b2", ["--holdings", hpath, "--firm", FIRM_ID, "--household", HOUSEHOLD])
        b2 = next((ln for ln in lines if ln.startswith("B2 ")), None)
        m = re.match(r"B2 filed ok ticket=(TCK-\d{8}-[0-9a-f]{8}) req=(REQ-[0-9a-f]{24}|none) at=(\S+)", b2 or "")
        t_after_b2 = time.time()
        found = identify_upload(ddb)
        run.st["upload_identified"] = {k: v for k, v in found.items() if k != "item"}
        if found.get("upload_id"):
            upload_id, input_id = found["upload_id"], found.get("input_id")
            run.record("upload", tenant=TENANT, upload_id=upload_id, input_id=input_id)
            art_key = original_holdings_key(ddb, upload_id)
            run.st["art_key_for_delete"], run.st["art_key_recorded"] = art_key, bool(art_key)
        if m:
            ticket_id = m.group(1)
            req_id = m.group(2) if m.group(2) != "none" else None
            run.record("ticket", table=ticket_table, **{tkeys[0]: ticket_id})
            tu, ti, nu, ni = attachment_ids(ddb, ticket_table, tkeys, ticket_id)
            run.st["attachment_counts"] = {"upload_ids": nu, "input_ids": ni, "ticket_upload_equals_identified": (tu == upload_id)}
            if req_id:
                run.record("request", table="irpt-requests", tenant=TENANT, request_revision="analysis#%s#1" % req_id)
                run.record("job", table="irpt-jobs", **{jobs_keys[0]: TENANT, jobs_keys[1]: req_id})
        ok = rc == 0 and bool(m) and bool(req_id)
        run.st["s_time_utc"] = run.st["b2_start_utc"]
        run.st["b2_line"] = ("filed ok ticket=%s req=%s at=%s" % (ticket_id, req_id, m.group(3))) if ok else ("REFUSED " + ((b2 or (lines[-1] if lines else "no output"))[:140]))
        run.hop("B2", run.st["b2_line"])
        if not ok:
            return run.stop("B2", "B2_REFUSED") or run
        # ---- P poll (20 s step, 30 minutes in total from the filing)
        green, sha, last_journal = {}, None, 0.0
        p7_ready = None
        deadline = t_after_b2 + POLL_BUDGET_S
        while time.time() < deadline:
            job = ddb.get_item(TableName="irpt-jobs", Key={jobs_keys[0]: {"S": TENANT}, jobs_keys[1]: {"S": req_id}}, ConsistentRead=True).get("Item")
            if job and job.get("state", {}).get("S") == "READY":
                green.setdefault("P1", utc())
            if "P1" in green and p7_ready is None:
                p7_ready = ticket_package(ddb, ticket_table, tkeys, ticket_id)
                run.st["p7_ready"] = p7_ready
                run.say("P7 at READY %s" % json.dumps(p7_ready, sort_keys=True))
            item = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": TENANT}, "request_revision": {"S": "analysis#%s#1" % req_id}}, ConsistentRead=True).get("Item")
            ref = (item or {}).get("commentary_ref", {}).get("M")
            if ref and re.fullmatch(r"[0-9a-f]{64}", ref.get("sha256", {}).get("S", "")):
                sha = ref["sha256"]["S"]
                green.setdefault("P2", utc())
            arts = ddb.query(TableName="irpt-requests", KeyConditionExpression="tenant = :t AND begins_with(request_revision, :p)", FilterExpression="contains(logical_id, :r)",
                             ExpressionAttributeValues={":t": {"S": TENANT}, ":p": {"S": "ARTIFACT#"}, ":r": {"S": req_id}}, ConsistentRead=True)["Items"]
            lids = {a.get("logical_id", {}).get("S") for a in arts}
            if req_id in lids:
                green.setdefault("P3", utc())
            if sha and ("%s-commentary-%s" % (req_id, sha)) in lids:
                green.setdefault("P5", utc())
            if time.time() - last_journal >= 60:
                last_journal = time.time()
                lines_j = journal_since(ssm, ec2_id(boto3), run.st["s_time_utc"])
                run.st["journal"] = lines_j
                if any("RecipeRefused" in x for x in lines_j):
                    run.hop("P1", "VENDOR PRODUCER (RecipeRefused): the routing fix failed")
                    break
                if any("outcome=ATTACHED" in x or "outcome=ALREADY_ATTACHED" in x for x in lines_j):
                    green.setdefault("P4", utc())
                if any("retained_for_retry" in x for x in lines_j):
                    run.hop("P4", "retained_for_retry seen")
                    break
            run.st["green"] = green
            run.save()
            if all(k in green for k in ("P1", "P2", "P3", "P4", "P5")):
                break
            time.sleep(POLL_STEP_S)
        run.st["green"] = green
        if all(k in green for k in ("P1", "P2", "P3", "P4", "P5")):
            run.st["p7_final"] = ticket_package(ddb, ticket_table, tkeys, ticket_id)
            run.say("P7 final %s" % json.dumps(run.st["p7_final"], sort_keys=True))
        first_red = next((k for k in ("P1", "P2", "P3", "P4", "P5") if k not in green), None)
        run.hop("POLL", "green=%s first_red=%s" % (sorted(green), first_red))
        if first_red:
            return run.stop(first_red, "RETAINED_FOR_RETRY" if any("retained_for_retry" in x for x in run.st["journal"]) else "NOT_READY_IN_BUDGET") or run
        # ---- B3: Open report on the finished ticket (a ticket without the report face is a finding, not a stop)
        rc, lines = b_leg(run, "b3", ["--ticket", ticket_id])
        b3 = next((ln for ln in lines if ln.startswith("B3 ")), None)
        m3 = re.match(r"B3 report face=(\S+) headings=(\d+) value=(\S+)", b3 or "")
        run.st["b3_line"] = ("report <face=%s headings=%s value=%s>" % m3.groups()) if (m3 and m3.group(1) == "yes") else ("FAIL " + ((b3 or (lines[-1] if lines else "no output"))[:120]))
        run.st["last_read_utc"] = utc()
        run.hop("B3", run.st["b3_line"])
        # ---- R: the Overview route /pdf; R3: saved outside the repository; R4: the commentary route (read whether R passed or not)
        s, obj, raw = run.call("POST", "/auth/login", {"email": EMAIL, "password": run.password}, authed=False)
        run.token = obj.get("accessToken") if isinstance(obj, dict) else run.token
        ov = read_pdf_route(run, "pdf", req_id)
        blob = ov.pop("_blob", None)
        run.st["route"] = ov
        if ov.get("pass") and blob:
            run.st["r3"] = save_pdf(blob)
            run.say("R3 %s" % json.dumps({k: (v if k != "sha256" else v[:12]) for k, v in run.st["r3"].items()}, sort_keys=True))
        blob = None
        run.st["last_read_utc"] = utc()
        run.hop("R", "route %s" % json.dumps(ov, sort_keys=True))
        r4 = read_pdf_route(run, "commentary-pdf", req_id)
        r4.pop("_blob", None)
        run.st["r4"] = r4
        run.st["last_read_utc"] = utc()
        run.hop("R4", "commentary %s" % json.dumps(r4, sort_keys=True))
        if not ov.get("pass"):
            run.stop("R", ov.get("code", "ROUTE_REFUSED"))
        return run
    finally:
        try:
            # ---- R2 sections read (ONE try; after R or after a stop at R; only when a REQ exists and the run got that far)
            if req_id and run.st["hops"].get("B2", "").startswith("filed ok") and run.st["stopped_at"] in (None, "R"):
                s, obj, raw = run.call("POST", "/auth/login", {"email": EMAIL, "password": run.password}, authed=False) if run.password else (0, None, "")
                run.token = obj.get("accessToken") if isinstance(obj, dict) else run.token
                s, obj, raw = run.call("GET", "/api/scoped/investor-reporting/analysis/%s/sections?selected_tenant=%s" % (req_id, TENANT))
                if s == 200 and isinstance(obj, (dict, list)):
                    run.st["r2"] = dict(sections_summary(obj if isinstance(obj, dict) else {"sections": obj}), status=s)
                else:
                    run.st["r2"] = {"refused": closed_code(obj) if closed_code(obj) != "NONE" else "STATUS_%s" % s, "status": s}
                run.st["last_read_utc"] = utc()
                run.say("R2 %s" % json.dumps(run.st["r2"], sort_keys=True))
        except Exception as e:  # noqa: BLE001
            run.st["r2"] = {"refused": "EXC_" + type(e).__name__}
            run.st["last_read_utc"] = utc()
        run.token = None
        run.password = None
        try:
            run.st["dlq_after"] = dlq_depth(sqs)
        except Exception as e:  # noqa: BLE001
            run.st["dlq_after"] = {"error": type(e).__name__}
        run.st["last_read_utc"] = utc()
        try:
            # ADDENDUM 4: 5 minutes since the last upload post cannot be observed (the page posts); the resolve of the upload is observed by a state line or 5 minutes after the filing
            if run.st.get("b2_start_utc"):
                lp = datetime.fromisoformat(run.st["b2_start_utc"].replace("Z", "+00:00")).timestamp()
                while time.time() < lp + 300:
                    rl = resolve_count(ssm, ec2_id(boto3), run.st["b2_start_utc"])
                    if rl.get("state_lines", 0) > 0:
                        run.st["resolve_observed"] = rl
                        break
                    time.sleep(30)
        except Exception as e:  # noqa: BLE001
            run.st["resolve_wait_error"] = type(e).__name__
        try:
            if any(k.get("kind") == "users" for k in run.keys):
                run.st["first_delete_utc"] = utc()
                delete_all(run, ddb, s3, mint, req_id, upload_id, input_id, ticket_id, ticket_table, tkeys, jobs_keys)
                write_residue(run, s3)
            else:
                run.say("D: nothing was minted by this run; nothing is deleted")
                run.st["deleted"] = {"absent": 0, "recorded": 0}
        except Exception as e:  # noqa: BLE001
            run.st["delete_error"] = type(e).__name__
            run.say("D ERROR %s" % type(e).__name__)
        # the private token file and its folder (the screenshots are copied out by hand after they are looked at, so the folder holds them until then: only the token and holdings files go here)
        try:
            for fn in (run.tokfile, os.path.join(run.tokdir, "holdings_e2e7d.csv")):
                if os.path.isfile(fn):
                    os.remove(fn)
            run.st["token_file_absent"] = not os.path.exists(run.tokfile)
            run.st["token_dir_kept_for_shots"] = run.tokdir  # a temp path; it holds only the screenshots now
        except Exception as e:  # noqa: BLE001
            run.st["token_delete_error"] = type(e).__name__
        run.st["finished_utc"] = utc()
        run.save()


def delete_all(run, ddb, s3, mint, req_id, upload_id, input_id, ticket_id, ticket_table, tkeys, jobs_keys):
    """Delete exactly the recorded keys (plus the artifact items found by a query on THIS run's REQ id and the upload's own ids), each conditional, each read back ABSENT."""
    run.say("D: deleting recorded keys (first delete %s after last read %s)" % (run.st["first_delete_utc"], run.st["last_read_utc"]))
    recorded, absent = 0, 0
    plan = []
    if upload_id:
        plan.append(("upload", "irpt-requests", {"tenant": {"S": TENANT}, "request_revision": {"S": "UPLOAD#" + upload_id}}))
        norm = ddb.query(TableName="irpt-requests", KeyConditionExpression="tenant = :t AND begins_with(request_revision, :p)",
                         ExpressionAttributeValues={":t": {"S": TENANT}, ":p": {"S": "NORMALIZATION#" + upload_id + "#"}}, ConsistentRead=True)["Items"]
        for it in norm:
            plan.append(("normalization", "irpt-requests", {"tenant": it["tenant"], "request_revision": it["request_revision"]}))
    if input_id:
        plan.append(("input", "irpt-requests", {"tenant": {"S": TENANT}, "request_revision": {"S": "INPUT#" + input_id}}))
    if req_id:
        plan.append(("request", "irpt-requests", {"tenant": {"S": TENANT}, "request_revision": {"S": "analysis#%s#1" % req_id}}))
        plan.append(("job", "irpt-jobs", {jobs_keys[0]: {"S": TENANT}, jobs_keys[1]: {"S": req_id}}))
    if ticket_id:
        plan.append(("ticket", ticket_table, {tkeys[0]: {"S": ticket_id}}))
    art_ids = set()
    for label, tbl, key in list(plan):
        if label in ("upload", "input", "normalization"):
            it = ddb.get_item(TableName=tbl, Key=key, ConsistentRead=True).get("Item") or {}
            art_ids.update(re.findall(r"ART-[0-9a-f]{16,}", json.dumps(it)))
    items = []
    if req_id:
        items += ddb.query(TableName="irpt-requests", KeyConditionExpression="tenant = :t AND begins_with(request_revision, :p)", FilterExpression="contains(logical_id, :r)",
                           ExpressionAttributeValues={":t": {"S": TENANT}, ":p": {"S": "ARTIFACT#"}, ":r": {"S": req_id}}, ConsistentRead=True)["Items"]
    for aid in sorted(art_ids):
        it = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": TENANT}, "request_revision": {"S": "ARTIFACT#" + aid}}, ConsistentRead=True).get("Item")
        if it and all(it["request_revision"]["S"] != x["request_revision"]["S"] for x in items):
            items.append(it)
    blobs = []
    for it in items:
        plan.append(("artifact", "irpt-requests", {"tenant": it["tenant"], "request_revision": it["request_revision"]}))
        b = (it.get("blob") or {}).get("M") or {}
        if b.get("bucket", {}).get("S") and b.get("key", {}).get("S"):
            blobs.append((b["bucket"]["S"], b["key"]["S"]))
    run.st["delete_plan"] = {"rows": len(plan), "blob_keys": len(blobs)}
    for label, tbl, key in plan:
        recorded += 1
        try:
            ddb.delete_item(TableName=tbl, Key=key, ConditionExpression=" AND ".join("attribute_exists(#k%d)" % i for i in range(len(key))), ExpressionAttributeNames={"#k%d" % i: n for i, n in enumerate(key)})
        except Exception as e:  # noqa: BLE001
            run.say("D %s not deleted: %s" % (label, type(e).__name__))
        absent += 1 if ddb.get_item(TableName=tbl, Key=key, ConsistentRead=True).get("Item") is None else 0
    for bucket, key in blobs:
        recorded += 1
        try:
            vs = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=key) for v in (pg.get("Versions", []) + pg.get("DeleteMarkers", [])) if v["Key"] == key]
            for v in vs:
                s3.delete_object(Bucket=bucket, Key=key, VersionId=v["VersionId"])
        except Exception as e:  # noqa: BLE001
            run.say("D blob not deleted: %s" % type(e).__name__)
            run.st.setdefault("leftover_blob_keys", []).append(key)
        left = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=key) for v in (pg.get("Versions", []) + pg.get("DeleteMarkers", [])) if v["Key"] == key]
        absent += 1 if not left else 0
    # the original-holdings blob: the key is recorded; the delete is refused for this principal (AR-y-402 W5 NONE FOUND): tried once, reported if it stays
    ahk = run.st.get("art_key_for_delete")
    if ahk:
        recorded += 1
        bucket = blobs[0][0] if blobs else None
        if bucket is None:
            run.st.setdefault("leftover_blob_keys", []).append(ahk)
        else:
            vs = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=ahk) for v in (pg.get("Versions", []) + pg.get("DeleteMarkers", [])) if v["Key"] == ahk]
            code = None
            try:
                for v in vs:
                    s3.delete_object(Bucket=bucket, Key=ahk, VersionId=v["VersionId"])
            except Exception as e:  # noqa: BLE001
                code = getattr(e, "response", {}).get("Error", {}).get("Code") or type(e).__name__
            left = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=ahk) for v in (pg.get("Versions", []) + pg.get("DeleteMarkers", [])) if v["Key"] == ahk]
            if left:
                run.st.setdefault("leftover_blob_keys", []).append(ahk)
                run.st["leftover_delete_code"] = code or "STILL_PRESENT"
                recorded += 0
            else:
                absent += 1
    recorded += 1
    so, sys.stdout = sys.stdout, io.StringIO()
    try:
        mint.cmd_remove()
    finally:
        out, sys.stdout = sys.stdout.getvalue(), so
    absent += 1 if ("ABSENT GSI" in out and "ABSENT CONSISTENT" in out) else 0
    if run.st.get("advisor_written"):
        recorded += 2
        rem = subprocess.run([sys.executable, str(ROOT / ADVISOR_TOOL), "remove", "--date", ADVISOR_DATE], capture_output=True, text=True, timeout=600)
        rout = rem.stdout or ""
        absent += 1 if ("ABSENT GSI" in rout and "ABSENT CONSISTENT" in rout) else 0
        absent += 1 if "ABSENT PARTNER" in rout else 0
    run.st["deleted"] = {"absent": absent, "recorded": recorded}
    run.say("D deleted %d of %d recorded keys ABSENT" % (absent, recorded))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--go" in sys.argv:
        r = main_run()
        sys.exit(0 if r and not r.st.get("stopped_at") else 1)
    print("USAGE e2e7d_run.py --selftest | --go")
    sys.exit(2)
