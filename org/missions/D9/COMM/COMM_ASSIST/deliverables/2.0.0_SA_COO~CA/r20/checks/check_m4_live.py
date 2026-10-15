"""CA-l-4 AC2: the NARROWER package (registry files named by the manifest) is LIVE, the mode stays enforce and the key stays narrowed, read from AWS, never from a report.

PASS needs all of:
  1. both functions carry the same CodeSha256, different from the pre-state (PRE, the CA-k-4 package live before this deploy);
  2. the zip the ingress function SERVES hashes to that CodeSha256, its eight contract files are byte-identical (LF) to M4_PIN's, and so is every other file the zip holds
     except the FOREIGN set (legacy_addresses.json, reporting_policies.json: rows other seats merged between the two pins; counted and printed, not graded);
  3. the registry files the zip serves == the manifest infra/aws/lambda/teams-chat-assist/registry_files.txt as M4_PIN holds it == the twelve recorded here, none of the five
     dropped files (catalog_fork_keys, event_rules, key_rulings, name_rulings, root_map) is served, and the zip holds 34 files (39 before);
  4. BOTH environments carry INGRESS_MARK_MODE == "enforce", the same fifteen key NAMES as recorded, and MUSE_ANSWER_PUBKEY (fingerprint as recorded), MAIL_BEARER_SECRET
     and SMS_ORIGINATION unchanged;
  5. the secret teams/global/ingress-mark exists and has a current VERSION (describe-secret; its value is NEVER read), and for each function's execution role
     iam simulate-principal-policy says secretsmanager:GetSecretValue on that secret is allowed;
  6. the SERVED code, imported from the extracted zip: the mark checks, the mention and mail records, AND the CA-k-1 probe (two considered mails one minute apart driven
     through mail_requests.on_mail_messages on a stand-in ctx, invented names, every outside call replaced, no AWS, no network, no text sent) leave state["pending_list"]
     holding both, with distinct seq and tag, and state["pending"] the newer;
  7. the 17 probes of check_l4_equiv.py (the S3 addresses for five chats and the mail parties) run against the SERVED zip equal EXPECTED_17, the output recorded from the
     package that was live before this deploy.
Prints one line per check and RESULT: PASS|FAIL. Read-only: get/describe/simulate calls and one download. Needs env M4_PIN.
Finds the repository from the current directory's git toplevel, never from this file's location.

PRE (the BEFORE hash) was read read-only on 2026-10-15 ~08:1xZ with the .tools/aws shim:
  .tools/aws lambda get-function-configuration --function-name teams-global-chat-assist-handler-lambda --query CodeSha256   (and -ingress-lambda)
  both read nQlJW0j/a2nE1om0ZbXm9CTMxAVDXwUQNju62S4xa9k= (CodeSize 320236; LastModified 2026-10-15T05:56:32Z handler, 05:56:24Z ingress; INGRESS_MARK_MODE enforce);
  this is the CA-k-4 package, built at 93a3f55d25.
EXPECTED_17 was recorded the same time: the zip of .tools/aws lambda get-function --function-name teams-global-chat-assist-ingress-lambda --query Code.Location
(downloaded, extracted to a scratch folder, 39 files, sha256 base64 = PRE), then
  cd <that folder> && python -c <PROBE of check_l4_equiv.py> <that folder>      (the 17-key JSON line, printed with sort_keys)
"""
import base64
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

PIN = os.environ.get("M4_PIN", "")
PRE = "nQlJW0j/a2nE1om0ZbXm9CTMxAVDXwUQNju62S4xa9k="
FUNCS = ["teams-global-chat-assist-handler-lambda", "teams-global-chat-assist-ingress-lambda"]
FILES = ["data/transcripts/scripts/teams_chat/tenant.py", "data/transcripts/scripts/teams_chat/ingress_mark.py", "data/transcripts/scripts/teams_chat/NAMES.json",
         "data/transcripts/scripts/teams_chat/assist.py", "data/transcripts/scripts/teams_chat/mail_requests.py", "data/transcripts/scripts/teams_chat/muse_verify.py",
         "data/transcripts/scripts/teams_chat/channel_mentions.py", "data/transcripts/scripts/teams_chat/folder_records.py"]
ROOT_FILES = {"handlers.py": "infra/aws/lambda/teams-chat-assist/handlers.py", "ldo.py": "infra/aws/terraform/modules/ldo/runtime/ldo.py"}
REG = "infra/logic/registry/"
MANIFEST = "infra/aws/lambda/teams-chat-assist/registry_files.txt"
DROPPED = sorted(["catalog_fork_keys.json", "event_rules.json", "key_rulings.json", "name_rulings.json", "root_map.json"])
FOREIGN = sorted([REG + "legacy_addresses.json", REG + "reporting_policies.json"])
TWELVE = sorted(["exemptions.json", "feeds.json", "firm_pages.json", "legacy_addresses.json", "mail_parties.json", "platinum_destinations.json",
                 "remediations.json", "reporting_policies.json", "resources.json", "scopes.json", "systems.json", "tiers.json"])
FILE_COUNT = 34
ENV_KEYS = sorted(["GATEWAY_BASE", "IGNORE_NAMES", "INGRESS_MARK_MODE", "LDO_ALARM_PREFIX", "LDO_ALARM_ROLE_ARN", "LDO_ARCHIVE_BUCKET", "LDO_DEDUP_DAYS", "LDO_ID",
                   "LDO_KMS_KEY_ARN", "LDO_MAILBOX_ARN", "LDO_MAILBOX_URL", "LDO_TABLE", "MAIL_BEARER_SECRET", "MUSE_ANSWER_PUBKEY", "SMS_ORIGINATION"])
FP = "SHA256:oq0WqfmN1I15uxqNGuoN64t+SubEBfmPINUyLgqFBRQ"
MAIL_ARN = "arn:aws:secretsmanager:us-east-1:313476888478:secret:gateway/mail/commassist-bearer-cPYbR3"
SMS = "arn:aws:sms-voice:us-east-1:313476888478:phone-number/phone-0e98f7739a16415c83d951336a7da12a"
SECRET = "teams/global/ingress-mark"

# The 17-probe output of the package live before this deploy (recorded 2026-10-15 ~08:1xZ; see the header for the command).
EXPECTED_17 = {
    "BUCKET": "opal-data-transcripts",
    "bronze_0": "teams/transcripts/bronze/chat_messages/chat=19-abc-unq.gbl.spaces/20261013T201351Z_m0.json",
    "bronze_1": "teams/transcripts/bronze/chat_messages/chat=19-meeting_XYZ-thread.v2/20261013T201351Z_m1.json",
    "bronze_2": "teams/transcripts/bronze/chat_messages/chat=eod-2026-10-13/20261013T201351Z_m2.json",
    "bronze_3": "teams/transcripts/bronze/chat_messages/chat=job-J290/20261013T201351Z_m3.json",
    "bronze_4": "teams/transcripts/bronze/chat_messages/chat=mail-owner/20261013T201351Z_m4.json",
    "firms": '{"49financial": ["49financial.com"], "cottonwood": ["cottonwoodmail.com"], "inflection": ["inflectionwealth.com"], "opal": ["opalinvest.com"]}',
    "silver_0": "teams/transcripts/silver/chat_threads/chat=19-abc-unq.gbl.spaces/context.md",
    "silver_1": "teams/transcripts/silver/chat_threads/chat=19-meeting_XYZ-thread.v2/context.md",
    "silver_2": "teams/transcripts/silver/chat_threads/chat=eod-2026-10-13/context.md",
    "silver_3": "teams/transcripts/silver/chat_threads/chat=job-J290/context.md",
    "silver_4": "teams/transcripts/silver/chat_threads/chat=mail-owner/context.md",
    "state_0": "teams/transcripts/state/chat_assist/global/x_0.json",
    "state_1": "teams/transcripts/state/chat_assist/global/x_1.json",
    "state_2": "teams/transcripts/state/chat_assist/global/x_2.json",
    "state_3": "teams/transcripts/state/chat_assist/global/x_3.json",
    "state_4": "teams/transcripts/state/chat_assist/global/x_4.json",
}

# The probe battery of check_l4_equiv.py, unchanged.
PROBE17 = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from data.transcripts.scripts.teams_chat import assist as a, mail_requests as mr
out = {"BUCKET": a.BUCKET}
try:
    out["firms"] = json.dumps({k: sorted(v) if isinstance(v, (list, set, tuple)) else v for k, v in mr.firm_domains().items()}, sort_keys=True, default=str)
except Exception as exc:
    out["firms"] = "ERR %s" % type(exc).__name__
for i, cid in enumerate(["19:abc@unq.gbl.spaces", "19:meeting_XYZ@thread.v2", "eod:2026-10-13", "job:J290", "mail:owner"]):
    out["state_%d" % i] = a.state_key("x_%d.json" % i)
    out["silver_%d" % i] = a.silver_key(cid, "context.md")
    out["bronze_%d" % i] = a.bronze_key(cid, {"created": "2026-10-13T20:13:51Z", "id": "m%d" % i})
print(json.dumps(out, sort_keys=True))
'''

PROBE = r'''
import contextlib, datetime, io, json, os, re, sys
sys.path.insert(0, sys.argv[1])
from data.transcripts.scripts.teams_chat import assist as a, ingress_mark as im, tenant as t
out = {"name": a.NAMES["secrets"].get("ingress_mark")}
now = datetime.datetime(2026, 10, 14, 4, 0, tzinfo=datetime.timezone.utc)
p = im.stamp("throwaway-secret", "obj", "sms.reply", {"tag": "C1", "action": "send"}, now)
out["roundtrip"] = im.verify("throwaway-secret", "obj", "sms.reply", p, now) == "ok"
q = dict(p, action="drop")
out["tamper"] = im.verify("throwaway-secret", "obj", "sms.reply", q, now) == "bad-mark"
out["max_age_4h"] = getattr(im, "MAX_AGE_S", None) == 4 * 3600
old = im.stamp("throwaway-secret", "obj", "sms.reply", {"tag": "C1", "action": "send"}, now - datetime.timedelta(hours=3, minutes=59))
out["edge_ok"] = im.verify("throwaway-secret", "obj", "sms.reply", old, now) == "ok"
older = im.stamp("throwaway-secret", "obj", "sms.reply", {"tag": "C1", "action": "send"}, now - datetime.timedelta(hours=4, minutes=1))
out["edge_stale"] = im.verify("throwaway-secret", "obj", "sms.reply", older, now) == "stale-mark"
os.environ.pop("INGRESS_MARK_MODE", None)
out["unset_off"] = t._mark_mode() == "off"
os.environ["INGRESS_MARK_MODE"] = "record"
out["record"] = t._mark_mode() == "record"
os.environ["INGRESS_MARK_MODE"] = "enforce"
out["enforce"] = t._mark_mode() == "enforce"
os.environ["INGRESS_MARK_MODE"] = "enfroce"
try:
    t._mark_mode()
    out["typo_raises"] = False
except ValueError:
    out["typo_raises"] = True
class _C:
    def __init__(self):
        self.state = {"marks_seen": ["legacy", {"mark": "m1", "at": a.iso(now - datetime.timedelta(hours=3))}, {"mark": "m2", "at": a.iso(now - datetime.timedelta(hours=5))}]}

    def now(self):
        return now


try:
    out["held"] = [e["mark"] for e in t._held_marks(_C())] == ["legacy", "m1"]
except Exception:
    out["held"] = False
import copy
from data.transcripts.scripts.teams_chat import channel_mentions as cm, folder_records as fr, mail_requests as mr


class _R:
    def __init__(self):
        self.state = {}

    def now(self):
        return now


try:
    sn = fr.snippet("<p>See https://x.example/q?k=1 AKIAIOSFODNN7EXAMPLE pat@example-fund.test " + "w " * 100 + "</p>")
    out["snippet_clean"] = 0 < len(sn) <= 120 and "http" not in sn and "@" not in sn and "AKIA" not in sn and "<" not in sn
    ctx = _R()
    pl = {"team": {"id": "t1", "display_name": "T"}, "channel": {"id": "c1", "display_name": "C"},
          "message": {"id": "m1", "created": "2026-10-14T13:00:00Z", "from_name": "F", "body_html": "<p>hello</p>"}}
    cm._keep_mention(ctx, pl, pl["message"])
    cm._keep_mention(ctx, pl, pl["message"])
    row = (ctx.state.get("mentions") or [{}])[0]
    out["mention_record"] = len(ctx.state.get("mentions") or []) == 1 and set(row) == {"id", "team", "channel", "from", "snippet", "mentioned_at", "seen_at"}
    ctx2 = _R()
    mr._log_mail(ctx2, {"seq": 1, "tag": "M001", "mail": {"firm": "f"}}, "Pat", "Pat@Example-Fund.Test", "Subject AKIAIOSFODNN7EXAMPLE")
    r2 = (ctx2.state.get("mail_log") or [{}])[0]
    out["mail_record"] = set(r2) == {"seq", "tag", "considered_at", "from", "domain", "firm", "subject"} and r2["domain"] == "example-fund.test" and "AKIA" not in r2["subject"] and "@" not in json.dumps(r2)
except Exception:
    out["snippet_clean"] = out["mention_record"] = out["mail_record"] = False
_ = copy

# CA-k-4: two considered mails one minute apart on the one mail object keep BOTH drafts (stand-in ctx, invented names; every outside call replaced, nothing sent).
UTC = datetime.timezone.utc
T0 = datetime.datetime(2026, 10, 14, 20, 0, tzinfo=UTC)
NOT_WORK = json.dumps({"is_work": False, "asked": "", "recommend": "reply", "why": ""})


class _K:
    def __init__(self, payload, state, at, once_store):
        self.object_id, self.kind, self.payload, self.state = "probe:k4-mail", "mail.messages", payload, state
        self.event_id, self.envelope = "evt-k4-%s" % at.isoformat(), {"sent_at": at.isoformat()}
        self._at, self.once_store = at, once_store

    def now(self):
        return self._at

    def once(self, key, fn):
        if key not in self.once_store:
            self.once_store[key] = json.loads(json.dumps(fn()))
        return self.once_store[key]

    def index(self, ns, key):
        pass

    def send(self, object_id, kind, payload=None):
        pass

    def set_alarm(self, key, at, kind, payload=None):
        pass

    def cancel_alarm(self, key):
        pass

    def expire_in(self, days):
        pass


def _mail(mid, subject):
    return {"message_id": mid, "subject": subject,
            "from": {"emailAddress": {"name": "Pat Invented", "address": "pat@example-fund.test"}},
            "body": {"contentType": "text", "content": "Hi Andrew, a note about %s from the invented-firm accounts." % subject}}


try:
    texts = []

    def _kimi(system, user, send=None):
        if system.startswith(a.WORK_SYSTEM):
            return NOT_WORK
        subject = (re.search(r"Subject: (.*)", user) or re.search(r"(.*)", "x")).group(1).strip()
        return "Reply for %s" % subject

    gw = type("GW", (), {})()
    a.kimi = _kimi
    a.send_sms = lambda body, tag: texts.append((tag, body)) or ["m%d" % len(texts)]
    a.me = lambda: {"id": "u-andrew", "display_name": "Andrew Berman"}
    a.get_text = lambda key, default="": ""
    a.assistant_on = lambda: True
    a.voice_block = lambda kind: ""
    a.gateway = lambda: gw
    mr.firm_domains = lambda registry=None: {"invented-firm": ["example-fund.test"]}
    mr._party_rows = lambda registry=None: []
    mr._lookup = lambda ns, key: None
    st, once = {}, {}
    with contextlib.redirect_stdout(io.StringIO()):
        r_a = mr.on_mail_messages(_K({"messages": [_mail("probe-k4-alpha", "alpha")]}, st, T0, once))
        first = json.dumps(dict(st.get("pending") or {}), sort_keys=True)
        r_b = mr.on_mail_messages(_K({"messages": [_mail("probe-k4-beta", "beta")]}, st, T0 + datetime.timedelta(seconds=60), once))
    lst = st.get("pending_list") or []
    newest = st.get("pending") or {}
    out["pending_list"] = (r_a == "texted" and r_b == "texted" and len(lst) == 2 and len(texts) == 2
                           and lst[0].get("seq") != lst[1].get("seq") and lst[0].get("tag") != lst[1].get("tag")
                           and [(e.get("mail") or {}).get("id") for e in lst] == ["probe-k4-alpha", "probe-k4-beta"]
                           and json.dumps(dict(lst[0]), sort_keys=True) == first
                           and newest.get("seq") == lst[1].get("seq") and newest.get("tag") == lst[1].get("tag")
                           and (newest.get("mail") or {}).get("id") == "probe-k4-beta")
except Exception as exc:
    out["pending_list"] = False
    out["pending_list_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:120])
print(json.dumps(out))
'''


def root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, encoding="utf-8").stdout.strip()


def aws(*args):
    exe = "aws.cmd" if os.name == "nt" else "aws"
    r = subprocess.run([exe, *args, "--output", "json"], capture_output=True, text=True, encoding="utf-8", timeout=90)
    if r.returncode != 0:
        return None, ((r.stderr or "").strip().splitlines() or ["rc=%d" % r.returncode])[-1]
    return json.loads(r.stdout), None


def fingerprint(line):
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "k.pub"
        p.write_text((line or "") + "\n", encoding="ascii")
        out = subprocess.run(["ssh-keygen", "-lf", str(p)], capture_output=True, text=True).stdout
    return (out.split() + ["", ""])[1]


def pin_bytes(path):
    r = subprocess.run(["git", "show", "%s:%s" % (PIN, path)], capture_output=True)
    return r.stdout.replace(b"\r\n", b"\n") if r.returncode == 0 else None


def main():
    os.chdir(root())
    ok = True
    if not PIN:
        print("ERROR: M4_PIN is not set")
        print("RESULT: FAIL")
        return 1
    shas, envs, roles = [], [], []
    for fn in FUNCS:
        cfg, err = aws("lambda", "get-function-configuration", "--function-name", fn)
        shas.append((cfg or {}).get("CodeSha256"))
        envs.append(((cfg or {}).get("Environment") or {}).get("Variables") or {})
        roles.append((cfg or {}).get("Role"))
        print("CHECK %s CodeSha256=%s LastModified=%s %s" % (fn, shas[-1], (cfg or {}).get("LastModified"), err or ""))
    c1 = bool(shas[0]) and shas[0] == shas[1] and shas[0] != PRE
    print("CHECK both functions on one package, not the pre-state: %s" % c1)
    ok &= c1

    doc, err = aws("lambda", "get-function", "--function-name", FUNCS[1])
    url = ((doc or {}).get("Code") or {}).get("Location")
    data = urllib.request.urlopen(url, timeout=60).read() if url else b""
    served = base64.b64encode(hashlib.sha256(data).digest()).decode() if data else None
    c2 = bool(served) and served == shas[1]
    tmp = tempfile.mkdtemp(prefix="comm_r20_m4_")
    zf = zipfile.ZipFile(io.BytesIO(data)) if data else None
    if zf:
        zf.extractall(tmp)
    same = True
    for path in FILES:
        want = pin_bytes(path)
        fp = os.path.join(tmp, *path.split("/"))
        eq = want is not None and os.path.isfile(fp) and open(fp, "rb").read() == want
        print("CHECK served %s == pin %s: %s" % (path, PIN, eq))
        same &= eq
    names = [i.filename for i in zf.infolist() if not i.is_dir()] if zf else []
    foreign_in = [n for n in names if n in FOREIGN]
    foreign_eq = [n for n in foreign_in if zf.read(n) == pin_bytes(n)]
    odd = [n for n in names if n not in FOREIGN and (pin_bytes(ROOT_FILES.get(n, n)) is None or zf.read(n) != pin_bytes(ROOT_FILES.get(n, n)))]
    allsame = bool(names) and not odd
    print("CHECK served zip hash equals CodeSha256: %s (%s bytes); %d contract files equal the pin: %s; all %d zip files but the %d foreign equal the pin: %s %s" % (
        c2, len(data), len(FILES), same, len(names), len(foreign_in), allsame, odd[:4] if odd else ""))
    print("INFO foreign files in the served zip (not graded): %d, of which equal to the pin: %d %s" % (len(foreign_in), len(foreign_eq), foreign_in))
    ok &= c2 and same and allsame

    served_reg = sorted(n[len(REG):] for n in names if n.startswith(REG))
    man_raw = pin_bytes(MANIFEST)
    man = sorted(x.strip() for x in (man_raw or b"").decode("utf-8", "replace").replace("\r", "").split("\n") if x.strip() and not x.strip().startswith("#"))
    stray = [n for n in DROPPED if n in served_reg]
    c3 = man_raw is not None and served_reg == man == TWELVE and not stray and len(names) == FILE_COUNT
    print("CHECK served registry files == manifest at the pin == the twelve (%d served, %d in the manifest), none of the five dropped files served %s, %d zip files (want %d): %s" % (
        len(served_reg), len(man), stray, len(names), FILE_COUNT, c3))
    if served_reg != man:
        print("INFO served-only %s manifest-only %s" % (sorted(set(served_reg) - set(man)), sorted(set(man) - set(served_reg))))
    ok &= c3

    c4 = True
    for fn, env in zip(FUNCS, envs):
        good = (env.get("INGRESS_MARK_MODE") == "enforce" and fingerprint(env.get("MUSE_ANSWER_PUBKEY")) == FP
                and env.get("MAIL_BEARER_SECRET") == MAIL_ARN and env.get("SMS_ORIGINATION") == SMS and sorted(env) == ENV_KEYS)
        print("CHECK %s environment: INGRESS_MARK_MODE=enforce, the 15 key names, muse key fingerprint, mail secret and sms origination as recorded: %s" % (fn, good))
        c4 &= good
    ok &= c4

    sec, err = aws("secretsmanager", "describe-secret", "--secret-id", SECRET)
    arn = (sec or {}).get("ARN")
    stages = [s for v in ((sec or {}).get("VersionIdsToStages") or {}).values() for s in v]
    c5 = bool(arn) and "AWSCURRENT" in stages
    print("CHECK secret %s exists with a current version (value not read): %s %s" % (SECRET, c5, err or ""))
    for fn, role in zip(FUNCS, roles):
        sim, err = aws("iam", "simulate-principal-policy", "--policy-source-arn", role or "none", "--action-names", "secretsmanager:GetSecretValue",
                       "--resource-arns", arn or "none")
        allowed = bool(sim) and all(r.get("EvalDecision") == "allowed" for r in sim.get("EvaluationResults", [])) and bool(sim.get("EvaluationResults"))
        print("CHECK %s role may read the secret (simulate): %s %s" % (fn, allowed, err or ""))
        c5 &= allowed
    ok &= c5

    probe = None
    p17 = None
    if data:
        env = {k: v for k, v in os.environ.items() if k not in ("AWS_PROFILE", "AWS_DEFAULT_PROFILE")}
        env.update(AWS_ACCESS_KEY_ID="probe-none", AWS_SECRET_ACCESS_KEY="probe-none", AWS_EC2_METADATA_DISABLED="true", AWS_DEFAULT_REGION="us-east-1")
        r = subprocess.run([sys.executable, "-c", PROBE, tmp], capture_output=True, text=True, encoding="utf-8", cwd=tmp, timeout=100, env=env)
        try:
            probe = json.loads((r.stdout or "").strip().splitlines()[-1])
        except Exception:  # noqa: BLE001 -- a failed probe reads as a FAIL with its stderr shown
            print("ERROR: probe failed: %s" % (r.stderr or "")[-300:])
        r = subprocess.run([sys.executable, "-c", PROBE17, tmp], capture_output=True, text=True, encoding="utf-8", cwd=tmp, timeout=100, env=env)
        try:
            p17 = json.loads((r.stdout or "").strip().splitlines()[-1])
        except Exception:  # noqa: BLE001 -- a failed probe reads as a FAIL with its stderr shown
            print("ERROR: 17-probe battery failed: %s" % (r.stderr or "")[-300:])
    shutil.rmtree(tmp, ignore_errors=True)
    keys = ("roundtrip", "tamper", "unset_off", "record", "enforce", "typo_raises", "max_age_4h", "edge_ok", "edge_stale", "held", "snippet_clean", "mention_record", "mail_record")
    c6 = bool(probe) and probe.get("name") == SECRET and all(probe.get(k) is True for k in keys)
    print("CHECK served code: secret name from the NAMES row, mark round trip, tamper refused, modes parse, typo raises, mention and mail records clean: %s" % c6)
    c7 = bool(probe) and probe.get("pending_list") is True
    print("CHECK served code: two considered mails one minute apart keep both drafts in state[pending_list] (distinct seq and tag, pending the newer): %s %s" % (
        c7, (probe or {}).get("pending_list_error", "")))
    c8 = bool(p17) and len(p17) == 17 and p17 == EXPECTED_17
    print("CHECK served code: the 17 probes (S3 addresses and mail parties) equal the output recorded from the previous package: %s %s" % (
        c8, [k for k in sorted(set(p17 or {}) | set(EXPECTED_17)) if (p17 or {}).get(k) != EXPECTED_17.get(k)][:4]))
    print("PROBE %s" % probe)
    ok &= c6 and c7 and c8

    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
