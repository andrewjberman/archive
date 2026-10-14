"""CA-i-13: a SIGNED muse answer is only good for a bounded time: its signed_at must lie within 24 hours before, and no more than 5 minutes after, the receiver's own clock.

Prints:  I13-FRESH ok=<True|False> arms=<n> of 6 failed=<names|none> reason=<text>
Uses a real `ssh-keygen -Y sign` (two throwaway keys: muse, and a forger) so the verifier is graded against the real SSHSIG format.
The tenant is imported from the repository root this script is run in, with the existing test harness (Ctx, Fakes) doing the outside-world fakes.
No AWS, no network. Exits 0 whatever the verdict.
"""
import datetime
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
NS = "muse-answer@opal"
_MISSING = object()
_SEQ = [0]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "infra" / "aws" / "terraform" / "modules" / "ldo" / "runtime"))


def load_harness():
    spec = importlib.util.spec_from_file_location("tenant_harness", ROOT / "data/transcripts/scripts/tests/test_teams_chat_tenant.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def keygen(d, name):
    k = Path(d) / name
    subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-C", name, "-f", str(k)], check=True, capture_output=True, timeout=60)
    pub = (Path(str(k) + ".pub")).read_text(encoding="ascii").split()
    return k, "%s %s" % (pub[0], pub[1])


def sign(d, key, payload_text, namespace=NS):
    _SEQ[0] += 1
    f = Path(d) / ("p%d.json" % _SEQ[0])
    f.write_bytes(payload_text.encode("utf-8"))
    subprocess.run(["ssh-keygen", "-q", "-Y", "sign", "-f", str(key), "-n", namespace, str(f)], check=True, capture_output=True, timeout=60)
    return Path(str(f) + ".sig").read_text(encoding="ascii")


def main():
    failed, why = [], ""
    try:
        T = load_harness()
        t, a, Ctx, Fakes, CHAT, msg = T.t, T.a, T.Ctx, T.Fakes, T.CHAT, T.msg
        import pytest
        with tempfile.TemporaryDirectory() as d:
            muse_key, muse_pub = keygen(d, "muse")

            def fresh(mp):
                f = Fakes(mp)
                mp.setenv("MUSE_ANSWER_PUBKEY", muse_pub)
                ctx = Ctx(CHAT["chat_id"], "teams.messages", {"chat": CHAT, "messages": [msg(1)]})
                t.on_chat_messages(ctx)
                return f, ctx.state

            def answer(state, signed_at):
                p = state["pending"]
                body = {"tag": p["tag"], "action": "send", "notes": "", "version": p["version"], "seq": p.get("seq")}
                if signed_at is not _MISSING:
                    body["signed_at"] = signed_at
                text = json.dumps(body, sort_keys=True)
                return {"payload": text, "signature": sign(d, muse_key, text)}

            def event(state, ans):
                return Ctx(CHAT["chat_id"], "muse.reply", {"answer": ans}, state=state, sent_at=a.iso(T.NOW))

            def reason(state):
                return (state.get("muse_refusals") or [{}])[-1].get("reason")

            def at(delta):
                return a.iso(T.NOW + delta)

            def arm(name, fn):
                try:
                    with pytest.MonkeyPatch.context() as mp:
                        if not fn(mp):
                            failed.append(name)
                except Exception as exc:
                    failed.append("%s(%s: %s)" % (name, type(exc).__name__, str(exc)[:60]))

            def acts(signed_at):
                def run(mp):
                    f, st = fresh(mp)
                    return t.on_muse_reply(event(st, answer(st, signed_at))) == "sent" and len(f.sent) == 1
                return run

            def refused(signed_at, why_):
                def run(mp):
                    f, st = fresh(mp)
                    before = dict(st["pending"])
                    res = t.on_muse_reply(event(st, answer(st, signed_at)))
                    return res == "muse-refused" and reason(st) == why_ and f.sent == [] and st["pending"] == before
                return run

            H = datetime.timedelta
            for name, fn in (("one-hour-old-acts", acts(at(-H(hours=1)))), ("just-inside-24h-acts", acts(at(-H(hours=23, minutes=59)))),
                             ("25h-old-refused", refused(at(-H(hours=25)), "stale-signature")), ("ten-minutes-future-refused", refused(at(H(minutes=10)), "stale-signature")),
                             ("missing-signed-at-refused", refused(_MISSING, "bad-payload")), ("unparsable-signed-at-refused", refused("yesterday-ish", "bad-payload"))):
                arm(name, fn)
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
        failed.append("harness")
    print("I13-FRESH ok=%s arms=%d of 6 failed=%s reason=%s" % (not failed, 0 if "harness" in failed else 6 - len(failed), ";".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
