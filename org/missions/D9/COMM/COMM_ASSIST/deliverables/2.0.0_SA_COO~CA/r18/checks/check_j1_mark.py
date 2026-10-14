"""CA-j-1: every event the assistant itself produces for Andrew's texts carries a mark only the assistant can make, and the handler refuses (or records) an unmarked one.

Prints:  J1-MARK ok=<True|False> arms=<n> of 9 failed=<names|none> reason=<text>
Contract (fixed by the issuer): module data/transcripts/scripts/teams_chat/ingress_mark.py with
    stamp(secret, object_id, kind, payload, now) -> a COPY of payload plus "mark_at" (UTC ISO, from `now`) and "mark" (hex HMAC-SHA256 over object_id, kind, mark_at and the
    canonical JSON of the payload without "mark"); verify(secret, object_id, kind, payload, now) -> "ok" | "no-mark" | "bad-mark" | "stale-mark" (mark_at older than 15 minutes or more than
    5 minutes ahead of `now`).
The kinds marked are sms.reply and owner.text. tenant.dispatch reads env INGRESS_MARK_MODE at call time: unset or "off" = no check; "record" = check, record a failure in
state["mark_refusals"] (last 50) and count it in state["unmarked_seen"], but ACT; "enforce" = check, record, and refuse (return "unmarked-refused", act on nothing, send nothing). A mark already seen
(state["marks_seen"], last 100) is "replayed-mark" and is refused in enforce mode. The secret is a.secret(a.NAMES["secrets"]["ingress_mark"]); a.NAMES carries that row.
The producers are found by reading the source: every `.send(object_id, "sms.reply"|"owner.text", payload ...)` in tenant.py passes its payload through a call named stamp.
No AWS, no network.
"""
import ast
import datetime
import importlib.util
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "infra" / "aws" / "terraform" / "modules" / "ldo" / "runtime"))
SECRET = "TEST-INGRESS-SECRET"
MARKED = ("sms.reply", "owner.text")


def load_harness():
    spec = importlib.util.spec_from_file_location("tenant_harness", ROOT / "data/transcripts/scripts/tests/test_teams_chat_tenant.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def producers_stamp(src):
    """(sites, unstamped): every .send(...) whose second argument is a marked kind; the unstamped are those whose third argument is not a call named *stamp*."""
    tree = ast.parse(src)
    sites, bad = 0, []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "send" and len(node.args) >= 3:
            kind = node.args[1]
            if isinstance(kind, ast.Constant) and kind.value in MARKED:
                sites += 1
                p = node.args[2]
                name = p.func.attr if isinstance(p, ast.Call) and isinstance(p.func, ast.Attribute) else (p.func.id if isinstance(p, ast.Call) and isinstance(p.func, ast.Name) else "")
                if "stamp" not in name:
                    bad.append(node.lineno)
    return sites, bad


def main():
    failed, why = [], ""
    try:
        T = load_harness()
        t, a, Ctx, Fakes, CHAT, msg = T.t, T.a, T.Ctx, T.Fakes, T.CHAT, T.msg
        import pytest
        from data.transcripts.scripts.teams_chat import ingress_mark as im
        NOW = T.NOW

        def arm(name, fn):
            try:
                with pytest.MonkeyPatch.context() as mp:
                    mp.setattr(a, "secret", lambda name_: SECRET if name_ == a.NAMES["secrets"]["ingress_mark"] else "+15550001111")
                    if not fn(mp):
                        failed.append(name)
            except Exception as exc:
                failed.append("%s(%s: %s)" % (name, type(exc).__name__, str(exc)[:60]))

        def fresh(mp, mode):
            f = Fakes(mp)
            if mode is None:
                mp.delenv("INGRESS_MARK_MODE", raising=False)
            else:
                mp.setenv("INGRESS_MARK_MODE", mode)
            ctx = Ctx(CHAT["chat_id"], "teams.messages", {"chat": CHAT, "messages": [msg(1)]})
            t.on_chat_messages(ctx)
            return f, ctx.state

        def reply(state, payload, kind="sms.reply"):
            return Ctx(CHAT["chat_id"], kind, payload, state=state, sent_at=a.iso(NOW + datetime.timedelta(minutes=2)))

        def marked(payload, at=NOW):
            return im.stamp(SECRET, CHAT["chat_id"], "sms.reply", payload, at)

        def reason(state):
            return (state.get("mark_refusals") or [{}])[-1].get("reason")

        def producers_mark_ingress(mp):
            f, st = fresh(mp, "enforce")
            mp.setattr(t.ldo, "lookup", lambda ns, key: CHAT["chat_id"] if key else None)
            mp.setattr(a, "now_utc", lambda: NOW)
            res = t.route_text({"originationNumber": "+15550001111", "messageBody": "C042 #1", "inboundMessageId": "in9"})
            oid, kind, payload, _eid = f.ldo_sent[-1]
            return res == "routed" and kind == "sms.reply" and im.verify(SECRET, oid, kind, payload, NOW) == "ok"

        def producers_mark_natural(mp):
            f, st = fresh(mp, "enforce")
            mp.setattr(a, "now_utc", lambda: NOW)
            t.route_text({"originationNumber": "+15550001111", "messageBody": "shorter please", "inboundMessageId": "in10"})
            oid, kind, payload, _eid = f.ldo_sent[-1]
            return kind == "owner.text" and im.verify(SECRET, oid, kind, payload, NOW) == "ok"

        def every_producer_site_stamps(mp):
            sites, bad = producers_stamp((ROOT / "data/transcripts/scripts/teams_chat/tenant.py").read_text(encoding="utf-8"))
            return sites >= 4 and not bad

        def enforce_marked_acts(mp):
            f, st = fresh(mp, "enforce")
            res = t.dispatch(reply(st, marked({"tag": None, "action": "send", "notes": ""})))
            return res == "sent" and len(f.sent) == 1

        def enforce_unmarked_refused(mp):
            f, st = fresh(mp, "enforce")
            before = dict(st["pending"])
            res = t.dispatch(reply(st, {"tag": None, "action": "send", "notes": ""}))
            return res == "unmarked-refused" and f.sent == [] and st["pending"] == before and reason(st) == "no-mark"

        def enforce_tampered_refused(mp):
            f, st = fresh(mp, "enforce")
            p = marked({"tag": None, "action": "drop", "notes": ""})
            p["action"] = "send"
            res = t.dispatch(reply(st, p))
            return res == "unmarked-refused" and f.sent == [] and reason(st) == "bad-mark"

        def enforce_stale_and_replayed_refused(mp):
            f, st = fresh(mp, "enforce")
            old = marked({"tag": None, "action": "edit", "notes": "x"}, NOW - datetime.timedelta(minutes=20))
            r1 = t.dispatch(reply(st, old))
            r1_reason = reason(st)
            ok1 = marked({"tag": None, "action": "none", "notes": ""})
            t.dispatch(reply(st, ok1))
            r3 = t.dispatch(reply(st, ok1))      # the same mark again
            return r1 == "unmarked-refused" and r1_reason == "stale-mark" and r3 == "unmarked-refused" and reason(st) == "replayed-mark"

        def record_mode_acts_and_counts(mp):
            f, st = fresh(mp, "record")
            res = t.dispatch(reply(st, {"tag": None, "action": "send", "notes": ""}))
            return res == "sent" and len(f.sent) == 1 and st.get("unmarked_seen") == 1 and reason(st) == "no-mark"

        def off_mode_unchanged(mp):
            f, st = fresh(mp, None)
            res = t.dispatch(reply(st, {"tag": None, "action": "send", "notes": ""}))
            return res == "sent" and len(f.sent) == 1 and not st.get("mark_refusals") and not st.get("unmarked_seen")

        for name, fn in (("ingress-sms-reply-marked", producers_mark_ingress), ("ingress-owner-text-marked", producers_mark_natural),
                         ("every-producer-site-stamps", every_producer_site_stamps), ("enforce-marked-acts", enforce_marked_acts),
                         ("enforce-unmarked-refused", enforce_unmarked_refused), ("enforce-tampered-refused", enforce_tampered_refused),
                         ("enforce-stale-and-replayed-refused", enforce_stale_and_replayed_refused),
                         ("record-mode-acts-and-counts", record_mode_acts_and_counts), ("off-mode-unchanged", off_mode_unchanged)):
            arm(name, fn)
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
        failed.append("harness")
    print("J1-MARK ok=%s arms=%d of 9 failed=%s reason=%s" % (not failed, 0 if "harness" in failed else 9 - len(failed), ";".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
