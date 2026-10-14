"""CA-j-12: the assistant keeps two small metadata-only records for the dell2 folder (CTO ruling on call 608c, RULING_20261014_124xZ_COMM_ASSIST_608C_FWD13_TWO_SCRUBBED_RECORDS.md).

Prints:  K1-RECORDS ok=<True|False> arms=<n> of 8 failed=<names|none> reason=<text>
Contract (fixed by the issuer; the reader check pins the other half):
  teams_chat/channel_mentions.on_channel_mention(ctx), WHERE AND ONLY WHEN it texts the mention (the same condition as the text), appends to ctx.state["mentions"] one entry
    {"id": "<team id>|<channel id>|<message id>", "team": <team display name>, "channel": <channel display name>, "from": <sender display name>,
     "snippet": <the message text, tags stripped, whitespace collapsed, links, addresses and tokens removed, at most 120 characters>,
     "mentioned_at": <the message's own `created`>, "seen_at": <iso of ctx.now()>}
    and nothing else. A repeat of the same id (a retry) adds no second entry. On every write entries whose seen_at is older than 7 days are dropped and the newest 50 are kept.
  teams_chat/mail_requests.on_mail_messages(ctx), for each CONSIDERED mail, appends to ctx.state["mail_log"] one entry
    {"seq": <the draft's seq>, "tag": <its tag>, "considered_at": <iso of ctx.now()>, "from": <sender display name>, "domain": <the sender address's domain, lowercase>,
     "firm": <the firm or "firm">, "subject": <scrubbed as the snippet, at most 120 characters>}
    and nothing else: never the body, never an address. On every write entries older than 7 days are dropped and the newest 10 are kept. A mail that is not considered adds none.
No AWS, no network.
"""
import contextlib
import copy
import datetime
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "infra" / "aws" / "terraform" / "modules" / "ldo" / "runtime"))
sys.path.insert(0, str(ROOT / "data" / "transcripts" / "scripts" / "tests"))
MENTION_KEYS = {"id", "team", "channel", "from", "snippet", "mentioned_at", "seen_at"}
MAIL_KEYS = {"seq", "tag", "considered_at", "from", "domain", "firm", "subject"}
TOKEN = re.compile(r"[A-Za-z0-9+/_=-]{20,}")


def main():
    failed, why = [], ""
    try:
        import test_inbound_channel_mentions as TM
        import test_inbound_mail_draft as TD
        from data.transcripts.scripts.teams_chat import assist as a
        from data.transcripts.scripts.teams_chat import channel_mentions as cm
        from data.transcripts.scripts.teams_chat import mail_requests as mr
        D = datetime.timedelta
        NOW = TM.T0

        class MCtx:
            def __init__(self, payload, state=None, once_store=None, now=NOW):
                self.payload, self.state, self._now = payload, state if state is not None else {}, now
                self.once_store = once_store if once_store is not None else {}

            def now(self):
                return self._now

            def once(self, key, fn):
                if key not in self.once_store:
                    self.once_store[key] = fn()
                return self.once_store[key]

        BODY = ("<p>Andrew, please see <a href='https://x.example/p?token=abc'>https://x.example/p?token=abc</a> and key "
                "AKIAIOSFODNN7EXAMPLE or 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 mail me at pat@example-fund.test " + "word " * 60 + "</p>")

        def payload(mid="p1", body=BODY):
            return {"team": {"id": "t1", "display_name": "Team One"}, "channel": {"id": "c1", "display_name": "Chan One"},
                    "message": TM.msg(mid, TM.NEW, mentions=[TM.ME], body=body)}

        def arm(name, fn):
            try:
                if not fn():
                    failed.append(name)
            except Exception as exc:
                failed.append("%s(%s: %s)" % (name, type(exc).__name__, str(exc)[:70]))

        def mention_record():
            TM.World()
            ctx = MCtx(payload())
            cm.on_channel_mention(ctx)
            rows = ctx.state.get("mentions") or []
            if len(rows) != 1 or set(rows[0]) != MENTION_KEYS:
                return False
            r = rows[0]
            sn = r["snippet"]
            return (r["id"] == "t1|c1|p1" and r["team"] == "Team One" and r["channel"] == "Chan One" and r["from"] == "Sender One"
                    and r["mentioned_at"] == TM.NEW and r["seen_at"] == a.iso(NOW) and 0 < len(sn) <= 120
                    and "http" not in sn and "<" not in sn and "@" not in sn and not TOKEN.search(sn) and "AKIA" not in sn)

        def mention_retry_once():
            w = TM.World()
            ctx = MCtx(payload())
            cm.on_channel_mention(ctx)
            ctx2 = MCtx(payload(), state=ctx.state, once_store=ctx.once_store)
            res = cm.on_channel_mention(ctx2)
            ctx3 = MCtx(payload("p2"), state=ctx.state, once_store=ctx.once_store)
            cm.on_channel_mention(ctx3)
            return res == "texted" and len(w.texts) == 2 and [x["id"] for x in ctx.state["mentions"]] == ["t1|c1|p1", "t1|c1|p2"]

        def mention_expiry_cap():
            TM.World()
            old = {"id": "t0|c0|old", "team": "T", "channel": "C", "from": "F", "snippet": "s", "mentioned_at": "2026-09-30T00:00:00Z",
                   "seen_at": a.iso(NOW - D(days=8))}
            fresh = [dict(old, id="t0|c0|n%d" % i, seen_at=a.iso(NOW - D(hours=i + 1)), mentioned_at=a.iso(NOW - D(hours=i + 1))) for i in range(60)]
            ctx = MCtx(payload("pnew"), state={"mentions": [old] + fresh})
            cm.on_channel_mention(ctx)
            ids = [x["id"] for x in ctx.state["mentions"]]
            return "t0|c0|old" not in ids and len(ids) == 50 and ids[-1] == "t1|c1|pnew"

        def mention_paused_writes_nothing():
            w = TM.World()
            w.on = False
            ctx = MCtx(payload())
            res = cm.on_channel_mention(ctx)
            return res == "paused" and not ctx.state.get("mentions") and not w.texts

        def run_mail(world, messages, state=None, once=None, now=TD.NOW):
            ctx = TD.Ctx(list(messages), state=state, once_store=once)
            ctx.now = lambda: now
            with contextlib.redirect_stdout(io.StringIO()):
                res = mr.on_mail_messages(ctx)
            return ctx, res

        def mail_record():
            world = TD.World()
            ctx, _ = run_mail(world, [TD.mail(subject="Following up https://x.example/q?k=1 AKIAIOSFODNN7EXAMPLE", mid="m1")])
            rows = ctx.state.get("mail_log") or []
            if len(rows) != 1 or set(rows[0]) != MAIL_KEYS:
                return False
            r, p = rows[0], ctx.state["pending"]
            return (r["seq"] == p["seq"] and r["tag"] == p["tag"] and r["considered_at"] == a.iso(TD.NOW) and r["from"] == "Pat Invented"
                    and r["domain"] == "example-fund.test" and r["firm"] == p["mail"]["firm"] and 0 < len(r["subject"]) <= 120
                    and "http" not in r["subject"] and "AKIA" not in r["subject"])

        def mail_two_rows():
            world = TD.World()
            ctx, _ = run_mail(world, [TD.mail(mid="m1"), TD.mail(mid="m2", subject="second")])
            rows = ctx.state.get("mail_log") or []
            return [r["seq"] for r in rows] == [1, 2] and ctx.state["pending"]["seq"] == 2 and rows[1]["subject"] == "second"

        def mail_expiry_cap():
            world = TD.World()
            old = {"seq": 1, "tag": "M001", "considered_at": a.iso(TD.NOW - D(days=8)), "from": "F", "domain": "d.test", "firm": "f", "subject": "s"}
            fresh = [dict(old, seq=i + 2, tag="M%03d" % (i + 2), considered_at=a.iso(TD.NOW - D(hours=i + 1))) for i in range(12)]
            state = {"mail_log": [old] + fresh, "draft_seq": 13}
            ctx, _ = run_mail(world, [TD.mail(mid="mnew")], state=state)
            seqs = [r["seq"] for r in ctx.state["mail_log"]]
            return 1 not in seqs and len(seqs) == 10 and seqs[-1] == 14

        def mail_no_body_no_address():
            world = TD.World()
            ctx, _ = run_mail(world, [TD.mail(mid="m1", body="<p>Andrew, SECRETBODYPHRASE about the Q3 numbers</p>"),
                                      TD.mail(mid="m2", addr="x@house-one.test", body="<p>no name here at all</p>")])
            blob = json.dumps(ctx.state.get("mail_log"))
            return "SECRETBODYPHRASE" not in blob and "Q3 numbers" not in blob and "@" not in blob and len(ctx.state["mail_log"]) == 1

        for name, fn in (("mention-record", mention_record), ("mention-retry-once", mention_retry_once), ("mention-expiry-cap", mention_expiry_cap),
                         ("mention-paused-writes-nothing", mention_paused_writes_nothing), ("mail-record", mail_record), ("mail-two-rows", mail_two_rows),
                         ("mail-expiry-cap", mail_expiry_cap), ("mail-no-body-no-address", mail_no_body_no_address)):
            arm(name, fn)
        _ = (cm, copy)
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
        failed.append("harness")
    print("K1-RECORDS ok=%s arms=%d of 8 failed=%s reason=%s" % (not failed, 0 if "harness" in failed else 8 - len(failed), ";".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
