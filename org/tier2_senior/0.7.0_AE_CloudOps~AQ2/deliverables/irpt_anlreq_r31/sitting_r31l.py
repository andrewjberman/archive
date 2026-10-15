"""IRPT_ANLREQ TO-APPLY-R31L reads (0.7.0_AE_CloudOps~AQ2): the before and after reads of the irpt-status release as ONE synthetic
internal viewer, one RS256 token held in this process only, never written, printed or logged.

  --selftest        the comparison helpers on synthetic data (no AWS, no network)
  --live --go       mint the viewer, take the BEFORE reads, wait for <flagdir>/go_after (or abort), take the AFTER reads, remove the row after exp

Kept: status, public/code names, sha256 of bodies, key-name PATTERNS (list indices and id-like keys normalised), counts. No response body,
no value from a body and no address is printed or written. The before body lives in this process's memory for the comparison only.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "irpt_anlreq_r28"))
import sitting_r28 as base  # noqa: E402

SECTIONS = "/api/scoped/investor-reporting/analysis/%s/sections?selected_tenant=%s"
PDF = "/api/scoped/investor-reporting/analysis/requests/%s/pdf?selected_tenant=%s"
BEFORE_SHA = "yNpw441TP5aMGYuZqkHQAPjAiQJDEPk7q8kFeDiIRIg="
AFTER_SHA = "PcGK+EpSq0EelZP+2T8+PB6b+ZXB+q3BCjD9g4UNiLE="
IDLIKE = re.compile(r"^(?:[0-9]{6,}|[0-9a-fA-F]{16,}|(?:REQ|RPT|ART|UP|sel|portfolio)[-_][0-9A-Za-z_-]{8,})$")
CODEWORD = re.compile(r"^[A-Z][A-Z0-9_]{3,}$")


def sha(x):
    return hashlib.sha256(x.encode("utf-8") if isinstance(x, str) else x).hexdigest()


def canon(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def patterns(o, prefix=""):
    """Counter of key-path PATTERNS: list indices become [], id-like dict keys become <id>. No value is kept."""
    out = Counter()
    if isinstance(o, dict):
        for k, v in o.items():
            seg = "<id>" if IDLIKE.match(str(k)) else str(k)
            p = prefix + "." + seg if prefix else seg
            out[p] += 1
            out.update(patterns(v, p))
    elif isinstance(o, list):
        for v in o:
            p = prefix + "[]"
            out[p] += 0
            out.update(patterns(v, p))
    return out


def strip_to(after, before):
    """A copy of `after` with every dict key absent from `before` removed (lists of equal length are walked element by element)."""
    if isinstance(after, dict) and isinstance(before, dict):
        return {k: strip_to(v, before[k]) for k, v in after.items() if k in before}
    if isinstance(after, list) and isinstance(before, list) and len(after) == len(before):
        return [strip_to(a, b) for a, b in zip(after, before)]
    return copy.deepcopy(after)


def top_names(o):
    return sorted(o) if isinstance(o, dict) else None


def codes_of(b):
    """Code-like STRING values of the status object and of data.state (names such as REPORT_TICKET_MISMATCH), nothing else."""
    out = set()
    if isinstance(b, dict):
        st = b.get("status")
        if isinstance(st, dict):
            for v in st.values():
                if isinstance(v, str) and CODEWORD.match(v):
                    out.add(v)
        d = b.get("data")
        if isinstance(d, dict) and isinstance(d.get("state"), str) and CODEWORD.match(d["state"]):
            out.add(d["state"])
    return sorted(out)


def selftest():
    before = {"data": {"request_ref": {"a": 1}, "sections": [{"title": "t", "dates": {"from": "x"}}, {"title": "u"}], "extraction_validation": {"ok": True}}}
    after = {"data": {"request_ref": {"a": 1}, "sections": [{"title": "t", "dates": {"from": "x"}, "provider_dates": {"d": "y"}}, {"title": "u"}],
                      "extraction_validation": {"ok": True}, "retained_ref": {"report_id": "RPT-" + "a" * 32}}}
    assert canon(strip_to(after, before)) == canon(before), "strip_to must remove only the added keys"
    added = patterns(after) - patterns(before)
    assert set(added) == {"data.sections[].provider_dates", "data.sections[].provider_dates.d", "data.retained_ref", "data.retained_ref.report_id"}, sorted(added)
    changed = json.loads(canon(after))
    changed["data"]["request_ref"]["a"] = 2
    assert canon(strip_to(changed, before)) != canon(before), "a changed value must show"
    shorter = json.loads(canon(after))
    shorter["data"]["sections"].pop()
    assert canon(strip_to(shorter, before)) != canon(before), "a removed element must show"
    assert "<id>" in "".join(patterns({"RPT-" + "b" * 32: 1})), "id-like keys are normalised"
    assert codes_of({"ok": False, "status": {"public_reason_code": "INVALID_INPUT", "message": "no codes in this sentence"}}) == ["INVALID_INPUT"]
    print("SELFTEST OK")
    return 0


class Client:
    def __init__(self, log):
        self.log, self.token, self.last = log, None, 0.0

    def get(self, arm, path, *, authed, gap=True):
        if gap and authed:
            wait = base.GAP - (time.time() - self.last)
            if wait > 0:
                time.sleep(wait)
        req = urllib.request.Request(base.BASE + path, method="GET")
        req.add_header("x-contract-version", "v1")
        if authed:
            req.add_header("Authorization", "Bearer " + self.token)
        start = time.time()
        if authed:
            self.last = start
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                st, raw = r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            st, raw = e.code, e.read().decode("utf-8", "replace")
        b = base.parsed(raw)
        self.log("read %s%s status=%s codes=%s body_sha256=%s bytes=%d" % (arm, "" if authed else " (no credential)", st, codes_of(b), sha(raw), len(raw)))
        return st, b, raw


def live(args):
    import boto3
    import jwt as pyjwt

    outdir, flagdir = Path(args.out), Path(args.flagdir)
    addr = "irpt-r31-iv-%s@opal.invalid" % args.date
    ddb = boto3.client("dynamodb", region_name=base.REGION)
    lam = boto3.client("lambda", region_name=base.REGION)
    lines, reads = [], []
    key = {"PK": {"S": "USER#" + addr}, "SK": {"S": "PROFILE"}}

    def say(msg):
        line = "%s %s" % (base.iso(), msg)
        print(line, flush=True)
        lines.append(line)

    def cread():
        return ddb.get_item(TableName=base.USERS, Key=key, ConsistentRead=True).get("Item")

    def gsi():
        return ddb.query(TableName=base.USERS, IndexName="email-index", KeyConditionExpression="email = :e",
                         ExpressionAttributeValues={":e": {"S": addr}}, Select="COUNT")["Count"]

    cl = Client(say)
    written, exp, stop = False, None, None
    st = {}
    try:
        got = lam.get_function_configuration(FunctionName="irpt-status")["CodeSha256"]
        say("irpt-status CodeSha256 before the window: %s" % ("EQUAL to the expected pre-window value" if got == BEFORE_SHA else "DIFFERENT"))
        if got != BEFORE_SHA:
            raise RuntimeError("the Lambda is not at its pre-window CodeSha256")
        if cread() is not None or gsi() != 0:
            raise RuntimeError("the viewer address is not ABSENT")
        now = base.iso()
        item = {"PK": key["PK"], "SK": key["SK"], "email": {"S": addr}, "firmId": {"S": "opal-capital"}, "status": {"S": "active"},
                "name": {"S": "IRPT_ANLREQ R31L synthetic internal viewer"}, "role": {"S": "user"}, "tier": {"S": "internal"},
                "userType": {"S": "test-filer"}, "createdAt": {"S": now}, "createdBy": {"S": "0.7.0_AE_CloudOps~AQ2"}, "updatedAt": {"S": now}}
        ddb.put_item(TableName=base.USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")
        written = True
        back = cread()
        if back is None or back["status"]["S"] != "active" or "allowedFirmIds" in back:
            raise RuntimeError("the viewer row is not PRESENT as designed (active, no allowedFirmIds)")
        say("viewer users row written (attribute_not_exists) and read back PRESENT: active, no allowedFirmIds")
        pem = boto3.client("secretsmanager", region_name=base.REGION).get_secret_value(SecretId=base.KEY_SECRET)["SecretString"]
        if "BEGIN" not in pem[:40]:
            raise RuntimeError("signing secret is not a PEM string")
        say("signing key read (value never printed or written)")
        iat = int(time.time())
        claims = {"sub": addr, "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal", "role": "user",
                  "userType": "test-filer", "name": "IRPT_ANLREQ R31L synthetic internal viewer", "iat": iat, "exp": iat + base.LIFE}
        cl.token = pyjwt.encode(claims, pem, algorithm="RS256")
        exp = claims["exp"]
        del pem
        say("token minted (held in memory only) iat=%s exp=%s" % (base.iso(iat), base.iso(exp)))

        # ---- BEFORE
        s, b, raw = cl.get("sections", SECTIONS % ("REQ-" + "0" * 24, "49financial"), authed=False)
        st["cred_before"] = (s, sha(raw))
        chosen = None
        for cand in args.cand:
            tenant, job = cand.split(":", 1)
            s, b, raw = cl.get("sections %s" % job, SECTIONS % (job, tenant), authed=True)
            d = b.get("data") if isinstance(b, dict) else None
            if s == 200 and isinstance(b, dict) and b.get("ok") is not False and isinstance(d, dict):
                chosen = (tenant, job)
                st["before"] = {"status": s, "sha": sha(raw), "env_keys": top_names(b), "data_keys": top_names(d), "data": copy.deepcopy(d),
                                "canon": sha(canon(d)), "envrest": sha(canon({k: v for k, v in b.items() if k != "data"})), "patterns": patterns(d)}
                break
            reads.append("BEFORE candidate %s: status %s codes %s (not used)" % (job, s, codes_of(b)))
        if not chosen:
            raise RuntimeError("no candidate report read as 200 for the viewer before the change: R0e(b) cannot be taken")
        tenant, job = chosen
        reads.append("R0E a credential-less sections read: status %s body_sha256 %s" % st["cred_before"])
        reads.append("R0E b report job %s tenant %s: status 200 body_sha256 %s; envelope keys %s; data keys %s; has retained_ref %s"
                     % (job, tenant, st["before"]["sha"], st["before"]["env_keys"], st["before"]["data_keys"], "retained_ref" in (st["before"]["data_keys"] or [])))
        s, b, raw = cl.get("pdf route", PDF % (job, tenant), authed=True)
        d = b.get("data") if isinstance(b, dict) else None
        st["pdf_before"] = (s, codes_of(b), top_names(d), (b.get("ok") if isinstance(b, dict) else None))
        reads.append("R0E c pdf route for the same request: status %s codes %s data keys %s ok %s" % st["pdf_before"])
        say("BEFORE-DONE job=%s tenant=%s (waiting for %s/go_after, abort flag %s/abort)" % (job, tenant, flagdir, flagdir))

        # ---- wait for the signal
        deadline = exp - 200
        while time.time() < deadline:
            if (flagdir / "abort").exists():
                raise RuntimeError("abort flag found: no after-reads")
            if (flagdir / "go_after").exists():
                break
            time.sleep(2)
        else:
            raise RuntimeError("the token neared its exp before go_after: no after-reads")
        say("go_after seen")

        # ---- AFTER
        got = lam.get_function_configuration(FunctionName="irpt-status")["CodeSha256"]
        say("irpt-status CodeSha256 at the after-reads: %s" % ("EQUAL to the expected released value" if got == AFTER_SHA else "DIFFERENT"))
        s, b, raw = cl.get("sections", SECTIONS % ("REQ-" + "0" * 24, "49financial"), authed=False)
        st["cred_after"] = (s, sha(raw))
        reads.append("T3 credential-less sections read after: status %s body_sha256 %s; equal to before: %s" % (s, sha(raw), st["cred_after"] == st["cred_before"]))
        s, b, raw = cl.get("sections (no ticket_id)", SECTIONS % (job, tenant), authed=True)
        d = b.get("data") if isinstance(b, dict) else None
        if s == 200 and isinstance(d, dict):
            bef = st["before"]
            stripped = strip_to(d, bef["data"])
            added = patterns(d) - bef["patterns"]
            removed = bef["patterns"] - patterns(d)
            same = sha(canon(stripped)) == bef["canon"]
            envrest = sha(canon({k: v for k, v in b.items() if k != "data"})) == bef["envrest"]
            reads.append("T4c viewer report read WITHOUT ticket_id after: status %s; envelope keys %s; data keys %s" % (s, top_names(b), top_names(d)))
            reads.append("T4c data key-path patterns ADDED after (count): %s" % sorted((k, n) for k, n in added.items()))
            reads.append("T4c data key-path patterns REMOVED after: %s" % sorted(removed))
            reads.append("T4c data with the added keys removed equals the before data (sha256 %s): %s; the envelope outside data equal: %s" % (bef["canon"][:16], same, envrest))
            st["t4c"] = {"status": s, "same": same, "envrest": envrest, "removed": len(removed), "added": sorted(added), "canon": sha(canon(d))}
        else:
            st["t4c"] = {"status": s}
            reads.append("T4c viewer report read WITHOUT ticket_id after: status %s codes %s (not a 200 answer)" % (s, codes_of(b)))
        # extra arms: the AR-y-71 selector on an UNTICKETED request
        s, b, raw = cl.get("sections ticket_id=malformed", SECTIONS % (job, tenant) + "&ticket_id=not-a-ticket", authed=True)
        reads.append("T4 extra: malformed ticket_id -> status %s codes %s (expect INVALID_REPORT_TICKET_ID / INVALID_INPUT)" % (s, codes_of(b)))
        st["malformed"] = (s, codes_of(b))
        s, b, raw = cl.get("sections ticket_id=well-formed on an unticketed request", SECTIONS % (job, tenant) + "&ticket_id=TCK-20261015-0a1b2c3d", authed=True)
        d2 = b.get("data") if isinstance(b, dict) else None
        same2 = bool(st.get("t4c", {}).get("canon")) and isinstance(d2, dict) and sha(canon(d2)) == st["t4c"].get("canon")
        reads.append("T4 extra: well-formed ticket_id on a request that stores none -> status %s codes %s; data equal to the no-ticket read: %s (expect 200, unchanged)" % (s, codes_of(b), same2))
        st["wellformed"] = (s, same2)
        s, b, raw = cl.get("pdf route", PDF % (job, tenant), authed=True)
        d = b.get("data") if isinstance(b, dict) else None
        after = (s, codes_of(b), top_names(d), (b.get("ok") if isinstance(b, dict) else None))
        reads.append("T7 pdf route for the same request after: status %s codes %s data keys %s ok %s; equal to before: %s" % (after + (after == st["pdf_before"],)))
        st["pdf_after"] = after
    except Exception as e:  # noqa: BLE001 -- anything is a STOP; the row is still removed after exp
        stop = "STOP (%s): %s" % (type(e).__name__, str(e)[:300])
        say(stop)
    finally:
        cl.token = None
        if written and exp:
            wait = exp + 5 - time.time()
            if wait > 0:
                say("waiting %ds for exp %s to pass before removal" % (int(wait), base.iso(exp)))
                time.sleep(wait)
        if written:
            try:
                ddb.delete_item(TableName=base.USERS, Key=key, ConditionExpression="attribute_exists(PK)")
                say("viewer users row deleted (attribute_exists)")
            except Exception as e:  # noqa: BLE001
                say("DELETE of the viewer row failed: %s" % str(e)[:160])
        rem, g, c = [], False, False
        deadline = time.time() + 300
        say("removal window: bounded 5 minutes, until %s" % base.iso(deadline))
        while time.time() < deadline:
            c, g = cread() is None, gsi() == 0
            say("removal read: GSI ABSENT=%s ConsistentRead ABSENT=%s" % (g, c))
            if g and c:
                break
            time.sleep(10)
        rem.append(("ABSENT GSI %s" if g else "PRESENT GSI %s") % addr)
        rem.append(("ABSENT CONSISTENT %s" if c else "PRESENT CONSISTENT %s") % addr)
        (outdir / "R31L_READS.txt").write_text("\n".join(reads + ([stop] if stop else [])) + "\n", encoding="utf-8")
        (outdir / "R31L_REMOVAL.txt").write_text("\n".join(rem) + "\n", encoding="utf-8")
        (outdir / "R31L_TRACE.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0 if not stop else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--go", action="store_true")
    ap.add_argument("--cand", action="append", default=[], help="tenant:REQ-... candidate READY report (tried in order)")
    ap.add_argument("--flagdir", default=".")
    ap.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d"))
    ap.add_argument("--out", default=str(HERE))
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.live and args.go and args.cand:
        return live(args)
    ap.error("choose --selftest, or --live --go with at least one --cand")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
