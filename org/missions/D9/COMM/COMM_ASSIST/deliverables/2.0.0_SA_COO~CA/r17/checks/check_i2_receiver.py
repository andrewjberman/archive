"""CA-i-2: the assistant's RECEIVER verifies muse's signature; every other answer is refused and recorded.

Prints:  I2-RECEIVER ok=<True|False> arms=<n> of 7 failed=<names|none> reason=<text>
Uses a real `ssh-keygen -Y sign` (two throwaway keys: muse, and a forger) so the verifier is graded against the real SSHSIG format.
The tenant is imported from the repository root this script is run in, with the existing test harness (Ctx, Fakes) doing the outside-world fakes.
No AWS, no network. Exits 0 whatever the verdict.
"""
import copy
import datetime
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
NS = "muse-answer@opal"
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
    f = Path(d) / ("p%d.json" % abs(hash((payload_text, str(key), namespace))))
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
            forger_key, _ = keygen(d, "forger")

            def fresh(mp, versions=1):
                f = Fakes(mp)
                mp.setenv("MUSE_ANSWER_PUBKEY", muse_pub)
                ctx = Ctx(CHAT["chat_id"], "teams.messages", {"chat": CHAT, "messages": [msg(1)]})
                t.on_chat_messages(ctx)
                if versions == 2:
                    edit = Ctx(CHAT["chat_id"], "sms.reply", {"action": "edit", "notes": "say 3pm works"}, state=ctx.state,
                               sent_at=a.iso(T.NOW + datetime.timedelta(minutes=2)))
                    t.on_sms_reply(edit)
                return f, ctx.state

            def event(state, answer, kind="muse.reply"):
                payload = {"answer": answer} if answer is not None else {"tag": state["pending"]["tag"], "action": "send", "notes": ""}
                return Ctx(CHAT["chat_id"], kind, payload, state=state, sent_at=a.iso(T.NOW + datetime.timedelta(minutes=30)))

            def body(state, action="send", notes="", version=None):
                p = state["pending"]
                return json.dumps({"tag": p["tag"], "action": action, "notes": notes,
                                   "version": p["version"] if version is None else version, "seq": p.get("seq"),
                                   "signed_at": a.iso(T.NOW - datetime.timedelta(minutes=1))}, sort_keys=True)

            def run(name, build, expect, check):
                try:
                    with pytest.MonkeyPatch.context() as mp:
                        f, state = fresh(mp, 2 if name == "stale-edit" else 1)
                        before = copy.deepcopy(state["pending"])
                        res = t.on_muse_reply(build(state))
                        ok = res == expect and check(f, state, before)
                        if not ok:
                            failed.append("%s(got %r)" % (name, res))
                except Exception as exc:  # an arm that raises is a failed arm
                    failed.append("%s(%s: %s)" % (name, type(exc).__name__, str(exc)[:60]))

            def ans(state, key, **kw):
                text = body(state, **{k: v for k, v in kw.items() if k in ("action", "notes", "version")})
                return {"payload": text, "signature": sign(d, key, text, kw.get("namespace", NS))}

            def refusal(state):
                return (state.get("muse_refusals") or [{}])[-1]

            def untouched(f, st, before):
                return f.sent == [] and st["pending"] == before

            if "muse.reply" not in t.ROUTES:
                failed.append("route-missing")
            run("valid-send", lambda s: event(s, ans(s, muse_key)), "sent",
                lambda f, st, b: len(f.sent) == 1 and st["pending"] is None)
            run("forged-key", lambda s: event(s, ans(s, forger_key)), "muse-refused",
                lambda f, st, b: untouched(f, st, b) and refusal(st).get("reason") == "bad-signature")
            run("unsigned", lambda s: event(s, {"payload": body(s)}), "muse-refused",
                lambda f, st, b: untouched(f, st, b) and refusal(st).get("reason") == "no-signature")
            run("direct-send", lambda s: event(s, None), "muse-refused",
                lambda f, st, b: untouched(f, st, b) and refusal(st).get("reason") == "no-signature")

            def tampered(s):
                a_ = ans(s, muse_key, action="drop")
                a_["payload"] = a_["payload"].replace('"drop"', '"send"')
                return event(s, a_)
            run("tampered", tampered, "muse-refused",
                lambda f, st, b: untouched(f, st, b) and refusal(st).get("reason") == "bad-signature")
            run("wrong-namespace", lambda s: event(s, ans(s, muse_key, namespace="other@ns")), "muse-refused",
                lambda f, st, b: untouched(f, st, b) and refusal(st).get("reason") == "bad-signature")
            run("stale-edit", lambda s: event(s, ans(s, muse_key, action="edit", notes="make it shorter", version=1)), "unseen",
                lambda f, st, b: st["pending"] == b and st["pending"]["version"] == 2)
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
        failed.append("harness")
    arms = 7
    done = arms - len([x for x in failed if not x.startswith("harness") and not x.startswith("route")])
    print("I2-RECEIVER ok=%s arms=%d of %d failed=%s reason=%s" % (not failed, max(done, 0), arms, ";".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
