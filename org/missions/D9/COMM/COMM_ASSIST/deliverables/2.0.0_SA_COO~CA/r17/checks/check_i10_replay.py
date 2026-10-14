"""CA-i-10: a SIGNED muse answer cannot be replayed against a later draft: it must carry the draft's version and seq, and a signature already acted on is refused.

Prints:  I10-REPLAY ok=<True|False> arms=<n> of 6 failed=<names|none> reason=<text>
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

            def answer(state, **over):
                p = state["pending"]
                body = {"tag": p["tag"], "action": "send", "notes": "", "version": p["version"], "seq": p.get("seq"), "signed_at": a.iso(T.NOW - datetime.timedelta(minutes=1))}
                body.update(over)
                body = {k: v for k, v in body.items() if v is not _MISSING}
                text = json.dumps(body, sort_keys=True)
                return {"payload": text, "signature": sign(d, muse_key, text)}

            def event(state, ans):
                return Ctx(CHAT["chat_id"], "muse.reply", {"answer": ans}, state=state, sent_at=a.iso(T.NOW + datetime.timedelta(minutes=30)))

            def reason(state):
                return (state.get("muse_refusals") or [{}])[-1].get("reason")

            def arm(name, fn):
                try:
                    with pytest.MonkeyPatch.context() as mp:
                        if not fn(mp):
                            failed.append(name)
                except Exception as exc:
                    failed.append("%s(%s: %s)" % (name, type(exc).__name__, str(exc)[:60]))

            def good_acts_once(mp):
                f, st = fresh(mp)
                ans = answer(st)
                return t.on_muse_reply(event(st, ans)) == "sent" and len(f.sent) == 1

            def replay_same_bytes_refused(mp):
                f, st = fresh(mp)
                ans = answer(st)
                t.on_muse_reply(event(st, ans))
                before = (len(f.sent), dict(st))
                res = t.on_muse_reply(event(st, ans))
                return res == "muse-refused" and reason(st) == "replayed" and len(f.sent) == before[0]

            def old_signature_vs_new_draft_under_same_tag(mp):
                f, st = fresh(mp)
                old = answer(st)
                t.on_muse_reply(event(st, old))                        # the first draft is sent
                again = Ctx(CHAT["chat_id"], "teams.messages", {"chat": CHAT, "messages": [msg(5, body="<p>new question?</p>")]}, state=st)
                t.on_chat_messages(again)                               # a NEW draft under the same tag, version 1, a new seq
                if not st.get("pending") or st["pending"]["version"] != 1:
                    return False
                sent_before, pending_before = len(f.sent), dict(st["pending"])
                res = t.on_muse_reply(event(st, old))
                return res == "muse-refused" and len(f.sent) == sent_before and st["pending"] == pending_before

            def missing_version_refused(mp):
                f, st = fresh(mp)
                res = t.on_muse_reply(event(st, answer(st, version=_MISSING)))
                return res == "muse-refused" and reason(st) == "bad-payload" and f.sent == []

            def missing_seq_against_a_seq_draft_refused(mp):
                f, st = fresh(mp)
                if not st["pending"].get("seq"):
                    return False
                res = t.on_muse_reply(event(st, answer(st, seq=_MISSING)))
                return res == "muse-refused" and reason(st) == "seq-mismatch" and f.sent == []

            def draft_without_seq_still_works(mp):
                f, st = fresh(mp)
                st["pending"].pop("seq", None)                          # a pending that carries no seq (a job or End of Day draft, or one made before seq existed)
                res = t.on_muse_reply(event(st, answer(st, seq=_MISSING)))
                return res == "sent" and len(f.sent) == 1

            for name, fn in (("good-acts-once", good_acts_once), ("same-bytes-replay-refused", replay_same_bytes_refused),
                             ("old-signature-vs-new-draft", old_signature_vs_new_draft_under_same_tag), ("missing-version-refused", missing_version_refused),
                             ("missing-seq-refused", missing_seq_against_a_seq_draft_refused), ("seqless-draft-control", draft_without_seq_still_works)):
                arm(name, fn)
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
        failed.append("harness")
    print("I10-REPLAY ok=%s arms=%d of 6 failed=%s reason=%s" % (not failed, 0 if "harness" in failed else 6 - len(failed), ";".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
