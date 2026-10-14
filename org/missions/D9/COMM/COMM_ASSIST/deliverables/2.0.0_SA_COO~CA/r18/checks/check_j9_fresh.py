"""CA-j-9: the ingress mark stays valid for 4 hours (the queue redelivers a failed event an hour later, twice) WITHOUT weakening replay protection.

Prints:  J9-FRESH ok=<True|False> arms=<n> of 7 failed=<names|none> reason=<text>
Contract (CTO ruling on call 847f, CTO_RULING_20261014_104xZ_COMM_ASSIST_MARK_FRESHNESS_4H.md): ingress_mark.MAX_AGE_S is 4 hours (a mark dated more than 5 minutes ahead is still stale);
state["marks_seen"] holds EVERY mark younger than MAX_AGE_S (pruned by age, never by a count cap) so a mark cannot be replayed inside the wider window; a refusal records the event's
KIND and TAG beside the reason (never the payload) so a lost text can be found and resent. The handler's modes, reasons and returns are otherwise unchanged. No AWS, no network.
Arms: edge (3h59m ok, 4h01m stale, +6m stale, +4m ok), redelivery (a first delivery 3h59m after the mark acts), replay (a replay at 3h59m is replayed-mark), nocap (150 marks in the
window, the first replayed: refused), prune (a mark older than 4h is no longer held after a later delivery), refusal-fields (kind and tag recorded, the payload's note never), regress (J1-MARK still 9 of 9).
"""
import datetime
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "infra" / "aws" / "terraform" / "modules" / "ldo" / "runtime"))
SECRET = "TEST-INGRESS-SECRET"
J1 = Path(__file__).with_name("check_j1_mark.py")
ARMS = ("edge", "redelivery", "replay", "nocap", "prune", "refusal-fields", "regress")


def load_harness():
    spec = importlib.util.spec_from_file_location("tenant_harness", ROOT / "data/transcripts/scripts/tests/test_teams_chat_tenant.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    failed, why = [], ""
    try:
        T = load_harness()
        t, a, Ctx, Fakes, CHAT, msg = T.t, T.a, T.Ctx, T.Fakes, T.CHAT, T.msg
        import pytest
        from data.transcripts.scripts.teams_chat import ingress_mark as im
        NOW = T.NOW
        H = datetime.timedelta

        def arm(name, fn):
            try:
                with pytest.MonkeyPatch.context() as mp:
                    mp.setattr(a, "secret", lambda name_: SECRET if name_ == a.NAMES["secrets"]["ingress_mark"] else "+15550001111")
                    if not fn(mp):
                        failed.append(name)
            except Exception as exc:
                failed.append("%s(%s: %s)" % (name, type(exc).__name__, str(exc)[:60]))

        def fresh(mp):
            f = Fakes(mp)
            mp.setenv("INGRESS_MARK_MODE", "enforce")
            ctx = Ctx(CHAT["chat_id"], "teams.messages", {"chat": CHAT, "messages": [msg(1)]})
            t.on_chat_messages(ctx)
            return f, ctx.state

        def marked(payload, at):
            return im.stamp(SECRET, CHAT["chat_id"], "sms.reply", payload, at)

        def deliver(state, payload, at):
            return t.dispatch(Ctx(CHAT["chat_id"], "sms.reply", payload, state=state, now=at))

        def last_reason(state):
            return (state.get("mark_refusals") or [{}])[-1].get("reason")

        def edge(mp):
            v = lambda dt: im.verify(SECRET, CHAT["chat_id"], "sms.reply", marked({"tag": None, "action": "send", "notes": ""}, NOW - dt), NOW)  # noqa: E731
            ahead = lambda dt: im.verify(SECRET, CHAT["chat_id"], "sms.reply", marked({"tag": None, "action": "send", "notes": ""}, NOW + dt), NOW)  # noqa: E731
            return (v(H(hours=3, minutes=59)) == "ok" and v(H(hours=4, minutes=1)) == "stale-mark"
                    and ahead(H(minutes=6)) == "stale-mark" and ahead(H(minutes=4)) == "ok")

        def redelivery(mp):
            f, st = fresh(mp)
            p = marked({"tag": None, "action": "send", "notes": ""}, NOW)
            res = deliver(st, p, NOW + H(hours=3, minutes=59))
            return res == "sent" and len(f.sent) == 1 and not st.get("mark_refusals")

        def replay(mp):
            f, st = fresh(mp)
            p = marked({"tag": None, "action": "send", "notes": ""}, NOW)
            deliver(st, p, NOW + H(minutes=1))
            res = deliver(st, p, NOW + H(hours=3, minutes=59))
            return res == "unmarked-refused" and last_reason(st) == "replayed-mark" and len(f.sent) == 1

        def nocap(mp):
            f, st = fresh(mp)
            first = marked({"tag": None, "action": "none", "notes": "n0"}, NOW)
            deliver(st, first, NOW + H(minutes=1))
            for i in range(1, 150):
                deliver(st, marked({"tag": None, "action": "none", "notes": "n%d" % i}, NOW + H(seconds=i)), NOW + H(minutes=2))
            res = deliver(st, first, NOW + H(hours=3))
            return res == "unmarked-refused" and last_reason(st) == "replayed-mark"

        def prune(mp):
            f, st = fresh(mp)
            deliver(st, marked({"tag": None, "action": "none", "notes": "old"}, NOW), NOW + H(minutes=1))
            before = len(st.get("marks_seen") or [])
            later = NOW + H(hours=4, minutes=10)
            deliver(st, marked({"tag": None, "action": "none", "notes": "new"}, later - H(minutes=1)), later)
            return before == 1 and len(st.get("marks_seen") or []) == 1

        def refusal_fields(mp):
            f, st = fresh(mp)
            stale = marked({"tag": "C042", "action": "edit", "notes": "SECRET-NOTE-TEXT"}, NOW - H(hours=5))
            res = deliver(st, stale, NOW)
            rec = (st.get("mark_refusals") or [{}])[-1]
            blob = json.dumps(st.get("mark_refusals"))
            return (res == "unmarked-refused" and rec.get("reason") == "stale-mark" and rec.get("kind") == "sms.reply" and rec.get("tag") == "C042"
                    and set(rec) <= {"at", "reason", "kind", "tag"} and "SECRET-NOTE-TEXT" not in blob)

        def regress(mp):
            out = subprocess.run([sys.executable, str(J1)], capture_output=True, text=True, cwd=str(ROOT), timeout=200).stdout
            return "J1-MARK ok=True arms=9 of 9" in out

        for name, fn in (("edge", edge), ("redelivery", redelivery), ("replay", replay), ("nocap", nocap), ("prune", prune),
                         ("refusal-fields", refusal_fields), ("regress", regress)):
            arm(name, fn)
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
        failed.append("harness")
    print("J9-FRESH ok=%s arms=%d of %d failed=%s reason=%s" % (not failed, 0 if "harness" in failed else len(ARMS) - len(failed), len(ARMS), ";".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
