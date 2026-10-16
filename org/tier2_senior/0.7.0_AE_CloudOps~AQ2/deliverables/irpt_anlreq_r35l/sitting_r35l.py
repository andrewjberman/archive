"""IRPT_ANLREQ TO-APPLY-R35L reads (0.7.0_AE_CloudOps~AQ2): R0(b), R0(c) before and G3, G4 after the irpt-status release, as ONE synthetic
internal viewer, one RS256 token held in this process only, never written, printed or logged.

  --selftest        the comparison helpers on synthetic data (no AWS, no network)
  --live --go       mint the viewer, take the BEFORE reads, wait for <flagdir>/go_after (or abort), take the AFTER reads, remove the row after exp

BEFORE: the credential-less refusal envelope of the route GET .../analysis/{jobId}/sections (status, body sha256), and ONE retained READY report
read as the viewer WITHOUT a ticket_id (status, body sha256, the top-level key set). AFTER: the same two reads; the report read must return the same
status and a BYTE-IDENTICAL body (sha256 equal). Kept: status, code names, sha256, key names. No body, no value from a body and no address is
printed or written. Reuses ../irpt_anlreq_r31/sitting_r31l.py (Client, helpers) and ../irpt_anlreq_r28/sitting_r28.py (constants).
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "irpt_anlreq_r31"))
import sitting_r31l as r31  # noqa: E402

base = r31.base
BEFORE_SHA = "OOez8YSmE22btOqx28/fJdK9sxGNDGAumU5pMJ++6Ss="
AFTER_SHA = "+TcZDWmwE7uv3sUwos2+jn1lbKyQikK+13nNBzD6q4A="
SECTIONS = r31.SECTIONS


def byte_identical(raw_before, raw_after):
    return r31.sha(raw_before) == r31.sha(raw_after)


def selftest():
    assert byte_identical('{"a":1}', '{"a":1}') and not byte_identical('{"a":1}', '{"a":2}')
    assert byte_identical("", "") and not byte_identical("x", "x ")
    assert r31.top_names({"b": 1, "a": 2}) == ["a", "b"] and r31.top_names([1]) is None
    assert r31.codes_of({"ok": False, "status": {"public_reason_code": "INVALID_INPUT"}}) == ["INVALID_INPUT"]
    print("SELFTEST OK helpers: byte_identical (equal, differ, empty, one trailing byte), top_names, codes_of")
    return 0


def live(args):
    import boto3
    import jwt as pyjwt

    outdir, flagdir = Path(args.out), Path(args.flagdir)
    addr = "irpt-r35l-iv-%s@opal.invalid" % args.date
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

    cl = r31.Client(say)
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
                "name": {"S": "IRPT_ANLREQ R35L synthetic internal viewer"}, "role": {"S": "user"}, "tier": {"S": "internal"},
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
                  "userType": "test-filer", "name": "IRPT_ANLREQ R35L synthetic internal viewer", "iat": iat, "exp": iat + base.LIFE}
        cl.token = pyjwt.encode(claims, pem, algorithm="RS256")
        exp = claims["exp"]
        del pem
        say("token minted (held in memory only) iat=%s exp=%s" % (base.iso(iat), base.iso(exp)))

        # ---- BEFORE: R0(b) the credential-less refusal envelope, R0(c) one READY report read without a ticket_id
        s, b, raw = cl.get("sections", SECTIONS % ("REQ-" + "0" * 24, "49financial"), authed=False)
        st["cred_before"] = (s, r31.sha(raw))
        chosen = None
        for cand in args.cand:
            tenant, job = cand.split(":", 1)
            s, b, raw = cl.get("sections %s" % job, SECTIONS % (job, tenant), authed=True)
            d = b.get("data") if isinstance(b, dict) else None
            if s == 200 and isinstance(b, dict) and b.get("ok") is not False and isinstance(d, dict):
                chosen = (tenant, job)
                st["before"] = {"status": s, "sha": r31.sha(raw), "raw_sha": r31.sha(raw), "env_keys": r31.top_names(b), "data_keys": r31.top_names(d)}
                break
            reads.append("BEFORE candidate %s: status %s codes %s (not used)" % (job, s, r31.codes_of(b)))
        if not chosen:
            raise RuntimeError("no candidate report read as 200 for the viewer before the change: R0(c) cannot be taken")
        tenant, job = chosen
        reads.append("R0B credential-less sections read: status %s body_sha256 %s" % st["cred_before"])
        reads.append("R0C READY report job %s tenant %s read WITHOUT ticket_id: status 200 body_sha256 %s; top-level key set %s; data key set %s"
                     % (job, tenant, st["before"]["sha"], st["before"]["env_keys"], st["before"]["data_keys"]))
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

        # ---- AFTER: G1 (the signal's own check), G3 the credential-less envelope, G4 the READY read byte-identical
        got = lam.get_function_configuration(FunctionName="irpt-status")["CodeSha256"]
        say("irpt-status CodeSha256 at the after-reads: %s" % ("EQUAL to the expected released value" if got == AFTER_SHA else "DIFFERENT"))
        s, b, raw = cl.get("sections", SECTIONS % ("REQ-" + "0" * 24, "49financial"), authed=False)
        st["cred_after"] = (s, r31.sha(raw))
        reads.append("G3 credential-less sections read after: status %s body_sha256 %s; equal to R0B (status and body sha256): %s" % (s, r31.sha(raw), st["cred_after"] == st["cred_before"]))
        s, b, raw = cl.get("sections %s (no ticket_id)" % job, SECTIONS % (job, tenant), authed=True)
        same = s == st["before"]["status"] and r31.sha(raw) == st["before"]["sha"]
        st["g4"] = (s, r31.sha(raw), same)
        reads.append("G4 READY report read WITHOUT ticket_id after: status %s body_sha256 %s; top-level key set %s; same status as R0C: %s; BYTE-IDENTICAL body (sha256 equal): %s"
                     % (s, r31.sha(raw), r31.top_names(b), s == st["before"]["status"], r31.sha(raw) == st["before"]["sha"]))
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
        (outdir / "R35L_READS.txt").write_text("\n".join(reads + ([stop] if stop else [])) + "\n", encoding="utf-8")
        (outdir / "R35L_REMOVAL.txt").write_text("\n".join(rem) + "\n", encoding="utf-8")
        (outdir / "R35L_TRACE.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
