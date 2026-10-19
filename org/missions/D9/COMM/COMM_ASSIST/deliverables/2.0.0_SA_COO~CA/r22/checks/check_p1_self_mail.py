"""CA-p-1 AC1: the mail handler never makes a draft for mail Andrew himself sent.

The defect (2026-10-19, Andrew approved the rule; muse reported drafts M741 and M044): a considered mail is one whose sender's
domain is one of the five parties' and whose body names "Andrew". Andrew's own sent mail (sender = his mailbox, domain
opalinvest.com, body naming Andrew in a reply chain) passes both tests, so the handler drafted a reply to Andrew's own mail and
texted it to him. The fix refuses a message whose sender address is Andrew's own (a.me()["mail"]) BEFORE anything else runs.

PASS needs all six arms against data/transcripts/scripts/teams_chat/mail_requests.py as the repository holds it:
  1. self_mail_refused   a mail from Andrew's address that names Andrew: result "none-to-text", no text, no work-request call, no
                         draft call, no pending, counts["from_andrew"] == 1;
  2. case_and_name       the same with the address in other letter cases and a different display name: refused;
  3. colleague_control   the same body from a colleague at the same domain: ONE text with a draft (the difference control);
  4. mixed_batch         one batch of [his mail, a colleague's mail]: exactly one text, for the colleague;
  5. reasons_and_api     "from_andrew" is in REASONS; considered(msg, domains, mine) returns (False, "from_andrew") for his mail and
                         the two-argument call considered(msg, domains) still works;
  6. fail_closed         when Andrew's mailbox is unknown (a.me raises, or has no mail), on_mail_messages RAISES and nothing is
                         drafted or texted (the event retries; it never drafts on a mailbox it cannot tell from his).
Prints one line per arm and P1-SELFMAIL ok=True|False arms=<passed> of 6.
Finds the repository from the current directory's git toplevel, never from this file's location; the seam P1_ROOT points it at
another copy (a scratch reference). No network, no AWS: the model, the texts, the gateway and a.me are injected.
"""
import contextlib
import datetime
import io
import json
import os
import subprocess
import sys

ROOT = os.environ.get("P1_ROOT") or subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                                                   text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "infra", "aws", "terraform", "modules", "ldo", "runtime"))
from data.transcripts.scripts.teams_chat import assist as a  # noqa: E402
from data.transcripts.scripts.teams_chat import mail_requests as mr  # noqa: E402

NOW = datetime.datetime(2026, 10, 19, 15, 0, tzinfo=a.UTC)
HIS = "boss.invented@house-one.test"         # invented: stands in for Andrew's mailbox
FAKE = {"invented-house": ["house-one.test"]}
INTERNAL_ROW = {"party": "invented-house", "role": "internal"}
DRAFT = "Thanks, I will look at it and come back to you this week."
NOT_WORK = json.dumps({"is_work": False, "asked": "", "recommend": "reply", "why": ""})
BODY = "<p>Andrew, thanks for yesterday's call.</p>"


class Ctx:
    def __init__(self, messages):
        self.object_id, self.kind, self.payload = "mail:owner", "mail.messages", {"messages": messages}
        self.event_id, self.state, self.once_store = "evt-mail", {}, {}

    def now(self):
        return NOW

    def once(self, key, fn):
        if key not in self.once_store:
            self.once_store[key] = json.loads(json.dumps(fn()))
        return self.once_store[key]

    def index(self, ns, key):
        pass

    def send(self, *args, **kwargs):
        pass


class World:
    def __init__(self, me=None):
        self.texts, self.work_calls, self.draft_calls = [], 0, 0
        a.kimi = self._kimi
        a.send_sms = lambda body, tag: self.texts.append((tag, body)) or ["m%d" % len(self.texts)]
        a.voice_block = lambda kind: "VOICEBLOCK-" + kind if kind == "mail_reply" else ""
        a.me = me if me is not None else (lambda: {"id": "u-me", "display_name": "Boss Invented", "mail": HIS})
        mr.firm_domains = lambda registry=None: dict(FAKE)
        mr._party_rows = lambda registry=None: [dict(INTERNAL_ROW)]
        mr._lookup = lambda ns, key: None

    def _kimi(self, system, user, send=None):
        if system.startswith(a.WORK_SYSTEM):
            self.work_calls += 1
            return NOT_WORK
        assert system.startswith(mr.MAIL_DRAFT_SYSTEM), "unexpected model call"
        self.draft_calls += 1
        return DRAFT


def mail(addr, name="Somebody Invented", mid="AAMk-invented-1"):
    return {"message_id": mid, "subject": "Re: pipelines", "from": {"emailAddress": {"name": name, "address": addr}},
            "body": {"contentType": "html", "content": BODY}}


def run(world, *messages):
    ctx = Ctx(list(messages))
    with contextlib.redirect_stdout(io.StringIO()):
        result = mr.on_mail_messages(ctx)
    return ctx, result


def self_mail_refused():
    w = World()
    ctx, result = run(w, mail(HIS, "Boss Invented"))
    assert result == "none-to-text", result
    assert not w.texts and w.work_calls == 0 and w.draft_calls == 0, (w.texts, w.work_calls, w.draft_calls)
    assert not ctx.state.get("pending") and not ctx.state.get("pending_list"), ctx.state.get("pending")
    assert ctx.state["counts"].get("from_andrew") == 1, ctx.state["counts"]


def case_and_name():
    w = World()
    ctx, result = run(w, mail(HIS.upper(), "Someone Else Entirely"), mail(" " + HIS.title() + " ", "B", mid="AAMk-invented-2"))
    assert result == "none-to-text" and not w.texts and w.draft_calls == 0, (result, w.texts)
    assert ctx.state["counts"].get("from_andrew") == 2, ctx.state["counts"]


def colleague_control():
    w = World()
    ctx, result = run(w, mail("pat.invented@house-one.test", "Pat Invented"))
    assert result == "texted" and len(w.texts) == 1 and w.draft_calls == 1, (result, len(w.texts), w.draft_calls)
    assert ctx.state["pending"]["draft"] == a.sms_free(DRAFT)


def mixed_batch():
    w = World()
    ctx, result = run(w, mail(HIS, "Boss Invented"), mail("pat.invented@house-one.test", "Pat Invented", mid="AAMk-invented-3"))
    assert result == "texted" and len(w.texts) == 1, (result, len(w.texts))
    rows = ctx.state["pending_list"]
    assert len(rows) == 1 and rows[0]["mail"]["sender"] == "Pat Invented", rows


def reasons_and_api():
    assert "from_andrew" in mr.REASONS, mr.REASONS
    msg = mail(HIS, "Boss Invented")
    assert mr.considered(msg, FAKE, {HIS}) == (False, "from_andrew"), mr.considered(msg, FAKE, {HIS})
    assert mr.considered(mail("pat.invented@house-one.test"), FAKE, {HIS}) == (True, "ok")
    assert mr.considered(mail("pat.invented@house-one.test"), FAKE) == (True, "ok")


def fail_closed():
    def broken():
        raise RuntimeError("me-unavailable")
    for me in (broken, lambda: {"id": "u-me", "display_name": "Boss Invented"}, lambda: {"id": "u-me", "mail": ""}):
        w = World(me=me)
        raised = False
        try:
            run(w, mail("pat.invented@house-one.test", "Pat Invented"))
        except Exception:  # noqa: BLE001 -- any raise is the fail-closed outcome
            raised = True
        assert raised and not w.texts and w.draft_calls == 0, (raised, w.texts, w.draft_calls)


ARMS = (self_mail_refused, case_and_name, colleague_control, mixed_batch, reasons_and_api, fail_closed)


def main():
    passed = 0
    for arm in ARMS:
        try:
            arm()
            ok = True
        except BaseException as exc:  # noqa: BLE001 -- a failed arm is reported, not raised
            ok = False
            print("  %s: %s %s" % (arm.__name__, type(exc).__name__, str(exc)[:160]))
        print("ARM %s ok=%s" % (arm.__name__, ok))
        passed += 1 if ok else 0
    print("P1-SELFMAIL ok=%s arms=%d of %d" % (passed == len(ARMS), passed, len(ARMS)))
    return 0 if passed == len(ARMS) else 1


if __name__ == "__main__":
    sys.exit(main())
