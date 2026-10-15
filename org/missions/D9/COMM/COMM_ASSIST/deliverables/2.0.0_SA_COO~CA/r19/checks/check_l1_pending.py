"""CA-k-1: the mail object keeps a LIST of open mail drafts, keyed by seq; a newer considered mail ADDS to it and never overwrites.

Prints one line per failed arm (`FAIL <arm>: <reason>`) and a last line:  L1-PENDING ok=<True|False> arms=<passed> of <total>
Run from the root of the checkout under test, by relative path:  python "org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/r19/checks/check_l1_pending.py"
It imports repo code from the CURRENT WORKING DIRECTORY's checkout (git toplevel of cwd), never from this file's own location.

Contract (fixed by the issuer; the CTO's ruling 2 in ROUND_ANALYSIS.round18.md):
  ctx.state["pending"]       stays and ALWAYS holds the NEWEST open mail draft (None when none is open); newest = the one texted last (a redraft re-texts its entry, so it becomes the newest).
  ctx.state["pending_list"]  NEW: every open mail draft on the mail object, ordered by texted_at (oldest first), each the same dict shape as a pending (own seq, tag, version,
                             draft, ...). mail_requests.on_mail_messages APPENDS each considered mail; on every write entries whose texted_at is more
                             than 7 days before ctx.now() are dropped and only the newest 20 kept (folder_records.prune). Created lazily; an object
                             with only a legacy `pending` is read as a one-entry list. A new mail's tag never repeats the tag of an entry still open.
  Replies (tenant.on_sms_reply, kind mail): the entry is the one whose tag equals the payload tag (no tag: the newest); approve (1), drop (0), notes
                             (redraft) and #dev act on THAT entry only; the stale check (unseen) is per entry; afterwards `pending` is the newest
                             remaining entry or None. An unknown tag changes nothing.
  Reader (muse_reader/refresh.py read_drafts): ONE row per open mail draft (pending_list; the legacy pending when there is no list), each with its own seq.
No AWS, no network: the model, the texts, the gateway and the table scan are stand-ins; names are invented.
"""
import contextlib
import copy
import datetime
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys

CWD = os.getcwd()
try:
    ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=CWD, capture_output=True, text=True, check=True).stdout.strip() or CWD
except Exception:  # noqa: BLE001 -- not a git checkout: the working directory is the root
    ROOT = CWD
ROOT = os.path.normpath(ROOT)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "infra", "aws", "terraform", "modules", "ldo", "runtime"))
from data.transcripts.scripts.teams_chat import assist as a  # noqa: E402
from data.transcripts.scripts.teams_chat import mail_requests as mr  # noqa: E402
from data.transcripts.scripts.teams_chat import tenant as t  # noqa: E402

UTC = datetime.timezone.utc
D = datetime.timedelta
T0 = datetime.datetime(2026, 10, 14, 20, 0, tzinfo=UTC)
FAKE = {"invented-firm": ["example-fund.test"]}
NOT_WORK_JSON = json.dumps({"is_work": False, "asked": "", "recommend": "reply", "why": ""})
OBJ = "mail:owner"
ME = {"id": "u-andrew", "display_name": "Andrew Berman"}


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class Ctx:
    def __init__(self, kind, payload, state, now, once_store=None):
        self.object_id, self.kind, self.payload = OBJ, kind, payload
        self.event_id = "evt-%s-%s" % (kind, iso(now))
        self.envelope = {"sent_at": iso(now)}
        self.state = state
        self._now = now
        self.once_store = once_store if once_store is not None else {}
        self.indexed, self.sent_events = [], []

    def now(self):
        return self._now

    def once(self, key, fn):
        if key not in self.once_store:
            self.once_store[key] = json.loads(json.dumps(fn()))
        return self.once_store[key]

    def index(self, ns, key):
        self.indexed.append((ns, key))

    def send(self, object_id, kind, payload=None):
        self.sent_events.append((object_id, kind, payload or {}))

    def set_alarm(self, key, at, kind, payload=None):
        pass

    def cancel_alarm(self, key):
        pass

    def expire_in(self, days):
        pass


class World:
    """Every outside call replaced and counted. The mail draft is 'Reply for <subject>' (or 'Redo for <subject>' with notes)."""

    def __init__(self):
        self.texts = []
        a.kimi = self._kimi
        a.send_sms = lambda body, tag: self.texts.append((tag, body)) or ["m%d" % len(self.texts)]
        a.me = lambda: ME
        a.get_text = lambda key, default="": ""
        a.assistant_on = lambda: True
        a.voice_block = lambda kind: ""
        gw = type("GW", (), {})()
        a.gateway = lambda: gw
        mr.firm_domains = lambda registry=None: dict(FAKE)
        mr._party_rows = lambda registry=None: []
        mr._lookup = lambda ns, key: None
        t.ldo.lookup = lambda ns, key: None
        t.ldo.send = lambda oid, kind, payload=None, event_id=None: None

    def _kimi(self, system, user, send=None):
        if system.startswith(a.WORK_SYSTEM):
            return NOT_WORK_JSON
        subject = (re.search(r"Subject: (.*)", user) or re.search(r"(.*)", "x")).group(1).strip()
        if system.startswith(mr.MAIL_DRAFT_SYSTEM):
            return ("Redo for %s" if "Andrew's notes on it" in user else "Reply for %s") % subject
        return "Sounds good"


def mail_message(mid, subject):
    return {"message_id": mid, "subject": subject,
            "from": {"emailAddress": {"name": "Pat Invented", "address": "pat@example-fund.test"}},
            "body": {"contentType": "text", "content": "Hi Andrew, a note about %s from the invented-firm accounts." % subject}}


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


def ingest(state, message, now):
    ctx = Ctx("mail.messages", {"messages": [message]}, state, now)
    return quiet(mr.on_mail_messages, ctx)


def reply(state, tag, action, notes="", version=None, at=None):
    payload = {"tag": tag, "action": action, "notes": notes}
    if version is not None:
        payload["version"] = version
    ctx = Ctx("sms.reply", payload, state, at or (T0 + D(minutes=10)))
    return ctx, quiet(t.on_sms_reply, ctx)


def snap(x):
    return json.dumps(x, sort_keys=True)


def plist(state):
    return list(state.get("pending_list") or [])


def two_mails(strict=True):
    """Two considered mails one minute apart on the one mail object: (world, state, snapshot of the first entry as texted)."""
    w = World()
    state = {}
    assert ingest(state, mail_message("AAMk-alpha", "alpha"), T0) == "texted"
    first = json.loads(snap(state["pending"]))
    assert ingest(state, mail_message("AAMk-beta", "beta"), T0 + D(seconds=60)) == "texted"
    if strict:
        assert len(plist(state)) == 2, "pending_list holds %d entries after two considered mails, want 2" % len(plist(state))
    return w, state, first


def tags(state):
    return [e["tag"] for e in plist(state)]


# ---------------------------------------------------------------------------------------------------------------
def arm_two_mails_both_kept():
    w, st, first = two_mails()
    pl = plist(st)
    assert len(pl) == 2, "pending_list holds %d entries after two considered mails, want 2" % len(pl)
    assert pl[0]["seq"] != pl[1]["seq"] and pl[0]["tag"] != pl[1]["tag"], (pl[0]["seq"], pl[1]["seq"], pl[0]["tag"], pl[1]["tag"])
    assert [e["mail"]["id"] for e in pl] == ["AAMk-alpha", "AAMk-beta"] and all(e["kind"] == "mail" for e in pl)
    assert pl[0]["draft"] == "Reply for alpha" and pl[1]["draft"] == "Reply for beta", [e["draft"] for e in pl]
    assert snap(pl[0]) == snap(first), "the older entry changed when the newer mail arrived"
    assert snap(st["pending"]) == snap(pl[1]), "pending is not the newest entry"
    assert len(w.texts) == 2


def arm_approve_older_leaves_newer():
    w, st, _ = two_mails()
    ta, tb = tags(st)
    newer = json.loads(snap(plist(st)[1]))
    _, res = reply(st, ta, "send")
    assert res == "mail-approved", res
    assert w.texts[-1][1] == "#%s approved. Final draft, to paste into your reply in Outlook (nothing is sent for you):\nReply for alpha" % ta, w.texts[-1][1]
    assert [snap(e) for e in plist(st)] == [snap(newer)], "the newer entry did not stay open and unchanged: %s" % tags(st)
    assert snap(st["pending"]) == snap(newer)


def arm_drop_newer_leaves_older():
    w, st, first = two_mails()
    ta, tb = tags(st)
    _, res = reply(st, tb, "drop")
    assert res == "dropped" and w.texts[-1][1] == "#%s dropped." % tb, (res, w.texts[-1][1])
    assert [snap(e) for e in plist(st)] == [snap(first)], "the older entry did not stay open and unchanged"
    assert st["pending"] is not None and snap(st["pending"]) == snap(first), "pending is not the older entry once the newer is dropped"


def arm_redraft_older_only():
    w, st, first = two_mails()
    ta, tb = tags(st)
    newer = json.loads(snap(plist(st)[1]))
    _, res = reply(st, ta, "edit", "make it shorter")
    assert res == "redrafted", res
    pl = plist(st)
    by_tag = {e["tag"]: e for e in pl}
    assert sorted(by_tag) == sorted([ta, tb]) and len(pl) == 2, [e["tag"] for e in pl]
    assert by_tag[ta]["version"] == 2 and by_tag[ta]["draft"] == "Redo for alpha" and by_tag[ta]["seq"] == first["seq"], by_tag[ta]
    assert snap(by_tag[tb]) == snap(newer), "the other entry changed when the older was redrafted"
    # the list is ordered by when each was last texted, and pending is the one texted last: the redraft he has just read
    assert [e["tag"] for e in pl] == [tb, ta] and snap(st["pending"]) == snap(by_tag[ta]), "pending is not the most recently texted entry"
    assert w.texts[-1][0] == ta and "Draft: Redo for alpha" in w.texts[-1][1]
    _, res = reply(st, None, "send", at=T0 + D(hours=2))              # an untagged 1 answers the text he has just read
    assert res == "mail-approved" and w.texts[-1][1].startswith("#%s approved." % ta), (res, w.texts[-1][1][:60])
    assert [e["tag"] for e in plist(st)] == [tb]


def arm_dev_one_removes_only_it():
    w, st, first = two_mails()
    ta, tb = tags(st)
    newer = json.loads(snap(plist(st)[1]))
    ctx, res = reply(st, ta, "dev", "fix the export")
    assert res == "job-opened", res
    (_, kind, pay), = ctx.sent_events
    assert kind == "job.open" and pay["message_id"] == "AAMk-alpha" and pay["notes"] == "fix the export", pay
    assert [snap(e) for e in plist(st)] == [snap(newer)] and snap(st["pending"]) == snap(newer)


def arm_stale_check_is_per_entry():
    w, st, _ = two_mails()
    ta, tb = tags(st)
    _, res = reply(st, ta, "edit", "make it shorter")
    assert res == "redrafted", res                                      # the older entry is now version 2, the newer still 1
    before = snap(st)
    n = len(w.texts)
    _, res = reply(st, ta, "send", version=1, at=T0 + D(minutes=20))
    assert res == "unseen" and snap(st) == before, "a version-1 reply to the version-2 entry must be refused and change nothing: %s" % res
    assert "changed just before your reply" in w.texts[-1][1] and len(w.texts) == n + 1
    _, res = reply(st, tb, "send", version=1, at=T0 + D(minutes=21))
    assert res == "mail-approved" and w.texts[-1][1].startswith("#%s approved." % tb), (res, w.texts[-1][1][:60])
    pl = plist(st)
    assert [e["tag"] for e in pl] == [ta] and pl[0]["version"] == 2, [(e["tag"], e["version"]) for e in pl]
    assert snap(st["pending"]) == snap(pl[0])


def arm_untagged_goes_to_newest():
    w, st, first = two_mails()
    ta, tb = tags(st)
    _, res = reply(st, None, "send", at=T0 + D(hours=2))
    assert res == "mail-approved" and w.texts[-1][1].startswith("#%s approved." % tb), (res, w.texts[-1][1][:60])
    assert [snap(e) for e in plist(st)] == [snap(first)] and snap(st["pending"]) == snap(first)


def arm_unknown_tag_changes_nothing():
    w, st, _ = two_mails(strict=False)     # a control: it holds at the base too
    before = snap(st)
    ctx, res = reply(st, "M999", "send")
    assert res == "nothing-open" and w.texts[-1][1] == "Nothing waiting under #M999.", (res, w.texts[-1][1])
    assert snap(st) == before and ctx.sent_events == []


def arm_expiry_and_cap_on_write():
    World()

    def entry(seq, texted_at):
        return {"tag": "M%03d" % seq, "kind": "mail", "draft": "d%d" % seq, "version": 1, "incoming": "x", "chat_title": "Pat, invented-firm",
                "texted_at": iso(texted_at), "status": "texted", "work": {"is_work": False}, "internal": False, "draft_error": "", "seq": seq,
                "mail": {"id": "m%d" % seq, "sender": "Pat Invented", "firm": "invented-firm", "subject": "s", "body": "b"}}
    old = entry(1, T0 - D(days=8))
    fresh = [entry(2 + i, T0 - D(hours=22 - i)) for i in range(22)]           # seq 2..23, oldest first, all inside 7 days
    state = {"kind": "mail", "draft_seq": 30, "pending_list": [old] + fresh, "pending": fresh[-1]}
    assert ingest(state, mail_message("AAMk-new", "newest"), T0) == "texted"
    seqs = [e["seq"] for e in plist(state)]
    assert seqs == list(range(5, 24)) + [31], "want the newest 20 (seq 5..23 and 31), the 8-day-old entry gone: %s" % seqs
    assert state["pending"]["seq"] == 31 and snap(state["pending"]) == snap(plist(state)[-1])


def arm_single_mail_as_before():
    w = World()
    state = {}
    assert ingest(state, mail_message("AAMk-alpha", "alpha"), T0) == "texted"
    p = state["pending"]
    assert p["version"] == 1 and p["seq"] == 1 and p["kind"] == "mail" and state["kind"] == "mail" and state["draft_seq"] == 1
    assert [snap(e) for e in plist(state)] == [snap(p)], "pending_list is not exactly [pending] for one mail"
    assert len(w.texts) == 1 and w.texts[0][1].startswith("#%s Mail - Pat Invented, invented-firm" % p["tag"]) and "Draft: Reply for alpha" in w.texts[0][1]
    _, res = reply(state, p["tag"], "send")
    assert res == "mail-approved" and state["pending"] is None and plist(state) == [], (res, state.get("pending"), plist(state))
    _, res = reply(state, p["tag"], "send")
    assert res == "nothing-open", res


def arm_legacy_object():
    World()
    state = {}
    ingest(state, mail_message("AAMk-alpha", "alpha"), T0)
    legacy = {k: copy.deepcopy(v) for k, v in state.items() if k != "pending_list"}      # an object written before this cell: pending only
    tag = legacy["pending"]["tag"]
    work = copy.deepcopy(legacy)
    _, res = reply(work, tag, "send")
    assert res == "mail-approved" and work["pending"] is None and plist(work) == [], "a legacy object no longer takes its reply: %s" % res
    grown = copy.deepcopy(legacy)
    assert ingest(grown, mail_message("AAMk-beta", "beta"), T0 + D(seconds=60)) == "texted"
    pl = plist(grown)
    assert len(pl) == 2 and snap(pl[0]) == snap(legacy["pending"]), "the legacy pending was not kept as an entry beside the new mail"
    assert snap(grown["pending"]) == snap(pl[1]) and pl[1]["seq"] == 2


def arm_tag_unique_among_open():
    """Two considered mails whose tags hash alike must not leave two open entries with one tag (a reply would name both)."""
    def tag_at_salt0(key):
        return int(hashlib.sha256(("0:%s" % key).encode("utf-8")).hexdigest()[:8], 16) % 1000
    seen, pair = {}, None
    for i in range(5000):
        key = "AAMk-collide-%d" % i
        n = tag_at_salt0(key)
        if n in seen:
            pair = (seen[n], key)
            break
        seen[n] = key
    assert pair, "no colliding pair found"
    World()
    state = {}
    ingest(state, mail_message(pair[0], "one"), T0)
    ingest(state, mail_message(pair[1], "two"), T0 + D(seconds=60))
    got = tags(state)
    assert len(got) == 2 and got[0] != got[1], "two open entries share a tag: %s" % got
    _, res = reply(state, got[0], "drop")
    assert res == "dropped" and [e["mail"]["id"] for e in plist(state)] == [pair[1]], res


def arm_reader_rows():
    spec = importlib.util.spec_from_file_location("refresh_under_check", os.path.join(ROOT, "data", "transcripts", "scripts", "muse_reader", "refresh.py"))
    R = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R)
    rows = []

    def fake_aws(args):
        if args[:2] == ["dynamodb", "scan"]:
            return json.dumps({"Items": rows, "ScannedCount": len(rows)})
        raise R.AwsError("unexpected call %s" % args[:2])
    R.aws_json = fake_aws

    def row(pk, state):
        return {"pk": {"S": pk}, "sk": {"S": "state"}, "data": {"S": json.dumps(state)}}

    def p(tag, seq, kind="mail", draft=None, version=1):
        return {"tag": tag, "kind": kind, "version": version, "seq": seq, "status": "texted", "texted_at": "2026-10-14T19:50:00Z",
                "draft": draft or "draft %s" % tag, "chat_title": "Pat, invented-firm"}
    a1, b1, c1, e1 = p("M101", 1), p("M102", 2), p("M103", 3), p("M104", 4)
    rows[:] = [row(OBJ, {"kind": "mail", "pending_list": [a1, b1], "pending": b1}),
               row("19:chat@unq.gbl.spaces", {"title": "t", "pending": p("C201", 9, kind="chat")}),
               row("mail:legacy", {"kind": "mail", "pending": c1}),
               row("mail:one", {"kind": "mail", "pending_list": [e1], "pending": e1}),
               row("mail:empty", {"kind": "mail", "pending_list": [], "pending": None}),
               row("#index#sms-tag", {"x": 1})]
    items = quiet(R.make_readers(datetime.datetime(2026, 10, 14, 20, 0, tzinfo=UTC))["drafts"])
    got = sorted((i["object_id"], i["tag"], i["seq"]) for i in items)
    want = sorted([(OBJ, "M101", 1), (OBJ, "M102", 2), ("19:chat@unq.gbl.spaces", "C201", 9), ("mail:legacy", "M103", 3), ("mail:one", "M104", 4)])
    assert got == want, "rows %s, want %s" % (got, want)
    keysets = {frozenset(i) for i in items}
    assert len(keysets) == 1, "the rows do not all carry the same keys: %s" % [sorted(k) for k in keysets]
    two = [i for i in items if i["object_id"] == OBJ]
    assert len({i["seq"] for i in two}) == 2 and {i["draft"] for i in two} == {"draft M101", "draft M102"}


def arm_muse_answer_binds_to_the_tagged_entry():
    """A signed muse answer names a tag AND a seq; with two open mails it reaches the entry that tag and seq name, not only the newest."""
    from data.transcripts.scripts.teams_chat import muse_verify
    muse_verify.verify = lambda pub, ns, data, sig: (True, "")
    w, st, _ = two_mails()
    ea, eb = plist(st)

    def answer(tag, seq, action="send", at=T0 + D(hours=1)):
        text = json.dumps({"tag": tag, "action": action, "notes": "", "version": 1, "seq": seq, "signed_at": iso(at - D(minutes=1))})
        ctx = Ctx("muse.reply", {"answer": {"payload": text, "signature": "sig"}}, st, at)
        return quiet(t.on_muse_reply, ctx)
    before = snap(plist(st))
    assert answer(eb["tag"], ea["seq"]) == "muse-refused" and snap(plist(st)) == before, "an answer naming the newer tag with the older seq must be refused"
    res = answer(ea["tag"], ea["seq"])
    assert res == "mail-approved", "a signed answer for the OLDER mail (its own tag and seq) was not acted on: %s" % res
    assert w.texts[-1][1].startswith("#%s approved." % ea["tag"]) and [snap(e) for e in plist(st)] == [snap(eb)] and snap(st["pending"]) == snap(eb)


def arm_open_items_lists_each_draft():
    """The natural-language path lists everything waiting on him by the sms-tag index; each open mail draft is listed, not only the newest."""
    w, st, _ = two_mails()
    ea, eb = plist(st)
    legacy = {"kind": "mail", "pending": dict(eb, tag="M777", seq=1, draft="legacy draft")}
    states = {OBJ: st, "mail:legacy": legacy}
    index_rows = [{"sk": {"S": ea["tag"]}, "object_id": {"S": OBJ}}, {"sk": {"S": eb["tag"]}, "object_id": {"S": OBJ}},
                  {"sk": {"S": "M777"}, "object_id": {"S": "mail:legacy"}}]

    class DDB:
        def query(self, **kw):
            return {"Items": index_rows}

    class RT:
        table = "t"

        def client(self, name):
            return DDB()

        def load(self, oid):
            return copy.deepcopy(states[oid]), None
    t.ldo.runtime = lambda: RT()
    items = t.open_items()
    got = sorted((i["tag"], i["draft"]) for i in items)
    want = sorted([(ea["tag"], "Reply for alpha"), (eb["tag"], "Reply for beta"), ("M777", "legacy draft")])
    assert got == want, "open_items lists %s, want %s" % (got, want)


ARMS = [arm_two_mails_both_kept, arm_approve_older_leaves_newer, arm_drop_newer_leaves_older, arm_redraft_older_only, arm_dev_one_removes_only_it,
        arm_stale_check_is_per_entry, arm_untagged_goes_to_newest, arm_unknown_tag_changes_nothing, arm_expiry_and_cap_on_write,
        arm_single_mail_as_before, arm_legacy_object, arm_tag_unique_among_open, arm_muse_answer_binds_to_the_tagged_entry,
        arm_open_items_lists_each_draft, arm_reader_rows]


def main():
    passed = 0
    for mod, name in ((mr, "mail_requests"), (t, "tenant")):          # the instrument rule: the code under test is the cwd checkout's
        if not os.path.normcase(os.path.abspath(mod.__file__)).startswith(os.path.normcase(ROOT)):
            print("FAIL instrument: %s imported from %s, outside the checkout under test %s" % (name, mod.__file__, ROOT))
            print("L1-PENDING ok=False arms=0 of %d" % len(ARMS))
            return 1
    for fn in ARMS:
        try:
            fn()
            passed += 1
        except Exception as exc:  # noqa: BLE001 -- an arm that raises is a failed arm
            print("FAIL %s: %s: %s" % (fn.__name__[4:], type(exc).__name__, str(exc)[:240]))
    print("L1-PENDING ok=%s arms=%d of %d" % (passed == len(ARMS), passed, len(ARMS)))
    return 0 if passed == len(ARMS) else 1


if __name__ == "__main__":
    sys.exit(main())
